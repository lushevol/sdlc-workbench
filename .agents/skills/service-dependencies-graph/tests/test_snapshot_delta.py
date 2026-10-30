"""Verify saved snapshot differences, integrity rejection, and freshness limits."""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
module = load_tool('snapshot_delta')
builder = load_tool('build_graph')
publication = load_tool('generate_all_graphs')


class SnapshotDeltaTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='graph-delta-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / 'repos/ui/client/src/index.ts'
        self.source.parent.mkdir(parents=True)
        (self.source.parent.parent / 'package.json').write_text('{"name":"@fixture/client"}')
        self.source.write_text('export const ready = true;\n')
        self.baseline = self.build('baseline')

    def build(self, name):
        output = self.root / name
        with redirect_stdout(io.StringIO()):
            status = builder.main(['--workspace', str(self.root), '--repos', str(self.root / 'repos'), '--out', str(output)])
        self.assertEqual(status, 0)
        publication.write_ai_outputs(output, self.root / 'absent.json')
        return output

    def compare(self, candidate=None, check_current=False):
        return module.compare_snapshots(self.baseline, candidate or self.baseline, self.root, check_current=check_current)

    def rewrite_graph(self, graph):
        path = self.baseline / 'graph.json'
        path.write_text(json.dumps(graph))
        manifest_path = self.baseline / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest['graph_sha256'] = digest
        next(row for row in manifest['artifacts'] if row['path'] == 'graph.json')['sha256'] = digest
        manifest_path.write_text(json.dumps(manifest))

    def test_given_same_snapshot_when_comparing_then_no_changes_or_affected_consumers_are_invented(self):
        result = self.compare()
        self.assertEqual(result['comparison'], 'UNCHANGED')
        self.assertFalse(result['affected_consumers'])
        self.assertTrue(all(value == 0 for counts in result['counts'].values() for value in counts.values()))
        self.assertEqual(result['baseline']['current_freshness']['status'], 'NOT_CHECKED')

    def test_given_new_http_dependency_when_comparing_then_exact_nodes_edges_and_direct_consumers_are_retained(self):
        self.source.write_text("export const ready = true;\nfetch('/new-operation');\n")
        candidate = self.build('candidate')
        result = self.compare(candidate)
        self.assertEqual(result['comparison'], 'CHANGED')
        self.assertGreater(result['counts']['edges']['added'], 0)
        self.assertTrue(any(row.get('properties', {}).get('path') == '/new-operation' for row in result['changes']['nodes']['added']))
        self.assertTrue(result['affected_consumers'])
        self.assertEqual(result['affected_consumer_scope'], 'DIRECT_STATIC_ONLY')
        self.assertFalse(result['contract_case_links'])
        self.assertEqual(result['contract_case_link_status'], 'UNAVAILABLE_IN_SNAPSHOT')

    def test_given_source_changed_after_snapshot_when_checking_freshness_then_saved_difference_remains_unchanged_but_sources_are_stale(self):
        self.source.write_text('export const ready = false;\n')
        result = self.compare(check_current=True)
        self.assertEqual(result['comparison'], 'UNCHANGED')
        self.assertEqual(result['baseline']['current_freshness']['status'], 'STALE')
        self.assertIn('repos/ui/client', result['baseline']['current_freshness']['changed_paths'])

    def test_given_changed_artifact_bytes_when_comparing_then_checksum_mismatch_is_rejected(self):
        with (self.baseline / 'graph.json').open('ab') as output:
            output.write(b'\n')
        with self.assertRaisesRegex(module.SnapshotError, 'manifest'):
            self.compare()

    def test_given_duplicate_ids_with_updated_checksums_when_comparing_then_the_ambiguous_graph_is_rejected(self):
        graph = json.loads((self.baseline / 'graph.json').read_text())
        graph['nodes'].append(graph['nodes'][0])
        self.rewrite_graph(graph)
        with self.assertRaisesRegex(module.SnapshotError, 'unique'):
            self.compare()

    def test_given_dangling_edge_with_updated_checksums_when_comparing_then_the_broken_reference_is_rejected(self):
        graph = json.loads((self.baseline / 'graph.json').read_text())
        graph['edges'][0]['target'] = 'absent-node'
        self.rewrite_graph(graph)
        with self.assertRaisesRegex(module.SnapshotError, 'dangling'):
            self.compare()

    def test_given_unsafe_artifact_path_when_comparing_then_external_artifact_reads_are_rejected(self):
        path = self.baseline / 'manifest.json'
        manifest = json.loads(path.read_text())
        manifest['artifacts'][0]['path'] = '../external.json'
        path.write_text(json.dumps(manifest))
        with self.assertRaises(module.SnapshotError):
            self.compare()

    def test_given_changed_record_when_comparing_then_before_after_and_source_evidence_remain_separate(self):
        candidate = self.build('candidate')
        graph = json.loads((candidate / 'graph.json').read_text())
        node = graph['nodes'][0]
        node['name'] += ' changed'
        old = self.baseline
        self.baseline = candidate
        self.rewrite_graph(graph)
        self.baseline = old
        result = self.compare(candidate)
        changed = result['changes']['nodes']['changed'][0]
        self.assertIn('name', changed['fields'])
        self.assertNotEqual(changed['before']['name'], changed['after']['name'])
        self.assertIn('evidence_before', changed)
        self.assertIn('evidence_after', changed)


    def test_given_captured_initial_instructions_when_notes_change_then_instruction_freshness_is_stale(self):
        helper = runpy.run_path(str(Path(__file__).with_name('test_architecture_context.py')))
        document, context_path, source = helper['supplied_context'](self.root)
        instructions = self.root / 'relationships/service-dependencies/initial-instructions.md'
        instructions.write_bytes(source.read_bytes())
        document['sources'][0]['path'] = instructions.relative_to(self.root).as_posix()
        context_path.write_text(json.dumps(document))
        context_tool = load_tool('architecture_context')
        captured = context_tool.load_context(self.root, context_path)
        context_tool.write_context(captured, self.baseline, {'repo:client'})
        (self.baseline / 'manifest.json').unlink()
        publication.write_ai_outputs(self.baseline, self.root / 'absent.json')
        instructions.write_text('Changed architecture notes.\n')
        result = self.compare(check_current=True)
        state = result['baseline']['initial_instruction_freshness']
        self.assertEqual(state['status'], 'STALE')
        self.assertNotEqual(state['saved_sha256'], state['current_sha256'])
        self.assertEqual(result['baseline']['architecture_context_freshness']['status'], 'STALE')

    def test_given_claim_rationale_changed_when_comparing_then_claim_delta_preserves_both_assessments(self):
        graph = json.loads((self.baseline / 'graph.json').read_text())
        edge = graph['edges'][0]
        edge.setdefault('properties', {})['architecture_claims'] = [{
            'claim_id': 'claim-existing', 'source_subject': 'consumer', 'target_subject': 'provider',
            'rationale': 'Previous source assessment.'}]
        self.rewrite_graph(graph)
        candidate = self.build('candidate')
        graph['edges'][0]['properties']['architecture_claims'][0]['rationale'] = 'New source assessment.'
        original = self.baseline
        self.baseline = candidate
        self.rewrite_graph(graph)
        self.baseline = original
        result = self.compare(candidate)
        self.assertEqual(result['counts']['claims']['changed'], 1)
        change = result['changes']['claims']['changed'][0]
        self.assertEqual(change['id'], 'claim-existing')
        self.assertNotEqual(change['before']['rationale'], change['after']['rationale'])


if __name__ == '__main__':
    unittest.main()
