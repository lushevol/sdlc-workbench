"""Exercise OpenKB's canonical-source boundary without its optional runtime."""

from contextlib import nullcontext, redirect_stdout
from dataclasses import dataclass
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import AsyncMock, Mock, patch


SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/llm-wiki/scripts/wiki.py"
SPEC = importlib.util.spec_from_file_location("workbench_openkb_workflow", SCRIPT)
WIKI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WIKI)


@dataclass(frozen=True)
class FakeCredentialBundle:
    api_key: str | None = None
    base_url: str | None = None
    timeout: int = 27


class OpenKBWorkflowTests(unittest.TestCase):
    fixture_url = "https://fixture.invalid/v1"
    fixture_token = "synthetic-routing-token"

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="workbench-openkb-")
        self.addCleanup(self.temporary.cleanup)
        self.project = (Path(self.temporary.name) / "project").resolve()
        self.candidates = self.project / "knowledge/candidates"
        self.candidates.mkdir(parents=True)
        self.kb = self.project / "knowledge/llm-wiki"
        self.registry_path = self.kb / ".openkb/hashes.json"
        self.manifest_path = self.kb / "source-manifest.json"
        self.registry_path.parent.mkdir(parents=True)
        self.registry_path.write_text("{}\n", encoding="utf-8")
        self.manifest_path.write_text(
            json.dumps({"engine": "OpenKB", "sources": []}) + "\n", encoding="utf-8"
        )
        self.compiler = AsyncMock()
        self.setup_key = Mock()
        self.append_log = Mock()
        self.native_main = Mock()
        self.effective_config = Mock(return_value=({"model": "test/model"}, {}))
        self.lint_checks = {name: Mock(return_value=[]) for name in (
            "find_broken_links", "find_orphans", "find_missing_entries", "check_index_sync",
            "find_invalid_frontmatter", "find_missing_okf_fields",
        )}
        self.lint_report = Mock(return_value="Native structural lint report")
        modules = {}
        for name, attributes in {
            "openkb": {},
            "openkb.agent": {},
            "openkb.agent.compiler": {"compile_short_doc": self.compiler},
            "openkb.cli": {"_setup_llm_key": self.setup_key,
                           "cli": SimpleNamespace(main=self.native_main)},
            "openkb.config": {
                "resolve_effective_config": self.effective_config,
                "resolve_concurrency": Mock(return_value=2),
                "resolve_credential_bundle": Mock(return_value=FakeCredentialBundle()),
            },
            "openkb.locks": {"kb_ingest_lock": Mock(side_effect=lambda _: nullcontext())},
            "openkb.log": {"append_log": self.append_log},
            "openkb.lint": {**self.lint_checks, "run_structural_lint": self.lint_report},
            "litellm": {"api_base": "https://inherited-fixture.invalid", "api_key": "inherited-synthetic-token"},
        }.items():
            module = ModuleType(name)
            module.__dict__.update(attributes)
            module.__path__ = []
            modules[name] = module
        self.module_patch = patch.dict(sys.modules, modules)
        self.module_patch.start()
        self.addCleanup(self.module_patch.stop)

    def record(self, relative="topic.md", identifier="TOPIC", body="Canonical full text.\n"):
        path = self.candidates / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nid: {identifier}\nstatus: candidate\n---\n\n{body}", encoding="utf-8")
        return path

    def compile(self):
        with patch.object(WIKI, "configured_credentials", return_value=(self.fixture_url, self.fixture_token)), \
                redirect_stdout(io.StringIO()):
            WIKI.compile_sources(self.project, "knowledge/candidates")

    def state_bytes(self):
        return self.registry_path.read_bytes(), self.manifest_path.read_bytes()

    def old_binding(self, source):
        sha = hashlib.sha256(f"previous-{source.stem}".encode()).hexdigest()
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        registry[sha] = {"doc_name": source.stem, "path": f"raw/{source.name}"}
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        manifest["sources"].append({
            "doc_name": source.stem, "id": source.stem.upper(),
            "origin": source.relative_to(self.project).as_posix(), "sha256": sha,
        })
        self.registry_path.write_text(json.dumps(registry) + "\n", encoding="utf-8")
        self.manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        return sha

    def test_native_semantic_compiler_reads_linked_full_text_without_changing_canonical_bytes(self):
        source = self.record(body="## Detailed source\n\nEvidence with a Unicode symbol: \u03b1.\n")
        original = source.read_bytes()

        async def inspect_source(doc_name, full_text, kb, model, **kwargs):
            self.assertEqual(doc_name, "topic")
            self.assertEqual(kb, self.kb)
            self.assertEqual(model, "test/model")
            self.assertEqual(kwargs, {"max_concurrency": 2, "bundle": FakeCredentialBundle(
                base_url=self.fixture_url, api_key=self.fixture_token,
            )})
            self.assertTrue(full_text.is_symlink())
            self.assertEqual(full_text.resolve(), source)
            self.assertEqual(full_text.read_bytes(), original)
            self.assertFalse(os.path.isabs(os.readlink(full_text)))
            (kb / "wiki/summaries").mkdir()
            (kb / "wiki/summaries/topic.md").write_text("Derived summary.\n", encoding="utf-8")

        self.compiler.side_effect = inspect_source
        self.compile()

        self.compiler.assert_awaited_once()
        self.assertEqual(source.read_bytes(), original)
        self.assertTrue((self.kb / "raw/topic.md").is_symlink())
        self.assertEqual((self.kb / "raw/topic.md").resolve(), source)
        sha = hashlib.sha256(original).hexdigest()
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        self.assertEqual(registry[sha]["source_path"], "wiki/sources/topic.md")
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["sources"], [{
            "doc_name": "topic", "id": "TOPIC", "origin": "knowledge/candidates/topic.md", "sha256": sha,
            "status": "candidate",
        }])
        self.append_log.assert_called_once()

    def test_compiled_binding_preserves_present_governance_metadata(self):
        source = self.record()
        source.write_text(source.read_text(encoding="utf-8").replace(
            "status: candidate\n", "status: candidate\nversion: 3\ngovernance_state: draft\n"
        ), encoding="utf-8")
        canonical = source.read_bytes()

        self.compile()

        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        binding = manifest["sources"][0]
        self.assertEqual(binding["version"], 3)
        self.assertEqual(binding["status"], "candidate")
        self.assertEqual(binding["governance_state"], "draft")
        self.assertEqual(source.read_bytes(), canonical)

    def test_provider_failure_preserves_existing_binding_and_canonical_bytes(self):
        source = self.record()
        self.old_binding(source)
        original = source.read_bytes()
        state = self.state_bytes()
        self.compiler.side_effect = RuntimeError("provider unavailable")

        with self.assertRaisesRegex(RuntimeError, "provider unavailable"):
            self.compile()

        self.assertEqual(self.state_bytes(), state)
        self.assertEqual(source.read_bytes(), original)
        self.append_log.assert_not_called()

    def test_concurrent_canonical_change_leaves_binding_unchanged(self):
        source = self.record()
        self.old_binding(source)
        state = self.state_bytes()
        newer = source.read_bytes() + b"Concurrent author's new requirement.\n"

        async def concurrent_writer(*args, **kwargs):
            source.write_bytes(newer)

        self.compiler.side_effect = concurrent_writer
        with self.assertRaisesRegex(ValueError, "Source changed during compilation; binding not advanced"):
            self.compile()

        self.assertEqual(self.state_bytes(), state)
        self.assertEqual(source.read_bytes(), newer)
        self.append_log.assert_not_called()

    def test_only_successful_documents_advance_their_binding(self):
        success = self.record("a.md", "A")
        failure = self.record("b.md", "B")
        old_success = self.old_binding(success)
        old_failure = self.old_binding(failure)
        previous_registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        previous_manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.compiler.side_effect = [None, RuntimeError("second document failed")]

        with self.assertRaisesRegex(RuntimeError, "second document failed"):
            self.compile()

        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        bindings = {item["doc_name"]: item for item in manifest["sources"]}
        sha = hashlib.sha256(success.read_bytes()).hexdigest()
        self.assertNotIn(old_success, registry)
        self.assertEqual(registry[sha]["doc_name"], "a")
        self.assertEqual(registry[old_failure], previous_registry[old_failure])
        self.assertEqual(bindings["a"]["sha256"], sha)
        self.assertEqual(bindings["b"], previous_manifest["sources"][1])
        self.assertEqual(self.compiler.await_count, 2)
        self.append_log.assert_called_once()

    def test_conflicting_duplicate_record_ids_are_rejected_before_compilation(self):
        self.record("a.md", "SAME", "First requirement.\n")
        self.record("b.md", "SAME", "Different requirement.\n")
        state = self.state_bytes()

        with self.assertRaisesRegex(ValueError, "Conflicting canonical records for SAME"):
            self.compile()

        self.assertEqual(self.state_bytes(), state)
        self.compiler.assert_not_awaited()
        self.setup_key.assert_not_called()
        self.assertFalse((self.kb / "raw").exists())

    def test_identical_duplicate_ids_compile_once_from_deepest_canonical_record(self):
        shallow = self.record("topic.md")
        deep = self.record("security/topic.md")

        self.compile()

        self.compiler.assert_awaited_once()
        self.assertEqual((self.kb / "wiki/sources/topic.md").resolve(), deep)
        self.assertEqual(shallow.read_bytes(), deep.read_bytes())
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["sources"][0]["origin"], "knowledge/candidates/security/topic.md")

    def test_external_canonical_symlink_is_rejected_before_provider_setup(self):
        outside = Path(self.temporary.name) / "outside.md"
        outside.write_text("---\nid: EXTERNAL\n---\nOutside project.\n", encoding="utf-8")
        (self.candidates / "external.md").symlink_to(outside)
        state = self.state_bytes()

        with self.assertRaises(ValueError):
            self.compile()

        self.assertEqual(self.state_bytes(), state)
        self.compiler.assert_not_awaited()
        self.setup_key.assert_not_called()
        self.assertFalse((self.kb / "raw").exists())

    def test_colliding_source_filenames_are_rejected_before_compilation(self):
        self.record("security/topic.md", "SECURITY")
        self.record("architecture/topic.md", "ARCHITECTURE")

        with self.assertRaisesRegex(ValueError, "Canonical filename collision"):
            self.compile()

        self.compiler.assert_not_awaited()
        self.setup_key.assert_not_called()

    def test_verify_rejects_every_native_structural_finding_including_frontmatter_and_schema(self):
        self.record()
        self.compile()

        for name, check in self.lint_checks.items():
            with self.subTest(check=name):
                finding = f"{name}: invalid generated page"
                check.return_value = [finding]
                output = io.StringIO()
                with patch("importlib.metadata.version", return_value=WIKI.VERSION), redirect_stdout(output):
                    with self.assertRaisesRegex(ValueError, finding):
                        WIKI.verify(self.project)
                self.assertIn("Native structural lint report", output.getvalue())
                self.assertNotIn("Verified OpenKB", output.getvalue())
                check.return_value = []

        self.setup_key.assert_called_once()

    def test_verify_calls_native_structural_checks_with_the_knowledge_workspace(self):
        self.record()
        self.compile()

        with patch("importlib.metadata.version", return_value=WIKI.VERSION), redirect_stdout(io.StringIO()):
            WIKI.verify(self.project)

        for name, check in self.lint_checks.items():
            if name == "find_missing_entries":
                check.assert_called_once_with(self.kb / "raw", self.kb / "wiki", kb_dir=self.kb)
            else:
                check.assert_called_once_with(self.kb / "wiki")
        self.lint_report.assert_called_once_with(self.kb)

    def run_main(self, *arguments):
        python = Path(sys.prefix) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        with patch.object(WIKI, "runtime_python", return_value=python), \
                patch.object(sys, "argv", [str(SCRIPT), "--project", str(self.project), *arguments]):
            WIKI.main()

    def test_native_source_owning_commands_are_blocked(self):
        for command in ("add", "remove", "watch", "init", "recompile", "use", "delete-kb", "chat"):
            with self.subTest(command=command):
                with self.assertRaisesRegex(ValueError, "use compile"):
                    self.run_main("run", command)
        self.native_main.assert_not_called()

    def test_native_separator_cannot_bypass_source_command_guard(self):
        for command in ("add", "remove"):
            with self.subTest(command=command):
                with self.assertRaisesRegex(ValueError, "use compile"):
                    self.run_main("run", "--", command, "topic.md")
        self.native_main.assert_not_called()

    def test_native_query_and_knowledge_graph_are_forwarded_to_openkb(self):
        with patch.dict(os.environ, {
            "OPENAI_API_BASE": self.fixture_url, "LLM_API_KEY": self.fixture_token,
        }, clear=True):
            self.run_main("run", "query", "What is the renewal policy?")
        self.native_main.assert_called_once_with(
            args=["--kb-dir", str(self.kb), "query", "What is the renewal policy?"], standalone_mode=False
        )
        self.native_main.reset_mock()

        with patch.dict(os.environ, {}, clear=True):
            self.run_main("graph")

        self.native_main.assert_called_once_with(
            args=["--kb-dir", str(self.kb), "visualize", "--no-open"], standalone_mode=False
        )
        self.setup_key.assert_not_called()

    def test_explicit_url_and_token_are_both_required_to_select_openkb(self):
        for url, token, engine in (
            ("", "", "llm-wiki-agent"),
            (self.fixture_url, "", "llm-wiki-agent"),
            ("", self.fixture_token, "llm-wiki-agent"),
            (" ", "\t", "llm-wiki-agent"),
            (self.fixture_url, self.fixture_token, "openkb"),
        ):
            with self.subTest(url_present=bool(url.strip()), token_present=bool(token.strip())):
                with patch.dict(os.environ, {"OPENAI_API_BASE": url, "LLM_API_KEY": token}, clear=True):
                    self.assertEqual(WIKI.selected_engine(self.project), engine)

    def test_provider_key_or_root_dotenv_does_not_select_openkb(self):
        (self.project / ".env").write_text(
            f"OPENAI_API_BASE={self.fixture_url}\nLLM_API_KEY={self.fixture_token}\n", encoding="utf-8"
        )
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": self.fixture_token}, clear=True):
            self.assertEqual(WIKI.selected_engine(self.project), "llm-wiki-agent")
            self.assertEqual(WIKI.configured_credentials(self.project), ("", ""))

    def test_kb_local_explicit_pair_overrides_environment_and_is_not_interpolated(self):
        local = self.kb / ".env"
        literal_token = "${ROUTING_FIXTURE_TOKEN}"
        local.write_text(
            f'export OPENAI_API_BASE="{self.fixture_url}" # local URL\nLLM_API_KEY=\'{literal_token}\'\n',
            encoding="utf-8",
        )
        with patch.dict(sys.modules, {"dotenv": None}), patch.dict(os.environ, {
            "OPENAI_API_BASE": "https://different-fixture.invalid", "LLM_API_KEY": "other-synthetic-token",
            "ROUTING_FIXTURE_TOKEN": "must-not-expand",
        }, clear=True):
            self.assertEqual(WIKI.configured_credentials(self.project), (self.fixture_url, literal_token))
            self.assertEqual(WIKI.selected_engine(self.project), "openkb")

    def test_missing_kb_local_value_can_use_its_explicit_environment_value(self):
        local = self.kb / ".env"
        local.write_text(f"OPENAI_API_BASE={self.fixture_url} # synthetic URL\nLLM_API_KEY=\n", encoding="utf-8")
        with patch.dict(sys.modules, {"dotenv": None}), patch.dict(os.environ, {
            "LLM_API_KEY": self.fixture_token,
        }, clear=True):
            self.assertEqual(WIKI.configured_credentials(self.project), (self.fixture_url, self.fixture_token))
            self.assertEqual(WIKI.selected_engine(self.project), "openkb")

    def test_whitespace_only_local_values_use_explicit_environment_values(self):
        (self.kb / ".env").write_text('OPENAI_API_BASE="  "\nLLM_API_KEY=\'   \'\n', encoding="utf-8")
        with patch.dict(os.environ, {
            "OPENAI_API_BASE": self.fixture_url, "LLM_API_KEY": self.fixture_token,
        }, clear=True):
            self.assertEqual(WIKI.configured_credentials(self.project), (self.fixture_url, self.fixture_token))
            self.assertEqual(WIKI.selected_engine(self.project), "openkb")

    def test_incomplete_local_credentials_select_ade_without_dotenv_dependency(self):
        (self.kb / ".env").write_text(f"OPENAI_API_BASE={self.fixture_url}\n", encoding="utf-8")
        missing_runtime = self.project / ".venv-openkb/bin/python"
        output = io.StringIO()
        with patch.dict(sys.modules, {"dotenv": None}), patch.dict(os.environ, {}, clear=True), \
                patch.object(WIKI, "runtime_python", return_value=missing_runtime), \
                patch.object(sys, "argv", [str(SCRIPT), "--project", str(self.project), "compile"]), \
                redirect_stdout(output):
            WIKI.main()
        self.assertIn("Selected engine: llm-wiki-agent", output.getvalue())
        self.assertNotIn(self.fixture_url, output.getvalue())
        self.compiler.assert_not_awaited()
        self.native_main.assert_not_called()

    def test_malformed_local_credentials_raise_sanitized_error(self):
        (self.kb / ".env").write_text(f'LLM_API_KEY="{self.fixture_token}\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "complete single-line quoted credential") as error:
            WIKI.configured_credentials(self.project)
        self.assertNotIn(self.fixture_token, str(error.exception))

    def test_semantic_fallback_needs_no_openkb_runtime_and_changes_no_pages(self):
        source = self.record()
        canonical = source.read_bytes()
        state = self.state_bytes()
        missing_runtime = self.project / ".venv-openkb/bin/python"
        for arguments in (("compile",), ("run", "query", "What is the renewal policy?"), ("run", "lint")):
            with self.subTest(operation=arguments[:2]):
                output = io.StringIO()
                with patch.dict(os.environ, {}, clear=True), \
                        patch.object(WIKI, "runtime_python", return_value=missing_runtime), \
                        patch.object(WIKI.subprocess, "run") as subprocess_run, \
                        patch.object(sys, "argv", [str(SCRIPT), "--project", str(self.project), *arguments]), \
                        redirect_stdout(output):
                    WIKI.main()
                self.assertIn("Selected engine: llm-wiki-agent", output.getvalue())
                self.assertIn("Agent handoff only", output.getvalue())
                self.assertIn("no wiki pages were changed", output.getvalue())
                subprocess_run.assert_not_called()
        self.assertEqual(source.read_bytes(), canonical)
        self.assertEqual(self.state_bytes(), state)
        self.compiler.assert_not_awaited()
        self.setup_key.assert_not_called()
        self.native_main.assert_not_called()

    def test_direct_semantic_compilation_rejects_incomplete_credentials(self):
        self.record()
        state = self.state_bytes()
        for url, token in (("", ""), (self.fixture_url, ""), ("", self.fixture_token)):
            with self.subTest(url_present=bool(url), token_present=bool(token)):
                with patch.dict(os.environ, {"OPENAI_API_BASE": url, "LLM_API_KEY": token}, clear=True):
                    with self.assertRaisesRegex(ValueError, "requires both OPENAI_API_BASE and LLM_API_KEY"):
                        WIKI.compile_sources(self.project, "knowledge/candidates")
        self.assertEqual(self.state_bytes(), state)
        self.compiler.assert_not_awaited()
        self.setup_key.assert_not_called()

    def unsupported_api_configs(self):
        yield {"model": "chatgpt/fixture-model"}
        yield {"model": "github_copilot/fixture-model"}
        for key in ("api_base", "api_key", "base_url", "provider_key"):
            yield {"model": "test/model", "litellm": {key: "synthetic-override"}}

    def test_compile_rejects_oauth_models_and_litellm_credential_overrides(self):
        self.record()
        state = self.state_bytes()
        for config in self.unsupported_api_configs():
            with self.subTest(config=config):
                self.effective_config.return_value = (config, {})
                with self.assertRaises(ValueError):
                    self.compile()
        self.assertEqual(self.state_bytes(), state)
        self.assertFalse((self.kb / "raw").exists())
        self.compiler.assert_not_awaited()
        self.setup_key.assert_not_called()

    def test_native_semantic_commands_reject_oauth_and_credential_overrides(self):
        for config in self.unsupported_api_configs():
            with self.subTest(config=config), patch.dict(os.environ, {
                "OPENAI_API_BASE": self.fixture_url, "LLM_API_KEY": self.fixture_token,
            }, clear=True):
                self.effective_config.return_value = (config, {})
                with self.assertRaises(ValueError):
                    self.run_main("run", "query", "Fixture question")
        self.native_main.assert_not_called()
        self.setup_key.assert_not_called()

    def test_native_semantic_commands_enforce_selected_url_alias_and_client_settings(self):
        litellm = sys.modules["litellm"]

        def inspect_client(*args, **kwargs):
            self.assertEqual(os.environ["OPENAI_API_BASE"], self.fixture_url)
            self.assertEqual(os.environ["OPENAI_BASE_URL"], self.fixture_url)
            self.assertEqual(os.environ["LLM_API_KEY"], self.fixture_token)
            self.assertEqual(litellm.api_base, self.fixture_url)
            self.assertEqual(litellm.api_key, self.fixture_token)

        self.native_main.side_effect = inspect_client
        for command in ("query", "lint"):
            with self.subTest(command=command), patch.dict(os.environ, {
                "OPENAI_API_BASE": self.fixture_url, "LLM_API_KEY": self.fixture_token,
                "OPENAI_BASE_URL": "https://conflicting-fixture.invalid",
            }, clear=True):
                self.run_main("run", command, "Fixture argument")
        self.assertEqual(self.native_main.call_count, 2)

    def test_engine_report_exposes_presence_flags_without_credentials(self):
        output = io.StringIO()
        with patch.dict(os.environ, {
            "OPENAI_API_BASE": self.fixture_url, "LLM_API_KEY": self.fixture_token,
        }, clear=True), redirect_stdout(output):
            self.run_main("engine")
        self.assertNotIn(self.fixture_url, output.getvalue())
        self.assertNotIn(self.fixture_token, output.getvalue())
        report = json.loads(output.getvalue())
        self.assertEqual(report["engine"], "openkb")
        self.assertTrue(report["url_configured"])
        self.assertTrue(report["token_configured"])

    def test_native_status_remains_available_without_provider_credentials(self):
        with patch.dict(os.environ, {}, clear=True):
            self.run_main("run", "status")
        self.native_main.assert_called_once_with(
            args=["--kb-dir", str(self.kb), "status"], standalone_mode=False
        )
        self.setup_key.assert_not_called()


if __name__ == "__main__":
    unittest.main()
