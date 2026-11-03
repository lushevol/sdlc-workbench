"""Protect bounded graph navigation, lifecycle scope, and saved evidence identity."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
queries = load_tool('knowledge_queries')
snapshot = load_tool('snapshot')
builder = load_tool('build_graph')


class KnowledgeQueryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='knowledge-query-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / 'knowledge/candidates/topic.md'
        self.source.parent.mkdir(parents=True)
        self.source.write_text('A retained intent source.\n', encoding='utf-8')
        self.graph = builder.Graph(self.root)
        self.evidence = self.graph.add_evidence(None, 'knowledge/candidates/topic.md', 1,
                                                'Recorded intent citation.', 'knowledge-projection')

    def node(self, identifier, state=None, node_type='KNOWLEDGE_RECORD', **properties):
        metadata = {'projection': 'knowledge', 'record_id': identifier, 'version': 1,
                    'record_type': 'KnowledgeTopic', 'owner': 'unknown',
                    'content_sha256': hashlib.sha256(self.source.read_bytes()).hexdigest(),
                    'evidence_class': 'DOCUMENTED_INTENT', **properties}
        if node_type == 'KNOWLEDGE_RECORD' and state is None:
            state = 'candidate'
        if node_type == 'SOURCE_REVISION':
            metadata.update(resource='conversation:fixture', revision='user-1', sha256=metadata['content_sha256'])
        if state:
            metadata['governance_state'] = state
        self.graph.add_node(identifier, node_type, identifier, None, dimensions=('KNOWLEDGE',),
                            component_kind='KNOWLEDGE', functional_role='Retain a declared identity.',
                            business_meaning='Source-backed navigation only.',
                            source_paths=('knowledge/candidates/topic.md',), evidence=(self.evidence,),
                            properties=metadata)
        return identifier

    def edge(self, source, target, relationship='RELATED_TO', **properties):
        return self.graph.add_edge(source, target, relationship, 'KNOWLEDGE', (self.evidence,),
                                   properties={'projection': 'knowledge', 'evidence_class': 'DOCUMENTED_INTENT',
                                               **properties})

    def document(self, projected=True):
        if projected:
            self.graph.knowledge = {'schema_version': '1.0.0', 'inputs': [], 'counts': {},
                                    'limitations': ['Declared relationships do not grant publication approval.']}
        return self.graph.document()

    def bundle(self, graph):
        output = self.root / 'bundle'
        output.mkdir(exist_ok=True)
        payloads = {'graph.json': graph, 'analysis-coverage.json': {'repository_root': 'repos', 'repositories': []},
                    'repository-relationships.json': {}, 'services.json': {'services': []}}
        artifacts = []
        for name, value in payloads.items():
            content = (json.dumps(value, sort_keys=True) + '\n').encode()
            (output / name).write_bytes(content)
            artifacts.append({'path': name, 'sha256': hashlib.sha256(content).hexdigest()})
        manifest = {'generated_at': graph['generated_at'], 'canonical_graph': 'graph.json',
                    'graph_sha256': artifacts[0]['sha256'], 'artifacts': artifacts}
        (output / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        return output

    def test_given_candidates_when_filtered_then_exact_nodes_and_limits_do_not_grant_approval(self):
        """Given candidate intent, when filtered, then state and source evidence remain explicit."""
        self.node('rule:a', 'candidate')
        self.node('rule:b', 'candidate')
        self.node('source:one', node_type='SOURCE_REVISION')
        self.edge('rule:a', 'source:one', 'CITES_SOURCE')
        graph = self.document()
        result = queries.query(graph, 'knowledge', {'governance_state': 'candidate', 'type': 'KnowledgeTopic', 'limit': 1})
        self.assertEqual(result['matching_total'], 2)
        self.assertTrue(result['truncated'])
        self.assertEqual(result['nodes'], [next(row for row in graph['nodes'] if row['id'] == 'rule:a')])
        self.assertEqual(result['evidence'], graph['evidence'])
        self.assertFalse(result['edges'])
        self.assertEqual(result['nodes'][0]['properties']['governance_state'], 'candidate')
        approved = queries.query(graph, 'knowledge', {'governance_state': 'published'})
        self.assertFalse(approved['nodes'])
        self.assertEqual(approved['matching_total'], 0)
        self.assertTrue(any('approval' in value for value in result['limitations']))

    def test_given_source_citations_when_reading_backlinks_then_direction_and_canonical_edges_are_preserved(self):
        """Given two citing records, when incoming references are read, then exact citation edges return."""
        self.node('rule:a', 'candidate')
        self.node('rule:b', 'published')
        self.node('source:one', node_type='SOURCE_REVISION')
        self.edge('rule:a', 'source:one', 'CITES_SOURCE')
        published_edge = self.edge('rule:b', 'source:one', 'CITES_SOURCE')
        graph = self.document()
        incoming = queries.references(graph, {'node_id': 'source:one', 'direction': 'in', 'governance_state': 'published'})
        self.assertEqual(incoming['total_edges'], 1)
        self.assertEqual(incoming['edges'], [next(row for row in graph['edges'] if row['id'] == published_edge)])
        self.assertEqual(incoming['excluded_by_state'], 1)
        self.assertEqual({row['id'] for row in incoming['nodes']}, {'rule:b', 'source:one'})
        self.assertFalse(queries.references(graph, {'node_id': 'source:one', 'direction': 'out'})['edges'])

    def test_given_directed_cycle_when_paths_are_read_then_reverse_paths_retain_original_edges(self):
        """Given a directed cycle, when reversed paths are read, then traversal terminates without changing arrows."""
        for identifier in ('a', 'b', 'c'):
            self.node(identifier, 'candidate')
        self.edge('a', 'b')
        self.edge('b', 'c')
        self.edge('c', 'a')
        result = queries.paths(self.document(), {'source': 'c', 'target': 'a', 'direction': 'in'})
        self.assertEqual(result['paths'][0]['node_ids'], ['c', 'b', 'a'])
        self.assertEqual(result['paths'][0]['traversal_directions'], ['in', 'in'])
        self.assertEqual({(row['source'], row['target']) for row in result['edges']}, {('a', 'b'), ('b', 'c')})
        self.assertLessEqual(result['visits'], 3)
        for path in result['paths']:
            self.assertEqual(len(path['node_ids']), len(set(path['node_ids'])))

    def test_given_candidate_intermediate_when_published_paths_are_requested_then_it_cannot_bridge_the_path(self):
        """Given a hidden candidate intermediary, when published paths are requested, then it cannot supply connectivity."""
        for identifier, state in (('a', 'published'), ('b', 'candidate'), ('c', 'published')):
            self.node(identifier, state)
        self.edge('a', 'b')
        self.edge('b', 'c')
        graph = self.document()
        self.assertTrue(queries.paths(graph, {'source': 'a', 'target': 'c'})['paths'])
        scoped = queries.paths(graph, {'source': 'a', 'target': 'c', 'governance_state': 'published'})
        self.assertFalse(scoped['paths'])
        self.assertEqual(scoped['excluded_by_state'], 1)
        self.node('neutral', node_type='SOURCE_REVISION')
        self.edge('a', 'neutral', 'CITES_SOURCE')
        self.edge('c', 'neutral', 'CITES_SOURCE')
        neutral = queries.paths(self.document(), {'source': 'a', 'target': 'c', 'direction': 'both', 'governance_state': 'published'})
        self.assertEqual(neutral['paths'][0]['node_ids'], ['a', 'neutral', 'c'])
        self.assertNotIn('governance_state', next(row for row in neutral['nodes'] if row['id'] == 'neutral')['properties'])

    def test_given_branching_search_when_work_budget_is_reached_then_truncation_is_explicit(self):
        """Given many branches, when traversal reaches its budget, then examined transitions cannot exceed that budget."""
        for identifier in ['root', 'target'] + [f'branch:{index:02}' for index in range(80)]:
            self.node(identifier)
        for index in range(80):
            self.edge('root', f'branch:{index:02}')
        result = queries.query(self.document(), 'paths', {'source': 'root', 'target': 'target', 'max_visits': 7})
        self.assertEqual(result['visits'], 7)
        self.assertFalse(result['paths'])
        self.assertTrue(result['truncated'])
        self.assertIn('MAX_VISITS', result['truncation_reasons'])
        self.assertTrue(any('empty result' in value for value in result['limitations']))

    def test_given_multiple_paths_when_result_or_depth_limits_apply_then_each_limit_is_reported(self):
        """Given alternate paths, when result or depth limits apply, then omitted search remains visible."""
        for identifier in ('a', 'b1', 'b2', 'b3', 'c'):
            self.node(identifier)
        for middle in ('b1', 'b2', 'b3'):
            self.edge('a', middle)
            self.edge(middle, 'c')
        graph = self.document()
        limited = queries.paths(graph, {'source': 'a', 'target': 'c', 'limit': 1})
        self.assertEqual(len(limited['paths']), 1)
        self.assertIn('RESULT_LIMIT', limited['truncation_reasons'])
        shallow = queries.paths(graph, {'source': 'a', 'target': 'c', 'max_depth': 1})
        self.assertFalse(shallow['paths'])
        self.assertIn('MAX_DEPTH', shallow['truncation_reasons'])

    def test_given_legacy_snapshot_when_new_operations_run_then_knowledge_unavailability_is_explicit(self):
        """Given a legacy snapshot, when queried, then old search works and new operations report unavailable knowledge."""
        self.node('legacy')
        graph = self.document(projected=False)
        output = self.bundle(graph)
        for operation, arguments in (('knowledge', {}), ('references', {'node_id': 'legacy'}),
                                     ('paths', {'source': 'legacy', 'target': 'legacy'})):
            result = snapshot.query(output, operation, arguments, self.root)
            self.assertEqual(result['knowledge_status'], 'NOT_AVAILABLE')
            self.assertEqual(result['knowledge_freshness']['status'], 'NOT_AVAILABLE')
        self.assertTrue(snapshot.query(output, 'search', {'query': 'legacy'}, self.root)['matches'])

    def test_given_unsafe_arguments_when_paths_are_requested_then_schema_rejects_unbounded_work(self):
        """Given unsupported bounds or filters, when queried, then validation rejects them before snapshot access."""
        for change in ({'max_depth': 7}, {'max_visits': 2001}, {'max_visits': 0}, {'limit': 51},
                       {'direction': 'any'}, {'governance_state': 'approved'}, {'source': '\x00'}):
            with self.subTest(change=change), self.assertRaises(snapshot.SnapshotError) as raised:
                snapshot.query(self.root / 'absent', 'paths', {'source': 'a', 'target': 'b', **change}, self.root)
            self.assertEqual(raised.exception.code, 'INVALID_ARGUMENT')

    def test_given_changed_inputs_when_freshness_is_checked_then_saved_nodes_remain_unchanged(self):
        """Given changed input bytes, when freshness is checked, then the saved graph stays historical and reports staleness."""
        projection = load_tool('knowledge_projection')
        self.node('rule:a', 'candidate')
        graph = self.document()
        original = {'path': 'knowledge/candidates/topic.md', 'sha256': hashlib.sha256(self.source.read_bytes()).hexdigest()}
        graph['knowledge']['inputs'] = [original]
        before = deepcopy(graph)
        with patch.object(projection, 'input_fingerprints', return_value=[original]):
            self.assertEqual(queries.freshness(graph, self.root)['status'], 'CURRENT')
        changed = {**original, 'sha256': 'f' * 64}
        with patch.object(projection, 'input_fingerprints', return_value=[changed]):
            result = queries.freshness(graph, self.root)
            self.assertEqual(result['status'], 'STALE')
            self.assertEqual(result['changed_paths'], [original['path']])
        with patch.object(projection, 'input_fingerprints', side_effect=ValueError('Unsafe current declaration')):
            self.assertEqual(queries.freshness(graph, self.root)['status'], 'UNKNOWN')
        self.assertEqual(graph, before)

    def test_given_live_input_addition_change_or_removal_when_compared_then_each_path_is_stale(self):
        """Given real selected inputs, when files change, appear, or disappear, then freshness names each affected path."""
        projection = load_tool('knowledge_projection')
        self.node('rule:a', 'candidate')
        graph = self.document()
        graph['knowledge']['inputs'] = projection.input_fingerprints(self.root)
        self.assertEqual(queries.freshness(graph, self.root)['status'], 'CURRENT')
        self.source.write_text('Changed intended text.\n', encoding='utf-8')
        added = self.source.with_name('added.md')
        added.write_text('A new source.\n', encoding='utf-8')
        changed = queries.freshness(graph, self.root)
        self.assertEqual(changed['status'], 'STALE')
        self.assertEqual(changed['changed_paths'], ['knowledge/candidates/added.md', 'knowledge/candidates/topic.md'])
        self.source.unlink()
        self.assertIn('knowledge/candidates/topic.md', queries.freshness(graph, self.root)['changed_paths'])

    def test_given_valid_bundle_when_bytes_or_references_are_tampered_then_queries_reject_it(self):
        """Given saved graph evidence, when checksums or endpoints change, then navigation rejects the invalid bundle."""
        self.node('a', 'candidate')
        self.node('b', 'candidate')
        self.edge('a', 'b')
        graph = self.document()
        output = self.bundle(graph)
        valid = snapshot.query(output, 'knowledge', {'record_id': 'a'}, self.root)
        self.assertEqual(valid['knowledge_status'], 'AVAILABLE')
        self.assertEqual(valid['nodes'][0]['properties']['record_id'], 'a')
        with (output / 'graph.json').open('ab') as stream:
            stream.write(b'\n')
        with self.assertRaises(snapshot.SnapshotError) as raised:
            snapshot.query(output, 'knowledge', {}, self.root)
        self.assertEqual(raised.exception.code, 'INVALID_SNAPSHOT')
        graph['edges'][0]['target'] = 'missing'
        output = self.bundle(graph)
        with self.assertRaises(snapshot.SnapshotError) as raised:
            snapshot.query(output, 'paths', {'source': 'a', 'target': 'b'}, self.root)
        self.assertEqual(raised.exception.code, 'INVALID_SNAPSHOT')


if __name__ == '__main__':
    unittest.main()
