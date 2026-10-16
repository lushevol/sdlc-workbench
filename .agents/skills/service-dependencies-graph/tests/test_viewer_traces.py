"""Protect method paths, declaration alternatives, and bounded graph navigation."""
from copy import deepcopy
from pathlib import Path
import runpy
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
build_trace_model = load_tool('viewer_traces').build_trace_model
build_viewer_model = load_tool('viewer_model').build_viewer_model


def node(identifier, *, kind='COMPONENT', type_kind='class', methods=(), qualified=None,
         path=None, component_kind=None, repository='repo:orders'):
    return {'id': identifier, 'name': identifier, 'type': kind, 'repository': repository,
            'component_kind': component_kind, 'source_paths': [path] if path else [],
            'evidence': ['ev:' + identifier],
            'properties': {'type_kind': type_kind, 'declared_methods': list(methods),
                           **({'qualified_name': qualified} if qualified else {})}}


def method(name, line, arity=0):
    return {'name': name, 'line': line, 'arity': arity}


def edge(identifier, source, target, relationship, **properties):
    return {'id': identifier, 'source': source, 'target': target, 'relationship': relationship,
            'dimension': 'RUNTIME', 'assertion_status': 'CONFIRMED', 'evidence': ['ev:' + identifier],
            'properties': properties}


def call_site(source, source_line, target, target_line=None, arity=0, **extra):
    return {'source_method': source, 'source_method_line': source_line, 'target_method': target,
            'target_method_line': target_line, 'arity': arity, 'line': source_line + 1,
            'path': 'src/Fixture.java', 'evidence': ['ev:call'], **extra}


def graph_fixture():
    nodes = [node('service', kind='SERVICE'), node('api', kind='API_OPERATION'),
             node('controller', methods=[method('get', 10), method('delete', 20)]),
             node('interface', type_kind='interface', methods=[method('find', 5)]),
             node('impl', methods=[method('find', 30), method('remove', 40)]),
             node('repo', methods=[method('lookup', 50)]), node('entity', kind='ENTITY'),
             node('column', kind='COLUMN'), node('config', kind='CONFIGURATION_KEY'),
             node('other-config', kind='CONFIGURATION_KEY'),
             node('external', kind='API_OPERATION', repository=None)]
    edges = [edge('exposes', 'service', 'api', 'EXPOSES'),
             edge('handler', 'api', 'controller', 'INVOKES', handler='get', handler_line=10, handler_arity=0),
             edge('controller-call', 'controller', 'interface', 'CALLS_COMPONENT',
                  call_sites=[call_site('get', 10, 'find', 5), call_site('delete', 20, 'find', 5)]),
             edge('implements', 'impl', 'interface', 'IMPLEMENTS_TYPE'),
             edge('repo-call', 'impl', 'repo', 'CALLS_COMPONENT', call_sites=[call_site('find', 30, 'lookup', 50)]),
             edge('mapping', 'repo', 'entity', 'USES_ENTITY'),
             edge('column-mapping', 'entity', 'column', 'MAPS_TO_COLUMN'),
             edge('config-read', 'impl', 'config', 'READS_CONFIG',
                  call_sites=[call_site('find', 30, 'getValue')]),
             edge('other-read', 'impl', 'other-config', 'READS_CONFIG',
                  call_sites=[call_site('remove', 40, 'getValue')]),
             edge('external-call', 'impl', 'external', 'CALLS_REST')]
    edges[-1]['resolution_status'] = 'UNRESOLVED'
    return {'nodes': nodes, 'edges': edges,
            'repositories': [{'id': 'repo:orders', 'name': 'Orders', 'kind': 'SPRING'}]}


class ViewerTraceTests(unittest.TestCase):
    def test_method_path_retains_alternatives_mapping_and_exact_evidence(self):
        graph = graph_fixture()
        original = deepcopy(graph)
        trace = build_viewer_model(graph)['traces']['api']
        self.assertEqual(graph, original)
        self.assertTrue({'handler', 'controller-call', 'implements', 'repo-call', 'mapping',
                         'column-mapping', 'config-read', 'external-call'} <= set(trace['edge_ids']))
        self.assertNotIn('other-read', trace['edge_ids'])
        steps = {step['edge_id']: step for step in trace['steps']}
        self.assertEqual(steps['controller-call']['selected_call_sites'],
                         [graph['edges'][2]['properties']['call_sites'][0]])
        self.assertEqual(steps['implements']['source'], 'impl')
        self.assertEqual(steps['implements']['target'], 'interface')
        self.assertEqual(steps['implements']['role'], 'implementation_candidate')
        self.assertEqual(steps['implements']['traversal'], 'reverse_context')
        self.assertEqual(steps['repo-call']['scope'], 'implementation_context')
        self.assertEqual(steps['config-read']['evidence'], ['ev:config-read'])
        self.assertEqual(steps['column-mapping']['scope'], 'declaration_context')
        reasons = {item['reason'] for item in trace['breaks']}
        self.assertIn('RUNTIME_IMPLEMENTATION_NOT_SELECTED', reasons)
        self.assertIn('PROVIDER_IDENTITY_UNRESOLVED', reasons)
        self.assertFalse(trace['limits']['truncated'])

    def test_legacy_class_calls_do_not_claim_handler_method_dispatch(self):
        graph = graph_fixture()
        graph['edges'][2]['properties'] = {'method': 'find'}
        trace = build_trace_model(graph)['traces']['api']
        step = next(step for step in trace['steps'] if step['edge_id'] == 'controller-call')
        self.assertEqual(step['role'], 'class_call_context')
        self.assertEqual(step['scope'], 'class_context')
        self.assertNotIn('repo-call', trace['edge_ids'])
        self.assertIn('CALLER_METHOD_NOT_RECORDED', {item['reason'] for item in trace['breaks']})

    def test_same_source_type_identity_bridges_are_explicit_and_ambiguous_candidates_stop(self):
        graph = graph_fixture()
        original = next(n for n in graph['nodes'] if n['id'] == 'entity')
        original['properties']['qualified_name'] = 'orders.Order'
        original['source_paths'] = ['src/Order.java']
        graph['nodes'].append(node('type', qualified='orders.Order', path='src/Order.java', component_kind='JAVA_TYPE'))
        graph['edges'].append(edge('identity-containment', 'type', 'entity', 'CONTAINS_COMPONENT'))
        model = build_trace_model(graph)
        bridges = model['traces']['api']['identity_bridges']
        self.assertTrue(any(item['source'] == 'entity' and item['target'] == 'type' for item in bridges))
        self.assertTrue(all(item['rule'] == 'exact-repository-qualified-type-source' for item in bridges))
        step = next(item for item in model['traces']['api']['steps'] if item['edge_id'] == 'identity-containment')
        self.assertEqual(step['role'], 'identity_context')
        self.assertEqual((step['source'], step['target']), ('type', 'entity'))
        graph['nodes'].append(node('duplicate-type', qualified='orders.Order', path='src/Order.java',
                                   component_kind='JAVA_TYPE'))
        ambiguous = build_trace_model(graph)['traces']['api']
        self.assertFalse(ambiguous['identity_bridges'])
        self.assertNotIn('duplicate-type', ambiguous['node_ids'])
        self.assertIn('AMBIGUOUS_SOURCE_TYPE_IDENTITY', {item['reason'] for item in ambiguous['breaks']})

    def test_method_cycles_terminate_and_limits_retain_every_anchor(self):
        graph = graph_fixture()
        graph['edges'].append(edge('self', 'repo', 'repo', 'CALLS_COMPONENT',
                                   call_sites=[call_site('lookup', 50, 'lookup', 50)]))
        model = build_trace_model(graph)
        self.assertIn('self', model['traces']['api']['edge_ids'])
        self.assertLess(len(model['traces']['api']['steps']), 20)
        limited = build_trace_model(graph, max_hops=1, max_nodes=3, max_edges=2)
        self.assertEqual(set(limited['traces']), set(model['traces']))
        trace = limited['traces']['api']
        self.assertTrue(trace['limits']['truncated'])
        self.assertIn('controller-call', trace['limits']['omitted_edge_ids'])
        self.assertIn('api', limited['trace_index']['by_repository']['repo:orders'])

    def test_self_calls_reach_helpers_and_deferred_http_calls_remain_context(self):
        graph = graph_fixture()
        controller = next(n for n in graph['nodes'] if n['id'] == 'controller')
        controller['properties']['declared_methods'].append(method('helper', 25))
        graph['edges'][2]['properties']['call_sites'] = [call_site('helper', 25, 'find', 5)]
        graph['edges'].append(edge('helper-call', 'controller', 'controller', 'CALLS_COMPONENT',
                                   call_sites=[call_site('get', 10, 'helper', 25)]))
        graph['edges'].append(edge('deferred-http', 'controller', 'external', 'CALLS_REST',
                                   call_sites=[call_site('helper', 25, 'fetch', deferred=True)]))
        trace = build_trace_model(graph)['traces']['api']
        self.assertTrue({'helper-call', 'controller-call', 'repo-call'} <= set(trace['edge_ids']))
        deferred = next(step for step in trace['steps'] if step['edge_id'] == 'deferred-http')
        self.assertEqual(deferred['role'], 'deferred_call_context')
        self.assertEqual(deferred['scope'], 'declaration_context')

    def test_ambiguous_overloads_deferred_and_candidate_calls_do_not_continue(self):
        for mode in ('overload', 'deferred', 'candidate'):
            with self.subTest(mode=mode):
                graph = graph_fixture()
                call = graph['edges'][2]
                if mode == 'overload':
                    interface = next(n for n in graph['nodes'] if n['id'] == 'interface')
                    interface['properties']['declared_methods'].append(method('find', 7))
                    call['properties']['call_sites'][0]['target_method_line'] = None
                elif mode == 'deferred':
                    call['properties']['call_sites'][0]['deferred'] = True
                else:
                    call['assertion_status'] = 'INFERRED'
                trace = build_trace_model(graph)['traces']['api']
                self.assertNotIn('repo-call', trace['edge_ids'])
                self.assertTrue(trace['breaks'])

    def test_same_class_edge_keeps_direct_and_deferred_methods_separate(self):
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                graph = graph_fixture()
                controller = next(n for n in graph['nodes'] if n['id'] == 'controller')
                controller['properties']['declared_methods'].append(method('helper', 25))
                graph['edges'][2]['properties']['call_sites'] = [
                    call_site('get', 10, 'find', 5, deferred=reverse),
                    call_site('helper', 25, 'find', 5, deferred=not reverse)]
                graph['edges'].append(edge('helper-call', 'controller', 'controller', 'CALLS_COMPONENT',
                                           call_sites=[call_site('get', 10, 'helper', 25)]))
                trace = build_trace_model(graph)['traces']['api']
                step = next(s for s in trace['steps'] if s['edge_id'] == 'controller-call')
                self.assertEqual(step['role'], 'call')
                self.assertEqual(len(step['selected_call_sites']), 1)
                self.assertFalse(step['selected_call_sites'][0]['deferred'])
                self.assertEqual(len(step['deferred_call_sites']), 1)
                self.assertTrue(step['deferred_call_sites'][0]['deferred'])

    def test_deferred_configuration_reads_do_not_claim_direct_method_scope(self):
        graph = graph_fixture()
        graph['edges'].append(edge('deferred-config', 'controller', 'config', 'READS_CONFIG',
                                   call_sites=[call_site('get', 10, 'getValue', deferred=True)]))
        trace = build_trace_model(graph)['traces']['api']
        step = next(item for item in trace['steps'] if item['edge_id'] == 'deferred-config')
        self.assertEqual(step['scope'], 'declaration_context')
        self.assertEqual(step['role'], 'deferred_configuration_context')
        self.assertEqual(len(step['selected_call_sites']), 0)
        self.assertEqual(len(step['deferred_call_sites']), 1)
        self.assertIn('DEFERRED_CONFIGURATION_EXECUTION_NOT_ESTABLISHED',
                      {item['reason'] for item in trace['breaks']})

    def test_direct_and_deferred_configuration_reads_retain_separate_sites(self):
        graph = graph_fixture()
        controller = next(n for n in graph['nodes'] if n['id'] == 'controller')
        controller['properties']['declared_methods'].append(method('helper', 25))
        graph['edges'].extend([
            edge('helper-call', 'controller', 'controller', 'CALLS_COMPONENT',
                 call_sites=[call_site('get', 10, 'helper', 25)]),
            edge('mixed-config', 'controller', 'config', 'READS_CONFIG', call_sites=[
                call_site('get', 10, 'getValue', deferred=True),
                call_site('helper', 25, 'getValue', deferred=False)])])
        trace = build_trace_model(graph)['traces']['api']
        step = next(item for item in trace['steps'] if item['edge_id'] == 'mixed-config')
        self.assertEqual((step['role'], step['scope']), ('configuration', 'method_path'))
        self.assertTrue(all(not site['deferred'] for site in step['selected_call_sites']))
        self.assertTrue(all(site['deferred'] for site in step['deferred_call_sites']))

    def test_ambiguous_handler_declarations_stay_class_context(self):
        graph = graph_fixture()
        graph['edges'][1]['properties']['handler_declarations'] = [
            {'handler': 'get', 'handler_line': 10, 'handler_arity': 0, 'path': 'src/Controller.java'},
            {'handler': 'delete', 'handler_line': 20, 'handler_arity': 0, 'path': 'src/Controller.java'}]
        trace = build_trace_model(graph)['traces']['api']
        step = next(item for item in trace['steps'] if item['edge_id'] == 'handler')
        self.assertEqual(step['scope'], 'class_context')
        self.assertEqual(step['role'], 'handler_context')
        self.assertIn('AMBIGUOUS_HANDLER_DECLARATION', {item['reason'] for item in trace['breaks']})
        self.assertFalse(any(item['scope'] == 'method_path' for item in trace['steps']))

    def test_unresolved_api_target_does_not_select_its_handler(self):
        graph = graph_fixture()
        graph['edges'].append(edge('unresolved-handler', 'external', 'controller', 'INVOKES', handler='get'))
        trace = build_trace_model(graph)['traces']['impl']
        self.assertIn('external-call', trace['edge_ids'])
        self.assertNotIn('unresolved-handler', trace['edge_ids'])


if __name__ == '__main__':
    unittest.main()
