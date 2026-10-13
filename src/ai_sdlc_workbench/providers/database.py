"""Read-only SQLite queries with authorization, time, and result bounds."""

from __future__ import annotations

from contextlib import closing
import json
import sqlite3
import time

from ..models import Context, Operation, Resource
from .common import BuiltinProvider, ProviderError, configured_path, integer_schema, object_schema, string_schema, timeout


def _authorize(action: int, first: str | None, second: str | None, database: str | None, trigger: str | None) -> int:
    allowed = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}
    if action == sqlite3.SQLITE_FUNCTION and (second or first or "").lower() in {"load_extension", "writefile", "readfile"}:
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY


def _cell(value):
    if isinstance(value, bytes):
        return {"hex": value[:32768].hex(), "bytes": len(value), "truncated": len(value) > 32768}
    if isinstance(value, str) and len(value) > 65536:
        return {"text": value[:65536], "characters": len(value), "truncated": True}
    return value


class SQLiteDatabaseProvider(BuiltinProvider):
    id = "database.sqlite"
    resource_kind = "database"
    operations = {
        "tables": Operation("tables", "List tables and views in a read-only database.", object_schema()),
        "query": Operation("query", "Run a bounded read-only SQLite query.", object_schema({
            "sql": string_schema(maximum=20000), "max_rows": integer_schema(1, 1000)}, ("sql",))),
    }

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        path = configured_path(resource, context)
        seconds = timeout(context)
        deadline = time.monotonic() + seconds
        try:
            with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=min(seconds, 5.0))) as database:
                database.execute("PRAGMA query_only=ON")
                if hasattr(database, "setlimit"):
                    database.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1024 * 1024)
                    database.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 256)
                    database.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 20000)
                database.set_authorizer(_authorize)
                database.set_progress_handler(lambda: int(time.monotonic() >= deadline), 1000)
                if operation == "tables":
                    rows = database.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY name").fetchmany(1001)
                    return {"status": "SUCCEEDED", "tables": [{"name": row[0], "type": row[1]} for row in rows[:1000]],
                            "truncated": len(rows) > 1000}
                cursor = database.execute(arguments["sql"])
                if cursor.description is None:
                    raise ProviderError("READ_ONLY_QUERY_REQUIRED", "The query must return read-only results.")
                maximum = arguments.get("max_rows", 100)
                rows, retained_bytes, truncated = [], 0, False
                for _ in range(maximum + 1):
                    if time.monotonic() >= deadline:
                        return {"status": "TIMEOUT", "message": "The database query exceeded its timeout."}
                    source_row = cursor.fetchone()
                    if source_row is None:
                        break
                    row = [_cell(value) for value in source_row]
                    row_bytes = len(json.dumps(row, ensure_ascii=False).encode("utf-8"))
                    if len(rows) == maximum or retained_bytes + row_bytes > 4 * 1024 * 1024:
                        truncated = True
                        break
                    rows.append(row)
                    retained_bytes += row_bytes
                return {"status": "SUCCEEDED", "columns": [column[0] for column in cursor.description],
                        "rows": rows, "truncated": truncated}
        except sqlite3.Error:
            if time.monotonic() >= deadline:
                return {"status": "TIMEOUT", "message": "The database query exceeded its timeout."}
            return {"status": "ERROR", "code": "QUERY_REJECTED", "message": "SQLite rejected the read-only query or database access."}
