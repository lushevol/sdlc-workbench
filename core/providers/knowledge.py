"""Curated domain Markdown with exact retained source identities."""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path

from ..governance.validation import _document_content, _FORBIDDEN_KNOWLEDGE_PARTS, _NAVIGATION
from ..models import Context, Operation, Resource, WorkbenchError
from .common import BuiltinProvider, ProviderError, configured_path, integer_schema, object_schema, relative_path, string_schema

MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
MAX_DOCUMENTS = 1000


def _domain_path(path: Path, base: Path) -> bool:
    return (path.suffix.lower() == ".md" and path.name not in _NAVIGATION
            and path.name.casefold() != "log.md"
            and not any(part.casefold() in _FORBIDDEN_KNOWLEDGE_PARTS for part in path.relative_to(base).parts))


def _domain_content(text: str):
    try:
        _document_content(text, domain_only=True)
    except (WorkbenchError, TypeError) as error:
        raise ProviderError("INVALID_DOCUMENT", str(error)) from None


def document(path: Path, base: Path, *, content: bool = False) -> dict:
    if not path.is_file() or not _domain_path(path, base):
        raise ProviderError("INVALID_DOCUMENT", "Select a domain Markdown document outside navigation and evidence directories.")
    with path.open("rb") as stream:
        raw = stream.read(MAX_DOCUMENT_BYTES + 1)
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise ProviderError("DOCUMENT_TOO_LARGE", "The document exceeds the two MiB limit.")
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        raise ProviderError("INVALID_DOCUMENT", "Use a UTF-8 domain Markdown document.") from None
    _domain_content(text)
    result = {"path": str(path), "relative_path": path.relative_to(base).as_posix(),
              "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    if content:
        result["content"] = text
    return result


class LocalKnowledgeProvider(BuiltinProvider):
    id = "knowledge.local"
    resource_kind = "knowledge"
    operations = {
        "list": Operation("list", "List structured domain Markdown documents.", object_schema()),
        "search": Operation("search", "Find literal text and retain source locators.", object_schema({
            "query": string_schema(maximum=4096), "limit": integer_schema(1, 1000)}, ("query",))),
        "read": Operation("read", "Read exact document bytes as UTF-8 text.", object_schema({
            "path": string_schema()}, ("path",))),
        "ingest": Operation("ingest", "Create or replace a structured domain knowledge document.", object_schema({
            "path": string_schema(), "content": string_schema(minimum=0, maximum=MAX_DOCUMENT_BYTES)},
            ("path", "content")), mutating=True),
    }

    def _files(self, base: Path, context: Context) -> tuple[list[Path], bool]:
        files = []
        truncated = False
        for directory, directories, filenames in os.walk(base, followlinks=False):
            directories[:] = sorted(name for name in directories if name.casefold() not in _FORBIDDEN_KNOWLEDGE_PARTS
                                    and not (Path(directory) / name).is_symlink())
            for name in sorted(filenames):
                candidate = Path(directory) / name
                if candidate.is_symlink() or not candidate.is_file() or not _domain_path(candidate, base):
                    continue
                path = relative_path(base, candidate.relative_to(base).as_posix(), context)
                try:
                    document(path, base)
                except ProviderError:
                    continue
                if len(files) == MAX_DOCUMENTS:
                    return files, True
                files.append(path)
        return files, truncated

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        base = configured_path(resource, context)
        if operation == "ingest":
            path = relative_path(base, arguments["path"], context)
            if not _domain_path(path, base):
                raise ProviderError("INVALID_DOCUMENT", "Select a domain Markdown document outside navigation and evidence directories.")
            raw = arguments["content"].encode("utf-8")
            if len(raw) > MAX_DOCUMENT_BYTES:
                raise ProviderError("DOCUMENT_TOO_LARGE", "The document exceeds the two MiB limit.")
            _domain_content(arguments["content"])
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(prefix=".ingest-", dir=path.parent)
            try:
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, path)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
            return {"status": "SUCCEEDED", "document": document(path, base, content=True)}
        if not base.is_dir():
            raise ProviderError("RESOURCE_UNAVAILABLE", "The knowledge folder is unavailable.")
        if operation == "read":
            return {"status": "SUCCEEDED", "document": document(relative_path(base, arguments["path"], context), base, content=True)}
        files, inventory_truncated = self._files(base, context)
        if operation == "list":
            return {"status": "SUCCEEDED", "files": [document(path, base) for path in files], "truncated": inventory_truncated}
        query, limit = arguments["query"].casefold(), arguments.get("limit", 20)
        matches, retained_bytes = [], 0
        for path in files:
            source = document(path, base, content=True)
            for line_number, text in enumerate(source["content"].splitlines(), 1):
                if query in text.casefold():
                    line_bytes = len(text.encode("utf-8"))
                    if len(matches) == limit or retained_bytes + line_bytes > MAX_DOCUMENT_BYTES:
                        return {"status": "SUCCEEDED", "matches": matches, "truncated": True}
                    matches.append({key: source[key] for key in ("path", "relative_path", "sha256")} |
                                   {"line_number": line_number, "text": text})
                    retained_bytes += line_bytes
        return {"status": "SUCCEEDED", "matches": matches, "truncated": inventory_truncated}
