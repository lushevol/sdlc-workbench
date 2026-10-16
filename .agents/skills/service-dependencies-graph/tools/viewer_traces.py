"""Build bounded, evidence-preserving dependency traces for viewer navigation.

An API handler path is distinct from class declarations and implementation
alternatives. No projection here selects runtime dispatch or adds graph facts.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from typing import Any


_CALLS = {'CALLS_COMPONENT', 'CALLS_REST', 'CALLS_GRAPHQL', 'CALLS_GRPC', 'CALLS_SERVICE', 'SUBSCRIBES_WS'}
_CONFIG = {'READS_CONFIG', 'READS_CONFIGURATION', 'REFERENCES_CONFIG', 'REFERENCES_CONFIGURATION',
           'BINDS_CONFIG', 'BINDS_CONFIGURATION', 'CONFIGURES_TOPIC'}
_STORAGE = {'READS', 'WRITES', 'CONNECTS_TO', 'USES_ENTITY', 'MAPS_TO_TABLE', 'MAPS_TO_COLUMN',
            'REFERENCES_COLUMN', 'READS_CACHE', 'WRITES_CACHE', 'QUERIES_DATA_PLATFORM', 'CALLS_DATA_PLATFORM'}
_MESSAGES = {'PUBLISHES', 'CONSUMES'}
_TYPES = {'INJECTS', 'DEPENDS_ON_TYPE', 'IMPORTS_TYPE', 'EXTENDS_TYPE'}
_IMPORTS = {'IMPORTS_MODULE', 'IMPORTS_SOURCE', 'IMPORTS_SYMBOL', 'IMPORTS_COMPONENT',
            'SHARES_COMPONENT', 'LOADS_REMOTE', 'EXPORTS_SYMBOL'}
_CONTEXT = {'EXPOSES', 'CONTAINS', 'CONTAINS_COMPONENT', 'USES_COMPONENT'}
_FOLLOW = _CALLS | _CONFIG | _STORAGE | _MESSAGES | _TYPES | _IMPORTS | {'INVOKES'}


def _role(node: dict, incoming: list[dict], outgoing: list[dict]) -> str:
    kind, component = node.get('type'), node.get('component_kind')
    if kind in {'APPLICATION', 'SERVICE'}:
        return 'repository'
    if kind in {'CONFIGURATION_KEY', 'CONFIGURATION_SOURCE'}:
        return 'configuration'
    if kind in {'TABLE', 'COLUMN', 'ENTITY', 'DATABASE', 'CACHE', 'DATA_PLATFORM', 'FILE'}:
        return 'storage'
    if kind in {'MESSAGE_CHANNEL', 'TOPIC'}:
        return 'message'
    if kind == 'API_OPERATION':
        return 'entrypoint' if any(e['relationship'] == 'EXPOSES' for e in incoming) else 'external'
    if component == 'CONTROLLER' or any(e['relationship'] == 'INVOKES' for e in incoming):
        return 'handler'
    if any(e['relationship'] in _CALLS - {'CALLS_COMPONENT'} for e in outgoing):
        return 'client'
    if any(e['relationship'] == 'IMPLEMENTS_TYPE' for e in outgoing):
        return 'implementation'
    return 'external' if node.get('repository') is None else 'component'


def _identity_groups(nodes: dict[str, dict]) -> tuple[dict[str, list[dict]], dict[str, list[str]]]:
    """Bridge distinct representations only with exact source and type evidence.

    Simple names, shared files without qualified types, and duplicate candidates
    of one representation cannot establish identity.
    """
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for node in nodes.values():
        qualified = node.get('properties', {}).get('qualified_name')
        paths = node.get('source_paths', [])
        concrete = [path for path in paths if path.endswith('.java') and not any(c in path for c in '*?[')]
        if qualified and node.get('repository') and len(concrete) == 1:
            groups[(node['repository'], qualified, concrete[0])].append(node)
    bridges: dict[str, list[dict]] = defaultdict(list)
    ambiguous: dict[str, list[str]] = {}
    for (repository, qualified, path), group in sorted(groups.items()):
        if len(group) < 2:
            continue
        categories = Counter((n.get('type'), n.get('component_kind') == 'JAVA_TYPE') for n in group)
        if max(categories.values()) > 1:
            for node in group:
                ambiguous[node['id']] = sorted(n['id'] for n in group if n['id'] != node['id'])
            continue
        for source in group:
            for target in group:
                if source['id'] == target['id']:
                    continue
                bridges[source['id']].append({
                    'source': source['id'], 'target': target['id'],
                    'rule': 'exact-repository-qualified-type-source', 'repository': repository,
                    'qualified_name': qualified, 'path': path,
                    'evidence': sorted(set(source.get('evidence', []) + target.get('evidence', []))),
                    'scope': 'identity_context',
                })
    return bridges, ambiguous


def _method(node: dict, name: str | None, line: int | None = None,
            arity: int | None = None) -> tuple[str | None, int | None, int | None, bool]:
    declarations = [method for method in node.get('properties', {}).get('declared_methods', [])
                    if method.get('name') == name and (arity is None or method.get('arity') == arity)]
    if line is not None:
        declarations = [method for method in declarations if method.get('line') == line]
    ambiguous = len(declarations) > 1
    if len(declarations) == 1:
        line, arity = declarations[0].get('line'), declarations[0].get('arity')
    return name, line, arity, ambiguous


def build_trace_model(graph: dict[str, Any], *, max_hops: int = 6,
                      max_nodes: int = 160, max_edges: int = 240) -> dict[str, Any]:
    """Return canonical IDs, scoped steps, explicit breaks, and display limits."""
    nodes = {node['id']: node for node in graph.get('nodes', [])}
    incoming: dict[str, list[dict]] = defaultdict(list)
    outgoing: dict[str, list[dict]] = defaultdict(list)
    for edge in sorted(graph.get('edges', []), key=lambda item: item['id']):
        incoming[edge['target']].append(edge)
        outgoing[edge['source']].append(edge)
    identity_context_edges = {
        (edge['source'], edge['target']): edge for edge in graph.get('edges', [])
        if edge['relationship'] in {'CONTAINS', 'CONTAINS_COMPONENT'} and edge.get('assertion_status') == 'CONFIRMED'
    }
    roles = {identifier: _role(node, incoming[identifier], outgoing[identifier]) for identifier, node in nodes.items()}
    bridges, ambiguous_identities = _identity_groups(nodes)
    anchors: dict[str, str] = {}
    for edge in graph.get('edges', []):
        relation = edge['relationship']
        if relation == 'EXPOSES':
            anchors[edge['target']] = 'provided_api'
        elif relation in _CALLS - {'CALLS_COMPONENT'}:
            anchors.setdefault(edge['source'], 'outbound_client')
        elif relation in _MESSAGES:
            anchors.setdefault(edge['source'], 'message_component')
    traces, by_repository, by_node = {}, defaultdict(list), defaultdict(list)
    for anchor, kind in sorted(anchors.items()):
        selected_nodes = {anchor}
        steps: dict[str, dict] = {}
        selected_bridges: dict[tuple[str, str], dict] = {}
        breaks: dict[tuple, dict] = {}
        omitted_edges: set[str] = set()
        visited: dict[tuple, int] = {}
        queue = deque([(anchor, None, None, None, 'method_path' if kind == 'provided_api' else 'class_context', 0)])

        def add_break(node_id, reason, edge=None, status=None):
            key = (node_id, reason, edge and edge['id'])
            breaks[key] = {'node_id': node_id, 'reason': reason,
                           **({'edge_id': edge['id']} if edge else {}), **({'status': status} if status else {})}

        def add_step(edge, role, scope, selected_sites=None, traversal='forward'):
            if edge['id'] not in steps and (len(steps) >= max_edges or
                    len(selected_nodes | {edge['source'], edge['target']}) > max_nodes):
                omitted_edges.add(edge['id'])
                return False
            selected_nodes.update((edge['source'], edge['target']))
            step = steps.setdefault(edge['id'], {
                'edge_id': edge['id'], 'source': edge['source'], 'target': edge['target'],
                'relationship': edge['relationship'], 'role': role, 'scope': scope,
                'traversal': traversal, 'evidence': sorted(edge.get('evidence', [])),
                'assertion_status': edge.get('assertion_status'),
                'resolution_status': edge.get('resolution_status'), 'selected_call_sites': [],
                'scoped_call_sites': [],
            })
            deferred_roles = {'deferred_call_context', 'deferred_configuration_context'}
            if role in {'call', 'configuration'} and step['role'] in deferred_roles:
                previous_sites = step.get('selected_call_sites', [])
                if previous_sites:
                    step.setdefault('deferred_call_sites', []).extend(
                        site for site in previous_sites
                        if site not in step['deferred_call_sites'])
                step['selected_call_sites'] = []
                step['role'], step['scope'] = role, scope
            selected_field = 'deferred_call_sites' if role in deferred_roles else 'selected_call_sites'
            step.setdefault(selected_field, [])
            # A canonical class edge can carry multiple method calls. Keep each
            # selected site rather than replacing it with its scalar method.
            for site in selected_sites or []:
                if site not in step[selected_field]:
                    step[selected_field].append(site)
                scoped_site = {'scope': scope, 'role': role, 'call_site': site}
                if scoped_site not in step['scoped_call_sites']:
                    step['scoped_call_sites'].append(scoped_site)
            if step['scope'] != scope:
                step.setdefault('additional_scopes', [])
                if scope not in step['additional_scopes']:
                    step['additional_scopes'].append(scope)
            return True

        # Consumer calls and service ownership provide entry context. Their
        # canonical direction remains intact, and traversal stops at the caller.
        for edge in incoming[anchor]:
            if edge['source'] != anchor and edge['relationship'] in _CONTEXT | _CALLS:
                add_step(edge, 'ownership_context' if edge['relationship'] in _CONTEXT else 'consumer_call',
                         'declaration_context', traversal='reverse_context')
        while queue:
            current, method, method_line, arity, scope, depth = queue.popleft()
            state = (current, method, method_line, arity, scope)
            if state in visited and visited[state] <= depth:
                continue
            visited[state] = depth
            node = nodes[current]
            if current in ambiguous_identities:
                add_break(current, 'AMBIGUOUS_SOURCE_TYPE_IDENTITY', status='AMBIGUOUS')
            if depth >= max_hops:
                remaining = [e for e in outgoing[current] if e['relationship'] in _FOLLOW and e['id'] not in steps]
                omitted_edges.update(e['id'] for e in remaining)
                if remaining:
                    add_break(current, 'HOP_LIMIT')
                continue
            for bridge in bridges.get(current, []):
                target = bridge['target']
                if len(selected_nodes | {target}) > max_nodes:
                    add_break(current, 'NODE_LIMIT')
                    continue
                selected_nodes.add(target)
                selected_bridges[(current, target)] = bridge
                context_edge = identity_context_edges.get((current, target)) or identity_context_edges.get((target, current))
                if context_edge:
                    add_step(context_edge, 'identity_context', 'declaration_context',
                             traversal='forward' if context_edge['source'] == current else 'reverse_context')
                queue.append((target, method, method_line, arity, scope, depth))
            # Implementations depend on interfaces in the canonical direction.
            # Reverse navigation shows alternatives without selecting dispatch.
            if node.get('properties', {}).get('type_kind') == 'interface':
                alternatives = [edge for edge in incoming[current] if edge['relationship'] == 'IMPLEMENTS_TYPE']
                if alternatives:
                    add_break(current, 'RUNTIME_IMPLEMENTATION_NOT_SELECTED', status='UNRESOLVED')
                for edge in alternatives:
                    if edge.get('assertion_status') != 'CONFIRMED':
                        add_step(edge, 'candidate_context', 'declaration_context', traversal='reverse_context')
                        add_break(edge['source'], 'ASSERTION_NOT_CONFIRMED', edge, 'CANDIDATE')
                        continue
                    if add_step(edge, 'implementation_candidate', 'implementation_context', traversal='reverse_context'):
                        target = edge['source']
                        resolved_method = _method(nodes[target], method, arity=arity)
                        if resolved_method[3]:
                            add_break(target, 'AMBIGUOUS_TARGET_METHOD', edge, 'AMBIGUOUS')
                        else:
                            queue.append((target, *resolved_method[:3], 'implementation_context', depth + 1))
            for edge in outgoing[current]:
                relation, target = edge['relationship'], edge['target']
                if relation not in _FOLLOW:
                    continue
                if scope == 'boundary_context' and relation not in _CONFIG:
                    continue
                properties = edge.get('properties', {})
                sites = properties.get('call_sites', [])
                scoped_sites = [site for site in sites if method is None or
                                (site.get('source_method') == method and
                                 (method_line is None or site.get('source_method_line') == method_line))]
                class_sites = [site for site in sites if not site.get('source_method')]
                if relation in _CONFIG and class_sites and not scoped_sites:
                    scoped_sites = class_sites
                if sites and not scoped_sites:
                    continue
                if edge.get('assertion_status') != 'CONFIRMED':
                    add_step(edge, 'candidate_context', 'declaration_context', scoped_sites)
                    add_break(target, 'ASSERTION_NOT_CONFIRMED', edge, 'CANDIDATE')
                    continue
                deferred_sites = [site for site in scoped_sites if site.get('deferred')]
                if relation in _CALLS | _CONFIG and deferred_sites:
                    direct_sites = [site for site in scoped_sites if not site.get('deferred')]
                    add_break(target, 'DEFERRED_CALL_EXECUTION_NOT_ESTABLISHED' if relation in _CALLS
                              else 'DEFERRED_CONFIGURATION_EXECUTION_NOT_ESTABLISHED', edge)
                    if not direct_sites:
                        add_step(edge, 'deferred_call_context' if relation in _CALLS
                                 else 'deferred_configuration_context', 'declaration_context', deferred_sites)
                        continue
                    scoped_sites = direct_sites
                if relation == 'INVOKES':
                    declarations = properties.get('handler_declarations', [])
                    identities = {(declaration.get('handler'), declaration.get('handler_line'),
                                   declaration.get('handler_arity'), declaration.get('path'))
                                  for declaration in declarations}
                    if len(identities) > 1:
                        if add_step(edge, 'handler_context', 'class_context'):
                            steps[edge['id']]['handler_declarations'] = declarations
                            add_break(target, 'AMBIGUOUS_HANDLER_DECLARATION', edge, 'AMBIGUOUS')
                            queue.append((target, None, None, None, 'class_context', depth + 1))
                        continue
                    declaration = declarations[0] if declarations else properties
                    handler = declaration.get('handler') or node.get('properties', {}).get('handler')
                    resolved_method = _method(nodes[target], handler, declaration.get('handler_line'),
                                              declaration.get('handler_arity'))
                    if add_step(edge, 'handler', scope):
                        if not handler:
                            add_break(target, 'HANDLER_METHOD_NOT_RECORDED', edge)
                            queue.append((target, None, None, None, 'class_context', depth + 1))
                        elif resolved_method[3]:
                            add_break(target, 'AMBIGUOUS_HANDLER_METHOD', edge, 'AMBIGUOUS')
                        else:
                            queue.append((target, *resolved_method[:3], scope, depth + 1))
                elif relation == 'CALLS_COMPONENT':
                    if not scoped_sites:
                        add_step(edge, 'class_call_context', 'class_context')
                        add_break(current, 'CALLER_METHOD_NOT_RECORDED', edge)
                        continue
                    if not add_step(edge, 'call', scope, scoped_sites):
                        continue
                    if deferred_sites:
                        retained = steps[edge['id']].setdefault('deferred_call_sites', [])
                        retained.extend(site for site in deferred_sites if site not in retained)
                    for site in scoped_sites:
                        resolved_method = _method(nodes[target], site.get('target_method'),
                                                  site.get('target_method_line'), site.get('arity'))
                        if resolved_method[3]:
                            add_break(target, 'AMBIGUOUS_TARGET_METHOD', edge, 'AMBIGUOUS')
                        else:
                            queue.append((target, *resolved_method[:3], scope, depth + 1))
                else:
                    role = ('configuration' if relation in _CONFIG else 'storage' if relation in _STORAGE else
                            'message' if relation in _MESSAGES else 'type_dependency' if relation in _TYPES else
                            'import_context' if relation in _IMPORTS else 'call')
                    edge_scope = ('declaration_context' if relation in _STORAGE | _TYPES | _IMPORTS else
                                  'class_context' if relation in _CONFIG and
                                  (not scoped_sites or all(not site.get('source_method') for site in scoped_sites)) else
                                  'class_context' if relation in _CALLS and method and not sites else scope)
                    if not add_step(edge, role, edge_scope, scoped_sites):
                        continue
                    if deferred_sites:
                        retained = steps[edge['id']].setdefault('deferred_call_sites', [])
                        retained.extend(site for site in deferred_sites if site not in retained)
                    status = edge.get('resolution_status')
                    if status in {'UNRESOLVED', 'AMBIGUOUS'}:
                        reason = 'STORAGE_IDENTITY_' if relation in _STORAGE else 'PROVIDER_IDENTITY_'
                        add_break(target, reason + status, edge, status)
                    # Mapping edges remain navigable, while type/import context
                    # cannot turn a declaration into an invoked implementation.
                    if relation in _STORAGE | _MESSAGES | (_CALLS - {'CALLS_COMPONENT'}):
                        if relation in _CALLS and status in {'UNRESOLVED', 'AMBIGUOUS'}:
                            # Symbolic endpoint reads can still explain the
                            # destination. They cannot resolve its provider.
                            queue.append((target, None, None, None, 'boundary_context', depth + 1))
                        else:
                            queue.append((target, None, None, None, edge_scope, depth + 1))
            if node.get('type') == 'API_OPERATION' and kind == 'provided_api' and current == anchor:
                if not any(e['relationship'] == 'INVOKES' for e in outgoing[current]):
                    add_break(current, 'HANDLER_MAPPING_NOT_RECORDED')
        trace = {
            'id': anchor, 'kind': kind, 'repository': nodes[anchor].get('repository'),
            'dependency_scope': ('TESTING' if nodes[anchor].get('properties', {}).get('dependency_scope') == 'TESTING'
                                 else 'PRODUCTION'),
            'label': nodes[anchor].get('name', anchor), 'node_ids': sorted(selected_nodes),
            'edge_ids': sorted(steps), 'steps': [steps[key] for key in sorted(steps)],
            'identity_bridges': [selected_bridges[key] for key in sorted(selected_bridges)],
            'breaks': [breaks[key] for key in sorted(breaks, key=str)],
            'limits': {'max_hops': max_hops, 'max_nodes': max_nodes, 'max_edges': max_edges,
                       'truncated': bool(omitted_edges) or any(b['reason'] == 'NODE_LIMIT' for b in breaks.values()),
                       'omitted_edge_ids': sorted(omitted_edges)},
            'summary': {'nodes': len(selected_nodes), 'edges': len(steps),
                        'by_role': dict(sorted(Counter(step['role'] for step in steps.values()).items()))},
            'evidence_limit': 'Static dependencies and declaration context do not establish executed end-to-end behavior.',
        }
        traces[anchor] = trace
        if trace['repository']:
            by_repository[trace['repository']].append(anchor)
        for identifier in selected_nodes:
            by_node[identifier].append(anchor)
    return {
        'node_roles': roles, 'traces': traces,
        'trace_index': {'schema_version': '1.0.0',
                        'by_repository': {key: sorted(value) for key, value in sorted(by_repository.items())},
                        'by_node': {key: sorted(value) for key, value in sorted(by_node.items())},
                        'counts': {'entries': len(traces), 'truncated': sum(t['limits']['truncated'] for t in traces.values()),
                                   'with_breaks': sum(bool(t['breaks']) for t in traces.values())}},
    }
