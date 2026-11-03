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


def _render(result, directory):
    esc = lambda value: html.escape(str(value))
    content = """<!doctype html><html lang="en"><meta charset="utf-8">
<title>All migration coverage</title><style>
body{font:16px system-ui;max-width:1120px;margin:32px auto;padding:0 20px;background:#f5f7fa;color:#192332}
section{background:white;border-radius:10px;padding:22px;margin:18px 0}h1{font-size:28px}
table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px;border-bottom:1px solid #ddd}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}a{color:#195ab4}.note{border-left:5px solid #946b16;padding-left:16px}
</style><h1>All migration coverage</h1>"""
    content += "<p class='note'><b>" + esc(result["evidence_source"]) + "</b><br>" + esc(result["status"]) + "</p>"
    content += "<p>" + esc(result["scope"]) + "</p><p>" + esc(result["conclusion"]) + "</p>"
    for check in result["checks"]:
        summary = check.get("summary", {})
        content += "<section><h2>" + esc(check["label"]) + "</h2><p><b>" + esc(check["status"]) + "</b></p>"
        metrics = (("Subjects retained", summary.get("subject_coverage", "UNASSESSED")),
                   ("Users compared", summary.get("compared_accounts", "UNASSESSED")),
                   ("Users different", summary.get("different_accounts", "UNASSESSED")),
                   ("Users unassessed", summary.get("unassessed_accounts", "UNASSESSED")),
                   ("Exact functional profiles", "UNASSESSED" if summary.get("functional_profile_coverage_percent") is None
                    else str(summary["functional_profile_coverage_percent"]) + "%"))
        content += "<table><tr>" + "".join("<th>" + esc(k) + "</th>" for k, _ in metrics) + "</tr><tr>"
        content += "".join("<td>" + esc(v) + "</td>" for _, v in metrics) + "</tr></table>"
        if check.get("report"):
            content += "<p><a href='" + esc(check["report"]) + "'>Open comparison report and differences</a></p>"
        if check.get("errors"):
            content += "<p>Comparison setup failed. Owner: unknown. Review configuration and source files.</p>"
        content += "<details><summary>Counts and evidence limits</summary><pre>" + esc(json.dumps(check, indent=2)) + "</pre></details></section>"
    content += "<p>Each linked report records its excluded entities and data-profile limits.</p>"
    content += "<p>Account populations overlap. Counts from separate comparisons must not be added together.</p>"
    content += "<p><a href='result.json'>Complete suite result</a></p></html>"
    (directory / "index.html").write_text(content, encoding="utf-8")


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
              "binding": {"config_sha256": _hash(path.read_bytes()), "implementation_sha256": _hash(Path(__file__).read_bytes())}}
    for check in checks:
        child_config = (path.parent / check["config"]).resolve()
        record = {"id": check["id"], "label": check.get("label", check["id"]), "status": "INCOMPLETE"}
        try:
            record["config_sha256"] = _hash(child_config.read_bytes())
            child, child_dir = runners[check["kind"]](child_config, mode=mode, output=directory / check["id"], user_limit=user_limit)
            record.update(status=child["status"], summary=child["summary"], binding=child["binding"])
            if (child_dir / "report.html").is_file():
                record["report"] = check["id"] + "/report.html"
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
    result["writing_review"] = {"standard": "ASD-STE100", "automated_check": "PASSED", "asd_review": "PENDING",
                               "reviewer": None, "reviewed_at": None,
                               "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."]}
    _write(directory / "result.json", result)
    _render(result, directory)
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
                      "report": str(directory / "index.html"), "checks": [{"id": c["id"], "status": c["status"]} for c in result["checks"]]}, indent=2))
    if args.open_report:
        webbrowser.open((directory / "index.html").as_uri())
    return 0 if result["status"] == "FUNCTIONAL_MATCH" else 1 if result["status"] == "DIFFERENCES" else 2


if __name__ == "__main__":
    raise SystemExit(main())
