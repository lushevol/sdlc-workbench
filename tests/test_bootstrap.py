"""Protect setup boundaries with mocked commands and local fixture wheels."""

import base64
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from ai_sdlc_workbench import bootstrap, offline


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
        output = json.dumps(offline.target()) if arguments[-1:] == ["target"] else ""
        return subprocess.CompletedProcess(arguments, 0, stdout=output, stderr="")

    def install(self, workspace=None, *, core_only=True, offline_bundle=None):
        with patch.object(bootstrap, "command", side_effect=self.fake_command), \
                patch.object(bootstrap, "npm_command", return_value=["node", "npm-cli.js"]), \
                patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                redirect_stdout(io.StringIO()):
            result = bootstrap.install(self.root, workspace or self.root, core_only=core_only,
                                       offline_bundle=offline_bundle)
        return result, create

    def bundle(self, *, core_only=False):
        path = self.root.parent / "offline bundle with spaces & symbols^"
        wheelhouse = path / "wheelhouse"
        wheelhouse.mkdir(parents=True)
        wheel = wheelhouse / "ai_sdlc_workbench-0.1.0-py3-none-any.whl"
        wheel.write_bytes(b"Wheel fixture; validation is mocked for install tests.\n")
        (path / "manifest.json").write_bytes(b'{"retained":"manifest fixture"}\n')
        cache = None
        if not core_only:
            cache = path / "npm-cache"
            (cache / "_cacache").mkdir(parents=True)
            (cache / "_cacache/retained-entry").write_bytes(b"Original cache bytes.\n")
        return path, offline.OfflineBundle(wheelhouse, wheel, cache)

    @staticmethod
    def file_bytes(folder):
        return {path.relative_to(folder).as_posix(): path.read_bytes()
                for path in folder.rglob("*") if path.is_file()}

    @staticmethod
    def fixture_wheel(folder, marker):
        folder.mkdir(parents=True)
        wheel = folder / "ai_sdlc_workbench-0.1.0-py3-none-any.whl"
        metadata = "ai_sdlc_workbench-0.1.0.dist-info"
        members = {
            "ai_sdlc_workbench/__init__.py": f"MARKER = {marker!r}\n".encode("utf-8"),
            f"{metadata}/METADATA": b"Metadata-Version: 2.1\nName: ai-sdlc-workbench\nVersion: 0.1.0\n\n",
            f"{metadata}/WHEEL": b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
        }
        records = []
        for name, contents in members.items():
            digest = base64.urlsafe_b64encode(hashlib.sha256(contents).digest()).rstrip(b"=").decode("ascii")
            records.append(f"{name},sha256={digest},{len(contents)}\n")
        records.append(f"{metadata}/RECORD,,\n")
        members[f"{metadata}/RECORD"] = "".join(records).encode("utf-8")
        with zipfile.ZipFile(wheel, "w") as archive:
            for name, contents in members.items():
                archive.writestr(name, contents)
        return wheel

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

    def test_offline_command_ignores_inherited_package_settings_without_mutating_environment(self):
        essentials = {
            "PATH": "approved-runtime-path", "PATHEXT": ".EXE;.CMD", "SYSTEMROOT": r"C:\Windows",
            "WINDIR": r"C:\Windows", "COMSPEC": r"C:\Windows\System32\cmd.exe",
            "TEMP": str(self.root / "temp"), "TMP": str(self.root / "tmp"),
            "TMPDIR": str(self.root / "tmpdir"), "USERPROFILE": str(self.root / "profile"),
            "APPDATA": str(self.root / "appdata"), "LOCALAPPDATA": str(self.root / "localappdata"),
            "HOME": str(self.root / "home"), "LANG": "en_US.UTF-8",
        }
        inherited_settings = {
            "PIP_REQUIREMENT": "remote-requirements.txt", "PIP_FIND_LINKS": "https://packages.example/wheels",
            "PIP_INDEX_URL": "https://credential@packages.example/simple", "PIP_CONFIG_FILE": "private-pip.ini",
            "PIP_DISABLE_PIP_VERSION_CHECK": "0", "NPM_CONFIG_REGISTRY": "https://credential@packages.example/",
            "npm_config_//packages.example/:_authToken": "private-token", "npm_config_userconfig": "private.npmrc",
            "NODE_OPTIONS": "--require private-module.js", "PYTHONPATH": "unapproved-python-path",
            "PYTHONHOME": "unapproved-python-home",
        }
        with patch.dict(os.environ, {**essentials, **inherited_settings}, clear=True):
            original = dict(os.environ)
            with patch.object(bootstrap.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
                bootstrap.command([str(self.python), "-m", "pip", "check"], self.root,
                                  python=self.python, offline=True)
            child_environment = run.call_args.kwargs["env"]
            self.assertEqual(dict(os.environ), original)

        self.assertEqual(child_environment["PATH"], str(self.python.parent) + os.pathsep + essentials["PATH"])
        for name, value in essentials.items():
            if name != "PATH":
                self.assertEqual(child_environment[name], value)
        self.assertEqual({name for name in child_environment if name.upper().startswith("PIP_")},
                         {"PIP_CONFIG_FILE", "PIP_DISABLE_PIP_VERSION_CHECK"})
        self.assertEqual(child_environment["PIP_CONFIG_FILE"], os.devnull)
        self.assertEqual(child_environment["PIP_DISABLE_PIP_VERSION_CHECK"], "1")
        self.assertFalse(any(name.upper().startswith("NPM_CONFIG_") for name in child_environment))
        for name in ("NODE_OPTIONS", "PYTHONPATH", "PYTHONHOME"):
            self.assertNotIn(name, child_environment)

    def test_offline_install_uses_local_wheels_and_copies_npm_cache_before_writes(self):
        bundle_path, bundle = self.bundle()
        before = self.file_bytes(bundle_path)
        copied_caches = []

        def install_command(arguments, root, **kwargs):
            result = self.fake_command(arguments, root, **kwargs)
            if "ci" in arguments:
                self.assertIn("--offline", arguments)
                self.assertTrue(kwargs["offline"])
                cache = Path(arguments[arguments.index("--cache") + 1])
                user_config = Path(arguments[arguments.index("--userconfig") + 1])
                global_config = Path(arguments[arguments.index("--globalconfig") + 1])
                self.assertNotEqual(user_config, global_config)
                self.assertEqual(user_config.read_bytes(), b"")
                self.assertEqual(global_config.read_bytes(), b"")
                self.assertEqual(user_config.parent, cache.parent)
                self.assertEqual(global_config.parent, cache.parent)
                self.assertNotEqual(cache, bundle.npm_cache)
                self.assertEqual((cache / "_cacache/retained-entry").read_bytes(), b"Original cache bytes.\n")
                (cache / "_cacache/retained-entry").write_bytes(b"npm updated its index.\n")
                (cache / "new-npm-cache-file").write_bytes(b"npm cache mutation.\n")
                copied_caches.append(cache)
            return result

        with patch.object(offline, "validate_bundle", return_value=bundle) as validate, \
                patch.object(bootstrap, "command", side_effect=install_command), \
                patch.object(bootstrap, "npm_command", return_value=["node", "npm-cli.js"]), \
                patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                redirect_stdout(io.StringIO()):
            _, stages = bootstrap.install(self.root, self.root, core_only=False, offline_bundle=bundle_path)

        validate.assert_called_once_with(self.root, bundle_path, core_only=False)
        create.assert_not_called()
        pip_install = [arguments for arguments, _, _ in self.calls if arguments[1:4] == ["-m", "pip", "install"]]
        expected = [str(self.python), "-m", "pip", "install", "--no-index", "--find-links", str(bundle.wheelhouse),
                    "--only-binary=:all:", "--no-build-isolation", "--no-cache-dir", "--force-reinstall",
                    str(bundle.workbench_wheel) + "[release-clinic]"]
        if os.name == "nt":
            expected.append("pywin32>=305")
        self.assertEqual(pip_install, [expected])
        npm_install = [arguments for arguments, _, _ in self.calls if "ci" in arguments]
        self.assertEqual(len(npm_install), 1)
        self.assertEqual(npm_install[0], ["node", "npm-cli.js", "ci", "--ignore-scripts", "--no-audit", "--no-fund",
                                          "--offline", "--cache", str(copied_caches[0]),
                                          "--userconfig", str(copied_caches[0].parent / "user.npmrc"),
                                          "--globalconfig", str(copied_caches[0].parent / "global.npmrc")])
        self.assertEqual(self.file_bytes(bundle_path), before)
        self.assertFalse(copied_caches[0].exists())
        self.assertEqual(stages, [{"id": "python", "status": "SUCCEEDED"},
                                  {"id": "connectors", "status": "SUCCEEDED"}])

    def test_offline_install_refreshes_same_version_runtime_from_selected_local_wheel(self):
        original = self.fixture_wheel(self.root.parent / "original-wheel", "installed-old-runtime")
        selected = self.fixture_wheel(self.root.parent / "selected-wheel", "selected-refreshed-runtime")
        (self.root / "core/offline.py").write_bytes(Path(offline.__file__).read_bytes())
        (self.root / "core/bootstrap.py").write_bytes(Path(bootstrap.__file__).read_bytes())
        self.python.unlink()
        with patch.dict(os.environ, bootstrap.environment(offline=True), clear=True):
            bootstrap.venv.EnvBuilder(with_pip=True).create(self.root / ".venv")

        installed = bootstrap.command(
            [str(self.python), "-m", "pip", "install", "--no-index", "--no-deps", "--no-cache-dir", str(original)],
            self.root, python=self.python, offline=True,
        )
        self.assertEqual(installed.returncode, 0)
        inspect = [str(self.python), "-c", "import ai_sdlc_workbench; print(ai_sdlc_workbench.MARKER)"]
        before = bootstrap.command(inspect, self.root, capture=True, python=self.python, offline=True)
        self.assertEqual(before.returncode, 0)
        self.assertEqual(before.stdout.strip(), "installed-old-runtime")

        bundle = offline.OfflineBundle(selected.parent, selected, None)
        with patch.object(offline, "validate_bundle", return_value=bundle), redirect_stdout(io.StringIO()):
            python, stages = bootstrap.install(self.root, self.root, core_only=True, offline_bundle=selected.parent)

        after = bootstrap.command(inspect, self.root, capture=True, python=self.python, offline=True)
        self.assertEqual(after.returncode, 0)
        self.assertEqual(after.stdout.strip(), "selected-refreshed-runtime")
        self.assertEqual(python, self.python)
        self.assertEqual(stages, [{"id": "python", "status": "SUCCEEDED"}])

    def test_invalid_offline_bundle_fails_before_environment_or_installer_changes(self):
        bundle_path = self.root.parent / "invalid-offline-bundle"
        bundle_path.mkdir()
        retained = bundle_path / "retain-me"
        retained.write_bytes(b"Preserve incomplete delivery.\n")
        self.python.unlink()
        with patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                patch.object(bootstrap, "npm_command") as npm, \
                patch.object(bootstrap, "command") as command, \
                patch.object(bootstrap, "ensure_environment_file") as ensure:
            with self.assertRaisesRegex(bootstrap.SetupError, "manifest is invalid or incomplete"):
                bootstrap.install(self.root, self.root, core_only=False, offline_bundle=bundle_path)
        create.assert_not_called()
        npm.assert_not_called()
        command.assert_not_called()
        ensure.assert_not_called()
        self.assertEqual(self.file_bytes(bundle_path), {"retain-me": b"Preserve incomplete delivery.\n"})
        self.assertFalse((self.root / ".env").exists())
        self.assertFalse(self.python.exists())

    def test_offline_install_rejects_selected_venv_python_identity_before_pip(self):
        bundle_path, bundle = self.bundle(core_only=True)
        for field in ("cpu", "abi", "platform"):
            with self.subTest(field=field):
                self.calls.clear()
                different = {**offline.target(), field: "different-platform-identity"}

                def identity_result(arguments, root, **kwargs):
                    result = self.fake_command(arguments, root, **kwargs)
                    if arguments[-1:] == ["target"]:
                        return subprocess.CompletedProcess(arguments, 0, stdout=json.dumps(different), stderr="")
                    return result

                with patch.object(offline, "validate_bundle", return_value=bundle), \
                        patch.object(bootstrap, "command", side_effect=identity_result), \
                        patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                        patch.object(bootstrap, "ensure_environment_file") as ensure, \
                        redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(bootstrap.SetupError, "existing .venv differs from the bundle Python"):
                        bootstrap.install(self.root, self.root, core_only=True, offline_bundle=bundle_path)

                create.assert_not_called()
                ensure.assert_not_called()
                self.assertEqual(len(self.calls), 2)
                self.assertEqual(self.calls[0][0][:2], [str(self.python), "-c"])
                self.assertEqual(self.calls[1][0], [str(self.python), str(self.root / "core/offline.py"), "target"])
                self.assertTrue(self.calls[1][2]["capture"])
                self.assertTrue(all(kwargs["python"] == self.python for _, _, kwargs in self.calls))
                self.assertTrue(all(kwargs["offline"] for _, _, kwargs in self.calls))
                self.assertFalse((self.root / ".env").exists())

    def test_failed_offline_python_install_never_retries_with_a_registry(self):
        bundle_path, bundle = self.bundle(core_only=True)

        def failed_pip(arguments, root, **kwargs):
            result = self.fake_command(arguments, root, **kwargs)
            return subprocess.CompletedProcess(arguments, 1, stdout="", stderr="") if "install" in arguments else result

        with patch.object(offline, "validate_bundle", return_value=bundle), \
                patch.object(bootstrap, "command", side_effect=failed_pip), \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(bootstrap.SetupError, "online fallback is disabled"):
                bootstrap.install(self.root, self.root, core_only=True, offline_bundle=bundle_path)

        installs = [arguments for arguments, _, _ in self.calls if "install" in arguments]
        self.assertEqual(len(installs), 1)
        self.assertIn("--no-index", installs[0])
        self.assertIn("--only-binary=:all:", installs[0])
        self.assertIn(str(bundle.workbench_wheel), installs[0])
        self.assertNotIn(str(self.root), installs[0])
        self.assertFalse((self.root / ".env").exists())

    def test_failed_offline_npm_install_reports_incomplete_without_online_retry(self):
        bundle_path, bundle = self.bundle()
        before = self.file_bytes(bundle_path)

        def failed_npm(arguments, root, **kwargs):
            result = self.fake_command(arguments, root, **kwargs)
            return subprocess.CompletedProcess(arguments, 1, stdout="", stderr="") if "ci" in arguments else result

        with patch.object(offline, "validate_bundle", return_value=bundle), \
                patch.object(bootstrap, "command", side_effect=failed_npm), \
                patch.object(bootstrap, "npm_command", return_value=["node", "npm-cli.js"]), \
                redirect_stdout(io.StringIO()):
            _, stages = bootstrap.install(self.root, self.root, core_only=False, offline_bundle=bundle_path)

        installs = [arguments for arguments, _, _ in self.calls if "ci" in arguments]
        self.assertEqual(len(installs), 1)
        self.assertIn("--offline", installs[0])
        self.assertEqual(stages[-1]["status"], "INCOMPLETE")
        self.assertIn("online fallback is disabled", stages[-1]["next_action"])
        self.assertEqual(self.file_bytes(bundle_path), before)

    def test_main_selects_explicit_bundle_before_auto_detected_bundle(self):
        selected, bundle = self.bundle(core_only=True)
        (self.root / "offline-bundle").mkdir()
        payload = {"features": [], "core_status": "READY", "status": "READY", "next_actions": []}
        with patch.object(bootstrap, "source_root", return_value=self.root), \
                patch.object(offline, "validate_bundle", return_value=bundle) as validate, \
                patch.object(bootstrap, "command", side_effect=self.fake_command), \
                patch.object(bootstrap, "doctor", return_value=payload) as doctor, \
                patch.object(bootstrap, "save_report", return_value=self.root / "report.md"), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(bootstrap.main(["--core-only", "--offline-bundle", str(selected)]), 0)
        validate.assert_called_once_with(self.root, selected, core_only=True)
        doctor.assert_called_once_with(self.python, self.root, self.root, core_only=True)

    def test_main_auto_detects_local_offline_bundle(self):
        prepared, bundle = self.bundle(core_only=True)
        detected = self.root / "offline-bundle"
        prepared.rename(detected)
        bundle = offline.OfflineBundle(detected / "wheelhouse", detected / "wheelhouse" / bundle.workbench_wheel.name, None)
        payload = {"features": [], "core_status": "READY", "status": "READY", "next_actions": []}
        with patch.object(bootstrap, "source_root", return_value=self.root), \
                patch.object(offline, "validate_bundle", return_value=bundle) as validate, \
                patch.object(bootstrap, "command", side_effect=self.fake_command), \
                patch.object(bootstrap, "doctor", return_value=payload), \
                patch.object(bootstrap, "save_report", return_value=self.root / "report.md"), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(bootstrap.main(["--core-only"]), 0)
        validate.assert_called_once_with(self.root, detected, core_only=True)
        installs = [arguments for arguments, _, _ in self.calls if "install" in arguments]
        self.assertEqual(len(installs), 1)
        self.assertIn("--no-index", installs[0])

    def test_main_rejects_broken_auto_detected_bundle_without_online_fallback(self):
        detected = self.root / "offline-bundle"
        try:
            detected.symlink_to(self.root.parent / "missing-bundle", target_is_directory=True)
        except OSError:
            self.skipTest("This platform does not permit directory symlinks.")
        errors = io.StringIO()
        with patch.object(bootstrap, "source_root", return_value=self.root), \
                patch.object(bootstrap, "command") as command, \
                patch.object(bootstrap, "npm_command") as npm, \
                patch.object(bootstrap.venv.EnvBuilder, "create") as create, \
                patch.object(bootstrap, "doctor") as doctor, \
                patch.object(bootstrap, "save_report") as save, \
                redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(bootstrap.main([]), 1)
        command.assert_not_called()
        npm.assert_not_called()
        create.assert_not_called()
        doctor.assert_not_called()
        save.assert_not_called()
        self.assertIn("offline bundle directory", errors.getvalue())
        self.assertTrue(detected.is_symlink())
        self.assertFalse((self.root / ".env").exists())

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
