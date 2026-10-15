#!/usr/bin/env python3
"""Validate repository evidence paths/line references/revision; does NOT assess semantic truth."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

STATUSES = {"verified", "inferred", "conflicting", "unknown"}
KINDS = {"source", "test", "contract", "configuration", "documentation", "runtime-artifact"}
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")


def git_head(repo: Path) -> str | None:
    try:
        p = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True, capture_output=True, timeout=5)
        return p.stdout.strip() if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def git_dirty(repo: Path) -> bool | None:
    try:
        p = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=normal"], text=True, capture_output=True, timeout=5)
        return bool(p.stdout.strip()) if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def is_within(repo: Path, candidate: Path) -> bool:
    try:
        return os.path.commonpath([str(repo), str(candidate)]) == str(repo)
    except ValueError:
        return False


def validate(repo: Path, report: dict) -> list[str]:
    errors = []
    if report.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    info = report.get("repository")
    if not isinstance(info, dict):
        return errors + ["repository must be an object"]
    declared_path = info.get("path")
    if not isinstance(declared_path, str) or not declared_path.strip():
        errors.append("repository.path must identify the checkout being validated")
    elif Path(declared_path).expanduser().resolve() != repo:
        errors.append("repository.path does not match --repo")
    revision = info.get("revision")
    if not isinstance(revision, str) or not SHA40.fullmatch(revision):
        errors.append("repository.revision must be a real 40-character commit SHA")
    current = git_head(repo)
    if not current:
        errors.append("cannot confirm current Git revision")
    elif revision != current:
        errors.append(f"report revision differs from checked-out HEAD ({current})")
    dirty = git_dirty(repo)
    if dirty is None:
        errors.append("cannot determine whether working tree is clean")
    elif dirty:
        errors.append("working tree is dirty; exact revision cannot attest current line evidence")
    claims = report.get("claims")
    if not isinstance(claims, list):
        return errors + ["claims must be an array"]
    ids = set()
    for n, claim in enumerate(claims, 1):
        prefix = f"claims[{n}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        ident = claim.get("id")
        if not isinstance(ident, str) or not ident.strip():
            errors.append(f"{prefix}: id required")
        elif ident in ids:
            errors.append(f"{prefix}: duplicate id {ident}")
        else:
            ids.add(ident)
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            errors.append(f"{prefix}: statement required")
        if not isinstance(claim.get("category"), str) or not claim["category"].strip():
            errors.append(f"{prefix}: category required")
        status = claim.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix}: invalid status {status!r}")
        evidences = claim.get("evidence", [])
        if not isinstance(evidences, list):
            errors.append(f"{prefix}: evidence must be an array")
            continue
        if status == "verified" and not evidences:
            errors.append(f"{prefix}: verified claim lacks evidence")
        if status == "conflicting" and len(evidences) < 2:
            errors.append(f"{prefix}: conflicting claim needs at least two evidence items")
        if status in {"inferred", "conflicting", "unknown"} and not str(claim.get("reason", "")).strip():
            errors.append(f"{prefix}: reason required for {status} claim")
        for index, ev in enumerate(evidences, 1):
            ref = f"{prefix}.evidence[{index}]"
            if not isinstance(ev, dict):
                errors.append(f"{ref}: must be an object")
                continue
            raw = ev.get("path")
            if not isinstance(raw, str) or not raw or "\\" in raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw) or ".." in Path(raw).parts:
                errors.append(f"{ref}: path must be a safe POSIX-style repo-relative file path")
                continue
            p = (repo / raw).resolve()
            if not is_within(repo, p) or not p.is_file():
                errors.append(f"{ref}: file does not exist inside the repository: {raw}")
                continue
            if ev.get("kind") not in KINDS:
                errors.append(f"{ref}: invalid evidence kind")
            start, end = ev.get("start_line"), ev.get("end_line")
            if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool) or start < 1 or end < start:
                errors.append(f"{ref}: invalid inclusive line range")
                continue
            try:
                with p.open("rb") as source:
                    # Only count bytes/newlines, no source content leaves the machine.
                    line_count = sum(chunk.count(b"\n") for chunk in iter(lambda: source.read(65536), b""))
                if p.stat().st_size > 0:
                    with p.open("rb") as source:
                        source.seek(-1, os.SEEK_END)
                        if source.read(1) != b"\n":
                            line_count += 1
                if end > line_count:
                    errors.append(f"{ref}: lines {start}-{end} exceed {raw} length ({line_count})")
            except OSError as exc:
                errors.append(f"{ref}: cannot inspect file: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        parser.error("repository not found")
    try:
        report = json.loads(Path(args.report).expanduser().read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        parser.error(f"could not read report JSON: {exc}")
    if not isinstance(report, dict):
        parser.error("report root must be an object")
    errors = validate(repo, report)
    if errors:
        for msg in errors:
            print("FAIL:", msg, file=sys.stderr)
        print(f"Validation failed ({len(errors)} issues)", file=sys.stderr)
        return 1
    print(f"Evidence reference validation passed ({len(report['claims'])} claims).")
    print("NOTE: This does not validate semantic accuracy or runtime behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
