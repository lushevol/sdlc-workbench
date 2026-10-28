"""Project canonical facts into deterministic architecture navigation metadata.

The display levels select detail. They do not assign business criticality.
Canonical edges and evidence remain the source of relationship assertions.
"""
from __future__ import annotations

from collections import Counter
import hashlib
from typing import Any

from .viewer_traces import build_trace_model


FAMILIES = ('api', 'data', 'shared', 'configuration', 'package', 'structure', 'other')
STATUSES = ('resolved', 'unresolved', 'ambiguous', 'candidate', 'declared')
LANES = ('ui', 'service', 'infra', 'data', 'external', 'package')
LEVELS = ('highest', 'medium', 'low', 'context')

_STRUCTURE = {
    'CONTAINS', 'CONTAINS_COMPONENT', 'USES_COMPONENT', 'REALIZED_BY',
    'IMPLEMENTS', 'DELIVERS', 'ROUTES_TO', 'OWNS', 'BELONGS_TO',
    'EXPORTS_SYMBOL',
}
_API = {
    'CALLS_REST', 'CALLS_GRAPHQL', 'CALLS_GRPC', 'CALLS_SERVICE',
    'SUBSCRIBES_WS', 'EXPOSES', 'INVOKES',
    'DECLARES_GRAPHQL_DOCUMENT', 'SELECTS_GRAPHQL_FIELD',
}
_DATA = {
    'READS', 'WRITES', 'PUBLISHES', 'CONSUMES', 'CONNECTS_TO',
    'QUERIES_DATA_PLATFORM', 'CALLS_DATA_PLATFORM', 'READS_CACHE', 'WRITES_CACHE',
    'MAPS_TO_COLUMN', 'MAPS_TO_TABLE', 'REFERENCES_COLUMN', 'USES_ENTITY',
}
_SHARED = {'IMPORTS_MODULE', 'LOADS_REMOTE', 'IMPORTS_COMPONENT', 'SHARES_COMPONENT',
           'IMPORTS_TYPE', 'INJECTS', 'CALLS_COMPONENT', 'DEPENDS_ON_TYPE', 'IMPLEMENTS_TYPE', 'EXTENDS_TYPE',
           'IMPORTS_SOURCE', 'IMPORTS_SYMBOL'}
_SHARED |= {'IMPORTS_TEST_LIBRARY', 'IMPORTS_TEST_RESOURCE'}
_CONFIGURATION = {'DECLARES_CONFIGURATION', 'BINDS_CONFIGURATION', 'READS_CONFIGURATION', 'CONFIGURES_TOPIC',
                  'DECLARES_CONFIG', 'BINDS_CONFIG', 'READS_CONFIG', 'REFERENCES_CONFIG'}
_DATA_TYPES = {'TABLE', 'COLUMN', 'ENTITY', 'DATABASE', 'MESSAGE_CHANNEL', 'DATA_PLATFORM', 'CACHE', 'FILE', 'TOPIC'}
_API_PROTOCOLS = {'REST', 'HTTP', 'HTTPS', 'GRAPHQL', 'GRPC', 'WEBSOCKET', 'WS', 'WSS', 'STOMP'}
_DATA_PROTOCOLS = {'KAFKA', 'FILE', 'SFTP', 'FTP', 'REDIS', 'SQL', 'JDBC', 'AMQP'}
_LABELS = {
    'CALLS_REST': 'Calls REST API', 'CALLS_GRAPHQL': 'Calls GraphQL API',
    'CALLS_GRPC': 'Calls gRPC API', 'CALLS_SERVICE': 'Calls service',
    'SUBSCRIBES_WS': 'Subscribes to WebSocket', 'EXPOSES': 'Exposes API',
    'INVOKES': 'Invokes handler', 'READS': 'Reads data', 'WRITES': 'Writes data',
    'PUBLISHES': 'Publishes messages', 'CONSUMES': 'Consumes messages',
    'CONNECTS_TO': 'Connects to data store', 'QUERIES_DATA_PLATFORM': 'Queries data platform',
    'READS_CACHE': 'Reads cache', 'WRITES_CACHE': 'Writes cache',
    'IMPORTS_MODULE': 'Imports shared module', 'LOADS_REMOTE': 'Loads remote application',
    'IMPORTS_COMPONENT': 'Imports shared component', 'SHARES_COMPONENT': 'Shares component',
    'DEPENDS_ON_PACKAGE': 'Declares build package dependency', 'CONTAINS': 'Contains',
    'CONTAINS_COMPONENT': 'Contains component', 'USES_COMPONENT': 'Uses component',
    'REALIZED_BY': 'Realized by component', 'IMPLEMENTS': 'Implements capability',
    'DELIVERS': 'Delivers page', 'ROUTES_TO': 'Routes to page',
    'OWNS': 'Owns', 'BELONGS_TO': 'Belongs to',
    'DECLARES_CONFIGURATION': 'Declares configuration', 'BINDS_CONFIGURATION': 'Binds configuration',
    'READS_CONFIGURATION': 'Reads configuration', 'CONFIGURES_TOPIC': 'Configures topic',
    'IMPORTS_TYPE': 'Imports Java type', 'INJECTS': 'Injects component',
    'CALLS_COMPONENT': 'Calls component', 'MAPS_TO_COLUMN': 'Maps field to column',
    'MAPS_TO_TABLE': 'Maps entity to table', 'REFERENCES_COLUMN': 'References column',
    'USES_ENTITY': 'Uses entity', 'DECLARES_CONFIG': 'Declares configuration',
    'BINDS_CONFIG': 'Binds configuration', 'READS_CONFIG': 'Reads configuration',
    'REFERENCES_CONFIG': 'References configuration', 'DEPENDS_ON_TYPE': 'Depends on Java type',
    'IMPLEMENTS_TYPE': 'Implements Java type', 'EXTENDS_TYPE': 'Extends Java type',
    'IMPORTS_SOURCE': 'Imports source module', 'IMPORTS_SYMBOL': 'Imports exported symbol',
    'EXPORTS_SYMBOL': 'Exports value symbol',
    'DECLARES_GRAPHQL_DOCUMENT': 'Declares GraphQL document', 'SELECTS_GRAPHQL_FIELD': 'Selects GraphQL field',
    'IMPORTS_TEST_LIBRARY': 'Imports testing library', 'IMPORTS_TEST_RESOURCE': 'Imports testing resource',
}
_FAMILY_LABELS = {
    'api': 'API calls', 'data': 'Data flow', 'shared': 'Shared modules',
    'package': 'Build dependencies', 'structure': 'Ownership and navigation', 'other': 'Other relationships',
    'configuration': 'Configuration',
}


def _protocol(node: dict[str, Any]) -> str:
    return str(node.get('properties', {}).get('protocol', '')).upper()


def _node_family(node: dict[str, Any]) -> str:
    properties = node.get('properties', {})
    node_type = node.get('type', '')
    kind = node.get('component_kind', '')
    if node_type in {'CONFIGURATION_KEY', 'CONFIGURATION_SOURCE'}:
        return 'configuration'
    if properties.get('dependency_kind') == 'BUILD' or properties.get('boundary_kind') == 'PACKAGE':
        return 'package'
    if node_type in {'API_OPERATION', 'GRAPHQL_DOCUMENT', 'GRAPHQL_FIELD_SELECTION'} or _protocol(node) in _API_PROTOCOLS or kind in {
            'REST_CLIENT', 'GRAPHQL_CLIENT', 'WEBSOCKET_CLIENT', 'FEIGN_CLIENT', 'CONTROLLER'}:
        return 'api'
    if node_type in _DATA_TYPES or _protocol(node) in _DATA_PROTOCOLS:
        return 'data'
    if node_type == 'REMOTE_APPLICATION' or properties.get('dependency_kind') == 'MODULE':
        return 'shared'
    if node_type in {'BUSINESS_CAPABILITY', 'PAGE'}:
        return 'structure'
    return 'other'


def _edge_family(edge: dict[str, Any], source: dict, target: dict) -> str:
    relation = edge.get('relationship', '')
    properties = edge.get('properties', {})
    if properties.get('origin') == 'ARCHITECTURE_INVESTIGATION':
        return properties['family']
    if relation == 'DEPENDS_ON_PACKAGE' or properties.get('dependency_kind') == 'BUILD':
        return 'package'
    if relation in _CONFIGURATION or target.get('type') in {'CONFIGURATION_KEY', 'CONFIGURATION_SOURCE'}:
        return 'configuration'
    if relation in _STRUCTURE or edge.get('dimension') == 'BUSINESS':
        return 'structure'
    if relation in _SHARED or properties.get('dependency_kind') == 'MODULE':
        return 'shared'
    if (str(properties.get('protocol', '')).upper() in _API_PROTOCOLS
            or (relation in _DATA and _protocol(target) in _API_PROTOCOLS)):
        return 'api'
    if relation in _API:
        return 'api'
    if relation in _DATA:
        return 'data'
    # Unknown relationship names remain visible. Typed API and data boundaries
    # supply a category without assigning a new relationship assertion.
    endpoint_families = {_node_family(source), _node_family(target)}
    if 'data' in endpoint_families:
        return 'data'
    if 'api' in endpoint_families:
        return 'api'
    return 'other'


def _status(edge: dict[str, Any]) -> str:
    resolution = edge.get('resolution_status')
    if resolution == 'AMBIGUOUS':
        return 'ambiguous'
    if edge.get('assertion_status') != 'CONFIRMED':
        return 'candidate'
    if resolution == 'RESOLVED':
        return 'resolved'
    if resolution == 'UNRESOLVED':
        return 'unresolved'
    return 'declared'


def _lane(node: dict[str, Any], repository: dict[str, Any] | None) -> str:
    family = _node_family(node)
    if family == 'package':
        return 'package'
    if family == 'data' or node.get('type') in _DATA_TYPES:
        return 'data'
    if repository is None:
        return 'external'
    if repository.get('kind') == 'WEB':
        return 'ui'
    if repository.get('kind') == 'INFRA':
        return 'infra'
    return 'service'


def _count(values, field: str, keys: tuple[str, ...]) -> dict[str, int]:
    counts = Counter(value[field] for value in values)
    return {key: counts[key] for key in keys}


def _edge_label(edge: dict[str, Any], target: dict[str, Any]) -> str:
    if edge.get('properties', {}).get('origin') == 'ARCHITECTURE_INVESTIGATION':
        return edge['properties']['kind'].replace('_', ' ').capitalize()
    protocol = str(edge.get('properties', {}).get('protocol', '')).upper() or _protocol(target)
    if protocol == 'GRPC' and edge.get('relationship') in _API | _DATA:
        return 'Calls gRPC API'
    relation = edge['relationship']
    if protocol == 'KAFKA' and relation in {'PUBLISHES', 'CONSUMES'}:
        return 'Publishes Kafka messages' if relation == 'PUBLISHES' else 'Consumes Kafka messages'
    return _LABELS.get(relation, relation.replace('_', ' ').capitalize())


def build_viewer_model(graph: dict[str, Any]) -> dict[str, Any]:
    """Return display metadata without changing canonical nodes or relationships."""
    canonical_nodes = {node['id']: node for node in graph.get('nodes', [])}
    repositories = {repository['id']: repository for repository in graph.get('repositories', [])}
    roots: dict[str, str] = {}
    for node in sorted(canonical_nodes.values(), key=lambda item: item['id']):
        if node.get('repository') in repositories and node.get('type') in {'APPLICATION', 'SERVICE'}:
            roots.setdefault(node['repository'], node['id'])
    for node in sorted(canonical_nodes.values(), key=lambda item: item['id']):
        repository = repositories.get(node.get('repository'), {})
        if (node.get('properties', {}).get('dependency_scope') == 'TESTING'
                and repository.get('path') in node.get('source_paths', [])):
            roots.setdefault(node['repository'], node['id'])

    nodes: dict[str, dict[str, Any]] = {}
    for identifier, node in sorted(canonical_nodes.items()):
        repository_id = node.get('repository')
        lane = _lane(node, repositories.get(repository_id))
        nodes[identifier] = {
            'lane': lane, 'group': repository_id or lane,
            'root_id': roots.get(repository_id, identifier), 'label': node.get('name', identifier),
            'family': _node_family(node),
            'dependency_scope': 'TESTING' if node.get('properties', {}).get('dependency_scope') == 'TESTING' else 'PRODUCTION',
        }
        subjects = node.get('properties', {}).get('architecture_subjects', [])
        if subjects:
            nodes[identifier]['label'] = subjects[0]['label']
            nodes[identifier]['architecture_roles'] = sorted({row['role'] for row in subjects})
            layers = [row for row in subjects if row.get('layer_id')]
            if layers:
                layer = min(layers, key=lambda row: row['layer_order'])
                nodes[identifier]['architecture_layer'] = {
                    'id': layer['layer_id'], 'label': layer['layer_label'], 'order': layer['layer_order']}

    edges: dict[str, dict[str, str]] = {}
    aggregate: dict[tuple[str, ...], dict[str, Any]] = {}
    for edge in sorted(graph.get('edges', []), key=lambda item: item['id']):
        source, target = canonical_nodes[edge['source']], canonical_nodes[edge['target']]
        source_repository, target_repository = source.get('repository'), target.get('repository')
        family, status = _edge_family(edge, source, target), _status(edge)
        dependency_scope = 'TESTING' if edge.get('properties', {}).get('dependency_scope') == 'TESTING' else 'PRODUCTION'
        cross_repository = bool(source_repository and target_repository and source_repository != target_repository)
        claims = edge.get('properties', {}).get('architecture_claims', [])
        assessments = sorted({row.get('investigation_status', row.get('status', 'UNVERIFIED')) for row in claims})
        assessment = next((value for value in ('CONFLICTED', 'UNVERIFIED', 'OUT_OF_SCOPE', 'INFERRED', 'SUPPORTED')
                           if value in assessments), 'EXTRACTED')
        highest = bool(claims) or (cross_repository and family in {'api', 'data', 'shared'} and status == 'resolved')
        level = ('context' if family == 'structure' else 'low' if family == 'package'
                 else 'highest' if highest else 'medium')
        if claims:
            level = 'highest'
        edges[edge['id']] = {
            'family': family, 'status': status, 'level': level,
            'label': _edge_label(edge, target),
            'dependency_scope': dependency_scope,
            'assessment': assessment, 'assessments': assessments,
            'origin': 'INVESTIGATED' if claims else 'EXTRACTED',
        }
        if (family == 'structure' or not (source_repository or target_repository)) and not claims:
            continue
        source_root = roots.get(source_repository, edge['source'])
        target_root = roots.get(target_repository, edge['target'])
        if source_root == target_root:
            continue
        # Owned endpoints without a root retain canonical identity. External
        # endpoints never collapse into a guessed repository or common bucket.
        key = source_root, target_root, family, status, dependency_scope, ','.join(assessments)
        link = aggregate.setdefault(key, {
            'source': source_root, 'target': target_root,
            'source_repository': source_repository, 'target_repository': target_repository,
            'family': family, 'status': status, 'label': _FAMILY_LABELS[family],
            'dependency_scope': dependency_scope,
            'assessment': assessment, 'assessments': assessments,
            'origin': 'INVESTIGATED' if claims else 'EXTRACTED',
            'level': level, 'edge_ids': set(), 'evidence': set(), 'relationships': set(),
        })
        link['edge_ids'].add(edge['id'])
        link['evidence'].update(edge.get('evidence', []))
        link['relationships'].add(edge['relationship'])

    # A canonical boundary can omit protocol properties. Its incoming edges
    # still identify package, module, API, or data usage without a guessed name.
    incoming_families: dict[str, set[str]] = {}
    for edge in graph.get('edges', []):
        if canonical_nodes[edge['target']].get('repository') is None:
            family = edges[edge['id']]['family']
            if family != 'structure':
                incoming_families.setdefault(edge['target'], set()).add(family)
    for identifier, families in incoming_families.items():
        if nodes[identifier]['family'] == 'other' and len(families) == 1:
            family = next(iter(families))
            nodes[identifier]['family'] = family
            if family in {'data', 'package'}:
                nodes[identifier]['lane'] = family
                nodes[identifier]['group'] = family

    system_links = []
    for key, link in sorted(aggregate.items()):
        identity = '|'.join(key).encode('utf-8')
        labels = {edges[identifier]['label'] for identifier in link['edge_ids']}
        label = next(iter(labels)) if len(labels) == 1 else _FAMILY_LABELS[link['family']]
        system_links.append({
            'id': 'view-link:' + hashlib.sha256(identity).hexdigest()[:24],
            **{name: sorted(value) if isinstance(value, set) else value for name, value in link.items()},
            'label': label, 'count': len(link['edge_ids']),
        })
    edge_values = list(edges.values())
    return {
        'schema_version': '1.0.0', 'nodes': nodes, 'edges': edges,
        **build_trace_model(graph),
        'repository_roots': {key: roots[key] for key in sorted(roots)}, 'system_links': system_links,
        'counts': {
            'nodes': len(nodes), 'edges': len(edges), 'system_links': len(system_links),
            'by_family': _count(edge_values, 'family', FAMILIES),
            'by_status': _count(edge_values, 'status', STATUSES),
            'by_level': _count(edge_values, 'level', LEVELS),
            'node_lanes': _count(nodes.values(), 'lane', LANES),
            'system_by_family': _count(system_links, 'family', FAMILIES),
            'system_by_status': _count(system_links, 'status', STATUSES),
            'system_by_level': _count(system_links, 'level', LEVELS),
        },
        'levels': [
            {'id': 'highest', 'label': 'Repository relationships',
             'description': 'Static joins and investigated architecture, with separate evidence assessments. Display level does not establish criticality.'},
            {'id': 'medium', 'label': 'API, data, and shared components',
             'description': 'Inspect declarations, resolved joins, and uncertain boundaries by dependency type.'},
            {'id': 'low', 'label': 'Build packages',
             'description': 'Inspect package declarations separately from API and data relationships.'},
            {'id': 'context', 'label': 'Ownership and navigation',
             'description': 'Inspect structural context separately from runtime flows.'},
        ],
    }
