"""Check standalone graph adoption and its source evidence boundaries."""

from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml

import runpy

load_tool = runpy.run_path(str(Path(__file__).with_name("_support.py")))["load_tool"]
build_graph = load_tool("build_graph")
generate_all_graphs = load_tool("generate_all_graphs")
inventory = load_tool("repository_inventory").inventory
validate = load_tool("validate_graph").validate
validate_dependencies = load_tool("validate_graph").validate_dependencies

try:
    from ai_sdlc_workbench.relationships.skill import load_graph_tool
    from ai_sdlc_workbench.runtime import Workbench
    from ai_sdlc_workbench.workspace import initialize_workspace, scaffold_root
except ImportError:
    Workbench = None


@unittest.skipUnless(Workbench is not None, "Workbench adapter integration requires its installed package.")
class ServiceGraphTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-graph-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        initialize_workspace(self.root)
        (self.root / "repos").mkdir(exist_ok=True)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def web(self, relative, name):
        self.write(f"{relative}/package.json", json.dumps({"name": name}))
        self.write(f"{relative}/src/index.ts", "export const ready = true;\n")
        return self.root / relative

    def spring(self, relative, name):
        self.write(f"{relative}/pom.xml", f"""<project>
  <modelVersion>4.0.0</modelVersion><groupId>fixture</groupId>
  <artifactId>{name}</artifactId><version>1.0</version>
</project>
""")
        self.write(f"{relative}/src/main/java/Controller.java", """
@RestController @RequestMapping("/v1/orders") class Controller {
    @GetMapping("/{id}") Object get() { return null; }
}
""")
        self.write(f"{relative}/src/main/resources/application.yml",
                   f"spring:\n  application:\n    name: {name}\n")
        return self.root / relative

    def build(self, output=None):
        output = output or self.root / ".workbench/graph"
        with redirect_stdout(io.StringIO()):
            result = build_graph.main([
                "--workspace", str(self.root), "--repos", str(self.root / "repos"), "--out", str(output)])
        self.assertEqual(result, 0)
        return output, json.loads((output / "graph.json").read_text(encoding="utf-8"))

    def graph_workbench(self, output, grants):
        self.write("registry/tools.yaml", yaml.safe_dump({"schema_version": 1, "tools": [{
            "id": "graph", "kind": "dependency_graph", "provider": "graph.snapshot", "environment": "local",
            "config": {"path": str(output.relative_to(self.root))}, "allowed_operations": grants}]}))
        return Workbench(self.root)

    def test_grouped_repository_inventory_scans_leaves_and_retains_unknown_inputs(self):
        self.web("repos/ui/client-one", "@fixture/client-one")
        self.web("repos/ui/client-two", "@fixture/client-two")
        self.spring("repos/services/auth-server", "auth-server")
        self.write("repos/infra/nginx/nginx.conf", "server { listen 80; }\n")
        self.write("repos/services/unknown/README.md", "Unsupported input.\n")
        rows = {row["name"]: row for row in inventory(self.root, self.root / "repos")["repositories"]}
        self.assertEqual(set(rows), {"client-one", "client-two", "auth-server", "nginx", "unknown"})
        self.assertEqual({name: row["kind"] for name, row in rows.items()}, {
            "client-one": "WEB", "client-two": "WEB", "auth-server": "SPRING",
            "nginx": "INFRA", "unknown": None})
        self.assertEqual(rows["client-one"]["path"], "repos/ui/client-one")
        self.assertEqual(rows["unknown"]["status"], "UNSUPPORTED")
        self.assertTrue(all(rows[name]["content_sha256"] for name in rows))

    def test_non_git_source_snapshot_does_not_inherit_workspace_revision(self):
        repository = self.web("repos/ui/client", "@fixture/client")
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        for arguments in (["git", "init", "-q", "-b", "main"],
                          ["git", "-c", "user.name=Test Fixture", "-c", "user.email=fixture@example.invalid",
                           "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-q", "-m", "Fixture"]):
            subprocess.run(arguments, cwd=self.root, env=environment,
                           check=True, capture_output=True, timeout=15)
        graph = build_graph.Graph(self.root)
        graph.add_repository(repository, "WEB", True)
        self.assertIsNone(graph.repositories[0]["commit"])
        self.assertIsNone(graph.repositories[0]["ref"])
        row = inventory(self.root, self.root / "repos")["repositories"][0]
        self.assertTrue(any("independent Git" in item for item in row["limitations"]))

    def test_missing_declared_repository_remains_visible_in_coverage(self):
        self.web("repos/ui/client", "@fixture/client")
        self.write("repos/manifest.json", json.dumps({"repositories": [
            {"path": "repos/services/absent", "name": "absent"}]}))
        output, graph = self.build()
        coverage = json.loads((output / "analysis-coverage.json").read_text(encoding="utf-8"))
        missing = [row for row in coverage["repositories"] if row["name"] == "absent"]
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]["status"], "MISSING")
        self.assertTrue(any(item["code"] == "MISSING_REPOSITORY" for item in graph["diagnostics"]))

    def test_duplicate_repository_basenames_are_rejected_before_graph_identity_merge(self):
        self.web("repos/ui/client", "@fixture/client")
        self.spring("repos/services/client", "different-service")
        with self.assertRaisesRegex(ValueError, "[Dd]uplicate|unique"):
            inventory(self.root, self.root / "repos")

    def test_maven_wrapper_package_does_not_hide_spring_controller_evidence(self):
        self.spring("repos/services/auth-server", "auth-server")
        self.write("repos/services/auth-server/package.json", json.dumps({
            "name": "auth-server-build-wrapper", "scripts": {"build": "mvn clean package"}}))
        output, graph = self.build()
        repository = next(row for row in graph["repositories"] if row["name"] == "auth-server")
        self.assertEqual(repository["kind"], "SPRING")
        self.assertTrue(any(node["type"] == "SERVICE" and node["repository"] == "repo:auth-server"
                            for node in graph["nodes"]))
        self.assertFalse(any(node["type"] == "APPLICATION" and node["repository"] == "repo:auth-server"
                             for node in graph["nodes"]))
        endpoints = [node for node in graph["nodes"] if node["type"] == "API_OPERATION"
                     and node["repository"] == "repo:auth-server"]
        self.assertTrue(any(node.get("properties", {}).get("path") == "/v1/orders/{id}" for node in endpoints))
        self.assertTrue(any(item["extractor"] == "spring-rest"
                            and item["path"] == "repos/services/auth-server/src/main/java/Controller.java"
                            for item in graph["evidence"]))
        coverage = json.loads((output / "analysis-coverage.json").read_text(encoding="utf-8"))
        self.assertEqual(coverage["repositories"][0]["status"], "PARTIAL")

    def test_static_module_import_retains_consumer_and_unique_package_provider_evidence(self):
        self.web("repos/ui/consumer", "@fixture/consumer")
        self.web("repos/ui/base", "@fixture/base")
        declaration = "import { ready } from '@fixture/base';"
        self.write("repos/ui/consumer/src/imports.ts", declaration + "\nconsole.log(ready);\n")
        output, graph = self.build()
        nodes = {node["id"]: node for node in graph["nodes"]}
        imports = [edge for edge in graph["edges"] if edge["relationship"] == "IMPORTS_MODULE"
                   and edge.get("resolution_status") == "RESOLVED"
                   and nodes[edge["source"]].get("repository") == "repo:consumer"
                   and nodes[edge["target"]].get("repository") == "repo:base"]
        self.assertEqual(len(imports), 1)
        self.assertEqual(imports[0]["assertion_status"], "CONFIRMED")
        self.assertEqual(imports[0]["properties"]["dependency_kind"], "MODULE")
        self.assertEqual(imports[0]["properties"]["module"], "@fixture/base")
        self.assertEqual(imports[0]["properties"]["resolution_rule"], "exact-npm-module-import")
        evidence = {item["id"]: item for item in graph["evidence"]}
        refs = [evidence[identifier] for identifier in imports[0]["evidence"]]
        self.assertTrue(any(item["path"] == "repos/ui/consumer/src/imports.ts"
                            and item["line"] == 1 and declaration in item["declaration"] for item in refs))
        self.assertTrue(any(item["path"] == "repos/ui/base/package.json" for item in refs))
        self.assertEqual(validate(graph, self.root), [])
        dependencies = json.loads((output / "dependencies.json").read_text(encoding="utf-8"))
        modules = dependencies["repositories"]["repo:consumer"]["modules"]
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0]["dependency_kind"], "MODULE")
        self.assertEqual(modules[0]["declared_modules"], ["@fixture/base"])
        self.assertEqual(validate_dependencies(dependencies, graph), [])

        generate_all_graphs.write_ai_outputs(output, self.root / "absent-descriptions.json")
        workbench = self.graph_workbench(output, ["search", "neighborhood"])
        searched = workbench.call("graph", "search", {"query": "base", "repository": "consumer", "limit": 100})
        self.assertEqual(searched["status"], "SUCCEEDED")
        matches = searched["result"]["matches"]
        self.assertTrue(matches)
        self.assertTrue(any(item["path"] == "repos/ui/consumer/src/imports.ts"
                            for match in matches for item in match["evidence"]))
        neighborhood = workbench.call("graph", "neighborhood", {"node_id": imports[0]["source"], "limit": 200})
        self.assertEqual(neighborhood["status"], "SUCCEEDED")
        result = neighborhood["result"]
        self.assertIn(imports[0], result["edges"])
        self.assertTrue(set(imports[0]["evidence"]) <= {item["id"] for item in result["evidence"]})
        self.assertEqual(result["snapshot"], searched["result"]["snapshot"])

    def test_duplicate_module_producers_remain_ambiguous(self):
        self.web("repos/ui/consumer", "@fixture/consumer")
        self.web("repos/ui/base-one", "@fixture/base")
        self.web("repos/ui/base-two", "@fixture/base")
        self.write("repos/ui/consumer/src/imports.ts", "import { ready } from '@fixture/base';\n")
        _, graph = self.build()
        imports = [edge for edge in graph["edges"] if edge["relationship"] == "IMPORTS_MODULE"]
        self.assertTrue(imports)
        self.assertFalse(any(edge.get("resolution_status") == "RESOLVED" for edge in imports))
        self.assertTrue(any(edge.get("resolution_status") == "AMBIGUOUS" for edge in imports))

    def test_type_only_module_import_does_not_create_a_confirmed_runtime_join(self):
        self.web("repos/ui/consumer", "@fixture/consumer")
        self.web("repos/ui/base", "@fixture/base")
        self.write("repos/ui/consumer/src/types.ts", """import type { Shape } from '@fixture/base';
import { type Metadata } from '@fixture/base';
export type { Shape } from '@fixture/base';
""")
        _, graph = self.build()
        imports = [edge for edge in graph["edges"] if edge["relationship"] == "IMPORTS_MODULE"]
        self.assertFalse(any(edge.get("resolution_status") == "RESOLVED"
                             and edge["assertion_status"] == "CONFIRMED" for edge in imports))

    def test_similar_package_name_does_not_establish_an_undeclared_module_alias(self):
        self.web("repos/ui/consumer", "@fixture/consumer")
        self.web("repos/ui/base-origin", "@fixture/base-origin")
        declaration = "import { ready } from '@fixture/base';"
        self.write("repos/ui/consumer/src/imports.ts", declaration + "\n")
        _, graph = self.build()
        imports = [edge for edge in graph["edges"] if edge["relationship"] == "IMPORTS_MODULE"]
        self.assertEqual(len(imports), 1)
        self.assertEqual(imports[0]["resolution_status"], "UNRESOLVED")
        self.assertEqual(imports[0]["properties"]["module"], "@fixture/base")
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertIsNone(nodes[imports[0]["target"]]["repository"])
        self.assertEqual(nodes[imports[0]["target"]]["name"], "@fixture/base")
        self.assertTrue(any(item["code"] == "UNRESOLVED_MODULE_PROVIDER"
                            and item["repository"] == "repo:consumer" for item in graph["diagnostics"]))
        evidence = {item["id"]: item for item in graph["evidence"]}
        self.assertTrue(any(evidence[identifier]["path"] == "repos/ui/consumer/src/imports.ts"
                            and declaration in evidence[identifier]["declaration"]
                            for identifier in imports[0]["evidence"]))

    def test_standalone_nginx_routes_resolve_http_with_both_source_repositories(self):
        self.web("repos/ui/client", "@fixture/client")
        self.write("repos/ui/client/src/call.ts", "fetch('/api/orders/42');\n")
        self.spring("repos/services/orders-service", "orders-service")
        self.write("repos/infra/nginx/nginx.conf", """upstream orders {
  server orders-service:8080;
}
server {
  location /api/orders/ {
    rewrite ^/api/orders/(.*)$ /v1/orders/$1 break;
    proxy_pass http://orders;
  }
}
""")
        output, graph = self.build()
        self.assertEqual({row["name"] for row in graph["repositories"]}, {"client", "orders-service", "nginx"})
        nodes = {node["id"]: node for node in graph["nodes"]}
        calls = [edge for edge in graph["edges"] if edge["relationship"] == "CALLS_REST"
                 and edge.get("resolution_status") == "RESOLVED"
                 and nodes[edge["source"]].get("repository") == "repo:client"
                 and nodes[edge["target"]].get("repository") == "repo:orders-service"]
        self.assertEqual(len(calls), 1)
        evidence = {item["id"]: item for item in graph["evidence"]}
        paths = {evidence[identifier]["path"] for identifier in calls[0]["evidence"]}
        self.assertIn("repos/ui/client/src/call.ts", paths)
        self.assertIn("repos/services/orders-service/src/main/java/Controller.java", paths)
        self.assertIn("repos/infra/nginx/nginx.conf", paths)
        proxy_calls = [edge for edge in graph["edges"] if edge["relationship"] == "CALLS_SERVICE"
                       and edge.get("resolution_status") == "RESOLVED"
                       and nodes[edge["source"]].get("repository") == "repo:nginx"
                       and nodes[edge["target"]].get("repository") == "repo:orders-service"]
        self.assertEqual(len(proxy_calls), 1)
        self.assertEqual(validate(graph, self.root), [])
        dependencies = json.loads((output / "dependencies.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_dependencies(dependencies, graph), [])

    def test_nginx_proxy_uri_replaces_the_location_prefix_and_preserves_the_suffix(self):
        self.web("repos/ui/client", "@fixture/client")
        self.write("repos/ui/client/src/call.ts", "fetch('/api/orders/42');\n")
        self.spring("repos/services/orders-service", "orders-service")
        for prefix, collection in (("/v1/orders/", "/v1/orders"), ("/", "")):
            with self.subTest(proxy_uri=prefix):
                self.write("repos/services/orders-service/src/main/java/Controller.java", f"""
@RestController @RequestMapping("{collection}") class Controller {{
    @GetMapping("/{{id}}") Object get() {{ return null; }}
    @GetMapping("") Object list() {{ return null; }}
}}
""")
                self.write("repos/infra/nginx/nginx.conf", f"""upstream orders {{
  server orders-service:8080;
}}
server {{
  location /api/orders/ {{
    proxy_pass http://orders{prefix};
  }}
}}
""")
                _, graph = self.build()
                nodes = {node["id"]: node for node in graph["nodes"]}
                calls = [edge for edge in graph["edges"] if edge["relationship"] == "CALLS_REST"
                         and edge.get("resolution_status") == "RESOLVED"
                         and nodes[edge["source"]].get("repository") == "repo:client"]
                self.assertEqual(len(calls), 1)
                self.assertEqual(nodes[calls[0]["target"]]["properties"]["path"], collection + "/{id}")
                routes = calls[0]["properties"]["gateway_routes"]
                self.assertTrue(any(route["rewritten_path"] == prefix + "42" for route in routes))

    def test_ip_only_nginx_upstream_does_not_establish_a_local_http_provider(self):
        self.web("repos/ui/client", "@fixture/client")
        self.write("repos/ui/client/src/call.ts", "fetch('/api/orders/42');\n")
        self.spring("repos/services/orders-service", "orders-service")
        self.write("repos/infra/nginx/nginx.conf", """upstream orders {
  server 10.0.0.1:8080;
}
server {
  location /api/orders/ {
    rewrite ^/api/orders/(.*)$ /v1/orders/$1 break;
    proxy_pass http://orders;
  }
}
""")
        _, graph = self.build()
        calls = [edge for edge in graph["edges"] if edge["relationship"] in {"CALLS_REST", "CALLS_SERVICE"}]
        self.assertTrue(calls)
        self.assertTrue(all(edge.get("resolution_status") != "RESOLVED" for edge in calls))

    def test_nginx_template_preserves_an_unresolved_diagnostic_without_service_joins(self):
        self.spring("repos/services/orders-service", "orders-service")
        self.write("repos/infra/nginx/templates/site.conf.j2", """server {
  location /api/orders/ {
    proxy_pass http://{{ orders_host }}:8080;
  }
}
""")
        output, graph = self.build()
        self.assertTrue(any(item["code"] == "UNRESOLVED_NGINX_TEMPLATE" for item in graph["diagnostics"]))
        self.assertFalse(any(edge["relationship"] == "CALLS_SERVICE"
                             and edge.get("resolution_status") == "RESOLVED" for edge in graph["edges"]))
        coverage = json.loads((output / "analysis-coverage.json").read_text(encoding="utf-8"))
        self.assertEqual(next(row for row in coverage["repositories"] if row["name"] == "nginx")["status"], "PARTIAL")

    def test_nginx_pool_with_multiple_servers_does_not_select_one_local_provider(self):
        self.web("repos/ui/client", "@fixture/client")
        self.write("repos/ui/client/src/call.ts", "fetch('/api/orders/42');\n")
        self.spring("repos/services/orders-service", "orders-service")
        self.spring("repos/services/payments-service", "payments-service")
        self.write("repos/infra/nginx/nginx.conf", """upstream orders-service {
  server orders-service:8080;
  server payments-service:8080;
}
server {
  location /api/orders/ {
    rewrite ^/api/orders/(.*)$ /v1/orders/$1 break;
    proxy_pass http://orders-service;
  }
}
""")
        _, graph = self.build()
        self.assertTrue(any(item["code"] == "UNRESOLVED_NGINX_UPSTREAM" for item in graph["diagnostics"]))
        calls = [edge for edge in graph["edges"] if edge["relationship"] in {"CALLS_REST", "CALLS_SERVICE"}]
        self.assertTrue(calls)
        self.assertFalse(any(edge.get("resolution_status") == "RESOLVED" for edge in calls))

    def test_empty_nginx_pool_does_not_borrow_a_server_from_the_next_pool(self):
        self.web("repos/ui/client", "@fixture/client")
        self.write("repos/ui/client/src/call.ts", "fetch('/api/orders/42');\n")
        self.spring("repos/services/orders-service", "orders-service")
        self.write("repos/infra/nginx/nginx.conf", """upstream orders-service {
}
upstream another-pool {
  server orders-service:8080;
}
server {
  location /api/orders/ {
    rewrite ^/api/orders/(.*)$ /v1/orders/$1 break;
    proxy_pass http://orders-service;
  }
}
""")
        _, graph = self.build()
        self.assertTrue(any(item["code"] == "UNRESOLVED_NGINX_UPSTREAM" for item in graph["diagnostics"]))
        calls = [edge for edge in graph["edges"] if edge["relationship"] in {"CALLS_REST", "CALLS_SERVICE"}]
        self.assertTrue(calls)
        self.assertFalse(any(edge.get("resolution_status") == "RESOLVED" for edge in calls))

    def test_failed_validation_preserves_every_published_snapshot_byte(self):
        self.web("repos/ui/client", "@fixture/client")
        output = self.root / ".workbench/published"
        self.build(output)
        generate_all_graphs.write_ai_outputs(output, self.root / "absent-descriptions.json")
        (output / "retained.bin").write_bytes(b"Retained snapshot\x00\xff")
        before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
        self.write("repos/ui/client/src/new.ts", "fetch('/new-boundary');\n")
        validation_seen = []

        def fail_validation(*parts, **kwargs):
            if any(str(part).endswith("validate_graph") for part in parts):
                validation_seen.append(True)
                raise subprocess.CalledProcessError(1, [str(part) for part in parts])
            return subprocess.run([str(part) for part in parts], cwd=kwargs["workspace"],
                                  check=True, capture_output=True, timeout=30)

        with patch.object(generate_all_graphs, "run", side_effect=fail_validation), redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError):
                generate_all_graphs.main(["--workspace", str(self.root), "--out", str(output)])
        self.assertEqual(validation_seen, [True])
        after = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
        self.assertEqual(after, before)

    def test_graph_queries_reject_changed_artifacts_and_retain_the_failed_action(self):
        self.web("repos/ui/client", "@fixture/client")
        output, _ = self.build()
        generate_all_graphs.write_ai_outputs(output, self.root / "absent-descriptions.json")
        workbench = self.graph_workbench(output, ["coverage"])
        accepted = workbench.call("graph", "coverage")
        self.assertEqual(accepted["status"], "SUCCEEDED")
        self.assertIn("graph_sha256", accepted["result"]["snapshot"])
        coverage = output / "analysis-coverage.json"
        coverage.write_bytes(coverage.read_bytes() + b"\n")
        rejected = workbench.call("graph", "coverage")
        self.assertEqual(rejected["status"], "FAILED")
        self.assertEqual(rejected["result"]["code"], "INVALID_SNAPSHOT")
        self.assertEqual(workbench.run(rejected["id"])["result"], rejected["result"])

    def test_query_uses_verified_bytes_when_published_files_change_after_bundle_validation(self):
        self.web("repos/ui/client", "@fixture/client")
        output, _ = self.build()
        generate_all_graphs.write_ai_outputs(output, self.root / "absent-descriptions.json")
        workbench = self.graph_workbench(output, ["services"])
        expected = json.loads((output / "services.json").read_text(encoding="utf-8"))
        manifest_sha256 = hashlib.sha256((output / "manifest.json").read_bytes()).hexdigest()
        snapshot = load_graph_tool("snapshot", self.root)
        original_bundle = snapshot._bundle
        replacements = []

        def replace_files_after_verification(root):
            verified = original_bundle(root)
            (root / "services.json").write_text('{"services": [{"id": "repo:unverified"}]}\n', encoding="utf-8")
            (root / "manifest.json").write_text('{"unverified": true}\n', encoding="utf-8")
            replacements.append(True)
            return verified

        with patch.object(snapshot, "_bundle", side_effect=replace_files_after_verification):
            action = workbench.call("graph", "services")
        self.assertEqual(replacements, [True])
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertEqual(action["result"]["catalog"], expected)
        self.assertEqual(action["result"]["snapshot"]["manifest_sha256"], manifest_sha256)

    def test_coverage_freshness_reports_source_changes_and_new_repositories(self):
        self.web("repos/ui/client", "@fixture/client")
        output, _ = self.build()
        generate_all_graphs.write_ai_outputs(output, self.root / "absent-descriptions.json")
        workbench = self.graph_workbench(output, ["coverage"])
        before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
        current = workbench.call("graph", "coverage")
        self.assertEqual(current["status"], "SUCCEEDED")
        self.assertEqual(current["result"]["freshness"], {"status": "CURRENT", "changed_paths": []})
        self.write("repos/ui/client/src/index.ts", "export const ready = false;\n")
        self.web("repos/ui/new-client", "@fixture/new-client")
        stale = workbench.call("graph", "coverage")
        self.assertEqual(stale["status"], "SUCCEEDED")
        self.assertEqual(stale["result"]["freshness"], {
            "status": "STALE", "changed_paths": ["repos/ui/client", "repos/ui/new-client"]})
        self.assertEqual(stale["result"]["snapshot"], current["result"]["snapshot"])
        self.assertEqual({path.relative_to(output): path.read_bytes()
                          for path in output.rglob("*") if path.is_file()}, before)

    def test_source_change_after_validation_aborts_publication_and_retains_previous_bytes(self):
        self.web("repos/ui/client", "@fixture/client")
        output = self.root / ".workbench/published"
        self.build(output)
        generate_all_graphs.write_ai_outputs(output, self.root / "absent-descriptions.json")
        before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
        self.write("repos/ui/client/src/new.ts", "fetch('/candidate-boundary');\n")
        validation_seen = []

        def change_source_after_validation(*parts, **kwargs):
            result = subprocess.run([str(part) for part in parts], cwd=kwargs["workspace"],
                                    check=True, capture_output=True, timeout=30)
            if any(str(part).endswith("validate_graph") for part in parts):
                validation_seen.append(True)
                self.write("repos/ui/client/src/new.ts", "fetch('/changed-during-build');\n")
            return result

        with patch.object(generate_all_graphs, "run", side_effect=change_source_after_validation), \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "sources changed during graph generation"):
                generate_all_graphs.main(["--workspace", str(self.root), "--out", str(output)])
        self.assertEqual(validation_seen, [True])
        self.assertEqual({path.relative_to(output): path.read_bytes()
                          for path in output.rglob("*") if path.is_file()}, before)

    def test_generation_rejects_nonempty_authored_output_directories_without_changing_bytes(self):
        self.web("repos/ui/client", "@fixture/client")
        authored = self.write("authored/retained.bin", "Retain authored evidence.\n").parent
        for output in (self.root / "registry", authored):
            with self.subTest(output=output.name):
                before = {path.relative_to(output): path.read_bytes()
                          for path in output.rglob("*") if path.is_file()}
                with patch.object(generate_all_graphs, "run", side_effect=AssertionError("Generation must not start")) as run:
                    with self.assertRaises(ValueError):
                        generate_all_graphs.main(["--workspace", str(self.root), "--out", str(output)])
                run.assert_not_called()
                self.assertEqual({path.relative_to(output): path.read_bytes()
                                  for path in output.rglob("*") if path.is_file()}, before)

    def test_generation_rejects_symlink_output_before_resolving_the_existing_snapshot(self):
        self.web("repos/ui/client", "@fixture/client")
        target = self.root / ".workbench/published"
        self.build(target)
        generate_all_graphs.write_ai_outputs(target, self.root / "absent-descriptions.json")
        alias = target.with_name("alias")
        alias.symlink_to(target, target_is_directory=True)
        before = {path.relative_to(target): path.read_bytes() for path in target.rglob("*") if path.is_file()}
        with patch.object(generate_all_graphs, "run", side_effect=AssertionError("Generation must not start")) as run:
            with self.assertRaises(ValueError):
                generate_all_graphs.main(["--workspace", str(self.root), "--out", str(alias)])
        run.assert_not_called()
        self.assertTrue(alias.is_symlink())
        self.assertEqual({path.relative_to(target): path.read_bytes()
                          for path in target.rglob("*") if path.is_file()}, before)

    def test_graph_operation_grants_deny_queries_before_snapshot_access(self):
        output = self.root / "missing-snapshot"
        workbench = self.graph_workbench(output, ["coverage"])
        with patch("ai_sdlc_workbench.providers.graph.GraphSnapshotProvider._invoke") as invoke:
            action = workbench.call("graph", "relationships")
        invoke.assert_not_called()
        self.assertEqual(action["status"], "DENIED")
        self.assertEqual(workbench.run(action["id"])["status"], "DENIED")
        self.assertFalse(output.exists())

    def test_generated_workspace_excludes_live_graph_data_and_runtime_source(self):
        shutil.copy2(scaffold_root() / "scaffold.json", self.root / "scaffold.json")
        self.write("core/relationships/graph/leaked.py", "raise RuntimeError('Runtime source leak')\n")
        self.write("relationships/service-dependencies/project-graph.json", '{"private": true}\n')
        target = self.root.parent / "generated"
        with patch("ai_sdlc_workbench.workspace.scaffold_root", return_value=self.root):
            initialize_workspace(target)
        self.assertFalse((target / "relationships/service-dependencies/project-graph.json").exists())
        self.assertFalse((target / "core/relationships/graph").exists())
        self.assertEqual(list((target / "core").rglob("*.py")), [])
        self.assertTrue((target / "relationships/service-dependencies/README.md").is_file())


if __name__ == "__main__":
    unittest.main()
