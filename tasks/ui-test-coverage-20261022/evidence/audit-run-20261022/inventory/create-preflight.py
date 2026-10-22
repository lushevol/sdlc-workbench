"""Freeze audit preflight references without changing canonical case outcomes."""
from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
CATALOG = ROOT / "tasks/ui-test-coverage-20261022/test-cases.md"
TRACEABILITY = ROOT / "e2e/traceability/cases.json"
GHERKIN = ROOT / "tasks/ui-test-coverage-20261022/evidence/refinement/gherkin-manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    target = OUT / "case-preflight.jsonl"
    if target.exists():
        raise SystemExit("The preflight is frozen. Use a new run directory for another snapshot.")
    traceability = json.loads(TRACEABILITY.read_text())
    scenarios = json.loads(GHERKIN.read_text())["scenarios"]
    lines = CATALOG.read_text().splitlines()
    recorded_at = datetime.now(timezone.utc).isoformat()
    counts: Counter[str] = Counter()
    frames = 0
    with target.open("x") as stream:
        for case_index, case in enumerate(traceability["cases"]):
            case_id = case["caseId"]
            scenario = scenarios[case_id]
            steps = sorted((int(line), step) for line, step in scenario["steps"].items())
            frame_plan: list[dict] = []
            first_action = next((line for line, step in steps if step["kind"] in {"interaction", "event"}), None)
            if first_action:
                frame_plan.append({
                    "frameId": f"{case_id}-setup",
                    "purpose": "setup-before-first-event",
                    "beforeStepLine": first_action,
                    "required": True,
                    "captureStatus": "NOT_CAPTURED",
                })
            pending_ui: list[int] = []
            for index, (line, step) in enumerate(steps):
                if step["kind"] == "assertion" and step.get("observation") == "ui":
                    pending_ui.append(line)
                next_step = steps[index + 1][1] if index + 1 < len(steps) else None
                if pending_ui and (next_step is None or next_step["kind"] != "assertion"):
                    component_ids = sorted({
                        component_id
                        for assertion_line in pending_ui
                        for component_id in scenario["steps"][str(assertion_line)].get("components", [])
                    })
                    frame_plan.append({
                        "frameId": f"{case_id}-state-{len(frame_plan):02d}",
                        "purpose": "observable-ui-assertion-state",
                        "afterStepLine": line,
                        "assertionLines": pending_ui.copy(),
                        "componentIds": component_ids,
                        "required": True,
                        "captureStatus": "NOT_CAPTURED",
                    })
                    pending_ui.clear()
            lifecycle_lines = [
                line for line, step in steps
                if step["kind"] in {"event", "interaction"}
                and any(word in lines[line - 1].lower() for word in ("reload", "navigat", "closes the", "close the", "closes this", "page from", "browser tab"))
            ]
            reasons = ["NO_COMPLETE_REAL_APPLICATION_BINDING"]
            if case["supportStatus"] == "BLOCKED":
                reasons.append("CANONICAL_UI_QUALITY_GATE_FAILED")
            if case["workflowBindingStatus"] == "PARTIAL":
                reasons.append("WORKFLOW_USES_SYNTHETIC_SUBSTITUTION")
            if case["canonicalQualityStatus"] != "PASS":
                reasons.append("CANONICAL_REVIEW_OR_EVIDENCE_UNRESOLVED")
            result = {
                "caseId": case_id,
                "definition": case["definition"],
                "definitionLine": case["definitionLine"],
                "definitionVersion": case["definitionVersion"],
                "definitionSha256": case["definitionSha256"],
                "preflightRecordedAt": recorded_at,
                "preflightStatus": "BLOCKED_NOT_EXECUTED",
                "executableAtSnapshot": False,
                "businessExecutionStatus": "NOT_RUN",
                "canonicalQualityStatus": case["canonicalQualityStatus"],
                "mappingStatus": case["supportStatus"],
                "workflowBindingStatus": case["workflowBindingStatus"],
                "totalSteps": case["totalSteps"],
                "assertionCount": case["assertionCount"],
                "uiAssertionCount": case["uiAssertionCount"],
                "functionalAssertionCount": case["functionalAssertionCount"],
                "reasonCodes": reasons,
                "gapDefinition": f"e2e/traceability/cases.json#/cases/{case_index}",
                "requiredFrames": frame_plan,
                "beforeLifecycleReplacementLines": lifecycle_lines,
                "machineEvidenceAssertionLines": [
                    line for line, step in steps
                    if step["kind"] == "assertion" and step.get("observation") != "ui"
                ],
                "screenshots": [],
                "actualAssertions": [],
                "limits": ["This record is a preflight snapshot. It is not a browser execution result."]
            }
            stream.write(json.dumps(result, separators=(",", ":")) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
            counts[case["supportStatus"]] += 1
            frames += len(frame_plan)
    inputs = [CATALOG, TRACEABILITY, GHERKIN, ROOT / "e2e/traceability/bindings.json"]
    summary = {
        "schemaVersion": 1,
        "scope": "canonical-business-case-preflight",
        "recordedAt": recorded_at,
        "workbenchRevision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "inputs": [{"path": str(path.relative_to(ROOT)), "sha256": sha(path)} for path in inputs],
        "caseRecords": {"path": str(target.relative_to(ROOT)), "sha256": sha(target)},
        "summary": {
            "cases": sum(counts.values()),
            "assertions": sum(case["assertionCount"] for case in traceability["cases"]),
            "mappingStatus": dict(counts),
            "businessExecutionStatus": {"NOT_RUN": sum(counts.values())},
            "preflightStatus": {"BLOCKED_NOT_EXECUTED": sum(counts.values())},
            "completeRealApplicationBindings": 0,
            "plannedEssentialScreenshotFrames": frames,
            "capturedBusinessScreenshotFrames": 0,
        },
        "framePlanRules": [
            "Capture setup before the first canonical event or interaction.",
            "Capture each UI assertion state before another event can replace it.",
            "Capture volatile state before each listed lifecycle replacement.",
            "Capture the actual failure state when an assertion fails.",
            "Retain non-UI assertion values separately. A screenshot does not prove service, token, timing, or count predicates.",
        ],
        "limits": [
            "The screenshot plan references canonical steps. No screenshot is claimed before actual execution.",
            "A later execution result can supersede this preflight status without changing the snapshot bytes.",
            "Mapping support is not passing execution or accepted business behavior.",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["summary"]))


if __name__ == "__main__":
    main()
