"""Collect release information through reusable connector sessions, without rendering."""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import threading
import time
from urllib.parse import unquote

from .models import Context, Resource, WorkbenchError
from .release_report_contract import artifact_record, read_release_report, write_report_snapshot
from .release_report_source import ConnectorSession, ReportReadError
from .workspace import load_workspace


def _now():
    return datetime.now(timezone.utc).isoformat()


def _write(path: Path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def _items(data, key="value"):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        values = data.get(key, [])
        return values if isinstance(values, list) else []
    return []


def _positive(value):
    if isinstance(value, bool):
        return None
    try:
        number = int(value)
        return number if 0 < number <= 2147483647 else None
    except (TypeError, ValueError, OverflowError):
        return None


def _chunks(values, size=200):
    values = sorted(set(values))
    return [values[index:index + size] for index in range(0, len(values), size)]


def _relation_ids(item, *, initial=False):
    identifiers = set()
    for relation in item.get("relations", []):
        kind = relation.get("rel", "")
        if kind in {"Microsoft.VSTS.Common.TestedBy-Forward", "System.LinkTypes.Hierarchy-Forward"} or (
                initial and kind == "System.LinkTypes.Related"):
            match = re.search(r"/workitems/(\d+)(?:$|[/?#])", relation.get("url", ""), re.I)
            if match:
                identifiers.add(int(match[1]))
    if initial:
        identifiers.update(int(value) for value in re.findall(r"\d+", str(item.get("fields", {}).get("Custom.StoriesLinked", ""))))
    return identifiers


def _build_ids(item):
    fields = item.get("fields", {})
    text = html.unescape(str(fields.get("Custom.LatestPipelineRuns", "")))
    identifiers = {int(value) for value in re.findall(r"buildId=(\d+)", text, re.I)}
    for relation in item.get("relations", []):
        if relation.get("rel") == "ArtifactLink":
            match = re.search(r"/Build/(\d+)$", unquote(relation.get("url", "")), re.I)
            if match:
                identifiers.add(int(match[1]))
    return {value for value in identifiers if _positive(value)}


def _date(value):
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"/Date\((\d+)", str(value))
    if match:
        return int(match[1]) / 1000
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except (ValueError, TypeError):
        return float("-inf")


def _coverage_summary(data):
    if isinstance(data, dict) and all(type(data.get(key)) in (int, float) and 0 <= data[key] <= 100
                                     for key in ("lineCoverage", "branchCoverage")):
        return {"line_coverage": data["lineCoverage"], "branch_coverage": data["branchCoverage"]}
    found = {}
    def visit(value):
        if isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, dict):
            label = str(value.get("label", value.get("name", ""))).lower()
            if label in {"lines", "line", "branches", "branch"}:
                covered, total = value.get("covered"), value.get("total")
                if type(covered) in (int, float) and type(total) in (int, float) and total > 0 and 0 <= covered <= total:
                    key = "line_coverage" if label.startswith("line") else "branch_coverage"
                    counts = found.setdefault(key, [0, 0])
                    counts[0] += covered
                    counts[1] += total
            for key, child in value.items():
                if isinstance(child, (list, dict)):
                    visit(child)
    visit(data)
    return {key: 100 * counts[0] / counts[1] for key, counts in found.items()}


class _Collector:
    def __init__(self, release_id, resource, context, resume=None):
        self.release_id, self.context = release_id, context
        self.workspace = context.workspace_root.resolve()
        self.directory = context.run_dir / "release-report"
        self.directory.mkdir()
        self.raw_dir = self.directory / "raw"
        self.raw_dir.mkdir()
        self.config = resource.config
        allowed = {"ado_resource", "sonar_resource", "collection_timeout_seconds", "request_timeout_seconds",
                   "ado_concurrency", "sonar_concurrency", "max_entities"}
        if set(self.config) - allowed:
            raise WorkbenchError("The release report resource contains an unsupported setting.")
        def number(name, default, minimum, maximum, integer=False):
            value = self.config.get(name, default)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not minimum <= value <= maximum:
                raise WorkbenchError(f"The release report setting {name} is invalid.")
            if integer and not isinstance(value, int):
                raise WorkbenchError(f"The release report setting {name} requires an integer.")
            return value
        self.started = time.monotonic()
        self.deadline = self.started + number("collection_timeout_seconds", context.timeout_seconds, .05, 3600)
        self.request_timeout = number("request_timeout_seconds", 30, .01, 3600)
        self.concurrency = {"ado": number("ado_concurrency", 6, 1, 32, True),
                            "sonar": number("sonar_concurrency", 2, 1, 32, True)}
        self.max_entities = number("max_entities", 20000, 1, 1000000, True)
        _, resources = load_workspace(self.workspace)
        self.resources = {}
        for connector in ("ado", "sonar"):
            identity = self.config.get(connector + "_resource", "external-" + connector)
            if identity in resources:
                candidate = resources[identity]
                if candidate.provider != "connector.mcp" or candidate.config.get("connector") != connector:
                    raise WorkbenchError("A report source must reference the matching native connector resource.")
                self.resources[connector] = candidate
        self.sessions = {}
        self.lock = threading.RLock()
        self.pending = {}
        self.evidence = []
        self.events = []
        self.cache_hits = 0
        self.resume_path = resume
        self.snapshot = {"schema_version": 1, "generated_at": _now(),
                         "source": {"release_id": release_id}, "collection_status": "failed", "release": {},
                         "builds": [], "workitems": [], "tests": [], "defects": [], "coverage": [],
                         "test_aggregation": {"status": "not_configured", "scope": "build_specific",
                                              "message": "No cross-build aggregation rule is configured. Counts remain separate for each build."},
                         "sonarqube": [], "graph": {"nodes": [], "edges": [], "warnings": [],
                                                      "unresolvedStoryIds": [], "unlinkedCommits": []},
                         "compliance": {"status": "unavailable", "links": []}, "warnings": [], "errors": [], "metrics": {}}

    def issue(self, code, *, tool=None, identity=None, message=None, warning=False):
        item = {"code": str(code), "message": message or "The requested report information is unavailable."}
        if tool:
            item["tool"] = tool
        if identity is not None:
            item["identity"] = identity
        with self.lock:
            target = self.snapshot["warnings" if warning else "errors"]
            if item not in target:
                target.append(item)

    def _session(self, connector):
        # Creation is synchronized; requests themselves remain concurrent.
        with self.lock:
            if connector not in self.sessions:
                self.sessions[connector] = ConnectorSession(
                    self.resources[connector], self.workspace, self.directory,
                    concurrency=self.concurrency[connector], deadline=self.deadline,
                    request_timeout=self.request_timeout,
                )
            return self.sessions[connector]

    def request(self, tool, arguments, connector="ado"):
        source = self.resources.get(connector)
        if not source or "call" not in source.allowed_operations or tool not in source.config.get("allowed_tools", []):
            self.issue("TOOL_NOT_GRANTED", tool=tool, identity=arguments)
            return None
        key = json.dumps([connector, tool, arguments], sort_keys=True, separators=(",", ":"), allow_nan=False)
        with self.lock:
            if key in self.pending:
                self.cache_hits += 1
                pending, owner = self.pending[key], False
            else:
                pending, owner = Future(), True
                self.pending[key] = pending
        if not owner:
            try:
                return pending.result(timeout=max(.01, self.deadline - time.monotonic()))
            except TimeoutError:
                self.issue("DEADLINE_EXCEEDED", tool=tool)
                return None
        result = None
        began = time.monotonic()
        event = {"connector": connector, "tool": tool, "arguments": arguments, "started_at": _now()}
        try:
            if time.monotonic() >= self.deadline:
                raise ReportReadError("DEADLINE_EXCEEDED")
            destination = self.raw_dir / (hashlib.sha256(key.encode()).hexdigest() + ".json")
            response = self._session(connector).call(tool, arguments, destination)
            event.update(status=response.get("status"), code=response.get("code"), http_status=response.get("http_status"))
            if response.get("artifact"):
                artifact = artifact_record(destination, self.directory)
                artifact.update(tool=tool, connector=connector)
                event["artifact"] = artifact
                with self.lock:
                    self.evidence.append(artifact)
            if response.get("status") != "SUCCEEDED":
                self.issue(response.get("code", "READ_FAILED"), tool=tool, identity=arguments)
            else:
                raw = destination.read_bytes()
                try:
                    data = json.loads(raw.decode("utf-8"), parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
                except (ValueError, UnicodeError):
                    data = {"artifact": event["artifact"], "text": raw[:100000].decode("utf-8", errors="replace")}
                result = {"data": data, "headers": response.get("headers", {}), "artifact": event.get("artifact")}
        except (WorkbenchError, OSError, ValueError) as error:
            code = getattr(error, "code", "READ_FAILED")
            event.update(status="ERROR", code=code)
            self.issue(code, tool=tool, identity=arguments)
        finally:
            event["elapsed_seconds"] = time.monotonic() - began
            with self.lock:
                self.events.append(event)
                with (self.directory / "requests.jsonl").open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(event, allow_nan=False) + "\n")
                    stream.flush()
                _write(self.directory / "checkpoint.json", {"release_id": self.release_id,
                       "release_revision": self.snapshot["source"].get("revision"), "requests": self.events,
                       "completed_at": _now()})
            pending.set_result(result)
        return result

    def parallel(self, jobs):
        if not jobs:
            return []
        with ThreadPoolExecutor(max_workers=min(8, len(jobs))) as pool:
            futures = [pool.submit(function, *args) for function, args in jobs]
            return [future.result() for future in futures]

    def workitems(self, identifiers, project=None):
        result = []
        for ids, response in zip(_chunks(identifiers), self.parallel([
                (self.request, ("report_work_items", {"ids": chunk, **({"project": project} if project else {})}))
                for chunk in _chunks(identifiers)])):
            values = _items(response["data"]) if response else []
            result.extend(values)
            received = {_positive(item.get("id")) for item in values if isinstance(item, dict)}
            for identifier in set(ids) - received:
                self.issue("WORK_ITEM_UNAVAILABLE", identity=identifier)
                result.append({"id": identifier, "collection_status": "failed", "fields": {}, "relations": []})
        return result

    def pages(self, tool, arguments, *, connector="ado", list_key="value", with_status=False):
        collected, page_number, skip, seen, complete = [], 1, 0, set(), True
        while time.monotonic() < self.deadline:
            values = dict(arguments)
            if connector == "sonar":
                values.update(page=page_number, pageSize=100)
            else:
                values.update(skip=skip, top=100)
            response = self.request(tool, values, connector)
            if not response:
                complete = False
                break
            data = response["data"]
            batch = _items(data, list_key)
            identity = json.dumps(batch, sort_keys=True, default=str)
            if batch and identity in seen:
                self.issue("PAGINATION_STALLED", tool=tool)
                complete = False
                break
            seen.add(identity)
            collected.extend(batch)
            paging = data.get("paging", {}) if isinstance(data, dict) else {}
            total = paging.get("total", data.get("total") if isinstance(data, dict) else None)
            if tool == "report_commit_changes" and isinstance(data.get("changeCounts"), dict):
                counts = data["changeCounts"].values()
                if all(type(count) is int and count >= 0 for count in counts):
                    total = sum(data["changeCounts"].values())
            if not batch and isinstance(total, int) and len(collected) < total:
                self.issue("PAGINATION_INCOMPLETE", tool=tool)
                complete = False
            if not batch or (isinstance(total, int) and len(collected) >= total):
                break
            if connector == "sonar":
                page_size = paging.get("pageSize", len(batch))
                if total is None and len(batch) < page_size:
                    break
                page_number += 1
            else:
                skip += len(batch)
            if len(collected) >= self.max_entities:
                self.issue("ENTITY_LIMIT", tool=tool)
                complete = False
                break
        else:
            self.issue("DEADLINE_EXCEEDED", tool=tool)
            complete = False
        return (collected, complete) if with_status else collected

    def deployments(self, project, pipeline):
        candidates = []
        for keyword in ("release", "main"):
            token, seen = None, set()
            while time.monotonic() < self.deadline:
                arguments = {"project": project, "pipelineId": pipeline, "keyword": keyword}
                if token:
                    arguments["continuationToken"] = token
                response = self.request("report_deployments", arguments)
                if not response:
                    break
                data = response["data"]
                provider = data.get("dataProviders", {}).get("ms.vss-build-web.runs-data-provider", data)
                runs = _items(provider, "runs") or _items(provider)
                candidates.extend(runs)
                headers = {str(key).lower(): value for key, value in response["headers"].items()}
                next_token = provider.get("continuationToken") or headers.get("x-ms-continuationtoken")
                if not next_token and len(runs) >= 25:
                    next_token = str(runs[-1].get("run", runs[-1]).get("finishTime", ""))
                if not next_token:
                    break
                if next_token in seen:
                    self.issue("PAGINATION_STALLED", tool="report_deployments")
                    break
                seen.add(next_token)
                token = next_token
            else:
                self.issue("DEADLINE_EXCEEDED", tool="report_deployments")
        qualifying = []
        for item in candidates:
            stages = item.get("stages", [])
            prod = next((stage for stage in stages if stage.get("refName") == "prod" and stage.get("result") == 0), None)
            rollback = next((stage for stage in stages if stage.get("refName") == "rollback_prod"), None)
            if prod and (rollback is None or rollback.get("result") == 4):
                qualifying.append((item, prod))
        qualifying.sort(key=lambda pair: _date(pair[1].get("finishTime")), reverse=True)
        return {"selected": qualifying[0][0], "stage": qualifying[0][1], "candidates": candidates} if qualifying else {
            "selected": None, "candidates": candidates}

    def compare(self, project, repo, base, target, common=False):
        if not base or not target:
            self.issue("COMPARISON_SOURCE_UNAVAILABLE", identity={"repository": repo, "base": base, "target": target})
            return {"status": "unavailable", "base": base, "target": target, "reason": "A required commit identity is unavailable."}
        skip, changes, result, seen = 0, [], {}, set()
        while time.monotonic() < self.deadline:
            response = self.request("report_compare", {"project": project, "repository": repo,
                                    "base": base, "target": target, "skip": skip, "top": 100, "common": common})
            if not response:
                return {**result, "status": "partial", "base": base, "target": target, "changes": changes}
            data = response["data"]
            if not isinstance(data, dict):
                self.issue("INVALID_COMPARISON", identity=repo)
                break
            result = data
            batch = data.get("changes", [])
            marker = json.dumps(batch, sort_keys=True)
            if batch and marker in seen:
                self.issue("PAGINATION_STALLED", tool="report_compare")
                break
            seen.add(marker)
            changes.extend(batch)
            if data.get("allChangesIncluded") is True:
                valid = all(type(data.get(key)) is int and data[key] >= 0 for key in ("aheadCount", "behindCount"))
                if not valid:
                    self.issue("COMPARISON_COUNTS_UNAVAILABLE", identity=repo)
                return {**data, "status": "complete" if valid else "unavailable", "base": base, "target": target, "changes": changes}
            if not batch:
                self.issue("COMPARISON_INCOMPLETE", identity=repo)
                break
            skip += len(batch)
        return {**result, "status": "partial", "base": base, "target": target, "changes": changes}

    def branch_tip(self, project, repo, name):
        token, seen = None, set()
        while time.monotonic() < self.deadline:
            args = {"project": project, "repository": repo, "filter": name}
            if token:
                args["continuationToken"] = token
            response = self.request("report_branches", args)
            if not response:
                break
            ref = next((item for item in _items(response["data"]) if item.get("name") == "refs/heads/" + name), None)
            if ref and ref.get("objectId"):
                return ref["objectId"]
            headers = {str(key).lower(): value for key, value in response["headers"].items()}
            token = headers.get("x-ms-continuationtoken")
            if not token or token in seen:
                break
            seen.add(token)
        self.issue("BRANCH_REF_UNAVAILABLE", identity={"repository": repo, "branch": name})
        return None

    def clinic(self, release):
        links = []
        pattern = re.compile(r"^(?:TDAReport_|TDA_Report_|Annotated_TDA_Report_|Annotated_TDAReport_).*\.html$", re.I)
        for relation in release.get("relations", []):
            attributes = relation.get("attributes", {})
            name = attributes.get("name", "")
            if relation.get("rel") == "AttachedFile" and pattern.match(name):
                links.append({"name": name, "url": relation.get("url", ""), "source_kind": "attachment",
                              "added_at": attributes.get("addedDate")})
        from .doctor import _environment
        environment, _ = _environment(self.workspace)
        output = environment.get("TDA_OUTPUT_DIR", "")
        directory = Path(output) if output else self.workspace / ".workbench/release-clinic/reports"
        if not directory.is_absolute():
            directory = self.workspace / directory
        if directory.is_dir() and not directory.is_symlink():
            for path in sorted(directory.glob("*.html")):
                if not path.is_symlink() and pattern.match(path.name) and re.search(rf"_{self.release_id}(?:\s*\(\d+\))?$", path.stem):
                    links.append({"name": path.name, "path": str(path.resolve()), "source_kind": "local"})
        return {"status": "available" if links else "unavailable", "links": links}

    def sonar(self, build):
        properties = build.get("properties") or {}
        if not isinstance(properties, dict):
            properties = {}
        properties = properties.get("value", properties)
        def prop(*keys):
            for key in keys:
                value = properties.get(key)
                if isinstance(value, dict):
                    value = value.get("$value", value.get("value"))
                if value:
                    return str(value)
            return None
        component = prop("sonar.projectKey", "SonarQube.ProjectKey", "sonarProjectKey")
        if not component:
            return {"build_id": build["id"], "status": "unavailable", "association_status": "unavailable",
                    "reason": "No Sonar project identity was published with this build."}
        raw = build["build"]
        branch = prop("sonar.branch.name") or raw.get("sourceBranch", "").removeprefix("refs/heads/")
        pull_request = prop("sonar.pullrequest.key")
        selector = {"pullRequest": pull_request} if pull_request else ({"branch": branch} if branch else {})
        args = {"component": component, **selector}
        measures = self.request("report_sonar_measures", args, "sonar")
        gate = self.request("report_sonar_gate", args, "sonar")
        analyses, analyses_complete = self.pages(
            "report_sonar_analyses", {"component": component, **({"branch": branch} if branch and not pull_request else {})},
            connector="sonar", list_key="analyses", with_status=True) if not pull_request else ([], True)
        analysis_id = prop("sonar.analysisId", "SonarQube.AnalysisId")
        analysis = next((item for item in analyses if item.get("key") == analysis_id), None) if analysis_id else None
        if analysis is None:
            analysis = next((item for item in analyses if item.get("revision") == raw.get("sourceVersion")), None)
        # Measures endpoints return current selector state, not arbitrary past
        # analysis values. Only call them matched when current analysis matches.
        current = analyses[0] if analyses else None
        matched = bool(current and current.get("revision") == raw.get("sourceVersion") and
                       (not analysis_id or current.get("key") == analysis_id))
        issues, issues_complete = self.pages("report_sonar_issues", args, connector="sonar", list_key="issues", with_status=True)
        hotspots, hotspots_complete = self.pages("report_sonar_hotspots", args, connector="sonar", list_key="hotspots", with_status=True)
        return {"build_id": build["id"], **args, "analysis": analysis, "current_analysis": current,
                "association_status": "matched" if matched else "current_snapshot",
                "status": "complete" if measures and gate and analyses_complete and issues_complete and hotspots_complete else "partial",
                "measures": measures["data"] if measures else None, "gate": gate["data"] if gate else None,
                "issues": issues, "hotspots": hotspots}

    def expand_workitems(self, related, visited, workitems, project):
        """Traverse supported child and test links, including commit-discovered work items."""
        related = set(related)
        while related - visited:
            pending = related - visited
            if len(visited | pending) > self.max_entities:
                self.issue("ENTITY_LIMIT", tool="report_work_items")
                break
            values = self.workitems(pending, project)
            workitems.extend(values)
            visited.update(pending)
            for item in values:
                related.update(_relation_ids(item))

    def graph(self, builds, workitems):
        nodes, edges, unlinked = {}, {}, []
        def node(identifier, kind, **details):
            nodes.setdefault(identifier, {"id": identifier, "type": kind, **details})
        def edge(source, target, kind, **details):
            identity = f"{kind}:{source}:{target}"
            edges.setdefault(identity, {"id": identity, "from": source, "to": target, "type": kind, **details})
        extra = set()
        for item in workitems:
            identifier = item["id"]
            kind = "testCase" if item.get("fields", {}).get("System.WorkItemType") == "Test Case" else "story"
            node(f"wi:{identifier}", kind, label=item.get("fields", {}).get("System.Title", str(identifier)), workItemId=identifier)
        jobs = []
        for build in builds:
            raw = build.get("build")
            if not raw:
                continue
            repo = raw.get("repository", {}).get("id") or raw.get("repository", {}).get("name")
            project = raw.get("project", {}).get("name") or self.snapshot["source"].get("project")
            commit = raw.get("sourceVersion")
            if not repo or not project or not commit:
                continue
            node(f"repo:{repo}", "repo", label=raw.get("repository", {}).get("name", repo), repo=repo)
            node(f"commit:{repo}:{commit}", "commit", label=commit[:12], repo=repo, commitId=commit)
            edge(f"repo:{repo}", f"commit:{repo}:{commit}", "contains")
            baseline = build.get("baseline", {}).get("selected")
            base = (baseline.get("run", baseline).get("sourceVersion") if baseline else None)
            if base:
                commits = self.pages("report_commits", {"project": project, "repository": repo, "base": base, "target": commit})
            else:
                commits = [{"commitId": commit, "workItems": []}]
            for change_commit in commits:
                sha = change_commit.get("commitId")
                if not sha:
                    continue
                source = f"commit:{repo}:{sha}"
                node(source, "commit", label=change_commit.get("comment", sha[:12]), repo=repo, commitId=sha)
                edge(f"repo:{repo}", source, "contains")
                linked = change_commit.get("workItems", [])
                if not linked:
                    unlinked.append(sha)
                for item in linked:
                    identity = _positive(item.get("id"))
                    if identity:
                        extra.add(identity)
                        node(f"wi:{identity}", "story", label=str(identity), workItemId=identity)
                        edge(source, f"wi:{identity}", "implements")
                jobs.append((project, repo, sha, source))
        # Requests are coalesced even when several builds reference the commit.
        results = self.parallel([(self.commit_changes, (p, r, sha))
                                 for p, r, sha, _ in jobs])
        file_jobs = []
        for (project, repo, sha, source), changes in zip(jobs, results):
            for change in changes:
                item = change.get("item", {})
                path = item.get("path")
                if not path or item.get("isFolder"):
                    continue
                target = f"file:{repo}:{sha}:{path}"
                node(target, "file", label=path, repo=repo, commitId=sha, path=path)
                edge(source, target, "changes", metadata={"path": path, "changeType": change.get("changeType")})
                if str(change.get("changeType", "")).lower() not in {"delete", "16"}:
                    file_jobs.append((self.request, ("report_file", {"project": project, "repository": repo, "path": path, "commit": sha})))
        self.parallel(file_jobs)
        for report in self.snapshot["tests"]:
            for requirement in report.get("requirementCoverages", []):
                identity = _positive(requirement.get("id"))
                if not identity:
                    continue
                extra.add(identity)
                node(f"wi:{identity}", "story", label=requirement.get("name", str(identity)), workItemId=identity)
                for testcase in requirement.get("testCaseIds", []):
                    test_id = _positive(testcase)
                    if test_id:
                        extra.add(test_id)
                        node(f"wi:{test_id}", "testCase", label=str(test_id), workItemId=test_id)
                        edge(f"wi:{identity}", f"wi:{test_id}", "testedBy")
        return {"nodes": list(nodes.values()), "edges": list(edges.values()), "unlinkedCommits": sorted(set(unlinked)),
                "warnings": [], "unresolvedStoryIds": []}, extra

    def commit_changes(self, project, repository, commit):
        return self.pages("report_commit_changes", {"project": project, "repository": repository, "commit": commit},
                          list_key="changes")

    def enrich_build(self, build, project):
        raw = build.get("build")
        if not raw:
            return
        repo = raw.get("repository", {}).get("id") or raw.get("repository", {}).get("name")
        pipeline = _positive(raw.get("definition", {}).get("id"))
        if not repo or not pipeline or not raw.get("sourceVersion"):
            self.issue("BUILD_SOURCE_UNAVAILABLE", identity=build["id"])
            build["status"] = "partial"
            return
        baseline = self.deployments(project, pipeline)
        build["baseline"] = baseline
        selected = baseline.get("selected")
        prod = selected.get("run", selected) if selected else {}
        branch = raw.get("sourceBranch", "").removeprefix("refs/heads/")
        tips = {}
        for name in {branch, "main"}:
            if not name:
                self.issue("BRANCH_REF_UNAVAILABLE", identity={"repository": repo, "branch": name})
                continue
            tips[name] = self.branch_tip(project, repo, name)
        if not prod.get("sourceVersion"):
            self.issue("PRODUCTION_BASELINE_UNAVAILABLE", identity=repo)
            build["status"] = "partial"
        comparisons = [("branch", tips.get(branch), raw["sourceVersion"]),
                       ("main", tips.get("main"), raw["sourceVersion"]),
                       ("production", prod.get("sourceVersion"), raw["sourceVersion"]),
                       ("main_production", prod.get("sourceVersion"), tips.get("main"))]
        for name, base, target in comparisons:
            build["comparisons"][name] = self.compare(project, repo, base, target, common=name in {"branch", "main"})
        if any(item["status"] != "complete" for item in build["comparisons"].values()):
            build["status"] = "partial"
        if _positive(prod.get("id")):
            response = self.request("report_coverage", {"project": project, "buildId": int(prod["id"])})
            if response:
                build["production_coverage"] = {"build_id": prod["id"], "raw": response["data"],
                                                   "summary": _coverage_summary(response["data"])}

    def collect(self):
        release_values = self.workitems([self.release_id])
        release = next((item for item in release_values if item.get("id") == self.release_id), {})
        self.snapshot["release"] = release
        fields = release.get("fields", {})
        project = fields.get("System.TeamProject")
        self.snapshot["source"].update(project=project, revision=release.get("rev"), url=release.get("url"))
        if "ado" in self.sessions:
            self.snapshot["source"]["organization"] = getattr(self.sessions["ado"], "endpoint", None)
        if release.get("collection_status") == "failed" or not project:
            self.issue("RELEASE_UNAVAILABLE", identity=self.release_id)
            return
        if fields.get("System.WorkItemType") != "Release":
            self.issue("INVALID_RELEASE_TYPE", identity=self.release_id)
            return
        if self.resume_path:
            old_path = self._workspace_path(self.resume_path)
            old = read_release_report(old_path)
            if old["source"]["release_id"] != self.release_id:
                raise WorkbenchError("A resume manifest must identify the requested release.")
            self.snapshot["resume"] = {"manifest_path": str(old_path), "sha256": hashlib.sha256(old_path.read_bytes()).hexdigest(),
                                       "revision": old["source"].get("revision")}
            if old["source"].get("revision") != release.get("rev"):
                self.issue("RESUME_REVISION_CHANGED", identity=self.release_id)
        self.snapshot["compliance"] = self.clinic(release)
        identifiers = _build_ids(release)
        if not identifiers:
            self.issue("NO_BUILD_REFERENCES", warning=True)
        raw_builds = []
        for response in self.parallel([(self.request, ("report_builds", {"project": project, "ids": chunk}))
                                       for chunk in _chunks(identifiers)]):
            if response:
                raw_builds.extend(_items(response["data"]))
        by_id = {_positive(item.get("id")): item for item in raw_builds}
        builds = []
        for identifier in sorted(identifiers):
            raw = by_id.get(identifier)
            item = {"id": identifier, "status": "complete" if raw else "failed", "build": raw,
                    "test_reports": [], "comparisons": {}, "warnings": []}
            builds.append(item)
            if not raw:
                self.issue("BUILD_UNAVAILABLE", identity=identifier)
        self.snapshot["builds"] = builds
        jobs, consumers = [], []
        for build in builds:
            if build["build"]:
                for name, tool in (("timeline", "report_build_timeline"), ("artifacts", "report_build_artifacts"),
                                   ("logs", "report_build_logs"), ("properties", "report_build_properties"), ("coverage", "report_coverage")):
                    jobs.append((self.request, (tool, {"project": project, "buildId": build["id"]})))
                    consumers.append((build, name))
        for (build, name), response in zip(consumers, self.parallel(jobs)):
            build[name] = response["data"] if response else None
            if not response:
                build["status"] = "partial"
            if name == "coverage":
                summary = _coverage_summary(build[name])
                if response and not summary:
                    self.issue("COVERAGE_FORMAT_UNAVAILABLE", identity=build["id"])
                    build["status"] = "partial"
                self.snapshot["coverage"].append({"build_id": build["id"], "source": "ado", "raw": build[name],
                                                  "summary": summary, "status": "complete" if summary else "unavailable"})
        attachments, consumers = [], []
        for build in builds:
            timeline = build.get("timeline") or {}
            records = [record for record in timeline.get("records", []) if record.get("refName") == "generatetestreport"]
            records.sort(key=lambda item: _date(item.get("finishTime")), reverse=True)
            if records:
                attachments.append((self.request, ("report_attachment", {"project": project, "buildId": build["id"],
                                    "timelineId": str(timeline["id"]), "recordId": str(records[0]["id"]),
                                    "type": "test.report", "name": "rtm.json"})))
                consumers.append(build)
            elif build.get("build"):
                build["status"] = "partial"
                self.issue("TEST_REPORT_UNAVAILABLE", identity=build["id"])
        related = _relation_ids(release, initial=True)
        for build, response in zip(consumers, self.parallel(attachments)):
            report = response["data"] if response else None
            if not isinstance(report, dict) or not isinstance(report.get("requirementCoverages"), list):
                self.issue("INVALID_TEST_REPORT", identity=build["id"])
                build["status"] = "partial"
                continue
            if _positive(report.get("release", {}).get("id")) != self.release_id:
                self.issue("TEST_REPORT_RELEASE_MISMATCH", identity=build["id"])
                build["status"] = "partial"
            build["test_reports"].append(report)
            self.snapshot["tests"].append({**report, "build_id": build["id"]})
            self.snapshot["defects"].extend({**item, "build_id": build["id"]} for item in report.get("defectCoverages", []))
            for key in ("requirementCoverages", "testCoverages", "defectCoverages"):
                related.update(value for item in report.get(key, []) if (value := _positive(item.get("id"))))
        # Independent build enrichment shares coalesced repository requests.
        self.parallel([(self.enrich_build, (build, project)) for build in builds])
        workitems, visited = [], {self.release_id}
        self.expand_workitems(related, visited, workitems, project)
        self.snapshot["workitems"] = workitems
        graph, extra = self.graph(builds, workitems)
        self.expand_workitems(extra, visited, workitems, project)
        # Replace commit-link placeholders with retained work item identities.
        nodes = {node["id"]: node for node in graph["nodes"]}
        edges = {edge["id"]: edge for edge in graph["edges"]}
        for item in workitems:
            identifier = item["id"]
            fields = item.get("fields", {})
            kind = "testCase" if fields.get("System.WorkItemType") == "Test Case" else "story"
            node_id = f"wi:{identifier}"
            nodes[node_id] = {"id": node_id, "type": kind, "label": fields.get("System.Title", str(identifier)),
                              "workItemId": identifier, "collection_status": item.get("collection_status", "complete")}
            for target in _relation_ids(item):
                relation = next((value.get("rel") for value in item.get("relations", [])
                                 if re.search(rf"/workitems/{target}(?:$|[/?#])", value.get("url", ""), re.I)), "")
                edge_kind = "testedBy" if relation == "Microsoft.VSTS.Common.TestedBy-Forward" else "contains"
                edge_id = f"{edge_kind}:{node_id}:wi:{target}"
                edges[edge_id] = {"id": edge_id, "from": node_id, "to": f"wi:{target}", "type": edge_kind}
        graph.update(nodes=list(nodes.values()), edges=list(edges.values()))
        self.snapshot["graph"] = graph
        actual_ids = {item["id"] for item in workitems if item.get("collection_status") != "failed"}
        graph["unresolvedStoryIds"] = sorted(extra - actual_ids)
        if graph["unlinkedCommits"]:
            graph["warnings"].append("Some commits have no linked work items.")
        if graph["unresolvedStoryIds"]:
            graph["warnings"].append("Some work item links are unresolved.")
        self.snapshot["sonarqube"] = self.parallel([(self.sonar, (build,)) for build in builds if build.get("build")])
        # Recheck the release revision to avoid claiming an atomic snapshot while
        # the source record changes during a long-running collection.
        fresh = self.request("report_work_items", {"ids": [self.release_id], "project": project})
        if fresh:
            latest = next((item for item in _items(fresh["data"]) if item.get("id") == self.release_id), {})
            if latest.get("rev") != release.get("rev"):
                self.issue("RELEASE_CHANGED_DURING_COLLECTION", identity=self.release_id)
        self.snapshot["collection_status"] = "partial" if self.snapshot["errors"] else "complete"

    def _workspace_path(self, value):
        supplied = Path(value).expanduser()
        supplied = supplied if supplied.is_absolute() else self.workspace / supplied
        if any(part.is_symlink() for part in (supplied, *supplied.parents)):
            raise WorkbenchError("Report paths must not use symlinks.")
        path = supplied.resolve()
        if not path.is_relative_to(self.workspace):
            raise WorkbenchError("Report paths must remain inside the selected workspace.")
        return path

    def finish(self):
        for session in self.sessions.values():
            session.close()
        metrics = {name: session.metrics for name, session in self.sessions.items()}
        self.snapshot["metrics"] = {"elapsed_seconds": time.monotonic() - self.started, "cache_hits": self.cache_hits,
                                    "requests": sum(value.get("requests", 0) for value in metrics.values()),
                                    "sessions": {key: value.get("sessions", 1) for key, value in metrics.items()},
                                    "sources": metrics, "tool_calls": len(self.events)}
        self.snapshot["warnings"].sort(key=lambda value: json.dumps(value, sort_keys=True))
        self.snapshot["errors"].sort(key=lambda value: json.dumps(value, sort_keys=True))
        evidence = list(self.evidence)
        for name in ("requests.jsonl", "checkpoint.json"):
            path = self.directory / name
            if path.exists():
                evidence.append(artifact_record(path, self.directory))
        return write_report_snapshot(self.directory, self.snapshot, evidence)


def _collect(release_id, resource: Resource, context: Context, *, output_dir=None, resume=None):
    collector = _Collector(release_id, resource, context, resume)
    try:
        collector.collect()
    except Exception as error:
        collector.issue(getattr(error, "code", "COLLECTION_FAILED"))
        if collector.snapshot["release"].get("fields"):
            collector.snapshot["collection_status"] = "partial"
    finally:
        manifest = collector.finish()
    retained = manifest
    if output_dir:
        target = collector._workspace_path(output_dir)
        if target.exists():
            raise WorkbenchError("Select a new report output directory.")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(manifest.parent, target)
        manifest = target / manifest.name
    return {"status": "SUCCEEDED" if collector.snapshot["collection_status"] != "failed" else "FAILED",
            "manifest_path": str(manifest), "retained_manifest_path": str(retained),
            "collection_status": collector.snapshot["collection_status"],
            "source": collector.snapshot["source"], "metrics": collector.snapshot["metrics"],
            "limitations": ["Collection is engineering evidence, not release approval.",
                            "Compliance content remains in the separately linked Release Clinic document."]}


def collect_release_report(release_id, workspace, *, resource_id="release-report", output_dir=None, resume=None):
    """Public data API. All external reads run under one registered action."""
    from .runtime import Workbench
    arguments = {"release_id": release_id}
    if output_dir is not None:
        arguments["output_dir"] = str(output_dir)
    if resume is not None:
        arguments["resume"] = str(resume)
    action = Workbench(workspace).call(resource_id, "collect", arguments)
    if not action.get("result"):
        raise WorkbenchError(action.get("error") or "Release report collection failed.")
    return {**action["result"], "action_id": action["id"]}
