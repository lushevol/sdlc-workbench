"""Regression tests for high-recall deterministic search candidates."""
from pathlib import Path
import json
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
patterns = load_tool('extract_pattern_candidates')
builder = load_tool('build_graph')
inventory = load_tool('repository_inventory').inventory
snapshot = load_tool('snapshot')
generator = load_tool('generate_all_graphs')


class PatternCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repos/ui/client'
        self.repo.mkdir(parents=True)

    def test_search_records_dependency_families_without_asserting_edges(self):
        source = self.repo / 'src' / 'client.ts'
        source.parent.mkdir()
        source.write_text('''
const base = process.env.API_BASE;
fetch(
  "/users"
);
axios.get("/orders");
System.clearProperty("WRITE_ONLY");
const topic = "orders.events"; kafkaTemplate.send("orders.events");
const rows = db.query("select id from orders");
import thing from "@fm/shared";
''')
        (self.repo / 'schema.graphqls').write_text('\n\ntype Order { id: ID! }')
        result = patterns.scan_repository(self.root, 'repo:client', self.repo)
        families = {row['family'] for row in result['candidates']}
        self.assertTrue({'HTTP_ENDPOINT', 'CONFIG_READ', 'MESSAGE_CHANNEL', 'DATABASE_TABLE', 'MODULE_IMPORT', 'GRAPHQL_SCHEMA'} <= families)
        endpoints = {row['value'] for row in result['candidates'] if row['family'] == 'HTTP_ENDPOINT'}
        self.assertIn('/users', endpoints)
        self.assertIn('/orders', endpoints)
        self.assertNotIn('WRITE_ONLY', {row['value'] for row in result['candidates'] if row['family'] == 'CONFIG_READ'})
        self.assertTrue(all(row['basis'] == 'deterministic-search-pattern' for row in result['candidates']))
        self.assertTrue(all(row['line'] >= 1 for row in result['candidates']))
        schema = next(row for row in result['candidates'] if row['family'] == 'GRAPHQL_SCHEMA')
        self.assertEqual(schema['line'], 3)

    def test_sensitive_pattern_values_are_redacted(self):
        path = self.repo / 'src' / 'secret.ts'
        path.parent.mkdir(exist_ok=True)
        path.write_text('const token = "https://api.example/orders?token=secret";\nfetch("https://user:pass@example.test/orders");')
        (self.repo / 'proxy.conf').write_text('proxy_pass https://user:pass@example.test/api;\n')
        result = patterns.scan_repository(self.root, 'repo:client', self.repo)
        endpoints = [row['value'] for row in result['candidates'] if row['family'] == 'HTTP_ENDPOINT']
        self.assertIn('https://api.example/orders', endpoints)
        self.assertIn('<redacted>', endpoints)
        self.assertNotIn('user:pass', endpoints)
        gateway_values = [row['value'] for row in result['candidates'] if row['family'] == 'GATEWAY_ROUTE']
        self.assertNotIn('user:pass', gateway_values)

    def test_import_map_adds_unresolved_remote_bindings_with_line_evidence(self):
        manifest = self.repo / 'package.json'
        manifest.write_text(json.dumps({'name': '@fm/root-config'}))
        import_map = self.repo / 'public' / 'import-map.json'
        import_map.parent.mkdir()
        import_map.write_text(json.dumps({'imports': {'@fm/base': '/base.js', '-@fm/base': '/base-local.js', 'fm/base': '/plain-base.js', '@fm/other': 'http://user:pass@localhost:8001/other.js?token=secret', '@fm/secret': 'https://cdn.example/client_secret.js'},
                                             'scopes': {'/tiles/': {'@fm/base': '/base-scoped.js', '@fm/tile': '/tile.js'}}}, indent=2))
        graph = builder.Graph(self.root)
        rid = graph.add_repository(self.repo, 'WEB', True)
        owner = 'application:client'
        graph.add_node(owner, 'APPLICATION', 'client', rid, dimensions=('RUNTIME',), component_kind='MICRO_FRONTEND',
                       functional_role='Hosts a web runtime', business_meaning='Test application', source_paths=('repos/ui/client',),
                       evidence=(graph.add_evidence(rid, 'repos/ui/client/package.json', 1, 'manifest', 'web-manifest'),))
        builder.extract_import_maps(graph, self.repo, rid, owner)
        edges = [edge for edge in graph.edges.values() if edge['relationship'] == 'LOADS_REMOTE']
        self.assertEqual(len(edges), 5)
        self.assertTrue(all(edge['resolution_status'] == 'UNRESOLVED' for edge in edges))
        self.assertTrue(any(node['name'] == '@fm/base' for node in graph.nodes.values()))
        self.assertTrue(any(ev['extractor'] == 'systemjs-import-map' for ev in graph.evidence.values()))
        base = next(node for node in graph.nodes.values() if node['name'] == '@fm/base')
        self.assertIn('<global>', base['properties']['import_map_scopes'])
        self.assertIn('/tiles/', base['properties']['import_map_scopes'])
        self.assertIn('/base-scoped.js', base['properties']['import_map_urls'])
        base_lines = [graph.evidence[evidence_id]['line'] for evidence_id in base['evidence']]
        self.assertGreaterEqual(len(set(base_lines)), 2)
        self.assertTrue(any(node['name'] == 'fm/base' for node in graph.nodes.values()))
        base_edge = next(edge for edge in edges if edge['target'] == base['id'])
        self.assertIn('/base-scoped.js', base_edge['properties']['import_map_urls'])
        self.assertNotIn('user:pass', json.dumps(graph.document()))
        self.assertNotIn('token=secret', json.dumps(graph.document()))
        self.assertNotIn('client_secret.js', json.dumps(graph.document()))

    def test_inventory_includes_schema_and_contract_suffixes(self):
        (self.repo / 'schema.graphqls').write_text('type Query { ok: Boolean }')
        (self.repo / 'contract.proto').write_text('syntax = "proto3";')
        (self.repo / '.env.local').write_text('API_BASE=https://api.example.test\n')
        census = inventory(self.root, self.root / 'repos')
        row = census['repositories'][0]
        self.assertEqual(row['source_extensions']['.graphqls'], 1)
        self.assertEqual(row['source_extensions']['.proto'], 1)
        self.assertEqual(row['source_files'], 3)

    def test_env_files_are_scanned_as_redacted_configuration_candidates(self):
        env = self.repo / '.env.local'
        env.write_text('API_BASE=https://api.example.test\nAPI_TOKEN=secret-value\n')
        result = patterns.scan_repository(self.root, 'repo:client', self.repo)
        values = {row['value'] for row in result['candidates'] if row['family'] == 'CONFIG_READ'}
        self.assertIn('API_BASE', values)
        self.assertIn('API_TOKEN', values)
        self.assertNotIn('secret-value', values)

    def test_built_snapshot_exposes_filtered_pattern_candidates(self):
        (self.repo / 'package.json').write_text(json.dumps({'name': '@fm/client'}))
        source = self.repo / 'src' / 'client.ts'
        source.parent.mkdir(exist_ok=True)
        source.write_text('const base = process.env.API_BASE; fetch("/api/orders");')
        (self.repo / 'schema.graphqls').write_text('type Query { ok: Boolean }')
        out = self.root / 'generated'
        generator.main(['--workspace', str(self.root), '--out', str(out)])
        result = snapshot.query(out, 'patterns', {'repository': 'client', 'family': 'HTTP_ENDPOINT', 'limit': 10}, self.root)
        self.assertEqual(result['status'], 'SUCCEEDED')
        self.assertTrue(result['matches'])
        self.assertEqual(result['matches'][0]['family'], 'HTTP_ENDPOINT')
        self.assertEqual(set(result['pattern_summary']['families']), {'HTTP_ENDPOINT'})
        self.assertIn('GRAPHQL_SCHEMA', result['global_pattern_summary']['families'])


if __name__ == '__main__':
    unittest.main()
