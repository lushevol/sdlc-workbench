"""Project canonical facts into deterministic architecture navigation metadata.

The display levels select detail. They do not assign business criticality.
Canonical edges and evidence remain the source of relationship assertions.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
import hashlib
from typing import Any
from urllib.parse import urlsplit

from .viewer_traces import build_trace_model


FAMILIES = ('api', 'data', 'shared', 'configuration', 'package', 'structure', 'other')
STATUSES = ('resolved', 'unresolved', 'ambiguous', 'candidate', 'declared')
LANES = ('ui', 'service', 'infra', 'source', 'data', 'external', 'package')
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
_SERVICE_SHARED = {'IMPORTS_MODULE', 'LOADS_REMOTE', 'IMPORTS_COMPONENT', 'SHARES_COMPONENT'}
_SERVICE_CALLS = {'CALLS_REST', 'CALLS_GRAPHQL', 'CALLS_GRPC', 'CALLS_SERVICE', 'SUBSCRIBES_WS'}
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
    if repository.get('kind') == 'SOURCE_ONLY':
        return 'source'
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


def _service_boundary_edge(edge: dict[str, Any], family: str, source_repository: str | None,
                           target_repository: str | None, claims: list[dict[str, Any]]) -> bool:
    """Select relationships that belong on the service boundary projection."""
    return bool(source_repository or target_repository) and family in {'api', 'data', 'shared'} and (
        edge['relationship'] in _SERVICE_CALLS | _SERVICE_SHARED | {'PUBLISHES', 'CONSUMES'}
        or (edge['relationship'] in {'READS', 'QUERIES_DATA_PLATFORM', 'CALLS_DATA_PLATFORM'}
            and str(edge.get('properties', {}).get('protocol', '')).upper() == 'GRPC')
        or (bool(claims) and edge['relationship'] == 'REVIEWED_RELATIONSHIP'))


def _service_status(statuses: set[str]) -> str:
    if len(statuses) == 1:
        return next(iter(statuses))
    return 'mixed'


def _service_assessment(assessments: set[str]) -> str:
    return next((value for value in ('CONFLICTED', 'UNVERIFIED', 'OUT_OF_SCOPE', 'INFERRED', 'SUPPORTED')
                 if value in assessments), 'EXTRACTED')


def build_viewer_model(graph: dict[str, Any], *, include_traces: bool = True) -> dict[str, Any]:
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

    def production_node(node: dict[str, Any]) -> bool:
        return (node.get('properties', {}).get('dependency_scope') != 'TESTING'
                and repositories.get(node.get('repository'), {}).get('kind') not in {'TESTING', 'SOURCE_ONLY'})

    root_candidates = defaultdict(list)
    for identifier, node in sorted(canonical_nodes.items()):
        if (node.get('type') in {'SERVICE', 'APPLICATION'} and node.get('repository') in repositories
                and production_node(node)):
            root_candidates[node['repository']].append(identifier)
    service_roots = {
        repository_id: candidates[0]
        for repository_id, candidates in sorted(root_candidates.items())
        if len(candidates) == 1
    }
    service_repository_by_id = {root: repository_id for repository_id, candidates in root_candidates.items()
                                for root in candidates}
    service_ids = set(service_repository_by_id) | {
        identifier for identifier, node in canonical_nodes.items()
        if node.get('repository') is None and node.get('type') in {'SERVICE', 'APPLICATION'} and production_node(node)}
    owners = {identifier: {identifier} for identifier in service_ids}
    children = defaultdict(set)
    for edge in graph.get('edges', []):
        source, target = canonical_nodes[edge['source']], canonical_nodes[edge['target']]
        if (edge['relationship'] in {'CONTAINS', 'CONTAINS_COMPONENT', 'USES_COMPONENT', 'EXPOSES'}
                and edge.get('properties', {}).get('dependency_scope') != 'TESTING'
                and production_node(source) and production_node(target)
                and source.get('repository') == target.get('repository')):
            children[edge['source']].add(edge['target'])
    queue = deque(sorted(service_ids))
    while queue:
        parent = queue.popleft()
        for child in sorted(children[parent]):
            if child in service_ids:
                continue
            known = owners.setdefault(child, set())
            additions = owners[parent] - known
            if additions:
                known.update(additions)
                queue.append(child)
    boundary_nodes = {}

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

    # Provider operations are implementation details. A uniquely exposed
    # operation is projected back to its owning service root.
    provider_roots: dict[str, set[str]] = {}
    for edge in graph.get('edges', []):
        if (edge.get('relationship') != 'EXPOSES'
                or edge.get('properties', {}).get('dependency_scope') == 'TESTING'):
            continue
        source, target = canonical_nodes[edge['source']], canonical_nodes[edge['target']]
        if (not production_node(source) or not production_node(target) or target.get('type') != 'API_OPERATION'
                or target.get('repository') not in {None, source.get('repository')}):
            continue
        known = owners.get(edge['source'], set()) or {service_roots.get(source.get('repository'))} - {None}
        provider_roots.setdefault(edge['target'], set()).update(known)

    def is_boundary_node(node: dict[str, Any]) -> bool:
        return node.get('repository') is None and (
            node.get('type') in {'SERVICE', 'APPLICATION'}
            or (node.get('type') in {'ARCHITECTURE_BOUNDARY', 'EXTERNAL_SYSTEM', 'REMOTE_APPLICATION'}
                and _node_family(node) not in {'data', 'package', 'configuration'})
            or (node.get('type') == 'DATA_PLATFORM' and _protocol(node) == 'GRPC'))

    def display_node(identifier: str) -> str | None:
        node = canonical_nodes[identifier]
        repository = node.get('repository')
        if not production_node(node):
            return None
        if identifier in service_ids:
            return identifier
        known = owners.get(identifier, set()) | provider_roots.get(identifier, set())
        if len(known) == 1:
            return next(iter(known))
        if len(known) > 1:
            return None
        if repository in service_roots:
            return service_roots[repository]
        return identifier if is_boundary_node(node) else None

    projected_nodes = {identifier: display_node(identifier) for identifier in canonical_nodes}

    def external_destination(node: dict[str, Any], caller: str, edge: dict[str, Any]) -> str | None:
        if (node.get('repository') is not None or node.get('type') != 'API_OPERATION'
                or not production_node(node) or node['id'] in provider_roots or owners.get(node['id'])):
            return None
        properties = node.get('properties', {})
        protocol = _protocol(node) or str(edge.get('properties', {}).get('protocol', '')).upper() or 'HTTP'
        authority = properties.get('authority')
        if not authority:
            try:
                authority = urlsplit(properties.get('url') or properties.get('path') or '').netloc
            except ValueError:
                authority = None
        authority = str(authority or '').split('@')[-1]
        destination = authority or f'Unresolved {protocol} destinations'
        identifier = 'viewer-boundary:' + hashlib.sha256(f'{caller}|{protocol}|{authority}'.encode()).hexdigest()[:24]
        boundary_nodes.setdefault(identifier, {
            'id': identifier, 'name': destination,
            'label': destination, 'type': 'SERVICE_BOUNDARY',
            'repository': None, 'lane': 'external', 'family': 'api', 'dependency_scope': 'PRODUCTION',
            'display_kind': 'Destination group', 'display_node': True,
            'provider_limit': 'Grouped declarations only. No shared provider or deployed service identity is established.',
        })
        return identifier

    edges: dict[str, dict[str, Any]] = {}
    aggregate: dict[tuple[str, ...], dict[str, Any]] = {}
    service_aggregate: dict[tuple[str, str, str], dict[str, Any]] = {}
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
        # Service projection: implementation nodes collapse into their owning
        # service or UI module. Only boundary relationships reach this graph.
        service_source, service_target = projected_nodes[edge['source']], projected_nodes[edge['target']]
        service_family = family
        if edge['relationship'] == 'REVIEWED_RELATIONSHIP':
            kind = edge.get('properties', {}).get('kind', '')
            if family == 'configuration' and kind.startswith(('FORWARDS_', 'ROUTES_')):
                service_family = 'api'
            elif family == 'structure' and kind.startswith('LOADS_'):
                service_family = 'shared'
        boundary_edge = (dependency_scope != 'TESTING' and production_node(source) and production_node(target)
                         and _service_boundary_edge(edge, service_family, source_repository, target_repository, claims))
        if service_source and not service_target and boundary_edge:
            service_target = external_destination(target, service_source, edge)
        if (service_source and service_target and service_source != service_target
                and boundary_edge):
            scope_key = dependency_scope
            service_key = service_source, service_target, scope_key
            service_link = service_aggregate.setdefault(service_key, {
                'source': service_source, 'target': service_target,
                'source_repository': service_repository_by_id.get(service_source)
                or canonical_nodes.get(service_source, {}).get('repository'),
                'target_repository': service_repository_by_id.get(service_target)
                or canonical_nodes.get(service_target, {}).get('repository'),
                'family': service_family, 'families': set(), 'family_counts': Counter(),
                'status': status, 'statuses': set(), 'label': _FAMILY_LABELS.get(service_family, service_family),
                'dependency_scope': dependency_scope, 'assessment': assessment,
                'assessments': set(), 'origin': 'INVESTIGATED' if claims else 'EXTRACTED',
                'level': 'highest', 'edge_ids': set(), 'evidence': set(), 'relationships': set(),
                'facets': {},
            })
            service_link['families'].add(service_family)
            service_link['family_counts'][service_family] += 1
            service_link['statuses'].add(status)
            service_link['assessments'].update(assessments)
            service_link['edge_ids'].add(edge['id'])
            service_link['evidence'].update(edge.get('evidence', []))
            service_link['relationships'].add(edge['relationship'])
            facet_key = (service_family, status, tuple(assessments), edge['relationship'], 'INVESTIGATED' if claims else 'EXTRACTED')
            facet = service_link['facets'].setdefault(facet_key, {
                **edges[edge['id']], 'family': service_family, 'relationship': edge['relationship'], 'count': 0})
            facet['count'] += 1
            if claims:
                service_link['origin'] = 'INVESTIGATED'

        if (family == 'structure' or not (source_repository or target_repository)) and not claims:
            continue
        source_root = roots.get(source_repository, edge['source'])
        target_root = roots.get(target_repository, edge['target'])
        if source_root == target_root:
            continue
        # Legacy detail projections retain canonical external identities.
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
    service_links = []
    family_order = ('api', 'shared', 'data', 'configuration', 'package', 'structure', 'other')
    status_order = ('unresolved', 'ambiguous', 'candidate', 'declared', 'resolved')
    for key, link in sorted(service_aggregate.items()):
        identity = '|'.join(key).encode('utf-8')
        family_counts = dict(link['family_counts'])
        primary_family = next((family for family in family_order if family in family_counts), 'other')
        statuses = sorted(link['statuses'], key=lambda value: status_order.index(value))
        assessments = sorted(link['assessments'])
        service_links.append({
            'id': 'service-link:' + hashlib.sha256(identity).hexdigest()[:24],
            'source': link['source'], 'target': link['target'],
            'source_repository': link['source_repository'], 'target_repository': link['target_repository'],
            'family': primary_family, 'families': sorted(link['families']), 'family_counts': family_counts,
            'status': _service_status(link['statuses']), 'statuses': statuses,
            'label': _FAMILY_LABELS.get(primary_family, primary_family),
            'dependency_scope': link['dependency_scope'],
            'assessment': _service_assessment(link['assessments']), 'assessments': assessments,
            'origin': link['origin'], 'level': 'highest',
            'edge_ids': sorted(link['edge_ids']), 'evidence': sorted(link['evidence']),
            'relationships': sorted(link['relationships']), 'count': len(link['edge_ids']),
            'facets': [facet for _, facet in sorted(link['facets'].items())],
        })

    # Service cards retain useful low-priority information without adding
    # implementation nodes to the service graph.
    display_ids = service_ids | {endpoint for link in service_links for endpoint in (link['source'], link['target'])}
    component_counts = Counter(root for identifier, root in projected_nodes.items()
                               if root in service_ids and identifier != root)
    inbound_counts = Counter(link['target'] for link in service_links)
    outbound_counts = Counter(link['source'] for link in service_links)
    projected_edge_ids = {identifier for link in service_links for identifier in link['edge_ids']}
    family_counts_by_root = defaultdict(Counter)
    internal_counts, low_priority_counts = Counter(), Counter()
    for edge in graph.get('edges', []):
        root = projected_nodes[edge['source']]
        if (root not in display_ids or edge.get('properties', {}).get('dependency_scope') == 'TESTING'
                or not production_node(canonical_nodes[edge['target']])):
            continue
        family_counts_by_root[root][edges[edge['id']]['family']] += 1
        if root == projected_nodes[edge['target']]:
            internal_counts[root] += 1
        if edge['id'] not in projected_edge_ids:
            low_priority_counts[root] += 1
    service_details: dict[str, dict[str, Any]] = {}
    for root in sorted(display_ids):
        service_details[root] = {
            'repository': service_repository_by_id.get(root),
            'component_count': component_counts[root],
            'internal_edge_count': internal_counts[root],
            'inbound_relationship_count': inbound_counts[root],
            'outbound_relationship_count': outbound_counts[root],
            'relationship_families': dict(sorted(family_counts_by_root[root].items())),
            'low_priority_relationship_count': low_priority_counts[root],
        }

    display_nodes = {}
    for identifier in sorted(display_ids):
        if identifier in boundary_nodes:
            display_nodes[identifier] = {**boundary_nodes[identifier], 'service_summary': service_details[identifier]}
            continue
        node = canonical_nodes[identifier]
        display_nodes[identifier] = {
            **{field: node[field] for field in ('id', 'name', 'type', 'repository') if field in node},
            **nodes[identifier], 'root_id': identifier, 'service_summary': service_details[identifier],
        }
        display_nodes[identifier]['display_node'] = True
        display_nodes[identifier]['display_kind'] = (
            'UI module' if display_nodes[identifier]['lane'] == 'ui' else
            'Gateway' if display_nodes[identifier]['lane'] == 'infra' else
            'External boundary' if node.get('repository') is None else 'Service')

    edge_values = list(edges.values())
    service_family_counts = Counter(link['family'] for link in service_links)
    service_status_counts = Counter(link['status'] for link in service_links)
    return {
        'schema_version': '1.0.0', 'nodes': nodes, 'edges': edges,
        **(build_trace_model(graph) if include_traces else {}),
        'repository_roots': {key: roots[key] for key in sorted(roots)}, 'system_links': system_links,
        'service_graph': {
            'nodes': display_nodes,
            'links': service_links,
            'details': service_details,
            'repository_roots': {key: service_roots[key] for key in sorted(service_roots)},
        },
        'counts': {
            'nodes': len(nodes), 'edges': len(edges), 'system_links': len(system_links),
            'by_family': _count(edge_values, 'family', FAMILIES),
            'by_status': _count(edge_values, 'status', STATUSES),
            'by_level': _count(edge_values, 'level', LEVELS),
            'node_lanes': _count(nodes.values(), 'lane', LANES),
            'system_by_family': _count(system_links, 'family', FAMILIES),
            'system_by_status': _count(system_links, 'status', STATUSES),
            'system_by_level': _count(system_links, 'level', LEVELS),
            'service_nodes': len(display_nodes), 'service_links': len(service_links),
            'service_by_family': {key: service_family_counts[key] for key in FAMILIES},
            'service_by_status': dict(sorted(service_status_counts.items())),
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
