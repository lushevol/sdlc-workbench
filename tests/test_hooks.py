"""Check native hook contracts, explicit scope, and advisory validation boundaries."""

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
from threading import Event
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import hooks as module
from ai_sdlc_workbench.hook_install import CONFIGS, install_hooks
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.workspace import initialize_workspace


class HookRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="workbench-hooks-runtime-")
        self.addCleanup(temporary.cleanup)
        self.root = (Path(temporary.name) / "workspace with spaces").resolve()
        self.root.mkdir()
        (self.root / "workspace.yaml").write_text(json.dumps({
            "schema_version": 1, "id": "hook-fixture", "name": "Hook fixture",
            "plugins": [], "resources": [],
        }), encoding="utf-8")
        self.record = self.write("tasks/example/01-intake.md", "# Current work\nPrivate record content.\n")
        self.code = self.write("repos/service/behavior.py", "result = 'old'\n")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return relative

    def payload(self, client, session="same-native-session", **values):
        key = "sessionId" if client == "copilot" else "session_id"
        return {key: session, "cwd": str(self.root), **values}

    def bind(self, client="codex", session="same-native-session", **options):
        return module.bind_scope(self.root, client, session, self.record, **options)

    def changed(self, relative=None):
        path = self.root / (relative or self.record)
        path.write_text(path.read_text(encoding="utf-8") + "Changed source.\n", encoding="utf-8")

    def snapshot(self):
        return {str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.root.rglob("*") if path.is_file()
                and ".workbench" not in path.relative_to(self.root).parts}

    def successful_runner(self):
        return patch.object(module.subprocess, "run", return_value=SimpleNamespace(
            returncode=0, stdout='{"valid": true, "status": "VALID"}', stderr=""))

    def cli(self, *arguments, payload="", explicit_workspace=True, cwd=None):
        command = [sys.executable, "-m", "ai_sdlc_workbench"]
        if explicit_workspace:
            command += ["--workspace", str(self.root)]
        return subprocess.run([*command, "hooks", *arguments], input=payload, cwd=cwd,
                              capture_output=True, text=True, timeout=15, shell=False)

    def native_context(self, client, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        output = json.loads(result.stdout)
        return output["additionalContext"] if client == "copilot" else output["hookSpecificOutput"]["additionalContext"]

    def test_public_cli_discovers_nearest_workspace_from_native_cwd(self):
        ordinary_child = self.root / "repos/service/src"
        ordinary_child.mkdir(parents=True)
        nested = self.root / "nested/workbench"
        nested_child = nested / "src"
        nested_child.mkdir(parents=True)
        (nested / "workspace.yaml").write_bytes((self.root / "workspace.yaml").read_bytes())
        nested_record = "tasks/nested/01-intake.md"
        (nested / nested_record).parent.mkdir(parents=True)
        (nested / nested_record).write_text("# Inner work\n", encoding="utf-8")
        for client in ("codex", "copilot", "claude"):
            self.bind(client)
            module.bind_scope(nested, client, "same-native-session", nested_record)
            for cwd, expected_record in ((self.root, self.record), (ordinary_child, self.record),
                                         (nested_child, nested_record)):
                with self.subTest(client=client, native_cwd=cwd):
                    result = self.cli("run", "--client", client, "--event", "start",
                                      payload=json.dumps(self.payload(client, cwd=str(cwd))),
                                      explicit_workspace=False, cwd=self.root.parent)
                    context = self.native_context(client, result)
                    self.assertIn("Declared living record: " + expected_record, context)
                    self.assertNotIn(str(self.root), context)
                    self.assertNotIn(sys.executable, context)

    def test_portable_registrations_and_bindings_survive_workspace_relocation(self):
        install_hooks(self.root)
        for client in ("codex", "copilot", "claude"):
            self.bind(client)
        saved = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*.json")}
        for raw in saved.values():
            self.assertNotIn(str(self.root).encode(), raw)
            self.assertNotIn(sys.executable.encode(), raw)
        previous_root = self.root
        self.root = self.root.rename(self.root.parent / "relocated workspace")
        child = self.root / "repos/service"
        for client in ("codex", "copilot", "claude"):
            result = self.cli("run", "--client", client, "--event", "start", explicit_workspace=False,
                              payload=json.dumps(self.payload(client, cwd=str(child))), cwd=self.root.parent)
            context = self.native_context(client, result)
            self.assertIn("Declared living record: " + self.record, context)
            self.assertNotIn(str(previous_root), context)
            self.assertNotIn(str(self.root), context)
        self.assertEqual({relative: (self.root / relative).read_bytes() for relative in saved}, saved)

        result = self.cli("run", "--client", "codex", "--event", "start", explicit_workspace=False,
                          payload=json.dumps(self.payload("codex", session="relocated-new-session", cwd=str(child))),
                          cwd=self.root.parent)
        context = self.native_context("codex", result)
        command = context.split("Before scoped edits, bind the existing living record: ", 1)[1].splitlines()[0]
        arguments = shlex.split(command.removeprefix("& "))
        self.assertEqual(arguments[:3], ["ai-sdlc", "--workspace", "../.."])
        arguments[-1] = self.record
        environment = dict(os.environ)
        environment["PATH"] = str(Path(sys.executable).parent) + os.pathsep + environment.get("PATH", "")
        binding = subprocess.run(arguments, cwd=child, env=environment, capture_output=True, text=True,
                                 timeout=15, shell=False)
        self.assertEqual(binding.returncode, 0, binding.stderr)
        self.assertEqual(json.loads(binding.stdout)["status"], "BOUND")
        for relative in (*CONFIGS.values(), ".workbench/hooks/installation.json"):
            self.assertEqual((self.root / relative).read_bytes(), saved[relative])

    def test_native_directory_without_declaration_reports_advisory_without_writes(self):
        outside = self.root.parent / "outside-native-directory"
        outside.mkdir()
        for client in ("codex", "copilot", "claude"):
            with self.subTest(client=client):
                result = self.cli("run", "--client", client, "--event", "stop", explicit_workspace=False,
                                  payload=json.dumps(self.payload(client, cwd=str(outside))), cwd=self.root)
                self.assertEqual(result.returncode, 2 if client == "copilot" else 0)
                output = json.loads(result.stdout)
                self.assertNotIn("decision", output)
                self.assertTrue(result.stderr if client == "copilot" else output.get("systemMessage"))
                self.assertNotIn(str(outside), result.stdout + result.stderr)
        self.assertFalse((self.root / ".workbench").exists())
        self.assertEqual(list(outside.iterdir()), [])

    def test_explicit_workspace_cannot_use_native_cwd_outside_its_boundary(self):
        outside = self.root.parent / "outside-explicit-directory"
        outside.mkdir()
        for client in ("codex", "copilot", "claude"):
            with self.subTest(client=client):
                self.bind(client)
                self.changed()
                before = {path: path.read_bytes() for path in (self.root / ".workbench").rglob("*") if path.is_file()}
                result = self.cli("run", "--client", client, "--event", "stop",
                                  payload=json.dumps(self.payload(client, cwd=str(outside))))
                self.assertEqual(result.returncode, 2 if client == "copilot" else 0)
                output = json.loads(result.stdout)
                self.assertTrue(result.stderr if client == "copilot" else output.get("systemMessage"))
                self.assertEqual({path: path.read_bytes() for path in before}, before)
        self.assertEqual(list(outside.iterdir()), [])

    def test_public_cli_returns_one_native_context_object_for_each_client(self):
        for client in ("codex", "copilot", "claude"):
            with self.subTest(client=client):
                result = self.cli("run", "--client", client, "--event", "start",
                                  payload=json.dumps(self.payload(client)))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                output = json.loads(result.stdout)
                context = output["additionalContext"] if client == "copilot" else output[
                    "hookSpecificOutput"]["additionalContext"]
                self.assertIn("hooks bind", context)
                self.assertIn("same-native-session", context)
                self.assertNotIn("decision", output)
        self.assertFalse((self.root / ".workbench").exists())

    def test_public_cli_rejects_malformed_and_oversized_payloads_without_leaking_input(self):
        private = "private-input-must-not-be-printed"
        payloads = [f'{{"session_id": "{private}", "session_id": "duplicate"}}',
                    json.dumps({"session_id": "test", "unused": private * 40000}),
                    json.dumps({"session_id": "test", "cwd": str(self.root), "unused": "\U0001f6e0" * 300000}, ensure_ascii=False)]
        for client in ("codex", "copilot", "claude"):
            for payload in payloads:
                with self.subTest(client=client, length=len(payload)):
                    result = self.cli("run", "--client", client, "--event", "stop", payload=payload)
                    self.assertEqual(result.returncode, 2 if client == "copilot" else 0)
                    output = json.loads(result.stdout)
                    self.assertNotIn("decision", output)
                    self.assertNotIn("continue", output)
                    self.assertNotIn(private, result.stdout + result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    if client == "copilot":
                        self.assertEqual(output, {})
                        self.assertTrue(result.stderr)
                    else:
                        self.assertTrue(output["systemMessage"])
        self.assertFalse((self.root / ".workbench").exists())

    def test_option_shaped_artifact_name_cannot_select_schema_instead_of_validation(self):
        artifact = self.write("--print-schema", "This is not a valid declared SDLC artifact.\n")
        self.bind(artifacts=[artifact])
        self.changed()
        result = self.cli("run", "--client", "codex", "--event", "stop",
                          payload=json.dumps(self.payload("codex")))
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertTrue(output.get("systemMessage"),
                        "The selected invalid file must fail lint rather than invoking --print-schema.")
        self.assertNotIn("decision", output)

    def test_unbound_stop_does_not_scan_or_create_state(self):
        before = self.snapshot()
        for client in ("codex", "copilot", "claude"):
            with self.subTest(client=client), self.successful_runner() as runner:
                self.assertEqual(module.run_hook(self.root, client, "stop", self.payload(client)), ({}, "", 0))
                runner.assert_not_called()
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / ".workbench").exists())

    def test_windows_start_guidance_uses_powershell_quoting(self):
        with patch.object(module.sys, "platform", "win32"), patch.object(module.sys, "executable", "C:\\User's Tools\\python.exe"):
            output, _, code = module.run_hook(self.root, "claude", "start", self.payload("claude"))
        self.assertEqual(code, 0)
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("& 'ai-sdlc' '--workspace' '.' 'hooks' 'bind'", context)
        self.assertNotIn("C:\\User", context)
        self.assertNotIn(str(self.root), context)

    def test_changed_workspace_configuration_invalidates_cached_checks(self):
        self.bind()
        self.write("workspace.local.yaml", "local: {}\n")
        with self.successful_runner() as runner:
            module.run_hook(self.root, "codex", "stop", self.payload("codex"))
            runner.assert_called_once()
            module.run_hook(self.root, "codex", "stop", self.payload("codex"))
            runner.assert_called_once()

    def test_start_returns_native_context_without_reading_document_content(self):
        for client in ("codex", "copilot", "claude"):
            with self.subTest(client=client):
                self.bind(client)
                output, diagnostic, code = module.run_hook(self.root, client, "start", self.payload(client))
                self.assertEqual((diagnostic, code), ("", 0))
                if client == "copilot":
                    self.assertNotIn("hookSpecificOutput", output)
                    context = output["additionalContext"]
                else:
                    self.assertNotIn("additionalContext", output)
                    self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
                    context = output["hookSpecificOutput"]["additionalContext"]
                self.assertIn(self.record, context)
                self.assertIn("same-native-session", context)
                self.assertNotIn("Private record content", context)
                self.assertLessEqual(len(context), 2400)
                self.assertNotIn("decision", output)

    def test_unchanged_bound_scope_and_unrelated_drafts_do_not_run_checks(self):
        self.bind(watch=[self.code])
        self.write("tasks/unrelated/draft.md", "An unrelated task changed.\n")
        with self.successful_runner() as runner:
            self.assertEqual(module.run_hook(self.root, "codex", "stop", self.payload("codex")), ({}, "", 0))
            runner.assert_not_called()

    def test_changed_watch_runs_once_and_later_changes_invalidate_the_result(self):
        self.bind(watch=[self.code])
        self.changed(self.code)
        before = self.snapshot()
        with self.successful_runner() as runner:
            self.assertEqual(module.run_hook(self.root, "codex", "stop", self.payload("codex")), ({}, "", 0))
            self.assertEqual(runner.call_count, 1)
            args, options = runner.call_args
            self.assertIn("validate", args[0])
            self.assertIn(str(self.root), args[0])
            self.assertFalse(options.get("shell", False))
            self.assertEqual(options["stdin"], subprocess.DEVNULL)
            self.assertGreater(options["timeout"], 0)
            self.assertLessEqual(options["timeout"], 30)
            self.assertEqual(module.run_hook(self.root, "codex", "stop", self.payload("codex")), ({}, "", 0))
            self.assertEqual(runner.call_count, 1)
            self.changed(self.code)
            module.run_hook(self.root, "codex", "stop", self.payload("codex"))
            self.assertEqual(runner.call_count, 2)
        expected = self.snapshot()
        self.assertEqual(set(expected), set(before))
        self.assertEqual({key: value for key, value in expected.items() if key != self.code},
                         {key: value for key, value in before.items() if key != self.code})

    def test_same_native_session_id_remains_separate_between_clients(self):
        for client in ("codex", "copilot", "claude"):
            self.bind(client, watch=[self.code])
        self.changed(self.code)
        with self.successful_runner() as runner:
            for client in ("codex", "copilot", "claude"):
                with self.subTest(client=client):
                    self.assertEqual(module.run_hook(self.root, client, "stop", self.payload(client)), ({}, "", 0))
            self.assertEqual(runner.call_count, 3)
        module.clear_scope(self.root, "codex", "same-native-session")
        self.changed(self.code)
        with self.successful_runner() as runner:
            module.run_hook(self.root, "codex", "stop", self.payload("codex"))
            runner.assert_not_called()
            module.run_hook(self.root, "copilot", "stop", self.payload("copilot"))
            runner.assert_called_once()

    def test_failed_checks_are_native_advisories_and_do_not_repeat(self):
        for client in ("codex", "copilot", "claude"):
            with self.subTest(client=client):
                self.bind(client)
                self.changed()
                with patch.object(module.subprocess, "run", return_value=SimpleNamespace(
                        returncode=1, stdout='{"valid": false}', stderr="private backend output")) as runner:
                    output, diagnostic, code = module.run_hook(self.root, client, "stop", self.payload(client))
                    self.assertNotIn("decision", output)
                    self.assertNotIn("continue", output)
                    combined = json.dumps(output) + diagnostic
                    self.assertNotIn("private backend output", combined)
                    if client == "copilot":
                        self.assertEqual(output, {})
                        self.assertEqual(code, 2)
                        self.assertTrue(diagnostic)
                    else:
                        self.assertEqual((diagnostic, code), ("", 0))
                        self.assertTrue(output["systemMessage"])
                    self.assertEqual(module.run_hook(self.root, client, "stop", self.payload(client)), ({}, "", 0))
                    runner.assert_called_once()

    def test_validator_diagnostic_paths_are_retained_relative_to_workspace(self):
        self.bind()
        self.changed()
        diagnostics = {"findings": [
            {"code": "INVALID_RECORD", "path": str(self.root / self.record)},
            {"code": "OUTSIDE", "path": str(self.root.parent / "private-external-path")},
        ]}
        with patch.object(module.subprocess, "run", return_value=SimpleNamespace(
                returncode=1, stdout=json.dumps(diagnostics), stderr="")):
            output, diagnostic, code = module.run_hook(self.root, "codex", "stop", self.payload("codex"))
        self.assertEqual((diagnostic, code), ("", 0))
        self.assertTrue(output["systemMessage"])
        state_path = next((self.root / ".workbench/hooks/sessions").glob("*.json"))
        state = json.loads(state_path.read_text(encoding="utf-8"))
        findings = state["last_result"]["checks"][0]["findings"]
        self.assertEqual([item["path"] for item in findings], [self.record, "(outside workspace)"])
        self.assertNotIn(str(self.root), state_path.read_text(encoding="utf-8"))
        self.assertNotIn("private-external-path", state_path.read_text(encoding="utf-8"))

    def test_existing_stop_continuation_never_launches_more_checks(self):
        self.bind()
        self.changed()
        with self.successful_runner() as runner:
            self.assertEqual(module.run_hook(self.root, "codex", "stop", self.payload(
                "codex", stop_hook_active=True)), ({}, "", 0))
            runner.assert_not_called()

    def test_only_explicitly_selected_artifact_and_evidence_checks_run(self):
        index = self.write("tasks/example/review-index.json", '{"schema_version": 1}\n')
        baseline = self.write("tasks/example/baseline.json", '{"schema_version": 1}\n')
        artifact = self.write("tasks/example/requirement.md", "# Selected requirement\n")
        case = self.write("tasks/example/selected.feature", "Feature: Selected behavior\n")
        self.bind(index=index, baseline=baseline, artifacts=[artifact], cases=[case])
        self.changed()
        with self.successful_runner() as runner:
            module.run_hook(self.root, "codex", "stop", self.payload("codex"))
        commands = [call.args[0] for call in runner.call_args_list]
        self.assertTrue(any("validate" in command and "assurance" not in command for command in commands))
        for operation, argument in (("index", index), ("validate", baseline)):
            matching = [command for command in commands
                        if "assurance" in command and command[command.index("assurance") + 1] == operation]
            self.assertEqual(len(matching), 1)
            self.assertIn("--require-current", matching[0])
            self.assertTrue(any(str(value).endswith(argument) for value in matching[0]))
        for operation, argument in (("lint", artifact), ("gherkin", case)):
            matching = [command for command in commands if operation in command]
            self.assertEqual(len(matching), 1)
            self.assertTrue(any(str(value).endswith(argument) for value in matching[0]))
        for command in commands:
            self.assertNotIn("save", command)
            self.assertNotIn("complete", command)
            self.assertNotIn("compile", command)

    def test_unknown_client_and_event_are_rejected_without_execution(self):
        with self.successful_runner() as runner:
            with self.assertRaises(WorkbenchError):
                module.run_hook(self.root, "unknown-client", "start", self.payload("codex"))
            with self.assertRaises(WorkbenchError):
                module.run_hook(self.root, "codex", "unknown-event", self.payload("codex"))
            runner.assert_not_called()

    def test_timeout_is_a_bounded_advisory_without_command_output(self):
        self.bind()
        self.changed()
        with patch.object(module.subprocess, "run", side_effect=subprocess.TimeoutExpired(
                ["private command argument"], timeout=1, output="private captured output")):
            output, diagnostic, code = module.run_hook(self.root, "codex", "stop", self.payload("codex"))
        self.assertEqual((diagnostic, code), ("", 0))
        self.assertTrue(output["systemMessage"])
        self.assertNotIn("private command argument", json.dumps(output))
        self.assertNotIn("private captured output", json.dumps(output))
        self.assertNotIn("decision", output)

    def test_concurrent_duplicate_event_is_bounded_without_duplicate_execution(self):
        self.bind(watch=[self.code])
        self.changed(self.code)
        entered, release = Event(), Event()

        def validate(*args, **options):
            entered.set()
            self.assertTrue(release.wait(3), "The test must release its controlled validator.")
            return SimpleNamespace(returncode=0, stdout='{"valid": true}', stderr="")

        with patch.object(module.subprocess, "run", side_effect=validate) as runner:
            with ThreadPoolExecutor(max_workers=2) as pool:
                first = pool.submit(module.run_hook, self.root, "codex", "stop", self.payload("codex"))
                self.assertTrue(entered.wait(3))
                try:
                    duplicate = pool.submit(module.run_hook, self.root, "codex", "stop", self.payload("codex"))
                    with self.assertRaisesRegex(WorkbenchError, "already running"):
                        duplicate.result(timeout=3)
                finally:
                    release.set()
                self.assertEqual(first.result(timeout=3), ({}, "", 0))
            runner.assert_called_once()

    def test_source_changed_during_validation_is_checked_again(self):
        self.bind(watch=[self.code])
        self.changed(self.code)
        calls = []

        def validate(*args, **options):
            calls.append(args[0])
            if len(calls) == 1:
                self.changed(self.code)
            return SimpleNamespace(returncode=0, stdout='{"valid": true}', stderr="")

        with patch.object(module.subprocess, "run", side_effect=validate):
            module.run_hook(self.root, "codex", "stop", self.payload("codex"))
            module.run_hook(self.root, "codex", "stop", self.payload("codex"))
        self.assertEqual(len(calls), 2, "A check must not cover bytes written after its starting fingerprint.")

    def test_binding_rejects_outside_paths_symlinks_directories_and_missing_records(self):
        outside = self.root.parent / "outside.md"
        outside.write_text("Outside content must stay private.\n", encoding="utf-8")
        link = self.root / "record-link.md"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            link = None
        invalid = ("../outside.md", str(outside), "tasks/example", "missing.md")
        if link is not None:
            invalid += ("record-link.md",)
        for record in invalid:
            with self.subTest(record=record):
                with self.assertRaises(WorkbenchError):
                    module.bind_scope(self.root, "codex", "scope-session", record)
        self.assertEqual(outside.read_text(encoding="utf-8"), "Outside content must stay private.\n")

    def test_invalid_payload_and_identifiers_do_not_create_scope_or_run_checks(self):
        cases = [None, [], {}, {"session_id": 42}, {"session_id": ""}, {"session_id": "bad\x00id"}]
        for payload in cases:
            with self.subTest(payload=payload), self.successful_runner() as runner:
                with self.assertRaises(WorkbenchError):
                    module.run_hook(self.root, "codex", "stop", payload)
                runner.assert_not_called()
        self.assertFalse((self.root / ".workbench").exists())

    def test_missing_watched_file_after_binding_reports_advisory_without_recreation(self):
        self.bind(watch=[self.code])
        (self.root / self.code).unlink()
        before = self.snapshot()
        output, diagnostic, code = module.run_hook(self.root, "codex", "stop", self.payload("codex"))
        self.assertEqual((diagnostic, code), ("", 0))
        self.assertTrue(output.get("systemMessage"))
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / self.code).exists())

    def test_generated_workspace_uses_installed_runtime_and_retains_domain_bytes(self):
        generated = self.root.parent / "generated workspace"
        initialize_workspace(generated)
        self.assertFalse((generated / "core/cli.py").exists())
        record = generated / "tasks/example/01-intake.md"
        record.parent.mkdir(parents=True)
        record.write_text("# Declared work\n", encoding="utf-8")
        module.bind_scope(generated, "codex", "generated-session", "tasks/example/01-intake.md")
        record.write_text("# Declared work\nUpdated current view.\n", encoding="utf-8")
        before = {str(path.relative_to(generated)): path.read_bytes() for path in generated.rglob("*")
                  if path.is_file() and ".workbench" not in path.relative_to(generated).parts}
        output, diagnostic, code = module.run_hook(generated, "codex", "stop", {
            "session_id": "generated-session", "cwd": str(generated)})
        self.assertEqual((output, diagnostic, code), ({}, "", 0))
        after = {str(path.relative_to(generated)): path.read_bytes() for path in generated.rglob("*")
                 if path.is_file() and ".workbench" not in path.relative_to(generated).parts}
        self.assertEqual(after, before)
        self.assertFalse((generated / ".workbench/actions.sqlite3").exists())


if __name__ == "__main__":
    unittest.main()
