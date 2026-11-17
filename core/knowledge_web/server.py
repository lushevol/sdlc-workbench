"""Small read-only HTTP preview for the Workbench knowledge collections."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from typing import Iterable
from urllib.parse import parse_qs, urlparse
import webbrowser

import yaml

from ..knowledge_layout import knowledge_layout
from ..models import WorkbenchError


MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
TEXT_SUFFIXES = frozenset({".md", ".markdown", ".txt", ".json", ".yaml", ".yml", ".log"})
SKIP_PARTS = frozenset({".git", ".venv", ".workbench", "node_modules", "__pycache__", ".openkb"})
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.S)
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")


@dataclass(frozen=True)
class Document:
    key: str
    collection: str
    path: str
    title: str
    content: str
    metadata: dict
    headings: tuple[dict, ...]
    sha256: str
    bytes: int

    def summary(self) -> dict:
        metadata = self.metadata
        return {
            "key": self.key,
            "collection": self.collection,
            "path": self.path,
            "title": self.title,
            "type": metadata.get("type"),
            "id": metadata.get("id"),
            "status": metadata.get("status"),
            "governance_state": metadata.get("governance_state"),
            "sha256": self.sha256,
            "bytes": self.bytes,
        }


@dataclass(frozen=True)
class RootSpec:
    collection: str
    label: str
    path: Path
    extensions: frozenset[str]
    evidence_only: bool = False
    allowed_files: frozenset[Path] | None = None


def _safe_json(value):
    if isinstance(value, dict):
        return {str(key): _safe_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_safe_json(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    try:
        value = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        value = {"_parse_error": "Frontmatter could not be parsed."}
    if not isinstance(value, dict):
        value = {"_parse_error": "Frontmatter is not a mapping."}
    return _safe_json(value), text[match.end():]


def _title(path: Path, body: str, metadata: dict) -> str:
    value = metadata.get("title") or metadata.get("name")
    if isinstance(value, str) and value.strip():
        return value.strip()
    for line in body.splitlines():
        match = HEADING.match(line)
        if match:
            return match.group(2).strip().strip("# ")
    return path.stem.replace("-", " ").replace("_", " ").strip().title()


def _headings(body: str) -> tuple[dict, ...]:
    result = []
    seen: dict[str, int] = {}
    fence = None
    for line_number, line in enumerate(body.splitlines(), 1):
        fence_match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence_match:
            token = fence_match.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        match = HEADING.match(line)
        if not match:
            continue
        text = match.group(2).strip().strip("# ")
        slug = re.sub(r"[^a-z0-9 -]", "", text.casefold()).strip().replace(" ", "-") or "section"
        occurrence = seen.get(slug, 0)
        seen[slug] = occurrence + 1
        if occurrence:
            slug = f"{slug}-{occurrence}"
        result.append({"level": len(match.group(1)), "text": text, "slug": slug, "line": line_number})
    return tuple(result)


def _read_document(collection: str, path: Path, workspace: Path) -> Document | None:
    try:
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(workspace) or path.is_symlink() or not resolved.is_file():
            return None
        raw = resolved.read_bytes()
    except (OSError, ValueError):
        return None
    if len(raw) > MAX_DOCUMENT_BYTES:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    metadata, body = _frontmatter(text)
    relative = resolved.relative_to(workspace).as_posix()
    return Document(
        key=f"{collection}:{relative}", collection=collection, path=relative,
        title=_title(resolved, body, metadata), content=text, metadata=metadata,
        headings=_headings(body), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
    )


def _walk(spec: RootSpec) -> Iterable[Path]:
    if spec.allowed_files is not None:
        for path in sorted(spec.allowed_files):
            if path.is_file() and not path.is_symlink():
                yield path
        return
    if spec.path.is_symlink():
        return
    if spec.path.is_file():
        if spec.path.suffix.casefold() in spec.extensions:
            yield spec.path
        return
    if not spec.path.is_dir():
        return
    for directory, directories, filenames in os.walk(spec.path, followlinks=False):
        base = Path(directory)
        directories[:] = sorted(name for name in directories
                                 if name not in SKIP_PARTS and not (base / name).is_symlink())
        for filename in sorted(filenames):
            path = base / filename
            if path.is_symlink() or path.suffix.casefold() not in spec.extensions:
                continue
            if spec.evidence_only and "evidence" not in path.relative_to(spec.path).parts:
                continue
            yield path


class KnowledgeCatalog:
    """Immutable document snapshots rooted in approved workspace collections."""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).expanduser().resolve()
        self._lock = threading.RLock()
        self._roots = self._root_specs()
        self._documents: dict[str, Document] = {}
        self.refresh()

    def _root_specs(self) -> tuple[RootSpec, ...]:
        records, evidence = knowledge_layout(self.workspace)
        specs = [RootSpec("records", "Canonical records", records, frozenset({".md", ".markdown"}))]
        wiki = self.workspace / "knowledge/llm-wiki/wiki"
        if wiki.is_dir():
            specs.append(RootSpec("wiki", "Derived wiki", wiki, frozenset({".md", ".markdown"})))
        docs = self.workspace / "docs"
        if docs.is_dir():
            specs.append(RootSpec("docs", "Current documentation", docs, frozenset({".md", ".markdown"})))
        for root_file in ("README.md", "ARCHITECTURE.md", "PRINCIPLE.md", "AGENTS.md", "knowledge/README.md"):
            path = self.workspace / root_file
            if path.is_file():
                specs.append(RootSpec("docs", "Current documentation", path, frozenset({path.suffix.casefold()})))
        if evidence.is_dir():
            specs.append(RootSpec("evidence", "Knowledge evidence", evidence, TEXT_SUFFIXES))
        tasks = self.workspace / "tasks"
        if tasks.is_dir():
            linked = set()
            manifest = evidence / "manifest.yaml"
            if manifest.is_file():
                try:
                    payload = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
                except (OSError, UnicodeError, yaml.YAMLError):
                    payload = {}
                for entry in payload.get("sources", []) if isinstance(payload, dict) else []:
                    snapshot = entry.get("snapshot") if isinstance(entry, dict) else None
                    if not isinstance(snapshot, str) or not snapshot.startswith("tasks/"):
                        continue
                    path = self.workspace / snapshot
                    if path.is_file() and path.resolve().is_relative_to(tasks.resolve()):
                        linked.add(path)
            specs.append(RootSpec("evidence", "Linked task evidence", tasks, TEXT_SUFFIXES,
                                  allowed_files=frozenset(linked)))
        return tuple(specs)

    def refresh(self) -> dict:
        fresh: dict[str, Document] = {}
        for spec in self._roots:
            for path in _walk(spec):
                document = _read_document(spec.collection, path, self.workspace)
                if document is not None:
                    fresh[document.key] = document
        with self._lock:
            self._documents = fresh
        return self.health()

    def health(self) -> dict:
        with self._lock:
            counts: dict[str, int] = {}
            for document in self._documents.values():
                counts[document.collection] = counts.get(document.collection, 0) + 1
            return {"status": "READY", "documents": len(self._documents), "collections": counts}

    def navigation(self) -> dict:
        with self._lock:
            documents = sorted(self._documents.values(), key=lambda item: (item.collection, item.path.casefold()))
            groups: dict[str, list[dict]] = {}
            labels = {spec.collection: spec.label for spec in self._roots}
            for document in documents:
                groups.setdefault(document.collection, []).append(document.summary())
            return {"collections": [{"id": collection, "label": labels.get(collection, collection.title()),
                                     "count": len(items), "documents": items}
                                     for collection, items in sorted(groups.items())], "health": self.health()}

    def document(self, key: str) -> Document:
        with self._lock:
            document = self._documents.get(key)
        if document is None:
            raise KeyError(key)
        return document

    def search(self, query: str, collection: str | None, limit: int) -> list[dict]:
        folded = query.casefold().strip()
        if not folded:
            return []
        with self._lock:
            documents = tuple(self._documents.values())
        matches = []
        for document in documents:
            if collection and document.collection != collection:
                continue
            body = document.content.casefold()
            haystack = "\n".join((document.title, document.path, json.dumps(document.metadata), document.content)).casefold()
            if folded not in haystack:
                continue
            position = body.find(folded)
            if position >= 0:
                start = max(0, position - 90)
                snippet = document.content[start:position + len(folded) + 140].replace("\n", " ").strip()
            else:
                snippet = document.title
            matches.append({**document.summary(), "snippet": snippet})
            if len(matches) >= limit:
                break
        return matches


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


class _Handler(BaseHTTPRequestHandler):
    server_version = "AI-SDLC-Knowledge-Preview/0.1"

    @property
    def catalog(self) -> KnowledgeCatalog:
        return self.server.catalog  # type: ignore[attr-defined]

    def _send(self, status: int, payload: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _error(self, status: int, message: str) -> None:
        self._send(status, _json_bytes({"error": message}), "application/json")

    def do_HEAD(self):  # noqa: N802
        self._route()

    def do_GET(self):  # noqa: N802
        self._route()

    def do_POST(self):  # noqa: N802
        self._error(405, "The preview is read-only.")

    def do_PUT(self):  # noqa: N802
        self._error(405, "The preview is read-only.")

    def do_DELETE(self):  # noqa: N802
        self._error(405, "The preview is read-only.")

    def _route(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(200, _asset("index.html"), "text/html")
            return
        if parsed.path.startswith("/assets/"):
            name = parsed.path.removeprefix("/assets/")
            if name not in {"app.js", "styles.css"}:
                self._error(404, "Not found.")
                return
            content_type = "text/javascript" if name.endswith(".js") else "text/css"
            self._send(200, _asset(name), content_type)
            return
        if not parsed.path.startswith("/api/"):
            self._error(404, "Not found.")
            return
        query = parse_qs(parsed.query, keep_blank_values=True)
        value = lambda name, default="": query.get(name, [default])[0]
        try:
            if parsed.path == "/api/health":
                self._send(200, _json_bytes(self.catalog.health()), "application/json")
            elif parsed.path == "/api/navigation":
                self._send(200, _json_bytes(self.catalog.navigation()), "application/json")
            elif parsed.path == "/api/document":
                document = self.catalog.document(value("key"))
                self._send(200, _json_bytes({**document.summary(), "metadata": document.metadata,
                                             "headings": list(document.headings), "content": document.content}), "application/json")
            elif parsed.path == "/api/search":
                try:
                    limit = min(100, max(1, int(value("limit", "30"))))
                except ValueError:
                    limit = 30
                results = self.catalog.search(value("q"), value("collection") or None, limit)
                self._send(200, _json_bytes({"query": value("q"), "results": results}), "application/json")
            elif parsed.path == "/api/refresh":
                self._send(200, _json_bytes(self.catalog.refresh()), "application/json")
            else:
                self._error(404, "Not found.")
        except KeyError:
            self._error(404, "Document not found.")
        except (OSError, ValueError):
            self._error(400, "The request could not be read.")

    def log_message(self, format: str, *args) -> None:
        return


def _asset(name: str) -> bytes:
    path = Path(__file__).with_name("static") / name
    return path.read_bytes()


class _PreviewServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, catalog: KnowledgeCatalog):
        super().__init__(address, _Handler)
        self.catalog = catalog


def serve(workspace: str | Path, *, host: str = "127.0.0.1", port: int = 8765, open_browser: bool = False) -> int:
    """Serve the read-only preview until interrupted."""
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise WorkbenchError("The knowledge preview binds to localhost only.")
    if not 0 <= port <= 65535:
        raise WorkbenchError("The preview port must be between 0 and 65535.")
    server = _PreviewServer((host, port), KnowledgeCatalog(workspace))
    address = server.server_address
    display_host = "localhost" if host in {"127.0.0.1", "::1"} else host
    url = f"http://{display_host}:{address[1]}"
    print(f"Knowledge preview: {url}", flush=True)
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 130
    finally:
        server.server_close()
    return 0
