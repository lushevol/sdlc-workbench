"""Install project hook registrations without replacing unrelated client settings."""

from __future__ import annotations

import base64
from contextlib import contextmanager
import copy
import json
import os
from pathlib import Path
import shlex
import stat
import sys
import tempfile

from .assurance import _json, _read, local_path
from .models import WorkbenchError
from .workspace import load_workspace


CONFIGS = {
    "codex": ".codex/hooks.json",
    "copilot": ".github/hooks/workbench.json",
    # Copilot imports ordinary Claude settings; an explicit settings file avoids double registration.
    "claude": ".claude/workbench-hooks.json",
}
_STATE = ".workbench/hooks/installation.json"
_LOCK = ".workbench/hooks/installation.lock"


def _clients(clients):
    selected = list(CONFIGS) if clients is None else [clients] if isinstance(clients, str) else list(clients)
    if not selected or any(client not in CONFIGS for client in selected):
        raise WorkbenchError("Select codex, copilot, or claude hook clients.")
    return list(dict.fromkeys(selected))


def _registrations(client, root, executable):
    result = {}
    for event, native in (("start", "sessionStart" if client == "copilot" else "SessionStart"),
                          ("stop", "agentStop" if client == "copilot" else "Stop")):
        arguments = ["-m", "ai_sdlc_workbench", "--workspace", str(root), "hooks", "run",
                     "--client", client, "--event", event]
        if client == "copilot":
            handler = {"type": "command", "exec": executable, "args": arguments, "timeoutSec": 15}
        elif client == "claude":
            handler = {"type": "command", "command": executable, "args": arguments, "timeout": 15}
        else:
            argv = [executable, *arguments]
            script = "& " + " ".join("'" + value.replace("'", "''") + "'" for value in argv) + "; exit $LASTEXITCODE"
            encoded = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
            handler = {"type": "command", "command": shlex.join(argv),
                       "commandWindows": "powershell.exe -NoProfile -NonInteractive -EncodedCommand " + encoded,
                       "timeout": 15}
        result[native] = handler if client == "copilot" else {"hooks": [handler]}
    return result


def _document(root, relative):
    path = local_path(root, relative)
    if not path.exists():
        return {}, None
    try:
        raw = _read(path)
        return _json(raw), raw
    except (OSError, ValueError, UnicodeError, RecursionError, WorkbenchError):
        raise WorkbenchError(f"Select a regular hook configuration containing strict JSON: {relative}") from None


def _state(root):
    state, raw = _document(root, _STATE)
    if raw is None:
        return {"schema_version": 1, "clients": {}}, None
    if (type(state.get("schema_version")) is not int or state["schema_version"] != 1 or not isinstance(state.get("clients"), dict)
            or set(state["clients"]) - CONFIGS.keys()):
        raise WorkbenchError("The Workbench hook installation record is invalid.")
    for client, record in state["clients"].items():
        if (not isinstance(record, dict) or set(record) != {"python", "workspace", "created", "had_hooks"}
                or not isinstance(record["python"], str) or not Path(record["python"]).is_absolute()
                or not isinstance(record["workspace"], str) or not Path(record["workspace"]).is_absolute()
                or type(record["created"]) is not bool or type(record["had_hooks"]) is not bool):
            raise WorkbenchError("The Workbench hook installation record is invalid.")
    return state, raw


def _hook_map(document, client):
    if client == "copilot" and document and document.get("version") != 1:
        raise WorkbenchError("The Copilot Workbench hook file must use version 1.")
    hooks = document.get("hooks", {})
    if (not isinstance(hooks, dict)
            or any(not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries)
                   for entries in hooks.values())):
        raise WorkbenchError("Hook events must map to arrays of handlers.")
    return hooks


def _remove_owned(document, client, record, *, missing=False):
    hooks = _hook_map(document, client)
    if missing:
        return
    for event, entry in _registrations(client, record["workspace"], record["python"]).items():
        entries = hooks.get(event, [])
        if entries.count(entry) != 1:
            raise WorkbenchError(f"Workbench {client} hooks changed after installation; preserve and reconcile them before updating or removing.")
        entries.remove(entry)
        if not entries:
            hooks.pop(event)
    if not hooks and not record["had_hooks"]:
        document.pop("hooks", None)


def _bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _current(path):
    if not path.exists():
        return None
    return _read(path)


def _atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".workbench-hook-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(mode)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


@contextmanager
def _lock(root):
    path = local_path(root, _LOCK)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        stream = path.open("x")
    except FileExistsError:
        raise WorkbenchError("Another hook installation holds the workspace lock; retry after it finishes.") from None
    try:
        stream.close()
        yield
    finally:
        path.unlink(missing_ok=True)


def _transaction(root, originals, updates):
    for relative, original in originals.items():
        if _current(local_path(root, relative)) != original:
            raise WorkbenchError("Hook configuration changed during planning; retry without overwriting it.")
    changed = []
    try:
        for relative, value in updates.items():
            path = local_path(root, relative)
            if _current(path) != originals[relative]:
                raise WorkbenchError("Hook configuration changed during installation; retry without overwriting it.")
            if value == originals[relative]:
                continue
            if value is None:
                path.unlink()
            else:
                _atomic(path, value)
            changed.append(relative)
    except (OSError, ValueError, WorkbenchError) as error:
        conflicts = []
        for relative in reversed(changed):
            try:
                path = local_path(root, relative)
                if _current(path) != updates[relative]:
                    conflicts.append(relative)
                elif originals[relative] is None:
                    path.unlink()
                else:
                    _atomic(path, originals[relative])
            except (OSError, ValueError, WorkbenchError):
                conflicts.append(relative)
        if conflicts:
            raise WorkbenchError("Hook installation failed; preserve and reconcile recovery conflicts: " + ", ".join(conflicts)) from None
        raise WorkbenchError("Hook installation failed; previous configuration bytes were restored.") from error


def install_hooks(root: Path, clients=None, python: str | Path | None = None) -> dict:
    """Merge two project registrations per selected client; preserve all unrelated entries."""
    root = Path(root).expanduser().resolve()
    selected = _clients(clients)
    executable = Path(python or sys.executable).expanduser().absolute()
    if not root.is_dir() or not executable.is_file() or not os.access(executable, os.X_OK):
        raise WorkbenchError("Select an existing workspace and installed Python executable.")
    load_workspace(root)
    with _lock(root):
        state, state_raw = _state(root)
        updated = copy.deepcopy(state)
        originals, updates = {_STATE: state_raw}, {}
        for client in selected:
            relative = CONFIGS[client]
            document, raw = _document(root, relative)
            hooks = _hook_map(document, client)
            record = state["clients"].get(client)
            if record:
                _remove_owned(document, client, record, missing=raw is None)
            elif client in {"copilot", "claude"} and raw is not None:
                raise WorkbenchError(f"Preserve the existing {relative}; it is not owned by this installation.")
            new_record = {"python": str(executable), "workspace": str(root),
                          "created": raw is None or (record["created"] if record else False),
                          "had_hooks": False if raw is None else record["had_hooks"] if record else "hooks" in document}
            if client == "copilot":
                document["version"] = 1
            hooks = document.setdefault("hooks", {})
            for event, entry in _registrations(client, root, str(executable)).items():
                if entry in hooks.get(event, []):
                    raise WorkbenchError(f"An identical {client} hook is not owned by this installation; reconcile it before installing.")
                hooks.setdefault(event, []).append(entry)
            updated["clients"][client] = new_record
            originals[relative], updates[relative] = raw, _bytes(document)
        updates[_STATE] = _bytes(updated)
        _transaction(root, originals, updates)
    return hook_status(root)


def remove_hooks(root: Path, clients=None) -> dict:
    """Remove only unmodified registrations recorded by the Workbench installer."""
    root = Path(root).expanduser().resolve()
    selected = _clients(clients)
    with _lock(root):
        state, raw_state = _state(root)
        updated = copy.deepcopy(state)
        originals, updates = {_STATE: raw_state}, {}
        for client in selected:
            record = updated["clients"].pop(client, None)
            if record is None:
                continue
            relative = CONFIGS[client]
            document, raw = _document(root, relative)
            _remove_owned(document, client, record, missing=raw is None)
            residue = {"version": 1} if client == "copilot" else {}
            value = None if raw is None or (record["created"] and document == residue) else _bytes(document)
            originals[relative], updates[relative] = raw, value
        updates[_STATE] = _bytes(updated) if updated["clients"] else None
        _transaction(root, originals, updates)
    return hook_status(root)


def hook_status(root: Path) -> dict:
    """Inspect configuration without launching clients, creating runtime state, or granting trust."""
    root = Path(root).expanduser().resolve()
    try:
        state, _ = _state(root)
    except WorkbenchError as error:
        return {"status": "INCOMPLETE", "clients": [], "findings": [str(error)], "client_execution": "NOT_RUN"}
    rows = []
    for client, relative in CONFIGS.items():
        record = state["clients"].get(client)
        configured, detail = False, None
        if record:
            try:
                document, raw = _document(root, relative)
                _remove_owned(document, client, record, missing=False)
                configured = (raw is not None and record["workspace"] == str(root)
                              and Path(record["python"]).is_file() and os.access(record["python"], os.X_OK))
                if record["workspace"] != str(root):
                    detail = "The installation points to another workspace location. Reinstall for this workspace."
                elif not configured:
                    detail = "The installed Python executable is unavailable. Reinstall with the active environment."
            except WorkbenchError as error:
                detail = str(error)
        row = {"client": client, "path": relative, "status": "CONFIGURED" if configured else
               "INCOMPLETE" if record else "NOT_CONFIGURED", "detail": detail}
        if client == "claude":
            row["launch_argv"] = ["claude", "--settings", str(root / relative)]
        rows.append(row)
    count = sum(row["status"] == "CONFIGURED" for row in rows)
    return {"status": "INCOMPLETE" if any(row["status"] == "INCOMPLETE" for row in rows) else
            "READY" if count == len(CONFIGS) else "PARTIAL" if count else "NOT_CONFIGURED",
            "clients": rows, "client_execution": "NOT_RUN",
            "limitations": ["Client trust, executable availability, and native hook dispatch require separate checks.",
                            "Launch Claude Code with the returned --settings file to avoid Copilot importing its hooks."]}
