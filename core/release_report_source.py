"""Collection-scoped sessions over the native connector's raw report readers."""

from __future__ import annotations

from concurrent.futures import Future
import hashlib
import json
from pathlib import Path
import subprocess
import threading
import time
import uuid

from .models import Resource, WorkbenchError
from .providers.connectors import ConnectorMcpProvider


class ReportReadError(WorkbenchError):
    def __init__(self, code: str, message: str = "The report source read failed."):
        super().__init__(message)
        self.code = code


class ConnectorSession:
    """One workspace-bound child process, with correlated concurrent requests."""

    def __init__(self, resource: Resource, workspace: Path, directory: Path, *,
                 concurrency: int, deadline: float, request_timeout: float):
        if resource.provider != "connector.mcp" or "call" not in resource.allowed_operations:
            raise ReportReadError("TOOL_NOT_GRANTED")
        command, connector, allowed = ConnectorMcpProvider()._configuration(resource)
        if connector not in {"ado", "sonar"}:
            raise ReportReadError("INVALID_CONFIGURATION")
        self.allowed = frozenset(allowed)
        self.connector = connector
        self.workspace = workspace.resolve()
        self.directory = directory.resolve()
        self.deadline = deadline
        self.metrics: dict = {}
        self._write_lock = threading.Lock()
        self._pending_lock = threading.Lock()
        self._pending: dict[str, Future] = {}
        self._closed = False
        # Keep custom commands usable by fixture providers. Native installations
        # select the session sibling of their already registered bridge command.
        command = list(command)
        for index, value in enumerate(command):
            if Path(value).name == "bridge.js":
                command[index] = str(Path(value).with_name("release-session.js"))
        try:
            self.process = subprocess.Popen(
                [*command, "--workspace", str(self.workspace), "--connector", connector],
                cwd=self.workspace, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1,
            )
        except OSError as error:
            raise ReportReadError("CONNECTOR_UNAVAILABLE") from error
        self._reader = threading.Thread(target=self._read_responses, daemon=True)
        self._reader.start()
        try:
            response = self._rpc({"operation": "init", "allowed_tools": sorted(self.allowed),
                                  "run_dir": str(self.directory), "concurrency": concurrency,
                                  "request_timeout_seconds": request_timeout,
                                  "deadline_seconds": max(0.01, deadline - time.monotonic())})
            if response.get("status") != "SUCCEEDED":
                raise ReportReadError(response.get("code", "CONNECTOR_FAILURE"))
            self.metrics = response.get("metrics", {})
            self.endpoint = response.get("endpoint")
        except Exception:
            self.close(force=True)
            raise

    def _read_responses(self):
        try:
            while True:
                line = self.process.stdout.readline(4 * 1024 * 1024 + 1)
                if not line:
                    break
                if len(line.encode("utf-8")) > 4 * 1024 * 1024:
                    raise ValueError("Response frame exceeds the limit.")
                payload = json.loads(line)
                if not isinstance(payload, dict):
                    raise ValueError("Invalid response frame.")
                with self._pending_lock:
                    pending = self._pending.pop(str(payload.get("id")), None)
                if pending is not None:
                    pending.set_result(payload)
        except (ValueError, OSError, UnicodeError):
            pass
        finally:
            with self._pending_lock:
                waiting = list(self._pending.values())
                self._pending.clear()
            for pending in waiting:
                if not pending.done():
                    pending.set_exception(ReportReadError("CONNECTOR_FAILURE"))

    def _rpc(self, request: dict, *, closing=False) -> dict:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0 and not closing:
            raise ReportReadError("DEADLINE_EXCEEDED")
        identifier = uuid.uuid4().hex
        pending = Future()
        with self._pending_lock:
            self._pending[identifier] = pending
        try:
            with self._write_lock:
                if self._closed:
                    raise ReportReadError("CONNECTOR_FAILURE")
                self.process.stdin.write(json.dumps({"id": identifier, **request}, allow_nan=False) + "\n")
                self.process.stdin.flush()
            return pending.result(timeout=max(0.01, remaining) if not closing else 3)
        except TimeoutError as error:
            raise ReportReadError("DEADLINE_EXCEEDED") from error
        except (OSError, ValueError) as error:
            raise ReportReadError("CONNECTOR_FAILURE") from error
        finally:
            with self._pending_lock:
                self._pending.pop(identifier, None)

    def call(self, tool: str, arguments: dict, destination: Path) -> dict:
        # The parent checks grants before serving any cache hit. Check again at
        # the process boundary; the child independently enforces the same list.
        if tool not in self.allowed:
            raise ReportReadError("TOOL_NOT_GRANTED")
        response = self._rpc({"operation": "call", "tool": tool,
                              "arguments": arguments, "evidence_path": str(destination)})
        if isinstance(response.get("metrics"), dict):
            self.metrics = response["metrics"]
        artifact = response.get("artifact")
        if artifact:
            self.verify_artifact(artifact, destination)
        return response

    def verify_artifact(self, artifact: dict, destination: Path):
        path = Path(artifact.get("path", ""))
        if (path != destination or path.is_symlink() or not path.resolve().is_relative_to(self.directory)
                or not path.is_file()):
            raise ReportReadError("INVALID_ARTIFACT")
        digest, size = hashlib.sha256(), 0
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
                size += len(chunk)
        if size != artifact.get("bytes") or digest.hexdigest() != artifact.get("sha256"):
            raise ReportReadError("INVALID_ARTIFACT")

    def close(self, *, force=False):
        if self._closed:
            return
        if not force and self.process.poll() is None:
            try:
                response = self._rpc({"operation": "close"}, closing=True)
                self.metrics = response.get("metrics", self.metrics)
            except (WorkbenchError, TimeoutError):
                pass
        self._closed = True
        try:
            self.process.stdin.close()
        except OSError:
            pass
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=3)
        self.process.stdout.close()
        self._reader.join(timeout=1)
