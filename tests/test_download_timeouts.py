"""Exercise bounded download processes and their offline recovery boundaries."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from ai_sdlc_workbench import bootstrap, offline


class DownloadTimeoutTests(unittest.TestCase):
    def test_stalled_download_stops_descendants_and_explains_manual_recovery(self):
        with tempfile.TemporaryDirectory(prefix="workbench-download-timeout-") as temporary:
            root = Path(temporary)
            started, completed = root / "started", root / "completed"
            child = ("import pathlib,sys,time; pathlib.Path(sys.argv[1]).write_text('started'); "
                     "time.sleep(2.5); pathlib.Path(sys.argv[2]).write_text('download continued')")
            parent = ("import subprocess,sys,time; "
                      f"subprocess.Popen([sys.executable, '-c', {child!r}, sys.argv[1], sys.argv[2]]); "
                      "time.sleep(60)")
            began = time.monotonic()
            with self.assertRaises(bootstrap.SetupError) as raised:
                bootstrap.command([sys.executable, "-c", parent, str(started), str(completed)],
                                  root, seconds=1, download="python")
            self.assertLess(time.monotonic() - began, 8)
            self.assertTrue(started.is_file(), "The descendant must start before timeout cleanup.")
            self.assertIn("timed out after 1 seconds", str(raised.exception))
            self.assertIn("Warning:", str(raised.exception))
            self.assertIn("--offline-bundle PATH", str(raised.exception))
            self.assertIn("docs/SETUP.md#blocked-downloads-and-manual-recovery", str(raised.exception))
            time.sleep(2.6)
            self.assertFalse(completed.exists(), "A downloader descendant survived the timeout.")

    def test_download_bounds_override_inherited_retries_without_changing_parent_settings(self):
        probe = "import json,os; print(json.dumps({k:os.environ[k] for k in ('PIP_TIMEOUT','PIP_RETRIES','PIP_DISABLE_PIP_VERSION_CHECK')}))"
        with tempfile.TemporaryDirectory() as temporary, \
                patch.dict(os.environ, PIP_TIMEOUT="900", PIP_RETRIES="99", PIP_DISABLE_PIP_VERSION_CHECK="0"):
            original = dict(os.environ)
            result = bootstrap.command([sys.executable, "-c", probe], Path(temporary),
                                       capture=True, seconds=2, download="python")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout),
                             {"PIP_TIMEOUT": "2", "PIP_RETRIES": "0", "PIP_DISABLE_PIP_VERSION_CHECK": "1"})
            self.assertEqual(dict(os.environ), original)

    def test_windows_timeout_targets_tree_and_reaps_original_process(self):
        process = Mock(pid=12345)
        process.poll.return_value = None
        with patch.object(bootstrap.os, "name", "nt"), \
                patch.object(bootstrap.subprocess, "run") as taskkill:
            bootstrap.stop_download(process)
        self.assertEqual(taskkill.call_args.args[0], ["taskkill", "/PID", "12345", "/T", "/F"])
        self.assertEqual(taskkill.call_args.kwargs["timeout"], 5)
        process.kill.assert_called_once_with()
        process.communicate.assert_called_once_with(timeout=5)

    def test_invalid_timeout_is_rejected_before_setup_or_bundle_mutation(self):
        for value in ("0", "-1", "1.5", "86401", "not-seconds"):
            with self.subTest(value=value), redirect_stderr(io.StringIO()), \
                    patch.object(bootstrap, "install") as install, patch.object(offline, "prepare") as prepare:
                for function, arguments in (
                    (bootstrap.main, ["--download-timeout", value]),
                    (offline.main, ["prepare", "--output", "unused", "--download-timeout", value]),
                ):
                    with self.assertRaises(SystemExit) as raised:
                        function(arguments)
                    self.assertEqual(raised.exception.code, 2)
                install.assert_not_called()
                prepare.assert_not_called()

    def test_setup_applies_selected_timeout_only_to_online_acquisition(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            python = bootstrap.python_path(root)
            python.parent.mkdir(parents=True)
            python.touch()
            (root / "workspace.yaml").write_text("schema_version: 1\n")
            (root / ".env.example").write_text("TOKEN=\n")
            for path in ("package.json", "package-lock.json", "core/connectors/workbench/bridge.js"):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}")
            with patch.object(bootstrap, "command", return_value=subprocess.CompletedProcess([], 0)) as command, \
                    patch.object(bootstrap, "npm_command", return_value=["node", "npm-cli.js"]), \
                    redirect_stdout(io.StringIO()):
                _, stages = bootstrap.install(root, root, core_only=False, download_timeout=3)
            network = [call for call in command.call_args_list if call.kwargs.get("download")]
            self.assertEqual([call.kwargs["download"] for call in network], ["python", "npm"])
            self.assertTrue(all(call.kwargs["seconds"] == 3 for call in network))
            self.assertIn("--fetch-retries=0", network[-1].args[0])
            self.assertIn("--fetch-timeout=3000", network[-1].args[0])
            self.assertTrue(all(stage["status"] == "SUCCEEDED" for stage in stages))

    def test_npm_timeout_keeps_installation_incomplete_and_prints_warning(self):
        payload = {"status": "INCOMPLETE", "core_status": "READY", "features": [], "next_actions": []}
        stages = [{"id": "python", "status": "SUCCEEDED"},
                  {"id": "connectors", "status": "INCOMPLETE", "next_action": bootstrap.download_guidance("npm")}]
        out = io.StringIO()
        with patch.object(bootstrap, "source_root", return_value=Path.cwd()), \
                patch.object(bootstrap, "install", return_value=(Path(sys.executable), stages)), \
                patch.object(bootstrap, "doctor", return_value=payload), \
                patch.object(bootstrap, "save_report", return_value=Path("report.md")), redirect_stdout(out):
            self.assertEqual(bootstrap.main(["--download-timeout", "3"]), 1)
        self.assertIn("Warning: locked npm packages", out.getvalue())
        self.assertIn("Installation: INCOMPLETE", out.getvalue())


if __name__ == "__main__":
    unittest.main()
