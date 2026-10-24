#!/usr/bin/env python3
"""Resume original cases only after an unlocked native visibility preflight."""

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path.cwd()
STAGE = ROOT / "tasks/portal-background-session-20261019/evidence/active-cutoff-fix-20261024"
RUNTIME = ROOT / ".workbench/session-active-cutoff-fix-20261024"
EVENTS = STAGE / "queue-events.jsonl"


def read(path):
    return json.loads(path.read_text())


def emit(kind, **values):
    event = {"at": datetime.now(timezone.utc).isoformat(), "event": kind, **values}
    with EVENTS.open("a") as stream:
        stream.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def directory(counterfactual=False):
    return STAGE / "counterfactual" if counterfactual else STAGE


def selected(mode, counterfactual=False):
    inventory = read(directory(counterfactual) / "case-inventory.json")
    return next(case for case in inventory["cases"] if case["mode"] == mode)


def eligible(case):
    return (case.get("candidate_result") is not None
            and case.get("comparison_valid") is True
            and case.get("candidate_business_outcome") not in {None, "NOT_RUN", "EXECUTION_ERROR"})


def guard_native_idle():
    for path in (RUNTIME / "native").glob("*/run.json"):
        if read(path).get("status") in {"STARTING", "RUNNING"}:
            raise RuntimeError(f"A native run remains active or unresolved: {path}")
    for line in subprocess.check_output(["ps", "-axo", "pid,command"], text=True).splitlines():
        if "browser-runner.mjs" in line:
            raise RuntimeError("A native browser runner remains active.")
        if ("Microsoft Edge.app/Contents/MacOS/Microsoft Edge" in line
                and "--remote-debugging-port=" in line and ".workbench/" in line):
            raise RuntimeError("A native automation browser remains active.")


def mark_running(mode, counterfactual, identity=None):
    path = directory(counterfactual) / "progress.json"
    progress = read(path)
    case = selected(mode, counterfactual)
    progress.update({"status": "RUNNING", "recorded_at": datetime.now(timezone.utc).isoformat(),
                     "running_cases": [case["id"]], "volatile_state": {
                         "mode": mode, "native_identity": identity,
                         "run_path": str(RUNTIME / "native" / identity / "run.json") if identity else None,
                         "restart": "Keep this attempt separate. Restart interrupted cases with a fresh native process.",
                     }})
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(progress, indent=2) + "\n")
    os.replace(temporary, path)


def run(mode, counterfactual=False):
    case = selected(mode, counterfactual)
    if eligible(case):
        emit("VALID_SELECTED_CASE_SKIPPED", scope="counterfactual" if counterfactual else "candidate",
             id=case["id"], mode=mode, result=case["candidate_result"])
        return
    guard_native_idle()
    mark_running(mode, counterfactual)
    launcher = RUNTIME / ("run-baseline.py" if counterfactual else "run-expanded.py")
    emit("CASE_STARTING", scope="counterfactual" if counterfactual else "candidate", id=case["id"], mode=mode)
    process = subprocess.Popen([sys.executable, str(launcher), mode], cwd=ROOT,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    lines = []
    with (RUNTIME / "resume-launcher-output.log").open("a") as stream:
        for line in process.stdout:
            stream.write(line)
            stream.flush()
            lines.append(line)
            if line.startswith('{"starting":'):
                started = json.loads(line)
                mark_running(mode, counterfactual, started["id"])
                emit("NATIVE_STARTED", scope="counterfactual" if counterfactual else "candidate", **started)
    if process.wait() != 0:
        print("".join(lines[-40:]), flush=True)
        raise RuntimeError("The launcher or durable retention failed.")
    case = selected(mode, counterfactual)
    if not case.get("candidate_run"):
        raise RuntimeError("The completed native run was not retained.")
    emit("CASE_RETAINED", scope="counterfactual" if counterfactual else "candidate",
         id=case["id"], mode=mode, outcome=case["candidate_business_outcome"],
         transition=case["transition"], comparison_valid=case.get("comparison_valid"),
         result=case["candidate_result"], run=case["candidate_run"], error=case.get("candidate_error"))
    if not eligible(case):
        raise RuntimeError("The retained comparison is invalid. Repair its precondition before continuing.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", type=Path, required=True,
                        help="Saved passing unlock and genuine native visibility preflight")
    args = parser.parse_args()
    receipt_path = args.preflight.resolve()
    receipt = read(receipt_path)
    if not (receipt.get("status") == "PASSED" and receipt.get("mac_unlocked") is True
            and receipt.get("genuine_visibility_verified") is True):
        raise RuntimeError("The saved unlocked native visibility preflight has not passed.")
    if not receipt.get("completed_at") or not receipt.get("evidence"):
        raise RuntimeError("The preflight lacks its completed time or retained evidence.")
    lock_path = Path(tempfile.gettempdir()) / "active-cutoff-native-resume.lock"
    with lock_path.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        guard_native_idle()
        emit("RESUME_QUEUE_STARTED", preflight={"path": str(receipt_path),
             "sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest()},
             order="candidate cross; baseline cross; remaining fast; missing; fresh natural")
        run("cross")
        run("cross", counterfactual=True)
        for mode in ["mouse", "keyboard", "scroll", "pending", "retry", "single", "manualLogout",
                     "activityLogout", "late", "expired", "workspace", "rapid", "keyboardExtend",
                     "activityRetry", "inconsistent", "promptActivity", "idleLogout", "visibility", "reload"]:
            run(mode)
        run("missing")
        run("natural")
        emit("RESUME_QUEUE_COMPLETED", candidate_progress=read(STAGE / "progress.json"),
             counterfactual_progress=read(STAGE / "counterfactual/progress.json"))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        emit("RESUME_QUEUE_STOPPED", error=str(error))
        raise
