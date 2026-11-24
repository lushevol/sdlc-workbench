"""Run copied source fixtures without changing the active browser checkout."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[5]
REPO = ROOT / "repos/ui/mfe-base"
EVIDENCE = Path(__file__).resolve().parent
FIXTURES = ROOT / ".workbench/session-active-cutoff-unit-proof-20261024"
BASE_REVISION = "6e34da31961eb6bce4ef6c3daea83a2f7bd48e85"
HOME = "src/pages/Home/common/useController.ts"
FOCUSED = [
    "src/pages/Home/common/sessionRefresh.test.tsx",
    "src/pages/Home/common/sessionLifecycle.test.tsx",
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(name, data):
    (EVIDENCE / name).write_text(json.dumps(data, indent=2) + "\n")


def run(label, fixture, tests):
    result_path = EVIDENCE / f"{label}-result.json"
    command = [
        str(fixture / "node_modules/.bin/jest"),
        "--runInBand",
        "--coverage=false",
        "--ci",
        "--reporters=default",
        "--json",
        f"--outputFile={result_path}",
        *tests,
    ]
    started_at = datetime.now(timezone.utc).isoformat()
    execution = subprocess.run(
        command,
        cwd=fixture,
        env={**os.environ, "BABEL_ENV": "test"},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    (EVIDENCE / f"{label}.log").write_text(execution.stdout)
    outcome = {
        "label": label,
        "started_at": started_at,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "cwd": str(fixture),
        "environment": {"BABEL_ENV": "test"},
        "exit_code": execution.returncode,
        "result": str(result_path.relative_to(ROOT)),
        "log": f"{label}.log",
    }
    if result_path.exists():
        result = json.loads(result_path.read_text())
        outcome["runner_summary"] = {
            key: result[key]
            for key in [
                "numPassedTestSuites",
                "numFailedTestSuites",
                "numPassedTests",
                "numFailedTests",
                "numPendingTests",
                "numTodoTests",
                "success",
            ]
        }
    write_json(f"{label}-execution.json", outcome)
    print(json.dumps(outcome), flush=True)
    return outcome


FIXTURES.mkdir(parents=True, exist_ok=True)
candidate = FIXTURES / "candidate"
baseline = FIXTURES / "baseline-home"
for fixture in [candidate, baseline]:
    if fixture.exists():
        raise SystemExit(f"Refuse to overwrite existing fixture: {fixture}")
    fixture.mkdir()
    shutil.copytree(REPO / "src", fixture / "src")
    for name in ["jest.config.ts", "jest.setup.tsx", "babel.config.json", "tsconfig.json", "package.json"]:
        shutil.copy2(REPO / name, fixture / name)
    (fixture / "node_modules").symlink_to((REPO / "node_modules").resolve(), target_is_directory=True)

baseline_bytes = subprocess.check_output(["git", "show", f"{BASE_REVISION}:{HOME}"], cwd=REPO)
(baseline / HOME).write_bytes(baseline_bytes)
source_binding = {
    "base_revision": BASE_REVISION,
    "candidate_home_sha256": sha((candidate / HOME).read_bytes()),
    "baseline_home_sha256": sha(baseline_bytes),
    "candidate_test_sha256": {path: sha((candidate / path).read_bytes()) for path in FOCUSED},
    "method": "Copy candidate src and config twice; replace only baseline fixture Home with Git base bytes.",
    "candidate_fixture": str(candidate),
    "baseline_fixture": str(baseline),
    "dependency_path": str((REPO / "node_modules").resolve()),
    "active_checkout_mutated": False,
    "limits": [
        "Controlled jsdom integration uses fake timers and a test Axios adapter.",
        "This proof does not establish browser or deployed service behavior.",
        "Jest reports it.failing as passed when the required assertion fails as expected.",
    ],
}
write_json("regression-source-binding.json", source_binding)

executions = [
    run("baseline-home-focused", baseline, FOCUSED),
    run("candidate-focused", candidate, FOCUSED),
    run("candidate-full", candidate, []),
]
write_json("regression-executions.json", executions)
