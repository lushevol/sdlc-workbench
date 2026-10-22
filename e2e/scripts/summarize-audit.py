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
STATUSES = ("PASS", "FAIL", "BLOCKED_NOT_EXECUTED", "SKIPPED_BY_USER")
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


def frame_context(frames: list[dict]) -> list[dict]:
    """Identify identical retained image bytes without inferring a visual or functional defect."""
    last_by_image_and_page = {}
    result = []
    for frame in frames:
        image_hash = frame.get("sha256")
        identity = (image_hash, frame.get("targetPageLabel"))
        previous = last_by_image_and_page.get(identity) if image_hash else None
        result.append({**frame, "sameImageAsSequence": frame.get("sameImageAsSequence", previous)})
        if image_hash:
            last_by_image_and_page[identity] = frame["sequence"]
    return result


def screenshot_content_evidence(attempt: dict | None) -> dict:
    """Keep recorded machine context separate from human review of screenshot relevance."""
    frames = frame_context(attempt.get("frames", [])) if attempt else []
    contextual = sum(any(isinstance(frame.get(key), dict) and bool(frame[key])
                         for key in ("observationsBefore", "observationsAfter")) for frame in frames)
    return {"screenshotContentReviewStatus": "CONTEXT_RECORDED" if contextual else "NOT_REVIEWED",
            "framesWithRecordedContext": contextual,
            "duplicateFrames": len(frames) - len({(frame.get("sha256"), frame.get("targetPageLabel")) for frame in frames})}


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
                           "catalog": file,
                           "catalogSha256": source["sha256"],
                           "steps": [{"number": number, "keyword": step[1], "text": step[2],
                                      "line": text[:match.start(1) + gherkin.start(1) + step.start()].count("\n") + 1}
                                     for number, step in enumerate(re.finditer(
                                         r"^[ \t]*(Given|When|Then|And|But)[ \t]+(.+)$", gherkin[1] if gherkin else "", re.M), 1)]}
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
    if run["category"] == "harness" and scope != "SYNTHETIC_HARNESS":
        raise ValueError(f"Harness run contains another scope: {file}")
    evidence_category = ("HISTORICAL_DECLARED_SYNTHETIC" if run["category"] == "application" and scope == "SYNTHETIC_HARNESS"
                         else "SYNTHETIC_HARNESS" if run["category"] == "harness" else "ACTUAL_APPLICATION")
    classification_limits = (["The original application path conflicts with the declared synthetic scope. "
                              "Retained traces can contain application activity. This report does not upgrade the declared scope. "
                              "This historical attempt cannot select the canonical local result."]
                             if evidence_category == "HISTORICAL_DECLARED_SYNTHETIC" else [])
    known_files = {"result.json", "started.json", "frames.json", "artifact-manifest.json"}
    observations = [reference(p, workspace) for p in sorted(directory.glob("*.json"))
                    if p.name not in known_files and not re.match(r"^\d{3}-", p.name)]
    blocker_file = directory / "execution-blocker.json"
    blockers = [read(blocker_file).get("observations", {})] if blocker_file.is_file() else []
    return {"attemptId": f'{run["name"]}/{directory.name}', "run": run["name"],
            "caseId": result["caseId"], "testId": result["testId"], "title": result["title"],
            "source": result["source"], "startedAt": result["startedAt"], "endedAt": result["endedAt"],
            "scope": scope, "pathCategory": run["category"], "evidenceCategory": evidence_category,
            "classificationLimits": classification_limits,
            "observedStatus": observed, "runnerStatus": result["actualStatus"],
            "assertionsSatisfied": result.get("assertionsSatisfied", False),
            "canonicalIdsMentioned": list(dict.fromkeys(result.get("canonicalIdsMentioned", []))),
            "mappingLimit": "Canonical IDs join records. Actual source assertions limit the supported local predicate.",
            "result": reference(file, workspace), "manifest": reference(manifest_file, workspace),
            "runInputs": run["inputs"], "frames": frame_context(frame_records),
            "canonical": (frames or {}).get("canonical"),
            "steps": (frames or {}).get("steps") or ((frames or {}).get("canonical") or {}).get("steps", []),
            "captureStatus": (frames or {}).get("captureStatus", "NOT_APPLICABLE" if (result.get("screenshotGap") or "").startswith("NOT_APPLICABLE") else "MISSING"),
            "captureGaps": (frames or {}).get("captureGaps", []),
            "fixture": (frames or {}).get("fixture") or next((item.get("description") for item in result.get("annotations", [])
                if item["type"] == "audit-fixture"), None),
            "attachments": attachments, "observations": observations, "executionBlockers": blockers,
            "errors": result.get("errors", []), "limits": result.get("limits", [])}


def step_evidence(attempt: dict | None, definition: dict, row: dict) -> dict:
    """Check exact canonical bindings before claiming complete screenshot coverage."""
    expected = definition["steps"]
    count = len(expected)
    gaps = []
    canonical = attempt.get("canonical") if attempt else None
    actual_steps = attempt.get("steps", []) if attempt else []
    if not canonical or not actual_steps:
        return {"stepEvidenceStatus": "LEGACY_ESSENTIAL_FRAMES" if attempt else "NOT_RECORDED", "completeStepEvidence": False,
                "canonicalStepCount": count, "stepsWithScreenshots": 0,
                "stepEvidenceGaps": ["Step evidence not recorded."],
                "stepTimeline": [{**step, "status": "NOT_RECORDED", "frameSequences": []} for step in expected]}
    if canonical.get("caseId") != row["caseId"]:
        gaps.append("The recorded canonical case ID differs from the selected case.")
    canonical_steps = canonical.get("steps", [])
    identity = lambda step: (step.get("number"), step.get("keyword"), step.get("text"), step.get("line"))
    if [identity(step) for step in canonical_steps] != [identity(step) for step in expected]:
        gaps.append("The recorded canonical steps differ from the frozen definition.")
    if canonical.get("sha256") != definition["catalogSha256"]:
        gaps.append("The recorded canonical catalog hash differs from the frozen catalog.")
    if count != row.get("totalSteps", count):
        gaps.append("The parsed canonical step count differs from the frozen inventory.")
    frames = attempt["frames"]
    frame_by_sequence = {frame["sequence"]: frame for frame in frames}
    if len(frame_by_sequence) != len(frames):
        gaps.append("The retained screenshots contain duplicate frame sequences.")
    numbers = [step.get("number") for step in actual_steps]
    if len(numbers) != len(set(numbers)) or set(numbers) != {step["number"] for step in expected}:
        gaps.append("The recorded step numbers do not match the canonical step numbers.")
    timeline = []
    covered = 0
    for expected_step in expected:
        matches = [step for step in actual_steps if step.get("number") == expected_step["number"]]
        actual = matches[0] if len(matches) == 1 else {}
        number = expected_step["number"]
        exact_step = bool(actual) and identity(actual) == identity(expected_step)
        if actual and not exact_step:
            gaps.append(f"Step {number} text differs from the canonical definition.")
        status = actual.get("status", "NOT_RECORDED")
        completed = status in ("PASSED", "FAILED")
        interval = None
        if completed:
            try:
                interval = tuple(datetime.fromisoformat(actual[key].replace("Z", "+00:00"))
                                 for key in ("startedAt", "endedAt"))
                if interval[0] > interval[1]:
                    raise ValueError("Reversed step times")
            except (KeyError, TypeError, ValueError):
                interval = None
                gaps.append(f"Step {number} has no valid execution interval.")
        sequences = actual.get("frameSequences", [])
        valid = []
        for sequence in sequences:
            frame = frame_by_sequence.get(sequence)
            if not frame or frame.get("canonicalStep", frame.get("stepNumber")) != number:
                gaps.append(f"Step {number} references a missing or differently bound screenshot.")
            elif completed and exact_step and interval:
                try:
                    captured = datetime.fromisoformat(frame["capturedAt"].replace("Z", "+00:00"))
                    in_interval = interval[0] <= captured <= interval[1]
                except (KeyError, TypeError, ValueError):
                    in_interval = False
                if not in_interval:
                    gaps.append(f"Step {number} screenshot time is outside its execution interval.")
                elif sequence not in valid:
                    valid.append(sequence)
        if status not in ("PENDING", "RUNNING", "PASSED", "FAILED", "NOT_EXECUTED"):
            gaps.append(f"Step {number} has no recognized execution result.")
        if completed and valid:
            covered += 1
        else:
            gaps.append(f"Step {number} has no screenshot from an executed step.")
        timeline.append({**actual, **expected_step, "status": status, "frameSequences": valid})
    complete = bool(count) and covered == count and not gaps
    return {"stepEvidenceStatus": "COMPLETE" if complete else "INCOMPLETE", "completeStepEvidence": complete,
            "canonicalStepCount": count, "stepsWithScreenshots": covered,
            "stepEvidenceGaps": list(dict.fromkeys(gaps)), "stepTimeline": timeline}


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
            application.extend(attempt for attempt in attempts if attempt["evidenceCategory"] == "ACTUAL_APPLICATION")
            harness.extend(attempt for attempt in attempts if attempt["evidenceCategory"] != "ACTUAL_APPLICATION")
            runs.append(run)
    return runs, application, harness


def reconcile(rows: list[dict], application: list[dict], harness: list[dict], definitions: dict,
              exclusions: dict[str, dict] | None = None) -> list[dict]:
    exclusions = exclusions or {}
    known = {row["caseId"] for row in rows}
    if set(exclusions) - known:
        raise ValueError("Scope exclusions contain unknown canonical IDs.")
    for attempt in application:
        unknown = set(attempt["canonicalIdsMentioned"]) - known
        if unknown or len(attempt["canonicalIdsMentioned"]) != 1:
            raise ValueError(f'Application attempt requires one known canonical ID: {attempt["attemptId"]}; unknown={unknown}')
    records = []
    for row in rows:
        case_id = row["caseId"]
        actual = sorted(({**attempt, "frames": frame_context(attempt["frames"]),
                          **step_evidence(attempt, definitions[case_id], row), **screenshot_content_evidence(attempt)}
                         for attempt in application if case_id in attempt["canonicalIdsMentioned"]),
                        key=lambda attempt: (attempt["endedAt"], attempt["attemptId"]), reverse=True)
        latest = actual[0] if actual else None
        coverage = {key: value for key, value in (latest or step_evidence(None, definitions[case_id], row)).items()
                    if key in ("stepEvidenceStatus", "completeStepEvidence", "canonicalStepCount", "stepsWithScreenshots", "stepEvidenceGaps")}
        reasons = list(row["reasonCodes"])
        reasons[:0] = [blocker["code"] for blocker in (latest or {}).get("executionBlockers", []) if blocker.get("code")]
        if row["canonicalQualityStatus"] == "FAIL":
            reasons.insert(0, "CANONICAL_QUALITY_FAIL_BLOCKS_ACCEPTANCE")
        if latest:
            status = latest["observedStatus"]
            if latest["captureStatus"] != "CAPTURED" or latest["captureGaps"]:
                reasons.insert(0, "ESSENTIAL_SCREENSHOT_EVIDENCE_INCOMPLETE")
        else:
            status = "BLOCKED_NOT_EXECUTED"
        excluded = exclusions.get(case_id)
        if excluded:
            status = "SKIPPED_BY_USER"
            reasons.insert(0, "USER_SCOPE_EXCLUSION")
        records.append({"caseId": case_id, "title": definitions[case_id]["title"],
                        "definition": row["definition"], "definitionLine": row["definitionLine"],
                        "definitionVersion": row["definitionVersion"], "definitionSha256": row["definitionSha256"],
                        "localPredicateStatus": status, "latestObservedStatus": latest["observedStatus"] if latest else "NOT_RUN",
                        "scopeStatus": "EXCLUDED_BY_USER" if excluded else "IN_SCOPE", "scopeExclusion": excluded,
                        "canonicalFullScenarioStatus": "NOT_VERIFIED", "canonicalAcceptanceStatus": "NOT_ESTABLISHED",
                        "canonicalQualityStatus": row["canonicalQualityStatus"], "mappingStatusAtPreflight": row["mappingStatus"],
                        "assertionCount": row["assertionCount"], "uiAssertionCount": row["uiAssertionCount"],
                        "functionalAssertionCount": row["functionalAssertionCount"],
                        "reasonCodes": list(dict.fromkeys(reasons)), "preflightStatus": row["preflightStatus"],
                        "plannedEssentialFrames": row["requiredFrames"],
                        "latestAttempt": latest["attemptId"] if latest else None,
                        **coverage,
                        **screenshot_content_evidence(latest),
                        "actualApplicationAttempts": actual,
                        "relatedHarnessAttempts": [attempt["attemptId"] for attempt in harness if case_id in attempt["canonicalIdsMentioned"]],
                        "limits": ["Each attempt records its implementation, fixture boundaries, and source hashes. Local execution does not establish deployed business acceptance.",
                                   "Canonical step and screenshot-plan completeness require separate review."]})
    return records


CSS = """body{font:15px/1.5 system-ui,sans-serif;color:#18212d;margin:24px auto;padding:0 24px;max-width:1400px;background:#f7f9fc}a{color:#1354a4}h1,h2{line-height:1.2}.callout{border-left:5px solid #a66100;padding:12px 18px;background:#fff2d6}table{border-collapse:collapse;width:100%;background:white}th,td{padding:8px 12px;border-bottom:1px solid #d3d9e2;text-align:left;vertical-align:top}th{position:sticky;top:0;background:#e9eef6}.PASS{color:#14613b}.FAIL{color:#a21724}.BLOCKED_NOT_EXECUTED{color:#835000}.badge{font-weight:700;white-space:nowrap}input,select{font:inherit;padding:8px;margin:8px}article,details{padding:16px;margin:18px 0;background:white;border:1px solid #d3d9e2;border-radius:6px}.frames{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}figure{margin:0;border:1px solid #d3d9e2;padding:10px}img{max-width:100%;height:auto;background:#e9eef6}code,pre{font:13px/1.5 ui-monospace,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#eff3f8;padding:12px}small{font-size:12px}dt{font-weight:700}dd{margin:0 0 8px}footer{margin-top:30px;border-top:1px solid #d3d9e2;padding-top:18px}.muted{color:#526075}summary{cursor:pointer;font-weight:700}"""


def page(title: str, content: str) -> str:
    return (f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title><style>{CSS}</style><body>{content}'
            '<footer><details><summary>Writing review</summary>'
            f'<pre>{esc(json.dumps(WRITING_REVIEW, indent=2))}</pre></details></footer></body></html>')


def frame_html(frame: dict, target: Path, workspace: Path) -> str:
    image = resolve(frame["path"], workspace)
    context = ""
    if frame.get("targetPageLabel"):
        context += f'<p>Captured page: <strong>{esc(frame["targetPageLabel"])}</strong>.</p>'
    if frame.get("sameImageAsSequence") is not None:
        context += (f'<p class="muted">Image bytes match frame {esc(frame["sameImageAsSequence"])}. '
                    'An unchanged image can be valid for consecutive assertions. '
                    'This match does not establish correct step content.</p>')
    observations = {key: frame[key] for key in ("observationsBefore", "observationsAfter") if key in frame}
    if observations:
        snapshot = observations.get("observationsAfter") or observations.get("observationsBefore") or {}
        session = snapshot.get("session") if isinstance(snapshot, dict) else None
        if isinstance(session, dict):
            parts = []
            clock = session.get("clock")
            if isinstance(clock, dict) and clock.get("mode") == "PLAYWRIGHT_CONTROLLED":
                elapsed = clock.get("elapsedMs")
                if type(elapsed) in (int, float):
                    parts.append(f'Controlled time T{elapsed / 1000:+.3f}s ({elapsed:g} ms)')
                remaining = clock.get("cutoffRemainingMs")
                if type(remaining) in (int, float):
                    parts.append(f'cutoff remaining {remaining:g} ms')
            ui = session.get("ui")
            if isinstance(ui, dict):
                if ui.get("extendVisible") is False:
                    parts.append("Extend absent")
                elif type(ui.get("extendEnabled")) is bool:
                    parts.append("Extend enabled" if ui["extendEnabled"] else "Extend disabled")
                if type(ui.get("dialogVisible")) is bool:
                    parts.append("dialog visible" if ui["dialogVisible"] else "dialog absent")
            label = session.get("pageLabel") or frame.get("targetPageLabel")
            if label:
                parts.append(f'page {label}')
            if parts:
                context += ('<p class="capture-context"><strong>Audit metadata — separate from application UI:</strong> '
                            + esc("; ".join(parts)) + '.</p>')
        context += ('<details class="capture-observations"><summary>Capture observations — separate from application UI</summary>'
                    '<p>These values come from the audit harness. They are not pixels or labels added to the application image.</p>'
                    f'<pre>{esc(json.dumps(observations, indent=2, ensure_ascii=False))}</pre></details>')
    return (f'<figure><a href="{esc(href(image, target))}"><img loading="lazy" src="{esc(href(image, target))}" '
            f'alt="{esc(frame["phase"])}: {esc(frame["claim"])}"></a><figcaption>'
            f'<strong>{frame["sequence"]}. {esc(frame["phase"])}</strong><p>{esc(frame["claim"])}</p>'
            f'<small>{esc(frame["capturedAt"])} · {frame["width"]}×{frame["height"]}<br>'
            f'Step: {esc(frame["step"])}<br>SHA-256: <code>{esc(frame["sha256"])}</code></small>{context}</figcaption></figure>')


def attempt_html(attempt: dict, target: Path, workspace: Path, *, historical: bool = False) -> str:
    result_file = resolve(attempt["result"]["path"], workspace)
    body = (f'<article><h3>{esc(attempt["title"])}</h3><p><span class="badge {attempt["observedStatus"]}">{attempt["observedStatus"]}</span>'
            f' · {esc(attempt["attemptId"])} · {esc(attempt["scope"])}</p>'
            f'<p>{esc(attempt["fixture"])}</p><p>{esc(attempt["startedAt"])} to {esc(attempt["endedAt"])}</p>'
            f'<p>{link(result_file, target, "Assertions and result")} · '
            f'{link(resolve(attempt["manifest"]["path"], workspace), target, "Artifact manifest")} · '
            f'{link(resolve(attempt["runInputs"]["path"], workspace), target, "Exact run inputs and source hashes")}</p>'
            f'<small>Result SHA-256: <code>{attempt["result"]["sha256"]}</code></small>')
    if attempt["errors"]:
        body += f'<details{"" if historical else " open"}><summary>Retained failure details</summary><pre>{esc(json.dumps(attempt["errors"], indent=2))}</pre></details>'
    for limit in attempt.get("classificationLimits", []):
        body += f'<p class="callout">{esc(limit)}</p>'
    for blocker in attempt.get("executionBlockers", []):
        body += (f'<p class="callout"><strong>Execution prerequisite: {esc(blocker.get("code", "UNKNOWN"))}.</strong> '
                 f'{esc(blocker.get("consequence", ""))} Owner: {esc(blocker.get("owner", "Unknown"))}. '
                 f'Next action: {esc(blocker.get("nextAction", "Resolve the retained prerequisite."))}</p>')
    traces = [a for a in attempt["attachments"] if a["contentType"] == "application/zip"]
    body += '<p>' + ' · '.join(link(resolve(a["retainedPath"], workspace), target, "Playwright trace") for a in traces) + '</p>'
    if attempt["observations"]:
        body += '<details><summary>Machine observations</summary><ul>' + ''.join(
            f'<li>{link(resolve(item["path"], workspace), target, Path(item["path"]).name)} '
            f'<code>{item["sha256"]}</code></li>' for item in attempt["observations"]) + '</ul></details>'
    body += f'<p>Screenshot capture: {esc(attempt["captureStatus"])}. Named frames: {len(attempt["frames"])}.</p>'
    if "stepTimeline" in attempt:
        body += (f'<p><strong>Step screenshot bindings: {esc(attempt["stepEvidenceStatus"])}.</strong> '
                 f'{attempt["stepsWithScreenshots"]}/{attempt["canonicalStepCount"]} canonical steps have execution screenshots.</p>'
                 '<p>Bindings measure structural coverage only. They do not establish screenshot content quality or relevance.</p>')
        content = screenshot_content_evidence(attempt)
        body += (f'<p>Screenshot content review: <strong>{esc(content["screenshotContentReviewStatus"])}</strong>. '
                 f'Recorded context: {content["framesWithRecordedContext"]}/{len(attempt["frames"])} frames. '
                 f'Identical image bytes: {content["duplicateFrames"]} repeated frames. '
                 'Recorded context does not establish human visual review.</p>')
        if attempt["stepEvidenceGaps"]:
            body += '<p class="callout">' + ' '.join(esc(gap) for gap in attempt["stepEvidenceGaps"]) + '</p>'
        body += '<h4>Canonical step timeline</h4><ol class="step-timeline">'
        frame_by_sequence = {frame["sequence"]: frame for frame in attempt["frames"]}
        displayed = set()
        for step in attempt["stepTimeline"]:
            body += (f'<li value="{step["number"]}" data-step="{step["number"]}"><p><strong>'
                     f'{esc(step["keyword"])} {esc(step["text"])}</strong><br>'
                     f'Execution: {esc(step["status"])}.</p>')
            step_frames = [frame_by_sequence[sequence] for sequence in step["frameSequences"]]
            if step_frames:
                body += '<div class="frames">' + ''.join(frame_html(frame, target, workspace) for frame in step_frames) + '</div>'
                displayed.update(step["frameSequences"])
            else:
                body += '<p class="muted">No screenshot is recorded for this step. No executed state is claimed.</p>'
            body += '</li>'
        body += '</ol>'
        remaining = [frame for frame in attempt["frames"] if frame["sequence"] not in displayed]
        if remaining:
            body += '<details><summary>Additional named frames</summary><div class="frames">'
            body += ''.join(frame_html(frame, target, workspace) for frame in remaining) + '</div></details>'
    else:
        body += '<div class="frames">' + ''.join(frame_html(frame, target, workspace) for frame in attempt["frames"]) + '</div>'
    return body + '<p class="muted">Screenshots establish visible state only. Assertions and traces support functional claims.</p></article>'


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
                f'<h2>Latest local result: <span class="badge {record["localPredicateStatus"]}">{record["localPredicateStatus"]}</span></h2>'
                f'<p>Business acceptance: {esc(record["canonicalAcceptanceStatus"])}.</p>'
                '<p>The latest local result describes execution. The historical definition review assesses the case design before execution.</p>'
                f'<p>Latest step screenshot bindings: <strong>{esc(record["stepEvidenceStatus"])}</strong>. '
                f'{record["stepsWithScreenshots"]}/{record["canonicalStepCount"]} canonical steps have execution screenshots.</p>'
                '<p>Bindings measure structural coverage only. They do not establish screenshot content quality or relevance.</p>'
                f'<p>Screenshot content review: <strong>{esc(record.get("screenshotContentReviewStatus", "NOT_REVIEWED"))}</strong>. '
                'Recorded context does not establish human visual review.</p>'
                f'<p>{link(definition["catalog"], target, "Canonical Gherkin definition", "#" + record["caseId"].lower())}. '
                f'Definition version: {record["definitionVersion"]}. SHA-256: <code>{record["definitionSha256"]}</code>.</p>'
                f'<details class="definition-review"><summary>Historical definition review (preflight): {esc(record["canonicalQualityStatus"])}</summary>'
                '<p>A definition review FAIL can coexist with local PASS. The definition failed preflight quality checks.</p>'
                '<p>This historical review does not change the latest execution result. Resolve definition gaps before business acceptance.</p></details>'
                f'<details><summary>Canonical Gherkin steps</summary><pre>{esc(definition["gherkin"])}</pre></details>'
                f'<p>Acceptance and evidence limits: {esc(", ".join(record["reasonCodes"]))}.</p>'
                f'<p>Planned essential canonical frames: {len(record["plannedEssentialFrames"])}. '
                'Plan completeness requires separate review.</p>')
        if record.get("scopeExclusion"):
            exclusion = record["scopeExclusion"]
            body += (f'<p class="callout"><strong>Skipped by user scope decision.</strong> '
                     f'Prerequisite: {esc(exclusion["prerequisite"])}. '
                     f'User instruction: {esc(exclusion["userInstruction"])}. '
                     'No passing result or step screenshot is claimed for excluded execution.</p>')
            if payload.get("scopeExclusions"):
                body += '<p>' + link(resolve(payload["scopeExclusions"]["path"], workspace), target, "Retained user scope decision") + '.</p>'
        attempts = record["actualApplicationAttempts"]
        if attempts:
            body += '<section class="latest-attempt"><h2>Latest attempt</h2>' + attempt_html(attempts[0], target, workspace) + '</section>'
        if len(attempts) > 1:
            body += f'<details class="attempt-history"><summary>Earlier attempt history ({len(attempts) - 1})</summary>'
            for attempt in attempts[1:]:
                label = (f'Earlier attempt {attempt["observedStatus"]} '
                         f'(superseded by latest {attempts[0]["observedStatus"]})')
                body += '<details class="historical-attempt"><summary>' + esc(label) + '</summary>'
                body += attempt_html(attempt, target, workspace, historical=True) + '</details>'
            body += '</details>'
        if not record["actualApplicationAttempts"]:
            body += '<p>No actual application attempt was retained. No screenshot is claimed.</p>'
        if record["relatedHarnessAttempts"]:
            body += '<p>Related evidence outside actual application scope: ' + ', '.join(link(output / "harness" / (attempt.replace("/", "--") + ".html"),
                target, attempt) for attempt in record["relatedHarnessAttempts"]) + '.</p>'
        target.write_text(page(record["caseId"], body), encoding="utf-8")
    for attempt in payload["harnessAttempts"] + payload.get("historicalDeclaredSyntheticAttempts", []):
        target = output / "harness" / (attempt["attemptId"].replace("/", "--") + ".html")
        mis_scoped = attempt.get("evidenceCategory") == "HISTORICAL_DECLARED_SYNTHETIC"
        heading = "Historical declared-synthetic or mis-scoped evidence" if mis_scoped else "Synthetic harness evidence"
        warning = ("The original application path conflicts with the declared synthetic scope. Review retained traces for actual activity. "
                   "This report preserves the declared scope and excludes this attempt from canonical local results." if mis_scoped else
                   "This check does not execute the actual MFE, BFF, or canonical business scenario.")
        body = (f'<p>{link(output / "index.html", target, "Audit ledger")}</p><h1>{heading}</h1>'
                f'<p class="callout"><strong>{warning}</strong></p>'
                + attempt_html(attempt, target, workspace))
        target.write_text(page(attempt["title"], body), encoding="utf-8")
    target = output / "index.html"
    summary = payload["summary"]
    body = ('<h1>UI audit results and screenshots</h1>'
            '<p class="callout"><strong>Business acceptance remains unverified. Owner: unknown. '
            'Review blocked cases and controlled service limits before acceptance.</strong></p>'
            f'<p>{summary["canonicalCases"]} canonical cases appear once. '
            f'Actual application attempts: {summary["applicationAttempts"]}. '
            f'Synthetic harness attempts: {summary["harnessAttempts"]}. '
            f'Historical declared-synthetic or mis-scoped attempts: {summary.get("historicalDeclaredSyntheticAttempts", 0)}.</p>'
            '<p>PASS and FAIL describe local browser predicates. They do not establish full canonical or deployed business acceptance.</p>'
            '<p>Definition review is the historical preflight design assessment. A definition review FAIL can coexist with local PASS.</p>'
            '<p>Step screenshot bindings measure structural coverage only. They do not establish screenshot content quality or relevance.</p>'
            '<p>CONTEXT_RECORDED means capture observations exist. It does not establish human visual review.</p>'
            f'<p>{link(output / "case-results.json", target, "Complete JSON ledger")} · '
            f'{link(output / "case-results.csv", target, "Canonical CSV ledger")} · '
            f'{link(output / "audit-summary.json", target, "Run and integrity summary")}</p>'
            f'<pre>{esc(json.dumps(summary, indent=2))}</pre>'
            '<label>Search <input id="search" type="search" placeholder="Case ID or title"></label>'
            '<label>Local result <select id="status"><option value="">All</option>'
            + ''.join(f'<option>{status}</option>' for status in STATUSES) + '</select></label>'
            '<p id="visible"></p><table><thead><tr><th>Case</th><th>Latest local result</th><th>Definition review (preflight)</th>'
            '<th>Actual attempts</th><th>Retained frames</th><th>Latest step screenshot bindings</th><th>Screenshot content review</th></tr></thead><tbody>')
    for record in records:
        count = sum(len(attempt["frames"]) for attempt in record["actualApplicationAttempts"])
        body += (f'<tr data-status="{record["localPredicateStatus"]}"><td>'
                 f'{link(output / "cases" / (record["caseId"] + ".html"), target, record["caseId"] + ": " + record["title"])}'
                 f'</td><td class="badge {record["localPredicateStatus"]}">{record["localPredicateStatus"]}</td>'
                 f'<td>{esc(record["canonicalQualityStatus"])}</td><td>{len(record["actualApplicationAttempts"])}</td><td>{count}</td>'
                 f'<td>{record["stepsWithScreenshots"]}/{record["canonicalStepCount"]} · {esc(record["stepEvidenceStatus"])}</td>'
                 f'<td>{esc(record.get("screenshotContentReviewStatus", "NOT_REVIEWED"))}<br>'
                 f'{record.get("duplicateFrames", 0)} repeated image frames</td></tr>')
    body += '</tbody></table><h2>Synthetic harness checks</h2><ul>'
    for attempt in payload["harnessAttempts"]:
        body += '<li>' + link(output / "harness" / (attempt["attemptId"].replace("/", "--") + ".html"), target,
                            attempt["title"]) + f' — {attempt["observedStatus"]}, {len(attempt["frames"])} named frames.</li>'
    body += '</ul><h2>Historical declared-synthetic or mis-scoped attempts</h2><p>The original paths and declared scopes remain unchanged. These attempts do not select canonical local results.</p><ul>'
    for attempt in payload.get("historicalDeclaredSyntheticAttempts", []):
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
    parser.add_argument("--scope-exclusions", type=Path, help="Retained user scope decision with exact case IDs and prerequisites.")
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
    exclusion_reference = None
    exclusions = {}
    if args.scope_exclusions:
        exclusion_file = args.scope_exclusions.resolve()
        decision = read(exclusion_file)
        catalog_hash = next(iter(definitions.values()))["catalogSha256"]
        if decision.get("catalogSha256") != catalog_hash or decision.get("status") != "SKIPPED_BY_USER":
            raise ValueError("The scope decision must bind this catalog and record SKIPPED_BY_USER.")
        items = decision["cases"]
        if len({item["caseId"] for item in items}) != len(items):
            raise ValueError("The scope decision contains duplicate case IDs.")
        for item in items:
            if not all(item.get(key) for key in ("prerequisite", "userInstruction")):
                raise ValueError("Each excluded case requires its prerequisite and user instruction.")
        exclusions = {item["caseId"]: item for item in items}
        exclusion_reference = reference(exclusion_file, workspace)
    runs, application, harness = load_runs(root, workspace)
    records = reconcile(rows, application, harness, definitions, exclusions)
    historical_synthetic = [attempt for attempt in harness if attempt["evidenceCategory"] == "HISTORICAL_DECLARED_SYNTHETIC"]
    harness = [attempt for attempt in harness if attempt["evidenceCategory"] == "SYNTHETIC_HARNESS"]
    if len(records) != len(rows) or len({row["caseId"] for row in records}) != len(rows):
        raise ValueError("Canonical reconciliation is incomplete or contains duplicate cases.")
    quality_blocked = sum(row["canonicalQualityStatus"] == "FAIL" for row in rows)
    summary = {"canonicalCases": len(records), "localPredicateStatus": dict(Counter(row["localPredicateStatus"] for row in records)),
               "latestStepEvidenceStatus": dict(Counter(row["stepEvidenceStatus"] for row in records)),
               "latestScreenshotContentReviewStatus": dict(Counter(row["screenshotContentReviewStatus"] for row in records)),
               "latestDuplicateFrames": sum(row["duplicateFrames"] for row in records),
               "latestFramesWithRecordedContext": sum(row["framesWithRecordedContext"] for row in records),
               "canonicalSteps": sum(row["canonicalStepCount"] for row in records),
               "latestStepsWithScreenshots": sum(row["stepsWithScreenshots"] for row in records),
               "casesWithCompleteStepEvidence": sum(row["completeStepEvidence"] for row in records),
               "applicationAttemptsWithCompleteStepEvidence": sum(attempt["completeStepEvidence"]
                   for row in records for attempt in row["actualApplicationAttempts"]),
               "canonicalAcceptanceEstablished": 0, "qualityBlockedCases": quality_blocked,
               "userExcludedCases": len(exclusions), "inScopeCases": len(records) - len(exclusions),
               "actualApplicationCasesObserved": len({case for attempt in application for case in attempt["canonicalIdsMentioned"]}),
               "applicationAttempts": len(application), "applicationAttemptStatus": dict(Counter(a["observedStatus"] for a in application)),
               "applicationScreenshotFrames": sum(len(a["frames"]) for a in application),
               "harnessAttempts": len(harness), "harnessAttemptStatus": dict(Counter(a["observedStatus"] for a in harness)),
               "harnessScreenshotFrames": sum(len(a["frames"]) for a in harness),
               "historicalDeclaredSyntheticAttempts": len(historical_synthetic),
               "historicalDeclaredSyntheticAttemptStatus": dict(Counter(a["observedStatus"] for a in historical_synthetic)),
               "historicalDeclaredSyntheticScreenshotFrames": sum(len(a["frames"]) for a in historical_synthetic),
               "integrityCheck": "PASSED", "canonicalCaseUniquenessCheck": "PASSED"}
    payload = {"schemaVersion": 2, "generatedAt": datetime.now(timezone.utc).isoformat(),
               "generator": reference(Path(__file__), workspace), "frozenInventory": reference(inventory_file, workspace),
               "frozenCaseRecords": reference(preflight_file, workspace), "summary": summary, "runs": runs,
               "scopeExclusions": exclusion_reference,
               "statusDefinitions": {"PASS": "The latest retained actual application attempt passed its local predicates. Screenshot completeness is reported separately.",
                   "FAIL": "The latest retained actual application attempt failed. The retained error limits the cause claim.",
                   "BLOCKED_NOT_EXECUTED": "No completed actual attempt exists. Quality and screenshot limits are reported separately.",
                   "SKIPPED_BY_USER": "The user excluded this prerequisite-dependent case from this audit. Prior attempts remain historical evidence."},
               "stepEvidenceDefinitions": {
                   "COMPLETE": "Each exact canonical step executed and has a retained screenshot binding. This is structural coverage only.",
                   "INCOMPLETE": "Canonical step metadata exists, but execution or screenshot evidence is incomplete.",
                   "LEGACY_ESSENTIAL_FRAMES": "Named screenshots exist without canonical step records. Step evidence not recorded.",
                   "NOT_RECORDED": "No actual application attempt has canonical step evidence."},
               "screenshotContentReviewDefinitions": {
                   "NOT_REVIEWED": "No capture context was recorded. Screenshot content and step relevance have not been reviewed.",
                   "CONTEXT_RECORDED": "At least one frame has machine capture observations. This does not establish human visual review."},
               "limits": ["Synthetic checks never change canonical results.",
                   "Each attempt records its implementation, fixture boundaries, and source hashes. Local execution does not establish deployed business acceptance.",
                   "All attempts remain available. The latest completed actual attempt determines the local predicate status.",
                   "Canonical quality failures block acceptance independently of the local execution result.",
                   "Complete step bindings do not establish screenshot content quality, complete assertion coverage, or business acceptance.",
                   "Identical image bytes can be valid for consecutive assertions. Duplicate counts identify review candidates only."],
               "cases": records, "harnessAttempts": harness, "historicalDeclaredSyntheticAttempts": historical_synthetic,
               "writing_review": WRITING_REVIEW}
    output.mkdir(parents=True)
    save_json(output / "case-results.json", payload)
    save_json(output / "audit-summary.json", {key: value for key, value in payload.items()
              if key not in ("cases", "harnessAttempts", "historicalDeclaredSyntheticAttempts")})
    fields = ["caseId", "title", "localPredicateStatus", "latestObservedStatus", "canonicalFullScenarioStatus", "canonicalAcceptanceStatus",
              "canonicalQualityStatus", "mappingStatusAtPreflight", "definition", "definitionVersion", "definitionSha256", "latestAttempt",
              "scopeStatus",
              "stepEvidenceStatus", "completeStepEvidence", "canonicalStepCount", "stepsWithScreenshots",
              "screenshotContentReviewStatus", "framesWithRecordedContext", "duplicateFrames",
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
