"""Retain a wheel installation and generated-workspace parity check."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent / ("distribution-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
EVIDENCE.mkdir()
RUN = Path(tempfile.mkdtemp(prefix="release-clinic-parity-wheel-")).resolve()
PYTHON = ROOT / ".venv/bin/python"
UPSTREAM = Path("plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md")
SKILL = Path(".agents/skills/release-clinic")
records = []


def execute(name, arguments, *, directory=RUN, environment=None):
    result = subprocess.run(
        [str(value) for value in arguments], cwd=directory, env=environment,
        capture_output=True, text=True, timeout=180,
    )
    (EVIDENCE / (name + ".log")).write_text(result.stdout + result.stderr, encoding="utf-8")
    records.append({
        "name": name, "argv": [str(value) for value in arguments],
        "cwd": str(directory), "exit_code": result.returncode,
        "log": name + ".log",
    })
    if result.returncode:
        raise RuntimeError(f"{name} returned {result.returncode}; inspect its retained log.")
    return result.stdout


report = {
    "started_at": datetime.now(timezone.utc).isoformat(), "run_directory": str(RUN),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
try:
    execute("wheel-build", [PYTHON, "-m", "pip", "wheel", ".", "--no-deps", "--no-build-isolation",
                            "--no-index", "--wheel-dir", RUN / "wheels"], directory=ROOT)
    wheels = list((RUN / "wheels").glob("*.whl"))
    assert len(wheels) == 1
    wheel = wheels[0]
    report["wheel"] = {"path": str(wheel), "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest()}
    installed = RUN / "installed"
    execute("wheel-install", [PYTHON, "-m", "pip", "install", "--no-deps", "--no-index", "--no-compile",
                              "--target", installed, wheel])
    environment = dict(os.environ, PYTHONPATH=str(installed))
    identity = json.loads(execute("installed-identity", [
        PYTHON, "-c", "import ai_sdlc_workbench,json; print(json.dumps(ai_sdlc_workbench.__file__))",
    ], environment=environment))
    assert Path(identity).is_relative_to(installed)
    workspace = RUN / "workspace"
    execute("workspace-init", [PYTHON, "-m", "ai_sdlc_workbench", "init", workspace,
                               "--name", "Release Clinic parity"], environment=environment)
    execute("workspace-validate", [PYTHON, "-m", "ai_sdlc_workbench", "--workspace", workspace, "validate"],
            environment=environment)
    paths = json.loads(execute("installed-paths", [
        PYTHON, "-m", "ai_sdlc_workbench", "--workspace", workspace, "release-clinic", "path",
    ], environment=environment))
    upstream = Path(paths["report_skill"])
    assert upstream == installed / "ai_sdlc_workbench/release-clinic" / UPSTREAM
    source_bytes = (ROOT / "core/release-clinic" / UPSTREAM).read_bytes()
    checks = {
        "installed_upstream": upstream.read_bytes() == source_bytes,
        "installed_scaffold": (installed / "ai_sdlc_workbench/scaffold" / SKILL /
                               "references/dtp-tda-report.md").read_bytes() == source_bytes,
        "generated_reference": (workspace / SKILL / "references/dtp-tda-report.md").read_bytes() == source_bytes,
        "generated_helper": (workspace / SKILL / "scripts/check_report_parity.py").read_bytes() ==
                            (ROOT / SKILL / "scripts/check_report_parity.py").read_bytes(),
        "no_runtime_copy": not (workspace / "core/release-clinic").exists(),
        "no_pyproject": not (workspace / "pyproject.toml").exists(),
    }
    for relative in (SKILL / "SKILL.md", SKILL / "references/html-reporting.md", Path("docs/RELEASE_CLINIC.md")):
        checks[str(relative)] = (workspace / relative).read_bytes() == (ROOT / relative).read_bytes()
    for relative in ("knowledge/schemas/requirement.schema.json", "tasks/README.md", "docs/RELEASE_CLINIC.md"):
        checks[relative] = (workspace / relative).is_file()
    report["checks"] = checks
    assert all(checks.values()), checks
    parity = json.loads(execute("installed-parity", [
        PYTHON, "-S", workspace / SKILL / "scripts/check_report_parity.py", "--upstream", upstream,
    ], directory=workspace))
    assert parity["status"] == "MATCH"
    report["comparison"] = parity
    report["status"] = "PASSED"
except Exception as error:
    report.update(status="FAILED", error=str(error))
    raise
finally:
    report.update(commands=records, finished_at=datetime.now(timezone.utc).isoformat())
    (EVIDENCE / "distribution.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
