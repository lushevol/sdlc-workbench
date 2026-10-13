"""Isolated workspaces for public API checks."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.runtime import Workbench
from ai_sdlc_workbench.workspace import initialize_workspace


class WorkspaceTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        initialize_workspace(self.root, name="Integration workspace", demo=True)
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
