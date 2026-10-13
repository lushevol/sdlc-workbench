"""Configured Git checkout operations without a command shell."""

from __future__ import annotations

import os
import re
import signal
import subprocess
import tempfile

from ..models import Context, Operation, Resource
from .common import BuiltinProvider, ProviderError, configured_path, object_schema, string_schema, timeout


def valid_ref(value: str) -> bool:
    return bool(value and not value.startswith(("-", "/", ".")) and not value.endswith(("/", ".", ".lock"))
                and not any(part in value for part in ("..", "@{", "//"))
                and not re.search(r"[\s~^:?*\[\\\x00-\x1f\x7f]", value))


class GitRepositoryProvider(BuiltinProvider):
    id = "repository.git"
    resource_kind = "repository"
    operations = {
        "status": Operation("status", "Inspect the configured checkout status.", object_schema()),
        "diff": Operation("diff", "Read a Git diff for specified revisions or files.", object_schema({
            "base": string_schema(maximum=256), "head": string_schema(maximum=256), "path": string_schema()})),
        "branch": Operation("branch", "Create a branch without switching the checkout.", object_schema({
            "name": string_schema(maximum=256), "start_point": string_schema(maximum=256)}, ("name",)), mutating=True),
    }

    def _git(self, resource: Resource, context: Context, arguments: list[str]) -> dict:
        path = configured_path(resource, context)
        marker = path / ".git"
        if not path.is_dir() or not (marker.is_file() or marker.is_dir()):
            raise ProviderError("INVALID_REPOSITORY", "The registered path must be an independent Git checkout.")
        executable = resource.config.get("git_executable", "git")
        if not isinstance(executable, str) or not executable or "\x00" in executable:
            raise ProviderError("INVALID_CONFIGURATION", "The Git executable setting is invalid.")
        seconds = timeout(context)
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        with tempfile.TemporaryFile() as stdout:
            process = subprocess.Popen([executable, "--no-optional-locks", "--literal-pathspecs", "-C", str(path), *arguments],
                                       stdout=stdout, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                       env=environment, start_new_session=os.name == "posix")
            try:
                process.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                if os.name == "posix":
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                else:
                    process.kill()
                process.wait()
                return {"status": "TIMEOUT", "message": "The Git operation exceeded its timeout."}
            if process.returncode:
                return {"status": "FAILED", "exit_code": process.returncode, "message": "Git could not complete the operation."}
            stdout.seek(0)
            raw = stdout.read(4 * 1024 * 1024 + 1)
        if len(raw) > 4 * 1024 * 1024:
            raise ProviderError("OUTPUT_TOO_LARGE", "The Git output exceeds the four MiB limit.")
        return {"status": "SUCCEEDED", "output": raw.decode("utf-8", errors="replace")}

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        for key in ("name", "base", "head", "start_point"):
            if key in arguments and not valid_ref(arguments[key]):
                raise ProviderError("INVALID_ARGUMENT", "A Git revision or branch name is invalid.")
        if operation == "status":
            result = self._git(resource, context, ["status", "--porcelain=v1", "--branch"])
            if result["status"] == "SUCCEEDED":
                result["status_text"] = result.pop("output")
            return result
        if operation == "branch":
            result = self._git(resource, context, ["branch", "--", arguments["name"], arguments.get("start_point", "HEAD")])
            if result["status"] == "SUCCEEDED":
                result.update(branch=arguments["name"], start_point=arguments.get("start_point", "HEAD"))
                result.pop("output")
            return result
        if "head" in arguments and "base" not in arguments:
            raise ProviderError("INVALID_ARGUMENT", "A head revision requires a base revision.")
        command = ["diff", "--no-ext-diff", "--no-textconv"]
        command.extend(arguments[key] for key in ("base", "head") if key in arguments)
        command.append("--")
        if "path" in arguments:
            path = arguments["path"]
            if path.startswith("-") or path.startswith(":") or path.startswith("/") or ".." in path.split("/"):
                raise ProviderError("INVALID_ARGUMENT", "The diff path must be a relative literal path.")
            command.append(path)
        result = self._git(resource, context, command)
        if result["status"] == "SUCCEEDED":
            result["diff"] = result.pop("output")
        return result
