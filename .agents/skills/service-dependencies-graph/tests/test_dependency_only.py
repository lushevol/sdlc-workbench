"""Keep dependency snapshots independent from standalone knowledge services."""
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
publication = load_tool('generate_all_graphs')
snapshot = load_tool('snapshot')
validator = load_tool('validate_graph')


class DependencyOnlyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='dependency-only-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / 'generated'
        self.write('repos/client/package.json', '{"name":"@fixture/client"}')
        self.write('repos/client/src/index.ts', 'fetch("/orders");\n')

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def build(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(publication.main(['--workspace', str(self.root), '--out', str(self.output)]), 0)
        return json.loads((self.output / 'graph.json').read_bytes())

    def rewrite_graph(self, graph):
        raw = (json.dumps(graph) + '\n').encode()
        (self.output / 'graph.json').write_bytes(raw)
        manifest_path = self.output / 'manifest.json'
        manifest = json.loads(manifest_path.read_bytes())
        digest = hashlib.sha256(raw).hexdigest()
        manifest['graph_sha256'] = digest
        next(row for row in manifest['artifacts'] if row['path'] == 'graph.json').update(sha256=digest, bytes=len(raw))
        manifest_path.write_text(json.dumps(manifest))

    def test_invalid_unrelated_records_and_catalogs_do_not_affect_dependency_build_or_freshness(self):
        unrelated = [self.write('knowledge/records/policy.md', '---\ninvalid: [\n'),
                     self.write('knowledge/evidence/manifest.yaml', 'sources: [\n'),
                     self.write('registry/services.yaml', 'services: [\n')]
        before = {path: path.read_bytes() for path in unrelated}
        graph = self.build()
        self.assertNotIn('knowledge', graph)
        self.assertEqual(graph['generator']['version'], '2.6.0')
        self.assertTrue(all(set(node['dimensions']) <= {'RUNTIME', 'BUSINESS'} for node in graph['nodes']))
        self.assertTrue(any(edge['relationship'] == 'CALLS_REST' for edge in graph['edges']))
        self.assertEqual(validator.validate(graph, self.root), [])
        unrelated[0].write_text('A separate policy revision.\n')
        result = snapshot.query(self.output, 'coverage', {}, self.root)
        self.assertEqual(result['freshness']['status'], 'CURRENT')
        self.assertNotIn('knowledge_freshness', result)
        self.assertEqual({path: path.read_bytes() for path in unrelated[1:]},
                         {path: raw for path, raw in before.items() if path != unrelated[0]})

    def test_unrelated_source_changes_during_generation_do_not_block_publication(self):
        policy = self.write('knowledge/records/policy.md', 'Initial policy.\n')
        run = publication.run

        def change_policy_after_validation(*arguments, **keywords):
            run(*arguments, **keywords)
            if 'validate_graph' in arguments:
                policy.write_text('Changed standalone policy.\n')

        with patch.object(publication, 'run', side_effect=change_policy_after_validation):
            graph = self.build()
        self.assertEqual(policy.read_text(), 'Changed standalone policy.\n')
        self.assertEqual(validator.validate(graph, self.root), [])

    def test_retired_operations_and_removed_schema_fields_cannot_reenter_regular_queries(self):
        graph = self.build()
        self.assertEqual(set(snapshot.OPERATIONS), {'coverage', 'patterns', 'relationships', 'services', 'search', 'neighborhood'})
        for operation in ('knowledge', 'references', 'paths'):
            with self.subTest(operation=operation), self.assertRaises(snapshot.SnapshotError) as error:
                snapshot.query(self.output, operation, {}, self.root)
            self.assertEqual(error.exception.code, 'UNKNOWN_OPERATION')
        for change in ('envelope', 'node_dimension', 'edge_dimension'):
            with self.subTest(change=change):
                altered = deepcopy(graph)
                if change == 'envelope':
                    altered['knowledge'] = {'schema_version': '1.0.0', 'inputs': [], 'counts': {}, 'limitations': []}
                elif change == 'node_dimension':
                    altered['nodes'][0]['dimensions'] = ['KNOWLEDGE']
                else:
                    altered['edges'][0]['dimension'] = 'KNOWLEDGE'
                self.assertTrue(validator.validate(altered, self.root))
                self.rewrite_graph(altered)
                with self.assertRaises(snapshot.SnapshotError) as error:
                    snapshot.query(self.output, 'search', {'query': 'orders'}, self.root)
                self.assertEqual(error.exception.code, 'INVALID_SNAPSHOT')

    def test_valid_legacy_dependency_snapshot_remains_queryable(self):
        graph = self.build()
        graph['generator']['version'] = '2.0.0'
        self.rewrite_graph(graph)
        result = snapshot.query(self.output, 'search', {'query': 'orders'}, self.root)
        self.assertEqual(result['status'], 'SUCCEEDED')
        self.assertTrue(result['matches'])


if __name__ == '__main__':
    unittest.main()
