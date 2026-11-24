"""Protect complete report instructions across source updates and workspace copies."""

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.workspace import initialize_workspace


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/release-clinic"
HELPER = SKILL / "scripts/check_report_parity.py"
INCLUDED = SKILL / "references/dtp-tda-report.md"
UPSTREAM = ROOT / "core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md"


class ReleaseClinicSkillParityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="release-clinic-skill-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def check(self, upstream, helper=HELPER):
        result = subprocess.run(
            [sys.executable, "-S", str(helper), "--upstream", str(upstream)],
            cwd=self.root, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.stderr, "", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_bundled_source_matches_complete_included_skill_without_writes(self):
        before = {path: path.read_bytes() for path in (INCLUDED, UPSTREAM)}
        exit_code, result = self.check(UPSTREAM)
        self.assertEqual((exit_code, result["status"]), (0, "MATCH"))
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["comparison"], "complete-skill-bytes")
        for field, path in (("included", INCLUDED), ("upstream", UPSTREAM)):
            self.assertEqual(result[field], {
                "path": str(path.resolve()),
                "sha256": hashlib.sha256(before[path]).hexdigest(),
                "size_bytes": len(before[path]),
                "line_count": len(before[path].splitlines()),
            })
            self.assertEqual(path.read_bytes(), before[path])
        self.assertEqual(result["errors"], [])
        self.assertIn("does not verify analyst decisions", result["limitations"][0])
        self.assertIn("browser controls", result["limitations"][0])

    def test_same_version_edit_is_mismatch(self):
        source = UPSTREAM.read_bytes()
        changed = source.replace(b"function remExport() {", b"function remExport() { /* changed */", 1)
        self.assertNotEqual(changed, source)
        upstream = self.root / "same-version.md"
        upstream.write_bytes(changed)
        exit_code, result = self.check(upstream)
        self.assertEqual((exit_code, result["status"]), (1, "MISMATCH"))
        self.assertNotEqual(result["included"]["sha256"], result["upstream"]["sha256"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(upstream.read_bytes(), changed)

    def test_missing_source_is_error(self):
        missing = self.root / "missing.md"
        exit_code, result = self.check(missing)
        self.assertEqual((exit_code, result["status"]), (2, "ERROR"))
        self.assertIsNone(result["upstream"]["sha256"])
        self.assertIn("Cannot read source", result["errors"][0])
        self.assertFalse(missing.exists())

    def test_path_resolution_failure_is_structured_error(self):
        namespace = runpy.run_path(str(HELPER))
        upstream = "~missing-account/SKILL.md"
        output = io.StringIO()
        with (patch.object(Path, "expanduser", side_effect=RuntimeError("Cannot determine home directory")),
              patch.object(sys, "argv", [str(HELPER), "--upstream", upstream]), redirect_stdout(output)):
            exit_code = namespace["main"]()
        result = json.loads(output.getvalue())
        self.assertEqual((exit_code, result["status"]), (2, "ERROR"))
        self.assertEqual(result["upstream"], {
            "path": upstream, "sha256": None, "size_bytes": None, "line_count": None,
        })
        self.assertEqual(result["included"]["sha256"], hashlib.sha256(INCLUDED.read_bytes()).hexdigest())
        self.assertIn("Cannot resolve source", result["errors"][0])
        self.assertIn("Cannot determine home directory", result["errors"][0])
        self.assertIn("does not verify analyst decisions", result["limitations"][0])

    def test_self_comparison_is_error(self):
        exit_code, result = self.check(INCLUDED)
        self.assertEqual((exit_code, result["status"]), (2, "ERROR"))
        self.assertIn("self-comparison", result["errors"][0])

    def test_alias_to_included_source_is_error(self):
        alias = self.root / "alias.md"
        try:
            alias.symlink_to(INCLUDED)
        except OSError:
            self.skipTest("File symlinks are unavailable on this platform.")
        exit_code, result = self.check(alias)
        self.assertEqual((exit_code, result["status"]), (2, "ERROR"))
        self.assertIn("self-comparison", result["errors"][0])

    def test_empty_non_skill_and_invalid_utf8_sources_are_errors(self):
        for content in (b"", b"# Unrelated instructions\n", b"\xff",
                        b"---\nname: release-clinic\n---\nInstructions\n",
                        b"---\nname: dtp-tda-report\n---\n"):
            with self.subTest(content=content):
                upstream = self.root / "invalid.md"
                upstream.write_bytes(content)
                exit_code, result = self.check(upstream)
                self.assertEqual((exit_code, result["status"]), (2, "ERROR"))
                self.assertTrue(result["errors"])
                self.assertEqual(result["upstream"]["sha256"], hashlib.sha256(content).hexdigest())
                self.assertEqual(upstream.read_bytes(), content)

    def test_initialized_workspace_retains_and_checks_complete_report_skill(self):
        workspace = initialize_workspace(self.root / "workspace", name="Report parity check")
        copied = workspace / ".agents/skills/release-clinic"
        helper = copied / "scripts/check_report_parity.py"
        included = copied / "references/dtp-tda-report.md"
        self.assertEqual(helper.read_bytes(), HELPER.read_bytes())
        self.assertEqual(included.read_bytes(), UPSTREAM.read_bytes())
        self.assertFalse((workspace / "core/release-clinic").exists())
        exit_code, result = self.check(UPSTREAM, helper=helper)
        self.assertEqual((exit_code, result["status"]), (0, "MATCH"))
        self.assertEqual(result["included"]["path"], str(included.resolve()))


if __name__ == "__main__":
    unittest.main()
