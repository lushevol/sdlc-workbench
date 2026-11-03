"""Install a source checkout with approved local runtimes and report remaining setup."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import uuid
import venv


class SetupError(Exception):
    """A recoverable setup failure with a credential-free message."""


DEFAULT_DOWNLOAD_TIMEOUT = 120


def positive_seconds(value: str) -> int:
    try:
        seconds = int(value)
        if 1 <= seconds <= 86400:
            return seconds
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("Use a whole number of seconds from 1 to 86400.")


def download_guidance(kind: str) -> str:
    """Describe recovery without reflecting private registry URLs or subprocess output."""
    packages = "Python wheels" if kind == "python" else "locked npm packages"
    return (f"Warning: {packages} could not be downloaded. Company network access may block the request. "
            "Use an approved package mirror, or prepare an offline bundle on an approved connected computer. "
            "Match the source checkout, OS, CPU, and Python version. Transfer the complete bundle, then run "
            "setup with --offline-bundle PATH. See docs/SETUP.md#blocked-downloads-and-manual-recovery.")


def npm_download_options(seconds: int) -> list[str]:
    return ["--fetch-retries=0", f"--fetch-timeout={min(15, seconds) * 1000}"]


def stop_download(process: subprocess.Popen) -> None:
    """Stop package-manager descendants as well as the original downloader."""
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=5, shell=False)
        except (OSError, subprocess.TimeoutExpired):
            pass
        if process.poll() is None:
            process.kill()
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.communicate(timeout=5)


def environment(python: Path | None = None, *, offline: bool = False) -> dict[str, str]:
    result = ({key: value for key, value in os.environ.items() if key.upper() in {
        "PATH", "PATHEXT", "SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP", "TMPDIR",
        "USERPROFILE", "APPDATA", "LOCALAPPDATA", "HOME", "LANG", "LC_ALL", "LC_CTYPE"}}
        if offline else dict(os.environ))
    result.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    result.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")
    if offline:
        result["PIP_CONFIG_FILE"] = os.devnull
    if python is not None:
        result["PATH"] = str(python.parent) + os.pathsep + result.get("PATH", "")
    return result


def command(arguments: list[str], root: Path, *, capture: bool = False, seconds: int = 900,
            python: Path | None = None, offline: bool = False,
            download: str | None = None) -> subprocess.CompletedProcess:
    """Keep installer diagnostics out of reports because indexes can contain credentials."""
    try:
        if download:
            settings = environment(python, offline=offline)
            settings.update(PIP_TIMEOUT=str(min(15, seconds)), PIP_RETRIES="0", PIP_DISABLE_PIP_VERSION_CHECK="1")
            # A separate session allows timeout cleanup to include pip build and browser helpers.
            process = subprocess.Popen(arguments, cwd=root, env=settings, shell=False,
                                       stdin=subprocess.DEVNULL,
                                       stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL, encoding="utf-8", errors="replace",
                                       start_new_session=os.name != "nt")
            try:
                stdout, _ = process.communicate(timeout=seconds)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                stop_download(process)
                raise
            return subprocess.CompletedProcess(arguments, process.returncode, stdout=stdout)
        return subprocess.run(arguments, cwd=root, env=environment(python, offline=offline), shell=False,
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, timeout=seconds, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        if download:
            raise SetupError(f"Download timed out after {seconds} seconds. " + download_guidance(download)) from None
        raise SetupError("A setup command could not finish. Check installed runtimes and company package access.") from None
    except OSError:
        if download:
            raise SetupError("The download command could not run. " + download_guidance(download)) from None
        raise SetupError("A setup command could not finish. Check installed runtimes and company package access.") from None


def source_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if not (root / "pyproject.toml").is_file() or not (root / "core/cli.py").is_file():
        raise SetupError("Run setup from the complete source checkout. Read docs/SETUP.md.")
    return root


def python_path(root: Path, *, windows: bool | None = None) -> Path:
    windows = os.name == "nt" if windows is None else windows
    return root / ".venv" / ("Scripts/python.exe" if windows else "bin/python")


def npm_command(root: Path, *, offline: bool = False) -> list[str]:
    """Run the npm JavaScript entry point directly, including on Windows."""
    node = shutil.which("node")
    if not node:
        raise SetupError("Node.js is missing. Install company-approved Node 24 LTS, then run setup again. "
                         "Use your company software portal or https://nodejs.org/en/download. "
                         "See docs/SETUP.md#blocked-downloads-and-manual-recovery.")
    result = command([node, "--version"], root, capture=True, seconds=10, offline=offline)
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
    """Diagnose fresh or damaged installations through the standard-library source checker."""
    selected = python if python.is_file() else Path(sys.executable)
    project_python_usable = python.is_file()

    def inspect(module: str) -> dict | None:
        result = command([str(selected), "-m", module, "--workspace", str(workspace),
                          "--profile", "core" if core_only else "all"], root,
                         capture=True, seconds=90, python=selected)
        try:
            payload = json.loads(result.stdout)
            if (isinstance(payload, dict) and isinstance(payload.get("features"), list)
                    and payload.get("core_status") in {"READY", "INCOMPLETE"}
                    and payload.get("status") in {"READY", "INCOMPLETE"}):
                return payload
        except (ValueError, TypeError):
            pass
        return None

    if project_python_usable:
        try:
            payload = inspect("ai_sdlc_workbench.doctor")
            if payload is not None:
                return payload
        except SetupError:
            selected = Path(sys.executable)
            project_python_usable = False
    try:
        payload = inspect("core.doctor")
    except SetupError:
        payload = None
    if payload is None and selected != Path(sys.executable):
        selected = Path(sys.executable)
        project_python_usable = False
        payload = inspect("core.doctor")
    if payload is None:
        raise SetupError("The installed setup checker is unavailable. Run setup without --check to repair the installation.") from None
    action = "Run setup without --check to install the project environment and Workbench package."
    checks = [
        {"id": "project-python", "status": "READY" if project_python_usable else "INCOMPLETE",
         "next_action": None if project_python_usable else action},
        {"id": "installed-runtime", "status": "INCOMPLETE", "next_action": action},
    ]
    payload["features"].insert(0, {"id": "setup", "status": "INCOMPLETE", "checks": checks,
        "integration_access": "UNTESTED", "next_actions": [action],
        "limitations": ["Source diagnosis does not establish an installed project environment."]})
    payload.update(status="INCOMPLETE", core_status="INCOMPLETE", diagnostic_source="source",
                   diagnostic_python=str(selected))
    payload["next_actions"] = list(dict.fromkeys([action, *payload.get("next_actions", [])]))
    return payload


def install(root: Path, workspace: Path, *, core_only: bool,
            offline_bundle: Path | None = None,
            download_timeout: int = DEFAULT_DOWNLOAD_TIMEOUT) -> tuple[Path, list[dict]]:
    if workspace.exists() and not workspace.is_dir():
        raise SetupError("Select a workspace directory. Read docs/SETUP.md.")
    initialized = any((workspace / name).is_file() for name in ("workspace.yaml", "workspace.json"))
    if workspace.exists() and any(workspace.iterdir()) and not initialized:
        raise SetupError("The selected directory has no workspace configuration. Choose an empty directory or an existing workspace.")
    if not core_only and not all((root / name).is_file() for name in
                                 ("package.json", "package-lock.json", "core/connectors/workbench/bridge.js")):
        raise SetupError("Connector source is missing. Use the complete Git checkout, or select --core-only.")
    bundle = None
    if offline_bundle is not None:
        if __package__:
            from .offline import target, validate_bundle
        else:
            from offline import target, validate_bundle
        bundle = validate_bundle(root, offline_bundle, core_only=core_only)
    stages = []
    npm = None
    if not core_only:
        try:
            npm = npm_command(root, offline=bundle is not None)
        except SetupError as error:
            stages.append({"id": "connectors", "status": "INCOMPLETE", "next_action": str(error)})
    python = python_path(root)
    if not python.is_file():
        if (root / ".venv").exists():
            raise SetupError("The existing .venv is incomplete or belongs to another platform. Preserve it and select a clean checkout.")
        print("Create the project Python environment.", flush=True)
        venv.EnvBuilder(with_pip=True).create(root / ".venv")
    version = command([str(python), "-c", "import sys; raise SystemExit(sys.version_info < (3, 10))"],
                      root, python=python, seconds=10, offline=bundle is not None)
    if version.returncode:
        raise SetupError("The project environment needs Python 3.10 or newer. Preserve it and use a compatible environment.")
    if bundle:
        identity = command([str(python), str(root / "core/offline.py"), "target"], root,
                           capture=True, python=python, seconds=10, offline=True)
        try:
            matching = identity.returncode == 0 and json.loads(identity.stdout) == target()
        except (ValueError, TypeError):
            matching = False
        if not matching:
            raise SetupError("The existing .venv differs from the bundle Python. Use a fresh checkout with the matching approved Python.")
    package = str(bundle.workbench_wheel) if bundle else str(root)
    packages = [package if core_only else package + "[release-clinic]"]
    if not core_only:
        if os.name == "nt":
            packages.append("pywin32>=305")
    pip_options = (["--no-index", "--find-links", str(bundle.wheelhouse), "--only-binary=:all:",
                    "--no-build-isolation", "--no-cache-dir", "--force-reinstall"] if bundle else [])
    print("Install Python packages from the offline bundle." if bundle else
          "Install Python packages through the configured package index.", flush=True)
    if command([str(python), "-m", "pip", "install", *pip_options, *packages], root,
               python=python, offline=bundle is not None, seconds=900 if bundle else download_timeout,
               download=None if bundle else "python").returncode:
        if bundle:
            raise SetupError("Offline Python installation failed. Prepare a complete bundle for this computer; online fallback is disabled.")
        raise SetupError("Python package installation failed. " + download_guidance("python"))
    if command([str(python), "-m", "pip", "check"], root, python=python, seconds=60,
               offline=bundle is not None).returncode:
        raise SetupError("Python dependency conflicts remain. Run the project Python with -m pip check to inspect them.")
    stages.append({"id": "python", "status": "SUCCEEDED"})
    if npm:
        print("Install connector packages from the offline bundle." if bundle else
              "Install connector packages through the configured npm registry.", flush=True)
        arguments = [*npm, "ci", "--ignore-scripts", "--no-audit", "--no-fund"]
        if bundle:
            # Keep bundle hashes stable when npm updates its cache index.
            with tempfile.TemporaryDirectory(prefix="workbench-offline-npm-") as temporary:
                cache = Path(temporary) / "cache"
                shutil.copytree(bundle.npm_cache, cache)
                user_config, global_config = Path(temporary) / "user.npmrc", Path(temporary) / "global.npmrc"
                user_config.touch()
                global_config.touch()
                result = command([*arguments, "--offline", "--cache", str(cache),
                                  "--userconfig", str(user_config), "--globalconfig", str(global_config)],
                                 root, python=python, offline=True)
        else:
            try:
                result = command([*arguments, *npm_download_options(download_timeout)], root,
                                 python=python, seconds=download_timeout, download="npm")
            except SetupError as error:
                stages.append({"id": "connectors", "status": "INCOMPLETE", "next_action": str(error)})
                result = None
        if result is None:
            pass
        elif result.returncode:
            stages.append({"id": "connectors", "status": "INCOMPLETE", "next_action":
                           ("Offline npm installation failed. Prepare the complete lockfile cache; online fallback is disabled."
                            if bundle else
                            "npm installation failed. " + download_guidance("npm"))})
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
    parser.add_argument("--json", action="store_true", help="Print structured diagnostics with --check")
    parser.add_argument("--offline-bundle", type=Path,
                        help="Install from a prepared bundle without package registry access; also detects ./offline-bundle")
    parser.add_argument("--download-timeout", type=positive_seconds, default=DEFAULT_DOWNLOAD_TIMEOUT,
                        help="Maximum seconds per online package command (default: 120); local/offline checks are separate")
    options = parser.parse_args(argv)
    if options.json and not options.check:
        parser.error("--json requires --check")
    try:
        if sys.version_info < (3, 10):
            raise SetupError("Python 3.10 or newer is required. Use company-approved Python 3.12.")
        root = source_root()
        workspace = (options.workspace or root).expanduser().resolve()
        if options.check:
            payload = doctor(python_path(root), root, workspace, core_only=options.core_only)
            if options.json:
                print(json.dumps(payload, indent=2, ensure_ascii=True))
            else:
                display(payload)
            return 0 if payload["status"] == "READY" else 1
        offline_bundle = options.offline_bundle
        if offline_bundle is None and ((root / "offline-bundle").exists() or (root / "offline-bundle").is_symlink()):
            offline_bundle = root / "offline-bundle"
        if offline_bundle is not None:
            offline_bundle = offline_bundle.expanduser().absolute()
        python, stages = install(root, workspace, core_only=options.core_only, offline_bundle=offline_bundle,
                                 download_timeout=options.download_timeout)
        payload = doctor(python, root, workspace, core_only=options.core_only)
        display(payload)
        for stage in stages:
            if stage.get("next_action"):
                print(stage["next_action"])
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
