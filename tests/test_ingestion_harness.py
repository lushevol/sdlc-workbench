"""Exercise retained evidence and final-byte checks through the harness CLI."""

from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml

from ai_sdlc_workbench.governance.schemas import HEADINGS
from ai_sdlc_workbench.ingestion.harness import main
from ai_sdlc_workbench.workspace import initialize_workspace


class IngestionHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ingestion-harness-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / "workspace"
        initialize_workspace(self.root)
        self.counter = 0
        self.raw = self.root / "evidence/knowledge/sources/source text.txt"
        self.raw.write_text("First source line.\nSecond source line.\nThird source line.\n",
                            encoding="utf-8")
        self.source = {
            "resource": "fixture://source",
            "revision": "v1",
            "sha256": self.digest(self.raw),
        }
        self.record = {
            "id": "fixture-source", **self.source,
            "ingested_at": "2026-10-16T00:00:00Z",
            "classification": "business",
            "snapshot": self.relative(self.raw),
        }
        self.manifest = self.root / "evidence/knowledge/manifest.yaml"
        self.manifest.write_text(yaml.safe_dump({"schema_version": 1,
            "sources": [self.record]}, sort_keys=False), encoding="utf-8")
        self.document = self.write_document()
        self.plan = {
            "schema_version": 1,
            "documents": [self.relative(self.document)],
            "repositories": {},
            "executions": [],
        }

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def relative(self, path):
        return path.relative_to(self.root).as_posix()

    def fresh_path(self, stem):
        self.counter += 1
        return self.directory / f"{stem}-{self.counter}.json"

    def invoke(self, arguments):
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(arguments)
        self.assertIn(code, (0, 1))
        try:
            result = json.loads(output.getvalue())
        except json.JSONDecodeError:
            self.fail(f"The harness did not emit JSON: {output.getvalue()!r}")
        return code, result

    def start(self):
        baseline = self.fresh_path("baseline")
        code, report = self.invoke(["start", "--workspace", str(self.root),
                                   "--output", str(baseline)])
        self.assertEqual(code, 0, report)
        self.assertTrue(baseline.is_file())
        self.assertEqual(json.loads(baseline.read_text())["schema_version"], 1)
        return baseline

    def check(self, baseline, *, plan=None, phase=None, seal=None):
        plan_path = self.fresh_path("plan")
        plan_path.write_text(json.dumps(self.plan if plan is None else plan), encoding="utf-8")
        output = self.fresh_path("result")
        arguments = ["check", "--workspace", str(self.root),
                     "--baseline", str(baseline), "--plan", str(plan_path),
                     "--output", str(output)]
        if phase is not None:
            arguments.extend(["--phase", phase])
        if seal is not None:
            arguments.extend(["--seal", str(seal)])
        code, report = self.invoke(arguments)
        self.assertTrue(output.is_file())
        self.assertEqual(json.loads(output.read_text()), report)
        return code, report, output

    @staticmethod
    def codes(report):
        return {finding["code"] for finding in report["findings"]}

    def snapshot(self):
        return {self.relative(path): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def write_document(self, *, identifier="KT-fixture", state="candidate", extra=""):
        path = self.root / f"knowledge/candidates/fixture/{identifier}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        metadata = {
            "type": "KnowledgeTopic", "id": identifier, "version": 1,
            "owner": "unknown", "governance_state": state, "status": "draft",
            "sources": [self.source],
            "generated": {"by": "agent:fixture", "at": "2026-10-16T00:00:00Z"},
            "verified": [], "classification": "fixture",
            "scope": "One retained local source.",
            "summary": "The fixture provides three source lines.",
            "related": [], "open_questions": ["Who owns the source?"],
        }
        body = "# Fixture topic\n\n" + "\n\n".join(
            f"## {heading}\n\nFixture context."
            for heading in HEADINGS["KnowledgeTopic"])
        body += ("\n\n[Source line](../../../evidence/knowledge/sources/source%20text.txt#L2)\n"
                 "[Summary](#summary)\n" + extra)
        path.write_text("---\n" + yaml.safe_dump(metadata, sort_keys=False)
                        + "---\n" + body, encoding="utf-8")
        return path

    def event(self, identifier, *, document=None, digest=None, previous=None,
              at="2026-10-16T00:01:00Z"):
        document = self.document if document is None else document
        metadata = yaml.safe_load(document.read_text().split("---", 2)[1])
        event = {
            "id": identifier, "item_id": metadata["id"], "item_version": metadata["version"],
            "actor": "agent:fixture", "at": at, "action": "transition",
            "from_state": "untracked", "to_state": "candidate",
            "content_sha256": digest or self.digest(document),
            "reason": "Retain the fixture candidate.", "evidence": [self.source],
        }
        if previous is not None:
            event["previous_event_id"] = previous
        path = self.root / f"evidence/knowledge/audit/{identifier}.yaml"
        path.write_text(yaml.safe_dump(event, sort_keys=False), encoding="utf-8")
        return path

    def test_unchanged_workspace_passes_without_mutating_workspace_bytes(self):
        before = self.snapshot()
        baseline = self.start()
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 0, report)
        self.assertEqual(report["phase"], "final")
        self.assertEqual(report["status"], "PASSED")
        self.assertEqual(report["automated_check"], "PASSED")
        self.assertEqual(report["standard"], "ASD-STE100")
        self.assertEqual(report["asd_review"], "PENDING")
        self.assertIsNone(report["reviewer"])
        self.assertIsNone(report["reviewed_at"])
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["prepared_content"],
                         {self.relative(self.document): self.digest(self.document)})
        self.assertEqual(self.snapshot(), before)

    def test_start_does_not_replace_an_existing_output(self):
        output = self.fresh_path("existing")
        output.write_bytes(b"Retain these original bytes.\n")
        before = output.read_bytes()
        code, _ = self.invoke(["start", "--workspace", str(self.root),
                               "--output", str(output)])
        self.assertEqual(code, 1)
        self.assertEqual(output.read_bytes(), before)

    def test_output_directory_alias_resolves_without_replacing_existing_files(self):
        directory = self.directory / "reports"
        directory.mkdir()
        alias = self.directory / "report-alias"
        try:
            alias.symlink_to(directory, target_is_directory=True)
        except OSError:
            self.skipTest("Directory links are unavailable on this platform")
        output = alias / "baseline.json"
        arguments = ["start", "--workspace", str(self.root), "--output", str(output)]
        code, report = self.invoke(arguments)
        self.assertEqual(code, 0, report)
        self.assertEqual(json.loads(output.read_text()), report)
        before = output.read_bytes()
        code, _ = self.invoke(arguments)
        self.assertEqual(code, 1)
        self.assertEqual(output.read_bytes(), before)

    def test_changed_and_missing_registered_snapshot_are_reported(self):
        baseline = self.start()
        original = self.raw.read_bytes()
        for expected, replacement in (("raw_file_changed", b"Changed bytes.\n"),
                                      ("raw_file_missing", None)):
            with self.subTest(expected=expected):
                if replacement is None:
                    self.raw.unlink()
                else:
                    self.raw.write_bytes(replacement)
                code, report, _ = self.check(baseline)
                self.assertEqual(code, 1)
                self.assertIn(expected, self.codes(report))
                self.raw.write_bytes(original)

    def test_appended_snapshot_and_manifest_record_preserve_the_baseline(self):
        baseline = self.start()
        second = self.root / "evidence/knowledge/sources/second.txt"
        second.write_text("Another retained source.\n", encoding="utf-8")
        record = {**self.record, "id": "second-source", "resource": "fixture://second",
                  "sha256": self.digest(second), "snapshot": self.relative(second)}
        self.manifest.write_text(self.manifest.read_text()
                                 + yaml.safe_dump([record], sort_keys=False), encoding="utf-8")
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 0, report)

    def test_registered_task_evidence_keeps_the_same_retention_checks(self):
        task_snapshot = self.root / "tasks/fixture/evidence/source.txt"
        task_snapshot.parent.mkdir(parents=True)
        task_snapshot.write_bytes(self.raw.read_bytes())
        self.record["snapshot"] = self.relative(task_snapshot)
        self.manifest.write_text(yaml.safe_dump({"schema_version": 1, "sources": [self.record]},
                                               sort_keys=False), encoding="utf-8")
        baseline = self.start()
        self.assertIn(self.relative(task_snapshot), json.loads(baseline.read_text())["raw_files"])
        task_snapshot.write_text("Changed task evidence.\n")
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        self.assertIn("raw_file_changed", self.codes(report))

    def test_first_source_can_be_added_after_an_empty_workspace_baseline(self):
        source_bytes = self.raw.read_bytes()
        self.root = self.directory / "empty-workspace"
        initialize_workspace(self.root)
        self.manifest = self.root / "evidence/knowledge/manifest.yaml"
        self.assertEqual(yaml.safe_load(self.manifest.read_text())["sources"], [])
        baseline = self.start()
        self.raw = self.root / "evidence/knowledge/sources/source text.txt"
        self.raw.write_bytes(source_bytes)
        self.manifest.write_text(yaml.safe_dump({"schema_version": 1,
            "sources": [self.record]}, sort_keys=False), encoding="utf-8")
        self.document = self.write_document()
        self.event("first-source-candidate")

        code, report, _ = self.check(baseline)
        self.assertEqual(code, 0, report)
        self.assertEqual(report["counts"]["manifest_records"], 1)
        self.assertEqual(self.raw.read_bytes(), source_bytes)

    def test_semantically_equivalent_manifest_rewrite_breaks_byte_retention(self):
        baseline = self.start()
        self.manifest.write_text("# Added before retained bytes.\n" + self.manifest.read_text(),
                                 encoding="utf-8")
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        self.assertIn("manifest_prefix_changed", self.codes(report))

    def test_historical_audit_files_cannot_be_changed_or_removed(self):
        audit = self.event("historical-event")
        baseline = self.start()
        original = audit.read_bytes()
        for expected, replacement in (("audit_file_changed", original + b"# changed\n"),
                                      ("audit_file_missing", None)):
            with self.subTest(expected=expected):
                if replacement is None:
                    audit.unlink()
                else:
                    audit.write_bytes(replacement)
                code, report, _ = self.check(baseline)
                self.assertEqual(code, 1)
                self.assertIn(expected, self.codes(report))
                audit.write_bytes(original)

    def test_unselected_baseline_candidate_cannot_be_removed(self):
        unselected = self.write_document(identifier="KT-unselected")
        baseline = self.start()
        unselected.unlink()

        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        missing = [finding for finding in report["findings"]
                   if finding["code"] == "governed_document_missing"]
        self.assertEqual([finding["path"] for finding in missing],
                         [self.relative(unselected)])

    def test_uppercase_markdown_change_requires_a_current_audit_event(self):
        uppercase = self.document.with_suffix(".MD")
        self.document.rename(uppercase)
        self.document = uppercase
        self.plan["documents"] = [self.relative(uppercase)]
        baseline = self.start()
        self.document.write_text(self.document.read_text() + "\nChanged candidate.\n",
                                 encoding="utf-8")

        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        self.assertIn("changed_document_audit_missing", self.codes(report))
        self.event("uppercase-candidate")
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 0, report)

    def test_malformed_and_escaping_plans_fail_closed(self):
        baseline = self.start()
        invalid = [
            {**self.plan, "documents": []},
            {**self.plan, "documents": self.plan["documents"] * 2},
            {**self.plan, "documents": ["../outside.md"]},
            {**self.plan, "documents": [str(self.document)]},
            {**self.plan, "unexpected": True},
            {**self.plan, "schema_version": 2},
        ]
        for plan in invalid:
            with self.subTest(plan=plan):
                code, report, _ = self.check(baseline, plan=plan)
                self.assertEqual(code, 1)
                self.assertIn("input_invalid", self.codes(report))

    def test_prepare_then_new_audit_then_sealed_final_is_valid(self):
        baseline = self.start()
        new_document = self.write_document(identifier="KT-new")
        plan = {**self.plan, "documents": [self.relative(new_document)]}
        code, failed, _ = self.check(baseline, plan=plan)
        self.assertEqual(code, 1)
        self.assertIn("changed_document_audit_missing", self.codes(failed))

        code, prepared, seal = self.check(baseline, plan=plan, phase="prepare")
        self.assertEqual(code, 0, prepared)
        self.assertEqual(prepared["status"], "PREPARED")
        self.assertIn("changed_document_audit_missing",
                      {finding["code"] for finding in prepared["deferred_findings"]})
        self.event("new-candidate", document=new_document)
        code, final, _ = self.check(baseline, plan=plan, seal=seal)
        self.assertEqual(code, 0, final)
        self.assertEqual(final["status"], "PASSED")
        self.assertEqual(final["prepared_content"], prepared["prepared_content"])

    def test_prepare_does_not_defer_an_unselected_document_gate(self):
        baseline = self.start()
        self.write_document(identifier="KT-unselected", state="investigated")
        code, report, _ = self.check(baseline, phase="prepare")
        self.assertEqual(code, 1)
        self.assertIn("audit_state_missing", self.codes(report))

    def test_seal_rejects_document_change_after_preparation(self):
        baseline = self.start()
        code, prepared, seal = self.check(baseline, phase="prepare")
        self.assertEqual(code, 0, prepared)
        self.document.write_text(self.document.read_text() + "\nLater changed content.\n",
                                 encoding="utf-8")
        self.event("changed-after-prepare")
        code, report, _ = self.check(baseline, seal=seal)
        self.assertEqual(code, 1)
        self.assertIn("seal_content_changed", self.codes(report))

    def test_a_failed_report_cannot_be_used_as_a_seal(self):
        baseline = self.start()
        code, prepared, _ = self.check(baseline, phase="prepare")
        self.assertEqual(code, 0, prepared)
        bad_seal = self.fresh_path("bad-seal")
        bad_seal.write_text(json.dumps({**prepared, "status": "FAILED",
                                       "automated_check": "FAILED"}), encoding="utf-8")
        code, report, _ = self.check(baseline, seal=bad_seal)
        self.assertEqual(code, 1)
        self.assertIn("input_invalid", self.codes(report))

    def test_a_new_audit_event_must_match_final_document_bytes(self):
        baseline = self.start()
        self.document.write_text(self.document.read_text() + "\nChanged candidate.\n",
                                 encoding="utf-8")
        self.event("wrong-target", digest="0" * 64)
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        self.assertIn("audit_target_hash_mismatch", self.codes(report))

    def test_correction_chain_preserves_older_event_and_checks_only_its_leaf(self):
        baseline = self.start()
        self.document.write_text(self.document.read_text() + "\nFirst draft.\n",
                                 encoding="utf-8")
        earlier = self.event("first-candidate")
        earlier_bytes = earlier.read_bytes()
        self.document.write_text(self.document.read_text() + "\nCorrected draft.\n",
                                 encoding="utf-8")
        self.event("corrected-candidate", previous="first-candidate",
                   at="2026-10-16T00:02:00Z")
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 0, report)
        self.assertEqual(earlier.read_bytes(), earlier_bytes)

    def test_audit_correction_chain_cannot_branch(self):
        baseline = self.start()
        self.document.write_text(self.document.read_text() + "\nChanged candidate.\n",
                                 encoding="utf-8")
        self.event("chain-root")
        self.event("first-child", previous="chain-root", at="2026-10-16T00:02:00Z")
        self.event("second-child", previous="chain-root", at="2026-10-16T00:03:00Z")
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        self.assertTrue(report["findings"])

    def test_audit_correction_cannot_branch_from_a_historical_chain(self):
        self.event("historical-root")
        child = self.event("historical-child", previous="historical-root",
                           at="2026-10-16T00:02:00Z")
        child_bytes = child.read_bytes()
        baseline = self.start()
        self.document.write_text(self.document.read_text() + "\nChanged candidate.\n",
                                 encoding="utf-8")
        self.event("new-sibling", previous="historical-root",
                   at="2026-10-16T00:03:00Z")

        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        self.assertIn("audit_correction_invalid", self.codes(report))
        self.assertEqual(child.read_bytes(), child_bytes)

    def test_audit_correction_can_extend_a_historical_chain(self):
        self.event("historical-root")
        child = self.event("historical-child", previous="historical-root",
                           at="2026-10-16T00:02:00Z")
        child_bytes = child.read_bytes()
        baseline = self.start()
        self.document.write_text(self.document.read_text() + "\nCorrected candidate.\n",
                                 encoding="utf-8")
        self.event("current-child", previous="historical-child",
                   at="2026-10-16T00:03:00Z")

        code, report, _ = self.check(baseline)
        self.assertEqual(code, 0, report)
        self.assertEqual(child.read_bytes(), child_bytes)

    def test_missing_target_and_invalid_physical_line_are_reported(self):
        baseline = self.start()
        self.document.write_text(self.document.read_text()
                                 + "\n[Missing](../../../evidence/knowledge/sources/missing.txt)\n"
                                 + "[Invalid line](../../../evidence/knowledge/sources/source%20text.txt#L99)\n",
                                 encoding="utf-8")
        self.event("broken-links")
        code, report, _ = self.check(baseline)
        self.assertEqual(code, 1)
        self.assertTrue({"link_missing", "line_fragment_invalid"} <= self.codes(report))

    def execution_fixture(self, *, stale):
        repository = self.directory / "fixture-repository"
        repository.mkdir()
        source = repository / "source.txt"
        source.write_text("Committed fixture source.\n", encoding="utf-8")
        environment = {key: value for key, value in os.environ.items()
                       if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")

        def git(*arguments):
            command = ["git", "-C", str(repository), "-c", "user.name=Fixture",
                       "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                       "-c", "core.hooksPath=/dev/null", *arguments]
            result = subprocess.run(command, capture_output=True, text=True, check=True,
                                    env=environment)
            return result.stdout.strip()

        git("init", "--quiet")
        git("add", "source.txt")
        git("commit", "--quiet", "-m", "Retain fixture source")
        revision = git("rev-parse", "HEAD")
        result = self.root / "tasks/fixture/evidence/execution/result.json"
        result.parent.mkdir(parents=True, exist_ok=True)
        result.write_text(json.dumps({
            "status": "PASSED",
            "source_sha256": {"source.txt": "0" * 64 if stale else self.digest(source)},
            "mocks": ["Fixture inputs only."],
            "limits": ["No business code was executed."],
        }), encoding="utf-8")
        execution_record = {
            "id": "fixture-execution", "resource": "fixture://execution",
            "revision": revision, "sha256": self.digest(result),
            "ingested_at": "2026-10-16T00:00:00Z",
            "classification": "implementation", "snapshot": self.relative(result),
        }
        self.manifest.write_text(self.manifest.read_text()
                                 + yaml.safe_dump([execution_record], sort_keys=False),
                                 encoding="utf-8")
        return {**self.plan, "repositories": {"fixture-repo": str(repository)},
                "executions": [{"result": self.relative(result),
                                "repository_id": "fixture-repo", "revision": revision}]}

    @unittest.skipUnless(shutil.which("git"), "Git is required for exact-revision fixtures")
    def test_execution_result_with_matching_commit_hash_passes(self):
        plan = self.execution_fixture(stale=False)
        baseline = self.start()
        code, report, _ = self.check(baseline, plan=plan)
        self.assertEqual(code, 0, report)

    @unittest.skipUnless(shutil.which("git"), "Git is required for exact-revision fixtures")
    def test_passing_execution_result_with_stale_source_hash_fails(self):
        plan = self.execution_fixture(stale=True)
        baseline = self.start()
        code, report, _ = self.check(baseline, plan=plan)
        self.assertEqual(code, 1)
        self.assertIn("execution_source_hash_mismatch", self.codes(report))


if __name__ == "__main__":
    unittest.main()
