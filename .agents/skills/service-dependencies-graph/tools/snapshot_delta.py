"""Compare checksum-verified static graph snapshots without changing either bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .graph_query import architecture_relationships
from .snapshot import SnapshotError, _bundle, _read, query
from .repository_inventory import extraction_fingerprints


def _mapping(rows, field='id'):
    result = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(field), str) or row[field] in result:
            raise SnapshotError('INVALID_SNAPSHOT', 'Compared collections require unique text identities.')
        result[row[field]] = row
    return result


def _changes(before, after, field='id'):
    old, new = _mapping(before, field), _mapping(after, field)
    return {
        'added': [new[key] for key in sorted(new.keys() - old.keys())],
        'removed': [old[key] for key in sorted(old.keys() - new.keys())],
        'changed': [{'id': key, 'fields': sorted(name for name in old[key].keys() | new[key].keys()
                                               if name not in old[key] or name not in new[key] or old[key][name] != new[key][name]),
                     'before': old[key], 'after': new[key]}
                    for key in sorted(old.keys() & new.keys()) if old[key] != new[key]],
        'unchanged': sum(old[key] == new[key] for key in old.keys() & new.keys()),
    }


def _ids(delta):
    return {row['id'] for name in ('added', 'removed', 'changed') for row in delta[name]}


def _evidence_rows(evidence, identifiers):
    return [evidence[key] for key in sorted(identifiers) if key in evidence]


def _side(path, workspace, check_current):
    try:
        manifest, artifacts, manifest_sha = _bundle(path)
        graph = _read(artifacts, 'graph.json')
        coverage = _read(artifacts, 'analysis-coverage.json')
        if graph.get('schema_version') != '2.0.0':
            raise SnapshotError('INVALID_SNAPSHOT', 'Compare supported graph schema_version 2.0.0 bundles.')
        for name in ('nodes', 'edges', 'evidence', 'repositories'):
            _mapping(graph[name])
        nodes, evidence = _mapping(graph['nodes']), _mapping(graph['evidence'])
        for edge in graph['edges']:
            if edge['source'] not in nodes or edge['target'] not in nodes or not set(edge['evidence']) <= evidence.keys():
                raise SnapshotError('INVALID_SNAPSHOT', 'A compared edge has dangling node or evidence identities.')
        for node in graph['nodes']:
            if not set(node['evidence']) <= evidence.keys():
                raise SnapshotError('INVALID_SNAPSHOT', 'A compared node has dangling evidence identities.')
        freshness = {'status': 'NOT_CHECKED', 'changed_paths': []}
        context_freshness = None
        knowledge_freshness = ({'status': 'NOT_CHECKED', 'changed_paths': []} if 'knowledge' in graph else
                               {'status': 'NOT_AVAILABLE', 'changed_paths': [],
                                'reason': 'This snapshot predates the knowledge projection. Rebuild it to add this layer.'})
        if check_current:
            current = query(path, 'coverage', {}, workspace)
            freshness = current['freshness']
            context_freshness = current.get('architecture_context', {}).get('freshness')
            knowledge_freshness = current['knowledge_freshness']
        instructions = workspace / 'relationships/service-dependencies/initial-instructions.md'
        instruction_identity = {'path': 'relationships/service-dependencies/initial-instructions.md',
                                'status': 'UNKNOWN', 'saved_sha256': None,
                                'current_sha256': hashlib.sha256(instructions.read_bytes()).hexdigest() if check_current and instructions.is_file() else None,
                                'reason': 'No instruction fingerprint is captured by this snapshot.'}
        if manifest.get('architecture_context'):
            provenance = _read(artifacts, 'architecture-context-provenance.json')
            binding = next((row for row in provenance['sources'] if row['path'] == instruction_identity['path']), None)
            if binding:
                instruction_identity['saved_sha256'] = binding['sha256']
                instruction_identity['status'] = ('NOT_CHECKED' if not check_current else 'CURRENT' if instruction_identity['current_sha256'] == binding['sha256'] else 'STALE')
                instruction_identity.pop('reason')
        identity = {'path': str(path), 'generated_at': manifest['generated_at'],
                    'manifest_sha256': manifest_sha, 'graph_sha256': manifest['graph_sha256'],
                    'generator': graph.get('generator'), 'schema_version': graph['schema_version'],
                    'counts': {name: len(graph[name]) for name in ('nodes', 'edges', 'evidence', 'repositories')},
                    'architecture_context_present': bool(manifest.get('architecture_context')),
                    'initial_instruction_freshness': instruction_identity,
                    'current_freshness': freshness, 'architecture_context_freshness': context_freshness,
                    'knowledge_freshness': knowledge_freshness,
                    'coverage_limits': coverage.get('limitations', [])}
        return identity, graph, coverage
    except SnapshotError:
        raise
    except (KeyError, TypeError, ValueError) as error:
        raise SnapshotError('INVALID_SNAPSHOT', 'The compared graph bundle has invalid structure.') from error


def compare_snapshots(baseline: Path, candidate: Path, workspace: Path, *, check_current: bool = True) -> dict:
    """Return exact saved differences and direct static consumers; perform no build or network call."""
    workspace = Path(workspace).resolve()
    baseline, candidate = Path(baseline).resolve(), Path(candidate).resolve()
    before_identity, before, old_coverage = _side(baseline, workspace, check_current)
    after_identity, after, new_coverage = _side(candidate, workspace, check_current)
    changes = {name: _changes(before[name], after[name]) for name in ('nodes', 'edges', 'evidence')}
    changes['repositories'] = _changes(old_coverage['repositories'], new_coverage['repositories'], 'path')
    changes['source_inventory'] = _changes(
        [{'path': path, 'fingerprint': list(value)} for path, value in extraction_fingerprints(old_coverage).items()],
        [{'path': path, 'fingerprint': list(value)} for path, value in extraction_fingerprints(new_coverage).items()], 'path')
    changes['claims'] = _changes(architecture_relationships(before), architecture_relationships(after), 'claim_id')
    old_evidence, new_evidence = _mapping(before['evidence']), _mapping(after['evidence'])
    for name in ('nodes', 'edges'):
        for row in changes[name]['changed']:
            row['evidence_before'] = _evidence_rows(old_evidence, row['before'].get('evidence', []))
            row['evidence_after'] = _evidence_rows(new_evidence, row['after'].get('evidence', []))
    changed_nodes, changed_edges, changed_evidence = (_ids(changes[key]) for key in ('nodes', 'edges', 'evidence'))
    consumers = {}
    reinvestigate = []
    seen_reinvestigation = {}
    for side, graph, identity in [('baseline', before, before_identity), ('candidate', after, after_identity)]:
        nodes = _mapping(graph['nodes'])
        for edge in graph['edges']:
            reasons = []
            if edge['id'] in changed_edges:
                reasons.append('EDGE_CHANGED')
            if edge['target'] in changed_nodes:
                reasons.append('TARGET_NODE_CHANGED')
            if set(edge['evidence']) & changed_evidence:
                reasons.append('EVIDENCE_CHANGED')
            if not reasons or edge['relationship'] == 'CONTAINS':
                continue
            source = nodes[edge['source']]
            entry = consumers.setdefault(source['id'], {'id': source['id'], 'name': source['name'],
                'repository': source.get('repository'), 'source_paths': source.get('source_paths', []), 'affected_edges': []})
            entry['affected_edges'].append({'snapshot': side, 'edge_id': edge['id'],
                                           'relationship': edge['relationship'], 'reasons': reasons})
        paths = set(identity['current_freshness'].get('changed_paths', []))
        for claim in architecture_relationships(graph):
            stale_refs = [ref for ref in claim.get('source_refs', []) if ref.get('path') in paths]
            if stale_refs:
                key = (identity['manifest_sha256'], claim['claim_id'])
                if key in seen_reinvestigation:
                    seen_reinvestigation[key]['snapshots'].append(side)
                else:
                    item = {'snapshots': [side], 'claim_id': claim['claim_id'], 'reason': 'STALE_SOURCE_REFERENCES',
                            'source_refs': stale_refs, 'owner': None, 'next_action': 'Reinspect cited source before reusing this claim.'}
                    seen_reinvestigation[key] = item
                    reinvestigate.append(item)
    counts = {name: {key: len(delta[key]) for key in ('added', 'removed', 'changed')} for name, delta in changes.items()}
    status = 'UNCHANGED' if not any(value for row in counts.values() for value in row.values()) else 'CHANGED'
    scope_changed = before_identity['architecture_context_present'] != after_identity['architecture_context_present']
    return {'schema_version': 1, 'status': 'SUCCEEDED', 'comparison': status,
            'baseline': before_identity, 'candidate': after_identity, 'counts': counts, 'changes': changes,
            'architecture_context_scope_changed': scope_changed,
            'repository_delta_meaning': 'repositories includes extraction coverage; source_inventory compares source-selection fingerprints separately',
            'claim_removal_interpretation': ('CONTEXT_SCOPE_DIFFERENCE' if scope_changed else 'SAVED_SNAPSHOT_DIFFERENCE'),
            'affected_consumers': [consumers[key] for key in sorted(consumers)], 'affected_consumer_scope': 'DIRECT_STATIC_ONLY',
            'requires_reinvestigation': reinvestigate, 'contract_case_links': [],
            'contract_case_link_status': 'UNAVAILABLE_IN_SNAPSHOT',
            'limitations': ['Static differences do not establish runtime calls, production impact, or broken dependencies.',
                'Added and removed records describe saved snapshots; extraction scope and generator differences require review.',
                'Omitted architecture context removes supplied claims from this snapshot; it does not disprove those relationships.',
                'Affected consumers include direct static sources only; dynamic dependencies and transitive impact remain unexamined.',
                'Current freshness compares recorded source and context fingerprints within inventory exclusions.',
                'Knowledge freshness separately compares selected projection input bytes; it does not establish authority, applicability, or execution.',
                'The initial instruction Markdown has no captured baseline fingerprint unless cited by the saved context.',
                'Contract and test-case links are unavailable unless exact relationship evidence supplies those identities.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=Path.cwd())
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--skip-current-check', action='store_true')
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    resolve = lambda path: path if path.is_absolute() else workspace / path
    try:
        result = compare_snapshots(resolve(args.baseline), resolve(args.candidate), workspace,
                                   check_current=not args.skip_current_check)
    except (SnapshotError, OSError) as error:
        print(json.dumps({'status': 'ERROR', 'code': getattr(error, 'code', 'UNAVAILABLE'), 'message': str(error)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0
