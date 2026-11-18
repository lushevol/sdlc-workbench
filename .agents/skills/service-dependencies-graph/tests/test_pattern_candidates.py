"""Regression tests for high-recall deterministic search candidates."""
from pathlib import Path
import hashlib
import json
import runpy
import tempfile
import unittest
from unittest.mock import patch

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
        self.assertEqual(result['offset'], 0)
        self.assertIsNone(result['next_offset'])

    def test_patterns_pages_traverse_all_filtered_candidates_in_one_snapshot(self):
        (self.repo / 'package.json').write_text(json.dumps({'name': '@fixture/client'}))
        source = self.repo / 'src' / 'client.ts'
        source.parent.mkdir(exist_ok=True)
        source.write_text('const base = process.env.API_BASE;\n' + '\n'.join(
            f'fetch("/api/orders/{index}");' for index in range(7)))
        out = self.root / 'generated'
        generator.main(['--workspace', str(self.root), '--out', str(out)])
        arguments = {'repository': 'client', 'family': 'HTTP_ENDPOINT', 'limit': 2}
        offset, observed, snapshots = 0, [], set()
        while offset is not None:
            result = snapshot.query(out, 'patterns', {**arguments, 'offset': offset}, self.root)
            self.assertEqual(result['matching_total'], 7)
            self.assertEqual(result['offset'], offset)
            self.assertEqual(set(result['pattern_summary']['families']), {'HTTP_ENDPOINT'})
            observed.extend(result['matches'])
            snapshots.add(result['snapshot']['manifest_sha256'])
            offset = result['next_offset']
        self.assertEqual(len(snapshots), 1)
        self.assertEqual(len(observed), 7)
        self.assertEqual(len({row['id'] for row in observed}), 7)
        self.assertEqual({row['value'] for row in observed}, {f'/api/orders/{index}' for index in range(7)})
        beyond = snapshot.query(out, 'patterns', {**arguments, 'offset': 99}, self.root)
        self.assertEqual(beyond['matches'], [])
        self.assertEqual(beyond['matching_total'], 7)
        self.assertIsNone(beyond['next_offset'])
        first = snapshot.query(out, 'patterns', arguments, self.root)
        self.assertEqual(first['matches'], observed[:2])

    def test_patterns_offset_requires_a_nonnegative_integer(self):
        for value in (-1, 1.5, True, '1'):
            with self.subTest(offset=value), self.assertRaises(snapshot.SnapshotError) as error:
                snapshot.query(self.root, 'patterns', {'offset': value}, self.root)
            self.assertEqual(error.exception.code, 'INVALID_ARGUMENT')

    def test_flat_arbitrary_text_paths_expose_external_calls_and_provider_contracts(self):
        flat = self.root / 'flat-service'
        flat.mkdir()
        sources = {
            'connector.custom': 'client.request(\n externalUrl\n);\nEXTERNAL_URL=https://outside.example/orders\n',
            'handlers.opaque': '@GetMapping(\n "/orders/{id}"\n)\napp.post("/payment", handler);\n',
            'schema.anything': 'openapi: 3.1.0\npaths:\n  /settlement:\n    post:\nasyncapi: 3.0.0\n',
            'payload.json': '{"endpoint":"https://third-party.example/service"}',
            'suite.robot': 'Call External    https://robot.example/test\n',
        }
        for name, text in sources.items():
            (flat / name).write_text(text)
        result = patterns.scan_repository(self.root, 'repo:flat', flat)
        self.assertEqual(result['scanned_files'], len(sources))
        self.assertEqual(result['skipped_files'], [])
        values = {row['value'] for row in result['candidates']}
        self.assertTrue({'https://outside.example/orders', 'https://third-party.example/service',
                         'https://robot.example/test', '/orders/{id}', '/payment', '/settlement'} <= values)
        self.assertIn('HTTP_CLIENT', {row['family'] for row in result['candidates']})
        self.assertIn('API_CONTRACT', {row['family'] for row in result['candidates']})
        self.assertTrue(all(row['disposition'] == 'CANDIDATE' and 'relationship' not in row for row in result['candidates']))
        self.assertEqual(result['discovery_sha256'], result['file_inventory']['content_sha256'])

    def test_solace_producers_consumers_configuration_and_kafka_remain_candidates(self):
        source = self.repo / 'integration.unknown'
        source.write_text('''import com.solacesystems.jcsmp.JCSMPFactory;
import com.solacesystems.jcsmp.JCSMPProperties;
JCSMPSession session = JCSMPFactory.onlyInstance().createSession(properties);
XMLMessageProducer producer = session.createProducer(listener);
XMLMessageConsumer consumer = session.createConsumer(listener);
Topic topic = JCSMPFactory.onlyInstance().createTopic("orders/created");
producer.send(message, topic);
consumer.receive();
const solace = require("solclientjs");
const jsSession = solace.SolclientFactory.createSession({url: "wss://broker.example/smf"});
jsSession.subscribe(solace.SolclientFactory.createTopicDestination("orders/confirmed"));
spring.cloud.stream.bindings.output.destination=orders/created
spring.cloud.stream.solace.binder.msgVpn=business
solace.java.host=smfs://broker.example:55443
kafkaTemplate.send("legacy-events", message);
''')
        result = patterns.scan_repository(self.root, 'repo:client', self.repo)
        rows = result['candidates']
        solace = [row for row in rows if row['family'] == 'MESSAGE_CLIENT' and 'SOLACE' in row['protocol_hints']]
        self.assertTrue(solace)
        channels = {row['value'] for row in rows if row['family'] == 'MESSAGE_CHANNEL'}
        self.assertTrue({'orders/created', 'orders/confirmed', 'legacy-events'} <= channels)
        self.assertTrue(any(row['family'] == 'CONFIG_DECLARATION' and 'destination' in row['value'] for row in rows))
        send = next(row for row in rows if row['family'] == 'CALL_HINT' and row['value'] == 'producer.send')
        receive = next(row for row in rows if row['family'] == 'CALL_HINT' and row['value'] == 'consumer.receive')
        self.assertEqual(send['protocol_hints'], [])
        self.assertIn('producer', send['role_hints'])
        self.assertIn('subscriber', receive['role_hints'])
        unknown = self.repo / 'unknown-client'
        unknown.write_text('solaceProducer.publish(payload);')
        unknown_rows = patterns.scan_files(self.root, 'repo:client', [unknown])['candidates']
        self.assertTrue(all(row['protocol_hints'] == [] for row in unknown_rows))

    def test_repeated_and_multiline_calls_keep_each_source_reference_and_role(self):
        path = self.repo / 'calls'
        raw = b'fetch(\n  "/orders"\n);\nfetch("/orders");\n@GetMapping("/orders")\n'
        path.write_bytes(raw)
        row = next(row for row in patterns.scan_files(self.root, 'repo:client', [path])['candidates']
                   if row['family'] == 'HTTP_ENDPOINT' and row['value'] == '/orders')
        self.assertEqual(row['source_sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual({ref['start_line'] for ref in row['occurrences']}, {1, 4, 5})
        self.assertEqual(len(row['occurrences']), 3)
        self.assertTrue({'consumer', 'provider'} <= set(row['role_hints']))
        self.assertEqual(row['occurrences'][0]['end_line'], 2)
        self.assertIn('consumer', row['occurrences'][0]['role_hints'])
        self.assertIn('provider', row['occurrences'][-1]['role_hints'])
        for occurrence in row['occurrences']:
            self.assertLessEqual(len(occurrence['snippet']), 1600)
            self.assertLessEqual(occurrence['snippet_end_line'] - occurrence['snippet_start_line'], 7)

    def test_snippets_redact_neighboring_and_multiline_credentials(self):
        path = self.repo / 'sensitive.data'
        path.write_text('''API_PASSWORD=env-secret-value
fetch("https://outside.example/orders?api_key=query-secret#fragment-secret");
{"password":
 "json-secret-value", "endpoint": "https://json.example/route"}
Authorization: Bearer bearer-secret-value
JCSMPProperties.PASSWORD,
 "argument-secret-value";
client.setPassword(
 "setter-secret-value");
JCSMPFactory.createSession(
 getConnectionName(), "positional-user", "positional-secret-value");
const credentials = new PasswordAuthentication("username", "constructor-secret-value");
password: |
  yaml-secret-first
  yaml-secret-second
client.connect("https://url-user:url-password@broker.example/api?access=hidden-query");
-----BEGIN PRIVATE KEY-----
private-material-value
-----END PRIVATE KEY-----
grpc.Dial("target");
''')
        result = patterns.scan_files(self.root, 'repo:client', [path])
        serialized = json.dumps(result)
        for secret in ('env-secret-value', 'query-secret', 'fragment-secret', 'json-secret-value',
                       'bearer-secret-value', 'argument-secret-value', 'setter-secret-value',
                       'positional-user', 'positional-secret-value', 'constructor-secret-value',
                       'yaml-secret-first', 'yaml-secret-second',
                       'url-user', 'url-password', 'hidden-query', 'private-material-value'):
            self.assertNotIn(secret, serialized)
        self.assertIn('https://outside.example/orders', serialized)
        self.assertIn('broker.example/api', serialized)
        self.assertIn('source_sha256', serialized)

    def test_content_patterns_cover_rpc_messaging_storage_and_network_families(self):
        path = self.repo / 'all.protocols'
        path.write_text('''ManagedChannelBuilder.forAddress(host, port);
grpc.Dial(endpoint);
rpc Settle (Request) returns (Response);
@JmsListener(destination = "orders.queue")
RabbitTemplate rabbit; mqtt.connect(endpoint);
StreamBridge bridge; JmsTemplate jms;
LdapTemplate directory; RedisTemplate cache;
S3Client storage; BlobServiceClient blobs;
MongoClient database; JdbcTemplate jdbc;
FileInputStream file; SFTPClient remote;
Socket socket; WebSocketClient websocket;
<wsdl:definitions targetNamespace="https://schemas.example/service" />
<dependency><groupId>external.api</groupId></dependency>
''')
        result = patterns.scan_files(self.root, 'repo:client', [path])
        families = {row['family'] for row in result['candidates']}
        self.assertTrue({'RPC_INTERFACE', 'MESSAGE_CLIENT', 'MESSAGE_CHANNEL', 'DIRECTORY_CLIENT',
                         'CACHE_CLIENT', 'STORAGE_CLIENT', 'DATABASE_CLIENT', 'FILE_CLIENT',
                         'NETWORK_CLIENT', 'API_CONTRACT', 'PACKAGE_DECLARATION'} <= families)

    def test_scanner_rejects_content_changed_after_inventory(self):
        path = self.repo / 'client'
        path.write_text('fetch("/before");')
        inventory = patterns.discovery_inventory(self.repo)
        path.write_text('fetch("/after");')
        with patch.object(patterns, 'discovery_inventory', return_value=inventory):
            with self.assertRaisesRegex(ValueError, 'DISCOVERY_SOURCE_CHANGED'):
                patterns.scan_repository(self.root, 'repo:client', self.repo)

    def test_inline_proto_rpcs_and_graphql_declarations_keep_each_occurrence(self):
        path = self.repo / 'inline-contract'
        path.write_text('service Orders { rpc Settle (Request) returns (Response); rpc Cancel (Request) returns (Response); }\n'
                        'type Query { order: ID } type Mutation { settle: ID } schema { query: Query }\n')
        rows = patterns.scan_files(self.root, 'repo:client', [path])['candidates']
        rpcs = [row for row in rows if row['family'] == 'RPC_INTERFACE']
        self.assertEqual({row['value'] for row in rpcs}, {'rpc Settle (', 'rpc Cancel ('})
        self.assertTrue(all(row['line'] == 1 for row in rpcs))
        graphql = next(row for row in rows if row['family'] == 'GRAPHQL_SCHEMA')
        self.assertEqual(len(graphql['occurrences']), 3)
        self.assertEqual({ref['start_line'] for ref in graphql['occurrences']}, {2})
        self.assertEqual(len({ref['start_column'] for ref in graphql['occurrences']}), 3)

    def test_custom_extension_graphql_operations_and_sdk_clients(self):
        path = self.repo / 'graphql.custom'
        path.write_text('''import {ApolloClient, useQuery} from "@apollo/client";
query Orders($id: ID!) { order(id: $id) { id } }
mutation Settle { settle }
subscription Changed { changed }
const result = useQuery(ORDERS);
const client = new ApolloClient(options);
''')
        rows = patterns.scan_files(self.root, 'repo:client', [path])['candidates']
        operations = [row for row in rows if row['family'] == 'GRAPHQL_OPERATION']
        self.assertEqual(len(operations), 3)
        clients = {row['value'] for row in rows if row['family'] == 'GRAPHQL_CLIENT'}
        self.assertTrue({'ApolloClient', 'useQuery'} <= clients)
        path.write_text('database.query(statement); useQuery(options);')
        rows = patterns.scan_files(self.root, 'repo:client', [path])['candidates']
        self.assertFalse(any(row['family'].startswith('GRAPHQL') for row in rows))

    def test_command_flags_redact_credentials_without_removing_external_urls(self):
        path = self.repo / 'commands.custom'
        path.write_text('''curl --user demo-user:synthetic-password https://outside.example/orders
docker login registry.example -u demo -p docker-synthetic-password
fetch("https://outside.example/next");
curl -u "quoted-user:quoted-password" https://outside.example/quoted
tool --auth-token=synthetic-auth-token --api-key synthetic-api-key
wget --password=wget-password https://outside.example/download
curl -uconcatenated-user:concatenated-password https://outside.example/short-option
''')
        serialized = json.dumps(patterns.scan_files(self.root, 'repo:client', [path]))
        for secret in ('demo-user', 'synthetic-password', 'docker-synthetic-password',
                       'quoted-user', 'quoted-password', 'synthetic-auth-token', 'synthetic-api-key', 'wget-password',
                       'concatenated-user', 'concatenated-password'):
            self.assertNotIn(secret, serialized)
        self.assertIn('https://outside.example/orders', serialized)
        self.assertIn('https://outside.example/next', serialized)

    def test_large_repeated_calls_keep_complete_line_evidence(self):
        path = self.repo / 'generated-text.custom'
        calls = 6000
        path.write_text(('fetch("/orders"); //' + 'padding' * 12 + '\n') * calls)
        rows = patterns.scan_files(self.root, 'repo:client', [path])['candidates']
        endpoint = next(row for row in rows if row['family'] == 'HTTP_ENDPOINT')
        self.assertEqual(endpoint['occurrence_count'], calls)
        self.assertEqual({ref['start_line'] for ref in endpoint['occurrences']}, set(range(1, calls + 1)))
        self.assertTrue(all(ref['start_column'] == 1 and 'fetch' in ref['snippet'] for ref in endpoint['occurrences']))


if __name__ == '__main__':
    unittest.main()
