"""Run the adopted Release Clinic tools with workspace-root configuration."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

from .models import WorkbenchError


_DEPENDENCIES = {
    "requests": "requests", "urllib3": "urllib3", "yaml": "PyYAML",
    "bs4": "beautifulsoup4", "lxml": "lxml", "atlassian": "atlassian-python-api",
    "sonarqube": "python-sonarqube-api", "cryptography": "cryptography", "rapidfuzz": "rapidfuzz",
    "fastapi": "fastapi", "uvicorn": "uvicorn", "pydantic": "pydantic",
}


def paths() -> dict[str, Path]:
    root = Path(__file__).resolve().parent / "release-clinic"
    report = root / "plugins/test/dtp-tda-report/skills/dtp-tda-report"
    service = root / "plugins/test/dtp-tda-service"
    return {"root": root, "scripts": report / "scripts", "report_skill": report / "SKILL.md",
            "portfolio_skill": service / "skills/dtp-tda-portfolio-report/SKILL.md",
            "trends_skill": root / "plugins/test/dtp-tda-trends/skills/dtp-tda-trends/SKILL.md",
            "service": service}


def _environment(root: Path, *, service: bool = False) -> dict[str, str]:
    """Prepare an isolated child environment without changing the caller's values."""
    helper = paths()["root"] / "release_clinic_env.py"
    spec = importlib.util.spec_from_file_location("_workbench_release_env", helper)
    if spec is None or spec.loader is None:
        raise WorkbenchError("Install the Release Clinic runtime assets.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # The imported tools use os.environ. Keep their loader confined to this copy.
    module.os = SimpleNamespace(environ=dict(os.environ, AI_SDLC_WORKSPACE=str(root)), PathLike=os.PathLike)
    try:
        module.load_environment((module.os.environ.get("SERVICE_ENV_FILE", "").strip() or None) if service else None)
    except (ValueError, OSError) as error:
        raise WorkbenchError("Load Release Clinic settings from the workspace root. Check the configured file path.") from error
    return dict(module.os.environ)


def doctor(root: Path) -> dict:
    """Check local prerequisites without contacting an external system."""
    environment = _environment(root)
    missing = [package for module, package in _DEPENDENCIES.items() if importlib.util.find_spec(module) is None]
    required = ["ADO_TOKEN", "ADO_ORGANIZATION", "ADO_PROJECT", "CONFLUENCE_URL",
                "CONFLUENCE_TOKEN", "SONAR_URL", "SONAR_TOKEN", "GENIE_TOKEN", "GENIE_REPORT_LINK"]
    if environment.get("SNOW_ENABLED", "true").lower() == "true":
        required += ["CLIENT_ID", "FERNET_KEY", "SNOW_BLADE_KEY"]
    unset = [key for key in required if not environment.get(key, "").strip()]
    locations = paths()
    configurations = {
        "TDA_STREAM_CONFIG": environment.get("TDA_STREAM_CONFIG") or str(locations["scripts"] / "stream_config.yaml"),
        "TDA_FIELD_CONFIG": environment.get("TDA_FIELD_CONFIG") or str(locations["scripts"] / "ado_field_config.yaml"),
        "STREAM_CONFIG_FILE": environment.get("STREAM_CONFIG_FILE") or str(locations["service"] / "service/stream_config.yaml"),
    }
    missing_files = [name for name, path in configurations.items() if not Path(path).is_file()]
    selected = environment.get("AI_SDLC_ENV_FILE") or ".env"
    env_path = Path(selected).expanduser()
    if not env_path.is_absolute():
        env_path = root / env_path
    return {"status": "READY" if not missing and not unset and not missing_files else "INCOMPLETE",
            "workspace": str(root), "environment_file": str(env_path),
            "environment_file_exists": env_path.is_file(), "missing_dependencies": missing,
            "missing_configuration": unset,
            "configuration_files": configurations, "missing_files": missing_files,
            "install": f'{sys.executable} -m pip install "ai-sdlc-workbench[release-clinic]"',
            "limitations": ["Checks inspect local configuration only.",
                            "Credentials and endpoint access remain untested.",
                            "Stream overrides can change the required ServiceNow settings.",
                            "A report verdict does not establish approved knowledge or verified business behavior."]}


def run(root: Path, operation: str, arguments: list[str]) -> int:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise WorkbenchError("Select an existing workspace directory.")
    if operation == "path":
        print(json.dumps({key: str(value) for key, value in paths().items()}, indent=2))
        return 0
    if operation == "doctor":
        result = doctor(root)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "READY" else 1
    locations = paths()
    environment = _environment(root, service=operation == "serve")
    scripts, service = locations["scripts"], locations["service"]
    environment["PYTHONPATH"] = os.pathsep.join([str(locations["root"]), str(scripts), str(service)])
    if operation == "serve":
        command = [sys.executable, "-m", "uvicorn", "service.main:app", "--host", "127.0.0.1", "--port", "8080"]
    else:
        script = {"collect": scripts / "AutoTDAScript.py", "report": scripts / "gen_tda_report.py",
                  "portfolio": service / "scripts/aggregate_portfolio.py",
                  "audit": scripts / "tda_audit/run_tda_audit.py"}[operation]
        command = [sys.executable, str(script)]
    forwarded = arguments[1:] if arguments[:1] == ["--"] else arguments
    return subprocess.run([*command, *forwarded], cwd=root, env=environment, check=False).returncode
