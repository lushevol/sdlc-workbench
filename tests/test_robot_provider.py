"""Check Robot execution boundaries without installing Robot Framework."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import Mock, patch

from ai_sdlc_workbench.mcp import McpServer
from ai_sdlc_workbench.providers.robot import RobotTestingProvider
from ai_sdlc_workbench.runtime import Workbench

from support import WorkspaceTestCase


FAKE_ROBOT = r'''
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

arguments = sys.argv[1:]
directory = Path(arguments[arguments.index("--outputdir") + 1])
spec = json.loads(Path(arguments[-1]).read_text())
directory.mkdir(parents=True, exist_ok=True)
(directory / "invocation.json").write_text(json.dumps({
    "arguments": arguments,
    "robot_options_present": "ROBOT_OPTIONS" in os.environ,
    "rebot_options_present": "REBOT_OPTIONS" in os.environ,
}))
print("Robot process started", flush=True)
(directory / "log.html").write_text("<html>retained native log</html>")
(directory / "report.html").write_text("<html>retained native report</html>")
if spec.get("mode") == "timeout":
    (directory / "output.xml").write_text("<robot><suite")
    subprocess.Popen([sys.executable, "-c",
        "import pathlib, time; time.sleep(2); pathlib.Path('escaped-child.txt').write_text('unexpected')"])
    time.sleep(30)
if spec.get("mode") == "missing":
    sys.exit(0)
if spec.get("mode") == "malformed":
    (directory / "output.xml").write_text("<robot><suite")
    sys.exit(0)
robot = ET.Element("robot", generator="Stub Robot")
outer = ET.SubElement(robot, "suite", name="Root")
suite = ET.SubElement(outer, "suite", name="Selected")
for index, status in enumerate(spec.get("statuses", ["PASS"]), 1):
    test = ET.SubElement(suite, "test", id=f"s1-s1-t{index}", name=f"Case {index}")
    keyword = ET.SubElement(test, "kw", name="Secret keyword data")
    ET.SubElement(keyword, "msg").text = "VARIABLE_SECRET_SENTINEL"
    ET.SubElement(keyword, "status", status="FAIL")
    if status != "MISSING":
        ET.SubElement(test, "status", status=status).text = "VARIABLE_SECRET_SENTINEL"
suite_status = spec.get("suite_status", "FAIL" if "FAIL" in spec.get("statuses", []) else "PASS")
ET.SubElement(suite, "status", status=suite_status)
ET.SubElement(outer, "status", status=suite_status)
ET.ElementTree(robot).write(directory / "output.xml", encoding="utf-8", xml_declaration=True)
sys.exit(spec.get("exit_code", 0))
'''


class RobotProviderTests(WorkspaceTestCase):
    def setUp(self):
        super().setUp()
        self.engine = self.root / "project"
        (self.engine / "robot.py").write_text(FAKE_ROBOT, encoding="utf-8")
        (self.engine / "suites").mkdir()
        self.suite = self.engine / "suites/offline.robot"
        self.suite.write_text(json.dumps({"statuses": ["PASS"]}), encoding="utf-8")
        configuration = self.read_configuration()
        configuration["resources"].append({
            "id": "robot-tests", "kind": "testing", "provider": "testing.robot", "environment": "offline",
            "config": {"path": "project", "python": "{python}", "suites": {"offline": "suites/offline.robot"}},
            "allowed_operations": ["list", "run"],
        })
        self.configure(configuration)

    def configure(self, configuration):
        (self.root / "workspace.json").write_text(json.dumps(configuration), encoding="utf-8")
        self.workbench = Workbench(self.root)

    def scenario(self, **spec):
        self.suite.write_text(json.dumps(spec), encoding="utf-8")

    def execute(self, **arguments):
        return self.call("testing.robot", "run", {"suite": "offline", **arguments})

    def test_native_results_preserve_statuses_and_hashed_evidence(self):
        self.scenario(statuses=["PASS", "FAIL", "SKIP"], exit_code=1)
        action = self.execute()
        self.assertEqual(action["status"], "FAILED")
        result = action["result"]
        self.assertEqual(result["counts"], {"PASS": 1, "FAIL": 1, "SKIP": 1, "total": 3})
        self.assertEqual([test["status"] for test in result["tests"]], ["PASS", "FAIL", "SKIP"])
        self.assertEqual(result["tests"][0]["suite"], "Root.Selected")
        self.assertEqual(result["environment"], "offline")
        self.assertEqual(result["exit_code"], 1)
        self.assertFalse(result["behavior_verified"])
        raw_suite = self.suite.read_bytes()
        self.assertEqual(result["suite_sources"], [{"path": "suites/offline.robot",
            "sha256": hashlib.sha256(raw_suite).hexdigest(), "size_bytes": len(raw_suite)}])
        self.assertNotIn("VARIABLE_SECRET_SENTINEL", json.dumps(result))
        paths = {item["path"] for item in action["evidence"]}
        for name in ("output.xml", "log.html", "report.html", "invocation.json"):
            self.assertTrue(any(path.endswith("/robot/" + name) for path in paths))
        for item in action["evidence"]:
            raw = (self.root / item["path"]).read_bytes()
            self.assertEqual(item["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(self.workbench.run(action["id"])["result"], result)
        self.assertFalse((self.engine / "output.xml").exists())

    def test_skips_remain_distinct_from_passes(self):
        self.scenario(statuses=["SKIP", "SKIP"], suite_status="SKIP")
        action = self.execute()
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertEqual(action["result"]["counts"], {"PASS": 0, "FAIL": 0, "SKIP": 2, "total": 2})
        self.assertFalse(action["result"]["behavior_verified"])
        self.assertTrue(any("Skipped tests supply no assertion" in item for item in action["result"]["limitations"]))

    def test_dry_run_and_inherited_options_cannot_imply_live_assertions(self):
        with patch.dict(os.environ, {"ROBOT_OPTIONS": "--variable SECRET:do-not-retain",
                                     "REBOT_OPTIONS": "--output evil.xml"}):
            action = self.execute(dry_run=True)
        self.assertEqual(action["status"], "SUCCEEDED")
        result = action["result"]
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["execution_mode"], "dry-run")
        self.assertFalse(result["behavior_verified"])
        self.assertTrue(any("without executing test assertions" in item for item in result["limitations"]))
        invocation = json.loads((Path(result["output_path"]).parent / "invocation.json").read_text())
        self.assertIn("--dryrun", invocation["arguments"])
        self.assertFalse(invocation["robot_options_present"])
        self.assertFalse(invocation["rebot_options_present"])
        self.assertNotIn("do-not-retain", json.dumps(action))

    def test_result_failures_override_successful_process_exit(self):
        scenarios = [({"mode": "missing"}, "MISSING_ROBOT_OUTPUT"),
                     ({"mode": "malformed"}, "INVALID_ROBOT_OUTPUT"),
                     ({"statuses": ["MISSING"]}, "INVALID_ROBOT_OUTPUT"),
                     ({"statuses": ["UNKNOWN"]}, "INVALID_ROBOT_OUTPUT"),
                     ({"statuses": []}, "INVALID_ROBOT_OUTPUT")]
        for spec, code in scenarios:
            with self.subTest(spec=spec):
                self.scenario(**spec)
                action = self.execute()
                self.assertEqual(action["status"], "FAILED")
                self.assertEqual(action["result"]["exit_code"], 0)
                self.assertEqual(action["result"]["code"], code)
                self.assertTrue(any(item["path"].endswith("stdout.txt") for item in action["evidence"]))
        for spec in ({"statuses": ["FAIL"]}, {"statuses": ["PASS"], "suite_status": "FAIL"},
                     {"statuses": ["PASS"], "exit_code": 7}):
            with self.subTest(spec=spec):
                self.scenario(**spec)
                action = self.execute()
                self.assertEqual(action["status"], "FAILED")
                self.assertIn("counts", action["result"])

    def test_list_and_denied_or_invalid_calls_do_not_execute(self):
        listed = self.call("testing.robot", "list")
        self.assertEqual(listed["result"]["suites"], ["offline"])
        self.update_resource("testing.robot", allowed_operations=["list"])
        denied = self.execute()
        self.assertEqual(denied["status"], "DENIED")
        self.assertEqual(self.workbench.run(denied["id"])["status"], "DENIED")
        self.update_resource("testing.robot", allowed_operations=["list", "run"])
        for arguments in ({"suite": "missing"}, {"suite": "offline", "command": "arbitrary"},
                          {"suite": "offline", "dry_run": "false"}):
            with self.subTest(arguments=arguments):
                action = self.call("testing.robot", "run", arguments)
                self.assertEqual(action["status"], "FAILED")
                self.assertFalse((self.root / ".workbench/runs" / action["id"] / "robot").exists())

    def test_configured_suite_paths_cannot_escape_or_become_options(self):
        outside = self.root / "outside.robot"
        outside.write_text("outside", encoding="utf-8")
        (self.engine / "escape.robot").symlink_to(outside)
        (self.engine / "suites/nested-escape.robot").symlink_to(outside)
        baseline = self.update_resource("testing.robot")["config"]
        for path in ("../outside.robot", str(outside), "C:/outside.robot", "escape.robot", "suites",
                     "suites\\offline.robot", "suites/missing.robot"):
            with self.subTest(path=path):
                self.update_resource("testing.robot", config={**baseline, "suites": {"offline": path}})
                action = self.execute()
                self.assertEqual(action["status"], "FAILED")
                self.assertFalse((self.root / ".workbench/runs" / action["id"] / "robot").exists())
        for suites in ({"--help": "suites/offline.robot"}, {"valid": ["--help"]}, {}, {"valid": None}):
            with self.subTest(suites=suites):
                self.update_resource("testing.robot", config={**baseline, "suites": suites})
                self.assertEqual(self.execute()["status"], "FAILED")
        for interpreter in (None, "", "../outside/python", "C:/outside/python", "python\x00bad", "missing-python"):
            with self.subTest(interpreter=interpreter):
                self.update_resource("testing.robot", config={**baseline, "python": interpreter})
                self.assertEqual(self.execute()["status"], "FAILED")

    def test_repo_relative_python_keeps_virtual_environment_symlink_path(self):
        executable = self.engine / ".venv/bin/python"
        executable.parent.mkdir(parents=True)
        executable.symlink_to(sys.executable)
        baseline = self.update_resource("testing.robot")["config"]
        self.update_resource("testing.robot", config={**baseline, "python": ".venv/bin/python"})
        action = self.execute()
        self.assertEqual(action["status"], "SUCCEEDED", action)
        self.assertEqual(action["result"]["command"][0], str(self.engine.resolve() / ".venv/bin/python"))

    def test_private_yaml_variable_files_supply_paths_without_retaining_values(self):
        private = self.root / "private.yaml"
        private.write_text("SECRET: PRIVATE_CONTENT_SENTINEL\n", encoding="utf-8")
        local = self.engine / "variables.yml"
        local.write_text("ENV: offline\n", encoding="utf-8")
        baseline = self.update_resource("testing.robot")["config"]
        self.update_resource("testing.robot", config={**baseline, "variable_files": [str(private), "variables.yml"]})
        action = self.execute()
        self.assertEqual(action["status"], "SUCCEEDED", action)
        command = action["result"]["command"]
        self.assertEqual(command[command.index("--variablefile") + 1], str(private.resolve()))
        self.assertIn(str(local.resolve()), command)
        self.assertEqual(command.count("--variablefile"), 2)
        self.assertNotIn("PRIVATE_CONTENT_SENTINEL", json.dumps(action))
        self.assertTrue(all(not item["path"].endswith(("private.yaml", "variables.yml")) for item in action["evidence"]))
        (self.engine / "variables.py").write_text("raise RuntimeError('must not import')", encoding="utf-8")
        for paths in (["variables.py"], ["missing.yaml"], ["variables.yml", "./variables.yml"],
                      ["../private.yaml"], "variables.yml", [None], ["variables.yml"] * 33):
            with self.subTest(paths=paths):
                self.update_resource("testing.robot", config={**baseline, "variable_files": paths})
                result = self.execute()
                self.assertEqual(result["status"], "FAILED")
                self.assertFalse((self.root / ".workbench/runs" / result["id"] / "robot").exists())

    def test_git_identity_ignores_inherited_repository_and_records_dirty_state(self):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        for command in (["git", "add", "--", "."], ["git", "-c", "user.name=Test Fixture",
                         "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                         "commit", "-q", "-m", "Record Robot fixture"]):
            subprocess.run(command, cwd=self.engine, env=environment, check=True, capture_output=True)
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.engine, env=environment,
                                  check=True, capture_output=True, text=True).stdout.strip()
        with patch.dict(os.environ, {"GIT_DIR": str(self.root / "wrong.git"), "GIT_WORK_TREE": str(self.root)}):
            action = self.execute()
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertEqual(action["result"]["source"], {"revision": revision, "dirty": False})
        self.scenario(statuses=["SKIP"])
        dirty = self.execute()["result"]
        self.assertTrue(dirty["source"]["dirty"])
        self.assertIn("HEAD does not identify uncommitted working tree bytes.", dirty["limitations"])
        (self.engine / "child").mkdir()
        (self.engine / "child/robot.py").write_text(FAKE_ROBOT, encoding="utf-8")
        (self.engine / "child/selected.robot").write_text(json.dumps({}), encoding="utf-8")
        self.update_resource("testing.robot", config={"path": "project/child", "python": "{python}",
                                                     "suites": {"offline": "selected.robot"}})
        unknown = self.execute()
        self.assertEqual(unknown["result"]["source"], {"revision": None, "dirty": None})

    def test_timeout_retains_partial_files_and_stops_child_process_group(self):
        self.scenario(mode="timeout")
        configuration = self.read_configuration()
        configuration["timeout_seconds"] = 1
        self.configure(configuration)
        action = self.execute()
        self.assertEqual(action["status"], "FAILED")
        self.assertEqual(action["result"]["status"], "TIMEOUT")
        self.assertIn("Robot process started", Path(action["result"]["stdout_path"]).read_text())
        self.assertEqual(Path(action["result"]["output_path"]).read_text(), "<robot><suite")
        self.assertTrue(any(item["path"].endswith("/robot/output.xml") for item in action["evidence"]))
        if os.name == "posix":
            time.sleep(1.2)
            self.assertFalse((self.engine / "escaped-child.txt").exists())

    def test_windows_timeout_uses_bounded_system_taskkill_for_the_process_tree(self):
        process = Mock(pid=1234)
        executable = r"C:\Windows\System32\taskkill.exe"
        with patch.object(RobotTestingProvider, "_taskkill_path", return_value=executable), \
                patch("ai_sdlc_workbench.providers.robot.subprocess.run", return_value=Mock(returncode=0)) as run:
            limitation = RobotTestingProvider._terminate(process, windows=True)
        run.assert_called_once_with([executable, "/PID", "1234", "/T", "/F"], stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5, shell=False)
        self.assertIsNone(limitation)
        process.kill.assert_not_called()
        for failure in (Mock(returncode=1), OSError("unavailable"),
                        subprocess.TimeoutExpired([executable], 5)):
            with self.subTest(failure=type(failure).__name__):
                process.reset_mock()
                arguments = {"side_effect": failure} if isinstance(failure, Exception) else {"return_value": failure}
                with patch.object(RobotTestingProvider, "_taskkill_path", return_value=executable), \
                        patch("ai_sdlc_workbench.providers.robot.subprocess.run", **arguments):
                    limitation = RobotTestingProvider._terminate(process, windows=True)
                self.assertEqual(limitation, "Windows child process termination was not confirmed.")
                process.kill.assert_called_once_with()

    def test_unknown_timeout_cleanup_is_retained_as_an_explicit_limit(self):
        self.scenario(mode="timeout")
        configuration = self.read_configuration()
        configuration["timeout_seconds"] = 1
        self.configure(configuration)
        original = RobotTestingProvider._terminate

        def kill_with_unknown_tree(process, *, windows):
            original(process, windows=windows)
            return "Windows child process termination was not confirmed."

        with patch.object(RobotTestingProvider, "_terminate", side_effect=kill_with_unknown_tree):
            action = self.execute()
        self.assertEqual(action["result"]["status"], "TIMEOUT")
        self.assertEqual(action["result"]["cleanup_status"], "UNKNOWN")
        self.assertIn("Windows child process termination was not confirmed.", action["result"]["limitations"])
        self.assertEqual(self.workbench.run(action["id"])["result"]["cleanup_status"], "UNKNOWN")

    def test_mcp_dispatch_exposes_native_results_and_failure_status(self):
        self.scenario(statuses=["FAIL"], exit_code=1)
        result = McpServer(self.workbench).call_tool("workbench_call", {
            "resource_id": "robot-tests", "operation": "run", "arguments": {"suite": "offline"}})
        self.assertTrue(result["isError"])
        self.assertEqual(result["structuredContent"]["result"]["counts"]["FAIL"], 1)
