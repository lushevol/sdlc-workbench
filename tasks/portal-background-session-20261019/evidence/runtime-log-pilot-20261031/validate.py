"""Reconcile local pilot source, assertions, captures, and retained evidence."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
TASK = OUT.parents[1]
read = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
checks = []


def check(name, condition, detail=None):
    checks.append({"check": name, "passed": bool(condition), "detail": detail})


binding = read(OUT / "local-source-binding.json")
source_count = 0
for side, entry in binding["source"].items():
    source = ROOT / entry["path"]
    matches = all(sha(source / path) == expected for path, expected in entry["instrumented_source_hashes"].items())
    check(side + " instrumented source identity", matches)
    archive = subprocess.check_output(["git", "-C", str(ROOT / "repos/ui/mfe-base"), "archive", entry["revision"]])
    check(side + " original archive identity", hashlib.sha256(archive).hexdigest() == entry["archive_sha256"])
    for kind, expected in entry["config_hashes"].items():
        check(side + " retained " + kind + " configuration", sha(OUT / (side + "-" + kind + ".webpack.cjs")) == expected)
    source_count += len(entry["instrumented_source_hashes"])
fixture_class_count = 0
for layer in binding["bff_fixture"]["class_layers_in_precedence_order"]:
    check("BFF fixture class layer " + layer["path"],
          all(sha(ROOT / layer["path"] / path) == expected for path, expected in layer["classes"].items()))
    fixture_class_count += len(layer["classes"])
for path, expected in binding["toolkit_substitute_hashes"].items():
    check("toolkit substitute " + path, sha(ROOT / path) == expected)
root_archive = subprocess.check_output(["git", "-C", str(ROOT / "repos/ui/mfe-root-config"), "archive", binding["root_source"]["revision"]])
check("root original archive identity", hashlib.sha256(root_archive).hexdigest() == binding["root_source"]["archive_sha256"])
check("instrumentation bytes", sha(OUT / "instrumentation.patch") == binding["instrumentation_patch_sha256"])
check("preparation runner identity", sha(OUT / "prepare-local.py") == binding["runner_sha256"])
case_count = screenshot_count = 0
runner_hashes = {sha(OUT / "run-browser.mjs"), sha(OUT / "runner-v1.mjs")}
for run in sorted((OUT / "runs").iterdir()):
    summary = read(run / "browser-summary.json")
    check(run.name + " runner source", summary["runner_sha256"] in runner_hashes)
    check(run.name + " explicit environment boundary", summary["source_kind"] == "local_development" and summary["uat_evidence_status"] == "NOT_RUN")
    for path in run.glob("*/result.json"):
        case_count += 1
        result = read(path)
        actual_status = "PASSED" if all(item["status"] == "PASSED" for item in result["assertions"]) else "FAILED"
        check(str(path.parent.relative_to(OUT)) + " assertion disposition", result["status"] == actual_status)
        events = [json.loads(line) for line in (path.parent / "application-events.ndjson").read_text().splitlines() if line]
        collection = result["collection"]
        check(str(path.parent.relative_to(OUT)) + " collection completeness",
              collection["emitted"] == collection["collected"] == len(events)
              and collection["parse_errors"] == 0
              and [event["seq"] for event in events] == list(range(1, len(events) + 1)))
        for image in result["screenshots"]:
            screenshot_count += 1
            check(str(path.parent.relative_to(OUT)) + "/" + image["file"], sha(path.parent / image["file"]) == image["sha256"])

analysis = read(OUT / "analysis.json")
check("local assessed inventory", analysis["local_metrics"]["evidence_assessed"] == 5 and analysis["local_metrics"]["required_observations"] == 6)
check("candidate execution inventory", analysis["candidate_cases"] == {"passed": 3, "failed": 0, "assertions_passed": 56, "events": 192})
check("UAT evidence remains unexecuted", analysis["uat"]["status"] == "NOT_RUN" and analysis["uat"]["required_observations"] is None)
check("stale renewal branch remains unverified", analysis["observations"][-1]["evidence_assessed"] is False and analysis["observations"][-1]["passing_behavior"] is None)
check("analysis script identity", sha(OUT / "analyze.py") == analysis["analysis_script_sha256"])
for row in analysis["observations"]:
    check(row["id"] + " result and log identity",
          sha(OUT / row["result_ref"]) == row["result_sha256"] and sha(OUT / row["log_ref"]) == row["log_sha256"])
check("negative collector control", read(OUT / "collector-negative-control.json")["collection_completeness_rejected"])
check("HTML runtime panels", len(read(OUT / "report-checks/results.json")))

def slug(text):
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


links = 0
documents = [TASK / "10-runtime-log-pilot.md", TASK / "10-release-confidence.md", TASK / "evidence/index.md"]
for document in documents:
    text = document.read_text()
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if document.name != "10-runtime-log-pilot.md" and "runtime-log-pilot" not in target:
            continue
        if "://" in target:
            continue
        local, _, anchor = target.partition("#")
        source = (document.parent / local).resolve() if local else document
        valid = source.is_file()
        if valid and anchor:
            body = source.read_text()
            if re.fullmatch(r"L\d+(?:-L?\d+)?", anchor):
                lines = [int(value) for value in re.findall(r"\d+", anchor)]
                valid = min(lines) >= 1 and max(lines) <= len(body.splitlines())
            else:
                headings = [slug(value) for value in re.findall(r"^#{1,6}\s+(.+)$", body, re.M)]
                ids = re.findall(r'id=[\"\x27]([^\"\x27]+)', body)
                valid = anchor in headings or anchor in ids
        links += 1
        check("link " + document.name + ": " + target, valid)

for line in (TASK / "10-runtime-log-pilot.md").read_text().splitlines():
    expected = re.findall(r"`([a-f0-9]{64})`", line)
    targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", line)
    if len(expected) == 1 and targets:
        sources = [(TASK / target.split("#")[0]).resolve() for target in targets]
        check("report SHA-256 " + expected[0], any(source.is_file() and sha(source) == expected[0] for source in sources))

leaks = []
token = re.compile(r"(?:Bearer\s+)?eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}|Bearer e30\.[A-Za-z0-9_-]{8,}\.")
for path in OUT.rglob("*"):
    if path.is_file() and path.suffix in {".json", ".ndjson", ".log"}:
        if token.search(path.read_text(errors="replace")):
            leaks.append(str(path.relative_to(OUT)))
check("retained structured evidence token scan", not leaks, leaks)

result = {"status": "PASSED" if all(item["passed"] for item in checks) else "FAILED",
          "source_files_checked": source_count, "fixture_classes_checked": fixture_class_count, "case_results_checked": case_count,
          "screenshots_checked": screenshot_count, "local_links_checked": links, "checks": checks,
          "limits": ["These checks establish retained identities and declared assertion outcomes only.",
                     "Token scanning is bounded and does not establish complete privacy or security compliance.",
                     "Automated checks do not check the complete approved ASD dictionary or grammar rules."]}
(OUT / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in ["status", "source_files_checked", "case_results_checked", "screenshots_checked", "local_links_checked"]}))
for item in checks:
    if not item["passed"]:
        print(json.dumps(item))
raise SystemExit(result["status"] != "PASSED")
