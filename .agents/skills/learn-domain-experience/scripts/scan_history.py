#!/usr/bin/env python3
"""Scan retained task and session files for bounded experience-discovery signals."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys


DEFAULT_PAST_DURATION = "7d"
DEFAULT_MAX_FILES = 512
DEFAULT_MAX_BYTES = 32 * 1024 * 1024
SKIP_PARTS = {".git", "__pycache__", "node_modules", ".venv", ".venv-openkb", ".venv-llm-wiki"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".log", ".robot", ".feature", ".toml"}
SIGNAL_WORDS = {
    "workflow", "steps", "commands", "result", "outcome", "validation", "recovery", "variable",
    "url", "knowledge", "evidence", "limit", "success", "passed", "assertion", "fixture",
}
HEADING = re.compile(r"^#{1,4}\s+(.+?)\s*$")
DURATION = re.compile(r"^(?P<value>[1-9][0-9]*)(?P<unit>[hdw])$")
REDACT = (
    (re.compile(r"https?://[^\s)]+"), "<url>"),
    (re.compile(r"\b(?:AKIA|ghp_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]+"), "<credential>"),
)


def parse_duration(value: str) -> int:
    """Return a bounded duration in seconds."""
    match = DURATION.fullmatch(value.strip()) if isinstance(value, str) else None
    if match is None:
        raise ValueError("Use a positive duration such as 24h, 7d, or 1w.")
    amount = int(match.group("value"))
    multiplier = {"h": 3600, "d": 86400, "w": 7 * 86400}[match.group("unit")]
    seconds = amount * multiplier
    if seconds > 366 * 86400:
        raise ValueError("Use a duration of at most 366 days.")
    return seconds


def _redact(value: str) -> str:
    for pattern, replacement in REDACT:
        value = pattern.sub(replacement, value)
    return value[:240]


def _files_for(path: Path):
    if path.is_symlink():
        return []
    if path.is_file():
        return [path]
    if not path.is_dir():
        return []
    return [candidate for candidate in sorted(path.rglob("*"))
            if not candidate.is_symlink() and candidate.is_file()
            and not any(part in SKIP_PARTS for part in candidate.parts)
            and candidate.suffix.lower() in TEXT_SUFFIXES]


def _record(path: Path, workspace: Path, *, session_id: str | None = None) -> tuple[dict | None, int]:
    try:
        raw = path.read_bytes()
        modified = path.stat().st_mtime
    except OSError:
        return None, 0
    if len(raw) > 8 * 1024 * 1024 or b"\0" in raw:
        return None, 0
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, 0
    headings = []
    signals = set()
    for line in text.splitlines()[:20000]:
        match = HEADING.match(line)
        if match:
            heading = _redact(match.group(1))
            headings.append(heading)
            lowered = heading.lower()
            signals.update(word for word in SIGNAL_WORDS if word in lowered)
    resolved = path.resolve()
    relative = resolved.relative_to(workspace).as_posix() if resolved.is_relative_to(workspace) else str(resolved)
    record = {
        "path": relative,
        "kind": "task" if relative.startswith("tasks/") else "session",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "modified_at": datetime.fromtimestamp(modified, timezone.utc).isoformat(),
        "headings": headings[:80],
        "signals": sorted(signals),
    }
    if session_id is not None:
        record["session_id"] = session_id
    return record, len(raw)


def _session_roots(workspace: Path, explicit: list[str], include_workbench: bool):
    roots: list[tuple[str, Path]] = []
    tasks = workspace / "tasks"
    if tasks.is_dir():
        roots.extend(("task", path) for path in sorted(tasks.iterdir()) if path.is_dir() and path.name != "__pycache__")
    if include_workbench and (workspace / ".workbench").is_dir():
        workbench = workspace / ".workbench"
        roots.extend(("session", path) for path in sorted(workbench.iterdir())
                     if path.name != "experience" and not path.is_symlink() and (path.is_file() or path.is_dir()))
    for value in explicit:
        candidate = Path(value).expanduser()
        candidate = candidate if candidate.is_absolute() else workspace / candidate
        kind = "task" if candidate.resolve().is_relative_to((workspace / "tasks").resolve()) else "session"
        roots.append((kind, candidate))
    return roots


def _load_state(path: Path) -> tuple[dict, list[str]]:
    if not path.exists():
        return {}, []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1 or not isinstance(payload.get("sessions"), dict):
            raise ValueError
        return payload["sessions"], []
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError):
        return {}, ["The previous scan state was invalid and was rebuilt."]


def _write_state(path: Path, sessions: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps({"schema_version": 1, "sessions": sessions}, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    os.replace(temporary, path)


def _fingerprint(records: list[dict]) -> str:
    values = [{key: record[key] for key in ("path", "bytes", "sha256", "modified_at")} for record in records]
    encoded = json.dumps(values, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _candidate_id(path: str) -> str:
    return "candidate." + hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]


def scan(workspace: Path, explicit: list[str], include_workbench: bool, max_files: int, max_bytes: int,
         past_duration: str, state_path: Path) -> tuple[dict, dict]:
    duration_seconds = parse_duration(past_duration)
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(seconds=duration_seconds)
    prior_state, state_limits = _load_state(state_path)
    next_state = dict(prior_state)
    records: list[dict] = []
    seen: set[Path] = set()
    total = 0
    truncated = False
    scanned_sessions = []
    skipped_sessions = []
    out_of_window_sessions = []

    for kind, root in _session_roots(workspace, explicit, include_workbench):
        source_id = root.resolve().relative_to(workspace).as_posix() if root.resolve().is_relative_to(workspace) else str(root.resolve())
        paths = []
        for path in _files_for(root):
            resolved = path.resolve()
            if resolved in seen:
                continue
            try:
                modified = path.stat().st_mtime
            except OSError:
                continue
            if kind == "session" and modified < cutoff.timestamp():
                continue
            paths.append(path)
        source_records: list[dict] = []
        for path in paths:
            if len(records) + len(source_records) >= max_files or total >= max_bytes:
                truncated = True
                break
            record, size = _record(path, workspace, session_id=source_id if kind == "session" else None)
            if record is None or total + size > max_bytes:
                truncated = True
                continue
            source_records.append(record)
            total += size
            seen.add(path.resolve())
        if kind != "session":
            records.extend(source_records)
            if truncated:
                break
            continue

        latest_mtime = max((datetime.fromisoformat(record["modified_at"]).timestamp() for record in source_records), default=0.0)
        if not source_records:
            out_of_window_sessions.append({"id": source_id, "cutoff": cutoff.isoformat()})
            continue
        fingerprint = _fingerprint(source_records)
        prior = prior_state.get(source_id)
        prior_cutoff = prior.get("cutoff") if isinstance(prior, dict) else None
        can_skip = (isinstance(prior, dict) and prior.get("fingerprint") == fingerprint
                    and prior.get("duration_seconds") == duration_seconds
                    and isinstance(prior.get("latest_mtime"), (int, float))
                    and latest_mtime <= prior["latest_mtime"]
                    and (not prior_cutoff or cutoff.timestamp() >= datetime.fromisoformat(prior_cutoff).timestamp()))
        if can_skip:
            skipped_sessions.append({"id": source_id, "latest_mtime": latest_mtime, "reason": "latest source already scanned"})
            continue
        records.extend(source_records)
        scanned_sessions.append({"id": source_id, "latest_mtime": latest_mtime, "files": len(source_records)})
        next_state[source_id] = {"fingerprint": fingerprint, "latest_mtime": latest_mtime,
                                 "duration_seconds": duration_seconds, "cutoff": cutoff.isoformat(),
                                 "scanned_at": now.isoformat()}
        if truncated:
            break

    tasks = sorted({record["path"].split("/", 2)[1] for record in records
                    if record["path"].startswith("tasks/") and len(record["path"].split("/")) > 1})
    candidates = [{"id": _candidate_id(record["path"]), "source_paths": [record["path"]],
                   "signals": record["signals"], "proposed_primary_recipe": None, "decision": "PENDING"}
                  for record in records if record["signals"]]
    payload = {
        "schema_version": 1,
        "scanned_at": now.isoformat(),
        "workspace": str(workspace),
        "tasks": tasks,
        "session_scan": {"past_duration": past_duration, "duration_seconds": duration_seconds,
                         "cutoff": cutoff.isoformat(), "scanned_sessions": scanned_sessions,
                         "skipped_sessions": skipped_sessions, "out_of_window_sessions": out_of_window_sessions},
        "review": {"review_status": "PENDING", "candidates": candidates,
                    "decision_required": "Approve, reject, or revise candidate IDs before invoking package-domain-experience."},
        "promotion": {"status": "BLOCKED_UNTIL_EXPLICIT_REVIEW", "packets_created": 0, "index_changed": False},
        "files": records,
        "limits": [f"Scanned at most {max_files} files and {max_bytes} bytes.",
                   "Signals and candidates are search hints. They do not establish a successful outcome or business approval.",
                   "No packet or experience index was created by this scan.", *state_limits,
                   *(["The scan was truncated at the configured limit."] if truncated else [])],
    }
    return payload, next_state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".", help="Workbench workspace root")
    parser.add_argument("--path", action="append", default=[], help="Additional retained task or session path")
    parser.add_argument("--include-workbench", action="store_true", help="Include ignored .workbench session state")
    parser.add_argument("--past-duration", default=DEFAULT_PAST_DURATION, help="Session scan window such as 7d, 1w, or 24h")
    parser.add_argument("--scan-state", help="Workspace-relative or absolute scan state JSON path")
    parser.add_argument("--output", required=True, help="Review inventory JSON output path")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    arguments = parser.parse_args(argv)
    if arguments.max_files < 1 or arguments.max_bytes < 1:
        parser.error("max-files and max-bytes must be positive")
    try:
        parse_duration(arguments.past_duration)
    except ValueError as error:
        parser.error(str(error))
    workspace = Path(arguments.workspace).expanduser().resolve()
    state = Path(arguments.scan_state).expanduser() if arguments.scan_state else workspace / ".workbench/experience/scan-state.json"
    state = state if state.is_absolute() else workspace / state
    output = Path(arguments.output).expanduser()
    output = output if output.is_absolute() else workspace / output
    try:
        payload, next_state = scan(workspace, arguments.path, arguments.include_workbench, arguments.max_files,
                                   arguments.max_bytes, arguments.past_duration, state)
        output = output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _write_state(state, next_state)
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "FAILED", "error": str(error)}, indent=2))
        return 1
    print(json.dumps({"status": "PASSED", "output": str(output), "files": len(payload["files"]),
                      "tasks": len(payload["tasks"]), "review_status": payload["review"]["review_status"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
