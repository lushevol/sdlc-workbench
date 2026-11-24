"""Behavior checks for detailed permission reports from retained results."""
from __future__ import annotations

from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest

from ai_sdlc_workbench import coverage_reporting as report
from ai_sdlc_workbench.entitlement_reconciliation import compare_sets


class _HTML(HTMLParser):
    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.text, self.ids, self.links = [], [], []
        self.feed(value)

    def handle_data(self, data):
        self.text.append(data)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs["href"])


def _comparison(old, new):
    return compare_sets(old, new)


def _fixture(ces=False):
    user = {"user_id": "person-a", "status": "DIFFERENT", "at": "2026-11-03T10:00:00Z", "errors": [],
            "effective": _comparison([["APP", "Ledger", "View"], ["APP", "Audit", "View"]],
                                     [["APP", "Ledger", "View"], ["APP", "Payment", "Edit"], ["APP", "Payment", "Approve"]]),
            "assignments": _comparison([["APP", "Reader"]], [["APP", "Operator"]]),
            "profile_grants": _comparison([["APP", "Reader", "Ledger", "View"]], [["APP", "Operator", "Ledger", "View"]]),
            "role_evidence": "Inspected permission rows", "exact_full_profile_status": "UNASSESSED",
            "data_scope": {"status": "UNASSESSED", "reason": "EMS2 fields unavailable"}}
    if ces:
        entitlements = {
            "profile_grants": _comparison([["APP", "Reader", "Ledger", "View"], ["APP", "Reader", "Audit", "View"]],
                                          [["APP", "Reader", "Ledger", "View"], ["APP", "Reader", "Payment", "Edit"]]),
            "profile_names": _comparison([["APP", "Reader"], ["APP", "Empty"]], [["APP", "Reader"]]),
            "subjects": _comparison([["APP", "Ledger"], ["APP", "Audit"]], [["APP", "Ledger"], ["APP", "Payment"]]),
            "matrix_limits": [[["APP", "Empty"]]],
            "live_inventories": [{"entity": "SOURCE", "kind": "roles", "status": "UNASSESSED", "error": {"code": "REPLAY_NOT_CAPTURED"}}]}
        user["data_scope"]["ces"] = [{"data_entitlements": [{"key": "Booking.Entity", "values": ["Entity-A", "Entity-B"]}]}]
    else:
        subjects = _comparison([["APP", "Ledger"]], [["APP", "Ledger"], ["APP", "Payment"]])
        subjects.update(complete=False, status="UNASSESSED", unassessed_entities=["OTHER"], coverage_percent=None)
        entitlements = {"subjects": subjects, "roles": _comparison([["APP", "Reader"]], [["APP", "Reader"], ["APP", "Operator"]]),
                        "inventories": [{"entity": "APP", "kind": "subjects", "status": "DIFFERENT", "errors": [], "comparison": _comparison([["APP", "Ledger"]], [["APP", "Ledger"], ["APP", "Payment"]])},
                                        {"entity": "OTHER", "kind": "subjects", "status": "UNASSESSED", "errors": [{"source": "prod", "code": "REPLAY_NOT_CAPTURED"}]}]}
    result = {"schema_version": 1, "scope": "Declared fixture scope", "mode": "replay", "evidence_source": "MOCK: supplied API responses",
              "status": "INCOMPLETE", "conclusion": "Captured sample differs; complete coverage remains unknown.",
              "started_at": "2026-11-03T10:00:00Z", "finished_at": "2026-11-03T10:01:00Z",
              "summary": {"discovered_accounts": 3, "baseline_accounts": 2, "compared_accounts": 1, "matching_accounts": 0,
                          "different_accounts": 1, "unassessed_accounts": 2, "functional_profile_coverage_percent": None,
                          "full_data_profile_coverage": "UNASSESSED", "subject_coverage": "Partial", "role_grant_preservation": "Partial"},
              "inventory": {"users": ["person-a", "person-b", "person-c"], "baseline_users": ["person-a", "person-b"], "source": "Matrix and declared examples"},
              "users": [user, {"user_id": "person-b", "status": "UNASSESSED", "errors": [{"source": "uat", "code": "ACCOUNT_CONTEXT_MISMATCH", "http_status": None}]}],
              "entitlements": entitlements, "excluded": [{"name": "UNLAUNCHED", "priority": "LOW", "reason": "No current assignments"}],
              "limits": ["No complete directory supplied"], "errors": [], "binding": {"config_sha256": "a" * 64, "implementation_sha256": {"source.py": "b" * 64}, "replay_sha256": {"supplied.yml": "c" * 64}}}
    if not ces:
        result["direction"] = {"baseline": "EMS2 PROD", "target": "EMS2 UAT"}
    return result


class DetailedCoverageReportTests(unittest.TestCase):
    def test_both_formats_show_direction_rates_and_exact_difference_rows(self):
        """Given unequal paired permission sets and an incomplete inventory
        When detailed Markdown and HTML render
        Then both formats retain every gap and separate both directional rates
        """
        result = _fixture()
        markdown, html = report.render_markdown(result), report.render_html(result)
        plain = " ".join(_HTML(html).text)
        for text in ("PROD is the baseline", "EMS2 PROD only", "EMS2 UAT only", "1/2 (50.00%)", "1/3 (33.33%)",
                     "Audit", "Payment", "Approve", "Operator", "Partial comparison", "Complete EMS2 role definitions are unavailable"):
            self.assertIn(text, plain)
            self.assertIn(text, markdown)
        self.assertIn("UNASSESSED", markdown)
        self.assertNotIn("<pre>", html)

    def test_ces_report_preserves_definitions_by_role_and_observed_data_values(self):
        """Given matrix definitions, unmatched roles, and target data restrictions
        When the migration report renders
        Then all tuples and values remain visible without claiming full data equality
        """
        result = _fixture(ces=True)
        markdown = report.render_markdown(result)
        html = report.render_html(result)
        plain = " ".join(_HTML(html).text)
        for text in ("Definition comparison by role / entitlement", "Matrix role / feature / action definitions",
                     "UNASSESSED: no baseline matrix content", "Empty", "Booking.Entity", "Entity-A", "Entity-B",
                     "Full data-profile equality", "Matched: Matrix role / feature / action definitions"):
            self.assertIn(text, plain)
            self.assertIn(text, markdown)
        for category in ("missing", "additional", "matched"):
            for row in result["entitlements"]["profile_grants"][category]:
                self.assertIn("| " + " | ".join(row) + " |", markdown)
        self.assertIn("No comparable complete EMS2 field/value definition was supplied", plain)

    def test_ces_inventory_consistency_does_not_mislabel_matrix_omissions_as_ces_gaps(self):
        """Given an EMS2 API role name absent from the supplied matrix
        When the migration report explains source-consistency differences
        Then the omission targets the matrix and remains separate from CES catalog gaps
        """
        result = _fixture(ces=True)
        result["entitlements"]["live_inventories"] = [{"entity": "SOURCE", "kind": "roles",
            "comparison": _comparison([["EMS2_ADMIN"], ["Reader"]], [["Reader"]])}]
        markdown = report.render_markdown(result)
        plain = " ".join(_HTML(report.render_html(result)).text)
        for text in ("EMS2 API inventory", "Supplied matrix", "EMS2 API inventory only — absent from Supplied matrix"):
            self.assertIn(text, markdown)
            self.assertIn(text, plain)
        self.assertIn("do not compare EMS2 inventories with CES", plain)

    def test_every_unassessed_account_and_exact_failure_reason_is_reported(self):
        """Given discovered accounts with missing and wrong-context captures
        When reports render a complete unassessed register
        Then no account is omitted and unavailable content cannot become a match
        """
        result = _fixture()
        extra = ["pending-" + str(i) for i in range(1200)]
        result["inventory"]["users"].extend(extra)
        result["summary"]["discovered_accounts"] += len(extra)
        result["summary"]["unassessed_accounts"] += len(extra)
        markdown, html = report.render_markdown(result), report.render_html(result)
        for account in ["person-b", "person-c"] + extra:
            self.assertIn(account, markdown)
            self.assertIn(account, html)
        self.assertIn(r"ACCOUNT\_CONTEXT\_MISMATCH", markdown)
        self.assertIn(r"NOT\_FETCHED", markdown)
        self.assertIn("Complete unassessed account register (1202)", markdown)
        self.assertIn("1201", markdown)

    def test_source_values_are_escaped_in_both_formats_and_cannot_create_links(self):
        """Given malicious-looking account names, source labels, and policy values
        When reports render these values
        Then they stay plain text and cannot inject markup or executable links
        """
        result = _fixture()
        payload = '<img src=x onerror="alert(1)">[bad](javascript:alert(2))|line\nnext'
        result["users"][0]["user_id"] = payload
        result["binding"]["replay_sha256"] = {payload: "sha"}
        result["users"][0]["data_scope"]["value"] = payload
        markdown, html = report.render_markdown(result), report.render_html(result)
        self.assertNotIn("<img", html)
        self.assertNotIn("<img", markdown)
        parsed = _HTML(html)
        self.assertTrue(all("javascript:" not in link for link in parsed.links))
        self.assertIn("&lt;img", html)
        self.assertIn(r"\[bad\](javascript:alert(2))\|line<br>next", markdown)
        self.assertNotIn("[bad](javascript:", markdown)

    def test_fragments_prefix_ids_and_rebase_only_generated_evidence_links(self):
        """Given two detailed comparisons embedded in one suite
        When HTML fragments and Markdown use distinct output prefixes
        Then anchors remain unique and all generated evidence links target their child
        """
        result = _fixture()
        left = report.render_fragment(result, prefix="first-", link_prefix="first/")
        right = report.render_fragment(result, prefix="second-", link_prefix="second/")
        parsed = _HTML(left + right)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertIn("#first-entitlements", parsed.links)
        self.assertIn("first/result.json", parsed.links)
        self.assertIn("second/report.md", parsed.links)
        markdown = report.render_markdown(result, prefix="first-", link_prefix="first/", heading_offset=2)
        self.assertFalse(markdown.startswith("---"))
        self.assertIn("(first/differences.csv)", markdown)
        self.assertIn("(#first-entitlements)", markdown)
        with self.assertRaises(ValueError):
            report.render_fragment(result, prefix='"><script>')
        with self.assertRaises(ValueError):
            report.render_fragment(result, link_prefix="javascript:alert(1)")
        with self.assertRaises(ValueError):
            report.render_fragment(result, link_prefix="../other/")

    def test_empty_or_unavailable_denominators_do_not_render_passing_rates(self):
        """Given an empty account population and unavailable inventories
        When reports calculate display rates
        Then empty denominators remain unassessed and no 100 percent rate appears
        """
        result = _fixture()
        result["users"] = []
        result["inventory"] = {"users": [], "baseline_users": []}
        result["entitlements"] = {"inventories": []}
        result["summary"] = {"discovered_accounts": 0, "baseline_accounts": 0, "compared_accounts": 0,
                             "matching_accounts": 0, "different_accounts": 0, "unassessed_accounts": 0,
                             "functional_profile_coverage_percent": None}
        markdown, html = report.render_markdown(result), report.render_html(result)
        self.assertIn("UNASSESSED (empty or unavailable denominator)", markdown)
        self.assertNotIn("100.00%", markdown)
        self.assertNotIn("100.00%", html)
        self.assertIn("No paired account responses were assessed", markdown)

    def test_writer_keeps_results_unchanged_and_links_sanitized_response_files(self):
        """Given a retained comparison result and sanitized response receipt
        When the writer generates both artifacts
        Then it preserves result semantics and links the hash-named response evidence
        """
        result = _fixture()
        before = deepcopy(result)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / "responses").mkdir()
            filename = "d" * 64 + ".json"
            (path / "responses" / filename).write_text(json.dumps({"source": "supplied.yml", "source_sha256": "e" * 64,
                                                                  "data_sha256": "f" * 64, "at": "2026-11-03"}))
            (path / "responses" / "unsafe.json").write_text("{}")
            report.write_report(result, path)
            self.assertEqual((path / "report.md").read_text(), report.render_markdown(result, path))
            self.assertEqual((path / "report.html").read_text(), report.render_html(result, path))
            parsed = _HTML((path / "report.html").read_text())
            self.assertIn("responses/" + filename, parsed.links)
            self.assertNotIn("responses/unsafe.json", parsed.links)
            self.assertEqual(result, before)
            self.assertIn("automated_check: NOT_RUN", (path / "report.md").read_text())

    def test_matching_accounts_leave_active_differences_but_keep_appendix_and_source_warnings(self):
        """Given matching account content with one matrix inconsistency
        When the active difference list and complete appendix render
        Then only the source-warning account stays active while matched accounts remain retained
        """
        result = _fixture(ces=True)
        matched = deepcopy(result["users"][0])
        matched["user_id"], matched["status"] = "matched-a", "MATCH"
        warning = deepcopy(matched)
        warning["user_id"] = "warning-b"
        warning["matrix_assignment_comparison"] = _comparison([], [["APP", "Reader"]])
        result["users"] = [matched, warning]
        result["inventory"]["users"] = ["matched-a", "warning-b"]
        html = report.render_html(result)
        active = html.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
        self.assertNotIn("<td>matched-a</td>", active)
        self.assertIn("<td>warning-b</td>", active)
        self.assertIn("matrix_assignment_comparison", active)
        self.assertIn('data-user-id="warning-b"', html)
        self.assertIn('data-user-id="matched-a"', html)
        appendix = html.split('id="account-register"', 1)[1]
        self.assertIn("<td>matched-a</td>", appendix)

    def test_matched_user_appendices_keep_account_ownership_for_search_and_status_filters(self):
        """Given matched permission rows retained outside each primary user detail
        When HTML exposes those appendices to its shared search and status controls
        Then every user appendix carries the same explicit account identity and status
        """
        result = _fixture(ces=True)
        matched = deepcopy(result["users"][0])
        matched["user_id"], matched["status"] = "matched-person", "MATCH"
        result["users"].append(matched)
        result["inventory"]["users"].append("matched-person")

        class AppendixOwners(HTMLParser):
            def __init__(self, value):
                super().__init__()
                self.stack, self.summaries, self.in_summary = [], [], False
                self.feed(value)

            def handle_starttag(self, tag, attrs):
                if tag == "details":
                    self.stack.append(dict(attrs))
                if tag == "summary":
                    self.in_summary = True

            def handle_endtag(self, tag):
                if tag == "details":
                    self.stack.pop()
                if tag == "summary":
                    self.in_summary = False

            def handle_data(self, data):
                if self.in_summary and self.stack and data.startswith("Matched:"):
                    self.summaries.append((data, self.stack[-1]))

        parser = AppendixOwners(report.render_html(result))
        account_appendices = [(title, attrs) for title, attrs in parser.summaries if title.startswith("Matched: Account ")]
        self.assertEqual(len(account_appendices), 2)
        for title, attrs in account_appendices:
            expected = "matched-person" if "matched-person" in title else "person-a"
            self.assertIn("data-user-record", attrs)
            self.assertEqual(attrs["data-user-id"], expected)
            self.assertEqual(attrs["data-user-status"], "MATCH" if expected == "matched-person" else "DIFFERENT")
        global_appendices = [(title, attrs) for title, attrs in parser.summaries if not title.startswith("Matched: Account ")]
        self.assertTrue(global_appendices)
        self.assertTrue(all("data-user-id" not in attrs for _, attrs in global_appendices))


if __name__ == "__main__":
    unittest.main()
