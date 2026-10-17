"""Run explicitly configured connector bridges through workspace grants."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile

from ..models import Context, Operation, Resource
from .common import BuiltinProvider, ProviderError, object_schema, string_schema, timeout
from .robot import RobotTestingProvider


class ConnectorMcpProvider(BuiltinProvider):
    id = "connector.mcp"
    resource_kind = "connector"
    operations = {
        "list": Operation("list", "Discover connector tools and their execution grants.", object_schema()),
        "call": Operation("call", "Invoke an explicitly granted external connector tool.", object_schema({
            "tool": string_schema(maximum=256), "arguments": {"type": "object"}}, ("tool",)), mutating=True),
    }
    connectors = {"ado", "confluence", "scwiki", "nexus", "sonar", "messaging", "web"}
    max_response_bytes = 4 * 1024 * 1024
    limitations = [
        "Connector results do not establish approved business behavior.",
        "Connector results are action evidence, not preserved raw source snapshots.",
    ]

    def _configuration(self, resource: Resource) -> tuple[list[str], str, list[str]]:
        if set(resource.config) - {"command", "connector", "allowed_tools"}:
            raise ProviderError("INVALID_CONFIGURATION", "The connector resource contains an unsupported setting.")
        command = resource.config.get("command")
        if (not isinstance(command, list) or not 1 <= len(command) <= 256 or
                any(not isinstance(value, str) or not 1 <= len(value) <= 8192 or "\x00" in value
                    for value in command)):
            raise ProviderError("INVALID_CONFIGURATION", "Configure the connector command as an explicit argument list.")
        connector = resource.config.get("connector")
        if not isinstance(connector, str) or connector not in self.connectors:
            raise ProviderError("INVALID_CONFIGURATION", "Configure a supported connector name.")
        allowed = resource.config.get("allowed_tools", [])
        if (not isinstance(allowed, list) or len(allowed) > 4096 or
                any(not isinstance(name, str) or not 1 <= len(name) <= 256 or "\x00" in name
                    for name in allowed) or len(set(allowed)) != len(allowed)):
            raise ProviderError("INVALID_CONFIGURATION", "Connector allowed_tools must contain unique exact tool names.")
        return command, connector, allowed

    def _failure(self, code: str, message: str, *, status: str = "ERROR", **details) -> dict:
        return {"status": status, "code": code, "message": message,
                "limitations": list(self.limitations), **details}

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        command, connector, allowed = self._configuration(resource)
        if operation == "call" and arguments["tool"] not in allowed:
            return self._failure("TOOL_NOT_GRANTED", "The connector resource does not grant this exact tool name.")
        request = {"connector": connector, "operation": operation}
        if operation == "call":
            values = arguments.get("arguments", {})
            if not isinstance(values, dict):
                raise ProviderError("INVALID_ARGUMENT", "Connector tool arguments must be an object.")
            request.update(tool=arguments["tool"], arguments=values)
        seconds = timeout(context)
        timed_out = False
        cleanup_limit = None
        with tempfile.TemporaryFile() as incoming, tempfile.TemporaryFile() as outgoing:
            incoming.write(json.dumps(request, allow_nan=False).encode("utf-8"))
            incoming.seek(0)
            try:
                process = subprocess.Popen([*command, "--workspace", str(context.workspace_root)],
                                           cwd=context.workspace_root, stdin=incoming, stdout=outgoing,
                                           stderr=subprocess.DEVNULL, shell=False,
                                           start_new_session=os.name == "posix")
            except OSError:
                return self._failure("CONNECTOR_UNAVAILABLE",
                                     "The connector command could not start. Install its runtime and dependencies.")
            try:
                process.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                cleanup_limit = RobotTestingProvider._terminate(process, windows=os.name == "nt")
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    cleanup_limit = "The connector process did not confirm termination within five seconds."
            if timed_out:
                result = self._failure("CONNECTOR_TIMEOUT", "The connector exceeded the configured operation timeout.",
                                       status="TIMEOUT", timeout_seconds=seconds)
                if cleanup_limit:
                    result["cleanup_status"] = "UNKNOWN"
                    result["limitations"].append(cleanup_limit)
                return result
            if process.returncode != 0:
                return self._failure("CONNECTOR_FAILURE",
                                     "The connector command failed. Check root variables and install connector dependencies.",
                                     exit_code=process.returncode)
            outgoing.seek(0)
            raw = outgoing.read(self.max_response_bytes + 1)
        if len(raw) > self.max_response_bytes:
            return self._failure("RESPONSE_TOO_LARGE", "The connector response exceeds the four MiB limit.")
        try:
            payload = json.loads(raw)
            if not isinstance(payload, dict) or payload.get("status") != "SUCCEEDED":
                return self._failure("CONNECTOR_FAILURE", "The connector could not complete the requested operation.")
            json.dumps(payload, allow_nan=False)
        except (ValueError, UnicodeError):
            return self._failure("INVALID_RESPONSE", "The connector did not return a valid JSON result.")
        if operation == "list":
            tools = payload.get("tools")
            if (not isinstance(tools, list) or len(tools) > 4096 or
                    any(not isinstance(tool, dict) or not isinstance(tool.get("name"), str) or
                        not 1 <= len(tool["name"]) <= 256 or "\x00" in tool["name"] for tool in tools)):
                return self._failure("INVALID_RESPONSE", "The connector did not return a valid tool list.")
            return {"status": "SUCCEEDED", "connector": connector,
                    "tools": [{**tool, "allowed": tool["name"] in allowed} for tool in tools],
                    "limitations": list(self.limitations)}
        result = payload.get("result")
        if not isinstance(result, dict) or ("isError" in result and type(result["isError"]) is not bool):
            return self._failure("INVALID_RESPONSE", "The connector did not return a valid tool result.")
        return {"status": "FAILED" if result.get("isError", False) else "SUCCEEDED",
                "connector": connector, "tool": arguments["tool"], "result": result,
                "limitations": list(self.limitations)}
