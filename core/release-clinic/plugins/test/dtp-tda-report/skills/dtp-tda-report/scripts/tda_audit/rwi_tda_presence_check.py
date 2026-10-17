#!/usr/bin/env python3
"""
rwi_tda_presence_check.py — standalone AutoTDA attachment presence audit
=================================================================================
Discovers ADO Release Work Items (RWIs) directly via an ADO WIQL query —
Work Item Type = Release, State = Released, Area Path under FMQPR, and
Actual Release Date within a date range controlled by --start-date /
--end-date — then checks each matching RWI for uploaded AutoTDA report
attachments (TDAReport_*.html / TDA_Report_*.html /
Annotated_TDA_Report_*.html / AutoTDAResults_*.json /
AutoTDASummary_*.json) and produces a self-contained HTML audit report
listing, per RWI:

  - RWI ID (linked to the work item in ADO)
  - Title (for readability — free from the same API call)
  - Area Path
  - Application Id and Application Name (split from Custom.ApplicationID,
    which follows a '<Name> <Id>' convention, e.g. "ECLiPSe Portal BA-50040")
  - Whether an AutoTDA report attachment was found
  - The name(s) of every matching attachment found (newest first), with
    upload date

This is a STANDALONE script — it does not import from or modify
run_tda_audit.py or any file under tda_audit/. It only imports the existing,
unmodified tda.config / tda.http_client modules (read-only) to reuse the
project's ADO authentication/session setup, the same way run_tda_audit.py
does. tda.config's load_env_file() looks for .env relative to the scripts/
directory automatically, so this script can be run from either scripts/ or
scripts/tda_audit/ (or any other cwd) — the output path default is anchored
to this file's own location, not the current working directory.

Usage:
    python tda_audit/rwi_tda_presence_check.py            # from scripts/
    python rwi_tda_presence_check.py                      # from scripts/tda_audit/
    python rwi_tda_presence_check.py --start-date 2026-09-01 --end-date 2026-09-03
    python rwi_tda_presence_check.py --application-id 50040   (ADO-side filter — only queries RWIs for that application)
    python rwi_tda_presence_check.py --output C:/Users/<you>/Downloads/RWITDAPresenceReport.html

Dependencies: Python 3.9+, existing tda/ package, .env file (ADO_TOKEN etc).
"""

from __future__ import annotations

import argparse
import datetime
import html
import logging
import pathlib
import re
import sys
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-8s  %(message)s',
    datefmt='%H:%M:%S',
)
log = logging.getLogger(__name__)

# scripts/ directory — where the tda/ package and .env live
_SCRIPTS_DIR = pathlib.Path(__file__).parent.parent

# Strict minimum delay (seconds) enforced between successive ADO API calls,
# to keep the request rate reasonable regardless of how fast ADO responds.
_ADO_CALL_DELAY_SECONDS = 1.0

# Recognised AutoTDA output filename patterns (case-insensitive). Covers both
# the HTML report uploaded by the dtp-tda-report SKILL (TDAReport_ /
# TDA_Report_ / Annotated_TDA_Report_ / Annotated_TDAReport_ prefixes — same
# convention as run_tda_audit.py's _find_tda_attachment) and the raw collector
# JSON output (AutoTDAResults_ / AutoTDASummary_), in case a stream uploads
# that instead.
#
# Annotated_TDA_Report_ vs Annotated_TDAReport_: the "Save Annotated Report"
# browser download names the file from the HTML <title> tag ("TDA Report —
# ..."), which sanitizes to Annotated_TDA_Report_... (space -> underscore).
# Annotated_TDAReport_... arises when a reviewer instead manually renames the
# original TDAReport_<STREAM>_<id>.html by just prepending "Annotated_" —
# both are real, observed naming variants and must both be recognised.
_TDA_ATTACHMENT_PATTERN = re.compile(
    r'^(TDAReport_|TDA_Report_|Annotated_TDA_Report_|Annotated_TDAReport_|AutoTDAResults_|AutoTDASummary_)'
    r'.*\.(html|json)$',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# ADO lookups
# ---------------------------------------------------------------------------

def _get_work_item(rwi_id: str, client) -> dict:
    """Fetch one RWI's fields + relations (single API call, no stream needed)."""
    resp = client.get('WorkItemsForRelease', rwi_id)
    return resp.json()


# ---------------------------------------------------------------------------
# RWI discovery via an ADO WIQL query (replaces reading RWIs from a config
# file — the query's output IS the input to the attachment-presence audit
# below). Only the date range is exposed on the CLI (--start-date/--end-date);
# the other filter criteria are fixed per the agreed audit scope.
# ---------------------------------------------------------------------------

# Fixed WIQL filter criteria (not exposed on the CLI — only the date range is).
_QUERY_WORK_ITEM_TYPE = "Release"
_QUERY_STATE = "Released"
_QUERY_AREA_PATH = "FMQPR"

# ADO field reference name used to filter on "Actual Release Date". ADO
# instances vary in what this custom field is actually called — open a
# Release WI -> (three-dot menu) -> Developer -> Field Reference Name to
# find yours if this needs to change.
_DEFAULT_DATE_FIELD = "Custom.ActualReleaseDate"


def _build_wiql_query(work_item_type: str, state: str, area_path: str,
                       start_date: str, end_date: str, date_field: str,
                       application_id_value: str | None = None) -> str:
    """Build a WIQL query string matching:
      Work Item Type = <work_item_type>, State = <state>,
      Area Path UNDER <area_path>, <date_field> between start_date and end_date
    (start_date/end_date are inclusive, 'YYYY-MM-DD' strings).

    When `application_id_value` is supplied (the exact, resolved
    Custom.ApplicationID dropdown value — see _resolve_application_id_filter),
    an additional 'AND [Custom.ApplicationID] = ...' clause is appended so
    ADO itself filters by application, rather than fetching every RWI in the
    date range and filtering client-side. Custom.ApplicationID is a fixed
    picklist (not free text), so an exact '=' match is reliable.
    """
    def esc(v: str) -> str:
        return v.replace("'", "''")

    query = (
        "SELECT [System.Id] FROM WorkItems WHERE "
        f"[System.WorkItemType] = '{esc(work_item_type)}' "
        f"AND [System.State] = '{esc(state)}' "
        f"AND [System.AreaPath] UNDER '{esc(area_path)}' "
        f"AND [{date_field}] >= '{esc(start_date)}' "
        f"AND [{date_field}] <= '{esc(end_date)}'"
    )
    if application_id_value:
        query += f" AND [Custom.ApplicationID] = '{esc(application_id_value)}'"
    return query


def _fetch_rwis_by_query(client, *, work_item_type: str, state: str, area_path: str,
                          start_date: str, end_date: str, date_field: str,
                          application_id_value: str | None = None) -> list[str]:
    """Run a WIQL query against ADO and return the matching work item IDs
    (as strings, in the order ADO returns them).
    """
    wiql = _build_wiql_query(work_item_type, state, area_path, start_date, end_date, date_field,
                              application_id_value=application_id_value)
    url = f"{client.cfg.ado_base_url.rstrip('/')}/wit/wiql?api-version=7.1"
    log.info("Running WIQL query: %s", wiql)
    resp = client.raw_post(url, json_body={"query": wiql})
    data = resp.json()
    return [str(wi['id']) for wi in data.get('workItems', [])]


def _resolve_application_id_filter(client, work_item_type: str, application_id: str) -> str:
    """Resolve a user-supplied Application Id (e.g. '50040') or a full
    Custom.ApplicationID dropdown value (e.g. 'ECLiPSe Portal BA-50040') to
    the exact string ADO uses for that field, by reading its fixed
    allowed-values list for `work_item_type`. Custom.ApplicationID is a
    picklist (a fixed set of '<Application Name>-<Id>' values), not free
    text, so this lets the WIQL query filter on it directly with an exact
    '=' comparison instead of fetching every RWI in the date range and
    filtering client-side.

    Exits the process (after logging an error) if the supplied value can't
    be resolved to exactly one allowed value.
    """
    url = (
        f"{client.cfg.ado_base_url.rstrip('/')}/wit/workitemtypes/"
        f"{work_item_type}/fields/Custom.ApplicationID?$expand=allowedValues&api-version=7.1"
    )
    resp = client.raw_get(url)
    allowed_values = resp.json().get('allowedValues', []) or []

    needle = application_id.strip()

    # 1) Exact match on the full dropdown value (case-insensitive)
    for value in allowed_values:
        if value.strip().lower() == needle.lower():
            return value

    # 2) Match on just the numeric Application Id suffix
    matches = [v for v in allowed_values if _parse_application_field(v)[1] == needle]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        log.error(
            "Application Id '%s' matches multiple Custom.ApplicationID values: %s. "
            "Supply the full 'Application Name-Id' value instead.",
            needle, ', '.join(matches),
        )
        sys.exit(1)

    log.error(
        "Application Id '%s' not found among Custom.ApplicationID's %d allowed value(s) for "
        "work item type '%s'. Check the Application Id / spelling.",
        needle, len(allowed_values), work_item_type,
    )
    sys.exit(1)
    wiql = _build_wiql_query(work_item_type, state, area_path, start_date, end_date, date_field)
    url = f"{client.cfg.ado_base_url.rstrip('/')}/wit/wiql?api-version=7.1"
    log.info("Running WIQL query: %s", wiql)
    resp = client.raw_post(url, json_body={"query": wiql})
    data = resp.json()
    return [str(wi['id']) for wi in data.get('workItems', [])]


def _find_tda_attachments(relations: list) -> list[dict]:
    """Return every AttachedFile relation matching a known AutoTDA output
    pattern, sorted newest-first by upload date.

    Returns a list of {'name': str, 'added_date': str, 'url': str}, where
    'url' is a direct link to view/download the attachment in the browser
    (ADO's attachment API URL — opens/downloads the file when the user is
    already authenticated to ADO in that browser).
    """
    found = []
    for rel in relations:
        if rel.get('rel') != 'AttachedFile':
            continue
        name = rel.get('attributes', {}).get('name', '')
        if not _TDA_ATTACHMENT_PATTERN.match(name):
            continue
        found.append({
            'name': name,
            'added_date': rel.get('attributes', {}).get('addedDate', ''),
            'url': rel.get('url', ''),
        })
    found.sort(key=lambda a: a['added_date'], reverse=True)
    return found


# ---------------------------------------------------------------------------
# HTML report generation
# ---------------------------------------------------------------------------

_CSS = """
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f8; color: #222; margin: 0; padding: 24px; }
  h1 { font-size: 22px; margin-bottom: 4px; }
  .meta { color: #666; font-size: 13px; margin-bottom: 20px; }
  .summary { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }
  .summary .card { background: #fff; border-radius: 8px; padding: 12px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); min-width: 120px; }
  .summary .card .n { font-size: 26px; font-weight: 700; }
  .summary .card .label { font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: .04em; }
  .summary .card.found .n { color: #1a7f37; }
  .summary .card.missing .n { color: #c0392b; }
  .summary .card.error .n { color: #b7791f; }
  table { border-collapse: collapse; width: 100%; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #eaecef; vertical-align: top; font-size: 13.5px; }
  th { background: #2c3e50; color: #fff; font-weight: 600; position: sticky; top: 0; }
  tr:last-child td { border-bottom: none; }
  tr:hover { background: #f8fafc; }
  .badge { display: inline-block; padding: 2px 9px; border-radius: 10px; font-size: 11.5px; font-weight: 600; }
  .badge.found { background: #e3f6e9; color: #1a7f37; }
  .badge.missing { background: #fdecea; color: #c0392b; }
  .badge.error { background: #fdf3da; color: #b7791f; }
  .file-list { margin: 0; padding-left: 18px; }
  .file-list li { margin-bottom: 2px; }
  .file-latest { font-weight: 600; }
  .added-date { color: #888; font-size: 11.5px; margin-left: 4px; }
  a { color: #0969da; text-decoration: none; }
  a:hover { text-decoration: underline; }
  h2 { font-size: 16px; margin: 28px 0 10px 0; color: #2c3e50; }
  table.app-breakdown { margin-bottom: 24px; }
  table.app-breakdown th { background: #566573; }
  table.app-breakdown td.h-count-cell { text-align: center; font-variant-numeric: tabular-nums; }
  td.h-found { color: #1a7f37; }
  td.h-missing { color: #c0392b; }
  td.h-error { color: #b7791f; }
  td.h-total { color: #555; font-weight: 700; }
  .filter-bar { display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end; margin-bottom: 12px; }
  .filter-bar .field { display: flex; flex-direction: column; gap: 4px; }
  .filter-bar label { font-size: 11.5px; color: #555; text-transform: uppercase; letter-spacing: .03em; }
  .filter-bar input, .filter-bar select { padding: 6px 10px; border: 1px solid #d0d7de; border-radius: 6px; font-size: 13px; min-width: 140px; }
  .filter-bar button { padding: 7px 14px; border: 1px solid #d0d7de; border-radius: 6px; background: #fff; cursor: pointer; font-size: 13px; }
  .filter-bar button:hover { background: #f1f3f5; }
  .filter-count { font-size: 12.5px; color: #666; margin-bottom: 8px; }
  tr.hidden-row { display: none; }
"""



def _status_badge(status: str) -> str:
    cls = {'FOUND': 'found', 'NOT FOUND': 'missing'}.get(status, 'error')
    return f'<span class="badge {cls}">{html.escape(status)}</span>'


def _file_list_html(attachments: list[dict]) -> str:
    if not attachments:
        return '<em>&mdash;</em>'
    items = []
    for i, att in enumerate(attachments):
        name_html = html.escape(att['name'])
        date_html = html.escape(att['added_date']) if att['added_date'] else ''
        css = ' class="file-latest"' if i == 0 else ''
        date_span = f'<span class="added-date">({date_html})</span>' if date_html else ''
        items.append(f'<li><span{css}>{name_html}</span>{date_span}</li>')
    return f'<ul class="file-list">{"".join(items)}</ul>'


# ---------------------------------------------------------------------------
# Application Id / Application Name breakdown
# ---------------------------------------------------------------------------

# ADO's Custom.ApplicationID field here follows a '<Application Name>-<Id>'
# convention, e.g. "ECLiPSe Portal BA-50040", "Blade BA-50665", where the
# splitting character is the '-' immediately before the trailing digits.
# Everything before that '-' (including any letter prefix like "BA") is the
# Application Name; everything after it is the numeric Application Id.
# Falls back to treating the whole raw value as the name (with a blank id)
# if it doesn't match this convention.
_APPLICATION_ID_PATTERN = re.compile(r'^(?P<name>.+)-(?P<code>\d+)\s*$')


def _parse_application_field(raw: str) -> tuple[str, str]:
    """Split a Custom.ApplicationID value into (app_name, app_id). Returns
    ('', '') for a blank/missing value, or (raw, '') if it doesn't match the
    '<Name>-<Id>' convention.
    """
    raw = (raw or '').strip()
    if not raw:
        return '', ''
    m = _APPLICATION_ID_PATTERN.match(raw)
    if m:
        return m.group('name').strip(), m.group('code').strip()
    return raw, ''


def _build_app_breakdown(rows: list[dict]) -> list[dict]:
    """Aggregate FOUND / NOT FOUND / ERROR counts per distinct (app_id,
    app_name) pair across all audited RWIs. Rows with no Application Id info
    at all are grouped under a '(Unknown)' bucket so nothing is dropped
    silently. Returned sorted by Application Name (then Id) for a stable,
    readable order.
    """
    buckets: dict[tuple[str, str], dict] = {}
    for r in rows:
        app_id = r.get('app_id', '')
        app_name = r.get('app_name', '') or '(Unknown)'
        status_key = r['status'] if r['status'] in ('FOUND', 'NOT FOUND') else 'ERROR'
        entry = buckets.setdefault(
            (app_id, app_name),
            {'app_id': app_id, 'app_name': app_name, 'counts': {'FOUND': 0, 'NOT FOUND': 0, 'ERROR': 0}},
        )
        entry['counts'][status_key] += 1
    return sorted(buckets.values(), key=lambda e: (e['app_name'].lower(), e['app_id']))


def _render_app_breakdown_table(breakdown_rows: list[dict]) -> str:
    """Render the Application Id / Application Name breakdown as a flat HTML
    table: App Id, App Name, Found, Not Found, Total (errors are still
    counted into Total, just not shown as their own column).
    """
    if not breakdown_rows:
        return '<p><em>No Application Id data available.</em></p>'

    body_rows = []
    for r in breakdown_rows:
        c = r['counts']
        total = c['FOUND'] + c['NOT FOUND'] + c['ERROR']
        app_id_cell = html.escape(r['app_id']) or '&nbsp;'
        app_name_cell = html.escape(r['app_name']) or '&nbsp;'
        body_rows.append(f"""
        <tr>
          <td>{app_id_cell}</td>
          <td>{app_name_cell}</td>
          <td class="h-count-cell h-found">{c['FOUND']}</td>
          <td class="h-count-cell h-missing">{c['NOT FOUND']}</td>
          <td class="h-count-cell h-total">{total}</td>
        </tr>""")

    return f"""<table class="app-breakdown">
    <thead>
      <tr>
        <th>App Id</th>
        <th>App Name</th>
        <th>Found</th>
        <th>Not Found</th>
        <th>Total</th>
      </tr>
    </thead>
    <tbody>{''.join(body_rows)}
    </tbody>
  </table>"""


def _build_html_report(rows: list[dict], ado_organization: str, ado_project: str,
                        generated_at: str, query_range_label: str = '') -> str:
    found_count   = sum(1 for r in rows if r['status'] == 'FOUND')
    missing_count = sum(1 for r in rows if r['status'] == 'NOT FOUND')
    error_count   = sum(1 for r in rows if r['status'] not in ('FOUND', 'NOT FOUND'))

    # Distinct, sorted values for the Status filter dropdown.
    status_values = sorted({r['status'] for r in rows})

    table_rows = []
    for r in rows:
        rwi_id = r['rwi_id']
        app_id = r.get('app_id', '')
        app_name = r.get('app_name', '')
        status = r['status']
        wi_url = f"https://dev.azure.com/{ado_organization}/{ado_project}/_workitems/edit/{rwi_id}"
        table_rows.append(f"""
        <tr data-rwi="{html.escape(rwi_id.lower())}" data-app-id="{html.escape(app_id.lower())}" data-app-name="{html.escape(app_name.lower())}" data-status="{html.escape(status.lower())}">
          <td><a href="{html.escape(wi_url)}" target="_blank">{html.escape(rwi_id)}</a></td>
          <td>{html.escape(r['title']) or '<em>&mdash;</em>'}</td>
          <td>{html.escape(app_id) or '<em>&mdash;</em>'}</td>
          <td>{html.escape(app_name) or '<em>&mdash;</em>'}</td>
          <td>{_status_badge(status)}</td>
          <td>{_file_list_html(r['attachments'])}</td>
        </tr>""")

    status_options = ''.join(
        f'<option value="{html.escape(s.lower())}">{html.escape(s)}</option>' for s in status_values
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AutoTDA Report Presence Audit</title>
<style>{_CSS}</style>
</head>
<body>
  <h1>AutoTDA Report Presence Audit</h1>
  <div class="meta">Generated: {html.escape(generated_at)} &nbsp;|&nbsp; RWIs checked: {len(rows)}{(' &nbsp;|&nbsp; Query range: ' + html.escape(query_range_label)) if query_range_label else ''}</div>

  <div class="summary">
    <div class="card found"><div class="n">{found_count}</div><div class="label">Report Found</div></div>
    <div class="card missing"><div class="n">{missing_count}</div><div class="label">Not Found</div></div>
    <div class="card error"><div class="n">{error_count}</div><div class="label">Errors</div></div>
  </div>

  <h2>Breakdown by Application</h2>
  {_render_app_breakdown_table(_build_app_breakdown(rows))}

  <h2>RWI Details</h2>
  <div class="filter-bar">
    <div class="field">
      <label for="filter-rwi">RWI</label>
      <input type="text" id="filter-rwi" placeholder="e.g. 15694998">
    </div>
    <div class="field">
      <label for="filter-app-id">App Id</label>
      <input type="text" id="filter-app-id" placeholder="e.g. 50040">
    </div>
    <div class="field">
      <label for="filter-app-name">App Name</label>
      <input type="text" id="filter-app-name" placeholder="e.g. ECLiPSe Portal">
    </div>
    <div class="field">
      <label for="filter-status">Status</label>
      <select id="filter-status">
        <option value="">All</option>
        {status_options}
      </select>
    </div>
    <button type="button" id="filter-clear">Clear filters</button>
  </div>
  <div class="filter-count" id="filter-count"></div>

  <table id="rwi-table">
    <thead>
      <tr>
        <th>RWI</th>
        <th>Title</th>
        <th>App Id</th>
        <th>App Name</th>
        <th>Status</th>
        <th>AutoTDA File(s) Found</th>
      </tr>
    </thead>
    <tbody>
      {''.join(table_rows)}
    </tbody>
  </table>

<script>
(function() {{
  var rwiInput = document.getElementById('filter-rwi');
  var appIdInput = document.getElementById('filter-app-id');
  var appNameInput = document.getElementById('filter-app-name');
  var statusSelect = document.getElementById('filter-status');
  var clearBtn = document.getElementById('filter-clear');
  var countEl = document.getElementById('filter-count');
  var rows = Array.prototype.slice.call(document.querySelectorAll('#rwi-table tbody tr'));
  var total = rows.length;

  function applyFilters() {{
    var rwiVal = rwiInput.value.trim().toLowerCase();
    var appIdVal = appIdInput.value.trim().toLowerCase();
    var appNameVal = appNameInput.value.trim().toLowerCase();
    var statusVal = statusSelect.value;
    var visible = 0;
    rows.forEach(function(row) {{
      var match =
        (rwiVal === '' || row.getAttribute('data-rwi').indexOf(rwiVal) !== -1) &&
        (appIdVal === '' || row.getAttribute('data-app-id').indexOf(appIdVal) !== -1) &&
        (appNameVal === '' || row.getAttribute('data-app-name').indexOf(appNameVal) !== -1) &&
        (statusVal === '' || row.getAttribute('data-status') === statusVal);
      row.classList.toggle('hidden-row', !match);
      if (match) visible++;
    }});
    countEl.textContent = 'Showing ' + visible + ' of ' + total + ' RWI(s)';
  }}

  [rwiInput, appIdInput, appNameInput].forEach(function(el) {{
    el.addEventListener('input', applyFilters);
  }});
  statusSelect.addEventListener('change', applyFilters);
  clearBtn.addEventListener('click', function() {{
    rwiInput.value = '';
    appIdInput.value = '';
    appNameInput.value = '';
    statusSelect.value = '';
    applyFilters();
  }});

  applyFilters();
}})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # Anchor the default output path to this script's own directory, not the
    # caller's current working directory — so it works whether invoked from
    # scripts/, scripts/tda_audit/, or anywhere else.
    default_output = pathlib.Path.home() / 'Downloads' / 'RWITDAPresenceReport.html'

    parser = argparse.ArgumentParser(
        description='Standalone audit: discover RWIs via an ADO query (Release/Released/FMQPR, '
                    'filtered by Actual Release Date range) and confirm which of them have an '
                    'AutoTDA report attachment uploaded.'
    )
    parser.add_argument('--start-date', default='2026-09-01',
                         help="Actual Release Date range start, inclusive, 'YYYY-MM-DD' (default: 2026-09-01)")
    parser.add_argument('--end-date', default='2026-09-03',
                         help="Actual Release Date range end, inclusive, 'YYYY-MM-DD' (default: 2026-09-03)")
    parser.add_argument(
        '--application-id', default=None,
        help="Optional Application Id filter — either the numeric suffix (e.g. '50040') or the "
             "full 'Application Name-Id' dropdown value (e.g. 'ECLiPSe Portal BA-50040'). "
             "Custom.ApplicationID is a fixed picklist, so when set this is resolved to its exact "
             "allowed value and applied as an '=' filter directly in the ADO WIQL query (only "
             "matching RWIs are fetched at all). Omit to include every RWI found in the date "
             "range (default behaviour).",
    )
    parser.add_argument(
        '--output', default=str(default_output),
        help=f'Path to write the HTML audit report (default: {default_output})',
    )
    args = parser.parse_args()

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Bootstrap ADO client — same pattern as run_tda_audit.py, reused read-only.
    sys.path.insert(0, str(_SCRIPTS_DIR))
    from tda.config import Config, load_env_file
    from tda.http_client import ADOClient

    env_path = _SCRIPTS_DIR / '.env'
    if not env_path.exists():
        log.error(".env file not found at %s — required for ADO credentials.", env_path)
        sys.exit(1)

    load_env_file(str(env_path))
    cfg = Config.from_env()
    client = ADOClient(cfg)

    application_id_value = None
    if args.application_id:
        application_id_value = _resolve_application_id_filter(
            client, _QUERY_WORK_ITEM_TYPE, args.application_id,
        )
        log.info("Application Id filter '%s' resolved to Custom.ApplicationID = '%s'",
                  args.application_id, application_id_value)

    # Discover RWIs via the WIQL query — this output IS the input to the
    # attachment-presence audit below (no config file involved).
    rwi_ids = _fetch_rwis_by_query(
        client,
        work_item_type=_QUERY_WORK_ITEM_TYPE,
        state=_QUERY_STATE,
        area_path=_QUERY_AREA_PATH,
        start_date=args.start_date,
        end_date=args.end_date,
        date_field=_DEFAULT_DATE_FIELD,
        application_id_value=application_id_value,
    )
    if not rwi_ids:
        log.error(
            "No RWIs found for %s/%s under '%s' with %s between %s and %s%s.",
            _QUERY_WORK_ITEM_TYPE, _QUERY_STATE, _QUERY_AREA_PATH,
            _DEFAULT_DATE_FIELD, args.start_date, args.end_date,
            f" and Custom.ApplicationID = '{application_id_value}'" if application_id_value else "",
        )
        sys.exit(1)
    log.info("Discovered %d RWI(s) via query (%s .. %s)", len(rwi_ids), args.start_date, args.end_date)

    rows: list[dict] = []
    for i, rwi_id in enumerate(rwi_ids):
        if i > 0:
            time.sleep(_ADO_CALL_DELAY_SECONDS)
        log.info("Checking RWI %s ...", rwi_id)
        try:
            wi = _get_work_item(rwi_id, client)
        except Exception as exc:
            log.warning("RWI %s — failed to fetch work item: %s", rwi_id, exc)
            rows.append({
                'rwi_id': rwi_id, 'title': '', 'area_path': '', 'app_id': '', 'app_name': '',
                'status': 'ERROR', 'attachments': [],
            })
            continue

        fields = wi.get('fields', {}) or {}
        title = fields.get('System.Title', '')
        area_path = fields.get('System.AreaPath', '')
        app_name, app_id = _parse_application_field(fields.get('Custom.ApplicationID', ''))
        relations = wi.get('relations', []) or []

        attachments = _find_tda_attachments(relations)
        status = 'FOUND' if attachments else 'NOT FOUND'
        log.info(
            "RWI %s — %s (%d matching attachment(s))",
            rwi_id, status, len(attachments),
        )
        rows.append({
            'rwi_id': rwi_id, 'title': title, 'area_path': area_path, 'app_id': app_id, 'app_name': app_name,
            'status': status, 'attachments': attachments,
        })

    generated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Group rows by Area Path (rows with the same area path appear together
    # in the report) rather than in query-return order. Rows with the same
    # area path keep their relative order via a stable sort.
    rows.sort(key=lambda r: r['area_path'])

    report_html = _build_html_report(
        rows, cfg.ado_organization, cfg.ado_project, generated_at,
        query_range_label=f"{args.start_date} .. {args.end_date} ({_DEFAULT_DATE_FIELD})",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_html, encoding='utf-8')

    found_count   = sum(1 for r in rows if r['status'] == 'FOUND')
    missing_count = sum(1 for r in rows if r['status'] == 'NOT FOUND')
    error_count   = sum(1 for r in rows if r['status'] not in ('FOUND', 'NOT FOUND'))

    print()
    print("=" * 60)
    print("RWI TDA PRESENCE AUDIT — COMPLETE")
    print("=" * 60)
    print(f"  Query range:     {args.start_date} .. {args.end_date} ({_DEFAULT_DATE_FIELD})")
    print(f"  RWIs checked:    {len(rows)}")
    print(f"  Report found:    {found_count}")
    print(f"  Not found:       {missing_count}")
    print(f"  Errors:          {error_count}")
    print()
    print(f"  HTML report:     {output_path.resolve()}")


if __name__ == '__main__':
    main()
