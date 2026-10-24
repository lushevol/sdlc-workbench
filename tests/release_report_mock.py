"""Loopback ADO and Sonar fixtures for the release report's public collection path.

The handlers are read-only fixtures. No route reaches an external service.
"""
from __future__ import annotations

from collections import Counter
from contextlib import AbstractContextManager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import time
from urllib.parse import parse_qs, unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = "a" * 40
TIP = "b" * 40
MAIN = "c" * 40
PRODUCTION = "d" * 40
ADO_TOOLS = [
    "report_work_items", "report_builds", "report_build_timeline", "report_build_artifacts",
    "report_build_logs", "report_build_properties", "report_attachment", "report_deployments",
    "report_branches", "report_compare", "report_commits", "report_commit_changes",
    "report_file", "report_coverage",
]
SONAR_TOOLS = [
    "report_sonar_measures", "report_sonar_gate", "report_sonar_issues",
    "report_sonar_hotspots", "report_sonar_analyses",
]


def safe_environment() -> dict[str, str]:
    """Do not inherit real connector credentials, proxy routing, or custom endpoints."""
    return {name: value for name, value in os.environ.items()
            if name in {"PATH", "HOME", "SYSTEMROOT", "TMPDIR", "LANG", "PYTHONPATH"}}


class MockReleaseService(AbstractContextManager):
    """Serve deterministic raw ADO/Sonar records and record every actual HTTP attempt."""

    def __init__(self, *, forbidden_build: int | None = None, no_clinic: bool = False,
                 no_production: bool = False, related_count: int = 3,
                 attachment_padding: int = 0, delay: float = 0.0, paged_changes: bool = False,
                 no_branch_refs: bool = False, unsupported_coverage: bool = False,
                 graph_extra_workitems: bool = False, duplicate_relations: int = 0,
                 sonar_issues_second_page_failure: bool = False):
        self.forbidden_build = forbidden_build
        self.no_clinic = no_clinic
        self.no_production = no_production
        self.related_count = related_count
        self.attachment_padding = attachment_padding
        self.delay = delay
        self.paged_changes = paged_changes
        self.no_branch_refs = no_branch_refs
        self.unsupported_coverage = unsupported_coverage
        self.graph_extra_workitems = graph_extra_workitems
        self.duplicate_relations = duplicate_relations
        self.sonar_issues_second_page_failure = sonar_issues_second_page_failure
        self.revision = 7
        self.requests: list[dict] = []
        self.counts = Counter()
        self.lock = threading.Lock()
        self.active = Counter()
        self.peak = Counter()
        self.throttle_once: dict[str, str] = {}
        self.failure_once: dict[str, int] = {}
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler_type())
        self._server.daemon_threads = True
        self.url = f"http://127.0.0.1:{self._server.server_port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *args):
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)

    def reset_requests(self):
        with self.lock:
            self.requests.clear()
            self.counts.clear()
            self.peak.clear()

    def _handler_type(self):
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args):
                pass

            def handle(self):
                try:
                    super().handle()
                except (BrokenPipeError, ConnectionResetError):
                    # Retry/cancellation closes a pooled client socket intentionally.
                    pass

            def do_GET(self):
                self._respond()

            def do_POST(self):
                self._respond()

            def _respond(self):
                parsed = urlsplit(self.path)
                path = unquote(parsed.path)
                query = parse_qs(parsed.query)
                content_length = int(self.headers.get("Content-Length", "0"))
                incoming = self.rfile.read(content_length) if content_length else b""
                try:
                    body = json.loads(incoming) if incoming else None
                except json.JSONDecodeError:
                    body = None
                host_kind = "sonar" if path.startswith("/api/") else "ado"
                key = self.command + " " + path
                with fixture.lock:
                    fixture.active[host_kind] += 1
                    fixture.peak[host_kind] = max(fixture.peak[host_kind], fixture.active[host_kind])
                    fixture.counts[key] += 1
                    fixture.requests.append({"method": self.command, "path": path, "query": query,
                                             "body": body, "at": time.monotonic(),
                                             "connector": host_kind})
                    failure = fixture.failure_once.pop(path, None)
                    retry_after = fixture.throttle_once.pop(path, None)
                try:
                    if fixture.delay:
                        time.sleep(fixture.delay)
                    if failure:
                        status, payload, headers = failure, {"message": "Transient fixture failure"}, {}
                    else:
                        status, payload, headers = fixture.route(self.command, path, query, body)
                    if retry_after is not None:
                        headers["Retry-After"] = retry_after
                    if isinstance(payload, bytes):
                        data = payload
                        content_type = headers.pop("Content-Type", "application/octet-stream")
                    else:
                        data = json.dumps(payload, separators=(",", ":")).encode()
                        content_type = headers.pop("Content-Type", "application/json")
                    self.send_response(status)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", str(len(data)))
                    for name, value in headers.items():
                        self.send_header(name, str(value))
                    self.end_headers()
                    self.wfile.write(data)
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass
                finally:
                    with fixture.lock:
                        fixture.active[host_kind] -= 1

        return Handler

    def related_ids(self):
        fixed = [201, 301, 401]
        if self.related_count <= 3:
            return fixed[:self.related_count]
        return fixed + list(range(1000, 1000 + self.related_count - len(fixed)))

    def release(self):
        components = "r1_node_ansible"
        # Source build links are identity references; all reads still use the loopback endpoint.
        pipeline_lines = [f"r1-node-ansible-released-https://dev.azure.com/mock/Project/_build/results?buildId={i}"
                          for i in (101, 102)]
        relations = [{"rel": "System.LinkTypes.Related", "url": f"{self.url}/_apis/wit/workItems/{i}"}
                     for i in self.related_ids() if i != 301]
        relations.extend({"rel": "System.LinkTypes.Related", "url": f"{self.url}/_apis/wit/workItems/201"}
                         for _ in range(self.duplicate_relations))
        relations.append({"rel": "Microsoft.VSTS.Common.TestedBy-Forward",
                          "url": f"{self.url}/_apis/wit/workItems/301"})
        if not self.no_clinic:
            relations.append({"rel": "AttachedFile", "url": self.url + "/attachments/clinic-501",
                              "attributes": {"name": "TDAReport_STREAM_501.html",
                                             "addedDate": "2026-10-23T01:00:00Z"}})
        return {"id": 501, "rev": self.revision, "url": self.url + "/_apis/wit/workItems/501",
                "fields": {"System.Id": 501, "System.WorkItemType": "Release",
                           "System.TeamProject": "Project", "System.Title": "Fixture release <501>",
                           "System.State": "Active", "System.Description": "<p>Complete release detail</p>",
                           "Custom.LatestPipelineRuns": "<div>" + "<br>".join(pipeline_lines) + "</div>",
                           "Custom.DeploymentComponents": "<p>" + components + "</p>",
                           "Custom.StoriesLinked": "201", "Custom.CHGID": "CHG-501",
                           "Custom.PlannedReleaseDate": "2026-10-24T08:00:00Z",
                           "Custom.UnmappedEvidence": "Preserve this custom field"},
                "relations": relations}

    def workitem(self, identifier):
        if identifier == 501:
            return self.release()
        kind = "Test Case" if identifier in {301, 701} else "Bug" if identifier == 401 else "Story"
        relations = []
        if identifier == 201:
            relations = [{"rel": "Microsoft.VSTS.Common.TestedBy-Forward",
                          "url": f"{self.url}/_apis/wit/workItems/301"}]
        if identifier == 601 and self.graph_extra_workitems:
            relations = [{"rel": "Microsoft.VSTS.Common.TestedBy-Forward",
                          "url": f"{self.url}/_apis/wit/workItems/701"}]
        return {"id": identifier, "rev": 3, "url": f"{self.url}/_apis/wit/workItems/{identifier}",
                "fields": {"System.WorkItemType": kind, "System.TeamProject": "Project",
                           "System.Title": f"{kind} {identifier}", "System.State": "Active",
                           "System.Description": f"Description {identifier}",
                           "Microsoft.VSTS.Common.AcceptanceCriteria": f"Assertion {identifier}",
                           "Microsoft.VSTS.Common.Priority": 2,
                           "Microsoft.VSTS.Common.Severity": "2 - High",
                           "System.AssignedTo": {"displayName": "Fixture owner"}},
                "relations": relations}

    def build(self, identifier):
        return {"id": identifier, "buildNumber": f"20261024.{identifier}", "status": "completed",
                "result": "succeeded", "sourceBranch": "refs/heads/release/2026",
                "sourceVersion": PRODUCTION if identifier == 90 else CANDIDATE,
                "queueTime": "2026-10-24T01:00:00Z", "startTime": "2026-10-24T01:01:00Z",
                "finishTime": "2026-10-24T01:05:00Z", "project": {"id": "p1", "name": "Project"},
                "definition": {"id": 11, "name": "r1_node_ansible"},
                "repository": {"id": "r1", "name": "r1", "type": "TfsGit", "url": self.url + "/Project/_git/r1"},
                "_links": {"web": {"href": f"{self.url}/Project/_build/results?buildId={identifier}"}},
                "url": f"{self.url}/Project/_apis/build/builds/{identifier}",
                "fixtureExtra": {"rawBuildRetained": True}}

    def test_report(self, build_id):
        passed, failed = (3, 1) if build_id == 101 else (2, 2)
        return {"version": "fixture-1", "release": {"id": "501", "name": "Fixture release",
                "permalink": self.url + "/_workitems/edit/501", "testingTypes": ["SYSTEM_TEST"],
                "rationaleForNotDoingPt": "Fixture scope", "rationaleForNotDoingMandatoryTestings": "Fixture scope",
                "catalystRelease": False},
                "requirementCoverages": [{"id": "201", "type": "Story", "name": "Story201",
                    "assignee": "Fixture owner", "permalink": self.url + "/_workitems/edit/201",
                    "testCaseIds": ["301"], "defectIds": ["401"],
                    "testExecutionStatusStats": {"totalCount": 4, "countByType": {
                        "PASSED": passed, "FAILED": failed, "NO_EXECUTION": 0, "BLOCKED": 0, "DEFERRED": 0}},
                    "defectStatusStats": {"totalCount": 1, "countByType": {"OPEN": 1, "CLOSED": 0, "IN_PROGRESS": 0}}}],
                "testCoverages": [{"id": "301", "name": "Check settlement", "status": "Passed",
                    "requirementIds": ["201"], "testPlan": {"id": "701", "name": "Release plan",
                        "permalink": self.url + "/tests/plan/701"},
                    "permalink": self.url + "/_workitems/edit/301", "executionType": "AUTOMATIC",
                    "testType": "SYSTEM_TEST", "testingTool": "Fixture", "executedBy": "Fixture runner",
                    "regression": False,
                    "testSuite": {"id": "702", "name": "System"}, "testRunId": str(800 + build_id),
                    "testResultId": "901", "executionTime": "2026-10-24T01:04:00Z",
                    "testResultEvidence": {"hasAttachment": True, "hasComment": True},
                    "testResultPermalink": f"{self.url}/tests/results/901"}],
                "defectCoverages": [{"id": "401", "name": "Bug401", "status": "Active",
                    "assignee": "Fixture owner", "permalink": self.url + "/_workitems/edit/401",
                    "severity": "2 - High", "priority": 2}],
                "nonRegressionTestExecStatusStats": {
                    key: {"totalCount": 4, "countByType": {"PASSED": passed, "FAILED": failed,
                          "NO_EXECUTION": 0, "BLOCKED": 0, "DEFERRED": 0}}
                    for key in ("SYSTEM_TEST", "ACCEPTANCE_TEST")},
                "regressionTestExecStatusStats": {"totalCount": 0, "countByType": {
                    "PASSED": 0, "FAILED": 0, "NO_EXECUTION": 0, "BLOCKED": 0, "DEFERRED": 0}},
                "defectSeverityStats": {key: {"totalCount": 1 if key == "HIGH" else 0,
                    "countByType": {"OPEN": 1 if key == "HIGH" else 0, "IN_PROGRESS": 0, "CLOSED": 0},
                    "outstandingCount": 1 if key == "HIGH" else 0} for key in ("CRITICAL", "HIGH", "MEDIUM", "LOW")},
                "complianceStatusDetail": {"status": "INFO", "errors": [], "warnings": []},
                "testEnvironmentSummaries": [{"name": "SIT", "deploymentType": "Pipeline",
                                               "appComponents": "r1"}],
                "updatedAt": "2026-10-24T01:05:00Z", "checksum": f"fixture-{build_id}",
                "fixturePadding": "x" * self.attachment_padding}

    def route(self, method, path, query, body):
        if path.endswith("/_apis/wit/workitemsbatch"):
            identifiers = (body or {}).get("ids", [])
            return 200, {"count": len(identifiers), "value": [self.workitem(int(i)) for i in identifiers]}, {}
        if path.endswith("/_apis/build/builds"):
            identifiers = [int(i) for i in query.get("buildIds", ["101,102"])[0].split(",") if i]
            if identifiers == [self.forbidden_build]:
                return 403, {"message": "Fixture build forbidden"}, {}
            builds = [self.build(i) for i in identifiers if i != self.forbidden_build]
            return 200, {"count": len(builds), "value": builds}, {}
        if "/_apis/build/builds/" in path:
            tail = path.split("/_apis/build/builds/", 1)[1].split("/")
            identifier = int(tail[0])
            if identifier == self.forbidden_build:
                return 403, {"message": "Fixture build forbidden"}, {}
            suffix = tail[1:]
            if suffix == ["timeline"]:
                return 200, {"id": f"timeline-{identifier}", "records": [
                    {"id": f"task-{identifier}", "refName": "generatetestreport", "type": "Task",
                     "name": "Generate test report", "result": "succeeded",
                     "finishTime": "2026-10-24T01:04:00Z"}]}, {}
            if suffix == ["artifacts"]:
                return 200, {"count": 1, "value": [{"id": 1, "name": "drop", "resource": {
                    "type": "Container", "downloadUrl": f"{self.url}/artifacts/build-{identifier}"}}]}, {}
            if suffix == ["logs"]:
                return 200, {"count": 1, "value": [{"id": 1, "lineCount": 42,
                    "url": f"{self.url}/logs/build-{identifier}"}]}, {}
            if suffix == ["properties"]:
                return 200, {"sonar.projectKey": "quality-r1", "sonar.analysisId": "analysis-101",
                             "sonar.analysisRevision": CANDIDATE}, {}
            if "attachments" in suffix:
                return 200, self.test_report(identifier), {}
        if path.endswith("/_apis/test/codecoverage"):
            identifier = int(query.get("buildId", ["101"])[0])
            if self.unsupported_coverage:
                return 200, {"value": [{"build": {"id": identifier},
                    "coverageFileUrl": self.url + "/coverage/unparsed.binary"}]}, {}
            return 200, {"count": 1, "value": [{"build": {"id": identifier}, "coverageData": [
                {"coverageStats": [{"label": "Lines", "covered": 80, "total": 100},
                                   {"label": "Branches", "covered": 30, "total": 50}]}]}]}, {}
        if "/_apis/Contribution/HierarchyQuery/" in path:
            properties = (body or {}).get("dataProviderContext", {}).get("properties", {})
            keyword = properties.get("keywordFilter", "release")
            runs = [] if self.no_production or keyword == "main" else [
                {"run": {**self.build(90), "sourceBranch": "refs/heads/release/2026"},
                 "stages": [{"refName": "prod", "result": 0, "finishTime": "/Date(1792713600000)/"},
                            {"refName": "rollback_prod", "result": 4}]}]
            return 200, {"dataProviders": {"ms.vss-build-web.runs-data-provider": {"runs": runs}}}, {}
        if "/_apis/git/repositories/" in path:
            suffix = path.split("/_apis/git/repositories/", 1)[1].split("/", 1)[1]
            if suffix == "refs":
                ref = query.get("filter", ["heads/"])[0]
                refs = [{"name": "refs/heads/release/2026", "objectId": TIP},
                        {"name": "refs/heads/main", "objectId": MAIN}]
                refs = [] if self.no_branch_refs else [r for r in refs if r["name"].replace("refs/", "").startswith(ref)]
                return 200, {"count": len(refs), "value": refs}, {}
            if suffix == "diffs/commits":
                base = query.get("baseVersion", [PRODUCTION])[0]
                target = query.get("targetVersion", [CANDIDATE])[0]
                skip = int(query.get("$skip", ["0"])[0])
                paths = ["/src/settlement.py", "/src/validation.py"] if self.paged_changes else ["/src/settlement.py"]
                selected = paths[skip:skip + 1] if self.paged_changes else paths[skip:]
                changes = [{"item": {"path": name, "gitObjectType": "blob"}, "changeType": "edit"}
                           for name in selected]
                return 200, {"baseCommit": base, "targetCommit": target, "commonCommit": PRODUCTION,
                             "aheadCount": 1, "behindCount": 0, "allChangesIncluded": skip + len(selected) >= len(paths),
                             "changeCounts": {"Edit": len(paths)}, "changes": changes}, {}
            if suffix == "commits":
                skip = int(query.get("$skip", ["0"])[0])
                workitems = [{"id": "201", "url": f"{self.url}/_apis/wit/workItems/201"}]
                if self.graph_extra_workitems:
                    workitems.append({"id": "601", "url": f"{self.url}/_apis/wit/workItems/601"})
                commits = [] if skip else [{"commitId": CANDIDATE, "parents": [PRODUCTION],
                    "comment": "Implement settlement", "workItems": workitems,
                    "url": f"{self.url}/Project/_apis/git/repositories/r1/commits/{CANDIDATE}"}]
                return 200, {"count": len(commits), "value": commits}, {}
            if suffix.endswith("/changes"):
                skip = int(query.get("skip", ["0"])[0])
                paths = ["/src/settlement.py", "/src/validation.py"] if self.paged_changes else ["/src/settlement.py"]
                selected = paths[skip:skip + 1] if self.paged_changes else paths[skip:]
                return 200, {"changeCounts": {"Edit": len(paths)}, "changes": [{"item": {
                    "path": name, "gitObjectType": "blob"}, "changeType": "edit"} for name in selected]}, {}
            if suffix == "items":
                path = query.get("path", ["/src/settlement.py"])[0]
                return 200, {"path": path, "content": "def settle():\n    return True\n"}, {}
        if path == "/api/measures/component":
            return 200, {"component": {"key": "quality-r1", "name": "R1 quality", "measures": [
                {"metric": "coverage", "value": "82.5"}, {"metric": "line_coverage", "value": "83.0"},
                {"metric": "branch_coverage", "value": "61.0"}, {"metric": "alert_status", "value": "OK"}]}}, {}
        if path == "/api/qualitygates/project_status":
            return 200, {"projectStatus": {"status": "OK", "conditions": []}}, {}
        if path == "/api/project_analyses/search":
            return 200, {"paging": {"pageIndex": 1, "pageSize": 100, "total": 1},
                         "analyses": [{"key": "analysis-101", "revision": CANDIDATE,
                                       "date": "2026-10-24T01:03:00Z", "events": []}]}, {}
        if path in {"/api/issues/search", "/api/hotspots/search"}:
            page = int(query.get("p", ["1"])[0])
            if path == "/api/issues/search" and page == 2 and self.sonar_issues_second_page_failure:
                return 403, {"message": "Fixture second issue page forbidden"}, {}
            # Two pages deliberately exercise total-aware pagination even for large requested page sizes.
            key = "issues" if "issues" in path else "hotspots"
            records = [{"key": f"{key}-{page}", "component": "quality-r1:src/settlement.py",
                        "message": f"Fixture {key} page {page}", "status": "OPEN" if key == "issues" else "TO_REVIEW",
                        "type": "BUG", "severity": "MAJOR", "line": page}] if page <= 2 else []
            return 200, {"total": 2, "p": page, "ps": 1,
                         "paging": {"pageIndex": page, "pageSize": 1, "total": 2}, key: records}, {}
        if path == "/attachments/clinic-501":
            return 200, b"<!doctype html><html><body>Original Clinic report</body></html>", {"Content-Type": "text/html"}
        return 404, {"message": f"No mock route for {method} {path}"}, {}


def write_mock_workspace(root: Path, service: MockReleaseService, *, denied_tools=(),
                         collection_timeout_seconds=120, ado_concurrency=6, sonar_concurrency=2):
    """Create a source-free workspace that points only at the loopback service."""
    root.mkdir(parents=True, exist_ok=True)
    command = ["node", str(ROOT / "core/connectors/workbench/bridge.js")]
    resources = [
        {"id": "external-ado", "kind": "connector", "provider": "connector.mcp", "environment": "mock",
         "config": {"command": command, "connector": "ado",
                    "allowed_tools": [x for x in ADO_TOOLS if x not in denied_tools]},
         "allowed_operations": ["list", "call"]},
        {"id": "external-sonar", "kind": "connector", "provider": "connector.mcp", "environment": "mock",
         "config": {"command": command, "connector": "sonar",
                    "allowed_tools": [x for x in SONAR_TOOLS if x not in denied_tools]},
         "allowed_operations": ["list", "call"]},
        {"id": "release-report", "kind": "release_report", "provider": "release.report", "environment": "mock",
         "config": {"ado_resource": "external-ado", "sonar_resource": "external-sonar",
                    "collection_timeout_seconds": collection_timeout_seconds,
                    "ado_concurrency": ado_concurrency, "sonar_concurrency": sonar_concurrency},
         "allowed_operations": ["collect"]},
    ]
    configuration = {"schema_version": 1, "id": "release-report-mock", "name": "Release report mock",
                     "timeout_seconds": 30, "plugins": [], "resources": resources}
    (root / "workspace.yaml").write_text(yaml.safe_dump(configuration, sort_keys=False), encoding="utf-8")
    (root / ".env").write_text(f"AZURE_DEVOPS_ORG_URL={service.url}\nAZURE_DEVOPS_PAT=fixture-ado-token\n"
                                f"ADO_PROJECT=Project\nSONAR_BASE_URL={service.url}\n"
                                "SONAR_TOKEN=fixture-sonar-token\n", encoding="utf-8")
    return configuration
