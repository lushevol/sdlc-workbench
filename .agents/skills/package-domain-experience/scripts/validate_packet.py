#!/usr/bin/env python3
"""Validate one domain experience packet without changing it."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml


HASH = re.compile(r"[0-9a-f]{64}\Z")
IDENTIFIER = re.compile(r"exp\.[A-Za-z0-9][A-Za-z0-9._-]*\.v[1-9][0-9]*\Z")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:ghp|github_pat|xox[baprs])_[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"https?://[^\s/@:]+:[^\s/@]+@"),
)
STATUSES = {"observed", "replayed", "reviewed", "retired"}
CLASSIFICATIONS = {"public", "redacted", "synthetic", "private-reference"}
PROMOTION_KINDS = {"guide", "skill", "runtime-skill", "script"}
PROMOTION_ACTIONS = {"add", "update"}
MAX_FILE_BYTES = 8 * 1024 * 1024


def _safe_relative(value: object) -> bool:
    return (isinstance(value, str) and bool(value) and not value.startswith("/")
            and "\\" not in value and all(part not in {"", ".", ".."} for part in value.split("/")))


def _workbench_target(value: object) -> bool:
    if not _safe_relative(value):
        return False
    return value == "AGENTS.md" or value.startswith((".agents/skills/", "core/skills/", "scripts/"))


def _text(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if len(raw) > MAX_FILE_BYTES or b"\0" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _sha256(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def validate(packet: Path, workspace: Path | None = None) -> list[str]:
    errors: list[str] = []
    manifest_path = packet / "manifest.yaml"
    experience_path = packet / "experience.md"
    if not packet.is_dir():
        return ["packet: directory required"]
    if not manifest_path.is_file():
        errors.append("manifest.yaml: file required")
        return errors
    if not experience_path.is_file():
        errors.append("experience.md: file required")
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return [f"manifest.yaml: invalid YAML ({error.__class__.__name__})"]
    if not isinstance(manifest, dict):
        return ["manifest.yaml: mapping required"]

    required = {"schema_version", "id", "title", "domain", "status", "applies_when", "retrospective", "requires",
                "provenance", "verification", "assets", "knowledge", "promotions", "security", "limits"}
    for key in sorted(required - set(manifest)):
        errors.append(f"manifest.{key}: required")
    if manifest.get("schema_version") != 1:
        errors.append("manifest.schema_version: version 1 required")
    if not isinstance(manifest.get("id"), str) or IDENTIFIER.fullmatch(manifest.get("id", "")) is None:
        errors.append("manifest.id: use exp.<domain>.<slug>.v<positive integer>")
    for key in ("title", "domain"):
        if not isinstance(manifest.get(key), str) or not manifest.get(key, "").strip():
            errors.append(f"manifest.{key}: nonempty text required")
    if manifest.get("status") not in STATUSES:
        errors.append("manifest.status: use observed, replayed, reviewed, or retired")
    for key in ("applies_when", "limits"):
        if not isinstance(manifest.get(key), list):
            errors.append(f"manifest.{key}: list required")
    retrospective = manifest.get("retrospective")
    if not isinstance(retrospective, dict) or set(retrospective) != {"summary", "successful_path", "reusable_reason", "discarded"}:
        errors.append("manifest.retrospective: summary, successful_path, reusable_reason, and discarded required")
    elif any(not isinstance(retrospective.get(key), str) or not retrospective[key].strip()
             for key in ("summary", "successful_path", "reusable_reason")):
        errors.append("manifest.retrospective: summary, successful_path, and reusable_reason must be nonempty")
    elif not isinstance(retrospective.get("discarded"), list) or not all(isinstance(item, str) for item in retrospective["discarded"]):
        errors.append("manifest.retrospective.discarded: list of strings required")
    requires = manifest.get("requires")
    if not isinstance(requires, dict):
        errors.append("manifest.requires: mapping required")
    else:
        for key in ("tools", "variables"):
            if not isinstance(requires.get(key), list) or not all(isinstance(item, str) and item.strip() for item in requires[key]):
                errors.append(f"manifest.requires.{key}: list of nonempty strings required")

    provenance = manifest.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("manifest.provenance: mapping required")
    else:
        if not isinstance(provenance.get("task_id"), str) or not provenance.get("task_id", "").strip():
            errors.append("manifest.provenance.task_id: nonempty text required")
        evidence = provenance.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append("manifest.provenance.evidence: nonempty list required")
        else:
            for index, record in enumerate(evidence):
                prefix = f"manifest.provenance.evidence[{index}]"
                if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
                    errors.append(f"{prefix}: path and sha256 required")
                    continue
                if not _safe_relative(record["path"]):
                    errors.append(f"{prefix}.path: workspace-relative path required")
                if not isinstance(record["sha256"], str) or HASH.fullmatch(record["sha256"]) is None:
                    errors.append(f"{prefix}.sha256: lowercase SHA-256 required")
                if workspace is not None and _safe_relative(record["path"]):
                    evidence_path = workspace / record["path"]
                    if evidence_path.exists() and not evidence_path.resolve().is_relative_to(workspace.resolve()):
                        errors.append(f"{prefix}.path: evidence path leaves the workspace")
                        continue
                    actual = _sha256(evidence_path)
                    if actual is None:
                        errors.append(f"{prefix}.path: retained evidence file is unavailable")
                    elif actual != record["sha256"]:
                        errors.append(f"{prefix}.sha256: retained evidence hash does not match")

    verification = manifest.get("verification")
    if not isinstance(verification, dict) or verification.get("outcome") != "successful":
        errors.append("manifest.verification.outcome: successful required")
    elif not all(isinstance(verification.get(key), list) for key in ("conditions", "assertions")):
        errors.append("manifest.verification: conditions and assertions lists required")

    assets = manifest.get("assets")
    referenced: list[str] = []
    if not isinstance(assets, dict):
        errors.append("manifest.assets: mapping required")
    else:
        primary = assets.get("primary")
        if not isinstance(primary, dict) or set(primary) != {"kind", "path"}:
            errors.append("manifest.assets.primary: kind and path required")
        elif primary.get("kind") not in {"script", "workflow", "instructions"} or not _safe_relative(primary.get("path")):
            errors.append("manifest.assets.primary: supported kind and packet-relative path required")
        elif not (packet / primary["path"]).is_file():
            errors.append("manifest.assets.primary.path: referenced file is unavailable")
        else:
            referenced.append(primary["path"])
        procedure = assets.get("procedure")
        if procedure != "experience.md":
            errors.append("manifest.assets.procedure: experience.md required")
        referenced.append("experience.md")
        for key in ("variables",):
            value = assets.get(key)
            if value is not None:
                if not _safe_relative(value):
                    errors.append(f"manifest.assets.{key}: packet-relative path required")
                else:
                    referenced.append(value)
        for key in ("scripts", "fixtures"):
            values = assets.get(key)
            if not isinstance(values, list) or not all(_safe_relative(value) for value in values):
                errors.append(f"manifest.assets.{key}: list of packet-relative paths required")
            else:
                referenced.extend(values)

    promotions = manifest.get("promotions")
    if not isinstance(promotions, list):
        errors.append("manifest.promotions: list required")
    else:
        for index, promotion in enumerate(promotions):
            prefix = f"manifest.promotions[{index}]"
            required_promotion = {"target", "kind", "action", "source", "purpose", "before_sha256", "after_sha256", "checks"}
            if not isinstance(promotion, dict) or set(promotion) != required_promotion:
                errors.append(f"{prefix}: target, kind, action, source, purpose, before_sha256, after_sha256, and checks required")
                continue
            if not _workbench_target(promotion["target"]):
                errors.append(f"{prefix}.target: unsupported Workbench asset target")
            if promotion["kind"] not in PROMOTION_KINDS:
                errors.append(f"{prefix}.kind: unsupported promotion kind")
            if promotion["action"] not in PROMOTION_ACTIONS:
                errors.append(f"{prefix}.action: use add or update")
            if not _safe_relative(promotion["source"]):
                errors.append(f"{prefix}.source: packet-relative path required")
            elif not (packet / promotion["source"]).is_file():
                errors.append(f"{prefix}.source: referenced packet file is unavailable")
            if not isinstance(promotion["purpose"], str) or not promotion["purpose"].strip():
                errors.append(f"{prefix}.purpose: nonempty text required")
            if promotion["before_sha256"] is not None and (not isinstance(promotion["before_sha256"], str)
                                                              or HASH.fullmatch(promotion["before_sha256"]) is None):
                errors.append(f"{prefix}.before_sha256: lowercase SHA-256 or null required")
            if promotion["action"] == "update" and promotion["before_sha256"] is None:
                errors.append(f"{prefix}.before_sha256: existing targets require a before hash")
            if promotion["action"] == "add" and promotion["before_sha256"] is not None:
                errors.append(f"{prefix}.before_sha256: new targets require null")
            if not isinstance(promotion["after_sha256"], str) or HASH.fullmatch(promotion["after_sha256"]) is None:
                errors.append(f"{prefix}.after_sha256: lowercase SHA-256 required")
            if not isinstance(promotion["checks"], list) or not all(isinstance(item, str) and item.strip() for item in promotion["checks"]):
                errors.append(f"{prefix}.checks: list of nonempty strings required")
            if workspace is not None and _workbench_target(promotion["target"]):
                target_path = workspace / promotion["target"]
                actual = _sha256(target_path)
                if actual is None:
                    errors.append(f"{prefix}.target: promoted target is unavailable")
                elif actual != promotion["after_sha256"]:
                    errors.append(f"{prefix}.after_sha256: promoted target hash does not match")

    security = manifest.get("security")
    if not isinstance(security, dict) or security.get("classification") not in CLASSIFICATIONS:
        errors.append("manifest.security.classification: supported classification required")
    elif security.get("secrets_present") is not False:
        errors.append("manifest.security.secrets_present: false required")

    for relative in referenced:
        if _safe_relative(relative) and not (packet / relative).is_file():
            errors.append(f"manifest.assets: referenced file is unavailable: {relative}")
    if (packet / "references.yaml").exists() and not (packet / "references.yaml").is_file():
        errors.append("references.yaml: regular file required")

    for path in sorted(packet.rglob("*")):
        if path.is_symlink():
            errors.append(f"{path.relative_to(packet)}: symlinks are not allowed in a packet")
            continue
        if not path.is_file():
            continue
        text = _text(path)
        if text is None:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(packet)}: possible secret or credential pattern")
                break
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="Path to one packet directory")
    parser.add_argument("--workspace", help="Workspace root for evidence hash checks")
    arguments = parser.parse_args(argv)
    errors = validate(Path(arguments.packet).expanduser().resolve(),
                      Path(arguments.workspace).expanduser().resolve() if arguments.workspace else None)
    result = {"status": "PASSED" if not errors else "FAILED", "packet": arguments.packet, "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
