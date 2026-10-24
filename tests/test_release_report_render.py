"""Verify offline report integrity, complete evidence access, and safe presentation."""

from copy import deepcopy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.release_report_contract import (
    artifact_record, read_release_report, validate_snapshot, write_report_snapshot,
)
from ai_sdlc_workbench.release_report_render import render_release_report


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag == "a":
            self.links.append(dict(attrs).get("href"))


class ReleaseReportRenderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="release-report-render-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.directory = self.root / "retained"
        self.directory.mkdir()
        (self.directory / "evidence").mkdir()
        self.evidence_file = self.directory / "evidence" / "read.json"
        self.evidence_file.write_text('{"count": 1}\n', encoding="utf-8")
        self.snapshot = {
            "schema_version": 1, "generated_at": "2026-10-24T03:00:00+00:00",
            "source": {"release_id": 501, "organization": "https://ado.example", "project": "TEST", "revision": 7},
            "collection_status": "partial",
            "release": {"id": 501, "rev": 7, "fields": {"System.Title": "Test release", "System.State": "Planned"},
                        "url": "https://ado.example/TEST/_workitems/edit/501", "relations": []},
            "builds": [{"id": 101, "status": "complete", "build": {"id": 101, "repository": {"name": "repo-one"},
                        "sourceBranch": "refs/heads/release/1", "sourceVersion": "abc123", "result": "succeeded"},
                        "comparisons": {"production": None}, "baseline": {"status": "unavailable"}}],
            "workitems": [{"id": 201, "rev": 3, "fields": {"System.Title": "Story", "System.WorkItemType": "Story",
                           "System.State": "Active", "Microsoft.VSTS.Common.AcceptanceCriteria": "Exact criterion retained"}}],
            "tests": [{"buildId": 101, "requirementCoverages": [{"id": 201, "passed": 3, "failed": 1}]}],
            "defects": [], "coverage": [{"buildId": 101, "lineCoverage": 0}],
            "sonarqube": [{"component": "project-one", "association_status": "current_snapshot", "measures": {"coverage": 88}}],
            "graph": {"nodes": [{"id": "story:201", "type": "story", "label": "Story"}], "edges": [],
                      "warnings": ["Story links are incomplete"], "unresolvedStoryIds": [501], "unlinkedCommits": ["abc123"]},
            "compliance": {"status": "unavailable", "links": []},
            "warnings": ["Production baseline unavailable"], "errors": [], "metrics": {"requests": 5},
        }

    def save(self, snapshot=None, evidence=None):
        return write_report_snapshot(self.directory, deepcopy(snapshot if snapshot is not None else self.snapshot),
                                     evidence if evidence is not None else [artifact_record(self.evidence_file, self.directory)])

    def change_snapshot_bytes(self, manifest, raw):
        snapshot_path = self.directory / "snapshot.json"
        snapshot_path.write_text(raw, encoding="utf-8")
        data = json.loads(manifest.read_text())
        data["snapshot"] = artifact_record(snapshot_path, self.directory)
        manifest.write_text(json.dumps(data), encoding="utf-8")

    def test_retained_snapshot_can_render_repeatedly_without_network_or_source_mutation(self):
        """Given a retained report and no network access,
        When it renders twice,
        Then output bytes match and every input stays unchanged."""
        manifest = self.save()
        before = {path: path.read_bytes() for path in self.directory.rglob("*") if path.is_file()}
        with patch("socket.create_connection", side_effect=AssertionError("No external access")), \
                patch("socket.socket", side_effect=AssertionError("No network sockets")), \
                patch("subprocess.Popen", side_effect=AssertionError("No child process")):
            first = render_release_report(manifest, self.root / "first.html")
            second = render_release_report(manifest, self.root / "second.html")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(before, {path: path.read_bytes() for path in before})
        content = first.read_text()
        for expected in ("Builds and comparisons", "Exact criterion retained", "ADO coverage", "SonarQube quality data",
                         "Story links are incomplete", "Unresolved story IDs", "Release Clinic report unavailable",
                         "Current branch snapshot; build association is unverified."):
            self.assertIn(expected, content)
        parsed = Elements(content)
        self.assertFalse(any(tag in {"script", "iframe", "img", "link"} for tag, _ in parsed.tags))
        self.assertTrue(any(link.endswith("snapshot.json") for link in parsed.links))
        self.assertIn(json.loads(manifest.read_text())["snapshot"]["sha256"], content)
        self.assertEqual(read_release_report(manifest)["coverage"][0]["lineCoverage"], 0)

    def test_rejects_modified_snapshot_or_evidence(self):
        """Given hash-bound report inputs,
        When retained bytes change,
        Then reading and rendering fail before creating output."""
        manifest = self.save()
        data = json.loads(manifest.read_text())
        snapshot_path = self.directory / data["snapshot"]["path"]
        original = snapshot_path.read_bytes()
        snapshot_path.write_bytes(original.replace(b"Test release", b"Best release"))
        with self.assertRaisesRegex(WorkbenchError, "SHA-256"):
            read_release_report(manifest)
        snapshot_path.write_bytes(original)
        self.evidence_file.write_text('{"count": 2}\n')
        with self.assertRaisesRegex(WorkbenchError, "SHA-256"):
            render_release_report(manifest, self.root / "output.html")
        self.assertFalse((self.root / "output.html").exists())

    def test_rejects_path_escape_absolute_paths_and_symlinks(self):
        """Given an artifact reference outside its confined report directory,
        When the report reader validates that reference,
        Then parent escapes, absolute paths, and symlinks are rejected."""
        manifest = self.save()
        data = json.loads(manifest.read_text())
        for path in ("../outside.json", str(self.evidence_file), "evidence\\read.json", "C:/read.json"):
            with self.subTest(path=path):
                changed = deepcopy(data)
                changed["evidence"][0]["path"] = path
                manifest.write_text(json.dumps(changed))
                with self.assertRaises(WorkbenchError):
                    read_release_report(manifest)
        manifest.write_text(json.dumps(data))
        link = self.directory / "evidence" / "linked.json"
        try:
            link.symlink_to(self.evidence_file)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        changed = deepcopy(data)
        changed["evidence"][0]["path"] = "evidence/linked.json"
        manifest.write_text(json.dumps(changed))
        with self.assertRaisesRegex(WorkbenchError, "symlink"):
            read_release_report(manifest)

    def test_finite_versioned_json_and_manifest_identity_are_required(self):
        """Given a saved report snapshot,
        When its finite JSON, schema, or source identity is invalid,
        Then the reader rejects the report."""
        manifest = self.save()
        original = (self.directory / "snapshot.json").read_text()
        for raw in (original.replace('"requests": 5', '"requests": NaN'),
                    original.replace('"schema_version": 1', '"schema_version": 2'),
                    original.replace('"collection_status": "partial"', '"collection_status": {}'),
                    original.replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1')):
            with self.subTest(raw=raw[:30]):
                self.change_snapshot_bytes(manifest, raw)
                with self.assertRaises(WorkbenchError):
                    read_release_report(manifest)
        self.change_snapshot_bytes(manifest, original)
        data = json.loads(manifest.read_text())
        data["source"]["release_id"] = 999
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(WorkbenchError, "identity"):
            read_release_report(manifest)

    def test_escapes_source_content_and_rejects_executable_or_credential_urls(self):
        """Given source values containing executable HTML and unsafe URLs,
        When the renderer creates HTML,
        Then no executable elements, handlers, or unsafe links exist."""
        snapshot = deepcopy(self.snapshot)
        snapshot["release"]["fields"]["System.Title"] = '<script>alert("x")</script><img src=x onerror=evil()>'
        snapshot["release"]["url"] = "javascript:alert(1)"
        snapshot["compliance"]["links"] = [
            {"name": "data", "url": "data:text/html,evil"},
            {"name": "script", "url": "javascript:alert(1)"},
            {"name": "credentials", "url": "https://user:password@example.test/report.html"},
            {"name": "backslash", "url": "https://example.test\\@evil.test/report.html"},
            {"name": '<img src=x onerror=evil()>', "url": "https://example.test/report.html?x=%22"},
        ]
        output = render_release_report(self.save(snapshot), self.root / "safe.html")
        content = output.read_text()
        parsed = Elements(content)
        self.assertFalse(any(tag in {"script", "img"} for tag, _ in parsed.tags))
        self.assertFalse(any(name.lower().startswith("on") for _, attrs in parsed.tags for name in attrs))
        self.assertFalse(any(link.startswith(("javascript:", "data:")) or "password" in link for link in parsed.links))
        self.assertIn("&lt;script&gt;", content)
        self.assertIn("https://example.test/report.html?x=%22", parsed.links)

    def test_compliance_links_preserve_clinic_files_and_renderer_cannot_replace_them(self):
        """Given an independent Clinic HTML and its report link,
        When the renderer creates its report,
        Then it links the original file without copying or replacing its content."""
        clinic = self.root / "clinic output" / "TDAReport_STREAM_501.html"
        clinic.parent.mkdir()
        clinic.write_bytes(b"<html>Independent Clinic content</html>")
        snapshot = deepcopy(self.snapshot)
        snapshot["compliance"] = {"status": "available", "links": [
            {"name": clinic.name, "path": str(clinic), "source_kind": "local"},
            {"name": "Attached report", "url": "https://ado.example/attachments/clinic-501", "source_kind": "attachment"},
        ]}
        manifest = self.save(snapshot)
        output = render_release_report(manifest, self.root / "report.html")
        parsed = Elements(output.read_text())
        self.assertIn("clinic%20output/TDAReport_STREAM_501.html", parsed.links)
        self.assertIn("https://ado.example/attachments/clinic-501", parsed.links)
        self.assertNotIn("Independent Clinic content", output.read_text())
        self.assertEqual(clinic.read_bytes(), b"<html>Independent Clinic content</html>")
        with self.assertRaisesRegex(WorkbenchError, "Clinic"):
            render_release_report(manifest, clinic)
        self.assertEqual(clinic.read_bytes(), b"<html>Independent Clinic content</html>")

    def test_large_artifact_remains_complete_without_embedding_it_in_html(self):
        """Given test evidence larger than five MiB,
        When the renderer creates HTML,
        Then complete bytes remain hash-bound and the bounded preview links them."""
        payload = {"payload": "x" * (5 * 1024 * 1024)}
        self.evidence_file.write_text(json.dumps(payload), encoding="utf-8")
        snapshot = deepcopy(self.snapshot)
        snapshot["tests"] = [payload]
        manifest = self.save(snapshot)
        expected_hash = hashlib.sha256(self.evidence_file.read_bytes()).hexdigest()
        output = render_release_report(manifest, self.root / "large.html")
        self.assertGreater(self.evidence_file.stat().st_size, 5 * 1024 * 1024)
        self.assertLess(output.stat().st_size, 150000)
        self.assertIn("Display preview is truncated", output.read_text())
        self.assertIn(expected_hash, output.read_text())
        self.assertEqual(read_release_report(manifest)["tests"][0]["payload"], payload["payload"])

    def test_local_clinic_identity_is_the_release_suffix_not_part_of_the_stream(self):
        """Given a Clinic filename containing another release ID in its stream,
        When its actual release suffix differs,
        Then it is not linked as this release's compliance document.
        """
        clinic = self.root / "TDAReport_STREAM_501_OTHER_999.html"
        clinic.write_text("<p>Other release</p>")
        snapshot = deepcopy(self.snapshot)
        snapshot["compliance"] = {"status": "available", "links": [
            {"name": clinic.name, "path": str(clinic), "source_kind": "local"},
        ]}
        output = render_release_report(self.save(snapshot), self.root / "report.html")
        self.assertIn("Release Clinic report unavailable", output.read_text())
        self.assertNotIn(clinic.name, Elements(output.read_text()).links)
        self.assertFalse(any(clinic.name in link for link in Elements(output.read_text()).links))

    def test_large_sections_link_complete_data_with_bounded_visible_previews(self):
        """Given many build details and work items,
        When HTML renders bounded previews,
        Then the complete dataset stays retained and each display limit is explicit.
        """
        snapshot = deepcopy(self.snapshot)
        snapshot["builds"] = [{"id": i, "status": "complete", "build": {"id": i, "fixture": "x" * 50000}}
                              for i in range(1000, 1060)]
        snapshot["workitems"] = [{"id": i, "fields": {"System.Title": f"Story {i}"}}
                                 for i in range(2000, 2600)]
        manifest = self.save(snapshot)
        output = render_release_report(manifest, self.root / "bounded.html")
        content = output.read_text()
        self.assertIn("Showing 50 of 60 build detail previews", content)
        self.assertIn("Showing the first 500 of 600 rows", content)
        self.assertLess(output.stat().st_size, 2000000)
        loaded = read_release_report(manifest)
        self.assertEqual(len(loaded["builds"]), 60)
        self.assertEqual(len(loaded["workitems"]), 600)
        self.assertTrue(any(link.endswith("snapshot.json") for link in Elements(content).links))

    def test_renderer_rejects_output_symlink_and_writer_rejects_snapshot_overwrite(self):
        """Given retained report files and an output symlink,
        When a writer or renderer would replace protected data,
        Then it rejects the write."""
        manifest = self.save()
        with self.assertRaises(WorkbenchError):
            self.save()
        link = self.root / "output.html"
        try:
            link.symlink_to(self.evidence_file)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        with self.assertRaisesRegex(WorkbenchError, "symlink"):
            render_release_report(manifest, link)

    def test_rejects_conflicting_release_identity_and_revision(self):
        """Given source metadata and a different returned release identity or revision,
        When the writer validates a snapshot,
        Then it rejects the contradictory source record.
        """
        for key, value in (("id", 999), ("rev", 8)):
            with self.subTest(key=key):
                snapshot = deepcopy(self.snapshot)
                snapshot["release"][key] = value
                with self.assertRaisesRegex(WorkbenchError, "identity|revision"):
                    validate_snapshot(snapshot)

    def test_parser_limits_reject_invalid_json_with_a_report_error(self):
        """Given JSON beyond the parser's supported nesting or integer limit,
        When the reader loads the retained snapshot,
        Then it raises a report error before rendering output.
        """
        manifest = self.save()
        for raw in ('{"value": ' + '[' * 2000 + '0' + ']' * 2000 + '}',
                    '{"value": ' + '9' * 10000 + '}'):
            with self.subTest(length=len(raw)):
                self.change_snapshot_bytes(manifest, raw)
                with self.assertRaises(WorkbenchError):
                    read_release_report(manifest)

    def test_comparison_and_coverage_tables_preserve_unknowns_and_zero_values(self):
        """Given pinned comparisons and coverage summaries with missing values,
        When HTML renders human-readable tables,
        Then identities, counts, zero coverage, and unknown values stay explicit.
        """
        snapshot = deepcopy(self.snapshot)
        snapshot["builds"][0]["comparisons"] = {
            "production": {"status": "complete", "base": "prod123", "target": "abc123", "aheadCount": 0, "behindCount": 2},
            "main": {"status": "unavailable", "base": "main123", "target": None},
        }
        snapshot["coverage"] = [{"build_id": 101, "summary": {"line_coverage": 0, "branch_coverage": 75.5}, "status": "complete"}]
        output = render_release_report(self.save(snapshot), self.root / "summary.html")
        content = output.read_text()
        for expected in ("Base commit", "Target commit", "Ahead", "Behind", "prod123", "main123", "Lines", "Branches", "0%", "75.5%"):
            self.assertIn(expected, content)
        self.assertIn("Unavailable", content)

    def test_duplicate_requirement_counts_remain_separate_by_build(self):
        """Given two builds with different counts for one requirement and no aggregation rule,
        When HTML renders the evidence,
        Then each build retains its counts without a combined statistic.
        """
        snapshot = deepcopy(self.snapshot)
        snapshot["tests"] = [{"build_id": build, "requirementCoverages": [{"id": 501,
                             "testExecutionStatusStats": {"countByType": {"PASSED": passed, "FAILED": failed}}}]}
                             for build, passed, failed in ((101, 3, 1), (102, 2, 2))]
        snapshot["test_aggregation"] = {"status": "not_configured", "scope": "build_specific",
            "message": "No cross-build aggregation rule is configured. Counts remain separate for each build."}
        output = render_release_report(self.save(snapshot), self.root / "counts.html")
        content = output.read_text()
        self.assertIn(snapshot["test_aggregation"]["message"], content)
        self.assertIn('<tr><td>101</td><td>501</td><td>3</td><td>1</td>', content)
        self.assertIn('<tr><td>102</td><td>501</td><td>2</td><td>2</td>', content)
        self.assertNotIn("Combined statistic", content)
        self.assertEqual([(item["build_id"], item["requirementCoverages"][0]["testExecutionStatusStats"]["countByType"])
                          for item in read_release_report(self.directory / "manifest.json")["tests"]],
                         [(101, {"PASSED": 3, "FAILED": 1}), (102, {"PASSED": 2, "FAILED": 2})])


if __name__ == "__main__":
    unittest.main()
