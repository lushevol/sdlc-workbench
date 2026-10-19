"""Check local document links and limited ASD writing constraints."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[4]
OUTPUT = Path(__file__).resolve().parent / "documentation.json"
DOCUMENTS = (
    ".agents/skills/release-clinic/SKILL.md",
    ".agents/skills/release-clinic/references/html-reporting.md",
    "docs/RELEASE_CLINIC.md",
    "tasks/release-clinic-html-20261020/parity-review.md",
    "tasks/release-clinic-html-20261020/evidence/parity-browser/assessment.md",
)
errors = []
identities = []
links = 0


def sentences(text):
    return [value for value in re.split(r"(?<=[.!?])\s+", text.strip()) if value]


for relative in DOCUMENTS:
    path = ROOT / relative
    content = path.read_bytes()
    identities.append({"path": relative, "sha256": hashlib.sha256(content).hexdigest()})
    text = re.sub(r"\A---\n.*?\n---\n", "", content.decode(), count=1, flags=re.S)
    code, paragraph = False, []

    def end_paragraph():
        if len(sentences(" ".join(paragraph))) > 6:
            errors.append({"path": relative, "error": "Paragraph exceeds six sentences", "text": list(paragraph)})
        paragraph.clear()

    for line_number, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            code = not code
            end_paragraph()
            continue
        if code:
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", line):
            target = target.strip("<>")
            if re.match(r"\w+:", target):
                continue
            links += 1
            local = unquote(target.split("#", 1)[0])
            if local and not (path.parent / local).exists():
                errors.append({"path": relative, "line": line_number, "error": "Missing local link", "target": target})
        if not line.strip() or line.startswith("#"):
            end_paragraph()
            continue
        table = line.startswith("|")
        bullet = bool(re.match(r"^(?:[-*]|\d+[.])\s", line))
        if table or bullet:
            end_paragraph()
        parts = line.strip("|").split("|") if table else [line]
        for part in parts:
            plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", part)
            for sentence in sentences(plain):
                if len(sentence.split()) > 20:
                    errors.append({"path": relative, "line": line_number,
                                   "error": "Sentence exceeds 20 words", "text": sentence})
        if not table and not bullet:
            paragraph.append(line)
    end_paragraph()

diff = subprocess.run(["git", "diff", "--check", "--", *DOCUMENTS,
                       ".agents/skills/release-clinic/scripts/check_report_parity.py",
                       "tests/test_release_clinic_skill.py", "tests/test_workspace_layout.py"],
                      cwd=ROOT, capture_output=True, text=True)
if diff.returncode:
    errors.append({"error": "git diff --check failed", "output": diff.stdout + diff.stderr})
record = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "status": "PASSED" if not errors else "FAILED", "local_links": links,
    "documents": identities, "diff_check_exit_code": diff.returncode, "errors": errors,
    "writing_review": {
        "standard": "ASD-STE100", "automated_check": "PASSED" if not errors else "FAILED",
        "asd_review": "PENDING", "reviewer": None, "reviewed_at": None,
        "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."],
    },
}
OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, indent=2))
raise SystemExit(bool(errors))
