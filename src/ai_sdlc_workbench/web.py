"""Loopback dashboard for a local workspace."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import threading
from urllib.parse import parse_qs, unquote, urlsplit

from .models import WorkbenchError
from .runtime import Workbench


MAX_REQUEST_BYTES = 1024 * 1024


class WorkbenchHttpServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, workbench: Workbench, port: int):
        self.workbench = workbench
        self.csrf_token = secrets.token_urlsafe(32)
        self.csp_nonce = secrets.token_urlsafe(24)
        self.action_lock = threading.Lock()
        super().__init__(("127.0.0.1", port), WorkbenchHandler)


class WorkbenchHandler(BaseHTTPRequestHandler):
    server: WorkbenchHttpServer
    server_version = "AI-SDLC-Workbench"

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(10)

    def log_message(self, format: str, *args: object) -> None:
        pass

    def _host(self) -> str | None:
        hosts = self.headers.get_all("Host", [])
        if len(hosts) != 1:
            return None
        port = self.server.server_address[1]
        permitted = {f"127.0.0.1:{port}", f"localhost:{port}"}
        if port == 80:
            permitted.update({"127.0.0.1", "localhost"})
        return hosts[0] if hosts[0] in permitted else None

    def _send(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Content-Security-Policy", "default-src 'none'; connect-src 'self'; "
                         f"script-src 'nonce-{self.server.csp_nonce}'; style-src 'unsafe-inline'; "
                         "img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, value: object) -> None:
        self._send(status, json.dumps(value, ensure_ascii=False).encode("utf-8"))

    def _error(self, status: int, code: str, message: str) -> None:
        self._json(status, {"error": {"code": code, "message": message}})

    def do_GET(self) -> None:
        if self._host() is None:
            self._error(403, "FORBIDDEN", "The request host is not permitted.")
            return
        route = urlsplit(self.path)
        workbench = self.server.workbench
        try:
            if route.path == "/":
                path = Path(__file__).parent / "static" / "index.html"
                document = path.read_text(encoding="utf-8")
                document = document.replace("__CSRF_TOKEN__", self.server.csrf_token)
                document = document.replace("__CSP_NONCE__", self.server.csp_nonce)
                self._send(200, document.encode("utf-8"), "text/html; charset=utf-8")
            elif route.path == "/api/status":
                self._json(200, {**workbench.describe(), "csrf_token": self.server.csrf_token})
            elif route.path == "/api/runs":
                values = parse_qs(route.query)
                if set(values) - {"limit"} or len(values.get("limit", [])) > 1:
                    raise WorkbenchError("Invalid query.")
                try:
                    limit = int(values.get("limit", ["20"])[0])
                except ValueError as error:
                    raise WorkbenchError("Invalid query.") from error
                if not 1 <= limit <= 100:
                    raise WorkbenchError("Invalid query.")
                self._json(200, {"runs": workbench.runs(limit)})
            elif route.path.startswith("/api/runs/"):
                identifier = unquote(route.path[len("/api/runs/"):])
                if not identifier or "/" in identifier:
                    self._error(404, "NOT_FOUND", "The action record was not found.")
                    return
                self._json(200, workbench.run(identifier))
            elif route.path == "/api/skills":
                self._json(200, {"skills": workbench.skill_list()})
            elif route.path.startswith("/api/skills/"):
                identifier = unquote(route.path[len("/api/skills/"):])
                self._json(200, {"id": identifier, "content": workbench.skill_read(identifier)})
            else:
                self._error(404, "NOT_FOUND", "The requested page was not found.")
        except WorkbenchError:
            self._error(400, "INVALID_REQUEST", "The requested resource or arguments are invalid.")
        except Exception:
            self._error(500, "INTERNAL_ERROR", "The request could not complete.")

    def do_POST(self) -> None:
        host = self._host()
        origins = self.headers.get_all("Origin", [])
        tokens = self.headers.get_all("X-CSRF-Token", [])
        if (host is None or origins != [f"http://{host}"] or len(tokens) != 1 or
                not secrets.compare_digest(tokens[0].encode("utf-8"), self.server.csrf_token.encode("utf-8"))):
            self._error(403, "FORBIDDEN", "The request origin or session token is invalid.")
            return
        if urlsplit(self.path).path != "/api/call":
            self._error(404, "NOT_FOUND", "The requested operation was not found.")
            return
        content_types = self.headers.get_all("Content-Type", [])
        if (len(content_types) != 1 or content_types[0].split(";", 1)[0].strip().lower() != "application/json"):
            self._error(415, "UNSUPPORTED_MEDIA_TYPE", "Use an application/json request body.")
            return
        lengths = self.headers.get_all("Content-Length", [])
        if self.headers.get_all("Transfer-Encoding") or len(lengths) != 1 or not lengths[0].isdigit():
            self._error(400, "INVALID_REQUEST", "A valid request length is required.")
            return
        length = int(lengths[0])
        if length > MAX_REQUEST_BYTES:
            self._error(413, "REQUEST_TOO_LARGE", "The request exceeds the size limit.")
            return
        try:
            body = self.rfile.read(length)
            if len(body) != length:
                raise ValueError("Incomplete body.")
            payload = json.loads(body)
            if (not isinstance(payload, dict) or set(payload) - {"resource_id", "operation", "arguments"} or
                    not isinstance(payload.get("resource_id"), str) or not payload["resource_id"].strip() or
                    not isinstance(payload.get("operation"), str) or not payload["operation"].strip() or
                    not isinstance(payload.get("arguments", {}), dict)):
                raise ValueError("Invalid payload.")
        except (ValueError, UnicodeError, OSError):
            self._error(400, "INVALID_REQUEST", "The request body must contain valid operation arguments.")
            return
        try:
            with self.server.action_lock:
                result = self.server.workbench.call(payload["resource_id"], payload["operation"],
                                                    payload.get("arguments", {}))
            self._json(200, result)
        except WorkbenchError:
            self._error(400, "INVALID_REQUEST", "The requested resource or arguments are invalid.")
        except Exception:
            self._error(500, "INTERNAL_ERROR", "The operation could not complete.")


def create_server(workbench: Workbench, port: int = 8765) -> WorkbenchHttpServer:
    if type(port) is not int or not 0 <= port <= 65535:
        raise WorkbenchError("The port must be an integer between 0 and 65535.")
    return WorkbenchHttpServer(workbench, port)


def serve(workbench: Workbench, port: int = 8765) -> None:
    server = create_server(workbench, port)
    print(f"AI-SDLC Workbench: http://127.0.0.1:{server.server_address[1]}", flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
