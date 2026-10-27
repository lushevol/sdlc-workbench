"""Run complete source-bound Jest discovery with instrumentation."""
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time

WORKSPACE = Path(__file__).resolve().parents[5]
APPLICATION = WORKSPACE / "repos/ui/mfe-base"
OUTPUT = Path(__file__).resolve().parent / "test-only-final-2"
OUTPUT.mkdir(exist_ok=False)
SCRATCH = WORKSPACE / ".workbench/four-checks-coverage-final-2-20261027"
CANDIDATE = "1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303"
BASE = "f025513f696476a9cc8162681410cbd21e029bcb"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, data):
    (OUTPUT / name).write_text(json.dumps(data, indent=2) + "\n")

if SCRATCH.exists():
    raise SystemExit("Refusing to overwrite existing scratch directory")
SCRATCH.mkdir(parents=True)
archive = subprocess.check_output(["git", "-C", str(APPLICATION), "archive", CANDIDATE])
with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
    bundle.extractall(SCRATCH, filter="data")
overlays = ["src/components/Timeout/common/coverageBoundaries.test.tsx", "src/pages/Home/common/sessionRefresh.test.tsx"]
for name in overlays:
    target = SCRATCH / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((APPLICATION / name).read_bytes())
(SCRATCH / "node_modules").symlink_to(APPLICATION / "node_modules", target_is_directory=True)
paths = subprocess.check_output(["git", "-C", str(APPLICATION), "ls-tree", "-r", "--name-only", CANDIDATE], text=True).splitlines()
paths = sorted(set(paths + overlays))
hashes = {name: sha(SCRATCH / name) for name in paths}
save("source-binding.json", {
    "candidate_commit": CANDIDATE, "base_commit": BASE,
    "scope": "Exact runtime snapshot with two explicit test-only worktree overlays; all declared Jest suites; no test filter",
    "test_only_overlays": {name: hashes[name] for name in overlays},
    "source_files": hashes,
    "dependency_source": str(APPLICATION / "node_modules"),
    "dependency_versions": {name: json.loads((SCRATCH / "node_modules" / name / "package.json").read_text())["version"] for name in ["jest", "babel-jest", "axios", "react", "typescript"]},
    "runner_sha256": sha(Path(__file__)),
    "limits": ["Installed dependencies are reused locally.", "No production artifact or environment parity is established."],
})
env = dict(os.environ, BABEL_ENV="test", RUN_EVIDENCE_DIR=str(OUTPUT))
inventory_cmd = ["node", "node_modules/jest/bin/jest.js", "--listTests", "--json", "--runInBand"]
inventory = subprocess.run(inventory_cmd, cwd=SCRATCH, env=env, capture_output=True, text=True)
(OUTPUT / "inventory-stderr.log").write_text(inventory.stderr)
inventory.check_returncode()
suites = json.loads(inventory.stdout)
save("suite-inventory.json", {"command": inventory_cmd, "suite_count": len(suites), "suites": suites, "test_exclusions": []})
command = [
    "node", "node_modules/jest/bin/jest.js", "--runInBand", "--coverage", "--ci", "--detectOpenHandles", "--json",
    f"--outputFile={OUTPUT / 'results.json'}", f"--coverageDirectory={OUTPUT / 'instrumented'}",
    "--coverageReporters=json", "--coverageReporters=json-summary", "--coverageReporters=text", "--coverageReporters=lcovonly",
    "--collectCoverageFrom=src/**/*.{js,ts,tsx}", "--collectCoverageFrom=!src/**/*.test.*",
    "--collectCoverageFrom=!src/**/*.stories.*", "--collectCoverageFrom=!src/**/*.d.ts", "--collectCoverageFrom=!src/fileMock.js",
    "--reporters=default", f"--reporters={OUTPUT.parent / 'case-reporter.cjs'}",
]
started_at = datetime.now(timezone.utc).isoformat()
started = time.monotonic()
save("progress.json", {"status": "RUNNING", "started_at": started_at, "candidate": CANDIDATE, "completed_cases": 0, "suites": len(suites)})
with (OUTPUT / "runner.log").open("w") as log:
    completed = subprocess.run(command, cwd=SCRATCH, env=env, stdout=log, stderr=subprocess.STDOUT)
result = json.loads((OUTPUT / "results.json").read_text())
execution = {
    "started_at": started_at, "ended_at": datetime.now(timezone.utc).isoformat(),
    "elapsed_seconds": time.monotonic() - started, "command": command,
    "cwd": str(SCRATCH), "exit_code": completed.returncode,
    "force_exit": False, "outer_timeout": False, "source_binding": "source-binding.json",
    "source_changed": [name for name in paths if sha(SCRATCH / name) != hashes[name]],
    "suites": result["numTotalTestSuites"], "passed_suites": result["numPassedTestSuites"], "failed_suites": result["numFailedTestSuites"],
    "tests": result["numTotalTests"], "passed_tests": result["numPassedTests"], "failed_tests": result["numFailedTests"],
    "skipped_tests": result["numPendingTests"], "todo_tests": result.get("numTodoTests", 0), "runtime_error_suites": result.get("numRuntimeErrorTestSuites", 0),
    "case_checkpoints": len(list((OUTPUT / "cases").glob("*.json"))),
    "coverage_summary": "instrumented/coverage-summary.json", "coverage_details": "instrumented/coverage-final.json",
}
save("execution.json", execution)
save("progress.json", {"status": "COMPLETED", "execution": "execution.json", "completed_cases": execution["case_checkpoints"]})
print(json.dumps(execution, indent=2))
raise SystemExit(completed.returncode)
