"""Check testing declarations, imported client identity, and secret omission."""
import json
import io
from contextlib import redirect_stdout
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
testing = load_tool('extract_testing_dependencies')
Graph = load_tool('build_graph').Graph


class TestingDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.repo = self.workspace / 'repos/testing/suite'
        self.repo.mkdir(parents=True)

    def write(self, path, content):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')

    def test_imported_requests_aliases_and_session_calls_retain_only_safe_destinations(self):
        self.write('clients.py', '''import requests as http
from requests import Session as Client, get as fetch
session = Client()
http.get("https://api.example/orders?token=QUERY_SECRET", headers={"Authorization":"HEADER_SECRET"})
session.post("https://USER_SECRET:PASSWORD_SECRET@api.example/orders#FRAGMENT_SECRET", json={"password":"BODY_SECRET"})
fetch(url="/orders", cookies={"session":"COOKIE_SECRET"})
session.request("PATCH", "/orders/42")
''')
        result = testing.extract(self.repo)
        self.assertEqual(len(result['declarations']), 4)
        self.assertEqual({r['method'] for r in result['declarations']}, {'GET', 'POST', 'PATCH'})
        self.assertEqual({r['destination'] for r in result['declarations']},
                         {'https://api.example/orders', '/orders', '/orders/42'})
        encoded = json.dumps(result)
        for secret in ['QUERY_SECRET', 'HEADER_SECRET', 'USER_SECRET', 'PASSWORD_SECRET', 'FRAGMENT_SECRET', 'BODY_SECRET', 'COOKIE_SECRET']:
            self.assertNotIn(secret, encoded)

    def test_dynamic_calls_keep_safe_symbols_and_credentials_never_enter_evidence(self):
        self.write('clients.py', '''import requests
def send(url, method):
    requests.request(method, url, auth=("USER_SECRET", "PASSWORD_SECRET"))
    requests.get("https://api.example/password/SECRET_PATH")
''')
        result = testing.extract(self.repo)
        self.assertEqual(len(result['declarations']), 2)
        self.assertTrue(all(row['dynamic'] for row in result['declarations']))
        self.assertEqual(result['declarations'][0]['destination_expression'], 'url')
        self.assertEqual(result['declarations'][0]['method'], 'UNKNOWN')
        encoded = json.dumps(result)
        self.assertNotIn('SECRET', encoded)

    def test_namespace_urls_strings_comments_and_unimported_objects_are_not_calls(self):
        self.write('fixtures.py', '''NAMESPACE="http://www.w3.org/2001/XMLSchema"
sample="requests.get('https://fixture.example')"
# requests.get('https://comment.example')
class Fake:
    def run(self):
        requests.get("https://unimported.example")
        thing.get("https://untyped.example")
''')
        self.assertEqual(testing.extract(self.repo)['declarations'], [])

    def test_shadowed_imports_and_session_names_do_not_establish_http_clients(self):
        self.write('client.py', '''import requests
session=requests.Session()
def wrong(requests):
    requests.get("https://fake.example")
def local():
    requests.get("https://before-local-assignment.example")
    requests=object()
session=object()
session.get("https://fake.example")
''')
        self.assertEqual(testing.extract(self.repo)['declarations'], [])

    def test_direct_session_field_construction_is_supported_without_executing_the_class(self):
        self.write('client.py', '''import requests
class Client:
    def __init__(self): self.session=requests.Session()
    def get(self): return self.session.get("https://api.example/orders")
''')
        result = testing.extract(self.repo)
        self.assertEqual(len(result['declarations']), 1)
        self.assertEqual(result['declarations'][0]['destination'], 'https://api.example/orders')

    def test_control_flow_reassignment_does_not_preserve_imported_client_identity(self):
        self.write('client.py', '''import requests
if True:
    requests=object()
    requests.get("/fake")
requests.get("/ambiguous")
''')
        self.assertEqual(testing.extract(self.repo)['declarations'], [])

    def test_psycopg_and_minio_keep_client_identity_without_connection_values(self):
        self.write('clients.py', '''import psycopg2 as postgres
from minio import Minio as Store
postgres.connect(host="DB_HOST_SECRET", dbname="DB_NAME_SECRET", password="DB_PASSWORD_SECRET")
Store("MINIO_ENDPOINT_SECRET", access_key="ACCESS_SECRET", secret_key="KEY_SECRET")
''')
        result = testing.extract(self.repo)
        self.assertEqual({r['family'] for r in result['declarations']}, {'TEST_DATABASE', 'TEST_OBJECT_STORAGE'})
        self.assertNotIn('SECRET', json.dumps(result))
        self.assertTrue(all(r['destination'] is None for r in result['declarations']))

    def test_robot_settings_imports_retain_local_paths_and_skip_constructor_values(self):
        self.write('Tests/api.robot', '''*** Settings ***
Library    RequestsLibrary    constructor_secret=ARGUMENT_SECRET
Library    ../support.py
Resource    ../Resources/common.resource
Resource    ${ROOT_SECRET}/dynamic.resource
*** Variables ***
${NAMESPACE}    http://www.w3.org/2001/XMLSchema
*** Test Cases ***
Example
    Log    Resource    fixture.resource
''')
        self.write('support.py', 'def keyword(): pass\n')
        self.write('Resources/common.resource', '*** Keywords ***\nKeyword\n    No Operation\n')
        result = testing.extract(self.repo)
        self.assertEqual(len(result['declarations']), 4)
        self.assertNotIn('SECRET', json.dumps(result))
        graph = Graph(self.workspace)
        stats = testing.add_to_graph(graph, self.repo, 'repo:suite')
        self.assertEqual(stats['declarations'], 4)
        imports = [e for e in graph.edges.values() if e['relationship'].startswith('IMPORTS_TEST_')]
        resolved = [e for e in imports if e.get('resolution_status') == 'RESOLVED']
        self.assertEqual(len(resolved), 2)
        self.assertTrue(all(len(e['evidence']) == 2 for e in resolved))
        self.assertTrue(all(e['properties']['dependency_scope'] == 'TESTING' for e in graph.edges.values()))
        self.assertTrue(all(n['properties']['dependency_scope'] == 'TESTING' for n in graph.nodes.values()))
        self.assertNotIn('SECRET', json.dumps(graph.document()))

    def test_env_files_are_not_treated_as_testing_sources(self):
        self.write('.env.local', '*** Settings ***\nLibrary    leaked-secret\n')
        result = testing.extract(self.repo)
        self.assertNotIn('.local', result['files_scanned'])
        self.assertEqual(result['declarations'], [])

    def test_excluded_and_symlinked_sources_do_not_supply_testing_evidence(self):
        self.write('tests/excluded.py', 'import requests; requests.get("/excluded")')
        outside = self.workspace / 'outside.py'
        outside.write_text('import requests; requests.get("/outside")')
        (self.repo / 'linked.py').symlink_to(outside)
        self.assertEqual(testing.extract(self.repo)['declarations'], [])

    def test_python_parse_failures_remain_diagnostics_without_raw_source(self):
        self.write('broken.py', 'password="SYNTAX_SECRET"\nthis is not Python !!!')
        result = testing.extract(self.repo)
        self.assertEqual(result['diagnostics'][0]['code'], 'TEST_PYTHON_PARSE_ERROR')
        self.assertEqual(result['ledger'][0]['disposition'], 'GAP')
        self.assertNotIn('SYNTAX_SECRET', json.dumps(result))

    def test_explicit_testing_catalog_builds_valid_testing_graph_without_production_claims(self):
        self.write('client.py', 'import requests; requests.get("/orders")')
        (self.workspace / 'workspace.yaml').write_text('schema_version: 1\nregistries:\n  repositories: registry/repositories.yaml\n')
        registry = self.workspace / 'registry'
        registry.mkdir()
        (registry / 'repositories.yaml').write_text('''schema_version: 1
repositories:
- id: suite
  primary_type: testing
  location: repos/testing/suite
''')
        ordinary = self.workspace / 'repos/ordinary'
        ordinary.mkdir()
        (ordinary / 'client.py').write_text('import requests; requests.get("/unclassified")')
        output = self.workspace / 'graph'
        with redirect_stdout(io.StringIO()):
            status = load_tool('build_graph').main(['--workspace', str(self.workspace), '--repos', str(self.workspace / 'repos'),
                                                    '--out', str(output)])
        self.assertEqual(status, 0)
        graph = json.loads((output / 'graph.json').read_text())
        coverage = json.loads((output / 'analysis-coverage.json').read_text())
        self.assertEqual([r['kind'] for r in graph['repositories']], ['TESTING'])
        self.assertEqual([r['name'] for r in graph['repositories']], ['suite'])
        self.assertTrue(all('BUSINESS' not in n['dimensions'] for n in graph['nodes']))
        self.assertFalse(any(n['type'] in {'SERVICE', 'APPLICATION'} for n in graph['nodes']))
        self.assertTrue(all(n['properties']['dependency_scope'] == 'TESTING' for n in graph['nodes']))
        self.assertEqual(load_tool('validate_graph').validate(graph, self.workspace), [])
        ordinary_coverage = next(r for r in coverage['repositories'] if r['name'] == 'ordinary')
        self.assertEqual(ordinary_coverage['status'], 'UNSUPPORTED')
        self.assertIsNone(ordinary_coverage['kind'])


if __name__ == '__main__':
    unittest.main()
