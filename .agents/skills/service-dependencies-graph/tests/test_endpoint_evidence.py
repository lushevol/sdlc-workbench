"""Retain static web routing and safe ORM type evidence."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
web = load_tool('extract_web_interfaces')
orm = load_tool('extract_orm_details')
Graph = load_tool('build_graph').Graph


class EndpointEvidenceTests(unittest.TestCase):
    def test_fetch_retains_root_paths_absolute_authorities_and_explicit_methods(self):
        result = web.extract_interfaces('''fetch("/orders");
fetch("https://outside.example/unknown", {method: "POST"});
fetch("/api/existing");
fetch(dynamicDestination);''')
        self.assertEqual({(row['method'], row['path']) for row in result['operations']}, {
            ('GET', '/orders'), ('POST', 'https://outside.example/unknown'), ('GET', '/api/existing')})
        self.assertEqual([row['line'] for row in result['diagnostics']
                          if row['code'] == 'UNRESOLVED_WEB_ENDPOINT'], [4])
        self.assertEqual(result['operations'][2]['declaration'], 'fetch("/api/existing")')

    def test_runtime_method_does_not_default_to_get(self):
        result = web.extract_interfaces('fetch("/orders", {method: requestMethod});')
        self.assertEqual(len(result['operations']), 1)
        self.assertEqual(result['operations'][0]['method'], 'ANY')
        self.assertEqual(result['operations'][0]['assertion_status'], 'INFERRED')
        self.assertTrue(result['operations'][0]['conditional'])

    def test_static_protocol_clients_accept_non_api_prefixes(self):
        result = web.extract_interfaces('''new WebSocket("wss://events.example/stream");
new SockJS("/events"); new GraphQLClient("https://api.example/graphql");''')
        self.assertEqual({(row['protocol'], row['path']) for row in result['operations']}, {
            ('WEBSOCKET', 'wss://events.example/stream'), ('WEBSOCKET', '/events'),
            ('GRAPHQL', 'https://api.example/graphql')})

    def test_expanded_rest_paths_require_a_supported_client_identity(self):
        result = web.extract_interfaces('''import client from "axios";
const api = client.create();
client.get("/orders"); api.post("https://outside.example/items");
const mapping = new Map(); mapping.get("/lookup-key");''')
        self.assertEqual({(row['method'], row['path']) for row in result['operations']}, {
            ('GET', '/orders'), ('POST', 'https://outside.example/items')})

    def test_web_evidence_excludes_query_header_values_and_credentialed_urls(self):
        result = web.extract_interfaces('''fetch("https://outside.example/orders?token=DO_NOT_RETAIN_QUERY#DO_NOT_RETAIN_FRAGMENT", {
method: "POST", headers: {Authorization: "DO_NOT_RETAIN_HEADER"}});
fetch("https://user:DO_NOT_RETAIN_PASSWORD@outside.example/orders");''')
        self.assertEqual(len(result['operations']), 1)
        operation = result['operations'][0]
        self.assertEqual(operation['method'], 'POST')
        self.assertEqual(operation['path'], 'https://outside.example/orders?token=%7Bvalue%7D')
        self.assertNotIn('DO_NOT_RETAIN', json.dumps(result))
        self.assertIn('UNRESOLVED_WEB_ENDPOINT', {row['code'] for row in result['diagnostics']})

    def test_orm_type_evidence_excludes_entity_initializers_and_repository_bodies(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            repo = workspace / 'repos/service'
            source = repo / 'src/main/java/example'
            source.mkdir(parents=True)
            (source / 'Order.java').write_text('''package example;
import jakarta.persistence.*;
@Entity @Table(name="orders") public class Order {
 @Column(name="customer_id") String customerId="DO_NOT_RETAIN_INITIALIZER";
 @Column(name="id") Long id;
 String defaultValue(){return "DO_NOT_RETAIN_DEFAULT";}
}''', encoding='utf-8')
            (source / 'OrderRepo.java').write_text('''package example;
import org.springframework.data.jpa.repository.JpaRepository;
interface OrderRepo extends JpaRepository<Order, Long> {
 default String data(){return "DO_NOT_RETAIN_REPOSITORY_DEFAULT";}
}''', encoding='utf-8')
            result = orm.extract(repo)
            self.assertNotIn('DO_NOT_RETAIN', json.dumps(result))
            self.assertEqual(result['entities'][0]['declaration'], '@Entity @Table class Order')
            self.assertEqual(result['entities'][0]['table'], 'orders')
            self.assertEqual({row['name'] for row in result['entities'][0]['columns']}, {'customer_id', 'id'})
            self.assertEqual(result['repositories'][0]['declared_operations'], ['data'])
            graph = Graph(workspace)
            orm.add_to_graph(graph, repo, 'repo:service', {})
            self.assertNotIn('DO_NOT_RETAIN', json.dumps(list(graph.evidence.values())))
            self.assertEqual({row['name'] for row in graph.nodes.values() if row['type'] == 'COLUMN'},
                             {'customer_id', 'id'})


if __name__ == '__main__':
    unittest.main()
