"""Retain bounded checks of the actual source-only and investigated bundles."""
from collections import Counter
import gc
import hashlib
import json
from pathlib import Path
import runpy

root = Path(__file__).resolve().parents[4]
load = runpy.run_path(str(root / '.agents/skills/service-dependencies-graph/tests/_support.py'))['load_tool']
snapshot = load('snapshot')
fingerprints = load('repository_inventory').extraction_fingerprints
published = root / 'relationships/service-dependencies/generated'
source_only = root / '.workbench/graph-snippet-discovery-20261118/source-only'
baseline = json.loads(Path(__file__).with_name('baseline.json').read_bytes())
bundles = {}
inventories = []
for name, output in (('source_only', source_only), ('investigated', published)):
    graph = json.loads((output / 'graph.json').read_bytes())
    bundles[name] = {'generator': graph['generator'],
                     'counts': {key: len(graph[key]) for key in ('repositories', 'nodes', 'edges', 'evidence')},
                     'graph_sha256': hashlib.sha256((output / 'graph.json').read_bytes()).hexdigest(),
                     'manifest_sha256': hashlib.sha256((output / 'manifest.json').read_bytes()).hexdigest()}
    del graph
    checked = snapshot.query(output, 'coverage', {}, root)
    assert checked['freshness']['status'] == 'CURRENT'
    bundles[name]['freshness'] = checked['freshness']
    inventories.append(fingerprints(checked['coverage']))
    del checked
    gc.collect()
assert inventories[0] == inventories[1]
audit = json.loads((published / 'coverage-declarations.json').read_bytes())
rows = audit['pattern_candidates']
summary = {
    'candidate_count': len(rows),
    'occurrence_count': sum(len(row['occurrences']) for row in rows),
    'accountability': dict(Counter(row['accountability'] for row in rows)),
    'discovery_inventory': audit['discovery_inventory']['summary'],
    'families': audit['pattern_summary']['families'],
    'solace_protocol_hint_candidates': sum('SOLACE' in row['protocol_hints'] for row in rows),
    'discovery_sha256_by_repository': {key: value['content_sha256']
                                        for key, value in audit['discovery_inventory']['repositories'].items()},
}
sources = {(row['repository'], row['path']): row['sha256']
           for row in audit['discovery_inventory']['files'] if row['status'] == 'SCANNED'}
assert all(row['source_sha256'] == sources[row['repository'], row['path']] for row in rows)
largest_id = max(rows, key=lambda row: row['occurrence_count'])['id']
del rows, audit, sources
gc.collect()
offset, pages, seen = 0, 0, []
while pages < 2:
    batch = snapshot.query(published, 'patterns', {
        'candidate_id': largest_id, 'include_snippets': True,
        'occurrence_limit': 2, 'occurrence_offset': offset, 'limit': 1,
    }, root)
    assert batch['matching_total'] == 1
    match, = batch['matches']
    assert len(match['occurrences']) == 2
    assert match['occurrence_count'] > 1000
    seen.extend((item['start_line'], item['start_column'], item['pattern_id']) for item in match['occurrences'])
    offset = match['next_occurrence_offset']
    assert offset is not None
    pages += 1
assert len(set(seen)) == 4
context = json.loads((published / 'architecture-context.json').read_bytes())
result = {
    'status': 'PASSED', 'bundles': bundles, 'matching_source_inventories': True,
    'baseline': {'pattern_candidates': baseline['pattern_candidates'],
                 'scanned_files': baseline['pattern_summary']['scanned_files']},
    'current': summary, 'every_candidate_hash_matches_captured_inventory': True,
    'bounded_real_query': {'candidate_id': largest_id, 'pages_checked': pages,
                           'occurrences_per_page': 2, 'distinct_occurrences_seen': len(set(seen))},
    'investigated_context': {'relationships': len(context['relationships']),
                             'sources': len(context['sources']),
                             'source_kinds': dict(Counter(row['kind'] for row in context['sources']))},
    'limits': ['Candidates and occurrences include examples, documentation, test data, and repeated calls.',
               'Candidate counts do not measure missing dependencies or semantic recall.',
               'The newly expanded corpus has not received complete semantic adjudication.',
               'No Solace protocol hints in this source snapshot do not prove absence of all Solace integrations.',
               'Source-only and investigated bundles establish static evidence, not live service connectivity.'],
}
Path(__file__).with_name('graph-validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'current': summary['discovery_inventory'],
                  'candidates': summary['candidate_count'], 'occurrences': summary['occurrence_count']}))
