"""Run the unchanged retained provider timer case against the final committed source."""
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time

out = Path(__file__).resolve().parent
root = out.parents[4]
app = root / "repos/ui/mfe-base"
historical = root / "tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/independent-review"
node = Path("/Users/lushevol/.nvm/versions/node/v24.16.0/bin/node")
revision = "1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303"
test_relative = "src/pages/Home/common/delayedTimerTie.provider.test.tsx"
test_source = historical / "delayedTimerTie.provider.test.tsx"
reporter = root / "tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/unit/case-reporter.cjs"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, value):
    (out / name).write_text(json.dumps(value, indent=2) + "\n")

head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=app, text=True).strip()
if head != revision:
    save("blocker.json", {"status": "BLOCKED", "expected_revision": revision, "actual_revision": head,
                          "blocker": "Final application HEAD changed before the focused run."})
    raise SystemExit(1)
if not node.is_file() or not (app / "node_modules/jest/bin/jest.js").is_file():
    save("blocker.json", {"status": "BLOCKED", "blocker": "The retained Node or Jest dependency is unavailable."})
    raise SystemExit(1)
scratch = Path(tempfile.mkdtemp(prefix="mfe-final-timer-control-20261027-"))
archive_bytes = subprocess.check_output(["git", "archive", revision], cwd=app)
with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as archive:
    archive.extractall(scratch, filter="data")
(scratch / "node_modules").symlink_to(app / "node_modules", target_is_directory=True)
(scratch / test_relative).write_bytes(test_source.read_bytes())
paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", revision], cwd=app, text=True).splitlines()
paths.append(test_relative)
before = {name: sha(scratch / name) for name in sorted(paths)}
app_before = {name: sha(app / name) for name in paths if (app / name).is_file()}
original_paths = ["late-timer-provider-comparison.json", "late-timer-provider-commands.json",
                  "late-timer-provider-main-observation.json", "late-timer-provider-candidate-observation.json",
                  "late-timer-provider-main-execution.json", "late-timer-provider-candidate-execution.json",
                  "delayedTimerTie.provider.test.tsx"]
original_hashes = {name: sha(historical / name) for name in original_paths}
source_binding = {
    "revision": revision, "application": str(app), "scratch": str(scratch),
    "execution_scope": "One unchanged retained default-lifetime provider case against final committed source.",
    "files": before, "test_relative_path": test_relative, "test_sha256": sha(test_source),
    "retained_test_sha256": "9f43f74fee05efb1065465ccc7afda71ac1551defc5ad7add2b8ce2af84c02ef",
    "assertions_changed": False, "application_source_changed": False,
    "reporter_sha256": sha(reporter), "runner_sha256": sha(Path(__file__)),
    "dependency_root": str((app / "node_modules").resolve()),
    "node": subprocess.check_output([str(node), "--version"], text=True).strip(),
    "installed_versions": {name: json.loads((app / "node_modules" / name / "package.json").read_text())["version"]
                           for name in ["axios", "jest", "react", "typescript"]},
    "historical_evidence_directory": str(historical), "historical_evidence_sha256": original_hashes,
    "limits": ["Dependencies reuse the existing local installation.",
               "The fake clock and immediate Axios adapter do not measure native timer jitter or live service issuance."]
}
save("source-binding.json", source_binding)
command = [str(node), "node_modules/jest/bin/jest.js", "--runInBand", "--runTestsByPath", test_relative,
           "--json", "--outputFile=" + str(out / "results.json"),
           "--reporters=default", "--reporters=" + str(reporter)]
environment = dict(os.environ, BABEL_ENV="test", MFE_REVIEW_OBSERVATION_PATH=str(out / "observation.json"),
                   RUN_EVIDENCE_DIR=str(out))
started_at = datetime.now(timezone.utc).isoformat()
launch = {"revision": revision, "cwd": str(scratch), "argv": command,
          "environment": {name: environment[name] for name in ["BABEL_ENV", "MFE_REVIEW_OBSERVATION_PATH", "RUN_EVIDENCE_DIR"]},
          "started_at": started_at, "force_exit": False, "outer_timeout": False,
          "reporter_difference": "An immediate case checkpoint reporter is added. Test bytes and assertions are unchanged."}
save("launch.json", launch)
started = time.monotonic()
with (out / "runner.log").open("w") as stream:
    completed = subprocess.run(command, cwd=scratch, env=environment, stdout=stream, stderr=subprocess.STDOUT)
execution = dict(launch, completed_at=datetime.now(timezone.utc).isoformat(),
                 elapsed_seconds=time.monotonic() - started, exit_code=completed.returncode,
                 source_changed_during_run=[name for name, digest in before.items() if sha(scratch / name) != digest],
                 application_checkout_changed=[name for name, digest in app_before.items() if sha(app / name) != digest],
                 historical_evidence_changed=[name for name, digest in original_hashes.items() if sha(historical / name) != digest],
                 case_checkpoints=len(list((out / "cases").glob("*.json"))))
if (out / "results.json").is_file():
    results = json.loads((out / "results.json").read_text())
    execution.update({name: results[name] for name in ["numTotalTestSuites", "numPassedTestSuites", "numFailedTestSuites",
                                                     "numTotalTests", "numPassedTests", "numFailedTests", "numPendingTests",
                                                     "numRuntimeErrorTestSuites", "numTodoTests", "success", "wasInterrupted"]})
else:
    execution["result_error"] = "The focused runner did not retain results.json."
save("execution.json", execution)
print(json.dumps(execution, indent=2))
raise SystemExit(completed.returncode)
