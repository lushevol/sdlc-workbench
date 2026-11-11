"""Retain local source revisions and prepare hash-bound, reviewed source views."""

from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import tempfile

import yaml

from ..context.catalogs import UniqueKeyLoader
from ..governance.schemas import RAW_MANIFEST_SCHEMA
from ..artifact_lint import _FRONTMATTER
from ..governance.validation import _timestamp, is_derived_knowledge_path
from ..models import WorkbenchError, validate_arguments
from ..workspace import load_workspace


_POLICY = ".agents/skills/ingest-knowledge/assets/source-filter.yaml"
_MANIFEST = "evidence/knowledge/manifest.yaml"
_HASH = re.compile(r"[a-f0-9]{64}\Z")
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z")
_DECISIONS = {"KEEP", "KEEP_SECTIONS", "EVIDENCE_ONLY", "EXCLUDE", "HOLD"}
_SOURCE_KEYS = {"id", "resource", "revision", "sha256", "snapshot"}
_ROW_KEYS = {"path", "source", "present", "decision", "reason", "ranges", "topic",
             "intent_status", "policy_sha256", "context"}
_MAX_BYTES = 16 * 1024 * 1024


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _relative(value):
    if (not isinstance(value, str) or not value or "\x00" in value or "\\" in value
            or Path(value).is_absolute() or PureWindowsPath(value).drive
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise WorkbenchError("Use a nonempty workspace-relative path without traversal.")
    return value


def _local(root, value):
    target = root
    for part in _relative(value).split("/"):
        target /= part
        if target.is_symlink():
            raise WorkbenchError("Source preparation requires regular paths without symbolic links: " + value)
    if not target.resolve().is_relative_to(root):
        raise WorkbenchError("Source preparation paths must stay inside the workspace.")
    return target


def _read(path):
    try:
        with path.open("rb") as stream:
            raw = stream.read(_MAX_BYTES + 1)
        if len(raw) > _MAX_BYTES:
            raise WorkbenchError("Source preparation inputs must not exceed sixteen MiB per file.")
        raw.decode("utf-8")
        return raw
    except (UnicodeError, OSError):
        raise WorkbenchError("Read a regular UTF-8 source preparation file: " + str(path)) from None


def _object(path):
    try:
        value = yaml.load(_read(path).decode("utf-8"), Loader=UniqueKeyLoader)
        json.dumps(value, allow_nan=False)
        if not isinstance(value, dict):
            raise WorkbenchError("Source preparation declarations must contain an object.")
        return value
    except (yaml.YAMLError, TypeError, ValueError, RecursionError):
        raise WorkbenchError("Use unique keys and JSON-compatible source preparation declarations.") from None


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _hash(value):
    return isinstance(value, str) and bool(_HASH.fullmatch(value))


def _index_path(source_id):
    if not isinstance(source_id, str) or not _ID.fullmatch(source_id):
        raise WorkbenchError("Use a registered source ID without path separators.")
    return f"evidence/knowledge/selections/{source_id}.json"


def _collection(root, source_id):
    _index_path(source_id)
    configuration, _ = load_workspace(root)
    entry = next((item for item in configuration.get("_catalogs", {}).get("sources", [])
                  if item["id"] == source_id), None)
    if not entry or entry["type"] != "filesystem":
        raise WorkbenchError("Source preparation requires a registered filesystem source collection.")
    return _local(root, entry["location"])


def _policy(root, path):
    value = _object(_local(root, path))
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise WorkbenchError("Use source-filter policy schema_version 1.")
    return {"path": path, "sha256": _digest(_read(_local(root, path)))}


def _manifest(root):
    path = _local(root, _MANIFEST)
    raw = _read(path)
    value = _object(path)
    validate_arguments(value, RAW_MANIFEST_SCHEMA, "source manifest")
    identities, resources = set(), set()
    for record in value["sources"]:
        if not _ID.fullmatch(record["id"]) or not _hash(record["sha256"]):
            raise WorkbenchError("Source manifest identities and SHA-256 values must be valid.")
        identity = (record["id"], record["revision"])
        resource = (record["resource"], record["revision"])
        if identity in identities or resource in resources:
            raise WorkbenchError("Source manifest revisions must have unique identities and resources.")
        identities.add(identity)
        resources.add(resource)
        _timestamp(record["ingested_at"])
        if "snapshot" in record:
            snapshot = _local(root, record["snapshot"])
            if snapshot.is_relative_to(root / "knowledge"):
                raise WorkbenchError("Retained source snapshots must remain outside knowledge.")
    return value, raw


def _binding(record):
    if not _SOURCE_KEYS <= record.keys():
        raise WorkbenchError("A prepared source requires a retained snapshot and complete source identity.")
    return {key: record[key] for key in sorted(_SOURCE_KEYS)}


def _snapshot(root, source):
    path = _local(root, source["snapshot"])
    if path.is_relative_to(root / "knowledge"):
        raise WorkbenchError("Prepared source snapshots must remain outside knowledge.")
    raw = _read(path)
    if _digest(raw) != source["sha256"]:
        raise WorkbenchError("Retained source hash mismatch: " + source["snapshot"])
    return raw


def _ranges(decision, ranges, count):
    if ranges is None and decision == "KEEP":
        ranges = [[1, count]] if count else []
    if not isinstance(ranges, list):
        raise WorkbenchError("Selections require a list of inclusive source line ranges.")
    previous = 0
    for pair in ranges:
        if (not isinstance(pair, list) or len(pair) != 2 or any(type(n) is not int for n in pair)
                or not previous < pair[0] <= pair[1] <= count):
            raise WorkbenchError("Source line ranges must be ordered, disjoint, and within the retained source.")
        previous = pair[1]
    if decision in {"KEEP", "KEEP_SECTIONS"} and not ranges:
        raise WorkbenchError("Kept sources require nonempty source line ranges.")
    if decision == "KEEP" and ranges != [[1, count]]:
        raise WorkbenchError("KEEP requires the complete source page; use KEEP_SECTIONS for excerpts.")
    if decision not in {"KEEP", "KEEP_SECTIONS"} and ranges:
        raise WorkbenchError("Excluded, held, and unreviewed sources cannot select intent passages.")
    return ranges


def _contexts(root, context, *, check_hash=False):
    if not isinstance(context, list):
        raise WorkbenchError("Selection context must list source paths and their SHA-256 values.")
    paths = set()
    for item in context:
        if (not isinstance(item, dict) or set(item) != {"path", "sha256"}
                or not _hash(item["sha256"]) or not isinstance(item["path"], str) or item["path"] in paths):
            raise WorkbenchError("Selection context requires unique path/SHA-256 bindings.")
        path = _local(root, item["path"])
        paths.add(item["path"])
        if check_hash and _digest(_read(path)) != item["sha256"]:
            raise WorkbenchError("Selection context changed: " + item["path"])
    return context


def _index(root, source_id, manifest):
    path = _local(root, _index_path(source_id))
    if not path.exists():
        return None
    index = _object(path)
    if (set(index) != {"schema_version", "source_id", "input_root", "policy", "sources"}
            or type(index.get("schema_version")) is not int or index["schema_version"] != 1
            or index["source_id"] != source_id or not isinstance(index["sources"], list)
            or not isinstance(index["policy"], dict) or set(index["policy"]) != {"path", "sha256"}
            or not _hash(index["policy"]["sha256"])):
        raise WorkbenchError("Use a valid version 1 source selection index for this collection.")
    _local(root, index["input_root"])
    _local(root, index["policy"]["path"])
    records = {tuple(record.get(key) for key in sorted(_SOURCE_KEYS))
               for record in manifest["sources"] if "snapshot" in record}
    paths = set()
    for row in index["sources"]:
        if (not isinstance(row, dict) or set(row) != _ROW_KEYS or not isinstance(row["source"], dict)
                or set(row["source"]) != _SOURCE_KEYS or type(row["present"]) is not bool
                or any(not isinstance(value, str) for value in row["source"].values())
                or not isinstance(row["path"], str) or not isinstance(row["decision"], str)
                or row["decision"] not in _DECISIONS | {"NEEDS_REVIEW"}
                or any(not isinstance(row[key], str) for key in ("reason", "topic", "intent_status"))
                or row["path"] in paths):
            raise WorkbenchError("Use unique, complete source selection rows.")
        _relative(row["path"])
        if not row["path"].lower().endswith(".md"):
            raise WorkbenchError("Source selections support Markdown pages only.")
        paths.add(row["path"])
        if tuple(row["source"].get(key) for key in sorted(_SOURCE_KEYS)) not in records:
            raise WorkbenchError("Selection source identity must match the retained source manifest.")
        raw = _snapshot(root, row["source"])
        _ranges(row["decision"], row["ranges"], len(raw.decode("utf-8").splitlines()))
        _contexts(root, row["context"])
        if row["decision"] != "NEEDS_REVIEW":
            if not _hash(row["policy_sha256"]) or not _text(row["reason"]):
                raise WorkbenchError("Reviewed selections require policy hashes and reasons.")
        elif row["policy_sha256"] is not None:
            raise WorkbenchError("Unreviewed selections cannot claim a reviewed policy hash.")
    return index


def _inventory(root, input_dir):
    directory = _local(root, input_dir)
    if not directory.is_dir():
        raise WorkbenchError("Select an existing raw input directory.")
    result = {}
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(root).as_posix()
        _local(root, relative)
        if path.is_file() and path.suffix.lower() == ".md":
            result[path.relative_to(directory).as_posix()] = _read(path)
    return result


def _origins(root, collection, source_id, records):
    origins = {}
    for record in records:
        if record.get("source_id") != source_id:
            continue
        relative = record.get("origin_path")
        if relative is None and "snapshot" in record:
            snapshot = _local(root, record["snapshot"])
            if snapshot.is_relative_to(collection):
                relative = snapshot.relative_to(collection).as_posix()
        if relative is not None:
            if "snapshot" in record:
                _snapshot(root, record)
            _relative(relative)
            origins.setdefault(relative, []).append(record)
    return origins


def _pending(path, source, present=True):
    return {"path": path, "source": source, "present": present, "decision": "NEEDS_REVIEW",
            "reason": "Source or governing context requires review.", "ranges": [], "topic": "",
            "intent_status": "unreviewed", "policy_sha256": None, "context": []}


def _atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".source-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _save_index(root, source_id, index):
    _atomic(_local(root, _index_path(source_id)),
            (json.dumps(index, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


@contextmanager
def _lock(root):
    path = _local(root, ".workbench/ingestion/source-preparation.lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        stream = path.open("x")
    except FileExistsError:
        raise WorkbenchError("Another source preparation operation holds the workspace lock.") from None
    try:
        stream.close()
        yield
    finally:
        path.unlink(missing_ok=True)


def _context_current(root, row):
    try:
        _contexts(root, row["context"], check_hash=True)
        return True
    except WorkbenchError:
        return False


def _summary(source_id, index, findings=()):
    if not index["sources"]:
        findings = [*findings, {"path": index["input_root"], "code": "empty_export",
                               "message": "No Markdown pages are available for source review."}]
    decisions = Counter(row["decision"] for row in index["sources"])
    pending = sum(not row["present"] or row["decision"] in {"NEEDS_REVIEW", "HOLD"}
                  for row in index["sources"])
    return {"schema_version": 1, "status": "NEEDS_REVIEW" if pending or findings else "READY",
            "source_id": source_id, "selection": _index_path(source_id),
            "counts": {"documents": len(index["sources"]),
                       "present": sum(row["present"] for row in index["sources"]),
                       "missing": sum(not row["present"] for row in index["sources"]),
                       "needs_review": pending, "decisions": dict(sorted(decisions.items()))},
            "findings": list(findings)}


def _affected_knowledge(root, changes):
    affected = []
    if not changes:
        return affected
    for path in sorted((root / "knowledge").rglob("*.md")):
        if is_derived_knowledge_path(path, root):
            continue
        _local(root, path.relative_to(root).as_posix())
        match = _FRONTMATTER.match(_read(path).decode("utf-8"))
        if not match:
            continue
        try:
            metadata = yaml.load(match.group(1), Loader=UniqueKeyLoader)
        except yaml.YAMLError:
            raise WorkbenchError("Read valid canonical knowledge frontmatter before calculating affected records.") from None
        if not isinstance(metadata, dict):
            raise WorkbenchError("Canonical knowledge frontmatter must contain an object.")
        references = metadata.get("sources", [])
        if not isinstance(references, list) or any(not isinstance(item, dict) for item in references):
            raise WorkbenchError("Canonical knowledge source references must contain objects.")
        linked = [change for change in changes if any(
            all(item.get(key) == change["previous"][key] for key in ("resource", "revision", "sha256"))
            for item in references)]
        if linked:
            affected.append({"path": path.relative_to(root).as_posix(), "changed_sources": linked})
    return affected


def refresh_sources(root: Path, source_id: str, input_dir: str, policy_path: str | None = None) -> dict:
    """Capture changed local pages, preserving reviewed decisions only for unchanged inputs."""
    root = Path(root).expanduser().resolve()
    with _lock(root):
        collection = _collection(root, source_id)
        directory = _local(root, input_dir)
        if (directory == root or directory.is_relative_to(root / "knowledge")
                or directory.is_relative_to(root / ".workbench")
                or directory.is_relative_to(root / ".git")
                or directory.is_relative_to(root / "evidence") and directory != collection):
            raise WorkbenchError("Use a writable raw import folder or this collection's existing retained snapshot directory.")
        manifest, manifest_raw = _manifest(root)
        previous = _index(root, source_id, manifest)
        policy = _policy(root, policy_path or (previous["policy"]["path"] if previous else _POLICY))
        incoming = _inventory(root, input_dir)
        origins = _origins(root, collection, source_id, manifest["sources"])
        old = {row["path"]: row for row in previous["sources"]} if previous else {}
        snapshots, additions, sources = {}, [], []
        changes = {"new": [], "modified": [], "missing": [], "reused": []}
        shared = {}
        for record in manifest["sources"]:
            if "snapshot" in record:
                shared.setdefault(record["sha256"], []).append(record)
        for path, raw in incoming.items():
            sha256 = _digest(raw)
            history = origins.get(path, [])
            same = next((record for record in reversed(history) if record["sha256"] == sha256), None)
            if same is not None:
                source = _binding(same)
                _snapshot(root, source)
            else:
                exemplar = history[-1] if history else None
                identifier = exemplar["id"] if exemplar else "SRC-" + _digest((source_id + "\0" + path).encode())[:24]
                resource = exemplar["resource"] if exemplar else f"source:{source_id}/{path}"
                snapshot = None
                for record in shared.get(sha256, []):
                    if record["snapshot"] not in snapshots:
                        _snapshot(root, record)
                    snapshot = record["snapshot"]
                    break
                snapshot = snapshot or f"evidence/knowledge/sources/sha256/{sha256}.md"
                target = _local(root, snapshot)
                if target.exists():
                    if _read(target) != raw:
                        raise WorkbenchError("A retained snapshot path contains different bytes: " + snapshot)
                else:
                    snapshots[snapshot] = raw
                record = {"id": identifier, "resource": resource, "revision": "sha256:" + sha256,
                          "sha256": sha256, "snapshot": snapshot,
                          "ingested_at": datetime.now(timezone.utc).isoformat(), "classification": "unknown",
                          "source_id": source_id, "origin_path": path}
                if any((r["id"], r["revision"]) == (identifier, record["revision"])
                       or (r["resource"], r["revision"]) == (resource, record["revision"])
                       for r in manifest["sources"] + additions):
                    raise WorkbenchError("A retained source revision already exists with another source binding.")
                additions.append(record)
                shared.setdefault(sha256, []).append(record)
                source = _binding(record)
            prior = old.get(path)
            reusable = (prior is not None and prior["source"]["sha256"] == sha256
                        and prior["policy_sha256"] == policy["sha256"] and _context_current(root, prior))
            row = dict(prior, source=source, present=True) if reusable else _pending(path, source)
            sources.append(row)
            changes["reused" if reusable else "modified" if prior else "new"].append(path)
        for path in sorted(old.keys() - incoming.keys()):
            sources.append(dict(old[path], present=False))
            changes["missing"].append(path)
        index = {"schema_version": 1, "source_id": source_id, "input_root": input_dir,
                 "policy": policy, "sources": sorted(sources, key=lambda row: row["path"])}
        changed_sources = [{"path": path, "previous": old[path]["source"],
                            "current": next(row["source"] for row in sources if row["path"] == path),
                            "present": path in incoming}
                           for path in sorted(set(changes["modified"] + changes["missing"]))]
        affected = _affected_knowledge(root, changed_sources)
        if _read(_local(root, _MANIFEST)) != manifest_raw or _inventory(root, input_dir) != incoming:
            raise WorkbenchError("Sources or manifest changed during refresh; repeat the operation.")
        if _policy(root, policy["path"]) != policy:
            raise WorkbenchError("Filter policy changed during refresh; repeat the operation.")
        for name, raw in snapshots.items():
            path = _local(root, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(raw)
        if additions:
            manifest["sources"].extend(additions)
            _atomic(_local(root, _MANIFEST), yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True).encode("utf-8"))
        _save_index(root, source_id, index)
        return {**_summary(source_id, index), "changes": changes,
                "new_source_revisions": len(additions), "new_snapshot_payloads": len(snapshots),
                "changed_sources": changed_sources, "affected_knowledge": affected}


def _freshness(root, index):
    findings = []
    current_policy = _policy(root, index["policy"]["path"])
    if current_policy != index["policy"]:
        findings.append({"path": index["policy"]["path"], "code": "policy_changed",
                         "message": "Refresh and review selections under the current filter policy."})
    directory = _local(root, index["input_root"])
    incoming = _inventory(root, index["input_root"]) if directory.exists() else {}
    known = {row["path"] for row in index["sources"]}
    for path in sorted(incoming.keys() - known):
        findings.append({"path": path, "code": "input_added", "message": "Refresh before selecting or rendering new pages."})
    for row in index["sources"]:
        path = row["path"]
        raw = incoming.get(path)
        if row["present"] != (raw is not None):
            findings.append({"path": path, "code": "input_presence_changed",
                             "message": "Refresh before selecting or rendering pages with changed export presence."})
        if not row["present"] or raw is None:
            findings.append({"path": path, "code": "input_missing", "message": "The current export omits this retained page."})
        elif _digest(raw) != row["source"]["sha256"]:
            findings.append({"path": path, "code": "input_changed", "message": "Refresh and review the changed source page."})
        if row["decision"] != "NEEDS_REVIEW" and row["policy_sha256"] != current_policy["sha256"]:
            findings.append({"path": path, "code": "decision_policy_changed", "message": "The selection requires the current policy hash."})
        if not _context_current(root, row):
            findings.append({"path": path, "code": "context_changed", "message": "Refresh and review the changed governing context."})
    return findings


def apply_selections(root: Path, source_id: str, decisions_path: str) -> dict:
    """Apply a complete prevalidated batch of agent-reviewed, hash-bound decisions."""
    root = Path(root).expanduser().resolve()
    with _lock(root):
        _collection(root, source_id)
        manifest, _ = _manifest(root)
        index = _index(root, source_id, manifest)
        if index is None:
            raise WorkbenchError("Refresh the source collection before applying decisions.")
        freshness = [finding for finding in _freshness(root, index) if finding["code"] != "input_missing"]
        if freshness:
            raise WorkbenchError("Source preparation is stale; refresh before applying decisions.")
        decisions = _object(_local(root, decisions_path))
        if (set(decisions) != {"schema_version", "source_id", "decisions"}
                or type(decisions.get("schema_version")) is not int or decisions["schema_version"] != 1
                or decisions["source_id"] != source_id or not isinstance(decisions["decisions"], list)
                or not decisions["decisions"]):
            raise WorkbenchError("Use a nonempty version 1 decision batch for this source collection.")
        rows = {row["path"]: row for row in index["sources"]}
        updates, seen = [], set()
        required = {"path", "sha256", "decision", "reason", "topic", "intent_status"}
        for decision in decisions["decisions"]:
            if (not isinstance(decision, dict) or not required <= decision.keys()
                    or decision.keys() - required - {"ranges", "context"}
                    or not isinstance(decision["path"], str) or decision["path"] in seen
                    or decision["path"] not in rows or not isinstance(decision["decision"], str)
                    or decision["decision"] not in _DECISIONS
                    or not _hash(decision["sha256"])
                    or any(not _text(decision[key]) for key in ("reason", "topic", "intent_status"))):
                raise WorkbenchError("Use unique known source paths, supported decisions, hashes, and nonempty review details.")
            seen.add(decision["path"])
            row = rows[decision["path"]]
            if not row["present"] or decision["sha256"] != row["source"]["sha256"]:
                raise WorkbenchError("Decision hashes must match present retained source pages.")
            raw = _snapshot(root, row["source"])
            ranges = _ranges(decision["decision"], decision.get("ranges", None if decision["decision"] == "KEEP" else []),
                             len(raw.decode("utf-8").splitlines()))
            context = _contexts(root, decision.get("context", []), check_hash=True)
            updates.append({**row, **{key: decision[key] for key in ("decision", "reason", "topic", "intent_status")},
                            "ranges": ranges, "context": context, "policy_sha256": index["policy"]["sha256"]})
        rows.update({row["path"]: row for row in updates})
        index["sources"] = sorted(rows.values(), key=lambda row: row["path"])
        if [finding for finding in _freshness(root, index) if finding["code"] != "input_missing"]:
            raise WorkbenchError("Source or context changed during selection; refresh and repeat the review.")
        _save_index(root, source_id, index)
        return {**_summary(source_id, index), "applied_decisions": len(updates)}


def verify_sources(root: Path, source_id: str) -> dict:
    """Check source, policy, and context hashes without changing stored decisions."""
    root = Path(root).expanduser().resolve()
    try:
        _collection(root, source_id)
        manifest, _ = _manifest(root)
        index = _index(root, source_id, manifest)
        if index is None:
            raise WorkbenchError("Refresh the collection before verifying source selections.")
        return _summary(source_id, index, _freshness(root, index))
    except (WorkbenchError, OSError) as error:
        return {"schema_version": 1, "status": "FAILED", "source_id": source_id,
                "findings": [{"path": _index_path(source_id), "code": "source_binding_invalid", "message": str(error)}]}


def render_sources(root: Path, source_id: str, output_dir: str) -> dict:
    """Materialize current reviewed intent passages, with original and output hashes."""
    root = Path(root).expanduser().resolve()
    with _lock(root):
        _collection(root, source_id)
        manifest, manifest_raw = _manifest(root)
        index = _index(root, source_id, manifest)
        if index is None:
            raise WorkbenchError("Refresh and review source selections before creating a view.")
        index_raw = _read(_local(root, _index_path(source_id)))
        freshness = [finding for finding in _freshness(root, index) if finding["code"] != "input_missing"]
        if freshness:
            raise WorkbenchError("Source preparation is stale; refresh and review before creating a view.")
        output = _local(root, output_dir)
        if not output.is_relative_to(root / ".workbench") or output == root / ".workbench" or output.exists():
            raise WorkbenchError("Create a source view in a new directory below .workbench/.")
        selected, omitted = [], []
        for row in index["sources"]:
            if not row["present"] or row["decision"] not in {"KEEP", "KEEP_SECTIONS"}:
                omitted.append({"path": row["path"], "decision": row["decision"], "present": row["present"]})
                continue
            raw = _snapshot(root, row["source"])
            selected.append((row, raw))
        output.mkdir(parents=True)
        entries = []
        for row, raw in selected:
            destination = output / row["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            mapping, fragments, output_line = [], [], 1
            raw_lines = raw.decode("utf-8").splitlines(keepends=True)
            for start, end in row["ranges"]:
                fragments.append("".join(raw_lines[start - 1:end]))
                mapping.append({"source_start": start, "source_end": end,
                                "output_start": output_line, "output_end": output_line + end - start})
                output_line += end - start + 1
            kind = "excerpt"
            if row["decision"] == "KEEP":
                try:
                    destination.symlink_to(os.path.relpath(_local(root, row["source"]["snapshot"]), destination.parent))
                    kind = "symlink"
                except (OSError, NotImplementedError):
                    destination.write_bytes(raw)
                    kind = "copy"
            else:
                destination.write_text("".join(fragments), encoding="utf-8", newline="")
            expected_output = raw if row["decision"] == "KEEP" else "".join(fragments).encode("utf-8")
            if destination.read_bytes() != expected_output:
                raise WorkbenchError("Source view output changed during rendering; create a new view after review.")
            entries.append({"path": row["path"], "output": row["path"], "kind": kind,
                            "source": row["source"], "source_sha256": row["source"]["sha256"],
                            "output_sha256": _digest(destination.read_bytes()),
                            "ranges": row["ranges"], "mapping": mapping})
        for row, raw in selected:
            if _snapshot(root, row["source"]) != raw:
                raise WorkbenchError("Retained source changed during rendering; restore its source binding.")
        if (_read(_local(root, _index_path(source_id))) != index_raw
                or _read(_local(root, _MANIFEST)) != manifest_raw
                or [finding for finding in _freshness(root, index) if finding["code"] != "input_missing"]):
            raise WorkbenchError("Source preparation changed during rendering; refresh and create a new view.")
        view = {"schema_version": 1, "source_id": source_id,
                "selection": {"path": _index_path(source_id),
                              "sha256": _digest(_read(_local(root, _index_path(source_id))))},
                "policy": index["policy"], "sources": entries, "omitted": omitted}
        _atomic(output / "manifest.json", (json.dumps(view, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        return {"schema_version": 1, "status": "VIEW_CREATED", "source_id": source_id,
                "output": output_dir, "manifest": output_dir + "/manifest.json",
                "counts": {"selected": len(entries), "omitted": len(omitted),
                           "links": sum(entry["kind"] == "symlink" for entry in entries),
                           "excerpts": sum(entry["kind"] == "excerpt" for entry in entries),
                           "copies": sum(entry["kind"] == "copy" for entry in entries)}}
