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
    return f'<details><summary>{html.escape(label)}</summary>{note}<pre>{html.escape(raw, quote=True)}</pre></details>'


def _section(title: str, body: str, identifier: str) -> str:
    return f'<section id="{identifier}"><h2>{html.escape(title)}</h2>{body}</section>'


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


def _render(snapshot: dict, manifest: dict, root: Path, output: Path) -> tuple[str, set[Path]]:
    source = _object(snapshot.get("source"))
    release = _object(snapshot.get("release"))
    fields = _object(release.get("fields"))
    release_id = source.get("release_id")
    snapshot_path = confined_artifact(root, manifest["snapshot"]["path"])
    protected = {snapshot_path}
    title = fields.get("System.Title") or f"Release {release_id}"
    stamp = snapshot.get("generated_at")
    status = snapshot.get("collection_status", "unavailable")
    summary = _table(["Property", "Value"], [
        ["Release", _record_link(release, release_id)], ["Title", _text(title)],
        ["Collection status", _text(status)], ["Collected at (UTC)", _text(stamp)],
        ["Organization", _text(source.get("organization"))], ["Project", _text(source.get("project"))],
        ["Release revision", _text(source.get("revision", release.get("rev")))],
        ["Work item state", _text(fields.get("System.State"))],
        ["Planned date", _text(fields.get("Custom.PlannedReleaseDate"))],
        ["Actual date", _text(fields.get("Custom.ActualReleaseDate"))],
    ])
    summary += _details("All release fields and relations", release, snapshot_path, output)
    sections = [_section("Release overview", summary, "release")]
    if snapshot.get("warnings") or snapshot.get("errors"):
        notices = '<p class="notice">Collection limits are recorded below. Missing evidence is not a passing result.</p>'
        notices += _details("Warnings", snapshot.get("warnings", []), snapshot_path, output)
        notices += _details("Errors", snapshot.get("errors", []), snapshot_path, output)
        sections.append(_section("Collection limits", notices, "limits"))

    builds = _array(snapshot.get("builds"))
    build_rows = []
    comparison_rows = []
    build_details = []
    for index, item in enumerate(builds):
        item = _object(item)
        build = _object(item.get("build"))
        repository = _object(build.get("repository"))
        build_rows.append([_record_link(build, item.get("id", build.get("id"))), _text(repository.get("name", repository.get("id"))),
                           _text(build.get("sourceBranch")), _text(build.get("sourceVersion")),
                           _text(build.get("status")), _text(build.get("result")), _text(item.get("status"))])
        for name, comparison in _object(item.get("comparisons")).items():
            comparison = _object(comparison)
            comparison_rows.append([_text(item.get("id", build.get("id"))), _text(name),
                                    _text(comparison.get("base")), _text(comparison.get("target")),
                                    _text(comparison.get("aheadCount")), _text(comparison.get("behindCount")),
                                    _text(comparison.get("status"))])
        if index < _CARD_LIMIT:
            build_details.append(_details(f'Build {item.get("id", build.get("id", "unavailable"))}: all collected data', item, snapshot_path, output))
    if len(builds) > _CARD_LIMIT:
        build_details.append(f'<p class="notice">Showing {_CARD_LIMIT} of {len(builds)} build detail previews. Complete records remain in the ' +
                             _file_anchor("normalized snapshot", snapshot_path, output) + '.</p>')
    sections.append(_section("Builds and comparisons", _table(
        ["Build", "Repository", "Branch", "Commit", "Build state", "Build result", "Collection"], build_rows) +
        '<h3>Commit comparisons</h3>' + _table(["Build", "Comparison", "Base commit", "Target commit", "Ahead", "Behind", "Collection"], comparison_rows) +
        ''.join(build_details), "builds"))

    workitems = _array(snapshot.get("workitems"))
    work_rows = []
    for item in workitems:
        item = _object(item)
        values = _object(item.get("fields"))
        assignee = values.get("System.AssignedTo")
        work_rows.append([_record_link(item), _text(values.get("System.WorkItemType")), _text(values.get("System.Title")),
                          _text(values.get("System.State")), _text(_object(assignee).get("displayName", assignee)), _text(item.get("rev"))])
    sections.append(_section("Related work items", _table(["ID", "Type", "Title", "State", "Assignee", "Revision"], work_rows) +
                             _details("Complete work item records", workitems, snapshot_path, output), "workitems"))

    test_rows = []
    for report in _array(snapshot.get("tests")):
        report = _object(report)
        for requirement in _array(report.get("requirementCoverages")):
            requirement = _object(requirement)
            counts = _object(_object(requirement.get("testExecutionStatusStats")).get("countByType"))
            test_rows.append([_text(report.get("build_id", report.get("buildId"))),
                              _anchor(requirement.get("id"), requirement.get("permalink", requirement.get("url"))),
                              _text(counts.get("PASSED", requirement.get("passed"))),
                              _text(counts.get("FAILED", requirement.get("failed"))),
                              _text(counts.get("NO_EXECUTION")), _text(counts.get("BLOCKED")), _text(counts.get("DEFERRED"))])
    aggregation = _object(snapshot.get("test_aggregation"))
    aggregation_note = aggregation.get("message") or "Cross-build aggregation rule is unavailable. Counts remain separate for each build."
    sections.append(_section("Tests and defects", '<p>These records preserve build-specific test and defect evidence.</p>' +
                             '<p class="notice">' + _text(aggregation_note) + '</p>' +
                             _table(["Build", "Requirement", "Passed", "Failed", "No execution", "Blocked", "Deferred"], test_rows) +
                             _details("Test reports and execution evidence", snapshot.get("tests", []), snapshot_path, output) +
                             _details("Defect records", snapshot.get("defects", []), snapshot_path, output), "tests"))
    coverage_rows = []
    for item in _array(snapshot.get("coverage")):
        item = _object(item)
        summary = _object(item.get("summary"))
        coverage_rows.append([_text(item.get("build_id", item.get("buildId"))), "Candidate",
                              _percentage(summary.get("line_coverage", item.get("lineCoverage"))),
                              _percentage(summary.get("branch_coverage", item.get("branchCoverage"))), _text(item.get("status"))])
    for item in builds:
        item = _object(item)
        coverage = _object(item.get("production_coverage"))
        if coverage:
            summary = _object(coverage.get("summary"))
            coverage_rows.append([_text(coverage.get("build_id")), "Production baseline for build " + _text(item.get("id")),
                                  _percentage(summary.get("line_coverage")), _percentage(summary.get("branch_coverage")),
                                  _text(coverage.get("status"))])
    sections.append(_section("ADO coverage", '<p>Coverage evidence collected from Azure DevOps is shown separately from SonarQube.</p>' +
                             _table(["Build", "Evidence", "Lines", "Branches", "Collection"], coverage_rows) +
                             _details("ADO coverage data", snapshot.get("coverage", []), snapshot_path, output), "coverage"))
    sonar_content = []
    sonar_items = _array(snapshot.get("sonarqube"))
    for item in sonar_items[:_CARD_LIMIT]:
        item = _object(item)
        association = item.get("association_status", "unavailable")
        note = "Current branch snapshot; build association is unverified." if association == "current_snapshot" else f"Build association: {association}"
        sonar_content.append(f'<article><h3>{_text(item.get("component"))}</h3><p class="notice">{_text(note)}</p>' +
                             _details("SonarQube analysis, measures, gate, issues, and hotspots", item, snapshot_path, output) + '</article>')
    if len(sonar_items) > _CARD_LIMIT:
        sonar_content.append(f'<p class="notice">Showing {_CARD_LIMIT} of {len(sonar_items)} analysis detail previews. Complete records remain in the ' +
                             _file_anchor("normalized snapshot", snapshot_path, output) + '.</p>')
    sections.append(_section("SonarQube quality data", ''.join(sonar_content) or '<p class="muted">SonarQube data unavailable.</p>', "sonarqube"))

    graph = _object(snapshot.get("graph"))
    graph_body = '<p>These relationships retain their unresolved boundaries and source metadata.</p>'
    for label, key in (("Relationship warnings", "warnings"), ("Unresolved story IDs", "unresolvedStoryIds"), ("Unlinked commits", "unlinkedCommits")):
        if graph.get(key):
            graph_body += f'<p class="notice"><strong>{html.escape(label)}:</strong> {_text(graph[key])}</p>'
    graph_body += _table(["Node ID", "Type", "Label"], [[_text(_object(item).get("id")), _text(_object(item).get("type")), _text(_object(item).get("label"))]
                                                            for item in _array(graph.get("nodes"))])
    graph_body += _table(["Edge ID", "Type", "From", "To", "Metadata"], [[_text(_object(item).get(key)) for key in ("id", "type", "from", "to", "metadata")]
                                                                             for item in _array(graph.get("edges"))])
    graph_body += _details("Complete relationship graph", graph, snapshot_path, output)
    sections.append(_section("Release relationships", graph_body, "relationships"))

    compliance, clinic_paths = _compliance(snapshot, root, output)
    protected.update(clinic_paths)
    sections.append(_section("Release compliance", compliance, "compliance"))
    evidence_rows = []
    seen = set()
    for item in [*manifest.get("evidence", []), *snapshot.get("evidence", [])]:
        if item["path"] in seen:
            continue
        seen.add(item["path"])
        path = confined_artifact(root, item["path"])
        protected.add(path)
        evidence_rows.append([_file_anchor(item.get("path"), path, output), _text(item.get("bytes")), _text(item.get("sha256"))])
    evidence_body = '<p>' + _file_anchor("Normalized report snapshot", snapshot_path, output) + '</p>' + \
        _table(["Input artifact", "SHA-256"], [["Normalized report snapshot", _text(manifest["snapshot"]["sha256"])]]) + \
        _table(["Retained evidence", "Bytes", "SHA-256"], evidence_rows)
    evidence_body += _details("Collection metrics", snapshot.get("metrics", {}), snapshot_path, output)
    sections.append(_section("Evidence and collection metrics", evidence_body, "evidence"))
    # Preserve any future contract fields without silently dropping them from the report.
    sections.append(_section("Complete normalized data", _details("Complete report snapshot", snapshot, snapshot_path, output), "complete"))
    navigation = ''.join(f'<a href="#{identifier}">{label}</a>' for identifier, label in [
        ("release", "Release"), ("builds", "Builds"), ("workitems", "Work items"), ("tests", "Tests"),
        ("coverage", "ADO coverage"), ("sonarqube", "SonarQube"), ("relationships", "Relationships"),
        ("compliance", "Compliance"), ("evidence", "Evidence")])
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Release {_text(release_id)} — {_text(title)}</title>
<style>
:root{{font-family:system-ui,-apple-system,sans-serif;color:#17253b;background:#f3f6fb;line-height:1.5}}*{{box-sizing:border-box}}body{{margin:0}}header,main,footer{{max-width:1240px;margin:auto;padding:24px}}header{{background:#172b4d;color:#fff;border-radius:0 0 16px 16px}}h1{{margin:0 0 8px;font-size:2rem}}h2{{margin:0 0 18px;font-size:1.35rem}}h3{{font-size:1.1rem}}nav{{display:flex;flex-wrap:wrap;gap:10px 18px;margin-top:18px}}nav a{{color:#dceaff}}section{{background:#fff;border:1px solid #d7e0ec;border-radius:12px;padding:22px;margin-bottom:20px;scroll-margin-top:16px}}a{{color:#075bc0;overflow-wrap:anywhere}}.table-wrap{{overflow:auto}}table{{width:100%;border-collapse:collapse;font-size:.9rem}}th,td{{border-bottom:1px solid #dce3ec;padding:10px;text-align:left;vertical-align:top;overflow-wrap:anywhere}}th{{background:#eef3fa}}details{{margin:14px 0;border:1px solid #dce3ec;border-radius:6px}}summary{{padding:10px;cursor:pointer;font-weight:600}}summary:focus-visible,a:focus-visible{{outline:3px solid #8c49dc;outline-offset:3px}}pre{{margin:0;padding:14px;background:#f5f7fb;white-space:pre-wrap;overflow-wrap:anywhere;font-size:.82rem}}.notice{{padding:10px 12px;background:#fff4d9;border-left:4px solid #bf7900}}.muted,footer{{color:#52627b}}article{{border-bottom:1px solid #dce3ec;padding:4px 0 12px}}@media(max-width:700px){{header,main,footer{{padding:14px}}section{{padding:14px}}h1{{font-size:1.5rem}}th,td{{padding:7px}}}}@media print{{body{{background:white}}header{{background:white;color:#17253b}}nav{{display:none}}section{{break-inside:avoid}}}}
</style></head><body><header><h1>Release {_text(release_id)}</h1><p>{_text(title)}</p><p>Collection: {_text(status)} · {_text(stamp)}</p><nav aria-label="Report sections">{navigation}</nav></header><main>{''.join(sections)}</main>
<footer>Generated from retained release evidence. Collection status does not establish deployment approval or verified business behavior.</footer></body></html>
'''
    return document, protected


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
