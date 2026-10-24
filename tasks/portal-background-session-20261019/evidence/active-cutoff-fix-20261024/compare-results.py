#!/usr/bin/env python3
"""Retain one completed native run and compare unchanged original assertions.

This helper never launches browsers, changes tests, or changes historical results.
Only result JSON and named PNG captures are copied. Browser profiles are excluded.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(temporary, path)


def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def classification(case, result):
    """Keep diagnostic and observation outcomes outside business pass counts."""
    if result is None:
        return "EXECUTION_ERROR"
    raw = result["status"]
    if (case["id"] == "E2E-07"
            and any(event.get("event") == "visibilitychange" and event.get("visibility") == "hidden"
                    for event in (result.get("controlLifecycle") or {}).get("events", []))):
        return "EXECUTION_ERROR"
    if raw == "FAILED" and str(result.get("error", "")).startswith("ENOTEMPTY:"):
        return "EXECUTION_ERROR"
    if (raw == "FAILED" and case["id"] == "E2E-06"
            and str(result.get("error", "")).startswith("page.waitForFunction: Timeout")
            and result.get("refresh") is None
            and not any(event.get("event") == "visibilitychange" and event.get("visibility") == "hidden"
                        for event in (result.get("lifecycle") or {}).get("events", []))):
        return "EXECUTION_ERROR"
    if case["id"] in {"E2E-21", "E2E-22"}:
        return "OBSERVATION_ONLY" if raw == "PASSED" else "OBSERVATION_FAILED"
    if case["id"] == "E2E-12":
        return "DIAGNOSTIC_PASSED" if raw == "PASSED" else "DIAGNOSTIC_FAILED"
    return raw


def validity(case, result, outcome):
    if outcome != "EXECUTION_ERROR":
        return {"comparison_valid": True, "evidence_validity": "VALID",
                "reason_code": "ORIGINAL_PREDICATES_REACHED",
                "validity_basis": "The retained original assertion result supplies the stated local outcome."}
    reason = "ASSERTION_RESULT_MISSING"
    basis = "No completed original assertion result is available."
    if result is not None and case["id"] == "E2E-06":
        reason = "SETUP_FAILED"
        basis = ("Original cross setup requires hidden visibility before refresh acquisition. "
                 "The retained lifecycle has no hidden transition and no refresh credential.")
    elif result is not None and case["id"] == "E2E-07":
        hidden = any(event.get("event") == "visibilitychange" and event.get("visibility") == "hidden"
                     for event in (result.get("controlLifecycle") or {}).get("events", []))
        reason = "INVALID_VISIBLE_CONTROL" if hidden else "NATIVE_CLEANUP_ERROR"
        basis = ("The paired control became hidden. The original comparison requires a visible control."
                 if hidden else "Native profile cleanup masked the original assertion result.")
    return {"comparison_valid": False, "evidence_validity": "INVALID_COMPARISON",
            "reason_code": reason, "validity_basis": basis,
            "validity_source": case.get("assertion_binding")}


def artifact(path, evidence_root):
    return {"path": os.path.relpath(path, evidence_root), "sha256": sha(path)}


def retain_file(source, destination):
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"Expected an ordinary artifact file: {source}")
    if destination.exists():
        if sha(source) != sha(destination):
            raise ValueError(f"Retained artifact changed: {destination}")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def locate_result(case, run, run_path):
    retained_result = run_path.parent / "artifacts" / "result.json"
    if retained_result.exists():
        return retained_result
    runtime = run_path.parent.parent.parent
    directory = runtime / "browser-results" / run["profile"]
    candidates = []
    for candidate in directory.glob(case["case_id"] + "-*/result.json"):
        result = read(candidate)
        if (result.get("caseId") == case["case_id"]
                and result.get("completedAt")
                and stamp(run["startedAt"]) <= stamp(result["startedAt"])
                <= stamp(result["completedAt"]) <= stamp(run["completedAt"])):
            candidates.append(candidate)
    if len(candidates) > 1:
        raise ValueError("Several assertion results match this run; supply --result.")
    return candidates[0] if candidates else None


def summarize(inventory):
    rows = []
    for case in inventory["cases"]:
        outcome = case.get("candidate_business_outcome", "NOT_RUN")
        rows.append({
            "id": case["id"], "mode": case["mode"],
            "prior": case["prior_business_outcome"], "candidate": outcome,
            "transition": case.get("transition", "PENDING"),
            "result": case.get("candidate_result"),
            "attempts": len(case.get("candidate_attempts", [])),
            "comparison_valid": case.get("comparison_valid"),
            "evidence_validity": case.get("evidence_validity", "NOT_RUN"),
            "reason_code": case.get("reason_code"),
        })
    counts = dict(sorted(Counter(row["candidate"] for row in rows).items()))
    return {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "expected_cases": inventory["total_cases"],
        "baseline_counts": inventory["baseline_counts"],
        "candidate_counts": counts,
        "failed_to_passed": [row["id"] for row in rows
                             if row["prior"] == "FAILED" and row["candidate"] == "PASSED"],
        "passed_to_failed": [row["id"] for row in rows
                             if row["prior"] == "PASSED" and row["candidate"] == "FAILED"],
        "remaining_business_failures": [row["id"] for row in rows if row["candidate"] == "FAILED"],
        "pending_cases": [row["id"] for row in rows if row["candidate"] == "NOT_RUN"],
        "execution_errors": [row["id"] for row in rows if row["candidate"] == "EXECUTION_ERROR"],
        "business_passes": counts.get("PASSED", 0),
        "cases": rows,
        "limits": [
            "Business pass totals exclude diagnostic and observation cases.",
            "Execution errors do not establish a business pass or business failure.",
            "Historical baseline bytes and original assertions remain unchanged.",
        ],
    }


def record(args, evidence_root, inventory):
    matches = [case for case in inventory["cases"]
               if case["id"] == args.record or case["mode"] == args.record_mode]
    if len(matches) != 1:
        raise ValueError("Select exactly one known case with --record or --record-mode.")
    case = matches[0]
    run_path = Path(args.run).resolve()
    run = read(run_path)
    if run.get("mode") != case["mode"] or not run.get("completedAt"):
        raise ValueError("The run has another mode or has not completed.")
    if run.get("status") not in {"PASSED", "FAILED"}:
        raise ValueError("The native run has no final status.")
    if run.get("extensionSha256") != case["assertion_module_sha256"]:
        raise ValueError("The native run did not use the original assertion module.")
    for key in ("prior_run", "prior_result"):
        prior = evidence_root / case[key]["path"]
        if sha(prior) != case[key]["sha256"]:
            raise ValueError(f"Historical evidence changed: {prior}")
    result_path = Path(args.result).resolve() if args.result else locate_result(case, run, run_path)
    result = read(result_path) if result_path else None
    if result is not None:
        if result.get("caseId") != case["case_id"]:
            raise ValueError("The assertion result has another case identity.")
        if result.get("testSourceSha256") != case["assertion_module_sha256"]:
            raise ValueError("The assertion result used another assertion module.")
        if result.get("status") not in {"PASSED", "FAILED"} or not result.get("completedAt"):
            raise ValueError("The assertion result has no final status.")
        if result.get("clock") != "REAL_WALL_CLOCK" or run.get("clock") != "REAL_WALL_CLOCK":
            raise ValueError("The original real wall clock condition changed.")
        if not (stamp(run["startedAt"]) <= stamp(result["startedAt"])
                <= stamp(result["completedAt"]) <= stamp(run["completedAt"])):
            raise ValueError("The assertion result falls outside this run.")
        if run["status"] != result["status"]:
            raise ValueError("Native and assertion statuses disagree.")
    destination = evidence_root / "browser" / run_path.parent.name
    retain_file(run_path, destination / "run.json")
    copied = [destination / "run.json"]
    for name in ("opened.png", "failed.png"):
        native_capture = run_path.parent / name
        if native_capture.exists():
            retain_file(native_capture, destination / name)
            copied.append(destination / name)
    if result is not None:
        retained_result = destination / "artifacts" / "result.json"
        retain_file(result_path, retained_result)
        copied.append(retained_result)
        for capture in result.get("screenshots", []):
            name = capture["file"]
            if Path(name).name != name or Path(name).suffix.lower() != ".png":
                raise ValueError("A screenshot path is outside the allowed PNG artifacts.")
            retain_file(result_path.parent / name, destination / "artifacts" / name)
            copied.append(destination / "artifacts" / name)
    retained = {
        "id": case["id"], "mode": case["mode"], "retained_at": datetime.now(timezone.utc).isoformat(),
        "source_run": {"path": str(run_path), "sha256": sha(run_path)},
        "source_result": {"path": str(result_path), "sha256": sha(result_path)} if result else None,
        "files": [artifact(path, evidence_root) for path in copied],
        "original_assertion_sha256": case["assertion_module_sha256"],
        "profile_directories_copied": False,
    }
    retention_path = destination / "retention.json"
    if not retention_path.exists():
        write(retention_path, retained)
    outcome = classification(case, result)
    evidence_validity = validity(case, result, outcome)
    attempt = {
        "run": artifact(destination / "run.json", evidence_root),
        "result": artifact(destination / "artifacts" / "result.json", evidence_root) if result else None,
        "retention": artifact(retention_path, evidence_root),
        "runner_status": run["status"], "business_outcome": outcome,
        "started_at": run["startedAt"], "completed_at": run["completedAt"],
        "error": (result or run).get("error"),
        "declared_source_revisions": result.get("sourceRevisions") if result else None,
        **evidence_validity,
    }
    attempts = case.setdefault("candidate_attempts", [])
    previous = next((old for old in attempts if old["run"]["sha256"] == attempt["run"]["sha256"]), None)
    if previous is None:
        attempts.append(attempt)
    else:
        previous.update(attempt)
    case.update({
        "candidate_execution_status": result["status"] if result else "EXECUTION_ERROR",
        "candidate_business_outcome": outcome, "candidate_result": attempt["result"],
        "candidate_run": attempt["run"], "candidate_error": attempt["error"],
        "transition": case["prior_business_outcome"] + " → " + outcome,
        **evidence_validity,
    })
    return case["id"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--record", metavar="E2E-ID")
    group.add_argument("--record-mode", metavar="MODE")
    parser.add_argument("--run", help="Completed native run.json path")
    parser.add_argument("--result", help="Exact assertion result.json; optional when unambiguous")
    parser.add_argument("--evidence-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    evidence_root = args.evidence_root.resolve()
    if bool(args.record or args.record_mode) != bool(args.run):
        parser.error("Recording needs a case selector and --run.")
    lock_name = hashlib.sha256(str(evidence_root).encode()).hexdigest()[:20]
    with open(Path(tempfile.gettempdir()) / ("cutoff-compare-" + lock_name + ".lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        inventory_path = evidence_root / "case-inventory.json"
        inventory = read(inventory_path)
        if args.run:
            recorded_id = record(args, evidence_root, inventory)
            write(inventory_path, inventory)
        summary = summarize(inventory)
        if args.run:
            progress_path = evidence_root / "progress.json"
            progress = read(progress_path)
            attempts = [case for case in inventory["cases"] if case.get("candidate_attempts")]
            complete = [case for case in attempts if case.get("candidate_result")
                        and case.get("candidate_business_outcome") != "EXECUTION_ERROR"
                        and case.get("comparison_valid") is not False]
            progress.update({
                "recorded_at": summary["recorded_at"],
                "status": "COMPLETED" if len(complete) == inventory["total_cases"] else "IN_PROGRESS",
                "completed_cases": len(complete), "attempted_cases": len(attempts),
                "eligible_completed_cases": len(complete),
                "eligible_pending_cases": inventory["total_cases"] - len(complete),
                "pending_cases": [case["id"] for case in inventory["cases"] if case not in complete],
                "completed_results": [{"id": case["id"], "result": case["candidate_result"],
                                       "outcome": case["candidate_business_outcome"]} for case in complete],
                "inventory_sha256": sha(inventory_path), "candidate_counts": summary["candidate_counts"],
                "next_action": "Finish pending original cases, then compare retained outcomes."
                               if len(complete) < inventory["total_cases"] else "Review all retained case transitions.",
            })
            progress["running_cases"] = [case for case in progress.get("running_cases", [])
                                         if case != recorded_id]
            if not progress["running_cases"]:
                progress.pop("volatile_state", None)
            write(progress_path, progress)
            write(evidence_root / "transitions.json", summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
