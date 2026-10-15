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


class GraphViewerRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render_graph = staticmethod(load_tool("render_graph").main)

    def test_script_payload_round_trip_preserves_untrusted_names_without_creating_script_elements(self):
        graph = graph_fixture()
        marker = '</script><script id="injected">alert("fixture")</script> __GRAPH__ __VIEWER__ __SOURCE_PREFIX__'
        graph["nodes"][0]["name"] = marker
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-viewer-") as temporary:
            root = Path(temporary)
            source, output = root / "graph.json", root / "viewer.html"
            source.write_text(json.dumps(graph), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                result = self.render_graph([str(source), "--output", str(output), "--source-prefix",
                                            '</script><script id="prefix-injected">alert("fixture")</script>'])
            self.assertEqual(result, 0)
            parser = ScriptCollector()
            parser.feed(output.read_text(encoding="utf-8"))
        self.assertNotIn("injected", parser.ids)
        self.assertNotIn("prefix-injected", parser.ids)
        payloads = {script["attributes"].get("id"): json.loads(script["text"])
                    for script in parser.scripts if script["attributes"].get("type") == "application/json"}
        self.assertEqual(payloads["graph-data"], graph)
        self.assertEqual(payloads["viewer-data"], build_viewer_model(graph))

    def test_viewer_exposes_priority_filters_legend_and_an_accessible_relationship_table(self):
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-viewer-") as temporary:
            root = Path(temporary)
            source, output = root / "graph.json", root / "viewer.html"
            source.write_text(json.dumps(graph_fixture()), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.render_graph([str(source), "--output", str(output)])
            parser = ScriptCollector()
            parser.feed(output.read_text(encoding="utf-8"))
        self.assertTrue({"priority", "scope", "status", "boundary", "relationship", "search", "sort"} <= parser.ids)
        self.assertTrue({"highest", "medium", "low"} <= {
            attributes.get("data-level") for tag, attributes in parser.elements if tag == "button"})
        self.assertTrue({"all", "resolved", "declared", "unresolved", "ambiguous", "candidate"} <= {
            attributes.get("value") for tag, attributes in parser.elements if tag == "option"})
        self.assertTrue({"api", "data", "shared", "package"} <= {
            attributes.get("value") for tag, attributes in parser.elements
            if tag == "input" and attributes.get("name") == "family"})
        self.assertTrue(any(tag == "svg" and attributes.get("aria-label")
                            for tag, attributes in parser.elements))
        self.assertTrue(any(tag == "table" and (attributes.get("aria-label") or attributes.get("aria-labelledby"))
                            for tag, attributes in parser.elements))

    def test_shipped_script_filters_unknown_providers_and_lists_every_package_across_pages(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js is unavailable for the isolated JavaScript interaction check.")
        graph = graph_fixture()
        external = deepcopy(next(item for item in graph["nodes"] if item["id"] == "external:orders"))
        external.update(id="external:graphql", name="GraphQL endpoint")
        external["properties"] = {"protocol": "GRAPHQL"}
        graph["nodes"].append(external)
        edge = deepcopy(next(item for item in graph["edges"] if item["id"] == "edge:external"))
        edge.update(id="edge:graphql:external", target="external:graphql", relationship="CALLS_GRAPHQL")
        graph["edges"].append(edge)
        package = next(item for item in graph["nodes"] if item["id"] == "external:package")
        dependency = next(item for item in graph["edges"] if item["id"] == "edge:package")
        for index in range(31):
            target = deepcopy(package)
            target.update(id=f"external:package:{index}", name=f"npm:fixture-{index}")
            graph["nodes"].append(target)
            edge = deepcopy(dependency)
            edge.update(id=f"edge:package:{index}", target=target["id"])
            graph["edges"].append(edge)
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-viewer-") as temporary:
            root = Path(temporary)
            source, output = root / "graph.json", root / "viewer.html"
            source.write_text(json.dumps(graph), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.render_graph([str(source), "--output", str(output)])
            result = subprocess.run([node, str(Path(__file__).with_name("viewer_interactions.cjs")), str(output)],
                                    capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = json.loads(result.stdout)
        self.assertEqual(result["package_relationships"], 32)
        self.assertEqual(result["pages"], 2)
        self.assertEqual(len(result["checks"]), 8)

    def test_complete_indexes_diagram_pages_repository_slices_and_isolated_node_focus(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js is unavailable for the isolated JavaScript interaction check.")
        graph = graph_fixture()
        sample = deepcopy(graph["nodes"][1])

        def add_node(identifier, kind, name, **extra):
            item = deepcopy(sample)
            item.update(id=identifier, type=kind, name=name, repository="repo:orders", **extra)
            graph["nodes"].append(item)

        def add_edge(identifier, source, target, relation, **extra):
            graph["edges"].append({"id": identifier, "source": source, "target": target,
                                   "relationship": relation, "dimension": "RUNTIME", "evidence": ["ev:get"],
                                   "assertion_status": "CONFIRMED", **extra})

        add_node("component:orders:handler", "COMPONENT", "OrdersHandler", component_kind="CONTROLLER",
                 business_meaning="Handles order creation", source_paths=["repos/orders/OrdersHandler.java"],
                 properties={"layer": "entrypoint", "client_secret": "fixture-secret"})
        for index in range(60):
            operation = f"operation:detail:{index}"
            add_node(operation, "API_OPERATION", f"GET /detail/{index}", properties={"protocol": "REST"})
            add_edge(f"edge:exposes:{index}", "service:orders", operation, "EXPOSES")
            add_edge(f"edge:invokes:{index}", operation, "component:orders:handler", "INVOKES")
        tables = ["table:orders"]
        for index in range(6):
            identifier = f"table:detail:{index}"
            tables.append(identifier)
            add_node(identifier, "TABLE", f"detail_table_{index}", properties={"access": "READ"})
        for index in range(7):
            add_edge(f"edge:read:{index}", "component:orders:handler", tables[index], "READS")
        add_node("column:orders:id", "COLUMN", "orders.id", properties={"column": "id"})
        add_node("entity:orders", "ENTITY", "OrderEntity")
        add_edge("edge:column", "entity:orders", "column:orders:id", "MAPS_TO_COLUMN")
        add_node("config:orders", "CONFIGURATION_KEY", "orders.timeout", properties={"key": "orders.timeout", "value": "fixture-value"})
        add_edge("edge:config", "component:orders:handler", "config:orders", "READS_CONFIG")
        add_node("topic:orders", "MESSAGE_CHANNEL", "orders.events", properties={"protocol": "KAFKA"})
        add_edge("edge:publish", "component:orders:handler", "topic:orders", "PUBLISHES")
        add_node("component:orders:isolated", "COMPONENT", "IsolatedOrdersUtility")
        add_node("capability:orders", "BUSINESS_CAPABILITY", "Order placement", dimensions=["BUSINESS"])
        add_edge("edge:business", "service:orders", "capability:orders", "IMPLEMENTS",
                 dimension="BUSINESS", assertion_status="INFERRED")
        add_edge("edge:class", "service:orders", "component:orders:handler", "CONTAINS_COMPONENT",
                 assertion_status="INFERRED")
        graph['repositories'].append({**graph['repositories'][0], 'id': 'repo:testing', 'name': 'testing',
                                      'path': 'repos/testing', 'kind': 'TESTING'})
        for identifier, kind, source_path in [('component:testing:root', 'COMPONENT', 'repos/testing'),
                                               ('operation:testing', 'API_OPERATION', 'repos/testing/client.py'),
                                               ('component:testing:resource', 'COMPONENT', 'repos/testing/common.resource')]:
            graph['nodes'].append({**deepcopy(sample), 'id': identifier, 'type': kind, 'name': identifier,
                                   'repository': 'repo:testing', 'component_kind': 'TESTING',
                                   'source_paths': [source_path], 'properties': {'dependency_scope': 'TESTING'}})
        add_edge('edge:testing:http', 'component:testing:root', 'operation:testing', 'CALLS_REST',
                 resolution_status='UNRESOLVED', properties={'dependency_scope': 'TESTING'})
        add_edge('edge:testing:resource', 'component:testing:root', 'component:testing:resource',
                 'IMPORTS_TEST_RESOURCE', resolution_status='RESOLVED', properties={'dependency_scope': 'TESTING'})
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-viewer-recovery-") as temporary:
            root = Path(temporary)
            source, output = root / "graph.json", root / "viewer.html"
            source.write_text(json.dumps(graph), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.render_graph([str(source), "--output", str(output)])
            result = subprocess.run([node, str(Path(__file__).with_name("viewer_interactions.cjs")),
                                     str(output), "recovery"], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = json.loads(result.stdout)
        self.assertGreater(result["diagram_pages"], 1)
        self.assertEqual(result["storage_tables"], 7)
        self.assertEqual(result["storage_reads"], 8)
        self.assertEqual(len(result["checks"]), 8)


if __name__ == "__main__":
    unittest.main()
