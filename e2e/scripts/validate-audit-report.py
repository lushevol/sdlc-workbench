#!/usr/bin/env python3
"""Read an audit report and verify its case, result, step, screenshot, and HTML bindings."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys


MODULE = importlib.util.spec_from_file_location("audit_summary", Path(__file__).with_name("summarize-audit.py"))
audit = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(audit)


def actual_status(result: dict) -> str:
    if result.get("actualStatus") in ("skipped", "interrupted"):
        return "BLOCKED_NOT_EXECUTED"
    if result.get("actualStatus") == "passed" and result.get("assertionsSatisfied"):
        return "PASS"
    return "FAIL"


def newest_first(attempts: list[dict]) -> bool:
    keys = [(attempt["endedAt"], attempt["attemptId"]) for attempt in attempts]
    return keys == sorted(keys, reverse=True)


class DetailsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.history_details = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "details" and values.get("class") in ("attempt-history", "historical-attempt"):
            self.history_details.append(values)


class Validation:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.errors = []
        self.findings = []
        self.limits = []
        self.counts = Counter()

    def check(self, condition: bool, code: str, locator: str, detail: str) -> None:
        self.counts["checks"] += 1
        if not condition:
            self.errors.append({"code": code, "locator": locator, "detail": detail})

    @lru_cache(maxsize=None)
    def digest(self, file: Path) -> str | None:
        if not file.is_file():
            return None
        return hashlib.sha256(file.read_bytes()).hexdigest()

    def file_reference(self, reference: dict, label: str) -> Path:
        file = audit.resolve(reference["path"], self.workspace)
        self.check(self.digest(file) == reference["sha256"], "HASH_MISMATCH", label,
                   f"Retained bytes differ or are unavailable: {reference['path']}")
        if "bytes" in reference and file.is_file():
            self.check(file.stat().st_size == reference["bytes"], "SIZE_MISMATCH", label, reference["path"])
        self.counts["fileReferences"] += 1
        return file

    def manifest(self, file: Path) -> None:
        if not file.is_file():
            self.check(False, "MISSING_MANIFEST", str(file), "The artifact manifest is unavailable.")
            return
        for reference in audit.read(file)["artifacts"]:
            self.file_reference(reference, str(file))

    def classification(self, attempt: dict, expected: str) -> None:
        label = attempt["attemptId"]
        result = audit.read(audit.resolve(attempt["result"]["path"], self.workspace))
        path_category = attempt["run"].split("/", 1)[0]
        scope = result.get("scope")
        category = ("HISTORICAL_DECLARED_SYNTHETIC" if path_category == "application" and scope == "SYNTHETIC_HARNESS"
                    else "SYNTHETIC_HARNESS" if path_category == "harness" and scope == "SYNTHETIC_HARNESS"
                    else "ACTUAL_APPLICATION" if path_category == "application" else "INVALID")
        self.check(attempt.get("scope") == scope, "DECLARED_SCOPE_MISMATCH", label,
                   "The report must preserve the original declared scope.")
        self.check(attempt.get("pathCategory") == path_category and attempt.get("evidenceCategory") == category == expected,
                   "EVIDENCE_CATEGORY_MISMATCH", label, "Declared synthetic attempts cannot select canonical local results.")
        if expected == "HISTORICAL_DECLARED_SYNTHETIC":
            self.check(bool(attempt.get("classificationLimits")), "MISSCOPED_HISTORY_LIMIT_MISSING", label,
                       "Disclose the path and scope conflict without inferring that no application activity occurred.")

    def non_application_attempt(self, attempt: dict, expected: str) -> None:
        label = attempt["attemptId"]
        result_file = self.file_reference(attempt["result"], label)
        manifest_file = self.file_reference(attempt["manifest"], label)
        self.manifest(manifest_file)
        self.file_reference(attempt["runInputs"], label)
        self.classification(attempt, expected)
        retained = audit.inspect_attempt(result_file, {"name": attempt["run"], "category": attempt["pathCategory"],
                                        "inputs": attempt["runInputs"]}, self.workspace)
        # Older immutable reports predate derived image-identity annotations.
        for recorded, current in zip(attempt["frames"], retained["frames"]):
            if "sameImageAsSequence" not in recorded:
                current.pop("sameImageAsSequence", None)
            self.frame_observations(recorded, current, label)
        self.check(attempt == retained, "NON_APPLICATION_RECONCILIATION", label,
                   "Historical and harness evidence must preserve retained results, frames, traces, and classification.")
        self.counts["nonApplicationAttempts"] += 1

    def frame_observations(self, frame: dict, original: dict, label: str) -> None:
        """Check optional context metadata without upgrading machine context into visual review."""
        target = frame.get("targetPageLabel")
        if "targetPageLabel" in frame or "targetPageLabel" in original:
            self.check(target == original.get("targetPageLabel") and isinstance(target, str) and bool(target.strip()),
                       "CAPTURE_PAGE_LABEL", label, "Preserve the nonempty captured-page identity.")
        for key in ("observationsBefore", "observationsAfter"):
            if key not in frame and key not in original:
                continue
            value = frame.get(key)
            self.check(value == original.get(key), "CAPTURE_OBSERVATIONS_MISMATCH", label, key)
            self.check(isinstance(value, dict), "CAPTURE_OBSERVATIONS_TYPE", label, key)
            if not isinstance(value, dict):
                continue
            session = value.get("session")
            if session is None:
                continue
            self.check(isinstance(session, dict), "CAPTURE_SESSION_TYPE", label, key)
            if not isinstance(session, dict):
                continue
            page_label = session.get("pageLabel")
            if "pageLabel" in session:
                self.check(isinstance(page_label, str) and bool(page_label.strip()), "CAPTURE_SESSION_PAGE_LABEL", label, key)
                if target is not None:
                    self.check(page_label == target, "CAPTURE_PAGE_TARGET_MISMATCH", label, key)
            clock = session.get("clock")
            if clock is not None:
                self.check(isinstance(clock, dict), "CAPTURE_CLOCK_TYPE", label, key)
                if isinstance(clock, dict):
                    self.check(clock.get("mode") == "PLAYWRIGHT_CONTROLLED", "CAPTURE_CLOCK_MODE", label, key)
                    for field in ("originMs", "nowMs", "elapsedMs", "refreshExpiryMs", "cutoffMs", "cutoffRemainingMs"):
                        number = clock.get(field)
                        self.check(number is None or (type(number) in (int, float) and math.isfinite(number)),
                                   "CAPTURE_CLOCK_VALUE", label, f"{key}.{field}")
                    if all(type(clock.get(field)) in (int, float) for field in ("originMs", "nowMs", "elapsedMs")):
                        self.check(clock["elapsedMs"] == clock["nowMs"] - clock["originMs"],
                                   "CAPTURE_CLOCK_ELAPSED", label, key)
                    if all(type(clock.get(field)) in (int, float) for field in ("cutoffMs", "nowMs", "cutoffRemainingMs")):
                        self.check(clock["cutoffRemainingMs"] == clock["cutoffMs"] - clock["nowMs"],
                                   "CAPTURE_CLOCK_REMAINING", label, key)
            for group, fields in (("ui", ("dialogVisible", "extendVisible", "extendEnabled", "logoutVisible", "logoutEnabled")),
                                  ("state", ("accessPresent", "refreshPresent", "isOnLogout", "isLoading"))):
                values = session.get(group)
                if values is None:
                    continue
                self.check(isinstance(values, dict), "CAPTURE_STATE_TYPE", label, f"{key}.{group}")
                if isinstance(values, dict):
                    for field in fields:
                        if field in values:
                            self.check(type(values[field]) is bool, "CAPTURE_STATE_VALUE", label, f"{key}.{group}.{field}")

    def source_provenance(self, root: Path, runs: list[dict]) -> list[dict]:
        variants = {}
        for file in sorted((root / "source-variants").glob("*.json")):
            item = audit.read(file)
            snapshot = audit.resolve(item["snapshot"], self.workspace)
            self.check(self.digest(snapshot) == item["sha256"], "SOURCE_VARIANT_HASH_MISMATCH", str(file), item["source"])
            variants[item["source"], item["sha256"]] = str(snapshot)
        groups = defaultdict(lambda: {"runs": [], "retention": set()})
        for run in runs:
            inputs_file = audit.resolve(run["inputs"]["path"], self.workspace)
            inputs = audit.read(inputs_file)
            for item in inputs.get("sourceHashes", []):
                source = audit.resolve(item["path"], self.workspace)
                current = self.digest(source)
                retention = "CURRENT_BYTES_MATCH"
                snapshot = item.get("snapshotPath")
                if snapshot:
                    saved = audit.resolve(snapshot, self.workspace)
                    self.check(self.digest(saved) == item["sha256"], "SOURCE_SNAPSHOT_HASH_MISMATCH", str(inputs_file), snapshot)
                    retention = "RUN_SOURCE_SNAPSHOT"
                elif (item["path"], item["sha256"]) in variants:
                    retention = "RETAINED_SOURCE_VARIANT"
                elif current != item["sha256"]:
                    retention = "HISTORICAL_BYTES_NOT_RETAINED"
                if current != item["sha256"]:
                    key = (item["path"], item["sha256"], current)
                    groups[key]["runs"].append(run["name"])
                    groups[key]["retention"].add(retention)
                self.counts["sourceBindings"] += 1
        limits = [{"path": path, "recordedSha256": recorded, "currentSha256": current,
                   "runs": sorted(set(value["runs"])), "retention": sorted(value["retention"]),
                   "claimLimit": "These attempts establish their recorded source variant. They do not establish unchanged current-source execution."}
                  for (path, recorded, current), value in sorted(groups.items())]
        return limits

    def attempt(self, attempt: dict, definition: dict, row: dict, *, historical: bool = False) -> None:
        label = attempt["attemptId"]
        result_file = self.file_reference(attempt["result"], label)
        manifest_file = self.file_reference(attempt["manifest"], label)
        self.manifest(manifest_file)
        self.file_reference(attempt["runInputs"], label)
        result = audit.read(result_file)
        self.check(attempt["observedStatus"] == actual_status(result), "ATTEMPT_STATUS_MISMATCH", label,
                   "The local result must follow the actual runner status and assertion result.")
        for key, raw_key in (("runnerStatus", "actualStatus"), ("startedAt", "startedAt"), ("endedAt", "endedAt")):
            self.check(attempt[key] == result[raw_key], "ATTEMPT_METADATA_MISMATCH", label, key)
        self.check(result.get("canonicalIdsMentioned") == [row["caseId"]], "CANONICAL_RESULT_BINDING", label,
                   "Each application attempt must bind exactly one canonical case.")
        frames_file = result_file.parent / "frames.json"
        raw = audit.read(frames_file) if frames_file.exists() else {}
        self.check(attempt.get("canonical") == raw.get("canonical"), "CANONICAL_METADATA_MISMATCH", label, str(frames_file))
        raw_steps = raw.get("steps") or (raw.get("canonical") or {}).get("steps", [])
        self.check(attempt.get("steps", []) == raw_steps, "STEP_METADATA_MISMATCH", label, str(frames_file))
        raw_frames = raw.get("frames", [])
        self.check(len(raw_frames) == len(attempt["frames"]), "FRAME_COUNT_MISMATCH", label, str(frames_file))
        earlier_frames = []
        for frame, original in zip(attempt["frames"], raw_frames):
            image = self.file_reference(frame, label)
            png = image.read_bytes() if image.is_file() else b""
            dimensions = struct.unpack(">II", png[16:24]) if len(png) >= 24 and png[:8] == b"\x89PNG\r\n\x1a\n" else (0, 0)
            self.check(dimensions == (frame.get("width"), frame.get("height")) and min(dimensions) > 0,
                       "EMPTY_OR_INVALID_SCREENSHOT", label, frame["path"])
            for key in ("sequence", "canonicalStep", "capturedAt", "sha256", "claim", "step"):
                self.check(frame.get(key) == original.get(key), "FRAME_METADATA_MISMATCH", label, key)
            self.check(audit.resolve(frame["path"], self.workspace) == audit.resolve(original["path"], self.workspace),
                       "FRAME_PATH_MISMATCH", label, frame["path"])
            self.frame_observations(frame, original, label)
            if "sameImageAsSequence" in original:
                self.check(frame.get("sameImageAsSequence") == original["sameImageAsSequence"],
                           "IDENTICAL_IMAGE_METADATA_MISMATCH", label, "Preserve the capture's retained image identity reference.")
            elif "sameImageAsSequence" in frame:
                prior = [earlier for earlier in earlier_frames if earlier.get("sha256") == frame.get("sha256")
                         and earlier.get("targetPageLabel") == frame.get("targetPageLabel")]
                self.check(frame["sameImageAsSequence"] == (prior[-1]["sequence"] if prior else None),
                           "IDENTICAL_IMAGE_DERIVATION", label, "Derive the latest matching earlier image when capture metadata is absent.")
            for value, source in ((frame, "report"), (original, "capture")):
                if value.get("sameImageAsSequence") is not None:
                    matches = [earlier for earlier in earlier_frames
                               if earlier["sequence"] == value["sameImageAsSequence"]
                               and earlier.get("sha256") == value.get("sha256")
                               and earlier.get("targetPageLabel") == value.get("targetPageLabel")]
                    self.check(len(matches) == 1, "IDENTICAL_IMAGE_BINDING", label, source)
            earlier_frames.append(original)
            self.counts["screenshotFrames"] += 1
        for key, value in audit.screenshot_content_evidence(attempt).items():
            if key in attempt:
                self.check(attempt[key] == value, "SCREENSHOT_CONTENT_RECONCILIATION", label, key)
        recomputed = audit.step_evidence(attempt, definition, row)
        for key, value in recomputed.items():
            self.check(attempt.get(key) == value, "STEP_EVIDENCE_RECONCILIATION", label, key)
        for step in attempt.get("stepTimeline", []):
            if step["status"] in ("NOT_EXECUTED", "PENDING", "RUNNING", "NOT_RECORDED"):
                self.check(not step["frameSequences"], "UNEXECUTED_SCREENSHOT_CLAIM", label, f"Step {step['number']}")
                contradictory = [frame for frame in attempt["frames"] if frame.get("canonicalStep") == step["number"]]
                if contradictory and historical:
                    self.findings.append({"code": "UNEXECUTED_FRAME_BINDING", "severity": "HISTORICAL_INVALID_STEP_BINDING",
                        "attemptId": label, "caseId": row["caseId"], "stepNumber": step["number"], "stepStatus": step["status"],
                        "result": attempt["result"], "framesMetadata": audit.reference(frames_file, self.workspace),
                        "screenshots": [{key: frame[key] for key in ("path", "sha256", "sequence", "canonicalStep")}
                                        for frame in contradictory],
                        "consequence": "The historical raw frame binding conflicts with its unexecuted step. It contributes no valid step screenshot.",
                        "owner": "Codex harness maintainer",
                        "nextAction": "Retain this contradiction and use the later attempt for current evidence."})
                    self.counts["historicalInvalidStepBindings"] += 1
                else:
                    self.check(not contradictory, "UNEXECUTED_FRAME_BINDING", label, f"Step {step['number']}")
            self.counts["stepRecords"] += 1
        self.counts["applicationAttempts"] += 1


def validate(report: Path, workspace: Path, expected_cases: int = 521, expected_steps: int = 4873) -> dict:
    review = Validation(workspace)
    payload_file = report / "case-results.json"
    payload = audit.read(payload_file)
    review.check(payload.get("schemaVersion") == 2, "SCHEMA_VERSION", str(payload_file), "This validator requires schema version 2.")
    manifest = report / "report-manifest.json"
    review.manifest(manifest)
    manifest_rows = audit.read(manifest)["artifacts"]
    expected_artifacts = {file.resolve() for file in report.rglob("*") if file.is_file() and file != manifest}
    listed_artifacts = [audit.resolve(item["path"], workspace).resolve() for item in manifest_rows]
    review.check(len(listed_artifacts) == len(set(listed_artifacts)) and set(listed_artifacts) == expected_artifacts,
                 "REPORT_MANIFEST_COMPLETENESS", str(manifest), "The manifest must list each report artifact exactly once.")
    inventory_file = review.file_reference(payload["frozenInventory"], "frozenInventory")
    inventory = audit.read(inventory_file)
    preflight_file = review.file_reference(payload["frozenCaseRecords"], "frozenCaseRecords")
    review.file_reference(inventory["caseRecords"], "inventory.caseRecords")
    rows = [json.loads(line) for line in preflight_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    definitions = audit.case_definitions(inventory, rows, workspace)
    exclusions = {}
    if payload.get("scopeExclusions"):
        decision_file = review.file_reference(payload["scopeExclusions"], "scopeExclusions")
        decision = audit.read(decision_file)
        review.check(decision.get("status") == "SKIPPED_BY_USER", "SCOPE_DECISION_STATUS", str(decision_file),
                     "The retained decision must identify the user scope exclusion.")
        review.check(decision.get("catalogSha256") == next(iter(definitions.values()))["catalogSha256"],
                     "SCOPE_DECISION_CATALOG", str(decision_file), "The decision must bind the frozen catalog.")
        exclusions = {item["caseId"]: item for item in decision["cases"]}
        review.check(len(exclusions) == len(decision["cases"]) and set(exclusions) <= set(definitions),
                     "SCOPE_DECISION_IDS", str(decision_file), "Every scope exclusion must identify one distinct canonical case.")
    cases = payload["cases"]
    ids = [case["caseId"] for case in cases]
    expected_ids = {row["caseId"] for row in rows}
    review.check(len(ids) == len(set(ids)) == expected_cases and set(ids) == expected_ids == set(definitions),
                 "CANONICAL_CASE_COMPLETENESS", str(payload_file), f"The report must contain exactly {expected_cases} unique frozen cases.")
    review.check(sum(len(item["steps"]) for item in definitions.values()) == expected_steps,
                 "CANONICAL_STEP_COUNT", str(inventory_file), f"The frozen catalog must contain {expected_steps} steps.")
    row_by_id = {row["caseId"]: row for row in rows}
    html_ids = {file.stem for file in (report / "cases").glob("*.html")}
    review.check(html_ids == expected_ids, "HTML_CASE_COMPLETENESS", str(report / "cases"), "Each canonical case requires one HTML page.")
    for case in cases:
        case_id = case["caseId"]
        if case_id not in row_by_id:
            continue
        row = row_by_id[case_id]
        attempts = case["actualApplicationAttempts"]
        review.check(newest_first(attempts), "ATTEMPT_ORDER", case_id, "Attempts must use descending endedAt and attemptId order.")
        latest = attempts[0] if attempts else None
        review.check(case["latestAttempt"] == (latest["attemptId"] if latest else None), "LATEST_ATTEMPT_POINTER", case_id,
                     "The latest pointer must identify the first retained attempt.")
        excluded = exclusions.get(case_id)
        expected_status = "SKIPPED_BY_USER" if excluded else latest["observedStatus"] if latest else "BLOCKED_NOT_EXECUTED"
        review.check(case["localPredicateStatus"] == expected_status, "CASE_STATUS_MISMATCH", case_id,
                     "Only an explicit user scope exclusion can replace the actual local execution status.")
        review.check(case.get("scopeStatus") == ("EXCLUDED_BY_USER" if excluded else "IN_SCOPE") and case.get("scopeExclusion") == excluded,
                     "SCOPE_DECISION_BINDING", case_id, "The displayed scope must follow the retained user decision.")
        review.check(case["latestObservedStatus"] == (latest["observedStatus"] if latest else "NOT_RUN"),
                     "LATEST_STATUS_MISMATCH", case_id, "The latest observed status must match the latest attempt.")
        review.check(case["canonicalAcceptanceStatus"] == "NOT_ESTABLISHED" and case["canonicalFullScenarioStatus"] == "NOT_VERIFIED",
                     "ACCEPTANCE_SCOPE", case_id, "Local browser outcomes do not establish deployed or full canonical acceptance.")
        review.check(case["canonicalQualityStatus"] == row["canonicalQualityStatus"], "QUALITY_SCOPE", case_id,
                     "Retain the frozen quality result independently of execution.")
        for key in ("definition", "definitionLine", "definitionVersion", "definitionSha256"):
            review.check(case[key] == row[key], "DEFINITION_BINDING", case_id, key)
        for index, attempt in enumerate(attempts):
            review.classification(attempt, "ACTUAL_APPLICATION")
            review.attempt(attempt, definitions[case_id], row, historical=index > 0)
        coverage = audit.step_evidence(latest, definitions[case_id], row)
        for key in ("stepEvidenceStatus", "completeStepEvidence", "canonicalStepCount", "stepsWithScreenshots", "stepEvidenceGaps"):
            review.check(case.get(key) == coverage[key], "LATEST_STEP_EVIDENCE", case_id, key)
        for key, value in audit.screenshot_content_evidence(latest).items():
            if key in case:
                review.check(case[key] == value, "LATEST_SCREENSHOT_CONTENT", case_id, key)
        document_file = report / "cases" / f"{case_id}.html"
        if not document_file.is_file():
            continue
        document = document_file.read_text(encoding="utf-8")
        parsed = DetailsParser()
        parsed.feed(document)
        review.check("Latest local result:" in document, "LATEST_RESULT_LABEL", case_id, "The current result requires a clear label.")
        if "screenshotContentReviewDefinitions" in payload:
            review.check("step screenshot bindings" in document.casefold() and "structural coverage only" in document,
                         "BINDING_SCOPE_LABEL", case_id, "Structural screenshot bindings must not imply content review.")
            review.check("Screenshot content review:" in document and "does not establish human visual review" in document,
                         "CONTENT_REVIEW_SCOPE_LABEL", case_id, "Machine context must remain distinct from human visual review.")
        if latest:
            review.check('<section class="latest-attempt">' in document, "LATEST_ATTEMPT_VISIBLE", case_id, "Expand the latest attempt.")
        if len(attempts) > 1:
            review.check(document.find('<section class="latest-attempt">') < document.find('<details class="attempt-history">'),
                         "LATEST_HTML_ORDER", case_id, "The latest attempt must precede earlier history.")
            review.check(len(parsed.history_details) == len(attempts), "HISTORY_SECTION_COUNT", case_id, "Retain a history group and each earlier attempt.")
            review.check(all("open" not in attrs for attrs in parsed.history_details), "HISTORY_COLLAPSED", case_id,
                         "Earlier attempts must start collapsed.")
        review.counts["canonicalCases"] += 1
    flat = [attempt for case in cases for attempt in case["actualApplicationAttempts"]]
    harness = payload["harnessAttempts"]
    historical_synthetic = payload.get("historicalDeclaredSyntheticAttempts", [])
    for attempt in harness:
        review.non_application_attempt(attempt, "SYNTHETIC_HARNESS")
    for attempt in historical_synthetic:
        review.non_application_attempt(attempt, "HISTORICAL_DECLARED_SYNTHETIC")
    expected_summary = {
        "canonicalCases": len(cases), "localPredicateStatus": dict(Counter(case["localPredicateStatus"] for case in cases)),
        "latestStepEvidenceStatus": dict(Counter(case["stepEvidenceStatus"] for case in cases)),
        "canonicalSteps": sum(case["canonicalStepCount"] for case in cases),
        "latestStepsWithScreenshots": sum(case["stepsWithScreenshots"] for case in cases),
        "casesWithCompleteStepEvidence": sum(case["completeStepEvidence"] for case in cases),
        "applicationAttemptsWithCompleteStepEvidence": sum(attempt["completeStepEvidence"] for attempt in flat),
        "canonicalAcceptanceEstablished": 0, "qualityBlockedCases": sum(row["canonicalQualityStatus"] == "FAIL" for row in rows),
        "userExcludedCases": len(exclusions), "inScopeCases": len(cases) - len(exclusions),
        "actualApplicationCasesObserved": sum(bool(case["actualApplicationAttempts"]) for case in cases),
        "applicationAttempts": len(flat), "applicationAttemptStatus": dict(Counter(attempt["observedStatus"] for attempt in flat)),
        "applicationScreenshotFrames": sum(len(attempt["frames"]) for attempt in flat),
        "harnessAttempts": len(harness), "harnessAttemptStatus": dict(Counter(attempt["observedStatus"] for attempt in harness)),
        "harnessScreenshotFrames": sum(len(attempt["frames"]) for attempt in harness),
        "historicalDeclaredSyntheticAttempts": len(historical_synthetic),
        "historicalDeclaredSyntheticAttemptStatus": dict(Counter(attempt["observedStatus"] for attempt in historical_synthetic)),
        "historicalDeclaredSyntheticScreenshotFrames": sum(len(attempt["frames"]) for attempt in historical_synthetic),
        "integrityCheck": "PASSED", "canonicalCaseUniquenessCheck": "PASSED"}
    if "latestScreenshotContentReviewStatus" in payload["summary"]:
        expected_summary["latestScreenshotContentReviewStatus"] = dict(Counter(case["screenshotContentReviewStatus"] for case in cases))
    if "latestDuplicateFrames" in payload["summary"]:
        expected_summary["latestDuplicateFrames"] = sum(case["duplicateFrames"] for case in cases)
    if "latestFramesWithRecordedContext" in payload["summary"]:
        expected_summary["latestFramesWithRecordedContext"] = sum(case["framesWithRecordedContext"] for case in cases)
    review.check(payload["summary"] == expected_summary, "SUMMARY_RECONCILIATION", str(payload_file), "The summary must reconcile with the case ledger.")
    summary = audit.read(report / "audit-summary.json")
    review.check(summary == {key: value for key, value in payload.items()
                 if key not in ("cases", "harnessAttempts", "historicalDeclaredSyntheticAttempts")},
                 "SUMMARY_FILE_RECONCILIATION", str(report / "audit-summary.json"), "The summary file must match the ledger metadata.")
    with (report / "case-results.csv").open(encoding="utf-8", newline="") as stream:
        csv_rows = list(csv.DictReader(stream))
    review.check([row["caseId"] for row in csv_rows] == ids, "CSV_CASE_COMPLETENESS", str(report / "case-results.csv"),
                 "CSV case order and uniqueness must match JSON.")
    for csv_row, case in zip(csv_rows, cases):
        for key, value in csv_row.items():
            if key in case and key != "reasonCodes":
                review.check(value == (str(case[key]) if case[key] is not None else ""), "CSV_VALUE_MISMATCH", case["caseId"], key)
        review.check(csv_row["reasonCodes"] == ";".join(case["reasonCodes"]), "CSV_REASON_MISMATCH", case["caseId"], "reasonCodes")
        review.check(int(csv_row["applicationAttempts"]) == len(case["actualApplicationAttempts"]), "CSV_ATTEMPT_COUNT", case["caseId"], "applicationAttempts")
        review.check(int(csv_row["screenshotFrames"]) == sum(len(a["frames"]) for a in case["actualApplicationAttempts"]),
                     "CSV_FRAME_COUNT", case["caseId"], "screenshotFrames")
    root = inventory_file.parent.parent
    for run in payload["runs"]:
        review.file_reference(run["inputs"], run["name"])
        result_file = review.file_reference(run["result"], run["name"])
        result = audit.read(result_file)
        for key in ("runnerStatus", "plannedTests", "completedTests", "statuses", "screenshotFrames"):
            review.check(run[key] == result[key], "RUN_METADATA_MISMATCH", run["name"], key)
        attempts = [attempt for attempt in flat + harness + historical_synthetic if attempt["run"] == run["name"]]
        review.check(len(attempts) == result["completedTests"], "RUN_ATTEMPT_COUNT", run["name"], "Each completed result must appear in the report.")
        review.check(sum(len(a["frames"]) for a in attempts) == result["screenshotFrames"], "RUN_FRAME_COUNT", run["name"], "Retained frame totals must match.")
        raw_files = list((result_file.parent / "cases").glob("*/result.json"))
        review.check({audit.resolve(attempt["result"]["path"], workspace) for attempt in attempts} == set(raw_files),
                     "RUN_RESULT_COMPLETENESS", run["name"], "Every retained result must appear once in its original run.")
    source_variants = review.source_provenance(root, payload["runs"])
    evidence_gaps = [{"caseId": case["caseId"], "latestAttempt": case["latestAttempt"],
                      "stepEvidenceStatus": case["stepEvidenceStatus"], "stepsWithScreenshots": case["stepsWithScreenshots"],
                      "canonicalStepCount": case["canonicalStepCount"], "gaps": case["stepEvidenceGaps"]}
                     for case in cases if not case["completeStepEvidence"]]
    return {"schemaVersion": 1, "validatedAt": datetime.now(timezone.utc).isoformat(),
            "status": "PASSED" if not review.errors else "FAILED", "report": str(report),
            "reportManifestSha256": review.digest(manifest), "catalogSha256": next(iter(definitions.values()))["catalogSha256"],
            "checks": dict(review.counts), "summary": payload["summary"], "errors": review.errors,
            "historicalEvidenceFindings": review.findings,
            "sourceVariants": source_variants, "stepEvidenceFindings": evidence_gaps,
            "limits": ["This read-only check validates retained bindings and bytes. It does not review every assertion or screenshot visually.",
                       "Source differences limit reuse for current source. Historical attempts and source variants remain available.",
                       "A passing validation result does not turn failed, blocked, or partial executions into passing business acceptance."]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, default=audit.WORKSPACE)
    parser.add_argument("--expected-cases", type=int, default=521)
    parser.add_argument("--expected-steps", type=int, default=4873)
    args = parser.parse_args()
    try:
        result = validate(args.report.resolve(), args.workspace.resolve(), args.expected_cases, args.expected_steps)
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {"status": "FAILED", "errors": [{"code": "UNREADABLE_OR_INVALID_REPORT", "detail": str(error)}]}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["status"] == "PASSED" else 1)


if __name__ == "__main__":
    main()
