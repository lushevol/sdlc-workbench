"""Regressions for independent audit reconciliation checks."""

import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


MODULE = importlib.util.spec_from_file_location("audit_validator", Path(__file__).with_name("validate-audit-report.py"))
validator = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(validator)
audit = validator.audit


class AuditValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.case = self.workspace / "application/run-001/cases/case-1"
        self.case.mkdir(parents=True)
        self.image = self.case / "001-step.png"
        self.image.write_bytes(base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+yWioAAAAASUVORK5CYII="))
        self.steps = [{"number": 1, "keyword": "Then", "text": "the result is visible", "line": 10,
                       "status": "FAILED", "startedAt": "2026-10-22T01:00:00Z", "endedAt": "2026-10-22T01:00:01Z",
                       "frameSequences": [1]}]
        self.definition = {"steps": self.steps, "catalogSha256": "catalog-hash"}
        self.row = {"caseId": "AUTH-001", "totalSteps": 1}
        self.result = {"actualStatus": "failed", "assertionsSatisfied": False,
                       "canonicalIdsMentioned": ["AUTH-001"], "startedAt": "2026-10-22T01:00:00Z",
                       "endedAt": "2026-10-22T01:00:01Z"}
        self.canonical = {"caseId": "AUTH-001", "sha256": "catalog-hash", "steps": self.steps}
        self.frame = {"sequence": 1, "canonicalStep": 1, "capturedAt": "2026-10-22T01:00:00.500Z",
                      "path": str(self.image), "sha256": audit.sha256(self.image), "claim": "Actual failure state", "step": "catalog:10"}

    def make_attempt(self):
        audit.save_json(self.case / "result.json", self.result)
        audit.save_json(self.case / "frames.json", {"canonical": self.canonical, "frames": [self.frame]})
        audit.save_json(self.case / "artifact-manifest.json", {"artifacts": [audit.reference(file, self.workspace)
                        for file in sorted(self.case.iterdir()) if file.name != "artifact-manifest.json"]})
        inputs = self.workspace / "application/run-001/run-inputs.json"
        audit.save_json(inputs, {"sourceHashes": []})
        attempt = {"attemptId": "application/run-001/case-1", "observedStatus": "FAIL", "runnerStatus": "failed",
                   "startedAt": self.result["startedAt"], "endedAt": self.result["endedAt"],
                   "result": audit.reference(self.case / "result.json", self.workspace),
                   "manifest": audit.reference(self.case / "artifact-manifest.json", self.workspace),
                   "runInputs": audit.reference(inputs, self.workspace), "canonical": self.canonical,
                   "steps": self.steps, "frames": [{**self.frame, "width": 1, "height": 1}]}
        return {**attempt, **audit.step_evidence(attempt, self.definition, self.row)}

    def test_execution_status_remains_independent_of_quality(self):
        self.assertEqual(validator.actual_status({"actualStatus": "failed", "canonicalQualityStatus": "FAIL"}), "FAIL")
        self.assertEqual(validator.actual_status({"actualStatus": "passed", "assertionsSatisfied": True,
                                                 "canonicalQualityStatus": "FAIL", "captureStatus": "MISSING"}), "PASS")
        for status in ("skipped", "interrupted"):
            self.assertEqual(validator.actual_status({"actualStatus": status}), "BLOCKED_NOT_EXECUTED")
        self.assertEqual(validator.actual_status({"actualStatus": "timedOut"}), "FAIL")

    def test_attempt_order_uses_timestamp_then_identifier(self):
        records = [{"endedAt": "2026-10-22T02:00:00Z", "attemptId": "run-002"},
                   {"endedAt": "2026-10-22T01:00:00Z", "attemptId": "run-002"},
                   {"endedAt": "2026-10-22T01:00:00Z", "attemptId": "run-001"}]
        self.assertTrue(validator.newest_first(records))
        self.assertFalse(validator.newest_first(list(reversed(records))))

    def test_actual_failure_screenshot_can_have_complete_step_evidence(self):
        attempt = self.make_attempt()
        review = validator.Validation(self.workspace)
        review.attempt(attempt, self.definition, self.row)
        self.assertEqual(review.errors, [])
        self.assertTrue(attempt["completeStepEvidence"])
        self.assertEqual(attempt["observedStatus"], "FAIL")

    def test_wrong_result_status_is_rejected_even_with_valid_hashes(self):
        attempt = self.make_attempt()
        attempt["observedStatus"] = "PASS"
        review = validator.Validation(self.workspace)
        review.attempt(attempt, self.definition, self.row)
        self.assertIn("ATTEMPT_STATUS_MISMATCH", {error["code"] for error in review.errors})

    def test_declared_synthetic_history_cannot_be_upgraded_to_actual_execution(self):
        self.result["scope"] = "SYNTHETIC_HARNESS"
        attempt = self.make_attempt()
        attempt.update(run="application/run-001", scope="SYNTHETIC_HARNESS", pathCategory="application",
                       evidenceCategory="ACTUAL_APPLICATION", classificationLimits=[])
        review = validator.Validation(self.workspace)
        review.classification(attempt, "ACTUAL_APPLICATION")
        self.assertIn("EVIDENCE_CATEGORY_MISMATCH", {error["code"] for error in review.errors})
        attempt.update(evidenceCategory="HISTORICAL_DECLARED_SYNTHETIC", classificationLimits=["Scope conflict remains unresolved."])
        review = validator.Validation(self.workspace)
        review.classification(attempt, "HISTORICAL_DECLARED_SYNTHETIC")
        self.assertEqual(review.errors, [])

    def test_empty_screenshot_is_rejected_even_with_updated_hashes(self):
        self.image.write_bytes(b"")
        self.frame["sha256"] = audit.sha256(self.image)
        attempt = self.make_attempt()
        review = validator.Validation(self.workspace)
        review.attempt(attempt, self.definition, self.row)
        self.assertIn("EMPTY_OR_INVALID_SCREENSHOT", {error["code"] for error in review.errors})

    def test_unexecuted_frame_cannot_claim_a_step_state(self):
        self.steps[0]["status"] = "NOT_EXECUTED"
        self.result["actualStatus"] = "skipped"
        attempt = self.make_attempt()
        attempt.update(observedStatus="BLOCKED_NOT_EXECUTED", runnerStatus="skipped")
        review = validator.Validation(self.workspace)
        review.attempt(attempt, self.definition, self.row)
        self.assertIn("UNEXECUTED_FRAME_BINDING", {error["code"] for error in review.errors})

    def test_historical_invalid_binding_stays_visible_without_claiming_step_coverage(self):
        self.steps[0]["status"] = "NOT_EXECUTED"
        self.result["actualStatus"] = "skipped"
        attempt = self.make_attempt()
        attempt.update(observedStatus="BLOCKED_NOT_EXECUTED", runnerStatus="skipped")
        review = validator.Validation(self.workspace)
        review.attempt(attempt, self.definition, self.row, historical=True)
        self.assertEqual(review.errors, [])
        self.assertEqual(len(review.findings), 1)
        finding = review.findings[0]
        self.assertEqual(finding["severity"], "HISTORICAL_INVALID_STEP_BINDING")
        self.assertEqual(finding["result"], attempt["result"])
        self.assertEqual(finding["framesMetadata"]["sha256"], audit.sha256(self.case / "frames.json"))
        self.assertEqual(finding["screenshots"][0]["sha256"], audit.sha256(self.image))
        self.assertEqual(attempt["stepsWithScreenshots"], 0)
        self.assertEqual(attempt["stepTimeline"][0]["frameSequences"], [])
        self.assertFalse(attempt["completeStepEvidence"])
        latest_review = validator.Validation(self.workspace)
        latest_review.attempt(attempt, self.definition, self.row)
        self.assertIn("UNEXECUTED_FRAME_BINDING", {error["code"] for error in latest_review.errors})

    def test_historical_classification_does_not_relax_artifact_integrity(self):
        attempt = self.make_attempt()
        self.image.write_bytes(b"corrupted")
        review = validator.Validation(self.workspace)
        review.attempt(attempt, self.definition, self.row, historical=True)
        codes = {error["code"] for error in review.errors}
        self.assertIn("HASH_MISMATCH", codes)
        self.assertIn("EMPTY_OR_INVALID_SCREENSHOT", codes)

    def test_historical_source_mismatch_is_a_limit_and_snapshot_corruption_is_an_error(self):
        source = self.workspace / "source.ts"
        source.write_text("new source\n", encoding="utf-8")
        snapshot = self.workspace / "snapshot.ts"
        snapshot.write_text("old source\n", encoding="utf-8")
        expected = audit.sha256(snapshot)
        inputs = self.workspace / "run-inputs.json"
        audit.save_json(inputs, {"sourceHashes": [{"path": "source.ts", "sha256": expected, "snapshotPath": str(snapshot)}]})
        runs = [{"name": "application/run-001", "inputs": {"path": str(inputs)}}]
        review = validator.Validation(self.workspace)
        limits = review.source_provenance(self.workspace, runs)
        self.assertEqual(review.errors, [])
        self.assertEqual(limits[0]["recordedSha256"], expected)
        self.assertEqual(limits[0]["retention"], ["RUN_SOURCE_SNAPSHOT"])
        snapshot.write_text("changed evidence\n", encoding="utf-8")
        review = validator.Validation(self.workspace)
        review.source_provenance(self.workspace, runs)
        self.assertIn("SOURCE_SNAPSHOT_HASH_MISMATCH", {error["code"] for error in review.errors})


if __name__ == "__main__":
    unittest.main()
