"""Check file-level planning and successful canonical processing boundaries."""

from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from ai_sdlc_workbench.governance.schemas import HEADINGS
from ai_sdlc_workbench.ingestion import harness
from ai_sdlc_workbench.ingestion.incremental import complete_sources, load_plan, plan_sources
from ai_sdlc_workbench.ingestion.sources import apply_selections, refresh_sources
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.validation import validate_workspace
from tests.knowledge_fixtures import initialize_legacy_workspace as initialize_workspace


class IncrementalIngestionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="incremental-ingestion-")
        self.addCleanup(temporary.cleanup)
        self.root = (Path(temporary.name) / "workspace").resolve()
        initialize_workspace(self.root)
        self.raw = self.root / "evidence/knowledge/incoming/docs"
        self.raw.mkdir(parents=True)
        (self.root / "registry/sources.yaml").write_text(yaml.safe_dump({"schema_version": 1, "sources": [
            {"id": "docs", "type": "filesystem", "purpose": "context",
             "location": "evidence/knowledge/sources/docs"}]}))
        self.policy = self.root / ".agents/skills/ingest-knowledge/assets/source-filter.yaml"
        self.policy.parent.mkdir(parents=True, exist_ok=True)
        self.policy.write_text("schema_version: 1\nversion: 1\n")
        self.counter = 0

    def save(self, value, stem="input"):
        self.counter += 1
        name = f".workbench/{stem}-{self.counter}.json"
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return name

    def page(self, name="page.md", body="The system must deny invalid requests.\n"):
        path = self.raw / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return path

    def refresh(self):
        return refresh_sources(self.root, "docs", "evidence/knowledge/incoming/docs")

    def rows(self):
        return json.loads((self.root / "evidence/knowledge/selections/docs.json").read_text())["sources"]

    def select(self, name="page.md", decision="KEEP", *, context=None, ranges=None):
        row = next(row for row in self.rows() if row["path"] == name)
        item = {"path": name, "sha256": row["source"]["sha256"], "decision": decision,
                "reason": "Inspected the exact page for target behavior.", "topic": "Request validation",
                "intent_status": "proposed intent", "context": context or []}
        if ranges is not None:
            item["ranges"] = ranges
        name = self.save({"schema_version": 1, "source_id": "docs", "decisions": [item]})
        return apply_selections(self.root, "docs", name)

    def plan(self, recipe="canonical-v1"):
        value = plan_sources(self.root, "docs", recipe)
        return value, self.save(value, "source-plan")

    def result(self, path="page.md", disposition="no_change", outputs=(), checkpoint=None):
        value = {"path": path, "disposition": disposition, "outputs": list(outputs),
                 "review": {"actor": "agent:fixture", "reviewed_at": "2026-11-12T00:00:00Z",
                            "note": "Inspected retained source and applicable intent; the disposition is supported."}}
        if checkpoint is not None:
            value["checkpoint"] = checkpoint
        return value

    def complete(self, plan, path, *results):
        batch = {"schema_version": 1, "source_id": "docs", "plan_id": plan["plan_id"], "results": list(results)}
        return complete_sources(self.root, "docs", path, self.save(batch, "completion"))

    def record(self, identifier="KT-first", *, source="page.md", extra=""):
        row = next(row for row in self.rows() if row["path"] == source)
        metadata = {"type": "KnowledgeTopic", "id": identifier, "version": 1,
                    "owner": "unknown", "governance_state": "candidate", "status": "draft",
                    "sources": [{key: row["source"][key] for key in ("resource", "revision", "sha256")}],
                    "generated": {"by": "agent:fixture", "at": "2026-11-12T00:00:00Z"}, "verified": [],
                    "classification": "fixture", "scope": "Request validation.",
                    "summary": "Invalid requests must be denied.", "related": [], "open_questions": []}
        body = "# Request validation\n\n" + "\n\n".join(
            "## " + heading + "\n\nThe system must deny invalid requests."
            for heading in HEADINGS["KnowledgeTopic"])
        body += f"\n\n[Retained source](../../{row['source']['snapshot']}#L1)\n" + extra
        name = f"knowledge/candidates/{identifier}.md"
        (self.root / name).write_text("---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n" + body)
        return name

    def audit(self, name):
        source = next(row["source"] for row in self.rows() if row["path"] == "page.md")
        event = {"id": "EV-incremental", "item_id": "KT-first", "item_version": 1,
                 "actor": "agent:fixture", "at": "2026-11-12T00:01:00Z", "action": "transition",
                 "from_state": "untracked", "to_state": "candidate",
                 "content_sha256": self.digest(name), "reason": "Retain the reviewed intent candidate.",
                 "evidence": [{key: source[key] for key in ("resource", "revision", "sha256")}]}
        (self.root / "evidence/knowledge/audit/EV-incremental.yaml").write_text(yaml.safe_dump(event))

    def digest(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def checkpoint(self, operation, **arguments):
        name = self.save({}, "checkpoint")
        (self.root / name).unlink()
        argv = [operation, "--workspace", str(self.root), "--output", str(self.root / name)]
        for key, value in arguments.items():
            argv.extend(["--" + key, str(self.root / value) if key != "phase" else value])
        with redirect_stdout(io.StringIO()):
            code = harness.main(argv)
        report = json.loads((self.root / name).read_text())
        self.assertEqual(code, 0, report)
        return name

    def sealed(self, baseline, outputs):
        plan = self.save({"schema_version": 1, "documents": list(outputs), "repositories": {}, "executions": []})
        prepared = self.checkpoint("check", baseline=baseline, plan=plan, phase="prepare")
        final = self.checkpoint("check", baseline=baseline, plan=plan, seal=prepared)
        return {"final": final, "prepared": prepared}

    def test_unreviewed_refresh_is_not_successful_canonical_processing(self):
        """Given new source bytes, when refresh repeats, then review remains queued until selected and completed."""
        self.page()
        self.refresh()
        plan, _ = self.plan()
        self.assertEqual(plan["counts"], {"documents": 1, "review": 1, "process": 0, "unchanged": 0})
        self.assertEqual(plan["review_queue"][0]["path"], "page.md")
        self.select()
        self.refresh()
        selected, path = self.plan()
        self.assertEqual([row["path"] for row in selected["process_queue"]], ["page.md"])
        self.assertEqual(load_plan(self.root, "docs", path), selected)
        self.assertNotIn("canonical_hashes", selected)
        baseline = json.loads((self.root / selected["baseline"]["path"]).read_text())
        self.assertIn("canonical_hashes", baseline)
        self.assertFalse((self.root / "evidence/knowledge/processing/docs.json").exists())

    def test_supported_no_change_is_idempotent_and_skips_unchanged_semantic_work(self):
        """Given reviewed unchanged intent, when completion retries, then one receipt remains and the next queue is empty."""
        self.page()
        self.refresh()
        self.select()
        plan, path = self.plan()
        result = self.result()
        completed = self.complete(plan, path, result)
        self.assertEqual((completed["written"], completed["remaining"]), (1, 0))
        before = (self.root / completed["receipts"]).read_bytes()
        self.assertEqual(self.complete(plan, path, result)["written"], 0)
        self.assertEqual((self.root / completed["receipts"]).read_bytes(), before)
        self.refresh()
        after, _ = self.plan()
        self.assertEqual(after["process_queue"], [])
        self.assertEqual(after["counts"]["unchanged"], 1)
        changed_recipe, _ = self.plan("canonical-v2")
        self.assertEqual(len(changed_recipe["process_queue"]), 1)

    def test_partial_completion_preserves_unfinished_work_and_rejects_conflicting_retry(self):
        """Given two pending pages, when only one completes, then the other remains retryable and success cannot be overwritten."""
        for name in ("a.md", "b.md"):
            self.page(name)
        self.refresh()
        for name in ("a.md", "b.md"):
            self.select(name)
        plan, path = self.plan()
        result = self.result("a.md")
        self.assertEqual(self.complete(plan, path, result)["remaining"], 1)
        next_plan, _ = self.plan()
        self.assertEqual([item["path"] for item in next_plan["process_queue"]], ["b.md"])
        changed = deepcopy(result)
        changed["review"]["note"] = "A conflicting completion must use a new plan."
        with self.assertRaisesRegex(WorkbenchError, "different completion"):
            self.complete(plan, path, changed)
        self.assertEqual(self.complete(plan, path, self.result("b.md"))["remaining"], 0)

    def test_excluded_changed_page_requires_selection_then_no_intent_processing(self):
        """Given excluded content, when its bytes change, then selection is reassessed without forcing unrelated canonical work."""
        page = self.page()
        self.refresh()
        self.select(decision="EXCLUDE")
        self.assertEqual(self.plan()[0]["counts"]["process"], 0)
        page.write_text("An updated operational checklist.\n")
        self.refresh()
        self.assertEqual(self.plan()[0]["counts"]["review"], 1)
        self.select(decision="EXCLUDE")
        self.assertEqual(self.plan()[0]["counts"]["process"], 0)

    def test_policy_context_and_raw_changes_invalidate_saved_plans(self):
        """Given hash-bound plans, when source or governing input changes, then stale completion cannot be recorded."""
        page = self.page()
        self.refresh()
        context = self.root / "governing.md"
        context.write_text("A governing condition.\n")
        self.select(context=[{"path": "governing.md", "sha256": self.digest("governing.md")}])
        plan, path = self.plan()
        for changed in (page, context, self.policy):
            with self.subTest(path=changed.name):
                original = changed.read_bytes()
                changed.write_bytes(original + b"# Changed governing input.\n")
                with self.assertRaises(WorkbenchError):
                    load_plan(self.root, "docs", path)
                self.assertGreater(self.plan()[0]["counts"]["review"], 0)
                with self.assertRaises(WorkbenchError):
                    self.complete(plan, path, self.result())
                changed.write_bytes(original)
        self.assertEqual(load_plan(self.root, "docs", path), plan)

    def test_selected_ranges_and_output_hashes_are_part_of_success_identity(self):
        """Given successful selected passages, when ranges or canonical bytes change, then the page is queued again."""
        self.page(body="First intended condition.\nSecond intended condition.\n")
        self.refresh()
        self.select(decision="KEEP_SECTIONS", ranges=[[1, 1]])
        record = self.record()
        plan, path = self.plan()
        self.complete(plan, path, self.result(outputs=[record]))
        self.assertEqual(self.plan()[0]["counts"]["process"], 0)
        self.select(decision="KEEP_SECTIONS", ranges=[[2, 2]])
        self.assertEqual(self.plan()[0]["counts"]["process"], 1)
        self.select(decision="KEEP_SECTIONS", ranges=[[1, 1]])
        (self.root / record).write_text((self.root / record).read_text() + "\nA new condition.\n")
        changed = self.plan()[0]["process_queue"][0]
        self.assertIn("output_changed_or_missing", changed["reasons"])
        self.assertEqual(changed["starting_outputs"][record], self.digest(record))

    def test_affected_scope_follows_citations_prior_outputs_and_canonical_dependents(self):
        """Given linked topics, when a source changes, then prior cited outputs and transitive dependents are selected."""
        self.page()
        self.page("other.md", "Another source.\n")
        self.refresh()
        self.select()
        self.select("other.md")
        first = self.record()
        second = self.record("KT-dependent", source="other.md", extra="[Depends on first](KT-first.md)\n")
        third = self.record("KT-independent", source="other.md")
        (self.root / "knowledge/index.md").write_text("[First](candidates/KT-first.md)\n[Other](candidates/KT-independent.md)\n")
        plan, path = self.plan()
        queued = next(item for item in plan["process_queue"] if item["path"] == "page.md")
        self.assertEqual(queued["affected_knowledge"], sorted([first, second]))
        self.assertNotIn(third, queued["affected_knowledge"])
        self.complete(plan, path, self.result(outputs=[first, second]))
        (self.raw / "page.md").write_text("A new intended condition.\n")
        self.refresh()
        self.select()
        updated = next(item for item in self.plan()[0]["process_queue"] if item["path"] == "page.md")
        self.assertEqual(updated["affected_knowledge"], sorted([first, second]))

    def test_missing_source_keeps_history_and_requires_explicit_disposition(self):
        """Given a completed source, when an export omits it, then history remains and missing review is explicit."""
        page = self.page()
        self.refresh()
        self.select()
        record = self.record()
        plan, path = self.plan()
        self.complete(plan, path, self.result(outputs=[record]))
        manifest = (self.root / "evidence/knowledge/manifest.yaml").read_bytes()
        canonical = (self.root / record).read_bytes()
        page.unlink()
        self.refresh()
        missing, missing_path = self.plan()
        self.assertIn("input_missing", missing["process_queue"][0]["reasons"])
        with self.assertRaisesRegex(WorkbenchError, "dispositions"):
            self.complete(missing, missing_path, self.result(outputs=[record]))
        self.complete(missing, missing_path, self.result(disposition="missing_reviewed", outputs=[record]))
        self.assertEqual(self.plan()[0]["counts"]["process"], 0)
        self.assertEqual((self.root / record).read_bytes(), canonical)
        self.assertEqual((self.root / "evidence/knowledge/manifest.yaml").read_bytes(), manifest)

    def test_excluding_former_intent_still_requires_affected_record_review(self):
        """Given successful kept intent, when selection withdraws it, then former outputs cannot be silently omitted."""
        self.page()
        self.refresh()
        self.select()
        record = self.record()
        plan, path = self.plan()
        self.complete(plan, path, self.result(outputs=[record]))
        self.select(decision="EXCLUDE")
        withdrawal, path = self.plan()
        self.assertEqual(withdrawal["process_queue"][0]["affected_knowledge"], [record])
        with self.assertRaisesRegex(WorkbenchError, "every affected"):
            self.complete(withdrawal, path, self.result(disposition="excluded"))
        self.complete(withdrawal, path, self.result(disposition="excluded", outputs=[record]))
        self.assertEqual(self.plan()[0]["counts"]["process"], 0)

    def test_updated_receipt_requires_real_matching_final_seal_and_preserves_retry(self):
        """Given new canonical bytes, when final sealed checks pass, then success binds their exact hashes and skips the next run."""
        self.page()
        self.refresh()
        self.select()
        plan, path = self.plan()
        baseline = self.checkpoint("start")
        record = self.record()
        self.audit(record)
        with self.assertRaisesRegex(WorkbenchError, "checkpoint"):
            self.complete(plan, path, self.result(disposition="updated", outputs=[record]))
        checkpoint = self.sealed(baseline, [record])
        self.assertTrue(validate_workspace(self.root)["valid"])
        result = self.result(disposition="updated", outputs=[record], checkpoint=checkpoint)
        self.assertEqual(self.complete(plan, path, result)["written"], 1)
        self.assertEqual(self.complete(plan, path, result)["written"], 0)
        self.assertEqual(self.plan()[0]["process_queue"], [])
        receipt = json.loads((self.root / "evidence/knowledge/processing/docs.json").read_text())["receipts"]["page.md"]
        self.assertEqual(receipt["outputs"], {record: self.digest(record)})
        self.assertEqual(receipt["starting_outputs"], {record: None})
        self.assertEqual(receipt["starting_fingerprint"], plan["process_queue"][0]["fingerprint"])
        self.assertEqual(receipt["input"]["recipe"], "canonical-v1")
        self.assertEqual(receipt["checkpoint"]["prepared"]["sha256"], self.digest(checkpoint["prepared"]))

    def test_no_change_and_unsealed_or_stale_checkpoints_cannot_hide_changed_outputs(self):
        """Given changed intent outputs, when completion claims no change or uses unsealed evidence, then it fails without a receipt."""
        self.page()
        self.refresh()
        self.select()
        plan, path = self.plan()
        baseline = self.checkpoint("start")
        record = self.record()
        self.audit(record)
        with self.assertRaisesRegex(WorkbenchError, "no-change"):
            self.complete(plan, path, self.result(outputs=[record]))
        checkpoint = self.sealed(baseline, [record])
        final = self.root / checkpoint["final"]
        report = json.loads(final.read_text())
        original = final.read_bytes()
        report.pop("seal")
        final.write_text(json.dumps(report))
        with self.assertRaisesRegex(WorkbenchError, "sealed"):
            self.complete(plan, path, self.result(disposition="updated", outputs=[record], checkpoint=checkpoint))
        final.write_bytes(original)
        (self.root / record).write_text((self.root / record).read_text() + "\nChanged after prepare.\n")
        with self.assertRaisesRegex(WorkbenchError, "current bytes"):
            self.complete(plan, path, self.result(disposition="updated", outputs=[record], checkpoint=checkpoint))
        self.assertFalse((self.root / "evidence/knowledge/processing/docs.json").exists())

    def test_unrelated_canonical_edits_and_changed_receipts_reject_old_plan(self):
        """Given an active plan, when unrelated canonical bytes or another plan's receipt changes, then completion must reconcile."""
        self.page()
        self.refresh()
        self.select()
        plan, path = self.plan()
        navigation = self.root / "knowledge/README.md"
        original = navigation.read_bytes()
        navigation.write_bytes(original + b"\nAn unrelated concurrent edit.\n")
        with self.assertRaisesRegex(WorkbenchError, "Unrelated canonical"):
            self.complete(plan, path, self.result())
        navigation.write_bytes(original)
        other, other_path = self.plan("canonical-v2")
        self.complete(other, other_path, self.result())
        with self.assertRaisesRegex(WorkbenchError, "processing changed"):
            self.complete(plan, path, self.result())

    def test_malformed_state_unsafe_outputs_and_symlink_paths_fail_without_mutation(self):
        """Given unsafe declarations, when planning or completing, then no successful receipt is written."""
        self.page()
        self.refresh()
        self.select()
        plan, path = self.plan()
        for output in ("../outside.md", "/tmp/outside.md", "knowledge/llm-wiki/wiki/page.md"):
            with self.subTest(output=output), self.assertRaises(WorkbenchError):
                self.complete(plan, path, self.result(outputs=[output]))
        alias = self.root / "knowledge/candidates/alias.md"
        alias.symlink_to(self.raw / "page.md")
        with self.assertRaisesRegex(WorkbenchError, "symbolic links"):
            self.plan()
        alias.unlink()
        receipts = self.root / "evidence/knowledge/processing/docs.json"
        receipts.parent.mkdir(parents=True)
        malformed = b'{"schema_version":1,"source_id":"docs","receipts":{"page.md":{}}}\n'
        receipts.write_bytes(malformed)
        with self.assertRaises(WorkbenchError):
            self.plan()
        self.assertEqual(receipts.read_bytes(), malformed)

    def test_completion_race_and_busy_lock_never_commit_success(self):
        """Given concurrent changes or a held source lock, when completion runs, then the success metadata remains absent."""
        self.page()
        self.refresh()
        self.select()
        plan, path = self.plan()
        original = validate_workspace

        def racing_validation(root):
            result = original(root)
            (self.raw / "page.md").write_text("Concurrent source change.\n")
            return result

        with patch("ai_sdlc_workbench.ingestion.incremental.validate_workspace", side_effect=racing_validation):
            with self.assertRaisesRegex(WorkbenchError, "changed during completion"):
                self.complete(plan, path, self.result())
        self.assertFalse((self.root / "evidence/knowledge/processing/docs.json").exists())
        lock = self.root / ".workbench/ingestion/source-preparation.lock"
        lock.write_text("Another operation owns this lock.\n")
        with self.assertRaisesRegex(WorkbenchError, "holds the workspace lock"):
            self.plan()
        self.assertEqual(lock.read_text(), "Another operation owns this lock.\n")

    def test_authored_malformed_metadata_and_urls_return_workbench_errors(self):
        """Given malformed authored content, when a plan scans it, then errors remain structured and no success is saved."""
        self.page()
        self.refresh()
        self.select()
        record = self.record()
        document = self.root / record
        original = document.read_bytes()
        for extra in (b"\n[Invalid URL](http://[)\n", b""):
            with self.subTest(kind="url" if extra else "non-JSON date"):
                if extra:
                    document.write_bytes(original + extra)
                else:
                    document.write_text("---\ndate: 2026-11-12\n---\nA malformed record.\n")
                with self.assertRaises(WorkbenchError):
                    self.plan()
                document.write_bytes(original)
        self.assertFalse((self.root / "evidence/knowledge/processing/docs.json").exists())

    def test_uppercase_canonical_files_and_missing_outputs_remain_in_scope(self):
        """Given a successful canonical output, when it disappears, then repair is queued and uppercase Markdown edits are detected."""
        self.page()
        self.refresh()
        self.select()
        record = self.record()
        plan, path = self.plan()
        self.complete(plan, path, self.result(outputs=[record]))
        original = (self.root / record).read_bytes()
        (self.root / record).unlink()
        repair = self.plan()[0]["process_queue"][0]
        self.assertEqual(repair["starting_outputs"], {record: None})
        self.assertIn("output_changed_or_missing", repair["reasons"])
        (self.root / record).write_bytes(original)
        uppercase = self.root / "knowledge/CUSTOM.MD"
        uppercase.write_text("An independently maintained canonical navigation page.\n")
        _, path = self.plan()
        uppercase.write_text("Concurrent uppercase Markdown edit.\n")
        with self.assertRaisesRegex(WorkbenchError, "Canonical content changed"):
            load_plan(self.root, "docs", path)

    def test_shared_navigation_update_preserves_other_source_success(self):
        """Given two completed sources sharing an index, when only navigation changes, then prior intent stays complete and domain edits still queue."""
        for name in ("a.md", "b.md"):
            self.page(name, body=f"The system must enforce the rule from {name}.\n")
        self.refresh()
        for name in ("a.md", "b.md"):
            self.select(name)
        first = self.record("KT-first", source="a.md")
        second = self.record("KT-second", source="b.md")
        navigation = "knowledge/index.md"
        (self.root / navigation).write_text("[First](candidates/KT-first.md)\n")
        first_plan, first_path = self.plan()
        self.complete(first_plan, first_path, self.result("a.md", outputs=[first, navigation]))
        first_index_hash = self.digest(navigation)
        second_plan, second_path = self.plan()
        self.assertEqual([item["path"] for item in second_plan["process_queue"]], ["b.md"])
        baseline = self.checkpoint("start")
        (self.root / navigation).write_text("[First](candidates/KT-first.md)\n[Second](candidates/KT-second.md)\n")
        checkpoint = self.sealed(baseline, [second, navigation])
        self.complete(second_plan, second_path, self.result("b.md", disposition="updated",
                      outputs=[second, navigation], checkpoint=checkpoint))
        self.assertEqual(self.plan()[0]["process_queue"], [])
        receipts = json.loads((self.root / "evidence/knowledge/processing/docs.json").read_text())["receipts"]
        self.assertEqual(receipts["a.md"]["outputs"][navigation], first_index_hash)
        self.assertNotEqual(receipts["a.md"]["outputs"][navigation], self.digest(navigation))
        self.assertNotIn(navigation, receipts["a.md"]["input"]["dependencies"])
        self.assertEqual(receipts["b.md"]["outputs"][navigation], self.digest(navigation))
        (self.root / first).write_text((self.root / first).read_text() + "\nA changed intended condition.\n")
        semantic = self.plan()[0]["process_queue"]
        self.assertEqual([item["path"] for item in semantic], ["a.md"])
        self.assertIn("output_changed_or_missing", semantic[0]["reasons"])

    def test_new_record_requires_review_of_newly_resolved_dependents(self):
        """Given an unresolved related ID, when its target is created, then completion must review the newly affected dependent too."""
        self.page()
        self.page("other.md", "The system must retain another intended condition.\n")
        self.refresh()
        self.select()
        self.select("other.md")
        dependent = self.record("KT-dependent", source="other.md")
        document = self.root / dependent
        _, frontmatter, body = document.read_text().split("---", 2)
        metadata = yaml.safe_load(frontmatter)
        metadata["related"] = ["KT-first"]
        document.write_text("---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---" + body)
        self.assertTrue(validate_workspace(self.root)["valid"])
        plan, path = self.plan()
        item = next(item for item in plan["process_queue"] if item["path"] == "page.md")
        self.assertEqual(item["affected_knowledge"], [])
        baseline = self.checkpoint("start")
        first = self.record()
        self.audit(first)
        checkpoint = self.sealed(baseline, [first])
        with self.assertRaisesRegex(WorkbenchError, "every affected"):
            self.complete(plan, path, self.result(disposition="updated", outputs=[first], checkpoint=checkpoint))
        self.assertFalse((self.root / "evidence/knowledge/processing/docs.json").exists())
        checkpoint = self.sealed(baseline, [first, dependent])
        self.complete(plan, path, self.result(disposition="updated", outputs=[first, dependent], checkpoint=checkpoint))
        next_plan, _ = self.plan()
        self.assertNotIn("page.md", [item["path"] for item in next_plan["process_queue"]])
        receipt = json.loads((self.root / "evidence/knowledge/processing/docs.json").read_text())["receipts"]["page.md"]
        self.assertEqual(set(receipt["outputs"]), {first, dependent})

    def test_completion_reports_pending_review_and_processing_separately(self):
        """Given selected and pending sources, when selected work completes, then pending review keeps the overall result partial."""
        self.page()
        self.page("pending.md", "An unreviewed intended condition.\n")
        self.refresh()
        self.select()
        plan, path = self.plan()
        completed = self.complete(plan, path, self.result())
        self.assertEqual(completed["status"], "PARTIAL")
        self.assertEqual(completed["remaining_process"], 0)
        self.assertEqual(completed["remaining_review"], 1)
        self.assertEqual(completed["remaining"], 0)
        self.select("pending.md")
        next_plan, path = self.plan()
        completed = self.complete(next_plan, path, self.result("pending.md"))
        self.assertEqual(completed["status"], "COMPLETED")
        self.assertEqual(completed["remaining_process"], 0)
        self.assertEqual(completed["remaining_review"], 0)
