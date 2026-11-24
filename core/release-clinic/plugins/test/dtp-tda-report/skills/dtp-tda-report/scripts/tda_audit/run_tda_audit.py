#!/usr/bin/env python3
"""
run_tda_audit.py  —  TDA audit pipeline (download + extract, self-contained)
=================================================================================
Runs the complete TDA audit data pipeline in a single script:

  Step 1 — Discover Release Work Items (RWIs) directly via an ADO WIQL query
           (Work Item Type = Release, State = Released, Area Path under
           FMQPR, Actual Release Date within --start-date/--end-date — same
           approach as rwi_tda_presence_check.py) and download each one's
           signed-off TDA HTML report attachment, if present.
  Step 2 — Parse each HTML report into a structured TDAFindings_*.json file,
           including any human "remediation" annotations reviewers recorded
           directly on the report (reason / false-positive / workaround
           explanations). Each finding is extracted as {"text", "annotation"}
           where annotation (when present) carries the reviewer, timestamp,
           note, and a resolution_status (resolved | false_positive |
           workaround | acknowledged | unresolved). resolution_status is
           taken from the reviewer's explicit "Type of Remediation" dropdown
           selection when present (recorded reports from 2026-10-06 onward),
           falling back to a heuristic classification of the note text for
           older reports saved before that dropdown existed. The result also includes open_finding_counts /
           open_findings_by_area — the same counts/breakdowns as
           finding_counts / findings_by_area but excluding findings annotated
           as resolved or false_positive, so downstream trend analysis can
           tell genuinely outstanding risk apart from reviewed/closed items.

No config/sources file is required — the date range on the CLI IS the input.

Each run clears stale output from the previous run first: the TDAAttachments/
and TDAFindings/ directories only ever contain files produced by the CURRENT
invocation (TDAAttachments/ is only cleared when Step 1 actually runs, i.e.
not under --skip-download). This keeps TDAFindings/ in sync with the current
date range so trend analysis (dtp-tda-trends) never sees leftover data from
an unrelated earlier run.

Usage (run from the scripts/ directory):
    python tda_audit/run_tda_audit.py
    python tda_audit/run_tda_audit.py --start-date 2026-09-01 --end-date 2026-09-03
    python tda_audit/run_tda_audit.py --application-id 50040   (ADO-side filter — only queries RWIs for that application)
    python tda_audit/run_tda_audit.py --attachments tda_audit/TDAAttachments --findings tda_audit/TDAFindings
    python tda_audit/run_tda_audit.py --skip-download   (re-extract from already-downloaded HTMLs)

Dependencies: Python 3.10+, existing tda/ package, configured root environment.
"""

import argparse
import json
import logging
import os
import pathlib
import re
import sys
import time
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-8s  %(message)s',
    datefmt='%H:%M:%S',
)
log = logging.getLogger(__name__)

# scripts/ directory — contains the tda/ package.
_SCRIPTS_DIR = pathlib.Path(__file__).parent.parent


# ===========================================================================
# STEP 1 HELPERS  —  Discover RWIs via ADO query, then download TDA attachments
# ===========================================================================

# Fixed WIQL filter criteria (not exposed on the CLI — only the date range
# is). Mirrors rwi_tda_presence_check.py's query so both scripts discover
# the same scope of Release Work Items.
_QUERY_WORK_ITEM_TYPE = "Release"
_QUERY_STATE = "Released"
_QUERY_AREA_PATH = "FMQPR"

# ADO field reference name used to filter on "Actual Release Date". ADO
# instances vary in what this custom field is actually called — open a
# Release WI -> (three-dot menu) -> Developer -> Field Reference Name to
# find yours if this needs to change.
_DEFAULT_DATE_FIELD = "Custom.ActualReleaseDate"

# Strict minimum delay (seconds) enforced between successive ADO API calls.
_ADO_CALL_DELAY_SECONDS = 1.0


def _build_wiql_query(work_item_type: str, state: str, area_path: str,
                       start_date: str, end_date: str, date_field: str,
                       application_id_value: str = None) -> str:
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
                          application_id_value: str = None) -> list:
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


# ADO's Custom.ApplicationID field follows a '<Application Name>-<Id>'
# convention, e.g. "ECLiPSe Portal BA-50040", "CORTEX XVA BATCH BA-50513",
# where the splitting character is the '-' immediately before the trailing
# digits. The Application Name portion is used as the "stream" label for
# attachment filename/logging purposes, replacing the manually-maintained
# `stream` field previously supplied via tda_audit_sources.yaml.
_APPLICATION_ID_PATTERN = re.compile(r'^(?P<name>.+)-(?P<code>\d+)\s*$')


def _parse_application_field(raw: str):
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


_BAD_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|\s]+')


def _sanitize_stream(name: str) -> str:
    """Strip characters that are illegal in Windows filenames, for use in
    the TDAReport_<STREAM>_<id>.html naming convention.
    """
    return _BAD_FILENAME_CHARS.sub('_', name).strip('_') or 'UNKNOWN'


def _get_work_item(rwi_id: str, client) -> dict:
    """Fetch one RWI's fields + relations in a single API call."""
    resp = client.get('WorkItemsForRelease', rwi_id)
    return resp.json()


def _clear_directory(dir_path: pathlib.Path, pattern: str) -> int:
    """Delete all files matching `pattern` directly inside dir_path (if it
    exists). Used to ensure TDAAttachments/ and TDAFindings/ only ever
    contain output from the current run — not leftovers from a previous run
    with a different date range (which would otherwise accumulate forever
    and skew dtp-tda-trends analysis with stale data). Returns the count of
    files deleted.
    """
    if not dir_path.exists():
        return 0
    deleted = 0
    for f in dir_path.glob(pattern):
        if f.is_file():
            f.unlink()
            deleted += 1
    return deleted


def _find_tda_attachment(relations: list, stream: str, release_id: str):
    """
    Find the best TDA HTML report attachment from a work item's relations list.

    Recognised filename patterns (case-insensitive):
      - TDAReport_<STREAM>_<id>.html          (original)
      - TDA_Report_<STREAM>_<id>.html         (underscore variant)
      - Annotated_TDA_Report_<STREAM>_<id>.html   (browser "Save Annotated
        Report" download, named from the HTML <title> tag's sanitized text)
      - Annotated_TDAReport_<STREAM>_<id>.html    (reviewer manually prepends
        "Annotated_" to the original TDAReport_ filename — no inserted
        underscore, a distinct but equally real naming variant)

    Priority:
      1. Exact match on the preferred name for each pattern, in pattern order
         (TDAReport preferred over TDA_Report preferred over Annotated_TDA_Report)
      2. Any candidate matching any recognised pattern — pick most recently
         uploaded (latest addedDate)
    Returns the relation dict or None.
    """
    # Preferred exact names, in priority order.
    # Annotated_TDA_Report/Annotated_TDAReport are not included here — their
    # suffix is unpredictable, so they are matched purely by prefix and
    # selected via the addedDate fallback.
    preferred_names = [
        f"TDAReport_{stream}_{release_id}.html".lower(),
        f"TDA_Report_{stream}_{release_id}.html".lower(),
    ]

    # Regex that matches any of the four recognised prefixes
    _TDA_PREFIX = re.compile(
        r'^(TDAReport_|TDA_Report_|Annotated_TDA_Report_|Annotated_TDAReport_)', re.IGNORECASE
    )

    candidates = []
    for rel in relations:
        if rel.get('rel') != 'AttachedFile':
            continue
        name = rel.get('attributes', {}).get('name', '')
        if not name.lower().endswith('.html'):
            continue
        if not _TDA_PREFIX.match(name):
            continue
        candidates.append(rel)

    if not candidates:
        return None

    # Exact match — first hit in priority order wins
    candidate_names = {
        c['attributes'].get('name', '').lower(): c for c in candidates
    }
    for preferred in preferred_names:
        if preferred in candidate_names:
            return candidate_names[preferred]

    # Fallback: latest by addedDate
    def _added(rel):
        return rel.get('attributes', {}).get('addedDate', '')

    return sorted(candidates, key=_added, reverse=True)[0]


def _download_attachment(url: str, client, dest: pathlib.Path) -> None:
    """Download a raw attachment URL to dest."""
    client._throttle()
    client.set_proxy()
    r = client._session.get(url, headers=client.cfg.ado_headers, verify=False)
    r.raise_for_status()
    dest.write_bytes(r.content)


# ===========================================================================
# STEP 2 HELPERS  —  Parse TDA HTML reports into structured findings JSON
# ===========================================================================

SEV_CRITICAL = "critical"
SEV_MODERATE = "moderate"
SEV_MINOR    = "minor"
SEV_LOOKS    = "looksGood"

_SECTION_CLASS_MAP = {
    "critical":  SEV_CRITICAL,
    "moderate":  SEV_MODERATE,
    "minor":     SEV_MINOR,
    "looksgood": SEV_LOOKS,
}

_AREA_PATTERNS = [
    ("Sonar Coverage",      ["sonar coverage", "coverage below", "new code coverage", "overall coverage"]),
    ("Sonar Quality Gate",  ["quality gate", "sonarway"]),
    ("Genie Regression",    ["genie", "regression", "failure rate"]),
    ("Unit Tests",          ["unit test", "test pass", "tests passed", "tests failed"]),
    ("PIT",                 ["pit", "post implementation testing", "post-implementation"]),
    ("Story Traceability",  ["traceability", "test case", "source linked", "tc linked"]),
    ("App Architecture",    ["app arch", "application architecture", "asrm", "architecture"]),
    ("PO Reprioritization", ["reprioritization", "modified_after", "po re"]),
    ("SNOW / CHG",          ["snow", "chg", "change record", "servicenow"]),
    ("Release WI State",    ["release wi", "rwi state", "work item state"]),
    ("Collector / Drift",   ["collector version", "drift", "version mismatch"]),
]


def _classify_finding(text: str) -> str:
    lower = text.lower()
    for area, keywords in _AREA_PATTERNS:
        if any(kw in lower for kw in keywords):
            return area
    return "Other"


# Reviewer annotation note → resolution status, in priority order. A note can
# contain language matching more than one category (e.g. "this was a false
# positive, now resolved"), so order reflects which classification should win:
# false_positive and resolved are the two "this is no longer live risk"
# outcomes (checked first), workaround is a mitigated-but-real issue,
# acknowledged means the reviewer has seen it but it is NOT yet addressed,
# and unresolved is the default when the note doesn't match anything.
_RESOLUTION_PATTERNS = [
    ("false_positive", [
        r"false positive", r"not a (real )?(failure|issue|bug)", r"reporting gap",
        r"no content change", r"cosmetic", r"tests exist and pass", r"works fine",
        r"incorrectly flagged", r"non[- ]issue",
    ]),
    ("resolved", [
        r"resolved", r"has been fixed", r"fixed now", r"remediated", r"remediation attached",
        r"issue fixed", r"now passing", r"no longer (an )?issue",
    ]),
    ("workaround", [
        r"workaround", r"manual(ly)? verif", r"alternative (approach|process)", r"mitigat",
    ]),
    ("acknowledged", [
        r"will be done", r"to be done", r"planned", r"approved", r"discussed and approved",
        r"accepted risk", r"acknowledg", r"tracked separately", r"follow[- ]?up",
        r"will be addressed",
    ]),
]


def _classify_resolution(note: str) -> str:
    """Heuristically classify a reviewer annotation note's resolution status.

    Fallback only — used when a recorded annotation has no explicit
    data-resolution attribute (legacy reports saved before the "Type of
    Remediation" dropdown was added). Returns one of: false_positive,
    resolved, workaround, acknowledged, unresolved (default when nothing
    matches, e.g. an empty/non-committal note).
    """
    lower = note.lower()
    for status, patterns in _RESOLUTION_PATTERNS:
        for pat in patterns:
            if re.search(pat, lower):
                return status
    return "unresolved"


_SENTINEL_PLACEHOLDER_RE = re.compile(
    r'^(none identified|no (critical|moderate) findings identified for this release)',
    re.IGNORECASE,
)

# Bare-word sentinel variants seen in some reports — the ENTIRE finding text
# is just one of these (not a prefix of a longer real finding), so they are
# matched as a full-string equality check rather than via the regex above.
_SENTINEL_PLACEHOLDER_EXACT = {'none.', 'none', 'n/a', 'none identified'}


def _is_sentinel_placeholder(text: str) -> bool:
    """Some reports (both "skill" and "script" modes) represent an *empty*
    CRITICAL/MODERATE category with a literal placeholder sentence, e.g.
    "None identified ✅" or "No CRITICAL findings identified for this
    release." (sometimes followed by additional explanatory text), or a bare
    word/short phrase like "None." as the entire finding text. This is not a
    real finding and must never be counted as one — otherwise every "clean"
    category inflates finding_counts/open_finding_counts by +1 and gets
    misclassified under the "Other" area."""
    stripped = text.strip()
    if stripped.rstrip('.').strip().lower() in _SENTINEL_PLACEHOLDER_EXACT:
        return True
    return bool(_SENTINEL_PLACEHOLDER_RE.match(stripped))


def _is_open_finding(item) -> bool:
    """A finding is still "open" (live risk) unless a reviewer annotation has
    marked it resolved or a false positive. Legacy plain-string findings
    (no annotation data) are always considered open."""
    if isinstance(item, dict):
        annotation = item.get('annotation')
        if annotation and annotation.get('resolution_status') in ('resolved', 'false_positive'):
            return False
    return True


def _finding_text(item) -> str:
    """Return the descriptive text of a finding item, whether it's the
    current {"text", "annotation"} dict shape or a legacy plain string."""
    return item.get('text', '') if isinstance(item, dict) else item


def _categorise_findings(findings: dict, open_only: bool = False) -> dict:
    """Return a dict: area → {critical: n, moderate: n, minor: n, looksGood: n}

    When open_only is True, findings annotated as resolved or false_positive
    are excluded from the counts (see _is_open_finding).
    """
    area_counts = {}
    for sev, items in findings.items():
        for item in items:
            if open_only and not _is_open_finding(item):
                continue
            area = _classify_finding(_finding_text(item))
            if area not in area_counts:
                area_counts[area] = {SEV_CRITICAL: 0, SEV_MODERATE: 0, SEV_MINOR: 0, SEV_LOOKS: 0}
            area_counts[area][sev] += 1
    return area_counts



class _TDAReportParser(HTMLParser):
    """
    State-machine HTML parser that extracts structured data from a TDA report,
    including any reviewer "remediation" annotations recorded on findings.

    Produces:
      self.result  — dict with all extracted fields

    Annotation HTML shape (rendered by the report's "Save Annotation" action):
        <div class="finding">
          ...finding text...
          <button class="rem-btn">📝 Remediate</button>
          <div class="rem-panel" id="rem-N">...editable form, placeholders only...</div>
          <div class="rem-recorded">
            <div class="rem-meta" data-resolution="resolved|unresolved|false_positive|workaround">✅ Annotated by <strong>NAME</strong> on TIMESTAMP &mdash; <span>LABEL</span></div>
            <div>NOTE TEXT</div>
          </div>
        </div>
    The data-resolution attribute reflects the reviewer's explicit "Type of
    Remediation" dropdown selection and is preferred over the heuristic note
    classification whenever present; it is absent on annotations saved by
    older report versions (pre-dropdown), which fall back to
    _classify_resolution(note).
    rem-panel is always present (even with no annotation) but only ever holds
    editable-form placeholder text, never real data, so it must be skipped
    entirely. rem-recorded only appears once a reviewer has actually saved an
    annotation.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.result = {
            "stream": "",
            "release_id": "",
            "report_date": "",
            "chg_id": "",
            "branch": "",
            "snow_state": "",
            "rwi_state": "",
            "report_mode": "",        # "skill" | "script" | "unknown"
            "collector_version": "",
            "verdict": "",            # "BLOCKED" | "CONDITIONAL PASS" | "PASS" | "unknown"
            "findings": {
                SEV_CRITICAL: [],
                SEV_MODERATE: [],
                SEV_MINOR:    [],
                SEV_LOOKS:    [],
            },
        }
        self._in_header      = False
        self._in_verdict     = False
        self._in_section     = None
        self._in_finding     = False
        self._current_finding_parts = []
        self._in_h1          = False
        self._finding_depth  = 0
        self._buf = ""

        # Annotation sub-state (only meaningful while self._in_finding).
        self._in_button          = False
        self._in_rem_panel       = False
        self._rem_panel_depth    = None
        self._in_rem_recorded    = False
        self._rem_recorded_depth = None
        self._in_rem_meta        = False
        self._rem_meta_depth     = None
        self._rem_meta_buf       = ""
        self._rem_note_parts     = []
        self._rem_meta_reviewer  = ""
        self._rem_meta_timestamp = ""
        self._rem_meta_resolution = ""
        self._rem_meta_reviewer_attr = ""
        self._rem_meta_timestamp_attr = ""

    def _flush(self) -> str:
        t = self._buf.strip()
        self._buf = ""
        return t

    @staticmethod
    def _class_list(attrs: list) -> list:
        for k, v in attrs:
            if k == 'class':
                return (v or "").lower().split()
        return []

    @staticmethod
    def _attr_value(attrs: list, name: str) -> str:
        for k, v in attrs:
            if k == name:
                return (v or "").strip()
        return ""

    def handle_starttag(self, tag, attrs):
        classes = self._class_list(attrs)

        if tag == 'div' and 'header' in classes:
            self._in_header = True
            return

        if tag == 'h1' and self._in_header:
            self._in_h1 = True
            self._buf = ""
            return

        if tag == 'div' and 'verdict' in classes:
            self._in_verdict = True
            self._buf = ""
            return

        if tag == 'div' and 'section' in classes:
            for c in classes:
                if c in _SECTION_CLASS_MAP:
                    self._in_section = _SECTION_CLASS_MAP[c]
                    break
            return

        if tag == 'div' and 'finding' in classes and self._in_section:
            self._in_finding = True
            self._finding_depth = 0
            self._current_finding_parts = []
            self._buf = ""
            self._in_button          = False
            self._in_rem_panel       = False
            self._rem_panel_depth    = None
            self._in_rem_recorded    = False
            self._rem_recorded_depth = None
            self._in_rem_meta        = False
            self._rem_meta_depth     = None
            self._rem_meta_buf       = ""
            self._rem_note_parts     = []
            self._rem_meta_reviewer  = ""
            self._rem_meta_timestamp = ""
            self._rem_meta_resolution = ""
            self._rem_meta_reviewer_attr = ""
            self._rem_meta_timestamp_attr = ""
            return

        if not self._in_finding:
            return

        if tag == 'button':
            self._in_button = True
            return

        # Depth tracking is restricted to <div> tags only. Void elements such
        # as <input> (used inside the annotation form) have a start tag but
        # no matching end tag in this HTML; a naive "increment on every tag"
        # counter would drift upward forever on those and corrupt
        # finding-boundary detection (siblings getting merged/dropped). Only
        # <div> is guaranteed to be well-formed/paired here.
        if tag == 'div':
            self._finding_depth += 1
            if 'rem-panel' in classes and not self._in_rem_panel:
                self._in_rem_panel = True
                self._rem_panel_depth = self._finding_depth
            elif 'rem-recorded' in classes and not self._in_rem_recorded:
                self._in_rem_recorded = True
                self._rem_recorded_depth = self._finding_depth
            elif 'rem-meta' in classes and self._in_rem_recorded and not self._in_rem_meta:
                self._in_rem_meta = True
                self._rem_meta_depth = self._finding_depth
                self._rem_meta_buf = ""
                self._rem_meta_resolution = self._attr_value(attrs, 'data-resolution')
                self._rem_meta_reviewer_attr = self._attr_value(attrs, 'data-reviewer')
                self._rem_meta_timestamp_attr = self._attr_value(attrs, 'data-timestamp')

    def handle_endtag(self, tag):
        if tag == 'div' and self._in_header:
            self._in_header = False
            self._parse_meta_block()
            return

        if tag == 'h1' and self._in_h1:
            self._in_h1 = False
            return

        if tag == 'div' and self._in_verdict:
            self._in_verdict = False
            self._parse_verdict(self._flush())
            return

        if not self._in_finding:
            return

        if tag == 'button':
            self._in_button = False
            return

        if tag != 'div':
            return

        if self._finding_depth > 0:
            self._finding_depth -= 1
            if self._in_rem_meta and self._finding_depth < self._rem_meta_depth:
                self._in_rem_meta = False
                self._parse_rem_meta()
            if self._in_rem_panel and self._finding_depth < self._rem_panel_depth:
                self._in_rem_panel = False
            if self._in_rem_recorded and self._finding_depth < self._rem_recorded_depth:
                self._in_rem_recorded = False
            return

        # finding_depth is 0 — this closing </div> is the finding's own.
        self._in_finding = False
        full_text = " ".join(self._current_finding_parts).strip()
        full_text = re.sub(r'\s+', ' ', full_text)

        annotation = None
        if self._rem_meta_reviewer or self._rem_note_parts:
            note = re.sub(r'\s+', ' ', " ".join(self._rem_note_parts).strip())
            annotation = {
                "reviewer": self._rem_meta_reviewer,
                "timestamp": self._rem_meta_timestamp,
                "note": note,
                "resolution_status": self._rem_meta_resolution or _classify_resolution(note),
            }

        if full_text and self._in_section and not _is_sentinel_placeholder(full_text):
            self.result['findings'][self._in_section].append({
                "text": full_text,
                "annotation": annotation,
            })

        self._current_finding_parts = []
        self._rem_note_parts = []
        self._buf = ""
        return

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self._in_header:
            self._buf += data
            return
        if self._in_verdict:
            self._buf += data
            return
        if self._in_finding:
            if self._in_rem_panel:
                return  # editable form placeholders/labels — never real data
            if self._in_button:
                return  # button labels, e.g. "📝 Remediate"
            if self._in_rem_meta:
                self._rem_meta_buf += data
                return
            if self._in_rem_recorded:
                self._rem_note_parts.append(text)
                return
            self._current_finding_parts.append(text)
            return

    def _parse_rem_meta(self):
        """Parse reviewer/timestamp from a rem-meta div.

        Newer reports carry explicit data-reviewer / data-timestamp
        attributes on the rem-meta div (preferred — unambiguous, no text
        parsing needed). Older reports (pre dropdown/attribute support)
        only have the visible '✅ Annotated by NAME on TIMESTAMP' text, so
        fall back to regex extraction for those."""
        if self._rem_meta_reviewer_attr or self._rem_meta_timestamp_attr:
            self._rem_meta_reviewer = self._rem_meta_reviewer_attr
            self._rem_meta_timestamp = self._rem_meta_timestamp_attr
            return
        text = re.sub(r'\s+', ' ', self._rem_meta_buf).strip()
        m = re.search(r'Annotated by\s+(.+?)\s+on\s+(.+)$', text, re.IGNORECASE)
        if m:
            self._rem_meta_reviewer = m.group(1).strip()
            self._rem_meta_timestamp = m.group(2).strip()
        else:
            self._rem_meta_reviewer = text
            self._rem_meta_timestamp = ""

    def _parse_meta_block(self):
        text = re.sub(r'\s+', ' ', self._flush())

        def _extract(label: str) -> str:
            m = re.search(
                rf'{re.escape(label)}:\s*([^|<\n]+?)(?:\s*\||\s*<br|\s*$)',
                text, re.IGNORECASE
            )
            return m.group(1).strip() if m else ""

        self.result['release_id']        = _extract('Release ID')
        self.result['stream']            = _extract('Stream')
        self.result['branch']            = _extract('Branch')
        self.result['chg_id']            = _extract('CHG')
        self.result['snow_state']        = _extract('SNOW State')
        self.result['rwi_state']         = _extract('Release WI State')
        self.result['report_date']       = _extract('Report Date')
        self.result['collector_version'] = _extract('Collector Version')

        mode_raw = _extract('Report Mode')
        if 'script' in mode_raw.lower():
            self.result['report_mode'] = 'script'
        elif 'skill' in text.lower() and 'script' not in mode_raw.lower():
            self.result['report_mode'] = 'skill'
        else:
            self.result['report_mode'] = 'unknown'

    def _parse_verdict(self, text: str):
        t = text.upper()
        if 'BLOCKED' in t:
            self.result['verdict'] = 'BLOCKED'
        elif 'CONDITIONAL' in t:
            self.result['verdict'] = 'CONDITIONAL PASS'
        elif 'PASS' in t:
            self.result['verdict'] = 'PASS'
        else:
            self.result['verdict'] = 'unknown'


def _extract_from_file(html_path: pathlib.Path) -> dict:
    """Parse one HTML report file and return the findings dict."""
    content = html_path.read_text(encoding='utf-8', errors='replace')
    parser = _TDAReportParser()
    parser.feed(content)
    result = parser.result

    # Always prefer stream / release_id derived from the filename — the file was
    # named TDAReport_<STREAM>_<id>.html by our own download step, so it is
    # guaranteed to be clean and correct.  Only fall back to the HTML-parsed
    # values when the filename doesn't match the expected pattern (e.g. a report
    # loaded manually with an arbitrary name).
    # NOTE: <STREAM> can itself contain underscores (e.g. "BLADE_BA", derived
    # from the Application Name), so match greedily up to the LAST underscore
    # immediately before the trailing release id digits, rather than stopping
    # at the first underscore.
    stem = html_path.stem  # e.g. TDAReport_BLADE_BA_14722369
    m = re.match(r'TDAReport_(.+)_(\d+)$', stem, re.IGNORECASE)
    if m:
        result['stream']     = m.group(1).upper()
        result['release_id'] = m.group(2)

    result['finding_counts'] = {
        SEV_CRITICAL: len(result['findings'][SEV_CRITICAL]),
        SEV_MODERATE: len(result['findings'][SEV_MODERATE]),
        SEV_MINOR:    len(result['findings'][SEV_MINOR]),
        SEV_LOOKS:    len(result['findings'][SEV_LOOKS]),
    }
    result['findings_by_area'] = _categorise_findings(result['findings'])

    # "Open" = excluding findings a reviewer has annotated as resolved or a
    # false positive — these no longer represent live risk. The raw
    # finding_counts / findings_by_area above are left untouched for full
    # audit-trail transparency; open_* is what trend/compliance analysis
    # should treat as the primary signal.
    result['open_finding_counts'] = {
        sev: sum(1 for item in result['findings'][sev] if _is_open_finding(item))
        for sev in (SEV_CRITICAL, SEV_MODERATE, SEV_MINOR, SEV_LOOKS)
    }
    result['open_findings_by_area'] = _categorise_findings(result['findings'], open_only=True)
    return result


# ===========================================================================
# Main pipeline
# ===========================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description='TDA audit pipeline: discover RWIs via an ADO query (Release/Released/FMQPR, '
                    'filtered by Actual Release Date range), download their signed-off reports, '
                    'then extract findings.'
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
             "matching RWIs are fetched at all). Omit to process every RWI found in the date "
             "range (default behaviour).",
    )
    parser.add_argument(
        '--attachments',
        help='Downloaded HTML directory, relative to the workspace (default: TDA_OUTPUT_DIR/audit/attachments)',
    )
    parser.add_argument(
        '--findings',
        help='Extracted JSON directory, relative to the workspace (default: TDA_OUTPUT_DIR/audit/findings)',
    )
    parser.add_argument(
        '--skip-download', action='store_true',
        help='Skip Step 1 (download) and go straight to Step 2 extraction. '
             'Use when HTML reports are already present in the attachments folder.',
    )
    args = parser.parse_args()

    # Parse help before loading configuration or optional collector dependencies.
    for ancestor in pathlib.Path(__file__).resolve().parents:
        if (ancestor / 'release_clinic_env.py').is_file():
            sys.path.insert(0, str(ancestor))
            break
    from release_clinic_env import load_environment, workspace_path

    load_environment()
    audit_dir = workspace_path(os.environ['TDA_OUTPUT_DIR']) / 'audit'
    attachments_dir = workspace_path(args.attachments) if args.attachments else audit_dir / 'attachments'
    findings_dir = workspace_path(args.findings) if args.findings else audit_dir / 'findings'

    # ── Step 1: Discover + Download ───────────────────────────────────────
    if not args.skip_download:
        log.info("=" * 60)
        log.info("STEP 1 — Discovering RWIs via ADO query and downloading TDA reports")
        log.info("=" * 60)

        attachments_dir.mkdir(parents=True, exist_ok=True)
        cleared = _clear_directory(attachments_dir, '*.html')
        if cleared:
            log.info("Cleared %d stale HTML report(s) from a previous run in %s", cleared, attachments_dir)

        # Bootstrap ADO client
        sys.path.insert(0, str(_SCRIPTS_DIR))
        from tda.config import Config, load_env_file
        from tda.http_client import ADOClient

        load_env_file()
        cfg    = Config.from_env()
        client = ADOClient(cfg)

        application_id_value = None
        if args.application_id:
            application_id_value = _resolve_application_id_filter(
                client, _QUERY_WORK_ITEM_TYPE, args.application_id,
            )
            log.info("Application Id filter '%s' resolved to Custom.ApplicationID = '%s'",
                      args.application_id, application_id_value)

        # Discover RWIs via the WIQL query — this output IS the input to the
        # download step below (no config/sources file involved).
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

        dl_downloaded = 0
        dl_skipped    = 0
        for i, rwi_id in enumerate(rwi_ids):
            if i > 0:
                time.sleep(_ADO_CALL_DELAY_SECONDS)

            release_id = rwi_id

            log.info("[RWI %s]  Fetching fields + relations ...", rwi_id)
            try:
                wi = _get_work_item(rwi_id, client)
            except Exception as exc:
                log.error("[RWI %s]  Failed to fetch work item: %s", rwi_id, exc)
                dl_skipped += 1
                continue

            fields = wi.get('fields', {}) or {}
            relations = wi.get('relations', []) or []
            app_name, _app_id = _parse_application_field(fields.get('Custom.ApplicationID', ''))
            stream = _sanitize_stream(app_name.upper()) if app_name else 'UNKNOWN'

            rel = _find_tda_attachment(relations, stream, release_id)
            if rel is None:
                log.warning(
                    "[%s / %s]  No TDAReport_*.html attachment found on RWI %s "
                    "(total attachments: %d)",
                    stream, release_id, rwi_id,
                    sum(1 for r in relations if r.get('rel') == 'AttachedFile'),
                )
                dl_skipped += 1
                continue

            attachment_name = rel['attributes'].get('name', f'TDAReport_{stream}_{release_id}.html')
            added_date      = rel.get('attributes', {}).get('addedDate', 'unknown')
            log.info("[%s / %s]  Found: %s  (uploaded: %s)", stream, release_id, attachment_name, added_date)

            dest_path = attachments_dir / f"TDAReport_{stream}_{release_id}.html"
            try:
                _download_attachment(rel.get('url', ''), client, dest_path)
                log.info("[%s / %s]  Saved: %s  (%d bytes)", stream, release_id, dest_path, dest_path.stat().st_size)
                dl_downloaded += 1
            except Exception as exc:
                log.error("[%s / %s]  Download failed: %s", stream, release_id, exc)
                dl_skipped += 1

        print()
        log.info("Step 1 complete.  Downloaded: %d   Skipped/failed: %d", dl_downloaded, dl_skipped)
    else:
        log.info("Step 1 skipped (--skip-download).")

    # ── Step 2: Extract findings ──────────────────────────────────────────
    log.info("=" * 60)
    log.info("STEP 2 — Extracting findings from HTML reports")
    log.info("=" * 60)

    if not attachments_dir.exists():
        log.error("Attachments directory not found: %s", attachments_dir)
        sys.exit(1)

    findings_dir.mkdir(parents=True, exist_ok=True)
    cleared = _clear_directory(findings_dir, '*.json')
    if cleared:
        log.info("Cleared %d stale findings file(s) from a previous run in %s", cleared, findings_dir)
    html_files = sorted(attachments_dir.glob('TDAReport_*.html'))

    if not html_files:
        log.error("No TDAReport_*.html files found in %s", attachments_dir)
        sys.exit(1)

    log.info("Found %d HTML report(s) to parse", len(html_files))

    ex_processed = 0
    ex_errors    = 0
    for html_path in html_files:
        log.info("Parsing: %s", html_path.name)
        try:
            result = _extract_from_file(html_path)
        except Exception as exc:
            log.error("Failed to parse %s: %s", html_path.name, exc)
            ex_errors += 1
            continue

        stream     = result.get('stream', 'UNKNOWN')
        release_id = result.get('release_id', html_path.stem)
        # Strip characters that are illegal in Windows filenames
        _bad = re.compile(r'[\\/:*?"<>|\s]+')
        safe_stream     = _bad.sub('_', stream).strip('_') or 'UNKNOWN'
        safe_release_id = _bad.sub('_', release_id).strip('_') or html_path.stem
        out_path   = findings_dir / f"TDAFindings_{safe_stream}_{safe_release_id}.json"

        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        counts = result['finding_counts']
        log.info(
            "  -> %s  |  verdict: %-18s  C:%d  M:%d  m:%d  G:%d",
            out_path.name, result.get('verdict', 'unknown'),
            counts['critical'], counts['moderate'],
            counts['minor'],    counts['looksGood'],
        )
        ex_processed += 1

    # ── Summary ────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("TDA AUDIT PIPELINE — COMPLETE")
    print("=" * 60)
    if not args.skip_download:
        print(f"  Step 1 — Downloaded:  {dl_downloaded}  (skipped/failed: {dl_skipped})")
    print(f"  Step 2 — Parsed:      {ex_processed}  (errors: {ex_errors})")
    print()
    print(f"  HTML reports:    {attachments_dir.resolve()}")
    print(f"  Findings JSON:   {findings_dir.resolve()}")
    print()
    print("Next step: invoke the  dtp-tda-trends  skill, pointing it at the findings folder above.")


if __name__ == '__main__':
    main()
