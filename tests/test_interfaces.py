"""Check CLI and MCP requests through public interfaces."""

import io
import json
import os
import subprocess
import sys
from contextlib import redirect_stderr

from ai_sdlc_workbench.models import Operation
from ai_sdlc_workbench.mcp import McpServer, serve

from support import WorkspaceTestCase


class InterfaceTests(WorkspaceTestCase):
    def test_doctor_cli_reports_an_unconfigured_workspace_without_creating_state(self):
        missing = self.root.parent / "not-initialized"
        command = [sys.executable, "-m", "ai_sdlc_workbench", "--workspace", str(missing),
                   "doctor", "--profile", "core"]
        result = subprocess.run(command, cwd=self.root.parent, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["core_status"], "INCOMPLETE")
        self.assertEqual(report["integration_access"], "UNTESTED")
        self.assertFalse(missing.exists())

    def test_cli_imports_and_runs_without_harness_runtime(self):
        environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        command = [sys.executable, "-m", "ai_sdlc_workbench.cli", "--workspace", str(self.root)]
        status = subprocess.run(command + ["status"], cwd=self.root.parent,
                                env=environment, capture_output=True, text=True)
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertEqual(json.loads(status.stdout)["workspace"]["name"], "Integration workspace")
        call = subprocess.run(command + ["call", self.resource_id("knowledge.local"), "list"],
                              cwd=self.root.parent, env=environment, capture_output=True, text=True)
        self.assertEqual(call.returncode, 0, call.stderr)
        action = json.loads(call.stdout)
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertEqual(self.workbench.run(action["id"])["status"], "SUCCEEDED")
        invalid = subprocess.run(command + ["call", self.resource_id("knowledge.local"), "read",
                                           "--args", "[]"],
                                 cwd=self.root.parent, env=environment, capture_output=True, text=True)
        self.assertNotEqual(invalid.returncode, 0)
        self.assertEqual(json.loads(invalid.stdout)["error"]["code"], "WORKBENCH_ERROR")

    def test_mcp_startup_error_does_not_emit_protocol_output(self):
        environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        result = subprocess.run([sys.executable, "-m", "ai_sdlc_workbench.cli", "--workspace",
                                 str(self.root / "missing"), "mcp"],
                                cwd=self.root.parent, env=environment, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("MCP workspace could not load", result.stderr)

    def test_mcp_keeps_plugin_prints_out_of_protocol_output(self):
        class Provider:
            id = "example.printing"
            version = "1.0.0"
            resource_kind = "example"
            operations = {"check": Operation("check", "Return an operation result.", {"type": "object"})}

            def invoke(self, *_):
                print("plugin diagnostic")
                return {"status": "SUCCEEDED"}

        workbench = self.install_fixture_provider(Provider())
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
            "name": "workbench_call", "arguments": {"resource_id": "fixture", "operation": "check"}}}
        output, diagnostics = io.StringIO(), io.StringIO()
        with redirect_stderr(diagnostics):
            serve(workbench, io.StringIO(json.dumps(request) + "\n"), output)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0]["result"]["structuredContent"]["status"], "SUCCEEDED")
        self.assertIn("plugin diagnostic", diagnostics.getvalue())

    def test_mcp_line_protocol_recovers_after_parse_error_and_ignores_notifications(self):
        requests = ["invalid JSON", json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2025-03-26"}}),
                    json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
                    json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                        "name": "workbench_call", "arguments": {
                            "resource_id": self.resource_id("knowledge.local"), "operation": "list"}}})]
        output = io.StringIO()
        serve(self.workbench, io.StringIO("\n".join(requests) + "\n"), output)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(len(responses), 3)
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[1]["result"]["protocolVersion"], "2025-03-26")
        action = responses[2]["result"]["structuredContent"]
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertFalse(responses[2]["result"]["isError"])

    def test_mcp_reports_invalid_tool_arguments_and_unknown_methods(self):
        server = McpServer(self.workbench)
        invalid = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
            "name": "workbench_call", "arguments": {"operation": "list"}}})
        self.assertTrue(invalid["result"]["isError"])
        unknown = server.handle({"jsonrpc": "2.0", "id": 2, "method": "missing"})
        self.assertEqual(unknown["error"]["code"], -32601)
        self.assertEqual(self.workbench.runs(), [])
