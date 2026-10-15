"""Check static onboarding boundaries and exact source evidence."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1] / ".agents/skills/repository-onboarding/scripts"


def load_helper(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scanner = load_helper("scan_repo")
validator = load_helper("validate_evidence")


@unittest.skipUnless(shutil.which("git"), "Git is required for source revision checks")
class RepositoryOnboardingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.environment.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
        self.git("init", "--template=")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.source = self.repo / "source.py"
        self.source.write_text("first line\nsecond line", encoding="utf-8")
        (self.repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "Source fixture")
        self.revision = self.git("rev-parse", "HEAD")
        self.report = {
            "schema_version": "1.0",
            "repository": {"path": str(self.repo), "revision": self.revision},
            "claims": [{
                "id": "OBS-001", "category": "source", "statement": "Two source lines exist.",
                "status": "observed",
                "evidence": [{"path": "source.py", "start_line": 1, "end_line": 2, "kind": "source"}],
            }],
        }

    def git(self, *arguments, check=True):
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(self.repo), *arguments],
            env=self.environment, capture_output=True, text=True, check=check,
        )
        return result.stdout.strip() if check else result

    def errors(self, report=None):
        return validator.validate(self.repo, report or self.report)

    def test_committed_bytes_pass_and_line_ranges_are_checked(self):
        self.assertEqual([], self.errors())
        self.report["claims"][0]["evidence"][0]["end_line"] = 3
        self.assertTrue(any("exceed" in issue for issue in self.errors()))

    def test_ignored_and_untracked_files_cannot_attest_a_commit(self):
        for filename in ("ignored.txt", "untracked.txt"):
            with self.subTest(filename=filename):
                (self.repo / filename).write_text("uncommitted\n", encoding="utf-8")
                self.report["claims"][0]["evidence"][0].update(path=filename, end_line=1)
                self.assertTrue(any("not tracked" in issue for issue in self.errors()))

    def test_assume_unchanged_does_not_hide_modified_evidence(self):
        self.git("update-index", "--assume-unchanged", "source.py")
        self.source.write_text("changed\nsecond line", encoding="utf-8")
        self.assertEqual("", self.git("status", "--porcelain"))
        self.assertTrue(any("bytes differ" in issue for issue in self.errors()))

    def test_unrelated_modifications_do_not_invalidate_committed_evidence(self):
        (self.repo / "unrelated.txt").write_text("local change\n", encoding="utf-8")
        self.assertEqual([], self.errors())

    def test_symlink_evidence_is_rejected(self):
        link = self.repo / "linked.py"
        try:
            link.symlink_to(self.source.name)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation is unavailable")
        self.git("add", "linked.py")
        self.git("commit", "-m", "Symlink fixture")
        self.report["repository"]["revision"] = self.git("rev-parse", "HEAD")
        self.report["claims"][0]["evidence"][0]["path"] = "linked.py"
        self.assertTrue(any("symlink" in issue for issue in self.errors()))

    def test_malformed_claim_fields_report_errors_without_crashing(self):
        for field, value in (("status", []), ("status", {}), ("reason", None), ("reason", [])):
            with self.subTest(field=field, value=value):
                report = copy.deepcopy(self.report)
                report["claims"][0]["status"] = "inferred"
                report["claims"][0][field] = value
                self.assertTrue(self.errors(report))
        for field, value in (("kind", []), ("kind", {}), ("path", "bad\x00path"), ("start_line", True)):
            with self.subTest(field=field, value=value):
                report = copy.deepcopy(self.report)
                report["claims"][0]["evidence"][0][field] = value
                self.assertTrue(self.errors(report))

    def test_observed_and_inferred_claims_require_evidence(self):
        for status in ("observed", "inferred"):
            with self.subTest(status=status):
                self.report["claims"][0].update(status=status, evidence=[], reason="Source is unavailable.")
                self.assertTrue(any("lacks evidence" in issue for issue in self.errors()))
        self.report["claims"][0]["status"] = "verified"
        self.assertTrue(any("invalid status" in issue for issue in self.errors()))

    def test_malformed_dependency_metadata_does_not_abort_inventory(self):
        for value in (42, ["react"], [{"react": "*"}]):
            with self.subTest(value=value):
                (self.repo / "package.json").write_text(json.dumps({"dependencies": value}), encoding="utf-8")
                self.assertIn("warning", scanner.safe_package_metadata(self.repo))

    def test_ignored_child_repository_does_not_contaminate_python_inventory(self):
        (self.repo / ".gitignore").write_text("ignored.txt\nrepos/\n.workbench/\n", encoding="utf-8")
        child = self.repo / "repos/child"
        child.mkdir(parents=True)
        subprocess.run(
            ["git", "-C", str(child), "init", "--template="],
            env=self.environment, capture_output=True, check=True,
        )
        (child / "pom.xml").write_text("<project/>\n", encoding="utf-8")
        (child / "tests").mkdir()
        (child / "tests/OtherTest.java").write_text("class OtherTest {}\n", encoding="utf-8")
        (self.repo / ".workbench").mkdir()
        (self.repo / ".workbench/old-openapi.yaml").write_text("unretained\n", encoding="utf-8")
        (self.repo / "pyproject.toml").write_text('[project]\nname = "fixture"\n', encoding="utf-8")
        (self.repo / "core").mkdir()
        (self.repo / "core/cli.py").write_text("def main():\n    pass\n", encoding="utf-8")
        (self.repo / "tests").mkdir()
        (self.repo / "tests/test_core.py").write_text("assert True\n", encoding="utf-8")
        inventory = scanner.scan(self.repo)
        self.assertEqual(["python-build"], inventory["stack_signals"])
        self.assertEqual(["pyproject.toml"], inventory["manifests"])
        self.assertEqual(["core"], inventory["source_roots"])
        self.assertEqual(["tests/test_core.py"], inventory["test_candidates"])
        self.assertEqual(["core/cli.py"], inventory["entrypoint_candidates"])
        self.assertEqual([], inventory["contract_candidates"])
        omissions = {item["path"] for item in inventory["inventory_scope"]["omitted_directories"]}
        self.assertTrue({"repos", ".workbench"} <= omissions)
        self.assertEqual("tracked-and-untracked-nonignored-files", inventory["inventory_scope"]["file_selection"])

    def test_nested_checkouts_are_excluded_and_monorepo_directories_remain(self):
        child = self.repo / "independent"
        child.mkdir()
        subprocess.run(
            ["git", "-C", str(child), "init", "--template="],
            env=self.environment, capture_output=True, check=True,
        )
        (child / "pom.xml").write_text("<project/>\n", encoding="utf-8")
        # A directory named repos can contain this repository's own modules.
        module = self.repo / "repos/module"
        module.mkdir(parents=True)
        (module / "package.json").write_text('{"name":"module"}\n', encoding="utf-8")
        inventory = scanner.scan(self.repo)
        self.assertEqual(["repos/module/package.json"], inventory["manifests"])
        self.assertNotIn("jvm-build", inventory["stack_signals"])
        self.assertIn(
            {"path": "independent", "reason": "nested Git checkout"},
            inventory["inventory_scope"]["omitted_directories"],
        )

    def test_no_git_inventory_uses_disclosed_filename_fallback(self):
        with mock.patch.object(scanner, "git", return_value=None):
            inventory = scanner.scan(self.repo)
        self.assertEqual("filesystem-fallback", inventory["inventory_scope"]["file_selection"])
        self.assertEqual("unknown", inventory["repository"]["revision"])
        self.assertTrue(any("cannot exclude all ignored files" in warning for warning in inventory["warnings"]))

    def test_checkout_subdirectory_cannot_write_inside_its_actual_git_root(self):
        subdirectory = self.repo / "src"
        subdirectory.mkdir()
        output = self.repo / "inventory.json"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "scan_repo.py"), "--repo", str(subdirectory), "--output", str(output)],
            env=self.environment, capture_output=True, text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(output.exists())
        self.assertIn("checkout root", result.stderr)

    @unittest.skipIf(os.name == "nt", "This fixture requires an executable POSIX hook")
    def test_static_inspection_does_not_run_fsmonitor_or_refresh_the_index(self):
        marker = self.root / "hook-ran"
        hook = self.root / "fsmonitor-hook"
        hook.write_text(
            f"#!{sys.executable}\nfrom pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n",
            encoding="utf-8",
        )
        hook.chmod(0o700)
        self.git("config", "core.fsmonitor", str(hook))
        source_stat = self.source.stat()
        os.utime(self.source, ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns + 2_000_000_000))
        index = self.repo / ".git/index"
        before = index.read_bytes(), index.stat().st_mtime_ns
        scanner.scan(self.repo)
        self.assertEqual([], self.errors())
        self.assertFalse(marker.exists())
        self.assertEqual(before, (index.read_bytes(), index.stat().st_mtime_ns))

    def test_external_git_environment_cannot_redirect_source_identity(self):
        with mock.patch.dict(os.environ, {"GIT_DIR": str(self.root / "missing.git"), "GIT_WORK_TREE": str(self.root)}):
            self.assertEqual(self.revision, scanner.git(self.repo, "rev-parse", "HEAD"))
            self.assertEqual([], self.errors())

    def test_sha256_revisions_are_supported_when_git_supports_them(self):
        self.repo = self.root / "sha256-repo"
        self.repo.mkdir()
        result = self.git("init", "--object-format=sha256", "--template=", check=False)
        if result.returncode:
            self.skipTest("Installed Git does not support SHA-256 repositories")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.repo / "source.py").write_text("first line\nsecond line", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "SHA-256 source fixture")
        self.report["repository"] = {"path": str(self.repo), "revision": self.git("rev-parse", "HEAD")}
        self.assertEqual(64, len(self.report["repository"]["revision"]))
        self.assertEqual(self.report["repository"]["revision"], scanner.scan(self.repo)["repository"]["revision"])
        self.assertEqual([], self.errors())


if __name__ == "__main__":
    unittest.main()
