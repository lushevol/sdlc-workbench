"""Regressions for read-only metadata and publication gate checks."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from ai_sdlc_workbench.governance import validate_knowledge
from ai_sdlc_workbench.governance.schemas import HEADINGS, SCHEMA_FILES
from ai_sdlc_workbench.models import validate_schema


class KnowledgeGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="knowledge-governance-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        for folder in ("knowledge/candidates", "evidence/knowledge/sources", "evidence/knowledge/audit"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        self.raw = self.root / "evidence/knowledge/sources/source.txt"
        self.raw.write_bytes(b"Illustrative fixture source.\n")
        self.source = {"resource": "fixture://source", "revision": "v1",
                       "sha256": hashlib.sha256(self.raw.read_bytes()).hexdigest()}
        self.record = {"id": "source-1", **self.source, "ingested_at": "2026-10-14T00:00:00Z",
                       "classification": "business", "snapshot": "evidence/knowledge/sources/source.txt"}
        self.manifest = {"schema_version": 1, "sources": [self.record]}
        self.write_manifest()
        self.metadata = {
            "type": "Requirement", "id": "req-1", "version": 1, "owner": "fixture-owner",
            "governance_state": "candidate", "status": "draft", "sources": [self.source],
            "generated": {"by": "fixture-generator", "at": "2026-10-14T00:00:00Z"}, "verified": [],
            "description": "Return one fixture item.", "rationale": "Keep the fixture bounded.",
            "acceptance_criteria": [{"id": "AC-1", "given": "Given one valid request",
                "when": "When the fixture handles the request", "then": "Then return one item",
                "measure": {"metric": "item count", "operator": "equals", "value": 1, "unit": "count"}}],
        }
        self.document = self.root / "knowledge/candidates/requirement.md"

    def write_manifest(self):
        (self.root / "evidence/knowledge/manifest.yaml").write_text(yaml.safe_dump(self.manifest))

    def write_document(self, metadata=None, body=None):
        metadata = self.metadata if metadata is None else metadata
        if body is None:
            body = "# Fixture\n\n" + "\n\n".join("## " + heading + "\n\nFixture content."
                    for heading in HEADINGS[metadata["type"]]) + "\n"
        self.document.write_text("---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n" + body)

    def event(self, identifier, to_state, *, actor="fixture-reviewer", action="transition",
              at="2026-10-14T01:00:00Z", from_state="candidate", digest=None):
        event = {"id": identifier, "item_id": self.metadata["id"], "item_version": self.metadata["version"],
                 "actor": actor, "at": at, "action": action, "from_state": from_state,
                 "to_state": to_state, "content_sha256": digest or hashlib.sha256(self.document.read_bytes()).hexdigest(),
                 "reason": "Review the fixture metadata.", "evidence": [self.source]}
        path = self.root / "evidence/knowledge/audit" / (identifier + ".yaml")
        path.write_text(yaml.safe_dump(event))
        return event, path

    def publish(self, *, human=True):
        self.metadata["governance_state"] = "published"
        self.metadata["verified"] = [{"by": "human:fixture-owner", "at": "2026-10-14T01:00:00Z"}]
        self.write_document()
        self.event("verified-1", "verified", actor="human:fixture-owner", from_state="investigated")
        if human:
            self.event("approved-1", "verified", actor="human:fixture-owner", action="approval",
                       from_state="verified", at="2026-10-14T02:00:00Z")
        self.event("published-1", "published", from_state="verified", at="2026-10-14T03:00:00Z")

    def codes(self):
        return {finding["code"] for finding in validate_knowledge(self.root)["findings"]}

    def test_candidate_is_valid_without_approval_and_validation_is_read_only(self):
        self.write_document()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with patch.object(Path, "write_text", side_effect=AssertionError("write forbidden")), \
                patch.object(Path, "write_bytes", side_effect=AssertionError("write forbidden")), \
                patch.object(Path, "mkdir", side_effect=AssertionError("mkdir forbidden")):
            result = validate_knowledge(self.root)
        self.assertEqual(result, {"valid": True, "documents": 1, "findings": []})
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_knowledge_topic_requires_classification_source_binding_and_topic_sections(self):
        metadata = {key: value for key, value in self.metadata.items()
                    if key not in {"description", "rationale", "acceptance_criteria"}}
        metadata.update(type="KnowledgeTopic", classification="fixture-context",
                        scope="One supplied fixture statement.",
                        summary="The fixture provides illustrative source text.",
                        related=[], open_questions=["Who owns this fixture?"])
        self.document = self.root / "knowledge/candidates/fixture-context/topic.md"
        self.document.parent.mkdir()
        body = "# Fixture topic\n\n" + "\n\n".join(
            "## " + heading + "\n\nFixture content."
            for heading in HEADINGS["KnowledgeTopic"]) + "\n"
        self.write_document(metadata, body)
        self.assertEqual(validate_knowledge(self.root), {"valid": True, "documents": 1, "findings": []})

        for field in ("classification", "scope", "summary", "related", "open_questions"):
            with self.subTest(missing=field):
                incomplete = deepcopy(metadata)
                del incomplete[field]
                self.write_document(incomplete, body)
                self.assertIn("document_invalid", self.codes())
        blank = {**metadata, "classification": "   "}
        self.write_document(blank, body)
        self.assertIn("document_invalid", self.codes())

        unmatched = deepcopy(metadata)
        unmatched["sources"][0]["revision"] = "unretained-revision"
        self.write_document(unmatched, body)
        self.assertEqual(self.codes(), {"source_invalid"})
        for heading in HEADINGS["KnowledgeTopic"]:
            with self.subTest(missing_heading=heading):
                self.write_document(metadata, body.replace("## " + heading + "\n\nFixture content.", ""))
                self.assertIn("document_invalid", self.codes())

    def test_required_frontmatter_fields_and_domain_fields_are_enforced(self):
        body = "\n\n".join("## " + heading + "\n\nFixture content."
                           for heading in HEADINGS[self.metadata["type"]]) + "\n"
        self.write_document(body=body)
        self.assertTrue(validate_knowledge(self.root)["valid"])
        for field in ("type", "id", "owner", "version", "governance_state", "status", "sources",
                      "generated", "verified", "description", "rationale", "acceptance_criteria"):
            with self.subTest(field=field):
                metadata = deepcopy(self.metadata)
                del metadata[field]
                self.write_document(metadata, body)
                self.assertIn("document_invalid", self.codes())

    def test_gherkin_and_measurable_criteria_structure_are_enforced(self):
        for field, value in (("given", "A user has an account"), ("when", "Whenever needed"),
                             ("then", "Works well"), ("measure", {}),
                             ("measure", {"metric": "quality", "operator": "equals", "value": "good", "unit": "count"})):
            with self.subTest(field=field, value=value):
                metadata = deepcopy(self.metadata)
                metadata["acceptance_criteria"][0][field] = value
                self.write_document(metadata)
                self.assertIn("document_invalid", self.codes())

    def test_missing_empty_and_code_fence_headings_do_not_satisfy_body_contract(self):
        for body in ("## Description\n\nFixture only.\n",
                     "## Description\n## Rationale\n## Acceptance criteria\n",
                     "```markdown\n## Description\nFixture.\n## Rationale\nFixture.\n## Acceptance criteria\nFixture.\n```\n"):
            with self.subTest(body=body):
                self.write_document(body=body)
                self.assertIn("document_invalid", self.codes())

    def test_published_requirement_needs_verification_and_human_approval(self):
        self.metadata["governance_state"] = "published"
        self.write_document()
        self.assertTrue({"audit_state_missing", "verification_missing", "human_approval_missing"} <= self.codes())
        self.publish(human=False)
        self.assertEqual(self.codes(), {"human_approval_missing"})
        self.event("approved-1", "verified", actor="human:fixture-owner", action="approval",
                   from_state="verified", at="2026-10-14T02:00:00Z")
        self.assertTrue(validate_knowledge(self.root)["valid"])

    def test_edit_after_publication_invalidates_hash_bound_gates(self):
        self.publish()
        self.assertTrue(validate_knowledge(self.root)["valid"])
        self.document.write_text(self.document.read_text() + "\nChanged content.\n")
        self.assertTrue({"audit_state_missing", "verification_missing", "human_approval_missing"} <= self.codes())

    def test_human_approval_must_bind_to_that_humans_verification(self):
        self.publish()
        self.metadata["verified"] = [{"by": "process:qa", "at": "2026-10-14T01:00:00Z"}]
        self.write_document()
        self.event("verified-1", "verified", actor="process:qa", from_state="investigated")
        self.event("approved-1", "verified", actor="human:fixture-owner", action="approval",
                   from_state="verified", at="2026-10-14T02:00:00Z")
        self.event("published-1", "published", from_state="verified", at="2026-10-14T03:00:00Z")
        self.assertEqual(self.codes(), {"human_approval_missing"})

    def test_investigated_state_requires_matching_transition_and_current_version(self):
        self.metadata["governance_state"] = "investigated"
        self.write_document()
        self.assertEqual(self.codes(), {"audit_state_missing"})
        _, event_path = self.event("investigated-1", "investigated")
        self.assertTrue(validate_knowledge(self.root)["valid"])
        event = yaml.safe_load(event_path.read_text())
        event["item_version"] = 2
        event_path.write_text(yaml.safe_dump(event))
        self.assertEqual(self.codes(), {"audit_state_missing"})

    def test_stale_verification_and_approval_before_verification_are_rejected(self):
        self.publish()
        self.metadata["verified"][0]["at"] = "2026-10-13T00:00:00Z"
        self.write_document()
        self.assertIn("document_invalid", self.codes())
        self.metadata["verified"][0]["at"] = "2026-10-14T01:00:00Z"
        self.publish()
        self.event("approved-1", "verified", actor="human:fixture-owner", action="approval",
                   from_state="verified", at="2026-10-14T00:30:00Z")
        self.assertIn("human_approval_missing", self.codes())

    def test_verification_timestamps_compare_the_same_instant(self):
        self.publish()
        path = self.root / "evidence/knowledge/audit/verified-1.yaml"
        event = yaml.safe_load(path.read_text())
        event["at"] = "2026-10-14T09:00:00+08:00"
        path.write_text(yaml.safe_dump(event))
        self.assertTrue(validate_knowledge(self.root)["valid"])

    def test_malformed_manifest_duplicate_keys_dates_hashes_and_classification(self):
        path = self.root / "evidence/knowledge/manifest.yaml"
        self.write_document()
        for content in ("schema_version: 1\nsources: []\nsources: []\n", "schema_version: 1\n",
                        "schema_version: 1\nsources: [unterminated"):
            with self.subTest(content=content):
                path.write_text(content)
                self.assertIn("manifest_invalid", self.codes())
        for field, value in (("sha256", "x" * 64), ("ingested_at", "2026-10-14"),
                             ("classification", "invented-class")):
            with self.subTest(field=field):
                self.manifest["sources"] = [{**self.record, field: value}]
                self.write_manifest()
                self.assertIn("manifest_invalid", self.codes())

    def test_raw_snapshot_hash_mismatch_and_new_revisions(self):
        self.write_document()
        self.raw.write_bytes(b"changed original bytes\n")
        self.assertIn("source_hash_mismatch", self.codes())
        second = {**self.record, "revision": "v2", "sha256": hashlib.sha256(self.raw.read_bytes()).hexdigest()}
        self.manifest["sources"] = [{key: value for key, value in self.record.items() if key != "snapshot"}, second]
        self.write_manifest()
        self.assertTrue(validate_knowledge(self.root)["valid"])
        self.manifest["sources"].append(deepcopy(second))
        self.write_manifest()
        self.assertIn("manifest_invalid", self.codes())

    def test_unsafe_snapshot_and_document_symlink_paths_are_rejected(self):
        outside = self.root.parent / "external.txt"
        outside.write_text("Private external fixture.\n")
        self.write_document()
        for value in ("../external.txt", str(outside), "knowledge/../raw/source.txt"):
            with self.subTest(value=value):
                self.manifest["sources"] = [{**self.record, "snapshot": value}]
                self.write_manifest()
                self.assertIn("source_snapshot_invalid", self.codes())
        self.manifest["sources"] = [self.record]
        self.write_manifest()
        link = self.root / "knowledge/candidates/unsafe.md"
        link.symlink_to(outside)
        self.assertIn("unsafe_path", self.codes())
        self.assertEqual(outside.read_text(), "Private external fixture.\n")

    def test_external_resource_is_only_a_reference_without_snapshot(self):
        self.source["resource"] = str(self.root.parent / "not-readable-or-fetched.txt")
        self.manifest["sources"] = [{**self.record, **self.source}]
        del self.manifest["sources"][0]["snapshot"]
        self.write_manifest()
        self.write_document()
        self.assertTrue(validate_knowledge(self.root)["valid"])

    def test_malformed_audit_and_automatic_approval_are_rejected(self):
        self.publish()
        _, path = self.event("bad-event", "verified", from_state="investigated")
        base = yaml.safe_load(path.read_text())
        for field, value in (("content_sha256", "x" * 64), ("at", "yesterday"),
                             ("to_state", "candidate")):
            with self.subTest(field=field):
                path.write_text(yaml.safe_dump({**base, field: value}))
                self.assertIn("audit_invalid", self.codes())
        path.write_text("id: bad-event\nid: hidden-override\n")
        self.assertIn("audit_invalid", self.codes())
        path.unlink()
        self.event("approved-1", "verified", actor="ai:reviewer", action="approval",
                   from_state="verified", at="2026-10-14T02:00:00Z")
        self.assertTrue({"audit_invalid", "human_approval_missing"} <= self.codes())

    def test_json_incompatible_yaml_and_duplicate_document_keys_are_findings(self):
        self.write_document()
        content = self.document.read_text()
        for changed in (content.replace("'2026-10-14T00:00:00Z'", "2026-10-14T00:00:00Z"),
                        content.replace("type: Requirement", "type: Requirement\ntype: Decision")):
            with self.subTest(content=changed[:80]):
                self.document.write_text(changed)
                self.assertIn("document_invalid", self.codes())

    def test_extensions_are_preserved_and_navigation_is_excluded(self):
        self.metadata["x-extension"] = {"blank": "", "other": None, "nested": [1, True]}
        self.metadata["sources"][0]["locator"] = ""
        self.write_document()
        for relative in ("index.md", "README.md", "candidates/index.md"):
            path = self.root / "knowledge" / relative
            path.parent.mkdir(exist_ok=True)
            path.write_text("Not a governed document.\n")
        self.assertEqual(validate_knowledge(self.root), {"valid": True, "documents": 1, "findings": []})

    def test_legacy_empty_workspace_and_empty_knowledge_remain_valid(self):
        legacy = self.root.parent / "legacy"
        legacy.mkdir()
        self.assertEqual(validate_knowledge(legacy), {"valid": True, "documents": 0, "findings": []})
        (legacy / "knowledge/requirements").mkdir(parents=True)
        (legacy / "knowledge/requirements/README.md").write_text("Legacy guidance.\n")
        self.assertTrue(validate_knowledge(legacy)["valid"])

    def test_knowledge_root_cannot_hide_unstructured_content_as_a_file(self):
        other = self.root.parent / "other-workspace"
        other.mkdir()
        (other / "knowledge").write_text("Execution output without domain metadata.\n")
        result = validate_knowledge(other)
        self.assertFalse(result["valid"])
        self.assertEqual(result["findings"][0]["code"], "knowledge_asset_invalid")

    def test_reference_schemas_and_all_illustrative_templates_match_runtime(self):
        source_root = Path(__file__).resolve().parents[1] / "core/knowledge"
        for filename, schema in SCHEMA_FILES.items():
            with self.subTest(schema=filename):
                validate_schema(schema)
                self.assertEqual(json.loads((source_root / "schemas" / filename).read_text()), schema)
        self.manifest = yaml.safe_load((source_root / "templates/examples/manifest.yaml").read_text())
        self.manifest["sources"][0]["snapshot"] = "evidence/knowledge/sources/source.txt"
        self.raw.write_bytes((source_root / "templates/examples/source.txt").read_bytes())
        self.write_manifest()
        for path in sorted((source_root / "templates").glob("*.md")):
            if path.name == "README.md":
                continue
            with self.subTest(template=path.name):
                self.document = self.root / ("evidence/knowledge/findings/template.md" if path.name == "governance-finding.md"
                                             else "knowledge/candidates/requirement.md")
                self.document.parent.mkdir(parents=True, exist_ok=True)
                self.document.write_bytes(path.read_bytes())
                self.assertTrue(validate_knowledge(self.root)["valid"], validate_knowledge(self.root))
                self.document.unlink()

    def test_non_domain_assets_and_legacy_storage_are_rejected(self):
        self.write_document()
        for relative in ("raw/source.md", "audit/event.yaml", "templates/example.md", "schemas/record.json",
                         "findings/result.md", "logs/run.md", "execution/result.md", "nested/run.txt", "log.md"):
            with self.subTest(path=relative):
                path = self.root / "knowledge" / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Non-domain artifact.\n")
                self.assertIn("knowledge_asset_invalid", self.codes())
                path.unlink()

    def test_registered_snapshots_cannot_live_in_domain_knowledge(self):
        self.write_document()
        snapshot = self.root / "knowledge/source.md"
        snapshot.write_bytes(self.raw.read_bytes())
        self.manifest["sources"][0]["snapshot"] = "knowledge/source.md"
        self.write_manifest()
        self.assertIn("source_snapshot_invalid", self.codes())

    def test_findings_are_validated_outside_domain_knowledge(self):
        metadata = {key: value for key, value in self.metadata.items()
                    if key not in {"description", "rationale", "acceptance_criteria"}}
        metadata.update(type="GovernanceFinding", subject={"id": "req-1", "version": 1},
                        category="missing-intent", severity="warning", evidence=[self.source],
                        proposed_action="Ask the business owner.", resolution="open")
        self.document = self.root / "evidence/knowledge/findings/finding.md"
        self.document.parent.mkdir()
        self.write_document(metadata)
        self.assertTrue(validate_knowledge(self.root)["valid"])
        self.document.write_text(self.document.read_text().replace("severity: warning", "severity: invalid"))
        self.assertIn("document_invalid", self.codes())
        self.document.unlink()
        self.document = self.root / "knowledge/candidates/finding.md"
        self.write_document(metadata)
        self.assertIn("document_invalid", self.codes())


if __name__ == "__main__":
    unittest.main()
