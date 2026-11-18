import json
from pathlib import Path
import shutil
import tempfile
import unittest
import runpy

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']

http = load_tool('extract_java_http')
source_inventory = load_tool('source_inventory')
builder = load_tool('build_graph')


class HttpCoverageTests(unittest.TestCase):
    def test_rewrite_targets_strip_userinfo_query_values_and_fragments(self):
        gateway = load_tool('extract_gateway_routes')
        for prefix in ('https://', '//'):
            with self.subTest(prefix=prefix):
                target = gateway._safe_rewrite_target(prefix + 'user:DO_NOT_RETAIN@orders-service/path?token=DO_NOT_RETAIN#DO_NOT_RETAIN')
                self.assertEqual(target, prefix + 'orders-service/path?token=%7Bvalue%7D')

    def test_nginx_templates_keep_route_declarations_without_environment_provider_guesses(self):
        gateway = load_tool('extract_gateway_routes')
        path = self.write('site.conf.j2', '''{% if enabled %}
server {
 location ^~ /api/ {
  proxy_pass {{ protocol }}://gateway-{{ environment }};
 }
 location /{{ app.endpoint }}/ {
  proxy_pass http://{{ app.name }}-{{ environment }};
 }
 location /notification/ {
  proxy_pass {{ protocol }}://query-service-{{ environment }};
  proxy_set_header Upgrade $http_upgrade;
 }
}
{% endif %}''')
        routes, _ = gateway.extract_nginx_routes(path)
        self.assertEqual([row['location'] for row in routes], ['/api/', '/{{ app.endpoint }}/', '/notification/'])
        self.assertEqual([row['line'] for row in routes], [3, 6, 9])
        self.assertTrue(all(row['template'] for row in routes))
        self.assertEqual(routes[0]['upstream'], 'gateway-{{ environment }}')
        self.assertTrue(routes[-1]['websocket'])
        graph = builder.Graph(self.root.parent)
        repository = graph.add_repository(self.root, 'INFRA', True)
        builder.extract_infrastructure(graph, self.root, repository)
        builder.resolve_cross_repository(graph)
        boundaries = [node for node in graph.nodes.values() if node.get('properties', {}).get('template')]
        self.assertEqual(len(boundaries), 3)
        self.assertTrue(all(not node['properties']['service_alias'] for node in boundaries))
        self.assertTrue(all(edge.get('resolution_status') != 'RESOLVED' for edge in graph.edges.values()
                            if edge['relationship'] == 'CALLS_SERVICE'))

    def test_template_and_static_upstreams_cannot_merge_provider_evidence(self):
        template = self.write('a.conf.j2', '''server {
 location /api/ {
  rewrite ^/api/(.*)$ /$1?api_key=DO_NOT_RETAIN_QUERY break;
  proxy_pass http://user:DO_NOT_RETAIN_PASSWORD@orders-service?api_key=DO_NOT_RETAIN_PROXY#DO_NOT_RETAIN_FRAGMENT;
 }
}''')
        self.write('z.conf', '''server {
 location /api/ {
  proxy_pass http://orders-service;
 }
}''')
        graph = builder.Graph(self.root.parent)
        repository = graph.add_repository(self.root, 'INFRA', True)
        builder.extract_infrastructure(graph, self.root, repository)
        provider = self.root.parent / (self.root.name + '-provider')
        provider.mkdir()
        self.addCleanup(lambda: shutil.rmtree(provider))
        (provider / 'pom.xml').write_text('<project><groupId>fixture</groupId><artifactId>orders-service</artifactId></project>')
        builder.extract_spring(graph, provider, graph.add_repository(provider, 'SPRING', True))
        builder.resolve_cross_repository(graph)
        calls = [edge for edge in graph.edges.values() if edge['relationship'] == 'CALLS_SERVICE']
        self.assertTrue(any(edge['resolution_status'] == 'RESOLVED' for edge in calls))
        template_calls = [edge for edge in calls if any(graph.evidence[ref]['path'].endswith(template.name) for ref in edge['evidence'])]
        self.assertTrue(template_calls)
        self.assertTrue(all(edge['resolution_status'] == 'UNRESOLVED' for edge in template_calls))
        self.assertNotIn('DO_NOT_RETAIN', json.dumps(graph.document()))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'pom.xml').write_text('<project/>')

    def write(self, relative, source):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
        return path

    def test_typed_calls_keep_symbolic_destinations_and_methods(self):
        self.write('src/main/java/example/Client.java', '''
import org.springframework.web.client.RestTemplate;
class Client {
  private RestTemplate client;
  void run() {
    String url = settings.getEndpoint();
    client.exchange(url, HttpMethod.POST, request, String.class);
    client.getForObject("https://example.test/data", String.class);
    client.postForEntity(settings.getHost().concat("/items"), body, String.class);
  }
}''')
        result = http.extract(self.root)
        self.assertEqual(len(result['calls']), 3)
        self.assertEqual([c['method'] for c in result['calls']], ['POST', 'GET', 'POST'])
        self.assertEqual(result['calls'][0]['endpoint_expression'], 'settings.getEndpoint()')
        self.assertTrue(result['calls'][0]['unresolved'])
        self.assertEqual(result['calls'][1]['path_value'], 'https://example.test/data')
        self.assertEqual(len(result['diagnostics']), 2)
        self.assertTrue(all(call['source_method'] == 'run' and not call['deferred'] for call in result['calls']))
        self.assertEqual(len({call['source_method_line'] for call in result['calls']}), 1)

    def test_http_calls_preserve_distinct_methods_and_deferred_callbacks(self):
        self.write('src/main/java/Client.java', '''
import org.springframework.web.client.RestTemplate;
class Client { RestTemplate client;
 void first(){ client.getForObject("/first", String.class); }
 void second(){ client.getForObject("/second", String.class); }
 void callback(){ Runnable later = () -> client.getForObject("/later", String.class); }
}''')
        graph = builder.Graph(self.root.parent)
        repository = graph.add_repository(self.root, 'SPRING', True)
        builder.extract_spring(graph, self.root, repository)
        calls = [edge for edge in graph.edges.values() if edge['relationship'] == 'CALLS_REST']
        self.assertEqual(len(calls), 3)
        by_path = {edge['properties']['path']: edge['properties']['call_sites'][0] for edge in calls}
        self.assertEqual(by_path['/first']['source_method'], 'first')
        self.assertEqual(by_path['/second']['source_method'], 'second')
        self.assertTrue(by_path['/later']['deferred'])

    def test_shadowed_foreign_and_commented_receivers_are_not_http_calls(self):
        self.write('src/main/java/Client.java', '''
import org.springframework.web.client.RestTemplate;
class Client {
  RestTemplate client;
  void run(Other client) {
    client.getForObject("https://wrong.test", String.class);
    // this.client.getForObject("https://comment.test", String.class);
  }
}''')
        self.write('src/main/java/Foreign.java', '''
import example.RestTemplate;
class Foreign { RestTemplate client;
  void run(){ client.getForObject("https://foreign.test", String.class); }
}''')
        self.assertEqual(http.extract(self.root)['calls'], [])

    def test_credentials_and_query_values_do_not_enter_new_evidence(self):
        self.write('src/main/java/Client.java', '''
import org.springframework.web.client.RestTemplate;
class Client { RestTemplate client;
  void run(){ client.getForObject("https://user:SECRET@example.test/data?token=PRIVATE", String.class); }
}''')
        result = http.extract(self.root)
        encoded = json.dumps(result)
        self.assertNotIn('SECRET', encoded)
        self.assertNotIn('PRIVATE', encoded)
        self.assertEqual(result['calls'][0]['path_value'], 'https://example.test/data?token=%7Bvalue%7D')

    def test_rooted_and_protocol_relative_urls_redact_query_values_and_fragments(self):
        self.write('src/main/java/Client.java', '''
import org.springframework.web.client.RestTemplate;
class Client { RestTemplate client;
  void run(){
    client.getForObject("/lookup?token=PRIVATE_ROOT&empty=#PRIVATE_FRAGMENT", String.class);
    client.getForObject("//user:PRIVATE_PASSWORD@example.test/data?token=PRIVATE_NETWORK", String.class);
  }
}''')
        result = http.extract(self.root)
        self.assertNotIn('PRIVATE_', json.dumps(result))
        self.assertEqual([call['path_value'] for call in result['calls']], [
            '/lookup?token=%7Bvalue%7D&empty=%7Bvalue%7D',
            '//example.test/data?token=%7Bvalue%7D'])
        self.assertTrue(all(not call['unresolved'] for call in result['calls']))

    def test_legacy_uri_literals_and_constants_redact_values_without_changing_safe_evidence(self):
        self.write('src/main/java/Client.java', '''
import java.net.URI;
class Client {
  static final String PRIVATE_URL="https://user:PRIVATE_PASSWORD@example.test/data?token=PRIVATE_QUERY#PRIVATE_FRAGMENT";
  static final String SAFE_URL="https://Example.test/data";
  void run(){
    client.execute(new URI(PRIVATE_URL), body);
    client.execute(URI.create("https://example.test/other?token=PRIVATE_LITERAL"), body);
    client.execute(new URI(SAFE_URL), body);
  }
}''')
        result = http.extract(self.root)
        self.assertNotIn('PRIVATE_PASSWORD', json.dumps(result))
        self.assertNotIn('PRIVATE_QUERY', json.dumps(result))
        self.assertNotIn('PRIVATE_FRAGMENT', json.dumps(result))
        self.assertNotIn('PRIVATE_LITERAL', json.dumps(result))
        self.assertEqual([call['path_value'] for call in result['calls']], [
            'https://example.test/data?token=%7Bvalue%7D',
            'https://example.test/other?token=%7Bvalue%7D', 'https://Example.test/data'])
        self.assertEqual(result['calls'][2]['supporting_evidence'][0]['declaration'],
                         'static final String SAFE_URL="https://Example.test/data";')
        graph = builder.Graph(self.root.parent)
        repository = graph.add_repository(self.root, 'SPRING', True)
        builder.extract_spring(graph, self.root, repository)
        artifacts = json.dumps([list(graph.nodes.values()), list(graph.edges.values()), list(graph.evidence.values())])
        for sentinel in ('PRIVATE_PASSWORD', 'PRIVATE_QUERY', 'PRIVATE_FRAGMENT', 'PRIVATE_LITERAL'):
            self.assertNotIn(sentinel, artifacts)

    def test_declared_nested_modules_preserve_original_repository_paths(self):
        (self.root / 'pom.xml').write_text('<project><modules><module>sdk</module></modules></project>')
        self.write('sdk/pom.xml', '<project/>')
        self.write('sdk/src/main/java/Client.java', '''
import org.springframework.web.client.RestTemplate;
class Client { RestTemplate client;
  void run(){ client.delete(settings.getEndpoint()); }
}''')
        calls = http.extract(self.root)['calls']
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]['path'], 'sdk/src/main/java/Client.java')
        self.assertEqual(calls[0]['method'], 'DELETE')

    def test_reassigned_url_remains_symbolic(self):
        self.write('src/main/java/Client.java', '''
import org.springframework.web.client.RestTemplate;
class Client { RestTemplate client;
  void run(String replacement){
    String url = "https://initial.test";
    url = replacement;
    client.getForObject(url, String.class);
  }
}''')
        call = http.extract(self.root)['calls'][0]
        self.assertTrue(call['unresolved'])
        self.assertEqual(call['endpoint_expression'], 'url')

    def test_module_escape_missing_and_cycles_are_explicit(self):
        (self.root / 'pom.xml').write_text('''<project><modules>
<module>../outside</module><module>missing</module><module>child</module>
</modules></project>''')
        self.write('child/pom.xml', '<project><modules><module>..</module></modules></project>')
        result = source_inventory.discover_maven_modules(self.root)
        self.assertEqual(len(result['modules']), 2)
        self.assertEqual({d['code'] for d in result['diagnostics']},
                         {'UNRESOLVED_MAVEN_MODULE', 'DUPLICATE_MAVEN_MODULE'})

    def test_endpoint_configuration_join_uses_only_destination_expression_span(self):
        self.write('src/main/java/example/Settings.java', '''package example;
import org.springframework.boot.context.properties.ConfigurationProperties;
@ConfigurationProperties(prefix="remote") class Settings {
 String url; String token;
 String getUrl(){return url;} String getToken(){return token;}
}''')
        self.write('src/main/java/example/Client.java', '''package example;
import org.springframework.web.client.RestTemplate;
class Client { RestTemplate client; Settings props;
 void run(){ String url = props.getUrl(); String unrelated = props.getToken();
 client.getForObject(url, String.class); }
}''')
        graph = builder.Graph(self.root.parent)
        repository = graph.add_repository(self.root, 'SPRING', True)
        builder.extract_spring(graph, self.root, repository)
        operations = {node['id'] for node in graph.nodes.values() if node['type'] == 'API_OPERATION'}
        reads = [edge for edge in graph.edges.values() if edge['source'] in operations and edge['relationship'] == 'READS_CONFIG']
        self.assertEqual(len(reads), 1)
        self.assertEqual(graph.nodes[reads[0]['target']]['properties']['canonical_key'], 'remote.url')
        self.assertFalse(reads[0]['properties']['profile_selected'])


if __name__ == '__main__':
    unittest.main()
