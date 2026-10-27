"""Retain exact coverage counters and added-line coverage for changed runtime paths."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUTPUT = Path(__file__).resolve().parent
WORKSPACE = OUTPUT.parents[4]
APPLICATION = WORKSPACE / "repos/ui/mfe-base"
SCRATCH = WORKSPACE / ".workbench/four-checks-coverage-20261027"
BASE = "f025513f696476a9cc8162681410cbd21e029bcb"
HEAD = "1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303"

def metric(values):
    values = list(values)
    hit = sum(value > 0 for value in values)
    return {"covered": hit, "total": len(values), "pct": round(100 * hit / len(values), 2) if values else None}

def counters(item):
    lines = {}
    for identifier, location in item["statementMap"].items():
        line = location["start"]["line"]
        lines[line] = max(lines.get(line, 0), item["s"][identifier])
    return {
        "statements": metric(item["s"].values()),
        "functions": metric(item["f"].values()),
        "branches": metric(value for values in item["b"].values() for value in values),
        "lines": metric(lines.values()),
    }, lines

def arm_location(branch, arm):
    location = branch["locations"][arm]
    return location if "line" in location.get("start", {}) else branch["loc"]

def overlaps(location, added):
    return any(location["start"]["line"] <= number <= location["end"]["line"] for number in added)

raw = json.loads((OUTPUT / "instrumented/coverage-final.json").read_text())
coverage = {str(Path(name).relative_to(SCRATCH)): item for name, item in raw.items()}
paths = subprocess.check_output(["git", "-C", str(APPLICATION), "diff", "--name-only", BASE, HEAD], text=True).splitlines()
runtime = [name for name in paths if name.startswith("src/") and not re.search(r"\.(test|stories)\.", name) and name.endswith((".ts", ".tsx", ".js"))]
files = []
aggregate = {"statements": [], "functions": [], "branches": [], "lines": []}
added_aggregate = {"statements": [], "functions": [], "branches": [], "lines": []}
for name in runtime:
    patch = subprocess.check_output(["git", "-C", str(APPLICATION), "diff", "--unified=0", BASE, HEAD, "--", name], text=True)
    added = []
    line = 0
    for entry in patch.splitlines():
        match = re.match(r"@@ .* \+(\d+)(?:,(\d+))? @@", entry)
        if match:
            line = int(match.group(1))
        elif entry.startswith("+++") or entry.startswith("---"):
            continue
        elif entry.startswith("+"):
            added.append(line)
            line += 1
        elif entry.startswith(" "):
            line += 1
    item = coverage.get(name)
    row = {"path": name, "source_sha256": hashlib.sha256((SCRATCH / name).read_bytes()).hexdigest(), "added_source_lines": added}
    if item is None:
        row["instrumentation"] = "ABSENT"
        files.append(row)
        continue
    summary, lines = counters(item)
    row["whole_file"] = summary
    source = (SCRATCH / name).read_text().splitlines()
    row["uncovered_lines"] = [{"line": number, "source": source[number - 1]} for number, count in lines.items() if count == 0]
    row["uncovered_branches"] = []
    for identifier, counts in item["b"].items():
        branch = item["branchMap"][identifier]
        for arm, count in enumerate(counts):
            if count == 0:
                location = arm_location(branch, arm)
                row["uncovered_branches"].append({"id": identifier, "arm": arm, "type": branch["type"], "location": location, "synthetic_arm_location": location != branch["locations"][arm], "added_line_overlap": overlaps(location, added)})
    selected_s = [count for identifier, count in item["s"].items() if item["statementMap"][identifier]["start"]["line"] in added]
    selected_f = [count for identifier, count in item["f"].items() if any(item["fnMap"][identifier]["loc"]["start"]["line"] <= n <= item["fnMap"][identifier]["loc"]["end"]["line"] for n in added)]
    selected_b = [count for identifier, counts in item["b"].items() for arm, count in enumerate(counts) if overlaps(arm_location(item["branchMap"][identifier], arm), added)]
    selected_l = [count for number, count in lines.items() if number in added]
    row["added_executable"] = {kind: metric(values) for kind, values in {"statements": selected_s, "functions": selected_f, "branches": selected_b, "lines": selected_l}.items()}
    row["uncovered_added_lines"] = [entry for entry in row["uncovered_lines"] if entry["line"] in added]
    files.append(row)
    for kind, values in {"statements": item["s"].values(), "functions": item["f"].values(), "branches": [count for counts in item["b"].values() for count in counts], "lines": lines.values()}.items():
        aggregate[kind].extend(values)
    for kind, values in {"statements": selected_s, "functions": selected_f, "branches": selected_b, "lines": selected_l}.items():
        added_aggregate[kind].extend(values)
result = {
    "base_commit": BASE, "candidate_commit": HEAD, "comparison": "exact endpoints",
    "changed_runtime_path_count": len(runtime),
    "changed_files_aggregate": {kind: metric(values) for kind, values in aggregate.items()},
    "added_executable_aggregate": {kind: metric(values) for kind, values in added_aggregate.items()},
    "whole_application": json.loads((OUTPUT / "instrumented/coverage-summary.json").read_text())["total"],
    "files": files,
    "definitions": {
        "added_lines": "Actual added candidate-side lines from zero-context Git diff; comments and types lack counters.",
        "changed_line_coverage": "Istanbul statement start-line maximum hit count, restricted to added lines.",
        "changed_branch_coverage": "Istanbul branch arms whose source ranges overlap at least one added line. Synthetic empty arm locations use their containing branch range.",
        "functions": "Changed functions include any function range overlapping an added line.",
        "limits": "Instrumentation measures executed source only. It does not establish assertions or complete intended behavior.",
    },
}
(OUTPUT / "coverage-analysis.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in ["changed_runtime_path_count", "changed_files_aggregate", "added_executable_aggregate", "whole_application"]}, indent=2))
