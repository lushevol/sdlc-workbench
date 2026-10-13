"""Check CLI, MCP, and dashboard requests through public interfaces."""

import http.client
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from contextlib import redirect_stderr

from ai_sdlc_workbench.models import Operation
from ai_sdlc_workbench.mcp import McpServer, serve
from ai_sdlc_workbench.web import create_server

from support import WorkspaceTestCase


class InterfaceTests(WorkspaceTestCase):
    def test_cli_imports_and_runs_without_harness_runtime(self):
        source = Path(__file__).resolve().parents[1] / "src"
        environment = {**os.environ, "PYTHONPATH": str(source)}
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
        source = Path(__file__).resolve().parents[1] / "src"
        environment = {**os.environ, "PYTHONPATH": str(source)}
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

    def test_dashboard_requires_origin_and_token_before_running_action(self):
        server = self.start_dashboard()
        body = {"resource_id": self.resource_id("knowledge.local"), "operation": "list", "arguments": {}}
        status, payload = self.request(server, "POST", "/api/call", body)
        self.assertEqual(status, 403)
        self.assertEqual(self.workbench.runs(), [])
        base = f"http://127.0.0.1:{server.server_port}"
        headers = {"Origin": base, "X-CSRF-Token": server.csrf_token}
        status, payload = self.request(server, "POST", "/api/call", body, headers)
        self.assertEqual(status, 200, payload)
        self.assertEqual(payload["status"], "SUCCEEDED")
        self.assertEqual(self.workbench.run(payload["id"])["status"], "SUCCEEDED")
        status, _ = self.request(server, "POST", "/api/call", body,
                                 {**headers, "Origin": "http://untrusted.test"})
        self.assertEqual(status, 403)
        status, _ = self.request(server, "POST", "/api/call", body,
                                 {**headers, "X-CSRF-Token": "\u00e9-invalid"})
        self.assertEqual(status, 403)
        self.assertEqual(len(self.workbench.runs()), 1)

    def test_dashboard_blocks_untrusted_host_and_exposes_resource_status(self):
        server = self.start_dashboard()
        status, _ = self.request(server, "GET", "/api/status", headers={"Host": "untrusted.test"})
        self.assertEqual(status, 403)
        status, payload = self.request(server, "GET", "/api/status")
        self.assertEqual(status, 200)
        self.assertEqual(payload["workspace"]["name"], "Integration workspace")
        self.assertEqual(payload["csrf_token"], server.csrf_token)

    def start_dashboard(self):
        server = create_server(self.workbench, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(thread.join, 2)
        self.addCleanup(server.shutdown)
        return server

    def request(self, server, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        try:
            actual_headers = dict(headers or {})
            if body is not None:
                actual_headers.setdefault("Content-Type", "application/json")
            connection.request(method, path, body=json.dumps(body) if body is not None else None,
                               headers=actual_headers)
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()
