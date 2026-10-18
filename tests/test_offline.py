"""Protect offline dependency integrity, platform matching, and preparation boundaries."""

from contextlib import redirect_stdout
import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from ai_sdlc_workbench import offline
from ai_sdlc_workbench import bootstrap


class OfflineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="workbench-offline-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "source with spaces & metacharacters^$"
        self.root.mkdir()
        for name in offline._ROOT_INPUTS:
            (self.root / name).write_text("{}\n", encoding="utf-8")
        (self.root / "scaffold.json").write_text(json.dumps({"paths": ["README.md", ".agents/skills"]}), encoding="utf-8")
        for name in ("README.md", ".agents/skills/example/SKILL.md", "core/cli.py", "core/connectors/workbench/bridge.js",
                     "core/connectors/packages/example/package.json"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Source fixture.\n", encoding="utf-8")
        self.tarballs = {"https://registry.example/optional-win.tgz": b"Windows native package",
                         "https://registry.example/optional-mac.tgz": b"macOS native package"}
        records = {"": {}, "core/connectors/packages/example": {},
                   "node_modules/example": {"resolved": "core/connectors/packages/example", "link": True}}
        for index, (url, content) in enumerate(self.tarballs.items()):
            records[f"node_modules/optional-{index}"] = {
                "resolved": url, "integrity": self.integrity(content), "optional": True,
                "os": ["win32" if index == 0 else "darwin"], "cpu": ["x64"], "hasInstallScript": True}
        records["node_modules/duplicate"] = records["node_modules/optional-0"].copy()
        self.lock = {"lockfileVersion": 3, "packages": records}
        self.write_lock()
        self.output = self.base / "bundle"
        self.calls = []

    @staticmethod
    def integrity(content):
        return "sha512-" + base64.b64encode(hashlib.sha512(content).digest()).decode("ascii")

    def write_lock(self):
        (self.root / "package-lock.json").write_text(json.dumps(self.lock), encoding="utf-8")

    @staticmethod
    def wheel(folder, *, name="ai_sdlc_workbench", requirement="PyYAML==6.0.2", tag="py3-none-any"):
        path = folder / f"{name}-0.1.0-{tag}.whl"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(f"{name}-0.1.0.dist-info/METADATA",
                             f"Metadata-Version: 2.1\nName: {name}\nVersion: 0.1.0\n"
                             + (f"Requires-Dist: {requirement}\n" if requirement else "") + "\n")
            archive.writestr(f"{name}-0.1.0.dist-info/WHEEL",
                             f"Wheel-Version: 1.0\nGenerator: local-fixture\nRoot-Is-Purelib: true\nTag: {tag}\n\n")
            archive.writestr(f"{name}-0.1.0.dist-info/RECORD", "")
        return path

    def cache_tarball(self, cache, content):
        digest = hashlib.sha512(content).hexdigest()
        path = cache / "_cacache/content-v2/sha512" / digest[:2] / digest[2:4] / digest[4:]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        index = cache / "_cacache/index-v5/entry"
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text("Cache index fixture.\n", encoding="utf-8")

    def command(self, arguments, root, **kwargs):
        self.calls.append(list(arguments))
        if "wheel" in arguments:
            folder = Path(arguments[arguments.index("--wheel-dir") + 1])
            self.wheel(folder)
        elif "download" in arguments:
            folder = Path(arguments[arguments.index("--dest") + 1])
            self.wheel(folder, name="PyYAML", requirement="typing-extensions>=4")
        elif "add" in arguments:
            cache = Path(arguments[arguments.index("--cache") + 1])
            self.cache_tarball(cache, self.tarballs[arguments[arguments.index("add") + 1]])
            logs = cache / "_logs"
            logs.mkdir(exist_ok=True)
            (logs / "debug.log").write_text("PRIVATE_NPM_LOG", encoding="utf-8")
            (cache / ".npmrc").write_text("PRIVATE_NPM_CONFIG", encoding="utf-8")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    def prepare(self, *, core_only=False):
        with patch.object(offline, "command", side_effect=self.command), \
                patch.object(offline, "npm_command", return_value=["node", "npm-cli.js"]) as npm, \
                redirect_stdout(io.StringIO()):
            result = offline.prepare(self.root, self.output, core_only=core_only)
        return result, npm

    def manifest(self):
        return json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))

    def update_manifest(self, manifest):
        (self.output / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def rehash(self):
        manifest = self.manifest()
        manifest["files"] = offline._bundle_files(self.output)
        self.update_manifest(manifest)

    def test_prepare_caches_all_native_variants_without_scripts_and_excludes_private_cache_files(self):
        result, _ = self.prepare()
        self.assertEqual(result, self.output)
        bundle = offline.validate_bundle(self.root, self.output)
        self.assertEqual(bundle.wheelhouse, self.output / "wheelhouse")
        self.assertEqual(bundle.workbench_wheel.name, "ai_sdlc_workbench-0.1.0-py3-none-any.whl")
        self.assertEqual(bundle.npm_cache, self.output / "npm-cache")
        add = [call for call in self.calls if "add" in call]
        self.assertEqual({call[call.index("add") + 1] for call in add}, set(self.tarballs))
        self.assertEqual(len(add), len(self.tarballs))
        for call in add:
            self.assertTrue({"--ignore-scripts", "--no-audit", "--no-fund"}.issubset(call))
        build = next(call for call in self.calls if "wheel" in call)
        self.assertIn("--no-deps", build)
        download = next(call for call in self.calls if "download" in call)
        self.assertIn("--only-binary=:all:", download)
        self.assertTrue(any(item.endswith(".whl[release-clinic]") for item in download))
        verification = [call for call in self.calls if "download" in call and "--no-index" in call]
        self.assertEqual(len(verification), 1)
        self.assertIn("--no-cache-dir", verification[0])
        self.assertFalse((bundle.npm_cache / "_logs").exists())
        self.assertFalse((bundle.npm_cache / ".npmrc").exists())
        self.assertFalse((bundle.npm_cache / "_cacache/index-v5").exists())
        self.assertNotIn("PRIVATE_NPM", (self.output / "manifest.json").read_text(encoding="utf-8"))

    def test_core_bundle_does_not_probe_npm_or_include_clinic_and_windows_preparation_includes_outlook(self):
        _, npm = self.prepare(core_only=True)
        npm.assert_not_called()
        bundle = offline.validate_bundle(self.root, self.output, core_only=True)
        self.assertIsNone(bundle.npm_cache)
        self.assertFalse(any("release-clinic" in argument for call in self.calls for argument in call))
        self.output = self.base / "windows-bundle"
        self.calls.clear()
        with patch.object(offline.platform, "system", return_value="Windows"):
            self.prepare()
            offline.validate_bundle(self.root, self.output)
        download = next(call for call in self.calls if "download" in call)
        self.assertIn("pywin32>=305", download)

    def test_validation_never_runs_commands_or_changes_files(self):
        self.prepare()
        before = offline._bundle_files(self.output)
        source_before = offline.source_fingerprint(self.root)
        with patch.object(offline, "command", side_effect=AssertionError("No process is allowed")), \
                patch.object(offline, "npm_command", side_effect=AssertionError("No process is allowed")):
            offline.validate_bundle(self.root, self.output)
        self.assertEqual(offline._bundle_files(self.output), before)
        self.assertEqual(offline.source_fingerprint(self.root), source_before)
        self.assertFalse((self.root / ".venv").exists())

    def test_target_mismatch_rejects_os_cpu_minor_bitness_implementation_and_abi(self):
        self.prepare()
        original = self.manifest()
        replacements = {"system": "OtherOS", "cpu": "other", "python": [3, 99], "bits": 17,
                        "implementation": "other", "abi": "other", "platform": "other"}
        for key, value in replacements.items():
            with self.subTest(key=key):
                manifest = json.loads(json.dumps(original))
                manifest["target"][key] = value
                self.update_manifest(manifest)
                with self.assertRaisesRegex(offline.SetupError, "operating system, CPU"):
                    offline.validate_bundle(self.root, self.output)

    def test_source_fingerprint_covers_runtime_lock_and_scaffold_but_ignores_machine_state(self):
        baseline = offline.source_fingerprint(self.root)
        for relative in (".env", "workspace.local.yaml", "TODO", "core/__pycache__/private.pyc",
                         "core/connectors/packages/example/node_modules/private.js",
                         "core/connectors/packages/example/coverage/report.html"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("private local data", encoding="utf-8")
        self.assertEqual(offline.source_fingerprint(self.root), baseline)
        for relative in ("core/cli.py", "package-lock.json", ".agents/skills/example/SKILL.md", "README.md"):
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_bytes()
                path.write_bytes(original + b"changed")
                self.assertNotEqual(offline.source_fingerprint(self.root), baseline)
                path.write_bytes(original)

    def test_stale_source_and_wrong_profile_fail_without_modification(self):
        self.prepare()
        with self.assertRaisesRegex(offline.SetupError, "profile"):
            offline.validate_bundle(self.root, self.output, core_only=True)
        (self.root / "core/cli.py").write_text("Changed runtime", encoding="utf-8")
        with self.assertRaisesRegex(offline.SetupError, "source checkout"):
            offline.validate_bundle(self.root, self.output)
        self.assertFalse((self.root / ".venv").exists())

    def test_missing_or_corrupt_wheels_fail_manifest_hash_checks(self):
        self.prepare(core_only=True)
        bundle = offline.validate_bundle(self.root, self.output, core_only=True)
        original = bundle.workbench_wheel.read_bytes()
        bundle.workbench_wheel.write_bytes(original + b"changed")
        with self.assertRaisesRegex(offline.SetupError, "missing or changed"):
            offline.validate_bundle(self.root, self.output, core_only=True)
        bundle.workbench_wheel.unlink()
        with self.assertRaisesRegex(offline.SetupError, "missing or changed"):
            offline.validate_bundle(self.root, self.output, core_only=True)

    def test_no_sdists_or_other_unlisted_files_are_accepted(self):
        self.prepare(core_only=True)
        foreign = self.output / "wheelhouse/source.tar.gz"
        foreign.write_bytes(b"No target builds")
        with self.assertRaisesRegex(offline.SetupError, "unexpected files"):
            offline.validate_bundle(self.root, self.output, core_only=True)
        foreign.unlink()
        (self.output / "private.env").write_text("private", encoding="utf-8")
        with self.assertRaisesRegex(offline.SetupError, "unexpected files"):
            offline.validate_bundle(self.root, self.output, core_only=True)

    def test_direct_url_transitive_requirements_are_rejected_even_with_matching_file_hash(self):
        self.prepare(core_only=True)
        self.wheel(self.output / "wheelhouse", name="PyYAML", requirement="other @ https://private.example/package.whl")
        self.rehash()
        with self.assertRaisesRegex(offline.SetupError, "direct URL") as context:
            offline.validate_bundle(self.root, self.output, core_only=True)
        self.assertNotIn("private.example", str(context.exception))

    def test_npm_cache_must_contain_every_locked_optional_tarball_with_correct_integrity(self):
        self.prepare()
        content = next(iter(self.tarballs.values()))
        digest = hashlib.sha512(content).hexdigest()
        path = self.output / "npm-cache/_cacache/content-v2/sha512" / digest[:2] / digest[2:4] / digest[4:]
        path.write_bytes(b"Corrupt tarball")
        self.rehash()
        with self.assertRaisesRegex(offline.SetupError, "npm cache is incomplete or corrupt"):
            offline.validate_bundle(self.root, self.output)
        path.unlink()
        self.rehash()
        with self.assertRaisesRegex(offline.SetupError, "npm cache is incomplete or corrupt"):
            offline.validate_bundle(self.root, self.output)

    def test_credentials_and_unlocked_sources_fail_before_preparation_writes_or_processes(self):
        originals = self.lock["packages"]["node_modules/optional-0"].copy()
        for url in ("https://user:PRIVATE_TOKEN@registry.example/a.tgz", "https://registry.example/a.tgz?token=PRIVATE_TOKEN",
                    "http://registry.example/a.tgz", "git+https://registry.example/repo", "file:../package"):
            with self.subTest(url=url):
                self.lock["packages"]["node_modules/optional-0"] = {**originals, "resolved": url}
                self.write_lock()
                with patch.object(offline, "npm_command", return_value=["node", "npm-cli.js"]), \
                        patch.object(offline, "command") as execute:
                    with self.assertRaisesRegex(offline.SetupError, "credential-free") as context:
                        offline.prepare(self.root, self.output)
                execute.assert_not_called()
                self.assertFalse(self.output.exists())
                self.assertNotIn("PRIVATE_TOKEN", str(context.exception))

    def test_external_workspace_links_are_not_treated_as_bundled_source(self):
        self.lock["packages"]["node_modules/example"]["resolved"] = "../../unbundled-source"
        self.write_lock()
        with self.assertRaisesRegex(offline.SetupError, "npm lockfile"):
            offline._lock_tarballs(self.root)

    def test_symbolic_links_in_source_and_bundle_are_rejected(self):
        self.prepare(core_only=True)
        folder = self.output / "wheelhouse"
        saved = self.output / "saved-wheels"
        folder.rename(saved)
        try:
            folder.symlink_to(saved, target_is_directory=True)
        except OSError:
            saved.rename(folder)
            self.skipTest("This platform does not permit symbolic links.")
        with self.assertRaisesRegex(offline.SetupError, "symbolic links"):
            offline.validate_bundle(self.root, self.output, core_only=True)
        folder.unlink()
        saved.rename(folder)
        path = self.root / "core/linked.py"
        path.symlink_to(self.root / "core/cli.py")
        with self.assertRaisesRegex(offline.SetupError, "symbolic links"):
            offline.source_fingerprint(self.root)

    def test_existing_output_is_preserved_and_failed_download_never_publishes_a_bundle(self):
        self.output.mkdir()
        existing = self.output / "existing"
        existing.write_bytes(b"Preserve this file")
        with patch.object(offline, "command") as execute:
            with self.assertRaisesRegex(offline.SetupError, "Existing bundle files are preserved"):
                offline.prepare(self.root, self.output, core_only=True)
        execute.assert_not_called()
        self.assertEqual(existing.read_bytes(), b"Preserve this file")
        self.output = self.base / "failed-bundle"

        def fail_download(arguments, root, **kwargs):
            if "download" in arguments:
                return SimpleNamespace(returncode=1)
            return self.command(arguments, root, **kwargs)

        with patch.object(offline, "command", side_effect=fail_download), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(offline.SetupError, "Binary dependency download failed"):
                offline.prepare(self.root, self.output, core_only=True)
        self.assertFalse(self.output.exists())
        self.assertFalse(list(self.base.glob("workbench-bundle-*")))

    def test_source_changes_during_preparation_do_not_publish_a_stale_bundle(self):
        def changing_source(arguments, root, **kwargs):
            result = self.command(arguments, root, **kwargs)
            if "download" in arguments:
                (root / "core/cli.py").write_text("Changed during dependency resolution", encoding="utf-8")
            return result

        with patch.object(offline, "command", side_effect=changing_source), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(offline.SetupError, "changed during preparation"):
                offline.prepare(self.root, self.output, core_only=True)
        self.assertFalse(self.output.exists())

    def test_local_resolution_detects_missing_transitive_wheels_despite_inherited_no_deps(self):
        if importlib.util.find_spec("pip") is None:
            self.skipTest("pip is unavailable for the local dependency resolution integration check.")
        pool = self.base / "approved-local-wheels"
        pool.mkdir()
        self.wheel(pool, name="fixture_parent", requirement="fixture-child==0.1.0")
        self.wheel(pool, name="fixture_child", requirement=None)
        requirements = self.base / "local-requirements.txt"
        requirements.write_text("fixture-parent==0.1.0\n", encoding="utf-8")
        environment = bootstrap.environment(offline=True)
        environment.update(PIP_NO_DEPS="1", PIP_NO_INDEX="1", PIP_FIND_LINKS=str(pool),
                           PIP_REQUIREMENT=str(requirements))
        actual_command = offline.command
        resolutions = []

        def local_command(arguments, root, **kwargs):
            if "wheel" in arguments:
                self.wheel(Path(arguments[arguments.index("--wheel-dir") + 1]), requirement="fixture-parent==0.1.0")
                return SimpleNamespace(returncode=0)
            result = actual_command(arguments, root, **kwargs)
            resolutions.append((list(arguments), kwargs, result.returncode))
            return result

        with patch.dict(os.environ, environment, clear=True), \
                patch.object(offline, "command", side_effect=local_command), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(offline.SetupError, "Offline dependency resolution failed"):
                offline.prepare(self.root, self.output, core_only=True)
        self.assertEqual([code for _, _, code in resolutions], [0, 1])
        self.assertTrue(resolutions[-1][1]["offline"])
        self.assertFalse(self.output.exists())
        self.assertFalse(list(self.base.glob("workbench-bundle-*")))

        environment["PIP_NO_DEPS"] = "0"
        resolutions.clear()
        with patch.dict(os.environ, environment, clear=True), \
                patch.object(offline, "command", side_effect=local_command), redirect_stdout(io.StringIO()):
            offline.prepare(self.root, self.output, core_only=True)
        self.assertEqual([code for _, _, code in resolutions], [0, 0])
        bundle = offline.validate_bundle(self.root, self.output, core_only=True)
        self.assertTrue((bundle.wheelhouse / "fixture_child-0.1.0-py3-none-any.whl").is_file())

    def test_local_resolution_rejects_wheels_selected_by_inherited_target_overrides(self):
        if importlib.util.find_spec("pip") is None:
            self.skipTest("pip is unavailable for the local dependency resolution integration check.")
        pool = self.base / "foreign-target-wheels"
        pool.mkdir()
        self.wheel(pool, name="fixture_parent", requirement=None, tag="cp399-cp399-win_amd64")
        environment = bootstrap.environment(offline=True)
        environment.update(PIP_NO_INDEX="1", PIP_FIND_LINKS=str(pool), PIP_PLATFORM="win_amd64",
                           PIP_PYTHON_VERSION="3.99", PIP_ABI="cp399", PIP_IMPLEMENTATION="cp")
        actual_command = offline.command
        resolutions = []

        def local_command(arguments, root, **kwargs):
            if "wheel" in arguments:
                self.wheel(Path(arguments[arguments.index("--wheel-dir") + 1]), requirement="fixture-parent==0.1.0")
                return SimpleNamespace(returncode=0)
            result = actual_command(arguments, root, **kwargs)
            resolutions.append((kwargs, result.returncode))
            return result

        with patch.dict(os.environ, environment, clear=True), \
                patch.object(offline, "command", side_effect=local_command), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(offline.SetupError, "Offline dependency resolution failed"):
                offline.prepare(self.root, self.output, core_only=True)
        self.assertEqual([code for _, code in resolutions], [0, 1])
        self.assertTrue(resolutions[-1][0]["offline"])
        self.assertFalse(self.output.exists())

    def test_direct_script_help_uses_standard_library_without_installed_dependencies(self):
        script = Path(offline.__file__).resolve()
        result = subprocess.run([sys.executable, "-S", str(script), "--help"], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("prepare", result.stdout)

    def test_target_command_uses_standard_library_without_a_source_checkout_or_file_changes(self):
        script = Path(offline.__file__).resolve()
        before = sorted(self.base.iterdir())
        result = subprocess.run([sys.executable, "-S", str(script), "target"], cwd=self.base,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), offline.target())
        self.assertEqual(sorted(self.base.iterdir()), before)
        with patch.object(offline, "source_root", side_effect=AssertionError("Target needs no source checkout")):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(offline.main(["target"]), 0)

    def test_direct_setup_launcher_handles_offline_errors_without_a_traceback_or_mutation(self):
        script = self.root / "core/bootstrap.py"
        shutil.copy2(Path(bootstrap.__file__), script)
        shutil.copy2(Path(offline.__file__), self.root / "core/offline.py")
        (self.root / "workspace.yaml").write_text("schema_version: 1\n", encoding="utf-8")
        result = subprocess.run([sys.executable, "-S", str(script), "--core-only", "--offline-bundle", str(self.base / "missing")],
                                cwd=self.root, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Setup incomplete.", result.stderr)
        self.assertIn("offline bundle", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse((self.root / ".venv").exists())
        self.assertFalse((self.root / ".env").exists())


class OfflineNpmIntegrationTests(unittest.TestCase):
    def test_locked_tarball_installs_offline_from_content_without_request_metadata_or_scripts(self):
        environment = {key: value for key, value in os.environ.items() if key.upper() in {
            "PATH", "PATHEXT", "SYSTEMROOT", "WINDIR", "TMPDIR", "TEMP", "TMP", "LANG", "LC_ALL"}}
        with tempfile.TemporaryDirectory(prefix="workbench-npm-local-") as temporary:
            base = Path(temporary).resolve()
            with patch.dict(os.environ, environment, clear=True):
                try:
                    npm = offline.npm_command(base)
                except offline.SetupError:
                    self.skipTest("Approved Node/npm are unavailable for the local offline integration check.")
            userconfig, globalconfig = base / "empty-user.npmrc", base / "empty-global.npmrc"
            userconfig.write_bytes(b"")
            globalconfig.write_bytes(b"")
            environment.update(NPM_CONFIG_USERCONFIG=str(userconfig), NPM_CONFIG_GLOBALCONFIG=str(globalconfig),
                               NPM_CONFIG_UPDATE_NOTIFIER="false")
            project = base / "project"
            project.mkdir()
            package = {"name": "offline-proof", "version": "1.0.0",
                       "scripts": {"install": 'node -e "process.exit(99)"'}}
            payload = json.dumps(package).encode("utf-8")
            archive = base / "fixture.tgz"
            with tarfile.open(archive, "w:gz") as stream:
                info = tarfile.TarInfo("package/package.json")
                info.size = len(payload)
                stream.addfile(info, io.BytesIO(payload))
            integrity = "sha512-" + base64.b64encode(hashlib.sha512(archive.read_bytes()).digest()).decode("ascii")
            definition = {"name": "offline-project", "version": "1.0.0", "dependencies": {"offline-proof": "1.0.0"}}
            (project / "package.json").write_text(json.dumps(definition), encoding="utf-8")
            (project / "package-lock.json").write_text(json.dumps({**definition, "lockfileVersion": 3, "packages": {
                "": definition, "node_modules/offline-proof": {"version": "1.0.0", "integrity": integrity,
                    "resolved": "https://example.invalid/offline-proof.tgz", "hasInstallScript": True}}}), encoding="utf-8")
            flags = ["--offline", "--ignore-scripts", "--no-audit", "--no-fund"]
            source_cache = base / "source-cache"
            seed = subprocess.run([*npm, "cache", "add", str(archive), "--cache", str(source_cache), *flags],
                                  cwd=project, env=environment, stdin=subprocess.DEVNULL,
                                  capture_output=True, timeout=60, shell=False)
            self.assertEqual(seed.returncode, 0, "Local npm cache creation failed.")
            cache = base / "content-cache"
            shutil.copytree(source_cache / "_cacache/content-v2", cache / "_cacache/content-v2")
            self.assertFalse((cache / "_cacache/index-v5").exists())
            result = subprocess.run([*npm, "ci", "--cache", str(cache), *flags],
                                    cwd=project, env=environment, stdin=subprocess.DEVNULL,
                                    capture_output=True, timeout=60, shell=False)
            self.assertEqual(result.returncode, 0, "npm could not install the local fixture in offline mode.")
            installed = json.loads((project / "node_modules/offline-proof/package.json").read_text(encoding="utf-8"))
            self.assertEqual(installed["version"], "1.0.0")


if __name__ == "__main__":
    unittest.main()
