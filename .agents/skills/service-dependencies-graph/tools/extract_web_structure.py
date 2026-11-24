"""Resolve static ES value imports within one repository, without execution claims.

Relative paths, tsconfig paths/baseUrl, index modules, named exports, and barrel
exports use exact source identities. Type-only imports and test sources stay out.
Package imports remain the responsibility of the npm module extractor.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_typescript

from .source_inventory import iter_source_files, is_source_file

_SUFFIXES = ('.ts', '.tsx', '.js', '.jsx')
_TEST = re.compile(r'\.(?:test|spec)\.[cm]?[jt]sx?$|\.d\.[cm]?ts$')
_SAFE_MODULE = re.compile(r'^[A-Za-z0-9_@./$-]+$')


def _id(prefix, *parts):
    return prefix + ':' + hashlib.sha256('|'.join(map(str, parts)).encode()).hexdigest()[:24]


def _jsonc(text):
    """Remove JSON comments and trailing commas without changing quoted strings."""
    output = []; index = 0; quoted = False; escaped = False
    while index < len(text):
        char = text[index]
        if quoted:
            output.append(char)
            if escaped: escaped = False
            elif char == '\\': escaped = True
            elif char == '"': quoted = False
            index += 1; continue
        if char == '"': quoted = True; output.append(char); index += 1; continue
        if text[index:index + 2] == '//':
            end = text.find('\n', index); index = len(text) if end < 0 else end; continue
        if text[index:index + 2] == '/*':
            end = text.find('*/', index + 2)
            if end < 0: raise ValueError('Unclosed configuration comment')
            output.append(' '); index = end + 2; continue
        if char == ',':
            look = index + 1
            while look < len(text) and text[look].isspace(): look += 1
            if look < len(text) and text[look] in '}]': index += 1; continue
        output.append(char); index += 1
    return json.loads(''.join(output))


def _has(node, kind):
    return any(child.type == kind for child in node.children)


def _unit(path, repository):
    encoded = path.read_bytes()
    language = tree_sitter_typescript.language_tsx() if path.suffix in {'.tsx', '.jsx'} else tree_sitter_typescript.language_typescript()
    root = Parser(Language(language)).parse(encoded).root_node
    text = lambda node: encoded[node.start_byte:node.end_byte].decode('utf-8', errors='replace') if node else ''
    unit = {'path': path, 'relative': path.relative_to(repository).as_posix(), 'imports': [], 'exports': {},
            'stars': [], 'definitions': {}, 'locals': {}, 'types': set(), 'type_exports': {}, 'type_stars': [],
            'type_locals': {}, 'parse_error': root.has_error, 'unsupported': []}
    pending = [root]
    while pending:
        item = pending.pop()
        if item.type == 'call_expression':
            function = item.child_by_field_name('function')
            if function and (function.type == 'import' or function.type == 'identifier' and text(function) == 'require'):
                unit['unsupported'].append({'line': item.start_point.row + 1,
                                            'reason': 'DYNAMIC_IMPORT_SYNTAX' if function.type == 'import' else 'COMMONJS_REQUIRE_SYNTAX'})
        pending.extend(item.named_children)

    def definitions(node):
        if node.type in {'lexical_declaration', 'variable_declaration'}:
            return [(text(child.child_by_field_name('name')), child.start_point.row + 1, 'VALUE')
                    for child in node.named_children if child.type == 'variable_declarator'
                    and child.child_by_field_name('name') and child.child_by_field_name('name').type == 'identifier']
        name = node.child_by_field_name('name')
        if node.type in {'function_declaration', 'generator_function_declaration', 'class_declaration',
                         'abstract_class_declaration', 'enum_declaration'} and name:
            return [(text(name), node.start_point.row + 1, node.type.upper())]
        return []

    for node in root.named_children:
        declaration = node.child_by_field_name('declaration') if node.type == 'export_statement' else node
        if declaration:
            for name, line, kind in definitions(declaration):
                unit['definitions'][name] = {'path': path, 'name': name, 'line': line, 'kind': kind}
            if declaration.type in {'interface_declaration', 'type_alias_declaration'}:
                name = declaration.child_by_field_name('name')
                if name: unit['types'].add(text(name))
    for node in root.named_children:
        if node.type not in {'import_statement', 'export_statement'}: continue
        source = node.child_by_field_name('source')
        raw = text(source)
        module = raw[1:-1] if source and len(raw) >= 2 and '\\' not in raw else None
        row = {'line': node.start_point.row + 1, 'module': module, 'bindings': [], 'reexport': node.type == 'export_statement',
               'parse_error': node.has_error, 'type_only': _has(node, 'type')}
        if node.type == 'import_statement':
            clause = next((item for item in node.named_children if item.type == 'import_clause'), None)
            if clause:
                for binding in clause.named_children:
                    if binding.type == 'identifier': row['bindings'].append(('default', text(binding)))
                    elif binding.type == 'namespace_import':
                        name = next((item for item in binding.named_children if item.type == 'identifier'), None)
                        if name: row['bindings'].append(('*', text(name)))
                    elif binding.type == 'named_imports':
                        for specifier in binding.named_children:
                            name = specifier.child_by_field_name('name'); alias = specifier.child_by_field_name('alias')
                            if _has(specifier, 'type'):
                                if name: unit['type_locals'][text(alias or name)] = (module, text(name))
                                continue
                            if name: row['bindings'].append((text(name), text(alias or name)))
                if not row['bindings']: row['type_only'] = True
            if not row['type_only']:
                for imported, local in row['bindings']: unit['locals'][local] = (module, imported)
            else:
                for imported, local in row['bindings']: unit['type_locals'][local] = (module, imported)
            unit['imports'].append(row); continue
        clause = next((item for item in node.named_children if item.type == 'export_clause'), None)
        if clause:
            for specifier in clause.named_children:
                name = specifier.child_by_field_name('name'); alias = specifier.child_by_field_name('alias')
                if name:
                    original, exported = text(name), text(alias or name)
                    if row['type_only'] or _has(specifier, 'type'):
                        unit['type_exports'].setdefault(exported, []).append({'module': module, 'name': original})
                        continue
                    unit['exports'].setdefault(exported, []).append({'module': module, 'name': original})
                    row['bindings'].append((original, exported))
            if source:
                if not row['bindings']: row['type_only'] = True
                unit['imports'].append(row)
            continue
        declaration = node.child_by_field_name('declaration')
        if declaration and declaration.type in {'interface_declaration', 'type_alias_declaration'}:
            name = declaration.child_by_field_name('name')
            if name: unit['type_exports'].setdefault('default' if _has(node, 'default') else text(name), []).append({'module': None, 'name': text(name)})
            continue
        if row['type_only']:
            if source: unit['type_stars'].append(module); unit['imports'].append(row)
            continue
        namespace = next((item for item in node.named_children if item.type == 'namespace_export'), None)
        if namespace:
            name = text(namespace.named_children[0])
            unit['definitions'][name] = {'path': path, 'name': name, 'line': row['line'], 'kind': 'NAMESPACE'}
            unit['exports'].setdefault(name, []).append({'module': None, 'name': name})
            unit['imports'].append(row); continue
        declaration = node.child_by_field_name('declaration')
        if declaration and declaration.type in {'interface_declaration', 'type_alias_declaration', 'ambient_declaration'}: continue
        if _has(node, 'default'):
            value = node.child_by_field_name('value')
            name = text(declaration.child_by_field_name('name')) if declaration and declaration.child_by_field_name('name') else text(value) if value and value.type == 'identifier' else 'default'
            if name not in unit['definitions'] and name not in unit['locals']:
                unit['definitions'][name] = {'path': path, 'name': name, 'line': row['line'], 'kind': 'DEFAULT_VALUE'}
            unit['exports'].setdefault('default', []).append({'module': None, 'name': name})
        elif declaration:
            for name, _, _ in definitions(declaration): unit['exports'].setdefault(name, []).append({'module': None, 'name': name})
        elif source:
            unit['stars'].append(module); unit['imports'].append(row)
    return unit


def add_to_graph(graph, repo: Path, repository: str) -> dict[str, Any]:
    """Add source and exact exported-symbol relationships inside one repository."""
    repo = Path(os.path.abspath(repo)); workspace = Path(os.path.abspath(graph.workspace))
    ledger = []; statistics = Counter(); units = {}; config_cache = {}; source_nodes = {}; symbol_nodes = {}

    def relative(path): return path.relative_to(workspace).as_posix()
    def record(family, path, line, disposition, reason=None, **extra):
        row = {'family': family, 'path': path.relative_to(repo).as_posix(), 'line': line, 'disposition': disposition, **extra}
        if reason: row['reason'] = reason
        ledger.append(row)
    def diagnostic(code, path, message): graph.diagnostic(code, message, repository, relative(path))

    for path in iter_source_files(repo, suffixes=_SUFFIXES):
        if _TEST.search(path.name):
            record('web_source_file', path, 1, 'EXCLUDED', 'TYPE_DECLARATION_OR_TEST'); continue
        try:
            if path.stat().st_size > 2 * 1024 * 1024:
                record('web_source_file', path, 1, 'UNRESOLVED', 'SOURCE_SIZE_LIMIT'); continue
            unit = _unit(path, repo)
        except (OSError, ValueError) as error:
            diagnostic('UNREADABLE_WEB_SOURCE', path, 'Cannot parse source module: ' + type(error).__name__)
            record('web_source_file', path, 1, 'UNRESOLVED', 'UNREADABLE_WEB_SOURCE'); continue
        units[path] = unit
        record('web_source_file', path, 1, 'UNRESOLVED' if unit['parse_error'] else 'EXTRACTED',
               'SOURCE_PARSE_ERROR' if unit['parse_error'] else None)
        if unit['parse_error']: diagnostic('WEB_SOURCE_PARSE_ERROR', path, 'Source contains parse errors; supported declarations remain partial')
        for row in unit['unsupported']:
            record('web_source_import', path, row['line'], 'UNRESOLVED', row['reason'])
            diagnostic('UNSUPPORTED_WEB_IMPORT_SYNTAX', path, row['reason'] + ' requires a separate extraction rule')
    statistics['source_files'] = len(units)
    paths = set(units)

    def load_config(path, stack=()):
        if path in config_cache: return config_cache[path]
        if path in stack or not path.is_relative_to(repo) or not is_source_file(repo, path): return None
        try: document = _jsonc(path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            diagnostic('UNREADABLE_WEB_ALIAS_CONFIG', path, 'Cannot read tsconfig/jsconfig JSON declarations'); return None
        if not isinstance(document, dict):
            diagnostic('UNREADABLE_WEB_ALIAS_CONFIG', path, 'Configuration must contain a JSON object'); return None
        config = {'base': path.parent, 'paths': {}, 'base_declared': False}
        extended = document.get('extends')
        if isinstance(extended, str):
            parent = Path(os.path.abspath(path.parent / extended))
            if not parent.suffix: parent = parent.with_suffix('.json')
            if not extended.startswith('.') or not parent.is_relative_to(repo):
                diagnostic('UNSUPPORTED_WEB_ALIAS_CONFIG', path, 'External tsconfig inheritance is not resolved')
            else:
                inherited = load_config(parent, (*stack, path))
                if inherited: config = dict(inherited)
        options = document.get('compilerOptions', {})
        if isinstance(options, dict):
            if isinstance(options.get('baseUrl'), str):
                config['base'] = Path(os.path.abspath(path.parent / options['baseUrl'])); config['base_declared'] = True
            if isinstance(options.get('paths'), dict):
                # Each binding retains the base from the declaring configuration.
                config['paths'] = {key: (config['base'] if config['base_declared'] else path.parent, value) for key, value in options['paths'].items()
                                   if isinstance(key, str) and isinstance(value, list) and all(isinstance(item, str) for item in value)}
        config_cache[path] = config; return config

    def config_for(path):
        for directory in [path.parent, *path.parent.parents]:
            if not directory.is_relative_to(repo): break
            for name in ('tsconfig.json', 'jsconfig.json'):
                candidate = directory / name
                if is_source_file(repo, candidate): return load_config(candidate)
        return None

    def candidates(path, module):
        if not module or not _SAFE_MODULE.fullmatch(module): return [], 'UNSUPPORTED'
        bases = []; kind = 'LOCAL' if module.startswith('.') else 'PACKAGE'
        if kind == 'LOCAL': bases.append(path.parent / module)
        else:
            config = config_for(path)
            if config:
                matches = []
                for pattern, (base, targets) in config['paths'].items():
                    if pattern.count('*') > 1: continue
                    prefix, _, suffix = pattern.partition('*')
                    if ('*' not in pattern and pattern == module) or ('*' in pattern and module.startswith(prefix) and module.endswith(suffix) and len(module) >= len(prefix) + len(suffix)):
                        capture = module[len(prefix):len(module)-len(suffix) if suffix else None] if '*' in pattern else ''
                        matches.append((1000000 + len(pattern) if '*' not in pattern else len(prefix), pattern, base, targets, capture))
                if matches:
                    best = max(item[0] for item in matches)
                    for score, pattern, base, targets, capture in matches:
                        if score != best: continue
                        bases.extend(base / target.replace('*', capture) for target in targets)
                    kind = 'LOCAL'
                elif config['base_declared']:
                    bases.append(config['base'] / module)
        result = set()
        for base in bases:
            base = Path(os.path.abspath(base))
            if not base.is_relative_to(repo): continue
            options = [base] if base.suffix in _SUFFIXES else [Path(str(base) + suffix) for suffix in _SUFFIXES] + [base / ('index' + suffix) for suffix in _SUFFIXES]
            if base.suffix in {'.js', '.jsx'}: options.extend(base.with_suffix(suffix) for suffix in ('.ts', '.tsx'))
            result.update(item for item in options if item in paths)
        if result: kind = 'LOCAL'
        return sorted(result), kind

    def exports(path, name, visited=frozenset()):
        key = path, name
        if key in visited or path not in units or len(visited) >= 128: return []
        visited = visited | {key}; unit = units[path]; result = []
        bindings = unit['exports'].get(name, [])
        for binding in bindings:
            if binding['module']:
                targets, _ = candidates(path, binding['module'])
                if len(targets) == 1: result.extend(exports(targets[0], binding['name'], visited))
            elif binding['name'] in unit['definitions']: result.append(unit['definitions'][binding['name']])
            elif binding['name'] in unit['locals']:
                module, imported = unit['locals'][binding['name']]; targets, _ = candidates(path, module)
                if len(targets) == 1 and imported != '*': result.extend(exports(targets[0], imported, visited))
        if not bindings and name != 'default':
            for module in unit['stars']:
                targets, _ = candidates(path, module)
                if len(targets) == 1: result.extend(exports(targets[0], name, visited))
        return list({(item['path'], item['name']): item for item in result}.values())

    def is_type_export(path, name, visited=frozenset()):
        key = path, name
        if key in visited or path not in units or len(visited) >= 128: return False
        visited = visited | {key}; unit = units[path]
        bindings = unit['type_exports'].get(name, []) + unit['exports'].get(name, [])
        for binding in bindings:
            if binding['module']:
                targets, _ = candidates(path, binding['module'])
                if len(targets) == 1 and is_type_export(targets[0], binding['name'], visited): return True
            elif binding['name'] in unit['types']: return True
            else:
                local = unit['locals'].get(binding['name']) or unit['type_locals'].get(binding['name'])
                if local:
                    targets, _ = candidates(path, local[0])
                    if len(targets) == 1 and is_type_export(targets[0], local[1], visited): return True
        if not bindings and name != 'default':
            for module in unit['type_stars'] + unit['stars']:
                targets, _ = candidates(path, module)
                if len(targets) == 1 and is_type_export(targets[0], name, visited): return True
        return False

    # Reuse only exact existing component paths; directory scopes cannot prove identity.
    existing = {}
    for node in list(graph.nodes.values()):
        if node.get('repository') == repository and node['type'] == 'COMPONENT' and node.get('component_kind') != 'EXPORTED_SYMBOL':
            for path in node.get('source_paths', []):
                if '*' not in path: existing.setdefault(path, []).append(node['id'])

    def module_node(path):
        if path in source_nodes: return source_nodes[path]
        known = existing.get(relative(path), [])
        if len(known) == 1: identifier = known[0]
        else:
            identifier = _id('source-module', repository, relative(path))
            ev = graph.add_evidence(repository, relative(path), 1, 'Source module ' + path.name, 'web-source-module')
            graph.add_node(identifier, 'COMPONENT', path.name, repository, dimensions=('RUNTIME', 'BUSINESS'),
                           component_kind='SOURCE_MODULE', functional_role='Contains static ES module declarations',
                           business_meaning='Groups source dependencies for repository analysis', source_paths=(relative(path),),
                           evidence=(ev,), properties={'detail_level': 'MODULE', 'language': 'TYPESCRIPT' if path.suffix in {'.ts', '.tsx'} else 'JAVASCRIPT'})
        source_nodes[path] = identifier; return identifier

    def symbol_node(origin):
        key = origin['path'], origin['name']
        if key not in symbol_nodes:
            path = origin['path']; identifier = _id('exported-symbol', repository, relative(path), origin['name'])
            ev = graph.add_evidence(repository, relative(path), origin['line'], 'Declares exported value ' + origin['name'], 'web-exported-symbol')
            graph.add_node(identifier, 'COMPONENT', origin['name'], repository, dimensions=('RUNTIME', 'BUSINESS'),
                           component_kind='EXPORTED_SYMBOL', functional_role='Declares an exported source value',
                           business_meaning='Provides an importable source value; execution is not established',
                           source_paths=(relative(path),), evidence=(ev,), properties={'detail_level': 'EXPORTED_SYMBOL', 'symbol_kind': origin['kind'], 'symbol': origin['name']})
            graph.add_edge(module_node(path), identifier, 'EXPORTS_SYMBOL', 'RUNTIME', (ev,))
            symbol_nodes[key] = identifier
        return symbol_nodes[key]

    for path, unit in sorted(units.items()):
        module_node(path)
        for name in unit['exports']:
            for origin in exports(path, name): symbol_node(origin)
        for row in unit['imports']:
            statistics['import_declarations'] += 1
            if row['type_only']:
                record('web_source_import', path, row['line'], 'EXCLUDED', 'TYPE_ONLY_IMPORT'); continue
            if row['parse_error']:
                record('web_source_import', path, row['line'], 'UNRESOLVED', 'SOURCE_PARSE_ERROR'); continue
            targets, kind = candidates(path, row['module'])
            if kind == 'PACKAGE':
                record('web_source_import', path, row['line'], 'EXCLUDED', 'PACKAGE_IMPORT_HANDLED_SEPARATELY'); continue
            if len(targets) != 1:
                reason = 'AMBIGUOUS_WEB_SOURCE_IMPORT' if len(targets) > 1 else 'UNSUPPORTED_WEB_SOURCE_IMPORT' if kind == 'UNSUPPORTED' else 'UNRESOLVED_WEB_SOURCE_IMPORT'
                diagnostic(reason, path, 'Static source import has no unique supported provider')
                record('web_source_import', path, row['line'], 'UNRESOLVED', reason,
                       **({'candidate_paths': [item.relative_to(repo).as_posix() for item in targets]} if targets else {})); continue
            target = targets[0]
            value_bindings = []
            for name, local in row['bindings']:
                if name != '*' and not exports(target, name) and is_type_export(target, name):
                    record('web_symbol_import', path, row['line'], 'EXCLUDED', 'TYPE_ONLY_EXPORTED_SYMBOL', symbol=name)
                else: value_bindings.append((name, local))
            if row['bindings'] and not value_bindings:
                record('web_source_import', path, row['line'], 'EXCLUDED', 'TYPE_ONLY_EXPORTED_BINDINGS'); continue
            source_id = module_node(path); target_id = module_node(target)
            ev = graph.add_evidence(repository, relative(path), row['line'], ('Re-exports from ' if row['reexport'] else 'Imports source ') + row['module'], 'web-source-import')
            provider_ev = graph.nodes[target_id]['evidence']
            bindings = [name + (' as ' + local if name != local else '') for name, local in value_bindings]
            graph.add_edge(source_id, target_id, 'IMPORTS_SOURCE', 'RUNTIME', (ev, *provider_ev), resolution_status='RESOLVED',
                           properties={'modules': [row['module']], 'bindings': bindings, 'import_kinds': ['REEXPORT' if row['reexport'] else 'IMPORT'],
                                       'dependency_kind': 'SOURCE', 'resolution_rule': 'exact-repository-source-import'})
            record('web_source_import', path, row['line'], 'EXTRACTED'); statistics['resolved_source_imports'] += 1
            for name, local in value_bindings:
                if name == '*': continue
                origins = exports(target, name)
                if len(origins) != 1:
                    reason = 'AMBIGUOUS_WEB_SYMBOL_IMPORT' if len(origins) > 1 else 'UNRESOLVED_WEB_SYMBOL_IMPORT'
                    diagnostic(reason, path, 'Imported value ' + name + ' has no unique exported declaration')
                    record('web_symbol_import', path, row['line'], 'UNRESOLVED', reason, symbol=name); continue
                identifier = symbol_node(origins[0])
                graph.add_edge(source_id, identifier, 'IMPORTS_SYMBOL', 'RUNTIME', (ev, *graph.nodes[identifier]['evidence']),
                               resolution_status='RESOLVED', properties={'modules': [row['module']], 'symbols': [name], 'bindings': [local],
                               'dependency_kind': 'SOURCE', 'resolution_rule': 'exact-exported-value-binding'})
                record('web_symbol_import', path, row['line'], 'EXTRACTED', symbol=name); statistics['resolved_symbol_imports'] += 1
    statistics['source_modules'] = len(source_nodes); statistics['exported_symbols'] = len(symbol_nodes)
    statistics['barrel_depth_limit'] = 128
    statistics['ledger_counts'] = dict(sorted(Counter(row['family'] + ':' + row['disposition'] for row in ledger).items()))
    return {'ledger': ledger, 'statistics': dict(statistics)}


__all__ = ['add_to_graph']
