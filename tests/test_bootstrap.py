"""Protect setup boundaries without installing packages or accessing a network."""

from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import bootstrap


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="workbench-setup-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "source with spaces & metacharacters^$"
        self.root.mkdir()
        (self.root / "core/connectors/workbench").mkdir(parents=True)
        for relative in ("pyproject.toml", "core/cli.py", "package.json", "package-lock.json",
                         "core/connectors/workbench/bridge.js"):
            (self.root / relative).write_text("{}\n", encoding="utf-8")
        self.template = self.root / ".env.example"
        self.template.write_bytes(b"TOKEN=\n# Company configuration goes here.\r\n")
        (self.root / "workspace.yaml").write_text("schema_version: 1\n", encoding="utf-8")
        self.python = bootstrap.python_path(self.root)
        self.python.parent.mkdir(parents=True)
        self.python.write_bytes(b"Existing environment executable.\n")
        self.calls = []

    def fake_command(self, arguments, root, **kwargs):
        self.calls.append((list(arguments), root, kwargs))
        if "init" in arguments:
            workspace = Path(arguments[-1])
            workspace.mkdir(parents=True, exist_ok=True)
            (workspace / "workspace.yaml").write_text("schema_version: 1\n", encoding="utf-8")
        return subprocess.CompletedProcess(arguments, 0, stdout="", stderr="")

    def install(self, workspace=None, *, core_only=True):
        with patch.object(bootstrap, "command", side_effect=self.fake_command), \
                patch.object(bootstrap, "npm_command", return_value=["node", "npm-cli.js"]), \
                patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                redirect_stdout(io.StringIO()):
            result = bootstrap.install(self.root, workspace or self.root, core_only=core_only)
        return result, create

    def test_environment_file_creation_preserves_exact_existing_bytes(self):
        destination = self.root / ".env"
        bootstrap.ensure_environment_file(self.root, self.template)
        self.assertEqual(destination.read_bytes(), self.template.read_bytes())
        private = b"TOKEN=private\x00bytes\r\n\xff"
        destination.write_bytes(private)
        bootstrap.ensure_environment_file(self.root, self.root / "missing-template")
        self.assertEqual(destination.read_bytes(), private)

    def test_environment_file_preserves_existing_and_dangling_symlinks(self):
        destination = self.root / ".env"
        target = self.root / "private-company-configuration"
        target.write_bytes(b"PRIVATE_TOKEN=retain\r\n")
        try:
            destination.symlink_to(target)
        except OSError:
            self.skipTest("This platform does not permit file symlinks.")
        bootstrap.ensure_environment_file(self.root, self.template)
        self.assertTrue(destination.is_symlink())
        self.assertEqual(target.read_bytes(), b"PRIVATE_TOKEN=retain\r\n")
        target.unlink()
        bootstrap.ensure_environment_file(self.root, self.template)
        self.assertTrue(destination.is_symlink())
        self.assertFalse(target.exists())

    def test_incomplete_connector_checkout_fails_before_environment_changes(self):
        (self.root / "core/connectors/workbench/bridge.js").unlink()
        self.python.unlink()
        with patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                patch.object(bootstrap, "npm_command") as npm, \
                patch.object(bootstrap, "command") as command:
            with self.assertRaisesRegex(bootstrap.SetupError, "Connector source is missing"):
                bootstrap.install(self.root, self.root, core_only=False)
        create.assert_not_called()
        npm.assert_not_called()
        command.assert_not_called()
        self.assertFalse((self.root / ".env").exists())

    def test_existing_environment_is_reused_and_initialized_workspace_is_preserved(self):
        marker = self.python.parent / "retain-installed-files"
        marker.write_bytes(b"Do not recreate this environment.\n")
        before = (self.root / "workspace.yaml").read_bytes()
        (python, stages), create = self.install()
        create.assert_not_called()
        self.assertEqual(python, self.python)
        self.assertEqual(stages, [{"id": "python", "status": "SUCCEEDED"}])
        self.assertEqual(marker.read_bytes(), b"Do not recreate this environment.\n")
        self.assertEqual((self.root / "workspace.yaml").read_bytes(), before)
        self.assertFalse(any("init" in arguments for arguments, _, _ in self.calls))
        self.assertTrue(all(arguments[0] == str(self.python) for arguments, _, _ in self.calls))

    def test_incomplete_existing_environment_is_not_recreated(self):
        self.python.unlink()
        with patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                patch.object(bootstrap, "command") as command:
            with self.assertRaisesRegex(bootstrap.SetupError, "existing .venv is incomplete"):
                bootstrap.install(self.root, self.root, core_only=True)
        create.assert_not_called()
        command.assert_not_called()

    def test_nonempty_uninitialized_workspace_fails_before_mutation(self):
        workspace = self.root.parent / "independent-workspace"
        workspace.mkdir()
        retained = workspace / "business-file.txt"
        retained.write_bytes(b"Preserve business content.\n")
        with patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                patch.object(bootstrap, "npm_command") as npm, \
                patch.object(bootstrap, "command") as command:
            with self.assertRaisesRegex(bootstrap.SetupError, "no workspace configuration"):
                bootstrap.install(self.root, workspace, core_only=False)
        create.assert_not_called()
        npm.assert_not_called()
        command.assert_not_called()
        self.assertEqual(sorted(path.name for path in workspace.iterdir()), ["business-file.txt"])
        self.assertEqual(retained.read_bytes(), b"Preserve business content.\n")

    def test_empty_explicit_workspace_is_initialized_only_once(self):
        workspace = self.root.parent / "new workspace"
        workspace.mkdir()
        self.install(workspace)
        self.assertTrue((workspace / "workspace.yaml").is_file())
        self.assertEqual((workspace / ".env").read_bytes(), self.template.read_bytes())
        self.install(workspace)
        init = [arguments for arguments, _, _ in self.calls if "init" in arguments]
        self.assertEqual(init, [[str(self.python), "-m", "ai_sdlc_workbench", "init", str(workspace)]])

    def test_platform_environment_executable_paths(self):
        self.assertEqual(bootstrap.python_path(self.root, windows=True),
                         self.root / ".venv/Scripts/python.exe")
        self.assertEqual(bootstrap.python_path(self.root, windows=False),
                         self.root / ".venv/bin/python")

    def test_windows_npm_uses_javascript_and_literal_subprocess_arguments(self):
        node = self.root / "approved Node & tools^!" / "node.exe"
        node.parent.mkdir()
        node.write_bytes(b"Executable fixture.")
        cli = node.parent / "node_modules/npm/bin/npm-cli.js"
        cli.parent.mkdir(parents=True)
        cli.write_text("// npm entry point fixture\n", encoding="utf-8")
        shim = node.parent / "npm.cmd"
        shim.write_text("@echo off\n", encoding="utf-8")
        windows_os = SimpleNamespace(name="nt", environ=dict(os.environ), pathsep=os.pathsep)
        version = subprocess.CompletedProcess([], 0, stdout="v24.0.0\n")
        installed = subprocess.CompletedProcess([], 0, stdout="")
        with patch.object(bootstrap, "os", windows_os), \
                patch.object(bootstrap.shutil, "which", side_effect=lambda name: str(node if name == "node" else shim)), \
                patch.object(bootstrap.subprocess, "run", side_effect=[version, installed]) as run:
            npm = bootstrap.npm_command(self.root)
            bootstrap.command([*npm, "ci", "--ignore-scripts", "--no-audit", "--no-fund"], self.root)
        self.assertEqual(npm, [str(node), str(cli)])
        self.assertEqual(run.call_args.args[0],
                         [str(node), str(cli), "ci", "--ignore-scripts", "--no-audit", "--no-fund"])
        self.assertTrue(all(call.kwargs["shell"] is False for call in run.call_args_list))
        self.assertTrue(all(call.kwargs["cwd"] == self.root for call in run.call_args_list))

    def test_npm_cli_symlink_resolves_a_unix_node_installation(self):
        prefix = self.root / "approved-node"
        node = prefix / "bin/node"
        cli = prefix / "lib/node_modules/npm/bin/npm-cli.js"
        node.parent.mkdir(parents=True)
        cli.parent.mkdir(parents=True)
        node.write_bytes(b"Executable fixture.")
        cli.write_text("// npm entry point fixture\n", encoding="utf-8")
        shim = node.parent / "npm"
        try:
            shim.symlink_to(cli)
        except OSError:
            self.skipTest("This platform does not permit file symlinks.")
        unix_os = SimpleNamespace(name="posix")
        with patch.object(bootstrap, "os", unix_os), \
                patch.object(bootstrap.shutil, "which", side_effect=lambda name: str(node if name == "node" else shim)), \
                patch.object(bootstrap, "command", return_value=subprocess.CompletedProcess([], 0, stdout="v24.0.0\n")):
            self.assertEqual(bootstrap.npm_command(self.root), [str(node), str(cli)])

    def test_check_does_not_install_initialize_create_environment_or_save_report(self):
        payload = {"features": [], "core_status": "READY", "status": "INCOMPLETE", "next_actions": []}
        with patch.object(bootstrap, "source_root", return_value=self.root), \
                patch.object(bootstrap, "doctor", return_value=payload) as doctor, \
                patch.object(bootstrap, "install") as install, \
                patch.object(bootstrap, "ensure_environment_file") as ensure, \
                patch.object(bootstrap, "save_report") as save, \
                patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                redirect_stdout(io.StringIO()):
            self.assertEqual(bootstrap.main(["--check", "--core-only"]), 1)
        doctor.assert_called_once_with(self.python, self.root, self.root, core_only=True)
        install.assert_not_called()
        ensure.assert_not_called()
        save.assert_not_called()
        create.assert_not_called()
        self.assertFalse((self.root / ".env").exists())
        self.assertFalse((self.root / ".workbench").exists())

    def test_failed_install_diagnostics_never_reach_stdout_or_stderr(self):
        private = "PRIVATE_COMPANY_INDEX_CREDENTIAL"

        def subprocess_result(arguments, **kwargs):
            if "pip" in arguments:
                return subprocess.CompletedProcess(arguments, 1, stdout=private, stderr=private)
            return subprocess.CompletedProcess(arguments, 0, stdout="", stderr="")

        out, err = io.StringIO(), io.StringIO()
        with patch.object(bootstrap, "source_root", return_value=self.root), \
                patch.object(bootstrap.subprocess, "run", side_effect=subprocess_result) as run, \
                redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(bootstrap.main(["--core-only"]), 1)
        self.assertNotIn(private, out.getvalue() + err.getvalue())
        self.assertIn("Python package installation failed", err.getvalue())
        self.assertTrue(all(call.kwargs["stdout"] == subprocess.DEVNULL and
                            call.kwargs["stderr"] == subprocess.DEVNULL for call in run.call_args_list))
        self.assertFalse((self.root / ".env").exists())
        self.assertFalse((self.root / ".workbench").exists())

    def test_doctor_failure_does_not_print_malformed_private_output(self):
        private = "PRIVATE_COMPANY_INDEX_CREDENTIAL"
        with patch.object(bootstrap, "command", return_value=subprocess.CompletedProcess([], 1, stdout=private)), \
                self.assertRaisesRegex(bootstrap.SetupError, "setup checker is unavailable") as raised:
            bootstrap.doctor(self.python, self.root, self.root, core_only=True)
        self.assertNotIn(private, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
