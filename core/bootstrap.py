"""Install a source checkout with approved local runtimes and report remaining setup."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
import venv


class SetupError(Exception):
    """A recoverable setup failure with a credential-free message."""


def environment(python: Path | None = None) -> dict[str, str]:
    result = dict(os.environ)
    result.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    result.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")
    if python is not None:
        result["PATH"] = str(python.parent) + os.pathsep + result.get("PATH", "")
    return result


def command(arguments: list[str], root: Path, *, capture: bool = False, seconds: int = 900,
            python: Path | None = None) -> subprocess.CompletedProcess:
    """Keep installer diagnostics out of reports because indexes can contain credentials."""
    try:
        return subprocess.run(arguments, cwd=root, env=environment(python), shell=False,
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, timeout=seconds, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        raise SetupError("A setup command could not finish. Check installed runtimes and company package access.") from None


def source_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if not (root / "pyproject.toml").is_file() or not (root / "core/cli.py").is_file():
        raise SetupError("Run setup from the complete source checkout. Read docs/SETUP.md.")
    return root


def python_path(root: Path, *, windows: bool | None = None) -> Path:
    windows = os.name == "nt" if windows is None else windows
    return root / ".venv" / ("Scripts/python.exe" if windows else "bin/python")


def npm_command(root: Path) -> list[str]:
    """Run the npm JavaScript entry point directly, including on Windows."""
    node = shutil.which("node")
    if not node:
        raise SetupError("Node.js is missing. Install company-approved Node 24 LTS, then run setup again.")
    result = command([node, "--version"], root, capture=True, seconds=10)
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)\s*", result.stdout or "")
    version = tuple(map(int, match.groups())) if match else (0, 0, 0)
    if result.returncode or not ((version[0] == 22 and version >= (22, 12, 0)) or version[0] >= 24):
        raise SetupError("Use company-approved Node 22.12+ or Node 24+. Node 23 is outside the locked toolchain range.")
    shim = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    candidates = [Path(node).resolve().parent / "node_modules/npm/bin/npm-cli.js"]
    if shim:
        resolved = Path(shim).resolve()
        candidates.extend([resolved, resolved.parent / "node_modules/npm/bin/npm-cli.js",
                           resolved.parent.parent / "lib/node_modules/npm/bin/npm-cli.js"])
    for candidate in candidates:
        if candidate.name == "npm-cli.js" and candidate.is_file():
            return [node, str(candidate)]
    raise SetupError("The npm JavaScript entry point is missing. Repair the approved Node/npm installation.")


def ensure_environment_file(workspace: Path, template: Path) -> None:
    destination = workspace / ".env"
    if destination.exists() or destination.is_symlink():
        return
    contents = template.read_bytes()
    try:
        with destination.open("xb") as target:
            target.write(contents)
    except FileExistsError:
        pass


def doctor(python: Path, root: Path, workspace: Path, *, core_only: bool) -> dict:
    if not python.is_file():
        raise SetupError("The project environment is missing. Run setup without --check first.")
    result = command([str(python), "-m", "ai_sdlc_workbench.doctor", "--workspace", str(workspace),
                      "--profile", "core" if core_only else "all"], root,
                     capture=True, seconds=90, python=python)
    try:
        payload = json.loads(result.stdout)
        if not isinstance(payload, dict) or "features" not in payload or "core_status" not in payload:
            raise ValueError
    except (ValueError, TypeError):
        raise SetupError("The installed setup checker is unavailable. Run setup without --check to repair the installation.") from None
    return payload


def install(root: Path, workspace: Path, *, core_only: bool) -> tuple[Path, list[dict]]:
    if workspace.exists() and not workspace.is_dir():
        raise SetupError("Select a workspace directory. Read docs/SETUP.md.")
    initialized = any((workspace / name).is_file() for name in ("workspace.yaml", "workspace.json"))
    if workspace.exists() and any(workspace.iterdir()) and not initialized:
        raise SetupError("The selected directory has no workspace configuration. Choose an empty directory or an existing workspace.")
    if not core_only and not all((root / name).is_file() for name in
                                 ("package.json", "package-lock.json", "core/connectors/workbench/bridge.js")):
        raise SetupError("Connector source is missing. Use the complete Git checkout, or select --core-only.")
    stages = []
    npm = None
    if not core_only:
        try:
            npm = npm_command(root)
        except SetupError as error:
            stages.append({"id": "connectors", "status": "INCOMPLETE", "next_action": str(error)})
    python = python_path(root)
    if not python.is_file():
        if (root / ".venv").exists():
            raise SetupError("The existing .venv is incomplete or belongs to another platform. Preserve it and select a clean checkout.")
        print("Create the project Python environment.", flush=True)
        venv.EnvBuilder(with_pip=True).create(root / ".venv")
    version = command([str(python), "-c", "import sys; raise SystemExit(sys.version_info < (3, 10))"],
                      root, python=python, seconds=10)
    if version.returncode:
        raise SetupError("The project environment needs Python 3.10 or newer. Preserve it and use a compatible environment.")
    packages = [str(root) if core_only else str(root) + "[release-clinic]"]
    if not core_only:
        if os.name == "nt":
            packages.append("pywin32>=305")
    print("Install Python packages through the configured package index.", flush=True)
    if command([str(python), "-m", "pip", "install", *packages], root, python=python).returncode:
        raise SetupError("Python package installation failed. Check company package indexes, proxy settings, and compatible wheels.")
    if command([str(python), "-m", "pip", "check"], root, python=python, seconds=60).returncode:
        raise SetupError("Python dependency conflicts remain. Run the project Python with -m pip check to inspect them.")
    stages.append({"id": "python", "status": "SUCCEEDED"})
    if npm:
        print("Install connector packages through the configured npm registry.", flush=True)
        if command([*npm, "ci", "--ignore-scripts", "--no-audit", "--no-fund"], root,
                   python=python).returncode:
            stages.append({"id": "connectors", "status": "INCOMPLETE", "next_action":
                           "npm installation failed. Check company registry access and target-platform package availability."})
        else:
            stages.append({"id": "connectors", "status": "SUCCEEDED"})
    if not initialized:
        print("Initialize the selected empty workspace.", flush=True)
        if command([str(python), "-m", "ai_sdlc_workbench", "init", str(workspace)], root,
                   python=python, seconds=60).returncode:
            raise SetupError("Workspace initialization failed. Select an empty writable directory.")
    ensure_environment_file(workspace, root / ".env.example")
    return python, stages


def display(payload: dict) -> None:
    print("\nFeature                         Local readiness")
    print("------------------------------  ----------------")
    for feature in payload.get("features", []):
        print(f"{feature['id']:<30}  {feature['status']}")
    print(f"\nCore: {payload['core_status']}. Selected features: {payload['status']}.")
    print("External access and business behavior remain untested.")
    for action in payload.get("next_actions", []):
        print(f"- {action}")


def save_report(root: Path, payload: dict, stages: list[dict]) -> Path:
    folder = root / ".workbench/setup"
    if folder.parent.is_symlink() or folder.is_symlink():
        raise SetupError("Setup reports need a local .workbench/setup directory without symbolic links.")
    folder.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output = folder / run_id
    review = {"standard": "ASD-STE100", "automated_check": "PASSED" if payload["status"] == "READY" else "FAILED",
              "asd_review": "PENDING", "reviewer": None, "reviewed_at": None,
              "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."]}
    record = {"installation": stages, "readiness": payload, "output_review": review}
    output.with_suffix(".json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["---", *(f"{key}: {json.dumps(value)}" for key, value in review.items()), "---", "",
             "# Local setup report", "", f"Core: `{payload['core_status']}`.",
             f"Selected features: `{payload['status']}`.", "External access and business behavior remain untested.", "",
             "| Feature | Local readiness |", "| --- | --- |"]
    lines.extend(f"| {item['id']} | {item['status']} |" for item in payload["features"])
    lines.extend(["", "## Required actions", ""])
    lines.extend("- " + item for item in payload.get("next_actions", []))
    for stage in stages:
        if stage.get("next_action"):
            lines.append("- " + stage["next_action"])
    lines.extend(["", "Read docs/SETUP.md for installation limits and feature configuration.", ""])
    output.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    return output.with_suffix(".md")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, help="Existing workspace or empty directory; defaults to the source checkout")
    parser.add_argument("--core-only", action="store_true", help="Install or check only the Python core")
    parser.add_argument("--check", action="store_true", help="Check the installed environment without installing or writing files")
    options = parser.parse_args(argv)
    try:
        if sys.version_info < (3, 10):
            raise SetupError("Python 3.10 or newer is required. Use company-approved Python 3.12.")
        root = source_root()
        workspace = (options.workspace or root).expanduser().resolve()
        if options.check:
            payload = doctor(python_path(root), root, workspace, core_only=options.core_only)
            display(payload)
            return 0 if payload["status"] == "READY" else 1
        python, stages = install(root, workspace, core_only=options.core_only)
        payload = doctor(python, root, workspace, core_only=options.core_only)
        display(payload)
        complete = all(stage["status"] == "SUCCEEDED" for stage in stages) and payload["core_status"] == "READY"
        print("\nInstallation: " + ("COMPLETE" if complete else "INCOMPLETE") + ".")
        print("Report: " + str(save_report(root, payload, stages)))
        print("Guide: " + str(root / "docs/SETUP.md"))
        return 0 if complete else 1
    except SetupError as error:
        print("Setup incomplete. " + str(error), file=sys.stderr)
        return 1
    except OSError:
        print("Setup incomplete. Check local file permissions and installed runtimes. Read docs/SETUP.md.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Setup interrupted. Existing configuration is preserved. Run setup again to continue.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
