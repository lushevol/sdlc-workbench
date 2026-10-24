"""Render retained release data without querying ADO, SonarQube, or Release Clinic."""

from __future__ import annotations

import html
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote, urlsplit

from .models import WorkbenchError
from .release_report_contract import confined_artifact, load_report_bundle

_PREVIEW_LIMIT = 24000
_CELL_LIMIT = 1200
_ROW_LIMIT = 500
_CARD_LIMIT = 50
_CLINIC_PREFIX = re.compile(r"^(?:TDAReport_|TDA_Report_|Annotated_TDA_Report_|Annotated_TDAReport_)", re.IGNORECASE)


def _json_preview(value, limit: int) -> tuple[str, bool]:
    """Encode only the visible prefix instead of duplicating every nested record."""
    parts, remaining = [], limit
    for part in json.JSONEncoder(indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False).iterencode(value):
        if len(part) > remaining:
            parts.append(part[:remaining])
            return "".join(parts), True
        parts.append(part)
        remaining -= len(part)
    return "".join(parts), False


def _text(value) -> str:
    if value is None or value == "":
        return "Unavailable"
    if isinstance(value, (dict, list)):
        value, truncated = _json_preview(value, _CELL_LIMIT)
    else:
        value = str(value)
        truncated = len(value) > _CELL_LIMIT
        value = value[:_CELL_LIMIT]
    if truncated:
        value += " … [complete value in snapshot]"
    return html.escape(value, quote=True)


def _object(value) -> dict:
    return value if isinstance(value, dict) else {}


def _array(value) -> list:
    return value if isinstance(value, list) else []


def _percentage(value) -> str:
    if type(value) not in {int, float} or not 0 <= value <= 100:
        return _text(None)
    return f"{value:.2f}".rstrip("0").rstrip(".") + "%"


def _http_url(value) -> str | None:
    if not isinstance(value, str) or not value or len(value) > 8192 or "\\" in value or any(ord(char) <= 32 or ord(char) == 127 for char in value):
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname or parsed.username is not None or parsed.password is not None:
            return None
        parsed.port
    except ValueError:
        return None
    return value


def _local_href(path: Path, output: Path) -> str | None:
    try:
        relative = os.path.relpath(path.resolve(), output.parent.resolve())
    except ValueError:
        return None
    return quote(Path(relative).as_posix(), safe="/.-_")


def _anchor(label, url) -> str:
    valid = _http_url(url)
    if valid is None:
        return _text(label)
    return f'<a href="{html.escape(valid, quote=True)}" target="_blank" rel="noopener noreferrer">{_text(label)}</a>'


def _file_anchor(label, path: Path, output: Path) -> str:
    href = _local_href(path, output)
    if href is None:
        return _text(label)
    return f'<a href="{html.escape(href, quote=True)}">{_text(label)}</a>'


def _record_link(record: dict, label=None) -> str:
    links = _object(record.get("_links"))
    web = _object(links.get("web")).get("href")
    return _anchor(label if label is not None else record.get("id", "Source"), web or record.get("url"))


def _table(headers: list[str], rows: list[list[str]], empty: str = "No records were collected.") -> str:
    if not rows:
        return f'<p class="muted">{html.escape(empty)}</p>'
    note = f'<p class="notice">Showing the first {_ROW_LIMIT} of {len(rows)} rows. Complete records remain in the normalized snapshot.</p>' if len(rows) > _ROW_LIMIT else ""
    return note + '<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th scope="col">{html.escape(header)}</th>' for header in headers) + \
        '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>' for row in rows[:_ROW_LIMIT]) + '</tbody></table></div>'


def _details(label: str, value, snapshot_path: Path, output: Path) -> str:
    raw, truncated = _json_preview(value, _PREVIEW_LIMIT)
    note = ""
    if truncated:
        note = '<p class="notice">Display preview is truncated. The complete value remains in the ' + \
            _file_anchor("normalized snapshot", snapshot_path, output) + '.</p>'
    return f'<details class="disclosure raw-data"><summary><span>{html.escape(label)}</span><span class="summary-note">Source data</span></summary>{note}<pre>{html.escape(raw, quote=True)}</pre></details>'


def _clinic_file(record: dict, root: Path, release_id) -> Path | None:
    value = record.get("path")
    if not isinstance(value, str) or not value or "\x00" in value or value.startswith("~") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        return None
    path = Path(value)
    candidate = path if path.is_absolute() else root / path
    if candidate.is_symlink() or not candidate.is_file() or candidate.suffix.lower() not in {".html", ".htm"}:
        return None
    if not _CLINIC_PREFIX.match(candidate.name):
        return None
    # Local files need their own release association; attachment relations provide that association remotely.
    if re.search(rf"_{re.escape(str(release_id))}(?: \(\d+\))?$", candidate.stem) is None:
        return None
    return candidate.resolve()


def _compliance(snapshot: dict, root: Path, output: Path) -> tuple[str, set[Path]]:
    rows = []
    protected = set()
    for item in _array(_object(snapshot.get("compliance")).get("links")):
        if not isinstance(item, dict):
            continue
        label = item.get("name") or "Release Clinic report"
        if _http_url(item.get("url")) is not None:
            link = _anchor(label, item["url"])
        else:
            path = _clinic_file(item, root, _object(snapshot.get("source")).get("release_id"))
            if path is None:
                continue
            protected.add(path)
            link = _file_anchor(label, path, output)
        rows.append([link, _text(item.get("source_kind")), _text(item.get("added_at"))])
    if not rows:
        return '<p class="notice">Release Clinic report unavailable</p>', protected
    body = '<p>Open the separate Release Clinic document for compliance content.</p>' + \
        _table(["Release Clinic document", "Source", "Recorded date"], rows)
    return body, protected


def _badge(label, tone="neutral"):
    return f'<span class="badge {tone}">{_text(label)}</span>'


def _date_label(value):
    from datetime import datetime
    try:
        date = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        zone = " UTC" if date.tzinfo and date.utcoffset().total_seconds() == 0 else date.strftime(" %z") if date.tzinfo else ""
        return date.strftime("%d %b %Y · %H:%M") + zone
    except (ValueError, TypeError):
        return str(value) if value else "Unavailable"


def _number(value):
    return value if type(value) in (int, float) and value >= 0 else None


def _short_commit(value):
    return f'<code title="{_text(value)}">{_text(str(value)[:10])}</code>' if value else '<span class="muted">Unavailable</span>'


def _disclosure(label, content, *, identifier=None, summary_note="", css=""):
    identity = f' id="{identifier}"' if identifier else ""
    return f'<details{identity} class="disclosure {css}"><summary><span>{html.escape(label)}</span><span class="summary-note">{html.escape(summary_note)}</span></summary><div class="disclosure-body">{content}</div></details>'


def _check_rows(checks):
    rows = []
    for item in checks:
        severity = item["severity"]
        label = {"failed": "Failed", "warning": "Review", "unavailable": "Unavailable"}[severity]
        entity = '<span class="check-entity">' + _text(item["entity"]) + '</span>' if item.get("entity") else ""
        section = "supporting-evidence" if item["section"] == "evidence" else item["section"]
        rows.append(f'<li class="check-item {severity}" data-severity="{severity}"><span class="check-mark" aria-hidden="true">{"×" if severity == "failed" else "!"}</span>'
                    f'<div class="check-copy">{entity}<div class="check-title">{_text(item["title"])} {_badge(label, severity)}</div>'
                    f'<p class="check-reason">{_text(item["reason"])}</p></div><a class="check-jump" href="#{section}" aria-label="View {_text(item["title"])}">View <span aria-hidden="true">↗</span></a></li>')
    return '<ul class="check-list">' + ''.join(rows) + '</ul>'


def _attention(checks):
    failed = [item for item in checks if item["severity"] == "failed"]
    failed.sort(key=lambda item: (0 if item["section"] == "builds" and ".comparisons." not in item.get("source", "")
                                 else {"quality": 1, "workitems": 2, "builds": 3, "evidence": 4}[item["section"]],
                                 item.get("entity", ""), item["title"]))
    warnings = [item for item in checks if item["severity"] == "warning"]
    unavailable = [item for item in checks if item["severity"] == "unavailable"]
    title = "Needs attention" if failed else "Review observations" if warnings else "Evidence is incomplete" if unavailable else "No failed checks reported"
    label = f'{len(failed)} failed check' + ("s" if len(failed) != 1 else "")
    tone = "failed" if failed else "warning" if warnings or unavailable else "neutral"
    heading = f'<div class="section-heading"><div><div class="eyebrow">Review first</div><h2>{title}</h2></div>{_badge(label, tone)}</div>'
    if failed or warnings:
        body = '<p class="attention-guide">Each failed check includes its recorded reason. Scroll to review all observations.</p>' + _check_rows(failed + warnings)
    else:
        body = '<p class="empty-state">' + ("Some checks could not be evaluated. Open the missing evidence below." if unavailable else "The collected sources report no failures. This is not a deployment approval.") + '</p>'
    if unavailable:
        body += _disclosure("Missing evidence", _check_rows(unavailable), summary_note=f'{len(unavailable)} unavailable', css="evidence-gaps")
    return f'<section id="attention" class="panel attention {tone}" data-failed-count="{len(failed)}" data-unavailable-count="{len(unavailable)}">{heading}{body}</section>'


def _coverage_metric(label, current, production):
    value = _percentage(current)
    delta = ""
    if _number(current) is not None and _number(production) is not None:
        difference = round(current - production, 1)
        if difference:
            delta = f'<span class="metric-delta {"down" if difference < 0 else "up"}">{difference:+g} pp <span>vs PROD</span></span>'
        else:
            delta = '<span class="metric-baseline">Same as PROD</span>'
    width = min(100, max(0, current)) if _number(current) is not None else 0
    return f'<div class="coverage-metric"><span class="metric-label">{label}</span><div class="metric-value">{value}{delta}</div><div class="meter" aria-hidden="true"><span style="width:{width:g}%"></span></div></div>'


def _comparison_rows(comparisons):
    labels = {"branch": "Latest branch commit", "main": "Against main", "production": "Against PROD", "main_production": "Main ↔ PROD"}
    rows = []
    for name, value in comparisons.items():
        value = _object(value)
        rows.append([_text(labels.get(name, name)), _short_commit(value.get("base")), _short_commit(value.get("target")),
                     _text(value.get("aheadCount")), _text(value.get("behindCount")), _badge(value.get("status", "unavailable")), _text(value.get("reason"))])
    return _table(["Comparison", "Base commit", "Target commit", "Ahead", "Behind", "Data", "Reason"], rows)


def _build_card(item, coverage, checks, reports):
    raw = _object(item.get("build"))
    identifier = item.get("id", raw.get("id"))
    repo = _object(raw.get("repository"))
    repo_name = repo.get("name", repo.get("id")) or f"Build {identifier}"
    result = raw.get("result") or raw.get("status") or "Unavailable"
    related = [check for check in checks if str(check.get("build_id")) == str(identifier) and check["section"] == "builds"]
    failed = [check for check in related if check["severity"] == "failed"]
    tone = "failed" if str(result).lower() in {"failed", "partiallysucceeded", "canceled"} else "success" if result == "succeeded" else "neutral"
    status_label = "Build failed" if str(result).lower() == "failed" else "Build succeeded" if result == "succeeded" else str(result)
    branch = str(raw.get("sourceBranch", "")).removeprefix("refs/heads/") or "Unavailable"
    top = f'<div class="build-heading"><div><h3>{_record_link(raw, repo_name)}</h3><div class="build-ref">Build {_record_link(raw, identifier)} <span>·</span> {_text(raw.get("buildNumber"))}</div></div>{_badge(status_label, tone)}</div>'
    top += f'<div class="branch-line"><span class="branch-label">⑂</span><span>{_text(branch)}</span>{_short_commit(raw.get("sourceVersion"))}</div>'
    if related:
        notes = ''.join(f'<div class="inline-check {check["severity"]}"><span aria-hidden="true">{"×" if check["severity"] == "failed" else "!"}</span><div><strong>{_text(check["title"])}</strong><p>{_text(check["reason"])}</p></div></div>' for check in related)
        top += notes
    elif raw:
        top += '<div class="quiet-check">Comparison data has no reported exceptions.</div>'
    current = _object(coverage.get("summary"))
    if not current:
        current = {"line_coverage": coverage.get("lineCoverage"), "branch_coverage": coverage.get("branchCoverage")}
    production = _object(_object(item.get("production_coverage")).get("summary"))
    top += '<div class="coverage-grid">' + _coverage_metric("ADO line coverage", current.get("line_coverage"), production.get("line_coverage")) + _coverage_metric("ADO branch coverage", current.get("branch_coverage"), production.get("branch_coverage")) + '</div>'
    for report in reports:
        if str(report.get("build_id", report.get("buildId"))) == str(identifier):
            count = len(_array(report.get("testCoverages")))
            top += f'<div class="build-footnote">{count} test case' + ("s" if count != 1 else "") + ' · <a href="#workitems">View test evidence ↗</a></div>'
    top += _disclosure("Commit comparisons", _comparison_rows(_object(item.get("comparisons"))), summary_note=f'{len(_object(item.get("comparisons")))} comparisons')
    return f'<article id="build-{_text(identifier)}" class="build-card {"has-failure" if failed else ""}">{top}</article>'


def _count_chips(counts, *, defect=False):
    labels = [("OPEN", "Open", "failed"), ("IN_PROGRESS", "In progress", "warning"), ("CLOSED", "Closed", "success")] if defect else [
        ("FAILED", "Failed", "failed"), ("BLOCKED", "Blocked", "warning"), ("NO_EXECUTION", "Not run", "warning"),
        ("DEFERRED", "Deferred", "warning"), ("PASSED", "Passed", "success")]
    chips = [_badge(f'{value:g} {label.lower()}', tone) for key, label, tone in labels if (value := _number(counts.get(key))) is not None and value > 0]
    return '<div class="count-chips">' + ''.join(chips) + '</div>' if chips else '<span class="muted">No reported counts</span>'


def _workitems(snapshot):
    reports = [_object(item) for item in _array(snapshot.get("tests"))]
    evidence = {}
    test_rows = []
    for report in reports:
        build_id = report.get("build_id", report.get("buildId"))
        for requirement in _array(report.get("requirementCoverages")):
            requirement = _object(requirement)
            counts = _object(_object(requirement.get("testExecutionStatusStats")).get("countByType"))
            if not counts:
                counts = {"PASSED": requirement.get("passed"), "FAILED": requirement.get("failed")}
            defect_counts = _object(_object(requirement.get("defectStatusStats")).get("countByType"))
            evidence.setdefault(str(requirement.get("id")), []).append((build_id, counts, defect_counts))
            test_rows.append([_text(build_id), _anchor(requirement.get("id"), requirement.get("permalink")),
                              _text(counts.get("PASSED")), _text(counts.get("FAILED")), _text(counts.get("NO_EXECUTION")), _text(counts.get("BLOCKED")), _text(counts.get("DEFERRED"))])
    rows = []
    for item in _array(snapshot.get("workitems")):
        item = _object(item)
        values = _object(item.get("fields"))
        test_parts, defect_parts = [], []
        for build_id, counts, defects in evidence.get(str(item.get("id")), []):
            test_parts.append('<div class="build-counts"><span class="build-count-label">Build ' + _text(build_id) + '</span>' + _count_chips(counts) + '</div>')
            defect_parts.append('<div class="build-counts"><span class="build-count-label">Build ' + _text(build_id) + '</span>' + _count_chips(defects, defect=True) + '</div>')
        rows.append([_record_link(item), '<span class="item-title">' + _text(values.get("System.Title")) + '</span>',
                     _text(values.get("System.WorkItemType")), _badge(values.get("System.State", "Unavailable")),
                     ''.join(test_parts) or '<span class="muted">No linked test counts</span>', ''.join(defect_parts) or '<span class="muted">Unavailable</span>'])
    aggregation = _object(snapshot.get("test_aggregation")).get("message") or "Cross-build aggregation rule is unavailable. Counts remain separate for each build."
    body = '<div class="section-heading"><div><div class="eyebrow">Scope & verification</div><h2>Work items and tests</h2></div><span class="section-count">' + str(len(rows)) + ' work items</span></div>'
    body += '<p class="section-description">Review test outcomes beside each requirement. Counts remain separate for every build.</p>'
    body += _disclosure("Related work items", _table(["ID", "Title", "Type", "State", "Test cases", "Test bugs"], rows), summary_note=f'{len(rows)} records')
    body += _disclosure("Test execution by build", '<p class="small-note">' + _text(aggregation) + '</p>' + _table(["Build", "Requirement", "Passed", "Failed", "No execution", "Blocked", "Deferred"], test_rows), summary_note=f'{len(reports)} test reports')
    defect_rows = []
    for item in _array(snapshot.get("defects")):
        item = _object(item)
        defect_rows.append([_anchor(item.get("id"), item.get("permalink", item.get("url"))), _text(item.get("name", item.get("title"))),
                            _badge(item.get("status", item.get("state", "Unavailable"))), _text(item.get("severity")), _text(item.get("build_id"))])
    body += _disclosure("Defect records", _table(["ID", "Title", "State", "Severity", "Build"], defect_rows), summary_note=f'{len(defect_rows)} build records')
    return '<section id="workitems" class="panel">' + body + '</section>'


def _quality(snapshot):
    cards = []
    groups = {}
    for item in _array(snapshot.get("sonarqube")):
        item = _object(item)
        # Share cards only for identical observations. The same selector can
        # have different analysis associations for different build revisions.
        key = json.dumps({name: value for name, value in item.items() if name != "build_id"},
                         sort_keys=True, ensure_ascii=False)
        group = groups.setdefault(key, {"item": item, "builds": []})
        if item.get("build_id") is not None and item["build_id"] not in group["builds"]:
            group["builds"].append(item["build_id"])
    for group in groups.values():
        item = group["item"]
        gate = _object(_object(item.get("gate")).get("projectStatus")) or _object(item.get("gate"))
        status = gate.get("status", "Unavailable")
        tone = "failed" if status in {"ERROR", "FAILED"} else "success" if status == "OK" else "neutral"
        label = "Gate failed" if tone == "failed" else "Gate passed" if status == "OK" else "Gate unavailable"
        heading = f'<div class="build-heading"><div><h3>{_text(item.get("component") or "SonarQube")}</h3><p class="small-note">{_text(item.get("branch") or ("PR " + str(item["pullRequest"]) if item.get("pullRequest") else "No branch identity"))}</p></div>{_badge(label, tone)}</div>'
        heading += '<p class="small-note">' + (" · ".join("Build " + _text(value) for value in group["builds"]) or "Build identity unavailable") + '</p>'
        note = "Current branch snapshot; build association is unverified." if item.get("association_status") == "current_snapshot" else "Analysis matched to the build revision." if item.get("association_status") == "matched" else item.get("reason", "Analysis association is unavailable.")
        heading += '<p class="association-note">' + _text(note) + '</p>'
        conditions = _array(gate.get("conditions"))
        rows = []
        for condition in conditions:
            condition = _object(condition)
            condition_status = condition.get("status", "Unavailable")
            rows.append([_text(condition.get("metricKey")), _badge(condition_status, "failed" if condition_status == "ERROR" else "neutral"),
                         _text(condition.get("actualValue")), _text(condition.get("comparator")), _text(condition.get("errorThreshold"))])
        incomplete = item.get("status") != "complete"
        if incomplete:
            heading += '<p class="small-note">' + _badge("Partial quality data", "warning") + ' Counts show retained records only. Source totals are unavailable.</p>'
        counts = []
        for name in ("issues", "hotspots"):
            values = item.get(name)
            if isinstance(values, list):
                counts.append(f'<span><strong>{len(values)}</strong> {"retained " if incomplete else ""}{name}</span>')
            else:
                counts.append('<span>' + name.capitalize() + ' unavailable</span>')
        heading += '<div class="quality-counts">' + ''.join(counts) + '</div>'
        heading += _disclosure("Quality gate conditions", _table(["Metric", "Status", "Actual", "Comparator", "Threshold"], rows), summary_note=f'{len(rows)} conditions')
        cards.append('<article class="quality-card">' + heading + '</article>')
    return '<section id="quality" class="panel"><div class="section-heading"><div><div class="eyebrow">Code quality</div><h2>SonarQube quality data</h2></div></div><p class="section-description">Source quality gate results. ADO coverage appears on each build card.</p><div class="build-grid">' + (''.join(cards) or '<p class="empty-state">SonarQube data unavailable.</p>') + '</div></section>'


def _render(snapshot: dict, manifest: dict, root: Path, output: Path) -> tuple[str, set[Path]]:
    from .release_report_checks import release_checks
    checks = release_checks(snapshot)
    source = _object(snapshot.get("source"))
    release = _object(snapshot.get("release"))
    fields = _object(release.get("fields"))
    release_id = source.get("release_id")
    snapshot_path = confined_artifact(root, manifest["snapshot"]["path"])
    protected = {snapshot_path}
    builds = [_object(item) for item in _array(snapshot.get("builds"))]
    reports = [_object(item) for item in _array(snapshot.get("tests"))]
    failed = sum(check["severity"] == "failed" for check in checks)
    title = fields.get("System.Title") or f"Release {release_id}"
    state = fields.get("System.State", "Unavailable")
    status = snapshot.get("collection_status", "unavailable")
    status_label = {"complete": "Data collected", "partial": "Partial data", "failed": "Collection failed"}.get(status, "Data unavailable")
    status_tone = "neutral" if status == "complete" else "warning" if status == "partial" else "failed"
    metadata = [("Release ID", _record_link(release, release_id)), ("Planned date", _text(_date_label(fields.get("Custom.PlannedReleaseDate")))),
                ("State", _text(state))]
    for label, value in [("Release approach", fields.get("Custom.ReleaseApproach")),
                         ("Nature of change", fields.get("Custom.NatureoftheChange", fields.get("Custom.NatureOfTheChange")))]:
        if value:
            metadata.append((label, _text(value)))
    metadata_html = ''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for label, value in metadata)
    source_link = _anchor("Open in Azure DevOps ↗", _object(_object(release.get("_links")).get("web")).get("href") or release.get("url"))
    heading = '<header id="overview"><div class="topline"><span class="brand-mark" aria-hidden="true">W</span><span class="brand-name">Workbench</span><span class="breadcrumb-sep">/</span><span>Release report</span><span class="topline-project">' + _text(source.get("project")) + '</span></div>'
    heading += '<div class="hero-title"><div><div class="eyebrow">Release ' + _text(release_id) + '</div><h1>' + _text(title) + '</h1></div><div class="hero-actions">' + _badge(status_label, status_tone) + source_link + '</div></div>'
    heading += f'<dl class="release-meta" style="--meta-count:{len(metadata)}">' + metadata_html + '</dl></header>'
    nav = '<nav class="section-nav" aria-label="Report sections"><a href="#attention">Overview' + (f'<span class="nav-count">{failed}</span>' if failed else '') + '</a><a href="#builds">Builds</a><a href="#workitems">Work items & tests</a><a href="#quality">Code quality</a><a href="#compliance">Compliance</a><a href="#supporting-evidence">Evidence</a></nav>'
    attention = _attention(checks)
    count_tiles = [
        ("Builds", len(builds), "Release components", "#builds"),
        ("Work items", len(_array(snapshot.get("workitems"))), "Related records", "#workitems"),
        ("Test reports", len(reports), "Kept per build", "#workitems"),
    ]
    counts = '<div class="scope-stats">' + ''.join(f'<a href="{target}"><span class="stat-value">{value}</span><span class="stat-copy"><strong>{label}</strong><span>{note}</span></span><span class="stat-arrow" aria-hidden="true">↗</span></a>' for label, value, note, target in count_tiles) + '</div>'
    coverage = {str(item.get("build_id", item.get("buildId"))): item for item in (_object(value) for value in _array(snapshot.get("coverage")))}
    build_cards = [_build_card(item, coverage.get(str(item.get("id")), {}), checks, reports) for item in builds[:_CARD_LIMIT]]
    build_body = '<div class="section-heading"><div><div class="eyebrow">Components</div><h2>Builds and comparisons</h2></div><span class="section-count">' + str(len(builds)) + ' builds</span></div>'
    build_body += '<p class="section-description">Branch alignment, build outcomes, and ADO coverage at a glance.</p>'
    build_body += '<div class="build-grid">' + (''.join(build_cards[:6]) or '<p class="empty-state">No build records were collected.</p>') + '</div>'
    if len(build_cards) > 6:
        build_body += _disclosure("More builds", '<div class="build-grid">' + ''.join(build_cards[6:]) + '</div>', summary_note=f'{len(build_cards) - 6} more')
    if len(builds) > _CARD_LIMIT:
        build_body += f'<p class="small-note">Showing {_CARD_LIMIT} of {len(builds)} build cards. Complete records remain in the ' + _file_anchor("normalized snapshot", snapshot_path, output) + '.</p>'
    compliance, clinic_paths = _compliance(snapshot, root, output)
    protected.update(clinic_paths)
    compliance_section = '<section id="compliance" class="panel clinic-panel"><div class="section-heading"><div><div class="eyebrow">Separate assessment</div><h2>Release compliance</h2></div>' + _badge("Release Clinic") + '</div>' + compliance + '</section>'
    graph = _object(snapshot.get("graph"))
    graph_notes = ''.join('<p class="small-note">' + _text(value) + '</p>' for value in _array(graph.get("warnings")))
    for label, key in (("Unresolved story IDs", "unresolvedStoryIds"), ("Unlinked commits", "unlinkedCommits")):
        if graph.get(key):
            graph_notes += '<p class="small-note"><strong>' + label + ':</strong> ' + _text(graph[key]) + '</p>'
    graph_rows = [[_text(_object(item).get("type")), _text(_object(item).get("label")), _text(_object(item).get("id"))] for item in _array(graph.get("nodes"))]
    relationships = _disclosure("Release relationships", graph_notes + _table(["Type", "Label", "Identity"], graph_rows) + _details("Complete relationship graph", graph, snapshot_path, output), summary_note=f'{len(graph_rows)} nodes · {len(_array(graph.get("edges")))} relationships')
    evidence_rows, seen = [], set()
    for item in [*manifest.get("evidence", []), *snapshot.get("evidence", [])]:
        if item["path"] in seen:
            continue
        seen.add(item["path"])
        path = confined_artifact(root, item["path"])
        protected.add(path)
        evidence_rows.append([_file_anchor(item["path"], path, output), _text(item.get("bytes")), '<code>' + _text(item.get("sha256")) + '</code>'])
    support = '<div class="evidence-intro"><p>Original data and source identities remain available for inspection.</p><p>' + _file_anchor("Open complete report snapshot ↗", snapshot_path, output) + '</p></div>'
    support += '<dl class="source-meta"><div><dt>Collected</dt><dd>' + _text(_date_label(snapshot.get("generated_at"))) + '</dd></div><div><dt>Release revision</dt><dd>' + _text(source.get("revision")) + '</dd></div><div><dt>Snapshot SHA-256</dt><dd><code>' + _text(manifest["snapshot"]["sha256"]) + '</code></dd></div></dl>'
    support += relationships
    support += _details("All release fields and relations", release, snapshot_path, output)
    support += _details("Complete work item records", snapshot.get("workitems", []), snapshot_path, output)
    support += _details("Test reports and execution evidence", snapshot.get("tests", []), snapshot_path, output)
    support += _details("ADO coverage data", snapshot.get("coverage", []), snapshot_path, output)
    support += _details("SonarQube source data", snapshot.get("sonarqube", []), snapshot_path, output)
    support += _disclosure("Retained evidence files", _table(["Artifact", "Bytes", "SHA-256"], evidence_rows), summary_note=f'{len(evidence_rows)} files')
    support += _details("Collection metrics", snapshot.get("metrics", {}), snapshot_path, output)
    support += _details("Complete normalized data", snapshot, snapshot_path, output)
    support += _details("Collection errors and warnings", {"errors": snapshot.get("errors", []), "warnings": snapshot.get("warnings", [])}, snapshot_path, output)
    supporting = _disclosure("Supporting evidence", support, identifier="supporting-evidence", summary_note="Source data, relationships & collection details", css="supporting-evidence")
    content = attention + counts + '<section id="builds" class="panel">' + build_body + '</section>' + _workitems(snapshot) + _quality(snapshot) + compliance_section + supporting
    document = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    document += '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'">'
    document += '<title>Release ' + _text(release_id) + ' · ' + _text(title) + '</title><style>' + _STYLE + '</style></head><body>'
    document += '<div class="page-shell">' + heading + nav + '<main>' + content + '</main><footer><span>Release ' + _text(release_id) + ' · ' + _text(_date_label(snapshot.get("generated_at"))) + '</span><span>Source observations only. Deployment approval remains separate.</span></footer></div></body></html>\n'
    return document, protected


_STYLE = """
:root{font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#202939;background:#f6f7fa;font-size:14px;line-height:1.5;font-synthesis:none;-webkit-font-smoothing:antialiased}
*{box-sizing:border-box}
body{margin:0}
a{color:#4355b9;text-decoration:none;overflow-wrap:anywhere}
a:hover{text-decoration:underline}
a:focus-visible,summary:focus-visible{outline:3px solid #6967df;outline-offset:4px;border-radius:3px}
button,summary{font:inherit}
h1,h2,h3,p{margin:0}
h1{font-size:28px;line-height:1.25;letter-spacing:-.8px;font-weight:650}
h2{font-size:18px;line-height:1.35;letter-spacing:-.35px;font-weight:650}
h3{font-size:14px;font-weight:650;line-height:1.4}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;overflow-wrap:anywhere}
pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap;overflow-wrap:anywhere;max-height:400px;overflow:auto;font-size:11px;padding:16px;background:#f7f8fb;border-top:1px solid #e7eaf0;margin:0}
.page-shell{max-width:1280px;margin:auto;padding:0 40px}
header{padding:24px 0 22px}
.topline{display:flex;align-items:center;gap:10px;color:#747c8d;font-size:12px;margin-bottom:30px}
.brand-mark{display:grid;place-items:center;background:#4d50b8;color:#fff;border-radius:7px;width:25px;height:25px;font-weight:700;font-size:13px}
.brand-name{color:#3a4356;font-weight:650}
.breadcrumb-sep{color:#b1b7c5;margin:0 3px}
.topline-project{margin-left:auto}
.hero-title{display:flex;justify-content:space-between;align-items:center;gap:24px}
.eyebrow{text-transform:uppercase;font-size:10px;font-weight:700;letter-spacing:1.2px;color:#858c9c;margin-bottom:7px}
.hero-actions{display:flex;align-items:center;gap:16px;font-size:12px;flex-shrink:0}
.release-meta{display:grid;grid-template-columns:repeat(var(--meta-count,5),minmax(0,1fr));gap:24px;margin:22px 0 0}
.release-meta dt,.source-meta dt{font-size:11px;color:#7c8495;margin-bottom:4px}
.release-meta dd,.source-meta dd{margin:0;font-size:12px;font-weight:550;overflow-wrap:anywhere}
.release-meta>div+div{border-left:1px solid #e0e4ed;padding-left:24px}
.section-nav{display:flex;align-items:center;gap:29px;border-bottom:1px solid #dfe4ec;position:sticky;top:0;background:#f6f7faf5;backdrop-filter:blur(12px);z-index:2;margin-bottom:24px;overflow:auto;white-space:nowrap}
.section-nav a{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:550;color:#697286;padding:13px 0}
.section-nav a:first-child{color:#4843a3;border-bottom:2px solid #625cc6}
.nav-count{background:#fce6e7;color:#b83d49;font-size:10px;padding:0 5px;border-radius:4px}
main{display:grid;gap:20px}
.panel{padding:23px 24px;background:white;border:1px solid #e3e7ee;border-radius:11px;scroll-margin-top:68px;min-width:0}
.section-heading{display:flex;justify-content:space-between;gap:16px;align-items:center;margin-bottom:15px}
.section-heading .eyebrow{margin-bottom:4px}
.section-count{font-size:11px;color:#8991a0}
.section-description{font-size:12px;color:#7a8494;margin-top:-5px;margin-bottom:20px}
.badge{display:inline-flex;align-items:center;gap:5px;white-space:normal;background:#f0f2f6;color:#677185;padding:3px 8px;border-radius:5px;font-size:10px;font-weight:600;line-height:1.5}
.badge.failed{color:#b42d40;background:#fce9ed}
.badge.warning,.badge.unavailable{color:#936119;background:#fff3dc}
.badge.success{color:#287861;background:#eaf6f0}
.attention{border-top:3px solid #cd5261;padding-bottom:8px}
.attention.neutral{border-top-color:#8c93aa}
.attention.warning{border-top-color:#d6a450}
.attention-guide{font-size:10px;color:#9b8590;margin:0 0 6px}
.attention .section-heading{margin-bottom:8px}
.attention .eyebrow{color:#a16770}
.check-list{list-style:none;margin:0;padding:0;max-height:264px;overflow:auto;overscroll-behavior:contain;scrollbar-width:thin}
.check-item{display:flex;gap:12px;padding:13px 0;border-bottom:1px solid #f0e8eb;align-items:flex-start}
.check-item:last-child{border-bottom:0}
.check-mark{display:grid;place-items:center;flex:0 0 20px;width:20px;height:20px;border:1px solid #ebc0c6;color:#b63849;background:#fff0f3;border-radius:50%;line-height:1;font-size:16px;margin-top:2px}
.check-item.warning .check-mark,.check-item.unavailable .check-mark{color:#90641f;border-color:#ead5ac;background:#fff6e6}
.check-copy{min-width:0;flex:1}
.check-entity{display:block;font-size:10px;color:#92808a;margin-bottom:3px}
.check-title{font-size:12px;font-weight:650;display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.check-title .badge{font-size:9px;padding:1px 6px}
.check-reason{font-size:12px;color:#93505a;margin-top:4px;overflow-wrap:anywhere}
.warning .check-reason,.unavailable .check-reason{color:#856d44}
.check-jump{font-size:11px;color:#8b7b87;flex-shrink:0;margin-top:4px}
.evidence-gaps{border:0!important;border-top:1px solid #eee7e8!important;border-radius:0!important;margin-top:4px!important}
.evidence-gaps>summary{padding:12px 0!important;font-size:11px!important;color:#946c36}
.evidence-gaps>.disclosure-body{padding:0!important}
.scope-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.scope-stats>a{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid #e3e7ee;padding:16px 20px;border-radius:9px;color:inherit}
.stat-value{font-size:25px;line-height:1;font-weight:600;letter-spacing:-1px}
.stat-copy{display:flex;flex-direction:column}
.stat-copy strong{font-size:11px;font-weight:600;color:#4f5a70}
.stat-copy>span{font-size:10px;color:#9199a9;margin-top:2px}
.stat-arrow{margin-left:auto;color:#b2b9c7}
.build-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.build-card,.quality-card{border:1px solid #e5e8ef;border-radius:8px;padding:17px 18px;min-width:0;scroll-margin-top:70px}
.build-card.has-failure{border-color:#ecc7cd}
.build-heading{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.build-heading h3 a{color:#34415b}
.build-ref{font-size:10px;color:#9299a8;margin-top:4px;display:flex;align-items:center;gap:5px}
.build-ref a{color:#75829c}
.branch-line{display:flex;gap:8px;align-items:center;margin:17px 0 14px;font-size:11px;color:#65718a;overflow-wrap:anywhere;flex-wrap:wrap}
.branch-line code{margin-left:auto;font-size:10px;color:#8c94a5;background:#f5f6fa;border-radius:4px;padding:3px 6px}
.branch-label{font-size:18px;color:#8c91b2;line-height:1}
.inline-check{display:flex;align-items:flex-start;gap:7px;font-size:10px;background:#fff3f5;border-radius:5px;color:#a33b4b;padding:8px 9px;margin-bottom:6px}
.inline-check>span{font-size:16px;line-height:1}
.inline-check strong{font-size:10px}
.inline-check p{margin-top:2px;font-size:10px;line-height:1.5}
.inline-check.unavailable,.inline-check.warning{background:#fff8ec;color:#997231}
.quiet-check{font-size:10px;color:#7e8798;margin-bottom:10px}
.coverage-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:18px;padding-top:14px;border-top:1px solid #edf0f5}
.metric-label{color:#8791a1;font-size:10px}
.metric-value{font-size:21px;font-weight:600;letter-spacing:-.5px;margin-top:4px;display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.metric-delta{font-size:9px;letter-spacing:0;font-weight:550;color:#2b846c}
.metric-delta.down{color:#b94050}
.metric-delta span{font-size:8px;color:#949baa;font-weight:400}
.metric-baseline{font-size:8px;color:#939baa;letter-spacing:0;font-weight:400}
.meter{height:3px;border-radius:3px;overflow:hidden;background:#edf0f6;margin-top:8px}
.meter span{display:block;height:100%;background:#8a8ace;border-radius:3px}
.build-footnote{font-size:10px;color:#939baa;margin-top:14px}
.build-footnote a{color:#777caa}
.disclosure{margin-top:12px;border:1px solid #e7eaf0;border-radius:7px;min-width:0}
.disclosure>summary{display:flex;align-items:center;gap:12px;list-style:none;cursor:pointer;padding:12px 14px;font-size:12px;color:#536078;font-weight:550}
.disclosure>summary::-webkit-details-marker{display:none}
.disclosure>summary:before{content:"›";font-size:18px;color:#969eae;line-height:1;transform:rotate(0deg);transition:transform .15s}
.disclosure[open]>summary:before{transform:rotate(90deg)}
.disclosure[open]>summary{border-bottom:1px solid #edf0f5}
.summary-note{margin-left:auto;color:#9aa2b1;font-size:10px;font-weight:400;text-align:right}
.disclosure-body{padding:14px;min-width:0}
.build-card>.disclosure{border:0;border-top:1px solid #edf0f5;border-radius:0;margin:14px -18px -17px}
.build-card>.disclosure>summary{padding:10px 18px;font-size:10px}
.build-card .summary-note{font-size:9px}
.table-wrap{overflow-x:auto;max-width:100%;scrollbar-width:thin}
table{border-collapse:collapse;width:100%;font-size:11px}
th{text-align:left;font-weight:550;color:#8a93a5;background:#f8f9fc;white-space:nowrap}
td,th{padding:11px 12px;border-bottom:1px solid #edf0f5;vertical-align:top;overflow-wrap:anywhere}
td{color:#637087}
td:first-child a{font-weight:600}
tbody tr:last-child td{border-bottom:0}
.item-title{color:#34415b;min-width:140px;display:block}
.count-chips{display:flex;gap:4px;flex-wrap:wrap;min-width:135px}
.count-chips .badge{font-size:9px;padding:2px 5px}
.build-counts+.build-counts{margin-top:7px}
.build-count-label{font-size:9px;color:#9aa2af;display:block;margin-bottom:3px}
.small-note,.association-note{font-size:11px;color:#9299a8}
.small-note{margin-bottom:12px}
.association-note{padding:8px 10px;border-left:2px solid #e1d7b5;background:#fbf9f2;margin-top:15px;color:#918262;font-size:10px}
.quality-counts{display:flex;gap:24px;margin-top:16px;font-size:10px;color:#8d96a5}
.quality-counts strong{font-size:15px;font-weight:600;color:#4c5870;margin-right:4px}
.notice{font-size:11px;color:#9a7948;margin-bottom:12px}
.muted{color:#a0a8b6;font-size:11px}
.empty-state{padding:12px 0;color:#8e96a6;font-size:12px}
.supporting-evidence{margin-top:0;background:transparent;border-color:#e0e4ed}
.supporting-evidence>summary{padding:18px 20px}
.supporting-evidence>.disclosure-body{background:white}
.evidence-intro{font-size:12px;color:#8c95a5;margin-bottom:18px}
.evidence-intro p+p{margin-top:8px}
.source-meta{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:0 0 18px}
.source-meta>div:last-child{grid-column:1/-1}
.source-meta code{font-size:10px;color:#9099a9}
.clinic-panel .section-heading{margin-bottom:8px}
.clinic-panel>p{font-size:12px;color:#8590a2;margin-bottom:12px}
.clinic-panel .table-wrap{margin-top:10px}
footer{display:flex;justify-content:space-between;gap:20px;color:#a1a8b6;font-size:10px;padding:24px 0 35px}
section{min-width:0}
details:target{outline:2px solid #aaa7d9;outline-offset:3px}

@media(min-width:1500px){.page-shell{max-width:1360px;padding:0 50px}
}
@media(max-width:900px){.page-shell{padding:0 24px}
.hero-title{align-items:flex-start}
.hero-actions{flex-direction:column;align-items:flex-end;gap:8px}
.release-meta{gap:14px;grid-template-columns:.7fr 1.4fr .7fr 1fr 1fr}
.release-meta>div+div{padding-left:14px}
.section-nav{gap:22px}
.build-grid{grid-template-columns:1fr}
.scope-stats>a{padding:14px;gap:10px}
.stat-value{font-size:23px}
.stat-copy>span{font-size:9px}
.check-title{font-size:11px}
}
@media(max-width:600px){.page-shell{padding:0 16px}
header{padding:18px 0}
.topline{margin-bottom:22px}
.hero-title{display:block}
h1{font-size:24px;letter-spacing:-.6px}
.hero-actions{flex-direction:row;align-items:center;justify-content:space-between;margin-top:14px;font-size:11px}
.release-meta{grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}
.release-meta>div+div{padding-left:0;border:0}
.release-meta>div:first-child{display:none}
.release-meta dt{font-size:10px}
.release-meta dd{font-size:11px}
.section-nav{margin-bottom:16px;gap:22px}
.section-nav a{font-size:11px;padding:11px 0}
main{gap:14px}
.panel{padding:18px 16px}
.section-heading{gap:8px}
h2{font-size:16px}
.check-list{max-height:280px}
.check-item{gap:9px}
.check-jump{font-size:0}
.check-jump span{font-size:15px}
.check-reason{font-size:11px}
.check-title{gap:6px}
.check-mark{flex-basis:18px;width:18px;height:18px;font-size:14px}
.scope-stats{gap:8px}
.scope-stats>a{padding:12px 10px;display:block}
.stat-copy{margin-top:7px}
.stat-value{font-size:24px}
.stat-copy strong{font-size:10px}
.stat-copy>span{display:none}
.stat-arrow{display:none}
.build-card,.quality-card{padding:15px}
.build-card>.disclosure{margin-left:-15px;margin-right:-15px;margin-bottom:-15px}
.build-grid{gap:12px}
.build-heading .badge{font-size:9px}
.section-description{font-size:11px}
.summary-note{font-size:9px;max-width:45%}
.disclosure>summary{font-size:11px;padding:12px 10px}
.disclosure-body{padding:10px}
.source-meta{grid-template-columns:1fr}
.source-meta>div:last-child{grid-column:auto}
footer{font-size:9px;display:block}
footer>span{display:block;margin-bottom:6px}
.supporting-evidence>summary{padding:16px 12px}
.supporting-evidence>summary .summary-note{max-width:40%;font-size:9px}
}
@media print{.page-shell{max-width:none;padding:0}
body{background:white}
.section-nav{position:static;display:none}
.check-list{max-height:none;overflow:visible}
.panel{break-inside:avoid}
.build-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.scope-stats{break-inside:avoid}
a{color:inherit}
.hero-actions{display:none}
details[open]{break-inside:auto}
}

"""


def render_release_report(manifest_path: str | Path, output_path: str | Path) -> Path:
    """Render a verified report snapshot without network access or source mutation."""
    snapshot, manifest, root = load_report_bundle(manifest_path)
    candidate = Path(output_path).expanduser()
    if candidate.is_symlink():
        raise WorkbenchError("The release report output must not be a symlink.")
    output = candidate.resolve()
    if output.suffix.lower() not in {".html", ".htm"}:
        raise WorkbenchError("Select an HTML output file for the release report.")
    document, protected = _render(snapshot, manifest, root, output)
    protected.add(Path(manifest_path).resolve())
    if output in protected or _CLINIC_PREFIX.match(output.name) or "release-clinic" in output.parts:
        raise WorkbenchError("The renderer must not replace evidence or Release Clinic files.")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".release-report-render-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(document.encode("utf-8"))
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return output
