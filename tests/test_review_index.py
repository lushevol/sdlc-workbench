"""Check derived review references and preserve the boundaries of execution claims."""

from __future__ import annotations

import copy
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
from unittest.mock import patch

from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.review_index import analyze_index, read_index, schema


@unittest.skipUnless(shutil.which("git"), "Git is required to check exact revision evidence")
class ReviewIndexTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="review-index-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "repos/service"
        self.repo.mkdir(parents=True)
        self.code = "def accepts(value):\n    return value == 'valid'\n"
        (self.repo / "service.py").write_text(self.code)
        self.git("init", "-q", "-b", "main")
        self.git("add", "service.py")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qm", "Create source fixture")
        self.revision = self.git("rev-parse", "HEAD").strip()
        (self.root / "registry").mkdir()
        (self.root / "registry/repositories.yaml").write_text(json.dumps({
            "schema_version": 1, "repositories": [{"id": "service", "location": "repos/service"}],
        }))
        (self.root / "workspace.yaml").write_text(json.dumps({
            "schema_version": 1, "id": "index-fixture", "name": "Index boundary fixture",
            "resources": [], "plugins": [], "registries": {"repositories": "registry/repositories.yaml"},
        }))
        self.index = {"schema_version": 1, "id": "review-1", "scope_id": "service-review",
                      "title": "One derived evidence fixture",
                      "inventory_completeness": {"criteria": "COMPLETE", "changes": "SELECTED", "cases": "COMPLETE"},
                      "artifacts": [], "criteria": [], "changes": [], "cases": [], "assertions": [],
                      "links": [], "executions": [], "limits": ["Fixture evidence supplies no business approval."]}
        self.artifact("intent", "INTENT", "evidence/definitions.md", "# AC-1\nRequire acceptance.\n# TC-1\nAssert acceptance.\n")
        self.artifact("code", "CODE", "evidence/service.py", self.code,
                      repository_id="service", revision=self.revision, source_path="service.py")
        self.artifact("test", "TEST", "evidence/test_service.py", "from service import accepts\nassert accepts('valid') is True\n")
        self.artifact("result", "EXECUTION", "evidence/result.json", '{"status":"FAILED"}\n')
        self.artifact("assessment-source", "ASSESSMENT", "evidence/assessment.json", '{"recommendation":"NO_GO"}\n')
        self.index["criteria"] = [{"id": "AC-1", "definition": self.loc("intent", anchor="ac-1"),
                                   "required_levels": ["UNIT"], "limits": []}]
        self.index["changes"] = [{"id": "CH-1", "classification": "BUSINESS", "evidence": [self.loc("code", 1, 2)],
                                  "predicate_scope": "SELECTED", "limits": ["Selected predicate only."]}]
        self.index["cases"] = [{"id": "TC-1", "definition": self.loc("intent", anchor="tc-1"), "limits": []}]
        self.index["assertions"] = [{"id": "ASSERT-1", "case_id": "TC-1", "source": self.loc("test", 1, 2),
                                     "predicate_scope": "SELECTED", "limits": []}]
        for identifier, relation, source, target in [("L-1", "AC_CASE", "AC-1", "TC-1"),
                                                    ("L-2", "AC_CHANGE", "AC-1", "CH-1"),
                                                    ("L-3", "CHANGE_CASE", "CH-1", "TC-1")]:
            self.index["links"].append({"id": identifier, "relationship": relation, "from_id": source,
                                       "to_id": target, "evidence": [self.loc("test", 2, 2)],
                                       "assertion_ids": [] if relation == "AC_CHANGE" else ["ASSERT-1"],
                                       "predicate_scope": "SELECTED", "conformance": "UNKNOWN", "limits": []})
        self.index["executions"] = [{"id": "RUN-1", "case_id": "TC-1", "source": self.loc("result"),
                                     "original_status": "FAILED", "outcome": "FAILED", "characterization": False,
                                     "level": "UNIT", "mode": "CONTROLLED_SOURCE", "assertion_ids": ["ASSERT-1"],
                                     "environment_id": None, "limits": ["Fixture input; no deployment evidence."]}]
        self.index["assessment"] = {"source": self.loc("assessment-source"), "recommendation": "NO_GO",
                                    "decision_certainty": "HIGH", "summary": "Recorded fixture recommendation.",
                                    "review_state": "pending", "issues": [], "limits": ["No human approval."]}

    def git(self, *args):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True, env=environment)

    def artifact(self, identifier, kind, relative, content, **identity):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.index["artifacts"].append({"id": identifier, "kind": kind, "path": relative,
                                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), **identity})

    def loc(self, identifier, start=None, end=None, anchor=None):
        value = {"artifact_id": identifier}
        if start is not None:
            value.update(start_line=start, end_line=end)
        if anchor is not None:
            value["anchor"] = anchor
        return value

    def analyze(self):
        return analyze_index(self.index, self.root)

    def codes(self, report):
        return {item["code"] for item in report["diagnostics"]}

    def cli(self, *args):
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(["--workspace", str(self.root), "assurance", *args])
        return code, json.loads(stream.getvalue())

    def write_index(self):
        path = self.root / "review.json"
        path.write_text(json.dumps(self.index))
        return path

    def test_valid_current_references_never_grant_business_verification(self):
        """Given exact evidence
        When checked
        Then all references are current and business verification remains NOT_VERIFIED
        """
        report = self.analyze()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["freshness"], "CURRENT")
        self.assertEqual(report["verification"], "NOT_VERIFIED")
        self.assertEqual(report["records"]["executions"][0]["outcome"], "FAILED")
        self.assertEqual(report["assessment"]["recommendation"], "NO_GO")
        self.assertEqual(schema()["$id"], "urn:ai-sdlc-workbench:review-index:1")

    def test_characterization_pass_remains_distinct_from_verification(self):
        """Given a passing characterization
        When indexed
        Then its original outcome stays separate from business verification
        """
        self.index["executions"][0].update(original_status="passed", outcome="PASSED", characterization=True)
        row = self.analyze()["records"]["executions"][0]
        self.assertTrue(row["characterization"])
        self.assertEqual(row["original_status"], "passed")
        self.assertEqual(row["outcome"], "PASSED")
        self.assertEqual(row["verification"], "NOT_VERIFIED")

    def test_missing_result_is_unknown_without_turning_it_into_a_product_failure(self):
        """Given absent result bytes
        When indexed
        Then the contract stays valid and execution freshness becomes UNKNOWN
        """
        (self.root / "evidence/result.json").unlink()
        report = self.analyze()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["freshness"], "UNKNOWN")
        self.assertEqual(report["records"]["executions"][0]["freshness"], "UNKNOWN")
        self.assertEqual(report["records"]["executions"][0]["outcome"], "FAILED")
        self.assertIn("artifact_missing", self.codes(report))

    def test_stale_assertion_bytes_propagate_without_rewriting_results(self):
        """Given changed assertion bytes
        When indexed
        Then related links become STALE and original outcomes remain unchanged
        """
        (self.root / "evidence/test_service.py").write_text("from service import accepts\nassert False\n")
        report = self.analyze()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["freshness"], "STALE")
        self.assertEqual(report["records"]["assertions"][0]["freshness"], "STALE")
        self.assertEqual(report["records"]["links"][0]["freshness"], "STALE")
        self.assertEqual(report["records"]["executions"][0]["original_status"], "FAILED")

    def test_declared_git_revision_checks_exact_source_bytes(self):
        """Given retained code differs from its declared revision
        When checked
        Then source freshness is STALE
        """
        path = self.root / "evidence/service.py"
        path.write_text("def accepts(value):\n    return True\n")
        self.index["artifacts"][1]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        report = self.analyze()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["freshness"], "STALE")
        self.assertIn("git_hash_mismatch", self.codes(report))

    def test_unknown_git_revision_is_unknown_source_evidence(self):
        """Given unavailable revision bytes
        When checked
        Then freshness is UNKNOWN without inventing a source result
        """
        self.index["artifacts"][1]["revision"] = "a" * 40
        report = self.analyze()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["freshness"], "UNKNOWN")
        self.assertIn("source_unavailable", self.codes(report))

    def test_unsafe_and_symlink_evidence_paths_are_invalid(self):
        """Given escaping or symbolic evidence paths
        When checked
        Then the contract is INVALID
        """
        original = self.index["artifacts"][0]["path"]
        for value in ("../escape.md", "/tmp/escape.md", "C:/escape.md", "evidence/../definitions.md"):
            with self.subTest(path=value):
                self.index["artifacts"][0]["path"] = value
                report = self.analyze()
                self.assertFalse(report["valid"])
                self.assertIn("unsafe_evidence", self.codes(report))
        self.index["artifacts"][0]["path"] = original
        link = self.root / "evidence/link.md"
        link.symlink_to(self.root / original)
        self.index["artifacts"][0]["path"] = "evidence/link.md"
        self.assertFalse(self.analyze()["valid"])

    def test_duplicate_core_ids_and_issue_ids_are_invalid(self):
        """Given ambiguous record IDs
        When indexed
        Then duplicate records cannot establish valid references
        """
        self.index["cases"].append(copy.deepcopy(self.index["cases"][0]))
        report = self.analyze()
        self.assertFalse(report["valid"])
        self.assertIn("duplicate_id", self.codes(report))
        self.index["cases"].pop()
        issue = {"id": "ISSUE-1", "title": "Fixture issue", "observed_impact": "Fixture only.",
                 "priority": "P3", "release_blocking": False, "owner": "unknown", "next_action": "Inspect fixture.",
                 "evidence": [self.loc("result")], "limits": []}
        self.index["assessment"]["issues"] = [issue, copy.deepcopy(issue)]
        report = self.analyze()
        self.assertFalse(report["valid"])
        self.assertIn("duplicate_issue_id", self.codes(report))

    def test_absent_and_wrong_direction_references_are_invalid(self):
        """Given dangling or wrongly typed relationships
        When indexed
        Then reference validation fails
        """
        self.index["criteria"][0]["definition"]["artifact_id"] = "absent"
        self.index["links"][0]["to_id"] = "CH-1"
        report = self.analyze()
        self.assertFalse(report["valid"])
        self.assertIn("invalid_artifact_reference", self.codes(report))
        self.assertIn("invalid_record_reference", self.codes(report))

    def test_direct_change_test_links_require_a_matching_case_assertion(self):
        """Given a change-to-test claim without its direct assertion
        When checked
        Then the contract is INVALID
        """
        self.index["links"][2]["assertion_ids"] = []
        self.assertFalse(self.analyze()["valid"])
        self.index["links"][2]["assertion_ids"] = ["ASSERT-1"]
        self.index["cases"].append({"id": "TC-2", "definition": self.loc("intent"), "limits": []})
        self.index["assertions"][0]["case_id"] = "TC-2"
        report = self.analyze()
        self.assertFalse(report["valid"])
        self.assertIn("assertion_case_mismatch", self.codes(report))

    def test_invalid_or_ambiguous_text_locators_are_rejected(self):
        """Given malformed ranges or ambiguous anchors
        When checked
        Then text reference validation fails
        """
        original = self.index["criteria"][0]["definition"]
        for locator in [self.loc("intent", 4, 2), self.loc("intent", 1, 100),
                        {"artifact_id": "intent", "start_line": 1},
                        self.loc("intent", 1, 2, anchor="ac-1"), self.loc("intent", anchor="absent")]:
            with self.subTest(locator=locator):
                self.index["criteria"][0]["definition"] = locator
                self.assertFalse(self.analyze()["valid"])
        self.index["criteria"][0]["definition"] = self.loc("intent", anchor="same")
        path = self.root / "evidence/definitions.md"
        path.write_text('<a id="same"></a>\n<a id="same"></a>\n# TC-1\nCase.\n')
        self.index["artifacts"][0]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        report = self.analyze()
        self.assertFalse(report["valid"])
        self.assertIn("invalid_anchor", self.codes(report))
        self.index["criteria"][0]["definition"] = original

    def test_strict_json_and_unknown_fields_are_rejected(self):
        """Given duplicate JSON keys, non-finite values, or unknown fields
        When read
        Then strict input validation fails
        """
        path = self.root / "input.json"
        for value in ('{"id":1,"id":2}', '{"value":NaN}', '[]'):
            path.write_text(value)
            with self.subTest(value=value), self.assertRaises(WorkbenchError):
                read_index(path)
        self.index["unknown"] = True
        self.assertFalse(self.analyze()["valid"])

    def test_evidence_changes_during_analysis_invalidate_the_snapshot(self):
        """Given evidence changes during inspection
        When analysis ends
        Then the contract is INVALID and freshness is STALE
        """
        from ai_sdlc_workbench import review_index
        original = review_index._read
        target = self.root / "evidence/test_service.py"
        changed = False

        def mutate(path):
            nonlocal changed
            data = original(path)
            if path == target and not changed:
                changed = True
                path.write_text("assert False\n")
            return data

        with patch.object(review_index, "_read", side_effect=mutate):
            report = self.analyze()
        self.assertFalse(report["valid"])
        self.assertEqual(report["freshness"], "STALE")
        self.assertIn("evidence_changed_during_check", self.codes(report))

    def test_wrong_artifact_roles_cannot_establish_reference_validity(self):
        """Given an assertion points to result evidence
        When checked
        Then the artifact role mismatch is INVALID
        """
        self.index["assertions"][0]["source"] = self.loc("result")
        report = self.analyze()
        self.assertFalse(report["valid"])
        self.assertIn("artifact_kind_mismatch", self.codes(report))

    def test_anchor_catalog_is_parsed_once_for_multiple_definition_locators(self):
        """Given several references to one catalog
        When checked
        Then anchors are parsed once without losing valid references
        """
        from ai_sdlc_workbench import review_index
        with patch.object(review_index, "_anchors", wraps=review_index._anchors) as parser:
            report = self.analyze()
        self.assertTrue(report["valid"], report)
        self.assertEqual(parser.call_count, 1)

    def test_assessment_record_id_does_not_overwrite_artifact_freshness(self):
        """Given an artifact named assessment is stale
        When checked
        Then an assessment summary cannot overwrite that stale state
        """
        self.artifact("assessment", "SOURCE", "evidence/additional.json", '{}\n')
        (self.root / "evidence/additional.json").write_text('{"changed":true}\n')
        report = self.analyze()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["freshness"], "STALE")
        self.assertEqual(report["assessment"]["freshness"], "CURRENT")

    def test_cli_prints_schema_and_checks_current_index(self):
        """Given a current derived index
        When CLI inspection runs
        Then schema and current reference checks succeed
        """
        self.write_index()
        code, definition = self.cli("index-schema")
        self.assertEqual(code, 0)
        self.assertEqual(definition["$id"], "urn:ai-sdlc-workbench:review-index:1")
        code, report = self.cli("index", "--input", "review.json", "--require-current")
        self.assertEqual(code, 0, report)
        self.assertEqual(report["verification"], "NOT_VERIFIED")

    def test_cli_require_current_fails_on_unknown_evidence_without_failing_contract(self):
        """Given an absent result
        When current evidence is required
        Then CLI fails and preserves a valid UNKNOWN report
        """
        self.write_index()
        (self.root / "evidence/result.json").unlink()
        code, report = self.cli("index", "--input", "review.json")
        self.assertEqual(code, 0, report)
        code, report = self.cli("index", "--input", "review.json", "--require-current")
        self.assertEqual(code, 1)
        self.assertTrue(report["valid"])
        self.assertEqual(report["freshness"], "UNKNOWN")

    def test_cli_rejects_input_escapes_and_symlinks(self):
        """Given an input outside its workspace
        When CLI inspection runs
        Then path confinement rejects the input
        """
        path = self.write_index()
        for value in ("../review.json", str(self.root.parent / "review.json")):
            with self.subTest(path=value):
                code, report = self.cli("index", "--input", value)
                self.assertEqual(code, 1)
                self.assertIn("error", report)
        (self.root / "linked.json").symlink_to(path)
        code, report = self.cli("index", "--input", "linked.json")
        self.assertEqual(code, 1)
        self.assertIn("error", report)


if __name__ == "__main__":
    unittest.main()
