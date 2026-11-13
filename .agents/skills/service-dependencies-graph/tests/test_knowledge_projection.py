"""Exercise source-bound knowledge projection without changing canonical records."""
from copy import deepcopy
import builtins
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

import yaml

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
projection = load_tool('knowledge_projection')
build = load_tool('build_graph')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def record_digest(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


class KnowledgeProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='knowledge-projection-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.graph = build.Graph(self.root)
        self.source_path = 'evidence/knowledge/sources/policy.txt'
        self.write(self.source_path, 'Orders require review.\nPRIVATE_SOURCE_BODY_987\n')
        self.source = {'id': 'SRC-policy', 'resource': 'policy://orders', 'revision': 'policy-v1',
                       'sha256': digest((self.root / self.source_path).read_bytes()),
                       'snapshot': self.source_path, 'classification': 'business',
                       'ingested_at': '2026-11-03T01:00:00Z'}
        self.write_yaml('evidence/knowledge/manifest.yaml', {'schema_version': 1, 'sources': [self.source]})
        self.record_path = 'knowledge/candidates/orders.md'
        self.metadata = {'type': 'Requirement', 'id': 'REQ-orders', 'version': 1, 'owner': 'human:orders',
                         'governance_state': 'candidate', 'status': 'draft',
                         'sources': [{key: self.source[key] for key in ('resource', 'revision', 'sha256')}],
                         'related': ['CAP-orders'],
                         'acceptance_criteria': [{'id': 'AC-review', 'given': 'Given an order',
                                                  'when': 'When review finishes', 'then': 'Then one decision exists',
                                                  'measure': {'metric': 'decisions', 'operator': 'equals', 'value': 1, 'unit': 'count'}}]}
        self.write_record()
        self.write_yaml('registry/capabilities.yaml', {'schema_version': 1, 'capabilities': [
            {'id': 'CAP-orders', 'name': 'Order review', 'repository_ids': ['SDK-catalog-identity']}]})
        self.write_yaml('registry/repositories.yaml', {'schema_version': 1, 'repositories': [
            {'id': 'SDK-catalog-identity', 'location': 'repos/libraries/different-folder'}]})
        repo = self.root / 'repos/libraries/different-folder'
        self.write('repos/libraries/different-folder/src/index.py', 'value = 1\n')
        repository = self.graph.add_repository(repo, 'SPRING', True)
        evidence = self.graph.add_evidence(repository, 'repos/libraries/different-folder/src/index.py', 1,
                                           'Fixture application', 'fixture')
        self.graph.add_node('service:fixture', 'SERVICE', 'Fixture service', repository,
                            dimensions=['RUNTIME'], component_kind=None, functional_role='Fixture',
                            business_meaning='Fixture', source_paths=['repos/libraries/different-folder/src/index.py'], evidence=[evidence])

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding='utf-8')
        return target

    def write_yaml(self, path, value):
        return self.write(path, yaml.safe_dump(value, sort_keys=False))

    def write_record(self):
        self.write(self.record_path, '---\n' + yaml.safe_dump(self.metadata, sort_keys=False) +
                   '---\n# Order policy\n\nPRIVATE_AUTHORED_BODY_321\n')

    def nodes(self, kind):
        return [node for node in self.graph.nodes.values() if node['type'] == kind]

    def edges(self, relationship):
        return [edge for edge in self.graph.edges.values() if edge['relationship'] == relationship]

    def baseline(self):
        code_path = 'evidence/code/orders.py'
        test_path = 'evidence/tests/orders.py'
        result_path = 'evidence/execution/orders.json'
        self.write(code_path, 'reviewed = True\n')
        self.write(test_path, 'assert reviewed\n')
        self.write(result_path, json.dumps({'status': 'FAILED', 'private': 'PRIVATE_RESULT_BODY_456'}))
        artifacts = [
            {'id': 'ART-intent', 'kind': 'INTENT', 'path': self.record_path,
             'sha256': digest((self.root / self.record_path).read_bytes())},
            {'id': 'ART-code', 'kind': 'CODE', 'path': code_path,
             'sha256': digest((self.root / code_path).read_bytes()),
             'repository_id': 'SDK-catalog-identity', 'revision': 'a' * 40, 'source_path': 'src/orders.py'},
            {'id': 'ART-test', 'kind': 'TEST', 'path': test_path, 'sha256': digest((self.root / test_path).read_bytes())},
            {'id': 'ART-result', 'kind': 'EXECUTION', 'path': result_path, 'sha256': digest((self.root / result_path).read_bytes())},
        ]
        behavior = {'id': 'REQ-orders:review', 'version': 1, 'criterion_id': 'AC-review', 'state': 'ACTIVE',
                    'intent': {'artifact_id': 'ART-intent', 'record_sha256': record_digest(artifacts[0]), 'start_line': 1, 'end_line': 2}}
        links = [
            {'id': 'LINK-code', 'behavior_id': behavior['id'], 'behavior_record_sha256': record_digest(behavior),
             'artifact_id': 'ART-code', 'artifact_record_sha256': record_digest(artifacts[1]), 'relationship': 'IMPLEMENTED_BY',
             'grade': 'LIKELY', 'start_line': 1, 'end_line': 1, 'limitations': ['Local inspection only.']},
            {'id': 'LINK-assertion', 'behavior_id': behavior['id'], 'behavior_record_sha256': record_digest(behavior),
             'artifact_id': 'ART-test', 'artifact_record_sha256': record_digest(artifacts[2]), 'relationship': 'ASSERTED_BY',
             'grade': 'CONFIRMED', 'start_line': 1, 'end_line': 1, 'assertion': 'PRIVATE_ASSERTION_BODY_789', 'limitations': []},
        ]
        value = {'schema_version': 1, 'baseline_id': 'BASELINE-orders', 'story_id': 'REQ-orders', 'scope': 'Fixture',
                 'artifacts': artifacts, 'behaviors': [behavior], 'links': links,
                 'executions': [{'id': 'EXEC-orders', 'artifact_id': 'ART-result',
                                 'artifact_record_sha256': record_digest(artifacts[3]), 'mode': 'CONTROLLED_SOURCE',
                                 'level': 'UNIT', 'environment': 'Local fixture', 'code_artifact_ids': ['ART-code'],
                                 'assertion_bindings': [{'link_id': 'LINK-assertion', 'link_record_sha256': record_digest(links[1]), 'check_name': 'review'}],
                                 'limitations': ['No deployed execution.']}], 'findings': []}
        self.write('relationships/requirement-code/baselines/orders.json', json.dumps(value, indent=2))
        return value

    def test_candidate_state_exact_sources_and_weak_related_are_preserved(self):
        self.write_yaml('registry/tools.yaml', {'schema_version': 1, 'tools': [
            {'id': 'private-tool', 'config': {'token': 'PRIVATE_TOOL_TOKEN_654'}}]})
        before = {path: digest(path.read_bytes()) for path in self.root.rglob('*') if path.is_file()}
        projection.apply_knowledge(self.graph)
        record = self.nodes('KNOWLEDGE_RECORD')[0]
        self.assertEqual(record['properties']['governance_state'], 'candidate')
        self.assertEqual(record['properties']['content_sha256'], digest((self.root / self.record_path).read_bytes()))
        self.assertEqual(self.nodes('SOURCE_REVISION')[0]['properties']['snapshot_status'], 'MATCH')
        self.assertEqual(self.edges('CITES_SOURCE')[0]['source'], record['id'])
        self.assertEqual(len(self.edges('RELATED_TO')), 1)
        self.assertEqual(self.edges('RELATED_TO')[0]['properties']['evidence_class'], 'DECLARED_METADATA')
        self.assertEqual(self.nodes('ACCEPTANCE_CRITERION')[0]['properties']['governance_state'], 'candidate')
        self.assertEqual(before, {path: digest(path.read_bytes()) for path in self.root.rglob('*') if path.is_file()})
        self.assertTrue(all(type(count) is int for count in self.graph.knowledge['counts'].values()))
        serialized = json.dumps(self.graph.document())
        self.assertNotIn('PRIVATE_SOURCE_BODY_987', serialized)
        self.assertNotIn('PRIVATE_AUTHORED_BODY_321', serialized)
        self.assertNotIn('PRIVATE_TOOL_TOKEN_654', serialized)

    def test_explicit_repository_path_join_uses_catalog_identity(self):
        projection.apply_knowledge(self.graph)
        joined = self.edges('SAME_REPOSITORY_AS')
        self.assertEqual(len(joined), 1)
        self.assertEqual(joined[0]['target'], 'service:fixture')
        self.assertEqual(joined[0]['properties']['graph_repository_id'], 'repo:different-folder')
        source = self.graph.nodes[joined[0]['source']]
        self.assertEqual(source['properties']['record_id'], 'SDK-catalog-identity')

    def test_audit_only_binds_exact_version_and_final_file_hash(self):
        event = {'id': 'AUD-orders', 'item_id': 'REQ-orders', 'item_version': 1,
                 'action': 'transition', 'from_state': 'untracked', 'to_state': 'candidate',
                 'content_sha256': digest((self.root / self.record_path).read_bytes()), 'evidence': []}
        self.write_yaml('evidence/knowledge/audit/AUD-orders.yaml', event)
        projection.apply_knowledge(self.graph)
        self.assertEqual(self.graph.nodes[self.edges('RECORDS_EVENT_FOR')[0]['target']]['type'], 'KNOWLEDGE_RECORD')
        self.write(self.record_path, (self.root / self.record_path).read_text() + '\nChanged final bytes.\n')
        changed = build.Graph(self.root)
        projection.apply_knowledge(changed)
        edge = next(edge for edge in changed.edges.values() if edge['relationship'] == 'RECORDS_EVENT_FOR')
        self.assertEqual(changed.nodes[edge['target']]['type'], 'UNRESOLVED_REFERENCE')

    def test_historical_missing_and_ambiguous_related_stay_boundaries(self):
        self.metadata['related'] = ['REQ-missing', 'CAP-orders']
        self.write_record()
        self.write_yaml('registry/services.yaml', {'schema_version': 1, 'services': [{'id': 'CAP-orders'}]})
        projection.apply_knowledge(self.graph)
        related = self.edges('RELATED_TO')
        self.assertEqual(len(related), 2)
        self.assertTrue(all(self.graph.nodes[edge['target']]['type'] == 'UNRESOLVED_REFERENCE' for edge in related))
        self.assertEqual({self.graph.nodes[edge['target']]['properties']['reason'] for edge in related},
                         {'Missing exact reference', 'Ambiguous reference'})

    def test_baseline_assertion_identity_grade_and_failed_outcome_are_retained(self):
        self.baseline()
        projection.apply_knowledge(self.graph)
        self.assertEqual(self.edges('IMPLEMENTED_BY')[0]['properties']['grade'], 'LIKELY')
        self.assertEqual(self.edges('IMPLEMENTED_BY')[0]['properties']['binding_status'], 'MATCH')
        assertions = [node for node in self.nodes('TEST_ASSERTION') if node['properties'].get('assertion_kind') == 'DECLARED_ASSERTION']
        self.assertEqual(len(assertions), 1)
        self.assertEqual(assertions[0]['properties']['governance_state'], 'candidate')
        self.assertEqual(self.edges('ASSERTED_BY')[0]['target'], assertions[0]['id'])
        self.assertEqual(self.edges('DECLARES_ASSERTION_BINDING')[0]['target'], assertions[0]['id'])
        self.assertEqual(len(self.edges('DECLARES_CRITERION')), 1)
        execution = next(node for node in self.nodes('EXECUTION') if node['properties']['record_id'] == 'EXEC-orders')
        self.assertEqual(execution['properties']['outcome'], 'FAILED')
        self.assertEqual(execution['properties']['business_verification'], 'NOT_VERIFIED')
        serialized = json.dumps(self.graph.document())
        self.assertNotIn('PRIVATE_RESULT_BODY_456', serialized)
        self.assertNotIn('PRIVATE_ASSERTION_BODY_789', serialized)

    def test_changed_intent_does_not_join_baseline_to_current_criterion(self):
        self.baseline()
        self.metadata['version'] = 2
        self.write_record()
        projection.apply_knowledge(self.graph)
        self.assertEqual(self.edges('DECLARES_CRITERION'), [])
        artifact = next(node for node in self.nodes('KNOWLEDGE_RECORD') if node['properties'].get('artifact_kind') == 'INTENT')
        self.assertEqual(artifact['properties']['retained_status'], 'MISMATCH')
        self.assertNotIn('governance_state', artifact['properties'])

    def test_fingerprints_detect_raw_record_and_missing_snapshot_addition(self):
        initial = projection.input_fingerprints(self.root)
        self.write(self.source_path, 'Changed policy.\n')
        changed = projection.input_fingerprints(self.root)
        self.assertNotEqual(initial, changed)
        self.source['snapshot'] = 'evidence/knowledge/sources/later.txt'
        self.write_yaml('evidence/knowledge/manifest.yaml', {'schema_version': 1, 'sources': [self.source]})
        absent = projection.input_fingerprints(self.root)
        self.write(self.source['snapshot'], 'New retained snapshot.\n')
        self.assertNotEqual(absent, projection.input_fingerprints(self.root))

    def test_symlink_and_escaping_inputs_fail_without_graph_mutation(self):
        before = deepcopy(self.graph.document())
        self.source['snapshot'] = '../outside-policy.txt'
        self.write_yaml('evidence/knowledge/manifest.yaml', {'schema_version': 1, 'sources': [self.source]})
        with self.assertRaisesRegex(ValueError, 'within the workspace'):
            projection.apply_knowledge(self.graph)
        self.source['snapshot'] = self.source_path
        self.write_yaml('evidence/knowledge/manifest.yaml', {'schema_version': 1, 'sources': [self.source]})
        (self.root / 'knowledge/linked.md').symlink_to(self.root / self.record_path)
        with self.assertRaisesRegex(ValueError, 'symbolic links'):
            projection.apply_knowledge(self.graph)
        for key in ('nodes', 'edges', 'evidence'):
            self.assertEqual(before[key], self.graph.document()[key])

    def test_malformed_duplicate_keys_and_invalid_record_version_fail_closed(self):
        self.write('registry/services.yaml', 'schema_version: 1\nservices: []\nservices: []\n')
        with self.assertRaisesRegex(ValueError, 'unique'):
            projection.apply_knowledge(self.graph)
        (self.root / 'registry/services.yaml').unlink()
        self.metadata['version'] = True
        self.write_record()
        with self.assertRaisesRegex(ValueError, 'version'):
            projection.apply_knowledge(self.graph)
        self.assertEqual(len(self.graph.nodes), 1)

    def test_invalid_baseline_range_fails_before_graph_mutation(self):
        baseline = self.baseline()
        baseline['links'][0]['end_line'] = 0
        self.write('relationships/requirement-code/baselines/orders.json', json.dumps(baseline))
        before = deepcopy(self.graph.document())
        with self.assertRaisesRegex(ValueError, 'line ranges'):
            projection.apply_knowledge(self.graph)
        for key in ('nodes', 'edges', 'evidence'):
            self.assertEqual(before[key], self.graph.document()[key])

    def test_reprojection_replaces_old_version_and_preserves_static_declarations(self):
        projection.apply_knowledge(self.graph)
        first = self.nodes('KNOWLEDGE_RECORD')[0]['id']
        self.metadata['version'] = 2
        self.metadata['governance_state'] = 'stale'
        self.write_record()
        projection.apply_knowledge(self.graph)
        self.assertNotIn(first, self.graph.nodes)
        self.assertEqual(len(self.nodes('KNOWLEDGE_RECORD')), 1)
        self.assertEqual(self.nodes('KNOWLEDGE_RECORD')[0]['properties']['governance_state'], 'stale')
        self.assertEqual(self.graph.nodes['service:fixture']['type'], 'SERVICE')
        self.assertEqual(self.nodes('ACCEPTANCE_CRITERION')[0]['properties']['version'], 2)


    def consolidate(self):
        canonical = self.root / 'knowledge/records'
        canonical.mkdir()
        (self.root / 'knowledge/candidates').rename(canonical / 'candidates')
        (self.root / 'evidence/knowledge').rename(self.root / 'knowledge/evidence')
        manifest_path = self.root / 'knowledge/evidence/manifest.yaml'
        manifest = yaml.safe_load(manifest_path.read_text())
        for source in manifest['sources']:
            source['snapshot'] = source['snapshot'].replace('evidence/knowledge/', 'knowledge/evidence/', 1)
        manifest_path.write_text(yaml.safe_dump(manifest))

    def test_consolidated_projection_excludes_raw_source_markdown_and_wiki(self):
        self.consolidate()
        self.write('knowledge/evidence/sources/not-canonical.md', '# Unreviewed original without metadata.\n')
        self.write('knowledge/llm-wiki/wiki/summaries/not-canonical.md', '# Derived content without canonical metadata.\n')
        projection.apply_knowledge(self.graph)
        records = [node for node in self.graph.nodes.values() if node['type'] == 'KNOWLEDGE_RECORD']
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['source_paths'], ['knowledge/records/candidates/orders.md'])
        inputs = {row['path'] for row in projection.input_fingerprints(self.root)}
        self.assertIn('knowledge/evidence/sources/policy.txt', inputs)
        self.assertNotIn('knowledge/evidence/sources/not-canonical.md', inputs)
        self.assertNotIn('knowledge/llm-wiki/wiki/summaries/not-canonical.md', inputs)

    def test_standalone_fallback_supports_consolidation_and_rejects_ambiguous_layout(self):
        self.consolidate()
        original_import = builtins.__import__
        def standalone_import(name, *args, **kwargs):
            if name == 'ai_sdlc_workbench.knowledge_layout':
                raise ModuleNotFoundError('Synthetic standalone environment', name=name)
            return original_import(name, *args, **kwargs)
        with patch('builtins.__import__', side_effect=standalone_import):
            projection.apply_knowledge(self.graph)
            self.write('evidence/knowledge/manifest.yaml', 'schema_version: 1\nsources: []\n')
            with self.assertRaisesRegex(ValueError, 'Both knowledge manifests'):
                projection.input_fingerprints(self.root)
        with self.assertRaisesRegex(ValueError, 'Both knowledge manifests'):
            projection.input_fingerprints(self.root)


if __name__ == '__main__':
    unittest.main()
