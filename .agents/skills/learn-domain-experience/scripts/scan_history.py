#!/usr/bin/env python3
"""Scan retained task and session files for bounded experience-discovery signals."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys


DEFAULT_MAX_FILES = 512
DEFAULT_MAX_BYTES = 32 * 1024 * 1024
SKIP_PARTS = {".git", "__pycache__", "node_modules", ".venv", ".venv-openkb", ".venv-llm-wiki"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".log", ".robot", ".feature", ".toml"}
SIGNAL_WORDS = {
    "workflow", "steps", "commands", "result", "outcome", "validation", "recovery", "variable",
    "url", "knowledge", "evidence", "limit", "success", "passed", "assertion", "fixture",
}
HEADING = re.compile(r"^#{1,4}\s+(.+?)\s*$")
REDACT = (
    (re.compile(r"https?://[^\s)]+"), "<url>"),
    (re.compile(r"\b(?:AKIA|ghp_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]+"), "<credential>"),
)


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


def _record(path: Path, workspace: Path) -> tuple[dict | None, int]:
    try:
        raw = path.read_bytes()
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
    return {
        "path": relative,
        "kind": "task" if relative.startswith("tasks/") else "session",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "headings": headings[:80],
        "signals": sorted(signals),
    }, len(raw)


def scan(workspace: Path, explicit: list[str], include_workbench: bool, max_files: int, max_bytes: int) -> dict:
    roots: list[Path] = []
    tasks = workspace / "tasks"
    if tasks.is_dir():
        roots.extend(path for path in sorted(tasks.iterdir()) if path.is_dir() and path.name != "__pycache__")
    if include_workbench and (workspace / ".workbench").is_dir():
        roots.append(workspace / ".workbench")
    for value in explicit:
        candidate = Path(value).expanduser()
        roots.append(candidate if candidate.is_absolute() else workspace / candidate)

    seen = set()
    files = []
    for root in roots:
        for path in _files_for(root):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(path)
    files.sort()
    records = []
    total = 0
    truncated = False
    for path in files:
        if len(records) >= max_files or total >= max_bytes:
            truncated = True
            break
        record, size = _record(path, workspace)
        if record is None or total + size > max_bytes:
            truncated = True
            continue
        records.append(record)
        total += size
    tasks = sorted({record["path"].split("/", 2)[1] for record in records if record["path"].startswith("tasks/") and len(record["path"].split("/")) > 1})
    return {
        "schema_version": 1,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "tasks": tasks,
        "files": records,
        "limits": [
            f"Scanned at most {max_files} files and {max_bytes} bytes.",
            "Signals are search hints. They do not establish a successful outcome or business approval.",
            *(["The scan was truncated at the configured limit."] if truncated else []),
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".", help="Workbench workspace root")
    parser.add_argument("--path", action="append", default=[], help="Additional retained task or session path")
    parser.add_argument("--include-workbench", action="store_true", help="Include ignored .workbench session state")
    parser.add_argument("--output", required=True, help="JSON output path")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    arguments = parser.parse_args(argv)
    if arguments.max_files < 1 or arguments.max_bytes < 1:
        parser.error("max-files and max-bytes must be positive")
    workspace = Path(arguments.workspace).expanduser().resolve()
    payload = scan(workspace, arguments.path, arguments.include_workbench, arguments.max_files, arguments.max_bytes)
    output = Path(arguments.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASSED", "output": str(output), "files": len(payload["files"]), "tasks": len(payload["tasks"])}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
