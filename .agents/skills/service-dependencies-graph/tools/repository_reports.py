"""Reproducible repository-level projections of canonical graph facts."""
from __future__ import annotations

from collections import Counter, defaultdict
from .output_standard import finalize_report, render_prose


def relationship_report(document):
    nodes = {n['id']: n for n in document['nodes']}
    rows = []
    frontiers = []
    topics = defaultdict(lambda: {'PUBLISHES': [], 'CONSUMES': []})
    for edge in document['edges']:
        source, target = nodes[edge['source']], nodes[edge['target']]
        left, right = source.get('repository'), target.get('repository')
        if left and right and left != right:
            rows.append({'source_repository': left, 'target_repository': right,
                         'relationship': edge['relationship'], 'assertion_status': edge['assertion_status'],
                         'resolution_status': edge.get('resolution_status', 'RESOLVED'),
                         'edge_ids': [edge['id']], 'evidence': edge['evidence'],
                         'dependency_kind': edge.get('properties', {}).get('dependency_kind', edge['dimension'])})
        elif left and edge.get('resolution_status') in {'UNRESOLVED', 'AMBIGUOUS'}:
            frontiers.append({'repository': left, 'target': target['id'], 'name': target['name'],
                              'relationship': edge['relationship'], 'status': edge['resolution_status'],
                              'edge_id': edge['id'], 'evidence': edge['evidence'],
                              'dependency_kind': edge.get('properties', {}).get('dependency_kind', edge['dimension']),
                              'assertion_status': edge['assertion_status'],
                              'candidate_providers': edge.get('properties', {}).get('candidate_providers', [])})
        if (left and target['type'] == 'MESSAGE_CHANNEL' and edge['relationship'] in {'PUBLISHES', 'CONSUMES'}
                and edge['assertion_status'] == 'CONFIRMED' and target.get('properties', {}).get('protocol') == 'KAFKA'):
            topics[target['name']][edge['relationship']].append((left, edge))
    # These are deliberately report candidates, never resolved canonical edges.
    for topic, directions in sorted(topics.items()):
        for producer, outgoing in directions['PUBLISHES']:
            for consumer, incoming in directions['CONSUMES']:
                if producer == consumer:
                    continue
                rows.append({'source_repository': producer, 'target_repository': consumer,
                             'relationship': 'KAFKA_TOPIC_CANDIDATE', 'topic': topic,
                             'assertion_status': 'INFERRED', 'resolution_status': 'UNRESOLVED',
                             'dependency_kind': 'RUNTIME', 'reason': 'Topic names match; cluster/environment identity is not established',
                             'edge_ids': sorted([outgoing['id'], incoming['id']]),
                             'evidence': sorted(set(outgoing['evidence']) | set(incoming['evidence']))})
    rows.sort(key=lambda row: (row['source_repository'], row['target_repository'], row['relationship'], row['edge_ids']))
    return {'schema_version': '1.0.0', 'relationships': rows, 'unresolved_boundaries': frontiers,
            'counts': {'resolved_relationships': sum(r['resolution_status'] == 'RESOLVED' for r in rows),
                       'candidate_relationships': sum(r['resolution_status'] != 'RESOLVED' for r in rows),
                       'unresolved_boundaries': len(frontiers)}}


def coverage_report(document, census):
    report = dict(census)
    report['repositories'] = [dict(row) for row in census['repositories']]
    for row in report['repositories']:
        repo = 'repo:' + row['name']
        evidence = [ev for ev in document['evidence'] if ev.get('repository') == repo]
        diagnostics = [d for d in document['diagnostics'] if d.get('repository') == repo or d.get('path') == row['path']]
        row['evidence_files'] = len({ev['path'] for ev in evidence})
        row['extractors'] = dict(sorted(Counter(ev['extractor'] for ev in evidence).items()))
        row['diagnostics'] = dict(sorted(Counter(d['code'] for d in diagnostics).items()))
    report['generated_at'] = document['generated_at']
    report['limitations'] = [
        'Static declarations do not prove deployment, reachability, or execution.',
        'Runtime extraction supports root src layouts. Nested manifests supply package identities and build dependencies.',
        'The inventory also lists nested modules, Gradle, Kotlin, and other languages.',
        'Package links show declared dependencies. They do not prove version compatibility or installed artifacts.',
        'Service aliases include declared profile variants. The analysis does not select an active environment.',
        'HTTP joins require an exposed provider, compatible method, and path. Absolute URLs also require a declared authority.',
        'Static nginx rewrites can identify a local REST operation through a declared upstream identity.',
        'Spring open-apis routes declare transport paths. They do not establish implemented handlers.',
        'Nginx templates require environment values. The graph retains their source evidence and unresolved diagnostics.',
        'Kafka topic matches require cluster identity before confirmation. Equal table names do not prove a shared database.',
        'GraphQL providers, dynamic configuration, generated clients, and reflection can remain unresolved.',
        'Evidence-file counts measure provenance coverage. They do not measure semantic code coverage.',
        *census.get('registry_limits', []),
    ]
    return report


def markdown_report(coverage, relationships):
    lines = ['# Repository relationship analysis', '',
             'This report describes static source declarations. See graph.json for canonical facts and evidence.', '',
             f"Snapshot time: `{coverage['generated_at']}`.", '',
             '## Inventory', '', '| Repository | Status | Source files | Evidence files |',
             '| --- | --- | ---: | ---: |']
    for row in coverage['repositories']:
        lines.append(f"| {row['name']} | {row['status']} | {row['source_files']} | {row['evidence_files']} |")
    lines += ['', '## Repository links', '', '| Consumer/source | Provider/target | Relationship | Status |', '| --- | --- | --- | --- |']
    seen = set()
    for row in relationships['relationships']:
        fields = tuple(row[k] for k in ('source_repository', 'target_repository', 'relationship', 'resolution_status'))
        if fields not in seen:
            lines.append('| ' + ' | '.join(fields) + ' |')
            seen.add(fields)
    lines += ['', '## Coverage findings', '',
              '| Evidence | Consequence | Owner | Next action |', '| --- | --- | --- | --- |']
    for row in coverage['repositories']:
        if row['status'] in {'MISSING', 'UNSUPPORTED', 'PARTIAL'} or row['diagnostics']:
            lines.append(f"| `{row['path']}`: `{row['status']}`; see analysis-coverage.json | Dependency coverage has explicit limits. | UNKNOWN | Review source diagnostics and unresolved boundaries. |")
    lines += ['', '## Limits and follow-up', '']
    lines += ['- ' + render_prose(limit) for limit in coverage['limitations']]
    for row in coverage['repositories']:
        lines += [f"- {render_prose(row['name'])}: {render_prose(limit)}" for limit in row['limitations']]
    lines += ['', f"Unresolved or ambiguous boundaries: {relationships['counts']['unresolved_boundaries']}. Inspect repository-relationships.json for source evidence and candidates.", '']
    authored = {f'limitation[{index}]': value for index, value in enumerate(coverage['limitations'])}
    for row in coverage['repositories']:
        for index, value in enumerate(row['limitations']):
            authored[f"{row['name']}.limitations[{index}]"] = value
    return finalize_report('\n'.join(lines), authored_fields=authored)
