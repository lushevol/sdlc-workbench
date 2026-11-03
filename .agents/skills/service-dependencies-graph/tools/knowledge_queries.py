"""Bounded, read-only navigation of the canonical knowledge projection."""
from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path


LIMITATIONS = [
    'Paths preserve recorded relationships. A connected path does not establish semantic support, business approval, or runtime behavior.',
    'Lifecycle filters apply to every governed node in a path. Neutral source and catalog nodes do not gain approval.',
    'Bounded traversal can omit paths. An empty result does not establish the absence of a relationship.',
]


class KnowledgeQueryError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def freshness(graph: dict, workspace: Path) -> dict:
    """Compare selected current inputs without changing saved projection bytes."""
    if 'knowledge' not in graph:
        return {'status': 'NOT_AVAILABLE', 'changed_paths': [],
                'reason': 'This snapshot predates the knowledge projection. Rebuild it to add this layer.'}
    from .knowledge_projection import input_fingerprints
    try:
        saved = {row['path']: row['sha256'] for row in graph['knowledge']['inputs']}
        current = {row['path']: row['sha256'] for row in input_fingerprints(workspace)}
        changed = sorted(path for path in saved.keys() | current.keys()
                         if saved.get(path) != current.get(path))
        return {'status': 'STALE' if changed else 'CURRENT', 'changed_paths': changed,
                'scope': 'Selected knowledge projection input bytes; not authority, applicability, or execution.'}
    except (KeyError, TypeError, ValueError, OSError):
        return {'status': 'UNKNOWN', 'changed_paths': [],
                'reason': 'Current knowledge inputs could not be safely compared.'}


def validate_references(graph: dict) -> None:
    """Reject ambiguous or dangling saved graph references before navigation."""
    identifiers = {}
    for name in ('nodes', 'edges', 'evidence'):
        values = [row['id'] for row in graph[name]]
        if len(values) != len(set(values)):
            raise ValueError('The graph ' + name + ' IDs must be unique.')
        identifiers[name] = set(values)
    for node in graph['nodes']:
        if not set(node['evidence']) <= identifiers['evidence']:
            raise ValueError('A graph node references missing evidence.')
    for edge in graph['edges']:
        if not {edge['source'], edge['target']} <= identifiers['nodes']:
            raise ValueError('A graph edge has a dangling endpoint.')
        if not set(edge['evidence']) <= identifiers['evidence']:
            raise ValueError('A graph edge references missing evidence.')


def _projected(node: dict) -> bool:
    return node.get('properties', {}).get('projection') == 'knowledge'


def _allowed(node: dict, state: str | None) -> bool:
    actual = node.get('properties', {}).get('governance_state')
    # Source, catalog, and execution evidence have no invented business lifecycle.
    return not state or actual is None or actual == state


def _subgraph(graph: dict, node_ids: set[str], edge_ids: set[str]) -> dict:
    nodes = [row for row in graph['nodes'] if row['id'] in node_ids]
    edges = [row for row in graph['edges'] if row['id'] in edge_ids]
    evidence_ids = {ref for row in nodes + edges for ref in row.get('evidence', [])}
    return {'nodes': nodes, 'edges': edges,
            'evidence': [row for row in graph['evidence'] if row['id'] in evidence_ids]}


def knowledge(graph: dict, arguments: dict) -> dict:
    query = arguments.get('query', '').casefold()
    rows = []
    for node in graph['nodes']:
        if not _projected(node):
            continue
        properties = node.get('properties', {})
        if arguments.get('type') and arguments['type'] not in (node['type'], properties.get('record_type')):
            continue
        if any(properties.get(key) != arguments[key]
               for key in ('governance_state', 'record_id', 'owner') if key in arguments):
            continue
        text = ' '.join(str(node.get(key, '')) for key in
                        ('id', 'name', 'functional_role', 'business_meaning', 'source_paths', 'properties'))
        if query and query not in text.casefold():
            continue
        rows.append(node)
    limit = arguments.get('limit', 60)
    selected = rows[:limit]
    return {**_subgraph(graph, {row['id'] for row in selected}, set()),
            'matching_total': len(rows), 'limit': limit,
            'filters': {key: value for key, value in arguments.items() if key != 'limit'},
            'truncated': len(rows) > limit,
            'truncation_reasons': ['RESULT_LIMIT'] if len(rows) > limit else []}


def references(graph: dict, arguments: dict) -> dict:
    nodes = {row['id']: row for row in graph['nodes']}
    node_id, direction = arguments['node_id'], arguments.get('direction', 'both')
    if node_id not in nodes:
        raise KnowledgeQueryError('UNKNOWN_NODE', 'The graph contains no node with this ID.')
    state = arguments.get('governance_state')
    excluded = 0
    edges = []
    if _allowed(nodes[node_id], state):
        for edge in graph['edges']:
            if not ((direction in ('out', 'both') and edge['source'] == node_id) or
                    (direction in ('in', 'both') and edge['target'] == node_id)):
                continue
            if not all(_allowed(nodes[edge[key]], state) for key in ('source', 'target')):
                excluded += 1
                continue
            edges.append(edge)
    else:
        excluded = 1
    limit = arguments.get('limit', 60)
    selected = edges[:limit]
    node_ids = ({node_id} if _allowed(nodes[node_id], state) else set())
    node_ids.update(edge[key] for edge in selected for key in ('source', 'target'))
    return {**_subgraph(graph, node_ids, {edge['id'] for edge in selected}),
            'total_edges': len(edges), 'limit': limit, 'direction': direction,
            'governance_state': state,
            'excluded_by_state': excluded, 'truncated': len(edges) > limit,
            'truncation_reasons': ['RESULT_LIMIT'] if len(edges) > limit else []}


def paths(graph: dict, arguments: dict) -> dict:
    """Enumerate simple paths with bounded depth, results, and examined transitions."""
    nodes = {row['id']: row for row in graph['nodes']}
    source, target = arguments['source'], arguments['target']
    if source not in nodes or target not in nodes:
        raise KnowledgeQueryError('UNKNOWN_NODE', 'A path endpoint does not occur in this graph.')
    state, direction = arguments.get('governance_state'), arguments.get('direction', 'out')
    max_depth, max_visits = arguments.get('max_depth', 4), arguments.get('max_visits', 1000)
    limit = arguments.get('limit', 10)
    excluded = {key for key, node in nodes.items() if not _allowed(node, state)}
    adjacency = defaultdict(list)
    for edge in graph['edges']:
        if edge['source'] in excluded or edge['target'] in excluded:
            continue
        if direction in ('out', 'both'):
            adjacency[edge['source']].append((edge['target'], edge['id'], 'out'))
        if direction in ('in', 'both') and (direction != 'both' or edge['source'] != edge['target']):
            adjacency[edge['target']].append((edge['source'], edge['id'], 'in'))
    for entries in adjacency.values():
        entries.sort(key=lambda row: (row[0], row[1], row[2]))
    queue = deque([([source], [], [])]) if not {source, target} & excluded else deque()
    found, reasons, visits = [], set(), 0
    if queue and source == target:
        found.append({'node_ids': [source], 'edge_ids': [], 'traversal_directions': []})
        queue.clear()
    while queue:
        node_ids, edge_ids, directions = queue.popleft()
        current = node_ids[-1]
        entries = adjacency[current]
        if len(edge_ids) == max_depth:
            if any(neighbor not in node_ids for neighbor, _, _ in entries):
                reasons.add('MAX_DEPTH')
            continue
        for neighbor, edge_id, orientation in entries:
            if visits == max_visits:
                reasons.add('MAX_VISITS')
                queue.clear()
                break
            visits += 1
            if neighbor in node_ids:
                continue
            next_nodes, next_edges = node_ids + [neighbor], edge_ids + [edge_id]
            next_directions = directions + [orientation]
            if neighbor == target:
                found.append({'node_ids': next_nodes, 'edge_ids': next_edges,
                              'traversal_directions': next_directions})
                if len(found) > limit:
                    reasons.add('RESULT_LIMIT')
                    queue.clear()
                    break
            else:
                queue.append((next_nodes, next_edges, next_directions))
    selected = found[:limit]
    node_ids = {node for row in selected for node in row['node_ids']}
    edge_ids = {edge for row in selected for edge in row['edge_ids']}
    return {**_subgraph(graph, node_ids, edge_ids), 'paths': selected,
            'source': source, 'target': target, 'direction': direction,
            'governance_state': state,
            'max_depth': max_depth, 'max_visits': max_visits, 'visits': visits,
            'limit': limit, 'excluded_by_state': len(excluded),
            'truncated': bool(reasons), 'truncation_reasons': sorted(reasons)}


def query(graph: dict, operation: str, arguments: dict) -> dict:
    if 'knowledge' not in graph:
        result = {'knowledge_status': 'NOT_AVAILABLE', 'nodes': [], 'edges': [], 'evidence': [],
                  'truncated': False, 'truncation_reasons': [],
                  'reason': 'This snapshot predates the knowledge projection. Rebuild it to add this layer.'}
        if operation == 'paths':
            result['paths'] = []
        return result
    operation_function = {'knowledge': knowledge, 'references': references, 'paths': paths}[operation]
    result = {'knowledge_status': 'AVAILABLE', **operation_function(graph, arguments)}
    result['limitations'] = list(graph['knowledge'].get('limitations', [])) + LIMITATIONS
    return result
