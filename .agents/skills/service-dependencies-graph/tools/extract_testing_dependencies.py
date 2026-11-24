"""Extract explicitly selected testing dependencies without running test code.

Only imported Python clients and Robot Settings imports establish declarations.
Configuration values, credentials, call arguments, and execution are not retained.
"""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re
import warnings
from urllib.parse import urlsplit, urlunsplit

from .source_inventory import is_source_file, iter_source_files


SCOPE = 'TESTING'
METHODS = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options'}


def _id(prefix, *values):
    return prefix + ':' + hashlib.sha256('|'.join(map(str, values)).encode()).hexdigest()[:24]


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted(node.value)
        return parent + '.' + node.attr if parent else None
    return None


def _symbol(node):
    return _dotted(node) or '<dynamic expression>'


def _identity(node, environment):
    name = _dotted(node)
    if name in environment:
        return environment[name]
    if isinstance(node, ast.Attribute):
        parent = _identity(node.value, environment)
        return parent + '.' + node.attr if parent else None
    return None


def _literal(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _safe_url(node):
    """Retain an inline transport destination; strip authentication and queries."""
    value = _literal(node)
    if value is None:
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme not in {'http', 'https', ''}:
            return None
        if not parsed.scheme and not value.startswith('/'):
            return None
        authority = parsed.hostname or ''
        if parsed.scheme and not authority:
            return None
        if ':' in authority:
            authority = '[' + authority + ']'
        if parsed.port is not None:
            authority += ':' + str(parsed.port)
        # Tokens in userinfo, query strings, and fragments are never retained.
        # A path containing credential markers also remains symbolic.
        if re.search(r'(?i)(?:password|passwd|secret|token|credential|authorization)[=/]', parsed.path):
            return None
        return urlunsplit((parsed.scheme.lower(), authority, parsed.path or '/', '', ''))
    except ValueError:
        return None


def extract(repo: Path) -> dict:
    """The caller must select a testing repository explicitly before calling."""
    repo = Path(os.path.abspath(repo))
    result = {'declarations': [], 'diagnostics': [], 'ledger': [], 'files_scanned': {}}

    def add(path, line, family, declaration, **values):
        row = {'path': path.relative_to(repo).as_posix(), 'line': line,
               'family': family, 'declaration': declaration, 'dependency_scope': SCOPE, **values}
        result['declarations'].append(row)
        result['ledger'].append({**row, 'disposition': 'EXTRACTED' if not row.get('dynamic') else 'UNRESOLVED'})
        if row.get('dynamic'):
            result['diagnostics'].append({**row, 'code': 'UNRESOLVED_TEST_DEPENDENCY',
                                          'message': 'Testing dependency identity is dynamic or unavailable.'})

    def python_file(path):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', SyntaxWarning)
                tree = ast.parse(path.read_text(encoding='utf-8-sig', errors='replace'))
        except (SyntaxError, ValueError) as error:
            row = {'path': path.relative_to(repo).as_posix(), 'line': getattr(error, 'lineno', 1) or 1}
            result['diagnostics'].append({**row,
                                          'code': 'TEST_PYTHON_PARSE_ERROR',
                                          'message': 'Python source has unsupported or incomplete syntax.'})
            result['ledger'].append({**row, 'family': 'TEST_PYTHON_SOURCE', 'disposition': 'GAP',
                                      'dependency_scope': SCOPE, 'reason': 'Python source parse failed'})
            return

        def call(node, environment):
            identity = _identity(node.func, environment)
            if not identity:
                return
            parts = identity.split('.')
            owner, method = '.'.join(parts[:-1]), parts[-1]
            if owner in {'requests', 'requests.api', 'requests.Session', 'requests.sessions.Session'} and method in METHODS | {'request'}:
                url = next((kw.value for kw in node.keywords if kw.arg == 'url'), None)
                http_method = method.upper()
                if method == 'request':
                    method_node = next((kw.value for kw in node.keywords if kw.arg == 'method'), node.args[0] if node.args else None)
                    literal_method = _literal(method_node)
                    http_method = literal_method.upper() if literal_method and literal_method.lower() in METHODS else 'UNKNOWN'
                    url = url or (node.args[1] if len(node.args) > 1 else None)
                else:
                    url = url or (node.args[0] if node.args else None)
                destination = _safe_url(url)
                add(path, node.lineno, 'TEST_HTTP', f'{identity}(<arguments omitted>)',
                    client='requests', method=http_method, destination=destination,
                    destination_expression=None if destination else _symbol(url),
                    dynamic=destination is None or http_method == 'UNKNOWN')
            elif identity in {'psycopg2.connect', 'psycopg.connect'}:
                add(path, node.lineno, 'TEST_DATABASE', identity + '(<connection arguments omitted>)',
                    client=identity.rsplit('.', 1)[0], protocol='POSTGRESQL', destination=None,
                    destination_expression='<connection identity omitted>', dynamic=True)
            elif identity == 'minio.Minio':
                add(path, node.lineno, 'TEST_OBJECT_STORAGE', 'minio.Minio(<connection arguments omitted>)',
                    client='MinIO', protocol='S3', destination=None,
                    destination_expression='<connection identity omitted>', dynamic=True,
                    client_declaration_only=True)

        def expressions(node, environment):
            if node is None:
                return
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                return
            for child in ast.iter_child_nodes(node):
                expressions(child, environment)
            if isinstance(node, ast.Call):
                call(node, environment)

        def local_names(statements):
            names, globals_ = set(), set()
            def walk(node):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    names.add(node.name)
                    return
                if isinstance(node, ast.Global):
                    globals_.update(node.names)
                if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
                    names.add(node.id)
                if isinstance(node, ast.Import):
                    names.update(alias.asname or alias.name.split('.')[0] for alias in node.names)
                if isinstance(node, ast.ImportFrom):
                    names.update(alias.asname or alias.name for alias in node.names)
                for child in ast.iter_child_nodes(node):
                    walk(child)
            for statement in statements:
                walk(statement)
            return names - globals_

        def body(statements, inherited, function=None):
            environment = dict(inherited)
            if function:
                for name in local_names(statements):
                    environment.pop(name, None)
                for arg in [*function.args.posonlyargs, *function.args.args, *function.args.kwonlyargs,
                            *([function.args.vararg] if function.args.vararg else []),
                            *([function.args.kwarg] if function.args.kwarg else [])]:
                    environment.pop(arg.arg, None)
            for statement in statements:
                if isinstance(statement, ast.Import):
                    for imported in statement.names:
                        environment[imported.asname or imported.name.split('.')[0]] = imported.name if imported.asname else imported.name.split('.')[0]
                elif isinstance(statement, ast.ImportFrom):
                    for imported in statement.names:
                        if imported.name != '*':
                            environment[imported.asname or imported.name] = (statement.module or '') + '.' + imported.name
                elif isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    body(statement.body, environment, statement)
                elif isinstance(statement, ast.ClassDef):
                    class_environment = dict(environment)
                    # Only unique, unreassigned Session fields have a known type.
                    assignments = {}
                    for member in statement.body:
                        if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            for assigned in ast.walk(member):
                                if isinstance(assigned, ast.Assign):
                                    for target in assigned.targets:
                                        dotted = _dotted(target)
                                        if dotted and dotted.startswith('self.'):
                                            assignments.setdefault(dotted, []).append(assigned.value)
                    for target, values in assignments.items():
                        if len(values) == 1 and isinstance(values[0], ast.Call) and _identity(values[0].func, environment) in {'requests.Session', 'requests.sessions.Session'}:
                            class_environment[target] = 'requests.Session'
                    body(statement.body, class_environment)
                elif isinstance(statement, (ast.Assign, ast.AnnAssign)):
                    expressions(statement.value, environment)
                    targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
                    identity = (_identity(statement.value.func, environment)
                                if isinstance(statement.value, ast.Call) else None)
                    for target in targets:
                        name = _dotted(target)
                        if name:
                            environment.pop(name, None)
                            if identity in {'requests.Session', 'requests.sessions.Session'}:
                                environment[name] = identity
                elif isinstance(statement, ast.If):
                    expressions(statement.test, environment)
                    body(statement.body, environment)
                    body(statement.orelse, environment)
                    for name in local_names([statement]):
                        environment.pop(name, None)
                elif isinstance(statement, (ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)):
                    branch = dict(environment)
                    if isinstance(statement, (ast.For, ast.AsyncFor)):
                        expressions(statement.iter, environment)
                        for name in local_names([statement.target]):
                            branch.pop(name, None)
                    elif isinstance(statement, ast.While):
                        expressions(statement.test, environment)
                    elif isinstance(statement, (ast.With, ast.AsyncWith)):
                        for item in statement.items:
                            expressions(item.context_expr, environment)
                            if item.optional_vars:
                                for name in local_names([item.optional_vars]):
                                    branch.pop(name, None)
                    body(statement.body, branch)
                    body(getattr(statement, 'orelse', []), environment)
                    for handler in getattr(statement, 'handlers', []):
                        handler_environment = dict(environment)
                        handler_environment.pop(handler.name, None)
                        body(handler.body, handler_environment)
                    for name in local_names([statement]):
                        environment.pop(name, None)
                    body(getattr(statement, 'finalbody', []), environment)
                else:
                    # Nested control-flow assignments are not propagated as definite types.
                    expressions(statement, environment)
                    for node in ast.walk(statement):
                        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
                            environment.pop(node.id, None)
        body(tree.body, {})

    def robot_file(path):
        settings = False
        for line_number, raw in enumerate(path.read_text(encoding='utf-8-sig', errors='replace').splitlines(), 1):
            stripped = raw.strip()
            section = re.fullmatch(r'\*{3}\s*(.*?)\s*\*{3}', stripped)
            if section:
                settings = section.group(1).lower() in {'settings', 'setting'}
                continue
            if not settings or not stripped or stripped.startswith('#'):
                continue
            cells = re.split(r'\t+| {2,}', stripped)
            if len(cells) < 2 or cells[0].lower() not in {'library', 'resource'}:
                continue
            kind, target = cells[0].upper(), cells[1]
            dynamic = bool(re.search(r'[$@&%]\{|://', target))
            safe_target = '<dynamic Robot import>' if dynamic else target.replace('\\', '/')
            family = 'TEST_ROBOT_' + kind
            add(path, line_number, family, f'Robot {kind.title()} {safe_target}',
                import_kind=kind, target=safe_target, dynamic=dynamic)

    for path in iter_source_files(repo, suffixes={'.py', '.robot', '.resource'}):
        result['files_scanned'][path.suffix] = result['files_scanned'].get(path.suffix, 0) + 1
        python_file(path) if path.suffix == '.py' else robot_file(path)
    return result


def add_to_graph(graph, repo: Path, repository: str) -> dict:
    """Build testing declarations only when selected by the owning caller."""
    extracted = extract(repo)
    root = f'component:{repo.name}:testing-root'
    root_path = repo.relative_to(graph.workspace).as_posix()
    root_evidence = graph.add_evidence(repository, root_path, 1, 'Explicitly selected testing repository', 'testing-scope')

    def node(identity, kind, name, path, evidence, properties=None, owner=repository):
        graph.add_node(identity, kind, name, owner, dimensions=('RUNTIME',), component_kind='TESTING',
                       functional_role='Retains a testing dependency declaration',
                       business_meaning='Source declaration does not establish test execution or passing behavior',
                       source_paths=(path,) if path else (), evidence=evidence,
                       properties={'dependency_scope': SCOPE, 'execution_status': 'NOT_ESTABLISHED', **(properties or {})})
        return identity

    def edge(source, target, relationship, evidence, status=None, properties=None):
        graph.add_edge(source, target, relationship, 'RUNTIME', evidence, resolution_status=status,
                       properties={'dependency_scope': SCOPE, 'execution_status': 'NOT_ESTABLISHED', **(properties or {})})

    node(root, 'COMPONENT', repo.name + ' testing', root_path, (root_evidence,))
    files = {}
    for declaration in extracted['declarations']:
        path = (repo / declaration['path']).relative_to(graph.workspace).as_posix()
        ev = graph.add_evidence(repository, path, declaration['line'], declaration['declaration'],
                                'testing-' + declaration['family'].lower().removeprefix('test_').replace('_', '-'))
        source = _id('test-source', repository, declaration['path'])
        if source not in files:
            node(source, 'COMPONENT', Path(declaration['path']).name, path, (ev,), {'source_kind': 'TEST_SOURCE'})
            files[source] = source
            edge(root, source, 'CONTAINS_COMPONENT', (ev, root_evidence))
        family = declaration['family']
        if family == 'TEST_HTTP':
            destination = declaration['destination']
            target = _id('test-api', repository, declaration['method'], destination or declaration['path'],
                         '' if destination else declaration['line'])
            url = urlsplit(destination) if destination else None
            properties = {'method': declaration['method'], 'path': url.path if url else None,
                          'authority': url.netloc if url else None, 'url': destination,
                          'destination_expression': declaration.get('destination_expression'), 'protocol': 'HTTP'}
            node(target, 'API_OPERATION', declaration['method'] + ' ' + (destination or '<unknown testing URL>'),
                 path, (ev,), properties)
            edge(source, target, 'CALLS_REST', (ev,), 'UNRESOLVED', {'client': declaration['client'], **properties})
        elif family in {'TEST_DATABASE', 'TEST_OBJECT_STORAGE'}:
            target = _id('test-boundary', repository, family, declaration['path'], declaration['line'])
            node(target, 'DATABASE' if family == 'TEST_DATABASE' else 'EXTERNAL_SYSTEM',
                 declaration['client'] + ' testing client (unknown destination)', path, (ev,),
                 {'protocol': declaration['protocol'], 'identity_status': 'UNKNOWN',
                  'client_declaration_only': declaration.get('client_declaration_only', False)})
            edge(source, target, 'CONNECTS_TO', (ev,), 'UNRESOLVED', {'client': declaration['client'],
                                                                   'client_declaration_only': True})
        else:
            target_path = None
            imported = declaration['target']
            if not declaration['dynamic'] and (family == 'TEST_ROBOT_RESOURCE' or imported.endswith('.py')):
                candidate = Path(os.path.abspath(repo / declaration['path'] / '..' / imported))
                if candidate.is_relative_to(repo) and is_source_file(repo, candidate):
                    target_path = candidate.relative_to(graph.workspace).as_posix()
            if target_path:
                provider = graph.add_evidence(repository, target_path, 1, 'Local Robot import source', 'testing-import-provider')
                target = _id('test-source', repository, candidate.relative_to(repo).as_posix())
                node(target, 'COMPONENT', candidate.name, target_path, (provider,), {'source_kind': 'TEST_SOURCE'})
                edge(source, target, 'IMPORTS_TEST_RESOURCE' if family == 'TEST_ROBOT_RESOURCE' else 'IMPORTS_TEST_LIBRARY',
                     (ev, provider), 'RESOLVED', {'resolution_rule': 'same-repository-test-import-file'})
            else:
                # Unknown destinations cannot establish shared provider identity.
                identity_scope = (declaration['path'], declaration['line']) if declaration['dynamic'] or family == 'TEST_ROBOT_RESOURCE' else ()
                target = _id('test-import', repository, family, imported, *identity_scope)
                node(target, 'EXTERNAL_SYSTEM', 'Robot ' + declaration['import_kind'].lower() + ': ' + imported,
                     None, (ev,), {'identity_status': 'UNKNOWN', 'dependency_kind': declaration['import_kind']}, owner=None)
                edge(source, target, 'IMPORTS_TEST_RESOURCE' if family == 'TEST_ROBOT_RESOURCE' else 'IMPORTS_TEST_LIBRARY',
                     (ev,), 'UNRESOLVED')
    for diagnostic in extracted['diagnostics']:
        graph.diagnostic(diagnostic['code'], f"Line {diagnostic['line']}: {diagnostic['message']}", repository,
                         (repo / diagnostic['path']).relative_to(graph.workspace).as_posix())
    return {'declarations': len(extracted['declarations']), 'files_scanned': extracted['files_scanned'],
            'diagnostics': len(extracted['diagnostics']), 'ledger': extracted['ledger']}
