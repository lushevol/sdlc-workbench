"""Named configured test commands with retained output and timeout cleanup."""

from __future__ import annotations

import os
import signal
import subprocess
import sys

from ..models import Context, Operation, Resource
from .common import BuiltinProvider, ProviderError, configured_path, object_schema, string_schema, timeout


class CommandTestingProvider(BuiltinProvider):
    id = "testing.command"
    resource_kind = "testing"
    operations = {
        "list": Operation("list", "List named configured test suites.", object_schema()),
        "run": Operation("run", "Run a named configured test suite.", object_schema({
            "suite": string_schema(maximum=256)}, ("suite",)), mutating=True),
    }

    def _suites(self, resource: Resource) -> dict:
        suites = resource.config.get("suites")
        if not isinstance(suites, dict) or not suites or len(suites) > 256:
            raise ProviderError("INVALID_CONFIGURATION", "The testing resource needs named command suites.")
        for name, command in suites.items():
            if (not isinstance(name, str) or not 1 <= len(name) <= 256 or "\x00" in name
                    or not isinstance(command, list) or not 1 <= len(command) <= 256
                    or any(not isinstance(item, str) or not item or len(item) > 8192 or "\x00" in item for item in command)):
                raise ProviderError("INVALID_CONFIGURATION", "A configured test suite is invalid.")
        return suites

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        suites = self._suites(resource)
        if operation == "list":
            return {"status": "SUCCEEDED", "suites": sorted(suites)}
        suite = arguments["suite"]
        if suite not in suites:
            raise ProviderError("UNKNOWN_SUITE", "The testing resource does not define this suite.")
        command = [sys.executable if item == "{python}" else item for item in suites[suite]]
        cwd = configured_path(resource, context)
        seconds = timeout(context)
        context.run_dir.mkdir(parents=True, exist_ok=True)
        stdout_path, stderr_path = context.run_dir / "stdout.txt", context.run_dir / "stderr.txt"
        timed_out = False
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                       shell=False, start_new_session=os.name == "posix")
            try:
                process.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                if os.name == "posix":
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                else:
                    process.kill()
                process.wait()
        return {"status": "TIMEOUT" if timed_out else "SUCCEEDED" if process.returncode == 0 else "FAILED",
                "suite": suite, "exit_code": process.returncode, "stdout_path": str(stdout_path),
                "stderr_path": str(stderr_path), "stdout_bytes": stdout_path.stat().st_size,
                "stderr_bytes": stderr_path.stat().st_size, "command": command, "cwd": str(cwd),
                "timeout_seconds": seconds}
