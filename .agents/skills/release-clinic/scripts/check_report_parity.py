#!/usr/bin/env python3
"""Compare the complete included report skill with an explicit upstream source."""

import argparse
import hashlib
import json
from pathlib import Path
import re


LIMITATION = (
    "Byte equality covers the distributed instructions and canonical report assets. "
    "It does not verify analyst decisions, generated reports, browser controls, or release behavior."
)


def read_source(path):
    """Read bytes once and retain their identity even when skill validation fails."""
    record = {
        "path": str(path),
        "sha256": None,
        "size_bytes": None,
        "line_count": None,
    }
    try:
        content = path.read_bytes()
    except OSError as error:
        return record, None, f"Cannot read source {path}: {error.strerror or str(error)}"
    record.update(
        sha256=hashlib.sha256(content).hexdigest(),
        size_bytes=len(content),
        line_count=len(content.splitlines()),
    )
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return record, None, f"Source is not UTF-8: {path}"
    if not text.strip():
        return record, None, f"Source is empty: {path}"
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.DOTALL)
    if (not frontmatter
            or not re.search(r"^name:\s*(?:dtp-tda-report|\"dtp-tda-report\"|'dtp-tda-report')\s*$",
                             frontmatter.group(1), re.MULTILINE)
            or not text[frontmatter.end():].strip()):
        return record, None, f"Source must contain dtp-tda-report skill frontmatter and instructions: {path}"
    return record, content, None


def check_parity(upstream):
    included = Path(__file__).resolve().parents[1] / "references/dtp-tda-report.md"
    included_record, included_bytes, included_error = read_source(included)
    upstream = Path(upstream)
    try:
        upstream = upstream.expanduser().resolve()
    except (OSError, RuntimeError, ValueError) as error:
        upstream_record = {"path": str(upstream), "sha256": None, "size_bytes": None, "line_count": None}
        upstream_bytes = None
        upstream_error = f"Cannot resolve source {upstream}: {error}"
    else:
        upstream_record, upstream_bytes, upstream_error = read_source(upstream)
    errors = [error for error in (included_error, upstream_error) if error]
    try:
        same_source = included == upstream or included.samefile(upstream)
    except (OSError, RuntimeError, ValueError):
        same_source = included == upstream
    if same_source:
        errors.append("Select an independent upstream file; self-comparison cannot establish parity.")
    status = "ERROR" if errors else "MATCH" if included_bytes == upstream_bytes else "MISMATCH"
    return {
        "schema_version": 1,
        "status": status,
        "comparison": "complete-skill-bytes",
        "included": included_record,
        "upstream": upstream_record,
        "errors": errors,
        "limitations": [LIMITATION],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", required=True, type=Path, help="Independent dtp-tda-report SKILL.md source")
    arguments = parser.parse_args()
    result = check_parity(arguments.upstream)
    print(json.dumps(result, indent=2))
    return {"MATCH": 0, "MISMATCH": 1, "ERROR": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
