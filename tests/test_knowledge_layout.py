"""Check layout compatibility and the consolidated knowledge trust boundaries."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from ai_sdlc_workbench.governance import validate_knowledge
from ai_sdlc_workbench.governance.schemas import HEADINGS
from ai_sdlc_workbench.ingestion import harness
from ai_sdlc_workbench.ingestion.incremental import complete_sources, plan_sources
from ai_sdlc_workbench.ingestion.sources import apply_selections, refresh_sources, render_sources, verify_sources
from ai_sdlc_workbench.knowledge_layout import knowledge_layout
from ai_sdlc_workbench.models import Context, Resource, WorkbenchError
from ai_sdlc_workbench.providers.knowledge import LocalKnowledgeProvider


class _LayoutFixture(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="knowledge-layout-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path


class KnowledgeLayoutTests(_LayoutFixture):
    def test_empty_and_legacy_workspaces_keep_their_existing_roots(self):
        expected = self.root / "knowledge", self.root / "evidence/knowledge"
        self.assertEqual(knowledge_layout(self.root), expected)
        self.assertTrue(validate_knowledge(self.root)["valid"])
        self.write("evidence/knowledge/manifest.yaml", "schema_version: 1\nsources: []\n")
        self.assertEqual(knowledge_layout(self.root), expected)
        self.assertTrue(validate_knowledge(self.root)["valid"])

    def test_incomplete_or_dual_layouts_fail_instead_of_merging_authority(self):
        manifest = self.write("knowledge/evidence/manifest.yaml", "schema_version: 1\nsources: []\n")
        with self.assertRaisesRegex(WorkbenchError, "requires knowledge/records"):
            knowledge_layout(self.root)
        (self.root / "knowledge/records").mkdir()
        self.assertEqual(knowledge_layout(self.root),
                         (self.root / "knowledge/records", self.root / "knowledge/evidence"))
        self.write("evidence/knowledge/manifest.yaml", manifest.read_text())
        self.assertEqual(validate_knowledge(self.root)["findings"][0]["code"], "knowledge_layout_invalid")
        with self.assertRaisesRegex(WorkbenchError, "Both knowledge manifests"):
            knowledge_layout(self.root)
        (self.root / "evidence/knowledge/manifest.yaml").unlink()
        manifest.unlink()
        with self.assertRaisesRegex(WorkbenchError, "incomplete"):
            knowledge_layout(self.root)


class ConsolidatedKnowledgeTests(_LayoutFixture):
    def setUp(self):
        super().setUp()
        (self.root / "knowledge/records/candidates").mkdir(parents=True)
        self.write("knowledge/evidence/manifest.yaml", "schema_version: 1\nsources: []\n")
        self.write("workspace.yaml", yaml.safe_dump({"schema_version": 1, "id": "layout-fixture",
            "name": "Layout fixture", "resources": [], "registries": {"sources": "registry/sources.yaml"}}))
        self.write("registry/sources.yaml", yaml.safe_dump({"schema_version": 1, "sources": [
            {"id": "docs", "type": "filesystem", "purpose": "context",
             "location": "knowledge/evidence/sources/docs"}]}))
        self.write(".agents/skills/ingest-knowledge/assets/source-filter.yaml", "schema_version: 1\nversion: 1\n")
        self.write("knowledge/evidence/incoming/docs/page.md", "The system must deny invalid requests.\n")

    def prepare_source(self):
        refreshed = refresh_sources(self.root, "docs", "knowledge/evidence/incoming/docs")
        self.assertEqual(refreshed["selection"], "knowledge/evidence/selections/docs.json")
        index = json.loads((self.root / refreshed["selection"]).read_text())
        source = index["sources"][0]["source"]
        self.assertTrue(source["snapshot"].startswith("knowledge/evidence/sources/sha256/"))
        decision = {"path": "page.md", "sha256": source["sha256"], "decision": "KEEP",
                    "reason": "Inspected exact behavior source.", "topic": "Request validation",
                    "intent_status": "proposed intent", "context": []}
        self.write(".workbench/decisions.json", json.dumps({"schema_version": 1, "source_id": "docs",
                                                           "decisions": [decision]}))
        apply_selections(self.root, "docs", ".workbench/decisions.json")
        self.assertEqual(verify_sources(self.root, "docs")["status"], "READY")
        return source

    def record(self, source):
        metadata = {"type": "KnowledgeTopic", "id": "KT-policy", "version": 1,
                    "owner": "unknown", "governance_state": "candidate", "status": "draft",
                    "sources": [{key: source[key] for key in ("resource", "revision", "sha256")}],
                    "generated": {"by": "agent:fixture", "at": "2026-11-13T00:00:00Z"}, "verified": [],
                    "classification": "fixture", "scope": "Request validation.", "summary": "Deny invalid requests.",
                    "related": [], "open_questions": []}
        content = "---\n" + yaml.safe_dump(metadata) + "---\n# Request validation\n\n"
        content += "\n\n".join("## " + heading + "\n\nDeny invalid requests."
                                for heading in HEADINGS["KnowledgeTopic"])
        return self.write("knowledge/records/candidates/policy.md", content)

    def test_source_selection_processing_and_checkpoint_use_consolidated_roots(self):
        source = self.prepare_source()
        record = self.record(source)
        self.assertEqual(validate_knowledge(self.root), {"valid": True, "documents": 1, "findings": []})
        baseline = harness._capture(self.root)
        self.assertEqual(set(baseline["governed_documents"]), {"knowledge/records/candidates/policy.md"})
        self.assertIn(source["snapshot"], baseline["raw_files"])
        self.assertIn("knowledge/evidence/manifest.yaml", baseline["raw_files"])
        baseline.update(schema_version=1, operation="start", status="PASSED", automated_check="PASSED",
                        workspace=str(self.root))
        baseline_path = self.write(".workbench/baseline.json", json.dumps(baseline))
        plan = plan_sources(self.root, "docs")
        self.write(".workbench/source-plan.json", json.dumps(plan))
        result = {"path": "page.md", "disposition": "no_change",
                  "outputs": [record.relative_to(self.root).as_posix()],
                  "review": {"actor": "agent:fixture", "reviewed_at": "2026-11-13T00:00:00Z",
                             "note": "Inspected source and unchanged canonical output."}}
        self.write(".workbench/completion.json", json.dumps({"schema_version": 1, "source_id": "docs",
            "plan_id": plan["plan_id"], "results": [result]}))
        completed = complete_sources(self.root, "docs", ".workbench/source-plan.json", ".workbench/completion.json")
        self.assertEqual(completed["receipts"], "knowledge/evidence/processing/docs.json")
        self.assertEqual(plan_sources(self.root, "docs")["process_queue"], [])
        view = render_sources(self.root, "docs", ".workbench/view")
        self.assertEqual(view["counts"]["selected"], 1)
        self.assertEqual((self.root / ".workbench/view/page.md").read_bytes(), (self.root / source["snapshot"]).read_bytes())
        check_plan = self.write(".workbench/check-plan.yaml", yaml.safe_dump({"schema_version": 1,
            "documents": [record.relative_to(self.root).as_posix()], "repositories": {}, "executions": []}))
        checked = harness.check(self.root, baseline_path, check_plan)
        self.assertEqual(checked["status"], "PASSED", checked)

    def test_evidence_and_wiki_never_enter_canonical_consumers(self):
        source = self.prepare_source()
        record = self.record(source)
        self.write("knowledge/evidence/sources/canonical-shaped.md", record.read_text())
        self.write("knowledge/llm-wiki/wiki/summaries/canonical-shaped.md", record.read_text())
        self.assertEqual(validate_knowledge(self.root)["documents"], 1)
        self.assertEqual(set(harness._governed(self.root)), {record.relative_to(self.root).as_posix()})
        provider = LocalKnowledgeProvider()
        context = Context(self.root, self.root / "run")
        resource = Resource("knowledge", "knowledge", "knowledge.local", "test", {"path": "knowledge"},
                            ["list", "read", "ingest"])
        self.assertEqual([row["relative_path"] for row in provider.invoke("list", resource, {}, context)["files"]],
                         ["candidates/policy.md"])
        for base in ("knowledge/evidence", "knowledge/llm-wiki"):
            chosen = deepcopy(resource)
            chosen.config["path"] = base
            self.assertEqual(provider.invoke("list", chosen, {}, context)["code"], "INVALID_DOCUMENT")
        for destination in ("../evidence/sources/canonical-shaped.md", "../llm-wiki/wiki/summaries/canonical-shaped.md"):
            self.assertEqual(provider.invoke("read", resource, {"path": destination}, context)["code"], "INVALID_DOCUMENT")
        plan = plan_sources(self.root, "docs")
        self.assertEqual(plan["process_queue"][0]["affected_knowledge"], [record.relative_to(self.root).as_posix()])

    def test_snapshots_in_records_are_rejected_by_validation_sources_and_checkpoint(self):
        source = self.prepare_source()
        forbidden = self.write("knowledge/records/raw-source.md", (self.root / source["snapshot"]).read_text())
        manifest = self.root / "knowledge/evidence/manifest.yaml"
        payload = yaml.safe_load(manifest.read_text())
        payload["sources"][0]["snapshot"] = forbidden.relative_to(self.root).as_posix()
        manifest.write_text(yaml.safe_dump(payload))
        self.assertIn("source_snapshot_invalid", {row["code"] for row in validate_knowledge(self.root)["findings"]})
        self.assertEqual(verify_sources(self.root, "docs")["status"], "FAILED")
        with self.assertRaisesRegex(ValueError, "outside the domain knowledge"):
            harness._capture(self.root)

    def test_refresh_cannot_capture_records_wiki_or_unrelated_evidence_as_imports(self):
        manifest = self.root / "knowledge/evidence/manifest.yaml"
        before = manifest.read_bytes()
        for directory in ("knowledge", "knowledge/records", "knowledge/llm-wiki",
                          "knowledge/evidence/audit", "knowledge/evidence/incoming-other/docs"):
            with self.subTest(directory=directory):
                (self.root / directory).mkdir(parents=True, exist_ok=True)
                with self.assertRaisesRegex(WorkbenchError, "Use a writable import folder"):
                    refresh_sources(self.root, "docs", directory)
                self.assertEqual(manifest.read_bytes(), before)
                self.assertFalse((self.root / "knowledge/evidence/selections/docs.json").exists())


if __name__ == "__main__":
    unittest.main()
