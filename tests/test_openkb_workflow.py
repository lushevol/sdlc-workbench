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

    def compile(self, **kwargs):
        with patch.object(WIKI, "configured_credentials", return_value=(self.fixture_url, self.fixture_token)), \
                redirect_stdout(io.StringIO()):
            return WIKI.compile_sources(self.project, "knowledge/candidates", **kwargs)

    def state_bytes(self):
        return self.registry_path.read_bytes(), self.manifest_path.read_bytes()

    def assert_bindings_unchanged_with_failed_attempt(self, state):
        self.assertEqual(self.registry_path.read_bytes(), state[0])
        manifest = json.loads(self.manifest_path.read_text())
        self.assertEqual(manifest["sources"], json.loads(state[1])["sources"])
        self.assertEqual(manifest["incremental"]["attempts"]["topic"]["status"], "failed")

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

        self.assert_bindings_unchanged_with_failed_attempt(state)
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

        self.assert_bindings_unchanged_with_failed_attempt(state)
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
        self.record()
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

    def derived(self, relative, text):
        path = self.kb / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    async def synthetic_compiler(self, doc_name, *args, **kwargs):
        self.derived(f"wiki/summaries/{doc_name}.md", f"Synthetic summary for {doc_name}.\n")
        summaries = sorted(path.stem for path in (self.kb / "wiki/summaries").glob("*.md"))
        self.derived("wiki/index.md", "\n".join(f"[[summaries/{name}]]" for name in summaries))

    def receipt(self, sources, recipe="default"):
        selected = [source.relative_to(self.project).as_posix() for source in sources]
        plan = WIKI.update_plan(self.project, selected=selected, recipe=recipe)
        state = WIKI.wiki_state(self.kb)[0]["incremental"]
        reviewed = {"recipe": recipe, "engine": "openkb", "reviewed_by": "Synthetic test reviewer",
                    "reviewed_at": "2026-11-12T12:00:00+00:00", "review_note": "Synthetic fixture review only.",
                    "sources": [], "outputs": []}
        owners = {}
        for completion in state["completed"].values():
            for relative in completion["outputs"]:
                owners.setdefault(relative, set()).add(completion["id"])
        for item in plan["records"]:
            reviewed["sources"].append({"path": item["path"], "sha256": item["sha256"], "outputs": item["expected_outputs"],
                                        "unchanged_reason": "Synthetic fixture summary intentionally does not synthesize changed requirements."})
            for relative in item["expected_outputs"]:
                owners.setdefault(relative, set()).add(item["id"])
        for relative in sorted({relative for item in plan["records"] for relative in item["expected_outputs"]}):
            path = self.kb / relative
            reviewed["outputs"].append({"path": relative, "sha256": WIKI.digest(path) if path.is_file() else None,
                                        "sources": sorted(owners[relative]), "note": "Reviewed synthetic fixture bytes."})
        output_hashes = {item["path"]: item["sha256"] for item in reviewed["outputs"]}
        for source in reviewed["sources"]:
            attempt = state["attempts"].get(Path(source["path"]).stem, {})
            before = attempt.get("output_before", {})
            changed = sorted(relative for relative in source["outputs"]
                             if before.get(relative) != output_hashes.get(relative))
            if changed:
                source["claim_review"] = {
                    "changed_outputs": [{"path": relative, "change_type": "additive", "removed_claims": []}
                                         for relative in changed],
                    "review_note": "Synthetic fixture claim review accounted for every changed output.",
                }
        return reviewed

    def review(self, receipt):
        with patch("importlib.metadata.version", return_value=WIKI.VERSION), redirect_stdout(io.StringIO()):
            return WIKI.review_sources(self.project, receipt)

    def complete(self, *sources):
        self.compiler.side_effect = self.synthetic_compiler
        self.compile(selected=[source.relative_to(self.project).as_posix() for source in sources])
        self.review(self.receipt(sources))

    def test_reviewed_unchanged_rerun_makes_zero_additional_compiler_calls(self):
        source = self.record()
        self.complete(source)
        state = self.state_bytes()
        self.compiler.reset_mock()
        self.setup_key.reset_mock()
        self.effective_config.reset_mock()

        plan = self.compile()

        self.assertEqual(plan["counts"], {"unchanged": 1})
        self.assertEqual(self.state_bytes(), state)
        self.compiler.assert_not_awaited()
        self.setup_key.assert_not_called()
        self.effective_config.assert_not_called()

    def test_compiler_return_is_pending_until_explicit_review(self):
        self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        self.compiler.reset_mock()

        plan = self.compile()

        self.assertEqual(plan["counts"], {"pending_review": 1})
        self.assertFalse(WIKI.wiki_state(self.kb)[0]["incremental"]["completed"])
        self.compiler.assert_not_awaited()

    def test_legacy_binding_bootstraps_review_without_automatic_recompile(self):
        source = self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        manifest = json.loads(self.manifest_path.read_text())
        manifest.pop("incremental")
        self.manifest_path.write_text(json.dumps(manifest))
        self.compiler.reset_mock()

        self.assertEqual(self.compile()["counts"], {"bootstrap_review": 1})
        self.compiler.assert_not_awaited()
        self.review(self.receipt([source]))
        self.assertEqual(self.compile()["counts"], {"unchanged": 1})
        self.compile(force=True)
        self.compiler.assert_awaited_once()

    def test_exact_changed_record_preserves_other_source_and_shared_output_receipts(self):
        first, second = self.record("a.md", "A"), self.record("b.md", "B")
        self.complete(first, second)
        other_summary = (self.kb / "wiki/summaries/b.md").read_bytes()
        first.write_text(first.read_text() + "Changed requirement.\n")
        self.compiler.reset_mock()

        self.compile(selected=[first.relative_to(self.project).as_posix()])
        self.review(self.receipt([first]))

        self.compiler.assert_awaited_once()
        self.assertEqual(self.compiler.await_args.args[0], "a")
        self.assertEqual((self.kb / "wiki/summaries/b.md").read_bytes(), other_summary)
        self.assertEqual(WIKI.update_plan(self.project)["counts"], {"unchanged": 2})

    def test_changed_or_deleted_reviewed_outputs_require_scoped_repair(self):
        source = self.record()
        self.complete(source)
        summary = self.kb / "wiki/summaries/topic.md"
        self.compiler.reset_mock()
        for mutation in (lambda: summary.write_text("Unreviewed output edit."), summary.unlink):
            mutation()
            self.assertEqual(self.compile()["counts"], {"repair_review": 1})
        self.compiler.assert_not_awaited()

    def test_new_and_missing_requested_records_cannot_be_skipped(self):
        source = self.record()
        relative = source.relative_to(self.project).as_posix()
        self.assertEqual(WIKI.update_plan(self.project, selected=[relative])["counts"], {"new": 1})
        self.complete(source)
        source.unlink()
        with self.assertRaisesRegex(ValueError, "Requested canonical record is missing"):
            WIKI.update_plan(self.project, selected=[relative])
        self.assertEqual(WIKI.update_plan(self.project)["counts"], {"missing": 1})
        self.assertEqual(len(json.loads(self.manifest_path.read_text())["sources"]), 1)

    def test_exact_selection_rejects_escape_derived_navigation_and_out_of_scope(self):
        self.record()
        outside = self.project / "outside.md"
        outside.write_text("---\nid: OUTSIDE\n---\n")
        for relative in ("outside.md", "../outside.md", str(outside), "knowledge/llm-wiki/wiki/index.md"):
            with self.subTest(path=relative), self.assertRaises(ValueError):
                WIKI.update_plan(self.project, selected=[relative])

    def test_partial_generation_missing_output_cannot_receive_completion(self):
        source = self.record()
        self.compile()
        self.derived("wiki/index.md", "Index only; summary generation was partial.")
        with self.assertRaisesRegex(ValueError, "missing or changed"):
            self.review(self.receipt([source]))
        state = WIKI.wiki_state(self.kb)[0]["incremental"]
        self.assertFalse(state["completed"])
        self.assertEqual(state["attempts"]["topic"]["status"], "pending_review")

    def test_changed_output_requires_explicit_claim_review(self):
        source = self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        self.derived("wiki/summaries/topic.md", "A changed derived claim.\n")
        receipt = self.receipt([source])
        receipt["sources"][0].pop("claim_review")
        with self.assertRaisesRegex(ValueError, "explicit claim review"):
            self.review(receipt)

    def test_removed_claim_review_requires_classification_and_evidence(self):
        source = self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        self.derived("wiki/summaries/topic.md", "A changed derived claim.\n")
        receipt = self.receipt([source])
        changed = receipt["sources"][0]["claim_review"]["changed_outputs"][0]
        changed["change_type"] = "removal"
        changed["removed_claims"] = [{
            "claim": "A prior implementation fact",
            "claim_type": "implementation",
            "disposition": "preserved",
            "evidence": [],
        }]
        with self.assertRaisesRegex(ValueError, "supporting evidence"):
            self.review(receipt)

    def test_replacement_claim_review_requires_removed_claim(self):
        source = self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        self.derived("wiki/summaries/topic.md", "A replacement that drops an old fact.\n")
        receipt = self.receipt([source])
        changed = receipt["sources"][0]["claim_review"]["changed_outputs"][0]
        changed["change_type"] = "replacement"
        with self.assertRaisesRegex(ValueError, "Replacement, removal, or mixed"):
            self.review(receipt)

    def test_recipe_and_schema_changes_invalidate_completed_sources(self):
        source = self.record()
        self.complete(source)
        self.assertEqual(WIKI.update_plan(self.project, recipe="different-settings")["counts"], {"recipe_changed": 1})
        self.derived("wiki/AGENTS.md", "A changed semantic output contract.")
        self.assertEqual(WIKI.update_plan(self.project)["counts"], {"recipe_changed": 1})

    def test_failed_attempt_stays_visible_and_retryable(self):
        self.record()
        self.compiler.side_effect = RuntimeError("Synthetic provider failure")
        with self.assertRaises(RuntimeError):
            self.compile()
        self.assertEqual(WIKI.update_plan(self.project)["counts"], {"retry": 1})
        manifest = WIKI.wiki_state(self.kb)[0]
        self.assertEqual(manifest["incremental"]["attempts"]["topic"]["status"], "failed")
        self.compiler.side_effect = self.synthetic_compiler
        self.assertEqual(self.compile()["counts"], {"pending_review": 1})

    def test_plan_needs_no_engine_runtime_credentials_or_native_calls(self):
        self.record()
        with patch.object(WIKI, "configured_credentials", side_effect=AssertionError("private config")), \
                patch.object(WIKI, "runtime_python", side_effect=AssertionError("engine runtime")), \
                patch.object(sys, "argv", [str(SCRIPT), "--project", str(self.project), "plan"]), \
                redirect_stdout(io.StringIO()) as output:
            WIKI.main()
        self.assertEqual(json.loads(output.getvalue())["counts"], {"new": 1})
        self.compiler.assert_not_awaited()
        self.native_main.assert_not_called()

    def test_review_requires_former_dependents_and_affected_explorations(self):
        source = self.record()
        self.derived("wiki/concepts/prior.md", '---\nsources: ["summaries/topic.md"]\n---\nPrior claim.\n')
        self.derived("wiki/explorations/synthesis.md", "A saved synthesis uses [[concepts/prior]].\n")
        self.complete(source)
        source.write_text(source.read_text() + "The prior claim is withdrawn.\n")
        self.compile()
        receipt = self.receipt([source])
        self.assertIn("wiki/explorations/synthesis.md", receipt["sources"][0]["outputs"])
        receipt["sources"][0]["outputs"].remove("wiki/concepts/prior.md")
        with self.assertRaisesRegex(ValueError, "omitted former"):
            self.review(receipt)
        self.derived("wiki/concepts/prior.md", "The prior unsupported claim was removed after review.\n")
        self.derived("wiki/explorations/synthesis.md", "Stale: source withdrew the prior claim; regenerate only when authorized.\n")
        receipt = self.receipt([source])
        receipt["sources"][0]["outputs"].remove("wiki/concepts/prior.md")
        receipt["sources"][0]["withdrawn_outputs"] = [{"path": "wiki/concepts/prior.md", "reason": "Removed withdrawn claim and source citation."}]
        receipt["sources"][0]["withdrawal_review_note"] = "Reviewed former concept and qualified saved synthesis."
        next(output for output in receipt["outputs"] if output["path"] == "wiki/concepts/prior.md")["sources"] = []
        self.review(receipt)
        self.assertEqual(WIKI.update_plan(self.project)["counts"], {"unchanged": 1})

    def test_shared_output_review_must_explicitly_preserve_other_source_claims(self):
        first, second = self.record("a.md", "A"), self.record("b.md", "B")
        self.complete(first, second)
        receipt = self.receipt([first])
        index = next(output for output in receipt["outputs"] if output["path"] == "wiki/index.md")
        index["sources"].remove("B")
        state = self.state_bytes()
        with self.assertRaisesRegex(ValueError, "omitted preserved source claims"):
            self.review(receipt)
        self.assertEqual(self.state_bytes(), state)

    def test_review_source_race_restores_both_binding_files_and_keeps_semantic_edits(self):
        source = self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        receipt = self.receipt([source])
        state = self.state_bytes()
        original_save = WIKI.save_json

        def racing_save(path, value):
            original_save(path, value)
            if path == self.registry_path:
                source.write_text(source.read_text() + "Concurrent canonical change.\n")

        with patch.object(WIKI, "save_json", side_effect=racing_save), self.assertRaisesRegex(ValueError, "Source changed during review"):
            self.review(receipt)
        self.assertEqual(self.state_bytes(), state)
        self.assertIn("Concurrent", source.read_text())
        self.assertTrue((self.kb / "wiki/summaries/topic.md").is_file())

    def test_review_pair_write_failure_restores_both_provenance_before_images(self):
        source = self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        receipt = self.receipt([source])
        state = self.state_bytes()
        original_save = WIKI.save_json

        def failing_save(path, value):
            if path == self.registry_path:
                raise OSError("Synthetic second binding write failure")
            original_save(path, value)

        with patch.object(WIKI, "save_json", side_effect=failing_save), self.assertRaises(OSError):
            self.review(receipt)
        self.assertEqual(self.state_bytes(), state)

    def test_source_race_before_compilation_stops_without_model_calls(self):
        source = self.record()

        def changed_config(*args):
            source.write_text(source.read_text() + "Concurrent source edit.\n")
            return {"model": "test/model"}, {}

        self.effective_config.side_effect = changed_config
        with self.assertRaisesRegex(ValueError, "Source changed before compilation"):
            self.compile()
        self.compiler.assert_not_awaited()

    def test_compile_noop_avoids_credentials_and_engine_runtime_even_in_public_api(self):
        source = self.record()
        self.complete(source)
        with patch.object(WIKI, "configured_credentials", side_effect=AssertionError("private config")), \
                patch.object(WIKI, "runtime_python", side_effect=AssertionError("engine runtime")), \
                patch.object(sys, "argv", [str(SCRIPT), "--project", str(self.project), "compile"]), \
                redirect_stdout(io.StringIO()):
            WIKI.main()
            WIKI.compile_sources(self.project, "knowledge/candidates")

    def test_ade_handoff_carries_exact_queue_recipe_and_force(self):
        source, other = self.record("a.md", "A"), self.record("b.md", "B")
        relative = source.relative_to(self.project).as_posix()
        with patch.dict(os.environ, {}, clear=True), patch.object(WIKI, "agent_handoff") as handoff:
            self.run_main("compile", "--record", relative, "--recipe", "test-policy", "--force")
        arguments = handoff.call_args.args[3]
        self.assertEqual(arguments, ["--recipe", "test-policy", "--record", relative, "--force"])
        self.assertNotIn(other.relative_to(self.project).as_posix(), arguments)

    def test_unchanged_summary_after_changed_source_requires_explicit_reason(self):
        source = self.record()
        self.complete(source)
        source.write_text(source.read_text() + "Metadata-only fixture change.\n")
        self.compile()
        receipt = self.receipt([source])
        receipt["sources"][0].pop("unchanged_reason")
        with self.assertRaisesRegex(ValueError, "unchanged_reason"):
            self.review(receipt)

    def test_transitive_concepts_entities_and_explorations_remain_in_review_scope(self):
        self.record()
        self.derived("wiki/concepts/a.md", '---\nsources: ["summaries/topic.md"]\n---\nDirect claim.\n')
        self.derived("wiki/concepts/b.md", "An indirect claim from [[concepts/a]].\n")
        self.derived("wiki/entities/c.md", "A dependent entity from [[concepts/b]].\n")
        self.derived("wiki/explorations/d.md", "Saved synthesis from [[entities/c]].\n")
        expected = WIKI.update_plan(self.project)["records"][0]["expected_outputs"]
        self.assertTrue({"wiki/concepts/a.md", "wiki/concepts/b.md", "wiki/entities/c.md", "wiki/explorations/d.md"}.issubset(expected))

    def test_force_cannot_replace_existing_canonical_id_for_same_filename(self):
        source = self.record()
        self.complete(source)
        state = self.state_bytes()
        source.write_text(source.read_text().replace("id: TOPIC", "id: DIFFERENT"))
        self.compiler.reset_mock()
        with self.assertRaisesRegex(ValueError, "filename/ID collision"):
            self.compile(force=True)
        self.assertEqual(self.state_bytes(), state)
        self.compiler.assert_not_awaited()

    def test_new_filename_cannot_duplicate_existing_canonical_id(self):
        source = self.record()
        self.complete(source)
        renamed = self.record("other.md", "TOPIC")
        with self.assertRaisesRegex(ValueError, "another filename binding"):
            WIKI.update_plan(self.project, selected=[renamed.relative_to(self.project).as_posix()])

    def test_plan_source_directory_must_stay_within_canonical_knowledge(self):
        outside = self.project / "other"
        outside.mkdir()
        (outside / "topic.md").write_text("---\nid: OUTSIDE\n---\n")
        with self.assertRaises(ValueError):
            WIKI.update_plan(self.project, source="other")

    def test_review_does_not_overwrite_external_provenance_edit_during_checks(self):
        source = self.record()
        self.compiler.side_effect = self.synthetic_compiler
        self.compile()
        receipt = self.receipt([source])
        for target in (self.manifest_path, self.registry_path):
            state = self.state_bytes()
            marker = json.loads(target.read_text())
            marker["external_edit"] = "Preserve this unrelated writer"
            external = json.dumps(marker).encode()
            def external_writer(*args):
                target.write_bytes(external)
            with patch.object(WIKI, "check_structure", side_effect=external_writer), self.assertRaisesRegex(ValueError, "provenance changed concurrently"):
                self.review(receipt)
            self.assertEqual(target.read_bytes(), external)
            self.registry_path.write_bytes(state[0])
            self.manifest_path.write_bytes(state[1])

    def test_plan_output_cannot_overwrite_canonical_or_existing_unrelated_file(self):
        source = self.record()
        canonical = source.read_bytes()
        with self.assertRaisesRegex(ValueError, "ignored .workbench"):
            WIKI.save_plan(self.project, source, {"records": []})
        self.assertEqual(source.read_bytes(), canonical)
        report = self.project / ".workbench/wiki/plan.json"
        WIKI.save_plan(self.project, report, {"records": []})
        prior = report.read_bytes()
        with self.assertRaises(FileExistsError):
            WIKI.save_plan(self.project, report, {"records": ["changed"]})
        self.assertEqual(report.read_bytes(), prior)
        link = self.project / ".workbench/link"
        link.symlink_to(self.candidates, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            WIKI.save_plan(self.project, link / "report.json", {})
        self.assertFalse((self.candidates / "report.json").exists())

    def test_local_yaml_launcher_reuses_existing_workbench_runtime_without_installing(self):
        python = self.project / ".venv/bin/python"
        python.parent.mkdir(parents=True)
        python.touch()
        with patch.object(WIKI.importlib.util, "find_spec", return_value=None), \
                patch.object(WIKI.subprocess, "run") as run:
            self.assertTrue(WIKI.local_yaml_runtime(self.project))
        self.assertEqual(run.call_args.args[0][0], str(python))

    def test_json_writes_preserve_unrelated_fixed_tmp_file(self):
        path = self.project / "report.json"
        fixed_tmp = path.with_suffix(".json.tmp")
        fixed_tmp.write_text("An unrelated recovery marker")
        WIKI.save_json(path, {"fixture": True})
        self.assertEqual(fixed_tmp.read_text(), "An unrelated recovery marker")


if __name__ == "__main__":
    unittest.main()
