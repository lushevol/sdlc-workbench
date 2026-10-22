#!/usr/bin/env python3
"""Reconcile frozen canonical cases with retained browser attempts, without changing evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import re
import struct
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import quote


WORKSPACE = Path(__file__).resolve().parents[2]
STATUSES = ("PASS", "FAIL", "BLOCKED_NOT_EXECUTED")
WRITING_REVIEW = {
    "standard": "ASD-STE100",
    "automated_check": "PASSED",
    "asd_review": "PENDING",
    "reviewer": None,
    "reviewed_at": None,
    "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."],
}


def sha256(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def read(file: Path):
    return json.loads(file.read_text(encoding="utf-8"))


def resolve(value: str, workspace: Path) -> Path:
    """Resolve current relative paths and historical absolute workspace locators."""
    file = Path(value)
    if not file.is_absolute():
        return workspace / file
    if file.exists():
        return file
    for marker in ("tasks/", "e2e/"):
        if f"/{marker}" in value:
            return workspace / marker / value.split(f"/{marker}", 1)[1]
    return file


def reference(file: Path, workspace: Path) -> dict:
    return {"path": os.path.relpath(file, workspace), "sha256": sha256(file), "bytes": file.stat().st_size}


def href(file: Path, page: Path, fragment: str = "") -> str:
    return quote(os.path.relpath(file.resolve(), page.parent.resolve()).replace(os.sep, "/"), safe="/.") + fragment


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def link(file: Path, page: Path, label: str, fragment: str = "") -> str:
    return f'<a href="{esc(href(file, page, fragment))}">{esc(label)}</a>'


def save_json(file: Path, data) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def case_definitions(inventory: dict, rows: list[dict], workspace: Path) -> dict:
    source = next(item for item in inventory["inputs"] if item["path"].endswith("test-cases.md"))
    file = resolve(source["path"], workspace)
    if sha256(file) != source["sha256"]:
        raise ValueError("The canonical catalog differs from the frozen preflight. Use its exact retained version.")
    text = file.read_text(encoding="utf-8")
    result = {}
    for row in rows:
        case_id = row["caseId"]
        match = re.search(rf"^#### {re.escape(case_id)}\s*\n(.*?)(?=^#### |\Z)", text, re.M | re.S)
        if not match:
            raise ValueError(f"Missing canonical definition: {case_id}")
        title = re.search(r"^\*\*(.*?)\*\*", match[1], re.M)
        gherkin = re.search(r"```gherkin\n(.*?)```", match[1], re.S)
        result[case_id] = {"title": title[1] if title else case_id,
                           "gherkin": gherkin[1].strip() if gherkin else "",
                           "catalog": file}
    return result


def inspect_attempt(file: Path, run: dict, workspace: Path) -> dict:
    result = read(file)
    directory = file.parent
    manifest_file = directory / "artifact-manifest.json"
    manifest = read(manifest_file)
    for artifact in manifest["artifacts"]:
        retained = resolve(artifact["path"], workspace)
        if not retained.is_file() or sha256(retained) != artifact["sha256"]:
            raise ValueError(f"Artifact integrity failure: {retained}")
    frames_file = directory / "frames.json"
    frames = read(frames_file) if frames_file.exists() else None
    frame_records = []
    for frame in (frames or {}).get("frames", []):
        image = resolve(frame["path"], workspace)
        if sha256(image) != frame["sha256"]:
            raise ValueError(f"Screenshot integrity failure: {image}")
        png = image.read_bytes()
        if png[:8] != b"\x89PNG\r\n\x1a\n" or len(png) < 24:
            raise ValueError(f"Invalid PNG screenshot: {image}")
        width, height = struct.unpack(">II", png[16:24])
        frame_records.append({**frame, "path": os.path.relpath(image, workspace),
                              "width": width, "height": height})
    attachments = []
    for attachment in result.get("attachments", []):
        if attachment.get("retainedPath"):
            retained = resolve(attachment["retainedPath"], workspace)
            if not retained.is_file() or sha256(retained) != attachment["sha256"]:
                raise ValueError(f"Attachment integrity failure: {retained}")
            attachments.append({**attachment, "retainedPath": os.path.relpath(retained, workspace)})
    observed = "PASS" if result["actualStatus"] == "passed" and result.get("assertionsSatisfied") else (
        "BLOCKED_NOT_EXECUTED" if result["actualStatus"] in ("skipped", "interrupted") else "FAIL")
    scope = result["scope"]
    valid_scope = "SYNTHETIC_HARNESS" if run["category"] == "harness" else None
    if valid_scope and scope != valid_scope:
        raise ValueError(f"Harness run contains another scope: {file}")
    if run["category"] == "application" and scope == "SYNTHETIC_HARNESS":
        raise ValueError(f"Application run contains synthetic evidence: {file}")
    known_files = {"result.json", "started.json", "frames.json", "artifact-manifest.json"}
    observations = [reference(p, workspace) for p in sorted(directory.glob("*.json"))
                    if p.name not in known_files and not re.match(r"^\d{3}-", p.name)]
    return {"attemptId": f'{run["name"]}/{directory.name}', "run": run["name"],
            "caseId": result["caseId"], "testId": result["testId"], "title": result["title"],
            "source": result["source"], "startedAt": result["startedAt"], "endedAt": result["endedAt"],
            "scope": scope, "observedStatus": observed, "runnerStatus": result["actualStatus"],
            "assertionsSatisfied": result.get("assertionsSatisfied", False),
            "canonicalIdsMentioned": list(dict.fromkeys(result.get("canonicalIdsMentioned", []))),
            "mappingLimit": "Canonical IDs join records. Actual source assertions limit the supported local predicate.",
            "result": reference(file, workspace), "manifest": reference(manifest_file, workspace),
            "runInputs": run["inputs"], "frames": frame_records,
            "captureStatus": (frames or {}).get("captureStatus", "NOT_APPLICABLE" if (result.get("screenshotGap") or "").startswith("NOT_APPLICABLE") else "MISSING"),
            "captureGaps": (frames or {}).get("captureGaps", []),
            "fixture": (frames or {}).get("fixture") or next((item.get("description") for item in result.get("annotations", [])
                if item["type"] == "audit-fixture"), None),
            "attachments": attachments, "observations": observations,
            "errors": result.get("errors", []), "limits": result.get("limits", [])}


def load_runs(root: Path, workspace: Path) -> tuple[list[dict], list[dict], list[dict]]:
    runs, application, harness = [], [], []
    for category in ("application", "harness"):
        for directory in sorted((root / category).glob("run-*")):
            if not (directory / "run-inputs.json").exists():
                continue
            if not (directory / "run-result.json").exists():
                raise ValueError(f"The run has no final result: {directory}. Retain and finish it before reconciliation.")
            result = read(directory / "run-result.json")
            run = {"name": f"{category}/{directory.name}", "category": category,
                   "inputs": reference(directory / "run-inputs.json", workspace),
                   "result": reference(directory / "run-result.json", workspace),
                   "runnerStatus": result["runnerStatus"], "plannedTests": result["plannedTests"],
                   "completedTests": result["completedTests"], "statuses": result["statuses"],
                   "screenshotFrames": result["screenshotFrames"]}
            attempts = [inspect_attempt(file, run, workspace) for file in sorted((directory / "cases").glob("*/result.json"))]
            if len(attempts) != result["completedTests"]:
                raise ValueError(f"The run and retained case counts differ: {directory}")
            if sum(len(attempt["frames"]) for attempt in attempts) != result["screenshotFrames"]:
                raise ValueError(f"The run and retained frame counts differ: {directory}")
            (application if category == "application" else harness).extend(attempts)
            runs.append(run)
    return runs, application, harness


def reconcile(rows: list[dict], application: list[dict], harness: list[dict], definitions: dict) -> list[dict]:
    known = {row["caseId"] for row in rows}
    for attempt in application:
        unknown = set(attempt["canonicalIdsMentioned"]) - known
        if unknown or len(attempt["canonicalIdsMentioned"]) != 1:
            raise ValueError(f'Application attempt requires one known canonical ID: {attempt["attemptId"]}; unknown={unknown}')
    records = []
    for row in rows:
        case_id = row["caseId"]
        actual = sorted((attempt for attempt in application if case_id in attempt["canonicalIdsMentioned"]),
                        key=lambda attempt: (attempt["endedAt"], attempt["attemptId"]))
        latest = actual[-1] if actual else None
        reasons = list(row["reasonCodes"])
        if row["canonicalQualityStatus"] == "FAIL":
            status = "BLOCKED_NOT_EXECUTED"
            reasons.insert(0, "CANONICAL_QUALITY_FAIL_BLOCKS_ACCEPTANCE")
        elif latest:
            if latest["captureStatus"] != "CAPTURED" or latest["captureGaps"]:
                status = "BLOCKED_NOT_EXECUTED"
                reasons.insert(0, "ESSENTIAL_SCREENSHOT_EVIDENCE_INCOMPLETE")
            else:
                status = latest["observedStatus"]
        else:
            status = "BLOCKED_NOT_EXECUTED"
        records.append({"caseId": case_id, "title": definitions[case_id]["title"],
                        "definition": row["definition"], "definitionLine": row["definitionLine"],
                        "definitionVersion": row["definitionVersion"], "definitionSha256": row["definitionSha256"],
                        "localPredicateStatus": status, "latestObservedStatus": latest["observedStatus"] if latest else "NOT_RUN",
                        "canonicalFullScenarioStatus": "NOT_VERIFIED", "canonicalAcceptanceStatus": "NOT_ESTABLISHED",
                        "canonicalQualityStatus": row["canonicalQualityStatus"], "mappingStatusAtPreflight": row["mappingStatus"],
                        "assertionCount": row["assertionCount"], "uiAssertionCount": row["uiAssertionCount"],
                        "functionalAssertionCount": row["functionalAssertionCount"],
                        "reasonCodes": list(dict.fromkeys(reasons)), "preflightStatus": row["preflightStatus"],
                        "plannedEssentialFrames": row["requiredFrames"],
                        "latestAttempt": latest["attemptId"] if latest else None,
                        "actualApplicationAttempts": actual,
                        "relatedHarnessAttempts": [attempt["attemptId"] for attempt in harness if case_id in attempt["canonicalIdsMentioned"]],
                        "limits": ["Local predicate results use controlled service fixtures. They do not establish deployed business acceptance.",
                                   "Canonical step and screenshot-plan completeness require separate review."]})
    return records


CSS = """body{font:15px/1.5 system-ui,sans-serif;color:#18212d;margin:24px auto;padding:0 24px;max-width:1400px;background:#f7f9fc}a{color:#1354a4}h1,h2{line-height:1.2}.callout{border-left:5px solid #a66100;padding:12px 18px;background:#fff2d6}table{border-collapse:collapse;width:100%;background:white}th,td{padding:8px 12px;border-bottom:1px solid #d3d9e2;text-align:left;vertical-align:top}th{position:sticky;top:0;background:#e9eef6}.PASS{color:#14613b}.FAIL{color:#a21724}.BLOCKED_NOT_EXECUTED{color:#835000}.badge{font-weight:700;white-space:nowrap}input,select{font:inherit;padding:8px;margin:8px}article,details{padding:16px;margin:18px 0;background:white;border:1px solid #d3d9e2;border-radius:6px}.frames{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}figure{margin:0;border:1px solid #d3d9e2;padding:10px}img{max-width:100%;height:auto;background:#e9eef6}code,pre{font:13px/1.5 ui-monospace,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#eff3f8;padding:12px}small{font-size:12px}dt{font-weight:700}dd{margin:0 0 8px}footer{margin-top:30px;border-top:1px solid #d3d9e2;padding-top:18px}.muted{color:#526075}summary{cursor:pointer;font-weight:700}"""


def page(title: str, content: str) -> str:
    return (f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title><style>{CSS}</style><body>{content}'
            '<footer><details><summary>Writing review</summary>'
            f'<pre>{esc(json.dumps(WRITING_REVIEW, indent=2))}</pre></details></footer></body></html>')


def attempt_html(attempt: dict, target: Path, workspace: Path) -> str:
    result_file = resolve(attempt["result"]["path"], workspace)
    body = (f'<article><h3>{esc(attempt["title"])}</h3><p><span class="badge {attempt["observedStatus"]}">{attempt["observedStatus"]}</span>'
            f' · {esc(attempt["attemptId"])} · {esc(attempt["scope"])}</p>'
            f'<p>{esc(attempt["fixture"])}</p><p>{esc(attempt["startedAt"])} to {esc(attempt["endedAt"])}</p>'
            f'<p>{link(result_file, target, "Assertions and result")} · '
            f'{link(resolve(attempt["manifest"]["path"], workspace), target, "Artifact manifest")} · '
            f'{link(resolve(attempt["runInputs"]["path"], workspace), target, "Exact run inputs and source hashes")}</p>'
            f'<small>Result SHA-256: <code>{attempt["result"]["sha256"]}</code></small>')
    if attempt["errors"]:
        body += f'<details open><summary>Retained failure details</summary><pre>{esc(json.dumps(attempt["errors"], indent=2))}</pre></details>'
    traces = [a for a in attempt["attachments"] if a["contentType"] == "application/zip"]
    body += '<p>' + ' · '.join(link(resolve(a["retainedPath"], workspace), target, "Playwright trace") for a in traces) + '</p>'
    if attempt["observations"]:
        body += '<details><summary>Machine observations</summary><ul>' + ''.join(
            f'<li>{link(resolve(item["path"], workspace), target, Path(item["path"]).name)} '
            f'<code>{item["sha256"]}</code></li>' for item in attempt["observations"]) + '</ul></details>'
    body += f'<p>Screenshot capture: {esc(attempt["captureStatus"])}. Named frames: {len(attempt["frames"])}.</p><div class="frames">'
    for frame in attempt["frames"]:
        image = resolve(frame["path"], workspace)
        body += (f'<figure><a href="{esc(href(image, target))}"><img loading="lazy" src="{esc(href(image, target))}" '
                 f'alt="{esc(frame["phase"])}: {esc(frame["claim"])}"></a><figcaption>'
                 f'<strong>{frame["sequence"]}. {esc(frame["phase"])}</strong><p>{esc(frame["claim"])}</p>'
                 f'<small>{esc(frame["capturedAt"])} · {frame["width"]}×{frame["height"]}<br>'
                 f'Step: {esc(frame["step"])}<br>SHA-256: <code>{frame["sha256"]}</code></small></figcaption></figure>')
    return body + '</div><p class="muted">Screenshots establish visible state only. Assertions and traces support functional claims.</p></article>'


def render(output: Path, payload: dict, definitions: dict, workspace: Path) -> None:
    records = payload["cases"]
    (output / "cases").mkdir()
    (output / "harness").mkdir()
    for record in records:
        target = output / "cases" / f'{record["caseId"]}.html'
        definition = definitions[record["caseId"]]
        body = (f'<p>{link(output / "index.html", target, "All canonical cases")}</p>'
                f'<h1>{esc(record["caseId"])}: {esc(record["title"])}</h1>'
                '<p class="callout"><strong>Business acceptance remains unverified. Owner: unknown. '
                'Review the canonical definition and fixture limits before acceptance.</strong></p>'
                f'<p>Local predicate: <span class="badge {record["localPredicateStatus"]}">{record["localPredicateStatus"]}</span>. '
                f'Canonical quality: {esc(record["canonicalQualityStatus"])}.</p>'
                f'<p>{link(definition["catalog"], target, "Canonical Gherkin definition", "#" + record["caseId"].lower())}. '
                f'Definition version: {record["definitionVersion"]}. SHA-256: <code>{record["definitionSha256"]}</code>.</p>'
                f'<details><summary>Canonical Gherkin steps</summary><pre>{esc(definition["gherkin"])}</pre></details>'
                f'<p>Preflight reasons: {esc(", ".join(record["reasonCodes"]))}.</p>'
                f'<p>Planned essential canonical frames: {len(record["plannedEssentialFrames"])}. '
                'Plan completeness requires separate review.</p>')
        body += ''.join(attempt_html(attempt, target, workspace) for attempt in record["actualApplicationAttempts"])
        if not record["actualApplicationAttempts"]:
            body += '<p>No actual application attempt was retained. No screenshot is claimed.</p>'
        if record["relatedHarnessAttempts"]:
            body += '<p>Related synthetic checks: ' + ', '.join(link(output / "harness" / (attempt.replace("/", "--") + ".html"),
                target, attempt) for attempt in record["relatedHarnessAttempts"]) + '.</p>'
        target.write_text(page(record["caseId"], body), encoding="utf-8")
    for attempt in payload["harnessAttempts"]:
        target = output / "harness" / (attempt["attemptId"].replace("/", "--") + ".html")
        body = (f'<p>{link(output / "index.html", target, "Audit ledger")}</p><h1>Synthetic harness evidence</h1>'
                '<p class="callout"><strong>This check does not execute the actual MFE, BFF, or canonical business scenario.</strong></p>'
                + attempt_html(attempt, target, workspace))
        target.write_text(page(attempt["title"], body), encoding="utf-8")
    target = output / "index.html"
    summary = payload["summary"]
    body = ('<h1>UI audit results and screenshots</h1>'
            '<p class="callout"><strong>Business acceptance remains unverified. Owner: unknown. '
            'Review blocked cases and controlled service limits before acceptance.</strong></p>'
            f'<p>{summary["canonicalCases"]} canonical cases appear once. '
            f'Actual application attempts: {summary["applicationAttempts"]}. '
            f'Synthetic harness attempts: {summary["harnessAttempts"]}.</p>'
            '<p>PASS and FAIL describe local browser predicates. They do not establish full canonical or deployed business acceptance.</p>'
            f'<p>{link(output / "case-results.json", target, "Complete JSON ledger")} · '
            f'{link(output / "case-results.csv", target, "Canonical CSV ledger")} · '
            f'{link(output / "audit-summary.json", target, "Run and integrity summary")}</p>'
            f'<pre>{esc(json.dumps(summary, indent=2))}</pre>'
            '<label>Search <input id="search" type="search" placeholder="Case ID or title"></label>'
            '<label>Local result <select id="status"><option value="">All</option>'
            + ''.join(f'<option>{status}</option>' for status in STATUSES) + '</select></label>'
            '<p id="visible"></p><table><thead><tr><th>Case</th><th>Local predicate</th><th>Canonical quality</th>'
            '<th>Actual attempts</th><th>Retained frames</th></tr></thead><tbody>')
    for record in records:
        count = sum(len(attempt["frames"]) for attempt in record["actualApplicationAttempts"])
        body += (f'<tr data-status="{record["localPredicateStatus"]}"><td>'
                 f'{link(output / "cases" / (record["caseId"] + ".html"), target, record["caseId"] + ": " + record["title"])}'
                 f'</td><td class="badge {record["localPredicateStatus"]}">{record["localPredicateStatus"]}</td>'
                 f'<td>{esc(record["canonicalQualityStatus"])}</td><td>{len(record["actualApplicationAttempts"])}</td><td>{count}</td></tr>')
    body += '</tbody></table><h2>Synthetic harness checks</h2><ul>'
    for attempt in payload["harnessAttempts"]:
        body += '<li>' + link(output / "harness" / (attempt["attemptId"].replace("/", "--") + ".html"), target,
                            attempt["title"]) + f' — {attempt["observedStatus"]}, {len(attempt["frames"])} named frames.</li>'
    body += ('</ul><script>const rows=[...document.querySelectorAll("tbody tr")];function filter(){'
             'const q=document.getElementById("search").value.toLowerCase();const s=document.getElementById("status").value;'
             'let count=0;for(const row of rows){const show=(!s||row.dataset.status===s)&&row.textContent.toLowerCase().includes(q);'
             'row.hidden=!show;if(show)count++;}document.getElementById("visible").textContent=`${count} canonical cases shown`;}'
             'document.getElementById("search").addEventListener("input",filter);document.getElementById("status").addEventListener("change",filter);filter();</script>')
    target.write_text(page("UI audit ledger", body), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-root", type=Path, required=True, help="Directory containing inventory, application, and harness records.")
    parser.add_argument("--output", type=Path, required=True, help="New report directory; existing files are never overwritten.")
    parser.add_argument("--workspace", type=Path, default=WORKSPACE)
    args = parser.parse_args()
    workspace, root, output = args.workspace.resolve(), args.audit_root.resolve(), args.output.resolve()
    if output.exists():
        raise ValueError("Choose a new report directory. Existing audit reports are never overwritten.")
    if output == root / "inventory" or root / "inventory" in output.parents:
        raise ValueError("The frozen preflight inventory cannot contain generated reconciliation outputs.")
    inventory_file = root / "inventory" / "summary.json"
    inventory = read(inventory_file)
    preflight_file = resolve(inventory["caseRecords"]["path"], workspace)
    if sha256(preflight_file) != inventory["caseRecords"]["sha256"]:
        raise ValueError("The frozen preflight case hash differs.")
    rows = [json.loads(line) for line in preflight_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != inventory["summary"]["cases"] or len({row["caseId"] for row in rows}) != len(rows):
        raise ValueError("The frozen inventory count or uniqueness check failed.")
    definitions = case_definitions(inventory, rows, workspace)
    runs, application, harness = load_runs(root, workspace)
    records = reconcile(rows, application, harness, definitions)
    if len(records) != len(rows) or len({row["caseId"] for row in records}) != len(rows):
        raise ValueError("Canonical reconciliation is incomplete or contains duplicate cases.")
    quality_blocked = sum(row["canonicalQualityStatus"] == "FAIL" for row in rows)
    summary = {"canonicalCases": len(records), "localPredicateStatus": dict(Counter(row["localPredicateStatus"] for row in records)),
               "canonicalAcceptanceEstablished": 0, "qualityBlockedCases": quality_blocked,
               "actualApplicationCasesObserved": len({case for attempt in application for case in attempt["canonicalIdsMentioned"]}),
               "applicationAttempts": len(application), "applicationAttemptStatus": dict(Counter(a["observedStatus"] for a in application)),
               "applicationScreenshotFrames": sum(len(a["frames"]) for a in application),
               "harnessAttempts": len(harness), "harnessAttemptStatus": dict(Counter(a["observedStatus"] for a in harness)),
               "harnessScreenshotFrames": sum(len(a["frames"]) for a in harness),
               "integrityCheck": "PASSED", "canonicalCaseUniquenessCheck": "PASSED"}
    payload = {"schemaVersion": 1, "generatedAt": datetime.now(timezone.utc).isoformat(),
               "generator": reference(Path(__file__), workspace), "frozenInventory": reference(inventory_file, workspace),
               "frozenCaseRecords": reference(preflight_file, workspace), "summary": summary, "runs": runs,
               "statusDefinitions": {"PASS": "The latest retained actual application attempt passed its local predicates with named screenshots.",
                   "FAIL": "The latest retained actual application attempt failed. The retained error limits the cause claim.",
                   "BLOCKED_NOT_EXECUTED": "No usable actual attempt exists, screenshot evidence is incomplete, or canonical quality blocks acceptance."},
               "limits": ["Synthetic checks never change canonical results.",
                   "Local predicates use controlled service fixtures. No deployed identity, BFF, or full business acceptance is established.",
                   "All attempts remain available. The latest completed actual attempt determines the local predicate status.",
                   "Canonical quality failures remain blocked even when a local probe passes.",
                   "Screenshot-plan completeness and canonical assertion coverage require separate review."],
               "cases": records, "harnessAttempts": harness, "writing_review": WRITING_REVIEW}
    output.mkdir(parents=True)
    save_json(output / "case-results.json", payload)
    save_json(output / "audit-summary.json", {key: value for key, value in payload.items() if key not in ("cases", "harnessAttempts")})
    fields = ["caseId", "title", "localPredicateStatus", "latestObservedStatus", "canonicalFullScenarioStatus", "canonicalAcceptanceStatus",
              "canonicalQualityStatus", "mappingStatusAtPreflight", "definition", "definitionVersion", "definitionSha256", "latestAttempt",
              "applicationAttempts", "screenshotFrames", "reasonCodes", "gallery"]
    with (output / "case-results.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in records:
            values = {field: row[field] for field in fields if field in row}
            values.update(applicationAttempts=len(row["actualApplicationAttempts"]),
                          screenshotFrames=sum(len(a["frames"]) for a in row["actualApplicationAttempts"]),
                          reasonCodes=";".join(row["reasonCodes"]), gallery=f'cases/{row["caseId"]}.html')
            writer.writerow(values)
    render(output, payload, definitions, workspace)
    save_json(output / "report-manifest.json", {"generatedAt": payload["generatedAt"],
        "artifacts": [reference(file, workspace) for file in sorted(output.rglob("*")) if file.is_file()]})
    print(json.dumps({"output": str(output), **summary}, indent=2))


if __name__ == "__main__":
    main()
