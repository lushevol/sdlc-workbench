"""Support source investigation without inventing service joins from snippets."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
snapshot = load_tool('snapshot')
inventory_tool = load_tool('repository_inventory')


class ServiceSnippetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / 'generated'
        self.output.mkdir()
        self.coverage = {'repository_root': 'repos', 'repositories': [],
                         'declaration_audit': 'coverage-declarations.json'}
        self.graph = {
            'schema_version': '2.0.0', 'generated_at': '2026-11-18T00:00:00Z',
            'generator': {'name': 'service-dependencies-graph', 'version': '2.6.0'},
            'repositories': [],
            'nodes': [{'id': identifier, 'type': 'COMPONENT', 'name': identifier,
                       'repository': None, 'dimensions': ['RUNTIME'], 'functional_role': 'Fixture source boundary',
                       'business_meaning': 'Dependency query fixture', 'source_paths': [],
                       'assertion_status': 'CONFIRMED', 'evidence': ['evidence:client']}
                      for identifier in ('client', 'boundary')],
            'edges': [{'id': 'edge:call', 'source': 'client', 'target': 'boundary', 'evidence': ['evidence:client'],
                       'relationship': 'CALLS_COMPONENT', 'dimension': 'RUNTIME', 'assertion_status': 'CONFIRMED'}],
            'evidence': [{'id': 'evidence:client', 'repository': 'repo:caller',
                          'path': 'repos/caller/transport.ts', 'line': 5,
                          'declaration': 'HTTP call with unresolved provider',
                          'extractor': 'fixture', 'directness': 'DIRECT'}],
            'diagnostics': [],
        }
        self.rows = [
            self.candidate('endpoint', 'repo:caller', 'HTTP_ENDPOINT', '/orders',
                           'const service = client.get("/orders"); // OrderClient*[', 4, 6),
            self.candidate('provider', 'repo:provider', 'HTTP_PROVIDER', '/orders',
                           '@GetMapping("/orders")', 10, 10),
            self.candidate('module', 'repo:caller', 'MODULE_IMPORT', '@internal/order-client',
                           'import OrderClient from "@internal/order-client";', 1, 1),
            self.candidate('call', 'repo:caller', 'CALL_HINT', 'orderClient.send',
                           'orderClient.send(request);', 20, 20),
        ]
        self.write_bundle()

    @staticmethod
    def candidate(identifier, repository, family, value, snippet, start, end):
        return {'id': identifier, 'repository': repository,
                'path': 'repos/caller/transport.ts' if repository == 'repo:caller' else 'repos/provider/api.java',
                'line': start, 'family': family, 'pattern_id': 'fixture', 'value': value,
                'source_sha256': 'a' * 64, 'accountability': 'REVIEW_REQUIRED',
                'role_hints': ['provider' if family == 'HTTP_PROVIDER' else 'consumer'],
                'protocol_hints': ['HTTP'] if family.startswith('HTTP_') else [],
                'occurrences': [{'start_line': start, 'end_line': end, 'start_column': 0, 'end_column': 20,
                                 'snippet_start_line': start, 'snippet_end_line': end, 'snippet': snippet}]}

    def write_bundle(self):
        audit = {'schema_version': '1.0.0', 'pattern_candidates': self.rows,
                 'pattern_summary': {'families': {}}, 'repositories': {}, 'families': {}, 'limitations': []}
        artifacts = {'graph.json': self.graph, 'analysis-coverage.json': self.coverage,
                     'repository-relationships.json': {}, 'services.json': {}, 'coverage-declarations.json': audit}
        manifest_rows = []
        for name, value in artifacts.items():
            raw = (json.dumps(value) + '\n').encode()
            (self.output / name).write_bytes(raw)
            manifest_rows.append({'path': name, 'sha256': hashlib.sha256(raw).hexdigest()})
        graph_hash = next(row['sha256'] for row in manifest_rows if row['path'] == 'graph.json')
        (self.output / 'manifest.json').write_text(json.dumps({
            'canonical_graph': 'graph.json', 'generated_at': '2026-11-18T00:00:00Z',
            'graph_sha256': graph_hash, 'artifacts': manifest_rows}))

    def query(self, **arguments):
        return snapshot.query(self.output, 'patterns', arguments, self.root)

    def test_default_retains_candidate_scope_and_hides_snippet_text(self):
        result = self.query()
        self.assertEqual(result['matching_total'], 4)
        self.assertEqual([row['id'] for row in result['matches']], [row['id'] for row in self.rows])
        first = result['matches'][0]
        self.assertNotIn('snippet', first['occurrences'][0])
        self.assertEqual(first['occurrences'][0]['start_line'], 4)
        self.assertEqual(first['source_sha256'], 'a' * 64)
        self.assertEqual(first['canonical_evidence_ids'], ['evidence:client'])
        self.assertEqual(first['related_node_ids'], ['boundary', 'client'])
        self.assertNotIn('resolution_status', first)

    def test_literal_case_insensitive_search_follows_snippet_references(self):
        result = self.query(query='ORDERCLIENT*[')
        self.assertEqual([row['id'] for row in result['matches']], ['endpoint'])
        self.assertNotIn('snippet', result['matches'][0]['occurrences'][0])
        shown = self.query(query='orderclient*[', include_snippets=True)
        self.assertEqual(shown['matches'][0]['occurrences'][0]['snippet'], self.rows[0]['occurrences'][0]['snippet'])
        self.assertEqual(self.query(query='client.get("/orders")')['matching_total'], 1)
        self.assertEqual(self.query(query='HTTP')['matching_total'], 2)
        self.assertEqual(self.query(query='missing-name')['matching_total'], 0)

    def test_service_scope_pagination_keeps_providers_and_uncertain_calls(self):
        first = self.query(service_only=True, query='orders', limit=1)
        second = self.query(service_only=True, query='orders', limit=1, offset=first['next_offset'])
        self.assertEqual(first['matching_total'], 2)
        self.assertEqual(first['matches'][0]['id'], 'endpoint')
        self.assertEqual(second['matches'][0]['id'], 'provider')
        self.assertIsNone(second['next_offset'])
        self.assertEqual(first['snapshot'], second['snapshot'])
        self.assertEqual(set(first['pattern_summary']['families']), {'HTTP_ENDPOINT', 'HTTP_PROVIDER'})
        caller = self.query(service_only=True, repository='caller')
        self.assertEqual(caller['matching_total'], 2)
        self.assertEqual({row['id'] for row in caller['matches']}, {'endpoint', 'call'})
        self.assertNotIn('resolution_status', next(row for row in caller['matches'] if row['id'] == 'call'))
        self.assertEqual(self.query(service_only=True, family='MODULE_IMPORT')['matching_total'], 0)

    def test_service_scope_retains_graphql_clients_and_operations(self):
        for identifier, family, value in (
            ('graphql-client', 'GRAPHQL_CLIENT', 'ApolloClient'),
            ('graphql-operation', 'GRAPHQL_OPERATION', 'query Orders'),
        ):
            row = self.candidate(identifier, 'repo:caller', family, value,
                                 value, 30, 30)
            row['protocol_hints'] = ['GRAPHQL']
            self.rows.append(row)
        self.write_bundle()
        result = self.query(service_only=True, repository='caller', query='graphql')
        self.assertEqual(result['matching_total'], 2)
        self.assertEqual({row['family'] for row in result['matches']},
                         {'GRAPHQL_CLIENT', 'GRAPHQL_OPERATION'})
        self.assertTrue(all('snippet' not in occurrence for row in result['matches']
                            for occurrence in row['occurrences']))

    def test_occurrence_pages_bound_snippets_and_canonical_links_without_losing_matches(self):
        row = self.candidate('many', 'repo:caller', 'HTTP_ENDPOINT', '/orders', '', 100, 100)
        row['occurrences'] = [self.candidate('unused', 'repo:caller', 'HTTP_ENDPOINT', '/orders',
                                             f'fetch("/orders"); // occurrence {index}',
                                             100 + index, 100 + index)['occurrences'][0]
                              for index in range(25)]
        self.rows.extend((row, {**deepcopy(row), 'id': 'many-copy'}))
        for index, line in enumerate((100, 110, 124)):
            identifier = f'evidence:page-{index}'
            self.graph['evidence'].append({
                'id': identifier, 'repository': 'repo:caller',
                'path': row['path'], 'line': line,
                'declaration': 'HTTP call occurrence', 'extractor': 'fixture', 'directness': 'DIRECT',
            })
            self.graph['nodes'][0]['evidence'].append(identifier)
        self.write_bundle()
        default = self.query(candidate_id='many')
        first = default['matches'][0]
        self.assertEqual(default['matching_total'], 1)
        self.assertEqual(first['occurrence_count'], 25)
        self.assertEqual(len(first['occurrences']), 10)
        self.assertEqual(first['next_occurrence_offset'], 10)
        self.assertTrue(all('snippet' not in ref for ref in first['occurrences']))
        offset, observed, page_sizes, snapshots = 0, [], [], set()
        while offset is not None:
            result = self.query(candidate_id='many', include_snippets=True, occurrence_offset=offset)
            page = result['matches'][0]
            self.assertEqual(page['occurrence_offset'], offset)
            self.assertEqual(page['occurrence_count'], 25)
            self.assertEqual(page['line'], 100)
            self.assertEqual(page['canonical_evidence_ids'], [f'evidence:page-{len(page_sizes)}'])
            self.assertEqual(page['related_node_ids'], ['client'])
            self.assertTrue(all('snippet' in ref for ref in page['occurrences']))
            page_sizes.append(len(page['occurrences']))
            observed.extend(page['occurrences'])
            snapshots.add(result['snapshot']['manifest_sha256'])
            offset = page['next_occurrence_offset']
        self.assertEqual(page_sizes, [10, 10, 5])
        self.assertEqual(observed, row['occurrences'])
        self.assertEqual(len(snapshots), 1)
        beyond = self.query(candidate_id='many', occurrence_offset=25)['matches'][0]
        self.assertEqual(beyond['occurrences'], [])
        self.assertEqual(beyond['canonical_evidence_ids'], [])
        self.assertIsNone(beyond['next_occurrence_offset'])
        short = self.query(candidate_id='many', occurrence_limit=2)['matches'][0]
        self.assertEqual(len(short['occurrences']), 2)
        self.assertEqual(short['next_occurrence_offset'], 2)
        self.assertEqual(self.query(candidate_id='missing')['matching_total'], 0)

    def test_optional_fields_require_correct_types_and_preserve_checksum_validation(self):
        for arguments in ({'query': ''}, {'query': 1}, {'query': 'a\x00b'},
                          {'service_only': 'true'}, {'include_snippets': 1}, {'other': True},
                          {'candidate_id': ''}, {'candidate_id': 1},
                          {'occurrence_offset': -1}, {'occurrence_offset': True},
                          {'occurrence_limit': 0}, {'occurrence_limit': 501}, {'occurrence_limit': 1.5}):
            with self.subTest(arguments=arguments), self.assertRaises(snapshot.SnapshotError) as error:
                self.query(**arguments)
            self.assertEqual(error.exception.code, 'INVALID_ARGUMENT')
        path = self.output / 'coverage-declarations.json'
        path.write_text(path.read_text().replace('OrderClient', 'ChangedClient'))
        with self.assertRaises(snapshot.SnapshotError) as error:
            self.query(include_snippets=True)
        self.assertEqual(error.exception.code, 'INVALID_SNAPSHOT')

    def test_legacy_rows_without_occurrences_remain_searchable(self):
        self.rows = [{key: value for key, value in self.rows[0].items()
                      if key not in {'occurrences', 'source_sha256', 'role_hints', 'protocol_hints'}}]
        self.write_bundle()
        result = self.query(query='orders', service_only=True, include_snippets=True)
        self.assertEqual(result['matching_total'], 1)
        self.assertNotIn('occurrences', result['matches'][0])
        continued = self.query(candidate_id='endpoint', occurrence_offset=10, occurrence_limit=2)
        self.assertNotIn('occurrences', continued['matches'][0])
        self.assertEqual(continued['matches'], result['matches'])

    def test_legacy_source_freshness_does_not_compare_uncaptured_discovery_scope(self):
        repository = {'name': 'caller', 'path': 'repos/caller', 'kind': 'WEB', 'content_sha256': 'typed',
                      'commit': None, 'ref': None, 'dirty': None}
        self.coverage['repositories'] = [repository]
        self.write_bundle()
        current = deepcopy(self.coverage)
        current['repositories'][0]['discovery_sha256'] = 'new-broad-scope'
        with patch.object(inventory_tool, 'inventory', return_value=current):
            result = snapshot.query(self.output, 'coverage', {}, self.root)
        self.assertEqual(result['freshness']['status'], 'CURRENT')
        self.assertEqual(result['discovery_freshness']['status'], 'UNKNOWN')
        self.coverage['repositories'][0]['discovery_sha256'] = 'old-broad-scope'
        self.write_bundle()
        with patch.object(inventory_tool, 'inventory', return_value=current):
            changed = snapshot.query(self.output, 'coverage', {}, self.root)
        self.assertEqual(changed['freshness']['status'], 'STALE')
        self.assertTrue(changed['freshness']['changed_paths'])


if __name__ == '__main__':
    unittest.main()
