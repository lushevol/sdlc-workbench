"""Derive concise presentation checks from retained release evidence.

These checks describe observed failures and evidence limits. They do not supply
release approval, new quality thresholds, or cross-build test aggregation.
"""

from __future__ import annotations

import hashlib
import json


def _object(value):
    return value if isinstance(value, dict) else {}


def _array(value):
    return value if isinstance(value, list) else []


def _count(value):
    return value if type(value) is int and value >= 0 else None


def _value(value):
    return str(value) if isinstance(value, (str, int, float)) and not isinstance(value, bool) else ""


def _reason(record):
    return next((_value(record.get(key)) for key in ("failureReason", "errorMessage", "message")
                 if _value(record.get(key))), "")


_ERROR_REASONS = {
    "TOOL_NOT_GRANTED": "The workspace does not grant this exact source read.",
    "DEADLINE_EXCEEDED": "The collection deadline expired before this read completed.",
    "CONNECTOR_TIMEOUT": "The source read exceeded its time limit.",
    "CONNECTOR_UNAVAILABLE": "The configured connector process could not start.",
    "WORK_ITEM_UNAVAILABLE": "The source did not return the requested work item.",
    "BUILD_UNAVAILABLE": "The source did not return the requested build.",
    "TEST_REPORT_UNAVAILABLE": "No matching test report attachment was found in the build timeline.",
    "INVALID_TEST_REPORT": "The attachment did not contain the expected requirement coverage records.",
    "TEST_REPORT_RELEASE_MISMATCH": "The test attachment identifies a different release.",
    "PRODUCTION_BASELINE_UNAVAILABLE": "No qualifying production deployment was found for this comparison.",
    "BRANCH_REF_UNAVAILABLE": "The requested branch did not return an exact commit reference.",
    "COMPARISON_SOURCE_UNAVAILABLE": "A required base or target commit identity is unavailable.",
    "COMPARISON_COUNTS_UNAVAILABLE": "The comparison did not return valid ahead and behind counts.",
    "COMPARISON_INCOMPLETE": "The comparison ended before all changes were returned.",
    "PAGINATION_STALLED": "The source repeated a page, so the collection could not finish safely.",
    "PAGINATION_INCOMPLETE": "The source returned fewer records than its reported total.",
    "ENTITY_LIMIT": "The collection reached the configured record limit.",
    "COVERAGE_FORMAT_UNAVAILABLE": "The retained coverage format has no supported numeric summary.",
    "RESUME_REVISION_CHANGED": "The release revision differs from the previous report.",
    "RELEASE_CHANGED_DURING_COLLECTION": "The release changed while its related records were collected.",
}


def release_checks(snapshot: dict) -> list[dict]:
    """Return stable, plain-text failures, warnings, and unavailable checks.

    Each entry has id, severity, title, reason, section, entity, and source.
    Section values match the report navigation. Failed checks sort first.
    """
    checks = {}

    def add(severity, title, reason, section, *, entity="", source="", identity=None, build_id=None, build_ids=None):
        # Deduplicate by source identity, not by HTML order or error wording.
        key = json.dumps([section, identity if identity is not None else [entity, title, reason]],
                         sort_keys=True, separators=(",", ":"), default=str)
        identifier = "check-" + hashlib.sha256(key.encode()).hexdigest()[:16]
        record = {"id": identifier, "severity": severity, "title": title,
                  "reason": reason, "section": section, "entity": entity, "source": source}
        if build_id is not None:
            record["build_id"] = build_id
        if build_ids:
            record["build_ids"] = list(build_ids)
        checks.setdefault(identifier, record)

    for index, item in enumerate(_array(snapshot.get("builds"))):
        item = _object(item)
        raw = _object(item.get("build"))
        identity = item.get("id", raw.get("id", "Unknown"))
        entity = f"Build {identity}"
        source = f"builds[{index}]"
        result = _value(raw.get("result")).lower().replace("_", "")
        if result in {"failed", "partiallysucceeded", "canceled", "cancelled"}:
            reasons = []
            if _reason(raw):
                reasons.append(_reason(raw))
            for record in _array(_object(item.get("timeline")).get("records")):
                record = _object(record)
                if _value(record.get("result")).lower() not in {"failed", "partiallysucceeded", "canceled"}:
                    continue
                for issue in _array(record.get("issues")):
                    issue = _object(issue)
                    if issue.get("message") and _value(issue.get("type")).lower() in {"error", ""}:
                        prefix = _value(record.get("name"))
                        reasons.append((prefix + ": " if prefix else "") + _value(issue["message"]))
            reason = " ".join(dict.fromkeys(reasons)) or "No failure reason was provided in the retained build evidence."
            add("failed", "Build " + ("failed" if result == "failed" else "partially succeeded" if result == "partiallysucceeded" else "canceled"),
                reason, "builds", entity=entity, source=source, identity=["build-result", identity], build_id=identity)
        else:
            for record_index, record in enumerate(_array(_object(item.get("timeline")).get("records"))):
                record = _object(record)
                if _value(record.get("result")).lower() not in {"failed", "partiallysucceeded", "canceled"}:
                    continue
                messages = [_value(_object(issue).get("message")) for issue in _array(record.get("issues"))
                            if _value(_object(issue).get("type")).lower() in {"error", ""}
                            and _value(_object(issue).get("message"))]
                title = _value(record.get("name")) or "Unnamed build step"
                add("failed", "Build step failed: " + title,
                    " ".join(dict.fromkeys(messages)) or "No failure reason was provided for this timeline step.",
                    "builds", entity=entity, source=source + f".timeline.records[{record_index}]",
                    identity=["build-step", identity, record.get("id", title)], build_id=identity)
        if item.get("status") in {"failed", "partial", "unavailable"}:
            add("unavailable", "Build evidence is incomplete", _value(item.get("reason")) or
                "Some requested build information is unavailable. Inspect the source-read errors for the cause.",
                "builds", entity=entity, source=source, identity=["build-evidence", identity], build_id=identity)

        for name, comparison in _object(item.get("comparisons")).items():
            if name not in {"branch", "main", "production", "main_production"}:
                continue
            comparison = _object(comparison)
            label = {"branch": "Branch tip", "main": "Main branch", "production": "Production baseline",
                     "main_production": "Main and production"}[name]
            ahead, behind = _count(comparison.get("aheadCount")), _count(comparison.get("behindCount"))
            comparison_source = source + ".comparisons." + name
            if comparison.get("status") != "complete" or ahead is None or behind is None:
                add("unavailable", label + " comparison unavailable", _value(comparison.get("reason")) or
                    "A complete comparison with valid ahead and behind counts was not retained.", "builds",
                    entity=entity, source=comparison_source, identity=["comparison", identity, name], build_id=identity)
                continue
            if name == "branch" and (ahead or behind):
                add("failed", "Candidate is not the branch tip",
                    f"The candidate is {ahead} commit(s) ahead and {behind} commit(s) behind the collected branch tip.",
                    "builds", entity=entity, source=comparison_source, identity=["comparison", identity, name], build_id=identity)
            elif name in {"main", "production"} and behind:
                baseline = "main" if name == "main" else "production"
                add("failed", f"Candidate is behind {baseline}",
                    f"The candidate lacks {behind} commit(s) from {baseline}. Merge-only exceptions were not evaluated.",
                    "builds", entity=entity, source=comparison_source, identity=["comparison", identity, name], build_id=identity)
            elif name == "main_production" and (ahead or behind or any(
                    type(value) is int and value > 0 for value in _object(comparison.get("changeCounts")).values())):
                add("failed", "Main and production differ",
                    f"Main is {ahead} commit(s) ahead and {behind} commit(s) behind production. Merge-only exceptions were not evaluated.",
                    "builds", entity=entity, source=comparison_source, identity=["comparison", identity, name], build_id=identity)

    # Requirement counts remain independent for each build. Do not add them.
    for report_index, report in enumerate(_array(snapshot.get("tests"))):
        report = _object(report)
        build_id = report.get("build_id", report.get("buildId", "Unknown"))
        for requirement_index, requirement in enumerate(_array(report.get("requirementCoverages"))):
            requirement = _object(requirement)
            requirement_id = requirement.get("id", "Unknown")
            counts = _object(_object(requirement.get("testExecutionStatusStats")).get("countByType"))
            failed = _count(counts.get("FAILED", requirement.get("failed")))
            blocked = _count(counts.get("BLOCKED"))
            unexecuted = _count(counts.get("NO_EXECUTION"))
            deferred = _count(counts.get("DEFERRED"))
            entity = f"Build {build_id} · Requirement {requirement_id}"
            source = f"tests[{report_index}].requirementCoverages[{requirement_index}]"
            if failed:
                reason = _reason(requirement) or "The report does not provide the individual failure reasons."
                add("failed", "Tests failed", f"{failed} failed test(s) are recorded for this requirement. {reason}",
                    "workitems", entity=entity, source=source, identity=["test-failures", build_id, requirement_id], build_id=build_id)
            incomplete = [("blocked", blocked), ("not executed", unexecuted), ("deferred", deferred)]
            incomplete = [f"{count} {label}" for label, count in incomplete if count]
            if incomplete:
                add("unavailable", "Tests have incomplete execution", ", ".join(incomplete) +
                    ". These results do not establish passing execution.", "workitems", entity=entity, source=source,
                    identity=["test-incomplete", build_id, requirement_id], build_id=build_id)
        for testcase_index, testcase in enumerate(_array(report.get("testCoverages"))):
            testcase = _object(testcase)
            if _value(testcase.get("status")).lower() not in {"failed", "fail"}:
                continue
            add("failed", "Test case failed", _reason(testcase) or "No failure reason was provided in the retained test result.",
                "workitems", entity=f"Build {build_id} · Test {testcase.get('id', 'Unknown')}",
                source=f"tests[{report_index}].testCoverages[{testcase_index}]",
                identity=["test-case", build_id, testcase.get("id"), testcase.get("testRunId"), testcase.get("testResultId")], build_id=build_id)

    # One Sonar response can serve several builds. Show its gate failure once.
    sonar_groups = {}
    for index, item in enumerate(_array(snapshot.get("sonarqube"))):
        item = _object(item)
        gate = _object(item.get("gate"))
        gate = _object(gate.get("projectStatus", gate))
        selector = {key: item.get(key) for key in ("component", "branch", "pullRequest", "association_status", "current_analysis")}
        key = json.dumps([selector, gate, item.get("status")], sort_keys=True, default=str)
        group = sonar_groups.setdefault(key, {"item": item, "gate": gate, "builds": set(), "source": f"sonarqube[{index}]"})
        if item.get("build_id") is not None:
            group["builds"].add(str(item["build_id"]))
    for key, group in sonar_groups.items():
        item, gate = group["item"], group["gate"]
        entity = "SonarQube " + (_value(item.get("component")) or "project unavailable")
        builds = ", ".join(sorted(group["builds"]))
        association = (f" Current analysis; association with build(s) {builds or 'unknown'} is unverified."
                       if item.get("association_status") != "matched" else "")
        failed_conditions = [_object(value) for value in _array(gate.get("conditions"))
                             if _value(_object(value).get("status")).upper() == "ERROR"]
        status = _value(gate.get("status")).upper()
        if status == "ERROR" or failed_conditions:
            reasons = []
            for condition in failed_conditions:
                metric = _value(condition.get("metricKey")) or "Metric unavailable"
                actual = _value(condition.get("actualValue")) or "unavailable"
                threshold = _value(condition.get("errorThreshold")) or "unavailable"
                comparator = {"GT": ">", "LT": "<", "EQ": "="}.get(condition.get("comparator"),
                    _value(condition.get("comparator")) or "comparator unavailable")
                reasons.append(f"{metric}: observed {actual}; failure condition {comparator} {threshold}.")
            reason = " ".join(reasons) or _reason(gate) or "SonarQube returned ERROR without failed condition details."
            add("failed", "Quality gate failed", reason + association, "quality", entity=entity,
                source=group["source"] + ".gate", identity=["sonar-gate", key], build_ids=sorted(group["builds"]))
        elif status == "WARN":
            add("warning", "Quality gate warning", (_reason(gate) or "SonarQube returned WARN without condition details.") + association,
                "quality", entity=entity, source=group["source"] + ".gate", identity=["sonar-gate", key], build_ids=sorted(group["builds"]))
        if item.get("status") in {"partial", "failed", "unavailable"} or not status or status == "NONE":
            add("unavailable", "SonarQube evidence is incomplete", _value(item.get("reason")) or
                "A complete quality gate and analysis response was not retained.", "quality", entity=entity,
                source=group["source"], identity=["sonar-evidence", key], build_ids=sorted(group["builds"]))

    for index, defect in enumerate(_array(snapshot.get("defects"))):
        defect = _object(defect)
        state = _value(defect.get("status", _object(defect.get("fields")).get("System.State")))
        if state.lower() in {"open", "active", "new", "in progress", "in_progress"}:
            identifier = defect.get("id", "Unknown")
            build = defect.get("build_id")
            add("warning", "Defect remains open", f"The defect state is {state}." +
                (f" Severity: {_value(defect['severity'])}." if _value(defect.get("severity")) else ""),
                "workitems", entity=f"Defect {identifier}" + (f" · Build {build}" if build is not None else ""),
                source=f"defects[{index}]", identity=["defect", identifier, build], build_id=build)

    for category in ("errors", "warnings"):
        for index, value in enumerate(_array(snapshot.get(category))):
            item = _object(value)
            code = _value(item.get("code"))
            reason = _value(item.get("message")) if item else _value(value)
            default = "The requested report information is unavailable."
            if not reason or reason == default:
                if code.startswith("HTTP_"):
                    reason = "The source returned HTTP " + code.removeprefix("HTTP_") + "."
                else:
                    reason = _ERROR_REASONS.get(code, "No further reason was provided in the retained collection result.")
            tool = _value(item.get("tool"))
            if tool:
                reason += " Source read: " + tool + "."
            identity = item.get("identity")
            entity = ""
            if isinstance(identity, (str, int)):
                entity = "Source record " + str(identity)
            elif isinstance(identity, dict):
                if identity.get("buildId"):
                    entity = "Build " + str(identity["buildId"])
                elif identity.get("repository"):
                    entity = "Repository " + str(identity["repository"])
            add("unavailable" if category == "errors" else "warning", code.replace("_", " ").capitalize()
                if code else "Collection warning", reason, "evidence", entity=entity,
                source=f"{category}[{index}]", identity=[category, code, identity, tool, reason],
                build_id=identity.get("buildId") if isinstance(identity, dict) else None)

    order = {"failed": 0, "unavailable": 1, "warning": 2}
    return sorted(checks.values(), key=lambda item: (order[item["severity"]], item["section"], item["entity"], item["title"], item["id"]))
