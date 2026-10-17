"""Check Release Clinic root configuration and native command boundaries."""

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.release_clinic import _environment, doctor, paths


class ReleaseClinicTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="release-clinic-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "workspace"
        self.root.mkdir()
        # Drop host credentials and paths from these offline command checks.
        self.environment = {key: value for key, value in os.environ.items()
                            if key in {"PATH", "HOME", "SYSTEMROOT", "TMPDIR", "LANG"}}

    def command(self, *arguments):
        return subprocess.run([sys.executable, "-m", "ai_sdlc_workbench.cli", "--workspace", str(self.root),
                               "release-clinic", *arguments], cwd=self.root.parent,
                              env=self.environment, capture_output=True, text=True, timeout=30)

    def fixture(self, **overrides):
        data = {"release_stream": "TEST", "release_id": "123", "release_title": "Offline fixture", **overrides}
        (self.root / "input.json").write_text(json.dumps(data), encoding="utf-8")

    def test_report_handles_missing_sonar_data_and_uses_root_output_setting(self):
        self.fixture()
        (self.root / ".env").write_text("TDA_OUTPUT_DIR=retained/reports\n", encoding="utf-8")
        result = self.command("report", "input.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / "retained/reports/TDAReport_TEST_123.html").read_text(encoding="utf-8")
        self.assertIn("No quality gate data", html)
        self.assertIn("[Requires Review]", html)
        self.assertIn("standard: ASD-STE100", html)
        self.assertIn("automated_check: PASSED", html)
        self.assertIn("asd_review: PENDING", html)
        self.assertTrue(html.rstrip().endswith("</html>"))
        self.assertFalse((self.root.parent / "retained").exists())

    def test_report_explicit_output_resolves_from_workspace(self):
        self.fixture()
        result = self.command("report", "input.json", "--output", "chosen/report.html")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "chosen/report.html").is_file())
        missing = self.command("report", "missing.json")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("Input file not found", missing.stderr)

    def test_report_identifiers_cannot_escape_default_output_directory(self):
        self.fixture(release_stream="../../outside", release_id="../456")
        result = self.command("report", "input.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        generated = list((self.root / ".workbench/release-clinic/reports").glob("*.html"))
        self.assertEqual(len(generated), 1)
        self.assertFalse((self.root / "outside").exists())

    def test_native_flags_and_separator_keep_their_original_order(self):
        with patch("ai_sdlc_workbench.release_clinic.subprocess.run") as child:
            child.return_value.returncode = 7
            with patch.dict(os.environ, self.environment, clear=True):
                result = main(["--workspace", str(self.root), "release-clinic", "audit",
                               "--start-date", "2026-10-01", "--end-date", "2026-10-02", "--skip-download"])
            self.assertEqual(result, 7)
            self.assertEqual(child.call_args.args[0][-5:],
                             ["--start-date", "2026-10-01", "--end-date", "2026-10-02", "--skip-download"])
            self.assertEqual(child.call_args.kwargs["cwd"], self.root)
            self.assertEqual(child.call_args.kwargs["env"]["AI_SDLC_WORKSPACE"], str(self.root))
        result = self.command("report", "--", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--output", result.stdout)

    def test_doctor_never_discloses_credentials_or_mutates_process_environment(self):
        (self.root / ".env").write_text("ADO_TOKEN=fixture-secret-never-display\nSNOW_ENABLED=false\n", encoding="utf-8")
        with patch.dict(os.environ, self.environment, clear=True):
            before = dict(os.environ)
            prepared = _environment(self.root)
            with patch("ai_sdlc_workbench.release_clinic.importlib.util.find_spec", return_value=None):
                result = doctor(self.root)
            self.assertEqual(dict(os.environ), before)
        self.assertEqual(prepared["ADO_TOKEN"], "fixture-secret-never-display")
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertIn("requests", result["missing_dependencies"])
        self.assertIn("GENIE_TOKEN", result["missing_configuration"])
        self.assertNotIn("fixture-secret-never-display", json.dumps(result))
        self.assertNotIn("CLIENT_ID", result["missing_configuration"])

    def test_path_exposes_installed_instructions_and_scripts(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["--workspace", str(self.root), "release-clinic", "path"]), 0)
        declared = json.loads(output.getvalue())
        for name in ("report_skill", "portfolio_skill", "trends_skill"):
            self.assertTrue(Path(declared[name]).is_file(), name)
        self.assertTrue((paths()["scripts"] / "stream_config.yaml").is_file())

    def test_doctor_identifies_missing_explicit_configuration_files(self):
        (self.root / ".env").write_text("TDA_STREAM_CONFIG=missing-stream.yaml\n", encoding="utf-8")
        with patch.dict(os.environ, self.environment, clear=True):
            result = doctor(self.root)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["missing_files"], ["TDA_STREAM_CONFIG"])
        self.assertEqual(result["configuration_files"]["TDA_STREAM_CONFIG"], str(self.root / "missing-stream.yaml"))

    def test_service_explicit_environment_file_does_not_merge_root_secrets(self):
        (self.root / ".env").write_text("ADO_TOKEN=root-fixture\n", encoding="utf-8")
        (self.root / "service.env").write_text("ADO_TOKEN=service-fixture\n", encoding="utf-8")
        with patch.dict(os.environ, {**self.environment, "SERVICE_ENV_FILE": "service.env"}, clear=True):
            environment = _environment(self.root, service=True)
        self.assertEqual(environment["ADO_TOKEN"], "service-fixture")


if __name__ == "__main__":
    unittest.main()
