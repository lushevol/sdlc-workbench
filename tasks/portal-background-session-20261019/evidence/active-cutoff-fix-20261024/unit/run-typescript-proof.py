"""Compare type diagnostics without emitting files or writing compiler caches."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[5]
EVIDENCE = Path(__file__).resolve().parent
FIXTURES = ROOT / ".workbench/session-active-cutoff-unit-proof-20261024"
CACHE = ROOT / "repos/ui/mfe-base/tsconfig.tsbuildinfo"
cache_before = hashlib.sha256(CACHE.read_bytes()).hexdigest()


def run(label):
    fixture = FIXTURES / label
    command = [str(fixture / "node_modules/.bin/tsc"), "--noEmit", "--incremental", "false",
               "--emitDeclarationOnly", "false", "--pretty", "false"]
    started_at = datetime.now(timezone.utc).isoformat()
    execution = subprocess.run(command, cwd=fixture, env=os.environ.copy(), stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, timeout=120)
    log_name = f"typescript-source-{label}.log"
    (EVIDENCE / log_name).write_text(execution.stdout)
    record = {
        "fixture": label,
        "command": command,
        "cwd": str(fixture),
        "started_at": started_at,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": execution.returncode,
        "log": log_name,
        "log_sha256": hashlib.sha256(execution.stdout.encode()).hexdigest(),
        "diagnostic_count": sum("error TS" in line for line in execution.stdout.splitlines()),
        "home_sha256": hashlib.sha256((fixture / "src/pages/Home/common/useController.ts").read_bytes()).hexdigest(),
    }
    (EVIDENCE / f"typescript-source-{label}-execution.json").write_text(json.dumps(record, indent=2) + "\n")
    return record, execution.stdout


with ThreadPoolExecutor(max_workers=2) as pool:
    baseline, candidate = list(pool.map(run, ["baseline-home", "candidate"]))
cache_after = hashlib.sha256(CACHE.read_bytes()).hexdigest()
same = baseline[1] == candidate[1]
summary = {
    "baseline": baseline[0],
    "candidate": candidate[0],
    "diagnostics_byte_identical": same,
    "introduced_diagnostics": 0 if same else "NOT_ESTABLISHED",
    "cache_before_sha256": cache_before,
    "cache_after_sha256": cache_after,
    "application_cache_preserved": cache_before == cache_after,
    "files_emitted": False,
    "limit": "Both fixtures share candidate tests and all source except Home. Existing diagnostics are not fixed in this scope.",
}
(EVIDENCE / "typescript-source-comparison.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
