"""Check this documentation consolidation without running business services."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile


EVIDENCE = Path(__file__).resolve().parent
TASK = EVIDENCE.parent
ROOT = TASK.parents[1]
DOCUMENTS = [TASK / "intake.md", TASK / "verification.md", EVIDENCE / "index.md"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


manifest = json.loads((EVIDENCE / "manifest.json").read_text())
integrity_errors = []
for record in manifest["records"]:
    original = ROOT / record["original_path"]
    if not original.is_file() or digest(original.read_bytes()) != record["sha256"]:
        integrity_errors.append(record["original_path"])
    if record["retained_path"]:
        retained = TASK / record["retained_path"]
        if not retained.is_file() or digest(retained.read_bytes()) != record["sha256"]:
            integrity_errors.append(record["retained_path"])

source_receipt = json.loads((EVIDENCE / "source-inspection.json").read_text())
for source in source_receipt["sources"]:
    data = subprocess.check_output(
        ["git", "-C", str(ROOT / source["repository_path"]), "show", f'{source["revision"]}:{source["path"]}']
    )
    if digest(data) != source["sha256"]:
        integrity_errors.append(f'{source["repository_path"]}:{source["path"]}')

tooling = json.loads((EVIDENCE / "browser-final/verification.json").read_text())
for path, expected in tooling["evidence_files"].items():
    if digest((EVIDENCE / "browser-final" / path).read_bytes()) != expected:
        integrity_errors.append("browser-final/" + path)
for run in ["run-001", "run-002"]:
    folder = EVIDENCE / "portal" / run / "browser"
    receipt = json.loads((folder / "browser-events-001.receipt.json").read_text())
    events = (folder / "browser-events-001.json").read_bytes()
    if receipt["sha256"] != digest(events):
        integrity_errors.append(run + "/event-receipt")

broken_links = []
long_prose = []
table_errors = []
for document in DOCUMENTS:
    text = document.read_text()
    for target in re.findall(r'!?\[[^\]]*\]\((<[^>]+>|[^)\s]+)\)', text):
        target = target.strip("<>")
        if "://" in target or target.startswith("#"):
            continue
        file_target = target.split("#")[0]
        if file_target and not (document.parent / file_target).exists():
            broken_links.append({"document": str(document.relative_to(TASK)), "target": target})
    fenced = False
    frontmatter = False
    table_width = None
    for number, line in enumerate(text.splitlines(), 1):
        if number == 1 and line == "---":
            frontmatter = True
            continue
        if frontmatter:
            if line == "---":
                frontmatter = False
            continue
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("|"):
            width = len(line.split("|"))
            if table_width is not None and table_width != width:
                table_errors.append({"document": str(document.relative_to(TASK)), "line": number})
            table_width = width
            continue
        table_width = None
        if not line.strip() or line.startswith("#"):
            continue
        for sentence in re.split(r'(?<=[.!?])\s+', line):
            words = re.findall(r"[A-Za-z0-9]+(?:[-’'][A-Za-z0-9]+)*", sentence)
            if len(words) > 20:
                long_prose.append({"document": str(document.relative_to(TASK)), "line": number, "words": len(words)})

patterns = {
    "jwt": re.compile(rb"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential_url": re.compile(rb"https?://[^\s/:]+:[^\s/@]+@"),
    "common_live_token": re.compile(rb"(?:ghp_|github_pat_|sk-live-)[A-Za-z0-9_]{16,}"),
}
privacy_matches = []
privacy_items = 0
for path in TASK.rglob("*"):
    if not path.is_file():
        continue
    items = [(str(path.relative_to(TASK)), path.read_bytes())]
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            items.extend((f"{path.relative_to(TASK)}!{name}", archive.read(name)) for name in archive.namelist())
    for locator, data in items:
        privacy_items += 1
        for name, pattern in patterns.items():
            if pattern.search(data):
                privacy_matches.append({"locator": locator, "pattern": name})

tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
history_paths = [p for p in tracked if p.startswith("knowledge/raw/") or "/audit/" in p]
history_changed = []
for path in history_paths:
    committed = subprocess.check_output(["git", "show", f'{manifest["base_revision"]}:{path}'], cwd=ROOT)
    if committed != (ROOT / path).read_bytes():
        history_changed.append(path)

failures = integrity_errors + broken_links + long_prose + table_errors + privacy_matches + history_changed
result = {
    "status": "FAILED" if failures else "PASSED",
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "base_revision": manifest["base_revision"],
    "writing_review": {
        "standard": "ASD-STE100",
        "automated_check": "FAILED" if failures else "PASSED",
        "asd_review": "PENDING",
        "reviewer": None,
        "reviewed_at": None,
        "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."],
    },
    "indexed_sources": len(manifest["records"]),
    "byte_identical_copies": sum(bool(r["retained_path"]) for r in manifest["records"]),
    "exact_revision_source_reads": len(source_receipt["sources"]),
    "integrity_errors": integrity_errors,
    "broken_local_links": broken_links,
    "prose_sentences_over_20_words": long_prose,
    "table_structure_errors": table_errors,
    "privacy_pattern_scan": {"items": privacy_items, "patterns": list(patterns), "matches": privacy_matches},
    "retained_history": {"checked": len(history_paths), "changed": history_changed},
    "limits": [
        "Local documentation and evidence integrity checks only; no business execution.",
        "Privacy patterns do not detect every secret format.",
        "Sentence counts do not establish complete ASD-STE100 compliance.",
        "Authoring structure is checked separately with the installed ai-sdlc linter.",
    ],
}
output = EVIDENCE / (sys.argv[1] if len(sys.argv) > 1 else "document-checks.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(bool(failures))
