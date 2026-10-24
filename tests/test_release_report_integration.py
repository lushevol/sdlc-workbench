"""Verify the public report API against loopback ADO and Sonar services.

Canonical cases: docs/RELEASE_REPORT_REPRODUCTION.md RR-1 through RR-8;
docs/RELEASE_REPORT_API_DESIGN.md RR-P1 through RR-P6.
These tests use actual connector HTTP reads. No target environment is contacted.
"""
from __future__ import annotations

from collections import Counter
from contextlib import redirect_stdout
import io
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch

from release_report_mock import (CANDIDATE, MockReleaseService,
                                 safe_environment, write_mock_workspace)


@unittest.skipUnless(shutil.which("node"), "Release report integration requires the optional Node connector runtime")
class ReleaseReportIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="release-report-mock-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        self.environment = patch.dict(os.environ, safe_environment(), clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def fixture(self, **options):
        service = MockReleaseService(**options)
        service.__enter__()
        self.addCleanup(service.__exit__, None, None, None)
        write_mock_workspace(self.root, service)
        return service

    def collect(self, **options):
        from ai_sdlc_workbench.release_report import collect_release_report
        from ai_sdlc_workbench.release_report_contract import read_release_report
        result = collect_release_report(501, self.root, **options)
        self.assertIn("manifest_path", result, result)
        manifest = Path(result["manifest_path"])
        self.assertTrue(manifest.is_file(), result)
        snapshot = read_release_report(manifest)
        return result, snapshot, manifest

    def test_complete_release_collection_and_offline_render(self):
        """RR-4/6/7: Given one release ID, collect all records, then render without HTTP or Clinic writes."""
        service = self.fixture(delay=0.01)
        clinic = self.root / ".workbench/release-clinic/reports/TDAReport_LOCAL_501.html"
        clinic.parent.mkdir(parents=True)
        clinic.write_bytes(b"<!doctype html><p>Independently generated Clinic content</p>")
        clinic_before = clinic.read_bytes()
        result, snapshot, manifest = self.collect()
        self.assertEqual(result["status"], "SUCCEEDED", result)
        self.assertEqual(snapshot["collection_status"], "complete", snapshot.get("errors"))
        self.assertEqual(int(snapshot["source"]["release_id"]), 501)
        self.assertEqual(snapshot["release"]["fields"]["Custom.UnmappedEvidence"], "Preserve this custom field")
        self.assertEqual({int(b["id"]) for b in snapshot["builds"]}, {101, 102})
        for build in snapshot["builds"]:
            self.assertTrue(build["build"]["fixtureExtra"]["rawBuildRetained"])
            self.assertEqual(build["build"]["sourceVersion"], CANDIDATE)
            self.assertIn("production", build["comparisons"])
        items = {int(w["id"]): w for w in snapshot["workitems"]}
        self.assertTrue({201, 301, 401}.issubset(items))
        self.assertEqual(items[201]["fields"]["Microsoft.VSTS.Common.AcceptanceCriteria"], "Assertion 201")
        text = json.dumps(snapshot)
        self.assertIn("fixture-101", text)
        self.assertIn("fixture-102", text)
        self.assertIn('"testRunId": "901"', text)
        self.assertIn('"testRunId": "902"', text)
        counts = {int(report["build_id"]): report["requirementCoverages"][0]["testExecutionStatusStats"]["countByType"]
                  for report in snapshot["tests"]}
        self.assertEqual((counts[101]["PASSED"], counts[101]["FAILED"]), (3, 1))
        self.assertEqual((counts[102]["PASSED"], counts[102]["FAILED"]), (2, 2))
        self.assertEqual(snapshot["test_aggregation"]["status"], "not_configured")
        self.assertEqual(snapshot["test_aggregation"]["scope"], "build_specific")
        self.assertIn("issues-1", text)
        self.assertIn("issues-2", text)
        self.assertIn("hotspots-2", text)
        self.assertTrue(snapshot["graph"]["nodes"])
        self.assertTrue(snapshot["graph"]["edges"])
        self.assertTrue(any(node["type"] == "file" for node in snapshot["graph"]["nodes"]))
        self.assertTrue(any(request["path"].endswith("/items") for request in service.requests))
        self.assertEqual(snapshot["compliance"]["status"], "available")
        self.assertIn(service.url + "/attachments/clinic-501", json.dumps(snapshot["compliance"]))
        self.assertEqual(service.counts["GET /attachments/clinic-501"], 0,
                         "Compliance HTML must be linked, not fetched or parsed")
        self.assertLessEqual(service.peak["ado"], 6)
        self.assertLessEqual(service.peak["sonar"], 2)
        self.assertGreater(service.peak["ado"], 1, "Fixture must exercise concurrent HTTP reads")
        self.assertEqual(snapshot["metrics"]["sessions"], {"ado": 1, "sonar": 1})
        self.assertEqual(snapshot["metrics"]["requests"], len(service.requests))
        for source in snapshot["metrics"]["sources"].values():
            self.assertEqual(source["client_creations"], 1)
        timelines = [r for r in service.requests if r["path"].endswith("/timeline")]
        self.assertEqual(len(timelines), 2, "Each identified build needs one shared timeline read")
        comparisons = [r for r in service.requests if r["path"].endswith("/diffs/commits")]
        pairs = [(r["query"]["baseVersion"][0], r["query"]["targetVersion"][0]) for r in comparisons]
        self.assertEqual(len(pairs), len(set(pairs)), "Identical comparison requests must be shared")
        before_requests = len(service.requests)
        from ai_sdlc_workbench.release_report_render import render_release_report
        html_path = render_release_report(manifest, self.root / "rendered/report.html")
        first = Path(html_path).read_bytes()
        second_path = render_release_report(manifest, self.root / "rendered/report.html")
        self.assertEqual(Path(second_path).read_bytes(), first)
        self.assertEqual(len(service.requests), before_requests)
        self.assertEqual(clinic.read_bytes(), clinic_before)
        self.assertIn(b"TDAReport_STREAM_501.html", first)
        self.assertIn(b"Fixture release", first)
        self.assertNotIn(b"fixture-ado-token", first)
        self.assertNotIn(b"fixture-sonar-token", first)
        self.assertNotIn(b"Independently generated Clinic content", first,
                         "Separate Clinic content must not be copied into the release report")

    def test_commit_changes_and_comparisons_preserve_server_capped_pages(self):
        """Given two server-capped change pages, collection retains both files and complete comparison results."""
        service = self.fixture(paged_changes=True)
        _, snapshot, _ = self.collect()
        expected = {"/src/settlement.py", "/src/validation.py"}
        file_nodes = {node["path"] for node in snapshot["graph"]["nodes"] if node["type"] == "file"}
        self.assertTrue(expected.issubset(file_nodes), file_nodes)
        file_reads = {request["query"]["path"][0] for request in service.requests
                      if request["path"].endswith("/items")}
        self.assertTrue(expected.issubset(file_reads))
        for build in snapshot["builds"]:
            for comparison in build["comparisons"].values():
                if not comparison or comparison.get("status") == "unavailable":
                    continue
                self.assertTrue(comparison.get("allChangesIncluded"), comparison)
                self.assertEqual({change["item"]["path"] for change in comparison["changes"]}, expected)
        pages = [request for request in service.requests if request["path"].endswith("/changes")]
        self.assertTrue(any(request["query"].get("skip") == ["1"] for request in pages), pages)

    def test_missing_build_remains_in_partial_report(self):
        """RR-1: Given inaccessible build102, collection retains both identities and marks the missing read."""
        self.fixture(forbidden_build=102)
        result, snapshot, _ = self.collect()
        self.assertEqual(snapshot["collection_status"], "partial")
        entries = {int(b["id"]): b for b in snapshot["builds"]}
        self.assertEqual(set(entries), {101, 102})
        self.assertNotEqual(entries[102]["status"], "complete")
        self.assertTrue(snapshot["errors"])
        self.assertIn(entries[101]["status"], {"complete", "partial"})

    def test_missing_clinic_link_does_not_remove_release_information(self):
        """RR-8: Given no Clinic document, rendering states unavailable and keeps successful release data."""
        self.fixture(no_clinic=True)
        _, snapshot, manifest = self.collect()
        self.assertEqual(snapshot["compliance"]["status"], "unavailable")
        self.assertEqual(len(snapshot["builds"]), 2)
        self.assertTrue(snapshot["workitems"])
        from ai_sdlc_workbench.release_report_render import render_release_report
        target = render_release_report(manifest, self.root / "report.html")
        self.assertIn("Release Clinic report unavailable", Path(target).read_text())

    def test_work_item_reads_batch_401_unique_ids(self):
        """RR-P1: Given 401 unique related IDs, exactly three detail batches preserve all 401 records."""
        service = self.fixture(related_count=401, duplicate_relations=99)
        _, snapshot, _ = self.collect()
        batches = [r["body"]["ids"] for r in service.requests
                   if r["path"].endswith("/workitemsbatch") and r.get("body", {}).get("ids") != [501]]
        self.assertEqual(len(batches), 3, batches)
        self.assertTrue(all(0 < len(batch) <= 200 for batch in batches))
        all_ids = [int(i) for batch in batches for i in batch]
        self.assertEqual(set(all_ids), set(service.related_ids()))
        self.assertTrue(all(n == 1 for n in Counter(all_ids).values()))
        self.assertEqual({int(w["id"]) for w in snapshot["workitems"]}, set(service.related_ids()))

    def test_graph_discovered_story_traverses_test_relations(self):
        """Scenario: Traverse tests from a commit-linked story.

        Given commit evidence links story 601 outside the release relations
        And story 601 has a TestedBy-Forward relation to test case 701
        When the release report is collected
        Then both work items and both graph relationships are retained
        """
        self.fixture(graph_extra_workitems=True)
        _, snapshot, _ = self.collect()
        self.assertEqual(snapshot["collection_status"], "complete", snapshot["errors"])
        items = {int(item["id"]): item for item in snapshot["workitems"]}
        self.assertIn(601, items)
        self.assertIn(701, items, "Relations from graph-discovered work items must also be traversed")
        self.assertEqual(items[701]["fields"]["System.WorkItemType"], "Test Case")
        nodes = {node["id"]: node for node in snapshot["graph"]["nodes"]}
        self.assertEqual(nodes["wi:601"]["type"], "story")
        self.assertEqual(nodes["wi:701"]["type"], "testCase")
        edges = {(edge["from"], edge["to"], edge["type"]) for edge in snapshot["graph"]["edges"]}
        self.assertIn((f"commit:r1:{CANDIDATE}", "wi:601", "implements"), edges)
        self.assertIn(("wi:601", "wi:701", "testedBy"), edges)

    def test_serial_and_scheduled_collection_preserve_equivalent_coverage(self):
        """Scenario: Compare serial and scheduled reads with equal fixture delays.

        Given the same release fixture delays each HTTP response by 10 milliseconds
        When one collection uses one ADO request and one Sonar request at a time
        And another collection uses six ADO requests and two Sonar requests at a time
        Then both snapshots retain equal report data and request counts
        And both runs reuse one client and session per source
        And observed concurrency stays within each configured limit
        """
        service = self.fixture(delay=0.01)
        write_mock_workspace(self.root, service, ado_concurrency=1, sonar_concurrency=1)
        _, serial, _ = self.collect()
        serial_count, serial_peak = len(service.requests), dict(service.peak)
        service.reset_requests()
        write_mock_workspace(self.root, service, ado_concurrency=6, sonar_concurrency=2)
        _, scheduled, _ = self.collect()
        variable = {"generated_at", "metrics", "evidence"}
        self.assertEqual({key: value for key, value in serial.items() if key not in variable},
                         {key: value for key, value in scheduled.items() if key not in variable})
        self.assertEqual(serial["collection_status"], "complete", serial["errors"])
        self.assertEqual(scheduled["collection_status"], "complete", scheduled["errors"])
        self.assertEqual(serial_count, len(service.requests))
        self.assertEqual(serial_peak, {"ado": 1, "sonar": 1})
        self.assertGreater(service.peak["ado"], 1)
        self.assertLessEqual(service.peak["ado"], 6)
        self.assertLessEqual(service.peak["sonar"], 2)
        for snapshot in (serial, scheduled):
            self.assertEqual(snapshot["metrics"]["sessions"], {"ado": 1, "sonar": 1})
            for source in snapshot["metrics"]["sources"].values():
                self.assertEqual(source["client_creations"], 1)
        self.benchmark_record = {
            "fixture_delay_seconds": 0.01,
            "coverage_equal": True,
            "serial": {"metrics": serial["metrics"], "observed_peak": serial_peak,
                       "request_count": serial_count},
            "scheduled": {"metrics": scheduled["metrics"], "observed_peak": dict(service.peak),
                          "request_count": len(service.requests)},
            "limitations": ["Synthetic loopback measurements do not establish live endpoint latency or speedup."]}

    def test_sonar_later_page_failure_keeps_evidence_and_partial_section(self):
        """Scenario: Retain successful pages after a Sonar issue page is denied.

        Given issue page one succeeds and issue page two returns HTTP 403
        When the release report is collected
        Then page-one issues remain in the snapshot and hashed evidence
        And the report and Sonar section have partial status
        And complete hotspot results remain available
        """
        service = self.fixture(sonar_issues_second_page_failure=True)
        _, snapshot, manifest_path = self.collect()
        self.assertEqual(snapshot["collection_status"], "partial")
        self.assertTrue(snapshot["errors"])
        for sonar in snapshot["sonarqube"]:
            self.assertEqual(sonar["status"], "partial", sonar)
            self.assertEqual({issue["key"] for issue in sonar["issues"]}, {"issues-1"})
            self.assertEqual({hotspot["key"] for hotspot in sonar["hotspots"]}, {"hotspots-1", "hotspots-2"})
        manifest = json.loads(manifest_path.read_text())
        issue_evidence = [item for item in manifest["evidence"] if item.get("tool") == "report_sonar_issues"]
        self.assertTrue(issue_evidence)
        retained = b"\n".join((manifest_path.parent / item["path"]).read_bytes() for item in issue_evidence)
        self.assertIn(b"issues-1", retained)
        issue_requests = [request for request in service.requests if request["path"] == "/api/issues/search"]
        self.assertEqual([request["query"]["p"][0] for request in issue_requests], ["1", "2"])

    def test_large_test_attachments_are_complete_and_hash_bound(self):
        """RR-P5: Given 5 MiB padding, streamed attachment bytes survive small manifest responses and hashing."""
        service = self.fixture(attachment_padding=5 * 1024 * 1024)
        _, snapshot, manifest_path = self.collect()
        manifest = json.loads(manifest_path.read_text())
        artifacts = manifest.get("evidence", snapshot.get("evidence", []))
        large = [a for a in artifacts if a.get("bytes", 0) > 5 * 1024 * 1024]
        self.assertTrue(large, "Large attachment artifacts must be retained and indexed")
        for item in large:
            data = (manifest_path.parent / item["path"]).read_bytes()
            self.assertEqual(len(data), item["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
        self.assertIn("fixture-101", json.dumps(snapshot))
        self.assertIn("fixture-102", json.dumps(snapshot))
        self.assertLess(manifest_path.stat().st_size, 4 * 1024 * 1024)
        self.assertEqual(sum(1 for r in service.requests if "/attachments/test.report/rtm.json" in r["path"]), 2)

    def test_ungranted_coverage_read_makes_zero_network_requests(self):
        """RR-P4: Given coverage is ungranted, collect partial evidence without any coverage HTTP request."""
        service = self.fixture()
        write_mock_workspace(self.root, service, denied_tools=["report_coverage"])
        _, snapshot, _ = self.collect()
        self.assertEqual(service.counts["GET /Project/_apis/test/codecoverage"], 0)
        self.assertEqual(snapshot["collection_status"], "partial")
        self.assertIn("TOOL_NOT_GRANTED", json.dumps(snapshot))

    def test_successful_retry_after_response_is_paced_without_replay(self):
        """RR-P3: Given HTTP200 Retry-After, retain success and delay the next request without replay."""
        service = self.fixture()
        service.throttle_once["/_apis/wit/workitemsbatch"] = "0.1"
        _, snapshot, _ = self.collect()
        self.assertEqual(snapshot["collection_status"], "complete", snapshot["errors"])
        first = service.requests[0]
        next_ado = next(r for r in service.requests[1:] if r["connector"] == "ado")
        self.assertGreaterEqual(next_ado["at"] - first["at"], 0.09)
        initial_reads = [r for r in service.requests if r["path"] == "/_apis/wit/workitemsbatch"]
        # A final release revision recheck is permitted; the successful first response is not a retry.
        self.assertLessEqual(len(initial_reads), 2)
        self.assertNotIn("HTTP_429", json.dumps(snapshot))

    def test_transient_http_failure_retries_without_losing_build_evidence(self):
        """Given one HTTP503, when collecting, retry the read and retain complete build properties."""
        service = self.fixture()
        path = "/Project/_apis/build/builds/101/properties"
        service.failure_once[path] = 503
        _, snapshot, _ = self.collect()
        self.assertEqual(snapshot["collection_status"], "complete", snapshot["errors"])
        self.assertEqual(service.counts["GET " + path], 2)
        self.assertIn("quality-r1", json.dumps(snapshot))

    def test_unavailable_production_baseline_never_becomes_passed(self):
        """RR-2: Given no qualifying production run, preserve explicit unavailability instead of a passed comparison."""
        self.fixture(no_production=True)
        _, snapshot, _ = self.collect()
        for build in snapshot["builds"]:
            baseline = build["baseline"]
            comparison = build["comparisons"]["production"]
            self.assertIsNone(baseline["selected"])
            self.assertEqual(comparison["status"], "unavailable")
            self.assertTrue(comparison["reason"])
        self.assertTrue(snapshot["warnings"] or snapshot["errors"])

    def test_missing_branch_refs_remain_unavailable(self):
        """Given missing refs, collection retains unavailable branch comparisons instead of successful defaults."""
        self.fixture(no_branch_refs=True)
        _, snapshot, _ = self.collect()
        for build in snapshot["builds"]:
            for name in ("branch", "main"):
                self.assertEqual(build["comparisons"][name]["status"], "unavailable")
        self.assertTrue(snapshot["errors"] or snapshot["warnings"])

    def test_unsupported_coverage_preserves_raw_evidence_and_unknown_values(self):
        """Given unsupported coverage bytes, preserve raw evidence and mark coverage unavailable without invented percentages."""
        self.fixture(unsupported_coverage=True)
        _, snapshot, _ = self.collect()
        for coverage in snapshot["coverage"]:
            self.assertEqual(coverage["summary"], {})
            self.assertIn(coverage["status"], {"unavailable", "partial"})
            self.assertIn("coverageFileUrl", json.dumps(coverage["raw"]))
        self.assertTrue(snapshot["warnings"] or snapshot["errors"])

    def test_cli_collect_render_and_verify_remain_separate(self):
        """Given a mock workspace, CLI collection creates evidence; render and verify require zero further HTTP reads."""
        service = self.fixture()
        from ai_sdlc_workbench.cli import main
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--workspace", str(self.root), "release-report", "collect", "501"])
        result = json.loads(output.getvalue())
        self.assertEqual(code, 0, result)
        manifest = result["manifest_path"]
        count = len(service.requests)
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--workspace", str(self.root), "release-report", "render", manifest,
                         "--output", "cli/report.html"])
        self.assertEqual(code, 0, output.getvalue())
        self.assertTrue((self.root / "cli/report.html").is_file())
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--workspace", str(self.root), "release-report", "verify", manifest])
        self.assertEqual(code, 0, output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["status"], "VALID")
        self.assertEqual(len(service.requests), count)

    def test_mcp_collect_and_parent_grant_denial(self):
        """Given a configured resource, MCP collects through the same API and denies removed parent grants before HTTP."""
        service = self.fixture()
        from ai_sdlc_workbench.mcp import McpServer
        from ai_sdlc_workbench.runtime import Workbench
        response = McpServer(Workbench(self.root)).call_tool("workbench_call", {
            "resource_id": "release-report", "operation": "collect", "arguments": {"release_id": 501}})
        self.assertFalse(response["isError"], response)
        action = response["structuredContent"]
        self.assertEqual(action["status"], "SUCCEEDED")
        self.assertTrue(Path(action["result"]["manifest_path"]).is_file())
        count = len(service.requests)
        configuration = write_mock_workspace(self.root, service)
        configuration["resources"][-1]["allowed_operations"] = []
        import yaml
        (self.root / "workspace.yaml").write_text(yaml.safe_dump(configuration), encoding="utf-8")
        denied = McpServer(Workbench(self.root)).call_tool("workbench_call", {
            "resource_id": "release-report", "operation": "collect", "arguments": {"release_id": 501}})
        self.assertTrue(denied["isError"])
        self.assertEqual(denied["structuredContent"]["status"], "DENIED")
        self.assertEqual(len(service.requests), count)

    def test_collection_deadline_retains_completed_evidence(self):
        """Given a short deadline, when reads exceed it, retain completed records in an explicit partial report."""
        service = self.fixture(delay=0.3)
        write_mock_workspace(self.root, service, collection_timeout_seconds=1)
        started = time.monotonic()
        _, snapshot, manifest_path = self.collect()
        self.assertLess(time.monotonic() - started, 5)
        self.assertIn(snapshot["collection_status"], {"partial", "failed"})
        self.assertEqual(snapshot["release"]["id"], 501)
        self.assertTrue(snapshot["errors"])
        manifest = json.loads(manifest_path.read_text())
        self.assertTrue(manifest["evidence"])
        for artifact in manifest["evidence"]:
            retained = manifest_path.parent / artifact["path"]
            self.assertTrue(retained.is_file())
            self.assertEqual(hashlib.sha256(retained.read_bytes()).hexdigest(), artifact["sha256"])

    def test_resume_detects_changed_release_revision(self):
        """RR-P6: Given a changed release revision, resumed collection cannot conceal mixed source identities."""
        service = self.fixture()
        _, first, manifest = self.collect()
        original_bytes = manifest.read_bytes()
        service.revision = 8
        _, resumed, resumed_manifest = self.collect(resume=manifest)
        self.assertEqual(manifest.read_bytes(), original_bytes, "A resume must preserve the original checkpoint")
        self.assertEqual(resumed["collection_status"], "partial")
        self.assertIn("RESUME_REVISION_CHANGED", {error["code"] for error in resumed["errors"]})
        self.assertEqual(resumed["resume"]["sha256"], hashlib.sha256(original_bytes).hexdigest())
        self.assertEqual(resumed["resume"]["revision"], 7)
        self.assertEqual(resumed["source"]["revision"], 8)
        self.assertEqual(resumed["release"]["rev"], 8)
        self.assertEqual(first["release"]["rev"], 7)


if __name__ == "__main__":
    unittest.main()
