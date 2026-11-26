"""Protect graph priorities, evidence aggregation, and safe viewer output."""

from contextlib import redirect_stdout
from copy import deepcopy
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import runpy

load_tool = runpy.run_path(str(Path(__file__).with_name("_support.py")))["load_tool"]
build_viewer_model = load_tool("viewer_model").build_viewer_model


def graph_fixture():
    """Supply distinct source facts that require different viewer projections."""
    repositories = [{"id": "repo:" + name, "name": name, "path": "repos/" + name,
                     "kind": kind, "role": "APPLICATION", "visible": True, "ref": None, "commit": None}
                    for name, kind in (("client", "WEB"), ("orders", "SPRING"), ("base", "WEB"))]

    def node(identifier, kind, repository, *, name=None, properties=None):
        return {"id": identifier, "type": kind, "name": name or identifier,
                "repository": repository, "dimensions": ["RUNTIME"], "functional_role": "Fixture declaration",
                "business_meaning": "Fixture scope", "source_paths": [], "evidence": [],
                "assertion_status": "CONFIRMED", "properties": properties or {}}

    nodes = [
        node("application:client", "APPLICATION", "repo:client", name="Client"),
        node("component:client:call", "COMPONENT", "repo:client", name="Order caller"),
        node("service:orders", "SERVICE", "repo:orders", name="Orders"),
        node("operation:orders:get", "API_OPERATION", "repo:orders", name="GET /orders/{id}",
             properties={"protocol": "REST"}),
        node("operation:orders:list", "API_OPERATION", "repo:orders", name="GET /orders",
             properties={"protocol": "REST"}),
        node("operation:orders:graphql", "API_OPERATION", "repo:orders", name="QUERY orders",
             properties={"protocol": "GRAPHQL"}),
        node("application:base", "APPLICATION", "repo:base", name="Shared base"),
        node("external:orders", "EXTERNAL_SYSTEM", None, name="Orders"),
        node("external:package", "EXTERNAL_SYSTEM", None, name="npm:react",
             properties={"coordinate": "npm:react", "dependency_kind": "BUILD", "boundary_kind": "PACKAGE"}),
        node("table:orders", "TABLE", "repo:orders", name="orders"),
    ]

    def edge(identifier, source, target, relation, evidence, status="RESOLVED", assertion="CONFIRMED", properties=None):
        return {"id": identifier, "source": source, "target": target, "relationship": relation,
                "dimension": "RUNTIME", "evidence": evidence, "assertion_status": assertion,
                "resolution_status": status, "properties": properties or {}}

    edges = [
        edge("edge:rest:get", "component:client:call", "operation:orders:get", "CALLS_REST", ["ev:client", "ev:get"]),
        edge("edge:rest:list", "application:client", "operation:orders:list", "CALLS_REST", ["ev:client", "ev:list"]),
        edge("edge:graphql", "application:client", "operation:orders:graphql", "CALLS_GRAPHQL", ["ev:client", "ev:graphql"]),
        edge("edge:module", "application:client", "application:base", "IMPORTS_MODULE", ["ev:import", "ev:package"],
             properties={"dependency_kind": "MODULE", "module": "@fixture/base"}),
        edge("edge:package", "application:client", "external:package", "DEPENDS_ON_PACKAGE", ["ev:package"],
             status="UNRESOLVED", properties={"dependency_kind": "BUILD", "coordinate": "npm:react", "scopes": ["dependencies"]}),
        edge("edge:external", "application:client", "external:orders", "CALLS_REST", ["ev:external"], status="UNRESOLVED"),
        edge("edge:candidate", "application:client", "operation:orders:get", "CALLS_REST", ["ev:candidate"], assertion="INFERRED"),
        edge("edge:ambiguous", "application:client", "external:orders", "CALLS_REST", ["ev:ambiguous"], status="AMBIGUOUS"),
        edge("edge:reads", "application:client", "table:orders", "READS", ["ev:client", "ev:table"]),
        edge("edge:contains", "application:client", "component:client:call", "USES_COMPONENT", ["ev:client"], status=None),
        edge("edge:exposes", "service:orders", "operation:orders:get", "EXPOSES", ["ev:get"], status=None),
    ]
    evidence = [{"id": identifier, "repository": None, "path": "fixture.txt", "line": 1,
                 "declaration": identifier, "extractor": "fixture", "directness": "DIRECT"}
                for identifier in sorted({ref for item in edges for ref in item["evidence"]})]
    return {"schema_version": "2.0.0", "generated_at": "2026-10-15T00:00:00Z",
            "generator": {"name": "service-dependencies-graph", "version": "fixture"},
            "repositories": repositories, "nodes": nodes, "edges": edges, "evidence": evidence, "diagnostics": []}


def scale_fixture():
    """One hundred repositories, a busy hub, cycles, and internal implementation noise."""
    graph = {**graph_fixture(), 'repositories':[], 'nodes':[], 'edges':[]}
    graph['generator']['version'] = 'synthetic-scale-fixture'
    for index in range(100):
        kind = 'WEB' if index < 12 else 'SPRING' if index < 95 else 'SOURCE_ONLY'
        rid, root = f'repo:scale-{index:03}', f'service:scale-{index:03}'
        graph['repositories'].append({'id':rid,'name':rid[5:],'kind':kind,'visible':True,
                                      'role':'LIBRARY' if 87 <= index < 95 else 'APPLICATION'})
        if kind == 'SOURCE_ONLY':
            graph['nodes'].append({'id':rid+':inventory','repository':rid,'name':'Source inventory','type':'COMPONENT'})
            continue
        graph['nodes'].append({'id':root,'repository':rid,'name':root[8:],
                               'type':'APPLICATION' if kind == 'WEB' else 'SERVICE', 'dimensions':['RUNTIME']})
        for item in range(20):
            identifier=f'component:{index}:{item}'
            graph['nodes'].append({'id':identifier,'repository':rid,'name':identifier,'type':'COMPONENT'})
            graph['edges'].append({'id':f'internal:{index}:{item}','source':root,'target':identifier,
                                   'relationship':'USES_COMPONENT','dimension':'RUNTIME','evidence':[],
                                   'assertion_status':'CONFIRMED'})
        targets = {0, (index+1)%95}
        targets.discard(index)
        for target in targets:
            for call in range(3):
                graph['edges'].append({'id':f'call:{index}:{target}:{call}','source':root,
                    'target':f'service:scale-{target:03}','relationship':'CALLS_SERVICE','dimension':'RUNTIME',
                    'evidence':['ev:client'],'assertion_status':'CONFIRMED','resolution_status':'RESOLVED'})
    return graph


class ScriptCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.current = None
        self.ids = set()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.elements.append((tag, attributes))
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        if tag == "script":
            self.current = {"attributes": attributes, "text": ""}
            self.scripts.append(self.current)

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.current = None


class GraphViewerModelTests(unittest.TestCase):
    def setUp(self):
        self.graph = graph_fixture()

    def test_highest_priority_contains_system_connections_and_excludes_build_dependencies(self):
        model = build_viewer_model(self.graph)
        self.assertEqual(model["repository_roots"], {
            "repo:client": "application:client", "repo:orders": "service:orders", "repo:base": "application:base"})
        highest = [link for link in model["system_links"] if link["level"] == "highest"]
        self.assertTrue(highest)
        self.assertTrue(all(link["status"] == "resolved" for link in highest))
        self.assertTrue(all(link["source_repository"] != link["target_repository"] for link in highest))
        self.assertFalse(any("edge:package" in link["edge_ids"] for link in highest))
        self.assertEqual(model["edges"]["edge:package"]["level"], "low")
        self.assertEqual(model["edges"]["edge:exposes"]["level"], "medium")
        self.assertEqual(model["nodes"]["component:client:call"]["root_id"], "application:client")
        self.assertEqual(model["nodes"]["component:client:call"]["lane"], "ui")
        self.assertEqual(model["nodes"]["external:package"]["lane"], "package")
        self.assertTrue({"api", "data", "shared"} <= {link["family"] for link in highest})

    def test_investigated_external_claims_and_mixed_assessments_keep_their_meanings(self):
        """Given mixed review results, when projected, then status and evidence remain independently visible."""
        graph = self.graph
        reviewed = next(edge for edge in graph['edges'] if edge['id'] == 'edge:external')
        reviewed['properties']['architecture_claims'] = [
            {'claim_id': 'reported-call', 'investigation_status': 'UNVERIFIED', 'family': 'api'}]
        supported = next(edge for edge in graph['edges'] if edge['id'] == 'edge:rest:get')
        supported['properties']['architecture_claims'] = [
            {'claim_id': 'call', 'investigation_status': 'SUPPORTED', 'family': 'api'},
            {'claim_id': 'deployment', 'investigation_status': 'CONFLICTED', 'family': 'api'}]
        graph['nodes'][0]['properties']['architecture_subjects'] = [
            {'id': 'shell', 'label': 'Portal shell', 'role': 'SHELL', 'layer_id': 'shell-layer',
             'layer_label': 'Shell', 'layer_order': 2}]
        model = build_viewer_model(graph)
        link = next(row for row in model['system_links'] if 'edge:external' in row['edge_ids'])
        self.assertEqual((link['level'], link['status'], link['assessment']), ('highest', 'unresolved', 'UNVERIFIED'))
        mixed = next(row for row in model['system_links'] if 'edge:rest:get' in row['edge_ids'])
        self.assertEqual(mixed['assessments'], ['CONFLICTED', 'SUPPORTED'])
        self.assertEqual(mixed['edge_ids'], ['edge:rest:get'])
        self.assertEqual(supported['resolution_status'], 'RESOLVED')
        self.assertEqual(model['nodes']['application:client']['architecture_layer']['order'], 2)
        self.assertEqual(model['nodes']['application:client']['label'], 'Portal shell')

    def test_system_link_aggregation_preserves_all_canonical_edges_and_evidence(self):
        before = deepcopy(self.graph)
        model = build_viewer_model(self.graph)
        canonical = {edge["id"]: edge for edge in self.graph["edges"]}
        matching = [link for link in model["system_links"]
                    if {"edge:rest:get", "edge:rest:list"} <= set(link["edge_ids"])]
        self.assertEqual(len(matching), 1)
        aggregated = matching[0]
        self.assertEqual(aggregated["source"], "application:client")
        self.assertEqual(aggregated["target"], "service:orders")
        self.assertEqual(aggregated["count"], len(aggregated["edge_ids"]))
        self.assertEqual(set(aggregated["evidence"]),
                         {ref for identifier in aggregated["edge_ids"] for ref in canonical[identifier]["evidence"]})
        self.assertEqual(aggregated["label"], "API calls")
        module = next(link for link in model["system_links"] if "edge:module" in link["edge_ids"])
        self.assertIn("module", module["label"].lower())
        reads = next(link for link in model["system_links"] if "edge:reads" in link["edge_ids"])
        self.assertEqual(reads["label"], "Reads data")
        self.assertEqual(self.graph, before)

    def test_unknown_candidates_and_ambiguous_links_never_become_confirmed_system_connections(self):
        model = build_viewer_model(self.graph)
        for identifier, status in (("edge:external", "unresolved"), ("edge:candidate", "candidate"),
                                   ("edge:ambiguous", "ambiguous")):
            with self.subTest(edge=identifier):
                self.assertEqual(model["edges"][identifier]["status"], status)
                links = [link for link in model["system_links"] if identifier in link["edge_ids"]]
                self.assertTrue(links)
                self.assertTrue(all(link["status"] == status and link["level"] != "highest" for link in links))
        unknown = next(link for link in model["system_links"] if "edge:external" in link["edge_ids"])
        self.assertEqual(unknown["target"], "external:orders")
        self.assertIsNone(unknown["target_repository"])

    def test_connection_labels_distinguish_protocols_shared_modules_and_build_packages(self):
        model = build_viewer_model(self.graph)
        for identifier, family, label in (("edge:rest:get", "api", "REST"),
                                          ("edge:graphql", "api", "GraphQL"),
                                          ("edge:reads", "data", "read"),
                                          ("edge:module", "shared", "module"),
                                          ("edge:package", "package", "build")):
            with self.subTest(edge=identifier):
                metadata = model["edges"][identifier]
                self.assertEqual(metadata["family"], family)
                self.assertIn(label.lower(), metadata["label"].lower())
        self.assertEqual(model["edges"]["edge:contains"]["family"], "structure")
        self.assertEqual(model["edges"]["edge:contains"]["level"], "context")

    def test_configuration_columns_and_typed_component_dependencies_remain_distinct(self):
        graph = graph_fixture()
        for kind in ("CONFIGURATION_KEY", "CONFIGURATION_SOURCE", "COLUMN", "ENTITY", "JAVA_TYPE"):
            graph["nodes"].append({"id": kind, "type": kind, "name": kind, "repository": "repo:orders"})
        expected = {"READS_CONFIG": ("CONFIGURATION_KEY", "configuration"),
                    "BINDS_CONFIG": ("CONFIGURATION_SOURCE", "configuration"),
                    "REFERENCES_COLUMN": ("COLUMN", "data"), "USES_ENTITY": ("ENTITY", "data"),
                    "CALLS_COMPONENT": ("JAVA_TYPE", "shared"), "INJECTS": ("JAVA_TYPE", "shared"),
                    "DEPENDS_ON_TYPE": ("JAVA_TYPE", "shared")}
        for relation, (target, _) in expected.items():
            graph["edges"].append({"id": relation, "source": "service:orders", "target": target,
                                   "relationship": relation, "dimension": "RUNTIME", "assertion_status": "CONFIRMED"})
        model = build_viewer_model(graph)
        for relation, (_, family) in expected.items():
            self.assertEqual(model["edges"][relation]["family"], family)
        self.assertEqual(model["nodes"]["COLUMN"]["family"], "data")
        self.assertEqual(model["nodes"]["CONFIGURATION_KEY"]["family"], "configuration")

    def test_service_graph_collapses_calls_and_keeps_internal_details_outside_canvas(self):
        before = deepcopy(self.graph)
        projection = build_viewer_model(self.graph)['service_graph']
        link = next(row for row in projection['links']
                    if row['source'] == 'application:client' and row['target'] == 'service:orders')
        self.assertEqual(set(link['edge_ids']), {'edge:rest:get', 'edge:rest:list', 'edge:graphql', 'edge:candidate'})
        self.assertEqual(link['status'], 'mixed')
        self.assertEqual(set(link['statuses']), {'resolved', 'candidate'})
        self.assertEqual(sum(row['count'] for row in link['facets']), link['count'])
        self.assertNotIn('component:client:call', projection['nodes'])
        self.assertNotIn('operation:orders:get', projection['nodes'])
        self.assertNotIn('table:orders', projection['nodes'])
        self.assertNotIn('external:package', projection['nodes'])
        self.assertGreater(projection['details']['application:client']['internal_edge_count'], 0)
        self.assertEqual(self.graph, before)

    def test_separate_services_in_one_repository_use_explicit_ownership(self):
        graph = deepcopy(self.graph)
        extra = deepcopy(next(row for row in graph['nodes'] if row['id'] == 'service:orders'))
        extra.update(id='service:second', name='Second service')
        graph['nodes'].append(extra)
        graph['edges'].append({'id':'edge:second-call', 'source':'service:orders', 'target':'service:second',
                               'relationship':'CALLS_SERVICE', 'dimension':'RUNTIME', 'evidence':[],
                               'assertion_status':'CONFIRMED', 'resolution_status':'RESOLVED'})
        projection = build_viewer_model(graph)['service_graph']
        self.assertTrue({'service:orders','service:second'} <= projection['nodes'].keys())
        call = next(row for row in projection['links'] if 'edge:second-call' in row['edge_ids'])
        self.assertEqual((call['source'],call['target']), ('service:orders','service:second'))
        self.assertNotIn('repo:orders',projection['repository_roots'])
        # Unowned operations cannot be assigned to the first root in a monorepo.
        self.assertFalse(any('edge:rest:list' in row['edge_ids'] for row in projection['links']))

    def test_unresolved_urls_are_destination_groups_without_provider_identity(self):
        graph = deepcopy(self.graph)
        for index in range(30):
            graph['nodes'].append({'id':f'url:{index}', 'type':'API_OPERATION','repository':None,
                                   'name':f'/different/{index}', 'properties':{'protocol':'REST','path':f'/different/{index}'}})
            graph['edges'].append({'id':f'call:{index}', 'source':'application:client','target':f'url:{index}',
                                   'relationship':'CALLS_REST','dimension':'RUNTIME','evidence':[],
                                   'assertion_status':'CONFIRMED','resolution_status':'UNRESOLVED'})
        projection = build_viewer_model(graph)['service_graph']
        groups = [row for row in projection['nodes'].values() if row.get('display_kind') == 'Destination group']
        self.assertEqual(len(groups),1)
        self.assertIn('No shared provider',groups[0]['provider_limit'])
        call = next(row for row in projection['links'] if row['target'] == groups[0]['id'])
        self.assertEqual((call['status'],call['count']),('unresolved',30))

    def test_large_repository_set_uses_service_nodes_and_pair_lines(self):
        graph = deepcopy(self.graph)
        for index in range(97):
            name = f'ui-{index}' if index < 9 else f'service-{index}'
            kind = 'WEB' if index < 9 else 'SPRING'
            repository = 'repo:' + name
            root = ('application:' if kind == 'WEB' else 'service:') + name
            graph['repositories'].append({'id':repository,'name':name,'path':'repos/'+name,
                                          'kind':kind,'role':'APPLICATION','visible':True})
            graph['nodes'].append({'id':root,'type':'APPLICATION' if kind == 'WEB' else 'SERVICE','name':name,
                                   'repository':repository,'dimensions':['RUNTIME'],'properties':{}})
            previous = 'application:client' if index == 0 else ('application:ui-'+str(index-1) if index < 10 else 'service-'+str(index-1))
            previous = previous if previous.startswith(('application:','service:')) else 'service:'+previous
            graph['edges'].append({'id':f'edge:service:{index}','source':root,'target':previous,
                                   'relationship':'CALLS_SERVICE','dimension':'RUNTIME','evidence':[],
                                   'assertion_status':'CONFIRMED','resolution_status':'RESOLVED'})
            for component in range(12):
                component_id=f'component:{name}:{component}'
                graph['nodes'].append({'id':component_id,'type':'COMPONENT','name':component_id,
                                       'repository':repository,'dimensions':['RUNTIME'],'properties':{}})
                graph['edges'].append({'id':f'edge:internal:{index}:{component}','source':root,'target':component_id,
                                       'relationship':'USES_COMPONENT','dimension':'RUNTIME','evidence':[],
                                       'assertion_status':'CONFIRMED'})
        projection = build_viewer_model(graph)['service_graph']
        local_nodes = [row for row in projection['nodes'].values() if row.get('repository')]
        self.assertEqual(len(projection['repository_roots']),100)
        self.assertEqual(len(local_nodes),100)
        self.assertTrue(all(row.get('display_node') for row in local_nodes))
        self.assertFalse(any(row['id'].startswith('component:') for row in projection['nodes'].values()))
        self.assertLessEqual(len(projection['links']),100)
        self.assertTrue(any(row['count'] > 1 for row in projection['links']))


def read_chunk(path):
    import base64
    import gzip
    import re
    text = path.read_text(encoding='utf-8')
    match = re.fullmatch(r'window.serviceGraphChunk\(("[^"\n]+"),("[^"\n]+")\);\n', text)
    if not match:
        raise AssertionError('Invalid local chunk: ' + str(path))
    return json.loads(match[1]), json.loads(gzip.decompress(base64.b64decode(json.loads(match[2]))))


def logical_chunks(folder):
    return {key: value for path in folder.glob('bucket-*.js')
            for key, value in read_chunk(path)[1].items()}


class GraphViewerRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render_graph = staticmethod(load_tool('render_graph').main)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='service-viewer-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / 'relationship-viewer.html'

    def render(self, graph=None):
        graph = graph or graph_fixture()
        source = self.root / 'graph.json'
        source.write_text(json.dumps(graph), encoding='utf-8')
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.render_graph([str(source), '--output', str(self.output)]), 0)
        self.html = self.output.read_text(encoding='utf-8')
        parser = ScriptCollector()
        parser.feed(self.html)
        self.parser = parser
        self.bootstrap = json.loads(next(row['text'] for row in parser.scripts
                                         if row['attributes'].get('id') == 'bootstrap-data'))
        self.data = self.output.with_suffix('.data')
        return self.bootstrap

    def interactions(self, mode='progressive'):
        node = shutil.which('node')
        self.assertIsNotNone(node, 'Node.js is required for supported viewer interactions.')
        result = subprocess.run([node, str(Path(__file__).with_name('viewer_interactions.cjs')),
                                 str(self.output), mode], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_overview_keeps_repository_inventory_and_plots_only_service_nodes(self):
        graph = graph_fixture()
        graph['repositories'].append({'id':'repo:inventory','name':'Inventory','kind':'SOURCE_ONLY','visible':True})
        graph['nodes'].append({'id':'inventory:anchor','name':'Inventory anchor','type':'COMPONENT',
                               'repository':'repo:inventory','dimensions':['RUNTIME']})
        bootstrap = self.render(graph)
        self.assertEqual({row['id'] for row in bootstrap['repositories']}, {row['id'] for row in graph['repositories']})
        self.assertNotIn('repo:inventory',bootstrap['roots'])
        self.assertEqual(len(bootstrap['nodes']),3)
        roots = set(bootstrap['roots'].values())
        self.assertTrue(all(row['source'] in roots and row['target'] in roots for row in bootstrap['links']))
        self.assertTrue(all('edge_ids' not in row and 'evidence' not in row for row in bootstrap['links']))
        self.assertEqual(graph['nodes'][-1]['id'], 'inventory:anchor')

    def test_canonical_records_round_trip_once_and_untrusted_source_stays_inert(self):
        graph = graph_fixture()
        marker = '</script><script id="injected">unsafe()</script> __BOOTSTRAP__\u2028\u2029\u0085'
        graph['nodes'][0]['name'] = marker
        graph['evidence'][0]['declaration'] = marker
        self.render(graph)
        self.assertNotIn('injected', self.parser.ids)
        for kind in ('nodes','edges','evidence'):
            rows = [row for key, batch in logical_chunks(self.data).items() if key.startswith(kind+'-') for row in batch]
            for row in rows:
                row.pop('evidence_chunks', None)
            self.assertEqual(sorted(rows,key=lambda row:row['id']), sorted(graph[kind],key=lambda row:row['id']))
        data=logical_chunks(self.data)
        for kind in ('node','edge'):
            ids=[row['id'] for key, rows in data.items() if key.startswith(kind+'-index-') for row in rows]
            self.assertEqual(len(ids),len(set(ids)))
            self.assertEqual(set(ids),{row['id'] for row in graph[kind+'s']})
        neighborhoods=[value for value in data.values() if isinstance(value,dict) and 'node_refs' in value]
        self.assertTrue(neighborhoods)
        self.assertTrue(all(row.get('service_link') for value in neighborhoods for row in value['edges']))
        self.assertFalse(any(row.get('navigation') for value in neighborhoods for row in value['edges']))
        service_nodes={row['id'] for key, batch in data.items() if key.startswith('service-index-') for row in batch}
        self.assertTrue(all(ref['id'] in service_nodes for value in neighborhoods for ref in value['node_refs']))
        self.assertEqual(next(row for row in self.bootstrap['nodes'] if row['id']=='application:client')['name'], marker)
        self.assertNotIn('</script><script id="injected">', self.html)

    def test_html_does_not_grow_with_evidence_and_data_is_compressed(self):
        small = graph_fixture()
        self.render(small)
        small_bytes = self.output.stat().st_size
        graph = deepcopy(small)
        graph['evidence'] = [{'id':f'ev:{index}', 'repository':None, 'path':'fixture.txt', 'line':index+1,
                              'declaration':'large source declaration '*200, 'extractor':'fixture', 'directness':'DIRECT'}
                             for index in range(900)]
        for edge in graph['edges']:
            edge['evidence'] = []
        self.render(graph)
        self.assertEqual(self.output.stat().st_size, small_bytes)
        self.assertLess(self.output.stat().st_size, 100_000)
        self.assertLess(sum(path.stat().st_size for path in self.data.glob('bucket-*.js')), 150_000)
        self.assertNotIn('large source declaration', self.html)

    def test_card_and_indexes_preserve_all_dependencies_without_plotting_isolated_components(self):
        graph = graph_fixture()
        sample = deepcopy(graph['nodes'][1])
        for index in range(47):
            graph['nodes'].append({**sample,'id':f'isolated:{index}','name':f'Isolated {index}'})
        self.render(graph)
        result = self.interactions('complete')
        self.assertEqual(result['canonical_nodes'],len(graph['nodes']))
        self.assertEqual(result['canonical_edges'],len(graph['edges']))
        self.assertTrue(result['only_service_nodes'])
        self.assertGreater(result['batches'],1)

    def test_progressive_graph_keeps_overview_deduplicates_loads_and_collapses_branches(self):
        self.render()
        result=self.interactions()
        self.assertTrue(result['same_graph'])
        self.assertTrue(result['focused_connections'])
        self.assertTrue(result['collapsed'])
        self.assertTrue(result['deduplicated_requests'])

    def test_hundred_repository_hub_expands_in_bounded_service_batches(self):
        bootstrap = self.render(scale_fixture())
        self.assertEqual(len(bootstrap['repositories']),100)
        self.assertEqual(len(bootstrap['nodes']),95)
        self.assertLess(self.output.stat().st_size,400_000)
        result = self.interactions('scale')
        self.assertTrue(result['bounded_focus'])
        self.assertTrue(result['more_adds_peers'])
        self.assertTrue(result['stable_layout'])

    def test_failure_is_retryable_and_does_not_leave_loading_or_expansion_stuck(self):
        self.render()
        result=self.interactions('recovery')
        self.assertTrue(result['retry_succeeded'])
        self.assertTrue(result['loading_cleared'])

    def test_filters_and_source_inspection_keep_status_and_redact_properties(self):
        graph=graph_fixture()
        edge=next(row for row in graph['edges'] if row['id']=='edge:external')
        edge['properties']={'secret':'DO_NOT_DISPLAY','resolution_rule':'fixture rule'}
        self.render(graph)
        result=self.interactions('inspection')
        self.assertTrue(result['unresolved_preserved'])
        self.assertTrue(result['source_evidence'])
        self.assertTrue(result['redacted'])

    def test_compact_layout_removes_graph_pagination_and_collapses_help(self):
        self.render()
        self.assertNotIn('Inspect unresolved',self.html)
        self.assertNotIn('Next diagram',self.html)
        self.assertNotIn('Previous diagram',self.html)
        self.assertEqual(self.html.count('<h1>'),1)
        elements={attrs['id']:attrs for _,attrs in self.parser.elements if attrs.get('id')}
        self.assertNotIn('open',elements['overview'])
        self.assertNotIn('open',elements['legend'])
        self.assertTrue({'graph','fit','collapse','scope','status','family','index-panel'}<=elements.keys())
        self.assertIn('overflow:hidden',self.html)

    def test_trace_streaming_preserves_existing_method_scopes_without_retaining_all_traces(self):
        graph=graph_fixture()
        tool=load_tool('viewer_traces')
        expected=tool.build_trace_model(graph)
        actual=[]
        streamed=tool.build_trace_model(graph,trace_sink=actual.append)
        self.assertEqual({row['id']:row for row in actual},expected['traces'])
        self.assertEqual(streamed['traces'],{})
        self.assertEqual(streamed['trace_index']['counts'],expected['trace_index']['counts'])
        self.render(graph)
        data=logical_chunks(self.data)
        index=data['trace-index']
        for identifier,key in index.items():
            self.assertEqual(data[key],expected['traces'][identifier])
        self.assertNotIn('selected_call_sites',self.html.split('<script>')[0])

    def test_failed_renderer_preserves_previous_html_and_bucket_bytes(self):
        graph=graph_fixture()
        self.render(graph)
        before={path.name:path.read_bytes() for path in self.data.glob('*.js')}
        html=self.output.read_bytes()
        graph['edges'][0]['target']='missing-provider-node'
        (self.root/'graph.json').write_text(json.dumps(graph))
        with self.assertRaises(KeyError), redirect_stdout(io.StringIO()):
            self.render_graph([str(self.root/'graph.json'),'--output',str(self.output)])
        self.assertEqual(self.output.read_bytes(),html)
        self.assertEqual({path.name:path.read_bytes() for path in self.data.glob('*.js')},before)

    def test_renderer_rejects_foreign_data_without_overwriting_it(self):
        self.render()
        protected=self.data/'keep.txt'
        protected.write_text('Unrelated user content')
        with self.assertRaisesRegex(ValueError,'generated data buckets'), redirect_stdout(io.StringIO()):
            self.render_graph([str(self.root/'graph.json'),'--output',str(self.output)])
        self.assertEqual(protected.read_text(),'Unrelated user content')

    def test_invalid_template_shows_recovery_message(self):
        self.output.write_text((Path(__file__).parents[1]/'tools/viewer.html').read_text())
        result=self.interactions('template-error')
        self.assertTrue(result['visible_recovery'])


if __name__ == '__main__':
    unittest.main()
