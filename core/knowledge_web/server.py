"""Small read-only HTTP preview for the Workbench knowledge collections."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from typing import Iterable
from urllib.parse import parse_qs, unquote, urlparse
import webbrowser

import yaml

from ..knowledge_layout import knowledge_layout
from ..models import WorkbenchError


MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
TEXT_SUFFIXES = frozenset({".md", ".markdown", ".txt", ".json", ".yaml", ".yml"})
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
        if resolved != path or not resolved.is_relative_to(workspace / "knowledge") or not resolved.is_file():
            return None
        raw = resolved.read_bytes()
    except (OSError, ValueError, RuntimeError):
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
    try:
        resolved = spec.path.resolve()
    except (OSError, RuntimeError):
        return
    if resolved != spec.path:
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
                                 if name not in SKIP_PARTS and not name.startswith(".")
                                 and not (base / name).is_symlink()
                                 and (spec.collection != "records" or name not in {"evidence", "llm-wiki"}))
        for filename in sorted(filenames):
            path = base / filename
            if path.is_symlink() or filename.startswith(".") or path.suffix.casefold() not in spec.extensions:
                continue
            if filename == "AGENTS.md" or (spec.collection == "wiki" and filename == "log.md"):
                continue
            yield path


class KnowledgeCatalog:
    """Immutable document snapshots rooted in approved workspace collections."""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).expanduser().resolve()
        self._lock = threading.RLock()
        self._roots = self._root_specs()
        self._documents: dict[str, Document] = {}
        self._paths: dict[str, str] = {}
        self._aliases: dict[str, str] = {}
        self.refresh()

    def _root_specs(self) -> tuple[RootSpec, ...]:
        records, evidence = knowledge_layout(self.workspace)
        markdown = frozenset({".md", ".markdown"})
        specs = [RootSpec("records", "Canonical records", records, markdown)]
        wiki = self.workspace / "knowledge/llm-wiki/wiki"
        specs.append(RootSpec("wiki", "Derived wiki", wiki, markdown))
        for name in ("README.md", "index.md"):
            path = self.workspace / "knowledge" / name
            if path.parent != records:
                specs.append(RootSpec("guide", "Knowledge guide", path, markdown))
        if evidence.is_relative_to(self.workspace / "knowledge"):
            for name in ("sources", "selections", "findings", "README.md", "manifest.yaml"):
                specs.append(RootSpec("evidence", "Sources and evidence", evidence / name, TEXT_SUFFIXES))
        return tuple(specs)

    def _source_aliases(self, paths: dict[str, str]) -> dict[str, str]:
        manifest = self.workspace / "knowledge/llm-wiki/source-manifest.json"
        try:
            if manifest.resolve(strict=True) != manifest:
                return {}
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError, RuntimeError):
            return {}
        aliases = {}
        entries = payload.get("sources", []) if isinstance(payload, dict) else []
        for entry in entries if isinstance(entries, list) else []:
            if not isinstance(entry, dict):
                continue
            origin, name = entry.get("origin"), entry.get("doc_name")
            if not isinstance(origin, str) or origin not in paths or not isinstance(name, str) or not name or "/" in name or "\\" in name:
                continue
            if not origin.startswith("knowledge/records/"):
                continue
            for folder in ("raw", "wiki/sources"):
                alias = self.workspace / "knowledge/llm-wiki" / folder / f"{name}.md"
                try:
                    if alias.parent.resolve(strict=True) != alias.parent:
                        continue
                    if alias.is_symlink() and alias.resolve(strict=True) == self.workspace / origin:
                        aliases[alias.relative_to(self.workspace).as_posix()] = paths[origin]
                except (OSError, ValueError, RuntimeError):
                    continue
        return aliases

    def refresh(self) -> dict:
        fresh: dict[str, Document] = {}
        roots = self._root_specs()
        for spec in roots:
            for path in _walk(spec):
                document = _read_document(spec.collection, path, self.workspace)
                if document is not None:
                    fresh[document.key] = document
        paths = {document.path: document.key for document in fresh.values()}
        aliases = self._source_aliases(paths)
        with self._lock:
            self._roots = roots
            self._documents = fresh
            self._paths = paths
            self._aliases = aliases
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

    def resolve(self, key: str, target: str) -> dict:
        document = self.document(key)
        parsed = urlparse(target)
        if parsed.netloc or parsed.scheme not in {"", "wiki"} or "\\" in target or "\x00" in target:
            raise KeyError(target)
        path, fragment = unquote(parsed.path), unquote(parsed.fragment)
        if not path:
            return {"key": key, "fragment": fragment}
        wiki_root = "knowledge/llm-wiki/wiki"
        if parsed.scheme == "wiki":
            candidates = [posixpath.join(wiki_root, path)]
        elif path.startswith("/"):
            candidates = [path.lstrip("/")]
        else:
            candidates = [posixpath.join(posixpath.dirname(document.path), path)]
            if document.collection == "wiki":
                candidates.append(posixpath.join(wiki_root, path))
        with self._lock:
            for candidate in candidates:
                normalized = posixpath.normpath(candidate)
                for item in (normalized, normalized + ".md", normalized.rstrip("/") + "/index.md"):
                    found = self._paths.get(item) or self._aliases.get(item)
                    if found:
                        return {"key": found, "fragment": fragment}
            if parsed.scheme == "wiki" and "/" not in path:
                matches = [item.key for item in self._documents.values()
                           if item.collection == "wiki" and Path(item.path).stem == path.removesuffix(".md")]
                if len(matches) == 1:
                    return {"key": matches[0], "fragment": fragment}
        raise KeyError(target)

    def graph_bytes(self) -> bytes:
        path = self.workspace / "knowledge/llm-wiki/output/visualize/graph.html"
        try:
            if path.resolve(strict=True) != path:
                raise KeyError("graph")
            return path.read_bytes()
        except (OSError, RuntimeError) as error:
            raise KeyError("graph") from error

    def graph(self) -> dict:
        try:
            payload = self.graph_bytes()
        except KeyError:
            return {"available": False, "reason": "The existing wiki graph has not been generated in knowledge/llm-wiki/output/visualize/."}
        return {"available": True, "url": "/wiki-graph", "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload), "description": "Existing OpenKB graph snapshot of summaries, concepts, and entities."}

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

    def _send(self, status: int, payload: bytes, content_type: str, *, graph: bool = False) -> None:
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        policy = ("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; "
                  "base-uri 'none'; form-action 'none'; frame-ancestors 'self'; sandbox allow-scripts" if graph else
                  "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
                  "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.send_header("Content-Security-Policy", policy)
        self.send_header("X-Content-Type-Options", "nosniff")
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
        try:
            host = urlparse("//" + self.headers.get("Host", "")).hostname
        except ValueError:
            host = None
        if host not in {"127.0.0.1", "localhost", "::1"}:
            self._error(403, "The knowledge preview accepts localhost requests only.")
            return
        parsed = urlparse(self.path)
        if parsed.path == "/wiki-graph":
            try:
                self._send(200, self.catalog.graph_bytes(), "text/html", graph=True)
            except KeyError:
                self._error(404, "Wiki graph not found.")
            return
        if parsed.path == "/":
            self._send(200, _asset("index.html"), "text/html")
            return
        if parsed.path.startswith("/assets/"):
            name = parsed.path.removeprefix("/assets/")
            if name not in {"app.js", "styles.css", "marked.umd.js"}:
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
            elif parsed.path == "/api/resolve":
                self._send(200, _json_bytes(self.catalog.resolve(value("from"), value("target"))), "application/json")
            elif parsed.path == "/api/graph":
                self._send(200, _json_bytes(self.catalog.graph()), "application/json")
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
