"""Detailed, dependency-free coverage reports from retained comparison results.

The renderer never acquires permissions or changes comparison outcomes.  Both
formats consume the same document model so row details have one source.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import html
import json
from pathlib import Path
import re


STYLE = """
:root{--ink:#1b2b42;--muted:#53657b;--line:#d9e2ee;--blue:#124e8c;--amber:#8a4b09;--paper:#fff}
*{box-sizing:border-box}body{margin:0;background:#edf2f7;color:var(--ink);font:15px/1.55 system-ui,sans-serif}
main{max-width:1440px;margin:0 auto;padding:32px 28px 70px}h1{font-size:clamp(25px,4vw,38px);line-height:1.18;letter-spacing:-.03em}
h2{margin-top:40px;border-top:2px solid var(--line);padding-top:22px;font-size:24px}h3{font-size:19px;margin-top:27px}
h4{font-size:16px;margin-top:24px}p{max-width:1050px}a{color:var(--blue);overflow-wrap:anywhere}a:focus,input:focus,select:focus,button:focus,summary:focus{outline:3px solid #d68421;outline-offset:3px}
.coverage-report{background:var(--paper);padding:28px;border-radius:14px;box-shadow:0 5px 25px #16304d0d;margin-bottom:30px}
.critical{border-left:5px solid #b36916;background:#fff6e6;padding:16px 20px;margin:20px 0;font-weight:600}
.context{color:var(--muted)}.toolbar{display:flex;gap:12px;align-items:end;flex-wrap:wrap;background:#edf3fa;padding:15px;border-radius:8px;margin:20px 0}
label{display:grid;gap:5px;font-size:13px;font-weight:650}input,select,button{font:inherit;padding:9px 11px;border:1px solid #a6b6c9;border-radius:5px;background:white;color:var(--ink)}
input{min-width:250px}button{cursor:pointer}.table-wrap{overflow-x:auto;margin:14px 0 24px;border:1px solid var(--line);border-radius:7px}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
th{background:#eef3f9;font-size:12px;font-weight:700;position:sticky;top:0}tr:last-child td{border-bottom:0}tr:nth-child(even) td{background:#fafcfe}
td:first-child{font-weight:550}details{margin:17px 0;border:1px solid var(--line);padding:15px;border-radius:8px}summary{cursor:pointer;font-weight:700;color:var(--blue)}
.empty{color:var(--muted);font-style:italic}.pill{display:inline-block;padding:3px 8px;background:#e9eff8;border-radius:4px;font-size:12px;font-weight:750}
nav{display:flex;flex-wrap:wrap;gap:8px 18px;margin:20px 0}small{color:var(--muted)}[hidden]{display:none!important}
@media(max-width:700px){main{padding:12px}.coverage-report{padding:16px;border-radius:8px}th,td{padding:8px}input{min-width:180px;width:100%}.toolbar label{width:100%}}
@media print{body{background:white;font-size:10pt}main,.coverage-report{max-width:none;padding:0;box-shadow:none}.toolbar,nav{display:none}details{break-inside:avoid}details>*{display:block!important}th{position:static}h2,h3{break-after:avoid}.table-wrap{overflow:visible}a{color:inherit;text-decoration:none}tr{break-inside:avoid}}
"""

SCRIPT = """
document.querySelectorAll('[data-coverage-report]').forEach(root=>{
 const search=root.querySelector('[data-report-search]');
 const status=root.querySelector('[data-account-filter]');
 const apply=()=>{
  const query=(search?.value||'').toLowerCase().trim(), wanted=status?.value||'';
  root.querySelectorAll('[data-filter-row]').forEach(row=>{
   const accountStatus=row.getAttribute('data-account-status');
   const owner=row.closest('[data-user-record]');
   const accountMatch=!!(query&&owner&&(owner.getAttribute('data-user-id')||'').toLowerCase().includes(query));
   row.hidden=!!((query&&!accountMatch&&!row.textContent.toLowerCase().includes(query))||(wanted&&accountStatus&&accountStatus!==wanted));
   if(query&&!row.hidden){let d=row.closest('details');while(d&&root.contains(d)){d.open=true;d=d.parentElement.closest('details')}}
  });
  root.querySelectorAll('[data-user-record]').forEach(record=>{
   record.hidden=!!((query&&!record.textContent.toLowerCase().includes(query))||(wanted&&record.getAttribute('data-user-status')!==wanted));
  });
 };
 search?.addEventListener('input',apply);status?.addEventListener('change',apply);
 root.querySelector('[data-expand]')?.addEventListener('click',()=>root.querySelectorAll('details').forEach(d=>d.open=true));
 root.querySelector('[data-collapse]')?.addEventListener('click',()=>root.querySelectorAll('details').forEach(d=>d.open=false));
});
"""


def _text(value):
    if value is None:
        return "UNASSESSED"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)


def _md(value):
    value = html.escape(_text(value), quote=False).replace("\n", "<br>")
    return re.sub(r"([\\`*_[\]{}|#!])", r"\\\1", value)


def _esc(value):
    return html.escape(_text(value), quote=True)


@dataclass(frozen=True)
class _Link:
    label: str
    href: str


class _Document:
    def __init__(self, prefix="", link_prefix="", heading_offset=0):
        # Prefixes and links come from caller-owned output paths, never source fields.
        if not re.fullmatch(r"[A-Za-z0-9_-]*", prefix):
            raise ValueError("Report anchor prefix must use safe identifier characters")
        if link_prefix and (not re.fullmatch(r"[A-Za-z0-9_./-]+", link_prefix)
                            or ".." in link_prefix.split("/") or link_prefix.startswith("/")):
            raise ValueError("Report links require a safe relative prefix")
        self.prefix, self.link_prefix, self.heading_offset = prefix, link_prefix, heading_offset
        self.markdown, self.html = [], []

    def cell(self, value, md=False):
        if isinstance(value, _Link):
            target = ("#" + self.prefix + value.href[1:] if value.href.startswith("#")
                      else self.link_prefix + value.href)
            return ("[" + _md(value.label) + "](" + target + ")" if md
                    else '<a href="' + _esc(target) + '">' + _esc(value.label) + "</a>")
        return _md(value) if md else _esc(value)

    def heading(self, title, level=2, anchor=None):
        ident = ' id="' + self.prefix + anchor + '"' if anchor else ""
        self.html.append(f"<h{level}{ident}>" + _esc(title) + f"</h{level}>")
        if anchor:
            self.markdown.append('<a id="' + self.prefix + anchor + '"></a>\n')
        self.markdown.append("#" * min(6, level + self.heading_offset) + " " + _md(title) + "\n")

    def paragraph(self, value, critical=False):
        self.html.append('<p class="critical">' + _esc(value) + "</p>" if critical else "<p>" + _esc(value) + "</p>")
        self.markdown.append(("> **" + _md(value) + "**" if critical else _md(value)) + "\n")

    def links(self, links):
        self.html.append("<nav aria-label=\"Report sections and downloads\">" + "".join(self.cell(link) for link in links) + "</nav>")
        self.markdown.append(" · ".join(self.cell(link, True) for link in links) + "\n")

    def table(self, headers, rows, *, ident=None, account_statuses=None, explicit_body=False):
        rows = list(rows)
        if not rows:
            self.html.append('<p class="empty">No rows in this assessed comparison.</p>')
            self.markdown.append("No rows in this assessed comparison.\n")
            return
        attrs = ' id="' + self.prefix + ident + '"' if ident else ""
        self.html.append('<div class="table-wrap"><table' + attrs + "><thead><tr>" +
                         "".join("<th scope=\"col\">" + _esc(h) + "</th>" for h in headers) + "</tr></thead>" +
                         ("<tbody>" if explicit_body else ""))
        self.markdown.extend(["| " + " | ".join(_md(h) for h in headers) + " |",
                              "| " + " | ".join("---" for _ in headers) + " |"])
        for i, row in enumerate(rows):
            extra = (' data-account-status="' + _esc(account_statuses[i]) + '"' if account_statuses else "")
            self.html.append("<tr data-filter-row" + extra + ">" +
                             "".join("<td>" + self.cell(v) + "</td>" for v in row) + "</tr>")
            self.markdown.append("| " + " | ".join(self.cell(v, True) for v in row) + " |")
        self.html.append(("</tbody>" if explicit_body else "") + "</table></div>")
        self.markdown.append("")

    def details(self, title, *, user_status=None, user_id=None):
        attrs = (' data-user-record data-user-status="' + _esc(user_status) + '" data-user-id="' + _esc(user_id) + '"'
                 if user_status else "")
        self.html.append("<details" + attrs + "><summary>" + _esc(title) + "</summary>")
        self.markdown.append("### " + _md(title) + "\n")

    def close_details(self):
        self.html.append("</details>")


def _rate(numerator, denominator):
    if denominator in (None, 0) or numerator is None:
        return "UNASSESSED (empty or unavailable denominator)"
    return f"{numerator}/{denominator} ({100 * numerator / denominator:.2f}%)"


def _counts(comparison, baseline, target):
    baseline_rate = _rate(comparison.get("matched_count"), comparison.get("baseline_count"))
    target_rate = _rate(comparison.get("matched_count"), comparison.get("candidate_count"))
    if comparison.get("complete") is False:
        baseline_rate, target_rate = "Assessed only: " + baseline_rate, "Assessed only: " + target_rate
    return [comparison.get("status", "UNASSESSED"), comparison.get("baseline_count"),
            comparison.get("candidate_count"), comparison.get("matched_count"),
            comparison.get("missing_count"), comparison.get("additional_count"),
            baseline_rate, target_rate,
            comparison.get("equal")]


def _count_headers(baseline, target):
    return ["Status", baseline + " count", target + " count", "Shared", baseline + " only",
            target + " only", baseline + " retained in " + target,
            target + " retained in " + baseline, "Exactly equal"]


def _tuple_headers(kind, length, same_system):
    first = "Entity" if same_system else "Mapped application"
    if kind == "effective":
        known = [first, "Subject / feature", "Action"]
    elif kind in ("profile_grants", "grants"):
        known = [first, "Role / entitlement", "Subject / feature", "Action"]
    elif kind in ("assignments", "profile_names", "roles", "matrix_assignment_comparison", "catalog_membership"):
        known = [first, "Role / entitlement"] if length > 1 else ["Role / entitlement"]
    elif kind == "subjects":
        known = [first, "Subject / feature"] if length > 1 else ["Subject / feature"]
    else:
        known = ["Item " + str(i + 1) for i in range(length)]
    return known[:length] + ["Item " + str(i + 1) for i in range(len(known), length)]


def _tuple_table(doc, items, kind, same_system):
    items = [list(item) if isinstance(item, (list, tuple)) else [item] for item in items]
    length = max((len(item) for item in items), default=1)
    doc.table(_tuple_headers(kind, length, same_system), [item + [""] * (length - len(item)) for item in items])


def _flatten(value, prefix=""):
    if isinstance(value, dict):
        if not value:
            yield prefix, "Empty object supplied"
        for key, child in value.items():
            yield from _flatten(child, prefix + "." + str(key) if prefix else str(key))
    elif isinstance(value, list):
        if not value:
            yield prefix, "No entries supplied"
        for index, child in enumerate(value):
            yield from _flatten(child, prefix + "[" + str(index + 1) + "]")
    else:
        yield prefix, value


def _errors(record):
    values = list(record.get("errors", []))
    if record.get("error"):
        values.append(record["error"])
    return values


def _error_text(errors):
    return "; ".join(str(e.get("source", "source")) + ": " + str(e.get("code", "UNKNOWN_ERROR")) +
                     (" (HTTP " + str(e["http_status"]) + ")" if e.get("http_status") is not None else "") for e in errors)


def _case_warning(user):
    warnings = []
    if user.get("catalog_membership", {}).get("status") == "UNASSESSED":
        warnings.append("catalog_membership: UNASSESSED")
    if not user.get("matrix_assignment_comparison", {}).get("equal", True):
        warnings.append("matrix_assignment_comparison: DIFFERENT")
    return "; ".join(warnings)


def _comparison_details(doc, title, comparison, kind, same_system, matched_appendix, baseline, target,
                        *, account_id=None, account_status=None):
    doc.heading(title, 4)
    doc.table(_count_headers(baseline, target), [_counts(comparison, baseline, target)])
    if comparison.get("complete") is False:
        doc.paragraph("Partial comparison. Counts cover assessed inventories only; complete coverage remains UNASSESSED.")
        doc.table(["Unavailable entity"], [[e] for e in comparison.get("unassessed_entities", [])])
    for key, label in (("missing", baseline + " only — absent from " + target),
                       ("additional", target + " only — absent from " + baseline)):
        doc.heading(label, 4)
        _tuple_table(doc, comparison.get(key, []), kind, same_system)
    if comparison.get("matched"):
        matched_appendix.append((title, comparison["matched"], kind, account_id, account_status))


def _role_definition_summary(doc, entitlements):
    comparison = entitlements.get("profile_grants")
    if not isinstance(comparison, dict):
        return
    shared = {tuple(row) for row in comparison.get("matched", []) if len(row) == 4}
    missing = {tuple(row) for row in comparison.get("missing", []) if len(row) == 4}
    additional = {tuple(row) for row in comparison.get("additional", []) if len(row) == 4}
    roles = {row[:2] for row in shared | missing | additional}
    names = entitlements.get("profile_names", {})
    roles.update(tuple(row) for kind in ("matched", "missing", "additional")
                 for row in names.get(kind, []) if len(row) == 2)
    rows = []
    for app, role in sorted(roles):
        matched_count = sum(row[:2] == (app, role) for row in shared)
        missing_count = sum(row[:2] == (app, role) for row in missing)
        additional_count = sum(row[:2] == (app, role) for row in additional)
        baseline_count = matched_count + missing_count
        target_count = matched_count + additional_count
        status = ("UNASSESSED: no baseline matrix content" if baseline_count == 0 else
                  "DIFFERENT" if missing_count or additional_count else "MATCH")
        rows.append([app, role, baseline_count, target_count, matched_count, missing_count,
                     additional_count, _rate(matched_count, baseline_count), status])
    doc.heading("Definition comparison by role / entitlement", 3)
    doc.paragraph("Each row groups observed application/role/feature/action tuples. A role name without baseline content cannot establish definition equality.")
    doc.table(["Mapped application", "Role / entitlement", "Baseline tuples", "Target tuples", "Shared",
               "Baseline only", "Target only", "Baseline tuple retention", "Observed definition status"], rows)


def _source_rows(result, directory, doc):
    binding = result.get("binding", {})
    rows = []
    for field, value in binding.items():
        if field == "replay_sha256" and isinstance(value, dict):
            rows.extend(["Supplied capture", path, digest] for path, digest in value.items())
        elif field == "implementation_sha256" and isinstance(value, dict):
            rows.extend(["Implementation", path, digest] for path, digest in value.items())
        elif field == "matrix_sha256" and isinstance(value, list):
            rows.extend(["Matrix", "Matrix " + str(i + 1), digest] for i, digest in enumerate(value))
        else:
            rows.append(["Binding", field, value])
    doc.table(["Evidence type", "Source or field", "Recorded SHA-256 / value"], rows)
    if directory is None:
        doc.paragraph("Retained response-file listing is unavailable without a run directory. See binding.json and result.json.")
        return
    files = []
    for path in sorted((Path(directory) / "responses").glob("*.json")):
        if not re.fullmatch(r"[a-f0-9]{64}\.json", path.name):
            continue
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            files.append([_Link(path.name, "responses/" + path.name), "UNREADABLE", "UNASSESSED", "UNASSESSED", "UNASSESSED"])
            continue
        files.append([_Link(path.name, "responses/" + path.name), item.get("source", "Not recorded"),
                      item.get("at"), item.get("source_sha256"), item.get("data_sha256")])
    doc.heading("Retained response bodies", 3)
    doc.table(["Response file", "Recorded source", "Captured at", "Source SHA-256", "Response data SHA-256"], files)
    doc.paragraph("Response links point to retained, sanitized bodies. Capture times do not establish an atomic cross-environment snapshot.")


def _build(result, directory=None, *, prefix="", link_prefix="", heading_offset=0):
    doc = _Document(prefix, link_prefix, heading_offset)
    same_system = "direction" in result and "inventories" in result.get("entitlements", {})
    direction = result.get("direction", {})
    baseline = direction.get("baseline", "EMS2 PROD" if same_system else "EMS2")
    target = direction.get("target", "EMS2 UAT" if same_system else "CES")
    title = baseline + " → " + target + " coverage report"
    doc.html.append('<article class="coverage-report" id="' + prefix + 'coverage-report" data-coverage-report>')
    doc.heading(title, 1)
    status = result.get("status", "INCOMPLETE")
    doc.paragraph(status + ": " + result.get("conclusion", "Review the measured differences and unassessed scope."), critical=True)
    doc.paragraph("Action: review missing, additional, and unavailable content before declaring parity. Owner: unknown.")
    doc.paragraph("Consequence: name coverage and matching effective permissions do not establish complete profile equality.")
    doc.links([_Link("Summary", "#summary"), _Link("Entitlements", "#entitlements"), _Link("Users", "#user-details"),
               _Link("Unassessed scope", "#unassessed"), _Link("Evidence", "#evidence"),
               _Link("Markdown", "report.md"), _Link("JSON", "result.json"), _Link("Differences CSV", "differences.csv"),
               _Link("Checkpoints", "cases.jsonl"), _Link("Source binding", "binding.json")])
    doc.table(["Run field", "Value"], [["Evidence source", result.get("evidence_source", "Not recorded")],
              ["Mode", result.get("mode")], ["Scope", result.get("scope")], ["Baseline", baseline], ["Target", target],
              ["Started at", result.get("started_at")], ["Finished at", result.get("finished_at")]])
    doc.paragraph(("PROD is the baseline. " if same_system else "EMS2 is the baseline. ") +
                  "Missing means baseline-only content absent from the target. Additional means target-only content absent from the baseline.")
    doc.paragraph("Reverse-direction gaps use the same rows with those labels exchanged. Environment-specific numeric IDs are request locators.")
    if result.get("mode") == "replay":
        doc.paragraph("MOCK SAMPLE: supplied API responses only. These findings do not establish current live-state parity.", critical=True)
    doc.html.append('<div class="toolbar"><label>Search all report tables<input type="search" data-report-search placeholder="Account, role, feature, action, error"></label>'
                    '<label>Account status<select data-account-filter><option value="">All account statuses</option><option>MATCH</option><option>DIFFERENT</option><option>UNASSESSED</option></select></label>'
                    '<button type="button" data-expand>Expand details</button><button type="button" data-collapse>Collapse details</button></div>')

    summary = result.get("summary", {})
    inventory = result.get("inventory", {})
    users = result.get("users", [])
    doc.heading("Coverage summary and denominators", anchor="summary")
    metric_rows = [["Discovered accounts", summary.get("discovered_accounts"), "Union of declared discovery sources; not a complete directory guarantee"],
                   ["Baseline accounts", summary.get("baseline_accounts"), "Baseline matrix and observed baseline assignments"],
                   ["Compared accounts", summary.get("compared_accounts"), "Paired, valid responses"],
                   ["Matching functional accounts", summary.get("matching_accounts"), "Assignments, effective permissions, and role grants match"],
                   ["Different functional accounts", summary.get("different_accounts"), "At least one assessed functional comparison differs"],
                   ["Unassessed accounts", summary.get("unassessed_accounts"), "Unavailable, invalid, failed, or not fetched"],
                   ["Account assessment rate", _rate(summary.get("compared_accounts"), summary.get("discovered_accounts")), "Compared / discovered; measures assessment completeness"],
                   ["Functional matches among assessed accounts", _rate(summary.get("matching_accounts"), summary.get("compared_accounts")), "Sample rate; does not describe unassessed accounts"],
                   ["Complete functional profile coverage", "UNASSESSED" if summary.get("functional_profile_coverage_percent") is None else str(summary["functional_profile_coverage_percent"]) + "%", "Requires the declared population to be assessed; full data equality is separate"],
                   ["Full data-profile equality", summary.get("full_data_profile_coverage", "UNASSESSED"), "Requires comparable field/value policies and empty-role definitions"],
                   ["Reported subject retention", summary.get("subject_coverage", "UNASSESSED"), "Read the inventory and definition limits below"],
                   ["Reported role-grant retention", summary.get("role_grant_preservation", "UNASSESSED"), "Definition tuples for CES; observed user role grants for EMS2 environments"]]
    doc.table(["Metric", "Result", "Denominator and meaning"], metric_rows)
    extra = [(key.replace("_", " "), value) for key, value in summary.items()
             if key not in {"discovered_accounts", "baseline_accounts", "compared_accounts", "matching_accounts", "different_accounts", "unassessed_accounts", "functional_profile_coverage_percent", "full_data_profile_coverage", "subject_coverage", "role_grant_preservation"}]
    doc.table(["Additional retained metric", "Value"], extra)
    doc.paragraph("Retention measures shared / baseline. Exact equality also requires zero target-only entries. Empty denominators remain UNASSESSED.")
    doc.heading("Active user differences and source-consistency warnings", 3)
    active = [u for u in users if u.get("status") not in ("MATCH", "UNASSESSED") or _case_warning(u)]
    doc.table(["Account", "Status", baseline + " effective", target + " effective", "Shared", baseline + " only", target + " only", "Source warning"],
              [[u["user_id"], u.get("status"), u.get("effective", {}).get("baseline_count"), u.get("effective", {}).get("candidate_count"),
                u.get("effective", {}).get("matched_count"), u.get("effective", {}).get("missing_count"), u.get("effective", {}).get("additional_count"),
                _case_warning(u) or "None"] for u in active], ident="users", explicit_body=True,
              account_statuses=[u.get("status", "UNASSESSED") for u in active])
    doc.paragraph("Matching accounts leave the active difference list. Their counts, account register, and matched content remain below.")

    matched_appendix = []
    entitlements = result.get("entitlements", {})
    doc.heading("Entitlement definitions and inventories", anchor="entitlements")
    doc.paragraph("Role-name and subject-name inventories establish presence only. They do not establish complete role-to-subject-to-action equality.")
    if same_system:
        doc.paragraph("Complete EMS2 role definitions are unavailable. User permission rows cannot reconstruct unused or empty role content.")
    else:
        doc.paragraph("EMS2 role/entity/subject/action map to CES entitlement/app/feature/action. Matrix definitions and API inventories remain separate evidence.")
    doc.paragraph("Partial inventory retention rates cover assessed inventories only. Complete inventory coverage remains UNASSESSED when any entity is unavailable.")
    comparisons = [(k, v) for k, v in entitlements.items() if isinstance(v, dict) and "baseline_count" in v]
    label_names = {"profile_grants": "Matrix role / feature / action definitions", "profile_names": "Mapped role / entitlement names", "subjects": "Subject / feature names", "roles": "Role-name inventory"}
    definition_baseline, definition_target = (baseline, target) if same_system else ("Supplied EMS2 matrix", "CES catalog")
    doc.table(["Comparison"] + _count_headers(definition_baseline, definition_target),
              [[label_names.get(key, key)] + _counts(value, definition_baseline, definition_target) for key, value in comparisons])
    _role_definition_summary(doc, entitlements)
    checks = entitlements.get("inventories", entitlements.get("live_inventories", []))
    inventory_baseline, inventory_target = (baseline, target) if same_system else ("EMS2 API inventory", "Supplied matrix")
    doc.heading("Inventory assessment by entity", 3)
    if not same_system:
        doc.paragraph("These source-consistency checks compare EMS2 API inventory names with supplied matrix names. They do not compare EMS2 inventories with CES.")
    doc.table(["Entity", "Inventory", "Status", "Baseline source", "Target source", "Baseline count", "Target count", "Shared", "Baseline only", "Target only", "Errors"],
              [[c.get("entity"), c.get("kind"), c.get("status", c.get("comparison", {}).get("status", "UNASSESSED")),
                inventory_baseline, inventory_target,
                c.get("comparison", {}).get("baseline_count"), c.get("comparison", {}).get("candidate_count"),
                c.get("comparison", {}).get("matched_count"), c.get("comparison", {}).get("missing_count"),
                c.get("comparison", {}).get("additional_count"), _error_text(_errors(c)) or "None"] for c in checks])
    for key, comparison in comparisons:
        _comparison_details(doc, label_names.get(key, key), comparison, key, same_system, matched_appendix, definition_baseline, definition_target)
    for check in checks:
        if "comparison" not in check:
            continue
        label = str(check.get("entity", "Unknown entity")) + " / " + str(check.get("kind", "inventory"))
        doc.details("Inventory detail: " + label)
        _comparison_details(doc, label, check["comparison"], check.get("kind", "inventory"), same_system, matched_appendix, inventory_baseline, inventory_target)
        doc.close_details()
    if entitlements.get("matrix_limits"):
        doc.heading("Matrix definitions unavailable", 3)
        doc.paragraph("These roles have names without complete matrix permission content. Their coverage cannot establish complete definition equality.")
        doc.table(["Unavailable matrix definition", "Value"], list(_flatten(entitlements["matrix_limits"])))

    doc.heading("User profile comparisons", anchor="user-details")
    doc.paragraph("Each account keeps assignments, effective permissions, role-specific grants, and data restrictions separate.")
    assessed = [u for u in users if u.get("status") != "UNASSESSED"]
    for user in assessed:
        account = str(user.get("user_id", "Unknown account"))
        doc.details("Account " + account + " — " + str(user.get("status", "UNASSESSED")), user_status=user.get("status", "UNASSESSED"), user_id=account)
        doc.table(["Field", "Result"], [["Account", account], ["Functional status", user.get("status")],
                  ["Compared at", user.get("at")], ["Role evidence", user.get("role_evidence", "Not recorded")],
                  ["Exact full profile", user.get("exact_full_profile_status", "UNASSESSED")]])
        for key, label in (("effective", "Effective permissions"), ("assignments", "Role assignments"), ("profile_grants", "Role-specific grants")):
            _comparison_details(doc, "Account " + account + " / " + label, user.get(key, {}), key, same_system,
                                matched_appendix, baseline, target, account_id=account,
                                account_status=user.get("status", "UNASSESSED"))
        if "matrix_assignment_comparison" in user:
            doc.paragraph("Matrix consistency compares matrix assignments as baseline with EMS2 response assignments as target.")
            _comparison_details(doc, "Account " + account + " / Matrix assignment consistency", user["matrix_assignment_comparison"], "matrix_assignment_comparison", same_system,
                                matched_appendix, "Matrix", "EMS2 response", account_id=account,
                                account_status=user.get("status", "UNASSESSED"))
        if "catalog_membership" in user:
            membership = user["catalog_membership"]
            doc.paragraph("Catalog membership status: " + str(membership.get("status")) + ". " + str(membership.get("limit", "")))
            _comparison_details(doc, "Account " + account + " / Catalog membership consistency", membership.get("comparison", {}), "catalog_membership", same_system,
                                matched_appendix, "Catalog membership", "Effective role names", account_id=account,
                                account_status=user.get("status", "UNASSESSED"))
        if user.get("outside_scope_permissions"):
            doc.heading("Excluded target permissions retained for review", 4)
            _tuple_table(doc, user["outside_scope_permissions"], "effective", same_system)
        if user.get("outside_baseline_roles"):
            doc.heading("Excluded target roles retained for review", 4)
            _tuple_table(doc, user["outside_baseline_roles"], "assignments", same_system)
        doc.heading("Data restrictions and observed target content", 4)
        doc.paragraph("UNASSESSED: target policy names and values are observations. No comparable complete EMS2 field/value definition was supplied.")
        doc.table(["Policy / field path", "Recorded value"], list(_flatten(user.get("data_scope", {"status": "UNASSESSED"}))))
        if user.get("errors"):
            doc.table(["Source", "Error code", "HTTP status"], [[e.get("source", "source"), e.get("code"), e.get("http_status")] for e in user["errors"]])
        doc.close_details()
    if not assessed:
        doc.paragraph("No paired account responses were assessed. Unavailable responses do not represent empty passing profiles.")

    doc.heading("Unassessed scope and acquisition errors", anchor="unassessed")
    account_map = {str(u.get("user_id")): u for u in users}
    population = sorted({str(u) for u in inventory.get("users", [])} | set(account_map))
    unassessed = []
    causes = Counter()
    for account in population:
        user = account_map.get(account)
        if user and user.get("status") != "UNASSESSED":
            continue
        errors = _errors(user or {}) or [{"source": "collection", "code": "NOT_FETCHED", "http_status": None}]
        reason = _error_text(errors)
        causes[reason] += 1
        unassessed.append([account, "UNASSESSED", reason])
    doc.paragraph("Every discovered unassessed account appears below. Missing or wrong-context captures cannot contribute passing coverage.")
    doc.table(["Unassessed cause", "Accounts"], sorted(causes.items()))
    doc.details("Complete unassessed account register (" + str(len(unassessed)) + ")")
    doc.table(["Account", "Status", "Cause"], unassessed, ident="unassessed-users", account_statuses=["UNASSESSED"] * len(unassessed))
    doc.close_details()
    acquisition = [["Run", "", e.get("source", "source"), e.get("code"), e.get("http_status")] for e in result.get("errors", [])]
    acquisition += [["Inventory", c.get("entity"), e.get("source", c.get("kind", "source")), e.get("code"), e.get("http_status")]
                    for c in checks for e in _errors(c)]
    doc.table(["Scope", "Entity", "Source", "Error code", "HTTP status"], acquisition)

    doc.heading("Scope, mappings, and exclusions", anchor="scope")
    doc.paragraph("Discovery source: " + str(inventory.get("source", "Not recorded")))
    counts = [[key.replace("_", " "), len(value)] for key, value in inventory.items() if isinstance(value, list)]
    doc.table(["Discovery inventory", "Entries"], counts)
    doc.table(["Excluded entity", "Priority", "Reason"], [[e.get("name"), e.get("priority", "Not recorded"), e.get("reason", "Not recorded")] for e in result.get("excluded", [])])
    doc.table(["Excluded application", "Feature", "Reason"], [[e.get("app"), e.get("feature"), e.get("reason", "Not recorded")] for e in result.get("excluded_features", [])])
    context = result.get("comparison_context")
    if context:
        doc.details("Environment routing, matrices, and explicit mappings")
        doc.table(["Configuration field", "Recorded value"], list(_flatten(context)))
        doc.close_details()
    doc.table(["Evidence limit"], [[value] for value in result.get("limits", [])])

    doc.heading("Evidence, source identity, and review", anchor="evidence")
    doc.links([_Link("Complete result", "result.json"), _Link("Exact binding", "binding.json"), _Link("Differences CSV", "differences.csv"), _Link("Durable account checkpoints", "cases.jsonl")])
    _source_rows(result, directory, doc)
    doc.table(["Review field", "Value"], [["Standard", "ASD-STE100"], ["Automated report check", "NOT_RUN"], ["ASD review", "PENDING"],
              ["Reviewer", "Not recorded"], ["Reviewed at", "Not recorded"],
              ["Review limit", "Automated checks do not check the complete approved dictionary or grammar rules."]])
    doc.paragraph("The generated report does not establish business approval, migration acceptance, deployment authorization, or full live parity.")

    doc.heading("Matched content and complete account appendix", anchor="matched")
    doc.paragraph("Matched rows remain counted and preserved. They are separated from active differences, not discarded.")
    for label, items, kind, account_id, account_status in matched_appendix:
        doc.details("Matched: " + label + " (" + str(len(items)) + ")", user_id=account_id,
                    user_status=account_status)
        _tuple_table(doc, items, kind, same_system)
        doc.close_details()
    baseline_users = {str(u) for u in inventory.get("baseline_users", [])}
    catalog_users = {str(u) for u in inventory.get("catalog_users", [])}
    doc.details("Complete discovered account register (" + str(len(population)) + ")")
    register = [[account, account_map.get(account, {}).get("status", "UNASSESSED"),
                 "Yes" if account in baseline_users else "No", "Yes" if account in catalog_users else "Not listed",
                 _error_text(_errors(account_map.get(account, {}))) or ("NOT_FETCHED" if account not in account_map else "None")]
                for account in population]
    doc.table(["Account", "Status", "Baseline account", "Catalog account", "Acquisition error"], register, ident="account-register",
              account_statuses=[account_map.get(account, {}).get("status", "UNASSESSED") for account in population])
    doc.close_details()
    doc.html.append("</article>")
    return doc, title


def render_markdown(result, directory=None, *, prefix="", link_prefix="", heading_offset=0):
    """Return all report rows in portable Markdown with safe relative links."""
    doc, _ = _build(result, directory, prefix=prefix, link_prefix=link_prefix, heading_offset=heading_offset)
    review = ("---\nwriting_review:\n  standard: ASD-STE100\n  automated_check: NOT_RUN\n"
              "  asd_review: PENDING\n  reviewer: null\n  reviewed_at: null\n  limitations:\n"
              "    - Automated checks do not check the complete approved dictionary or grammar rules.\n---\n\n")
    return (review if heading_offset == 0 else "") + "\n".join(doc.markdown) + "\n"


def render_fragment(result, directory=None, *, prefix="", link_prefix=""):
    """Return a prefixed HTML body fragment for embedding in a suite report."""
    doc, _ = _build(result, directory, prefix=prefix, link_prefix=link_prefix)
    return "\n".join(doc.html)


def render_html(result, directory=None, *, prefix="", link_prefix=""):
    """Return a self-contained, accessible HTML document with every detail."""
    doc, title = _build(result, directory, prefix=prefix, link_prefix=link_prefix)
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            "<title>" + _esc(title) + "</title><style>" + STYLE + "</style></head><body><main>" +
            "\n".join(doc.html) + "</main><script>" + SCRIPT + "</script></body></html>\n")


def write_report(result, directory):
    """Write detailed Markdown and HTML beside a run's retained evidence."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "report.md").write_text(render_markdown(result, directory), encoding="utf-8")
    (directory / "report.html").write_text(render_html(result, directory), encoding="utf-8")
