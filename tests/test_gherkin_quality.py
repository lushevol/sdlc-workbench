"""Exercise quality gates, source freshness, and false-readiness boundaries."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from ai_sdlc_workbench.gherkin_quality import check_gherkin, evidence_schema
from jsonschema import Draft202012Validator


class GherkinQualityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="gherkin-quality-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = self.root / "case.feature"
        self.source = self.root / "source.txt"
        self.source.write_text('Fixture rule: saving displays Saved.\n<button>Save</button> in invoice form\n'
                               'def fixture_assertion(): assert saved_status == "Saved"\n', encoding="utf-8")
        self.text = ('Feature: Save an invoice\n  @UI-001\n  Scenario: Save invoice INV-1\n'
                     '    Given User A owns invoice INV-1\n'
                     '    When User A clicks the button labeled "Save" in the invoice form\n'
                     '    Then invoice INV-1 status equals "Saved"\n')
        self.path.write_text(self.text, encoding="utf-8")
        review = {"state": "PASS", "reviewer": "synthetic unit-test reviewer", "reviewed_at": "2000-01-01T00:00:00Z",
                  "notes": "Synthetic fixture only; this record does not approve actual business behavior."}
        self.data = {
            "version": 1,
            "evidence": {key: {"path": "source.txt", "sha256": self.digest(self.source), "start_line": 1,
                                "end_line": 3, "kind": kind, "authority": "established"}
                         for key, kind in (("B", "behavior"), ("U", "ui"), ("A", "automation"))},
            "scenarios": {"UI-001": {
                "file": "case.feature", "sha256": self.digest(self.path),
                "behavior": {"intent": "User A saves invoice INV-1.", "requirement": "B", "criterion": "source.txt:1"},
                "components": {"save": {"type": "button", "identity": "Save", "identity_kind": "visible_label",
                                         "scope": "in the invoice form", "evidence": ["U"]}},
                "steps": {"4": {"kind": "condition", "evidence": ["B"]},
                          "5": {"kind": "interaction", "components": ["save"], "evidence": ["U"]},
                          "6": {"kind": "assertion", "observation": "functional", "evidence": ["B"]}},
                "review": copy.deepcopy(review),
                "automation": {"framework": "Synthetic fixture", "mode": "mapped", "review": copy.deepcopy(review),
                               "bindings": {str(line): {"symbol": "fixture_assertion", "evidence": ["A"]} for line in (4, 5, 6)}}}}}
        self.entry = self.data["scenarios"]["UI-001"]
        self.manifest = self.root / "manifest.json"

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def check(self, **kwargs):
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")
        return check_gherkin([self.path], manifest=self.manifest, root=self.root, **kwargs)

    def rules(self, result):
        return {item["rule"] for item in result["findings"]}

    def replace(self, before, after):
        self.text = self.text.replace(before, after)
        self.path.write_text(self.text, encoding="utf-8")
        self.entry["sha256"] = self.digest(self.path)

    def test_schema_is_valid_and_supported_fixture_is_ready_without_execution_claim(self):
        Draft202012Validator.check_schema(evidence_schema())
        result = self.check()
        self.assertEqual(result["status"], "PASS", result)
        self.assertTrue(result["automation_ready"], result)
        self.assertEqual(result["exit_code"], 0)
        self.assertTrue(any("does not establish" in limit for limit in result["limitations"]))
        self.assertNotIn("execution_status", result)

    def test_ambiguous_click_has_actionable_failure_at_exact_step(self):
        self.replace('clicks the button labeled "Save" in the invoice form', 'clicks Save')
        result = self.check()
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["automation_ready"])
        self.assertTrue({"ui_type", "ui_identity", "ui_scope"}.issubset(self.rules(result)))
        finding = next(item for item in result["findings"] if item["rule"] == "ui_type")
        self.assertEqual((finding["scenario_id"], finding["line"]), ("UI-001", 5))
        self.assertTrue(finding["explanation"] and finding["correction"])

    def test_vague_success_and_circular_session_claim_fail(self):
        for clause in ("the operation succeeds", "the session is extended because the dialog closed"):
            with self.subTest(clause=clause):
                self.path.write_text(self.text.replace('invoice INV-1 status equals "Saved"', clause), encoding="utf-8")
                self.entry["sha256"] = self.digest(self.path)
                self.assertIn("result_vague", self.rules(self.check()))

    def test_complete_wording_without_manifest_is_unverified(self):
        result = check_gherkin([self.path])
        self.assertEqual(result["status"], "UNVERIFIED", result)
        self.assertEqual(result["exit_code"], 2)
        self.assertFalse(result["automation_ready"])

    def test_matching_hashes_do_not_replace_semantic_review(self):
        self.entry["review"]["state"] = "UNVERIFIED"
        result = self.check()
        self.assertEqual(result["status"], "UNVERIFIED")
        self.assertIn("semantic_review", self.rules(result))
        self.assertFalse(result["automation_ready"])

    def test_draft_expectations_cannot_produce_pass(self):
        self.data["evidence"]["B"]["authority"] = "draft"
        result = self.check()
        self.assertIn("expectation_authority", self.rules(result))
        self.assertFalse(result["automation_ready"])

    def test_changed_definition_invalidates_review(self):
        self.path.write_text(self.text + "# Changed after review\n", encoding="utf-8")
        result = self.check()
        self.assertIn("scenario_stale", self.rules(result))
        self.assertFalse(result["automation_ready"])

    def test_changed_or_missing_sources_remain_unverified(self):
        self.source.write_text("changed bytes\n", encoding="utf-8")
        self.assertIn("evidence_stale", self.rules(self.check()))
        self.source.unlink()
        self.assertFalse(self.check()["automation_ready"])

    def test_invalid_source_line_bounds_are_rejected(self):
        for first, last in ((2, 1), (1, 999)):
            self.data["evidence"]["B"].update(start_line=first, end_line=last)
            self.assertIn("evidence_stale", self.rules(self.check()))

    def test_evidence_cannot_escape_root_through_path_or_symlink(self):
        self.data["evidence"]["B"]["path"] = "../outside.txt"
        self.assertIn("evidence_stale", self.rules(self.check()))
        (self.root / "outside").symlink_to(self.root.parent, target_is_directory=True)
        self.data["evidence"]["B"]["path"] = "outside/outside.txt"
        self.assertIn("evidence_stale", self.rules(self.check()))

    def test_missing_assertion_binding_is_not_ready(self):
        del self.entry["automation"]["bindings"]["6"]
        result = self.check()
        self.assertIn("binding_missing", self.rules(result))
        self.assertFalse(result["automation_ready"])

    def test_missing_automation_or_its_review_is_not_ready(self):
        self.entry["automation"]["review"]["reviewer"] = None
        self.assertIn("automation_review", self.rules(self.check()))
        del self.entry["automation"]
        self.assertIn("automation_missing", self.rules(self.check()))

    def test_misclassified_automation_evidence_does_not_prove_binding(self):
        self.data["evidence"]["A"]["kind"] = "ui"
        self.assertIn("evidence_kind", self.rules(self.check()))

    def test_missing_ui_identity_or_inventory_component_is_not_ready(self):
        self.entry["components"]["save"]["identity"] = "Approve"
        self.assertIn("component_reference", self.rules(self.check()))
        del self.entry["components"]["save"]
        self.assertIn("component_unknown", self.rules(self.check()))

    def test_ui_result_needs_observed_component_and_assertion_kind(self):
        self.entry["steps"]["6"]["observation"] = "ui"
        self.assertIn("result_target", self.rules(self.check()))
        del self.entry["steps"]["6"]["observation"]
        self.assertIn("result_kind", self.rules(self.check()))

    def test_ui_action_cannot_be_hidden_as_event(self):
        self.entry["steps"]["5"]["kind"] = "event"
        self.assertIn("event_ui_action", self.rules(self.check()))

    def test_manifest_duplicate_keys_or_invalid_types_fail_without_crash(self):
        for value in ('{"version":1,"version":1}', '{"version":NaN}', '[]', '{"version":1}',
                      '{"version":1,"evidence":{},"scenarios":{"UI-001":null}}'):
            with self.subTest(value=value):
                self.manifest.write_text(value, encoding="utf-8")
                result = check_gherkin([self.path], manifest=self.manifest, root=self.root)
                self.assertEqual(result["status"], "FAIL", result)
                self.assertFalse(result["automation_ready"])

    def test_orphan_steps_and_bindings_fail(self):
        self.entry["steps"]["99"] = self.entry["steps"]["4"]
        self.entry["automation"]["bindings"]["99"] = self.entry["automation"]["bindings"]["4"]
        rules = self.rules(self.check())
        self.assertTrue({"step_orphan", "binding_orphan"}.issubset(rules))

    def test_warning_and_strict_policy_keep_readiness_explicit(self):
        self.entry["components"]["save"]["identity_kind"] = "stable_identifier"
        normal, strict = self.check(), self.check(strict=True)
        self.assertEqual(normal["status"], "WARNING")
        self.assertTrue(normal["automation_ready"])
        self.assertEqual(normal["exit_code"], 0)
        self.assertEqual(strict["exit_code"], 1)
        self.assertFalse(strict["automation_ready"])

    def test_background_and_markdown_fences_keep_absolute_lines(self):
        self.path = self.root / "case.md"
        self.entry["file"] = "case.md"
        body = ('# Fixture\n\n```gherkin\nFeature: Save\n  Background:\n'
                '    Given User A owns invoice INV-1\n  @UI-001\n  Scenario: Save invoice INV-1\n'
                '    When User A clicks the button labeled "Save" in the invoice form\n'
                '    Then invoice INV-1 status equals "Saved"\n```\n')
        self.path.write_text(body, encoding="utf-8")
        self.entry["sha256"] = self.digest(self.path)
        self.entry["steps"] = {str(new): self.entry["steps"][str(old)] for old, new in ((4, 6), (5, 9), (6, 10))}
        self.entry["automation"]["bindings"] = {str(new): self.entry["automation"]["bindings"][str(old)]
                                                   for old, new in ((4, 6), (5, 9), (6, 10))}
        result = self.check()
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["scenarios"][0]["line"], 8)

    def test_outline_examples_are_structural_not_execution_evidence(self):
        self.replace("Scenario: Save invoice INV-1", "Scenario Outline: Save invoice <invoice>")
        self.replace("invoice INV-1", "invoice <invoice>")
        self.path.write_text(self.text + "    Examples:\n      | invoice |\n      | INV-1 |\n", encoding="utf-8")
        self.entry["sha256"] = self.digest(self.path)
        result = self.check()
        self.assertEqual(result["status"], "PASS", result)
        self.path.write_text(self.path.read_text().replace("| invoice |", "| wrong |"), encoding="utf-8")
        self.assertEqual(self.check()["status"], "FAIL")

    def test_comments_and_other_fences_cannot_hide_missing_scenarios(self):
        self.path = self.root / "case.md"
        self.path.write_text('<!--\n```gherkin\n' + self.text + '```\n-->\n```text\n' + self.text + '```\n', encoding="utf-8")
        result = check_gherkin([self.path])
        self.assertIn("gherkin_missing", self.rules(result))

    def test_unknown_step_syntax_and_duplicate_scenario_ids_fail(self):
        self.replace('Then invoice', 'Thn invoice')
        self.assertIn("gherkin_unrecognized", self.rules(self.check()))
        other = self.root / "duplicate.feature"
        other.write_text(self.text, encoding="utf-8")
        result = check_gherkin([self.path, other])
        self.assertIn("scenario_duplicate", self.rules(result))

    def test_invalid_input_and_empty_selection_return_findings(self):
        self.assertEqual(check_gherkin([])["status"], "FAIL")
        self.assertEqual(check_gherkin([self.root / "missing.feature"])["status"], "FAIL")
        self.assertEqual(check_gherkin(["invalid\x00.feature"])["status"], "FAIL")
        self.assertEqual(check_gherkin([self.path], root="invalid\x00")["status"], "FAIL")

    def test_proposal_vague_success_example_cannot_pass(self):
        self.replace('invoice INV-1 status equals "Saved"', "the page shows success")
        self.assertIn("result_vague", self.rules(self.check()))

    def test_grammatical_statement_alone_is_not_an_observation(self):
        self.replace('invoice INV-1 status equals "Saved"', "the application is wonderful")
        result = self.check()
        self.assertIn("result_unknown", self.rules(result))
        self.assertFalse(result["automation_ready"])

    def test_identity_prefix_and_quoted_component_type_do_not_match(self):
        self.replace('labeled "Save"', 'labeled "Saved"')
        self.assertIn("component_reference", self.rules(self.check()))
        self.replace('the button labeled "Saved"', '"button" labeled "Save"')
        self.assertIn("ui_type", self.rules(self.check()))

    def test_ui_precondition_cannot_omit_inventory(self):
        self.replace("User A owns invoice INV-1", "the dialog is visible")
        result = self.check()
        self.assertIn("ui_reference", self.rules(result))
        self.assertFalse(result["automation_ready"])

    def test_multiple_actions_cannot_hide_an_unmapped_target(self):
        self.replace('in the invoice form\n', 'in the invoice form and clicks the button labeled "Delete"\n')
        result = self.check()
        self.assertIn("ui_multiple_actions", self.rules(result))
        self.assertFalse(result["automation_ready"])

    def test_blank_reviewer_and_nonexistent_binding_are_not_ready(self):
        self.entry["review"]["reviewer"] = "  "
        self.assertIn("manifest_schema", self.rules(self.check()))
        self.entry["review"]["reviewer"] = "synthetic unit-test reviewer"
        self.entry["automation"]["bindings"]["6"]["symbol"] = "missing_assertion"
        self.assertIn("binding_symbol", self.rules(self.check()))

    def test_every_duplicate_id_is_unready(self):
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")
        other = self.root / "duplicate.feature"
        other.write_text(self.text, encoding="utf-8")
        result = check_gherkin([self.path, other], manifest=self.manifest, root=self.root)
        self.assertTrue(all(not item["automation_ready"] for item in result["scenarios"]), result)

    def test_selection_leaves_business_only_scenarios_outside_ui_gate(self):
        self.path.write_text(self.text + '\n  @BUSINESS-1\n  Scenario: Business intent\n'
                            '    Given a draft invoice\n    When the owner approves it\n    Then its status equals approved\n', encoding="utf-8")
        self.entry["sha256"] = self.digest(self.path)
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")
        result = check_gherkin([self.path], manifest=self.manifest, root=self.root, scenario_ids=["UI-001"])
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(len(result["scenarios"]), 1)
        result = check_gherkin([self.path], manifest=self.manifest, root=self.root, scenario_ids=["missing"])
        self.assertIn("scenario_selection", self.rules(result))


if __name__ == "__main__":
    unittest.main()
