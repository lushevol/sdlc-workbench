"""Integrate investigated architecture claims without replacing extracted facts."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import PurePosixPath

from .architecture_context import ContextInput, validate_document, validate_source_ranges


def _identity(prefix: str, *parts: str) -> str:
    return prefix + ':' + hashlib.sha256('\x1f'.join(parts).encode()).hexdigest()[:24]


def apply_context(graph, captured: ContextInput) -> None:
    """Apply version 1.1 decisions before canonical projections are generated.

    Version 1.0 remains a captured annotation contract. It never changes facts.
    Human/agent source review is explicit input; this function validates evidence
    identity and bindings, not the semantic correctness of a review decision.
    """
    document = captured.document
    if document['schema_version'] == '1.0.0':
        return
    repositories = {row['id']: row for row in graph.repositories}
    validate_document(document, set(repositories))
    validate_source_ranges(document, captured.sources)
    sources = {row['id']: row for row in document['sources']}
    subjects = {row['id']: row for row in document['subjects']}
    layers = {row['id']: row for row in document['layers']}
    relationships = {row['id']: row for row in document['relationships']}
    existing_edges = {row['id']: row for row in graph.edges.values()}

    def source_repository(path):
        candidates = [row['id'] for row in graph.repositories
                      if PurePosixPath(path).is_relative_to(PurePosixPath(row['path']))]
        if len(candidates) > 1:
            raise ValueError('Architecture source belongs to ambiguous repository roots: ' + path)
        return candidates[0] if candidates else None

    def evidence(source_id, line, end_line, claim):
        row = sources[source_id]
        # Keep source values out of declarations. Captured hashes bind the full bytes.
        return graph.add_evidence(
            source_repository(row['path']), row['path'], line,
            f"Architecture claim {claim}; reviewed lines {line}-{end_line}; SHA-256 {row['sha256']}",
            'architecture-source-review' if row['kind'] == 'SOURCE_REVIEW' else 'architecture-user-input',
            directness='SEMANTIC')

    bindings = {}
    repository_roots = {}
    for node in graph.nodes.values():
        if node.get('repository') is not None and node['type'] in {'APPLICATION', 'SERVICE'}:
            repository_roots.setdefault(node['repository'], []).append(node['id'])
    repository_subjects = set()
    for subject in document['subjects']:
        node_id = subject.get('node_id')
        if node_id is not None:
            node = graph.nodes.get(node_id)
            if node is None or node.get('repository') != subject['repository']:
                raise ValueError('Architecture subject node binding does not match repository: ' + subject['id'])
        elif subject['repository'] is not None:
            candidates = repository_roots.get(subject['repository'], [])
            if len(candidates) != 1:
                raise ValueError('Architecture subject requires an explicit node_id: ' + subject['id'])
            node_id = candidates[0]
        else:
            node_id = _identity('architecture-boundary', subject['id'])
        bindings[subject['id']] = node_id
        # Only a unique repository analysis root can stand for owned callsites.
        # Component/API bindings and roots of multi-root repositories stay exact.
        if subject['repository'] is not None and repository_roots.get(subject['repository']) == [node_id]:
            repository_subjects.add(subject['id'])

    # Validate every relationship before mutating graph collections.
    for decision in document['investigations']:
        claim = relationships[decision['relationship_id']]
        left, right = subjects[claim['source']], subjects[claim['target']]
        if decision['status'] == 'SUPPORTED':
            reviewed_repositories = {source_repository(sources[ref['source_id']]['path'])
                                     for ref in decision['source_refs']
                                     if sources[ref['source_id']]['kind'] == 'SOURCE_REVIEW'}
            required = {row['repository'] for row in (left, right) if row['repository'] is not None}
            if not required <= reviewed_repositories:
                raise ValueError('SUPPORTED relationship requires source ranges from each bound repository: ' + claim['id'])
        for edge_id in decision['canonical_edge_ids']:
            edge = existing_edges.get(edge_id)
            if edge is None:
                raise ValueError('Investigation references an unknown canonical edge: ' + edge_id)
            for endpoint, subject in ((edge['source'], left), (edge['target'], right)):
                canonical_node = graph.nodes[endpoint]
                if subject['repository'] is not None:
                    if canonical_node.get('repository') != subject['repository']:
                        raise ValueError('Investigation canonical edge direction or repository disagrees: ' + claim['id'])
                    if endpoint != bindings[subject['id']] and subject['id'] not in repository_subjects:
                        raise ValueError('Investigation canonical edge does not match exact subject node binding: ' + claim['id'])
                elif endpoint != bindings[subject['id']]:
                    # An unbound subject must explicitly name a pre-existing external node.
                    raise ValueError('Investigation external endpoint requires matching node_id: ' + claim['id'])
            if decision['status'] == 'SUPPORTED' and edge['assertion_status'] != 'CONFIRMED':
                raise ValueError('SUPPORTED investigation cannot promote an inferred canonical edge: ' + edge_id)

    for subject in document['subjects']:
        layer = layers.get(subject['layer_id'], {})
        evs = [evidence(source_id, 1, 1, subject['id']) for source_id in subject['source_ids']]
        metadata = {key: deepcopy(subject[key]) for key in
                    ('id', 'label', 'role', 'layer_id', 'status', 'description', 'source_ids')}
        metadata.update(layer_label=layer.get('label'), layer_order=layer.get('order'), evidence_ids=evs)
        node_id = bindings[subject['id']]
        if node_id not in graph.nodes:
            graph.add_node(
                node_id, 'ARCHITECTURE_BOUNDARY', subject['label'], None,
                dimensions=['RUNTIME'], component_kind=subject['role'],
                functional_role=subject['role'], business_meaning=subject['description'],
                source_paths=[], evidence=evs, assertion_status='INFERRED',
                properties={'origin': 'ARCHITECTURE_INVESTIGATION', 'provider_status': 'NOT_ESTABLISHED'})
        node = graph.nodes[node_id]
        node.setdefault('properties', {}).setdefault('architecture_subjects', []).append(metadata)
        node['properties']['architecture_subjects'].sort(key=lambda row: row['id'])
        node['evidence'] = sorted(set(node['evidence']) | set(evs))

    for decision in document['investigations']:
        claim = relationships[decision['relationship_id']]
        refs = [{**ref, **{key: sources[ref['source_id']][key] for key in ('path', 'sha256', 'revision', 'kind')}}
                for ref in decision['source_refs']]
        reviewed = [evidence(ref['source_id'], ref['line'], ref['end_line'], claim['id']) for ref in refs]
        reported = [evidence(source_id, 1, 1, claim['id']) for source_id in claim['source_ids']]
        evidence_ids = sorted(set(reviewed + reported))
        metadata = {
            'investigation_id': decision['id'], 'claim_id': claim['id'],
            'investigation_status': decision['status'], 'family': decision['family'],
            'kind': claim['kind'], 'description': claim['description'], 'rationale': decision['rationale'],
            'source_subject': claim['source'], 'target_subject': claim['target'],
            'source_refs': refs, 'evidence_ids': evidence_ids,
            'runtime_status': 'NOT_VERIFIED',
        }
        if decision['canonical_edge_ids']:
            for edge_id in decision['canonical_edge_ids']:
                edge = existing_edges[edge_id]
                edge.setdefault('properties', {}).setdefault('architecture_claims', []).append(deepcopy(metadata))
                edge['properties']['architecture_claims'].sort(key=lambda row: row['claim_id'])
                edge['evidence'] = sorted(set(edge['evidence']) | set(evidence_ids))
        else:
            left, right = bindings[claim['source']], bindings[claim['target']]
            edge_id = _identity('architecture-edge', claim['id'])
            edge = {
                'id': edge_id, 'source': left, 'target': right,
                'relationship': 'REVIEWED_RELATIONSHIP', 'dimension': 'RUNTIME',
                'evidence': evidence_ids,
                'assertion_status': 'CONFIRMED' if decision['status'] == 'SUPPORTED' else 'INFERRED',
                'resolution_status': 'UNRESOLVED',
                'properties': {**deepcopy(metadata), 'origin': 'ARCHITECTURE_INVESTIGATION',
                               'architecture_claims': [deepcopy(metadata)]},
            }
            # Authored claims between identical endpoints retain separate identities.
            graph.edges[(left, right, 'REVIEWED_RELATIONSHIP', claim['id'])] = edge
