#!/usr/bin/env python3
"""Validate source citations and optional dependency structure, not semantic truth or runtime behavior."""
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
DEPENDENCY_PROFILE = "external-dependencies/1"
DEPENDENCY_FAMILIES = {
    "api", "messaging", "managed-events", "data", "identity", "trust", "configuration",
    "storage", "network", "platform", "scheduling", "observability", "frontend",
    "business-provider", "delivery", "other",
}
DEPENDENCY_DIRECTIONS = {"inbound", "outbound", "bidirectional", "local"}
DEPENDENCY_PHASES = {"runtime", "build", "test", "deployment", "configuration"}
COVERAGE_STATUSES = {"inspected", "not-observed", "unknown", "out-of-scope"}
DEPENDENCY_ATTRIBUTES = {
    "component", "peer", "protocol", "operation", "environment", "activation", "trigger",
    "conditions", "timing", "interaction", "authentication", "authorization", "network_access",
    "configuration", "resilience", "impact", "criticality", "family_details",
}


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_ids(value: object, prefix: str, errors: list[str]) -> list[str]:
    """Check ID arrays without assuming that malformed input is hashable."""
    if not isinstance(value, list):
        errors.append(f"{prefix}: must be an array of unique nonempty strings")
        return []
    identifiers = []
    seen = set()
    for index, ident in enumerate(value, 1):
        if not nonempty_string(ident):
            errors.append(f"{prefix}[{index}]: must be a nonempty string")
        elif ident in seen:
            errors.append(f"{prefix}[{index}]: duplicate id {ident}")
        else:
            seen.add(ident)
            identifiers.append(ident)
    return identifiers


def claim_citations(claim: dict) -> set[tuple[str, int, int]]:
    """Return citation identities; changing the evidence kind does not create a new citation."""
    evidence = claim.get("evidence")
    if not isinstance(evidence, list):
        return set()
    citations = set()
    for item in evidence:
        if not isinstance(item, dict):
            continue
        path, start, end = item.get("path"), item.get("start_line"), item.get("end_line")
        if (nonempty_string(path) and isinstance(start, int) and not isinstance(start, bool)
                and isinstance(end, int) and not isinstance(end, bool) and start >= 1 and end >= start):
            citations.add((path, start, end))
    return citations


def validate_attribute(attribute: object, prefix: str, claims: dict[str, dict], errors: list[str]) -> None:
    if not isinstance(attribute, dict):
        errors.append(f"{prefix}: must be an object")
        return
    if "evidence" in attribute:
        errors.append(f"{prefix}: evidence belongs in claims; use claim_ids")
    status = attribute.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        errors.append(f"{prefix}: invalid status {status!r}")
        status = None
    if "value" not in attribute:
        errors.append(f"{prefix}: value required")
    elif status == "unknown":
        if attribute["value"] is not None:
            errors.append(f"{prefix}: unknown value must be null")
    elif status in {"observed", "inferred", "conflicting"} and not nonempty_string(attribute["value"]):
        errors.append(f"{prefix}: {status} value must be a nonempty string")
    if status in {"inferred", "conflicting", "unknown"} and not nonempty_string(attribute.get("reason")):
        errors.append(f"{prefix}: reason required for {status} attribute")
    identifiers = string_ids(attribute.get("claim_ids"), f"{prefix}.claim_ids", errors)
    support = []
    for ident in identifiers:
        if ident not in claims:
            errors.append(f"{prefix}: unknown claim id {ident}")
        else:
            claim = claims[ident]
            claim_status = claim.get("status")
            support.append((claim_status if isinstance(claim_status, str) else None, claim_citations(claim)))
    if status == "observed":
        if any(claim_status == "conflicting" for claim_status, _ in support):
            errors.append(f"{prefix}: observed attribute cannot reference conflicting claims")
        if not any(claim_status == "observed" and citations for claim_status, citations in support):
            errors.append(f"{prefix}: observed attribute needs an observed evidence-bearing claim")
    elif status == "inferred":
        if not any(claim_status in {"observed", "inferred"} and citations for claim_status, citations in support):
            errors.append(f"{prefix}: inferred attribute needs observed or inferred evidence-bearing support")
    elif status == "conflicting":
        conflicting = any(claim_status == "conflicting" and len(citations) >= 2
                          for claim_status, citations in support)
        observations = [citations for claim_status, citations in support
                        if claim_status in {"observed", "inferred"} and citations]
        distinct_citations = set().union(*observations)
        if not conflicting and (len(observations) < 2 or len(distinct_citations) < 2):
            errors.append(f"{prefix}: conflicting attribute needs conflicting evidence or two claims with distinct citations")


def validate_dependency_profile(report: dict, claims: list) -> list[str]:
    errors = []
    extension_keys = {"dependency_profile", "external_dependencies", "dependency_coverage"}
    if not extension_keys.intersection(report):
        return errors
    if report.get("dependency_profile") != DEPENDENCY_PROFILE:
        return [f"dependency_profile must be '{DEPENDENCY_PROFILE}' when dependency extension keys are present"]
    claim_map = {}
    for claim in claims:
        if isinstance(claim, dict) and nonempty_string(claim.get("id")):
            claim_map.setdefault(claim["id"], claim)
    dependencies = report.get("external_dependencies")
    if not isinstance(dependencies, list):
        errors.append("external_dependencies must be an array")
        dependencies = []
    dependency_map = {}
    for index, dependency in enumerate(dependencies, 1):
        prefix = f"external_dependencies[{index}]"
        if not isinstance(dependency, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        if "evidence" in dependency:
            errors.append(f"{prefix}: evidence belongs in claims; use attribute claim_ids")
        ident = dependency.get("id")
        if not nonempty_string(ident):
            errors.append(f"{prefix}: id required")
        elif ident in dependency_map:
            errors.append(f"{prefix}: duplicate id {ident}")
        else:
            dependency_map[ident] = dependency
        for field, choices in (("family", DEPENDENCY_FAMILIES), ("direction", DEPENDENCY_DIRECTIONS),
                               ("phase", DEPENDENCY_PHASES)):
            value = dependency.get(field)
            if not isinstance(value, str) or value not in choices:
                errors.append(f"{prefix}: invalid {field} {value!r}")
        review = dependency.get("review")
        if not isinstance(review, dict):
            errors.append(f"{prefix}.review: must be an object")
        else:
            for field in ("owner", "next_action"):
                if not nonempty_string(review.get(field)):
                    errors.append(f"{prefix}.review.{field}: nonempty string required")
        attributes = dependency.get("attributes")
        if not isinstance(attributes, dict):
            errors.append(f"{prefix}.attributes: must be an object")
            continue
        for field in sorted(DEPENDENCY_ATTRIBUTES - attributes.keys()):
            errors.append(f"{prefix}.attributes.{field}: required attribute missing")
        for field, attribute in attributes.items():
            if not nonempty_string(field):
                errors.append(f"{prefix}.attributes: attribute names must be nonempty strings")
            validate_attribute(attribute, f"{prefix}.attributes.{field}", claim_map, errors)
    coverage = report.get("dependency_coverage")
    if not isinstance(coverage, list):
        errors.append("dependency_coverage must be an array")
        coverage = []
    families = set()
    references = {ident: 0 for ident in dependency_map}
    for index, entry in enumerate(coverage, 1):
        prefix = f"dependency_coverage[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        if "evidence" in entry:
            errors.append(f"{prefix}: evidence belongs in claims")
        family = entry.get("family")
        valid_family = isinstance(family, str) and family in DEPENDENCY_FAMILIES
        if not valid_family:
            errors.append(f"{prefix}: invalid family {family!r}")
        elif family in families:
            errors.append(f"{prefix}: duplicate family {family}")
        else:
            families.add(family)
        status = entry.get("status")
        if not isinstance(status, str) or status not in COVERAGE_STATUSES:
            errors.append(f"{prefix}: invalid status {status!r}")
            status = None
        scope = entry.get("scope")
        if not isinstance(scope, list) or not scope or any(not nonempty_string(item) for item in scope):
            errors.append(f"{prefix}.scope: nonempty string array required")
        if not nonempty_string(entry.get("reason")):
            errors.append(f"{prefix}.reason: nonempty string required")
        identifiers = string_ids(entry.get("dependency_ids"), f"{prefix}.dependency_ids", errors)
        if status in {"not-observed", "out-of-scope"} and identifiers:
            errors.append(f"{prefix}: {status} coverage must not reference dependencies")
        if status == "inspected" and not identifiers:
            errors.append(f"{prefix}: inspected coverage needs at least one dependency; use not-observed for no findings")
        for ident in identifiers:
            if ident not in dependency_map:
                errors.append(f"{prefix}: unknown dependency id {ident}")
            elif not valid_family or dependency_map[ident].get("family") != family:
                errors.append(f"{prefix}: dependency {ident} belongs to a different family")
            else:
                references[ident] += 1
    for family in sorted(DEPENDENCY_FAMILIES - families):
        errors.append(f"dependency_coverage: missing family {family}")
    for ident, count in references.items():
        if count != 1:
            errors.append(f"dependency_coverage: dependency {ident} must appear once in its family coverage (found {count})")
    return errors


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
    errors.extend(validate_dependency_profile(report, claims))
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
    if report.get("dependency_profile") == DEPENDENCY_PROFILE:
        print(f"Dependency profile structural validation passed ({len(report['external_dependencies'])} dependencies).")
    else:
        print("Legacy report: dependency profile structure was not checked.")
    print("NOTE: This does not validate completeness, semantic accuracy, effective permissions, or runtime behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
