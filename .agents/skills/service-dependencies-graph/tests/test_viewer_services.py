"""Keep service projection identities, ownership, summaries, and evidence truthful."""

from copy import deepcopy
import json
from pathlib import Path
import runpy
import unittest


load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
build_viewer_model = load_tool('viewer_model').build_viewer_model


def node(identifier, kind='COMPONENT', repository='mono', **properties):
    return {'id': identifier, 'name': identifier, 'type': kind,
            'repository': repository, 'properties': properties}


def edge(identifier, source, target, relationship='CALLS_SERVICE', status='RESOLVED', **properties):
    return {'id': identifier, 'source': source, 'target': target, 'relationship': relationship,
            'dimension': 'RUNTIME', 'assertion_status': 'CONFIRMED', 'resolution_status': status,
            'properties': properties, 'evidence': ['evidence:' + identifier]}


def fixture():
    return {
        'repositories': [{'id': identifier, 'kind': kind} for identifier, kind in
                         (('client', 'WEB'), ('mono', 'SPRING'), ('single', 'SPRING'))],
        'nodes': [node('client', 'APPLICATION', 'client'), node('a', 'SERVICE'), node('b', 'SERVICE'),
                  node('single', 'SERVICE', 'single')],
        'edges': [],
    }


class ViewerServicesTests(unittest.TestCase):
    def project(self, graph):
        return build_viewer_model(graph, include_traces=False)['service_graph']

    def test_actual_roots_survive_and_inventory_and_testing_never_become_services(self):
        graph = fixture()
        graph['repositories'] += [{'id': 'inventory', 'kind': 'SOURCE_ONLY'}, {'id': 'tests', 'kind': 'TESTING'}]
        graph['nodes'] += [node('ui', 'APPLICATION'), node('inventory', repository='inventory'),
                           node('test-service', 'SERVICE', 'tests'),
                           node('test-local', 'APPLICATION', 'single', dependency_scope='TESTING')]
        graph['edges'] += [edge('inventory-call', 'inventory', 'a'), edge('test-call', 'test-service', 'a'),
                           edge('test-target', 'a', 'test-service'), edge('test-local-call', 'test-local', 'a'),
                           edge('test-edge', 'client', 'a', dependency_scope='TESTING')]
        projection = self.project(graph)
        self.assertEqual(set(projection['nodes']), {'client', 'a', 'b', 'ui', 'single'})
        self.assertEqual(projection['repository_roots'], {'client': 'client', 'single': 'single'})
        self.assertEqual(projection['links'], [])

    def test_monorepo_ownership_is_transitive_exact_and_never_uses_the_first_root(self):
        graph = fixture()
        graph['nodes'] += [node('component-a'), node('operation-a', 'API_OPERATION'),
                           node('operation-b', 'API_OPERATION'), node('unowned', 'API_OPERATION'),
                           node('shared'), node('ambiguous', 'API_OPERATION')]
        graph['edges'] += [edge('owns-a', 'a', 'component-a', 'CONTAINS'),
                           edge('exposes-a', 'component-a', 'operation-a', 'EXPOSES'),
                           edge('exposes-b', 'b', 'operation-b', 'EXPOSES'),
                           edge('shared-a', 'a', 'shared', 'CONTAINS_COMPONENT'),
                           edge('shared-b', 'b', 'shared', 'CONTAINS_COMPONENT'),
                           edge('shared-exposes', 'shared', 'ambiguous', 'EXPOSES'),
                           edge('cycle', 'ambiguous', 'shared', 'CONTAINS'),
                           edge('uses-foreign', 'client', 'component-a', 'USES_COMPONENT'),
                           edge('contains-root', 'a', 'b', 'CONTAINS'),
                           edge('call-a', 'client', 'operation-a', 'CALLS_REST'),
                           edge('call-b', 'client', 'operation-b', 'CALLS_REST'),
                           edge('call-unowned', 'client', 'unowned', 'CALLS_REST'),
                           edge('call-ambiguous', 'client', 'ambiguous', 'CALLS_REST'),
                           edge('from-unowned', 'unowned', 'single'),
                           edge('from-ambiguous', 'shared', 'single'), edge('between-roots', 'a', 'b')]
        projection = self.project(graph)
        self.assertEqual({(link['source'], link['target'], tuple(link['edge_ids'])) for link in projection['links']},
                         {('client', 'a', ('call-a',)), ('client', 'b', ('call-b',)),
                          ('a', 'b', ('between-roots',))})
        self.assertEqual(projection['nodes']['b']['root_id'], 'b')

    def test_summaries_count_owned_declarations_and_direct_pairs_per_service(self):
        graph = fixture()
        graph['nodes'] += [node('component-a'), node('operation-a', 'API_OPERATION'), node('type-a', 'JAVA_TYPE'),
                           node('component-b'), node('operation-b', 'API_OPERATION'), node('unowned')]
        graph['edges'] += [edge('owns-a', 'a', 'component-a', 'CONTAINS'),
                           edge('exposes-a', 'component-a', 'operation-a', 'EXPOSES'),
                           edge('owns-type', 'a', 'type-a', 'CONTAINS'),
                           edge('type-use', 'component-a', 'type-a', 'DEPENDS_ON_TYPE'),
                           edge('owns-b', 'b', 'component-b', 'CONTAINS'),
                           edge('exposes-b', 'b', 'operation-b', 'EXPOSES'),
                           edge('a-b', 'component-a', 'operation-b', 'CALLS_REST'), edge('a-single', 'a', 'single'),
                           edge('b-a', 'b', 'a'), edge('client-a', 'client', 'operation-a', 'CALLS_REST')]
        projection = self.project(graph)
        self.assertEqual(projection['details']['a'], {
            'repository': 'mono', 'component_count': 3, 'internal_edge_count': 4,
            'inbound_relationship_count': 2, 'outbound_relationship_count': 2,
            'relationship_families': {'api': 3, 'shared': 1, 'structure': 2},
            'low_priority_relationship_count': 4,
        })
        self.assertEqual(projection['details']['b']['component_count'], 2)
        self.assertEqual(projection['details']['b']['internal_edge_count'], 2)
        self.assertEqual(projection['nodes']['a']['service_summary'], projection['details']['a'])

    def test_external_identities_and_counts_preserve_mixed_pair_evidence(self):
        graph = fixture()
        graph['nodes'] += [node('external-a', 'SERVICE', None), node('external-b', 'SERVICE', None),
                           node('topic-a', 'MESSAGE_CHANNEL', None, protocol='KAFKA'),
                           node('topic-b', 'MESSAGE_CHANNEL', None, protocol='KAFKA')]
        for item in graph['nodes'][-4:]:
            item['name'] = 'same-name'
        graph['edges'] += [edge('rest', 'a', 'external-a', 'CALLS_REST'),
                           edge('remote', 'a', 'external-a', 'LOADS_REMOTE', 'UNRESOLVED',
                                architecture_claims=[{'investigation_status': 'UNVERIFIED'}]),
                           edge('return', 'external-a', 'a'), edge('separate-id', 'a', 'external-b'),
                           edge('publish', 'a', 'topic-a', 'PUBLISHES'), edge('consume', 'b', 'topic-b', 'CONSUMES')]
        projection = self.project(graph)
        pair = next(link for link in projection['links'] if link['source'] == 'a' and link['target'] == 'external-a')
        self.assertEqual(pair['edge_ids'], ['remote', 'rest'])
        self.assertEqual(pair['evidence'], ['evidence:remote', 'evidence:rest'])
        self.assertEqual(pair['family_counts'], {'shared': 1, 'api': 1})
        self.assertEqual(pair['status'], 'mixed')
        self.assertEqual({facet['assessment'] for facet in pair['facets']}, {'EXTRACTED', 'UNVERIFIED'})
        self.assertEqual(sum(facet['count'] for facet in pair['facets']), 2)
        self.assertEqual(projection['details']['external-a']['inbound_relationship_count'], 1)
        self.assertEqual(projection['details']['external-a']['outbound_relationship_count'], 1)
        self.assertEqual(projection['details']['external-b']['inbound_relationship_count'], 1)
        self.assertNotIn('topic-a', projection['nodes'])
        self.assertNotIn('topic-b', projection['nodes'])
        self.assertFalse(any(link['source'] == 'a' and link['target'] == 'b' for link in projection['links']))

    def test_unknown_destinations_group_only_by_caller_protocol_and_literal_authority(self):
        graph = fixture()
        declarations = [('one', 'a', 'REST', 'https://api.example/one'),
                        ('two', 'a', 'REST', 'https://api.example/two'),
                        ('other-caller', 'b', 'REST', 'https://api.example/one'),
                        ('other-protocol', 'a', 'GRAPHQL', 'https://api.example/one'),
                        ('other-host', 'a', 'REST', 'https://elsewhere.example/one'),
                        ('relative-one', 'a', 'REST', '/one'), ('relative-two', 'a', 'REST', '/two')]
        for identifier, caller, protocol, path in declarations:
            graph['nodes'].append(node(identifier, 'API_OPERATION', None, protocol=protocol, path=path))
            graph['edges'].append(edge(identifier, caller, identifier, 'CALLS_REST', 'UNRESOLVED'))
        graph['nodes'].append(node('canonical-external', 'SERVICE', None, authority='api.example'))
        graph['edges'].append(edge('canonical', 'a', 'canonical-external'))
        projection = self.project(graph)
        groups = [item for item in projection['nodes'].values() if item['display_kind'] == 'Destination group']
        self.assertEqual(len(groups), 5)
        self.assertTrue(all('No shared provider' in item['provider_limit'] for item in groups))
        links = {tuple(link['edge_ids']): link for link in projection['links']}
        self.assertEqual(links[('one', 'two')]['count'], 2)
        self.assertIn(('relative-one', 'relative-two'), links)
        self.assertEqual(links[('canonical',)]['target'], 'canonical-external')
        self.assertTrue(all(item['service_summary']['inbound_relationship_count'] == 1 for item in groups))

    def test_exposed_external_operations_need_unique_provider_ownership(self):
        graph = fixture()
        graph['nodes'] += [node('known', 'API_OPERATION', None), node('ambiguous', 'API_OPERATION', None),
                           node('unowned', 'API_OPERATION', None), node('unowned-controller')]
        graph['edges'] += [edge('known-provider', 'a', 'known', 'EXPOSES'),
                           edge('provider-a', 'a', 'ambiguous', 'EXPOSES'),
                           edge('provider-b', 'b', 'ambiguous', 'EXPOSES'),
                           edge('unknown-provider', 'unowned-controller', 'unowned', 'EXPOSES'),
                           edge('known-call', 'client', 'known', 'CALLS_REST'),
                           edge('ambiguous-call', 'client', 'ambiguous', 'CALLS_REST'),
                           edge('unowned-call', 'client', 'unowned', 'CALLS_REST')]
        projection = self.project(graph)
        self.assertEqual([(link['source'], link['target'], link['edge_ids']) for link in projection['links']],
                         [('client', 'a', ['known-call'])])

    def test_low_level_relationships_stay_card_only_even_with_review_claims(self):
        graph = fixture()
        relations = [('IMPORTS_TYPE', 'JAVA_TYPE'), ('DEPENDS_ON_PACKAGE', 'EXTERNAL_SYSTEM'),
                     ('USES_ENTITY', 'ENTITY'), ('READS_CONFIG', 'CONFIGURATION_KEY'),
                     ('CALLS_COMPONENT', 'COMPONENT')]
        for relationship, kind in relations:
            graph['nodes'].append(node(relationship, kind, 'single'))
            graph['edges'].append(edge(relationship, 'a', relationship, relationship,
                                       architecture_claims=[{'investigation_status': 'SUPPORTED'}]))
        projection = self.project(graph)
        self.assertEqual(projection['links'], [])
        self.assertEqual(set(projection['nodes']), {'a', 'b', 'client', 'single'})
        self.assertEqual(projection['details']['a']['low_priority_relationship_count'], len(relations))

    def test_reviewed_gateway_routes_and_ui_loads_remain_boundary_connections(self):
        graph = fixture()
        graph['nodes'].append(node('gateway-destination', 'ARCHITECTURE_BOUNDARY', None))
        for identifier, source, target, family, kind in [
            ('route', 'a', 'gateway-destination', 'configuration', 'FORWARDS_BACKEND_REQUESTS'),
            ('remote-ui', 'client', 'single', 'structure', 'LOADS_CONTAINER'),
        ]:
            graph['edges'].append(edge(identifier, source, target, 'REVIEWED_RELATIONSHIP', 'UNRESOLVED',
                origin='ARCHITECTURE_INVESTIGATION', family=family, kind=kind,
                architecture_claims=[{'investigation_status':'SUPPORTED'}]))
        model = build_viewer_model(graph, include_traces=False)
        links = {link['edge_ids'][0]:link for link in model['service_graph']['links']}
        self.assertEqual(links['route']['family'],'api')
        self.assertEqual(links['remote-ui']['family'],'shared')
        self.assertEqual(model['edges']['route']['family'],'configuration')
        self.assertEqual(model['edges']['remote-ui']['family'],'structure')

    def test_canonical_bytes_and_legacy_metadata_remain_unchanged_and_projection_is_deterministic(self):
        graph = fixture()
        graph['edges'] += [edge('a-b', 'a', 'b'), edge('b-a', 'b', 'a')]
        original = json.dumps(graph).encode()
        model = build_viewer_model(graph, include_traces=False)
        self.assertEqual(json.dumps(graph).encode(), original)
        self.assertTrue(all('service_summary' not in item for item in model['nodes'].values()))
        reversed_graph = {key: list(reversed(value)) for key, value in deepcopy(graph).items()}
        self.assertEqual(build_viewer_model(reversed_graph, include_traces=False), model)

    def test_summary_work_does_not_rescan_all_edges_for_every_service(self):
        class CountedEdges(list):
            visits = 0

            def __iter__(self):
                for item in super().__iter__():
                    self.visits += 1
                    yield item

        graph = fixture()
        graph['edges'] = CountedEdges()
        for index in range(100):
            identifier = 'service-' + str(index)
            graph['repositories'].append({'id': identifier, 'kind': 'SPRING'})
            graph['nodes'].append(node(identifier, 'SERVICE', identifier))
            graph['edges'].append(edge(identifier, identifier, 'client'))
        projection = self.project(graph)
        self.assertEqual(len(projection['nodes']), 104)
        self.assertEqual(len(projection['links']), 100)
        self.assertLessEqual(graph['edges'].visits, 12 * len(graph['edges']))


if __name__ == '__main__':
    unittest.main()
