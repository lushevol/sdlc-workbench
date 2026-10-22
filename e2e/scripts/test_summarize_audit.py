"""Regression checks for audit result history and canonical screenshot evidence."""

import base64
import copy
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("summarize-audit.py")
SPEC = importlib.util.spec_from_file_location("summarize_audit", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class ReportElements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.text = []
        self.details = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("section", "details", "li"):
            self.stack.append((tag, attrs))
        if tag == "details":
            self.details.append(attrs)

    def handle_endtag(self, tag):
        if tag in ("section", "details", "li"):
            self.stack.pop()

    def handle_data(self, data):
        if data.strip():
            self.text.append((data.strip(), list(self.stack)))


class AuditReportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.catalog = self.workspace / "test-cases.md"
        self.catalog.write_text("Canonical fixture\n", encoding="utf-8")
        self.steps = [
            {"number": 1, "keyword": "Given", "text": "the login page is open", "line": 10},
            {"number": 2, "keyword": "Then", "text": "the sign-in button is visible", "line": 11},
        ]
        self.definition = {"title": "Login controls", "gherkin": "Given the login page is open\nThen the sign-in button is visible",
                           "catalog": self.catalog, "catalogSha256": audit.sha256(self.catalog), "steps": self.steps}
        self.row = {"caseId": "AUTH-001", "definition": "test-cases.md#auth-001", "definitionLine": 1,
                    "definitionVersion": 2, "definitionSha256": "definition-hash", "canonicalQualityStatus": "UNVERIFIED",
                    "mappingStatus": "PARTIAL", "assertionCount": 1, "uiAssertionCount": 1, "functionalAssertionCount": 0,
                    "reasonCodes": ["PARTIAL_BINDING"], "preflightStatus": "BLOCKED_NOT_EXECUTED", "requiredFrames": [],
                    "totalSteps": 2}

    def attempt(self, status="PASS", *, ended="2026-10-22T01:00:04Z", name="run-001", legacy=False):
        steps = [{**step, "status": "PASSED", "startedAt": f"2026-10-22T01:00:0{step['number']}Z",
                  "endedAt": f"2026-10-22T01:00:0{step['number'] + 1}Z", "frameSequences": [step["number"]]}
                 for step in self.steps]
        frames = [{"sequence": step["number"], "phase": f"step-{step['number']}", "claim": step["text"],
                   "step": f"test-cases.md:{step['line']}", "canonicalStep": step["number"],
                   "capturedAt": f"2026-10-22T01:00:0{step['number']}.500Z", "path": f"step-{step['number']}.png",
                   "sha256": "image-hash", "width": 800, "height": 600} for step in self.steps]
        return {"attemptId": f"application/{name}/case-1", "run": f"application/{name}",
                "caseId": "case-1", "testId": "test-1", "title": "Login controls", "source": "login.spec.ts:1",
                "startedAt": "2026-10-22T01:00:00Z", "endedAt": ended,
                "scope": "ACTUAL_APPLICATION_LOCAL_SERVICES", "observedStatus": status,
                "runnerStatus": "passed" if status == "PASS" else "failed", "assertionsSatisfied": status == "PASS",
                "canonicalIdsMentioned": ["AUTH-001"], "result": {"path": "result.json", "sha256": "result-hash"},
                "manifest": {"path": "artifact-manifest.json"}, "runInputs": {"path": "run-inputs.json"},
                "captureStatus": "CAPTURED", "captureGaps": [], "fixture": "Controlled local services.",
                "attachments": [], "observations": [], "errors": [] if status == "PASS" else [{"message": "Retained failure"}],
                "limits": [], "frames": frames, "steps": [] if legacy else steps,
                "canonical": None if legacy else {"caseId": "AUTH-001", "sha256": self.definition["catalogSha256"], "steps": steps}}

    def reconcile(self, attempts):
        return audit.reconcile([self.row], attempts, [], {"AUTH-001": self.definition})[0]

    def render(self, record):
        output = self.workspace / "report"
        output.mkdir()
        payload = {"cases": [record], "harnessAttempts": [], "summary": {
            "canonicalCases": 1, "applicationAttempts": len(record["actualApplicationAttempts"]), "harnessAttempts": 0}}
        audit.render(output, payload, {"AUTH-001": self.definition}, self.workspace)
        document = (output / "cases" / "AUTH-001.html").read_text(encoding="utf-8")
        parsed = ReportElements()
        parsed.feed(document)
        return document, parsed

    def test_latest_pass_precedes_collapsed_failure_history(self):
        failed = self.attempt("FAIL", name="run-001")
        passed = self.attempt("PASS", name="run-002", ended="2026-10-22T02:00:04Z")
        originals = copy.deepcopy([failed, passed])
        record = self.reconcile([passed, failed])
        self.assertEqual(record["localPredicateStatus"], "PASS")
        self.assertEqual(record["actualApplicationAttempts"][0]["attemptId"], passed["attemptId"])
        self.assertEqual(record["canonicalAcceptanceStatus"], "NOT_ESTABLISHED")
        document, parsed = self.render(record)
        latest_pass = next(i for i, (text, stack) in enumerate(parsed.text)
                           if text == "PASS" and any(attrs.get("class") == "latest-attempt" for _, attrs in stack))
        earlier_fail = next(i for i, (text, stack) in enumerate(parsed.text)
                           if text == "FAIL" and any(attrs.get("class") == "historical-attempt" for _, attrs in stack))
        self.assertLess(latest_pass, earlier_fail)
        for attrs in parsed.details:
            if attrs.get("class") in ("attempt-history", "historical-attempt"):
                self.assertNotIn("open", attrs)
        self.assertIn("Earlier attempt FAIL (superseded by latest PASS)", document)
        self.assertIn("Retained failure", document)
        self.assertEqual([failed, passed], originals)

    def test_legacy_pass_does_not_claim_complete_step_screenshots(self):
        record = self.reconcile([self.attempt(legacy=True)])
        self.assertEqual(record["localPredicateStatus"], "PASS")
        self.assertEqual(record["stepEvidenceStatus"], "LEGACY_ESSENTIAL_FRAMES")
        self.assertFalse(record["completeStepEvidence"])
        self.assertEqual(record["stepsWithScreenshots"], 0)
        document, parsed = self.render(record)
        self.assertIn("Step evidence not recorded.", document)
        self.assertIn("0/2 canonical steps have execution screenshots", document)
        steps = [attrs for tag, attrs in [item for _, stack in parsed.text for item in stack]
                 if tag == "li" and "data-step" in attrs]
        self.assertEqual({step["data-step"] for step in steps}, {"1", "2"})

    def test_quality_and_capture_limits_do_not_erase_actual_execution(self):
        self.row["canonicalQualityStatus"] = "FAIL"
        attempt = self.attempt("FAIL")
        attempt["captureStatus"] = "INCOMPLETE"
        attempt["captureGaps"] = [{"error": "Screenshot capture failed"}]
        record = self.reconcile([attempt])
        self.assertEqual(record["localPredicateStatus"], "FAIL")
        self.assertEqual(record["latestObservedStatus"], "FAIL")
        self.assertEqual(record["canonicalQualityStatus"], "FAIL")
        self.assertEqual(record["canonicalAcceptanceStatus"], "NOT_ESTABLISHED")
        self.assertIn("CANONICAL_QUALITY_FAIL_BLOCKS_ACCEPTANCE", record["reasonCodes"])
        self.assertIn("ESSENTIAL_SCREENSHOT_EVIDENCE_INCOMPLETE", record["reasonCodes"])
        self.assertEqual(self.reconcile([])["localPredicateStatus"], "BLOCKED_NOT_EXECUTED")

    def test_historical_definition_failure_is_distinct_from_latest_execution_pass(self):
        self.row["canonicalQualityStatus"] = "FAIL"
        record = self.reconcile([self.attempt("PASS")])
        document, parsed = self.render(record)
        self.assertEqual(record["localPredicateStatus"], "PASS")
        self.assertEqual(record["canonicalQualityStatus"], "FAIL")
        self.assertEqual(record["canonicalAcceptanceStatus"], "NOT_ESTABLISHED")
        self.assertIn('Latest local result: <span class="badge PASS">PASS</span>', document)
        self.assertIn("Historical definition review (preflight): FAIL", document)
        self.assertIn("A definition review FAIL can coexist with local PASS.", document)
        definition = next(attrs for attrs in parsed.details if attrs.get("class") == "definition-review")
        self.assertNotIn("open", definition)
        index = (self.workspace / "report" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Definition review (preflight)", index)
        self.assertIn("A definition review FAIL can coexist with local PASS.", index)

    def test_missing_or_wrongly_bound_frames_cannot_complete_coverage(self):
        for mutation in ("missing", "wrong-step", "wrong-time", "wrong-text", "wrong-line", "wrong-hash"):
            with self.subTest(mutation=mutation):
                attempt = self.attempt()
                if mutation == "missing":
                    attempt["steps"][1]["frameSequences"] = [99]
                elif mutation == "wrong-step":
                    attempt["frames"][1]["canonicalStep"] = 1
                elif mutation == "wrong-time":
                    attempt["frames"][1]["capturedAt"] = "2026-10-22T02:00:00Z"
                elif mutation == "wrong-text":
                    attempt["steps"][1]["text"] = "an unrelated assertion passes"
                elif mutation == "wrong-line":
                    attempt["steps"][1]["line"] = 99
                else:
                    attempt["canonical"]["sha256"] = "stale-catalog"
                result = self.reconcile([attempt])
                self.assertEqual(result["localPredicateStatus"], "PASS")
                self.assertEqual(result["stepEvidenceStatus"], "INCOMPLETE")
                self.assertFalse(result["completeStepEvidence"])
                self.assertTrue(result["stepEvidenceGaps"])

    def test_not_executed_steps_do_not_receive_execution_screenshots(self):
        attempt = self.attempt("FAIL")
        attempt["steps"][0]["status"] = "FAILED"
        attempt["steps"][1]["status"] = "NOT_EXECUTED"
        result = self.reconcile([attempt])
        self.assertEqual(result["stepsWithScreenshots"], 1)
        self.assertFalse(result["completeStepEvidence"])
        self.assertEqual(result["actualApplicationAttempts"][0]["stepTimeline"][1]["frameSequences"], [])

    def test_final_step_failure_can_have_complete_screenshot_evidence(self):
        attempt = self.attempt("FAIL")
        attempt["steps"][1]["status"] = "FAILED"
        result = self.reconcile([attempt])
        self.assertEqual(result["localPredicateStatus"], "FAIL")
        self.assertEqual(result["stepEvidenceStatus"], "COMPLETE")
        self.assertTrue(result["completeStepEvidence"])
        self.assertEqual(result["canonicalAcceptanceStatus"], "NOT_ESTABLISHED")

    def test_partial_execution_keeps_prerequisite_and_missing_steps_visible(self):
        attempt = self.attempt("FAIL")
        attempt.update(observedStatus="BLOCKED_NOT_EXECUTED", runnerStatus="skipped", errors=[],
                       executionBlockers=[{"code": "VIEWER_UNAVAILABLE", "owner": "Unknown",
                                           "consequence": "The export ran. The viewer did not run.",
                                           "nextAction": "Provide the required viewer."}])
        attempt["steps"][1]["status"] = "NOT_EXECUTED"
        record = self.reconcile([attempt])
        self.assertEqual(record["localPredicateStatus"], "BLOCKED_NOT_EXECUTED")
        self.assertIn("VIEWER_UNAVAILABLE", record["reasonCodes"])
        self.assertEqual(record["stepsWithScreenshots"], 1)
        self.assertFalse(record["completeStepEvidence"])
        document, _ = self.render(record)
        self.assertIn("Execution prerequisite: VIEWER_UNAVAILABLE", document)
        self.assertIn("Provide the required viewer.", document)

    def test_retained_canonical_metadata_reaches_reconciled_coverage(self):
        attempt = self.attempt()
        directory = self.workspace / "application" / "run-001" / "cases" / "case-1"
        directory.mkdir(parents=True)
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+yWioAAAAASUVORK5CYII=")
        for frame in attempt["frames"]:
            file = directory / f"step-{frame['sequence']}.png"
            file.write_bytes(png)
            frame.update(path=str(file), sha256=audit.sha256(file))
        audit.save_json(directory / "frames.json", {"canonical": attempt["canonical"], "frames": attempt["frames"],
                        "captureStatus": "CAPTURED", "captureGaps": [], "fixture": attempt["fixture"]})
        result = {"caseId": "case-1", "testId": "test-1", "title": "Login controls", "source": "login.spec.ts:1",
                  "startedAt": attempt["startedAt"], "endedAt": attempt["endedAt"], "scope": attempt["scope"],
                  "actualStatus": "passed", "assertionsSatisfied": True, "canonicalIdsMentioned": ["AUTH-001"]}
        audit.save_json(directory / "result.json", result)
        audit.save_json(directory / "artifact-manifest.json", {"artifacts": [audit.reference(file, self.workspace)
                        for file in sorted(directory.iterdir())]})
        inspected = audit.inspect_attempt(directory / "result.json", {"name": "application/run-001", "category": "application",
                                         "inputs": {"path": "run-inputs.json"}}, self.workspace)
        record = self.reconcile([inspected])
        self.assertTrue(record["completeStepEvidence"])
        self.assertEqual(record["stepsWithScreenshots"], 2)

    def test_user_scope_exclusion_is_distinct_from_an_execution_blocker(self):
        decision = {"caseId": "AUTH-001", "prerequisite": "Selected native runtime", "userInstruction": "skip them"}
        records = audit.reconcile([self.row], [], [], {"AUTH-001": self.definition}, {"AUTH-001": decision})
        record = records[0]
        self.assertEqual(record["localPredicateStatus"], "SKIPPED_BY_USER")
        self.assertEqual(record["latestObservedStatus"], "NOT_RUN")
        self.assertEqual(record["scopeStatus"], "EXCLUDED_BY_USER")
        self.assertEqual(record["scopeExclusion"], decision)
        self.assertEqual(record["stepsWithScreenshots"], 0)
        document, _ = self.render(record)
        self.assertIn("Skipped by user scope decision", document)
        self.assertIn("Selected native runtime", document)
        self.assertEqual(self.reconcile([])["localPredicateStatus"], "BLOCKED_NOT_EXECUTED")

    def test_mis_scoped_history_cannot_override_actual_application_result(self):
        for number, scope, status in ((1, "ACTUAL_APPLICATION_LOCAL_SERVICES", "passed"),
                                      (2, "SYNTHETIC_HARNESS", "failed")):
            run = self.workspace / "application" / f"run-{number:03}"
            directory = run / "cases" / "case-1"
            directory.mkdir(parents=True)
            source = self.attempt()
            result = {key: source[key] for key in ("caseId", "testId", "title", "source", "startedAt", "canonicalIdsMentioned")}
            result.update(scope=scope, actualStatus=status, assertionsSatisfied=status == "passed",
                          endedAt=f"2026-10-22T0{number}:00:04Z")
            audit.save_json(directory / "result.json", result)
            audit.save_json(directory / "artifact-manifest.json", {"artifacts": [audit.reference(directory / "result.json", self.workspace)]})
            audit.save_json(run / "run-inputs.json", {"sourceHashes": []})
            audit.save_json(run / "run-result.json", {"runnerStatus": status, "plannedTests": 1, "completedTests": 1,
                            "statuses": {status: 1}, "screenshotFrames": 0})
        runs, application, non_application = audit.load_runs(self.workspace, self.workspace)
        self.assertEqual(len(runs), 2)
        self.assertEqual(len(application), 1)
        self.assertEqual(len(non_application), 1)
        historical = non_application[0]
        self.assertEqual(historical["scope"], "SYNTHETIC_HARNESS")
        self.assertEqual(historical["pathCategory"], "application")
        self.assertEqual(historical["evidenceCategory"], "HISTORICAL_DECLARED_SYNTHETIC")
        self.assertTrue(historical["classificationLimits"])
        record = audit.reconcile([self.row], application, non_application, {"AUTH-001": self.definition})[0]
        self.assertEqual(record["localPredicateStatus"], "PASS")
        self.assertEqual(record["relatedHarnessAttempts"], [historical["attemptId"]])
        output = self.workspace / "report"
        output.mkdir()
        audit.render(output, {"cases": [record], "harnessAttempts": [], "historicalDeclaredSyntheticAttempts": non_application,
                     "summary": {"canonicalCases": 1, "applicationAttempts": 1, "harnessAttempts": 0,
                                 "historicalDeclaredSyntheticAttempts": 1}}, {"AUTH-001": self.definition}, self.workspace)
        history_html = (output / "harness" / (historical["attemptId"].replace("/", "--") + ".html")).read_text()
        self.assertIn("Review retained traces for actual activity", history_html)
        self.assertNotIn("This check does not execute the actual MFE", history_html)

    def test_scope_exclusion_preserves_an_earlier_failed_attempt(self):
        attempt = self.attempt("FAIL")
        decision = {"caseId": "AUTH-001", "prerequisite": "Selected native runtime", "userInstruction": "skip them"}
        record = audit.reconcile([self.row], [attempt], [], {"AUTH-001": self.definition}, {"AUTH-001": decision})[0]
        self.assertEqual(record["localPredicateStatus"], "SKIPPED_BY_USER")
        self.assertEqual(record["latestObservedStatus"], "FAIL")
        self.assertEqual(record["actualApplicationAttempts"][0]["observedStatus"], "FAIL")
        self.assertEqual(record["canonicalAcceptanceStatus"], "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
