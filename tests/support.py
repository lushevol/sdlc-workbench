"""Isolated workspaces for public API checks."""

from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.runtime import Workbench


def initialize_provider_fixture(root):
    """Create only the isolated resources consumed by provider and interface checks."""
    for directory in ("knowledge", "project", "logs", "database"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    (root / "knowledge/fixture.md").write_text("# Provider fixture\n", encoding="utf-8")
    (root / "project/.gitignore").write_text("__pycache__/\n", encoding="utf-8")
    (root / "logs/application.log").write_text("INFO fixture\n", encoding="utf-8")
    with closing(sqlite3.connect(root / "database/app.sqlite")) as connection, connection:
        connection.execute("CREATE TABLE fixture (id INTEGER)")
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    for arguments in (["git", "init", "-q", "-b", "main"], ["git", "add", "--", "."],
                      ["git", "-c", "user.name=Test Fixture", "-c", "user.email=fixture@example.invalid",
                       "-c", "commit.gpgsign=false", "commit", "-q", "-m", "Create provider fixture"]):
        subprocess.run(arguments, cwd=root / "project", env=environment,
                       check=True, capture_output=True, timeout=15)
    resources = [
        {"id": "knowledge", "kind": "knowledge", "provider": "knowledge.local", "environment": "test",
         "config": {"path": "knowledge"}, "allowed_operations": ["list", "search", "read", "ingest"]},
        {"id": "repository", "kind": "repository", "provider": "repository.git", "environment": "test",
         "config": {"path": "project"}, "allowed_operations": ["status", "diff", "branch"]},
        {"id": "tests", "kind": "testing", "provider": "testing.command", "environment": "test",
         "config": {"path": "project", "suites": {"unit": ["{python}", "-c", "print('observed suite output')"]}},
         "allowed_operations": ["list", "run"]},
        {"id": "logs", "kind": "logs", "provider": "logs.file", "environment": "test",
         "config": {"path": "logs/application.log"}, "allowed_operations": ["search"]},
        {"id": "database", "kind": "database", "provider": "database.sqlite", "environment": "test",
         "config": {"path": "database/app.sqlite"}, "allowed_operations": ["tables", "query"]},
    ]
    (root / "workspace.json").write_text(json.dumps({
        "schema_version": 1, "id": "provider-fixture", "name": "Integration workspace",
        "timeout_seconds": 30, "plugins": [], "resources": resources}), encoding="utf-8")


class WorkspaceTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        initialize_provider_fixture(self.root)
        self.workbench = Workbench(self.root)

    def resource_id(self, provider):
        configuration = self.read_configuration()
        return next(item["id"] for item in configuration["resources"]
                    if item["provider"] == provider)

    def read_configuration(self):
        return json.loads((self.root / "workspace.json").read_text(encoding="utf-8"))

    def update_resource(self, provider, **changes):
        configuration = self.read_configuration()
        resource = next(item for item in configuration["resources"]
                        if item["provider"] == provider)
        resource.update(changes)
        (self.root / "workspace.json").write_text(
            json.dumps(configuration), encoding="utf-8")
        self.workbench = Workbench(self.root)
        return resource

    def call(self, provider, operation, arguments=None):
        return self.workbench.call(self.resource_id(provider), operation, arguments)

    def install_fixture_provider(self, provider):
        class EntryPoint:
            name = provider.id

            def load(self):
                return lambda: provider

        configuration = self.read_configuration()
        configuration["plugins"] = [provider.id]
        configuration["resources"].append({
            "id": "fixture", "kind": provider.resource_kind, "provider": provider.id,
            "environment": "local", "config": {}, "allowed_operations": list(provider.operations)})
        (self.root / "workspace.json").write_text(json.dumps(configuration), encoding="utf-8")
        with patch("ai_sdlc_workbench.registry.entry_points", return_value=[EntryPoint()]):
            return Workbench(self.root)
