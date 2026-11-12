"""Check hook readiness without dispatching clients or changing configuration."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import doctor as module
from ai_sdlc_workbench.hook_install import install_hooks


class HookDoctorTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="workbench-hook-doctor-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        (self.root / "workspace.json").write_text(json.dumps({
            "schema_version": 1, "id": "hook-doctor-fixture", "name": "Hook doctor fixture",
            "plugins": [], "resources": [],
        }), encoding="utf-8")

    def snapshot(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def check(self, feature, identifier):
        return next(item for item in feature["checks"] if item["id"] == identifier)

    def test_absent_installation_is_not_configured_without_creating_state(self):
        before = self.snapshot()
        with patch.object(module.shutil, "which") as which, patch.object(module.subprocess, "run") as child:
            feature = module._hook_feature(self.root)
        self.assertEqual(feature["status"], "NOT_CONFIGURED")
        self.assertEqual(feature["checks"], [])
        which.assert_not_called()
        child.assert_not_called()
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / ".workbench").exists())

    def test_corrupt_installation_remains_incomplete_and_preserves_original_bytes(self):
        path = self.root / ".workbench/hooks/installation.json"
        path.parent.mkdir(parents=True)
        path.write_bytes(b'{"private-state": "do-not-echo", broken json}\n')
        before = self.snapshot()
        with patch.object(module.subprocess, "run") as child:
            feature = module._hook_feature(self.root)
        self.assertEqual(feature["status"], "INCOMPLETE")
        self.assertEqual(self.check(feature, "hook-configurations")["status"], "INCOMPLETE")
        self.assertNotIn("do-not-echo", json.dumps(feature))
        child.assert_not_called()
        self.assertEqual(self.snapshot(), before)

    def test_configured_clients_are_discovered_without_claiming_native_dispatch(self):
        install_hooks(self.root)
        before = self.snapshot()
        with patch.object(module.shutil, "which", return_value="/available/client") as which, \
                patch.object(module.subprocess, "run") as child:
            feature = module._hook_feature(self.root)
        self.assertEqual(feature["status"], "READY")
        self.assertEqual(feature["integration_access"], "UNTESTED")
        self.assertTrue({"codex", "copilot", "claude"}.issubset({call.args[0] for call in which.call_args_list}))
        for client in ("codex", "copilot", "claude"):
            self.assertEqual(self.check(feature, "hooks:" + client)["status"], "READY")
            self.assertEqual(self.check(feature, "executable:" + client)["status"], "READY")
        self.assertTrue(any("live event delivery" in value for value in feature["limitations"]))
        child.assert_not_called()
        self.assertEqual(self.snapshot(), before)

    def test_missing_selected_client_executable_is_incomplete(self):
        install_hooks(self.root, ["copilot"])
        with patch.object(module.shutil, "which", return_value=None) as which, \
                patch.object(module.subprocess, "run") as child:
            feature = module._hook_feature(self.root)
        self.assertEqual(feature["status"], "INCOMPLETE")
        self.assertEqual(self.check(feature, "hooks:copilot")["status"], "READY")
        executable = self.check(feature, "executable:copilot")
        self.assertEqual(executable["status"], "INCOMPLETE")
        self.assertFalse(executable["found"])
        which.assert_called_once_with("copilot")
        child.assert_not_called()

    def test_missing_registered_python_is_incomplete_even_with_client_on_path(self):
        executable = self.root / ("hook-python.exe" if sys.platform == "win32" else "hook-python")
        executable.write_text("Unused executable fixture.\n", encoding="utf-8")
        executable.chmod(0o755)
        install_hooks(self.root, ["copilot"], python=executable)
        executable.unlink()
        before = self.snapshot()
        with patch.object(module.shutil, "which", return_value="/available/copilot"), \
                patch.object(module.subprocess, "run") as child:
            feature = module._hook_feature(self.root)
        self.assertEqual(feature["status"], "INCOMPLETE")
        self.assertEqual(self.check(feature, "hooks:copilot")["status"], "INCOMPLETE")
        self.assertEqual(self.check(feature, "executable:copilot")["status"], "READY")
        child.assert_not_called()
        self.assertEqual(self.snapshot(), before)

    def test_unavailable_installed_hook_module_is_incomplete_without_dispatch(self):
        install_hooks(self.root, ["copilot"])
        before = self.snapshot()
        with patch.dict(sys.modules, {"ai_sdlc_workbench.hook_install": None}), \
                patch.object(module.subprocess, "run") as child:
            feature = module._hook_feature(self.root)
        self.assertEqual(feature["status"], "INCOMPLETE")
        self.assertEqual(self.check(feature, "hook-runtime")["status"], "INCOMPLETE")
        child.assert_not_called()
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
