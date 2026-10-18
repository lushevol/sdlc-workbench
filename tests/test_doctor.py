"""Check local readiness, independent environments, and confidential output boundaries."""

import importlib.metadata
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import doctor as module

RUN = subprocess.run


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="workbench-doctor-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        self.root.mkdir()
        self.configure([])
        self.versions = {name: requirement[2:] for name, requirement in {
            **module.CORE_REQUIREMENTS, **module.CLINIC_REQUIREMENTS}.items()}
        self.versions["robotframework"] = "7.3.0"
        self.versions["pywin32"] = "311"
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {}, clear=True).start()
        patch.object(module.metadata, "version", side_effect=self.distribution).start()
        self.which = patch.object(module.shutil, "which", return_value="/detected/executable").start()
        self.child = patch.object(module.subprocess, "run", return_value=SimpleNamespace(
            returncode=0, stdout=b"v22.12.0\n", stderr=b"")).start()
        patch.object(module, "_desktop_app", return_value=True).start()

    def distribution(self, name):
        if name not in self.versions:
            raise importlib.metadata.PackageNotFoundError(name)
        return self.versions[name]

    def configure(self, resources):
        (self.root / "workspace.json").write_text(json.dumps({
            "schema_version": 1, "id": "doctor-fixture", "name": "Doctor fixture",
            "plugins": [], "resources": resources,
        }), encoding="utf-8")

    def feature(self, result, identifier):
        return next(item for item in result["features"] if item["id"] == identifier)

    def source(self):
        source = self.root.parent / "source"
        bridge = source / "core/connectors/workbench/bridge.js"
        bridge.parent.mkdir(parents=True)
        bridge.write_text("throw new Error('Doctor must not execute connector source');", encoding="utf-8")
        (source / "package.json").write_text("{}", encoding="utf-8")
        for name in module.NODE_PACKAGES:
            package = source / "node_modules" / name / "package.json"
            package.parent.mkdir(parents=True, exist_ok=True)
            package.write_text('{"main":"src/index.js"}', encoding="utf-8")
            (package.parent / "src").mkdir()
            (package.parent / "src/index.js").write_text("// Installed fixture", encoding="utf-8")
        return source, bridge

    def connector(self, bridge):
        return {"id": "external-ado", "kind": "connector", "provider": "connector.mcp",
                "environment": "external", "config": {
                    "command": ["node", str(bridge)], "connector": "ado", "allowed_tools": ["wit_get_work_item"]},
                "allowed_operations": ["list", "call"]}

    def test_core_profile_checks_pinned_dependencies_without_optional_services(self):
        result = module.doctor(self.root, profile="core")
        self.assertEqual(result["core_status"], "READY")
        self.assertEqual(result["status"], "READY")
        self.assertEqual({item["id"] for item in result["features"]}, {"core", "workspace", "git"})
        self.child.assert_not_called()
        del self.versions["tree-sitter-java"]
        self.versions["PyYAML"] = "6.0.1"
        result = module.doctor(self.root, profile="core")
        self.assertEqual(result["core_status"], "INCOMPLETE")
        failed = {item["id"] for item in self.feature(result, "core")["checks"] if item["status"] == "INCOMPLETE"}
        self.assertEqual(failed, {"package:tree-sitter-java", "package:PyYAML"})

    def test_missing_or_invalid_workspace_does_not_create_runtime_state(self):
        (self.root / "workspace.json").unlink()
        result = module.doctor(self.root, profile="core")
        self.assertEqual(self.feature(result, "workspace")["status"], "NOT_CONFIGURED")
        self.assertEqual(result["core_status"], "INCOMPLETE")
        self.assertEqual(list(self.root.iterdir()), [])
        (self.root / "workspace.yaml").write_text("password: hidden-config-value", encoding="utf-8")
        result = module.doctor(self.root, profile="core")
        self.assertEqual(self.feature(result, "workspace")["status"], "INCOMPLETE")
        self.assertNotIn("hidden-config-value", json.dumps(result))
        self.assertFalse((self.root / ".workbench").exists())

    def test_missing_optional_credentials_preserve_core_readiness_and_expose_unsupported_packages(self):
        result = module.doctor(self.root)
        self.assertEqual(result["core_status"], "READY")
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(self.feature(result, "connector:ado")["status"], "NOT_CONFIGURED")
        self.assertEqual(self.feature(result, "tests")["status"], "NOT_CONFIGURED")
        for identifier in ("app-bridge", "ado-upload-app"):
            self.assertEqual(self.feature(result, identifier)["status"], "UNSUPPORTED")
        self.assertEqual(result["integration_access"], "UNTESTED")

    def test_wheel_workspace_needs_explicit_connector_source_instead_of_assuming_it_is_bundled(self):
        installed = self.root.parent / "site-packages/ai_sdlc_workbench/doctor.py"
        with patch.object(module, "__file__", str(installed)):
            result = module.doctor(self.root)
            checks = self.feature(result, "connectors")["checks"]
            self.assertEqual(next(item for item in checks if item["id"] == "connector-source")["status"], "INCOMPLETE")
            _, bridge = self.source()
            self.configure([self.connector(bridge)])
            (self.root / ".env").write_text("AZURE_DEVOPS_ORG_URL=https://internal.example/org\nAZURE_DEVOPS_PAT=private-token\n",
                                            encoding="utf-8")
            result = module.doctor(self.root)
        self.assertEqual(self.feature(result, "connectors")["status"], "READY")
        self.assertEqual(self.feature(result, "connector:ado")["status"], "READY")
        self.assertNotIn("private-token", json.dumps(result))
        self.assertNotIn("internal.example", json.dumps(result))

    def test_node_requires_a_successful_recognized_version_and_never_echoes_process_output(self):
        for output, code in ((b"v22.11.0", 0), (b"v20.19.0", 0), (b"v23.5.0", 0), (b"secret-node-diagnostic", 0),
                             (b"v22.12.0", 1), (b"v22.12.0-rc.1", 0)):
            with self.subTest(output=output):
                self.child.return_value = SimpleNamespace(returncode=code, stdout=output, stderr=b"secret-stderr")
                check = module._executable("node", minimum=(22, 12, 0))
                self.assertEqual(check["status"], "INCOMPLETE")
                self.assertNotIn("secret", json.dumps(check))
        self.child.side_effect = subprocess.TimeoutExpired(["node", "--version"], 5)
        self.assertEqual(module._executable("node", minimum=(22, 12, 0))["status"], "INCOMPLETE")

    def test_windows_uses_npm_cmd_without_invoking_a_command_shell(self):
        with patch.object(module.sys, "platform", "win32"):
            result = module.doctor(self.root)
        checks = self.feature(result, "connectors")["checks"]
        self.assertIn("executable:npm.cmd", {item["id"] for item in checks})
        self.which.assert_any_call("npm.cmd")
        for call in self.child.call_args_list:
            self.assertEqual(call.args[0][1:], ["--version"])
            self.assertFalse(call.kwargs["shell"])
            self.assertEqual(call.kwargs["timeout"], 5)
        with patch.object(module.sys, "platform", "win32"):
            for version, status in (("304", "INCOMPLETE"), ("305", "READY")):
                with self.subTest(pywin32=version):
                    self.versions["pywin32"] = version
                    outlook = self.feature(module.doctor(self.root), "messaging.outlook")
                    check = next(item for item in outlook["checks"] if item["id"] == "package:pywin32")
                    self.assertEqual(check["required"], ">=305")
                    self.assertEqual(check["status"], status)

    def test_doctor_preserves_files_environment_and_secret_values_without_network_or_connector_calls(self):
        sentinel = "secret-sentinel-never-print"
        (self.root / ".env").write_text(
            f'AZURE_DEVOPS_PAT="{sentinel}" # retained\nADO_TOKEN={sentinel}\nUSER_EMAIL={sentinel}\n'
            f'SNOW_ENABLED=false\nNODE_OPTIONS=--require {sentinel}\n', encoding="utf-8")
        os.environ["AZURE_DEVOPS_PAT"] = sentinel + "-process"
        os.environ["NODE_OPTIONS"] = "--require " + sentinel
        before_environment = dict(os.environ)
        before_files = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        with patch.object(socket, "create_connection", side_effect=AssertionError("No network")), \
                patch("ai_sdlc_workbench.providers.connectors.ConnectorMcpProvider._invoke",
                      side_effect=AssertionError("No connector calls")):
            result = module.doctor(self.root)
        self.assertEqual(dict(os.environ), before_environment)
        self.assertEqual({str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}, before_files)
        self.assertNotIn(sentinel, json.dumps(result))
        self.assertFalse((self.root / ".workbench").exists())
        for call in self.child.call_args_list:
            self.assertNotIn("NODE_OPTIONS", call.kwargs["env"])
            self.assertNotIn("AZURE_DEVOPS_PAT", call.kwargs["env"])
        clinic = self.feature(result, "release-clinic")
        self.assertEqual(next(item for item in clinic["checks"] if item["id"] == "variable:USER_EMAIL")["status"], "READY")
        self.assertNotIn("variable:CLIENT_ID", {item["id"] for item in clinic["checks"]})

    def test_release_clinic_reports_missing_message_parser_and_user_email(self):
        del self.versions["extract-msg"]
        result = module.doctor(self.root)
        checks = self.feature(result, "release-clinic")["checks"]
        for identifier in ("package:extract-msg", "variable:USER_EMAIL"):
            self.assertEqual(next(item for item in checks if item["id"] == identifier)["status"], "INCOMPLETE")

    def test_robot_metadata_is_checked_in_the_registered_independent_environment(self):
        engine = self.root.parent / "business-tests"
        executable = engine / ".venv/Scripts/python.exe"
        executable.parent.mkdir(parents=True)
        executable.write_bytes(b"Do not execute this registered test interpreter")
        suite = engine / "Tests/offline.robot"
        suite.parent.mkdir()
        suite.write_text("*** Test Cases ***", encoding="utf-8")
        self.configure([{"id": "business-tests", "kind": "testing", "provider": "testing.robot",
            "environment": "local", "config": {"path": str(engine), "python": ".venv/Scripts/python.exe",
                "suites": {"offline": "Tests/offline.robot"}}, "allowed_operations": ["list", "run"]}])
        result = module.doctor(self.root)
        self.assertEqual(self.feature(result, "tests:business-tests")["status"], "INCOMPLETE")
        package = engine / ".venv/Lib/site-packages/robotframework-7.3.0.dist-info"
        package.mkdir(parents=True)
        result = module.doctor(self.root)
        self.assertEqual(self.feature(result, "tests:business-tests")["status"], "READY")
        for call in self.child.call_args_list:
            self.assertNotIn(str(executable), call.args[0])

    def test_unreadable_dotenv_is_fixed_error_and_does_not_print_its_content(self):
        (self.root / ".env").write_bytes(b"TOKEN=private-value\xff")
        result = module.doctor(self.root)
        check = next(item for item in self.feature(result, "connectors")["checks"] if item["id"] == "root-environment-file")
        self.assertEqual(check["status"], "INCOMPLETE")
        self.assertNotIn("private-value", json.dumps(result))

    def test_list_only_grants_never_claim_connector_calls_are_ready(self):
        _, bridge = self.source()
        resource = self.connector(bridge)
        resource["config"]["connector"] = "nexus"
        resource["config"]["allowed_tools"] = []
        resource["allowed_operations"] = ["list"]
        self.configure([resource])
        (self.root / ".env").write_text("NEXUS_BASE_URL=https://example.invalid\nNEXUS_USER_CODE=user\nNEXUS_PASS_CODE=private\n",
                                        encoding="utf-8")
        self.assertEqual(self.feature(module.doctor(self.root), "connector:nexus")["status"], "INCOMPLETE")
        resource["allowed_operations"] = ["list", "call"]
        resource["config"]["allowed_tools"] = ["nexus_scan"]
        self.configure([resource])
        self.assertEqual(self.feature(module.doctor(self.root), "connector:nexus")["status"], "READY")

    def test_browser_requires_its_exact_tool_grant_and_workspace_exports_must_exist(self):
        source, bridge = self.source()
        resource = self.connector(bridge)
        resource["config"]["connector"] = "web"
        resource["config"]["allowed_tools"] = ["web_fetch"]
        self.configure([resource])
        result = module.doctor(self.root)
        self.assertEqual(self.feature(result, "connector:web")["status"], "READY")
        self.assertEqual(self.feature(result, "web.browser")["status"], "INCOMPLETE")
        resource["config"]["allowed_tools"].append("web_crawl_browser")
        self.configure([resource])
        self.assertEqual(self.feature(module.doctor(self.root), "web.browser")["status"], "READY")
        (source / "node_modules/@sc-node-mcp/ado/src/index.js").unlink()
        result = module.doctor(self.root)
        self.assertEqual(self.feature(result, "connectors")["status"], "INCOMPLETE")
        (source / "node_modules/cheerio/package.json").unlink()
        self.assertFalse(module._node_package(source, "cheerio"))

    def test_command_suite_missing_interpreter_is_detected_without_execution(self):
        engine = self.root / "test-engine"
        engine.mkdir()
        resource = {"id": "engine", "kind": "testing", "provider": "testing.command", "environment": "local",
                    "config": {"path": "test-engine", "suites": {"unit": [".venv/bin/python", "-m", "unittest"]}},
                    "allowed_operations": ["list", "run"]}
        self.configure([resource])
        self.assertEqual(self.feature(module.doctor(self.root), "tests:engine")["status"], "INCOMPLETE")
        executable = engine / ".venv/bin/python"
        executable.parent.mkdir(parents=True)
        executable.write_bytes(b"Never execute this fixture")
        self.assertEqual(self.feature(module.doctor(self.root), "tests:engine")["status"], "READY")
        for call in self.child.call_args_list:
            self.assertEqual(call.args[0][1:], ["--version"])

    def test_blank_dotenv_values_with_comments_remain_unconfigured(self):
        (self.root / ".env").write_text("AZURE_DEVOPS_PAT= # not configured\n", encoding="utf-8")
        result = module.doctor(self.root)
        check = next(item for item in self.feature(result, "connector:ado")["checks"] if item["id"] == "variable:AZURE_DEVOPS_PAT")
        self.assertFalse(check["present"])

    def test_connector_missing_configured_bridge_is_not_hidden_by_the_installed_source(self):
        self.configure([self.connector(self.root / "missing/bridge.js")])
        (self.root / ".env").write_text("AZURE_DEVOPS_ORG_URL=https://example.invalid\nAZURE_DEVOPS_PAT=private\n",
                                        encoding="utf-8")
        checks = self.feature(module.doctor(self.root), "connector:ado")["checks"]
        self.assertEqual(next(item for item in checks if item["id"] == "connector-command")["status"], "INCOMPLETE")

    def test_hosted_service_checks_vault_and_local_development_credentials_separately(self):
        self.assertEqual(self.feature(module.doctor(self.root), "release-clinic.service")["status"], "NOT_CONFIGURED")
        (self.root / ".env").write_text("HC_ROLE_ID=private-role\n", encoding="utf-8")
        result = module.doctor(self.root)
        feature = self.feature(result, "release-clinic.service")
        self.assertEqual(feature["status"], "INCOMPLETE")
        self.assertEqual(next(item for item in feature["checks"] if item["id"] == "variable:HC_SECRET_ID")["status"], "INCOMPLETE")
        (self.root / ".env").write_text("VAULT_DEV_MODE=true\n", encoding="utf-8")
        feature = self.feature(module.doctor(self.root), "release-clinic.service")
        self.assertIn("variable:USER_EMAIL", {item["id"] for item in feature["checks"]})
        self.assertNotIn("variable:HC_ROLE_ID", {item["id"] for item in feature["checks"]})
        self.assertNotIn("private-role", json.dumps(result))

    def test_standalone_module_reports_missing_dependencies_without_site_packages(self):
        package = self.root.parent / "isolated/ai_sdlc_workbench"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        (package / "doctor.py").write_bytes(Path(module.__file__).read_bytes())
        result = RUN([sys.executable, "-S", "-m", "ai_sdlc_workbench.doctor", "--workspace", str(self.root), "--profile", "core"],
                     cwd=self.root, env={**os.environ, "PYTHONPATH": str(package.parent)},
                     capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["core_status"], "INCOMPLETE")
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
