"""Inspect local prerequisites without contacting services or changing a workspace."""

from __future__ import annotations

import importlib.metadata as metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys


CORE_REQUIREMENTS = {
    "PyYAML": "==6.0.2", "tree-sitter": "==0.25.2", "tree-sitter-java": "==0.23.5",
    "tree-sitter-typescript": "==0.23.2", "jsonschema": "==4.25.1",
}
CLINIC_REQUIREMENTS = {
    "requests": ">=2.31.0", "urllib3": ">=2.0.0", "beautifulsoup4": ">=4.12.0",
    "lxml": ">=5.0.0", "atlassian-python-api": ">=3.41.0", "python-sonarqube-api": ">=2.0.4",
    "cryptography": ">=42.0.0", "rapidfuzz": ">=3.0.0", "fastapi": ">=0.111.0",
    "uvicorn": ">=0.29.0", "pydantic": ">=2.7.0", "extract-msg": ">=0.45.0",
}
CONNECTOR_VARIABLES = {
    "ado": ("AZURE_DEVOPS_ORG_URL", "AZURE_DEVOPS_PAT"),
    "confluence": ("CONFLUENCE_BASE_URL", "CONFLUENCE_PAT"),
    "scwiki": ("SCWIKI_URL", "SCWIKI_TOKEN"),
    "nexus": ("NEXUS_BASE_URL", "NEXUS_USER_CODE", "NEXUS_PASS_CODE"),
    "sonar": ("SONAR_BASE_URL", "SONAR_TOKEN"),
    "web": (), "messaging": (),
}
NODE_PACKAGES = ("@modelcontextprotocol/sdk", "axios", "azure-devops-node-api", "dotenv",
                 "https-proxy-agent", "node-fetch", "zod", "cheerio", *(
                     "@sc-node-mcp/" + name for name in (
                         "core", "ado-core", "ado", "ado-workitems-read", "ado-workitems-write",
                         "ado-repos-read", "ado-repos-write", "ado-review", "ado-pipelines",
                         "ado-search", "ado-sprints", "ado-testplans", "confluence", "scwiki",
                         "nexus", "sonar", "web", "messaging")))


def _check(identifier: str, ready: bool, action: str, **details) -> dict:
    return {"id": identifier, "status": "READY" if ready else "INCOMPLETE",
            **details, "next_action": None if ready else action}


def _feature(identifier: str, checks: list[dict], *, configured: bool = True,
             supported: bool = True, limitations: tuple[str, ...] = ()) -> dict:
    status = ("UNSUPPORTED" if not supported else "NOT_CONFIGURED" if not configured else
              "READY" if all(item["status"] == "READY" for item in checks) else "INCOMPLETE")
    return {"id": identifier, "status": status, "checks": checks,
            "integration_access": "UNTESTED", "limitations": list(limitations),
            "next_actions": list(dict.fromkeys(item["next_action"] for item in checks if item["next_action"]))}


def _version(value: str) -> tuple[int, ...] | None:
    if not re.fullmatch(r"\d+(?:\.\d+){0,3}", value):
        return None
    return tuple(int(part) for part in value.split(".")) + (0,) * (4 - len(value.split(".")))


def _distribution(name: str, requirement: str) -> dict:
    try:
        installed = metadata.version(name)
    except (metadata.PackageNotFoundError, ValueError, OSError):
        installed = ""
    actual, expected = _version(installed), _version(requirement[2:])
    ready = actual is not None and expected is not None and (actual == expected if requirement[:2] == "==" else actual >= expected)
    return _check("package:" + name, ready, f'Install {name}{requirement} in the selected Python environment.',
                  package=name, required=requirement, installed=installed if actual else None)


def _executable(name: str, *, minimum: tuple[int, int, int] | None = None) -> dict:
    executable = shutil.which(name)
    found_version = None
    if executable and minimum:
        try:
            result = subprocess.run([executable, "--version"], stdin=subprocess.DEVNULL,
                                    capture_output=True, timeout=5, shell=False,
                                    env={key: value for key, value in os.environ.items() if key.upper() in {
                                        "PATH", "PATHEXT", "SYSTEMROOT", "WINDIR", "HOME", "TMPDIR",
                                        "TEMP", "TMP", "LANG", "LC_ALL"}})
            match = re.fullmatch(rb"v?(\d+)\.(\d+)\.(\d+)\s*", result.stdout[:128])
            if result.returncode == 0 and match:
                found_version = tuple(int(part) for part in match.groups())
        except (OSError, subprocess.SubprocessError, ValueError):
            pass
    ready = bool(executable) and (not minimum or bool(found_version and found_version >= minimum))
    if name == "node" and found_version and found_version[0] == 23:
        ready = False
    action = f"Install {name} and add its executable directory to PATH."
    if minimum:
        action = "Install Node.js 22.12 or later in version 22, or version 24 or later; add it to PATH."
    return _check("executable:" + name, ready, action, executable=name, found=bool(executable),
                  version=".".join(map(str, found_version)) if found_version else None)


def _environment(root: Path) -> tuple[dict[str, str], dict]:
    """Read root dotenv assignments without interpolation, imports, or environment changes."""
    path = root / ".env"
    values = {}
    readable = True
    try:
        if path.exists():
            with path.open("rb") as stream:
                raw = stream.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise ValueError("Environment file exceeds its limit.")
            for line in raw.decode("utf-8-sig").splitlines():
                match = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
                if not match:
                    continue
                name, value = match.groups()
                value = value.strip()
                if value[:1] in {"'", '"'}:
                    end = value.find(value[0], 1)
                    value = value[1:end] if end >= 1 else value
                else:
                    value = value.split("#", 1)[0].rstrip()
                values[name] = value
    except (OSError, UnicodeError, ValueError):
        readable = False
    values.update(os.environ)
    return values, _check("root-environment-file", readable,
                          "Make the workspace .env readable UTF-8 and keep it below one MiB.",
                          exists=path.is_file())


def _variables(names: tuple[str, ...] | list[str], environment: dict) -> list[dict]:
    return [_check("variable:" + name, bool(environment.get(name, "").strip()),
                   f"Set {name} in the workspace .env or the process environment.",
                   variable=name, present=bool(environment.get(name, "").strip())) for name in names]


def _workspace(root: Path) -> tuple[dict, dict]:
    exists = (root / "workspace.yaml").is_file() or (root / "workspace.json").is_file()
    try:
        if not exists:
            return {}, _feature("workspace", [_check("workspace-declaration", False,
                "Run ai-sdlc init PATH in an empty directory, or select an existing workspace.")], configured=False)
        from .workspace import load_workspace
        _, resources = load_workspace(root)
        return resources, _feature("workspace", [_check("workspace-declaration", True, "")])
    except (ImportError, OSError, ValueError, TypeError, RecursionError):
        return {}, _feature("workspace", [_check("workspace-declaration", False,
            "Install core dependencies, then run ai-sdlc --workspace PATH validate.")])


def _connector_source(root: Path, resources: dict) -> Path | None:
    # The Python wheel intentionally excludes the Node connector implementation.
    candidates = []
    for resource in resources.values():
        if resource.provider != "connector.mcp":
            continue
        command = resource.config.get("command", [])
        if isinstance(command, list):
            for argument in command[1:]:
                if isinstance(argument, str) and argument.endswith("bridge.js") and "\x00" not in argument:
                    path = Path(argument).expanduser()
                    candidates.append(path if path.is_absolute() else root / path)
    candidates.extend([root / "core/connectors/workbench/bridge.js",
                       Path(__file__).resolve().parents[1] / "core/connectors/workbench/bridge.js"])
    for bridge in candidates:
        if (bridge.name == "bridge.js" and bridge.parent.name == "workbench" and
                bridge.parent.parent.name == "connectors" and bridge.is_file() and
                (bridge.parents[3] / "package.json").is_file()):
            return bridge.parents[3]
    return None


def _browser() -> dict:
    if sys.platform == "darwin":
        candidates = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                      "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge", "google-chrome", "chromium"]
    elif sys.platform == "win32":
        candidates = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                      r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                      r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
    else:
        candidates = ["google-chrome", "chromium-browser", "microsoft-edge", "chromium"]
    found = any(Path(candidate).is_file() if Path(candidate).is_absolute() else shutil.which(candidate)
                for candidate in candidates)
    return _feature("web.browser", [_check("browser-executable", found,
        "Install Chrome or Edge in a location supported by the web connector.", found=bool(found))],
        limitations=("Browser launch, rendering, and company browser policy remain untested.",
                     "The graph viewer uses a normal browser and does not require this crawler dependency."))


def _grant(resources: dict, connector: str, *, tool: str | None = None) -> dict:
    candidates = [resource for resource in resources.values() if resource.provider == "connector.mcp"
                  and resource.config.get("connector") == connector]
    granted = False
    for resource in candidates:
        tools = resource.config.get("allowed_tools", [])
        if ("call" in resource.allowed_operations and isinstance(tools, list) and tools
                and all(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.-]+", name) for name in tools)
                and len(set(tools)) == len(tools) and (tool is None or tool in tools)):
            granted = True
    action = (f"Grant call and the exact {tool} tool in the {connector} resource after reviewing its operation."
              if tool else f"Grant call and the required exact tool names in the {connector} resource after review.")
    return _check("tool-grants" if not tool else "tool-grant:" + tool, granted, action)


def _node_package(source: Path | None, name: str) -> bool:
    if source is None:
        return False
    location = source / "node_modules" / name
    if name == "cheerio" and not (location / "package.json").is_file():
        location = source / "core/connectors/packages/web/node_modules/cheerio"
    manifest = location / "package.json"
    if not manifest.is_file():
        return False
    if name.startswith("@sc-node-mcp/"):
        try:
            data = json.loads(manifest.read_bytes())
            paths = [data.get("main", "src/index.js")]
            exports = data.get("exports", {})
            if isinstance(exports, dict):
                paths.extend(value for value in exports.values() if isinstance(value, str))
            return all(isinstance(path, str) and (location / path).is_file() for path in paths)
        except (OSError, ValueError, TypeError, AttributeError):
            return False
    return True


def _test_command(command: object, location: Path | None) -> bool:
    if not isinstance(command, list) or not command or not isinstance(command[0], str) or not command[0]:
        return False
    executable = command[0]
    if executable == "{python}":
        return Path(sys.executable).is_file()
    if "/" in executable or "\\" in executable:
        path = Path(executable)
        if not path.is_absolute():
            if location is None:
                return False
            path = location / path
        return path.is_file()
    return shutil.which(executable) is not None


def _connector_command(root: Path, resources: dict, connector: str) -> dict:
    ready = False
    for resource in resources.values():
        if resource.provider != "connector.mcp" or resource.config.get("connector") != connector:
            continue
        command = resource.config.get("command", [])
        if not _test_command(command, root):
            continue
        for argument in command[1:]:
            if isinstance(argument, str) and "\x00" not in argument and argument.endswith("bridge.js"):
                path = Path(argument).expanduser()
                ready = ready or (path if path.is_absolute() else root / path).is_file()
    return _check("connector-command", ready,
                  "Configure an available Node executable and the existing native bridge.js path for this resource.")


def _test_features(root: Path, resources: dict) -> list[dict]:
    features = []
    for resource in resources.values():
        if resource.provider not in {"testing.robot", "testing.command"}:
            continue
        config = resource.config
        location = config.get("path")
        checks = []
        if not isinstance(location, str):
            checks.append(_check("test-repository", False, "Configure the test repository path in registry/tools.yaml."))
        else:
            location = Path(location).expanduser()
            location = location if location.is_absolute() else root / location
            checks.append(_check("test-repository", location.is_dir(), "Restore the configured independent test repository."))
        suites = config.get("suites", {})
        checks.append(_check("registered-suites", isinstance(suites, dict) and bool(suites),
                             "Register named suites in registry/tools.yaml."))
        checks.append(_check("test-operation-grant", "run" in resource.allowed_operations,
                             "Grant run on the test resource after reviewing its registered suites."))
        if resource.provider == "testing.command" and isinstance(suites, dict):
            checks.append(_check("test-command-executables", all(_test_command(command,
                location if isinstance(location, Path) else None) for command in suites.values()),
                "Restore each registered test executable; replace Unix interpreter paths with Windows paths when required."))
        if resource.provider == "testing.robot":
            selected = config.get("python", "")
            same_python = selected == "{python}"
            interpreter = Path(sys.executable) if same_python else Path(selected) if isinstance(selected, str) else Path("")
            if not interpreter.is_absolute() and isinstance(location, Path):
                interpreter = location / interpreter
            checks.append(_check("test-python", interpreter.is_file(),
                                 "Create the configured test environment and select its Python executable.",
                                 interpreter_scope="workbench" if same_python else "independent"))
            if same_python:
                checks.append(_distribution("robotframework", ">=0.0.0"))
            else:
                environment = interpreter.parent.parent
                installed = any(environment.glob("lib/python*/site-packages/robotframework-*.dist-info")) or any(
                    (environment / "Lib/site-packages").glob("robotframework-*.dist-info"))
                checks.append(_check("test-robotframework", installed,
                                     "Install Robot Framework in the configured independent test environment."))
            if isinstance(location, Path) and isinstance(suites, dict):
                checks.append(_check("test-suite-paths", all(isinstance(path, str) and (location / path).exists()
                    for path in suites.values()), "Restore the registered Robot suite files."))
        features.append(_feature("tests:" + resource.id, checks,
            limitations=("Tests and applications were not executed.",
                         "Suite libraries, private variables, and target system access remain untested.")))
    if not features:
        features.append(_feature("tests", [_check("test-resource", False,
            "Register a testing.robot or testing.command resource in registry/tools.yaml.")], configured=False))
    return features


def _desktop_app(name: str) -> bool:
    if sys.platform == "darwin":
        return any((base / ("Microsoft " + name + ".app")).is_dir()
                   for base in (Path("/Applications"), Path.home() / "Applications"))
    if sys.platform == "win32":
        if name == "Outlook":
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Outlook.Application\CLSID"):
                    return True
            except (ImportError, OSError):
                return False
        base = Path(os.environ.get("LOCALAPPDATA", ""))
        return bool(os.environ.get("LOCALAPPDATA")) and (
            (base / "Microsoft/Teams/current/Teams.exe").is_file() or
            any((base / "Packages").glob("MSTeams_*")))
    return False


def _messaging() -> list[dict]:
    supported = sys.platform in {"darwin", "win32"}
    common = []
    if sys.platform == "darwin":
        common.append(_check("osascript", bool(shutil.which("osascript")), "Make the macOS osascript executable available."))
    result = []
    for name in ("Outlook", "Teams"):
        checks = [*common, _check("desktop-app", _desktop_app(name),
                                 f"Install {name} and complete its company sign-in process.")]
        if name == "Outlook" and sys.platform == "win32":
            checks.append(_distribution("pywin32", ">=305"))
        result.append(_feature("messaging." + name.lower(), checks, supported=supported,
        limitations=("Desktop applications were not opened.",
                     "Sign-in state, macOS permissions, and Windows Outlook COM support remain untested.",
                     "Node helpers select Python through PATH; match it to the environment checked here.")))
    return result


def _clinic(root: Path) -> dict:
    checks = [_distribution(name, required) for name, required in CLINIC_REQUIREMENTS.items()]
    try:
        from .release_clinic import _environment as clinic_environment, paths
        environment, locations = clinic_environment(root), paths()
        names = ["ADO_TOKEN", "ADO_ORGANIZATION", "ADO_PROJECT", "USER_EMAIL", "CONFLUENCE_URL",
                 "CONFLUENCE_TOKEN", "SONAR_URL", "SONAR_TOKEN", "GENIE_TOKEN", "GENIE_REPORT_LINK"]
        if environment.get("SNOW_ENABLED", "true").lower() == "true":
            names += ["CLIENT_ID", "FERNET_KEY", "SNOW_BLADE_KEY"]
        checks.extend(_variables(names, environment))
        for name, default in (("TDA_STREAM_CONFIG", locations["scripts"] / "stream_config.yaml"),
                              ("TDA_FIELD_CONFIG", locations["scripts"] / "ado_field_config.yaml"),
                              ("STREAM_CONFIG_FILE", locations["service"] / "service/stream_config.yaml")):
            checks.append(_check("file:" + name, Path(environment.get(name) or default).is_file(),
                                 f"Restore the shipped configuration or correct {name} in the workspace .env."))
    except (ImportError, OSError, ValueError, TypeError):
        checks.append(_check("release-clinic-assets", False,
                             "Install the Release Clinic extra and restore readable workspace configuration."))
    return _feature("release-clinic", checks,
        limitations=("Credential validity, ServiceNow stream overrides, and hosted Vault access remain untested.",))


def _clinic_service(root: Path) -> dict:
    checks = [_distribution(name, CLINIC_REQUIREMENTS[name]) for name in ("fastapi", "uvicorn", "pydantic", "requests")]
    configured = True
    try:
        from .release_clinic import _environment as clinic_environment, paths
        environment = clinic_environment(root, service=True)
        development = environment.get("VAULT_DEV_MODE", "false").strip().lower() == "true"
        names = (["ADO_TOKEN", "SONAR_TOKEN", "GENIE_TOKEN", "CONFLUENCE_TOKEN", "USER_EMAIL"] if development
                 else ["HC_ROLE_ID", "HC_SECRET_ID"])
        configured = development or any(environment.get(name, "").strip() for name in names)
        checks.extend(_variables(names, environment))
        checks.extend(_variables(["CONFLUENCE_URL", "SONAR_URL", "GENIE_REPORT_LINK"], environment))
        checks.append(_check("service-runtime-assets", (paths()["service"] / "service/main.py").is_file(),
                             "Restore the installed Release Clinic service assets."))
        for name in ("VAULT_ADDR", "HC_VAULT_SECRET_PATH") if not development else ():
            if name in environment:
                checks.extend(_variables([name], environment))
    except (ImportError, OSError, ValueError, TypeError):
        checks.append(_check("service-environment", False,
                             "Restore readable Release Clinic service settings; check SERVICE_ENV_FILE when selected."))
    return _feature("release-clinic.service", checks, configured=configured,
        limitations=("The service was not started; Vault authentication and secret paths remain untested.",
                     "The hosted Vault client disables certificate verification and ignores environment proxy settings.",
                     "Use development credentials only within the documented local service mode."))


def doctor(root: str | Path, *, profile: str = "all") -> dict:
    """Return local readiness evidence for the selected workspace and installed runtime."""
    if profile not in {"core", "all"}:
        raise ValueError("Select doctor profile core or all.")
    root = Path(root).expanduser().resolve()
    core = _feature("core", [_check("python", sys.version_info >= (3, 10), "Install Python 3.10 or later.",
        required=">=3.10", installed=platform.python_version()),
        *[_distribution(name, required) for name, required in CORE_REQUIREMENTS.items()]])
    resources, workspace = _workspace(root)
    features = [core, workspace, _feature("git", [_executable("git")])]
    if profile == "all":
        environment, env_check = _environment(root)
        source = _connector_source(root, resources)
        checks = [_executable("node", minimum=(22, 12, 0)),
                  _executable("npm.cmd" if sys.platform == "win32" else "npm"),
                  _check("connector-source", source is not None,
                         "Keep the standalone source checkout and configure its absolute bridge.js path."), env_check]
        for name in NODE_PACKAGES:
            present = _node_package(source, name)
            checks.append(_check("node-package:" + name, present,
                                 "Run setup with a matching offline bundle or approved npm registry access.", package=name))
        connector_feature = _feature("connectors", checks,
            limitations=("The Python wheel does not include the Node connector source or node_modules.",
                         "Package files do not establish successful imports or external access."))
        features.append(connector_feature)
        registered = {resource.config.get("connector") for resource in resources.values() if resource.provider == "connector.mcp"}
        for name, variables in CONNECTOR_VARIABLES.items():
            credential_checks = _variables(variables, environment)
            configured = name in registered or any(item["present"] for item in credential_checks)
            features.append(_feature("connector:" + name,
                [_check("connector-runtime", connector_feature["status"] == "READY",
                        "Resolve the connectors feature prerequisites."),
                 _check("connector-registration", name in registered,
                        f"Register a connector.mcp resource for {name} in registry/tools.yaml."),
                 _connector_command(root, resources, name), _grant(resources, name), *credential_checks], configured=configured,
                 limitations=("Readiness covers configured grants; tool schema discovery and external access remain untested.",)))
        browser = _browser()
        browser["checks"].append(_grant(resources, "web", tool="web_crawl_browser"))
        browser["checks"].append(_check("connector-runtime", connector_feature["status"] == "READY",
                                        "Resolve the connectors feature prerequisites."))
        browser = _feature(browser["id"], browser["checks"], limitations=tuple(browser["limitations"]))
        messaging = _messaging()
        for feature in messaging:
            tool = "email_send" if feature["id"] == "messaging.outlook" else "teams_send_message"
            checks = [*feature["checks"], _grant(resources, "messaging", tool=tool),
                      _check("connector-runtime", connector_feature["status"] == "READY",
                             "Resolve the connectors feature prerequisites.")]
            features.append(_feature(feature["id"], checks, supported=feature["status"] != "UNSUPPORTED",
                                     limitations=tuple(feature["limitations"])))
        features.extend([browser, _clinic(root), _clinic_service(root), *_test_features(root, resources)])
        for identifier in ("app-bridge", "ado-upload-app"):
            features.append(_feature(identifier, [_check("native-workbench-support", False,
                "Use the separately configured package workflow; the native Workbench bridge does not expose this package.")],
                supported=False))
    actions = list(dict.fromkeys(action for feature in features for action in feature["next_actions"]))
    return {"schema_version": 1, "profile": profile, "workspace": str(root),
            "platform": {"system": platform.system(), "machine": platform.machine()},
            "status": "INCOMPLETE" if any(feature["status"] != "READY" for feature in features) else "READY",
            "core_status": "READY" if core["status"] == workspace["status"] == "READY" else "INCOMPLETE",
            "integration_access": "UNTESTED", "features": features,
            "next_actions": actions, "limitations": [
                "Checks inspect local files, package metadata, executable paths, and the Node version only.",
                "No network requests, connector calls, business tests, or desktop application launches were performed.",
                "Installed metadata does not establish compatible native imports or passing business behavior.",
                "Credential values and external command output are excluded from this report.",
                "Proxy routing and TLS trust were not exercised; configure company proxy and certificate settings before integration checks.",
                "Package downloads can use a matching offline bundle; live service operations still require their configured endpoints.",
                "The web crawler disables certificate checks; its browser flags require company review before use.",
                "Generic command tests kill only the parent process after Windows timeouts; child cleanup remains unconfirmed."]}


def main(argv: list[str] | None = None) -> int:
    """Keep dependency diagnosis available when the main CLI cannot import its dependencies."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--profile", choices=("core", "all"), default="all")
    arguments = parser.parse_args(argv)
    result = doctor(arguments.workspace, profile=arguments.profile)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
