"""Extract literal Single-SPA layout registrations through inspected loader code."""
from __future__ import annotations

from collections import Counter
import hashlib
from html.parser import HTMLParser
import os
from pathlib import Path
import re

from tree_sitter import Language, Parser
import tree_sitter_typescript

from .source_inventory import is_source_file, iter_source_files


_FUNCTIONS = {'arrow_function', 'function_expression', 'function_declaration', 'method_definition'}
_MODULE = re.compile(r'[@A-Za-z0-9_./-]+')


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _pattern_names(node, text):
    if node is None:
        return []
    if node.type in {'identifier', 'shorthand_property_identifier_pattern'}:
        return [text(node)]
    if node.type == 'pair_pattern':
        return _pattern_names(node.child_by_field_name('value'), text)
    if node.type in {'assignment_pattern', 'object_assignment_pattern'}:
        return _pattern_names(node.child_by_field_name('left'), text)
    if node.type in {'required_parameter', 'optional_parameter'}:
        return _pattern_names(node.child_by_field_name('pattern') or node.child_by_field_name('name'), text)
    if node.type in {'object_pattern', 'array_pattern', 'rest_pattern', 'formal_parameters'}:
        return [name for child in node.named_children for name in _pattern_names(child, text)]
    return []


def _root_identifier(node, text):
    while node is not None and node.type in {'member_expression', 'subscript_expression'}:
        node = node.child_by_field_name('object')
    return text(node) if node is not None and node.type == 'identifier' else None


def _write_target(node):
    if node.type in {'assignment_expression', 'augmented_assignment_expression'}:
        return node.child_by_field_name('left')
    if node.type == 'update_expression':
        return node.child_by_field_name('argument')
    if node.type == 'unary_expression' and any(child.type == 'delete' for child in node.children):
        return node.child_by_field_name('argument')
    return None


class _Layout(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.applications = []
        self.unresolved = []

    def handle_starttag(self, tag, attrs):
        if tag == 'single-spa-router':
            self.depth += 1
        if tag != 'application' or not self.depth:
            return
        names = [value for key, value in attrs if key == 'name']
        if len(names) == 1 and names[0] and _MODULE.fullmatch(names[0]):
            self.applications.append((names[0], self.getpos()[0]))
        else:
            self.unresolved.append(self.getpos()[0])

    def handle_endtag(self, tag):
        if tag == 'single-spa-router':
            self.depth = max(0, self.depth - 1)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)


def extract(repo: Path) -> dict:
    """Require imported framework APIs, bound layout, loader, and registration.

    shortcut: only direct const bindings and inline System.import loaders are
    supported; broaden after a source-backed counterexample needs indirection.
    """
    repo = Path(os.path.abspath(repo))
    result = {'registrations': [], 'diagnostics': []}
    for path in iter_source_files(repo, root=repo / 'src', suffixes={'.ts', '.tsx', '.js', '.jsx'}):
        raw = path.read_bytes()
        language = (tree_sitter_typescript.language_tsx() if path.suffix in {'.tsx', '.jsx'}
                    else tree_sitter_typescript.language_typescript())
        root = Parser(Language(language)).parse(raw).root_node
        text = lambda node: raw[node.start_byte:node.end_byte].decode('utf-8', errors='replace') if node is not None else ''
        imports = {}
        for node in root.named_children:
            if node.type != 'import_statement' or text(node).startswith('import type'):
                continue
            module = text(node.child_by_field_name('source'))[1:-1]
            clause = next((child for child in node.named_children if child.type == 'import_clause'), None)
            for item in _walk(clause) if clause is not None else ():
                if item.type == 'import_specifier' and not text(item).startswith('type '):
                    name = text(item.child_by_field_name('name'))
                    imports[text(item.child_by_field_name('alias')) or name] = (module, name, node)
                elif item.type == 'identifier' and item.parent == clause:
                    imports[text(item)] = (module, 'default', node)
        apis = {name: local for local, (module, name, _) in imports.items()
                if (module, name) in {('single-spa-layout', 'constructRoutes'),
                                      ('single-spa-layout', 'constructApplications'),
                                      ('single-spa', 'registerApplication')}}
        if set(apis) != {'constructRoutes', 'constructApplications', 'registerApplication'}:
            continue
        if root.has_error:
            result['diagnostics'].append({'path': path.relative_to(repo).as_posix(), 'line': 1,
                                          'code': 'UNRESOLVED_SINGLE_SPA_LAYOUT', 'message': 'Registration source contains parse errors.'})
            continue
        nodes = list(_walk(root))
        bindings = Counter(name for node in nodes
                           if node.type in {'variable_declarator', 'function_declaration', 'class_declaration'}
                           for name in _pattern_names(node.child_by_field_name('name'), text))
        # Imported framework names and HTML bindings must remain unshadowed.
        for node in nodes:
            if node.type in _FUNCTIONS:
                parameters = node.child_by_field_name('parameters') or node.child_by_field_name('parameter')
                bindings.update(_pattern_names(parameters, text))
            elif node.type == 'catch_clause':
                bindings.update(_pattern_names(node.child_by_field_name('parameter'), text))
        if any(bindings[name] for name in apis.values()) or bindings['System'] or 'System' in imports:
            result['diagnostics'].append({'path': path.relative_to(repo).as_posix(), 'line': 1,
                                          'code': 'UNRESOLVED_SINGLE_SPA_LAYOUT',
                                          'message': 'Framework or System bindings are shadowed by local declarations.'})
            continue
        declarations = {text(node.child_by_field_name('name')): node for node in nodes
                        if node.type == 'variable_declarator' and bindings[text(node.child_by_field_name('name'))] == 1
                        and node.parent.type == 'lexical_declaration' and text(node.parent).startswith('const ')}

        def call(node, function):
            return node is not None and node.type == 'call_expression' and text(node.child_by_field_name('function')) == function

        def arguments(node):
            args = node.child_by_field_name('arguments')
            return args.named_children if args is not None else []

        def returned(node):
            body = node.child_by_field_name('body')
            if body is None or body.type != 'statement_block':
                return body
            rows = [child for child in body.named_children if child.type != 'comment']
            return (rows[0].named_children[0] if len(rows) == 1 and rows[0].type == 'return_statement'
                    and len(rows[0].named_children) == 1 else None)

        safe_consumers = {local for local, (module, name, _) in imports.items()
                          if module == 'single-spa-layout' and name in {'constructApplications', 'constructLayoutEngine'}
                          and not bindings[local]}

        def safe_binding_uses(name, declaration, allow_foreach=False):
            for use in nodes:
                if use.type not in {'identifier', 'shorthand_property_identifier'} or text(use) != name:
                    continue
                if use == declaration.child_by_field_name('name'):
                    continue
                parent = use.parent
                if (allow_foreach and parent.type == 'member_expression' and parent.child_by_field_name('object') == use
                        and text(parent.child_by_field_name('property')) == 'forEach' and parent.parent.type == 'call_expression'):
                    continue
                # Framework options can read these bindings. Unknown aliases or helpers cannot.
                while parent is not None and parent.type not in {'arguments', 'statement_block', 'program'}:
                    parent = parent.parent
                if parent is None or parent.type != 'arguments' or text(parent.parent.child_by_field_name('function')) not in safe_consumers:
                    return False
            return True

        for app_name, declaration in declarations.items():
            creation = declaration.child_by_field_name('value')
            if not call(creation, apis['constructApplications']) or len(arguments(creation)) != 1:
                continue
            options = arguments(creation)[0]
            if options.type != 'object':
                continue
            route_name, loader, unsupported = None, None, False
            for item in options.named_children:
                property_key = item.child_by_field_name('key') or item.child_by_field_name('name')
                if (item.type == 'spread_element' or property_key is not None
                        and (property_key.type == 'computed_property_name' or '\\' in text(property_key))):
                    unsupported = True
                    break
                key = (text(item) if item.type == 'shorthand_property_identifier'
                       else text(property_key).strip('\"\''))
                if key == 'routes':
                    value = item.child_by_field_name('value')
                    route_name = ('routes' if item.type == 'shorthand_property_identifier'
                                  else text(value) if item.type == 'pair' and value.type == 'identifier' else None)
                elif key == 'loadApp':
                    loader = item.child_by_field_name('value') if item.type == 'pair' else item
            if unsupported:
                continue
            route = declarations.get(route_name)
            route_call = route.child_by_field_name('value') if route is not None else None
            if (not call(route_call, apis['constructRoutes']) or len(arguments(route_call)) != 1 or loader is None
                    or route.parent.parent != declaration.parent.parent):
                continue
            if not safe_binding_uses(route_name, route) or not safe_binding_uses(app_name, declaration, allow_foreach=True):
                continue
            layout_name = text(arguments(route_call)[0])
            imported = imports.get(layout_name)
            if imported is None or imported[1] != 'default' or bindings[layout_name] or not imported[0].startswith('.'):
                continue
            layout = Path(os.path.abspath(path.parent / imported[0]))
            if layout.suffix != '.html' or not is_source_file(repo, layout):
                continue
            protected = {*apis.values(), 'System', route_name, app_name, layout_name}
            if any(_root_identifier(_write_target(node), text) in protected for node in nodes):
                continue
            if any(node.type == 'identifier' and text(node) == 'System'
                   and (node.parent.type != 'member_expression' or node.parent.child_by_field_name('object') != node
                        or text(node.parent.child_by_field_name('property')) != 'import') for node in nodes):
                continue
            if (loader.type not in {'arrow_function', 'function_expression', 'method_definition'}
                    or loader.type == 'method_definition'
                    and any(child.type in {'get', 'set', '*'} for child in loader.children)):
                continue
            params = loader.child_by_field_name('parameters')
            # A single destructured name proves the loaded key comes from this layout.
            parameter = params.named_children[0] if params is not None and len(params.named_children) == 1 else None
            pattern = (parameter.child_by_field_name('pattern') or parameter) if parameter is not None else None
            loaded = returned(loader)
            if (pattern is None or pattern.type != 'object_pattern' or len(pattern.named_children) != 1
                    or pattern.named_children[0].type != 'shorthand_property_identifier_pattern'
                    or text(pattern.named_children[0]) != 'name' or not call(loaded, 'System.import')
                    or len(arguments(loaded)) != 1 or text(arguments(loaded)[0]) != 'name'):
                continue
            registration = None
            for each in nodes:
                if not call(each, app_name + '.forEach') or len(arguments(each)) != 1:
                    continue
                scope = each.parent
                while scope is not None and scope != declaration.parent.parent:
                    scope = scope.parent
                if scope is None:
                    continue
                callback = arguments(each)[0]
                if text(callback) == apis['registerApplication']:
                    registration = each
                    break
                params = callback.child_by_field_name('parameters')
                parameter = callback.child_by_field_name('parameter')
                if params is not None and len(params.named_children) == 1:
                    parameter = params.named_children[0]
                    parameter = parameter.child_by_field_name('pattern') or parameter
                if parameter is None or parameter.type != 'identifier' or bindings[text(parameter)] != 1:
                    continue
                body = callback.child_by_field_name('body')
                unsafe = False
                for item in _walk(body) if body is not None else ():
                    left = _write_target(item)
                    if _root_identifier(left, text) == text(parameter):
                        # Only customProps writes preserve the registered application identity.
                        if (left.type != 'member_expression' or text(left.child_by_field_name('object')) != text(parameter)
                                or text(left.child_by_field_name('property')) != 'customProps'):
                            unsafe = True
                    if item.type == 'call_expression' and _root_identifier(item.child_by_field_name('function'), text) == text(parameter):
                        unsafe = True
                    if item.type == 'identifier' and text(item) == text(parameter):
                        parent = item.parent
                        if parent.type in {'member_expression', 'subscript_expression'} and parent.child_by_field_name('object') == item:
                            continue
                        if (parent.type == 'arguments' and call(parent.parent, apis['registerApplication'])
                                and len(parent.named_children) == 1):
                            continue
                        unsafe = True
                if unsafe:
                    continue
                for invoked in _walk(body) if body is not None else ():
                    if (call(invoked, apis['registerApplication']) and len(arguments(invoked)) == 1
                            and text(arguments(invoked)[0]) == text(parameter)):
                        ancestor = invoked.parent
                        while ancestor is not None and ancestor != callback and ancestor.type not in _FUNCTIONS:
                            ancestor = ancestor.parent
                        if ancestor == callback:
                            registration = invoked
                            break
            if registration is None:
                continue
            html = _Layout()
            html.feed(layout.read_text(encoding='utf-8', errors='replace'))
            for line in html.unresolved:
                result['diagnostics'].append({'path': layout.relative_to(repo).as_posix(), 'line': line,
                                              'code': 'UNRESOLVED_SINGLE_SPA_LAYOUT', 'message': 'Application name is not one literal module identity.'})
            for module, line in html.applications:
                result['registrations'].append({'module': module, 'layout_path': layout.relative_to(repo).as_posix(),
                                                 'layout_line': line, 'path': path.relative_to(repo).as_posix(),
                                                 'routes_line': route_call.start_point.row + 1,
                                                 'loader_line': loaded.start_point.row + 1,
                                                 'registration_line': registration.start_point.row + 1})
        if not any(row['path'] == path.relative_to(repo).as_posix() for row in result['registrations']):
            result['diagnostics'].append({'path': path.relative_to(repo).as_posix(),
                                          'line': imports[apis['constructRoutes']][2].start_point.row + 1,
                                          'code': 'UNRESOLVED_SINGLE_SPA_LAYOUT',
                                          'message': 'Layout registration needs direct bindings, a static HTML layout, and an inspected System.import loader.'})
    return result


def add_to_graph(graph, repo: Path, repository: str) -> dict:
    result = extract(repo)
    for row in result['diagnostics']:
        graph.diagnostic(row['code'], f"Line {row['line']}: {row['message']}", repository,
                         (repo / row['path']).relative_to(graph.workspace).as_posix())
    for row in result['registrations']:
        module = row['module']
        evidence = [graph.add_evidence(repository, (repo / row[path]).relative_to(graph.workspace).as_posix(),
                                       row[line], description, 'single-spa-layout')
                    for path, line, description in (
                        ('layout_path', 'layout_line', 'Single-SPA layout application ' + module),
                        ('path', 'routes_line', 'constructRoutes uses the imported HTML layout'),
                        ('path', 'loader_line', 'constructApplications loads layout names through System.import'),
                        ('path', 'registration_line', 'registerApplication registers the constructed applications'))]
        remote = 'remote:' + hashlib.sha256(module.encode()).hexdigest()[:24]
        graph.add_node(remote, 'REMOTE_APPLICATION', module, None, dimensions=('RUNTIME',), component_kind=None,
                       functional_role='Provides a remotely loaded JavaScript application',
                       business_meaning='Single-SPA layout declaration; active deployment remains unverified',
                       source_paths=(), evidence=evidence, properties={'module': module})
        graph.add_edge('application:' + repo.name, remote, 'LOADS_REMOTE', 'RUNTIME', evidence,
                       resolution_status='UNRESOLVED', properties={'module': module, 'single_spa_registration': True})
    return result
