"""Check passive planning and consequential setup and served-identity boundaries."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import test_preflight as module


class BrowserCachePathTests(unittest.TestCase):
    def test_given_relative_browser_cache_when_workspace_differs_then_runner_workspace_resolves_cache(self):
        """Given a relative browser cache and a separate selected workspace
        When browser prerequisites are resolved
        Then the prepared asset path uses the runner working directory
        """
        with tempfile.TemporaryDirectory(prefix="preflight-browser-cache-") as directory:
            root = Path(directory).resolve()
            declaration = root / "node_modules/playwright-core/browsers.json"
            declaration.parent.mkdir(parents=True)
            declaration.write_text(json.dumps({"browsers": [{"name": "chromium", "revision": "123"}]}))
            with patch.dict(os.environ, {"E2E_BROWSER": "chromium", "PLAYWRIGHT_BROWSERS_PATH": "prepared-cache"}):
                browser = module._browser(root)
            self.assertTrue(browser.is_absolute())
            self.assertTrue(browser.is_relative_to(root / "prepared-cache"))
            browser.parent.mkdir(parents=True)
            browser.write_bytes(b"prepared browser fixture")
            self.assertTrue(browser.is_file())


class TestPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="workbench-preflight-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.resource = {"id": "checks", "kind": "testing", "provider": "testing.command",
                         "environment": "local", "config": {"path": ".", "suites": {
                             "unit": ["{python}", "-c", "raise RuntimeError('must never execute')"]}},
                         "allowed_operations": ["list", "run"]}
        self.configure()
        self.write("package.json", {"scripts": {"e2e:test": "existing test command", "e2e:remote": "existing remote command", "e2e:ai": "existing ai command"},
                                    "devDependencies": {"@playwright/test": "1.64.1", "tsx": "4.20.6"}})
        for package, version in [("@playwright/test", "1.64.1"), ("tsx", "4.20.6")]:
            self.write(f"node_modules/{package}/package.json", {"version": version})
        self.browser = self.root / "browser"
        self.browser.write_bytes(b"prepared browser executable")
        self.addCleanup(patch.stopall)
        patch.object(module.shutil, "which", return_value=str(self.browser)).start()
        patch.object(module, "_browser", return_value=self.browser).start()

    def write(self, name, data):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data))
        return p

    def configure(self):
        self.write("workspace.json", {"schema_version": 1, "id": "preflight-fixture", "name": "Preflight fixture", "resources": [self.resource]})

    def checks(self, data):
        return str(self.write("checks.json", {"schema_version": 1, **data}))

    def plan(self, **kwargs):
        return module.plan_test_execution(self.root, resource_id="checks", suite="unit", **kwargs)

    def asset(self):
        source = self.root / "application.js"
        source.write_bytes(b"export const version = 1;")
        built = self.root / "application.built.js"
        built.write_bytes(b"built application bytes")
        manifest = self.write("build-manifest.json", {"schema_version": 1,
            "sources": [{"path": source.name, "sha256": module._hash(source.read_bytes()), "revision": "a" * 40}],
            "artifacts": [{"path": built.name, "sha256": module._hash(built.read_bytes())}]})
        return {"id": "application", "url": "http://127.0.0.1:12345/application.js", "artifact_path": built.name,
                "source_manifest": manifest.name, "source_manifest_sha256": module._hash(manifest.read_bytes())}

    def result(self, **kwargs):
        plan = self.plan(**kwargs)
        return module.preflight_test_execution(plan, self.root)

    def test_given_registered_suite_when_planning_then_no_command_network_or_output_creation_occurs(self):
        before = set(self.root.rglob("*"))
        with patch.object(subprocess, "Popen", side_effect=AssertionError("No process")), patch.object(module, "_get", side_effect=AssertionError("No network")):
            plan = self.plan()
        self.assertEqual(plan["command"], [sys.executable, "-c", "raise RuntimeError('must never execute')"])
        self.assertFalse(plan["suite_executed"])
        self.assertEqual(before, set(self.root.rglob("*")))

    def test_given_missing_run_grant_when_preflighting_then_execution_is_not_ready(self):
        self.resource["allowed_operations"] = ["list"]
        self.configure()
        result = self.result()
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["checks"][0]["status"], "FAILED")
        self.assertFalse(result["suite_executed"])

    def test_given_missing_interpreter_when_preflighting_then_specific_setup_failure_is_reported(self):
        self.resource["config"]["suites"]["unit"][0] = "./missing-python"
        self.configure()
        result = self.result()
        row = next(r for r in result["checks"] if r["id"] == "runner-executable")
        self.assertEqual(row["status"], "FAILED")
        self.assertIn("executable", row["next_action"])

    def test_given_stopped_service_when_probing_then_setup_fails_without_product_failure(self):
        plan = self.plan(checks_file=self.checks({"services": [{"id": "portal", "url": "http://127.0.0.1:12345/"}]}))
        with patch.object(module, "_get", side_effect=ConnectionRefusedError()):
            result = module.preflight_test_execution(plan, self.root, probe_services=True)
        self.assertEqual(result["product_behavior"], "NOT_EXECUTED")
        self.assertEqual(next(r for r in result["checks"] if r["id"] == "service:portal")["status"], "FAILED")
        self.assertEqual(result["build_identity"], "UNKNOWN")

    def test_given_services_when_passive_preflight_then_no_network_probe_occurs(self):
        plan = self.plan(checks_file=self.checks({"services": [{"id": "portal", "url": "http://127.0.0.1:12345/"}]}))
        with patch.object(module, "_get", side_effect=AssertionError("No network")):
            result = module.preflight_test_execution(plan, self.root)
        self.assertEqual(next(r for r in result["checks"] if r["id"] == "service:portal")["status"], "NOT_PROBED")
        self.assertFalse(result["network_probed"])

    def test_given_matching_served_asset_when_probing_then_identity_matches_only_declared_scope(self):
        asset = self.asset()
        plan = self.plan(checks_file=self.checks({"served_assets": [asset]}))
        with patch.object(module, "_get", return_value=b"built application bytes"):
            result = module.preflight_test_execution(plan, self.root, probe_services=True)
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["build_identity"], "MATCHED")
        self.assertEqual(result["served_assets"][0]["actual_sha256"], result["served_assets"][0]["expected_sha256"])
        self.assertEqual(result["product_behavior"], "NOT_EXECUTED")
        self.assertNotIn("built application bytes", json.dumps(result))

    def test_given_mismatched_served_asset_when_probing_then_declared_build_is_rejected(self):
        plan = self.plan(checks_file=self.checks({"served_assets": [self.asset()]}))
        with patch.object(module, "_get", return_value=b"wrong deployment"):
            result = module.preflight_test_execution(plan, self.root, probe_services=True)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["build_identity"], "MISMATCH")

    def test_given_changed_build_source_when_probing_then_identity_fails_before_network(self):
        asset = self.asset()
        plan = self.plan(checks_file=self.checks({"served_assets": [asset]}))
        (self.root / "application.js").write_bytes(b"changed source")
        with patch.object(module, "_get", side_effect=AssertionError("No network")):
            result = module.preflight_test_execution(plan, self.root, probe_services=True)
        self.assertEqual(result["served_assets"][0]["status"], "INVALID_BINDING")
        self.assertEqual(result["build_identity"], "UNKNOWN")

    def test_given_changed_local_artifact_when_probing_then_old_fingerprint_is_not_reused(self):
        asset = self.asset()
        plan = self.plan(checks_file=self.checks({"served_assets": [asset]}))
        (self.root / "application.built.js").write_bytes(b"changed artifact")
        with patch.object(module, "_get", side_effect=AssertionError("No network")):
            result = module.preflight_test_execution(plan, self.root, probe_services=True)
        self.assertEqual(result["served_assets"][0]["status"], "INVALID_BINDING")

    def test_given_unreachable_asset_when_probing_then_network_failure_is_not_a_source_binding_failure(self):
        plan = self.plan(checks_file=self.checks({"served_assets": [self.asset()]}))
        with patch.object(module, "_get", side_effect=ConnectionRefusedError()):
            result = module.preflight_test_execution(plan, self.root, probe_services=True)
        self.assertEqual(result["served_assets"][0]["status"], "UNAVAILABLE")
        self.assertEqual(result["build_identity"], "UNKNOWN")

    def test_given_changed_configuration_when_preflighting_then_a_fresh_plan_is_required(self):
        filename = self.checks({})
        plan = self.plan(checks_file=filename)
        Path(filename).write_text('{"schema_version":1,"services":[]}')
        with self.assertRaisesRegex(module.PreflightError, "fresh plan"):
            module.preflight_test_execution(plan, self.root)

    def test_given_remote_environment_when_planning_then_exact_runner_env_and_safe_target_are_retained(self):
        profiles = self.write("profiles.json", {"schemaVersion": 1, "environments": {"nonprod": {
            "targetUrl": "https://nonprod.example.invalid/portal?private=query-secret", "prefix": "MicroWebUI_base", "area": "portal", "storageState": "private-state.json"}}})
        (self.root / "private-state.json").write_text('secret-authentication-value')
        plan = module.plan_test_execution(self.root, runner="playwright", suite="e2e:remote", environment="nonprod", environments_file=str(profiles))
        result = module.preflight_test_execution(plan, self.root)
        self.assertEqual(plan["invocation_environment"]["E2E_ENVIRONMENT"], "nonprod")
        self.assertEqual(plan["command"][2], "e2e:remote")
        self.assertNotIn("query-secret", json.dumps(result))
        self.assertNotIn("secret-authentication-value", json.dumps(result))
        auth = next(r for r in result["checks"] if r["id"] == "authentication-state")
        self.assertTrue(auth["present"])
        self.assertFalse(auth["content_inspected"])
        self.assertEqual(result["build_identity"], "UNKNOWN")

    def test_given_query_bound_checks_when_planning_then_reports_redact_queries_but_probes_retain_them(self):
        """Given a query-dependent readiness URL
        When a serializable plan is inspected and probed
        Then output omits query values and the request preserves its declared URL
        """
        private_url = "https://example.invalid/ready?token=SYNTHETIC_QUERY_MARKER"
        plan = self.plan(checks_file=self.checks({"services": [{"id": "portal", "url": private_url}]}))
        self.assertNotIn("SYNTHETIC_QUERY_MARKER", json.dumps(plan))
        with patch.object(module, "_get", return_value=b"ready") as probe:
            result = module.preflight_test_execution(json.loads(json.dumps(plan)), self.root, probe_services=True)
        probe.assert_called_once_with(private_url, 1024 * 1024)
        self.assertNotIn("SYNTHETIC_QUERY_MARKER", json.dumps(result))
        self.assertEqual(next(row for row in result["checks"] if row["id"] == "service:portal")["status"], "READY")

    def test_given_query_bound_asset_when_planning_then_serializable_plan_omits_query_values(self):
        """Given a served asset URL with a query marker
        When planning and probing
        Then output redacts the marker and fingerprint requests retain the full URL
        """
        asset = self.asset()
        asset["url"] += "?signature=SYNTHETIC_QUERY_MARKER"
        plan = self.plan(checks_file=self.checks({"served_assets": [asset]}))
        self.assertNotIn("SYNTHETIC_QUERY_MARKER", json.dumps(plan))
        with patch.object(module, "_get", return_value=b"built application bytes") as probe:
            result = module.preflight_test_execution(json.loads(json.dumps(plan)), self.root, probe_services=True)
        probe.assert_called_once_with(asset["url"], 16 * 1024 * 1024)
        self.assertEqual(result["build_identity"], "MATCHED")
        self.assertNotIn("SYNTHETIC_QUERY_MARKER", json.dumps(result))

    def test_given_checks_without_packages_when_reloading_then_automatic_package_checks_remain(self):
        """Given checks without package declarations
        When Playwright preflight reloads private prerequisites
        Then both automatically selected package versions remain checked
        """
        plan = module.plan_test_execution(self.root, runner="playwright", suite="e2e:test",
                                         checks_file=self.checks({}))
        self.write("node_modules/tsx/package.json", {"version": "0.0.0"})
        result = module.preflight_test_execution(plan, self.root)
        packages = [row for row in result["checks"] if row["id"].startswith("package:")]
        self.assertEqual(len(packages), 2)
        self.assertTrue(any(row["status"] == "FAILED" and row["required"] == "4.20.6" for row in packages))

    def test_given_runner_environment_when_preflighting_then_required_overrides_remain_in_report(self):
        """Given a remote profile and an isolated fixture plan
        When each plan is preflighted
        Then target overrides and explicit variable removals remain available
        """
        profiles = self.write("profiles.json", {"schemaVersion": 1, "environments": {"nonprod": {
            "targetUrl": "https://example.invalid/", "prefix": "MicroWebUI_base"}}})
        remote = module.plan_test_execution(self.root, runner="playwright", suite="e2e:remote",
                                            environment="nonprod", environments_file=str(profiles))
        fixture = module.plan_test_execution(self.root, runner="playwright", suite="e2e:test")
        for plan in (remote, fixture):
            with self.subTest(suite=plan["suite"]):
                result = module.preflight_test_execution(plan, self.root)
                self.assertEqual(result["plan"].get("invocation_environment"), plan["invocation_environment"])

    def test_given_private_state_missing_when_preflighting_then_authentication_remains_incomplete(self):
        result = self.result(checks_file=self.checks({"authentication_state": "missing-state.json"}))
        self.assertEqual(next(r for r in result["checks"] if r["id"] == "authentication-state")["status"], "FAILED")

    def test_given_wrong_package_version_when_preflighting_then_setup_is_not_ready(self):
        self.write("node_modules/@playwright/test/package.json", {"version": "0.0.0"})
        plan = module.plan_test_execution(self.root, runner="playwright", suite="e2e:test")
        result = module.preflight_test_execution(plan, self.root)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertTrue(any(r["id"].startswith("package:") and r["status"] == "FAILED" for r in result["checks"]))
        self.assertIsNone(plan["invocation_environment"]["E2E_ENVIRONMENT"])

    def test_given_missing_browser_when_preflighting_then_browser_prerequisite_is_reported(self):
        self.browser.unlink()
        plan = module.plan_test_execution(self.root, runner="playwright", suite="e2e:test")
        result = module.preflight_test_execution(plan, self.root)
        self.assertEqual(next(r for r in result["checks"] if r["id"] == "browser-asset")["status"], "FAILED")

    def test_given_embedded_credentials_when_planning_then_urls_are_rejected_without_echoing_secret(self):
        filename = self.checks({"services": [{"id": "private", "url": "https://name:credential-secret@example.invalid/"}]})
        with self.assertRaises(module.PreflightError) as context:
            self.plan(checks_file=filename)
        self.assertNotIn("credential-secret", str(context.exception))

    def test_given_duplicate_json_keys_when_planning_then_ambiguous_checks_are_rejected(self):
        filename = self.root / "checks.json"
        filename.write_text('{"schema_version":1,"schema_version":1}')
        with self.assertRaises(module.PreflightError):
            self.plan(checks_file=str(filename))

    def test_given_robot_suite_when_planning_then_existing_suite_and_variable_file_arguments_are_preserved(self):
        suite = self.root / "tests.robot"
        suite.write_text('*** Test Cases ***\nExisting case\n    No Operation\n')
        self.resource.update(provider="testing.robot", config={"path": ".", "python": "{python}", "suites": {"unit": "tests.robot"}})
        self.configure()
        plan = self.plan()
        self.assertEqual(plan["command"][:4], [sys.executable, "-m", "robot", "--outputdir"])
        self.assertEqual(plan["command"][-1], str(suite.resolve()))
        self.assertFalse(plan["suite_executed"])

    def test_given_resource_changed_after_planning_when_preflighting_then_a_fresh_plan_is_required(self):
        plan = self.plan()
        self.resource["allowed_operations"] = ["list"]
        self.configure()
        with self.assertRaisesRegex(module.PreflightError, "fresh plan"):
            module.preflight_test_execution(plan, self.root)

    def test_given_robot_directory_when_planning_then_child_sources_are_fingerprinted(self):
        folder = self.root / "suites"
        folder.mkdir()
        (folder / "case.robot").write_text('*** Test Cases ***\nCase\n    No Operation\n')
        self.resource.update(provider="testing.robot", config={"path": ".", "python": "{python}", "suites": {"unit": "suites"}})
        self.configure()
        plan = self.plan()
        self.assertEqual(len(plan["sources"]), 1)
        self.assertEqual(plan["sources"][0]["sha256"], module._hash((folder / "case.robot").read_bytes()))

    def test_given_robot_symlinked_interpreter_when_preflighting_then_the_selected_venv_is_checked(self):
        self.resource.update(provider="testing.robot", config={"path": ".", "python": str(self.root / "venv/bin/python"), "suites": {"unit": "case.robot"}})
        (self.root / "case.robot").write_text('*** Test Cases ***\nCase\n    No Operation\n')
        interpreter = self.root / "venv/bin/python"
        interpreter.parent.mkdir(parents=True)
        interpreter.symlink_to(sys.executable)
        (self.root / "venv/lib/python3.12/site-packages/robotframework-7.3.dist-info").mkdir(parents=True)
        self.configure()
        plan = self.plan()
        self.assertEqual(plan["command"][0], str(interpreter))
        result = module.preflight_test_execution(plan, self.root)
        self.assertEqual(next(r for r in result["checks"] if r["id"] == "robot-framework")["status"], "READY")
