"""Retain declarative JPA mappings and bounded native SQL column references.

Mappings and query text do not establish execution. Unknown naming strategies,
datasources, dynamic identifiers, and SQL wildcards remain explicit limits.
"""
from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_java

from .source_inventory import iter_source_files
from . import source_inventory


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _id(prefix, *parts):
    return prefix + ':' + hashlib.sha256('|'.join(map(str, parts)).encode()).hexdigest()[:24]


def _literal(value):
    value = value.strip()
    try:
        if value.startswith('"""') and value.endswith('"""'):
            # Text block indentation does not affect SQL token identities.
            return value[3:-3]
        result = json.loads(value)
        return result if isinstance(result, str) else None
    except (ValueError, TypeError):
        return None


def _annotations(node):
    modifiers = next((child for child in node.named_children if child.type == 'modifiers'), None)
    return [child for child in modifiers.named_children
            if child.type in {'annotation', 'marker_annotation'}] if modifiers else []


def _arguments(annotation, text):
    arguments = annotation.child_by_field_name('arguments')
    result = {}
    if arguments:
        for child in arguments.named_children:
            if child.type == 'element_value_pair':
                result[text(child.child_by_field_name('key'))] = child.child_by_field_name('value')
            else:
                result['value'] = child
    return result


def extract(repo: Path) -> dict:
    """Return declarations without guessing physical ORM names or execution."""
    repo = repo.resolve()
    files, constants = [], {}
    result = {'entities': [], 'repositories': [], 'queries': [], 'diagnostics': [], 'ledger': []}
    roots = source_inventory.java_source_roots(repo)
    paths = sorted({path for root in roots for path in iter_source_files(repo, root=root, suffixes={'.java'})})
    for path in paths:
        encoded = path.read_bytes()
        root = Parser(Language(tree_sitter_java.language())).parse(encoded).root_node
        def text(node, encoded=encoded):
            return encoded[node.start_byte:node.end_byte].decode('utf-8', errors='replace') if node else ''
        package = next((text(n).removeprefix('package').strip().rstrip(';')
                        for n in root.named_children if n.type == 'package_declaration'), '')
        imports = [text(n).removeprefix('import').strip().rstrip(';')
                   for n in root.named_children if n.type == 'import_declaration']
        unit = {'path': path.relative_to(repo).as_posix(), 'root': root, 'text': text,
                'package': package, 'imports': imports}
        files.append(unit)
        if root.has_error:
            result['diagnostics'].append({'code': 'ORM_JAVA_PARSE_ERROR', 'path': unit['path'], 'line': 1,
                                          'declaration': 'Java parse error',
                                          'message': 'Java source has parse errors; ORM extraction can be incomplete.'})
        for node in _walk(root):
            if node.type not in {'field_declaration', 'constant_declaration'}:
                continue
            modifiers = next((text(n) for n in node.named_children if n.type == 'modifiers'), '')
            owner = node.parent.parent if node.parent else None
            if not owner or text(node.child_by_field_name('type')) not in {'String', 'java.lang.String'}:
                continue
            if owner.type != 'interface_declaration' and not {'static', 'final'} <= set(modifiers.split()):
                continue
            owner_name = text(owner.child_by_field_name('name'))
            for variable in node.named_children:
                if variable.type == 'variable_declarator':
                    value = _literal(text(variable.child_by_field_name('value')))
                    if value is not None:
                        key = '.'.join(filter(None, [package, owner_name, text(variable.child_by_field_name('name'))]))
                        constants.setdefault(key, []).append(value)

    def record(unit, node):
        declaration = unit['text'](node)
        if node.type in {'class_declaration', 'interface_declaration'}:
            # Type evidence needs its identity and signature. Class bodies can
            # contain secret initializers, annotation defaults, and query data.
            # Annotation names retain the declaration context without values.
            body = node.child_by_field_name('body')
            modifiers = next((child for child in node.named_children if child.type == 'modifiers'), None)
            start = modifiers.end_byte if modifiers else node.start_byte
            end = body.start_byte if body else node.end_byte
            header = declaration.encode('utf-8')[start - node.start_byte:end - node.start_byte].decode('utf-8').strip()
            markers = ['@' + unit['text'](annotation.child_by_field_name('name'))
                       for annotation in _annotations(node)]
            declaration = ' '.join([*markers, header])
        return {'path': unit['path'], 'line': node.start_point.row + 1,
                'declaration': declaration[:500]}

    def diagnostic(unit, node, code, message):
        result['diagnostics'].append({**record(unit, node), 'code': code, 'message': message})

    def resolve(unit, node, owner=''):
        expression = unit['text'](node).strip()
        literal = _literal(expression)
        if literal is not None:
            return literal
        if node and node.type == 'binary_expression' and unit['text'](node.child_by_field_name('operator')) == '+':
            left, right = resolve(unit, node.child_by_field_name('left'), owner), resolve(unit, node.child_by_field_name('right'), owner)
            return left + right if left is not None and right is not None else None
        if not re.fullmatch(r'[\w$]+(?:\.[\w$]+)*', expression):
            return None
        identities = {expression, '.'.join(filter(None, [unit['package'], expression])),
                      '.'.join(filter(None, [unit['package'], owner, expression]))}
        for imported in unit['imports']:
            if imported.startswith('static '):
                imported = imported[7:]
                if imported.endswith('.*'):
                    identities.add(imported[:-2] + '.' + expression)
                elif imported.rsplit('.', 1)[-1] == expression:
                    identities.add(imported)
            elif '.' in expression and imported.rsplit('.', 1)[-1] == expression.split('.')[0]:
                identities.add(imported + expression[expression.find('.'):])
        values = [value for identity in identities for value in constants.get(identity, [])]
        return values[0] if len(values) == 1 else None

    def annotation_name(unit, node, namespaces):
        name = unit['text'](node.child_by_field_name('name'))
        for namespace in namespaces:
            if name.startswith(namespace + '.'):
                return name.rsplit('.', 1)[-1]
            if namespace + '.*' in unit['imports'] or namespace + '.' + name in unit['imports']:
                return name
        return None

    for unit in files:
        text = unit['text']
        for node in _walk(unit['root']):
            if node.type != 'class_declaration':
                continue
            annotations = {annotation_name(unit, n, ('jakarta.persistence', 'javax.persistence')): n
                           for n in _annotations(node)}
            if 'Entity' not in annotations:
                continue
            name = text(node.child_by_field_name('name'))
            qualified = '.'.join(filter(None, [unit['package'], name]))
            table_node = annotations.get('Table')
            args = _arguments(table_node, text) if table_node else {}
            table = resolve(unit, args.get('name'), name) if args.get('name') else None
            schema = resolve(unit, args.get('schema'), name) if args.get('schema') else None
            entity = {**record(unit, node), 'name': name, 'qualified_name': qualified,
                      'table': table, 'schema': schema, 'datasource': None, 'columns': [],
                      'table_expression': text(args.get('name')) or None,
                      'schema_expression': text(args.get('schema')) or None}
            if not table:
                diagnostic(unit, table_node or annotations['Entity'], 'UNRESOLVED_ORM_TABLE_NAME',
                           'Physical table name requires an explicit name and naming strategy evidence.')
            if args.get('schema') and schema is None:
                diagnostic(unit, table_node, 'UNRESOLVED_ORM_SCHEMA', 'Schema expression is not a unique static string.')
            body = node.child_by_field_name('body')
            for member in body.named_children if body else []:
                if member.type not in {'field_declaration', 'method_declaration'}:
                    continue
                for annotation in _annotations(member):
                    if annotation_name(unit, annotation, ('jakarta.persistence', 'javax.persistence')) != 'Column':
                        continue
                    column_args = _arguments(annotation, text)
                    physical = resolve(unit, column_args.get('name'), name) if column_args.get('name') else None
                    variables = [n for n in member.named_children if n.type == 'variable_declarator']
                    if len(variables) > 1:
                        diagnostic(unit, annotation, 'UNSUPPORTED_ORM_MULTI_FIELD',
                                   'One column annotation applies to multiple field declarations.')
                        result['ledger'].append({**record(unit, annotation), 'family': 'ORM_COLUMN', 'disposition': 'UNRESOLVED'})
                        continue
                    field = text(variables[0].child_by_field_name('name')) if len(variables) == 1 else text(member.child_by_field_name('name'))
                    column = {**record(unit, annotation), 'field': field, 'name': physical,
                              'name_expression': text(column_args.get('name')) or None,
                              'naming_status': 'EXPLICIT' if physical else 'UNKNOWN',
                              'attributes': {k: text(v) for k, v in column_args.items() if k != 'name'}}
                    entity['columns'].append(column)
                    result['ledger'].append({**column, 'family': 'ORM_COLUMN',
                                             'disposition': 'EXTRACTED' if physical else 'UNRESOLVED'})
                    if not physical:
                        diagnostic(unit, annotation, 'UNRESOLVED_ORM_COLUMN_NAME',
                                   'Column declaration is retained; physical naming strategy is unknown.')
            result['entities'].append(entity)
            result['ledger'].append({**record(unit, annotations['Entity']), 'family': 'ORM_ENTITY', 'disposition': 'EXTRACTED'})

    entities_by_simple = {}
    for entity in result['entities']:
        entities_by_simple.setdefault(entity['name'], []).append(entity)
    for unit in files:
        text = unit['text']
        for node in _walk(unit['root']):
            if node.type == 'interface_declaration':
                declaration = text(node)
                match = re.search(r'\bextends\s+([\w.]+)\s*<\s*([\w.]+)\s*,', declaration)
                if match and match[1].rsplit('.', 1)[-1] in {'JpaRepository', 'CrudRepository', 'PagingAndSortingRepository'}:
                    spring = ('org.springframework.data.jpa.repository.', 'org.springframework.data.repository.')
                    recognized = (match[1].startswith(spring) or any(
                        i in {p + match[1], p + '*'} for p in spring for i in unit['imports']))
                    if recognized:
                        candidates = entities_by_simple.get(match[2].rsplit('.', 1)[-1], [])
                        qualified = {match[2], '.'.join(filter(None, [unit['package'], match[2]])), *unit['imports']}
                        candidates = [e for e in candidates if e['qualified_name'] in qualified or
                                      e['qualified_name'].rsplit('.', 1)[0] + '.*' in unit['imports']]
                        entity = candidates[0]['qualified_name'] if len(candidates) == 1 else None
                        operations = [text(n.child_by_field_name('name')) for n in _walk(node) if n.type == 'method_declaration']
                        row = {**record(unit, node), 'name': text(node.child_by_field_name('name')),
                               'entity': entity, 'entity_expression': match[2], 'base_repository': match[1],
                               'declared_operations': operations, 'candidate_entities': [e['qualified_name'] for e in candidates]}
                        result['repositories'].append(row)
                        result['ledger'].append({**record(unit, node), 'family': 'ORM_REPOSITORY',
                                                 'disposition': 'EXTRACTED' if entity else 'UNRESOLVED'})
                        if not entity:
                            diagnostic(unit, node, 'UNRESOLVED_ORM_REPOSITORY_ENTITY',
                                       'Repository entity identity is missing or ambiguous.')
            if node.type not in {'annotation', 'marker_annotation'}:
                continue
            if annotation_name(unit, node, ('org.springframework.data.jpa.repository',)) != 'Query':
                continue
            args = _arguments(node, text)
            if text(args.get('nativeQuery')) != 'true':
                continue
            sql = resolve(unit, args.get('value'))
            if sql is None:
                diagnostic(unit, node, 'UNRESOLVED_SQL_EXPRESSION', 'Native query text is not a unique static string.')
                result['ledger'].append({**record(unit, node), 'family': 'SQL', 'disposition': 'UNRESOLVED'})
                continue
            query = {**record(unit, node), 'client': 'NATIVE_QUERY', **sql_columns(sql)}
            result['queries'].append(query)
            result['ledger'].append({**record(unit, node), 'family': 'SQL', 'disposition': 'EXTRACTED',
                                     'limitations': query['limits']})
            for code in query['limits']:
                diagnostic(unit, node, code, 'SQL column extraction retains a bounded syntax or identity limit.')
        jdbc_types = {'org.springframework.jdbc.core.JdbcTemplate',
                      'org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate'}
        receivers = {}
        def enclosing_class(node):
            owner = node.parent
            while owner and owner.type not in {'class_declaration', 'record_declaration', 'enum_declaration'}:
                owner = owner.parent
            return owner.start_byte if owner else None
        for declaration in _walk(unit['root']):
            if declaration.type != 'field_declaration':
                continue
            type_name = text(declaration.child_by_field_name('type'))
            if not any(type_name == name or (type_name == name.rsplit('.', 1)[-1] and
                       (name in unit['imports'] or name.rsplit('.', 1)[0] + '.*' in unit['imports']))
                       for name in jdbc_types):
                continue
            for variable in declaration.named_children:
                if variable.type == 'variable_declarator':
                    receivers.setdefault(enclosing_class(declaration), set()).add(text(variable.child_by_field_name('name')))
        for invocation in _walk(unit['root']):
            if invocation.type != 'method_invocation':
                continue
            receiver = text(invocation.child_by_field_name('object'))
            method = text(invocation.child_by_field_name('name'))
            fields = receivers.get(enclosing_class(invocation), set())
            if receiver.removeprefix('this.') not in fields or method not in {
                    'query', 'queryForObject', 'queryForList', 'queryForMap', 'update', 'execute', 'batchUpdate'}:
                continue
            # Bare field names can be shadowed by local declarations.
            owner = invocation.parent
            while owner and owner.type not in {'method_declaration', 'constructor_declaration'}:
                owner = owner.parent
            if receiver in fields and owner and any(
                    text(n.child_by_field_name('name')) == receiver
                    for n in _walk(owner) if n.type in {'variable_declarator', 'formal_parameter'}):
                diagnostic(unit, invocation, 'AMBIGUOUS_JDBC_RECEIVER', 'A local declaration can shadow the JDBC field.')
                result['ledger'].append({**record(unit, invocation), 'family': 'SQL', 'disposition': 'UNRESOLVED'})
                continue
            arguments = invocation.child_by_field_name('arguments')
            value = arguments.named_children[0] if arguments and arguments.named_children else None
            sql = resolve(unit, value)
            if sql is None:
                diagnostic(unit, invocation, 'UNRESOLVED_SQL_EXPRESSION', 'JDBC query text is not a unique static string.')
                result['ledger'].append({**record(unit, invocation), 'family': 'SQL', 'disposition': 'UNRESOLVED'})
                continue
            query = {**record(unit, invocation), 'client': 'JDBC_TEMPLATE', **sql_columns(sql)}
            result['queries'].append(query)
            result['ledger'].append({**record(unit, invocation), 'family': 'SQL', 'disposition': 'EXTRACTED',
                                     'limitations': query['limits']})
            for code in query['limits']:
                diagnostic(unit, invocation, code, 'SQL column extraction retains a bounded syntax or identity limit.')
    for resource_root in source_inventory.resource_source_roots(repo):
        for path in iter_source_files(repo, root=resource_root, suffixes={'.xml'}):
            original = path.read_text(encoding='utf-8', errors='replace')
            try:
                document = ET.fromstring(original)
            except ET.ParseError:
                if re.search(r'<mapper\b', original):
                    result['diagnostics'].append({'code': 'MYBATIS_SQL_PARSE_ERROR', 'path': path.relative_to(repo).as_posix(),
                                                  'line': 1, 'declaration': '<mapper>', 'message': 'Mapper XML is not parseable.'})
                continue
            if document.tag.rsplit('}', 1)[-1] != 'mapper':
                continue
            for statement in document:
                kind = statement.tag.rsplit('}', 1)[-1]
                if kind not in {'select', 'insert', 'update', 'delete'}:
                    continue
                identity = statement.get('id', '')
                start = re.search(r'<' + kind + r'\b[^>]*\bid\s*=\s*[\'"]' + re.escape(identity) + r'[\'"]', original)
                line = original.count('\n', 0, start.start()) + 1 if start else 1
                row = {'path': path.relative_to(repo).as_posix(), 'line': line,
                       'declaration': ET.tostring(statement, encoding='unicode')[:500]}
                sql = ''.join(statement.itertext())
                if len(statement) or '${' in sql:
                    result['diagnostics'].append({**row, 'code': 'UNRESOLVED_MYBATIS_SQL',
                                                  'message': 'Dynamic mapper SQL or included fragments require unsupported evaluation.'})
                    result['ledger'].append({**row, 'family': 'SQL', 'disposition': 'UNRESOLVED'})
                    continue
                sql = re.sub(r'#\{[^}]+\}', ':parameter', sql)
                query = {**row, 'client': 'MYBATIS_MAPPER', 'mapper_statement': identity, **sql_columns(sql.strip())}
                result['queries'].append(query)
                result['ledger'].append({**row, 'family': 'SQL', 'disposition': 'EXTRACTED', 'limitations': query['limits']})
                result['diagnostics'].extend({**row, 'code': code,
                                              'message': 'SQL column extraction retains a bounded syntax or identity limit.'}
                                             for code in query['limits'])
    return result


_TOKEN = re.compile(r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])+\"|[A-Za-z_][\w$]*|\d+(?:\.\d+)?|[^\s]")
_KEYWORDS = set('SELECT DISTINCT FROM JOIN INNER LEFT RIGHT FULL OUTER CROSS NATURAL ON USING WHERE AND OR NOT IN IS NULL TRUE FALSE AS ORDER BY GROUP HAVING LIMIT OFFSET ASC DESC UPDATE SET INSERT INTO VALUES DELETE RETURNING LIKE BETWEEN EXISTS CASE WHEN THEN ELSE END UNION ALL FETCH FOR ONLY OVER FILTER WINDOW'.split())


def sql_columns(sql: str) -> dict:
    """Extract simple SQL references; reject nested/union syntax explicitly."""
    sql = re.sub(r'/\*.*?\*/|--[^\n]*', ' ', sql, flags=re.S)
    tokens = [m.group() for m in _TOKEN.finditer(sql)]
    upper = [token.upper() for token in tokens]
    result = {'statement_kind': upper[0] if upper else 'UNKNOWN', 'tables': [], 'columns': [], 'limits': []}
    if '${' in sql or '#{' in sql:
        result['limits'].append('UNRESOLVED_SQL_IDENTIFIER')
        return result
    if not upper or upper[0] not in {'SELECT', 'INSERT', 'UPDATE', 'DELETE'}:
        result['limits'].append('UNSUPPORTED_SQL_STATEMENT')
        return result
    if (upper.count('SELECT') > 1 or result['statement_kind'] != 'SELECT' and 'SELECT' in upper
            or {'UNION', 'OVER', 'WINDOW'} & set(upper) or ';' in tokens[:-1]):
        result['limits'].append('UNSUPPORTED_COMPLEX_SQL')
        return result
    identifier = lambda token: bool(re.fullmatch(r'[A-Za-z_][\w$]*|"(?:""|[^"])+"', token))
    clean = lambda token: token[1:-1].replace('""', '"') if token.startswith('"') else token.lower()
    consumed, aliases = set(), {}
    def bind_alias(alias, table):
        if alias in aliases and aliases[alias] != table:
            aliases[alias] = None
        elif alias not in aliases:
            aliases[alias] = table
    def table_at(index):
        start = index
        names = []
        if index >= len(tokens) or not identifier(tokens[index]) or upper[index] in _KEYWORDS:
            return index
        names.append(clean(tokens[index])); index += 1
        while index + 1 < len(tokens) and tokens[index] == '.' and identifier(tokens[index + 1]):
            names.append(clean(tokens[index + 1])); index += 2
        if index < len(tokens) and tokens[index] == '(' and upper[start - 1] in {'FROM', 'JOIN'}:
            result['limits'].append('UNSUPPORTED_SQL_TABLE_EXPRESSION')
            return index
        table = {'name': names[-1], 'schema': '.'.join(names[:-1]) or None, 'datasource': None}
        result['tables'].append(table)
        bind_alias(table['name'], table)
        if index < len(tokens) and upper[index] == 'AS':
            index += 1
        if index < len(tokens) and identifier(tokens[index]) and upper[index] not in _KEYWORDS:
            bind_alias(clean(tokens[index]), table)
            index += 1
        consumed.update(range(start, index))
        return index
    index, in_from = 0, False
    while index < len(tokens):
        if upper[index] in {'FROM', 'JOIN', 'UPDATE', 'INTO'}:
            in_from = upper[index] in {'FROM', 'JOIN'}
            index = table_at(index + 1)
            continue
        if upper[index] in {'WHERE', 'ON', 'USING', 'SET', 'VALUES', 'GROUP', 'ORDER', 'HAVING', 'RETURNING'}:
            in_from = False
        if tokens[index] == ',' and in_from:
            index = table_at(index + 1)
            continue
        index += 1
    unique = {(t['schema'], t['name']): t for t in result['tables']}
    result['tables'] = list(unique.values())
    # Bare SELECT aliases are labels, not column declarations.
    projection_aliases = set()
    if result['statement_kind'] == 'SELECT' and 'FROM' in upper:
        end = upper.index('FROM')
        for position in range(2, end):
            if upper[position - 1] == 'AS' and identifier(tokens[position]):
                projection_aliases.add(clean(tokens[position]))
            if (identifier(tokens[position]) and upper[position] not in _KEYWORDS
                    and tokens[position - 1] != '.' and upper[position - 1] != 'AS'
                    and (identifier(tokens[position - 1]) or tokens[position - 1] == ')')
                    and position + 1 < len(tokens) and tokens[position + 1] in {',', 'FROM', 'from'}):
                consumed.add(position)
                projection_aliases.add(clean(tokens[position]))
    seen, clause = set(), 'PROJECTION'
    for index, token in enumerate(tokens):
        if index in consumed:
            continue
        word = upper[index]
        if word in {'WHERE', 'ON', 'HAVING'}: clause = 'PREDICATE'
        elif word == 'SET': clause = 'ASSIGNMENT'
        elif word in {'ORDER', 'GROUP'}: clause = word
        elif word == 'RETURNING': clause = 'RETURNING'
        elif word == 'VALUES': clause = 'VALUES'
        if token == '*' and (index == 0 or tokens[index - 1] in {'.', 'SELECT', 'select', ','}):
            result['limits'].append('SQL_WILDCARD_COLUMN_SET')
        if not identifier(token) or word in _KEYWORDS or token.startswith("'"):
            continue
        if index and tokens[index - 1] in {'.', ':', '@'}:
            continue
        if index and upper[index - 1] == 'AS':
            continue
        if clause in {'ORDER', 'GROUP'} and clean(token) in projection_aliases:
            continue
        if index + 1 < len(tokens) and tokens[index + 1] == '(':
            continue
        if index + 2 < len(tokens) and tokens[index + 1] == '.':
            parts, next_index = [clean(token)], index + 1
            while next_index + 1 < len(tokens) and tokens[next_index] == '.' and identifier(tokens[next_index + 1]):
                parts.append(clean(tokens[next_index + 1])); next_index += 2
            if len(parts) < 2:
                continue
            if len(parts) == 2:
                table = aliases.get(parts[0])
            else:
                matches = [t for t in result['tables'] if t['schema'] == '.'.join(parts[:-2]) and t['name'] == parts[-2]]
                table = matches[0] if len(matches) == 1 else None
            column = parts[-1]
        else:
            table = result['tables'][0] if len(result['tables']) == 1 else None
            column = clean(token)
        if table is None:
            result['limits'].append('AMBIGUOUS_SQL_COLUMN')
            continue
        role = clause
        if result['statement_kind'] == 'INSERT' and 'VALUES' not in upper[:index]: role = 'INSERT'
        key = (table['schema'], table['name'], column, role)
        if key not in seen:
            seen.add(key)
            result['columns'].append({'table': table, 'name': column, 'role': role})
    result['limits'] = sorted(set(result['limits']))
    return result


def add_to_graph(graph, repo: Path, repository: str, component_by_path: dict[str, str]) -> dict:
    """Add source-backed mapping detail without modifying legacy facts."""
    extracted = extract(repo)
    entities, table_ids, evidence_by_entity = {}, {}, {}
    def evidence(row, extractor):
        path = (repo / row['path']).relative_to(graph.workspace).as_posix()
        return path, graph.add_evidence(repository, path, row['line'], row['declaration'], extractor)
    def node(node_id, kind, name, row, ev, properties):
        graph.add_node(node_id, kind, name, repository, dimensions=('RUNTIME',), component_kind=None,
                       functional_role='Retains a declared data mapping or SQL reference',
                       business_meaning='Source declaration does not establish database execution',
                       source_paths=(row,), evidence=ev, properties=properties)
        return node_id
    def table(name, schema, logical, path, ev, scope_hint=None):
        identity = _id('orm-table', repository, 'UNKNOWN_DATASOURCE', schema or 'UNKNOWN_SCHEMA', name or logical,
                       scope_hint or '')
        # Reuse only the same unqualified source declaration. Legacy tables
        # omit schema identity, so a schema-qualified mapping stays separate.
        legacy = f"table:{repo.name}:" + re.sub(r'[^a-z0-9]+', '-', (name or '').lower()).strip('-')
        existing = graph.nodes.get(legacy)
        reuse = (name and schema is None and existing and existing.get('type') == 'TABLE' and existing.get('name') == name
                 and existing.get('properties', {}).get('schema') is None
                 and path in existing.get('source_paths', []))
        if reuse:
            identity = legacy
        node(identity, 'TABLE', name or logical, path, ev,
             {'datasource': None, 'schema': schema, 'physical_name': name, 'logical_name': logical,
              'identity_status': 'DECLARED_PHYSICAL' if name else 'LOGICAL_ONLY',
              **({'has_mapping_detail': True} if reuse else {'mapping_only': True})})
        return identity
    for entity in extracted['entities']:
        path, ev = evidence(entity, 'orm-entity')
        identity = _id('entity', repository, entity['qualified_name'], entity['path'])
        entities[entity['qualified_name']] = identity
        evidence_by_entity[entity['qualified_name']] = ev
        node(identity, 'ENTITY', entity['name'], path, (ev,),
             {k: entity[k] for k in ('qualified_name', 'table', 'schema', 'datasource')})
        scope_hint = entity['path'] if (not entity['table'] or
                                       entity['schema_expression'] and entity['schema'] is None) else None
        table_id = table(entity['table'], entity['schema'], entity['qualified_name'], path, (ev,), scope_hint)
        table_ids[entity['qualified_name']] = table_id
        graph.add_edge(identity, table_id, 'MAPS_TO_TABLE', 'RUNTIME', (ev,),
                       resolution_status='UNRESOLVED' if not entity['table'] else None,
                       properties={'mapping_kind': 'JPA', 'execution_status': 'NOT_ESTABLISHED'})
        component = component_by_path.get(entity['path'])
        if component:
            graph.add_edge(component, identity, 'CONTAINS_COMPONENT', 'RUNTIME', (ev,))
        for column in entity['columns']:
            column_path, column_ev = evidence(column, 'orm-column')
            column_id = _id('column', table_id, column['name'] or 'LOGICAL:' + column['field'])
            node(column_id, 'COLUMN', column['name'] or column['field'], column_path, (column_ev,),
                 {'field': column['field'], 'physical_name': column['name'], 'table': table_id,
                  'schema': entity['schema'], 'datasource': None, 'mapping_only': True,
                  'naming_status': column['naming_status'], 'attributes': column['attributes']})
            graph.add_edge(identity, column_id, 'MAPS_TO_COLUMN', 'RUNTIME', (ev, column_ev),
                           resolution_status='UNRESOLVED' if not column['name'] or not entity['table'] else None,
                           properties={'execution_status': 'NOT_ESTABLISHED'})
            graph.add_edge(table_id, column_id, 'CONTAINS', 'RUNTIME', (column_ev,))
    for declaration in extracted['repositories']:
        path, ev = evidence(declaration, 'orm-repository')
        source = component_by_path.get(declaration['path'])
        if source is None:
            source = node(_id('orm-repository', repository, declaration['path']), 'COMPONENT', declaration['name'],
                          path, (ev,), {'component_kind': 'REPOSITORY'})
        if declaration['entity'] in entities:
            graph.add_edge(source, entities[declaration['entity']], 'USES_ENTITY', 'RUNTIME',
                           (ev, evidence_by_entity[declaration['entity']]),
                           properties={'declared_operations': declaration['declared_operations'],
                                       'base_repository': declaration['base_repository'],
                                       'execution_status': 'NOT_ESTABLISHED'})
    for query in extracted['queries']:
        path, ev = evidence(query, 'sql-column-reference')
        source = component_by_path.get(query['path'])
        if source is None:
            source = node(_id('sql-source', repository, query['path']), 'COMPONENT', Path(query['path']).stem,
                          path, (ev,), {'component_kind': 'REPOSITORY'})
        for reference in query['columns']:
            target = reference['table']
            table_id = table(target['name'], target['schema'], target['name'], path, (ev,))
            column_id = _id('column', table_id, reference['name'])
            node(column_id, 'COLUMN', reference['name'], path, (ev,),
                 {'physical_name': reference['name'], 'table': table_id, 'schema': target['schema'],
                  'datasource': None, 'reference_only': True})
            graph.add_edge(table_id, column_id, 'CONTAINS', 'RUNTIME', (ev,))
            graph.add_edge(source, column_id, 'REFERENCES_COLUMN', 'RUNTIME', (ev,),
                           properties={'roles': [reference['role']], 'statement_kinds': [query['statement_kind']],
                                       'execution_status': 'NOT_ESTABLISHED'})
    for diagnostic in extracted['diagnostics']:
        graph.diagnostic(diagnostic['code'], f"Line {diagnostic['line']}: {diagnostic['message']}", repository,
                         (repo / diagnostic['path']).relative_to(graph.workspace).as_posix())
    return {'entities': len(extracted['entities']), 'column_mappings': sum(len(e['columns']) for e in extracted['entities']),
            'repositories': len(extracted['repositories']), 'queries': len(extracted['queries']),
            'column_references': sum(len(q['columns']) for q in extracted['queries']),
            'ledger': extracted['ledger']}
