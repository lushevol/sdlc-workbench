"""Protect portable registrations, user hook settings, and installation recovery."""

import base64
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import hook_install as module
from ai_sdlc_workbench.models import WorkbenchError


class HookInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="workbench-hooks-install-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "workspace ' $ ` 漢"
        self.root.mkdir()
        self.write("workspace.json", {"schema_version": 1, "id": "hook-install-fixture", "name": "Hook install fixture",
                                      "plugins": [], "resources": []})

    def write(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def read(self, relative):
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def settings(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*.json")}

    def install_legacy(self):
        """Keep the original v1 registration contract as the migration baseline."""
        state = {"schema_version": 1, "clients": {}}
        for client, relative in module.CONFIGS.items():
            hooks = {}
            for event in ("start", "stop"):
                native = ("sessionStart" if event == "start" else "agentStop") if client == "copilot" else (
                    "SessionStart" if event == "start" else "Stop")
                arguments = ["-m", "ai_sdlc_workbench", "--workspace", str(self.root), "hooks", "run",
                             "--client", client, "--event", event]
                handler = {"type": "command", "args": arguments}
                if client == "copilot":
                    handler.update(exec=sys.executable, timeoutSec=15)
                    entry = handler
                elif client == "claude":
                    handler.update(command=sys.executable, timeout=15)
                    entry = {"hooks": [handler]}
                else:
                    argv = [sys.executable, *arguments]
                    script = "& " + " ".join("'" + value.replace("'", "''") + "'" for value in argv) + "; exit $LASTEXITCODE"
                    encoded = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
                    entry = {"hooks": [{"type": "command", "command": shlex.join(argv),
                              "commandWindows": "powershell.exe -NoProfile -NonInteractive -EncodedCommand " + encoded,
                              "timeout": 15}]}
                hooks[native] = [entry]
            document = {"hooks": hooks}
            if client == "copilot":
                document["version"] = 1
            if client == "codex":
                document["owner"] = "preserve user settings"
                hooks["SessionStart"].append({"hooks": [{"type": "command", "command": "user-command"}]})
            self.write(relative, document)
            state["clients"][client] = {"python": sys.executable, "workspace": str(self.root),
                                        "created": client != "codex", "had_hooks": client == "codex"}
        self.write(module._STATE, state)

    def test_status_does_not_create_files_and_reports_execution_unverified(self):
        result = module.hook_status(self.root)
        self.assertEqual(result["status"], "NOT_CONFIGURED")
        self.assertEqual(result["client_execution"], "NOT_RUN")
        self.assertEqual([path.name for path in self.root.iterdir()], ["workspace.json"])

    def test_install_requires_a_loadable_workspace_before_creating_state(self):
        path = self.root / "workspace.json"
        path.unlink()
        for payload in (None, {"unexpected": "not a workspace"}):
            with self.subTest(payload=payload):
                if payload:
                    self.write("workspace.json", payload)
                with self.assertRaises(WorkbenchError):
                    module.install_hooks(self.root)
                self.assertFalse((self.root / ".workbench").exists())
                self.assertFalse((self.root / ".codex").exists())

    def test_relocated_configuration_remains_ready_and_byte_identical(self):
        module.install_hooks(self.root)
        before = self.settings()
        moved = self.root.parent / "moved workspace"
        shutil.move(self.root, moved)
        self.root = moved
        result = module.hook_status(self.root)
        self.assertEqual(result["status"], "READY")
        self.assertTrue(all(row["status"] == "CONFIGURED" for row in result["clients"]))
        self.assertEqual(self.settings(), before)
        self.assertEqual(module.install_hooks(self.root)["status"], "READY")
        self.assertEqual(self.settings(), before)

    def test_legacy_install_migrates_all_owned_clients_after_relocation(self):
        self.install_legacy()
        status = module.hook_status(self.root)
        self.assertEqual(status["status"], "INCOMPLETE")
        self.assertTrue(all("portable reinstall" in row["detail"] for row in status["clients"]))
        self.assertNotIn(sys.executable, json.dumps(status))
        moved = self.root.parent / "legacy moved"
        shutil.move(self.root, moved)
        self.root = moved
        self.assertEqual(module.install_hooks(self.root, ["codex"])["status"], "READY")
        self.assertEqual(self.read(module._STATE)["schema_version"], 2)
        self.assertNotIn(sys.executable, json.dumps(self.settings_as_json()))
        codex = self.read(module.CONFIGS["codex"])
        self.assertEqual(codex["owner"], "preserve user settings")
        self.assertIn({"hooks": [{"type": "command", "command": "user-command"}]}, codex["hooks"]["SessionStart"])
        module.remove_hooks(self.root)
        self.assertEqual(self.read(module.CONFIGS["codex"]), {"owner": "preserve user settings", "hooks": {
            "SessionStart": [{"hooks": [{"type": "command", "command": "user-command"}]}]}})

    def test_legacy_partial_uninstall_migrates_retained_clients_without_absolute_state(self):
        self.install_legacy()
        result = module.remove_hooks(self.root, ["claude"])
        self.assertEqual(result["status"], "PARTIAL")
        state = self.read(module._STATE)
        self.assertEqual(state["schema_version"], 2)
        self.assertEqual(set(state["clients"]), {"codex", "copilot"})
        self.assertFalse((self.root / module.CONFIGS["claude"]).exists())
        self.assertNotIn(sys.executable, json.dumps(self.settings_as_json()))
        self.assertTrue(all(row["status"] == "CONFIGURED" for row in result["clients"][:2]))

    def test_legacy_uninstall_removes_only_the_exact_old_registrations(self):
        self.install_legacy()
        self.assertEqual(module.remove_hooks(self.root)["status"], "NOT_CONFIGURED")
        self.assertFalse((self.root / module._STATE).exists())
        self.assertFalse((self.root / module.CONFIGS["copilot"]).exists())
        self.assertFalse((self.root / module.CONFIGS["claude"]).exists())
        self.assertEqual(self.read(module.CONFIGS["codex"])["hooks"]["SessionStart"],
                         [{"hooks": [{"type": "command", "command": "user-command"}]}])

    def test_modified_legacy_entry_prevents_migration_and_partial_uninstall(self):
        self.install_legacy()
        document = self.read(module.CONFIGS["claude"])
        document["hooks"]["Stop"][0]["hooks"][0]["timeout"] = 3
        self.write(module.CONFIGS["claude"], document)
        before = self.settings()
        for operation in (module.install_hooks, module.remove_hooks):
            with self.subTest(operation=operation.__name__):
                with self.assertRaisesRegex(WorkbenchError, "changed after installation"):
                    operation(self.root, ["codex"])
                self.assertEqual(self.settings(), before)

    def test_identical_unowned_codex_registration_cannot_double_run(self):
        entries = module._registrations("codex")
        path = self.write(module.CONFIGS["codex"], {"hooks": {event: [entry] for event, entry in entries.items()}})
        raw = path.read_bytes()
        with self.assertRaisesRegex(WorkbenchError, "not owned"):
            module.install_hooks(self.root)
        self.assertEqual(path.read_bytes(), raw)
        self.assertFalse((self.root / module._STATE).exists())

    def test_installation_is_idempotent_and_claude_does_not_cross_load(self):
        ordinary = self.write(".claude/settings.json", {"permissions": {"allow": ["Read"]}})
        original = ordinary.read_bytes()
        result = module.install_hooks(self.root)
        self.assertEqual(result["status"], "READY")
        self.assertEqual({row["client"] for row in result["clients"]}, {"codex", "copilot", "claude"})
        self.assertEqual(ordinary.read_bytes(), original)
        installed = self.settings()
        self.assertEqual(module.install_hooks(self.root)["status"], "READY")
        self.assertEqual(self.settings(), installed)
        self.assertEqual(ordinary.read_bytes(), original)
        claude = next(row for row in result["clients"] if row["client"] == "claude")
        self.assertEqual(claude["launch_argv"], ["claude", "--settings", ".claude/workbench-hooks.json"])
        self.assertEqual(set(self.read(module.CONFIGS["copilot"])["hooks"]), {"sessionStart", "agentStop"})
        self.assertEqual(set(self.read(module.CONFIGS["claude"])["hooks"]), {"SessionStart", "Stop"})

    def test_codex_user_hooks_and_unrelated_concurrent_settings_survive(self):
        user = {"hooks": [{"type": "command", "command": "user-command"}]}
        original = {"description": "Owner's configuration", "hooks": {"SessionStart": [user]}}
        self.write(module.CONFIGS["codex"], original)
        module.install_hooks(self.root)
        changed = self.read(module.CONFIGS["codex"])
        changed["customSetting"] = {"retained": True}
        changed["hooks"]["SessionStart"].append({"hooks": [{"type": "command", "command": "another-user-command"}]})
        self.write(module.CONFIGS["codex"], changed)
        module.install_hooks(self.root)
        module.remove_hooks(self.root)
        remaining = self.read(module.CONFIGS["codex"])
        self.assertEqual(remaining["description"], original["description"])
        self.assertEqual(remaining["customSetting"], {"retained": True})
        self.assertEqual([entry["hooks"][0]["command"] for entry in remaining["hooks"]["SessionStart"]],
                         ["user-command", "another-user-command"])
        self.assertFalse((self.root / module.CONFIGS["copilot"]).exists())
        self.assertFalse((self.root / module.CONFIGS["claude"]).exists())

    def test_preexisting_dedicated_file_is_preserved_before_any_config_write(self):
        path = self.write(module.CONFIGS["copilot"], {"version": 1, "hooks": {"agentStop": []}})
        before = path.read_bytes()
        with self.assertRaisesRegex(WorkbenchError, "not owned"):
            module.install_hooks(self.root)
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse((self.root / module.CONFIGS["codex"]).exists())
        self.assertFalse((self.root / module.CONFIGS["claude"]).exists())
        self.assertFalse((self.root / module._STATE).exists())

    def test_invalid_json_duplicate_keys_and_hook_arrays_are_rejected(self):
        path = self.root / module.CONFIGS["codex"]
        path.parent.mkdir()
        for raw in ('[]', '{"hooks":{},"hooks":{}}', '{"hooks":{"SessionStart":{}}}',
                    '{"hooks":{"SessionStart":["not a handler"]}}', '{"hooks":NaN}'):
            with self.subTest(raw=raw):
                path.write_text(raw, encoding="utf-8")
                with self.assertRaises(WorkbenchError):
                    module.install_hooks(self.root)
                self.assertEqual(path.read_text(encoding="utf-8"), raw)
                self.assertFalse((self.root / module.CONFIGS["copilot"]).exists())

    def test_late_invalid_configuration_does_not_partially_update_earlier_clients(self):
        codex = self.write(module.CONFIGS["codex"], {"hooks": {}, "owner": "preserve bytes"})
        before = codex.read_bytes()
        path = self.root / module.CONFIGS["claude"]
        path.parent.mkdir()
        path.write_text("not JSON", encoding="utf-8")
        with self.assertRaises(WorkbenchError):
            module.install_hooks(self.root)
        self.assertEqual(codex.read_bytes(), before)
        self.assertFalse((self.root / module.CONFIGS["copilot"]).exists())

    def test_modified_owned_handler_blocks_update_and_remove_without_overwrite(self):
        module.install_hooks(self.root)
        changed = self.read(module.CONFIGS["codex"])
        changed["hooks"]["Stop"][0]["hooks"][0]["timeout"] = 3
        self.write(module.CONFIGS["codex"], changed)
        before = self.settings()
        for operation in (module.install_hooks, module.remove_hooks):
            with self.subTest(operation=operation.__name__):
                with self.assertRaisesRegex(WorkbenchError, "changed after installation"):
                    operation(self.root)
                self.assertEqual(self.settings(), before)
        status = module.hook_status(self.root)
        self.assertEqual(status["status"], "INCOMPLETE")
        self.assertEqual(status["clients"][0]["status"], "INCOMPLETE")

    def test_partial_remove_preserves_other_clients_and_unrelated_new_content(self):
        module.install_hooks(self.root)
        document = self.read(module.CONFIGS["claude"])
        document["permissions"] = {"deny": ["Bash(rm *)"]}
        self.write(module.CONFIGS["claude"], document)
        module.remove_hooks(self.root, ["claude"])
        self.assertEqual(self.read(module.CONFIGS["claude"]), {"permissions": {"deny": ["Bash(rm *)"]}})
        result = module.hook_status(self.root)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertEqual([row["status"] for row in result["clients"]], ["CONFIGURED", "CONFIGURED", "NOT_CONFIGURED"])
        module.remove_hooks(self.root, ["codex", "copilot"])
        self.assertFalse((self.root / module._STATE).exists())
        self.assertEqual(module.remove_hooks(self.root)["status"], "NOT_CONFIGURED")

    def test_failed_write_restores_exact_previous_config_bytes(self):
        path = self.root / module.CONFIGS["codex"]
        path.parent.mkdir()
        raw = b'{ "hooks": {}, "owner": "preserve original formatting" }\n'
        path.write_bytes(raw)
        atomic = module._atomic

        def fail_copilot(destination, data):
            if destination == self.root / module.CONFIGS["copilot"]:
                raise OSError("controlled write failure")
            atomic(destination, data)

        with patch.object(module, "_atomic", side_effect=fail_copilot):
            with self.assertRaisesRegex(WorkbenchError, "previous configuration bytes were restored"):
                module.install_hooks(self.root)
        self.assertEqual(path.read_bytes(), raw)
        self.assertFalse((self.root / module.CONFIGS["copilot"]).exists())
        self.assertFalse((self.root / module.CONFIGS["claude"]).exists())
        self.assertFalse((self.root / module._STATE).exists())

    def test_recovery_preserves_an_external_edit_instead_of_restoring_over_it(self):
        path = self.write(module.CONFIGS["codex"], {"owner": "initial"})
        atomic = module._atomic
        external = b'{"owner":"concurrent edit"}'

        def fail_after_external_edit(destination, data):
            if destination == self.root / module.CONFIGS["copilot"]:
                path.write_bytes(external)
                raise OSError("controlled concurrent failure")
            atomic(destination, data)

        with patch.object(module, "_atomic", side_effect=fail_after_external_edit):
            with self.assertRaisesRegex(WorkbenchError, "recovery conflicts"):
                module.install_hooks(self.root)
        self.assertEqual(path.read_bytes(), external)

    def test_symlinked_configuration_parent_cannot_write_outside_workspace(self):
        external = Path(self.temporary.name) / "external"
        external.mkdir()
        try:
            (self.root / ".codex").symlink_to(external, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Platform cannot create directory symlinks")
        with self.assertRaises(WorkbenchError):
            module.install_hooks(self.root)
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse((self.root / module.CONFIGS["copilot"]).exists())

    def test_native_registrations_state_and_status_have_no_machine_paths(self):
        module.install_hooks(self.root)
        expected = ["hooks", "run", "--client", "copilot", "--event", "start"]
        handler = self.read(module.CONFIGS["copilot"])["hooks"]["sessionStart"][0]
        self.assertEqual(handler["exec"], "ai-sdlc")
        self.assertEqual(handler["args"], expected)
        self.assertNotIn("bash", handler)
        codex = self.read(module.CONFIGS["codex"])["hooks"]["SessionStart"][0]["hooks"][0]
        self.assertEqual(codex["command"], "ai-sdlc hooks run --client codex --event start")
        self.assertNotIn("commandWindows", codex)
        claude = self.read(module.CONFIGS["claude"])["hooks"]["SessionStart"][0]["hooks"][0]
        self.assertEqual(claude["command"], "ai-sdlc")
        self.assertEqual(claude["args"], ["hooks", "run", "--client", "claude", "--event", "start"])
        state = self.read(module._STATE)
        self.assertEqual(state["schema_version"], 2)
        for client, record in state["clients"].items():
            self.assertEqual(set(record), {"registrations", "created", "had_hooks"})
            self.assertEqual(record["registrations"], module._registrations(client))
        serialized = json.dumps([self.settings_as_json(), module.hook_status(self.root)], ensure_ascii=False)
        self.assertNotIn(str(self.root), serialized)
        self.assertNotIn(sys.executable, serialized)
        self.assertNotIn("powershell", serialized)

    def settings_as_json(self):
        return {relative: raw.decode("utf-8") for relative, raw in self.settings().items()}

    def test_compatibility_python_option_is_verified_but_never_persisted(self):
        executable = self.root / "python shim"
        executable.write_text("Unused executable fixture.\n", encoding="utf-8")
        executable.chmod(0o700)
        module.install_hooks(self.root, python=executable)
        executable.unlink()
        self.assertEqual(module.hook_status(self.root)["status"], "READY")
        self.assertNotIn(str(executable), json.dumps(self.settings_as_json()))
        before = self.settings()
        with self.assertRaisesRegex(WorkbenchError, "compatibility --python"):
            module.install_hooks(self.root, python=executable)
        self.assertEqual(self.settings(), before)

    @unittest.skipIf(os.name == "nt", "POSIX shell quoting probe")
    def test_posix_registrations_use_path_after_workspace_moves(self):
        directory = Path(self.temporary.name) / "bin ' $ ` 漢"
        directory.mkdir()
        executable = directory / "ai-sdlc"
        executable.write_text("#!" + sys.executable + "\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n", encoding="utf-8")
        executable.chmod(0o700)
        module.install_hooks(self.root)
        before = self.settings()
        moved = self.root.parent / "moved ' $ ` 漢"
        shutil.move(self.root, moved)
        self.root = moved
        environment = {**os.environ, "PATH": str(directory) + os.pathsep + os.environ.get("PATH", "")}
        for client in module.CONFIGS:
            with self.subTest(client=client):
                entries = self.read(module.CONFIGS[client])["hooks"]
                handler = entries["sessionStart"][0] if client == "copilot" else entries["SessionStart"][0]["hooks"][0]
                argv = (["/bin/sh", "-c", handler["command"]] if client == "codex" else
                        [handler["exec" if client == "copilot" else "command"], *handler["args"]])
                result = subprocess.run(argv, cwd=self.root, env=environment, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), ["hooks", "run", "--client", client, "--event", "start"])
        self.assertEqual(self.settings(), before)


if __name__ == "__main__":
    unittest.main()
