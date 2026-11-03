"""Check comparison routing, failure isolation, and truthful suite outcomes."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import coverage_suite as suite


class CoverageSuiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="coverage-suite-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = self.root / "suite.json"
        for name in ("ces.json", "ems2.json"):
            (self.root / name).write_text("{}")
        self.config = {"schema_version": 1, "output_dir": "runs", "scope": "Controlled suite",
                       "checks": [{"id": "ces", "kind": "ces", "label": "EMS2 → CES", "config": "ces.json"},
                                  {"id": "ems2", "kind": "ems2", "label": "PROD → UAT", "config": "ems2.json"}]}
        self.calls = []
        self.outcomes = ["FUNCTIONAL_MATCH", "FUNCTIONAL_MATCH"]

    def child(self, path, **kwargs):
        self.calls.append((path.name, kwargs))
        outcome = self.outcomes[len(self.calls) - 1]
        if isinstance(outcome, Exception):
            raise outcome
        directory = kwargs["output"]
        directory.mkdir()
        (directory / "report.html").write_text("Controlled report")
        return {"status": outcome, "summary": {"discovered_accounts": 10, "compared_accounts": 2,
                "unassessed_accounts": 8, "functional_profile_coverage_percent": None}, "binding": {"fixture": True}}, directory

    def run_suite(self, **kwargs):
        self.path.write_text(json.dumps(self.config))
        with patch.object(suite, "_runners", return_value={"ces": self.child, "ems2": self.child}):
            return suite.run(self.path, **kwargs)

    def test_default_suite_runs_both_in_replay_and_keeps_denominators_separate(self):
        """Given two configured comparison families
        When the suite runs without an execution mode
        Then both receive replay and their overlapping populations are never summed
        """
        self.outcomes = ["INCOMPLETE", "DIFFERENCES"]
        result, directory = self.run_suite(user_limit=2)
        self.assertEqual([name for name, _ in self.calls], ["ces.json", "ems2.json"])
        self.assertTrue(all(k["mode"] == "replay" and k["user_limit"] == 2 for _, k in self.calls))
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["evidence_source"], "MOCK: supplied API responses")
        self.assertNotIn("summary", result)
        self.assertEqual([c["summary"]["discovered_accounts"] for c in result["checks"]], [10, 10])
        report = (directory / "index.html").read_text()
        self.assertIn("ces/report.html", report)
        self.assertIn("ems2/report.html", report)
        self.assertIn("must not be added", report)

    def test_first_setup_failure_does_not_suppress_second_comparison(self):
        """Given the first source configuration fails
        When the suite executes both checks
        Then the second check still completes and the failed suite remains incomplete
        """
        self.outcomes = [ValueError("private data must not be emitted"), "FUNCTIONAL_MATCH"]
        result, directory = self.run_suite()
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(result["checks"][0]["errors"], [{"code": "ValueError", "http_status": None}])
        self.assertEqual(result["checks"][1]["status"], "FUNCTIONAL_MATCH")
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertNotIn("private data", (directory / "result.json").read_text())
        self.assertNotIn("href='ces/report.html'", (directory / "index.html").read_text())

    def test_completed_child_is_saved_before_next_child_starts(self):
        """Given the next comparison is interrupted
        When one comparison already completed
        Then its result is durable and the suite has no passing final status
        """
        original = self.child
        def interrupt(path, **kwargs):
            if path.name == "ems2.json":
                raise KeyboardInterrupt("Controlled interruption")
            return original(path, **kwargs)
        self.path.write_text(json.dumps(self.config))
        directory = self.root / "interrupted"
        with patch.object(suite, "_runners", return_value={"ces": interrupt, "ems2": interrupt}):
            with self.assertRaises(KeyboardInterrupt):
                suite.run(self.path, output=directory)
        saved = json.loads((directory / "result.json").read_text())
        self.assertEqual(saved["status"], "INCOMPLETE")
        self.assertEqual(len(saved["checks"]), 1)
        self.assertEqual(saved["checks"][0]["status"], "FUNCTIONAL_MATCH")

    def test_suite_differences_return_nonzero_and_html_escapes_labels(self):
        """Given complete comparisons with a reported difference and an unsafe label
        When the CLI builds the suite dashboard
        Then its exit is one and the label renders as plain text
        """
        self.outcomes = ["FUNCTIONAL_MATCH", "DIFFERENCES"]
        self.config["checks"][0]["label"] = "<script>alert(1)</script>"
        self.path.write_text(json.dumps(self.config))
        directory = self.root / "different"
        with patch.object(suite, "_runners", return_value={"ces": self.child, "ems2": self.child}), redirect_stdout(io.StringIO()):
            code = suite.main(["--config", str(self.path), "--output", str(directory)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads((directory / "result.json").read_text())["status"], "DIFFERENCES")
        self.assertNotIn("<script>", (directory / "index.html").read_text())

    def test_invalid_comparison_ids_cannot_escape_output_or_overwrite_results(self):
        """Given duplicate or traversal comparison identifiers
        When configuration is validated
        Then no child runs and output paths cannot overwrite another comparison
        """
        for identifier in ("../escaped", "ces"):
            with self.subTest(identifier=identifier):
                self.config["checks"][1]["id"] = identifier
                with self.assertRaises(ValueError):
                    self.run_suite()
                self.assertEqual(self.calls, [])

    def test_cli_returns_zero_only_for_complete_match_and_two_for_incomplete(self):
        """Given matching or incomplete outcomes from configured comparisons
        When the suite command reports its final status
        Then zero requires complete functional agreement and incomplete results return two
        """
        self.path.write_text(json.dumps(self.config))
        for status, expected in (("FUNCTIONAL_MATCH", 0), ("INCOMPLETE", 2)):
            with self.subTest(status=status):
                self.calls = []
                self.outcomes = ["FUNCTIONAL_MATCH", status]
                directory = self.root / status
                with patch.object(suite, "_runners", return_value={"ces": self.child, "ems2": self.child}), redirect_stdout(io.StringIO()):
                    code = suite.main(["--config", str(self.path), "--output", str(directory)])
                self.assertEqual(code, expected)
                self.assertEqual(json.loads((directory / "result.json").read_text())["status"], status)


if __name__ == "__main__":
    unittest.main()
