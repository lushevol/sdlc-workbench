"""Plan existing test runners and inspect bounded prerequisites without running suites."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict

from .models import Context, WorkbenchError
from .providers.robot import RobotTestingProvider
from .providers.testing import CommandTestingProvider
from .workspace import load_workspace


class PreflightError(WorkbenchError):
    """A plan or prerequisite declaration is invalid."""


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _resource_hash(resource) -> str:
    return _hash(json.dumps(asdict(resource), sort_keys=True, separators=(",", ":")).encode())


def _json(path: Path) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key.")
            result[key] = value
        return result
    try:
        data = path.read_bytes()
        if len(data) > 2 * 1024 * 1024:
            raise ValueError("Oversized declaration.")
        result = json.loads(data, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
        if not isinstance(result, dict):
            raise ValueError("Object required.")
        return result
    except (OSError, ValueError, UnicodeError, RecursionError):
        raise PreflightError("Read a valid JSON object below two MiB for the selected declaration.") from None


def _path(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise PreflightError("Use a nonempty prerequisite path.")
    path = Path(value).expanduser()
    return (path if path.is_absolute() else root / path).resolve()


def _url(value: object) -> str:
    if not isinstance(value, str):
        raise PreflightError("Use an absolute HTTP(S) prerequisite URL without credentials.")
    try:
        parsed = urllib.parse.urlsplit(value)
        valid = parsed.scheme in {"http", "https"} and parsed.hostname and not parsed.username and not parsed.password
        parsed.port
    except ValueError:
        valid = False
    if not valid or parsed.fragment:
        raise PreflightError("Use an absolute HTTP(S) prerequisite URL without credentials.")
    return value


def _safe_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def _sha(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise PreflightError("Use a lowercase SHA-256 fingerprint.")
    return value


def _checks(root: Path, filename: str | None) -> tuple[dict, dict | None]:
    if filename is None:
        return {}, None
    path = _path(root, filename)
    data = _json(path)
    allowed = {"schema_version", "packages", "browser_executable", "authentication_state", "services", "served_assets"}
    if data.get("schema_version") != 1 or set(data) - allowed:
        raise PreflightError("Use test prerequisite schema_version 1 and supported fields.")
    for name in ("packages", "services", "served_assets"):
        if not isinstance(data.get(name, []), list) or len(data.get(name, [])) > 32:
            raise PreflightError("Prerequisite lists must contain at most 32 entries.")
    for name in ("browser_executable", "authentication_state"):
        if name in data:
            _path(root, data[name])
    for entry in data.get("packages", []):
        if not isinstance(entry, dict) or set(entry) - {"path", "version"}:
            raise PreflightError("Package prerequisites need a path and optional exact version.")
        _path(root, entry.get("path"))
        if "version" in entry and not isinstance(entry["version"], str):
            raise PreflightError("A required package version must be text.")
    ids = set()
    for name in ("services", "served_assets"):
        for entry in data.get(name, []):
            required = {"id", "url"} if name == "services" else {"id", "url", "artifact_path", "source_manifest", "source_manifest_sha256"}
            if not isinstance(entry, dict) or set(entry) != required:
                raise PreflightError("A service or served asset prerequisite has invalid fields.")
            if not isinstance(entry["id"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", entry["id"]) or entry["id"] in ids:
                raise PreflightError("Prerequisite IDs must be unique simple names.")
            ids.add(entry["id"])
            _url(entry["url"])
            if name == "served_assets":
                _path(root, entry["artifact_path"])
                _path(root, entry["source_manifest"])
                _sha(entry["source_manifest_sha256"])
    return data, {"path": str(path), "sha256": _hash(path.read_bytes())}


def _environment(root: Path, name: str | None, filename: str | None) -> tuple[dict | None, dict | None]:
    if name is None:
        if filename is not None:
            raise PreflightError("An environment file requires an environment name.")
        return None, None
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", name):
        raise PreflightError("Use a simple environment name.")
    path = _path(root, filename or ".workbench/e2e-environments.json")
    catalog = _json(path)
    if set(catalog) - {"schemaVersion", "environments"} or catalog.get("schemaVersion", 1) != 1 or not isinstance(catalog.get("environments"), dict):
        raise PreflightError("Use the existing schemaVersion 1 environment catalog.")
    target = catalog["environments"].get(name)
    allowed = {"targetUrl", "prefix", "area", "storageState", "workspaceName", "refreshCredentialSha256"}
    if not isinstance(target, dict) or set(target) - allowed or not isinstance(target.get("prefix"), str) or not target["prefix"]:
        raise PreflightError("Select an existing environment with a targetUrl and prefix.")
    _url(target.get("targetUrl"))
    if target.get("area", "login") not in {"login", "portal", "category"}:
        raise PreflightError("Select a supported target area.")
    summary = {"name": name, "target_url": _safe_url(target["targetUrl"]), "area": target.get("area", "login")}
    if "storageState" in target:
        summary["authentication_state"] = str(_path(path.parent, target["storageState"]))
    return summary, {"path": str(path), "sha256": _hash(path.read_bytes())}


def plan_test_execution(root: Path, *, runner: str = "registered", resource_id: str | None = None,
                        suite: str, environment: str | None = None, environments_file: str | None = None,
                        output_dir: str | None = None, checks_file: str | None = None) -> dict:
    """Resolve exact existing runner commands; perform no subprocess or network operation."""
    root = Path(root).resolve()
    output_name = re.sub(r"[^A-Za-z0-9_.-]", "-", suite)
    output = _path(root, output_dir or f".workbench/test-execution/{output_name}")
    checks, checks_binding = _checks(root, checks_file)
    target, environment_binding = _environment(root, environment, environments_file)
    invocation_environment = {}
    sources = []
    resource_binding = None
    granted = True
    if runner == "registered":
        if environment is not None:
            raise PreflightError("Registered suites retain their configured environment; named UI targets use the playwright runner.")
        _, resources = load_workspace(root)
        resource = resources.get(resource_id)
        if resource is None or resource.provider not in {"testing.command", "testing.robot"}:
            raise PreflightError("Select a registered testing.command or testing.robot resource.")
        granted = "run" in resource.allowed_operations
        resource_binding = {"id": resource.id, "sha256": _resource_hash(resource)}
        cwd = _path(root, resource.config.get("path"))
        if resource.provider == "testing.command":
            suites = CommandTestingProvider()._suites(resource)
            if suite not in suites:
                raise PreflightError("The resource does not register the selected suite.")
            command = [sys.executable if value == "{python}" else value for value in suites[suite]]
        else:
            cwd, interpreter, suites, variable_files = RobotTestingProvider()._configuration(resource, Context(root, output))
            if suite not in suites:
                raise PreflightError("The resource does not register the selected suite.")
            python = Path(sys.executable) if interpreter == "{python}" else Path(interpreter)
            if not python.is_absolute():
                python = cwd / python
            command = [str(python), "-m", "robot", "--outputdir", str(output / "robot")]
            for variable_file in variable_files:
                command.extend(["--variablefile", str(variable_file)])
            command.append(str(suites[suite]))
            sources.extend({"path": str(cwd / source["path"]), "sha256": source["sha256"]}
                           for source in RobotTestingProvider._suite_sources(cwd, suites[suite]))
        target = {"name": resource.environment, "target_url": None, "area": None}
        provider = resource.provider
    elif runner == "playwright":
        if resource_id is not None or suite not in {"e2e:test", "e2e:remote", "e2e:ai"}:
            raise PreflightError("Select an existing e2e:test, e2e:remote, or e2e:ai npm script.")
        if (suite == "e2e:remote") != (environment is not None):
            raise PreflightError("Use a named environment only with e2e:remote.")
        manifest = _json(root / "package.json")
        script = manifest.get("scripts", {}).get(suite)
        if not isinstance(script, str) or not script:
            raise PreflightError("The selected workspace has no matching npm runner script.")
        command = ["npm.cmd" if os.name == "nt" else "npm", "run", suite, "--"]
        command.extend(["validate"] if suite == "e2e:ai" else ["--output", str(output / "playwright-artifacts")])
        invocation_environment = {"E2E_ENVIRONMENT": None, "E2E_ENVIRONMENTS_FILE": None}
        if environment is not None:
            invocation_environment = {"E2E_ENVIRONMENT": environment, "E2E_ENVIRONMENTS_FILE": environment_binding["path"], "E2E_AUDIT_OUTPUT": str(output)}
        sources.append({"path": str(root / "package.json"), "sha256": _hash((root / "package.json").read_bytes())})
        for name in ("e2e/browser-config.ts", "e2e/support/environment.ts",
                     "e2e/remote.config.ts" if environment else "e2e/playwright.config.ts"):
            path = root / name
            if path.is_file():
                sources.append({"path": str(path), "sha256": _hash(path.read_bytes())})
        if not checks.get("packages"):
            checks["packages"] = [{"path": f"node_modules/{name}/package.json", "version": manifest.get("devDependencies", {}).get(name)} for name in ("@playwright/test", "tsx")]
            if any(not isinstance(item["version"], str) or not item["version"] for item in checks["packages"]):
                raise PreflightError("Declare required Playwright and tsx package versions in devDependencies or prerequisite checks.")
        provider, cwd = "playwright.npm", root
    else:
        raise PreflightError("Choose registered or playwright runner.")
    public_checks = dict(checks)
    for name in ("services", "served_assets"):
        if name in public_checks:
            public_checks[name] = [{**entry, "url": _safe_url(entry["url"])} for entry in checks[name]]
    return {"schema_version": 1, "status": "PLANNED", "runner": runner, "provider": provider,
            "resource_id": resource_id, "suite": suite, "command": command, "cwd": str(cwd),
            "output_dir": str(output), "run_granted": granted, "environment": target,
            "invocation_environment": invocation_environment, "environment_binding": environment_binding,
            "checks_binding": checks_binding, "resource_binding": resource_binding, "checks": public_checks, "sources": sources,
            "suite_executed": False, "limitations": ["Planning does not execute commands, read credential values, or contact target services.",
            "Configured source and environment declarations do not establish served build identity."]}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _get(url: str, limit: int) -> bytes:
    opener = urllib.request.build_opener(_NoRedirect())
    with opener.open(urllib.request.Request(_url(url), method="GET"), timeout=3) as response:
        if response.status != 200:
            raise ValueError("Unexpected HTTP status.")
        result = response.read(limit + 1)
        if len(result) > limit:
            raise ValueError("Response exceeds the declared limit.")
        return result


def _browser(root: Path) -> Path | None:
    selected = os.environ.get("E2E_BROWSER", "chromium")
    if selected == "msedge":
        candidates = [Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
                      Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
                      Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")]
        found = shutil.which("msedge") or shutil.which("microsoft-edge")
        return next((p for p in candidates if p.is_file()), Path(found) if found else None)
    if selected != "chromium":
        raise PreflightError("E2E_BROWSER must be chromium or msedge.")
    declaration = root / "node_modules/playwright-core/browsers.json"
    if not declaration.is_file():
        return None
    chromium = next((b for b in _json(declaration).get("browsers", []) if b.get("name") == "chromium"), None)
    if not chromium:
        return None
    cache = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", str(root / "adapters/browser/.browsers")))
    if str(cache) == "0":
        cache = root / "node_modules/playwright-core/.local-browsers"
    elif not cache.is_absolute():
        cache = root / cache
    folder = cache / ("chromium-" + chromium["revision"])
    if sys.platform == "darwin":
        relative = f"chrome-mac{'-arm64' if platform.machine() == 'arm64' else ''}/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    elif os.name == "nt":
        relative = "chrome-win64/chrome.exe"
    else:
        relative = "chrome-linux64/chrome"
    return folder / relative


def _asset_binding(root: Path, asset: dict) -> tuple[Path, str]:
    manifest_path = _path(root, asset["source_manifest"])
    if _hash(manifest_path.read_bytes()) != _sha(asset["source_manifest_sha256"]):
        raise PreflightError("The source manifest changed after its declaration.")
    manifest = _json(manifest_path)
    sources, artifacts = manifest.get("sources"), manifest.get("artifacts")
    if manifest.get("schema_version") != 1 or not isinstance(sources, list) or not 1 <= len(sources) <= 512 or not isinstance(artifacts, list) or not 1 <= len(artifacts) <= 128:
        raise PreflightError("A served asset needs a source-bound manifest with sources and artifacts.")
    for source in sources:
        path = _path(root, source.get("path"))
        if _hash(path.read_bytes()) != _sha(source.get("sha256")):
            raise PreflightError("A declared build source has changed.")
        revision = source.get("revision")
        if revision is not None and (not isinstance(revision, str) or not re.fullmatch(r"[a-f0-9]{40}|[a-f0-9]{64}", revision)):
            raise PreflightError("Source revisions require complete Git object IDs or null.")
    path = _path(root, asset["artifact_path"])
    match = [item for item in artifacts if _path(root, item.get("path")) == path]
    if len(match) != 1:
        raise PreflightError("The manifest must bind the selected artifact exactly once.")
    expected = _sha(match[0].get("sha256"))
    if _hash(path.read_bytes()) != expected:
        raise PreflightError("The declared built artifact has changed.")
    return path, expected


def preflight_test_execution(plan: dict, root: Path, *, probe_services: bool = False) -> dict:
    """Inspect plan prerequisites; optional GET probes never launch a test or service."""
    root = Path(root).resolve()
    if not isinstance(plan, dict) or plan.get("schema_version") != 1 or plan.get("status") != "PLANNED":
        raise PreflightError("Use a schema_version 1 test execution plan.")
    checks = plan.get("checks", {})
    resource_binding = plan.get("resource_binding")
    if resource_binding:
        _, resources = load_workspace(root)
        resource = resources.get(resource_binding.get("id"))
        if resource is None or _resource_hash(resource) != resource_binding.get("sha256"):
            raise PreflightError("The selected resource changed; create a fresh plan.")
    # Recheck retained configuration identities before relying on their contents.
    for name in ("checks_binding", "environment_binding"):
        binding = plan.get(name)
        if binding and _hash(_path(root, binding["path"]).read_bytes()) != _sha(binding["sha256"]):
            raise PreflightError("A selected plan declaration changed; create a fresh plan.")
    checks_binding = plan.get("checks_binding")
    if checks_binding:
        # Serializable plans omit private URL queries. Reload requests only from their checked declaration.
        private_checks, current_binding = _checks(root, checks_binding["path"])
        if current_binding != checks_binding:
            raise PreflightError("A selected plan declaration changed; create a fresh plan.")
        checks = {**checks, **private_checks}
        if not private_checks.get("packages") and plan.get("checks", {}).get("packages"):
            checks["packages"] = plan["checks"]["packages"]
    rows = []
    def record(identifier, status, action=None, **details):
        rows.append({"id": identifier, "status": status, **details, "next_action": action if status != "READY" else None})
    record("execution-grant", "READY" if plan.get("run_granted") else "FAILED", "Review the selected resource's run grant.")
    cwd = _path(root, plan.get("cwd"))
    record("working-directory", "READY" if cwd.is_dir() else "FAILED", "Restore the selected runner directory.")
    command = plan.get("command", [])
    if not isinstance(command, list) or not command or not isinstance(command[0], str):
        raise PreflightError("The plan requires a runner command.")
    executable = command[0]
    found = _path(cwd, executable).is_file() if "/" in executable or "\\" in executable else shutil.which(executable) is not None
    record("runner-executable", "READY" if found else "FAILED", "Restore the selected runner executable.")
    for source in plan.get("sources", []):
        path = _path(root, source["path"])
        current = path.is_file() and source.get("sha256") == _hash(path.read_bytes())
        record("source:" + str(path), "READY" if current else "FAILED", "Create a fresh plan for the changed runner source.")
    if plan.get("provider") == "testing.robot":
        interpreter = Path(executable)
        if not interpreter.is_absolute():
            interpreter = cwd / interpreter
        environment_root = interpreter.parent.parent
        installed = any(environment_root.glob("lib/python*/site-packages/robotframework-*.dist-info")) or any(
            (environment_root / "Lib/site-packages").glob("robotframework-*.dist-info"))
        record("robot-framework", "READY" if installed else "FAILED", "Install Robot Framework in the selected interpreter environment.")
    for entry in checks.get("packages", []):
        path = _path(root, entry["path"])
        try:
            package = _json(path)
            installed = package.get("version")
            ready = bool(installed) and (not entry.get("version") or installed == entry["version"])
        except PreflightError:
            installed, ready = None, False
        record("package:" + str(path), "READY" if ready else "FAILED", "Install the declared package version from the prepared environment.", installed=installed, required=entry.get("version"))
    if plan.get("runner") == "playwright" or checks.get("browser_executable"):
        browser = _path(root, checks["browser_executable"]) if checks.get("browser_executable") else _browser(root)
        record("browser-asset", "READY" if browser and browser.is_file() else "FAILED", "Provision the selected browser explicitly.", executable=str(browser) if browser else None)
    target = plan.get("environment") or {}
    state = checks.get("authentication_state") or target.get("authentication_state")
    if state:
        path = _path(root, state)
        present = path.is_file() and path.stat().st_size > 0
        record("authentication-state", "READY" if present else "FAILED", "Prepare valid authorized authentication state for the selected target.", present=present, content_inspected=False)
    elif target.get("area") in {"portal", "category"}:
        record("authentication-state", "UNKNOWN", "Declare authorized authentication state or establish the target's supported authentication setup.", content_inspected=False)
    for service in checks.get("services", []):
        status = "NOT_PROBED"
        if probe_services:
            try:
                _get(service["url"], 1024 * 1024)
                status = "READY"
            except (OSError, ValueError):
                status = "FAILED"
        record("service:" + service["id"], status, "Start the declared service or inspect its readiness endpoint.", url=_safe_url(service["url"]))
    assets = []
    for asset in checks.get("served_assets", []):
        row = {"id": asset["id"], "url": _safe_url(asset["url"]), "status": "NOT_PROBED", "actual_sha256": None, "expected_sha256": None}
        try:
            _, expected = _asset_binding(root, asset)
            row["expected_sha256"] = expected
            if probe_services:
                try:
                    row["actual_sha256"] = _hash(_get(asset["url"], 16 * 1024 * 1024))
                    row["status"] = "READY" if row["actual_sha256"] == expected else "MISMATCH"
                except (OSError, ValueError):
                    row["status"] = "UNAVAILABLE"
        except (OSError, ValueError, AttributeError, TypeError):
            row["status"] = "INVALID_BINDING"
        assets.append(row)
        record("served-asset:" + asset["id"], row["status"], "Restore the source-bound artifact or select the correct served build.")
    identity = ("MATCHED" if assets and all(a["status"] == "READY" for a in assets) else
                "MISMATCH" if any(a["status"] == "MISMATCH" for a in assets) else
                "UNKNOWN" if assets or target.get("target_url") or checks.get("services") else "NOT_APPLICABLE")
    if identity == "UNKNOWN" and not assets:
        record("served-build-identity", "UNKNOWN", "Declare a supported served-asset fingerprint and its source-bound manifest.")
    return {"schema_version": 1, "status": "READY" if all(r["status"] == "READY" for r in rows) else "INCOMPLETE",
            "plan": {key: plan.get(key) for key in ("runner", "provider", "resource_id", "suite", "command", "cwd", "output_dir", "environment", "invocation_environment", "sources")},
            "checks": rows, "served_assets": assets, "build_identity": identity,
            "network_probed": probe_services, "suite_executed": False, "product_behavior": "NOT_EXECUTED",
            "limitations": ["Prerequisite presence does not prove browser launch, authenticated session validity, or passing business behavior.",
            "Matched asset bytes bind only the declared artifacts and source fingerprints; they do not authenticate the build process or prove deployment parity.",
            "Source revision labels remain declarations; this preflight does not fetch or attest repository history.",
            "HTTP probes use bounded GET requests without redirects; response bodies and credential values are not retained."]}
