"""Run local providers against isolated files and a mock service registry."""

import hashlib
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
from unittest.mock import patch

from ai_sdlc_workbench.runtime import Workbench

from support import WorkspaceTestCase


class ProviderTests(WorkspaceTestCase):
    def test_knowledge_ingest_search_and_read_preserve_exact_source(self):
        content = "# Release rule\nAn order with status READY can proceed.\n"
        written = self.call("knowledge.local", "ingest", {"path": "rules/release.md", "content": content})
        self.assertEqual(written["status"], "SUCCEEDED")
        document = written["result"]["document"]
        self.assertEqual(document["sha256"], hashlib.sha256(content.encode()).hexdigest())
        read = self.call("knowledge.local", "read", {"path": "rules/release.md"})
        self.assertEqual(read["result"]["document"]["content"], content)
        found = self.call("knowledge.local", "search", {"query": "READY"})
        match = next(item for item in found["result"]["matches"]
                     if item["relative_path"] == "rules/release.md")
        self.assertEqual(match["line_number"], 2)
        self.assertEqual(match["text"], "An order with status READY can proceed.")
        self.assertEqual(match["sha256"], document["sha256"])

    def test_knowledge_blocks_parent_and_symlink_escape(self):
        outside = self.root.parent / "outside.md"
        outside.write_text("private source", encoding="utf-8")
        (self.root / "knowledge" / "link.md").symlink_to(outside)
        for relative_path in ("../../outside.md", "link.md"):
            with self.subTest(path=relative_path):
                action = self.call("knowledge.local", "read", {"path": relative_path})
                self.assertEqual(action["status"], "FAILED")
                self.assertNotIn("private source", json.dumps(action))
        action = self.call("knowledge.local", "ingest", {"path": "link.md", "content": "replace"})
        self.assertEqual(action["status"], "FAILED")
        self.assertEqual(outside.read_text(encoding="utf-8"), "private source")

    def test_git_creates_branch_and_rejects_option_arguments(self):
        action = self.call("repository.git", "branch", {"name": "codex/integration-test"})
        self.assertEqual(action["status"], "SUCCEEDED")
        repository = self.resource_path("repository.git")
        ref = subprocess.run(["git", "show-ref", "--verify", "refs/heads/codex/integration-test"],
                             cwd=repository, capture_output=True, text=True)
        self.assertEqual(ref.returncode, 0, ref.stderr)
        for arguments in ({"name": "--help"},
                          {"name": "safe-name", "start_point": "--help"},
                          {"base": "--output=unexpected.txt"}):
            operation = "diff" if "base" in arguments else "branch"
            with self.subTest(arguments=arguments):
                self.assertEqual(self.call("repository.git", operation, arguments)["status"], "FAILED")
        self.assertFalse((repository / "unexpected.txt").exists())

    def test_git_ignores_inherited_checkout_override(self):
        repository = self.resource_path("repository.git")
        wrong_repository = self.root / "wrong-project"
        subprocess.run(["git", "init", "-q", str(wrong_repository)], check=True, capture_output=True)
        with patch.dict(os.environ, {"GIT_DIR": str(wrong_repository / ".git"),
                                     "GIT_WORK_TREE": str(wrong_repository)}):
            action = self.call("repository.git", "branch", {"name": "codex/intended-project"})
        self.assertEqual(action["status"], "SUCCEEDED")
        intended = subprocess.run(["git", "show-ref", "--verify", "refs/heads/codex/intended-project"],
                                  cwd=repository, capture_output=True)
        unintended = subprocess.run(["git", "show-ref", "--verify", "refs/heads/codex/intended-project"],
                                    cwd=wrong_repository, capture_output=True)
        self.assertEqual(intended.returncode, 0)
        self.assertNotEqual(unintended.returncode, 0)

    def test_git_plain_child_cannot_fall_back_to_parent_repository(self):
        repository = self.resource_path("repository.git")
        plain_child = repository / "unregistered-child"
        plain_child.mkdir()
        self.update_resource("repository.git", config={"path": str(plain_child)})
        status = self.call("repository.git", "status")
        self.assertEqual(status["status"], "FAILED")
        branch = self.call("repository.git", "branch", {"name": "codex/wrong-parent"})
        self.assertEqual(branch["status"], "FAILED")
        parent_ref = subprocess.run(["git", "show-ref", "--verify", "refs/heads/codex/wrong-parent"],
                                    cwd=repository, capture_output=True)
        self.assertNotEqual(parent_ref.returncode, 0)

    def test_named_test_suite_runs_and_retains_output(self):
        action = self.call("testing.command", "run", {"suite": "unit"})
        self.assertEqual(action["status"], "SUCCEEDED", action)
        self.assertEqual(action["result"]["exit_code"], 0)
        self.assertTrue(action["evidence"])
        self.assertTrue(self.output_path(action["result"]["stderr_path"]).exists())
        arbitrary = self.call("testing.command", "run", {"suite": "unit", "command": "echo injected"})
        self.assertEqual(arbitrary["status"], "FAILED")
        missing = self.call("testing.command", "run", {"suite": "unregistered"})
        self.assertEqual(missing["status"], "FAILED")

    def test_failed_test_run_is_an_observation_with_output(self):
        resource = self.update_resource("testing.command")
        configuration = {**resource["config"], "suites": {
            "failure": [sys.executable, "-c", "import sys; print('observed failure'); sys.exit(7)"]}}
        self.update_resource("testing.command", config=configuration)
        action = self.call("testing.command", "run", {"suite": "failure"})
        self.assertEqual(action["status"], "FAILED")
        self.assertEqual(action["result"]["exit_code"], 7)
        output = self.output_path(action["result"]["stdout_path"]).read_text(encoding="utf-8")
        self.assertIn("observed failure", output)
        self.assertEqual(self.workbench.run(action["id"])["result"]["exit_code"], 7)

    def test_test_timeout_retains_partial_output(self):
        configuration = self.read_configuration()
        configuration["timeout_seconds"] = 1
        resource = next(item for item in configuration["resources"]
                        if item["provider"] == "testing.command")
        resource["config"]["suites"] = {"timeout": [sys.executable, "-u", "-c",
            "import time; print('started'); time.sleep(5)"]}
        (self.root / "workspace.json").write_text(json.dumps(configuration), encoding="utf-8")
        self.workbench = Workbench(self.root)
        action = self.call("testing.command", "run", {"suite": "timeout"})
        self.assertEqual(action["status"], "FAILED")
        self.assertEqual(action["result"]["status"], "TIMEOUT")
        output = self.output_path(action["result"]["stdout_path"]).read_text(encoding="utf-8")
        self.assertIn("started", output)
        self.assertTrue(action["evidence"])

    def test_log_search_retains_observed_lines(self):
        path = self.resource_path("logs.file")
        path.write_text("INFO started\nERROR id=42 failed\nINFO completed\n", encoding="utf-8")
        action = self.call("logs.file", "search", {"query": "id=42"})
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertEqual(action["result"]["matches"], [
            {"line_number": 2, "text": "ERROR id=42 failed"}])
        self.assertEqual(action["result"]["scanned_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_sqlite_queries_are_bounded_and_readonly(self):
        tables = self.call("database.sqlite", "tables")
        self.assertEqual(tables["status"], "SUCCEEDED")
        self.assertTrue(tables["result"]["tables"])
        read = self.call("database.sqlite", "query", {
            "sql": "SELECT 1 AS value UNION ALL SELECT 2", "max_rows": 1})
        self.assertEqual(read["status"], "SUCCEEDED")
        self.assertEqual(read["result"]["columns"], ["value"])
        self.assertEqual(read["result"]["rows"], [[1]])
        self.assertTrue(read["result"]["truncated"])
        for sql in ("CREATE TABLE unauthorized (id INTEGER)",
                    "PRAGMA user_version = 42", "ATTACH DATABASE ':memory:' AS escaped"):
            with self.subTest(sql=sql):
                self.assertEqual(self.call("database.sqlite", "query", {"sql": sql})["status"], "FAILED")
        with closing(sqlite3.connect(self.resource_path("database.sqlite"))) as connection:
            names = [row[0] for row in connection.execute("SELECT name FROM sqlite_master")]
            self.assertNotIn("unauthorized", names)
            self.assertEqual(connection.execute("PRAGMA user_version").fetchone()[0], 0)

    def test_eureka_reads_instances_from_mock_registry(self):
        requests = []

        class RegistryHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                payload = {"applications": {"application": [{"name": "ORDERS", "instance": [
                    {"instanceId": "orders-1", "status": "UP", "hostName": "orders.test"}]}]}}
                body = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_):
                pass

        server = HTTPServer(("127.0.0.1", 0), RegistryHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(thread.join, 2)
        self.addCleanup(server.shutdown)
        configuration = self.read_configuration()
        configuration["resources"].append({
            "id": "mock-registry", "kind": "discovery", "provider": "discovery.eureka",
            "environment": "test", "allowed_operations": ["instances"],
            "config": {"url": f"http://127.0.0.1:{server.server_port}/eureka"}})
        (self.root / "workspace.json").write_text(json.dumps(configuration), encoding="utf-8")
        self.workbench = Workbench(self.root)
        action = self.workbench.call("mock-registry", "instances")
        self.assertEqual(action["status"], "SUCCEEDED", action)
        self.assertEqual(action["result"]["instances"][0]["instanceId"], "orders-1")
        self.assertEqual(action["result"]["instances"][0]["application"], "ORDERS")
        self.assertEqual(len(requests), 1)

    def resource_path(self, provider):
        resource = next(item for item in self.read_configuration()["resources"]
                        if item["provider"] == provider)
        path = Path(resource["config"]["path"])
        return path if path.is_absolute() else self.root / path

    def output_path(self, path):
        path = Path(path)
        return path if path.is_absolute() else self.root / path
