"""A newline JSON-RPC MCP interface with no external dependencies."""

from __future__ import annotations

import json
import sys
from contextlib import redirect_stdout
from typing import TextIO

from .models import WorkbenchError
from .runtime import Workbench


MAX_MESSAGE_BYTES = 1024 * 1024
PROTOCOLS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
TOOLS = [
    {"name": "workbench_status", "description": "Describe workspace resources, providers, and available operations.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "workbench_call", "description": "Run a permitted resource operation and retain its action record.",
     "inputSchema": {"type": "object", "properties": {
         "resource_id": {"type": "string", "minLength": 1},
         "operation": {"type": "string", "minLength": 1},
         "arguments": {"type": "object"}},
         "required": ["resource_id", "operation"], "additionalProperties": False}},
    {"name": "workbench_runs", "description": "List retained action records or read one action record.",
     "inputSchema": {"type": "object", "properties": {
         "run_id": {"type": "string", "minLength": 1},
         "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20}},
         "additionalProperties": False}},
    {"name": "workbench_skills", "description": "List workspace skills or read one skill procedure.",
     "inputSchema": {"type": "object", "properties": {"skill_id": {"type": "string", "minLength": 1}},
                     "additionalProperties": False}},
]


def _error(identifier: object, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": identifier, "error": {"code": code, "message": message}}


def _validate(name: str, arguments: object) -> dict:
    if not isinstance(arguments, dict):
        raise WorkbenchError("Tool arguments must be a JSON object.")
    descriptor = next((item for item in TOOLS if item["name"] == name), None)
    if descriptor is None:
        raise WorkbenchError("The requested tool does not exist.")
    schema = descriptor["inputSchema"]
    if set(arguments) - set(schema["properties"]):
        raise WorkbenchError("Tool arguments contain an unknown field.")
    for key in schema.get("required", []):
        if key not in arguments:
            raise WorkbenchError(f"Tool arguments require {key}.")
    for key, value in arguments.items():
        kind = schema["properties"][key]["type"]
        if kind == "string" and (not isinstance(value, str) or not value.strip()):
            raise WorkbenchError(f"{key} must be a nonempty string.")
        if kind == "object" and not isinstance(value, dict):
            raise WorkbenchError(f"{key} must be a JSON object.")
        if kind == "integer" and (type(value) is not int or not 1 <= value <= 100):
            raise WorkbenchError(f"{key} must be an integer between 1 and 100.")
    return arguments


def _content(value: object, *, failed: bool = False) -> dict:
    result = {"content": [{"type": "text", "text":
                          value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)}],
              "isError": failed}
    if isinstance(value, dict):
        result["structuredContent"] = value
    return result


class McpServer:
    def __init__(self, workbench: Workbench):
        self.workbench = workbench

    def call_tool(self, name: str, arguments: object) -> dict:
        values = _validate(name, arguments)
        if name == "workbench_status":
            return _content(self.workbench.describe())
        if name == "workbench_call":
            result = self.workbench.call(values["resource_id"], values["operation"], values.get("arguments", {}))
            return _content(result, failed=result.get("status") != "SUCCEEDED")
        if name == "workbench_runs":
            result = (self.workbench.run(values["run_id"]) if "run_id" in values else
                      {"runs": self.workbench.runs(values.get("limit", 20))})
            return _content(result)
        if "skill_id" in values:
            return _content(self.workbench.skill_read(values["skill_id"]))
        return _content({"skills": self.workbench.skill_list()})

    def handle(self, request: object) -> dict | None:
        if not isinstance(request, dict):
            return _error(None, -32600, "The request must be a JSON-RPC object.")
        identifier = request.get("id")
        if request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
            return _error(identifier, -32600, "The JSON-RPC request is invalid.")
        if "id" in request and (type(identifier) not in {str, int} and identifier is not None):
            return _error(None, -32600, "The request ID is invalid.")
        if "id" not in request:
            return None
        params = request.get("params", {})
        if not isinstance(params, dict):
            return _error(identifier, -32602, "Request parameters must be a JSON object.")
        try:
            method = request["method"]
            if method == "initialize":
                requested = params.get("protocolVersion", PROTOCOLS[0])
                result = {"protocolVersion": requested if requested in PROTOCOLS else PROTOCOLS[0],
                          "capabilities": {"tools": {"listChanged": False}},
                          "serverInfo": {"name": "ai-sdlc-workbench", "version": "0.1.0"},
                          "instructions": "Read resource operation schemas before calling tools. Retained actions identify results and evidence limits."}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                if not isinstance(params.get("name"), str):
                    return _error(identifier, -32602, "A tool name is required.")
                result = self.call_tool(params["name"], params.get("arguments", {}))
            else:
                return _error(identifier, -32601, "The requested method is not supported.")
            return {"jsonrpc": "2.0", "id": identifier, "result": result}
        except WorkbenchError as error:
            if request["method"] == "tools/call":
                return {"jsonrpc": "2.0", "id": identifier,
                        "result": _content({"error": {"code": "WORKBENCH_ERROR", "message": str(error)}}, failed=True)}
            return _error(identifier, -32602, "The request parameters are invalid.")
        except Exception:
            return _error(identifier, -32603, "The operation could not complete.")


def serve(workbench: Workbench, input_stream: TextIO | None = None,
          output_stream: TextIO | None = None) -> None:
    source = input_stream if input_stream is not None else sys.stdin
    target = output_stream if output_stream is not None else sys.stdout
    server = McpServer(workbench)
    while True:
        line = source.readline(MAX_MESSAGE_BYTES + 1)
        if not line:
            return
        if len(line.encode("utf-8")) > MAX_MESSAGE_BYTES:
            if not line.endswith("\n"):
                while line and not line.endswith("\n"):
                    line = source.readline(MAX_MESSAGE_BYTES + 1)
            response = _error(None, -32700, "The message exceeds the size limit.")
        elif not line.strip():
            continue
        else:
            try:
                request = json.loads(line)
            except (ValueError, TypeError):
                response = _error(None, -32700, "The message does not contain valid JSON.")
            else:
                # Provider diagnostics must not corrupt the MCP output stream.
                with redirect_stdout(sys.stderr):
                    response = server.handle(request)
        if response is not None:
            target.write(json.dumps(response, ensure_ascii=False) + "\n")
            target.flush()
