#!/usr/bin/env python3
"""Run an approved original DOM/service case while native lifecycle checks remain blocked."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
STAGE = HERE.parent
ALLOWED = {"single", "rapid", "keyboardExtend", "activityRetry", "inconsistent", "promptActivity",
           "idleLogout", "manualLogout", "activityLogout", "expired", "workspace"}
LIMIT = "macOS locked; no physical user UI or lifecycle verification"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=sorted(ALLOWED))
    args = parser.parse_args()
    scope_path = HERE / "locked-mac-case-scope.json"
    if not scope_path.is_file():
        raise RuntimeError("The inspected independent-case scope record is unavailable.")
    spec = importlib.util.spec_from_file_location("resume_queue", HERE / "execute-resume.py")
    queue = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(queue)
    queue.guard_native_idle()
    execution_error = None
    try:
        queue.run(args.mode)
    except Exception as error:
        execution_error = error
    inventory_path = STAGE / "case-inventory.json"
    inventory = json.loads(inventory_path.read_text())
    case = next(case for case in inventory["cases"] if case["mode"] == args.mode)
    if not case.get("candidate_run"):
        raise execution_error or RuntimeError("No completed native attempt was retained.")
    scope = {"execution_scope": "DOM_SERVICE_ONLY", "environment_limit": LIMIT,
             "scope_evidence": {"path": "setup/locked-mac-case-scope.json",
                                "sha256": hashlib.sha256(scope_path.read_bytes()).hexdigest()}}
    case.update(scope)
    for attempt in case["candidate_attempts"]:
        if attempt["run"]["sha256"] == case["candidate_run"]["sha256"]:
            attempt.update(scope)
    temporary = inventory_path.with_name(inventory_path.name + ".tmp")
    temporary.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
    os.replace(temporary, inventory_path)
    progress_path = STAGE / "progress.json"
    progress = json.loads(progress_path.read_text())
    eligible_cases = [item for item in inventory["cases"] if queue.eligible(item)]
    progress.update({"recorded_at": datetime.now(timezone.utc).isoformat(),
                     "status": "PARTIAL_EXECUTION_WITH_BLOCKED_NATIVE_CASES", "running_cases": [],
                     "completed_cases": len(eligible_cases), "eligible_completed_cases": len(eligible_cases),
                     "eligible_pending_cases": inventory["total_cases"] - len(eligible_cases),
                     "pending_cases": [item["id"] for item in inventory["cases"] if not queue.eligible(item)],
                     "blocked_cases": ["E2E-06", "E2E-07", "E2E-15", "E2E-16", "E2E-19", "E2E-21"],
                     "next_action": "Continue approved DOM/service cases. Native hide/restore cases require unlock and a passing preflight.",
                     "inventory_sha256": hashlib.sha256(inventory_path.read_bytes()).hexdigest()})
    progress_path.write_text(json.dumps(progress, indent=2) + "\n")
    queue.emit("DOM_SERVICE_SCOPE_RECORDED", id=case["id"], mode=args.mode,
               outcome=case["candidate_business_outcome"], transition=case["transition"], **scope)
    if execution_error:
        raise execution_error


if __name__ == "__main__":
    main()
