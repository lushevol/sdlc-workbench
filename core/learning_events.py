"""Store bounded lifecycle hints for Workbench capability learning."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from itertools import islice
import os
import re

from .assurance import _json, local_path
from .hook_install import CONNECTOR_PREFIX, NATIVE_EVENTS, TOOL_CLASSES, _atomic, _bytes
from .hooks import _file_lock
from .models import WorkbenchError


EVENTS_DIR = ".workbench/learning/events"
_EVENTS = ("start", "recovery", "completion", "compact", "end", "tool")
_OUTCOMES = ("complete", "failure")
_DIAGNOSTIC_LIMIT = 10000


def capture_enabled():
    return os.environ.get("WORKBENCH_LEARNING_CAPTURE", "1").casefold() not in {"0", "false", "off"}


def _filename(record):
    parts = [record["session_key"], record["event"]]
    if record["event"] == "tool":
        parts += [record["tool_class"], record["outcome"]]
    return "-".join(parts) + ".json"


def capture_event(root, client, session_key, event, payload):
    record = {"schema_version": 1, "client": client, "session_key": session_key}
    if event in ("tool", "tool-failure"):
        name = payload.get("toolName", payload.get("tool_name"))
        if not isinstance(name, str):
            return
        kind = "connector" if name.startswith(CONNECTOR_PREFIX) else TOOL_CLASSES.get(name)
        if kind is None:
            return
        result = payload.get("toolResult", payload.get("tool_result"))
        outcome = result.get("resultType", result.get("result_type")) if isinstance(result, dict) else None
        failed = event == "tool-failure" or outcome == "failure"
        record.update(event="tool", tool_class=kind, outcome="failure" if failed else "complete")
    elif event == "start" and payload.get("source") in ("resume", "compact", "fork"):
        record["event"] = "recovery"
    elif event == "stop":
        record["event"] = "end" if client == "codex" else "completion"
    else:
        record["event"] = event
    path = local_path(root, f"{EVENTS_DIR}/{_filename(record)}")
    if path.exists():
        return
    lock = local_path(root, f"{EVENTS_DIR}/{path.stem}.lock")
    with _file_lock(lock):
        if not path.exists():
            record["observed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            _atomic(path, _bytes(record))


def _read_event(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("Expected a regular lifecycle record.")
    with path.open("rb") as stream:
        record = _json(stream.read(1025))
    if (type(record.get("schema_version")) is not int or record["schema_version"] != 1
            or not isinstance(record.get("client"), str) or record["client"] not in NATIVE_EVENTS
            or record.get("event") not in _EVENTS
            or not isinstance(record.get("session_key"), str) or not re.fullmatch("[a-f0-9]{64}", record["session_key"])
            or not isinstance(record.get("observed_at"), str)):
        raise ValueError("Invalid lifecycle event.")
    fields = {"schema_version", "client", "session_key", "event", "observed_at"}
    if record["event"] == "tool":
        fields.update(("tool_class", "outcome"))
        if record.get("tool_class") not in ("shell", "edit", "connector") or record.get("outcome") not in _OUTCOMES:
            raise ValueError("Invalid lifecycle tool class or outcome.")
    if record.keys() != fields or path.name != _filename(record):
        raise ValueError("Invalid lifecycle record fields or identity.")
    datetime.fromisoformat(record["observed_at"])
    return record


def diagnose_events(root):
    """Inspect retained event classes without displaying raw session keys."""
    counts = {client: Counter() for client in NATIVE_EVENTS}
    invalid = 0
    scanned = 0
    try:
        directory = local_path(root, EVENTS_DIR)
        if directory.exists() and not directory.is_dir():
            raise WorkbenchError("Expected a lifecycle record directory.")
        for scanned, path in enumerate(islice(directory.glob("*.json"), _DIAGNOSTIC_LIMIT + 1), 1):
            if scanned > _DIAGNOSTIC_LIMIT:
                break
            try:
                record = _read_event(path)
            except (OSError, ValueError, RecursionError):
                invalid += 1
            else:
                counts[record["client"]][record["event"]] += 1
    except (OSError, WorkbenchError):
        return {"status": "UNAVAILABLE", "capture_enabled": capture_enabled(), "location": EVENTS_DIR}
    return {
        "status": "CHECK_REQUIRED" if invalid else "OBSERVED" if scanned else "NO_EVENTS",
        "capture_enabled": capture_enabled(), "location": EVENTS_DIR,
        "clients": {client: dict(counter) for client, counter in counts.items()},
        "invalid_records": invalid, "scan_limited": scanned > _DIAGNOSTIC_LIMIT,
    }
