#!/usr/bin/env python3
"""Retain the authorized resume command, queue output, and original launcher output."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import threading


ROOT = Path.cwd()
STAGE = ROOT / "tasks/portal-background-session-20261019/evidence/active-cutoff-fix-20261024"
RUNTIME_LOG = ROOT / ".workbench/session-active-cutoff-fix-20261024/resume-launcher-output.log"


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    identity = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    output = STAGE / "native-resume-20261025" / identity
    output.mkdir(parents=True, exist_ok=False)
    command = [sys.executable, str(STAGE / "setup/execute-resume.py"), "--preflight",
               str(STAGE / "setup/visibility-preflight.json")]
    offset = RUNTIME_LOG.stat().st_size if RUNTIME_LOG.exists() else 0
    record = {"started_at": now(), "command": command, "cwd": str(ROOT),
              "status": "RUNNING", "environment_names": ["SESSION_E2E_USERNAME", "SESSION_E2E_PASSWORD"],
              "credential_values_retained": False, "launcher_source_offset": offset,
              "queue_source_sha256": sha(STAGE / "setup/execute-resume.py"),
              "preflight_sha256": sha(STAGE / "setup/visibility-preflight.json")}
    manifest = output / "execution.json"
    manifest.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"capture_started": str(output), "command": command}), flush=True)
    finished = threading.Event()

    def retain_launcher():
        cursor = offset
        with (output / "launcher.stdout.log").open("wb") as retained:
            while True:
                if RUNTIME_LOG.exists():
                    with RUNTIME_LOG.open("rb") as source:
                        source.seek(cursor)
                        chunk = source.read()
                    if chunk:
                        retained.write(chunk)
                        retained.flush()
                        cursor += len(chunk)
                if finished.wait(0.2):
                    with RUNTIME_LOG.open("rb") as source:
                        source.seek(cursor)
                        retained.write(source.read())
                    retained.flush()
                    break

    thread = threading.Thread(target=retain_launcher)
    thread.start()
    try:
        process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, bufsize=1)
        record["queue_pid"] = process.pid
        manifest.write_text(json.dumps(record, indent=2) + "\n")
        with (output / "queue.stdout-stderr.log").open("w") as stream:
            for line in process.stdout:
                stream.write(line)
                stream.flush()
                print(line, end="", flush=True)
        record["wrapper_exit_code"] = process.wait()
        record["status"] = "COMPLETED" if record["wrapper_exit_code"] == 0 else "STOPPED"
    finally:
        finished.set()
        thread.join()
        record["completed_at"] = now()
        record["outputs"] = [{"path": name, "sha256": sha(output / name)}
                             for name in ["launcher.stdout.log", "queue.stdout-stderr.log"]]
        original = (output / "launcher.stdout.log").read_text()
        record["native_completions"] = [json.loads(line) for line in original.splitlines()
                                         if line.startswith('{"finished":')]
        manifest.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"capture_finished": str(output), "wrapper_exit_code": record["wrapper_exit_code"]}), flush=True)
    return record["wrapper_exit_code"]


if __name__ == "__main__":
    sys.exit(main())
