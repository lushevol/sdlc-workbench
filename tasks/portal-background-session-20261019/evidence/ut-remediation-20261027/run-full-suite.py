"""Run the complete isolated proposal suite and retain source-bound evidence."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


scratch = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
workspace = Path(__file__).resolve().parents[4]
application = workspace / "repos/ui/mfe-base"
reporter = (
    workspace
    / "tasks/portal-background-session-20261019/evidence"
    / "delivery-confidence-20261026/unit/case-reporter.cjs"
)
output.mkdir(parents=True, exist_ok=False)
environment = dict(os.environ, BABEL_ENV="test", RUN_EVIDENCE_DIR=str(output))
paths = subprocess.check_output(
    ["git", "-C", str(scratch), "ls-files", "-z"], text=True
).rstrip("\0").split("\0")
paths = sorted(set(paths + ["src/hooks/service/util/requestLoading.ts"]))
before = {name: sha256(scratch / name) for name in paths}
application_before = {
    name: sha256(application / name)
    for name in paths
    if (application / name).is_file()
}
binding = {
    "baseline_commit": "b8d4f1b837c6388452fbdc540f311257e805f932",
    "execution_scope": "isolated proposal; not the application checkout",
    "scratch": str(scratch),
    "application": str(application),
    "files": before,
    "reporter_sha256": sha256(reporter),
    "dependency_source": str(application / "node_modules"),
    "installed_versions": {
        name: json.loads((scratch / "node_modules" / name / "package.json").read_text())["version"]
        for name in ["axios", "jest", "react", "typescript"]
    },
    "limits": [
        "Dependencies reuse the existing installed local node_modules directory.",
        "These results do not identify a production artifact or target environment.",
    ],
}
(output / "source-binding.json").write_text(json.dumps(binding, indent=2) + "\n")
inventory_command = [
    "node", "node_modules/jest/bin/jest.js", "--listTests", "--json", "--runInBand"
]
inventory_result = subprocess.run(
    inventory_command, cwd=scratch, env=environment, capture_output=True, text=True
)
(output / "inventory-stderr.log").write_text(inventory_result.stderr)
inventory_result.check_returncode()
inventory = json.loads(inventory_result.stdout)
(output / "suite-inventory.json").write_text(json.dumps({
    "command": inventory_command,
    "cwd": str(scratch),
    "suite_count": len(inventory),
    "suites": inventory,
    "exclusions": [],
    "scope": "Complete configured Jest discovery; no path or test-name filter.",
}, indent=2) + "\n")
command = [
    "node", "node_modules/jest/bin/jest.js", "--runInBand", "--coverage=false",
    "--ci", "--detectOpenHandles", "--json", f"--outputFile={output / 'results.json'}",
    "--reporters=default", f"--reporters={reporter}",
]
started_at = datetime.now(timezone.utc).isoformat()
started = time.monotonic()
with (output / "runner.log").open("w") as log:
    completed = subprocess.run(command, cwd=scratch, env=environment, stdout=log, stderr=subprocess.STDOUT)
execution = {
    "started_at": started_at,
    "ended_at": datetime.now(timezone.utc).isoformat(),
    "elapsed_seconds": time.monotonic() - started,
    "command": command,
    "cwd": str(scratch),
    "environment": {"BABEL_ENV": "test", "RUN_EVIDENCE_DIR": str(output)},
    "exit_code": completed.returncode,
    "force_exit": False,
    "outer_timeout": False,
    "inventory_suites": len(inventory),
    "source_changed_during_run": [name for name in paths if sha256(scratch / name) != before[name]],
    "application_checkout_changed": [
        name for name, digest in application_before.items() if sha256(application / name) != digest
    ],
}
results_path = output / "results.json"
if results_path.is_file():
    result = json.loads(results_path.read_text())
    execution.update({
        "suites": result["numTotalTestSuites"],
        "passed_suites": result["numPassedTestSuites"],
        "failed_suites": result["numFailedTestSuites"],
        "tests": result["numTotalTests"],
        "passed_tests": result["numPassedTests"],
        "failed_tests": result["numFailedTests"],
        "skipped_tests": result["numPendingTests"],
        "todo_tests": result.get("numTodoTests", 0),
        "runtime_error_suites": result.get("numRuntimeErrorTestSuites", 0),
        "case_checkpoints": len(list((output / "cases").glob("*.json"))),
    })
else:
    execution["result_error"] = "Jest did not retain results.json."
(output / "execution.json").write_text(json.dumps(execution, indent=2) + "\n")
print(json.dumps(execution, indent=2))
raise SystemExit(completed.returncode)
