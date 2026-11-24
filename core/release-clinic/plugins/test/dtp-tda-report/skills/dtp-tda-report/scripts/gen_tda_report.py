#!/usr/bin/env python3
"""
gen_tda_report.py  —  Standalone TDA HTML report generator (hybrid approach)
=============================================================================
Reads an AutoTDAResults_<STREAM>_<release_id>.json (full) or
AutoTDASummary_<STREAM>_<release_id>.json (compact) file and produces a
self-contained HTML report identical in structure to the dtp-tda-report skill.

All deterministic checks are applied in Python (fast, consistent).
Three checks requiring natural-language judgement are flagged as
"[Requires Review]" placeholders — the LLM only needs to fill those in,
cutting LLM involvement to a fraction of a full skill invocation.

Usage (run from the scripts/ directory):
    python gen_tda_report.py AutoTDAReports/AutoTDAResults_BCF_15557366.json
    python gen_tda_report.py AutoTDAReports/AutoTDASummary_RATES_12169451.json

Output:
    TDA_OUTPUT_DIR/TDAReport_<STREAM>_<release_id>.html, or --output PATH.

Dependencies: Python 3.9+, no third-party packages required.

This script is STANDALONE — it does not import anything from the tda/ package
and does not modify any existing file. Safe to delete at any time.
"""

import argparse
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timezone, date
from html import escape as _esc

SKILL_VERSION = "1.10.2"
TODAY = date.today()
REPORT_DATE = TODAY.isoformat()

# ADO organisation/project used to build work-item hyperlinks (see wi_link() below).
# Set once in main() from the input JSON's top-level ado_organization/ado_project
# keys; falls back to sc-ado/FMQPR for JSON collected before those fields existed.
ADO_ORGANIZATION = "sc-ado"
ADO_PROJECT = "FMQPR"

# ---------------------------------------------------------------------------
# Severity constants
# ---------------------------------------------------------------------------
CRITICAL = "critical"
MODERATE = "moderate"
MINOR    = "minor"
LOOKS    = "looksGood"

# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------
CSS = """
body{font-family:Segoe UI,Arial,sans-serif;margin:0;padding:0;background:#f4f6f9;color:#222;}
.header{background:#1a3a5c;color:white;padding:24px 32px;}
.header h1{margin:0 0 6px 0;font-size:22px;}
.header .meta{font-size:13px;opacity:.85;line-height:1.8;}
.section{margin:20px 32px;}
h2{font-size:15px;margin-bottom:10px;padding:8px 14px;border-radius:4px;color:white;}
.critical h2{background:#c0392b;}
.moderate h2{background:#e67e22;}
.minor h2{background:#2980b9;}
.looksGood h2{background:#27ae60;}
.tables h2{background:#34495e;}
.finding{background:white;padding:10px 14px;margin-bottom:8px;border-radius:3px;font-size:14px;border-left:4px solid #ccc;}
.critical .finding{border-color:#c0392b;}
.moderate .finding{border-color:#e67e22;}
.minor .finding{border-color:#2980b9;}
.looksGood .finding{border-color:#27ae60;}
table{width:100%;border-collapse:collapse;background:white;font-size:13px;margin-bottom:20px;}
th{background:#1a3a5c;color:white;padding:8px 10px;text-align:left;}
td{padding:7px 10px;border-bottom:1px solid #e8e8e8;}
tr:nth-child(even) td{background:#f9f9f9;}
.verdict{margin:24px 32px;padding:20px 24px;border-radius:6px;font-size:17px;font-weight:bold;color:white;text-align:center;}
.verdict.blocked{background:#c0392b;}
.verdict.conditional{background:#e67e22;}
.verdict.pass{background:#27ae60;}
.badge{display:inline-block;border-radius:12px;padding:2px 10px;font-size:12px;color:white;margin-left:8px;}
.c-badge{background:#922b21;}
.m-badge{background:#a04000;}
.i-badge{background:#1a5276;}
.g-badge{background:#1e8449;}
.section-title{font-weight:600;font-size:14px;margin:16px 0 6px 0;color:#444;}
.warn{color:#c0392b;font-weight:bold;}
.ok{color:#27ae60;font-weight:bold;}
.na{color:#888;font-style:italic;}
.footer{text-align:center;padding:16px;font-size:11px;color:#999;border-top:1px solid #ddd;margin-top:8px;}
.info-note{background:#e8f4fd;border-left:4px solid #2980b9;padding:10px 14px;margin:8px 0 12px 0;font-size:13px;border-radius:3px;}
.flash-warning{background:#c0392b;color:#ffffff;font-weight:700;font-size:15px;line-height:1.6;text-align:center;padding:14px 24px;margin:20px 32px 0 32px;border-radius:5px;border:3px solid #c0392b;animation:flashWarning 3s ease-in-out infinite;}
@keyframes flashWarning{50%{background:#fdecea;color:#c0392b;}}
.script-notice{background:#f0f4ff;border:1px solid #a0b4e0;border-left:5px solid #2c5fa8;margin:20px 32px 0 32px;padding:16px 20px;border-radius:5px;font-size:13px;line-height:1.7;}
.script-notice h3{margin:0 0 8px 0;font-size:14px;color:#1a3a5c;}
.script-notice .sn-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px 24px;margin-top:10px;}
.script-notice .sn-col h4{margin:0 0 4px 0;font-size:13px;color:#1a3a5c;}
.script-notice ul{margin:2px 0 0 0;padding-left:18px;}
.script-notice li{margin-bottom:2px;}
.script-notice .sn-token{background:#fff7e6;border:1px solid #f0a500;border-radius:4px;padding:6px 10px;margin-top:10px;font-size:12px;color:#7a4f00;}
.rule-box{background:#eaf4fb;border-left:4px solid #2980b9;padding:10px 14px;margin:8px 0 16px 0;font-size:13px;border-radius:3px;}
.review-note{background:#fff8e1;border-left:4px solid #f39c12;padding:10px 14px;margin:8px 0 12px 0;font-size:13px;border-radius:3px;}
details.section{margin:20px 32px;}
details.tables summary{font-size:15px;margin-bottom:10px;padding:8px 14px;border-radius:4px;color:white;background:#34495e;cursor:pointer;user-select:none;list-style:revert;}
details.tables summary:hover{opacity:.9;}
details.tables[open] summary{margin-bottom:10px;}
details.tables .details-body{padding-top:4px;}
.rem-btn{margin-top:8px;padding:3px 10px;font-size:11px;border:1px solid #2980b9;background:white;color:#2980b9;border-radius:3px;cursor:pointer;float:right;}
.rem-btn:hover{background:#eaf4fb;}
.rem-panel{display:none;margin-top:8px;background:#f0faf4;border:1px solid #27ae60;border-radius:4px;padding:10px 12px;font-size:13px;clear:both;}
.rem-panel.open{display:block;}
.rem-panel label{display:block;font-size:11px;color:#555;margin-bottom:2px;margin-top:6px;}
.rem-panel input,.rem-panel textarea,.rem-panel select{width:100%;box-sizing:border-box;border:1px solid #ccc;border-radius:3px;padding:4px 7px;font-size:13px;font-family:inherit;}
.rem-panel textarea{resize:vertical;min-height:56px;}
.rem-panel .rem-actions{margin-top:8px;display:flex;gap:8px;}
.rem-panel .rem-save{background:#27ae60;color:white;border:none;border-radius:3px;padding:4px 14px;cursor:pointer;font-size:12px;}
.rem-panel .rem-cancel{background:#e0e0e0;color:#333;border:none;border-radius:3px;padding:4px 12px;cursor:pointer;font-size:12px;}
.rem-recorded{margin-top:8px;background:#eafaf1;border-left:4px solid #27ae60;padding:8px 12px;border-radius:3px;font-size:12px;clear:both;}
.rem-recorded .rem-meta{font-size:11.5px;color:#444;margin-bottom:5px;}
.rem-recorded .rem-note{font-size:13px;color:#222;}
.rem-status-badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:10.5px;font-weight:700;color:white;}
.rem-status-resolved{background:#27ae60;}
.rem-status-unresolved{background:#c0392b;}
.rem-status-false_positive{background:#2980b9;}
.rem-status-workaround{background:#8e44ad;}
.rem-toolbar{background:#1a3a5c;padding:8px 32px;display:flex;align-items:center;gap:14px;}
.rem-toolbar span{color:#aed6f1;font-size:12px;flex:1;}
.rem-toolbar button{padding:5px 14px;font-size:12px;border:none;border-radius:3px;cursor:pointer;}
.rem-export-btn{background:#27ae60;color:white;}
.rem-export-btn:hover{background:#1e8449;}
.rem-setname-btn{background:rgba(255,255,255,.15);color:white;border:1px solid rgba(255,255,255,.3)!important;}
.rem-setname-btn:hover{background:rgba(255,255,255,.25);}
.rem-export-btn.locked{background:#95a5a6;}
.rem-export-btn.locked:hover{background:#95a5a6;}
.rem-missing{outline:3px solid #c0392b!important;outline-offset:2px;animation:remPulse 1.2s ease-in-out 3;}
@keyframes remPulse{0%,100%{background-color:transparent;}50%{background-color:#fdecea;}}
"""

JS = r"""
var _remName = localStorage.getItem('tda_rem_name') || '';
var _REM_TYPE_LABELS = {resolved:'Resolved', unresolved:'Unresolved', false_positive:'False Positive', workaround:'Workaround'};
function remSetName() {
  var n = prompt('Enter your name (will appear on all annotations in this session):', _remName);
  if (n !== null) { _remName = n.trim(); localStorage.setItem('tda_rem_name', _remName); }
  _updateToolbar();
}
function _updateToolbar() {
  var info = document.getElementById('remToolbarInfo');
  var totalMandatory = document.querySelectorAll('[data-rem-mandatory="true"]').length;
  var missingMandatory = _getMandatoryUnannotated().length;
  var mandatoryHtml = '';
  if (totalMandatory > 0) {
    mandatoryHtml = missingMandatory > 0
      ? ' &mdash; <strong style="color:#ffd9d9;">' + (totalMandatory - missingMandatory) + '/' + totalMandatory + ' mandatory CRITICAL/MODERATE annotations complete (' + missingMandatory + ' remaining)</strong>'
      : ' &mdash; <strong>' + totalMandatory + '/' + totalMandatory + ' mandatory CRITICAL/MODERATE annotations complete &#9989;</strong>';
  }
  if (_remName) {
    var count = document.querySelectorAll('.rem-recorded').length;
    info.innerHTML = '&#128221; Reviewer: <strong>' + _escHtml(_remName) + '</strong> &mdash; ' + count + ' annotation(s) recorded.' + mandatoryHtml;
  } else {
    info.innerHTML = '&#128221; Remediation mode &mdash; set your name before annotating.' + mandatoryHtml;
  }
  var exportBtn = document.querySelector('.rem-export-btn');
  if (exportBtn) exportBtn.classList.toggle('locked', missingMandatory > 0);
}
function _escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function _formatTs(d) {
  var pad = function(n){return n<10?'0'+n:n;};
  return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())+' '+pad(d.getHours())+':'+pad(d.getMinutes());
}
document.addEventListener('DOMContentLoaded', function() {
  var findings = document.querySelectorAll('.finding');
  findings.forEach(function(f, idx) {
    if (f.querySelector('.rem-btn')) return;
    if (f.closest('.looksGood')) return;
    var isCritOrMod = !!(f.closest('.section.critical') || f.closest('.section.moderate'));
    var isSentinel = /^none identified/i.test(f.textContent.trim());
    var isMandatory = isCritOrMod && !isSentinel;
    if (isMandatory) f.setAttribute('data-rem-mandatory', 'true');
    var id = 'rem-' + idx;
    var btn = document.createElement('button');
    btn.className = 'rem-btn';
    btn.textContent = (isMandatory ? '\uD83D\uDD12 ' : '') + '\uD83D\uDCDD Remediate';
    if (isMandatory) btn.title = 'Mandatory: this CRITICAL/MODERATE finding must be annotated before the report can be saved.';
    btn.onclick = function() { remOpen(id); };
    var panel = document.createElement('div');
    panel.className = 'rem-panel';
    panel.id = id;
    panel.innerHTML =
      '<label>Reviewer name</label>' +
      '<input type="text" id="'+id+'-name" placeholder="Your name" />' +
      '<label>Type of Remediation</label>' +
      '<select id="'+id+'-type">' +
      '<option value="">-- Select --</option>' +
      '<option value="resolved">Resolved</option>' +
      '<option value="unresolved">Unresolved</option>' +
      '<option value="false_positive">False Positive</option>' +
      '<option value="workaround">Workaround</option>' +
      '</select>' +
      '<label>Remediation / response note</label>' +
      '<textarea id="'+id+'-note" placeholder="Describe the remediation applied or the reason this finding does not apply..."></textarea>' +
      '<div class="rem-actions">' +
      '<button class="rem-save" onclick="remSave(\''+id+'\')">Save Annotation</button>' +
      '<button class="rem-cancel" onclick="remClose(\''+id+'\')">Cancel</button></div>';
    f.appendChild(btn);
    f.appendChild(panel);
  });
  _updateToolbar();
});
function _getMandatoryUnannotated() {
  var missing = [];
  document.querySelectorAll('[data-rem-mandatory="true"]').forEach(function(f) {
    if (!f.querySelector('.rem-recorded')) missing.push(f);
  });
  return missing;
}
function remOpen(id) {
  var panel = document.getElementById(id);
  if (!panel) return;
  var isOpen = panel.classList.contains('open');
  document.querySelectorAll('.rem-panel.open').forEach(function(p){ p.classList.remove('open'); });
  if (!isOpen) {
    panel.classList.add('open');
    var nameField = document.getElementById(id + '-name');
    if (nameField && !nameField.value && _remName) nameField.value = _remName;
    panel.querySelector('textarea').focus();
  }
}
function remClose(id) {
  var panel = document.getElementById(id);
  if (panel) panel.classList.remove('open');
}
function remSave(id) {
  var nameField = document.getElementById(id + '-name');
  var typeField = document.getElementById(id + '-type');
  var noteField = document.getElementById(id + '-note');
  var name = (nameField ? nameField.value.trim() : '') || _remName || 'Unknown';
  var remType = typeField ? typeField.value : '';
  var note = noteField ? noteField.value.trim() : '';
  if (!remType) { alert('Please select a Type of Remediation before saving.'); return; }
  if (!note) { alert('Please enter a remediation note before saving.'); return; }
  if (name) { _remName = name; localStorage.setItem('tda_rem_name', name); }
  var ts = _formatTs(new Date());
  var typeLabel = _REM_TYPE_LABELS[remType] || remType;
  var recorded = document.createElement('div');
  recorded.className = 'rem-recorded';
  recorded.innerHTML =
    '<div class="rem-meta" data-resolution="' + remType + '" data-reviewer="' + _escHtml(name) + '" data-timestamp="' + ts + '">' +
    '<span class="rem-status-badge rem-status-' + remType + '">' + typeLabel + '</span>' +
    ' &nbsp;&middot;&nbsp; Reviewer: <strong>' + _escHtml(name) + '</strong>' +
    ' &nbsp;&middot;&nbsp; ' + ts + '</div>' +
    '<div class="rem-note"><strong>Remediation note:</strong> ' + _escHtml(note).replace(/\n/g,'<br>') + '</div>';
  var panel = document.getElementById(id);
  var f = panel.closest('.finding');
  panel.classList.remove('open');
  panel.parentNode.insertBefore(recorded, panel.nextSibling);
  if (f) f.classList.remove('rem-missing');
  if (noteField) noteField.value = '';
  if (typeField) typeField.value = '';
  _updateToolbar();
}
function remExport() {
  var missing = _getMandatoryUnannotated();
  if (missing.length > 0) {
    missing.forEach(function(f){ f.classList.add('rem-missing'); });
    missing[0].scrollIntoView({behavior: 'smooth', block: 'center'});
    alert('Cannot save: ' + missing.length + ' CRITICAL/MODERATE finding(s) still need an annotation.\n\nEvery CRITICAL/MODERATE observation must be annotated (Resolved / Unresolved / False Positive / Workaround, with a note) before the report can be exported. The affected finding(s) are now highlighted in red below \u2014 click "Remediate" on each one, save an annotation, then try Save Annotated Report again.');
    return;
  }
  document.querySelectorAll('.rem-panel.open').forEach(function(p){ p.classList.remove('open'); });
  var html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
  var blob = new Blob([html], {type: 'text/html;charset=utf-8'});
  var a = document.createElement('a');
  var title = document.title.replace(/[^a-zA-Z0-9_\-. ]/g, '_').replace(/ /g, '_');
  a.href = URL.createObjectURL(blob);
  a.download = 'Annotated_' + title + '.html';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
}
"""

# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------
def e(s):
    """HTML-escape a plain string value."""
    return _esc(str(s)) if s is not None else ""

def fmt_date(iso):
    """Return YYYY-MM-DD from an ISO-8601 string, or the original if unparseable."""
    if not iso:
        return ""
    try:
        return iso[:10]
    except Exception:
        return str(iso)

def days_from_today(iso):
    """Return days until expiry (negative = expired)."""
    try:
        d = date.fromisoformat(iso[:10])
        return (d - TODAY).days
    except Exception:
        return None

def wi_link(wid):
    """Wrap a bare Story/Bug/Test Case/WI ID in a clickable ADO work-item hyperlink.
    Returns an empty string for falsy input. The returned string is pre-escaped
    HTML — do NOT pass it through e() again (same guardrail as ok_span/warn_span)."""
    s = str(wid).strip() if wid is not None else ""
    if not s:
        return ""
    s_esc = e(s)
    return (f'<a href="https://dev.azure.com/{ADO_ORGANIZATION}/{ADO_PROJECT}/_workitems/edit/{s_esc}" '
            f'target="_blank" rel="noopener">{s_esc}</a>')

def ok_span(text):
    # Do NOT call e() here — callers pass pre-escaped content or HTML entities
    return f'<span class="ok">{text}</span>'

def warn_span(text):
    return f'<span class="warn">{text}</span>'

def na_span(text="N/A"):
    return f'<span class="na">{text}</span>'

def td(content, cls=""):
    attr = f' class="{cls}"' if cls else ""
    return f"<td{attr}>{content}</td>"

def tr(*cells):
    return "<tr>" + "".join(cells) + "</tr>\n"

def empty_row(cols, text="None identified"):
    # Do NOT call e() — empty_text strings may contain HTML entities (&mdash; etc.)
    return f'<tr><td colspan="{cols}" class="na">{text}</td></tr>\n'

def finding_html(title, detail):
    """Render a single .finding div (title already HTML, detail already HTML)."""
    return f'<div class="finding"><strong>{title}</strong>: {detail}</div>\n'

def table_html(headers, rows_html, empty_text="None identified"):
    # Headers may contain HTML entities (e.g. &ge;) — do NOT escape them
    th_cells = "".join(f"<th>{h}</th>" for h in headers)
    body = rows_html if rows_html.strip() else empty_row(len(headers), empty_text)
    return f"<table><tr>{th_cells}</tr>\n{body}</table>\n"

# ---------------------------------------------------------------------------
# Version drift
# ---------------------------------------------------------------------------
def drift_indicator(collector_version):
    if not collector_version:
        return '<span style="color:#c0392b;font-weight:bold;">&#9888; Unknown</span>', MINOR
    if collector_version == SKILL_VERSION:
        return '<span style="color:#27ae60;font-weight:bold;">&#10003; No Drift</span>', None
    return '<span style="color:#c0392b;font-weight:bold;">&#9888; Drift</span>', MINOR

# ---------------------------------------------------------------------------
# Canonical release version extractor
# ---------------------------------------------------------------------------
def extract_canonical_version(title):
    if not title:
        return ""
    m = re.search(r'\d+\.\d+(?:\.\d+)?', title)
    return m.group(0) if m else ""

# ---------------------------------------------------------------------------
# Findings accumulator
# ---------------------------------------------------------------------------
class Report:
    def __init__(self):
        self.criticals = []
        self.moderates = []
        self.minors    = []
        self.looks     = []
        self._counters = {CRITICAL: 0, MODERATE: 0, MINOR: 0, LOOKS: 0}

    def add(self, severity, title, detail):
        n = self._counters[severity] + 1
        self._counters[severity] = n
        item = finding_html(f"[{n}] {title}", detail)
        getattr(self, {CRITICAL:"criticals",MODERATE:"moderates",MINOR:"minors",LOOKS:"looks"}[severity]).append(item)

    def count(self, severity):
        return self._counters[severity]

# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def analyse(data: dict) -> Report:
    r = Report()
    stream = data.get("release_stream", "")
    release_id = data.get("release_id", "")

    # ── detect format ──────────────────────────────────────────────────────
    is_compact = "test_results_summary" in data and "stories_summary" in data

    # ── collector version drift ────────────────────────────────────────────
    collector_ver = data.get("collector_version", "")
    _drift_span, drift_sev = drift_indicator(collector_ver)
    if drift_sev == MINOR:
        if not collector_ver:
            r.add(MINOR, "Collector Version Unknown",
                  "<code>collector_version</code> is not present in this JSON — the collector predates version "
                  "tracking (introduced in v1.7.0). The report may be missing fields added in later collector versions. "
                  "Recommend re-running the collector with the latest version.")
        else:
            r.add(MINOR, "Collector / Skill Version Drift",
                  f"Version drift detected: this JSON was produced by collector v<code>{e(collector_ver)}</code> but is "
                  f"being analysed by script v<code>{SKILL_VERSION}</code>. Fields added in the newer version may be "
                  "absent, causing silent gaps in some checks. Recommend aligning both to the same version.")

    # ── release WI ────────────────────────────────────────────────────────
    rfs = data.get("release_features", [{}])
    rf  = rfs[0] if rfs else {}
    rwi_title  = rf.get("System.Title", "")
    rwi_state  = rf.get("System.State", "")
    chg_id     = rf.get("Custom.CHGID", "")
    branch_id  = rf.get("Branch Id", "")
    build_id   = rf.get("Build Id", "")
    rwi_cloned = str(rf.get("RWI Cloned Flag", "False")).strip().lower() == "true"
    po_appr    = rf.get("Custom.POApproval", "")
    tso_appr   = rf.get("Custom.TSOApproval", "")
    tsuo_appr  = rf.get("Custom.TSUOApproval", "")
    impl_plan  = rf.get("Custom.ImplementationPlan", "")
    backout    = rf.get("Custom.BackoutPlan", "")
    pit_plan_rwi = rf.get("Custom.PITPlan", "")
    canon_ver  = extract_canonical_version(rwi_title)

    # RWI Cloned
    if rwi_cloned:
        r.add(MINOR, "Release WI Was Cloned",
              "The Release WI was created by cloning another work item. The reviewer is expected to ensure that "
              "there are no stale links and content copied over from the original source.")

    # PO/TSO/TSUO
    missing_approvals = []
    for field, val, label in [("POApproval", po_appr, "PO"), ("TSOApproval", tso_appr, "TSO"), ("TSUOApproval", tsuo_appr, "TSUO")]:
        if val not in ("Yes", "yes"):
            missing_approvals.append(f"{label} ({e(val)})")
    if missing_approvals:
        r.add(MINOR, "PO/TSO/TSUO Approval Field(s) Not Set",
              f"The following approval field(s) show as missing/not &lsquo;Yes&rsquo; on the Release WI: "
              f"{', '.join(missing_approvals)}. These are enforced as a mandatory release-pipeline gate and "
              "are expected to self-resolve before/at release — not a blocker for this report.")

    # ── Implementation & Rollback Documentation — Equivalence Check (2026-10-13) ──
    # Supersedes the old standalone "AIG link present" check and the old always-MINOR
    # Implementation Plan / Backout Plan check. Mirrors dtp-tda-report SKILL.md v1.10.1's
    # "Implementation & Rollback Documentation — Equivalence Check": Implementation Plan /
    # Backout Plan (Change Manifest) are treated as alternate evidence sources equivalent
    # to the AIG document / rollback section, not independent requirements — only raise a
    # finding when a gate has NO source at all.
    impl_missing = not impl_plan or impl_plan.upper() == "NOT FOUND"
    backout_missing = not backout or backout.upper() == "NOT FOUND"
    aig_key_present = "aig_rollback_check" in data
    impl_key_present = "Custom.ImplementationPlan" in rf
    backout_key_present = "Custom.BackoutPlan" in rf

    if not (aig_key_present or impl_key_present or backout_key_present):
        # All relevant keys absent (pre-dates these fields) — skip silently, not a gap.
        pass
    else:
        aig_checks = data.get("aig_rollback_check", [])
        aig = aig_checks[0] if aig_checks else {}
        aig_present = bool(aig.get("Present"))
        aig_source = aig.get("Source", "")
        aig_artifact = aig.get("Artifact Name", "")
        aig_build_id = aig.get("Build Id", "")
        rollback_found = bool(aig.get("Rollback Section Found"))

        # Gate A — Implementation / Deployment steps
        impl_sources = []
        if aig_present and aig_source == "rwi_link":
            impl_sources.append("AIG document (Release WI link)")
        elif aig_present and aig_source == "build_artifact":
            impl_sources.append(f"AIG build artifact &lsquo;{e(aig_artifact)}&rsquo; on build &lsquo;{e(aig_build_id)}&rsquo;")
        if not impl_missing:
            impl_sources.append("Release WI Implementation Plan field")

        if impl_sources:
            r.add(LOOKS, "Implementation / Deployment Documentation",
                  f"Implementation/deployment steps are documented via {', '.join(impl_sources)}.")
        else:
            r.add(MODERATE, "Implementation / Deployment Documentation Missing",
                  "No implementation/deployment documentation was found — neither an AIG document (RWI link or "
                  "build artifact) nor the Release WI Change Manifest's <code>Custom.ImplementationPlan</code> "
                  "field is populated.")

        # Gate B — Rollback / Backout steps
        rollback_sources = []
        if aig_source == "rwi_link":
            rollback_sources.append("AIG document (Release WI link)")
        elif aig_source == "build_artifact" and rollback_found:
            rollback_sources.append(f"rollback section within AIG build artifact &lsquo;{e(aig_artifact)}&rsquo;")
        if not backout_missing:
            rollback_sources.append("Release WI Backout Plan field")

        if rollback_sources:
            r.add(LOOKS, "Rollback / Backout Documentation",
                  f"Rollback/backout steps are documented via {', '.join(rollback_sources)}.")
            if aig_source == "build_artifact" and not rollback_found and not backout_missing:
                r.add(MINOR, "AIG Artifact Missing Own Rollback Section",
                      f"The AIG build artifact (&lsquo;{e(aig_artifact)}&rsquo;) does not itself contain a "
                      "recognizable rollback section, but the Release WI's Backout Plan field is populated, "
                      "satisfying the rollback documentation gate via that alternate source. Recommend the AIG "
                      "artifact also be updated to include a rollback section for consistency.")
        else:
            r.add(MODERATE, "Rollback / Backout Documentation Missing",
                  "No rollback/backout documentation was found — neither a rollback section within the AIG "
                  "document, an RWI-linked AIG document, nor the Release WI Change Manifest's "
                  "<code>Custom.BackoutPlan</code> field is populated.")

    # ── SNOW ──────────────────────────────────────────────────────────────
    snow_enabled = data.get("snow_enabled", True)
    snow_features = data.get("snow_features", [])
    sf = snow_features[0] if snow_features else {}

    if not snow_enabled:
        r.add(MINOR, "SNOW / ServiceNow Not Enabled for This Stream",
              f"SNOW/ServiceNow tracking is not enabled for the <code>{e(stream)}</code> stream — "
              "CHG-related checks are not applicable for this release.")
        snow_state = "N/A"
        snow_desc  = "N/A"
        snow_risk  = ""
    elif not sf:
        r.add(MINOR, "SNOW Change Record Data Empty",
              "SNOW change record data is empty despite SNOW being enabled for this stream — verify the CHG "
              "number on the Release WI and SNOW connectivity for this collector run.")
        snow_state = "Unknown"
        snow_desc  = ""
        snow_risk  = ""
    else:
        snow_state = (sf.get("state") or [""])[0] if isinstance(sf.get("state"), list) else sf.get("state", "")
        snow_desc  = (sf.get("short_description") or [""])[0] if isinstance(sf.get("short_description"), list) else sf.get("short_description", "")
        snow_risk  = (sf.get("risk") or [""])[0] if isinstance(sf.get("risk"), list) else sf.get("risk", "")

        # Risk check
        if snow_risk.lower() in ("high", "very high"):
            r.add(CRITICAL, f"SNOW Change Risk: {e(snow_risk)}",
                  f"The ServiceNow change record CHG risk is <strong>{e(snow_risk)}</strong>. "
                  "High/Very High risk changes require additional approvals and scrutiny before release.")
        else:
            r.add(LOOKS, f"SNOW Change Risk: {e(snow_risk) or 'Not High'}",
                  f"SNOW change risk is <strong>{e(snow_risk or 'Not specified')}</strong> — not High or Very High.")

        # SNOW description vs ADO title version mismatch
        if canon_ver and snow_desc and canon_ver not in snow_desc:
            r.add(MODERATE, "SNOW Description Version Mismatch",
                  f"SNOW short description (<em>{e(snow_desc)}</em>) does not contain the expected release "
                  f"version <code>{e(canon_ver)}</code> from the ADO Release WI title (<em>{e(rwi_title)}</em>). "
                  "Verify the CHG record is for this release.")
        elif canon_ver and snow_desc:
            r.add(LOOKS, "SNOW Description Version Match",
                  f"SNOW description (<em>{e(snow_desc)}</em>) contains the expected version "
                  f"<code>{e(canon_ver)}</code>.")

    # ── Application approvals ─────────────────────────────────────────────
    app_features = data.get("application_features", [{}])
    af = app_features[0] if app_features else {}
    approval_fields = {
        "Application Architecture": "Custom.ApplicationArchitectureApprovalExpiryDate",
        "ASRM":                     "Custom.ASRMApprovalExpiryDate",
        "NFR":                      "Custom.NFRApprovalExpiryDate",
        "Test Environment Management": "Custom.TEMApprovalExpiryDate",
        "Test Strategy":            "Custom.TestStrategyApprovalExpiryDate",
    }
    app_approval_rows = ""
    if af:
        for label, field in approval_fields.items():
            val = af.get(field, "")
            if not val:
                continue
            d = days_from_today(val)
            expiry_str = fmt_date(val)
            if d is None:
                status = na_span("Unknown")
            elif d < 0:
                r.add(CRITICAL, f"Application Approval Expired: {label}",
                      f"The <strong>{e(label)}</strong> approval on Application WI expired on "
                      f"<strong>{e(expiry_str)}</strong> ({abs(d)} days ago). Must be renewed before release.")
                status = warn_span(f"CRITICAL — expired {abs(d)}d ago")
            elif d <= 90:
                r.add(MINOR, f"Application Approval Expiring Within 90 Days: {label}",
                      f"The <strong>{e(label)}</strong> approval expires on <strong>{e(expiry_str)}</strong> "
                      f"({d} days from today). Not yet expired — recommend initiating re-approval ahead of expiry.")
                status = warn_span(f"MINOR/Info — expires in {d}d")
            else:
                status = ok_span(f"Valid ({d}d remaining)")
            app_approval_rows += tr(td(e(label)), td(e(expiry_str)), td(status))

    # ── Confluence post-approval check ────────────────────────────────────
    conf_checks = af.get("confluence_post_approval_checks", []) if af else []
    conf_check_rows = ""
    conf_all_ok = True
    for cc in conf_checks:
        status_val = cc.get("status", "")
        label  = e(cc.get("label", ""))
        title_ = e(cc.get("page_title", ""))
        lmod   = e(fmt_date(cc.get("last_modified", "")))
        lappr  = e(fmt_date(cc.get("last_approval", "")))
        if status_val == "EDITED_AFTER_APPROVAL":
            conf_all_ok = False
            r.add(MODERATE, f"Confluence Post-Approval Edit: {cc.get('label','')}",
                  f"Application WI Confluence document &lsquo;{title_}&rsquo; (<code>{label}</code>) was last "
                  f"edited on <strong>{lmod}</strong> &mdash; AFTER the most recent approval recorded on "
                  f"<strong>{lappr}</strong>. The approver(s) may not have reviewed the current version.")
            conf_check_rows += tr(td(label), td(title_), td(warn_span(lmod)), td(e(lappr)), td(warn_span("EDITED AFTER APPROVAL")))
        elif status_val == "NO_APPROVAL_RECORDED":
            r.add(MINOR, f"Confluence No Approval Recorded: {cc.get('label','')}",
                  f"Application WI Confluence document &lsquo;{title_}&rsquo; (<code>{label}</code>) has no "
                  "approver comment recorded.")
            conf_check_rows += tr(td(label), td(title_), td(e(lmod)), td(na_span("None recorded")), td(warn_span("NO APPROVAL")))
        elif status_val == "PAGE_INACCESSIBLE":
            r.add(MINOR, f"Confluence Page Inaccessible: {cc.get('label','')}",
                  f"Application WI Confluence link (<code>{label}</code>) could not be accessed — post-approval "
                  "edit check could not be performed.")
            conf_check_rows += tr(td(label), td(na_span("Inaccessible")), td(na_span()), td(na_span()), td(warn_span("INACCESSIBLE")))
        else:  # OK
            conf_check_rows += tr(td(label), td(title_), td(e(lmod)), td(e(lappr)), td(ok_span("OK")))
    if conf_checks and conf_all_ok:
        r.add(LOOKS, "All Application WI Confluence Documents: No Post-Approval Edits",
              f"All {len(conf_checks)} Application WI Confluence document(s) were last modified before or at "
              "the time of their most recent recorded approval.")

    # ── PT / PIT checks ───────────────────────────────────────────────────
    ptf = (data.get("release_pt_features") or [{}])[0]
    pt_plan_exists   = (ptf.get("ReleasePTPlanExists") or ["NO"])[0] == "YES"
    pt_report_exists = (ptf.get("ReleasePTReportExists") or ["NO"])[0] == "YES"
    ptia_exists      = ptf.get("ReleasePTIAExists", "NO")
    ptia_just        = ptf.get("ReleasePTIAJustification", "")

    pt_plan_appr  = (ptf.get("ReleasePTPlanApproval") or [{}])[0]
    pt_report_appr = (ptf.get("ReleasePTReportApproval") or [{}])[0]
    ptia_title = ptf.get("ReleasePTIAPageTitle", "")

    # PT coverage gate
    has_pt_docs = pt_plan_exists and pt_report_exists
    has_ptia    = ptia_exists in ("YES", "TEXT")

    if not has_pt_docs and not has_ptia:
        r.add(CRITICAL, "PT Documentation Missing",
              "No PT documentation found &mdash; either PT Plan + PT Report or a PTIA (Confluence link or "
              "written justification) must be present before release.")
    elif has_pt_docs and has_ptia:
        r.add(MODERATE, "Both PT Documents and PTIA Present",
              "Both PT Plan/Report and a PTIA are present &mdash; only one set is expected.")

    # PT Plan accessibility and approval
    if pt_plan_exists:
        pp_accessible = pt_plan_appr.get("Page Accessible", "NO")
        pp_approved_by = pt_plan_appr.get("Approved By", [])
        pp_title = pt_plan_appr.get("Page Title", "")
        if pp_accessible != "YES":
            r.add(CRITICAL, "PT Plan Confluence Page Inaccessible",
                  f"PT Plan Confluence page is not accessible (<code>Page Accessible = NO</code>). "
                  "Verify the link on the Release WI.")
        elif not pp_approved_by:
            r.add(MODERATE, "PT Plan Not Approved",
                  f"PT Plan page &lsquo;{e(pp_title)}&rsquo; is accessible but has no recorded approver.")
        else:
            approver_str = ", ".join(pp_approved_by) if isinstance(pp_approved_by, list) else str(pp_approved_by)
            r.add(LOOKS, "PT Plan Approved",
                  f"&lsquo;{e(pp_title)}&rsquo; is accessible and approved by {e(approver_str)}.")

    # PT Report accessibility and approval
    if pt_report_exists:
        pr_accessible = pt_report_appr.get("Page Accessible", "NO")
        pr_approved_by = pt_report_appr.get("Approved By", [])
        pr_title = pt_report_appr.get("Page Title", "")
        if pr_accessible != "YES":
            r.add(CRITICAL, "PT Report Confluence Page Inaccessible",
                  f"PT Report Confluence page is not accessible (<code>Page Accessible = NO</code>). "
                  "Verify the link on the Release WI.")
        elif not pr_approved_by:
            r.add(MODERATE, "PT Report Not Approved",
                  f"PT Report page &lsquo;{e(pr_title)}&rsquo; is accessible but has no recorded approver.")
        else:
            approver_str = ", ".join(pr_approved_by) if isinstance(pr_approved_by, list) else str(pr_approved_by)
            r.add(LOOKS, "PT Report Approved",
                  f"&lsquo;{e(pr_title)}&rsquo; is accessible and approved by {e(approver_str)}.")

    # PTIA text justification — hybrid: rule-based heuristic + flag for LLM review
    if ptia_exists == "TEXT" and ptia_just:
        PLACEHOLDER_PATTERNS = [
            r"^n/?a$", r"^not required$", r"^no performance impact$", r"^pt not needed$",
            r"^n/a\b", r"^not applicable$",
        ]
        just_stripped = ptia_just.strip()
        is_placeholder = len(just_stripped) < 30 or any(
            re.match(p, just_stripped, re.IGNORECASE) for p in PLACEHOLDER_PATTERNS
        )
        snippet = (just_stripped[:150] + "...") if len(just_stripped) > 150 else just_stripped
        if is_placeholder:
            r.add(MODERATE, "PTIA Justification Appears Generic/Placeholder",
                  f"PTIA justification is present as text on the Release WI but appears generic or insufficient. "
                  f"Justification: <em>&ldquo;{e(snippet)}&rdquo;</em>. Release manager should confirm this "
                  "accurately reflects why PT was skipped.")
        else:
            # Heuristic says it's meaningful — flag for human confirmation
            r.add(MINOR, "PTIA Justification Present (Text) &mdash; Requires Review",
                  f'<div class="review-note">&#9888;&#65039; <strong>[Requires Review]</strong> PTIA justification '
                  f'is present as text on the Release WI. Justification: <em>&ldquo;{e(snippet)}&rdquo;</em>. '
                  "The automated heuristic suggests this is a meaningful justification, but a human reviewer "
                  "should confirm it is release-specific and not boilerplate.</div>")

    # PIT gate
    pit_result = (data.get("pit_result") or [{}])[0]
    pit_accessible = pit_result.get("Page Accessible", "NO")
    pit_approved_by = pit_result.get("Approved By", [])
    pit_page_title  = pit_result.get("Page Title", "")
    pit_source      = pit_result.get("PIT Source", "stream_config_pit_url")
    pit_via_review_comments = pit_source == "rwi_review_comments"
    pit_rwi_present = pit_plan_rwi and pit_plan_rwi.upper() not in ("NOT FOUND", "", "NONE")

    if pit_accessible == "YES":
        source_note = (
            " <em>(link found in the Release WI's Review Comments field, not the "
            "stream's standard PIT URL template.)</em>" if pit_via_review_comments else ""
        )
        if pit_approved_by:
            approver_str = ", ".join(pit_approved_by) if isinstance(pit_approved_by, list) else str(pit_approved_by)
            r.add(LOOKS, "PIT Confluence Page Accessible and Approved",
                  f"PIT page &lsquo;{e(pit_page_title)}&rsquo; is accessible and approved by {e(approver_str)}.{source_note}")
        else:
            # Empty approver — severity depends on release state
            if rwi_state == "Released":
                r.add(MODERATE, "PIT Confluence Page Has No Recorded Approver (Post-Release)",
                      f"PIT Confluence page &lsquo;{e(pit_page_title)}&rsquo; is accessible but has no recorded "
                      "approver, and the Release WI is in &lsquo;Released&rsquo; state. PIT approval sign-off "
                      f"should have been completed by now.{source_note}")
            else:
                r.add(MINOR, "PIT Confluence Page Has No Recorded Approver Yet",
                      f"PIT Confluence page &lsquo;{e(pit_page_title)}&rsquo; has no recorded approver yet. "
                      f"Expected to be completed before/at deployment.{source_note}")
    elif pit_rwi_present:
        r.add(MINOR, "PIT Plan Sourced from Release WI Change Manifest Field",
              "No PIT Confluence/SC Wiki page is accessible (checked both the stream's standard PIT URL "
              "template and the Release WI's <code>Custom.ReviewComments</code> field), but "
              "<code>Custom.PITPlan</code> is populated on the Release WI Change Manifest. Gate is satisfied "
              "via the RWI text field. <em>Note: execution of the PIT plan and approval sign-off cannot be "
              "independently verified by this tool &mdash; ownership remains with the application/release team.</em>")
    else:
        r.add(CRITICAL, "PIT Documentation Missing",
              "No PIT Confluence/SC Wiki page is accessible (checked both the stream's standard PIT URL "
              "template and the Release WI's <code>Custom.ReviewComments</code> field) AND "
              "<code>Custom.PITPlan</code> on the Release WI is not populated. None of the three sources "
              "satisfies the PIT gate. Must be resolved before deployment.")


    # ── Unit tests ────────────────────────────────────────────────────────
    unit_tests = data.get("unit_tests", [])
    if not unit_tests:
        r.add(MINOR, "Unit Test Data Not Available",
              "No unit test records found in the JSON. This may be expected for rwi-only mode releases.")
    else:
        ut_critical = []
        for ut in unit_tests:
            pname = ut.get("Pipeline Name", "Unknown")
            failed   = ut.get("Failed", 0)
            not_exec = ut.get("Not Executed", 0)
            others   = ut.get("increaseInOtherTests", 0)
            if failed > 0:
                ut_critical.append(f"{e(pname)}: <strong>{failed} failed</strong>")
            if not_exec > 0:
                ut_critical.append(f"{e(pname)}: <strong>{not_exec} not executed</strong>")
            if others > 0:
                ut_critical.append(f"{e(pname)}: <strong>{others} &lsquo;Others&rsquo;</strong> (unclassified)")
        if ut_critical:
            r.add(CRITICAL, "Unit Test Failures / Issues Detected",
                  "The following unit test issues require Dev Lead approval on the Release WI before proceeding: "
                  + "; ".join(ut_critical))
        else:
            total_passed = sum(ut.get("Passed", 0) for ut in unit_tests)
            total_all    = sum(ut.get("Total Tests", 0) for ut in unit_tests)
            r.add(LOOKS, f"Unit Tests: All Passed ({total_passed:,} / {total_all:,})",
                  f"All {total_passed:,} unit tests passed across {len(unit_tests)} pipeline(s). "
                  "Zero failed, zero not executed.")

    # ── Sonar ─────────────────────────────────────────────────────────────
    sonar_skipped     = data.get("sonar_skipped", False)
    sonar_skip_reason = data.get("sonar_skip_reason", "")
    sonar_coverage    = data.get("sonar_coverage", [])
    sonar_quality_gates = data.get("sonar_quality_gates", [])

    if sonar_skipped:
        r.add(LOOKS, "Sonar: Intentionally Skipped",
              f"Sonar coverage collection was intentionally skipped for this stream. "
              f"Reason: <em>{e(sonar_skip_reason)}</em>. Not applicable.")
    elif not sonar_coverage:
        r.add(CRITICAL, "Sonar Coverage Data Missing",
              "Sonar coverage data is empty and Sonar is not marked as skipped. This may indicate a "
              "collection failure. Verify Sonar connectivity and re-run the collector.")
    else:
        CONFIG_REPO_PATTERN = "fmdc-releases"
        sonar_issues = []
        for sc in sonar_coverage:
            pname = sc.get("Pipeline", sc.get("pipeline", "Unknown"))
            is_config_repo = CONFIG_REPO_PATTERN in pname.lower()
            overall = sc.get("coverage")
            new_cov  = sc.get("new_coverage")
            if overall is not None and float(overall) < 40:
                sonar_issues.append(f"{e(pname)}: overall coverage {overall}% &lt; 40%")
            if not is_config_repo:
                if new_cov is None:
                    sonar_issues.append(f"{e(pname)}: new code coverage is N/A (newCodeReferenceBranch not configured)")
                elif float(new_cov) < 40:
                    sonar_issues.append(f"{e(pname)}: new code coverage {new_cov}% &lt; 40%")
        if sonar_issues:
            r.add(CRITICAL, "Sonar Coverage Below Threshold",
                  "The following Sonar coverage issues were detected: " + "; ".join(sonar_issues))
        else:
            r.add(LOOKS, "Sonar Coverage: All Pipelines Above Threshold",
                  f"All {len(sonar_coverage)} pipeline(s) meet the &ge;40% overall coverage threshold.")

        # Quality gate check
        required_gate = "ESDLC-Sonarway-managed"  # default; could read from stream_config
        if sonar_quality_gates:
            non_compliant = [
                qg.get("Pipeline", "") for qg in sonar_quality_gates
                if qg.get("quality_gate_name", "").lower() != required_gate.lower()
            ]
            if non_compliant:
                r.add(CRITICAL, "Sonar Quality Gate Mismatch",
                      f"The following pipeline(s) do not use the required "
                      f"<code>{e(required_gate)}</code> quality gate: "
                      + ", ".join(e(p) for p in non_compliant))
            else:
                r.add(LOOKS, f"Sonar Quality Gate: All Pipelines Use {required_gate}",
                      f"All {len(sonar_quality_gates)} pipeline(s) are assigned the required "
                      f"<code>{e(required_gate)}</code> quality gate.")
        else:
            r.add(MINOR, "Sonar Quality Gate Data Not Available",
                  "Sonar quality gate data is absent from this JSON — re-run the collector to enable this check.")

    # ── Genie regression ──────────────────────────────────────────────────
    genie_count = data.get("genie_count", [{}])
    gc = genie_count[0] if genie_count else {}
    genie_source = gc.get("genie_source", "")
    genie_passed = gc.get("passed", 0)
    genie_failed = gc.get("failed", 0)
    genie_total  = genie_passed + genie_failed

    if genie_source in ("skipped", "test_management_api_error"):
        r.add(MINOR, "Genie Regression: Skipped / Not Collected",
              f"Regression data collection disabled or failed for this stream "
              f"(<code>{e(gc.get('skip_reason', genie_source))}</code>) &mdash; not evaluated.")
    elif genie_total == 0 and genie_passed == 0:
        r.add(MINOR, "Genie Regression: No Test Runs Found",
              "No Genie regression runs found (passed=0, failed=0). "
              "Verify that regression tests are being run and results published.")
    elif genie_failed == 0:
        r.add(LOOKS, f"Genie Regression: All Passed ({genie_passed:,} scenarios)",
              f"All {genie_passed:,} Genie regression scenarios passed. Zero failures.")
    else:
        rate = genie_failed / genie_total * 100 if genie_total else 0
        rate_str = f"{rate:.2f}%"
        if rate > 5:
            r.add(CRITICAL, f"Genie Regression Failure Rate: {rate_str} (> 5%)",
                  f"{genie_failed} of {genie_total:,} Genie scenarios failed ({rate_str}). "
                  "This exceeds the 5% CRITICAL threshold. All failed scenarios must be investigated before release.")
        elif rate >= 1:
            r.add(MODERATE, f"Genie Regression Failure Rate: {rate_str} (1&ndash;5%)",
                  f"{genie_failed} of {genie_total:,} Genie scenarios failed ({rate_str}). "
                  "Failure rate is within the MODERATE threshold (1&ndash;5%). Review the failure list.")
        else:
            r.add(MINOR, f"Genie Regression: Minor Failures ({rate_str} &lt; 1%)",
                  f"{genie_failed} of {genie_total:,} Genie scenarios failed ({rate_str}). "
                  "Failure rate is below 1% — note the failures and confirm they are known/accepted.")

    # ── Regression retest ─────────────────────────────────────────────────
    if genie_failed > 0:
        test_result_features = data.get("test_result_features", [])
        RETEST_STRICT = [
            r"re.?test.+automation.+regression",
            r"regression.+failure.+re.?test",
            r"manual.+retest.+regression",
            r"automation.+regression.+failure",
        ]
        RETEST_POTENTIAL = [r"failed.+tc", r"manual.+execution.+fail", r"regression.+manual"]
        retest_tc = None
        match_type = None
        for tc in test_result_features:
            name = tc.get("Test Name", "")
            for pat in RETEST_STRICT:
                if re.search(pat, name, re.IGNORECASE):
                    retest_tc = tc
                    match_type = "strict"
                    break
            if retest_tc:
                break
        if not retest_tc:
            for tc in test_result_features:
                name = tc.get("Test Name", "")
                for pat in RETEST_POTENTIAL:
                    if re.search(pat, name, re.IGNORECASE):
                        retest_tc = tc
                        match_type = "potential"
                        break
                if retest_tc:
                    break

        if not retest_tc:
            r.add(CRITICAL, "Regression Failure Retest TC Missing",
                  f"Genie regression has {genie_failed} failed scenario(s) but no manual re-test test case "
                  "covering regression failures was found in the test plan. A test case loosely titled "
                  "&lsquo;Re-Test Automation Regression Failures&rsquo; (or equivalent) is mandatory.")
        else:
            outcome  = retest_tc.get("Outcome", "")
            has_evidence = bool(retest_tc.get("Step-Attachments")) or (
                retest_tc.get("AttachmentName", "NOT AVAILABLE") != "NOT AVAILABLE"
            )
            tc_id   = retest_tc.get("TestCase Id", "")
            tc_name = retest_tc.get("Test Name", "")
            tc_link = wi_link(tc_id)
            if outcome.lower() != "passed":
                r.add(CRITICAL, f"Regression Retest TC Not Passed: {tc_link}",
                      f"Retest TC {tc_link} &lsquo;{e(tc_name)}&rsquo; has outcome "
                      f"<strong>{e(outcome)}</strong> &mdash; must be Passed with evidence.")
            elif not has_evidence:
                r.add(CRITICAL, f"Regression Retest TC Missing Evidence: {tc_link}",
                      f"Retest TC {tc_link} &lsquo;{e(tc_name)}&rsquo; is Passed but has no evidence attached.")
            elif match_type == "potential":
                r.add(MINOR, f"Regression Retest TC: Potential Match Found (Non-Standard Title): {tc_link}",
                      f"TC {tc_link} &lsquo;{e(tc_name)}&rsquo; appears to cover manual re-testing of "
                      f"the {genie_failed} failed Genie regression scenario(s) and is Passed with evidence &mdash; "
                      "gate satisfied. However, the title does not follow the standard naming convention. "
                      "Recommend renaming to &lsquo;Re-Test Automation Regression Failures&rsquo;.")
            else:
                r.add(LOOKS, f"Regression Retest TC: Found, Passed, Evidenced ({tc_link})",
                      f"TC {tc_link} &lsquo;{e(tc_name)}&rsquo; is Passed with evidence attached.")

    # ── Manual test execution ─────────────────────────────────────────────
    test_results = data.get("test_result_features", [])

    # Automation-Only Testing Strategy guardrail (2026-09-24, mirrors SKILL.md v1.9.3+):
    # some releases run their ENTIRE testing scope via automation (e.g. Genie), with no
    # manual test cases in the ADO Test Plan at all — for these, an empty Test Results
    # section is expected, not a data-quality gap. Check this BEFORE the "empty = CRITICAL"
    # rule below.
    tc_details_guard = data.get("test_case_details", [])
    no_manual_tc = (not tc_details_guard) or all(
        str(t.get("TC Automated", "")).strip().lower() == "automated" for t in tc_details_guard
    )
    genie_tag_split_guard = data.get("genie_tag_split", {}) or {}
    genie_tag_evidence = (genie_tag_split_guard.get("@tt_ST", 0) or 0) > 0 or \
                         (genie_tag_split_guard.get("@tt_IT", 0) or 0) > 0
    genie_breakdown_guard = data.get("genie_story_type_breakdown", [])
    genie_breakdown_evidence = any(
        (g.get("Genie ST Scenarios", 0) or 0) > 0 or (g.get("Genie IT Scenarios", 0) or 0) > 0
        for g in genie_breakdown_guard
    )
    automation_only = no_manual_tc and (genie_tag_evidence or genie_breakdown_evidence)

    if not test_results and not is_compact:
        if automation_only:
            r.add(LOOKS, "Automation-Only Testing Strategy (N/A — No Manual Test Results Expected)",
                  "This release uses an automation-only testing strategy — the ADO Test Plan contains no manual "
                  "test cases (<code>test_case_details</code> is empty / all test cases are marked "
                  "<code>Automated</code>), so no manual <code>Test Results</code> are expected. Testing "
                  "traceability is established via Genie automation tags (<code>@tt_ST</code> / <code>@tt_IT</code>) "
                  "— see the Traceability section for per-story System/Integration Testing coverage.")
        elif no_manual_tc:
            r.add(CRITICAL, "No Manual Test Execution Records Found",
                  "The <code>Test Results</code> section is empty, and no manual test cases are defined in the "
                  "ADO Test Plan. However, no Genie automation traceability (<code>genie_tag_split</code> "
                  "<code>@tt_ST</code>/<code>@tt_IT</code>, or <code>genie_story_type_breakdown</code>) could be "
                  "confirmed either — neither manual test execution nor Genie automation traceability could be "
                  "confirmed for this release.")
        else:
            r.add(CRITICAL, "No Manual Test Execution Records Found",
                  "The <code>Test Results</code> section is empty. Manual testing outcomes, step-level pass/fail "
                  "status, and evidence attachments cannot be verified.")
    else:
        tc_issues = []
        for tc in test_results:
            outcome = tc.get("Outcome", "")
            tc_id   = tc.get("TestCase Id", "")
            name    = tc.get("Test Name", "")
            steps   = tc.get("Step-Iteration-Identifier-Outcome", [])
            attachments = tc.get("Step-Attachments", [])
            att_name    = tc.get("AttachmentName", "NOT AVAILABLE")
            att_source  = tc.get("AttachmentSource", "")
            has_evidence = bool(attachments) or att_name != "NOT AVAILABLE"

            issues = []
            if outcome.lower() != "passed":
                issues.append(f"outcome = {e(outcome)}")
            failed_steps = [s for s in steps if "Failed" in s or "Blocked" in s]
            if failed_steps:
                issues.append(f"{len(failed_steps)} step(s) not Passed")
            if not has_evidence:
                issues.append("no evidence attached")
            if issues:
                tc_issues.append(f"TC {wi_link(tc_id)} &lsquo;{e(name)}&rsquo;: " + "; ".join(issues))

        if tc_issues:
            r.add(CRITICAL, f"Manual Test Execution Issues ({len(tc_issues)} test case(s))",
                  "The following test cases have issues that must be resolved: <ul>" +
                  "".join(f"<li>{issue}</li>" for issue in tc_issues) + "</ul>")
        elif test_results:
            r.add(LOOKS, f"All Manual Test Cases Passed with Evidence ({len(test_results)} TCs)",
                  f"All {len(test_results)} test case(s) are Passed with evidence attached at step or result level.")

    # ── Stories ───────────────────────────────────────────────────────────
    stories = data.get("story_features", [])
    if is_compact:
        stories_meta = data.get("stories_summary", {})
        all_stories  = stories_meta.get("all_comments_review", [])
    else:
        all_stories = stories

    # Similarity
    high_sim = []
    for s in all_stories:
        ratio = s.get("Desc-AC-Similary-Ratio", s.get("similarity_ratio", 0)) or 0
        if float(ratio) >= 85:
            high_sim.append((s.get("WI Id", s.get("id", "")), float(ratio)))
    if high_sim:
        r.add(MODERATE, f"High Desc-AC Similarity ({len(high_sim)} stories)",
              "The following stories have Desc-AC similarity &ge;85% (copy-paste risk): " +
              ", ".join(f"Story {wi_link(sid)} ({ratio:.1f}%)" for sid, ratio in high_sim))
    else:
        r.add(LOOKS, "No High Desc-AC Similarity",
              "No stories have a Desc-AC similarity ratio at or above the 85% copy-paste threshold.")

    # Open comments
    CONCERN_PHRASES = [
        "not working", "pending", "waiting", "failing", "to be confirmed",
        "will be done when", "isn't working", "mq issues", "not yet",
        "still", "raised #", "may not be required", "to handle",
    ]
    open_comment_stories = []
    for s in all_stories:
        comment = (s.get("Story Last Comment") or s.get("last_comment") or "").strip()
        if comment.upper() in ("", "NA", "N/A"):
            continue
        comment_lower = comment.lower()
        if any(phrase in comment_lower for phrase in CONCERN_PHRASES):
            open_comment_stories.append((
                s.get("WI Id", s.get("id", "")),
                s.get("WI State", s.get("state", "")),
                comment[:200],
            ))
    if open_comment_stories:
        r.add(MODERATE, f"Stories with Open/Unresolved Last Comments ({len(open_comment_stories)})",
              "The following stories have last comments suggesting pending/unresolved items: " +
              ", ".join(f"Story {wi_link(sid)} (<em>{e(cmt[:80])}</em>)" for sid, _, cmt in open_comment_stories))
    else:
        r.add(LOOKS, "No Open/Unresolved Story Comments",
              "No stories have last comments indicating pending or unresolved items.")

    # Reprioritization
    ACCEPTANCE_KEYWORDS = [
        "accepted", "reviewed and approved", "acknowledged", "po sign-off",
        "po confirms", "scope change accepted", "re-prioritized", "agreed",
        "approve the changes",
    ]
    reprio_stories = []
    for s in all_stories:
        check = s.get("PO Reprioritization Check", "NA")
        if check == "MODIFIED_AFTER":
            po_comment = s.get("PO Reprioritization Comment", {}) or {}
            comment_text = (po_comment.get("text") or "").lower()
            has_acceptance = any(kw in comment_text for kw in ACCEPTANCE_KEYWORDS)
            reprio_stories.append((s, has_acceptance, po_comment))

    for s, has_accept, po_comment in reprio_stories:
        sid = s.get("WI Id", "")
        stitle = s.get("WI Title", "")
        findings_list = s.get("PO Reprioritization Findings", [])
        changed_by = findings_list[0].get("Changed By", "Unknown") if findings_list else "Unknown"
        changed_date = fmt_date(findings_list[-1].get("Changed Date", "")) if findings_list else ""
        if has_accept:
            by = po_comment.get("by", "Unknown")
            date_ = fmt_date(po_comment.get("date", ""))
            ctext = po_comment.get("text", "")[:120]
            r.add(MINOR, f"PO Reprioritization: Story {wi_link(sid)} (Acceptance Comment Found &mdash; Downgraded)",
                  f"Story &lsquo;{e(stitle)}&rsquo; had Description/AC modified after prioritization by "
                  f"{e(changed_by)} (latest: {e(changed_date)}). A subsequent acceptance comment was recorded by "
                  f"{e(by)} on {e(date_)}: &ldquo;{e(ctext)}&rdquo;. Release manager should verify this is a genuine PO sign-off.")
        else:
            r.add(MODERATE, f"PO Reprioritization: Story {wi_link(sid)} (No Acceptance Comment)",
                  f"Story &lsquo;{e(stitle)}&rsquo; had Description/AC modified after PO prioritization by "
                  f"{e(changed_by)} (latest change: {e(changed_date)}), with no subsequent PO acceptance comment. "
                  "Recommend the release manager confirm the PO re-reviewed this story.")

    # Missing App ID / Story Type — MINOR/Info
    missing_app_id = [s for s in all_stories if not s.get("WI App Id") and not s.get("app_id")]
    missing_story_type = [s for s in all_stories if not s.get("Automated") and not s.get("story_type")]
    if missing_app_id:
        r.add(MINOR, f"Missing ApplicationID ({len(missing_app_id)} stories)",
              "The following stories are missing <code>Custom.ApplicationID</code>: " +
              ", ".join(wi_link(s.get("WI Id", s.get("id", ""))) for s in missing_app_id))
    if missing_story_type:
        r.add(MINOR, f"Missing StoryType ({len(missing_story_type)} stories)",
              "The following stories are missing <code>Custom.StoryType</code>: " +
              ", ".join(wi_link(s.get("WI Id", s.get("id", ""))) for s in missing_story_type))
    if not missing_app_id and not missing_story_type and all_stories:
        r.add(LOOKS, "Story Field Completeness: All Stories Have ApplicationID and StoryType",
              f"All {len(all_stories)} stories have both <code>Custom.ApplicationID</code> and "
              "<code>Custom.StoryType</code> populated.")

    # ── Traceability ──────────────────────────────────────────────────────
    traceability = data.get("traceability", [])
    genie_breakdown = data.get("genie_story_type_breakdown", [])
    genie_st_ids = {str(g["Story WI Id"]) for g in genie_breakdown if g.get("Genie ST Scenarios", 0) > 0}
    genie_it_ids = {str(g["Story WI Id"]) for g in genie_breakdown if g.get("Genie IT Scenarios", 0) > 0}

    story_ids = {str(s.get("WI Id", s.get("id", ""))) for s in all_stories}
    tc_details = data.get("test_case_details", [])
    tc_type_map = {str(t["TC Id"]): t.get("TC TestType", "") for t in tc_details}

    # Build coverage map: story_id -> set of coverage types
    coverage = {sid: set() for sid in story_ids}
    for tr_ in traceability:
        sid = str(tr_.get("Story WI Id", ""))
        tc_id = str(tr_.get("TC Id", ""))
        tc_type = tc_type_map.get(tc_id, tr_.get("TC Type", "")).lower()
        if sid in coverage:
            if "system" in tc_type:
                coverage[sid].add("ado_st")
            elif "integration" in tc_type:
                coverage[sid].add("ado_it")
            elif "acceptance" in tc_type:
                coverage[sid].add("ado_at")
            else:
                coverage[sid].add("ado_other")
    for sid in story_ids:
        if sid in genie_st_ids:
            coverage[sid].add("genie_st")
        if sid in genie_it_ids:
            coverage[sid].add("genie_it")

    uncovered = [sid for sid in story_ids if not coverage.get(sid)]
    if uncovered:
        r.add(MODERATE, f"Traceability Gaps: {len(uncovered)} Stories with No Coverage",
              "The following stories have no linked ADO test case (System/Integration/Acceptance) AND "
              "no Genie automation evidence: " + ", ".join(wi_link(s) for s in sorted(uncovered)))
    elif story_ids:
        r.add(LOOKS, f"Full Story Traceability: All {len(story_ids)} Stories Covered",
              "Every story in scope has at least one coverage source (ADO manual System/Integration/"
              "Acceptance Testing or Genie automation).")

    # ── Negative test coverage — keyword scan (fully deterministic) ───────
    NEG_KEYWORDS = [
        "negative", "invalid", "error", "reject", "rejection",
        "fail", "failure", "not found", "unauthori", "forbidden",
        "exceed", "cannot", "unable", "should not", "must not",
        "no result", "empty result", "no data", "boundary", "out of range",
        "wrong", "missing field", "mandatory field", "bad request", "exception",
    ]
    genie_failures = data.get("genie_failures", [])
    neg_genie = [f["name"] for f in genie_failures if any(k in f.get("name","").lower() for k in NEG_KEYWORDS)]
    neg_tc    = [t["TC Title"] for t in tc_details if any(k in t.get("TC Title","").lower() for k in NEG_KEYWORDS)]
    neg_stories = [
        (s.get("WI Id",""), s.get("Story Last Comment",""))
        for s in all_stories
        if any(k in (s.get("Story Last Comment") or "").lower() for k in NEG_KEYWORDS)
    ]
    has_neg = bool(neg_genie or neg_tc or neg_stories)
    if has_neg:
        sources = []
        if neg_genie: sources.append(f"Genie scenarios ({len(neg_genie)} found)")
        if neg_tc:    sources.append(f"TC titles ({len(neg_tc)} found)")
        if neg_stories: sources.append(f"story comments ({len(neg_stories)} found)")
        r.add(MINOR, "Negative Test Coverage Identified",
              "Negative testing evidence found in: " + ", ".join(sources) + ".")
    else:
        r.add(MINOR, "No Negative Test Coverage Identified",
              "No negative test indicators found in Genie scenario names, TC titles, or story comments. "
              "Recommend the QA team confirms negative scenarios are covered in manual or Genie regression suites.")

    # ── Desc/AC quality — heuristic + flag for LLM ───────────────────────
    PLACEHOLDER_AC = ["tbd", "n/a", "na", "see attached", "not applicable", "to be defined"]
    desc_ac_issues = []
    for s in all_stories[:30]:  # cap at 30 to avoid huge tables
        sid   = s.get("WI Id", s.get("id", ""))
        desc  = s.get("Description Text", s.get("desc_text", "")) or ""
        ac    = s.get("Acceptance Criteria Text", s.get("ac_text", "")) or ""
        desc_stripped = re.sub(r"<[^>]+>", "", desc).strip()
        ac_stripped   = re.sub(r"<[^>]+>", "", ac).strip()
        issues_here = []
        if desc_stripped and len(desc_stripped) < 50:
            issues_here.append(f"Description very short ({len(desc_stripped)} chars)")
        if ac_stripped and len(ac_stripped) < 50:
            issues_here.append(f"AC very short ({len(ac_stripped)} chars)")
        if ac_stripped.lower() in PLACEHOLDER_AC:
            issues_here.append("AC appears to be placeholder text")
        if issues_here:
            desc_ac_issues.append((sid, "; ".join(issues_here)))

    if desc_ac_issues:
        r.add(MINOR, f"Desc/AC Quality: {len(desc_ac_issues)} Stories May Have Terse/Placeholder Content "
              "[Requires Review]",
              f'<div class="review-note">&#9888;&#65039; <strong>[Requires Review]</strong> The following '
              f"{len(desc_ac_issues)} stories were flagged by automated heuristics as potentially having "
              "terse or placeholder Description/AC. A human reviewer should confirm: " +
              ", ".join(f"Story {wi_link(sid)} ({e(note)})" for sid, note in desc_ac_issues) +
              ". This is informational only &mdash; never a CRITICAL/MODERATE gate.</div>")

    # ── Cross-document consistency ────────────────────────────────────────
    docs_to_check = []
    if pt_plan_exists and pt_plan_appr.get("Page Accessible") == "YES":
        docs_to_check.append(("PT Plan", pt_plan_appr.get("Page Title", "")))
    if pt_report_exists and pt_report_appr.get("Page Accessible") == "YES":
        docs_to_check.append(("PT Report", pt_report_appr.get("Page Title", "")))
    if ptia_exists == "YES" and ptia_title:
        docs_to_check.append(("PTIA", ptia_title))
    if pit_accessible == "YES" and pit_page_title:
        docs_to_check.append(("PIT", pit_page_title))

    for doc_label, page_title in docs_to_check:
        if not page_title:
            continue
        ver_in_title = re.search(r'\d+\.\d+(?:\.\d+)?', page_title)
        if canon_ver and ver_in_title:
            if ver_in_title.group(0) != canon_ver:
                r.add(MODERATE, f"Cross-Document Version Mismatch: {doc_label}",
                      f"{e(doc_label)} page title &lsquo;{e(page_title)}&rsquo; contains version "
                      f"<code>{e(ver_in_title.group(0))}</code> but expected "
                      f"<code>{e(canon_ver)}</code>.")
        elif canon_ver and not ver_in_title:
            r.add(MINOR, f"Cross-Document: No Version Number in {doc_label} Title",
                  f"{e(doc_label)} page title &lsquo;{e(page_title)}&rsquo; does not contain a recognisable "
                  f"version number &mdash; cannot confirm it relates to version <code>{e(canon_ver)}</code>.")

    return r


# ---------------------------------------------------------------------------
# Table builders
# ---------------------------------------------------------------------------
def build_tables(data: dict) -> str:
    """Return the full HTML for all summary tables."""
    is_compact = "test_results_summary" in data and "stories_summary" in data
    stream = data.get("release_stream", "")

    parts = []
    _s = parts.append  # shorthand

    # ── Associated Builds ─────────────────────────────────────────────────
    builds = data.get("blade_release_builds", {})
    pv = data.get("pipeline_versions", {})
    _s('<div class="section-title">Associated Builds</div>\n')
    rows = ""
    for pname, bid in builds.items():
        ver = pv.get(pname, "") or na_span("Not resolved (inferred from release title)")
        rows += tr(td(e(pname)), td(e(str(bid))), td(ver))
    _s(table_html(["Pipeline", "Build ID", "Version"], rows, "No builds recorded (rwi-only or empty)"))

    # ── Application Approvals ─────────────────────────────────────────────
    af = (data.get("application_features") or [{}])[0]
    if af:
        approval_fields = {
            "Application Architecture": "Custom.ApplicationArchitectureApprovalExpiryDate",
            "ASRM":                     "Custom.ASRMApprovalExpiryDate",
            "NFR":                      "Custom.NFRApprovalExpiryDate",
            "Test Environment Management": "Custom.TEMApprovalExpiryDate",
            "Test Strategy":            "Custom.TestStrategyApprovalExpiryDate",
        }
        _s('<div class="section-title">Application Approvals</div>\n')
        rows = ""
        for label, field in approval_fields.items():
            val = af.get(field, "")
            if not val:
                continue
            d = days_from_today(val)
            expiry_str = fmt_date(val)
            if d is None:
                status = na_span()
            elif d < 0:
                status = warn_span(f"CRITICAL — expired {abs(d)}d ago")
            elif d <= 90:
                status = warn_span(f"MINOR/Info — expires in {d}d")
            else:
                status = ok_span(f"Valid ({d}d remaining)")
            rows += tr(td(e(label)), td(e(expiry_str)), td(status))
        _s(table_html(["Approval", "Expiry Date", "Status"], rows))

    # ── Confluence post-approval ──────────────────────────────────────────
    conf_checks = af.get("confluence_post_approval_checks", []) if af else []
    _s('<div class="section-title">Application WI &mdash; Confluence Post-Approval Checks</div>\n')
    _s('<div class="rule-box">&#8505;&#65039; Only populated when <code>application_confluence_post_approval_check_enabled: true</code> in <code>stream_config.yaml</code>.</div>\n')
    rows = ""
    for cc in conf_checks:
        sv = cc.get("status", "")
        label_ = e(cc.get("label", ""))
        title_ = e(cc.get("page_title", ""))
        lmod   = e(fmt_date(cc.get("last_modified", "")))
        lappr  = e(fmt_date(cc.get("last_approval", "")))
        status = warn_span(sv) if sv != "OK" else ok_span("OK")
        rows += tr(td(label_), td(title_), td(lmod), td(lappr), td(status))
    _s(table_html(["Document", "Page Title", "Last Modified", "Last Approval", "Status"],
                  rows, "N/A — check not enabled for this stream"))

    # ── Unit tests ────────────────────────────────────────────────────────
    _s('<div class="section-title">Unit Test Coverage</div>\n')
    rows = ""
    for ut in data.get("unit_tests", []):
        pname = e(ut.get("Pipeline Name", ""))
        bid   = e(str(ut.get("Build ID", "N/A")))
        total = ut.get("Total Tests", 0)
        passed  = ut.get("Passed", 0)
        failed  = ut.get("Failed", 0)
        not_exec= ut.get("Not Executed", 0)
        others  = ut.get("increaseInOtherTests", 0)
        stat = warn_span("CRITICAL — issues") if (failed or not_exec or others) else ok_span("All Passed")
        rows += tr(
            td(pname), td(bid), td(str(total)),
            td(ok_span(str(passed)) if not failed else warn_span(str(passed))),
            td(warn_span(str(failed)) if failed else ok_span("0")),
            td(warn_span(str(not_exec)) if not_exec else ok_span("0")),
            td(warn_span(str(others)) if others else ok_span("0")),
            td(stat),
        )
    _s(table_html(["Pipeline", "Build ID", "Total", "Passed", "Failed", "Not Executed", "Others", "Status"],
                  rows, "No unit test data"))

    # ── Sonar ─────────────────────────────────────────────────────────────
    _s('<div class="section-title">Sonar Coverage</div>\n')
    sonar_skipped = data.get("sonar_skipped", False)
    sonar_skip_reason = data.get("sonar_skip_reason", "")
    if sonar_skipped:
        _s(f'<div class="info-note">Sonar coverage intentionally skipped: <em>{e(sonar_skip_reason)}</em></div>\n')
    else:
        # Build lookup: pipeline name -> gate status entry
        _gate_status_map = {
            gs.get("Pipeline", ""): gs
            for gs in data.get("sonar_quality_gate_statuses", [])
        }
        def _gate_status_cell(pipeline_name):
            gs = _gate_status_map.get(pipeline_name)
            if gs is None:
                return na_span("N/A")
            s = (gs.get("status") or "").upper()
            failed = gs.get("conditions", [])
            detail = "; ".join(
                f"{c.get('metricKey','?')}: {c.get('actualValue','?')} (threshold {c.get('errorThreshold','?')})"
                for c in failed
            )
            if s == "OK":
                return ok_span("&#9989; PASSED")
            elif s == "ERROR":
                msg = "&#10060; FAILED" + (f" &mdash; {e(detail)}" if detail else "")
                return warn_span(msg)
            elif s == "WARN":
                msg = "&#9888; WARNING" + (f" &mdash; {e(detail)}" if detail else "")
                return warn_span(msg)
            elif s == "NONE":
                return na_span("&#9898; NOT COMPUTED")
            return na_span(s or "N/A")

        _new_code_periods_by_pipeline = {
            ncp.get("Pipeline", ""): ncp for ncp in data.get("sonar_new_code_periods", [])
        }
        def _new_code_baseline_cell(pname_raw):
            if "fmdc-releases" in pname_raw.lower():
                return na_span("N/A (exempt)")
            ncp = _new_code_periods_by_pipeline.get(pname_raw)
            if not ncp:
                return na_span("N/A")
            ptype = (ncp.get("type") or "").upper()
            if ptype == "REFERENCE_BRANCH":
                return e(f"Reference branch: {ncp.get('value', '')}")
            elif ptype:
                return e(ptype.replace("_", " ").title())
            return na_span("N/A")

        rows = ""
        for sc in data.get("sonar_coverage", []):
            pname_raw = sc.get("Pipeline", sc.get("pipeline", ""))
            pname = e(pname_raw)
            ov  = sc.get("coverage", "")
            lv  = sc.get("line_coverage", "")
            bv  = sc.get("branch_coverage", "")
            nv  = sc.get("new_coverage", "")
            nlv = sc.get("new_line_coverage", "")
            nbv = sc.get("new_branch_coverage", "")
            def _fmt(v): return na_span() if v is None or v == "" else str(v) + "%"
            def _cov_cell(v):
                if v is None or v == "": return na_span()
                try:
                    fv = float(v)
                    return (ok_span(f"{fv:.1f}%") if fv >= 40 else warn_span(f"{fv:.1f}%"))
                except Exception:
                    return e(str(v))
            rows += tr(td(pname), td(_cov_cell(ov)), td(_fmt(lv)), td(_fmt(bv)),
                       td(_cov_cell(nv)), td(_fmt(nlv)), td(_fmt(nbv)),
                       td(_new_code_baseline_cell(pname_raw)),
                       td(_gate_status_cell(pname_raw)), td(""))
        _s(table_html(["Pipeline", "Overall %", "Line %", "Branch %", "New Code %", "New Line %", "New Branch %",
                       "New Code Baseline", "Gate Status", "Status"],
                      rows, "No Sonar data"))

    # Quality gates
    _s('<div class="section-title">Sonar Quality Gate Assignment</div>\n')
    if sonar_skipped:
        _s('<div class="info-note">N/A &mdash; Sonar skipped for this stream.</div>\n')
    else:
        rows = ""
        required = "ESDLC-Sonarway-managed"
        for qg in data.get("sonar_quality_gates", []):
            pname_raw = qg.get("Pipeline", "")
            pname = e(pname_raw)
            gate  = e(qg.get("quality_gate_name", ""))
            match_cell = ok_span("&#9989; Yes") if gate.lower() == required.lower() else warn_span("&#10060; No &mdash; CRITICAL")
            rows += tr(td(pname), td(gate), td(match_cell), td(_gate_status_cell(pname_raw)))
        _s(table_html(["Pipeline", "Quality Gate", f"Matches {required}?", "Gate Status"], rows, "No quality gate data"))

    # Sonar exclusions
    _s('<div class="section-title">Sonar Exclusions</div>\n')
    if sonar_skipped:
        _s('<div class="info-note">N/A &mdash; Sonar skipped for this stream.</div>\n')
    else:
        rows = ""
        for se in data.get("sonar_exclusions", []):
            pname = e(se.get("Pipeline", ""))
            def _join(lst): return e(", ".join(lst)) if lst else na_span("None")
            rows += tr(td(pname), td(_join(se.get("sonar.exclusions", []))),
                       td(_join(se.get("sonar.coverage.exclusions", []))),
                       td(_join(se.get("sonar.test.exclusions", []))),
                       td(_join(se.get("sonar.cpd.exclusions", []))))
        _s(table_html(["Pipeline", "sonar.exclusions", "sonar.coverage.exclusions",
                        "sonar.test.exclusions", "sonar.cpd.exclusions"],
                      rows, "No exclusions data"))

    # ── Genie ─────────────────────────────────────────────────────────────
    _s('<div class="section-title">Genie Regression</div>\n')
    gc = (data.get("genie_count") or [{}])[0]
    gp = gc.get("passed", 0)
    gf = gc.get("failed", 0)
    gt = gp + gf
    rate_str = f"{gf/gt*100:.2f}%" if gt else "N/A"
    stat_cell = ok_span("&#9989; All Passed") if gf == 0 else warn_span(f"&#9888; {rate_str} failure rate")
    rows = tr(td(str(gt)), td(str(gp)), td(warn_span(str(gf)) if gf else ok_span("0")), td(rate_str), td(stat_cell))
    _s(table_html(["Total", "Passed", "Failed", "Failure Rate", "Status"], rows))

    _s('<div class="section-title">Genie Failures</div>\n')
    rows = ""
    for gf_ in data.get("genie_failures", []):
        rows += tr(td(e(gf_.get("name", ""))), td(warn_span(e(gf_.get("status", "")))))
    _s(table_html(["Scenario", "Status"], rows, "No failures"))

    # ── Regression retest ─────────────────────────────────────────────────
    _s('<div class="section-title">Regression Failure Re-Test</div>\n')
    genie_failed = gc.get("failed", 0)
    if genie_failed > 0:
        RETEST_STRICT = [r"re.?test.+automation.+regression", r"regression.+failure.+re.?test",
                         r"manual.+retest.+regression", r"automation.+regression.+failure"]
        retest_tc = None
        for tc_ in data.get("test_result_features", []):
            if any(re.search(p, tc_.get("Test Name",""), re.IGNORECASE) for p in RETEST_STRICT):
                retest_tc = tc_
                break
        if retest_tc:
            outcome = retest_tc.get("Outcome","")
            has_ev  = bool(retest_tc.get("Step-Attachments")) or retest_tc.get("AttachmentName","NOT AVAILABLE") != "NOT AVAILABLE"
            rows = tr(
                td(str(genie_failed)),
                td(ok_span(f"Yes &mdash; TC {e(retest_tc.get('TestCase Id',''))}")),
                td(e(retest_tc.get("Test Name",""))),
                td(ok_span(outcome) if outcome.lower()=="passed" else warn_span(outcome)),
                td(ok_span("Yes") if has_ev else warn_span("No &mdash; CRITICAL")),
            )
        else:
            rows = tr(td(str(genie_failed)), td(warn_span("Not Found &mdash; CRITICAL")),
                      td(na_span()), td(na_span()), td(na_span()))
    else:
        rows = tr(td("0"), td(ok_span("N/A &mdash; no failures")), td(na_span()), td(na_span()), td(na_span()))
    _s(table_html(["Genie Failures", "Re-Test TC Found", "TC Title", "Outcome", "Evidence Present"], rows))

    # ── Manual tests ──────────────────────────────────────────────────────
    _s('<div class="section-title">Manual Test Execution Summary</div>\n')
    rows = ""
    for tc_ in data.get("test_result_features", []):
        outcome = tc_.get("Outcome","")
        steps   = tc_.get("Step-Iteration-Identifier-Outcome",[])
        atts    = tc_.get("Step-Attachments",[])
        att_nm  = tc_.get("AttachmentName","NOT AVAILABLE")
        att_src = tc_.get("AttachmentSource","")
        has_ev  = bool(atts) or att_nm != "NOT AVAILABLE"
        steps_passed = sum(1 for s in steps if "Passed" in s)
        ev_src = att_src if att_src else ("Step" if atts else ("Result/Run" if has_ev else "None"))
        rows += tr(
            td(e(tc_.get("TestCase Id",""))),
            td(e(tc_.get("Test Name",""))),
            td(ok_span(outcome) if outcome.lower()=="passed" else warn_span(outcome)),
            td(str(steps_passed)), td(str(len(steps))),
            td(ok_span("Yes") if has_ev else warn_span("No &mdash; CRITICAL")),
            td(e(ev_src)),
            td(na_span("None") if outcome.lower()=="passed" and has_ev else warn_span("See findings")),
        )
    _s(table_html(["TC ID", "Title", "Outcome", "Steps Passed", "Steps Total",
                   "Evidence Present", "Evidence Source", "Issues"], rows, "No test results"))

    # ── Acceptance Testing PO Evidence ────────────────────────────────────
    _s('<div class="section-title">Acceptance Testing &mdash; PO Approval Email Evidence (Informational)</div>\n')
    rows = ""
    for poe in data.get("po_approval_evidence", []):
        parsed = poe.get("Parsed", False)
        rows += tr(
            td(e(poe.get("TC Id",""))),
            td(e(poe.get("Attachment Name",""))),
            td(ok_span("Yes") if parsed else warn_span("No &mdash; .msg not parsed")),
            td(e(poe.get("Sender","")) or na_span()),
            td(e(poe.get("Subject","")) or na_span()),
            td(e(", ".join(poe.get("Approval Keywords Found",[]))) or na_span("None")),
            td(e(", ".join(poe.get("Confluence Links",[]))) or na_span("None")),
        )
    _s(table_html(["TC Id","Attachment","Parsed","Sender","Subject","Approval Keywords","Confluence Link(s)"],
                  rows, "No PO approval email evidence found"))

    # ── Stories ───────────────────────────────────────────────────────────
    all_stories = data.get("story_features", [])
    if "stories_summary" in data:
        all_stories = data["stories_summary"].get("all_comments_review", [])

    _s('<div class="section-title">Stories in Scope</div>\n')
    rows = ""
    for s in all_stories:
        sid   = wi_link(s.get("WI Id", s.get("id","")))
        stitle= e(s.get("WI Title", s.get("title","")))
        state = e(s.get("WI State", s.get("state","")))
        desc  = ok_span("OK") if s.get("Desc Present","") == "OK" else warn_span(s.get("Desc Present","Missing"))
        ac    = ok_span("OK") if s.get("AC Present","") == "OK" else warn_span(s.get("AC Present","Missing"))
        ratio = s.get("Desc-AC-Similary-Ratio", s.get("similarity_ratio", 0)) or 0
        ratio_cell = warn_span(f"{float(ratio):.1f}%") if float(ratio) >= 85 else f"{float(ratio):.1f}%"
        app_id = e(s.get("WI App Id", s.get("app_id",""))) or na_span()
        stype  = e(s.get("Automated", s.get("story_type",""))) or na_span()
        rows += tr(td(sid), td(stitle), td(state), td(desc), td(ac), td(ratio_cell), td(app_id), td(stype))
    _s(table_html(["Story ID","Title","State","Desc","AC","Similarity %","App ID","Story Type"],
                  rows, "No stories"))

    # Story field completeness
    _s('<div class="section-title">Story Field Completeness</div>\n')
    total_s = len(all_stories)
    miss_app  = sum(1 for s in all_stories if not s.get("WI App Id") and not s.get("app_id"))
    miss_type = sum(1 for s in all_stories if not s.get("Automated") and not s.get("story_type"))
    rows = (
        tr(td("Stories with ApplicationID populated"), td(ok_span(f"{total_s - miss_app} / {total_s}"))) +
        tr(td("Stories with StoryType populated"),     td(ok_span(f"{total_s - miss_type} / {total_s}"))) +
        tr(td("Stories missing ApplicationID"),        td(warn_span(str(miss_app)) if miss_app else ok_span("0"))) +
        tr(td("Stories missing StoryType"),            td(warn_span(str(miss_type)) if miss_type else ok_span("0")))
    )
    _s(table_html(["Metric","Count"], rows))

    # Open comments
    CONCERN_PHRASES = ["not working","pending","waiting","failing","to be confirmed","isn't working",
                       "mq issues","not yet","still","raised #","may not be required","to handle"]
    _s('<div class="section-title">Stories with Open / Unresolved Last Comments</div>\n')
    rows = ""
    for s in all_stories:
        comment = (s.get("Story Last Comment") or s.get("last_comment") or "").strip()
        if comment.upper() in ("","NA","N/A"): continue
        if any(p in comment.lower() for p in CONCERN_PHRASES):
            rows += tr(td(wi_link(s.get("WI Id",""))), td(e(s.get("WI State",""))),
                       td(e(comment[:200])), td(warn_span("Review needed")))
    _s(table_html(["Story ID","State","Last Comment (snippet)","Risk Indicator"],
                  rows, "None identified"))

    # High similarity
    _s('<div class="section-title">High Desc-AC Similarity (&gt;85%)</div>\n')
    rows = ""
    for s in all_stories:
        ratio = float(s.get("Desc-AC-Similary-Ratio", s.get("similarity_ratio", 0)) or 0)
        if ratio >= 85:
            rows += tr(td(wi_link(s.get("WI Id",""))), td(e(s.get("WI State",""))),
                       td(warn_span(f"{ratio:.1f}%")), td(warn_span("Copy-paste risk")))
    _s(table_html(["Story ID","State","Similarity %","Risk"], rows, "None identified"))

    # Traceability
    _s('<div class="section-title">Traceability Coverage</div>\n')
    traceability = data.get("traceability", [])
    genie_breakdown = data.get("genie_story_type_breakdown", [])
    genie_st_ids = {str(g["Story WI Id"]) for g in genie_breakdown if g.get("Genie ST Scenarios",0) > 0}
    genie_it_ids = {str(g["Story WI Id"]) for g in genie_breakdown if g.get("Genie IT Scenarios",0) > 0}
    tc_details_map = {str(t["TC Id"]): t.get("TC TestType","") for t in data.get("test_case_details",[])}
    story_ids_all = {str(s.get("WI Id", s.get("id",""))) for s in all_stories}

    cov = {sid: set() for sid in story_ids_all}
    for tr_ in traceability:
        sid  = str(tr_.get("Story WI Id",""))
        tcid = str(tr_.get("TC Id",""))
        ttype = tc_details_map.get(tcid, "").lower()
        if sid in cov:
            if "system" in ttype: cov[sid].add("ado_st")
            elif "integration" in ttype: cov[sid].add("ado_it")
            elif "acceptance" in ttype: cov[sid].add("ado_at")
    for sid in story_ids_all:
        if sid in genie_st_ids: cov[sid].add("genie_st")
        if sid in genie_it_ids: cov[sid].add("genie_it")

    def _cov_row(label, key, story_set):
        has = sum(1 for sid in story_ids_all if key in cov.get(sid,set()))
        miss = len(story_ids_all) - has
        return tr(td(label), td(str(has)), td(str(miss)), td("Informational"))

    cov_rows = (
        _cov_row("ADO Manual System Testing", "ado_st", story_ids_all) +
        _cov_row("ADO Manual Integration Testing", "ado_it", story_ids_all) +
        _cov_row("ADO Manual Acceptance Testing", "ado_at", story_ids_all) +
        _cov_row("Genie / Automation System Testing", "genie_st", story_ids_all) +
        _cov_row("Genie / Automation Integration Testing", "genie_it", story_ids_all)
    )
    covered_any = sum(1 for sid in story_ids_all if cov.get(sid))
    uncovered   = len(story_ids_all) - covered_any
    overall_status = ok_span("&#9989; All stories covered") if uncovered == 0 else warn_span(f"&#9888; {uncovered} gap(s)")
    cov_rows += tr(
        td("<strong>Any of 5 sources (overall coverage)</strong>"),
        td(f"<strong>{covered_any}</strong>"),
        td(f"<strong>{uncovered}</strong>"),
        td(overall_status),
    )
    _s(table_html(["Testing Type","Stories with &ge;1 TC Linked","Stories Missing","Status"], cov_rows))

    # Gaps
    _s('<div class="section-title">Traceability Coverage Gaps</div>\n')
    rows = ""
    for sid in sorted(story_ids_all):
        if not cov.get(sid):
            rows += tr(
                td(wi_link(sid)),
                td(na_span("None")), td(na_span("None")), td(na_span("None")),
                td(na_span("None")), td(na_span("None")),
            )
    _s(table_html(["Story ID","ADO System","ADO Integration","ADO Acceptance","Genie ST","Genie IT"],
                  rows, "All stories have at least one coverage source"))

    # Resolved via Genie
    _s('<div class="section-title">Traceability Gaps Resolved via Genie Automation</div>\n')
    rows = ""
    for g in genie_breakdown:
        sid  = str(g.get("Story WI Id",""))
        gst  = g.get("Genie ST Scenarios",0)
        git_ = g.get("Genie IT Scenarios",0)
        if not (traceability and any(str(t.get("Story WI Id","")) == sid for t in traceability)):
            if gst > 0 or git_ > 0:
                rows += tr(td(wi_link(sid)), td(ok_span(str(gst))), td(ok_span(str(git_))))
    _s(table_html(["Story ID","Genie ST Scenarios","Genie IT Scenarios"],
                  rows, "None &mdash; no gaps resolved via Genie"))

    # Automation coverage
    _s('<div class="section-title">Automation Coverage</div>\n')
    ado_auto = sum(1 for sid in story_ids_all if "ado_auto" in cov.get(sid,set()))
    genie_auto = sum(1 for sid in story_ids_all if "genie_st" in cov.get(sid,set()) or "genie_it" in cov.get(sid,set()))
    rows = (
        tr(td("Stories with automated coverage"), td(str(ado_auto)), td(str(genie_auto))) +
        tr(td("Stories with 0 automated coverage"), td(str(len(story_ids_all)-ado_auto)), td(str(len(story_ids_all)-genie_auto))) +
        tr(td("Total stories in traceability"), td(str(len(story_ids_all))), td(str(len(story_ids_all))))
    )
    _s(table_html(["Metric","Count (ADO)","Count (Genie / Automation Tool)"], rows))

    # PO Reprioritization
    _s('<div class="section-title">Stories Modified After PO Prioritization</div>\n')
    ACCEPTANCE_KEYWORDS = ["accepted","reviewed and approved","acknowledged","po sign-off",
                           "po confirms","scope change accepted","re-prioritized","agreed","approve the changes"]
    rows = ""
    for s in all_stories:
        if s.get("PO Reprioritization Check","NA") == "MODIFIED_AFTER":
            sid    = wi_link(s.get("WI Id",""))
            stitle = e(s.get("WI Title","")[:60])
            finds  = s.get("PO Reprioritization Findings",[])
            fields = ", ".join(f"{e(f.get('Field',''))} ({e(fmt_date(f.get('Changed Date','')))})" for f in finds)
            changed_by = e(finds[0].get("Changed By","")) if finds else ""
            poc = s.get("PO Reprioritization Comment",{}) or {}
            poc_text = (poc.get("text","") or "")[:100]
            poc_by   = poc.get("by","")
            has_acc  = any(kw in poc_text.lower() for kw in ACCEPTANCE_KEYWORDS)
            status_cell = ok_span("MINOR/Info &mdash; Downgraded") if has_acc else warn_span("MODERATE &mdash; No acceptance comment")
            rows += tr(td(sid), td(stitle), td(fields), td(changed_by),
                       td(e(f"{poc_by}: {poc_text}") if poc_text else na_span("None")),
                       td(status_cell))
    _s(table_html(["Story ID","Title","Fields Changed","Changed By","PO Comment","Status"],
                  rows, "No stories modified after PO prioritization"))

    # Bugs
    _s('<div class="section-title">Bugs in Scope</div>\n')
    rows = ""
    for b in data.get("bug_features", []):
        rows += tr(td(wi_link(b.get("WI Id",""))), td(e(b.get("WI State",""))),
                   td(e(b.get("Test Phase",""))), td(e(b.get("Environment","") or b.get("System.AreaPath",""))))
    _s(table_html(["Bug ID","State","Test Phase","Environment"], rows, "No bugs in scope"))

    # Cloned stories
    _s('<div class="section-title">Cloned Stories</div>\n')
    rows = ""
    CLONE_PATTERN = re.compile(r"Copied (?:with all (?:links|attachments and links) )?from #(\d+)", re.IGNORECASE)
    for s in all_stories:
        comment = s.get("Story Last Comment") or s.get("last_comment") or ""
        m = CLONE_PATTERN.search(comment)
        if m:
            rows += tr(td(wi_link(s.get("WI Id",""))), td("#" + wi_link(m.group(1))), td(e(s.get("WI State",""))))
    _s(table_html(["Story ID","Cloned From","Current State"], rows, "No cloned stories identified"))

    # Negative tests
    _s('<div class="section-title">Negative Test Coverage</div>\n')
    NEG_KEYWORDS = ["negative","invalid","error","reject","fail","not found","unauthori","forbidden",
                    "exceed","cannot","unable","should not","must not","no result","empty result",
                    "no data","boundary","out of range","wrong","missing field","bad request","exception"]
    genie_fails  = data.get("genie_failures",[])
    tc_dets      = data.get("test_case_details",[])
    neg_genie_ex = [f["name"][:80] for f in genie_fails if any(k in f.get("name","").lower() for k in NEG_KEYWORDS)][:5]
    neg_tc_ex    = [t["TC Title"][:80] for t in tc_dets if any(k in t.get("TC Title","").lower() for k in NEG_KEYWORDS)][:5]
    neg_story_ex = [(s.get("WI Id",""), (s.get("Story Last Comment") or "")[:80])
                    for s in all_stories if any(k in (s.get("Story Last Comment") or "").lower() for k in NEG_KEYWORDS)][:5]
    rows = (
        tr(td("Genie Regression Scenarios"),
           td(ok_span(f"Yes ({len(neg_genie_ex)})") if neg_genie_ex else na_span("No")),
           td(e("; ".join(neg_genie_ex)) if neg_genie_ex else na_span("None identified"))) +
        tr(td("Test Case Titles"),
           td(ok_span(f"Yes ({len(neg_tc_ex)})") if neg_tc_ex else na_span("No")),
           td(e("; ".join(neg_tc_ex)) if neg_tc_ex else na_span("None identified"))) +
        tr(td("Story Last Comments"),
           td(ok_span(f"Yes ({len(neg_story_ex)})") if neg_story_ex else na_span("No")),
           td("; ".join(f"Story {wi_link(sid)}: {e(cmt)}" for sid, cmt in neg_story_ex) if neg_story_ex else na_span("None identified")))
    )
    _s(table_html(["Source","Negative Tests Found","Examples"], rows))

    # Desc/AC quality — [Requires Review] placeholder
    _s('<div class="section-title">Description &amp; Acceptance Criteria Quality</div>\n')
    _s('<div class="rule-box">&#8505;&#65039; <strong>Informational only</strong> &mdash; never a CRITICAL/MODERATE gate.</div>\n')
    _s('<div class="review-note">&#9888;&#65039; <strong>[Requires Review]</strong> Detailed Desc/AC text quality assessment requires human judgement. '
       'The table below shows automated heuristic flags only (terse/placeholder text detected). '
       'A human reviewer should read the full Description and Acceptance Criteria for any stories '
       'flagged and confirm whether they are sufficiently detailed.</div>\n')
    PLACEHOLDER_AC = ["tbd","n/a","na","see attached","not applicable","to be defined"]
    rows = ""
    for s in all_stories:
        sid   = wi_link(s.get("WI Id", s.get("id","")))
        stype = "Story"
        dp    = ok_span("OK") if s.get("Desc Present","") == "OK" else warn_span(s.get("Desc Present","Missing"))
        ap    = ok_span("OK") if s.get("AC Present","") == "OK" else warn_span(s.get("AC Present","Missing"))
        desc  = re.sub(r"<[^>]+>","", s.get("Description Text", s.get("desc_text","")) or "").strip()
        ac    = re.sub(r"<[^>]+>","", s.get("Acceptance Criteria Text", s.get("ac_text","")) or "").strip()
        notes = []
        if desc and len(desc) < 50: notes.append("Desc very short")
        if ac and len(ac) < 50:     notes.append("AC very short")
        if ac.lower() in PLACEHOLDER_AC: notes.append("AC appears placeholder")
        assessment = warn_span("Requires review") if notes else ok_span("OK")
        note_text  = e("; ".join(notes)) if notes else na_span("None")
        rows += tr(td(sid), td(stype), td(dp), td(ap), td(assessment), td(note_text))
    _s(table_html(["WI ID","Type","Desc Present","AC Present","Assessment","Note"],
                  rows, "No story data"))

    # Cross-doc consistency
    _s('<div class="section-title">Cross-Document Consistency</div>\n')
    ptf = (data.get("release_pt_features") or [{}])[0]
    rf_  = (data.get("release_features") or [{}])[0]
    canon_ver = extract_canonical_version(rf_.get("System.Title",""))
    pt_plan_appr  = (ptf.get("ReleasePTPlanApproval") or [{}])[0]
    pt_report_appr = (ptf.get("ReleasePTReportApproval") or [{}])[0]
    docs = [
        ("PT Plan",   pt_plan_appr.get("Page Title",""),   pt_plan_appr.get("Page Accessible","NO")),
        ("PT Report", pt_report_appr.get("Page Title",""), pt_report_appr.get("Page Accessible","NO")),
        ("PTIA",      ptf.get("ReleasePTIAPageTitle",""),  "YES" if ptf.get("ReleasePTIAExists","NO") == "YES" else "NO"),
        ("PIT",       (data.get("pit_result") or [{}])[0].get("Page Title",""),
                      (data.get("pit_result") or [{}])[0].get("Page Accessible","NO")),
    ]
    rows = ""
    for doc_label, page_title, accessible in docs:
        if accessible != "YES":
            rows += tr(td(doc_label), td(na_span("N/A &mdash; page inaccessible")),
                       td(e(canon_ver)), td(na_span("N/A")), td(warn_span("&#9888; Inaccessible")))
            continue
        if not page_title:
            rows += tr(td(doc_label), td(na_span("N/A &mdash; not present")),
                       td(e(canon_ver)), td(na_span("N/A")), td(na_span("N/A")))
            continue
        ver_in_title = re.search(r'\d+\.\d+(?:\.\d+)?', page_title)
        if not canon_ver:
            match_cell = na_span("No version to compare")
            status_cell= na_span()
        elif ver_in_title and ver_in_title.group(0) == canon_ver:
            match_cell  = ok_span("Yes")
            status_cell = ok_span("&#9989; Match")
        elif ver_in_title:
            match_cell  = warn_span(f"No &mdash; found {ver_in_title.group(0)}")
            status_cell = warn_span("&#9888; MODERATE")
        else:
            match_cell  = warn_span("No version number found")
            status_cell = warn_span("&#9888; MINOR")
        rows += tr(td(doc_label), td(e(page_title)), td(e(canon_ver)), td(match_cell), td(status_cell))
    _s(table_html(["Document","Page Title","Expected Version","Version Match","Status"], rows))

    snow_features = data.get("snow_features", [])
    sf = snow_features[0] if snow_features else {}
    snow_desc = (sf.get("short_description") or [""])[0] if isinstance(sf.get("short_description"), list) else sf.get("short_description","")
    snow_enabled = data.get("snow_enabled", True)
    if snow_enabled and snow_desc:
        ver_in_snow = re.search(r'\d+\.\d+(?:\.\d+)?', snow_desc)
        if canon_ver and ver_in_snow and ver_in_snow.group(0) == canon_ver:
            match_s = ok_span("Yes")
            stat_s  = ok_span("&#9989; Match")
        elif canon_ver and ver_in_snow:
            match_s = warn_span(f"No &mdash; found {ver_in_snow.group(0)}")
            stat_s  = warn_span("&#9888; MODERATE")
        else:
            match_s = na_span()
            stat_s  = na_span()
        _s(table_html(["Source","Value","Match ADO Release Title","Status"],
                      tr(td("SNOW Description"), td(e(snow_desc)), td(match_s), td(stat_s))))
    else:
        _s(table_html(["Source","Value","Match ADO Release Title","Status"],
                      tr(td("SNOW Description"), td(na_span("N/A &mdash; SNOW disabled or empty")),
                         td(na_span()), td(na_span()))))

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------
def build_html(data: dict, r: Report, tables_html: str) -> str:
    stream = data.get("release_stream", "")
    release_id = data.get("release_id", "")
    rf = (data.get("release_features") or [{}])[0]
    rwi_title  = rf.get("System.Title", "")
    rwi_state  = rf.get("System.State", "")
    chg_id     = rf.get("Custom.CHGID", "") or rf.get("Custom.ADOCHGID", "") or rf.get("Custom.ADOCHGID", "")
    branch_id  = rf.get("Branch Id", "")
    collector_ver = data.get("collector_version", "")
    drift_span, _ = drift_indicator(collector_ver)

    # Skill Version Staleness Check banner (2026-10-13, mirrors SKILL.md v1.10.2):
    # distinct from the local collector-vs-skill drift badge above — this compares
    # the collector's locally-installed SKILL.md against the canonical repo's
    # stable `main` branch. Only rendered when the collector actually ran the
    # live check (skill_version_check present) AND found the install outdated.
    svc = data.get("skill_version_check") or {}
    staleness_banner_html = ""
    if svc and not svc.get("check_error") and svc.get("is_outdated"):
        staleness_banner_html = (
            '<div class="flash-warning" role="alert">&#9888;&#65039; This dtp-tda-report installation is '
            f'OUT OF DATE &mdash; local SKILL.md v{e(svc.get("local_version", "?"))}, canonical '
            f'&lsquo;{e(svc.get("source_branch", "main"))}&rsquo; branch is at '
            f'v{e(svc.get("latest_stable_version", "?"))}. Findings/rules may be missing upstream fixes or '
            f'new checks. Re-sync this plugin (apm update / re-clone from {e(svc.get("source_repo", ""))}) '
            'before relying on this report for release gate decisions.</div>'
        )

    snow_features = data.get("snow_features", [])
    sf = snow_features[0] if snow_features else {}
    snow_state = ""
    if isinstance(sf.get("state"), list):
        snow_state = sf["state"][0] if sf["state"] else ""
    else:
        snow_state = sf.get("state", "")
    if not data.get("snow_enabled", True):
        snow_state = "N/A (SNOW disabled)"

    # Verdict
    if r.count(CRITICAL) > 0:
        verdict_class = "blocked"
        verdict_icon  = "&#128308; BLOCKED"
    elif r.count(MODERATE) > 0:
        verdict_class = "conditional"
        verdict_icon  = "&#128993; CONDITIONAL PASS"
    else:
        verdict_class = "pass"
        verdict_icon  = "&#9989; PASS"

    def section(sev, label, icon, badge_cls, items):
        count = len(items)
        inner = "\n".join(items) if items else '<div class="finding">None identified &#9989;</div>'
        return f"""
<div class="section {sev}">
  <h2>{icon} {e(label)} <span class="badge {badge_cls}">{count}</span></h2>
  {inner}
</div>"""

    verdict_text = (
        f"{verdict_icon} &mdash; "
        + (f"{r.count(CRITICAL)} CRITICAL finding(s)" if r.count(CRITICAL) else "No CRITICAL findings")
        + (f", {r.count(MODERATE)} MODERATE finding(s)" if r.count(MODERATE) else "")
        + "."
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TDA Report &mdash; {e(rwi_title)}</title>
<style>
{CSS}
</style>
</head>
<body>

<div class="rem-toolbar">
  <span id="remToolbarInfo">&#128221; Remediation mode &mdash; click <strong>Remediate</strong> on any finding to record an annotation, then export.</span>
  <button class="rem-setname-btn" onclick="remSetName()">&#128100; Set Reviewer Name</button>
  <button class="rem-export-btn" onclick="remExport()">&#11015; Save Annotated Report</button>
</div>

<div class="header">
  <h1>TDA Checkpoint Report &mdash; {e(rwi_title)}</h1>
  <div class="meta">
    <strong>Release ID:</strong> {e(release_id)} &nbsp;|&nbsp;
    <strong>Stream:</strong> {e(stream)} &nbsp;|&nbsp;
    <strong>Branch:</strong> {e(branch_id)}<br>
    <strong>CHG:</strong> {e(chg_id)} &nbsp;|&nbsp;
    <strong>SNOW State:</strong> {e(snow_state)} &nbsp;|&nbsp;
    <strong>Release WI State:</strong> {e(rwi_state)} &nbsp;|&nbsp;
    <strong>Report Date:</strong> {REPORT_DATE}<br>
    <strong>Report Mode:</strong> &#128196; Script-generated (gen_tda_report.py v{SKILL_VERSION}) &nbsp;|&nbsp;
    <strong>Collector Version:</strong> {e(collector_ver or "Unknown")} &nbsp;|&nbsp;
    <strong>Version Drift:</strong> {drift_span}
  </div>
</div>
{staleness_banner_html}

<div class="flash-warning" role="alert">
  &#9888;&#65039; <strong>This is script generated AutoTDA report and is intended to use only during initial phase of release. This is not suitable to be uploaded to RWI as a final report. A skill generated report must be used as final AutoTDA report.</strong>
</div>

{section(CRITICAL, "CRITICAL Findings", "&#128308;", "c-badge", r.criticals)}
{section(MODERATE, "MODERATE Findings", "&#128993;", "m-badge", r.moderates)}
{section(MINOR,    "MINOR / Info",       "&#128309;", "i-badge", r.minors)}
{section(LOOKS,    "Looks Good",         "&#9989;",   "g-badge", r.looks)}

<details class="section tables" open>
  <summary>&#128202; Summary Tables <em style="font-weight:normal;font-size:12px;opacity:.8;">(click to collapse/expand)</em></summary>
  <div class="details-body">
{tables_html}
  </div>
</details>

<div class="verdict {verdict_class}">{verdict_text}</div>

<div class="footer">Generated by gen_tda_report.py v{SKILL_VERSION} &nbsp;|&nbsp; {e(stream)} Release {e(release_id)} &nbsp;|&nbsp; {REPORT_DATE}</div>

<script>
{JS}
</script>

</body>
</html>"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate an initial TDA HTML report that requires review.")
    parser.add_argument("input", help="Collector results or summary JSON path, relative to the workspace")
    parser.add_argument("--output", help="HTML output path, relative to the workspace")
    args = parser.parse_args()

    for ancestor in pathlib.Path(__file__).resolve().parents:
        if (ancestor / "release_clinic_env.py").is_file():
            sys.path.insert(0, str(ancestor))
            break
    from release_clinic_env import load_environment, workspace_root
    load_environment()
    root = workspace_root()
    json_path = pathlib.Path(args.input).expanduser()
    if not json_path.is_absolute():
        json_path = root / json_path
    if not json_path.is_file():
        parser.error(f"Input file not found: {json_path}")

    print(f"Reading: {json_path}")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    global ADO_ORGANIZATION, ADO_PROJECT
    ADO_ORGANIZATION = data.get("ado_organization") or "sc-ado"
    ADO_PROJECT = data.get("ado_project") or "FMQPR"

    stream     = data.get("release_stream", "UNKNOWN")
    release_id = data.get("release_id", "0")

    print(f"Analysing: {stream} / {release_id} ...")
    report = analyse(data)
    print(f"  CRITICAL: {report.count(CRITICAL)}  MODERATE: {report.count(MODERATE)}  MINOR: {report.count(MINOR)}  LOOKS GOOD: {report.count(LOOKS)}")

    print("Building tables ...")
    tables = build_tables(data)

    print("Assembling HTML ...")
    html = build_html(data, report, tables)

    if args.output:
        out_path = pathlib.Path(args.output).expanduser()
        if not out_path.is_absolute():
            out_path = root / out_path
    else:
        safe_stream = re.sub(r"[^A-Za-z0-9_-]", "_", str(stream))
        safe_release = re.sub(r"[^A-Za-z0-9_-]", "_", str(release_id))
        directory = pathlib.Path(os.environ.get("TDA_OUTPUT_DIR") or root / ".workbench/release-clinic/reports")
        if not directory.is_absolute():
            directory = root / directory
        out_path = directory / f"TDAReport_{safe_stream}_{safe_release}.html"

    # Quick integrity check
    checks = [
        ("rem-toolbar present",    "rem-toolbar" in html),
        ("remSetName present",     "remSetName" in html),
        ("remExport present",      "remExport" in html),
        ("DOMContentLoaded",       "DOMContentLoaded" in html),
        ("script tag",             "<script>" in html),
        ("ends with </html>",      html.rstrip().endswith("</html>")),
    ]
    all_ok = all(v for _, v in checks)
    writing_review = (
        "standard: ASD-STE100\n"
        f"automated_check: {'PASSED' if all_ok else 'FAILED'}\n"
        "asd_review: PENDING\n"
        "reviewer: null\n"
        "reviewed_at: null\n"
        "limitations:\n"
        "  - Automated checks cover HTML structure only.\n"
        "  - Automated checks do not check the complete approved dictionary or grammar rules.\n"
    )
    review_html = '<details id="writing-review"><summary>Writing review</summary><pre>' + _esc(writing_review) + '</pre></details>\n'
    before, closing, after = html.rpartition('</body>')
    html = before + review_html + closing + after if closing else html + review_html
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"\nReport written to: {out_path}  ({len(html):,} chars)")

    for k, v in checks:
        print(f"  {'OK' if v else 'MISSING'}: {k}")
    if not all_ok:
        print("\nINTEGRITY CHECK FAILED — regenerate the report.")
        sys.exit(1)
    else:
        print("\nAll integrity checks passed.")

    # Remind about [Requires Review] items
    review_count = html.count("[Requires Review]")
    if review_count:
        print(f"\n[Requires Review] placeholders: {review_count}")
        print("  These sections need a human (or a brief LLM pass) to fill in judgement-based text:")
        print("  - PTIA justification quality (if applicable)")
        print("  - Desc/AC text quality assessment")
        print("  Open the report in a browser and search for '[Requires Review]' to locate them.")


if __name__ == "__main__":
    main()
