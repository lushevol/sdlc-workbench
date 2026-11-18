"""Verify the current dependency-only graph and retain compact evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--baseline', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[4]
output = root / 'relationships/service-dependencies/generated'
graph = json.loads((output / 'graph.json').read_bytes())
manifest = json.loads((output / 'manifest.json').read_bytes())
load = runpy.run_path(str(root / '.agents/skills/service-dependencies-graph/scripts/graph.py'))['load_tool']
assert graph['generator']['version'] == '2.6.0'
assert 'knowledge' not in graph
assert all(set(node['dimensions']) <= {'RUNTIME', 'BUSINESS'} for node in graph['nodes'])
assert all(edge['dimension'] in {'RUNTIME', 'BUSINESS'} for edge in graph['edges'])
assert all(row.get('properties', {}).get('projection') != 'knowledge' for row in graph['nodes'] + graph['edges'])
assert all(not row['path'].startswith('knowledge/') for row in graph['evidence'])
assert not load('validate_graph').validate(graph, root)
assert 'knowledge' not in (root / '.agents/skills/service-dependencies-graph/tools/viewer.html').read_text().casefold()
viewer = (output / 'relationship-viewer.html').read_text()
assert 'knowledge-workspace' not in viewer and 'knowledge-tab' not in viewer
for row in manifest['artifacts']:
    with (output / row['path']).open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == row['sha256'], row['path']
graph_digest = hashlib.sha256((output / 'graph.json').read_bytes()).hexdigest()
assert manifest['graph_sha256'] == graph_digest
snapshot = load('snapshot')
expected = {'coverage', 'patterns', 'relationships', 'services', 'search', 'neighborhood'}
assert set(snapshot.OPERATIONS) == expected
for operation in ('knowledge', 'references', 'paths'):
    try:
        snapshot.query(output, operation, {}, root)
    except snapshot.SnapshotError as error:
        assert error.code == 'UNKNOWN_OPERATION'
    else:
        raise AssertionError(operation)
coverage = snapshot.query(output, 'coverage', {}, root)
assert coverage['freshness']['status'] == 'CURRENT', coverage['freshness']
assert coverage['architecture_context']['freshness']['status'] == 'CURRENT'
assert 'knowledge_freshness' not in coverage
result = {
    'status': 'PASSED', 'generator': graph['generator'], 'graph_sha256': graph_digest,
    'counts': {key: len(graph[key]) for key in ('repositories', 'nodes', 'edges', 'evidence')},
    'knowledge_envelope': False, 'knowledge_nodes': 0, 'knowledge_edges': 0,
    'knowledge_input_paths': [], 'knowledge_viewer_interface': False,
    'artifact_checksums_verified': len(manifest['artifacts']),
    'operations': sorted(expected), 'retired_operations': 'UNKNOWN_OPERATION',
    'freshness': coverage['freshness'],
    'architecture_freshness': coverage['architecture_context']['freshness'],
    'limits': ['Static evidence does not establish deployment or runtime execution.',
               'Broad discovery candidates still require source interpretation.'],
}
if args.baseline:
    before = json.loads(args.baseline.read_bytes())
    comparison = {}
    for key in ('nodes', 'edges'):
        old = {row['id']: row for row in before[key]
               if row.get('dimension') != 'KNOWLEDGE' and 'KNOWLEDGE' not in row.get('dimensions', [])}
        new = {row['id']: row for row in graph[key]}
        changed = sorted(identity for identity in old.keys() & new.keys() if old[identity] != new[identity])
        comparison[key] = {'removed': len(old.keys() - new.keys()), 'added': len(new.keys() - old.keys()),
                           'modified': len(changed)}
    old_repos = {row['id']: row for row in before['repositories']}
    comparison['changed_repositories'] = [row['id'] for row in graph['repositories'] if old_repos.get(row['id']) != row]
    comparison['reason'] = 'The rebuild also captures current repository source revisions and reviewed BFF source bindings.'
    result['dependency_comparison'] = comparison
Path(__file__).with_name('graph-validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
