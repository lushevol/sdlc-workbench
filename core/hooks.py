"""Bounded native-client context and advisory checks for an explicitly selected scope."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

from .assurance import _json, _read, local_path
from .hook_install import _atomic
from .models import WorkbenchError


CLIENTS = ("codex", "copilot", "claude")
MAX_INPUT = 1024 * 1024
CHECK_TIMEOUT = 10
_MAX_FILE = 8 * 1024 * 1024
_LISTS = ("artifacts", "cases", "watch")
_LIMIT = "Deterministic checks do not establish business verification, readiness, or publication approval."


def _identity(client, session):
    if (client not in CLIENTS or not isinstance(session, str) or not session
            or len(session) > 256 or any(ord(character) < 32 for character in session)):
        raise WorkbenchError("Select a supported hook client and a nonempty native session ID of at most 256 characters.")
    return hashlib.sha256((client + "\0" + session).encode("utf-8")).hexdigest()


def _root(value):
    root = Path(value).expanduser().resolve()
    if not any((root / name).is_file() for name in ("workspace.yaml", "workspace.json")):
        raise WorkbenchError("Select the Workbench workspace explicitly with --workspace.")
    return root


def _path(root, value, *, exists=False):
    if (not isinstance(value, str) or len(value) > 1024
            or any(ord(character) < 32 for character in value)):
        raise WorkbenchError("Hook inputs require bounded workspace-relative file paths without control characters.")
    path = local_path(root, value)
    if path.exists() and not path.is_file():
        raise WorkbenchError("Hook scope inputs must be regular files, not directories.")
    if exists and not path.is_file():
        raise WorkbenchError("Select existing regular files for the hook scope.")
    return path


def _state_path(root, client, session):
    return local_path(root, ".workbench/hooks/sessions/" + _identity(client, session) + ".json")


@contextmanager
def _lock(root, client, session):
    path = local_path(root, ".workbench/hooks/sessions/" + _identity(client, session) + ".lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        if os.name == "nt":
            import msvcrt
            if stream.tell() == 0:
                stream.write(b"\0")
                stream.flush()
            stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                raise WorkbenchError("A hook check for this client session is already running; no duplicate check was started.") from None
        else:
            import fcntl
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise WorkbenchError("A hook check for this client session is already running; no duplicate check was started.") from None
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def _scope(root, value, *, exists=False):
    if (not isinstance(value, dict) or set(value) != {"record", "index", "baseline", *_LISTS}
            or not isinstance(value["record"], str)):
        raise WorkbenchError("The hook scope binding is invalid; bind the session again.")
    paths = [value["record"]]
    for field in ("index", "baseline"):
        if value[field] is not None:
            paths.append(value[field])
    for field in _LISTS:
        if not isinstance(value[field], list) or len(value[field]) > 32:
            raise WorkbenchError("Use at most 32 files per hook scope list.")
        paths.extend(value[field])
    if len(paths) > 64:
        raise WorkbenchError("Use at most 64 explicitly selected hook input files.")
    for value in paths:
        _path(root, value, exists=exists)
    return sorted(set(paths))


def _fingerprint(root, scope):
    from .context.catalogs import read_declaration
    configuration = ["workspace.yaml", "workspace.json", "workspace.local.yaml"]
    try:
        declaration = read_declaration(root / ("workspace.yaml" if (root / "workspace.yaml").exists() else "workspace.json"))
        registries = declaration.get("registries", {})
        if isinstance(registries, dict):
            configuration.extend(value for value in registries.values() if isinstance(value, str))
    except (OSError, ValueError, WorkbenchError):
        pass  # Changed invalid declaration bytes still invalidate the check and reach workspace validation.
    hashes = {}
    total = 0
    for value in sorted(set([*_scope(root, scope), *configuration])):
        path = _path(root, value)
        if not path.exists():
            hashes[value] = None
            continue
        with path.open("rb") as stream:
            raw = stream.read(_MAX_FILE + 1)
        total += len(raw)
        if len(raw) > _MAX_FILE or total > 32 * 1024 * 1024:
            raise WorkbenchError("Hook inputs exceed the bounded check size; select smaller files or run ordinary validation directly.")
        hashes[value] = hashlib.sha256(raw).hexdigest()
    runtime = Path(__file__).parent
    recipe = hashlib.sha256()
    for pattern in ("*.py", "context/*.py", "governance/*.py", "schemas/*.json", "knowledge/schemas/*.json"):
        for path in sorted(runtime.glob(pattern)):
            recipe.update(path.relative_to(runtime).as_posix().encode("utf-8"))
            recipe.update(path.read_bytes())
    return hashlib.sha256(json.dumps({"scope": scope, "files": hashes, "recipe": recipe.hexdigest()},
                                     sort_keys=True).encode("utf-8")).hexdigest()


def _load(root, client, session):
    path = _state_path(root, client, session)
    if not path.exists():
        return None
    try:
        state = _json(_read(path))
        if (state.get("schema_version") != 1 or state.get("client") != client
                or state.get("session") != session or not isinstance(state.get("fingerprint"), str)):
            raise ValueError
        _scope(root, state.get("scope"))
        return state
    except (ValueError, UnicodeError, RecursionError):
        raise WorkbenchError("The hook session state is invalid; clear and bind the session again.") from None


def _save(root, client, session, state):
    _atomic(_state_path(root, client, session),
            (json.dumps(state, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8"))


def bind_scope(root, client, session, record, *, index=None, baseline=None, artifacts=(), cases=(), watch=()):
    """Bind existing file pointers and their starting hashes; never infer a task or readiness state."""
    root = _root(root)
    _identity(client, session)
    scope = {"record": record, "index": index, "baseline": baseline,
             "artifacts": list(artifacts), "cases": list(cases), "watch": list(watch)}
    _scope(root, scope, exists=True)
    with _lock(root, client, session):
        state = {"schema_version": 1, "client": client, "session": session, "scope": scope,
                 "fingerprint": _fingerprint(root, scope), "last_result": None}
        _save(root, client, session, state)
    return {"status": "BOUND", "client": client, "session": session, "scope": scope,
            "note": "Bind before edits. Add --watch for indirect source, assertion, and intent dependencies. " + _LIMIT}


def clear_scope(root, client, session):
    root = _root(root)
    with _lock(root, client, session):
        _state_path(root, client, session).unlink(missing_ok=True)
    return {"status": "CLEARED", "client": client, "session": session}


def _native(client, context):
    if client == "copilot":
        return {"additionalContext": context}
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}


def advisory(client, message):
    """Report feedback without requesting continuation; Copilot's Stop warning exit differs from Claude's."""
    message = "Workbench hooks: " + message
    return ({}, message, 2) if client == "copilot" else ({"systemMessage": message}, "", 0)


def _checks(scope):
    checks = [("workspace (whole workspace; findings are not attributed to this task)", ["validate"])]
    if scope["artifacts"]:
        checks.append(("artifacts", ["lint", "--", *scope["artifacts"]]))
    if scope["cases"]:
        checks.append(("cases", ["gherkin", "--", *scope["cases"]]))
    if scope["index"]:
        checks.append(("index", ["assurance", "index", "--input", scope["index"], "--require-current"]))
    if scope["baseline"]:
        checks.append(("baseline", ["assurance", "validate", "--baseline", scope["baseline"], "--require-current"]))
    return checks


def _run_checks(root, scope):
    results = []
    deadline = time.monotonic() + CHECK_TIMEOUT
    for name, arguments in _checks(scope):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            results.append({"check": name, "status": "NOT_RUN", "reason": "check budget exhausted"})
            continue
        try:
            result = subprocess.run([sys.executable, "-m", "ai_sdlc_workbench", "--workspace", str(root), *arguments],
                                    stdin=subprocess.DEVNULL, cwd=root, capture_output=True, text=True,
                                    timeout=remaining, shell=False)
            try:
                payload = _json(result.stdout.encode("utf-8"))
            except (ValueError, UnicodeError, RecursionError):
                payload = {}
            diagnostics = payload.get("findings", payload.get("diagnostics", []))
            findings = []
            if isinstance(diagnostics, list):
                for item in diagnostics[:20]:
                    if isinstance(item, dict):
                        findings.append({key: str(item[key])[:160] for key in ("code", "path", "record_id") if key in item})
            results.append({"check": name, "status": "PASSED" if result.returncode == 0 and payload else "FAILED",
                            "exit_code": result.returncode, "findings": findings})
        except subprocess.TimeoutExpired:
            results.append({"check": name, "status": "NOT_RUN", "reason": "check timeout"})
        except OSError:
            results.append({"check": name, "status": "NOT_RUN", "reason": "validator process unavailable"})
    return results


def run_hook(root, client, event, payload):
    """Translate the native contract and perform only explicitly scoped local checks."""
    root = _root(root)
    if client not in CLIENTS or event not in {"start", "stop"} or not isinstance(payload, dict):
        raise WorkbenchError("Select a supported hook client, start or stop event, and a JSON object payload.")
    session = payload.get("sessionId") if client == "copilot" and "sessionId" in payload else payload.get("session_id")
    _identity(client, session)
    if "stop_hook_active" in payload and type(payload["stop_hook_active"]) is not bool:
        raise WorkbenchError("The native stop continuation flag must be a boolean.")
    expected = "SessionStart" if event == "start" else "Stop"
    if payload.get("hook_event_name", expected) != expected:
        raise WorkbenchError("The native hook event does not match the configured handler.")
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not Path(cwd).is_absolute() or not Path(cwd).resolve().is_relative_to(root):
        raise WorkbenchError("The hook working directory must be inside the explicitly selected workspace.")
    if payload.get("agent_id") or payload.get("agentId") or payload.get("parentAgentId"):
        return {}, "", 0
    if event == "start":
        state = _load(root, client, session)
        argv = [sys.executable, "-m", "ai_sdlc_workbench", "--workspace", str(root), "hooks", "bind", "--client", client,
                "--session", session, "--record", "PATH_TO_LIVING_RECORD"]
        command = ("& " + " ".join("'" + value.replace("'", "''") + "'" for value in argv)
                   if sys.platform == "win32" else shlex.join(argv))
        lines = ["Workbench workspace: " + str(root), "Native hook client/session: " + client + "/" + session]
        if state:
            lines += ["Declared living record: " + state["scope"]["record"],
                      "Next check: inspect this record and its sources; completion checks run after declared inputs change."]
        else:
            lines += ["No task or collection is bound. Reuse tasks/README.md or .agents/skills/manage-knowledge-lifecycle/SKILL.md.",
                      "Before scoped edits, bind the existing living record: " + command]
        lines.append("Reuse existing authorization and recorded answers. " + _LIMIT)
        return _native(client, "\n".join(lines)[:2000]), "", 0
    if payload.get("stop_hook_active"):
        return {}, "", 0
    if _load(root, client, session) is None:
        return {}, "", 0
    with _lock(root, client, session):
        state = _load(root, client, session)
        if state is None:
            return {}, "", 0
        fingerprint = _fingerprint(root, state["scope"])
        if fingerprint == state["fingerprint"]:
            return {}, "", 0
        missing = [value for value in _scope(root, state["scope"]) if not _path(root, value).is_file()]
        results = ([{"check": "scope", "status": "FAILED", "findings": [{"code": "MISSING_INPUT", "path": value}
                    for value in missing]}] if missing else _run_checks(root, state["scope"]))
        changed = _fingerprint(root, state["scope"]) != fingerprint
        if changed:
            results.append({"check": "inputs", "status": "NOT_RUN", "reason": "inputs changed during validation"})
        status = "CHECKS_PASSED" if all(item["status"] == "PASSED" for item in results) else "ACTION_REQUIRED"
        state["last_result"] = {"status": status, "checks": results, "verification": "NOT_VERIFIED"}
        if not changed and all(item["status"] != "NOT_RUN" for item in results):
            state["fingerprint"] = fingerprint
        _save(root, client, session, state)
        if status == "CHECKS_PASSED":
            return {}, "", 0
        failed = "; ".join(item["check"] + ": " + item["status"] for item in results if item["status"] != "PASSED")
        location = _state_path(root, client, session).relative_to(root).as_posix()
        return advisory(client, failed + ". Details: " + location + ". " + _LIMIT)
