"""Bounded literal search over one configured UTF-8 log file."""

from __future__ import annotations

import hashlib

from ..models import Context, Operation, Resource
from .common import BuiltinProvider, ProviderError, configured_path, integer_schema, object_schema, string_schema

MAX_LOG_BYTES = 16 * 1024 * 1024
MAX_LINE_BYTES = 64 * 1024


class FileLogsProvider(BuiltinProvider):
    id = "logs.file"
    resource_kind = "logs"
    operations = {"search": Operation("search", "Find literal text in a configured log file.", object_schema({
        "query": string_schema(), "limit": integer_schema(1, 1000)}, ("query",)))}

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        path = configured_path(resource, context)
        if not path.is_file():
            raise ProviderError("RESOURCE_UNAVAILABLE", "The configured log file is unavailable.")
        matches, scanned_bytes, truncated = [], 0, False
        digest = hashlib.sha256()
        query, limit = arguments["query"], arguments.get("limit", 100)
        with path.open("rb") as stream:
            line_number = 0
            while True:
                raw = stream.readline(MAX_LINE_BYTES + 1)
                if not raw:
                    break
                if len(raw) > MAX_LINE_BYTES:
                    raise ProviderError("LINE_TOO_LARGE", "A log line exceeds the 64 KiB limit.")
                if scanned_bytes + len(raw) > MAX_LOG_BYTES:
                    truncated = True
                    break
                digest.update(raw)
                scanned_bytes += len(raw)
                line_number += 1
                text = raw.decode("utf-8").rstrip("\r\n")
                if query in text:
                    if len(matches) < limit:
                        matches.append({"line_number": line_number, "text": text})
                    else:
                        truncated = True
        return {"status": "SUCCEEDED", "path": str(path), "matches": matches, "truncated": truncated,
                "scanned_bytes": scanned_bytes, "scanned_sha256": digest.hexdigest(),
                "hash_scope": "scanned file prefix"}
