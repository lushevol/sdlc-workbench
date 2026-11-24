"""Expose the retained expected-failure assertion in a separate copied fixture."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[5]
EVIDENCE = Path(__file__).resolve().parent
FIXTURES = ROOT / ".workbench/session-active-cutoff-unit-proof-20261024"
SOURCE = FIXTURES / "candidate"
FIXTURE = FIXTURES / "candidate-known-defect"
TEST = "src/pages/Home/common/sessionLifecycle.test.tsx"
if FIXTURE.exists():
    raise SystemExit(f"Refuse to overwrite existing fixture: {FIXTURE}")
shutil.copytree(SOURCE, FIXTURE, symlinks=True, ignore=shutil.ignore_patterns("coverage"))
test_file = FIXTURE / TEST
original = test_file.read_bytes()
assert original.count(b"it.failing(") == 1
test_file.write_bytes(original.replace(b"it.failing(", b"it(", 1))
result_path = EVIDENCE / "candidate-known-defect-normal-result.json"
command = [
    str(FIXTURE / "node_modules/.bin/jest"),
    "--runInBand", "--coverage=false", "--ci", "--reporters=default", "--json",
    f"--outputFile={result_path}", TEST, "--testNamePattern=\\[KNOWN-DEFECT\\]",
]
started_at = datetime.now(timezone.utc).isoformat()
execution = subprocess.run(command, cwd=FIXTURE, env={**os.environ, "BABEL_ENV": "test"},
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
(EVIDENCE / "candidate-known-defect-normal.log").write_text(execution.stdout)
result = json.loads(result_path.read_text())
record = {
    "started_at": started_at,
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "command": command,
    "cwd": str(FIXTURE),
    "exit_code": execution.returncode,
    "transform": "Replace the sole it.failing wrapper with normal it in this isolated fixture only.",
    "source_test_sha256": hashlib.sha256(original).hexdigest(),
    "diagnostic_test_sha256": hashlib.sha256(test_file.read_bytes()).hexdigest(),
    "home_sha256": hashlib.sha256((FIXTURE / "src/pages/Home/common/useController.ts").read_bytes()).hexdigest(),
    "runner_summary": {key: result[key] for key in ["numPassedTests", "numFailedTests", "numPendingTests", "success"]},
    "active_checkout_mutated": False,
    "limit": "This diagnostic exposes inherited delayed-response recovery failure; it does not change the shipped test.",
}
(EVIDENCE / "candidate-known-defect-normal-execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record))
