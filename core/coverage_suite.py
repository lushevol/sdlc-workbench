"""Run configured permission comparisons and produce one linked coverage report.

Supplied response replay is the default. Live collection requires --mode live.
Each comparison retains its own scope, denominator, checkpoints, and evidence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import sys
import webbrowser

from .entitlement_coverage import _bounded_error, _hash, _now, _write
from .entitlement_reconciliation import ReconciliationError
from .entitlement_sources import SourceError


def _runners():
    from . import ems2_coverage, entitlement_coverage
    return {"ces": entitlement_coverage.run, "ems2": ems2_coverage.run}


def _markdown(value):
    text = html.escape(str(value), quote=False).replace("\n", "<br>")
    return re.sub(r"([\\`*_[\]{}|#!])", r"\\\1", text)


def _render(result, directory, children):
    """Publish one detailed suite in each format without merging denominators."""
    from .coverage_reporting import STYLE, SCRIPT, render_fragment, render_markdown
    esc = lambda value: html.escape(str(value), quote=True)
    rows = []
    markdown = ["---", "writing_review:", "  standard: ASD-STE100", "  automated_check: NOT_RUN",
                "  asd_review: PENDING", "  reviewer: null", "  reviewed_at: null", "  limitations:",
                "    - Automated checks do not check the complete approved dictionary or grammar rules.",
                "---", "", "# All migration coverage", "",
                "**" + _markdown(result["status"]) + ": " + _markdown(result["conclusion"]) + "**", "",
                "Owner: unknown. Review differences and obtain evidence for unassessed comparisons.", "",
                _markdown(result["evidence_source"]) + ".", "", _markdown(result["scope"]), "",
                "Account populations overlap. Counts from separate comparisons must not be added together.", "",
                "[HTML report](index.html) · [Complete suite result](result.json)", "",
                "## Comparison overview", "",
                "| Comparison | Status | Discovered | Baseline | Compared | Matching | Different | Unassessed | Exact functional profiles |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for check in result["checks"]:
        summary = check.get("summary", {})
        exact = summary.get("functional_profile_coverage_percent")
        values = [check["label"], check["status"], *[summary.get(key, "UNASSESSED") for key in
                  ("discovered_accounts", "baseline_accounts", "compared_accounts", "matching_accounts",
                   "different_accounts", "unassessed_accounts")], "UNASSESSED" if exact is None else str(exact) + "%"]
        rows.append("<tr>" + "".join("<td>" + esc(value) + "</td>" for value in values) + "</tr>")
        markdown.append("| " + " | ".join(_markdown(value) for value in values) + " |")
    content = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
               "<meta name='viewport' content='width=device-width, initial-scale=1'>"
               "<title>All migration coverage</title><style>" + STYLE + "</style></head><body>"
               "<main><header><p>Coverage suite</p><h1>All migration coverage</h1>"
               "<p class='callout'><strong>" + esc(result["evidence_source"]) + " · " + esc(result["status"]) + "</strong></p>"
               "<p>" + esc(result["conclusion"]) + "</p><p>" + esc(result["scope"]) + "</p>"
               "<p>Owner: unknown. Review differences and obtain evidence for unassessed comparisons.</p>"
               "<p>Account populations overlap. Counts from separate comparisons must not be added together.</p>"
               "<p><a href='index.md'>Markdown report</a> · <a href='result.json'>Complete suite result</a></p></header>"
               "<section><h2>Comparison overview</h2><div class='table-wrap'><table><thead><tr>" +
               "".join("<th>" + esc(label) + "</th>" for label in ("Comparison", "Status", "Discovered", "Baseline", "Compared", "Matching", "Different", "Unassessed", "Exact functional profiles")) +
               "</tr></thead>" + "".join(rows) + "</table></div></section>")
    for check in result["checks"]:
        identifier = check["id"]
        content += "<section id='suite-" + identifier + "'><h2>" + esc(check["label"]) + "</h2><p><strong>" + esc(check["status"]) + "</strong></p>"
        markdown.extend(["", "## " + _markdown(check["label"]), "", "Status: **" + _markdown(check["status"]) + "**.", ""])
        artifacts = check.get("artifacts", {})
        labels = {"html": "Comparison HTML", "markdown": "Comparison Markdown", "result": "Complete JSON",
                  "differences": "Differences CSV", "binding": "Source binding", "checkpoints": "Account checkpoints"}
        links = [(labels[key], target) for key, target in artifacts.items() if key in labels]
        if links:
            content += "<p>" + " · ".join("<a href='" + esc(target) + "'>" + esc(label) + "</a>" for label, target in links) + "</p>"
            markdown.extend([" · ".join("[" + label + "](" + target + ")" for label, target in links), ""])
        if check.get("errors"):
            content += "<p>Comparison setup failed. Review configuration and source files. Owner: unknown.</p><table><tr><th>Error code</th><th>HTTP status</th></tr>"
            markdown.extend(["Comparison setup failed. Review configuration and source files. Owner: unknown.", "", "| Error code | HTTP status |", "| --- | --- |"])
            for error in check["errors"]:
                code, status = error.get("code", "UNKNOWN"), error.get("http_status")
                status = "Unavailable" if status is None else status
                content += "<tr><td>" + esc(code) + "</td><td>" + esc(status) + "</td></tr>"
                markdown.append("| " + _markdown(code) + " | " + _markdown(status) + " |")
            content += "</table>"
        child = children.get(identifier)
        child_dir = directory / identifier
        if child is not None and "users" in child and "entitlements" in child:
            content += render_fragment(child, child_dir, prefix=identifier + "-", link_prefix=identifier + "/")
            markdown.extend([render_markdown(child, child_dir, prefix=identifier + "-", link_prefix=identifier + "/", heading_offset=2)])
        elif not check.get("errors"):
            content += "<p>Detailed comparison content is available in the linked child artifacts.</p>"
            markdown.extend(["Detailed comparison content is available in the linked child artifacts.", ""])
        content += "</section>"
    content += "<section><h2>Suite source binding</h2><table><tr><th>Binding</th><th>SHA-256</th></tr>"
    for key, value in result.get("binding", {}).items():
        entries = value.items() if isinstance(value, dict) else [(key, value)]
        for name, digest in entries:
            content += "<tr><td>" + esc(key + ": " + name if isinstance(value, dict) else name) + "</td><td>" + esc(digest) + "</td></tr>"
    content += "</table><p>Writing review: automated_check NOT_RUN; asd_review PENDING; reviewer and reviewed_at are unset.</p>"
    content += "<p>Automated checks do not check the complete approved dictionary or grammar rules.</p></section>"
    content += "<footer><p>Functional comparisons do not establish complete data-profile equality or current live parity.</p></footer></main><script>" + SCRIPT + "</script></body></html>"
    markdown.extend(["", "## Evidence limits", "",
                     "Each comparison retains its own scope, denominators, source binding, and excluded entities.", "",
                     "Functional comparisons do not establish complete data-profile equality or current live parity.", "",
                     "## Suite source binding", "", "| Binding | SHA-256 |", "| --- | --- |"])
    for key, value in result.get("binding", {}).items():
        if isinstance(value, dict):
            for name, digest in value.items(): markdown.append("| " + _markdown(key + ": " + name) + " | " + _markdown(digest) + " |")
        else: markdown.append("| " + _markdown(key) + " | " + _markdown(value) + " |")
    (directory / "index.html").write_text(content, encoding="utf-8")
    (directory / "index.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")


def run(config_path, *, mode="replay", output=None, user_limit=None):
    if mode not in ("replay", "live"):
        raise ValueError("Unsupported coverage mode")
    path = Path(config_path).resolve()
    config = json.loads(path.read_text(encoding="utf-8"))
    checks = config.get("checks")
    if config.get("schema_version") != 1 or not isinstance(checks, list) or not checks:
        raise ValueError("A versioned nonempty comparison list is required")
    runners = _runners()
    identifiers = []
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("Each comparison requires an object")
        identifier = check.get("id", "")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", identifier):
            raise ValueError("Comparison IDs must be safe folder names")
        if check.get("kind") not in runners or not isinstance(check.get("config"), str):
            raise ValueError("Unsupported comparison kind or configuration path")
        identifiers.append(identifier)
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Comparison IDs must be unique")
    directory = Path(output).resolve() if output else (path.parent / config["output_dir"] /
        (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "-all-" + mode)).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    result = {"schema_version": 1, "scope": config.get("scope", "Configured permission comparisons"),
              "started_at": _now(), "mode": mode, "status": "INCOMPLETE", "checks": [],
              "evidence_source": "MOCK: supplied API responses" if mode == "replay" else "LIVE: collected API responses",
              "binding": {"config_sha256": _hash(path.read_bytes()),
                          "implementation_sha256": {name: _hash(Path(__file__).with_name(name).read_bytes())
                              for name in ("coverage_suite.py", "coverage_reporting.py")}}}
    children = {}
    for check in checks:
        child_config = (path.parent / check["config"]).resolve()
        record = {"id": check["id"], "label": check.get("label", check["id"]), "status": "INCOMPLETE"}
        try:
            record["config_sha256"] = _hash(child_config.read_bytes())
            child, child_dir = runners[check["kind"]](child_config, mode=mode, output=directory / check["id"], user_limit=user_limit)
            record.update(status=child["status"], summary=child["summary"], binding=child["binding"])
            children[check["id"]] = child
            artifacts = {key: check["id"] + "/" + name for key, name in
                         (("html", "report.html"), ("markdown", "report.md"), ("result", "result.json"),
                          ("differences", "differences.csv"), ("binding", "binding.json"), ("checkpoints", "cases.jsonl"))
                         if (child_dir / name).is_file()}
            record["artifacts"] = artifacts
            if "html" in artifacts: record["report"] = artifacts["html"]
            if "markdown" in artifacts: record["markdown_report"] = artifacts["markdown"]
        except (OSError, ValueError, KeyError, TypeError, SourceError, ReconciliationError) as error:
            record["errors"] = [_bounded_error(error)]
        result["checks"].append(record)
        _write(directory / "result.json", result)
    statuses = {check["status"] for check in result["checks"]}
    result["status"] = ("INCOMPLETE" if not statuses.issubset({"FUNCTIONAL_MATCH", "DIFFERENCES"})
                        else "DIFFERENCES" if "DIFFERENCES" in statuses else "FUNCTIONAL_MATCH")
    result["conclusion"] = ("Review each comparison separately. Missing captures remain unassessed; complete migration coverage is unknown."
                            if result["status"] == "INCOMPLETE" else "Review the differences in the linked comparison reports."
                            if result["status"] == "DIFFERENCES" else "All configured functional comparisons match within their declared evidence limits.")
    result["finished_at"] = _now()
    result["writing_review"] = {"standard": "ASD-STE100", "automated_check": "NOT_RUN", "asd_review": "PENDING",
                               "reviewer": None, "reviewed_at": None,
                               "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."]}
    _write(directory / "result.json", result)
    _render(result, directory, children)
    return result, directory


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=("replay", "live"), default="replay")
    parser.add_argument("--output")
    parser.add_argument("--user-limit", type=int)
    parser.add_argument("--open", action="store_true", dest="open_report")
    args = parser.parse_args(argv)
    if args.user_limit is not None and args.user_limit < 1:
        parser.error("--user-limit must be positive")
    try:
        result, directory = run(args.config, mode=args.mode, output=args.output, user_limit=args.user_limit)
    except (OSError, ValueError, KeyError, TypeError, SourceError) as error:
        print("Coverage suite setup failed: " + type(error).__name__ + ". Check configuration and source files.", file=sys.stderr)
        return 2
    print(json.dumps({"status": result["status"], "mode": result["mode"], "evidence_source": result["evidence_source"],
                      "report": str(directory / "index.html"), "html_report": str(directory / "index.html"),
                      "markdown_report": str(directory / "index.md"), "checks": [{"id": c["id"], "status": c["status"]} for c in result["checks"]]}, indent=2))
    if args.open_report:
        webbrowser.open((directory / "index.html").as_uri())
    return 0 if result["status"] == "FUNCTIONAL_MATCH" else 1 if result["status"] == "DIFFERENCES" else 2


if __name__ == "__main__":
    raise SystemExit(main())
