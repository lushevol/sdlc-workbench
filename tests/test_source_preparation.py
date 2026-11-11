"""Check source revision preservation and review-bound filtered views."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from ai_sdlc_workbench.ingestion.sources import (
    apply_selections, refresh_sources, render_sources, verify_sources,
)
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.workspace import initialize_workspace


class SourcePreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="source-preparation-")
        self.addCleanup(temporary.cleanup)
        self.root = (Path(temporary.name) / "workspace").resolve()
        initialize_workspace(self.root)
        self.raw = self.root / "evidence/knowledge/incoming/docs"
        self.raw.mkdir(parents=True)
        (self.root / "registry/sources.yaml").write_text(yaml.safe_dump({"schema_version": 1, "sources": [
            {"id": "docs", "type": "filesystem", "purpose": "context",
             "location": "evidence/knowledge/sources/docs"}]}))
        self.manifest = self.root / "evidence/knowledge/manifest.yaml"
        self.index_path = self.root / "evidence/knowledge/selections/docs.json"
        self.policy = self.root / ".agents/skills/ingest-knowledge/assets/source-filter.yaml"
        self.policy.parent.mkdir(parents=True, exist_ok=True)
        self.policy.write_text("schema_version: 1\nversion: 1\n")

    def page(self, name="page.md", content="# Rule\n\nThe system must deny invalid requests.\n"):
        path = self.raw / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def refresh(self):
        return refresh_sources(self.root, "docs", self.raw.relative_to(self.root).as_posix())

    def index(self):
        return json.loads(self.index_path.read_text())

    def decide(self, decision="KEEP", *, path="page.md", ranges=None, context=None):
        row = next(r for r in self.index()["sources"] if r["path"] == path)
        item = {"path": path, "sha256": row["source"]["sha256"], "decision": decision,
                "reason": "Reviewed for the initial behavior source batch.", "topic": "Request validation",
                "intent_status": "proposed intent", "context": context or []}
        if ranges is not None:
            item["ranges"] = ranges
        return item

    def apply(self, decisions):
        path = self.root / ".workbench/decisions.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"schema_version": 1, "source_id": "docs", "decisions": decisions}))
        return apply_selections(self.root, "docs", ".workbench/decisions.json")

    def test_equal_new_payloads_share_storage_but_keep_distinct_provenance(self):
        self.page("a.md")
        self.page("b.md")
        result = self.refresh()
        rows = self.index()["sources"]
        self.assertEqual(result["new_source_revisions"], 2)
        self.assertEqual(result["new_snapshot_payloads"], 1)
        self.assertEqual(rows[0]["source"]["snapshot"], rows[1]["source"]["snapshot"])
        self.assertNotEqual(rows[0]["source"]["id"], rows[1]["source"]["id"])
        before = self.manifest.read_bytes()
        self.assertEqual(self.refresh()["new_snapshot_payloads"], 0)
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_new_inbox_preserves_legacy_source_binding_and_changed_page_history(self):
        """Given retained sources, when imports switch inboxes, then identity and old bytes remain intact."""
        retained = self.root / "evidence/knowledge/sources/docs/page.md"
        retained.parent.mkdir(parents=True)
        original = b"# Rule\nThe system must deny invalid requests.\n"
        retained.write_bytes(original)
        record = {"id": "SRC-legacy-page", "resource": "local:prior-export/page.md",
                  "revision": "export-2026-11-11", "sha256": hashlib.sha256(original).hexdigest(),
                  "snapshot": retained.relative_to(self.root).as_posix(),
                  "ingested_at": "2026-11-11T00:00:00Z", "classification": "business", "source_id": "docs"}
        self.manifest.write_text(yaml.safe_dump({"schema_version": 1, "sources": [record]}, sort_keys=False))
        manifest_bytes = self.manifest.read_bytes()
        refresh_sources(self.root, "docs", "evidence/knowledge/sources/docs")
        self.apply([self.decide()])
        binding = self.index()["sources"][0]["source"]

        page = self.page(content=original.decode())
        result = self.refresh()
        row = self.index()["sources"][0]
        self.assertEqual(row["source"], binding)
        self.assertEqual(row["decision"], "KEEP")
        self.assertEqual(result["new_source_revisions"], 0)
        self.assertEqual(result["new_snapshot_payloads"], 0)
        self.assertEqual(self.manifest.read_bytes(), manifest_bytes)
        self.assertEqual(self.index()["input_root"], "evidence/knowledge/incoming/docs")

        page.write_text("The revised system must require a second approval.\n")
        result = self.refresh()
        updated = self.index()["sources"][0]
        self.assertEqual(updated["source"]["id"], binding["id"])
        self.assertEqual(updated["source"]["resource"], binding["resource"])
        self.assertNotEqual(updated["source"]["revision"], binding["revision"])
        self.assertNotEqual(updated["source"]["sha256"], binding["sha256"])
        self.assertEqual(updated["decision"], "NEEDS_REVIEW")
        self.assertEqual(retained.read_bytes(), original)
        self.assertEqual(yaml.safe_load(self.manifest.read_text())["sources"][0], record)
        self.assertEqual(result["new_source_revisions"], 1)
        self.assertEqual(result["new_snapshot_payloads"], 1)

    def test_generic_workspace_input_remains_supported(self):
        """Given a workspace import folder, when refreshed, then the explicit input remains supported."""
        self.raw = self.root / "imports/docs"
        self.page()
        result = self.refresh()
        self.assertEqual(result["counts"]["documents"], 1)
        self.assertEqual(self.index()["input_root"], "imports/docs")
        self.assertTrue((self.root / self.index()["sources"][0]["source"]["snapshot"]).is_file())

    def test_other_evidence_folders_remain_protected(self):
        """Given unrelated evidence, when selected as input, then refresh rejects it without manifest changes."""
        manifest_bytes = self.manifest.read_bytes()
        for relative in ("evidence/knowledge/audit/unrelated", "evidence/knowledge/sources/unregistered",
                         "evidence/knowledge/incoming-other/docs"):
            with self.subTest(input=relative):
                directory = self.root / relative
                directory.mkdir(parents=True)
                (directory / "page.md").write_text("Unrelated evidence.\n")
                with self.assertRaises(WorkbenchError):
                    refresh_sources(self.root, "docs", relative)
                self.assertEqual(self.manifest.read_bytes(), manifest_bytes)
                self.assertFalse(self.index_path.exists())

    def test_changed_exclusion_gets_new_revision_and_requires_review(self):
        path = self.page()
        self.refresh()
        self.apply([self.decide("EXCLUDE")])
        old = self.index()["sources"][0]["source"]
        snapshot = self.root / old["snapshot"]
        retained = snapshot.read_bytes()
        path.write_text("New business requirement.\n")
        result = self.refresh()
        new = self.index()["sources"][0]
        self.assertEqual(new["decision"], "NEEDS_REVIEW")
        self.assertNotEqual(new["source"]["sha256"], old["sha256"])
        self.assertEqual(new["source"]["id"], old["id"])
        self.assertEqual(new["source"]["resource"], old["resource"])
        self.assertEqual(snapshot.read_bytes(), retained)
        self.assertEqual(len(yaml.safe_load(self.manifest.read_text())["sources"]), 2)
        self.assertEqual(result["changed_sources"][0]["previous"], old)

    def test_missing_export_page_keeps_evidence_and_flags_affected_knowledge(self):
        page = self.page()
        self.refresh()
        self.apply([self.decide()])
        original = self.index()["sources"][0]["source"]
        topic = self.root / "knowledge/candidates/topic.md"
        topic.write_text("---\n" + yaml.safe_dump({"sources": [{k: original[k] for k in (
            "resource", "revision", "sha256")} ]}) + "---\nIntended validation.\n")
        alias = self.root / "knowledge/llm-wiki/raw/alias.md"
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.symlink_to(topic)
        canonical_bytes = topic.read_bytes()
        wiki_link = alias.readlink()
        page.unlink()
        before = self.manifest.read_bytes()
        result = self.refresh()
        self.assertEqual(result["status"], "NEEDS_REVIEW")
        self.assertEqual(result["affected_knowledge"][0]["path"], "knowledge/candidates/topic.md")
        self.assertEqual(len(result["affected_knowledge"]), 1)
        self.assertFalse(self.index()["sources"][0]["present"])
        self.assertTrue((self.root / original["snapshot"]).is_file())
        self.assertEqual(self.manifest.read_bytes(), before)
        self.assertEqual(topic.read_bytes(), canonical_bytes)
        self.assertEqual(alias.readlink(), wiki_link)
        self.assertEqual(alias.read_bytes(), canonical_bytes)

    def test_views_bind_links_and_excerpts_to_original_and_output_hashes(self):
        self.page("whole.md", "First\r\nSecond\r\nThird\r\n")
        self.page("partial.md", "A\nB\nC\nD\n")
        self.page("held.md", "Missing policy context.\n")
        self.refresh()
        self.apply([self.decide(path="whole.md"), self.decide("KEEP_SECTIONS", path="partial.md", ranges=[[2, 2], [4, 4]]),
                    self.decide("HOLD", path="held.md")])
        result = render_sources(self.root, "docs", ".workbench/view")
        view = json.loads((self.root / result["manifest"]).read_text())
        self.assertEqual(result["counts"]["selected"], 2)
        self.assertEqual(result["counts"]["omitted"], 1)
        entries = {entry["path"]: entry for entry in view["sources"]}
        partial = self.root / result["output"] / entries["partial.md"]["output"]
        self.assertEqual(partial.read_bytes(), b"B\nD\n")
        self.assertEqual(entries["partial.md"]["mapping"], [
            {"source_start": 2, "source_end": 2, "output_start": 1, "output_end": 1},
            {"source_start": 4, "source_end": 4, "output_start": 2, "output_end": 2}])
        for entry in entries.values():
            original = (self.root / entry["source"]["snapshot"]).read_bytes()
            output = (self.root / result["output"] / entry["output"]).read_bytes()
            self.assertEqual(entry["source_sha256"], hashlib.sha256(original).hexdigest())
            self.assertEqual(entry["output_sha256"], hashlib.sha256(output).hexdigest())
        whole = self.root / result["output"] / "whole.md"
        self.assertTrue(whole.is_symlink())
        self.assertEqual(whole.resolve(), (self.root / entries["whole.md"]["source"]["snapshot"]).resolve())

    def test_failed_decision_batch_does_not_commit_an_earlier_valid_decision(self):
        self.page("a.md")
        self.page("b.md")
        self.refresh()
        before = self.index_path.read_bytes()
        first = self.decide(path="a.md")
        second = self.decide("KEEP_SECTIONS", path="b.md", ranges=[[1, 999]])
        with self.assertRaises(WorkbenchError):
            self.apply([first, second])
        self.assertEqual(self.index_path.read_bytes(), before)

    def test_policy_and_context_changes_invalidate_reviewed_exclusions(self):
        self.page()
        context = self.root / "policy.md"
        context.write_text("Initial intent.\n")
        self.refresh()
        self.apply([self.decide("EXCLUDE", context=[{"path": "policy.md", "sha256": hashlib.sha256(context.read_bytes()).hexdigest()}])])
        self.assertEqual(verify_sources(self.root, "docs")["status"], "READY")
        context.write_text("Updated intent.\n")
        self.assertEqual(verify_sources(self.root, "docs")["status"], "NEEDS_REVIEW")
        self.refresh()
        self.assertEqual(self.index()["sources"][0]["decision"], "NEEDS_REVIEW")
        self.apply([self.decide("EXCLUDE")])
        self.policy.write_text("schema_version: 1\nversion: 2\n")
        with self.assertRaises(WorkbenchError):
            render_sources(self.root, "docs", ".workbench/stale")
        self.refresh()
        self.assertEqual(self.index()["sources"][0]["decision"], "NEEDS_REVIEW")

    def test_snapshot_tampering_is_not_reclassified_as_a_new_revision(self):
        self.page()
        self.refresh()
        source = self.index()["sources"][0]["source"]
        (self.root / source["snapshot"]).write_text("Altered evidence.\n")
        before = self.manifest.read_bytes()
        self.assertEqual(verify_sources(self.root, "docs")["status"], "FAILED")
        with self.assertRaises(WorkbenchError):
            self.refresh()
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_missing_and_empty_inputs_never_claim_ready(self):
        result = self.refresh()
        self.assertEqual(result["status"], "NEEDS_REVIEW")
        self.assertEqual(result["findings"][0]["code"], "empty_export")
        self.assertEqual(verify_sources(self.root, "docs")["status"], "NEEDS_REVIEW")

    def test_newly_missing_input_requires_refresh_before_selecting_or_rendering(self):
        page = self.page()
        self.refresh()
        decision = self.decide()
        self.apply([decision])
        page.unlink()
        with self.assertRaises(WorkbenchError):
            self.apply([decision])
        with self.assertRaises(WorkbenchError):
            render_sources(self.root, "docs", ".workbench/missing-view")
        self.assertFalse((self.root / ".workbench/missing-view").exists())
        self.refresh()
        result = render_sources(self.root, "docs", ".workbench/refreshed-missing-view")
        self.assertEqual(result["counts"]["selected"], 0)
        self.assertEqual(result["counts"]["omitted"], 1)

    def test_reappearing_input_requires_refresh_and_changed_content_review(self):
        page = self.page()
        self.refresh()
        self.apply([self.decide()])
        page.unlink()
        self.refresh()
        self.page(content="The revised system must request a second approval.\n")
        self.assertIn("input_presence_changed", {
            finding["code"] for finding in verify_sources(self.root, "docs")["findings"]})
        with self.assertRaises(WorkbenchError):
            render_sources(self.root, "docs", ".workbench/reappeared-view")
        self.refresh()
        self.assertEqual(self.index()["sources"][0]["decision"], "NEEDS_REVIEW")

    def test_bad_utf8_and_symlinks_fail_before_creating_a_selection(self):
        page = self.page()
        page.write_bytes(b"\xff")
        before = self.manifest.read_bytes()
        with self.assertRaises(WorkbenchError):
            self.refresh()
        self.assertEqual(self.manifest.read_bytes(), before)
        self.assertFalse(self.index_path.exists())
        page.unlink()
        outside = self.root / "outside.md"
        outside.write_text("Unrelated content.\n")
        page.symlink_to(outside)
        with self.assertRaises(WorkbenchError):
            self.refresh()
        self.assertFalse(self.index_path.exists())

    def test_malformed_unhashable_values_are_rejected_without_type_errors(self):
        self.page()
        self.refresh()
        good = self.index()
        cases = []
        for field in ("path", "decision"):
            bad = deepcopy(good)
            bad["sources"][0][field] = []
            cases.append(bad)
        bad = deepcopy(good)
        bad["sources"][0]["source"]["sha256"] = {}
        cases.append(bad)
        bad = deepcopy(good)
        bad["sources"][0]["context"] = [{"path": [], "sha256": "a" * 64}]
        cases.append(bad)
        for bad in cases:
            self.index_path.write_text(json.dumps(bad))
            self.assertEqual(verify_sources(self.root, "docs")["status"], "FAILED")
        self.index_path.write_text(json.dumps(good))
        decision = self.decide()
        for field in ("path", "decision"):
            bad = deepcopy(decision)
            bad[field] = []
            with self.assertRaises(WorkbenchError):
                self.apply([bad])

    def test_target_change_during_link_creation_never_publishes_valid_view(self):
        self.page()
        self.refresh()
        self.apply([self.decide()])
        source = self.index()["sources"][0]["source"]
        original_symlink = Path.symlink_to
        target = self.root / source["snapshot"]

        def changing_link(path, target_value, *args, **kwargs):
            result = original_symlink(path, target_value, *args, **kwargs)
            target.write_text("Changed while linking.\n")
            return result

        with patch.object(Path, "symlink_to", changing_link):
            with self.assertRaises(WorkbenchError):
                render_sources(self.root, "docs", ".workbench/racing-view")
        self.assertFalse((self.root / ".workbench/racing-view/manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
