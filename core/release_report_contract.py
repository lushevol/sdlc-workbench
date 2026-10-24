"""Versioned, hash-bound release report snapshots shared by collection and rendering."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import tempfile
from datetime import datetime, timezone

from .models import WorkbenchError

SCHEMA_VERSION = 1
_COLLECTION_STATES = {"complete", "partial", "failed"}
_ARRAY_FIELDS = {"builds", "workitems", "tests", "defects", "coverage", "sonarqube", "warnings", "errors", "evidence"}
_OBJECT_FIELDS = {"graph", "compliance", "metrics"}


def _invalid(message: str) -> WorkbenchError:
    return WorkbenchError(f"Invalid release report: {message}")


def _pairs(values):
    result = {}
    for key, value in values:
        if key in result:
            raise _invalid("JSON contains duplicate keys.")
        result[key] = value
    return result


def _nonfinite(value):
    raise _invalid("JSON contains a non-finite value.")


def _decode_json(raw: bytes) -> dict:
    try:
        result = json.loads(raw.decode("utf-8"), parse_constant=_nonfinite, object_pairs_hook=_pairs)
    except WorkbenchError:
        raise
    except (UnicodeError, ValueError, RecursionError) as error:
        raise _invalid("JSON input cannot be read.") from error
    if not isinstance(result, dict):
        raise _invalid("JSON input must contain an object.")
    return result


def read_json(path: str | Path) -> dict:
    """Read a finite JSON object; malformed input never falls back to an empty report."""
    try:
        raw = Path(path).read_bytes()
    except OSError as error:
        raise _invalid("JSON input cannot be read.") from error
    return _decode_json(raw)


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    try:
        with Path(path).open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as error:
        raise _invalid("A retained artifact cannot be read.") from error
    return digest.hexdigest()


def confined_artifact(root: str | Path, value: str) -> Path:
    """Resolve a portable relative artifact without following a symlink or parent escape."""
    if (not isinstance(value, str) or not value or "\x00" in value or "\\" in value or
            ":" in value or PureWindowsPath(value).drive):
        raise _invalid("Artifact paths must be portable relative paths.")
    relative = PurePosixPath(value)
    if relative.is_absolute() or any(part in {"..", "."} for part in relative.parts) or value in {".", ""}:
        raise _invalid("An artifact path leaves the report directory.")
    base = Path(root).resolve()
    candidate = base
    for part in relative.parts:
        candidate /= part
        if candidate.is_symlink():
            raise _invalid("Artifact symlinks are not permitted.")
    if not candidate.resolve().is_relative_to(base):
        raise _invalid("An artifact path leaves the report directory.")
    return candidate


def artifact_record(path: str | Path, root: str | Path) -> dict:
    """Describe an existing artifact relative to its report directory."""
    base = Path(root).resolve()
    item = Path(path)
    try:
        relative = item.absolute().relative_to(base).as_posix()
    except ValueError as error:
        raise _invalid("An artifact is outside the report directory.") from error
    target = confined_artifact(base, relative)
    if not target.is_file():
        raise _invalid("A retained artifact is not a regular file.")
    return {"path": relative, "sha256": sha256_file(target), "bytes": target.stat().st_size}


def verify_artifact(root: str | Path, record: dict) -> Path:
    if not isinstance(record, dict):
        raise _invalid("Artifact metadata must contain an object.")
    size, checksum = record.get("bytes"), record.get("sha256")
    if (isinstance(size, bool) or not isinstance(size, int) or size < 0 or
            not isinstance(checksum, str) or re.fullmatch(r"[0-9a-f]{64}", checksum) is None):
        raise _invalid("Artifact size or SHA-256 is invalid.")
    target = confined_artifact(root, record.get("path"))
    try:
        if not target.is_file() or target.stat().st_size != size:
            raise _invalid("A retained artifact is missing or its size changed.")
        if sha256_file(target) != checksum:
            raise _invalid("A retained artifact SHA-256 does not match.")
    except OSError as error:
        raise _invalid("A retained artifact cannot be inspected.") from error
    return target


def validate_snapshot(snapshot: dict) -> None:
    if not isinstance(snapshot, dict) or type(snapshot.get("schema_version")) is not int or snapshot["schema_version"] != SCHEMA_VERSION:
        raise _invalid("The snapshot schema version is unsupported.")
    if not isinstance(snapshot.get("collection_status"), str) or snapshot["collection_status"] not in _COLLECTION_STATES:
        raise _invalid("The collection status is invalid.")
    source = snapshot.get("source")
    if not isinstance(source, dict) or not isinstance(snapshot.get("release"), dict):
        raise _invalid("Source and release records are required objects.")
    identifier = source.get("release_id")
    def identity(value):
        if isinstance(value, bool) or not (isinstance(value, int) or isinstance(value, str) and value.isdecimal()):
            return None
        try:
            number = int(value)
            return number if number > 0 else None
        except ValueError:
            return None
    if identity(identifier) is None:
        raise _invalid("A positive release work item identity is required.")
    release = snapshot["release"]
    if "id" in release and identity(release["id"]) != identity(identifier):
        raise _invalid("The returned release identity does not match its source.")
    if source.get("revision") is not None and release.get("rev") is not None:
        if identity(source["revision"]) is None or identity(source["revision"]) != identity(release["rev"]):
            raise _invalid("The returned release revision does not match its source.")
    try:
        stamp = datetime.fromisoformat(snapshot["generated_at"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() != timezone.utc.utcoffset(stamp):
            raise ValueError("UTC is required")
    except (KeyError, AttributeError, TypeError, ValueError) as error:
        raise _invalid("generated_at must identify a UTC time.") from error
    for name in _ARRAY_FIELDS:
        if name in snapshot and not isinstance(snapshot[name], list):
            raise _invalid(f"{name} must contain an array.")
    for name in _OBJECT_FIELDS:
        if name in snapshot and not isinstance(snapshot[name], dict):
            raise _invalid(f"{name} must contain an object.")
    for name in ("builds", "workitems", "sonarqube"):
        if any(not isinstance(item, dict) for item in snapshot.get(name, [])):
            raise _invalid(f"{name} entries must contain objects.")
    try:
        json.dumps(snapshot, allow_nan=False)
    except (ValueError, TypeError, RecursionError) as error:
        raise _invalid("The snapshot must contain finite JSON values.") from error


def load_report_bundle(manifest_path: str | Path) -> tuple[dict, dict, Path]:
    """Validate a manifest, snapshot, and every declared evidence artifact."""
    original = Path(manifest_path).expanduser()
    if original.is_symlink():
        raise _invalid("The manifest must not be a symlink.")
    manifest_file = original.resolve()
    manifest = read_json(manifest_file)
    if type(manifest.get("schema_version")) is not int or manifest["schema_version"] != SCHEMA_VERSION:
        raise _invalid("The manifest schema version is unsupported.")
    root = manifest_file.parent
    snapshot_record = manifest.get("snapshot")
    snapshot_path = verify_artifact(root, snapshot_record)
    try:
        raw_snapshot = snapshot_path.read_bytes()
    except OSError as error:
        raise _invalid("The snapshot cannot be read.") from error
    if (len(raw_snapshot) != snapshot_record["bytes"] or
            hashlib.sha256(raw_snapshot).hexdigest() != snapshot_record["sha256"]):
        raise _invalid("The snapshot changed while it was read.")
    snapshot = _decode_json(raw_snapshot)
    validate_snapshot(snapshot)
    for name in ("source", "collection_status", "generated_at"):
        if name in manifest and manifest[name] != snapshot[name]:
            raise _invalid("Manifest identity does not match the snapshot.")
    seen = {snapshot_path: (snapshot_record["bytes"], snapshot_record["sha256"])}
    for records in (manifest.get("evidence", []), snapshot.get("evidence", [])):
        if not isinstance(records, list):
            raise _invalid("Evidence metadata must contain an array.")
        for record in records:
            if not isinstance(record, dict):
                raise _invalid("Artifact metadata must contain an object.")
            target = confined_artifact(root, record.get("path"))
            identity = (record.get("bytes"), record.get("sha256"))
            if target in seen:
                if seen[target] != identity or type(record.get("bytes")) is not int:
                    raise _invalid("Conflicting artifact identities are declared.")
                continue
            verify_artifact(root, record)
            seen[target] = identity
    return snapshot, manifest, root


def read_release_report(manifest_path: str | Path) -> dict:
    """Return verified saved report data without credentials or external access."""
    return load_report_bundle(manifest_path)[0]


def _write_json(path: Path, value: dict) -> None:
    data = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".release-report-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_report_snapshot(directory: str | Path, snapshot: dict, evidence: list[dict]) -> Path:
    """Save one new snapshot beside completed evidence and return its manifest path."""
    validate_snapshot(snapshot)
    root = Path(directory).resolve()
    root.mkdir(parents=True, exist_ok=True)
    snapshot_path, manifest_path = root / "snapshot.json", root / "manifest.json"
    if snapshot_path.exists() or manifest_path.exists():
        raise _invalid("Select a new directory for a report snapshot.")
    if not isinstance(evidence, list):
        raise _invalid("Evidence metadata must contain an array.")
    for record in evidence:
        verify_artifact(root, record)
    saved = json.loads(json.dumps(snapshot, allow_nan=False))
    saved["evidence"] = evidence
    _write_json(snapshot_path, saved)
    manifest = {"schema_version": SCHEMA_VERSION, "source": saved["source"],
                "collection_status": saved["collection_status"], "generated_at": saved["generated_at"],
                "snapshot": artifact_record(snapshot_path, root), "evidence": evidence,
                "metrics": saved.get("metrics", {})}
    _write_json(manifest_path, manifest)
    return manifest_path
