"""Check the reference-based workspace through its public interfaces."""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.runtime import Workbench
from ai_sdlc_workbench.workspace import initialize_workspace, load_workspace


class WorkspaceLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-layout-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        initialize_workspace(self.root, name="Reference workspace")

    def manifest(self):
        return yaml.safe_load((self.root / "workspace.yaml").read_text(encoding="utf-8"))

    def write_manifest(self, payload):
        (self.root / "workspace.yaml").write_text(yaml.safe_dump(payload), encoding="utf-8")

    def catalog_path(self, category):
        return self.root / self.manifest()["registries"][category]

    def write_catalog(self, category, records):
        self.catalog_path(category).write_text(
            yaml.safe_dump({"schema_version": 1, category: records}), encoding="utf-8")

    def knowledge_tool(self, directory, *, identifier="requirements", grants=None):
        return {"id": identifier, "kind": "knowledge", "provider": "knowledge.local",
                "environment": "local", "config": {"path": str(directory)},
                "allowed_operations": ["read"] if grants is None else grants}

    def test_clean_initialization_has_the_requested_roots_without_business_fixtures(self):
        directories = (
            "registry", "knowledge/requirements", "knowledge/architecture", "knowledge/decisions",
            "relationships/requirement-code", "relationships/code-test", "relationships/service-dependencies",
            "skills/analyze-requirement", "skills/impact-analysis", "skills/verify-implementation", "skills/detect-gaps",
            "core/context", "core/relationships", "core/evidence", "core/execution",
            "adapters/claude-code", "adapters/copilot", "adapters/mcp",
            "knowledge/raw", "knowledge/candidates", "knowledge/findings", "knowledge/audit",
            "knowledge/schemas", "knowledge/templates", "core/ingestion", "core/understanding",
            "core/governance", "adapters/sources", "skills/ingest-knowledge", "skills/govern-knowledge",
        )
        for directory in directories:
            with self.subTest(directory=directory):
                self.assertTrue((self.root / directory).is_dir())
        self.assertTrue((self.root / "workspace.yaml").is_file())
        for name in ("workspace.json", "project", "logs", "database"):
            self.assertFalse((self.root / name).exists(), name)
        for relative in ("README.md", "AGENTS.md", "docs/WORKSPACE_DESIGN.md",
                         "workspace.local.example.yaml", "registry/examples/contracts.yaml"):
            self.assertTrue((self.root / relative).is_file(), relative)
        ignored = (self.root / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertTrue({"repos/", ".workbench/", "workspace.local.yaml"} <= set(ignored))
        for relative in ("repos", "workspace.local.yaml", "src", "tests", "pyproject.toml",
                         "core/__init__.py", "core/cli.py", "core/runtime.py"):
            self.assertFalse((self.root / relative).exists(), relative)
        self.assertEqual(list((self.root / "core").rglob("*.py")), [])
        description = Workbench(self.root).describe()
        self.assertEqual(description["workspace"]["name"], "Reference workspace")
        self.assertEqual(description["resources"], [])
        self.assertEqual(description["catalogs"], {
            name: {"count": 0, "ids": []}
            for name in ("repositories", "services", "capabilities", "contracts", "sources")})

    def test_shared_skills_have_readable_titles_and_physical_workspace_copies(self):
        workbench = Workbench(self.root)
        skills = {item["id"]: item for item in workbench.skill_list()}
        canonical = ("analyze-requirement", "impact-analysis", "verify-implementation", "detect-gaps")
        self.assertTrue(set(canonical) | {"inspect-workspace", "verify-change"} <= skills.keys())
        for identifier in canonical:
            with self.subTest(skill=identifier):
                content = workbench.skill_read(identifier)
                heading = next(line.removeprefix("# ") for line in content.splitlines() if line.startswith("# "))
                self.assertEqual(skills[identifier]["title"], heading)
                self.assertTrue((self.root / "skills" / identifier / "SKILL.md").is_file())
        with self.assertRaises(WorkbenchError):
            workbench.skill_read("../unregistered-skill")

    def test_standard_yaml_takes_precedence_and_legacy_json_remains_supported(self):
        legacy = {"schema_version": 1, "id": "legacy", "name": "Legacy workspace", "resources": []}
        (self.root / "workspace.json").write_text(json.dumps(legacy), encoding="utf-8")
        (self.root / "workspace.yaml").write_text(
            "# Standard YAML, including a block scalar.\n"
            "schema_version: 1\nid: yaml-first\nname: |-\n  YAML workspace\nresources: []\n"
            "registries:\n  repositories: registry/repositories.yaml\n"
            "  services: registry/services.yaml\n  capabilities: registry/capabilities.yaml\n"
            "  tools: registry/tools.yaml\n", encoding="utf-8")
        payload, resources = load_workspace(self.root)
        self.assertEqual(payload["id"], "yaml-first")
        self.assertEqual(payload["name"], "YAML workspace")
        self.assertEqual(resources, {})
        self.assertEqual(Workbench(self.root).describe()["workspace"]["name"], "YAML workspace")
        (self.root / "workspace.yaml").unlink()
        self.assertEqual(Workbench(self.root).describe()["workspace"]["name"], "Legacy workspace")

    def test_invalid_yaml_and_duplicate_keys_do_not_fall_back_to_valid_json(self):
        (self.root / "workspace.json").write_text(json.dumps({
            "schema_version": 1, "id": "legacy", "name": "Valid legacy fallback", "resources": []}),
            encoding="utf-8")
        valid_yaml = (self.root / "workspace.yaml").read_text(encoding="utf-8")
        for content in ("schema_version: [unterminated", valid_yaml + "\nid: hidden-override\n"):
            with self.subTest(content=content[:50]):
                (self.root / "workspace.yaml").write_text(content, encoding="utf-8")
                with self.assertRaises(WorkbenchError):
                    Workbench(self.root)

    def test_duplicate_catalog_keys_are_rejected(self):
        self.catalog_path("tools").write_text(
            "schema_version: 1\ntools: []\ntools: []\n", encoding="utf-8")
        with self.assertRaises(WorkbenchError):
            Workbench(self.root)

    def test_missing_catalog_is_reported_before_operations_can_run(self):
        self.catalog_path("services").unlink()
        with self.assertRaises(WorkbenchError):
            Workbench(self.root)

    def test_catalog_paths_cannot_leave_the_workspace(self):
        outside = self.root.parent / "external-tools.yaml"
        outside.write_text("schema_version: 1\ntools: []\n", encoding="utf-8")
        original = self.manifest()
        for location in ("../external-tools.yaml", str(outside)):
            with self.subTest(location=location):
                payload = {**original, "registries": {**original["registries"], "tools": location}}
                self.write_manifest(payload)
                with self.assertRaises(WorkbenchError):
                    Workbench(self.root)
                self.assertEqual(outside.read_text(encoding="utf-8"), "schema_version: 1\ntools: []\n")

    def test_invalid_registry_path_returns_the_workspace_error_contract(self):
        payload = self.manifest()
        payload["registries"]["tools"] = "registry/invalid\x00.yaml"
        self.write_manifest(payload)
        with self.assertRaises(WorkbenchError):
            Workbench(self.root)
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main(["--workspace", str(self.root), "status"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["error"]["code"], "WORKBENCH_ERROR")
        self.assertEqual(errors.getvalue(), "")
        self.assertFalse((self.root / ".workbench").exists())

    def test_external_requirement_is_read_at_its_original_location_without_mutation(self):
        outside = self.root.parent / "original-requirements"
        outside.mkdir()
        source = outside / "payment.md"
        content = b"# Payment rule\n\nAccept positive amounts.\n"
        source.write_bytes(content)
        self.write_catalog("tools", [self.knowledge_tool(outside)])
        workbench = Workbench(self.root)
        action = workbench.call("requirements", "read", {"path": "payment.md"})
        self.assertEqual(action["status"], "SUCCEEDED")
        document = action["result"]["document"]
        self.assertEqual(Path(document["path"]), source.resolve())
        self.assertEqual(document["content"], content.decode("utf-8"))
        self.assertEqual(document["sha256"], hashlib.sha256(content).hexdigest())
        self.assertEqual(source.read_bytes(), content)
        self.assertEqual(list(outside.iterdir()), [source])
        self.assertEqual(list((self.root / "knowledge/requirements").glob("payment.md")), [])
        self.assertEqual(workbench.run(action["id"])["result"], action["result"])

    def test_catalog_tool_grants_deny_and_retain_a_write_attempt(self):
        outside = self.root.parent / "original-requirements"
        outside.mkdir()
        self.write_catalog("tools", [self.knowledge_tool(outside, grants=["read"])])
        workbench = Workbench(self.root)
        action = workbench.call("requirements", "ingest", {"path": "blocked.md", "content": "Must not write."})
        self.assertEqual(action["status"], "DENIED")
        self.assertEqual(workbench.run(action["id"])["status"], "DENIED")
        self.assertEqual(list(outside.iterdir()), [])

    def test_catalog_and_inline_tools_merge_without_losing_existing_resource_operations(self):
        outside = self.root.parent / "requirements"
        outside.mkdir()
        tool = self.knowledge_tool(outside)
        inline = {**self.knowledge_tool(outside, identifier="inline-knowledge"), "allowed_operations": ["list"]}
        payload = self.manifest()
        payload["resources"] = [inline]
        self.write_manifest(payload)
        self.write_catalog("tools", [tool])
        workbench = Workbench(self.root)
        self.assertEqual({item["id"] for item in workbench.describe()["resources"]},
                         {"requirements", "inline-knowledge"})
        self.assertEqual(workbench.call("inline-knowledge", "list")["status"], "SUCCEEDED")
        self.assertNotIn("tools", workbench.describe()["catalogs"])

    def test_duplicate_tool_ids_grants_and_incompatible_kinds_are_rejected(self):
        tool = self.knowledge_tool(self.root / "knowledge")
        original = self.manifest()
        cases = (([tool, tool], []), ([tool], [tool]),
                 ([{**tool, "allowed_operations": ["read", "read"]}], []),
                 ([{**tool, "kind": "repository"}], []))
        for tools, inline in cases:
            with self.subTest(tools=tools, inline=inline):
                self.write_manifest({**original, "resources": inline})
                self.write_catalog("tools", tools)
                with self.assertRaises(WorkbenchError):
                    Workbench(self.root)


if __name__ == "__main__":
    unittest.main()
