"""Check portable initialization, local path mappings, and read-only validation."""

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.workspace import initialize_workspace, load_workspace


DEFAULT_SETTINGS = {
    "auto_commit_staged_changes": True,
    "commit_message_style": "plain",
    "commit_granularity": "per_stage",
    "branch_prefix": "feature/",
    "ponytail_mode": "full",
    "report_verbosity": "standard",
}


class WorkspaceV2Tests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-v2-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        initialize_workspace(self.root)

    def register_repository(self):
        path = self.root / "registry/repositories.yaml"
        path.write_text(yaml.safe_dump({"schema_version": 1, "repositories": [
            {"id": "settlement-code", "location": "repos/settlement"}]}), encoding="utf-8")
        return path

    def local_paths(self, paths):
        (self.root / "workspace.local.yaml").write_text(yaml.safe_dump({
            "schema_version": 1, "repository_paths": paths}), encoding="utf-8")

    def test_agent_defaults_preserve_existing_yaml_and_legacy_json_without_rewriting(self):
        path = self.root / "workspace.yaml"
        generated = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(generated.pop("settings"), DEFAULT_SETTINGS)
        for filename in ("workspace.yaml", "workspace.json"):
            path.unlink(missing_ok=True)
            path = self.root / filename
            for settings in (None, {}, {"auto_commit_staged_changes": False}, {"report_verbosity": "detailed"}):
                with self.subTest(filename=filename, settings=settings):
                    payload = dict(generated)
                    if settings is not None:
                        payload["settings"] = settings
                    path.write_text(json.dumps(payload), encoding="utf-8")
                    before = path.read_bytes()
                    configuration, _ = load_workspace(self.root)
                    self.assertEqual(configuration["settings"], {**DEFAULT_SETTINGS, **(settings or {})})
                    self.assertEqual(path.read_bytes(), before)
                    self.assertFalse((self.root / ".workbench").exists())

    def test_status_reports_valid_overrides_and_omitted_defaults_in_yaml_and_legacy_json(self):
        path = self.root / "workspace.yaml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        for filename in ("workspace.yaml", "workspace.json"):
            path.unlink(missing_ok=True)
            path = self.root / filename
            for name, values in {
                "auto_commit_staged_changes": (True, False),
                "commit_message_style": ("plain", "conventional"),
                "commit_granularity": ("per_stage", "per_task"),
                "branch_prefix": ("feature/", "fix/", "team/feature-"),
                "ponytail_mode": ("lite", "full", "ultra", "off"),
                "report_verbosity": ("concise", "standard", "detailed"),
            }.items():
                for value in values:
                    with self.subTest(filename=filename, name=name, value=value):
                        payload["settings"] = {name: value}
                        path.write_text(yaml.safe_dump(payload) if filename.endswith(".yaml")
                                        else json.dumps(payload), encoding="utf-8")
                        output = io.StringIO()
                        with redirect_stdout(output):
                            code = main(["--workspace", str(self.root), "status"])
                        self.assertEqual(code, 0)
                        self.assertEqual(json.loads(output.getvalue())["settings"], {**DEFAULT_SETTINGS, name: value})
                        self.assertEqual(load_workspace(self.root)[0]["settings"], {**DEFAULT_SETTINGS, name: value})

    def test_invalid_agent_settings_fail_validation_instead_of_enabling_commits(self):
        path = self.root / "workspace.yaml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        for settings in (None, [], True, {"auto_commit_staged_changes": "false"},
                         {"auto_commit_staged_changes": 0}, {"auto_commit_staged_changes": 1},
                         {"auto_commit_staged_changes": None}, {"auto_commit": False},
                         {"commit_message_style": "arbitrary"}, {"commit_message_style": True},
                         {"commit_granularity": "stage"}, {"commit_granularity": None},
                         {"branch_prefix": ""}, {"branch_prefix": "a" * 81}, {"branch_prefix": False},
                         {"ponytail_mode": "normal"}, {"ponytail_mode": False},
                         {"report_verbosity": "verbose"}, {"report_verbosity": 2}):
            with self.subTest(settings=settings):
                payload["settings"] = settings
                path.write_text(yaml.safe_dump(payload), encoding="utf-8")
                with self.assertRaises(WorkbenchError):
                    load_workspace(self.root)
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main(["--workspace", str(self.root), "validate"])
                self.assertEqual(code, 1)
                self.assertEqual(json.loads(output.getvalue())["findings"][0]["code"], "WORKSPACE_ERROR")

    def test_local_mapping_resolves_paths_without_changing_catalog_bytes_or_grants(self):
        catalog = self.register_repository()
        original = catalog.read_bytes()
        self.local_paths({"settlement-code": "../existing-checkout"})
        configuration, resources = load_workspace(self.root)
        repository = configuration["_catalogs"]["repositories"][0]
        self.assertEqual(repository["location"], str((self.root.parent / "existing-checkout").resolve()))
        self.assertEqual(resources, {})
        self.assertEqual(catalog.read_bytes(), original)
        self.assertFalse((self.root / ".workbench").exists())

    def test_invalid_and_unknown_local_mappings_fail_closed(self):
        self.register_repository()
        for paths in ({"unknown": "/tmp/code"}, {"settlement-code": ""},
                      {"settlement-code": True}, {"settlement-code": "bad\x00path"}):
            with self.subTest(paths=paths):
                self.local_paths(paths)
                with self.assertRaises(WorkbenchError):
                    load_workspace(self.root)

    def test_local_mapping_cannot_add_tool_settings_or_hide_duplicate_ids(self):
        self.register_repository()
        path = self.root / "workspace.local.yaml"
        for content in (
                "schema_version: 1\nrepository_paths: {}\nresources: []\n",
                "schema_version: 1\nrepository_paths:\n  settlement-code: one\n  settlement-code: two\n"):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(WorkbenchError):
                    load_workspace(self.root)

    def test_validation_checks_fresh_workspace_without_loading_providers_or_writing(self):
        def snapshot():
            return {str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in self.root.rglob("*") if path.is_file()}
        before = snapshot()
        output = io.StringIO()
        with patch("ai_sdlc_workbench.cli.Workbench", side_effect=AssertionError("No provider runtime")):
            with redirect_stdout(output):
                code = main(["--workspace", str(self.root), "validate"])
        result = json.loads(output.getvalue())
        self.assertEqual(code, 0, result)
        self.assertEqual(result["status"], "VALID")
        self.assertEqual(result["documents"], 0)
        self.assertEqual(result["findings"], [])
        self.assertEqual(snapshot(), before)
        self.assertFalse((self.root / ".workbench").exists())

    def test_validation_reports_invalid_configuration_and_knowledge(self):
        (self.root / "knowledge/records/requirements/REQ-invalid.md").write_text(
            "# Requirement without metadata\n", encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--workspace", str(self.root), "validate"])
        result = json.loads(output.getvalue())
        self.assertEqual(code, 1)
        self.assertFalse(result["valid"])
        self.assertTrue(result["findings"])
        (self.root / "workspace.yaml").write_text("schema_version: [broken", encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--workspace", str(self.root), "validate"])
        result = json.loads(output.getvalue())
        self.assertEqual(code, 1)
        self.assertEqual(result["findings"][0]["code"], "WORKSPACE_ERROR")


if __name__ == "__main__":
    unittest.main()
