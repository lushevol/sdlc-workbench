"""Exercise complete knowledge builds, saved bundle validation, and atomic publication."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

from ai_sdlc_workbench.runtime import Workbench
from ai_sdlc_workbench.knowledge_layout import knowledge_layout
from ai_sdlc_workbench.workspace import initialize_workspace

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
publication = load_tool('generate_all_graphs')
snapshot = load_tool('snapshot')
validator = load_tool('validate_graph')


def digest(value):
    return hashlib.sha256(value).hexdigest()


class KnowledgeBuildIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='knowledge-integration-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        (self.root / 'repos').mkdir()
        self.output = self.root / 'relationships/service-dependencies/generated'

    def write(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding='utf-8')
        return path

    def fixture(self):
        canonical, evidence = knowledge_layout(self.root)
        canonical_name, evidence_name = (path.relative_to(self.root).as_posix() for path in (canonical, evidence))
        self.source = self.write(evidence_name + '/sources/policy.txt',
                                 'Orders require one recorded decision.\nPRIVATE_RETAINED_BODY_247\n')
        source = {'id': 'SRC-orders', 'resource': 'policy://orders', 'revision': 'policy-v1',
                  'sha256': digest(self.source.read_bytes()),
                  'snapshot': self.source.relative_to(self.root).as_posix(),
                  'classification': 'business', 'ingested_at': '2026-11-03T01:00:00Z'}
        self.write(evidence_name + '/manifest.yaml',
                   yaml.safe_dump({'schema_version': 1, 'sources': [source]}, sort_keys=False))
        metadata = {'type': 'Requirement', 'id': 'REQ-orders', 'version': 1,
                    'owner': 'human:orders', 'governance_state': 'candidate', 'status': 'draft',
                    'sources': [{key: source[key] for key in ('resource', 'revision', 'sha256')}],
                    'acceptance_criteria': [{'id': 'AC-review', 'given': 'Given an order',
                                             'when': 'When review finishes',
                                             'then': 'Then one decision exists',
                                             'measure': {'metric': 'decisions', 'operator': 'equals',
                                                         'value': 1, 'unit': 'count'}}]}
        self.record = self.write(canonical_name + '/candidates/orders.md',
                                 '---\n' + yaml.safe_dump(metadata, sort_keys=False) +
                                 '---\n# Order policy\n\nPRIVATE_AUTHORED_BODY_248\n')
        return source

    def build(self):
        return publication.main(['--workspace', str(self.root), '--repos', str(self.root / 'repos'),
                                 '--out', str(self.output)])

    def graph(self):
        return json.loads((self.output / 'graph.json').read_bytes())

    def bundle_bytes(self):
        return {path.relative_to(self.output).as_posix(): path.read_bytes()
                for path in self.output.rglob('*') if path.is_file()}

    def replace_graph_with_matching_manifest(self, graph):
        """Rebind checksums so tests reach semantic validation, beyond byte corruption checks."""
        raw = (json.dumps(graph, sort_keys=True) + '\n').encode('utf-8')
        (self.output / 'graph.json').write_bytes(raw)
        manifest_path = self.output / 'manifest.json'
        manifest = json.loads(manifest_path.read_bytes())
        manifest['graph_sha256'] = digest(raw)
        artifact = next(row for row in manifest['artifacts'] if row['path'] == 'graph.json')
        artifact.update(sha256=digest(raw), bytes=len(raw))
        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')

    def test_given_empty_workspace_when_built_then_empty_knowledge_is_available_and_current(self):
        """Given no records or repositories, when built, then an empty validated projection remains queryable."""
        self.assertEqual(self.build(), 0)
        graph = self.graph()
        self.assertEqual(validator.validate(graph, self.root), [])
        self.assertEqual(graph['repositories'], [])
        self.assertEqual(graph['knowledge']['inputs'], [])
        self.assertEqual(graph['knowledge']['counts'], {'nodes': 0, 'edges': 0, 'input_files': 0})
        result = snapshot.query(self.output, 'knowledge', {}, self.root)
        self.assertEqual(result['status'], 'SUCCEEDED')
        self.assertEqual(result['knowledge_status'], 'AVAILABLE')
        self.assertEqual(result['knowledge_freshness']['status'], 'CURRENT')
        self.assertEqual(result['matching_total'], 0)
        self.assertEqual(result['nodes'], [])
        self.assertEqual(result['edges'], [])
        self.assertEqual(result['evidence'], [])
        self.assertTrue((self.output / 'relationship-viewer.html').is_file())

    def test_given_candidate_intent_when_built_then_exact_citations_remain_candidates_without_source_bodies(self):
        """Given source-backed candidate intent, when published as a graph, then lifecycle and provenance remain explicit."""
        source = self.fixture()
        inputs_before = {path.relative_to(self.root).as_posix(): path.read_bytes()
                         for path in (self.record, self.source, self.source.parent.parent / 'manifest.yaml')}
        self.assertEqual(self.build(), 0)
        graph = self.graph()
        self.assertEqual(validator.validate(graph, self.root), [])
        result = snapshot.query(self.output, 'knowledge', {'record_id': 'REQ-orders'}, self.root)
        self.assertEqual(result['knowledge_freshness']['status'], 'CURRENT')
        self.assertEqual(result['matching_total'], 1)
        record = result['nodes'][0]
        self.assertEqual(record['properties']['governance_state'], 'candidate')
        self.assertEqual(record['properties']['content_sha256'], digest(self.record.read_bytes()))
        self.assertEqual(record['properties']['version'], 1)
        references = snapshot.query(self.output, 'references', {'node_id': record['id'], 'direction': 'out'}, self.root)
        citation = next(row for row in references['edges'] if row['relationship'] == 'CITES_SOURCE')
        retained = next(row for row in references['nodes'] if row['id'] == citation['target'])
        self.assertEqual(retained['type'], 'SOURCE_REVISION')
        self.assertEqual(retained['properties']['revision'], source['revision'])
        self.assertEqual(retained['properties']['sha256'], source['sha256'])
        self.assertEqual(retained['properties']['snapshot_status'], 'MATCH')
        self.assertTrue(any(row['relationship'] == 'HAS_CRITERION' for row in references['edges']))
        self.assertEqual(snapshot.query(self.output, 'knowledge', {'governance_state': 'published'}, self.root)['nodes'], [])
        self.assertEqual(inputs_before, {relative: (self.root / relative).read_bytes() for relative in inputs_before})
        serialized = json.dumps(graph)
        self.assertNotIn('PRIVATE_RETAINED_BODY_247', serialized)
        self.assertNotIn('PRIVATE_AUTHORED_BODY_248', serialized)

    def test_given_initialized_workspace_when_cli_discovers_and_calls_graph_then_new_schemas_and_filters_work(self):
        """Given a generated workspace, when CLI resources and graph calls run, then schemas load and grants retain results."""
        self.root = initialize_workspace(self.root / 'generated-workspace', name='Knowledge CLI integration')
        self.output = self.root / 'relationships/service-dependencies/generated'
        self.assertEqual(Workbench(self.root).describe()['resources'], [])
        self.fixture()
        self.write('registry/tools.yaml', yaml.safe_dump({'schema_version': 1, 'tools': [{
            'id': 'knowledge-graph', 'kind': 'dependency_graph', 'provider': 'graph.snapshot',
            'environment': 'local-fixture', 'config': {'path': self.output.relative_to(self.root).as_posix()},
            'allowed_operations': ['knowledge', 'references', 'paths']}]}))
        environment = {key: value for key, value in os.environ.items() if key != 'PYTHONPATH'}

        def cli(*arguments):
            result = subprocess.run([sys.executable, '-m', 'ai_sdlc_workbench', '--workspace', str(self.root),
                                     *arguments], cwd=self.root.parent, env=environment,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result.stdout

        cli('graph', 'build')
        resources = json.loads(cli('resources'))
        resource = next(row for row in resources if row['id'] == 'knowledge-graph')
        operations = {row['name']: row for row in resource['operations']}
        for name in ('knowledge', 'references', 'paths'):
            self.assertTrue(operations[name]['allowed'])
            state = operations[name]['input_schema']['properties']['governance_state']
            self.assertEqual(state['type'], 'string')
            self.assertIn('candidate', state['enum'])
            self.assertIn('published', state['enum'])
        for name in ('references', 'paths'):
            direction = operations[name]['input_schema']['properties']['direction']
            self.assertEqual(direction, {'type': 'string', 'enum': ['in', 'out', 'both']})

        def call(name, arguments):
            action = json.loads(cli('call', 'knowledge-graph', name, '--args', json.dumps(arguments)))
            self.assertEqual(action['status'], 'SUCCEEDED')
            self.assertEqual(action['operation'], name)
            self.assertEqual(Workbench(self.root).run(action['id'])['result'], action['result'])
            return action['result']

        knowledge = call('knowledge', {'record_id': 'REQ-orders', 'governance_state': 'candidate'})
        self.assertEqual(knowledge['knowledge_status'], 'AVAILABLE')
        self.assertEqual(knowledge['knowledge_freshness']['status'], 'CURRENT')
        self.assertEqual(knowledge['matching_total'], 1)
        record = knowledge['nodes'][0]
        references = call('references', {'node_id': record['id'], 'direction': 'out',
                                         'governance_state': 'candidate'})
        citation = next(row for row in references['edges'] if row['relationship'] == 'CITES_SOURCE')
        paths = call('paths', {'source': record['id'], 'target': citation['target'],
                               'direction': 'out', 'governance_state': 'candidate'})
        self.assertEqual(paths['paths'][0]['node_ids'], [record['id'], citation['target']])
        self.assertEqual(call('knowledge', {'governance_state': 'published'})['nodes'], [])
        invalid = subprocess.run([sys.executable, '-m', 'ai_sdlc_workbench', '--workspace', str(self.root),
                                  'call', 'knowledge-graph', 'references', '--args',
                                  json.dumps({'node_id': record['id'], 'direction': 'sideways'})],
                                 cwd=self.root.parent, env=environment, capture_output=True, text=True, timeout=30)
        self.assertEqual(invalid.returncode, 1, invalid.stdout + invalid.stderr)
        denied = json.loads(invalid.stdout)
        self.assertEqual(denied['status'], 'FAILED')
        self.assertIn('arguments.direction has an unsupported value', denied['error'])
        self.assertIsNone(denied['result'])

    def test_given_rebound_checksums_when_saved_metadata_is_invalid_then_queries_reject_snapshot(self):
        """Given checksum-consistent tampering, when read, then invalid lifecycle and unsafe input metadata are rejected."""
        self.fixture()
        self.build()
        original = self.graph()
        original_manifest = (self.output / 'manifest.json').read_bytes()
        for change in ('invalid-lifecycle', 'escaping-input'):
            with self.subTest(change=change):
                graph = deepcopy(original)
                if change == 'invalid-lifecycle':
                    record = next(row for row in graph['nodes'] if row['type'] == 'KNOWLEDGE_RECORD')
                    record['properties']['governance_state'] = 'approved'
                else:
                    graph['knowledge']['inputs'][0]['path'] = '../outside-policy.txt'
                (self.output / 'manifest.json').write_bytes(original_manifest)
                self.replace_graph_with_matching_manifest(graph)
                with self.assertRaises(snapshot.SnapshotError) as raised:
                    snapshot.query(self.output, 'knowledge', {}, self.root)
                self.assertEqual(raised.exception.code, 'INVALID_SNAPSHOT')

    def test_given_inputs_change_during_build_when_publication_runs_then_prior_bundle_is_preserved(self):
        """Given an existing snapshot, when record or source bytes change during a build, then publication aborts atomically."""
        self.fixture()
        self.build()
        before = self.bundle_bytes()
        original_run = publication.run
        for changed in (self.record, self.source):
            with self.subTest(path=changed.relative_to(self.root).as_posix()):
                original_bytes = changed.read_bytes()
                mutations = []

                def mutate_after_validation(*parts, workspace):
                    original_run(*parts, workspace=workspace)
                    if 'validate_graph' in parts:
                        changed.write_bytes(original_bytes + b'\nChanged during generation.\n')
                        mutations.append(changed)

                try:
                    with patch.object(publication, 'run', side_effect=mutate_after_validation):
                        with self.assertRaisesRegex(ValueError, 'Knowledge inputs changed during graph generation'):
                            self.build()
                    self.assertEqual(mutations, [changed])
                    self.assertEqual(self.bundle_bytes(), before)
                    self.assertFalse(self.output.with_name('.generated.previous').exists())
                    saved = snapshot.query(self.output, 'knowledge', {'record_id': 'REQ-orders'}, self.root)
                    self.assertEqual(saved['matching_total'], 1)
                    self.assertEqual(saved['nodes'][0]['properties']['content_sha256'], digest(self.record.read_bytes())
                                     if changed != self.record else digest(original_bytes))
                    self.assertEqual(saved['knowledge_freshness']['status'], 'STALE')
                    self.assertIn(changed.relative_to(self.root).as_posix(), saved['knowledge_freshness']['changed_paths'])
                finally:
                    changed.write_bytes(original_bytes)
                self.assertEqual(snapshot.query(self.output, 'knowledge', {}, self.root)['knowledge_freshness']['status'], 'CURRENT')


if __name__ == '__main__':
    unittest.main()
