"""Keep traceability, runner outcomes, and business verification claims separate."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.review_coverage import analyze_coverage, build_case_ledger


class ReviewCoverageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="review-coverage-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.index = {"schema_version": 1, "id": "fixture", "scope_id": "fixture", "title": "Traceability boundary",
            "inventory_completeness": {"criteria": "COMPLETE", "changes": "SELECTED", "cases": "COMPLETE"},
            "artifacts": [], "criteria": [], "changes": [], "cases": [], "assertions": [],
            "links": [], "executions": [], "limits": ["Fixture supplies no business approval."]}
        for identifier, kind, content in (("intent", "INTENT", "# AC-1\n# TC-1\n"),
            ("code", "SOURCE", "return True\n"), ("test", "TEST", "assert accepts() is True\n"),
            ("result", "EXECUTION", '{"status":"passed"}\n'), ("binding", "SOURCE", '{"source":"fixture"}\n')):
            ref = self.write(identifier + ".txt", content, raw=True)
            self.index["artifacts"].append({"id": identifier, "kind": kind, **ref})
        self.index["criteria"] = [{"id": "AC-1", "definition": {"artifact_id": "intent", "anchor": "ac-1"},
                                    "required_levels": ["UNIT"], "limits": []}]
        self.index["cases"] = [{"id": "TC-1", "definition": {"artifact_id": "intent", "anchor": "tc-1"}, "limits": []}]
        self.index["changes"] = [{"id": "CH-1", "classification": "BUSINESS", "evidence": [{"artifact_id": "code"}],
                                  "predicate_scope": "SELECTED", "limits": []}]
        self.index["assertions"] = [{"id": "A-1", "case_id": "TC-1", "source": {"artifact_id": "test"},
                                     "predicate_scope": "SELECTED", "limits": []}]
        self.link("L-1", "AC_CASE", "AC-1", "TC-1", ["A-1"])
        self.link("L-2", "AC_CHANGE", "AC-1", "CH-1", [])
        self.index["executions"] = [{"id": "RUN-1", "case_id": "TC-1", "source": {"artifact_id": "result"},
            "original_status": "passed", "outcome": "PASSED", "characterization": False, "level": "UNIT",
            "mode": "CONTROLLED_SOURCE", "assertion_ids": ["A-1"], "environment_id": "fixture-unit",
            "source_binding": {"artifact_id": "binding"}, "limits": []}]

    def write(self, name, value, raw=False):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if raw else json.dumps(value))
        return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def link(self, identifier, relationship, source, target, assertions):
        self.index["links"].append({"id": identifier, "relationship": relationship, "from_id": source,
            "to_id": target, "evidence": [{"artifact_id": "test"}], "assertion_ids": assertions,
            "predicate_scope": "SELECTED", "conformance": "UNKNOWN", "limits": []})

    def coverage(self):
        return analyze_coverage(self.index, self.root)

    def test_shared_ac_never_creates_a_change_assertion_link(self):
        """Given a case and change sharing an AC
        When coverage is calculated
        Then change-to-case assertion coverage stays zero
        """
        report = self.coverage()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["metrics"]["AC_CASE"]["has_current_assertion_link"]["numerator"], 1)
        self.assertEqual(report["metrics"]["CHANGE_CASE"]["has_current_assertion_link"]["numerator"], 0)
        self.assertEqual(report["matrices"]["CHANGE_CASE"][0]["links"], [])
        self.assertEqual(report["verification"], "NOT_VERIFIED")

    def test_selected_denominator_never_becomes_whole_behavior_percentage(self):
        """Given selected changed files
        When direct assertion evidence exists
        Then counts remain selected and complete predicate coverage remains zero
        """
        self.link("L-3", "CHANGE_CASE", "CH-1", "TC-1", ["A-1"])
        report = self.coverage()
        metrics = report["metrics"]["CHANGE_CASE"]
        self.assertEqual(metrics["has_current_assertion_link"]["numerator"], 1)
        self.assertEqual(metrics["has_current_assertion_link"]["denominator"]["inventory_scope"], "SELECTED")
        self.assertIsNone(metrics["has_current_assertion_link"]["whole_scope_percent"])
        self.assertIsNone(metrics["has_current_assertion_link"]["denominator"]["whole_scope_denominator"])
        self.assertEqual(metrics["has_declared_complete_assertion_link"]["numerator"], 0)
        self.assertEqual(metrics["has_declared_complete_match"]["numerator"], 0)

    def test_unknown_and_empty_denominators_are_distinct(self):
        """Given no changes and unknown case inventory
        When coverage is calculated
        Then empty complete scope differs from unknown scope
        """
        self.index["changes"] = []
        self.index["links"] = []
        self.index["inventory_completeness"].update(changes="COMPLETE", cases="UNKNOWN")
        report = self.coverage()
        metric = report["metrics"]["CHANGE_CASE"]["has_current_definition_link"]
        self.assertEqual(metric["denominator"]["status"], "EMPTY")
        self.assertIsNone(metric["whole_scope_percent"])
        self.index["inventory_completeness"]["changes"] = "UNKNOWN"
        self.assertEqual(self.coverage()["metrics"]["CHANGE_CASE"]["has_current_definition_link"]["denominator"]["status"], "UNKNOWN")

    def test_complete_link_does_not_expand_a_selected_change_predicate(self):
        """Given a selected change with a declared complete assertion link
        When coverage is calculated
        Then the source scope prevents a complete changed-behavior claim
        """
        self.link("L-3", "CHANGE_CASE", "CH-1", "TC-1", ["A-1"])
        self.index["links"][-1].update(predicate_scope="COMPLETE", conformance="MATCH")
        self.index["assertions"][0]["predicate_scope"] = "COMPLETE"
        report = self.coverage()
        metrics = report["metrics"]["CHANGE_CASE"]
        self.assertEqual(metrics["has_current_assertion_link"]["numerator"], 1)
        self.assertEqual(metrics["has_declared_complete_assertion_link"]["numerator"], 0)
        self.assertEqual(metrics["has_declared_complete_match"]["numerator"], 0)

    def test_characterization_simulation_and_unbound_passes_do_not_fill_execution_coverage(self):
        """Given passes with unsuitable evidence
        When each boundary is checked
        Then matching passing execution remains zero
        """
        for override in ({"characterization": True}, {"mode": "SIMULATION"}, {"mode": "UNKNOWN"},
                         {"assertion_ids": []}, {"level": "SYSTEM"}):
            with self.subTest(override=override):
                candidate = copy.deepcopy(self.index)
                candidate["executions"][0].update(override)
                report = analyze_coverage(candidate, self.root)
                self.assertEqual(report["metrics"]["AC_CASE"]["has_matching_passing_execution"]["numerator"], 0)
        self.assertEqual(self.coverage()["metrics"]["AC_CASE"]["has_matching_passing_execution"]["numerator"], 1)

    def test_failed_attempt_stays_visible_beside_a_matching_pass(self):
        """Given one passing and one failed attempt
        When their case is reported
        Then both original outcomes remain visible
        """
        failed = {**self.index["executions"][0], "id": "RUN-2", "original_status": "failed", "outcome": "FAILED"}
        self.index["executions"].append(failed)
        report = self.coverage()
        row = report["matrices"]["AC_CASE"][0]["links"][0]
        self.assertEqual(row["matching_passing_execution_ids"], ["RUN-1"])
        self.assertEqual(row["nonpassing_execution_ids"], ["RUN-2"])
        self.assertEqual(report["execution_outcomes"], {"PASSED": 1, "FAILED": 1})

    def test_missing_source_or_environment_binding_cannot_fill_passing_coverage(self):
        """Given a passing execution without source or environment identity
        When coverage is calculated
        Then matching execution coverage remains zero
        """
        for field in ("source_binding", "environment_id"):
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.index)
                if field == "source_binding":
                    candidate["executions"][0].pop(field)
                else:
                    candidate["executions"][0][field] = None
                report = analyze_coverage(candidate, self.root)
                self.assertTrue(report["valid"], report)
                self.assertEqual(report["metrics"]["AC_CASE"]["has_matching_passing_execution"]["numerator"], 0)

    def test_stale_assertions_do_not_count_as_current_coverage(self):
        """Given changed assertion bytes
        When coverage is recalculated
        Then old outcomes stay recorded and current assertion coverage becomes zero
        """
        (self.root / "test.txt").write_text("assert False\n")
        report = self.coverage()
        self.assertTrue(report["valid"])
        self.assertEqual(report["freshness"], "STALE")
        self.assertEqual(report["metrics"]["AC_CASE"]["has_current_assertion_link"]["numerator"], 0)
        self.assertEqual(report["execution_outcomes"], {"PASSED": 1})

    def test_invalid_index_has_no_calculated_matrices(self):
        """Given a dangling assertion
        When coverage is requested
        Then no matrices or misleading percentages are generated
        """
        self.index["links"][0]["assertion_ids"] = ["absent"]
        report = self.coverage()
        self.assertFalse(report["valid"])
        self.assertEqual(report["matrices"], {})

    def test_untraced_business_changes_stay_distinct_from_maintenance(self):
        """Given business and maintenance changes without AC links
        When reported
        Then unsupported extra behavior candidates include business changes only
        """
        self.index["links"] = []
        self.index["changes"].append({**self.index["changes"][0], "id": "CH-2", "classification": "MAINTENANCE"})
        report = self.coverage()
        self.assertEqual(report["untraced_changes"], ["CH-1", "CH-2"])
        self.assertEqual(report["unsupported_extra_behavior_candidates"], ["CH-1"])
        self.assertEqual(report["cases_without_criteria"], ["TC-1"])
        self.assertEqual(report["change_groups"]["BUSINESS"]["ids"], ["CH-1"])
        self.assertEqual(report["change_groups"]["MAINTENANCE"]["ids"], ["CH-2"])
        self.assertEqual(report["change_groups"]["UNCHANGED"]["ids"], [])


class CaseLedgerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="case-ledger-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.manifest = {"schema_version": 1, "scope_id": "fixture", "sources": []}

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def browser(self):
        result = self.write("task/result.json", {"security_assertion_passed": False})
        bound = self.write("task/binding.json", {"revision": "historical-source"})
        row = {"id": "TC-1", "status": "FAILED", "original_status": None, "characterization": False,
               "result_workspace_path": result["path"], "result_sha256": result["sha256"],
               "source_binding": "binding.json", "source_binding_sha256": bound["sha256"],
               "limits": ["Controlled source only."]}
        source = self.write("inventory.json", {"status": "PASSED", "total": 1, "rows": [row],
                                                "counts": {"FAILED": 1}, "source_definition_mismatch_count": 1})
        self.manifest["sources"].append({"id": "browser", "format": "BROWSER_INVENTORY", "task_root": "task", **source})

    def jest(self, interrupted=False):
        source = self.write("jest.json", {"numTotalTests": 3, "numPassedTests": 1, "numFailedTests": 1,
            "wasInterrupted": interrupted, "testResults": [{"name": "/source/service.test.js", "status": "failed",
                "assertionResults": [{"fullName": "accepts valid", "status": "passed", "invocations": 2,
                                      "retryReasons": ["first assertion failed"]},
                                     {"fullName": "rejects invalid", "status": "failed", "failureMessages": ["accepted invalid"]}]}]})
        binding = self.write("jest-execution.json", {"revision": "historical-source", "results_sha256": source["sha256"], "exit_code": 1})
        self.manifest["sources"].append({"id": "unit", "format": "JEST_JSON", "binding": binding, **source})

    def ledger(self):
        return build_case_ledger(self.manifest, self.root)

    def test_browser_raw_status_is_not_invented_from_aggregate_disposition(self):
        """Given an aggregate failure and no raw runner status
        When imported
        Then failure provenance and absent raw status stay separate
        """
        self.browser()
        report = self.ledger()
        entry = report["entries"][0]
        self.assertEqual(entry["outcome"], "FAILED")
        self.assertIsNone(entry["original_status"])
        self.assertIsNone(entry["runner_original_status"])
        self.assertEqual(report["imports"][0]["original_summary"]["status"], "PASSED")
        self.assertEqual(report["imports"][0]["original_summary"]["source_definition_mismatch_count"], 1)
        self.assertEqual(report["freshness"], "CURRENT")
        self.assertEqual(entry["verification"], "NOT_VERIFIED")

    def test_duplicate_imports_remain_visible_without_inflating_unique_counts(self):
        """Given the same browser inventory twice
        When imported under distinct IDs
        Then both records remain and one unique attempt is counted
        """
        self.browser()
        self.manifest["sources"].append({**self.manifest["sources"][0], "id": "browser-repeat"})
        report = self.ledger()
        self.assertEqual(report["counts"]["imported_records"], 2)
        self.assertEqual(report["counts"]["unique_attempts"], 1)
        self.assertEqual(report["counts"]["duplicate_import_records"], 1)
        self.assertEqual(report["entries"][1]["duplicate_of"], "browser:0")
        self.assertEqual(report["counts"]["outcomes"], {"FAILED": 1})

    def test_retries_interruptions_and_missing_tests_are_not_hidden_by_final_pass(self):
        """Given an interrupted Jest run with a retried final pass
        When imported
        Then retry uncertainty, missing cases, failure, and interruption remain visible
        """
        self.jest(interrupted=True)
        report = self.ledger()
        self.assertEqual(report["counts"]["outcomes"], {"PASSED": 1, "FAILED": 1})
        self.assertEqual(report["counts"]["retried_case_records"], 1)
        self.assertEqual(report["counts"]["interrupted_records"], 2)
        self.assertEqual(report["entries"][0]["prior_attempt_outcomes"], "UNKNOWN")
        self.assertEqual(report["entries"][0]["original_case"]["retryReasons"], ["first assertion failed"])
        self.assertEqual(report["imports"][0]["unrepresented_declared_tests"], 1)

    def test_stale_wrapper_does_not_rewrite_jest_outcomes(self):
        """Given a wrapper identifying different result bytes
        When imported
        Then source freshness is stale and runner outcomes remain original
        """
        self.jest()
        self.manifest["sources"][0]["binding"] = self.write("other-binding.json", {"results_sha256": "0" * 64})
        report = self.ledger()
        self.assertEqual(report["freshness"], "STALE")
        self.assertEqual(report["entries"][0]["original_status"], "passed")
        self.assertEqual(report["counts"]["outcomes"], {"PASSED": 1, "FAILED": 1})

    def test_duplicate_jest_names_preserve_distinct_runner_instances(self):
        """Given two Jest assertions with the same full name
        When imported
        Then both positions and outcomes remain distinct
        """
        self.jest()
        path = self.root / "jest.json"
        data = json.loads(path.read_text())
        data["testResults"][0]["assertionResults"][1]["fullName"] = "accepts valid"
        self.manifest["sources"][0].update(self.write("jest.json", data))
        report = self.ledger()
        self.assertEqual(report["counts"]["unique_case_instances"], 2)
        self.assertEqual(report["counts"]["distinct_case_names"], 1)
        self.assertEqual(report["counts"]["outcomes"], {"PASSED": 1, "FAILED": 1})

    def test_missing_browser_bytes_remain_unknown_without_inventing_product_failure(self):
        """Given unavailable raw browser result bytes
        When imported
        Then freshness becomes unknown and aggregate failure remains only its original disposition
        """
        self.browser()
        (self.root / "task/result.json").unlink()
        report = self.ledger()
        self.assertEqual(report["freshness"], "UNKNOWN")
        self.assertEqual(report["entries"][0]["outcome"], "FAILED")
        self.assertIsNone(report["entries"][0]["runner_original_status"])

    def test_unknown_status_is_not_converted_to_a_pass_or_not_run(self):
        """Given an unfamiliar runner status
        When imported
        Then its original value remains and normalization is UNKNOWN
        """
        self.jest()
        path = self.root / "jest.json"
        data = json.loads(path.read_text())
        data["testResults"][0]["assertionResults"][0]["status"] = "aborted-by-worker"
        self.manifest["sources"][0].update(self.write("jest.json", data))
        report = self.ledger()
        self.assertEqual(report["entries"][0]["outcome"], "UNKNOWN")
        self.assertEqual(report["entries"][0]["original_status"], "aborted-by-worker")

    def test_unsafe_source_paths_are_rejected(self):
        """Given a source outside the workspace
        When imported
        Then traversal is rejected before any external read
        """
        self.manifest["sources"] = [{"id": "bad", "format": "JEST_JSON", "path": "../private.json", "sha256": "0" * 64}]
        with self.assertRaises(WorkbenchError):
            self.ledger()

    def test_changed_evidence_during_import_invalidates_the_report(self):
        """Given evidence changed after its initial read
        When final reconciliation runs
        Then the ledger becomes invalid and stale
        """
        self.jest()
        from ai_sdlc_workbench.review_coverage import _read
        calls = {}
        def changed_read(path):
            raw = _read(path)
            calls[str(path)] = calls.get(str(path), 0) + 1
            return raw + b" " if calls[str(path)] > 1 else raw
        with patch("ai_sdlc_workbench.review_coverage._read", side_effect=changed_read):
            report = self.ledger()
        self.assertFalse(report["valid"])
        self.assertEqual(report["freshness"], "STALE")
        self.assertIn("evidence_changed_during_check", {item["code"] for item in report["diagnostics"]})


if __name__ == "__main__":
    unittest.main()
