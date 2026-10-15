#!/usr/bin/env python3
"""Validate repository evidence paths/line references/revision; does NOT assess semantic truth."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

STATUSES = {"observed", "inferred", "conflicting", "unknown"}
KINDS = {"source", "test", "contract", "configuration", "documentation", "runtime-artifact"}
COMMIT_ID = re.compile(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\Z")


def git(repo: Path, *args: str) -> bytes | None:
    try:
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_LITERAL_PATHSPECS": "1"})
        p = subprocess.run(
            ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(repo), *args],
            capture_output=True, timeout=5, env=environment,
        )
        return p.stdout if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def git_head(repo: Path) -> str | None:
    result = git(repo, "rev-parse", "HEAD")
    return result.decode("ascii", errors="replace").strip() if result is not None else None


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
    else:
        try:
            if "\x00" in declared_path or Path(declared_path).expanduser().resolve() != repo:
                errors.append("repository.path does not match --repo")
        except (OSError, ValueError, RuntimeError):
            errors.append("repository.path is not a usable checkout path")
    revision = info.get("revision")
    revision_valid = isinstance(revision, str) and COMMIT_ID.fullmatch(revision) is not None
    if not revision_valid:
        errors.append("repository.revision must be a full 40-character or 64-character Git commit ID")
    root = git(repo, "rev-parse", "--show-toplevel")
    if root is None:
        errors.append("cannot confirm Git checkout root")
    elif Path(os.fsdecode(root).strip()).resolve() != repo:
        errors.append("--repo must identify the Git checkout root, not a subdirectory")
    current = git_head(repo)
    if not current:
        errors.append("cannot confirm current Git revision")
    elif revision != current:
        errors.append(f"report revision differs from checked-out HEAD ({current})")
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
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f"{prefix}: invalid status {status!r}")
            status = None
        evidences = claim.get("evidence", [])
        if not isinstance(evidences, list):
            errors.append(f"{prefix}: evidence must be an array")
            continue
        if status in {"observed", "inferred"} and not evidences:
            errors.append(f"{prefix}: {status} claim lacks evidence")
        if status == "conflicting" and len(evidences) < 2:
            errors.append(f"{prefix}: conflicting claim needs at least two evidence items")
        reason = claim.get("reason")
        if status in {"inferred", "conflicting", "unknown"} and (not isinstance(reason, str) or not reason.strip()):
            errors.append(f"{prefix}: reason required for {status} claim")
        for index, ev in enumerate(evidences, 1):
            ref = f"{prefix}.evidence[{index}]"
            if not isinstance(ev, dict):
                errors.append(f"{ref}: must be an object")
                continue
            raw = ev.get("path")
            if not isinstance(raw, str) or not raw or "\x00" in raw or "\\" in raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw) or any(part in {"", ".", ".."} for part in raw.split("/")):
                errors.append(f"{ref}: path must be a safe POSIX-style repo-relative file path")
                continue
            p = repo / raw
            if any((repo.joinpath(*Path(raw).parts[:n])).is_symlink() for n in range(1, len(Path(raw).parts) + 1)):
                errors.append(f"{ref}: evidence paths must not contain symlinks")
                continue
            if not is_within(repo, p) or not p.is_file():
                errors.append(f"{ref}: file does not exist inside the repository: {raw}")
                continue
            kind = ev.get("kind")
            if not isinstance(kind, str) or kind not in KINDS:
                errors.append(f"{ref}: invalid evidence kind")
            start, end = ev.get("start_line"), ev.get("end_line")
            if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool) or start < 1 or end < start:
                errors.append(f"{ref}: invalid inclusive line range")
                continue
            try:
                if not revision_valid or revision != current:
                    continue
                tree = git(repo, "ls-tree", "-z", "--full-tree", revision, "--", raw)
                entries = tree.rstrip(b"\x00").split(b"\x00") if tree else []
                if len(entries) != 1:
                    errors.append(f"{ref}: file is not tracked at the report revision: {raw}")
                    continue
                metadata, tracked_path = entries[0].split(b"\t", 1)
                mode, object_type, object_id = metadata.split(b" ", 2)
                if mode not in {b"100644", b"100755"} or object_type != b"blob" or os.fsdecode(tracked_path) != raw:
                    errors.append(f"{ref}: evidence must be a tracked regular file: {raw}")
                    continue
                before = p.stat()
                digest = hashlib.sha1() if len(object_id) == 40 else hashlib.sha256()
                digest.update(f"blob {before.st_size}\x00".encode("ascii"))
                line_count = 0
                last_byte = b""
                with p.open("rb") as source:
                    for chunk in iter(lambda: source.read(65536), b""):
                        digest.update(chunk)
                        line_count += chunk.count(b"\n")
                        last_byte = chunk[-1:]
                after = p.stat()
                if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino) or digest.hexdigest().encode("ascii") != object_id:
                    errors.append(f"{ref}: file bytes differ from the report revision: {raw}")
                    continue
                if last_byte and last_byte != b"\n":
                    line_count += 1
                if end > line_count:
                    errors.append(f"{ref}: lines {start}-{end} exceed {raw} length ({line_count})")
            except (OSError, ValueError) as exc:
                errors.append(f"{ref}: cannot inspect file: {exc}")
    if current and git_head(repo) != current:
        errors.append("checked-out HEAD changed during evidence validation")
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
