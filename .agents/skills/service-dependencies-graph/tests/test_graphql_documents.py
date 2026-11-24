"""Protect imported document identity, static shape, and dynamic boundaries."""
from copy import deepcopy
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
builder = load_tool('build_graph')
Graph = builder.Graph
add_to_graph = load_tool('extract_graphql_documents').add_to_graph
build_viewer_model = load_tool('viewer_model').build_viewer_model


class GraphqlDocumentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='graphql-documents-')
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name); self.repo = self.workspace / 'repos' / 'ui'
        self.repo.mkdir(parents=True); self.graph = Graph(self.workspace)
        self.repository = self.graph.add_repository(self.repo, 'WEB', True)

    def write(self, source, name='src/documents.ts'):
        path = self.repo / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(source); return path

    def nodes(self, kind): return [node for node in self.graph.nodes.values() if node['type'] == kind]

    def test_anonymous_and_named_documents_keep_static_field_paths_without_literals(self):
        self.write('''import {gql as doc} from "@apollo/client";
const a = doc`query($id: ID = "secret-default") {
  alias: users(id: $id, auth: "secret-argument", size: 987654) @skip(if: false) {
    id profile { name }
  }
}`;
const b = doc`mutation Save { save(input: {credential: "secret-input"}) { id } }`;
const c = doc`{ version }`;
''')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['documents'], 3)
        self.assertEqual(result['statistics']['field_selections'], 7)
        self.assertEqual({node['name'] for node in self.nodes('GRAPHQL_FIELD_SELECTION')},
                         {'users', 'users.id', 'users.profile', 'users.profile.name', 'save', 'save.id', 'version'})
        user = next(node for node in self.nodes('GRAPHQL_FIELD_SELECTION') if node['name'] == 'users')
        self.assertEqual(user['properties']['response_path'], ['alias'])
        self.assertEqual(self.graph.evidence[user['evidence'][0]]['line'], 3)
        retained = str(self.graph.document()) + str(result)
        for secret in ('secret-default', 'secret-argument', 'secret-input', '987654', 'credential'):
            self.assertNotIn(secret, retained)
        self.assertFalse(any(edge['relationship'] in {'CALLS_GRAPHQL', 'SUBSCRIBES_WS'} for edge in self.graph.edges.values()))
        self.assertTrue(all('resolution_status' not in edge for edge in self.graph.edges.values()))
        model = build_viewer_model(self.graph.document())
        for node in self.nodes('GRAPHQL_DOCUMENT') + self.nodes('GRAPHQL_FIELD_SELECTION'):
            self.assertEqual(model['nodes'][node['id']]['family'], 'api')
        labels = {model['edges'][edge['id']]['label'] for edge in self.graph.edges.values()}
        self.assertEqual(labels, {'Declares GraphQL document', 'Selects GraphQL field'})
        self.assertFalse(any(edge['level'] == 'highest' for edge in model['edges'].values()))

    def test_dynamic_templates_retain_documents_and_explicit_limits_without_guessing_fields(self):
        self.write('''import {gql} from "@apollo/client";
const a = gql`query { users(token: ${secret}) { id ${fields} } }`;
const b = gql`query ${operation} { ${root}(payload: ${payload}) { id } }`;
''')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['dynamic_documents'], 2)
        self.assertEqual({node['properties']['document_status'] for node in self.nodes('GRAPHQL_DOCUMENT')}, {'PARTIAL'})
        self.assertFalse(self.nodes('GRAPHQL_FIELD_SELECTION'))
        self.assertEqual({item['reason'] for item in result['ledger']}, {'DYNAMIC_GRAPHQL_DOCUMENT'})
        self.assertTrue(all(node['properties']['operation_types'] == ['QUERY'] for node in self.nodes('GRAPHQL_DOCUMENT')))
        retained = str(self.graph.document())
        self.assertNotIn('payload', retained); self.assertNotIn('secret', retained)

    def test_import_identity_comments_and_shadowed_bindings_exclude_false_documents(self):
        self.write('''import {gql} from "@apollo/client";
// gql`query { commented }`
function parameter(gql: unknown) { return gql`query { parameter }`; }
function lexical() { const gql = other; return gql`query { lexical }`; }
function hoisted() { if (false) { var gql = other; } return gql`query { hoisted }`; }
try {} catch (gql) { gql`query { caught }`; }
const a = gql`query { active }`;
''')
        self.write('const gql = arbitrary; const a = gql`query { unrelated }`;', 'src/unrelated.ts')
        self.write('import {gql} from "unrelated"; const a = gql`query { unrelated }`;', 'src/other.ts')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['documents'], 2)
        self.assertEqual(result['statistics']['shadowed_templates'], 4)
        self.assertEqual(result['statistics']['unresolved_tag_providers'], 1)
        self.assertEqual([node['name'] for node in self.nodes('GRAPHQL_FIELD_SELECTION')], ['active'])
        unknown = next(node for node in self.nodes('GRAPHQL_DOCUMENT') if node['assertion_status'] == 'INFERRED')
        self.assertEqual(unknown['properties']['tag_provider_status'], 'UNRESOLVED')

    def test_default_graphql_tag_import_and_type_only_imports(self):
        self.write('import document from "graphql-tag"; const a = document`subscription { event { id } }`;')
        self.write('import type {gql} from "@apollo/client"; const a = gql`query { excluded }`;', 'src/types.ts')
        self.write('import {type gql} from "@apollo/client"; const a = gql`query { excluded }`;', 'src/inline-types.ts')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['documents'], 1)
        self.assertEqual(self.nodes('GRAPHQL_DOCUMENT')[0]['properties']['operation_types'], ['SUBSCRIPTION'])
        self.assertFalse(any(edge['relationship'] == 'SUBSCRIBES_WS' for edge in self.graph.edges.values()))

    def test_fragments_and_invalid_documents_retain_explicit_scope(self):
        self.write('''import {gql} from "@apollo/client";
const a = gql`query A { users { id ...Summary ... on User { name } } }
fragment Summary on User { address }`;
const b = gql`query { broken(`;
''')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['documents'], 2)
        self.assertEqual(result['statistics']['unsupported_documents'], 1)
        active = next(node for node in self.nodes('GRAPHQL_DOCUMENT') if node['properties']['document_status'] == 'STATIC')
        self.assertEqual(active['properties']['fragment_definitions'], ['Summary'])
        self.assertEqual(active['properties']['fragment_spreads'], ['Summary'])
        self.assertEqual({node['name'] for node in self.nodes('GRAPHQL_FIELD_SELECTION')}, {'users', 'users.id', 'users.name'})

    def test_existing_named_operation_and_transport_facts_stay_identical(self):
        path = self.write('import {gql} from "@apollo/client"; const a = gql`query Existing { version }`;')
        evidence = self.graph.add_evidence(self.repository, path.relative_to(self.workspace).as_posix(), 1,
                                            'Legacy named operation', 'fixture')
        self.graph.add_node('operation:graphql:existing', 'API_OPERATION', 'Existing', None,
                            dimensions=('RUNTIME',), component_kind=None, functional_role='Legacy operation',
                            business_meaning='Legacy declaration', source_paths=(), evidence=(evidence,),
                            properties={'protocol': 'GRAPHQL', 'operation_name': 'Existing'})
        before = deepcopy(self.graph.nodes['operation:graphql:existing'])
        add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(self.graph.nodes['operation:graphql:existing'], before)
        self.assertEqual(len(self.nodes('API_OPERATION')), 1)
        self.assertEqual(len(self.nodes('GRAPHQL_DOCUMENT')), 1)

    def test_dynamic_operation_name_never_creates_dollar_named_legacy_call(self):
        self.write('{"name":"fixture"}', 'package.json')
        self.write('''import {gql} from "graphql-request";
const a = gql`query ${operationName} { version }`;
const b = gql`query Valid_123 { version }`;
''')
        builder.extract_web(self.graph, self.repo, self.repository, True)
        legacy = [node['properties']['operation_name'] for node in self.nodes('API_OPERATION')
                  if node.get('properties', {}).get('operation_name')]
        self.assertEqual(legacy, ['Valid_123'])
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['documents'], 2)
        self.assertEqual(result['statistics']['dynamic_documents'], 1)


if __name__ == '__main__': unittest.main()
