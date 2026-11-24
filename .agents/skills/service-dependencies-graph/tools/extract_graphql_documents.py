"""Retain imported gql documents without inferring transports or providers.

Literal documents expose sanitized field selections. Template substitutions
remain explicit unresolved boundaries. Argument values never enter the graph.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import os
from pathlib import Path
import re

from tree_sitter import Language, Parser
import tree_sitter_typescript

from .source_inventory import iter_source_files

_MODULES = {'@apollo/client', '@apollo/client/core', 'graphql-tag', 'graphql-request'}
_TEST = re.compile(r'\.(?:test|spec)\.[cm]?[jt]sx?$|\.d\.[cm]?ts$')
_FUNCTIONS = {'function_declaration', 'function_expression', 'arrow_function',
              'generator_function_declaration', 'generator_function', 'method_definition'}
_SCOPES = _FUNCTIONS | {'program', 'statement_block', 'catch_clause', 'for_statement', 'for_in_statement'}


def _id(prefix, *parts):
    return prefix + ':' + hashlib.sha256('|'.join(map(str, parts)).encode()).hexdigest()[:24]


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _pattern_names(node, text):
    if node is None: return set()
    if node.type in {'identifier', 'shorthand_property_identifier_pattern'}: return {text(node)}
    if node.type == 'pair_pattern': return _pattern_names(node.child_by_field_name('value'), text)
    if node.type in {'assignment_pattern', 'object_assignment_pattern'}:
        return _pattern_names(node.child_by_field_name('left'), text)
    if node.type in {'required_parameter', 'optional_parameter'}:
        return _pattern_names(node.child_by_field_name('pattern') or node.child_by_field_name('name'), text)
    if node.type in {'object_pattern', 'array_pattern', 'rest_pattern', 'formal_parameters'}:
        return set().union(*(_pattern_names(child, text) for child in node.named_children)) if node.named_children else set()
    return set()


def _scope_bindings(scope, text):
    """Collect lexical declarations and function-scoped var bindings conservatively."""
    names = set()
    if scope.type in _FUNCTIONS:
        names |= _pattern_names(scope.child_by_field_name('parameters'), text)
        names |= _pattern_names(scope.child_by_field_name('parameter'), text)
        if scope.type in {'function_expression', 'generator_function'}:
            names |= _pattern_names(scope.child_by_field_name('name'), text)
        pending = list(scope.named_children)
        while pending:
            node = pending.pop()
            if node.type in _FUNCTIONS or node.type in {'class_declaration', 'class'}: continue
            if node.type == 'variable_declaration':
                for declaration in node.named_children:
                    if declaration.type == 'variable_declarator':
                        names |= _pattern_names(declaration.child_by_field_name('name'), text)
            pending.extend(node.named_children)
        return names
    if scope.type == 'catch_clause': names |= _pattern_names(scope.child_by_field_name('parameter'), text)
    pending = list(scope.named_children)
    while pending:
        node = pending.pop()
        if node.type in {'function_declaration', 'generator_function_declaration', 'class_declaration'}:
            names |= _pattern_names(node.child_by_field_name('name'), text)
        if node.type in _SCOPES or node.type in {'class_declaration', 'class'}: continue
        if node.type == 'lexical_declaration' or scope.type == 'program' and node.type == 'variable_declaration':
            for declaration in node.named_children:
                if declaration.type == 'variable_declarator':
                    names |= _pattern_names(declaration.child_by_field_name('name'), text)
        pending.extend(node.named_children)
    return names


def _shadowed(call, name, text, cache):
    parent = call.parent
    while parent:
        if parent.type in _SCOPES:
            key = parent.start_byte, parent.end_byte, parent.type
            if key not in cache: cache[key] = _scope_bindings(parent, text)
            if name in cache[key]: return True
        parent = parent.parent
    return False


def _tokens(source):
    """Tokenize names and punctuation; replace all literals before parsing."""
    tokens = []; index = 0
    while index < len(source):
        if len(tokens) >= 25000: raise ValueError('DOCUMENT_TOKEN_LIMIT')
        char = source[index]
        if char.isspace() or char in ',\ufeff': index += 1; continue
        if char == '#':
            end = source.find('\n', index); index = len(source) if end < 0 else end; continue
        if source.startswith('"""', index):
            end = index + 3
            while end < len(source) and (not source.startswith('"""', end) or source[end - 1] == '\\'): end += 1
            if end >= len(source): raise ValueError('INVALID_GRAPHQL_DOCUMENT')
            tokens.append(('VALUE', index)); index = end + 3; continue
        if char == '"':
            end = index + 1
            while end < len(source):
                if source[end] == '\\': end += 2; continue
                if source[end] == '"': break
                end += 1
            if end >= len(source): raise ValueError('INVALID_GRAPHQL_DOCUMENT')
            tokens.append(('VALUE', index)); index = end + 1; continue
        name = re.match(r'[_A-Za-z][_0-9A-Za-z]*', source[index:])
        if name:
            tokens.append((name.group(), index)); index += len(name.group()); continue
        number = re.match(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?', source[index:])
        if number:
            tokens.append(('VALUE', index)); index += len(number.group()); continue
        if source.startswith('...', index): tokens.append(('...', index)); index += 3; continue
        if char in '!$&():=@[]{|}': tokens.append((char, index)); index += 1; continue
        raise ValueError('INVALID_GRAPHQL_DOCUMENT')
    return tokens


def _document(source):
    tokens = _tokens(source); position = 0; count = 0; operations = []; fragments = []
    def current(): return tokens[position][0] if position < len(tokens) else None
    def take(expected=None):
        nonlocal position
        if position >= len(tokens) or expected is not None and current() != expected: raise ValueError('INVALID_GRAPHQL_DOCUMENT')
        value = tokens[position]; position += 1; return value
    def name():
        value, offset = take()
        if not re.fullmatch(r'[_A-Za-z][_0-9A-Za-z]*', value) or value == 'VALUE': raise ValueError('INVALID_GRAPHQL_DOCUMENT')
        return value, offset
    def group(opening, closing):
        take(opening); stack = [closing]
        while stack:
            value, _ = take()
            if value in {'(', '[', '{'}: stack.append({'(': ')', '[': ']', '{': '}'}[value])
            elif value in {')', ']', '}'}:
                if value != stack.pop(): raise ValueError('INVALID_GRAPHQL_DOCUMENT')
            if len(stack) > 64: raise ValueError('DOCUMENT_DEPTH_LIMIT')
    def directives():
        while current() == '@':
            take('@'); name()
            if current() == '(': group('(', ')')
    def selection(parent=(), response=(), depth=0):
        nonlocal count
        if depth > 32: raise ValueError('DOCUMENT_DEPTH_LIMIT')
        take('{'); fields = []; spreads = []
        while current() != '}':
            if current() == '...':
                take('...'); spread, _ = name()
                if spread == 'on':
                    name(); directives(); child, child_spreads = selection(parent, response, depth + 1)
                    fields.extend(child); spreads.extend(child_spreads)
                else:
                    spreads.append(spread); directives()
                continue
            field, offset = name(); alias = field
            if current() == ':': take(':'); field, offset = name()
            if current() == '(': group('(', ')')
            directives(); count += 1
            if count > 2000: raise ValueError('DOCUMENT_FIELD_LIMIT')
            fields.append({'name': field, 'field_path': [*parent, field], 'response_path': [*response, alias], 'offset': offset})
            if current() == '{':
                child, child_spreads = selection((*parent, field), (*response, alias), depth + 1)
                fields.extend(child); spreads.extend(child_spreads)
        take('}'); return fields, sorted(set(spreads))
    while current() is not None:
        kind = 'query' if current() == '{' else take()[0]
        if kind == 'fragment':
            fragment, _ = name(); take('on'); name(); directives(); selection(); fragments.append(fragment); continue
        if kind not in {'query', 'mutation', 'subscription'}: raise ValueError('UNSUPPORTED_GRAPHQL_DEFINITION')
        operation_name = None
        if current() not in {'(', '@', '{'}: operation_name, _ = name()
        if current() == '(': group('(', ')')
        directives(); fields, spreads = selection()
        operations.append({'operation_type': kind.upper(), 'operation_name': operation_name, 'fields': fields, 'fragment_spreads': spreads})
    if not operations and not fragments: raise ValueError('INVALID_GRAPHQL_DOCUMENT')
    return operations, fragments


def add_to_graph(graph, repo: Path, repository: str):
    """Add source document declarations and static selections, never API calls."""
    repo = Path(os.path.abspath(repo)); workspace = Path(os.path.abspath(graph.workspace))
    ledger = []; statistics = Counter(); existing = {}
    for node in graph.nodes.values():
        if node.get('repository') == repository and node.get('component_kind') == 'SOURCE_MODULE':
            for path in node.get('source_paths', []): existing.setdefault(path, []).append(node['id'])
    def record(path, line, disposition, reason=None, evidence=()):
        row = {'family': 'graphql_document', 'path': path.relative_to(repo).as_posix(), 'line': line,
               'disposition': disposition, 'evidence': list(evidence)}
        if reason: row['reason'] = reason
        ledger.append(row)
    for path in iter_source_files(repo, suffixes=('.ts', '.tsx', '.js', '.jsx')):
        if _TEST.search(path.name): continue
        try:
            if path.stat().st_size > 2 * 1024 * 1024: continue
            encoded = path.read_bytes()
        except OSError: continue
        language = tree_sitter_typescript.language_tsx() if path.suffix in {'.tsx', '.jsx'} else tree_sitter_typescript.language_typescript()
        root = Parser(Language(language)).parse(encoded).root_node
        text = lambda node: encoded[node.start_byte:node.end_byte].decode('utf-8', errors='replace') if node else ''
        bindings = {}; scope_cache = {}
        for node in root.named_children:
            if node.type != 'import_statement' or any(child.type == 'type' for child in node.children): continue
            module = text(node.child_by_field_name('source'))[1:-1]
            clause = next((child for child in node.named_children if child.type == 'import_clause'), None)
            if clause is None: continue
            for item in _walk(clause):
                local = None
                if item.type == 'import_specifier' and not any(child.type == 'type' for child in item.children):
                    if text(item.child_by_field_name('name')) == 'gql':
                        local = text(item.child_by_field_name('alias') or item.child_by_field_name('name'))
                elif item.type == 'identifier' and item.parent == clause and module == 'graphql-tag': local = text(item)
                if local:
                    safe_module = module if re.fullmatch(r'[@_A-Za-z0-9./+-]+', module) else 'UNRESOLVED_MODULE'
                    bindings.setdefault(local, []).append((safe_module, node.start_point.row + 1, module in _MODULES))
        if not bindings: continue
        path_value = path.relative_to(workspace).as_posix()
        for call in _walk(root):
            if call.type != 'call_expression': continue
            function = call.child_by_field_name('function'); template = call.child_by_field_name('arguments')
            if function is None or function.type != 'identifier' or template is None or template.type != 'template_string': continue
            binding = text(function)
            if binding not in bindings: continue
            line = call.start_point.row + 1
            if len(bindings[binding]) != 1 or _shadowed(call, binding, text, scope_cache):
                record(path, line, 'EXCLUDED', 'SHADOWED_OR_AMBIGUOUS_GQL_BINDING'); statistics['shadowed_templates'] += 1; continue
            module, import_line, bound_provider = bindings[binding][0]
            substitutions = [child for child in template.named_children if child.type == 'template_substitution']
            source = text(template)[1:-1]; operations = []; fragments = []; reason = None
            if substitutions or not bound_provider:
                reason = 'DYNAMIC_GRAPHQL_DOCUMENT' if bound_provider else 'UNRESOLVED_GQL_TAG_PROVIDER'
                prefix = encoded[template.start_byte + 1:substitutions[0].start_byte].decode('utf-8', errors='replace') if substitutions else source
                match = re.match(r'\s*(query|mutation|subscription)\b(?:\s+([_A-Za-z][_0-9A-Za-z]*))?', prefix)
                if match: operations = [{'operation_type': match[1].upper(), 'operation_name': match[2], 'fields': [], 'fragment_spreads': []}]
                elif prefix.lstrip().startswith('{'): operations = [{'operation_type': 'QUERY', 'operation_name': None, 'fields': [], 'fragment_spreads': []}]
                if substitutions: statistics['dynamic_documents'] += 1
                if not bound_provider: statistics['unresolved_tag_providers'] += 1
            else:
                try: operations, fragments = _document(source)
                except (ValueError, RecursionError) as error:
                    reason = str(error) if isinstance(error, ValueError) else 'DOCUMENT_DEPTH_LIMIT'
                    statistics['unsupported_documents'] += 1
                else: statistics['static_documents'] += 1
            types = sorted({item['operation_type'] for item in operations})
            names = sorted({item['operation_name'] for item in operations if item['operation_name']})
            fields = [item for operation in operations for item in operation['fields']]
            label = ', '.join(names) or '/'.join(kind.lower() for kind in types) or 'GraphQL'
            ev = graph.add_evidence(repository, path_value, line, 'Imported gql document; operation types: ' +
                                    (', '.join(types) or 'UNKNOWN') + '; operation names: ' + (', '.join(names) or 'anonymous or dynamic'),
                                    'web-graphql-document')
            import_ev = graph.add_evidence(repository, path_value, import_line,
                                           'Imports gql as ' + binding + ' from ' + module, 'web-graphql-document-import')
            document_id = _id('graphql-document', repository, path_value, call.start_byte)
            properties = {'protocol': 'GRAPHQL', 'document_status': 'PARTIAL' if reason else 'STATIC',
                          'operation_types': types, 'operation_names': names, 'substitution_count': len(substitutions),
                          'root_fields': sorted({item['name'] for item in fields if len(item['field_path']) == 1}),
                          'fragment_definitions': fragments,
                          'fragment_spreads': sorted({spread for item in operations for spread in item['fragment_spreads']}),
                          'source_line': line, 'dependency_kind': 'DOCUMENT_DECLARATION',
                          'tag_provider_status': 'IMPORTED' if bound_provider else 'UNRESOLVED'}
            if reason: properties['limitation'] = reason
            if substitutions and not bound_provider: properties['additional_limitations'] = ['DYNAMIC_GRAPHQL_DOCUMENT']
            graph.add_node(document_id, 'GRAPHQL_DOCUMENT', label + ' document', repository, dimensions=('RUNTIME',),
                           component_kind=None, functional_role='Declares a GraphQL source document',
                           business_meaning='Describes selected fields; transport and provider remain separate',
                           source_paths=(path_value,), evidence=(ev, import_ev), properties=properties,
                           assertion_status='CONFIRMED' if bound_provider else 'INFERRED')
            known = existing.get(path_value, [])
            owner = known[0] if len(known) == 1 else _id('source-module', repository, path_value)
            if owner not in graph.nodes:
                graph.add_node(owner, 'COMPONENT', path.name, repository, dimensions=('RUNTIME',), component_kind='SOURCE_MODULE',
                               functional_role='Contains static ES module declarations', business_meaning='Groups source declarations for repository analysis',
                               source_paths=(path_value,), evidence=(ev,))
                roots = [node['id'] for node in graph.nodes.values()
                         if node.get('repository') == repository and node['type'] in {'APPLICATION', 'SERVICE'}]
                if len(roots) == 1:
                    graph.add_edge(roots[0], owner, 'CONTAINS_COMPONENT', 'RUNTIME', (ev,), assertion_status='INFERRED')
            graph.add_edge(owner, document_id, 'DECLARES_GRAPHQL_DOCUMENT', 'RUNTIME', (ev, import_ev),
                           assertion_status='CONFIRMED' if bound_provider else 'INFERRED',
                           resolution_status=None if bound_provider else 'UNRESOLVED')
            for operation_index, operation in enumerate(operations):
                for field_index, field in enumerate(operation['fields']):
                    field_line = template.start_point.row + 1 + source.count('\n', 0, field['offset'])
                    selection = '.'.join(field['field_path'])
                    field_ev = graph.add_evidence(repository, path_value, field_line, 'Selects GraphQL field ' + selection,
                                                  'web-graphql-field-selection')
                    field_id = _id('graphql-selection', document_id, operation_index, field_index)
                    graph.add_node(field_id, 'GRAPHQL_FIELD_SELECTION', selection, repository, dimensions=('RUNTIME',), component_kind=None,
                                   functional_role='Selects a field within a source GraphQL document',
                                   business_meaning='Records document shape without a provider schema claim', source_paths=(path_value,), evidence=(field_ev,),
                                   properties={'protocol': 'GRAPHQL', 'field_name': field['name'], 'field_path': field['field_path'],
                                               'response_path': field['response_path'], 'operation_type': operation['operation_type'],
                                               'operation_name': operation['operation_name']})
                    graph.add_edge(document_id, field_id, 'SELECTS_GRAPHQL_FIELD', 'RUNTIME', (field_ev,))
                    statistics['field_selections'] += 1
            if reason:
                graph.diagnostic(reason, 'GraphQL document details remain partial; no transport or provider is inferred', repository, path_value)
            record(path, line, 'UNRESOLVED' if reason else 'EXTRACTED', reason, (ev, import_ev))
            statistics['documents'] += 1
    return {'ledger': ledger, 'statistics': dict(sorted(statistics.items()))}
