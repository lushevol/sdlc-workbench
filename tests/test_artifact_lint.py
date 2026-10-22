"""Check authoring contracts without claiming source authority or business execution."""

from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator
import yaml

from ai_sdlc_workbench.artifact_lint import artifact_schema, lint_artifacts
from ai_sdlc_workbench.cli import main


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "core/knowledge/templates/sdlc"


def sample_text(slug="requirement"):
    """Use the actual documented sample as a public authoring-contract fixture."""
    guide = (CATALOG / f"{slug}.md").read_text(encoding="utf-8")
    sample = guide.split("## Illustrative sample\n", 1)[1]
    return sample.split("````markdown\n", 1)[1].split("\n````", 1)[0] + "\n"


def replace_section(document, heading, replacement):
    pattern = rf"(^## {re.escape(heading)}\n).*?(?=^## |\Z)"
    changed, count = re.subn(pattern, lambda match: match.group(1) + "\n" + replacement + "\n\n",
                             document, flags=re.MULTILINE | re.DOTALL)
    if count != 1:
        raise AssertionError(f"Expected one section: {heading}")
    return changed


def replace_metadata(document, transform):
    _, raw_metadata, body = document.split("---", 2)
    metadata = yaml.safe_load(raw_metadata)
    transform(metadata)
    return "---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---" + body


class ArtifactLintTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-artifact-lint-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.sample = sample_text()

    def write(self, document=None, name="requirement.md"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.sample if document is None else document, encoding="utf-8")
        return path

    def assert_failed(self, result):
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["status"], "FAILED", result)
        self.assertFalse(result["valid"], result)
        self.assertTrue(result["findings"], result)

    def assert_error(self, result):
        self.assert_failed(result)
        self.assertTrue(any(item["severity"] == "error" for item in result["findings"]), result)

    def test_documented_requirement_sample_is_valid_and_discloses_limits(self):
        result = lint_artifacts([self.write()])
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["status"], "PASSED", result)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["artifacts"], 1)
        warnings = [finding for finding in result["findings"] if finding["severity"] == "warning"]
        self.assertTrue(warnings, result)
        descriptions = " ".join(finding["message"] for finding in warnings).lower()
        self.assertIn("owner", descriptions)
        self.assertIn("review", descriptions)
        self.assertTrue("sample" in descriptions or "illustrative" in descriptions, result)
        self.assertTrue(result["limitations"])
        for finding in result["findings"]:
            self.assertIsInstance(finding["path"], str)
            self.assertIsInstance(finding["code"], str)
            self.assertIn(finding["severity"], {"error", "warning"})
            self.assertTrue(finding["message"])

    def test_strict_mode_fails_on_warnings_without_changing_the_document(self):
        path = self.write()
        original = path.read_bytes()
        result = lint_artifacts([path], strict=True)
        self.assert_failed(result)
        self.assertTrue(any(finding["severity"] == "warning" for finding in result["findings"]))
        self.assertEqual(path.read_bytes(), original)

    def test_source_truth_and_execution_are_outside_the_authoring_check(self):
        document = self.sample.replace("SAMPLE-", "FIXTURE-").replace(
            "owner: unknown\n", "owner: Test fixture owner\n", 1)
        document = document.replace("sample-context.md", "unavailable-fixture-policy.md")
        document = document.replace("sample-v1", "a" * 40)
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["status"], "PASSED", result)
        self.assertFalse((self.root / "unavailable-fixture-policy.md").exists())

    def test_sample_identifiers_in_related_ids_or_body_produce_a_warning(self):
        fixture = self.sample.replace("SAMPLE-", "FIXTURE-")
        documents = (
            replace_metadata(fixture, lambda metadata: metadata.update({"related_ids": ["SAMPLE-RELATED-001"]})),
            replace_section(fixture, "Rationale", "SAMPLE-RULE-001 defines the proposed access condition."),
        )
        for document in documents:
            with self.subTest(document=document[:80]):
                result = lint_artifacts([self.write(document)])
                self.assertTrue(result["valid"], result)
                self.assertTrue(any(finding["code"] == "sample_content" and finding["severity"] == "warning"
                                    for finding in result["findings"]), result)

    def test_nonsample_identifiers_do_not_produce_a_sample_warning(self):
        document = self.sample.replace("SAMPLE-", "FIXTURE-").replace("sample", "fixture").replace(
            "illustrative", "fixture-only")
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)
        self.assertFalse(any(finding["code"] == "sample_content" for finding in result["findings"]), result)

    def test_catalog_guide_is_not_an_authored_document(self):
        result = lint_artifacts([CATALOG / "requirement.md"])
        self.assert_error(result)

    def test_every_catalog_sample_satisfies_its_authoring_contract(self):
        guides = sorted(path for path in CATALOG.glob("*.md")
                        if "## Illustrative sample\n" in path.read_text(encoding="utf-8"))
        self.assertEqual(len(guides), 37)
        for guide in guides:
            with self.subTest(kind=guide.stem):
                result = lint_artifacts([self.write(sample_text(guide.stem), guide.name)])
                self.assertTrue(result["valid"], result)
                self.assertEqual(result["artifacts"], 1)

    def test_all_catalog_samples_can_be_linted_as_one_artifact_collection(self):
        guides = sorted(path for path in CATALOG.glob("*.md")
                        if "## Illustrative sample\n" in path.read_text(encoding="utf-8"))
        self.assertEqual(len(guides), 37)
        for guide in guides:
            self.write(sample_text(guide.stem), f"samples/{guide.name}")
        result = lint_artifacts([self.root / "samples"])
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["artifacts"], 37)

    def defect_document(self, sections):
        """Bind explicit section fixtures to the public defect metadata contract."""
        _, metadata, _ = sample_text("defect-report").split("---", 2)
        body = "\n\n".join(f"## {heading}\n\n{content}" for heading, content in sections.items())
        return f"---{metadata}---\n\n# Invoice access defect fixture\n\n{body}\n"

    def test_six_section_defect_report_accepts_the_concise_issue_contract(self):
        sections = {
            "Problem description": "A denied request can expose invoice content. This fixture records no confirmed occurrence.",
            "Existing knowledge and code facts": "SAMPLE-AC-002 proposes zero invoices for a denied request.",
            "User clarifications": "No actual user supplied clarification for this fixture.",
            "Reproduction and verification": "Execution is NOT_RUN. No screenshots or runtime observations exist.",
            "Root cause analysis": "The cause remains unknown because no implementation revision was inspected.",
            "Proposed fix and acceptance criteria": "The proposed regression asserts zero invoices after a denied request.",
        }
        result = lint_artifacts([self.write(self.defect_document(sections), "defect.md")])
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["artifacts"], 1)

        for heading in sections:
            with self.subTest(missing=heading):
                incomplete = {name: content for name, content in sections.items() if name != heading}
                result = lint_artifacts([self.write(self.defect_document(incomplete), "defect.md")])
                self.assert_error(result)
                self.assertTrue(any(finding["code"] == "artifact_schema"
                                    for finding in result["findings"]), result)

    def test_legacy_defect_report_contract_remains_accepted(self):
        sections = {
            "Classification and scope": "The denied invoice request is a hypothetical defect fixture.",
            "Reproduction conditions": "Execution is NOT_RUN. No runtime observation exists.",
            "Hypothesis and impact": "Invoice exposure is hypothetical. The actual impact remains unknown.",
            "Resolution and regression": "The proposed regression asserts zero invoices for a denied request.",
            "Facts, inferences, and unresolved questions": "The actual implementation and cause remain unknown.",
            "Findings": "No execution supports confirmation. The owner must obtain a reproduction result.",
            "Sources": "SAMPLE-AC-002 is illustrative and establishes no actual policy authority.",
        }
        document = self.defect_document(sections)
        result = lint_artifacts([self.write(document, "legacy-defect.md")])
        self.assertTrue(result["valid"], result)
        incomplete = {name: content for name, content in sections.items() if name != "Sources"}
        self.assert_error(lint_artifacts([self.write(self.defect_document(incomplete), "legacy-defect.md")]))

    def test_frontmatter_contract_rejects_missing_fields_wrong_types_and_unknown_enums(self):
        replacements = (
            ("artifact_kind: requirement\n", "artifact_kind: unsupported\n"),
            ('id: "SAMPLE-REQ-001"\n', ""),
            ("version: 1\n", "version: true\n"),
            ("version: 1\n", 'version: "1"\n'),
            ("source_refs: [SAMPLE-SRC-001]\n", "source_refs: SAMPLE-SRC-001\n"),
            ("related_ids: []\n", "related_ids: [DUPLICATE, DUPLICATE]\n"),
            ("status: draft\n", "status: invented-status\n"),
        )
        for before, after in replacements:
            with self.subTest(replacement=after):
                self.assert_error(lint_artifacts([self.write(self.sample.replace(before, after, 1))]))

    def test_metadata_extensions_remain_valid_and_are_preserved(self):
        document = replace_metadata(self.sample, lambda metadata: metadata.update(
            {"project_tracking": {"work_item": "FIXTURE-123", "labels": ["invoice"]}}))
        path = self.write(document)
        before = path.read_bytes()
        result = lint_artifacts([path])
        self.assertTrue(result["valid"], result)
        self.assertEqual(path.read_bytes(), before)

    def test_metadata_identifiers_reject_trailing_newlines(self):
        for field, value in (("id", "REQ-001\n"), ("source_refs", ["SOURCE-001\n"]),
                             ("related_ids", ["RELATED-001\n"])):
            with self.subTest(field=field):
                document = replace_metadata(self.sample, lambda metadata: metadata.update({field: value}))
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_authored_sections_accept_nested_yaml_sequence_examples(self):
        body = '''The proposed response includes these fixture values.

```yaml
- invoice: INV-001
  lines:
    - description: Test fixture item
      quantity: 1
```'''
        document = replace_section(self.sample, "Description", body)
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)

    def test_completed_business_reviews_require_recorded_reviewer_and_date(self):
        for state in ("approved", "rejected"):
            for reviewer, reviewed_at in ((None, None), ("Test fixture reviewer", None),
                                           (None, "2026-10-15T01:00:00Z")):
                with self.subTest(state=state, reviewer=reviewer, reviewed_at=reviewed_at):
                    document = replace_metadata(self.sample, lambda metadata: metadata.update(
                        {"review": {"state": state, "reviewer": reviewer, "reviewed_at": reviewed_at}}))
                    self.assert_error(lint_artifacts([self.write(document)]))
            document = replace_metadata(self.sample, lambda metadata: metadata.update(
                {"review": {"state": state, "reviewer": "Test fixture reviewer",
                            "reviewed_at": "2026-10-15T01:00:00Z"}}))
            self.assertTrue(lint_artifacts([self.write(document)])["valid"])

    def test_complete_writing_review_requires_reviewer_and_date(self):
        for reviewer, reviewed_at in ((None, None), ("Test fixture reviewer", None),
                                       (None, "2026-10-15T01:00:00Z")):
            with self.subTest(reviewer=reviewer, reviewed_at=reviewed_at):
                document = replace_metadata(self.sample, lambda metadata: metadata["writing_review"].update(
                    {"asd_review": "PASSED", "reviewer": reviewer, "reviewed_at": reviewed_at}))
                self.assert_error(lint_artifacts([self.write(document)]))
        document = replace_metadata(self.sample, lambda metadata: metadata["writing_review"].update(
            {"automated_check": "PASSED", "asd_review": "PASSED", "reviewer": "Test fixture reviewer",
             "reviewed_at": "2026-10-15T01:00:00Z"}))
        self.assertTrue(lint_artifacts([self.write(document)])["valid"])

    def test_review_timestamps_require_real_calendar_dates_and_explicit_timezones(self):
        for timestamp in ("2026-02-30T01:00:00Z", "2026-10-15T01:00:00", "not-a-date"):
            with self.subTest(timestamp=timestamp):
                document = replace_metadata(self.sample, lambda metadata: metadata.update(
                    {"review": {"state": "approved", "reviewer": "Test fixture reviewer",
                                "reviewed_at": timestamp}}))
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_duplicate_yaml_keys_are_errors_in_frontmatter_and_criteria(self):
        documents = (
            self.sample.replace("version: 1\n", "version: 1\nversion: 2\n", 1),
            self.sample.replace("      value: 1\n", "      value: 1\n      value: 2\n", 1),
        )
        for document in documents:
            with self.subTest(document=document[:80]):
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_malformed_frontmatter_and_utf8_return_findings(self):
        documents = (
            self.sample.replace("---\n", "", 1),
            self.sample.replace("artifact_kind: requirement", "artifact_kind: [requirement", 1),
            self.sample.replace("\n---\n", "\n...\n", 1),
        )
        for document in documents:
            with self.subTest(document=document[:80]):
                self.assert_error(lint_artifacts([self.write(document)]))
        path = self.root / "invalid-utf8.md"
        path.write_bytes(b"---\nartifact_kind: requirement\n---\n\xff")
        self.assert_error(lint_artifacts([path]))

    def test_required_section_cannot_be_missing_or_empty(self):
        documents = (
            self.sample.replace("## Description", "## Other description", 1),
            replace_section(self.sample, "Description", ""),
            replace_section(self.sample, "Description", "<!-- A comment is not content. -->"),
            replace_section(self.sample, "Description", "| Behavior | Evidence |\n| --- | --- |"),
        )
        for document in documents:
            with self.subTest(document=document[-120:]):
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_inline_code_comment_markers_preserve_subsequent_required_sections(self):
        descriptions = (
            "Use `<!--` as a diagnostic marker.",
            "Use ``<!-- ` diagnostic`` as a diagnostic marker.",
            r"Use \` as a literal delimiter and `<!--` as a diagnostic marker.",
        )
        for description in descriptions:
            with self.subTest(description=description):
                document = replace_section(self.sample, "Description", description)
                result = lint_artifacts([self.write(document)])
                self.assertTrue(result["valid"], result)

    def test_fenced_html_comment_is_meaningful_code_content(self):
        document = replace_section(self.sample, "Description", "```html\n<!-- diagnostic marker -->\n```")
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)

    def test_required_atx_headings_allow_at_most_three_leading_spaces(self):
        for spaces in (1, 2, 3, 4):
            with self.subTest(spaces=spaces):
                document = self.sample.replace("## Description", " " * spaces + "## Description", 1)
                result = lint_artifacts([self.write(document)])
                if spaces <= 3:
                    self.assertTrue(result["valid"], result)
                else:
                    self.assert_error(result)

    def test_heading_inside_code_fence_does_not_supply_a_required_section(self):
        document = self.sample.replace("## Description", "```text\n## Description\n```", 1)
        self.assert_error(lint_artifacts([self.write(document)]))

    def test_heading_inside_html_comment_does_not_supply_a_required_section(self):
        commented_headings = (
            "<!--\n## Description\n-->",
            "<!--\n```markdown\n## Description\n```\n-->",
        )
        for heading in commented_headings:
            with self.subTest(heading=heading):
                document = self.sample.replace("## Description", heading, 1)
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_table_with_only_empty_data_cells_does_not_supply_section_content(self):
        document = replace_section(self.sample, "Description", "| A | B |\n|---|---|\n|||")
        self.assert_error(lint_artifacts([self.write(document)]))

    def test_duplicate_sections_cannot_hide_conflicting_content(self):
        document = self.sample + "\n## Description\n\nA different requirement description.\n"
        self.assert_error(lint_artifacts([self.write(document)]))

    def test_unresolved_template_placeholders_are_errors(self):
        for placeholder in ("{{business_need}}", "{{numeric_target}}"):
            with self.subTest(placeholder=placeholder):
                document = self.sample.replace("This sample records proposed intent only.", placeholder, 1)
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_structured_criteria_require_numeric_measures_and_supported_operators(self):
        replacements = (
            ("      value: 1\n", '      value: "1"\n'),
            ("      value: 1\n", "      value: true\n"),
            ("      value: 1\n", "      value: .nan\n"),
            ("      operator: equals\n", "      operator: approximately\n"),
            ("      unit: count\n", '      unit: ""\n'),
        )
        for before, after in replacements:
            with self.subTest(replacement=after):
                self.assert_error(lint_artifacts([self.write(self.sample.replace(before, after, 1))]))

    def test_structured_criteria_require_condition_action_result_prefixes(self):
        for prefix in ("Given ", "When ", "Then "):
            with self.subTest(prefix=prefix):
                # Mutate YAML only. The readable Gherkin remains complete.
                first, criteria = self.sample.split("```yaml\n", 1)
                document = first + "```yaml\n" + criteria.replace(prefix, "", 1)
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_structured_criterion_identifiers_reject_whitespace_and_newlines(self):
        for identifier in ('"SAMPLE AC 001"', '" SAMPLE-AC-001"', '"SAMPLE-AC-001 "',
                           '"SAMPLE-AC-001\\n"'):
            with self.subTest(identifier=identifier):
                document = self.sample.replace("  - id: SAMPLE-AC-001\n", f"  - id: {identifier}\n", 1)
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_requirement_cannot_omit_its_structured_acceptance_criteria(self):
        document = re.sub(r"(?ms)```yaml\nacceptance_criteria:.*?\n```", "", self.sample, count=1)
        self.assert_error(lint_artifacts([self.write(document)]))

    def test_requirement_accepts_multiple_criteria_in_one_structured_list(self):
        match = re.search(r"(?ms)```yaml\n(acceptance_criteria:.*?)\n```", self.sample)
        criteria = yaml.safe_load(match.group(1))["acceptance_criteria"]
        second = deepcopy(criteria[0])
        second["id"] = "SAMPLE-AC-002"
        second["measure"]["metric"] = "matching invoice identifier count"
        criteria.append(second)
        block = "```yaml\n" + yaml.safe_dump({"acceptance_criteria": criteria}, sort_keys=False) + "```"
        document = self.sample[:match.start()] + block + self.sample[match.end():]
        scenario = '''

  @SAMPLE-REQ-001 @SAMPLE-AC-002
  Scenario: Response preserves the requested invoice identifier
    Given customer "A" is authenticated and owns invoice "INV-001"
    When customer "A" requests invoice "INV-001"
    Then the response contains exactly one invoice with identifier "INV-001"
'''
        document = document.replace("\n```\n\n```yaml", scenario + "```\n\n```yaml", 1)
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)

    def test_distinct_repeated_structured_criteria_sets_remain_errors(self):
        match = re.search(r"(?ms)```yaml\n(acceptance_criteria:.*?)\n```", self.sample)
        different = yaml.safe_load(match.group(1))["acceptance_criteria"]
        different[0]["id"] = "SAMPLE-AC-002"
        repeated_block = "\n```yaml\n" + yaml.safe_dump({"acceptance_criteria": different}, sort_keys=False) + "```\n"
        documents = (
            self.sample + repeated_block,
            replace_metadata(self.sample, lambda metadata: metadata.update({"acceptance_criteria": different})),
        )
        for document in documents:
            with self.subTest(document=document[:80]):
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_gherkin_requires_ordered_conditions_action_and_observable_result(self):
        pattern = r"(?ms)```gherkin\n.*?\n```"
        scenarios = (
            'Feature: Access\n  Scenario: Missing condition\n    When a customer requests an invoice\n'
            '    Then the response contains one invoice',
            'Feature: Access\n  Scenario: Missing action\n    Given a customer owns an invoice\n'
            '    Then the response contains one invoice',
            'Feature: Access\n  Scenario: Missing result\n    Given a customer owns an invoice\n'
            '    When the customer requests the invoice',
            'Feature: Access\n  Scenario: Wrong order\n    When a customer requests an invoice\n'
            '    Given the customer owns the invoice\n    Then the response contains one invoice',
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                document = re.sub(pattern, "```gherkin\n" + scenario + "\n```", self.sample, count=1)
                self.assert_error(lint_artifacts([self.write(document)]))

    def test_gherkin_retains_intermediate_assertions_between_actions(self):
        specification = ('Feature: View invoice revisions\n  Scenario: Reopen an invoice\n'
                         '    Given a customer owns invoice INV-1\n'
                         '    When the customer opens invoice INV-1\n'
                         '    Then the invoice status equals Draft\n'
                         '    When the customer closes invoice INV-1\n'
                         '    Then the invoice list is visible')
        document = re.sub(r"(?ms)```gherkin\n.*?\n```", "```gherkin\n" + specification + "\n```", self.sample, count=1)
        self.assertTrue(lint_artifacts([self.write(document)])["valid"])
        unfinished = specification + '\n    When the customer opens invoice INV-1'
        document = re.sub(r"(?ms)```gherkin\n.*?\n```", "```gherkin\n" + unfinished + "\n```", self.sample, count=1)
        self.assert_error(lint_artifacts([self.write(document)]))

    def test_scenario_cannot_precede_its_feature(self):
        specification = '''```gherkin
Scenario: Customer views an owned invoice
  Given customer "A" owns invoice "INV-001"
  When customer "A" requests invoice "INV-001"
  Then the response contains exactly one invoice

Feature: View invoices
```'''
        document = replace_section(sample_text("bdd-feature"), "Gherkin specification", specification)
        self.assert_error(lint_artifacts([self.write(document)]))

    def test_background_and_rule_can_supply_shared_given_conditions(self):
        specification = '''```gherkin
Feature: View invoices
  Rule: Customers view owned invoices
    Background: Authenticated session
      Given customer "A" is authenticated
      And customer "A" owns invoice "INV-001"

    @SAMPLE-REQ-001 @SAMPLE-AC-001 @SAMPLE-TEST-001
    Scenario: Customer views the invoice
      When customer "A" requests invoice "INV-001"
      Then the response contains exactly one invoice
      And the invoice identifier is "INV-001"
```'''
        document = replace_section(sample_text("bdd-feature"), "Gherkin specification", specification)
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)

    def test_each_scenario_requires_its_own_conditions_without_a_background(self):
        specification = '''```gherkin
Feature: View invoices
  Scenario: Customer views an owned invoice
    Given customer "A" owns invoice "INV-001"
    When customer "A" requests invoice "INV-001"
    Then the response contains exactly one invoice

  Scenario: Customer requests another invoice
    When customer "A" requests invoice "INV-002"
    Then the response contains exactly one invoice
```'''
        document = replace_section(sample_text("bdd-feature"), "Gherkin specification", specification)
        self.assert_error(lint_artifacts([self.write(document)]))

    def test_unnamed_background_supplies_shared_given_conditions(self):
        specification = '''```gherkin
Feature: View invoices
  Background:
    Given customer "A" is authenticated and owns invoice "INV-001"

  Scenario: Customer views an owned invoice
    When customer "A" requests invoice "INV-001"
    Then the response contains exactly one invoice
```'''
        document = replace_section(sample_text("bdd-feature"), "Gherkin specification", specification)
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)

    def test_scenario_outline_requires_matching_example_columns_and_rows(self):
        specification = '''```gherkin
Feature: View invoices
  Scenario Outline: Customer requests an owned invoice
    Given customer "<customer>" is authenticated and owns invoice "<invoice>"
    When customer "<customer>" requests invoice "<invoice>"
    Then the response contains exactly <count> invoice

    Examples:
      | customer | invoice | count |
      | A | INV-001 | 1 |
```'''
        document = replace_section(sample_text("bdd-feature"), "Gherkin specification", specification)
        result = lint_artifacts([self.write(document)])
        self.assertTrue(result["valid"], result)
        invalid = (
            specification.replace("      | A | INV-001 | 1 |\n", ""),
            specification.replace("      | A | INV-001 | 1 |", "      | A | INV-001 |"),
            specification.replace("| customer | invoice | count |", "| customer | invoice | other |"),
            specification.split("    Examples:\n", 1)[0] + "```",
        )
        for candidate in invalid:
            with self.subTest(specification=candidate):
                malformed = replace_section(sample_text("bdd-feature"), "Gherkin specification", candidate)
                self.assert_error(lint_artifacts([self.write(malformed)]))

    def test_duplicate_artifact_ids_across_files_are_errors(self):
        paths = [self.write(name="first.md"), self.write(name="second.md")]
        self.assert_error(lint_artifacts(paths))

    def test_repeated_inputs_do_not_count_the_same_document_twice(self):
        path = self.write()
        result = lint_artifacts([path, path, self.root])
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["artifacts"], 1)

    def test_empty_directory_and_explicit_nonmarkdown_input_fail(self):
        empty = self.root / "empty"
        empty.mkdir()
        self.assert_error(lint_artifacts([empty]))
        unsupported = self.root / "note.txt"
        unsupported.write_text(self.sample, encoding="utf-8")
        self.assert_error(lint_artifacts([unsupported]))

    def test_directory_ignores_nonmarkdown_files_and_scans_nested_artifacts(self):
        self.write(name="nested/requirement.md")
        (self.root / "note.txt").write_text("This is not an artifact.", encoding="utf-8")
        result = lint_artifacts([self.root])
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["artifacts"], 1)

    def test_directory_symlink_cannot_expand_the_selected_read_scope(self):
        selected = self.root / "selected"
        selected.mkdir()
        self.write(name="selected/inside.md")
        outside = self.write(self.sample.replace("SAMPLE-REQ-001", "SAMPLE-REQ-999"), "outside.md")
        (selected / "escaped.md").symlink_to(outside)
        result = lint_artifacts([selected])
        self.assert_error(result)
        self.assertEqual(result["artifacts"], 1)

    def test_missing_path_and_oversize_artifact_return_findings(self):
        self.assert_error(lint_artifacts([self.root / "missing.md"]))
        path = self.root / "oversize.md"
        path.write_bytes(b"x" * (1024 * 1024 + 1))
        self.assert_error(lint_artifacts([path]))

    def test_results_are_deterministic_and_inputs_remain_unchanged(self):
        first = self.write(name="a.md")
        second = self.write(self.sample.replace("SAMPLE-REQ-001", "SAMPLE-REQ-002"), "b.md")
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in (first, second)}
        result = lint_artifacts([second, first])
        self.assertEqual(result, lint_artifacts([first, second]))
        self.assertEqual(set(self.root.rglob("*")), set(before))
        for path, (content, modified) in before.items():
            self.assertEqual(path.read_bytes(), content)
            self.assertEqual(path.stat().st_mtime_ns, modified)

    def test_exported_schema_validates_the_metadata_and_sections_projection(self):
        schema = artifact_schema()
        Draft202012Validator.check_schema(schema)
        _, metadata, body = self.sample.split("---", 2)
        sections = {}
        for match in re.finditer(r"(?ms)^## ([^\n]+)\n(.*?)(?=^## |\Z)", body):
            sections[match.group(1)] = match.group(2).strip()
        projection = {"metadata": yaml.safe_load(metadata), "sections": sections}
        errors = list(Draft202012Validator(schema).iter_errors(projection))
        self.assertEqual(errors, [])
        incomplete = deepcopy(projection)
        del incomplete["sections"]["Description"]
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(incomplete)))

    def test_canonical_and_shipped_reference_schemas_match(self):
        expected = artifact_schema()
        canonical = ROOT / "core/schemas/sdlc-artifact.schema.json"
        reference = CATALOG / "sdlc-artifact.schema.json"
        self.assertEqual(json.loads(canonical.read_text(encoding="utf-8")), expected)
        self.assertEqual(json.loads(reference.read_text(encoding="utf-8")), expected)

    def test_cli_lints_without_loading_a_workspace_or_providers(self):
        path = self.write()
        output = io.StringIO()
        with patch("ai_sdlc_workbench.cli.Workbench", side_effect=AssertionError("Unexpected workspace loading")):
            with redirect_stdout(output):
                result = main(["--workspace", str(self.root / "no-workspace"), "lint", str(path)])
        self.assertEqual(result, 0, output.getvalue())
        self.assertTrue(json.loads(output.getvalue())["valid"])

    def test_cli_returns_failure_for_invalid_artifact_and_for_strict_warnings(self):
        path = self.write()
        for arguments in (["lint", str(path), "--strict"],
                          ["lint", str(self.write("# No frontmatter\n", "invalid.md"))]):
            with self.subTest(arguments=arguments):
                output = io.StringIO()
                with redirect_stdout(output):
                    result = main(arguments)
                self.assertEqual(result, 1)
                self.assertFalse(json.loads(output.getvalue())["valid"])

    def test_cli_schema_export_matches_the_public_api(self):
        output = io.StringIO()
        with patch("ai_sdlc_workbench.cli.Workbench", side_effect=AssertionError("Unexpected workspace loading")):
            with redirect_stdout(output):
                result = main(["lint", "--print-schema"])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output.getvalue()), artifact_schema())

    def test_cli_rejects_missing_inputs_and_schema_export_mixed_with_artifacts(self):
        path = self.write()
        for arguments in (["lint"], ["lint", "--print-schema", str(path)]):
            with self.subTest(arguments=arguments):
                output = io.StringIO()
                try:
                    with redirect_stdout(output):
                        result = main(arguments)
                except SystemExit as error:
                    result = error.code
                self.assertNotEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
