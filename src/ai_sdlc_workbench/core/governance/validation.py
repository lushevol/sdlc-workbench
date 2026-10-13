"""Validate recorded knowledge metadata without changing or approving assets."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

import yaml

from ..context.catalogs import UniqueKeyLoader
from ...models import WorkbenchError, validate_arguments
from .schemas import AUDIT_EVENT_SCHEMA, DOCUMENT_SCHEMAS, HEADINGS, RAW_MANIFEST_SCHEMA


_MAX_BYTES = 1024 * 1024
_EXCLUDED = {"templates", "examples", "schemas", "raw", "audit"}
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z")
_HASH = re.compile(r"[a-f0-9]{64}\Z")
_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\Z")
_TRANSITIONS = {
    "untracked": {"candidate"}, "candidate": {"investigated", "contested", "stale"},
    "investigated": {"verified", "contested", "stale"},
    "verified": {"published", "contested", "stale"},
    "published": {"contested", "stale", "superseded"},
    "contested": {"investigated", "stale", "superseded"},
    "stale": {"investigated", "superseded"}, "superseded": set(),
}


def _timestamp(value):
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value):
        raise WorkbenchError("Use a quoted ISO 8601 timestamp with a timezone.")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise WorkbenchError("Use a valid ISO 8601 timestamp.") from None


def _yaml_object(text):
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
        json.dumps(value, allow_nan=False)
        if not isinstance(value, dict):
            raise WorkbenchError("YAML must contain an object.")
        return value
    except (yaml.YAMLError, TypeError, ValueError, RecursionError):
        raise WorkbenchError("Use unique YAML keys and JSON-compatible values; quote timestamps.") from None


def _read(path):
    try:
        with path.open("rb") as stream:
            raw = stream.read(_MAX_BYTES + 1)
        if len(raw) > _MAX_BYTES:
            raise WorkbenchError("Knowledge records must not exceed one MiB.")
        return raw, raw.decode("utf-8")
    except (OSError, UnicodeError):
        raise WorkbenchError("Use a readable UTF-8 knowledge record.") from None


def _values(value, schema):
    """Reject blank profile fields while leaving extension values unrestricted."""
    if isinstance(value, str) and not value.strip():
        raise WorkbenchError("Required text must not contain only whitespace.")
    if isinstance(value, dict):
        for key, child in schema.get("properties", {}).items():
            if key in value:
                _values(value[key], child)
    elif isinstance(value, list):
        for item in value:
            _values(item, schema.get("items", {}))


def _profile(value, schema):
    validate_arguments(value, schema, "record")
    # Extensions stay unchanged and may include values outside the profile.
    known = {key: value[key] for key in schema["properties"] if key in value}
    _values(known, schema)


def _source(source):
    if not _HASH.fullmatch(source["sha256"]):
        raise WorkbenchError("Source sha256 must contain 64 lowercase hexadecimal characters.")
    return source["resource"], source["revision"], source["sha256"]


def _safe_path(root, value):
    try:
        relative = Path(value)
        target = root / relative
        if (relative.is_absolute() or ".." in relative.parts or
                not target.resolve().is_relative_to(root.resolve())):
            raise WorkbenchError("Paths must stay within the workspace and must not contain '..'.")
        return target
    except (OSError, ValueError, TypeError):
        raise WorkbenchError("Use a valid path within the workspace.") from None


def _body_sections(body):
    sections, current, fence = {}, None, None
    for line in body.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        heading = re.match(r"^##[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$", line) if fence is None else None
        if heading:
            current = heading.group(1).strip().casefold()
            sections.setdefault(current, [])
        elif current is not None and line.strip():
            sections[current].append(line)
    return sections


def validate_knowledge(root: Path) -> dict:
    """Return deterministic findings for knowledge records and recorded gates.

    This function has no mutation path. It cannot establish source truth,
    reviewer identity, or whether a prior audit record was changed or deleted.
    """
    root = Path(root).resolve()
    findings = []
    documents = []

    def report(path, code, message):
        findings.append({"path": str(path.relative_to(root)), "code": code, "message": message})

    def confined(path):
        try:
            _safe_path(root, str(path.relative_to(root)))
            return True
        except WorkbenchError as error:
            report(path, "unsafe_path", str(error))
            return False

    knowledge = root / "knowledge"
    if not knowledge.exists():
        return {"valid": True, "documents": 0, "findings": findings}
    if not confined(knowledge):
        return {"valid": False, "documents": 0, "findings": findings}

    # Revisions are immutable declarations. Snapshots are optional; external
    # resource names are never opened, fetched, or modified by validation.
    manifest_path = knowledge / "raw" / "manifest.yaml"
    source_keys = set()
    source_identities = set()
    if confined(manifest_path) and manifest_path.exists():
        try:
            _, text = _read(manifest_path)
            manifest = _yaml_object(text)
            _profile(manifest, RAW_MANIFEST_SCHEMA)
            for source in manifest["sources"]:
                identity = (source["id"], source["revision"])
                if not _ID.fullmatch(source["id"]) or identity in source_identities:
                    raise WorkbenchError("Each source needs a stable ID and a unique ID/revision pair.")
                source_identities.add(identity)
                key = _source(source)
                if key in source_keys or any(existing[:2] == key[:2] for existing in source_keys):
                    raise WorkbenchError("A source resource/revision must have exactly one manifest record.")
                _timestamp(source["ingested_at"])
                source_keys.add(key)
                if "snapshot" in source:
                    try:
                        snapshot = _safe_path(root, source["snapshot"])
                        if not snapshot.is_file():
                            raise WorkbenchError("The declared source snapshot does not exist.")
                        # Hash original bytes. Do not normalize source text.
                        digest = hashlib.sha256()
                        with snapshot.open("rb") as stream:
                            for block in iter(lambda: stream.read(65536), b""):
                                digest.update(block)
                        if digest.hexdigest() != source["sha256"]:
                            report(manifest_path, "source_hash_mismatch",
                                   f"Source {source['id']} revision {source['revision']} does not match its snapshot hash.")
                    except (WorkbenchError, OSError) as error:
                        report(manifest_path, "source_snapshot_invalid", str(error))
        except WorkbenchError as error:
            report(manifest_path, "manifest_invalid", str(error))

    def check_sources(path, sources):
        for source in sources:
            try:
                key = _source(source)
                if key not in source_keys:
                    raise WorkbenchError("Source resource, revision, and sha256 must match a raw manifest record.")
            except WorkbenchError as error:
                report(path, "source_invalid", str(error))

    events = []
    event_ids = set()
    audit_root = knowledge / "audit"
    if confined(audit_root) and audit_root.exists():
        for path in sorted(audit_root.rglob("*")):
            if not confined(path) or not path.is_file() or path.name == "README.md":
                continue
            if path.suffix.lower() not in {".yaml", ".yml"}:
                report(path, "audit_file_invalid", "Store each audit event in a separate YAML file.")
                continue
            try:
                _, text = _read(path)
                event = _yaml_object(text)
                _profile(event, AUDIT_EVENT_SCHEMA)
                if (not _ID.fullmatch(event["id"]) or not _ID.fullmatch(event["item_id"]) or
                        event["id"] in event_ids or path.stem != event["id"]):
                    raise WorkbenchError("Use a unique audit ID as the event filename and a valid item ID.")
                event_ids.add(event["id"])
                _timestamp(event["at"])
                if not _HASH.fullmatch(event["content_sha256"]):
                    raise WorkbenchError("Audit content_sha256 must contain 64 lowercase hexadecimal characters.")
                if event["action"] == "approval" and not re.fullmatch(r"human:[A-Za-z0-9][A-Za-z0-9_.@-]*", event["actor"]):
                    raise WorkbenchError("Approval events must declare an actor in the form human:<id>.")
                if event["action"] == "transition" and event["to_state"] not in _TRANSITIONS[event["from_state"]]:
                    raise WorkbenchError("The audit state transition is not permitted.")
                if event["action"] == "approval" and (event["from_state"] != "verified" or
                                                       event["to_state"] not in {"verified", "published"}):
                    raise WorkbenchError("Human approval must refer to a verified item.")
                check_sources(path, event["evidence"])
                events.append(event)
            except WorkbenchError as error:
                report(path, "audit_invalid", str(error))

    identities = set()
    for path in sorted(knowledge.rglob("*")):
        relative = path.relative_to(knowledge)
        if relative.parts[0] in _EXCLUDED or path.name in {"README.md", "index.md", "log.md"}:
            continue
        if not confined(path) or not path.is_file() or path.suffix.lower() != ".md":
            continue
        documents.append(path)
        try:
            raw, text = _read(path)
            match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z", text, re.DOTALL)
            if not match:
                raise WorkbenchError("Start a knowledge document with YAML frontmatter between '---' lines.")
            metadata = _yaml_object(match.group(1))
            kind = metadata.get("type")
            if kind not in DOCUMENT_SCHEMAS:
                raise WorkbenchError("Use a supported Workbench knowledge type.")
            _profile(metadata, DOCUMENT_SCHEMAS[kind])
            if not _ID.fullmatch(metadata["id"]):
                raise WorkbenchError("Use a stable document ID without path separators.")
            identity = metadata["id"], metadata["version"]
            if identity in identities:
                raise WorkbenchError("A document ID/version pair must occur once.")
            identities.add(identity)
            generated_at = _timestamp(metadata["generated"]["at"])
            for verifier in metadata["verified"]:
                if _timestamp(verifier["at"]) < generated_at:
                    raise WorkbenchError("Verification must occur at or after generation of this version.")
            check_sources(path, metadata["sources"])
            if kind == "GovernanceFinding":
                check_sources(path, metadata["evidence"])
            sections = _body_sections(match.group(2))
            missing = [heading for heading in HEADINGS[kind] if not sections.get(heading.casefold())]
            if missing:
                raise WorkbenchError("Add required body headings: " + ", ".join(missing) + ".")
            if kind == "Requirement":
                criterion_ids = set()
                for criterion in metadata["acceptance_criteria"]:
                    if not _ID.fullmatch(criterion["id"]) or criterion["id"] in criterion_ids:
                        raise WorkbenchError("Acceptance criterion IDs must be valid and unique.")
                    criterion_ids.add(criterion["id"])
                    for field, keyword in (("given", "Given"), ("when", "When"), ("then", "Then")):
                        if not re.match(rf"{keyword}\s+\S", criterion[field]):
                            raise WorkbenchError("Each acceptance criterion must use Given, When, and Then clauses.")
            state = metadata["governance_state"]
            digest = hashlib.sha256(raw).hexdigest()
            matching = [event for event in events if
                        (event["item_id"], event["item_version"], event["content_sha256"]) ==
                        (*identity, digest) and _timestamp(event["at"]) >= generated_at]
            if state != "candidate" and not any(event["action"] == "transition" and
                                                 event["to_state"] == state for event in matching):
                report(path, "audit_state_missing", "Record a transition for the current ID, version, state, and file hash.")
            if state in {"verified", "published"}:
                verifications = [event for event in matching if event["action"] == "transition" and
                                 event["to_state"] == "verified"]
                bound = [verifier for verifier in metadata["verified"] if any(
                    event["actor"] == verifier["by"] and _timestamp(event["at"]) == _timestamp(verifier["at"])
                    for event in verifications)]
                if not bound:
                    report(path, "verification_missing", "Record verification metadata and a matching verification audit event for this file hash.")
            if state == "published" and kind in {"Requirement", "Decision"}:
                approvals = [(event["actor"], _timestamp(event["at"])) for event in matching
                             if event["action"] == "approval" and event["actor"].startswith("human:")]
                verifications = [(verifier["by"], _timestamp(verifier["at"])) for verifier in bound]
                publication_times = [_timestamp(event["at"]) for event in matching
                                     if event["action"] == "transition" and event["to_state"] == "published"]
                if not any(actor == reviewer and verified <= approved <= published
                           for reviewer, verified in verifications for actor, approved in approvals
                           for published in publication_times):
                    report(path, "human_approval_missing", "Record human verification and approval by the same actor for the current requirement or decision version and file hash.")
        except (WorkbenchError, TypeError) as error:
            report(path, "document_invalid", str(error))

    findings.sort(key=lambda item: (item["path"], item["code"], item["message"]))
    return {"valid": not findings, "documents": len(documents), "findings": findings}
