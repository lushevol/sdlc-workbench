#!/usr/bin/env python3
"""Run the authorized native comparison queue and retain every completed case."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path.cwd()
STAGE = ROOT / "tasks/portal-background-session-20261019/evidence/active-cutoff-fix-20261024"
RUNTIME = ROOT / ".workbench/session-active-cutoff-fix-20261024"
HELPER = STAGE / "compare-results.py"
EVENTS = STAGE / "queue-events.jsonl"


def read(path):
    return json.loads(path.read_text())


def emit(kind, **fields):
    event = {"at": datetime.now(timezone.utc).isoformat(), "event": kind, **fields}
    with EVENTS.open("a") as stream:
        stream.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def mark_running(mode, counterfactual=False, identity=None):
    directory = STAGE / "counterfactual" if counterfactual else STAGE
    inventory = read(directory / "case-inventory.json")
    case = next(case for case in inventory["cases"] if case["mode"] == mode)
    path = directory / "progress.json"
    progress = read(path)
    progress.update({"status": "RUNNING", "recorded_at": datetime.now(timezone.utc).isoformat(),
                     "running_cases": [case["id"]], "volatile_state": {
                         "mode": mode, "native_identity": identity,
                         "run_path": str(RUNTIME / "native" / identity / "run.json") if identity else None,
                         "restart": "Keep interrupted runs separate. Restart with a fresh isolated native process.",
                     }})
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(progress, indent=2) + "\n")
    os.replace(temporary, path)
    return case


def completed(mode, counterfactual=False):
    directory = STAGE / "counterfactual" if counterfactual else STAGE
    inventory = read(directory / "case-inventory.json")
    case = next(case for case in inventory["cases"] if case["mode"] == mode)
    if not case.get("candidate_run"):
        raise RuntimeError("The completed native case was not retained.")
    emit("CASE_RETAINED", scope="counterfactual" if counterfactual else "candidate",
         id=case["id"], mode=mode, outcome=case["candidate_business_outcome"],
         transition=case["transition"], run=case["candidate_run"],
         result=case["candidate_result"], error=case.get("candidate_error"))


def run(mode, counterfactual=False):
    for path in (RUNTIME / "native").glob("*/run.json"):
        if read(path).get("status") in {"STARTING", "RUNNING"}:
            raise RuntimeError(f"Another native run remains active: {path}")
    case = mark_running(mode, counterfactual)
    launcher = RUNTIME / ("run-baseline.py" if counterfactual else "run-expanded.py")
    emit("CASE_STARTING", scope="counterfactual" if counterfactual else "candidate",
         id=case["id"], mode=mode)
    process = subprocess.Popen([sys.executable, str(launcher), mode], cwd=ROOT,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, bufsize=1)
    lines = []
    with (RUNTIME / "queue-launcher-output.log").open("a") as output:
        for line in process.stdout:
            output.write(line)
            output.flush()
            lines.append(line)
            if line.startswith('{"starting":'):
                started = json.loads(line)
                mark_running(mode, counterfactual, started["id"])
                emit("NATIVE_STARTED", scope="counterfactual" if counterfactual else "candidate", **started)
    if process.wait() != 0:
        print("".join(lines[-40:]), flush=True)
        raise RuntimeError("The launcher or durable retention failed. Resume only after repair.")
    completed(mode, counterfactual)


def main():
    natural = RUNTIME / "native/cutoff-natural-20261024T152518/run.json"
    emit("QUEUE_STARTED", natural_run=str(natural),
         order="natural; candidate cross; baseline cross; nineteen fast cases; missing")
    while True:
        state = read(natural)
        if state.get("completedAt") and state.get("status") in {"PASSED", "FAILED"}:
            break
        start = datetime.fromisoformat(state["startedAt"].replace("Z", "+00:00"))
        if (datetime.now(timezone.utc) - start).total_seconds() > 2400:
            raise RuntimeError("The natural case exceeded forty real minutes without a final record.")
        time.sleep(5)
    subprocess.run([sys.executable, str(HELPER), "--record-mode", "natural", "--run", str(natural)],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    completed("natural")
    run("cross")
    run("cross", counterfactual=True)
    for mode in ["mouse", "keyboard", "scroll", "pending", "retry", "single", "manualLogout",
                 "activityLogout", "late", "expired", "workspace", "rapid", "keyboardExtend",
                 "activityRetry", "inconsistent", "promptActivity", "idleLogout", "visibility", "reload"]:
        run(mode)
    run("missing")
    emit("QUEUE_COMPLETED", candidate_progress=read(STAGE / "progress.json"),
         counterfactual_progress=read(STAGE / "counterfactual/progress.json"))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        emit("QUEUE_STOPPED", error=str(error))
        raise
