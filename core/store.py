"""Local action records and retained evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

from .models import WorkbenchError


class Store:
    def __init__(self, root: Path):
        self.root = root
        self.state = root / ".workbench"
        if self.state.is_symlink():
            raise WorkbenchError("Workbench state must use a local directory.")
        self.state.mkdir(exist_ok=True)
        self.runs_dir = self.state / "runs"
        if self.runs_dir.is_symlink():
            raise WorkbenchError("Action evidence must use a local directory.")
        self.runs_dir.mkdir(exist_ok=True)
        self.database = self.state / "actions.sqlite3"
        if self.database.is_symlink():
            raise WorkbenchError("Action records must use a local database file.")
        with closing(sqlite3.connect(self.database)) as db, db:
            db.execute("CREATE TABLE IF NOT EXISTS actions (id TEXT PRIMARY KEY, started_at TEXT, record TEXT NOT NULL)")

    def save(self, record: dict) -> None:
        encoded = json.dumps(record, ensure_ascii=False, allow_nan=False)
        with closing(sqlite3.connect(self.database, timeout=10)) as db, db:
            db.execute("INSERT INTO actions(id, started_at, record) VALUES (?, ?, ?) "
                       "ON CONFLICT(id) DO UPDATE SET record=excluded.record",
                       (record["id"], record["started_at"], encoded))

    def run(self, run_id: str) -> dict:
        if not isinstance(run_id, str) or not re.fullmatch(r"[a-f0-9]{32}", run_id):
            raise WorkbenchError("The action ID is invalid.")
        with closing(sqlite3.connect(self.database)) as db:
            row = db.execute("SELECT record FROM actions WHERE id=?", (run_id,)).fetchone()
        if row is None:
            raise WorkbenchError("The action does not exist.")
        return json.loads(row[0])

    def runs(self, limit: int = 20) -> list[dict]:
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
            raise WorkbenchError("Use an action limit from 1 to 100.")
        with closing(sqlite3.connect(self.database)) as db:
            rows = db.execute("SELECT record FROM actions ORDER BY started_at DESC LIMIT ?", (limit,)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def retain(self, record: dict, directory: Path) -> None:
        if directory.is_symlink() or not directory.resolve().is_relative_to(self.runs_dir.resolve()):
            raise WorkbenchError("Evidence must stay in the action directory.")
        for path in directory.rglob("*"):
            if path.is_symlink():
                raise WorkbenchError("Evidence must use regular files.")
        descriptor, temporary = tempfile.mkstemp(prefix=".result-", dir=directory)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump({"result": record["result"], "error": record["error"]}, stream,
                          indent=2, ensure_ascii=False, allow_nan=False)
            os.replace(temporary, directory / "result.json")
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        evidence = []
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise WorkbenchError("Evidence must use regular files.")
            if path.is_file():
                digest, size = hashlib.sha256(), 0
                with path.open("rb") as stream:
                    while chunk := stream.read(1024 * 1024):
                        digest.update(chunk)
                        size += len(chunk)
                evidence.append({"path": path.relative_to(self.root).as_posix(),
                                 "sha256": digest.hexdigest(), "size_bytes": size})
        record["evidence"] = evidence
        self.save(record)
