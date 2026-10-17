"""Check connector grants and subprocess boundaries without external systems."""

from contextlib import redirect_stdout
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

import jsonschema
import yaml

from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.context.catalogs import load_catalogs
from ai_sdlc_workbench.mcp import McpServer
from ai_sdlc_workbench.models import Resource
from ai_sdlc_workbench.providers.connectors import ConnectorMcpProvider
from ai_sdlc_workbench.runtime import Workbench


ROOT = Path(__file__).resolve().parents[1]


FAKE_BRIDGE = r'''
import json
import os
from pathlib import Path
import subprocess
import sys
import time

spec = json.loads(Path('bridge-spec.json').read_text())
request = json.load(sys.stdin)
Path('bridge-started').write_text('started')
print('PRIVATE_DIAGNOSTIC_SENTINEL', file=sys.stderr, flush=True)
mode = spec.get('mode')
if mode == 'timeout':
    subprocess.Popen([sys.executable, '-c',
        "import pathlib, time; time.sleep(2); pathlib.Path('escaped-child.txt').write_text('unexpected')"])
    time.sleep(30)
if mode == 'failure':
    print('PRIVATE_DIAGNOSTIC_SENTINEL')
    sys.exit(7)
if mode == 'malformed':
    print('PRIVATE_DIAGNOSTIC_SENTINEL')
    sys.exit(0)
if mode == 'oversized':
    print('x' * (4 * 1024 * 1024 + 1))
    sys.exit(0)
if 'response' in spec:
    response = spec['response']
elif request['operation'] == 'list':
    response = {'status': 'SUCCEEDED', 'tools': [
        {'name': 'read_item', 'description': 'Read one item.', 'inputSchema': {'type': 'object'}},
        {'name': 'write_item', 'description': 'Write one item.', 'inputSchema': {'type': 'object'}}]}
else:
    response = {'status': 'SUCCEEDED', 'result': {'content': [{'type': 'text', 'text': 'observed'}],
        'invocation': {'request': request, 'cwd': os.getcwd(), 'argv': sys.argv[1:],
                       'inherited': os.environ.get('CONNECTOR_FIXTURE_VALUE'),
                       'file_only_present': 'CONNECTOR_FILE_ONLY' in os.environ}}}
print(json.dumps(response))
'''


class ConnectorProviderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-connector-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.bridge = self.root / "bridge.py"
        self.bridge.write_text(FAKE_BRIDGE, encoding="utf-8")
        self.scenario()
        self.configuration = {"schema_version": 1, "id": "connector-fixture", "name": "Connector fixture",
                              "timeout_seconds": 10, "plugins": [], "resources": [{
                                  "id": "external", "kind": "connector", "provider": "connector.mcp",
                                  "environment": "offline", "allowed_operations": ["list", "call"],
                                  "config": {"command": [sys.executable, str(self.bridge)],
                                             "connector": "ado", "allowed_tools": ["read_item"]}}]}
        self.configure()

    def configure(self):
        (self.root / "workspace.json").write_text(json.dumps(self.configuration), encoding="utf-8")
        self.workbench = Workbench(self.root)

    def scenario(self, **spec):
        (self.root / "bridge-spec.json").write_text(json.dumps(spec), encoding="utf-8")

    def call(self, tool="read_item", arguments=None):
        values = {"tool": tool}
        if arguments is not None:
            values["arguments"] = arguments
        return self.workbench.call("external", "call", values)

    def test_granted_call_uses_workspace_and_retains_result_hashes(self):
        arguments = {"id": 17, "nested": {"values": [True, None, "literal"]}}
        action = self.call(arguments=arguments)
        self.assertEqual(action["status"], "SUCCEEDED", action)
        result = action["result"]
        invocation = result["result"]["invocation"]
        self.assertEqual(invocation["request"], {"connector": "ado", "operation": "call",
                                                 "tool": "read_item", "arguments": arguments})
        self.assertEqual(invocation["cwd"], str(self.root))
        self.assertEqual(invocation["argv"], ["--workspace", str(self.root)])
        self.assertIn("Connector results do not establish approved business behavior.", result["limitations"])
        self.assertEqual(self.workbench.run(action["id"])["result"], result)
        self.assertEqual(len(action["evidence"]), 1)
        saved = self.root / action["evidence"][0]["path"]
        self.assertEqual(hashlib.sha256(saved.read_bytes()).hexdigest(), action["evidence"][0]["sha256"])
        self.assertNotIn("PRIVATE_DIAGNOSTIC_SENTINEL", saved.read_text())

    def test_list_marks_each_tool_grant_without_enabling_other_tools(self):
        action = self.workbench.call("external", "list")
        self.assertEqual(action["status"], "SUCCEEDED")
        tools = action["result"]["tools"]
        self.assertEqual([(tool["name"], tool["allowed"]) for tool in tools],
                         [("read_item", True), ("write_item", False)])
        self.assertEqual(tools[0]["inputSchema"], {"type": "object"})
        description = self.workbench.describe()
        operation = next(item for item in description["resources"][0]["operations"] if item["name"] == "call")
        self.assertTrue(operation["mutating"])
        self.assertNotIn("config", description["resources"][0])

    def test_exact_tool_allowlist_denies_before_starting_process(self):
        for tool in ("write_item", "READ_ITEM", "read_*", "read_item "):
            with self.subTest(tool=tool), patch("ai_sdlc_workbench.providers.connectors.subprocess.Popen") as process:
                action = self.call(tool)
                process.assert_not_called()
                self.assertEqual(action["status"], "FAILED")
                self.assertEqual(action["result"]["code"], "TOOL_NOT_GRANTED")
                self.assertEqual(self.workbench.run(action["id"])["result"], action["result"])
        del self.configuration["resources"][0]["config"]["allowed_tools"]
        self.configure()
        with patch("ai_sdlc_workbench.providers.connectors.subprocess.Popen") as process:
            self.assertEqual(self.call()["result"]["code"], "TOOL_NOT_GRANTED")
            process.assert_not_called()
        self.assertFalse((self.root / "bridge-started").exists())

    def test_resource_operation_grant_denies_and_retains_without_spawning(self):
        self.configuration["resources"][0]["allowed_operations"] = ["list"]
        self.configure()
        with patch("ai_sdlc_workbench.providers.connectors.subprocess.Popen") as process:
            action = self.call()
            process.assert_not_called()
        self.assertEqual(action["status"], "DENIED")
        self.assertEqual(self.workbench.run(action["id"])["status"], "DENIED")

    def test_command_arguments_remain_literal_and_environment_is_inherited(self):
        literal = "$(touch shell-expanded) $CONNECTOR_FIXTURE_VALUE ~"
        self.configuration["resources"][0]["config"]["command"].append(literal)
        self.configure()
        (self.root / ".env").write_text("CONNECTOR_FIXTURE_VALUE=file\nCONNECTOR_FILE_ONLY=file\n", encoding="utf-8")
        with patch.dict(os.environ, {"CONNECTOR_FIXTURE_VALUE": "process"}):
            action = self.call()
        self.assertEqual(action["status"], "SUCCEEDED", action)
        invocation = action["result"]["result"]["invocation"]
        self.assertEqual(invocation["argv"], [literal, "--workspace", str(self.root)])
        self.assertEqual(invocation["inherited"], "process")
        self.assertFalse(invocation["file_only_present"])
        self.assertNotIn("CONNECTOR_FILE_ONLY", os.environ)
        self.assertFalse((self.root / "shell-expanded").exists())

    def test_nested_tool_error_propagates_through_mcp(self):
        self.scenario(response={"status": "SUCCEEDED", "result": {
            "isError": True, "content": [{"type": "text", "text": "Item unavailable."}]}})
        result = McpServer(self.workbench).call_tool("workbench_call", {
            "resource_id": "external", "operation": "call", "arguments": {"tool": "read_item"}})
        self.assertTrue(result["isError"])
        action = result["structuredContent"]
        self.assertEqual(action["status"], "FAILED")
        self.assertTrue(action["result"]["result"]["isError"])

    def test_cli_dispatches_connector_call_through_existing_interface(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(["--workspace", str(self.root), "call", "external", "call", "--args", '{"tool":"read_item"}'])
        self.assertEqual(code, 0)
        action = json.loads(stream.getvalue())
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertEqual(action["result"]["connector"], "ado")

    def test_startup_and_process_failures_suppress_raw_diagnostics(self):
        baseline = self.configuration["resources"][0]["config"]["command"]
        self.configuration["resources"][0]["config"]["command"] = [str(self.root / "missing-runtime")]
        self.configure()
        unavailable = self.call()
        self.assertEqual(unavailable["result"]["code"], "CONNECTOR_UNAVAILABLE")
        self.configuration["resources"][0]["config"]["command"] = baseline
        self.configure()
        for spec, code in (({"mode": "failure"}, "CONNECTOR_FAILURE"),
                           ({"mode": "malformed"}, "INVALID_RESPONSE"),
                           ({"response": {"status": "ERROR", "message": "PRIVATE_DIAGNOSTIC_SENTINEL"}}, "CONNECTOR_FAILURE")):
            with self.subTest(spec=spec):
                self.scenario(**spec)
                action = self.call()
                self.assertEqual(action["status"], "FAILED")
                self.assertEqual(action["result"]["code"], code)
                self.assertNotIn("PRIVATE_DIAGNOSTIC_SENTINEL", json.dumps(action))
                for evidence in action["evidence"]:
                    self.assertNotIn(b"PRIVATE_DIAGNOSTIC_SENTINEL", (self.root / evidence["path"]).read_bytes())

    def test_response_bound_and_malformed_results_fail_without_retaining_raw_output(self):
        cases = [({"mode": "oversized"}, "RESPONSE_TOO_LARGE"),
                 ({"response": []}, "CONNECTOR_FAILURE"),
                 ({"response": {"status": "SUCCEEDED"}}, "INVALID_RESPONSE"),
                 ({"response": {"status": "SUCCEEDED", "result": {"isError": "false"}}}, "INVALID_RESPONSE")]
        for spec, code in cases:
            with self.subTest(spec=spec):
                self.scenario(**spec)
                action = self.call()
                self.assertEqual(action["status"], "FAILED")
                self.assertEqual(action["result"]["code"], code)
                self.assertEqual(len(action["evidence"]), 1)
                self.assertLess(action["evidence"][0]["size_bytes"], 4096)
        self.scenario(response={"status": "SUCCEEDED", "tools": [{"description": "No name."}]})
        self.assertEqual(self.workbench.call("external", "list")["result"]["code"], "INVALID_RESPONSE")

    def test_invalid_configuration_and_arguments_fail_before_spawning(self):
        baseline = self.configuration["resources"][0]["config"]
        settings = [{**baseline, "command": "node bridge.js"}, {**baseline, "command": []},
                    {**baseline, "command": ["node", "invalid\x00path"]}, {**baseline, "connector": "unknown"},
                    {**baseline, "connector": "app-bridge"},
                    {**baseline, "allowed_tools": ["read_item", "read_item"]},
                    {**baseline, "allowed_tools": "*"}, {**baseline, "env": {"TOKEN": "invalid"}}]
        for config in settings:
            with self.subTest(config=config):
                self.configuration["resources"][0]["config"] = config
                self.configure()
                with patch("ai_sdlc_workbench.providers.connectors.subprocess.Popen") as process:
                    action = self.call()
                    process.assert_not_called()
                self.assertEqual(action["result"]["code"], "INVALID_CONFIGURATION")
        self.configuration["resources"][0]["config"] = baseline
        self.configure()
        for arguments in ({"tool": "read_item", "arguments": []}, {"tool": "read_item", "command": ["other"]}):
            with self.subTest(arguments=arguments), patch("ai_sdlc_workbench.providers.connectors.subprocess.Popen") as process:
                action = self.workbench.call("external", "call", arguments)
                process.assert_not_called()
                self.assertEqual(action["status"], "FAILED")

    def test_timeout_stops_descendants_and_retains_timeout_limit(self):
        self.scenario(mode="timeout")
        self.configuration["timeout_seconds"] = 1
        self.configure()
        action = self.call()
        self.assertEqual(action["status"], "FAILED")
        self.assertEqual(action["result"]["status"], "TIMEOUT")
        self.assertEqual(action["result"]["code"], "CONNECTOR_TIMEOUT")
        self.assertNotIn("PRIVATE_DIAGNOSTIC_SENTINEL", json.dumps(action))
        if os.name == "posix":
            time.sleep(1.2)
            self.assertFalse((self.root / "escaped-child.txt").exists())


class ConnectorExampleTests(unittest.TestCase):
    def test_connector_examples_match_catalog_and_provider_contracts(self):
        document = ROOT / "registry/examples/connectors.yaml"
        payload = yaml.safe_load(document.read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "registry/tools.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(payload)
        _, resources = load_catalogs(ROOT, {"tools": "registry/examples/connectors.yaml"})
        self.assertEqual(resources, payload["tools"])
        self.assertEqual({resource["config"]["connector"] for resource in resources}, ConnectorMcpProvider.connectors)
        for resource in resources:
            with self.subTest(resource=resource["id"]):
                self.assertEqual(resource["provider"], "connector.mcp")
                self.assertEqual(resource["kind"], "connector")
                self.assertLessEqual(set(resource["allowed_operations"]), ConnectorMcpProvider.operations.keys())
                ConnectorMcpProvider()._configuration(Resource(**resource))


@unittest.skipUnless(os.environ.get("WORKBENCH_CONNECTOR_INTEGRATION") == "1",
                     "Optional Node integration requires WORKBENCH_CONNECTOR_INTEGRATION=1.")
class NativeConnectorIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = shutil.which("node")
        cls.bridge = ROOT / "core/connectors/workbench/bridge.js"
        if not cls.node or not (ROOT / "node_modules/@modelcontextprotocol/sdk/package.json").is_file():
            raise unittest.SkipTest("Install Node.js and root npm dependencies for connector integration.")

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-native-connector-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.environment = {key: os.environ[key] for key in ("PATH", "SystemRoot") if key in os.environ}
        self.configuration = {"schema_version": 1, "id": "native-connector-fixture", "name": "Native connector fixture",
                              "timeout_seconds": 10, "plugins": [], "resources": []}

    def resource(self, connector, allowed_tools, *, identifier=None):
        return {"id": identifier or connector, "kind": "connector", "provider": "connector.mcp",
                "environment": "offline", "allowed_operations": ["list", "call"],
                "config": {"command": [self.node, str(self.bridge)], "connector": connector,
                           "allowed_tools": allowed_tools}}

    def configure(self, resources):
        self.configuration["resources"] = resources
        (self.root / "workspace.json").write_text(json.dumps(self.configuration), encoding="utf-8")
        self.workbench = Workbench(self.root)

    def test_example_grants_use_registered_native_tool_names(self):
        examples = yaml.safe_load((ROOT / "registry/examples/connectors.yaml").read_text(encoding="utf-8"))["tools"]
        self.configure([self.resource(item["config"]["connector"], item["config"]["allowed_tools"])
                        for item in examples])
        with patch.dict(os.environ, self.environment, clear=True):
            for example in examples:
                connector = example["config"]["connector"]
                with self.subTest(connector=connector):
                    action = self.workbench.call(connector, "list")
                    self.assertEqual(action["status"], "SUCCEEDED", action)
                    tools = action["result"]["tools"]
                    names = {tool["name"] for tool in tools}
                    self.assertTrue(names)
                    self.assertLessEqual(set(example["config"]["allowed_tools"]), names)
                    self.assertEqual({tool["name"] for tool in tools if tool["allowed"]},
                                     set(example["config"]["allowed_tools"]))

    def test_provider_bridge_services_use_root_variables_and_retain_observations(self):
        observed = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                observed.append({"path": self.path, "authorization": self.headers.get("Authorization")})
                if self.path.startswith("/api/projects/search"):
                    payload = {"components": [{"key": "fixture", "name": "Observed Sonar project"}]}
                elif self.path.startswith("/rest/api/space"):
                    payload = {"results": [{"key": "ROOT", "name": "Observed Confluence space"}]}
                else:
                    self.send_error(404)
                    return
                raw = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def log_message(self, *_):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        def close_server():
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        self.addCleanup(close_server)
        endpoint = f"http://127.0.0.1:{server.server_port}"
        (self.root / ".env").write_text(
            f"SONAR_BASE_URL={endpoint}\nSONAR_TOKEN=SONAR_FILE_CREDENTIAL\n"
            f"CONFLUENCE_BASE_URL={endpoint}\nCONFLUENCE_PAT=CONFLUENCE_FILE_CREDENTIAL\n", encoding="utf-8")
        self.configure([self.resource("sonar", ["sonar_search_projects"]),
                        self.resource("confluence", ["confluence_list_spaces"])])
        with patch.dict(os.environ, {**self.environment, "CONFLUENCE_PAT": "CONFLUENCE_PROCESS_CREDENTIAL"}, clear=True):
            sonar = self.workbench.call("sonar", "call", {"tool": "sonar_search_projects", "arguments": {"query": "fixture"}})
            confluence = self.workbench.call("confluence", "call", {"tool": "confluence_list_spaces"})
            invalid = self.workbench.call("sonar", "call", {"tool": "sonar_search_projects", "arguments": {"pageSize": "invalid"}})
        self.assertEqual(sonar["status"], "SUCCEEDED", sonar)
        self.assertEqual(confluence["status"], "SUCCEEDED", confluence)
        self.assertEqual(invalid["status"], "FAILED", invalid)
        self.assertEqual(len(observed), 2)
        self.assertTrue(observed[0]["path"].startswith("/api/projects/search"))
        self.assertIn("q=fixture", observed[0]["path"])
        self.assertEqual(observed[0]["authorization"], "Bearer SONAR_FILE_CREDENTIAL")
        self.assertTrue(observed[1]["path"].startswith("/rest/api/space"))
        self.assertEqual(observed[1]["authorization"], "Bearer CONFLUENCE_PROCESS_CREDENTIAL")
        for action, text in ((sonar, "Observed Sonar project"), (confluence, "Observed Confluence space")):
            with self.subTest(connector=action["result"]["connector"]):
                self.assertIn(text, action["result"]["result"]["content"][0]["text"])
                self.assertEqual(self.workbench.run(action["id"])["result"], action["result"])
                for evidence in action["evidence"]:
                    raw = (self.root / evidence["path"]).read_bytes()
                    self.assertEqual(hashlib.sha256(raw).hexdigest(), evidence["sha256"])
                    self.assertNotIn(b"CREDENTIAL", raw)
                self.assertNotIn("CREDENTIAL", json.dumps(action))


if __name__ == "__main__":
    unittest.main()
