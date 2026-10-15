"""Check the copied skill without Workbench or its original parent project."""

from contextlib import redirect_stdout
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SKILL_ROOT = Path(__file__).resolve().parents[1]


def repository_fixture(root):
    files = {
        "repos/ui/client/package.json": '{"name":"@fixture/client"}\n',
        "repos/ui/client/src/index.ts": "fetch('/api/orders/42');\n",
        "repos/services/orders/pom.xml": """<project>
  <modelVersion>4.0.0</modelVersion><groupId>fixture</groupId>
  <artifactId>orders</artifactId><version>1.0</version>
</project>
""",
        "repos/services/orders/src/main/java/Controller.java": """
@RestController @RequestMapping("/v1/orders") class Controller {
    @GetMapping("/{id}") Object get() { return null; }
}
""",
        "repos/infra/nginx/nginx.conf": """upstream orders-upstream {
  server orders:8080;
}
server {
  location /api/orders/ {
    proxy_pass http://orders-upstream/v1/orders/;
  }
}
""",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return {relative: (root / relative).read_bytes() for relative in files}


class CopiedSkillTests(unittest.TestCase):
    def _build_fixture(self, root):
        skill = root / ".agents/skills/service-dependencies-graph"
        shutil.copytree(SKILL_ROOT, skill, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        repository_fixture(root)
        runner = skill / "scripts/graph.py"
        output = root / "graph-output"
        result = subprocess.run([sys.executable, str(runner), "--workspace", str(root), "build",
                                 "--repos", "repos", "--out", "graph-output"],
                                cwd=root.parent, capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return runner, output

    def test_validate_resolves_graph_and_projection_paths_against_workspace_with_flags_first(self):
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-validate-paths-") as temporary:
            root = Path(temporary) / "workspace"
            runner, output = self._build_fixture(root)
            elsewhere = Path(temporary) / "elsewhere"
            elsewhere.mkdir()
            result = subprocess.run([
                sys.executable, str(runner), "--workspace", str(root), "validate",
                "--dependencies", "graph-output/dependencies.json",
                "--relationships", "graph-output/repository-relationships.json",
                "graph-output/graph.json",
            ], cwd=elsewhere, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["valid"])
            self.assertEqual(Path(payload["graph"]), (output / "graph.json").resolve())

    def test_query_returns_invalid_snapshot_json_when_manifest_generated_at_is_missing(self):
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-invalid-manifest-") as temporary:
            root = Path(temporary) / "workspace"
            runner, output = self._build_fixture(root)
            manifest_path = output / "manifest.json"
            manifest = json.loads(manifest_path.read_bytes())
            manifest.pop("generated_at")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(runner), "--workspace", str(root), "query",
                "--data-dir", "graph-output", "services", "--args", "{}",
            ], cwd=root.parent, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ERROR")
            self.assertEqual(payload["code"], "INVALID_SNAPSHOT")
            self.assertNotIn("Traceback", result.stderr)

    def test_copied_skill_builds_and_queries_with_parent_imports_denied_and_uses_its_own_viewer(self):
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-portable-skill-") as temporary:
            root = Path(temporary)
            skill = root / ".agents/skills/service-dependencies-graph"
            shutil.copytree(SKILL_ROOT, skill, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            before = repository_fixture(root)
            marker = '<meta name="skill-local-enhancement" content="copied-viewer">'
            template = skill / "tools/viewer.html"
            template.write_text(template.read_text(encoding="utf-8").replace("<head>", "<head>" + marker, 1),
                                encoding="utf-8")
            guard = root / "import-guard"
            guard.mkdir()
            (guard / "sitecustomize.py").write_text("""import sys
class DenyParentImports:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'ai_sdlc_workbench', 'ratan_harness'}:
            raise ImportError('PORTABILITY_IMPORT_DENIED: ' + fullname)
sys.meta_path.insert(0, DenyParentImports())
""", encoding="utf-8")
            environment = {key: value for key, value in os.environ.items()
                           if key not in {"PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP"}}
            environment.update(PYTHONPATH=str(guard), PYTHONDONTWRITEBYTECODE="1", PYTHONSAFEPATH="1")
            preflight = subprocess.run([sys.executable, "-c", """import importlib
for name in ('ai_sdlc_workbench', 'ratan_harness'):
    try:
        importlib.import_module(name)
    except ImportError as error:
        assert 'PORTABILITY_IMPORT_DENIED' in str(error), str(error)
    else:
        raise AssertionError('Parent import was allowed: ' + name)
import yaml, tree_sitter, tree_sitter_java, tree_sitter_typescript, jsonschema
"""], cwd=root, env=environment, capture_output=True, text=True, timeout=15)
            self.assertEqual(preflight.returncode, 0, preflight.stderr)
            runner = skill / "scripts/graph.py"
            output = root / "graph-output"
            built = subprocess.run([sys.executable, str(runner), "--workspace", str(root), "build",
                                    "--repos", "repos", "--out", str(output)],
                                   cwd=root, env=environment, capture_output=True, text=True, timeout=45)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            graph = json.loads((output / "graph.json").read_bytes())
            self.assertEqual({row["name"] for row in graph["repositories"]}, {"client", "orders", "nginx"})
            self.assertTrue(any(edge["relationship"] == "CALLS_REST" and edge.get("resolution_status") == "RESOLVED"
                                for edge in graph["edges"]))
            manifest = json.loads((output / "manifest.json").read_bytes())
            self.assertEqual(manifest["graph_sha256"], hashlib.sha256((output / "graph.json").read_bytes()).hexdigest())
            for artifact in manifest["artifacts"]:
                self.assertEqual(artifact["sha256"], hashlib.sha256((output / artifact["path"]).read_bytes()).hexdigest())
            self.assertIn(marker, (output / "relationship-viewer.html").read_text(encoding="utf-8"))
            queried = subprocess.run([sys.executable, str(runner), "--workspace", str(root), "query",
                                      "--data-dir", str(output), "services", "--args", "{}"],
                                     cwd=root, env=environment, capture_output=True, text=True, timeout=15)
            self.assertEqual(queried.returncode, 0, queried.stdout + queried.stderr)
            result = json.loads(queried.stdout)
            self.assertEqual(result["status"], "SUCCEEDED")
            self.assertEqual(len(result["catalog"]["services"]), 3)
            self.assertEqual({relative: (root / relative).read_bytes() for relative in before}, before)
            self.assertFalse((root / "core").exists())


try:
    workbench_package = importlib.import_module("ai_sdlc_workbench")
    from ai_sdlc_workbench.cli import main
    from ai_sdlc_workbench.relationships.skill import load_graph_tool
    from ai_sdlc_workbench.workspace import initialize_workspace
except ImportError:
    workbench_package = None


@unittest.skipUnless(workbench_package is not None, "Workbench adapter integration requires its installed package.")
class WorkbenchSkillAdapterTests(unittest.TestCase):
    def test_directory_symlink_denial_creates_forwarding_docs_without_duplicate_tools(self):
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-skill-discovery-fallback-") as temporary:
            root = Path(temporary) / "workspace"
            with patch.object(Path, "symlink_to", side_effect=OSError("Directory links are denied.")):
                initialize_workspace(root)
            canonical = root / ".agents/skills/service-dependencies-graph"
            self.assertTrue((canonical / "scripts/graph.py").is_file())
            self.assertTrue((canonical / "tools/build_graph.py").is_file())
            for relative in ("skills/service-dependencies-graph", ".claude/skills/service-dependencies-graph"):
                discovery = root / relative
                self.assertFalse(discovery.is_symlink(), relative)
                self.assertEqual({path.name for path in discovery.iterdir()}, {"SKILL.md"})
                content = (discovery / "SKILL.md").read_text(encoding="utf-8")
                target = os.path.relpath(canonical / "SKILL.md", discovery)
                self.assertIn(f"]({target})", content)
                self.assertTrue((discovery / target).is_file())

    def test_initialized_workspace_discovery_and_adapter_use_the_enhanced_local_skill(self):
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-local-skill-") as temporary:
            root = Path(temporary) / "workspace"
            initialize_workspace(root)
            canonical = root / ".agents/skills/service-dependencies-graph"
            self.assertTrue((canonical / "scripts/graph.py").is_file())
            for relative in ("skills/service-dependencies-graph", ".claude/skills/service-dependencies-graph"):
                discovery = root / relative
                self.assertTrue(discovery.is_symlink(), relative)
                self.assertEqual(discovery.resolve(), canonical.resolve())
            repository_fixture(root)
            marker = '<meta name="skill-local-enhancement" content="adapter-viewer">'
            template = canonical / "tools/viewer.html"
            template.write_text(template.read_text(encoding="utf-8").replace("<head>", "<head>" + marker, 1),
                                encoding="utf-8")
            renderer = load_graph_tool("render_graph", root)
            self.assertEqual(Path(renderer.__file__).resolve(), (canonical / "tools/render_graph.py").resolve())
            with redirect_stdout(io.StringIO()):
                code = main(["--workspace", str(root), "graph", "build"])
            self.assertEqual(code, 0)
            viewer = root / "relationships/service-dependencies/generated/relationship-viewer.html"
            self.assertIn(marker, viewer.read_text(encoding="utf-8"))
            self.assertFalse((Path(workbench_package.__file__).resolve().parent / "relationships/graph").exists())


if __name__ == "__main__":
    unittest.main()
