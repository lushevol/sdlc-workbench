"""Check Gherkin CLI isolation and CI exit policies."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.gherkin_quality import evidence_schema


class GherkinCliTests(unittest.TestCase):
    def run_check(self, result, *options):
        output = io.StringIO()
        with patch("ai_sdlc_workbench.cli.Workbench", side_effect=AssertionError("Unexpected workspace loading")):
            with patch("ai_sdlc_workbench.gherkin_quality.check_gherkin", return_value=result) as checker:
                with redirect_stdout(output):
                    code = main(["--workspace", "/unconfigured-workspace", "gherkin", "cases.feature", *options])
        self.assertEqual(json.loads(output.getvalue()), result)
        return code, checker

    def test_default_exit_policy_distinguishes_findings_from_missing_review(self):
        for status, expected in (("PASS", 0), ("FAIL", 1), ("UNVERIFIED", 2), ("WARNING", 0)):
            with self.subTest(status=status):
                code, _ = self.run_check({"status": status, "automation_ready": False, "exit_code": expected})
                self.assertEqual(code, expected)

    def test_strict_exit_policy_fails_warnings_without_claiming_semantic_review(self):
        for status, expected in (("PASS", 0), ("FAIL", 1), ("UNVERIFIED", 2), ("WARNING", 1)):
            with self.subTest(status=status):
                code, checker = self.run_check({"status": status, "automation_ready": False, "exit_code": expected}, "--strict")
                self.assertEqual(code, expected)
                self.assertTrue(checker.call_args.kwargs["strict"])

    def test_require_ready_rejects_unreviewed_cases_even_when_structure_passes(self):
        for status in ("PASS", "UNVERIFIED", "WARNING"):
            with self.subTest(status=status):
                code, _ = self.run_check({"status": status, "automation_ready": False, "exit_code": 0}, "--require-ready")
                self.assertEqual(code, 1)

    def test_require_ready_accepts_ready_cases_and_retains_failure_policy(self):
        for status, expected in (("PASS", 0), ("FAIL", 1)):
            with self.subTest(status=status):
                code, _ = self.run_check({"status": status, "automation_ready": True, "exit_code": expected}, "--require-ready")
                self.assertEqual(code, expected)

    def test_paths_and_evidence_options_reach_checker_without_workspace_loading(self):
        code, checker = self.run_check(
            {"status": "PASS", "automation_ready": True, "exit_code": 0},
            "additional.md", "--manifest", "evidence.json", "--root", "/evidence-root", "--strict", "--require-ready")
        self.assertEqual(code, 0)
        checker.assert_called_once_with(["cases.feature", "additional.md"], manifest="evidence.json",
                                        root="/evidence-root", strict=True)

    def test_defaults_do_not_turn_workspace_path_into_evidence_root(self):
        _, checker = self.run_check({"status": "UNVERIFIED", "automation_ready": False, "exit_code": 2})
        checker.assert_called_once_with(["cases.feature"], manifest=None, root=None, strict=False)

    def test_repeatable_scenario_options_select_only_requested_case_ids(self):
        code, checker = self.run_check({"status": "PASS", "automation_ready": True, "exit_code": 0},
                                       "--scenario", "UI-001", "--scenario", "UI-EDGE-002")
        self.assertEqual(code, 0)
        checker.assert_called_once_with(["cases.feature"], manifest=None, root=None, strict=False,
                                        scenario_ids=["UI-001", "UI-EDGE-002"])

    def test_missing_paths_is_an_argument_error(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as failure:
                main(["gherkin"])
        self.assertEqual(failure.exception.code, 2)

    def test_print_schema_uses_installed_schema_without_loading_workspace_or_checker(self):
        output = io.StringIO()
        with patch("ai_sdlc_workbench.cli.Workbench", side_effect=AssertionError("Unexpected workspace loading")):
            with patch("ai_sdlc_workbench.gherkin_quality.check_gherkin", side_effect=AssertionError("Unexpected check")):
                with redirect_stdout(output):
                    code = main(["--workspace", "/unconfigured-workspace", "gherkin", "--print-schema"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue()), evidence_schema())

    def test_print_schema_rejects_paths_and_other_gherkin_options(self):
        combinations = (
            ["cases.feature"], ["--manifest", "evidence.json"], ["--root", "/evidence-root"],
            ["--strict"], ["--require-ready"],
            ["--scenario", "UI-001"],
        )
        for options in combinations:
            with self.subTest(options=options):
                output = io.StringIO()
                with patch("ai_sdlc_workbench.gherkin_quality.check_gherkin", side_effect=AssertionError("Unexpected check")):
                    with redirect_stdout(output):
                        code = main(["gherkin", "--print-schema", *options])
                self.assertEqual(code, 1)
                self.assertIn("--print-schema", json.loads(output.getvalue())["error"]["message"])

    def test_real_incomplete_scenario_fails_without_workspace_configuration(self):
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-gherkin-cli-") as temporary:
            path = Path(temporary) / "incomplete.feature"
            path.write_text("Feature: Incomplete case\n  Scenario: Missing result\n    Given an authenticated user\n"
                            "    When the user opens the home page\n", encoding="utf-8")
            output = io.StringIO()
            with patch("ai_sdlc_workbench.cli.Workbench", side_effect=AssertionError("Unexpected workspace loading")):
                with redirect_stdout(output):
                    code = main(["--workspace", str(Path(temporary) / "not-a-workspace"),
                                 "gherkin", str(path)])
            result = json.loads(output.getvalue())
            self.assertEqual(code, 1, result)
            self.assertEqual(result["status"], "FAIL", result)
            self.assertFalse(result["automation_ready"], result)
            self.assertTrue(result["findings"], result)


if __name__ == "__main__":
    unittest.main()
