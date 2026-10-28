"""Verify investigated instructions enter the same graph without false joins."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
context = load_tool('architecture_context')
integration = load_tool('architecture_integration')
build = load_tool('build_graph')
validate = load_tool('validate_graph')


class ArchitectureIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='graph-investigation-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.graph = build.Graph(self.root)
        self.sources = {}
        source_rows = []
        for name in ('client', 'provider'):
            repo = self.root / 'repos/ui' / name
            (repo / 'src').mkdir(parents=True)
            (repo / 'package.json').write_text(json.dumps({'name': '@fixture/' + name}))
            source = repo / 'src/index.ts'
            source.write_text("export const value = 1;\nexport const load = () => fetch('/orders');\n")
            content = source.read_bytes()
            source_rows.append({'id': name + '-code', 'path': source.relative_to(self.root).as_posix(),
                                'sha256': hashlib.sha256(content).hexdigest(), 'revision': 'sha256:' + hashlib.sha256(content).hexdigest(),
                                'kind': 'SOURCE_REVIEW'})
            self.sources[name + '-code'] = content
            repository = self.graph.add_repository(repo, 'WEB', True)
            evidence = self.graph.add_evidence(repository, source_rows[-1]['path'], 1, 'Static fixture entry', 'web-entry')
            self.graph.add_node('application:' + name, 'APPLICATION', name, repository,
                                dimensions=['RUNTIME', 'BUSINESS'], component_kind='MICRO_FRONTEND',
                                functional_role='Fixture entry', business_meaning='Fixture application',
                                source_paths=[source_rows[-1]['path']], evidence=[evidence])
        user = self.root / 'instruction.txt'
        user.write_text('The client loads the provider.\n')
        self.sources['user'] = user.read_bytes()
        source_rows.append({'id': 'user', 'path': 'instruction.txt',
                            'sha256': hashlib.sha256(user.read_bytes()).hexdigest(),
                            'revision': 'user-message', 'kind': 'USER_CLARIFICATION'})
        self.document = {
            'schema_version': '1.1.0', 'sources': source_rows,
            'layers': [{'id': 'shell-layer', 'label': 'Shell', 'order': 1, 'description': 'Initial shell role', 'source_ids': ['user']}],
            'subjects': [
                {'id': name, 'repository': 'repo:' + name, 'node_id': 'application:' + name,
                 'label': name, 'role': 'SHELL' if name == 'client' else 'TILE',
                 'layer_id': 'shell-layer' if name == 'client' else None, 'status': 'USER_REPORTED',
                 'description': 'Initial role', 'source_ids': ['user']} for name in ('client', 'provider')],
            'relationships': [{'id': 'client-provider', 'source': 'client', 'target': 'provider',
                               'kind': 'LOADS_FEATURE', 'description': 'Initial loading claim', 'source_ids': ['user']}],
            'notes': [],
            'investigations': [{'id': 'review-client-provider', 'relationship_id': 'client-provider',
                                'status': 'SUPPORTED', 'family': 'shared', 'rationale': 'Reviewed source declarations support loading.',
                                'source_refs': [{'source_id': name + '-code', 'line': 1, 'end_line': 2}
                                                for name in ('client', 'provider')],
                                'canonical_edge_ids': []}],
        }

    def captured(self):
        raw = (json.dumps(self.document, indent=2) + '\n').encode()
        return context.ContextInput(self.document, context.DEFAULT_CONTEXT, raw, self.sources)

    def add_boundary_claims(self):
        for name in ('gateway', 'upstream'):
            self.document['subjects'].append({
                'id': name, 'repository': None, 'label': name, 'role': 'GATEWAY', 'layer_id': None,
                'status': 'OUT_OF_SCOPE', 'description': 'Unavailable source', 'source_ids': ['user']})
        for name, source, target in (('gateway-client', 'gateway', 'client'), ('upstream-gateway', 'upstream', 'gateway')):
            self.document['relationships'].append({
                'id': name, 'source': source, 'target': target, 'kind': 'FORWARDS_TRAFFIC',
                'description': 'Reported forwarding boundary', 'source_ids': ['user']})
            self.document['investigations'].append({
                'id': 'review-' + name, 'relationship_id': name, 'status': 'UNVERIFIED', 'family': 'api',
                'rationale': 'The deployment source is unavailable.', 'source_refs': [], 'canonical_edge_ids': []})

    def test_supported_claim_enters_canonical_neighborhood_without_resolved_join(self):
        """Given reviewed source, when integrated, then graph edges retain support and unresolved provider matching."""
        integration.apply_context(self.graph, self.captured())
        document = self.graph.document()
        self.assertEqual(validate.validate(document, self.root), [])
        edge = next(row for row in document['edges'] if row['relationship'] == 'REVIEWED_RELATIONSHIP')
        self.assertEqual((edge['source'], edge['target']), ('application:client', 'application:provider'))
        self.assertEqual(edge['assertion_status'], 'CONFIRMED')
        self.assertEqual(edge['resolution_status'], 'UNRESOLVED')
        self.assertEqual(edge['properties']['investigation_status'], 'SUPPORTED')
        self.assertEqual(len(edge['properties']['source_refs']), 2)
        self.assertEqual(self.graph.nodes['application:client']['properties']['architecture_subjects'][0]['layer_order'], 1)
        report = load_tool('repository_reports').relationship_report(document)
        self.assertEqual(report['counts']['resolved_relationships'], 0)

    def test_user_only_or_one_sided_evidence_cannot_promote_a_supported_link(self):
        """Given insufficient source evidence, when integration runs, then unsupported promotion fails before graph changes."""
        initial = deepcopy(self.graph.document())
        self.document['investigations'][0]['source_refs'] = [{'source_id': 'user', 'line': 1, 'end_line': 1}]
        with self.assertRaisesRegex(ValueError, 'SOURCE_REVIEW'):
            integration.apply_context(self.graph, self.captured())
        self.document['investigations'][0]['source_refs'] = [{'source_id': 'client-code', 'line': 1, 'end_line': 1}]
        with self.assertRaisesRegex(ValueError, 'each bound repository'):
            integration.apply_context(self.graph, self.captured())
        for key in ('nodes', 'edges', 'evidence'):
            self.assertEqual(initial[key], self.graph.document()[key])

    def test_reuse_preserves_extracted_identity_assertion_and_resolution(self):
        """Given an existing static join, when reviewed, then evidence augments its existing identity without duplication."""
        refs = [row['evidence'][0] for row in self.graph.nodes.values()]
        edge_id = self.graph.add_edge('application:client', 'application:provider', 'LOADS_REMOTE', 'RUNTIME', refs,
                                      resolution_status='RESOLVED', properties={'resolution_rule': 'exact-package-identity'})
        self.document['investigations'][0]['canonical_edge_ids'] = [edge_id]
        integration.apply_context(self.graph, self.captured())
        self.assertEqual(len(self.graph.edges), 1)
        edge = next(iter(self.graph.edges.values()))
        self.assertEqual(edge['id'], edge_id)
        self.assertEqual(edge['resolution_status'], 'RESOLVED')
        self.assertEqual(edge['assertion_status'], 'CONFIRMED')
        self.assertEqual(edge['properties']['resolution_rule'], 'exact-package-identity')
        self.assertEqual(edge['properties']['architecture_claims'][0]['claim_id'], 'client-provider')
        self.assertGreater(len(edge['evidence']), len(refs))
        report = load_tool('repository_reports').relationship_report(self.graph.document())
        self.assertEqual(report['architecture_relationships'][0]['canonical_edge_ids'], [edge_id])
        self.assertEqual(report['counts']['resolved_relationships'], 1)
        self.assertEqual(report['relationships'][0]['architecture_claims'][0]['kind'], 'LOADS_FEATURE')

    def test_reversed_or_inferred_canonical_edges_cannot_support_the_claim(self):
        """Given reversed or inferred edges, when review selects them, then validation rejects false support."""
        refs = [row['evidence'][0] for row in self.graph.nodes.values()]
        edge_id = self.graph.add_edge('application:provider', 'application:client', 'LOADS_REMOTE', 'RUNTIME', refs)
        self.document['investigations'][0]['canonical_edge_ids'] = [edge_id]
        with self.assertRaisesRegex(ValueError, 'direction or repository'):
            integration.apply_context(self.graph, self.captured())
        self.graph.edges.clear()
        edge_id = self.graph.add_edge('application:client', 'application:provider', 'LOADS_REMOTE', 'RUNTIME', refs,
                                      assertion_status='INFERRED')
        self.document['investigations'][0]['canonical_edge_ids'] = [edge_id]
        with self.assertRaisesRegex(ValueError, 'inferred canonical edge'):
            integration.apply_context(self.graph, self.captured())

    def test_same_repository_edges_cannot_replace_exact_component_or_ambiguous_root_bindings(self):
        """Given exact subject bindings, when unrelated same-repository edges are selected, then integration rejects them without mutation."""
        for name in ('client', 'provider'):
            root = self.graph.nodes['application:' + name]
            for variant in ('actual', 'claimed'):
                self.graph.add_node(
                    variant + ':' + name, 'COMPONENT', variant + ' component', root['repository'],
                    dimensions=['RUNTIME'], component_kind='CLIENT', functional_role='Fixture component',
                    business_meaning='Fixture implementation', source_paths=root['source_paths'], evidence=root['evidence'])
            self.document['subjects'][0 if name == 'client' else 1]['node_id'] = 'claimed:' + name
        refs = [row['evidence'][0] for row in self.graph.nodes.values()]
        edge_id = self.graph.add_edge('actual:client', 'actual:provider', 'CALLS_COMPONENT', 'RUNTIME', refs)
        self.document['investigations'][0]['canonical_edge_ids'] = [edge_id]
        before = deepcopy(self.graph.document())
        with self.assertRaisesRegex(ValueError, 'exact subject node binding'):
            integration.apply_context(self.graph, self.captured())
        for key in ('nodes', 'edges', 'evidence'):
            self.assertEqual(self.graph.document()[key], before[key])

        # Selecting one explicit root of a multi-root repository cannot guess ownership.
        self.document['subjects'][0]['node_id'] = 'application:client'
        self.document['subjects'][1]['node_id'] = 'application:provider'
        client = self.graph.nodes['application:client']
        self.graph.add_node(
            'secondary:client', 'SERVICE', 'Second application', 'repo:client',
            dimensions=['RUNTIME'], component_kind='SERVICE', functional_role='Separate entry',
            business_meaning='Separate application', source_paths=client['source_paths'], evidence=client['evidence'])
        before = deepcopy(self.graph.document())
        with self.assertRaisesRegex(ValueError, 'exact subject node binding'):
            integration.apply_context(self.graph, self.captured())
        for key in ('nodes', 'edges', 'evidence'):
            self.assertEqual(self.graph.document()[key], before[key])

        # Unique analysis roots can still summarize their repository's callsites.
        del self.graph.nodes['secondary:client']
        integration.apply_context(self.graph, self.captured())
        self.assertEqual(len(self.graph.edges), 1)
        self.assertEqual(next(iter(self.graph.edges.values()))['source'], 'actual:client')
        projected = load_tool('graph_query').architecture_relationships(self.graph.document())
        self.assertEqual(projected[0]['source_node'], 'application:client')
        self.assertEqual(projected[0]['target_node'], 'application:provider')

    def test_conflicting_and_external_claims_stay_visible_without_discovered_provider(self):
        """Given an unavailable provider, when a claim conflicts, then its explicit boundary remains an inferred graph endpoint."""
        self.document['subjects'][1].update(repository=None, status='OUT_OF_SCOPE')
        self.document['subjects'][1].pop('node_id')
        self.document['investigations'][0]['status'] = 'CONFLICTED'
        integration.apply_context(self.graph, self.captured())
        edge = next(iter(self.graph.edges.values()))
        boundary = self.graph.nodes[edge['target']]
        self.assertEqual(edge['assertion_status'], 'INFERRED')
        self.assertEqual(edge['properties']['investigation_status'], 'CONFLICTED')
        self.assertEqual(boundary['type'], 'ARCHITECTURE_BOUNDARY')
        self.assertIsNone(boundary['repository'])
        self.assertEqual(boundary['properties']['provider_status'], 'NOT_ESTABLISHED')

    def test_missing_reviews_unknown_sources_and_out_of_range_citations_fail(self):
        """Given incomplete review coverage or invalid citations, when validated, then unsupported inputs fail."""
        original = deepcopy(self.document)
        self.document['investigations'] = []
        with self.assertRaisesRegex(ValueError, 'exactly one investigation'):
            context.validate_document(self.document)
        self.document = deepcopy(original)
        self.document['investigations'][0]['source_refs'][0]['source_id'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'unknown source'):
            context.validate_document(self.document)
        self.document = deepcopy(original)
        self.document['investigations'][0]['source_refs'][0]['end_line'] = 99
        with self.assertRaisesRegex(ValueError, 'exceeds captured bytes'):
            integration.apply_context(self.graph, self.captured())

    def test_distinct_claims_on_the_same_endpoints_retain_separate_decisions(self):
        """Given two claims between repositories, when integrated, then neither decision replaces the other."""
        claim = deepcopy(self.document['relationships'][0])
        claim.update(id='client-provider-session', kind='SHARES_SESSION')
        self.document['relationships'].append(claim)
        decision = deepcopy(self.document['investigations'][0])
        decision.update(id='review-session', relationship_id=claim['id'], status='UNVERIFIED', source_refs=[])
        self.document['investigations'].append(decision)
        integration.apply_context(self.graph, self.captured())
        self.assertEqual(len(self.graph.edges), 2)
        self.assertEqual({row['properties']['investigation_status'] for row in self.graph.edges.values()},
                         {'SUPPORTED', 'UNVERIFIED'})
        self.assertEqual(len({row['id'] for row in self.graph.edges.values()}), 2)

    def test_architecture_projection_preserves_inbound_and_external_only_claims(self):
        """Given unbound endpoints, when projecting, then all claims retain nodes, subject IDs, decisions, and provenance."""
        self.add_boundary_claims()
        integration.apply_context(self.graph, self.captured())
        report = load_tool('repository_reports').relationship_report(self.graph.document())
        self.assertEqual(report['counts']['architecture_relationships'], 3)
        self.assertEqual(report['architecture_statuses'], {'SUPPORTED': 1, 'UNVERIFIED': 2})
        rows = {row['claim_id']: row for row in report['architecture_relationships']}
        inbound = rows['gateway-client']
        self.assertIsNone(inbound['source_repository'])
        self.assertEqual(inbound['target_repository'], 'repo:client')
        self.assertEqual(inbound['source_subject'], 'gateway')
        self.assertEqual(inbound['target_node'], 'application:client')
        external = rows['upstream-gateway']
        self.assertIsNone(external['source_repository'])
        self.assertIsNone(external['target_repository'])
        self.assertEqual(external['kind'], 'FORWARDS_TRAFFIC')
        self.assertTrue(external['canonical_edge_ids'])
        self.assertTrue(external['evidence'])
        self.assertEqual(report['counts']['resolved_relationships'], 0)
        catalog = load_tool('graph_query').service_catalog(self.graph.document(), {})
        self.assertEqual(len(catalog['architecture_relationships']), 3)

    def test_build_and_saved_query_publish_the_same_integrated_graph(self):
        """Given reviewed instructions, when built and queried, then source-bound canonical edges survive bundle validation."""
        self.add_boundary_claims()
        path = self.root / context.DEFAULT_CONTEXT
        path.parent.mkdir(parents=True)
        path.write_bytes(self.captured().content)
        runner = Path(__file__).resolve().parents[1] / 'scripts/graph.py'
        output = self.root / 'generated'
        result = subprocess.run([sys.executable, str(runner), '--workspace', str(self.root), 'build', '--out', str(output)],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        saved = json.loads((output / 'graph.json').read_bytes())
        reviewed = [row for row in saved['edges'] if row['relationship'] == 'REVIEWED_RELATIONSHIP']
        self.assertEqual(len(reviewed), 3)
        query = load_tool('snapshot').query(output, 'coverage', {}, self.root)
        self.assertEqual(query['architecture_context']['status'], 'INVESTIGATED')
        self.assertEqual(query['architecture_context']['freshness']['status'], 'CURRENT')
        neighborhood = load_tool('snapshot').query(output, 'neighborhood', {'node_id': 'application:client', 'limit': 200}, self.root)
        owned = next(row for row in reviewed if row['properties']['claim_id'] == 'client-provider')
        self.assertIn(owned['id'], {row['id'] for row in neighborhood['edges']})
        relations = load_tool('snapshot').query(output, 'relationships', {}, self.root)
        self.assertEqual(relations['matching_totals']['architecture_relationships'], 3)
        filtered = load_tool('snapshot').query(output, 'relationships', {'repository': 'client', 'limit': 1}, self.root)
        self.assertEqual(filtered['matching_totals']['architecture_relationships'], 2)
        self.assertEqual(len(filtered['report']['architecture_relationships']), 1)
        services = load_tool('snapshot').query(output, 'services', {'repository': 'client'}, self.root)
        self.assertEqual(len(services['catalog']['architecture_relationships']), 2)
        self.assertEqual(json.loads((output / 'summary.json').read_bytes())['counts']['edges'], len(saved['edges']))
        provenance = json.loads((output / context.PROVENANCE).read_bytes())
        self.assertEqual(provenance['schema_version'], '1.1.0')


if __name__ == '__main__':
    unittest.main()
