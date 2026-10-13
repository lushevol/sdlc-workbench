"""Check permissions and retained execution records through the public API."""

import hashlib
import json
from pathlib import Path
import shutil
from unittest.mock import patch

from ai_sdlc_workbench.models import Operation
from ai_sdlc_workbench.runtime import Workbench, WorkbenchError
from ai_sdlc_workbench.workspace import initialize_workspace

from support import WorkspaceTestCase


class CoreTests(WorkspaceTestCase):
    def test_initializer_preserves_existing_files(self):
        existing = self.root / "retained.txt"
        existing.write_text("Keep this file.", encoding="utf-8")
        with self.assertRaises(ValueError):
            initialize_workspace(self.root)
        self.assertEqual(existing.read_text(encoding="utf-8"), "Keep this file.")

    def test_describe_shows_operations_without_connection_configuration(self):
        secret_marker = "test-secret-must-not-appear"
        resource = self.update_resource("knowledge.local")
        self.update_resource("knowledge.local", config={**resource["config"], "test_secret": secret_marker})
        description = self.workbench.describe()
        self.assertEqual(description["workspace"]["name"], "Integration workspace")
        self.assertTrue(description["providers"])
        self.assertNotIn(secret_marker, repr(description))
        self.assertTrue(all("config" not in item for item in description["resources"]))

    def test_denied_action_is_retained_and_does_not_write_document(self):
        self.update_resource("knowledge.local", allowed_operations=["list", "search", "read"])
        action = self.call("knowledge.local", "ingest", {"path": "denied.md", "content": "blocked"})
        self.assertEqual(action["status"], "DENIED")
        self.assertFalse((self.root / "knowledge" / "denied.md").exists())
        self.assertEqual(self.workbench.run(action["id"])["status"], "DENIED")
        self.assertIn(action["id"], [run["id"] for run in self.workbench.runs()])

    def test_invalid_arguments_are_retained_without_execution(self):
        action = self.call("knowledge.local", "ingest", {
            "path": "invalid.md", "content": "must not write", "extra": True})
        self.assertEqual(action["status"], "FAILED")
        self.assertFalse((self.root / "knowledge" / "invalid.md").exists())
        self.assertEqual(self.workbench.run(action["id"])["status"], "FAILED")

    def test_unknown_resource_and_operation_raise_clear_errors(self):
        with self.assertRaises(WorkbenchError):
            self.workbench.call("missing-resource", "list")
        with self.assertRaises(WorkbenchError):
            self.call("knowledge.local", "missing-operation")

    def test_action_evidence_matches_saved_bytes(self):
        action = self.call("knowledge.local", "list")
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertTrue(action["evidence"])
        for evidence in action["evidence"]:
            path = Path(evidence["path"])
            if not path.is_absolute():
                path = self.root / path
            saved = path.read_bytes()
            self.assertEqual(hashlib.sha256(saved).hexdigest(), evidence["sha256"])
            self.assertEqual(len(saved), evidence["size_bytes"])
        restored = self.workbench.run(action["id"])
        self.assertEqual(restored["result"], action["result"])
        self.assertEqual(restored["evidence"], action["evidence"])

    def test_manifest_rejects_malformed_and_ambiguous_configuration(self):
        baseline = self.read_configuration()
        malformed = ["not JSON", "[]"]
        duplicate_resource = json.loads(json.dumps(baseline))
        duplicate_resource["resources"].append(duplicate_resource["resources"][0])
        malformed.append(json.dumps(duplicate_resource))
        duplicate_grant = json.loads(json.dumps(baseline))
        duplicate_grant["resources"][0]["allowed_operations"].append("list")
        malformed.append(json.dumps(duplicate_grant))
        nonfinite = json.loads(json.dumps(baseline))
        nonfinite["timeout_seconds"] = float("nan")
        malformed.append(json.dumps(nonfinite))
        for content in malformed:
            with self.subTest(content=content[:80]):
                (self.root / "workspace.json").write_text(content, encoding="utf-8")
                with self.assertRaises(WorkbenchError):
                    Workbench(self.root)

    def test_plugin_factory_loads_only_after_explicit_enable(self):
        calls = []

        class ExampleProvider:
            id = "example.echo"
            version = "1.0.0"
            resource_kind = "example"
            operations = {"echo": Operation("echo", "Return the supplied text.", {
                "type": "object", "properties": {"text": {"type": "string"}},
                "required": ["text"], "additionalProperties": False})}

            def invoke(self, operation, resource, arguments, context):
                calls.append((operation, resource.id))
                return {"status": "SUCCEEDED", "text": arguments["text"]}

        class EntryPoint:
            name = "example.echo"

            def load(self):
                calls.append("loaded")
                return ExampleProvider

        with patch("ai_sdlc_workbench.registry.entry_points", return_value=[EntryPoint()]):
            Workbench(self.root)
            self.assertEqual(calls, [])
            configuration = self.read_configuration()
            configuration["plugins"] = ["example.echo"]
            configuration["resources"].append({
                "id": "echo", "kind": "example", "provider": "example.echo", "environment": "local",
                "config": {}, "allowed_operations": ["echo"]})
            (self.root / "workspace.json").write_text(json.dumps(configuration), encoding="utf-8")
            loaded = Workbench(self.root)
            action = loaded.call("echo", "echo", {"text": "provider observation"})
            self.assertEqual(action["status"], "SUCCEEDED")
            self.assertEqual(action["result"]["text"], "provider observation")
            self.assertEqual(calls, ["loaded", ("echo", "echo")])

            configuration["resources"][-1]["allowed_operations"] = ["undeclared"]
            (self.root / "workspace.json").write_text(json.dumps(configuration), encoding="utf-8")
            with self.assertRaises(WorkbenchError):
                Workbench(self.root)

    def test_invalid_plugin_operation_contract_prevents_workspace_load(self):
        class BrokenProvider:
            id = "example.broken"
            version = "1.0.0"
            resource_kind = "example"
            operations = {"echo": Operation("other", "Invalid declared operation.", {"type": "object"})}

            def invoke(self, *_):
                raise AssertionError("The invalid provider must not execute.")

        class EntryPoint:
            name = "example.broken"

            def load(self):
                return BrokenProvider

        configuration = self.read_configuration()
        configuration["plugins"] = ["example.broken"]
        (self.root / "workspace.json").write_text(json.dumps(configuration), encoding="utf-8")
        with patch("ai_sdlc_workbench.registry.entry_points", return_value=[EntryPoint()]):
            with self.assertRaises(WorkbenchError):
                Workbench(self.root)

    def test_unenforceable_plugin_schemas_fail_before_dispatch(self):
        class Provider:
            id = "example.schema"
            version = "1.0.0"
            resource_kind = "example"

            def invoke(self, *_):
                raise AssertionError("An unsupported schema must not execute.")

        schemas = [
            {"type": "object", "properties": {"value": {"type": "string", "pattern": "^safe$"}}},
            {"type": "object", "$ref": "#/$defs/action"},
            {"type": "object", "description": object()},
            {"type": "object", "default": object()},
            {"type": "object", "properties": {"value": {"type": "number", "maximum": float("inf")}}},
        ]
        for schema in schemas:
            with self.subTest(schema=repr(schema)):
                provider = Provider()
                provider.operations = {"check": Operation("check", "Check a supplied value.", schema)}
                with self.assertRaises(WorkbenchError):
                    self.install_fixture_provider(provider)

    def test_provider_requires_an_explicit_result_status(self):
        class Provider:
            id = "example.result"
            version = "1.0.0"
            resource_kind = "example"
            operations = {"check": Operation("check", "Return an operation result.", {"type": "object"})}

            def invoke(self, *_):
                return self.result

        provider = Provider()
        workbench = self.install_fixture_provider(provider)
        for result in ({}, {"status": "UNRECOGNIZED"}):
            with self.subTest(result=result):
                provider.result = result
                action = workbench.call("fixture", "check")
                self.assertEqual(action["status"], "FAILED")
                self.assertEqual(workbench.run(action["id"])["status"], "FAILED")

    def test_evidence_symlink_cannot_overwrite_an_external_file(self):
        outside = self.root.parent / "retained-external.txt"
        outside.write_bytes(b"retain these exact bytes")

        class Provider:
            id = "example.symlink"
            version = "1.0.0"
            resource_kind = "example"
            operations = {"create": Operation("create", "Create an evidence fixture.", {"type": "object"})}

            def invoke(self, operation, resource, arguments, context):
                (context.run_dir / "result.json").symlink_to(outside)
                return {"status": "SUCCEEDED"}

        workbench = self.install_fixture_provider(Provider())
        action = workbench.call("fixture", "create")
        self.assertEqual(action["status"], "FAILED")
        self.assertEqual(outside.read_bytes(), b"retain these exact bytes")
        self.assertEqual(workbench.run(action["id"])["status"], "FAILED")

    def test_state_symlink_is_rejected_before_external_writes(self):
        shutil.rmtree(self.root / ".workbench")
        outside = self.root.parent / "external-state"
        outside.mkdir()
        (self.root / ".workbench").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(WorkbenchError):
            Workbench(self.root)
        self.assertEqual(list(outside.iterdir()), [])
