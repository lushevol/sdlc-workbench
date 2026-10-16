"""Extract static Java HTTP calls that use ``URI`` values.

This extractor covers the narrow form used by the orchestration service:
``client.execute(new URI(CONSTANT), body)`` and ``URI.create(CONSTANT)``.
It resolves only string literals and unambiguous string constants found in the
same repository. Dynamic configuration and computed URLs remain diagnostics.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java

from .source_inventory import iter_source_files, java_source_roots
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


CALL = re.compile(
    r"(?P<receiver>[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)\s*\.\s*"
    r"(?P<method>execute|exchange|getForEntity|getForObject|getForRequest|postForEntity|"
    r"postForObject|put|delete|send|request)\s*\(\s*"
    r"(?:(?:new\s+URI)|(?:URI\s*\.\s*create))\s*\(\s*(?P<expression>[^)]*)\)",
)
URI_CONSTRUCTION = re.compile(
    r"(?P<constructor>new\s+URI|URI\s*\.\s*create)\s*\(\s*(?P<expression>[^)]*)\)",
)


def _without_comments(text: str) -> str:
    encoded = bytearray(text.encode('utf-8'))
    root = Parser(Language(tree_sitter_java.language())).parse(bytes(encoded)).root_node
    for node in _walk(root):
        if node.type in {'line_comment', 'block_comment'}:
            for index in range(node.start_byte, node.end_byte):
                if encoded[index] not in {10, 13}:
                    encoded[index] = 32
    return encoded.decode('utf-8')


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _caller_context(node, text):
    deferred = False
    while node is not None and node.type not in {'class_declaration', 'interface_declaration', 'record_declaration', 'enum_declaration'}:
        if node.type == 'lambda_expression':
            deferred = True
        if node.type in {'method_declaration', 'constructor_declaration', 'compact_constructor_declaration'}:
            parameters = node.child_by_field_name('parameters')
            return {'source_method': text(node.child_by_field_name('name')),
                    'source_method_line': node.start_point.row + 1,
                    'source_arity': sum(child.type in {'formal_parameter', 'spread_parameter'} for child in parameters.named_children) if parameters is not None else 0,
                    'deferred': deferred}
        node = node.parent
    return {'deferred': deferred}


def _static_constants(source: str, path: Path, repo: Path):
    encoded = source.encode('utf-8')
    root = Parser(Language(tree_sitter_java.language())).parse(encoded).root_node
    def text(node):
        return encoded[node.start_byte:node.end_byte].decode('utf-8') if node else ''
    package = next((text(node).removeprefix('package').strip().rstrip(';').strip()
                    for node in root.named_children if node.type == 'package_declaration'), '')
    imports = [text(node).removeprefix('import').strip().rstrip(';').strip()
               for node in root.named_children if node.type == 'import_declaration']
    constants, contexts = [], []
    for node in _walk(root):
        if node.type in {'class_declaration', 'interface_declaration', 'enum_declaration', 'record_declaration'}:
            owners, owner = [], node
            while owner:
                if owner.type in {'class_declaration', 'interface_declaration', 'enum_declaration', 'record_declaration'}:
                    owners.insert(0, text(owner.child_by_field_name('name')))
                owner = owner.parent
            qualified = '.'.join(([package] if package else []) + owners)
            contexts.append((node.start_byte, node.end_byte, qualified))
        if node.type not in {'field_declaration', 'constant_declaration'} or text(node.child_by_field_name('type')) != 'String':
            continue
        modifiers = next((text(child) for child in node.named_children if child.type == 'modifiers'), '')
        owner = node.parent.parent if node.parent else None
        if not owner or (owner.type != 'interface_declaration' and not {'static', 'final'} <= set(modifiers.split())):
            continue
        context = next((row[2] for row in reversed(contexts) if row[0] <= node.start_byte < row[1]), None)
        for variable in node.named_children:
            if variable.type != 'variable_declarator':
                continue
            value_node = variable.child_by_field_name('value')
            value = _literal(text(value_node)) if value_node and value_node.type == 'string_literal' else None
            if value is not None and context:
                constants.append({
                    'identity': context + '.' + text(variable.child_by_field_name('name')), 'value': value,
                    'path': path.relative_to(repo).as_posix(), 'line': node.start_point.row + 1,
                    'declaration': text(node)[:500], 'extractor': 'java-http-constant',
                })
    return constants, package, imports, contexts


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _literal(expression: str) -> str | None:
    expression = expression.strip()
    if len(expression) >= 2 and expression[0] in {"'", '"'} and expression[-1] == expression[0]:
        try:
            value = json.loads(expression) if expression[0] == '"' else expression[1:-1]
        except (TypeError, ValueError):
            return None
        return value if isinstance(value, str) else None
    return None


def _safe_endpoint(value: str) -> str:
    """Keep routing identity while excluding embedded credentials and query values."""
    try:
        parsed = urlsplit(value)
        if parsed.scheme:
            if parsed.scheme not in {'http', 'https', 'ws', 'wss'} or not parsed.hostname:
                return ''
        elif not value.startswith('/'):
            return ''
        if value.startswith('//') and not parsed.hostname:
            return ''
        parsed.port  # Validate explicit ports even when no redaction is needed.
        if not parsed.query and not parsed.fragment and parsed.username is None and parsed.password is None:
            return value
        authority = parsed.hostname or ''
        if ':' in authority:
            authority = '[' + authority + ']'
        if parsed.port:
            authority += ':' + str(parsed.port)
        query = urlencode([(key, '{value}') for key, _ in parse_qsl(parsed.query, keep_blank_values=True)])
        return urlunsplit((parsed.scheme, authority, parsed.path, query, ''))
    except ValueError:
        return ''


def _safe_expression(value: str) -> str:
    def literal(match):
        decoded = _literal(match.group(0))
        if decoded and decoded.lower().startswith(('/', 'http://', 'https://', 'ws://', 'wss://')):
            safe = _safe_endpoint(decoded)
            return match.group(0) if safe == decoded else json.dumps(safe)
        return '"{literal}"'
    return re.sub(r'"(?:\\.|[^"\\])*"', literal, value)[:500]


def _safe_constant(record):
    return {**record, 'value': _safe_endpoint(record['value']),
            'declaration': _safe_expression(record['declaration'])}


def _typed_calls(source, path, repo, resolve_constant):
    """Retain typed RestTemplate calls even when their destination is symbolic."""
    encoded = source.encode('utf-8')
    root = Parser(Language(tree_sitter_java.language())).parse(encoded).root_node
    txt = lambda node: encoded[node.start_byte:node.end_byte].decode('utf-8') if node else ''
    imports = {txt(n).removeprefix('import').strip().rstrip(';') for n in root.named_children
               if n.type == 'import_declaration'}
    local_shadow = any(n.type in {'class_declaration', 'interface_declaration'}
                       and txt(n.child_by_field_name('name')) == 'RestTemplate' for n in _walk(root))
    known_simple = not local_shadow and bool(imports & {
        'org.springframework.web.client.RestTemplate', 'org.springframework.web.client.*'})
    declarations = []
    for node in _walk(root):
        if node.type not in {'field_declaration', 'local_variable_declaration', 'formal_parameter'}:
            continue
        type_name = txt(node.child_by_field_name('type'))
        scope = node.parent
        required_scope = ({'class_body'} if node.type == 'field_declaration'
                          else {'method_declaration', 'constructor_declaration'} if node.type == 'formal_parameter'
                          else {'block', 'for_statement', 'enhanced_for_statement'})
        while scope and scope.type not in required_scope:
            scope = scope.parent
        if not scope:
            continue
        variables = [node] if node.type == 'formal_parameter' else [c for c in node.named_children if c.type == 'variable_declarator']
        for variable in variables:
            declarations.append({'name': txt(variable.child_by_field_name('name')), 'type': type_name,
                                 'value': variable.child_by_field_name('value'), 'scope': scope,
                                 'start': node.start_byte, 'field': node.type == 'field_declaration'})

    def declaration(name, call, *, fields_only=False):
        candidates = [d for d in declarations if d['name'] == name and (not fields_only or d['field'])
                      and d['scope'].start_byte <= call.start_byte < d['scope'].end_byte
                      and (d['field'] or d['start'] < call.start_byte)]
        candidates.sort(key=lambda d: (d['scope'].end_byte-d['scope'].start_byte, -d['start']))
        return candidates[0] if candidates else None

    methods = {'getForEntity': 'GET', 'getForObject': 'GET', 'postForEntity': 'POST',
               'postForObject': 'POST', 'postForLocation': 'POST', 'put': 'PUT', 'patchForObject': 'PATCH',
               'delete': 'DELETE', 'headForHeaders': 'HEAD', 'optionsForAllow': 'OPTIONS',
               'exchange': 'ANY', 'execute': 'ANY'}
    calls, diagnostics = [], []
    for call in _walk(root):
        if call.type != 'method_invocation' or call.has_error:
            continue
        method = txt(call.child_by_field_name('name'))
        if method not in methods:
            continue
        receiver = txt(call.child_by_field_name('object'))
        name = receiver.removeprefix('this.')
        if not re.fullmatch(r'[A-Za-z_$][\w$]*', name):
            continue
        binding = declaration(name, call, fields_only=receiver.startswith('this.'))
        if not binding or not (binding['type'] == 'org.springframework.web.client.RestTemplate'
                               or binding['type'] == 'RestTemplate' and known_simple):
            continue
        arguments = call.child_by_field_name('arguments')
        args = list(arguments.named_children) if arguments else []
        if not args:
            continue
        expression_node = args[0]
        expression = txt(expression_node)
        value = _literal(expression)
        support = []
        char_offset = len(encoded[:call.start_byte].decode('utf-8'))
        constant = resolve_constant(expression, path, char_offset)
        if constant:
            value = constant['value']
            support.append({**_safe_constant(constant), 'declaration': 'Static URL constant ' + constant['identity']})
        # A single, unreassigned local initializer preserves the getter chain.
        if expression_node.type == 'identifier':
            local = declaration(expression, call)
            if local and local['value']:
                assignments = [n for n in _walk(local['scope']) if n.type in {'assignment_expression', 'update_expression'}
                               and txt(n.child_by_field_name('left') or n.child_by_field_name('operand')) == expression]
                if not assignments:
                    expression_node = local['value']
                    expression = txt(local['value'])
                    value = _literal(expression)
                    if value is None:
                        constant = resolve_constant(expression, path, char_offset)
                        if constant:
                            value = constant['value']
        verb = methods[method]
        if method in {'exchange', 'execute'} and len(args) > 1:
            verb_match = re.fullmatch(r'(?:HttpMethod\.)?(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)', txt(args[1]))
            if verb_match:
                verb = verb_match.group(1)
        endpoint = _safe_endpoint(value) if value else ''
        symbolic = _safe_expression(expression)
        line = call.start_point.row + 1
        calls.append({'path': path.relative_to(repo).as_posix(), 'line': line, 'method': verb,
                      **_caller_context(call, txt),
                      'path_value': endpoint, 'receiver': receiver, 'client_method': method,
                      'client_kind': 'REST_TEMPLATE', 'endpoint_expression': symbolic,
                      'destination_start_byte': expression_node.start_byte,
                      'destination_end_byte': expression_node.end_byte,
                      'unresolved': not bool(endpoint),
                      'declaration': f'RestTemplate.{method}({symbolic}, ...)', 'supporting_evidence': support})
        if not endpoint:
            diagnostics.append({'code': 'UNRESOLVED_JAVA_HTTP_DESTINATION', 'path': path.relative_to(repo).as_posix(),
                                'line': line, 'message': 'Typed HTTP call has a symbolic destination; provider identity is unknown'})
    return calls, diagnostics


def extract(repo: Path) -> dict[str, list[dict[str, Any]]]:
    repo = repo.resolve()
    files: list[tuple[Path, str, str]] = []
    constants: dict[str, list[dict]] = {}
    scopes = {}
    for java_root in java_source_roots(repo):
        for path in iter_source_files(repo, root=java_root, suffixes={".java"}):
            try:
                original = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            source = _without_comments(original)
            files.append((path, original, source))
            records, package, imports, contexts = _static_constants(source, path, repo)
            scopes[path] = (package, imports, contexts)
            for record in records:
                constants.setdefault(record['identity'], []).append(record)

    def resolve_constant(expression, path, offset):
        if not re.fullmatch(r'(?:[A-Za-z_$][\w$]*\.)*[A-Za-z_$][\w$]*', expression):
            return None
        package, imports, contexts = scopes[path]
        identities = {expression, (package + '.' + expression) if package else expression}
        for imported in imports:
            if imported.startswith('static '):
                imported = imported.removeprefix('static ')
                if imported.endswith('.*'):
                    identities.add(imported[:-2] + '.' + expression)
                elif imported.rsplit('.', 1)[-1] == expression:
                    identities.add(imported)
            else:
                prefix, _, rest = expression.partition('.')
                if imported.rsplit('.', 1)[-1] == prefix and rest:
                    identities.add(imported + '.' + rest)
        byte_offset = len(files_source[path][:offset].encode('utf-8'))
        local = [row for row in contexts if row[0] <= byte_offset < row[1]]
        if local:
            identities.add(min(local, key=lambda row: row[1] - row[0])[2] + '.' + expression)
        records = [record for identity in identities for record in constants.get(identity, [])]
        return records[0] if len(records) == 1 else None

    files_source = {path: source for path, _, source in files}

    calls: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for path, original, source in files:
        parsed = Parser(Language(tree_sitter_java.language())).parse(source.encode('utf-8')).root_node
        invocations = {node.start_byte: node for node in _walk(parsed) if node.type == 'method_invocation' and not node.has_error}
        constructions = {node.start_byte for node in _walk(parsed)
                         if node.type in {'method_invocation', 'object_creation_expression'} and not node.has_error}
        byte_offset = lambda position: len(source[:position].encode('utf-8'))
        for match in CALL.finditer(source):
            if byte_offset(match.start()) not in invocations:
                continue
            expression = match.group("expression").strip()
            value = _literal(expression)
            constant = resolve_constant(expression, path, match.start()) if value is None else None
            if constant:
                value = constant['value']
            if not value:
                diagnostics.append({
                    "code": "UNRESOLVED_JAVA_HTTP_URI",
                    "path": path.relative_to(repo).as_posix(),
                    "line": _line(source, match.start()),
                    "message": "Java HTTP URI uses a dynamic or ambiguous expression",
                })
                continue
            if not re.match(r"^(?:https?|wss?)://", value, re.I):
                diagnostics.append({
                    "code": "UNRESOLVED_JAVA_HTTP_URI",
                    "path": path.relative_to(repo).as_posix(),
                    "line": _line(source, match.start()),
                    "message": "Java HTTP URI is not an absolute HTTP URL",
                })
                continue
            calls.append({
                "path": path.relative_to(repo).as_posix(),
                **_caller_context(invocations[byte_offset(match.start())],
                                  lambda node: source.encode('utf-8')[node.start_byte:node.end_byte].decode('utf-8') if node else ''),
                "line": _line(source, match.start()),
                "method": "ANY",
                "path_value": _safe_endpoint(value),
                "receiver": match.group("receiver"),
                "client_method": match.group("method"),
                "declaration": _safe_expression(match.group(0)),
                "supporting_evidence": [_safe_constant(constant)] if constant else [],
            })
        # Surface direct URI construction that is not in a recognized client
        # call. It is a boundary candidate, but its use cannot be proven here.
        recognized = [(m.start(), m.end()) for m in CALL.finditer(source) if byte_offset(m.start()) in invocations]
        for construction in URI_CONSTRUCTION.finditer(source):
            if byte_offset(construction.start()) not in constructions:
                continue
            if any(start <= construction.start() < end for start, end in recognized):
                continue
            expression = construction.group("expression").strip()
            if expression and not _literal(expression) and not resolve_constant(expression, path, construction.start()):
                diagnostics.append({
                    "code": "UNRESOLVED_JAVA_HTTP_URI",
                    "path": path.relative_to(repo).as_posix(),
                    "line": _line(source, construction.start()),
                    "message": "Java URI construction uses a dynamic or unresolved expression",
                })

    existing = {(c['path'], c['line']) for c in calls}
    for path, original, source in files:
        typed, limits = _typed_calls(source, path, repo, resolve_constant)
        calls.extend(call for call in typed if (call['path'], call['line']) not in existing)
        diagnostics.extend(limits)
    return {"calls": calls, "diagnostics": diagnostics}


__all__ = ["extract"]
