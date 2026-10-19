"""Compare local ingestion evidence without executing business code or granting review."""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
from urllib.parse import unquote, urlsplit

import yaml

from ..artifact_lint import _FRONTMATTER
from ..context.catalogs import UniqueKeyLoader
from ..governance.schemas import DOCUMENT_SCHEMAS
from ..governance.validation import _FORBIDDEN_KNOWLEDGE_PARTS, _NAVIGATION, _timestamp
from ..models import WorkbenchError
from ..validation import validate_workspace


_HASH = re.compile(r"[a-f0-9]{64}\Z")
_REVISION = re.compile(r"[a-fA-F0-9]{40}\Z")
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_LIMITS = [
    "Automated checks do not check the complete approved dictionary or grammar rules.",
    "These checks do not establish source truth, assertion coverage, business execution, or human approval.",
    "The baseline and checkpoint are local records. Their hashes do not authenticate an actor.",
    "Markdown destination checks cover selected syntax, rather than the complete CommonMark specification.",
]


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(value):
    if (not isinstance(value, str) or not value or "\x00" in value or "\\" in value
            or Path(value).is_absolute() or PureWindowsPath(value).drive
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise ValueError("Use a nonempty workspace-relative path without traversal.")
    return value


def _local(root, value, *, required=True):
    target = root
    for part in _relative(value).split("/"):
        target = target / part
        if target.is_symlink():
            raise ValueError("Use regular local paths without symbolic links: " + value)
    if not target.resolve().is_relative_to(root):
        raise ValueError("Paths must stay within the workspace: " + value)
    if required and not target.exists():
        raise ValueError("The selected path does not exist: " + value)
    return target


def _external_file(value):
    path = Path(value).expanduser().absolute()
    if path.is_symlink() or not path.is_file():
        raise ValueError("Select an existing regular input file.")
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Harness input files must not exceed sixteen MiB.")
    return path


def _yaml(data):
    value = yaml.load(data, Loader=UniqueKeyLoader)
    json.dumps(value, allow_nan=False)
    if not isinstance(value, dict):
        raise ValueError("YAML must contain an object.")
    return value


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON keys must be unique.")
        result[key] = value
    return result


def _json(path):
    value = json.loads(_external_file(path).read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                       parse_constant=lambda value: (_ for _ in ()).throw(ValueError("Use finite JSON values.")))
    if not isinstance(value, dict):
        raise ValueError("JSON must contain an object.")
    return value


def _files(root, relative):
    directory = _local(root, relative, required=False)
    if not directory.exists():
        return {}
    if not directory.is_dir():
        raise ValueError("The evidence directory is not a directory: " + relative)
    result = {}
    for path in sorted(directory.rglob("*")):
        name = path.relative_to(root).as_posix()
        _local(root, name)
        if path.is_file():
            result[name] = _file_hash(path)
    return result


def _governed(root):
    result = {}
    for directory in ("knowledge", "evidence/knowledge/findings"):
        base = _local(root, directory, required=False)
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() != ".md" or path.name in _NAVIGATION or path.name.casefold() == "log.md":
                continue
            relative = path.relative_to(base)
            if directory == "knowledge" and any(part.casefold() in _FORBIDDEN_KNOWLEDGE_PARTS for part in relative.parts):
                continue
            name = path.relative_to(root).as_posix()
            _local(root, name)
            if path.is_file():
                result[name] = _file_hash(path)
    return result


def _capture(root):
    raw = _files(root, "evidence/knowledge/sources")
    audit = _files(root, "evidence/knowledge/audit")
    path = _local(root, "evidence/knowledge/manifest.yaml")
    data = path.read_bytes()
    raw["evidence/knowledge/manifest.yaml"] = _digest(data)
    manifest = _yaml(data.decode("utf-8"))
    if type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1 or not isinstance(manifest.get("sources"), list):
        raise ValueError("Use the supported raw manifest with a sources list.")
    for source in manifest["sources"]:
        if "snapshot" in source:
            name = source["snapshot"]
            if _relative(name).startswith("knowledge/"):
                raise ValueError("Store source snapshots outside the domain knowledge directory.")
            snapshot = _local(root, name, required=False)
            if snapshot.is_file():
                raw[name] = _file_hash(snapshot)
    if path.read_bytes() != data:
        raise ValueError("The manifest changed while the baseline was captured.")
    return {"raw_files": raw, "audit_files": audit, "governed_documents": _governed(root),
            "manifest": {"bytes_base64": base64.b64encode(data).decode("ascii"),
                         "sha256": _digest(data), "records": manifest["sources"]}}


def _projection(path):
    raw = path.read_bytes()
    match = _FRONTMATTER.match(raw.decode("utf-8"))
    return (_yaml(match.group(1)), match.group(2)) if match else ({}, raw.decode("utf-8"))


def _report(operation, root, phase=None):
    return {"schema_version": 1, "operation": operation, "phase": phase, "workspace": str(root),
            "checked_at": datetime.now(timezone.utc).isoformat(), "status": "FAILED",
            "standard": "ASD-STE100", "automated_check": "FAILED", "asd_review": "PENDING",
            "reviewer": None, "reviewed_at": None, "limitations": list(_LIMITS),
            "counts": {}, "findings": [], "deferred_findings": [], "unchecked_limits": [],
            "prepared_content": {}}


def _finding(report, code, path, evidence, consequence="The requested evidence check cannot pass.",
             next_action="Correct the recorded evidence, then run the check again."):
    report["findings"].append({"code": code, "path": str(path), "evidence": evidence,
                               "consequence": consequence, "owner": "unknown", "next_action": next_action})


def _baseline(path, root):
    baseline = _json(path)
    if (baseline.get("schema_version") != 1 or baseline.get("operation") != "start"
            or baseline.get("status") != "PASSED" or baseline.get("automated_check") != "PASSED"
            or baseline.get("workspace") != str(root)):
        raise ValueError("Use a successful start baseline for this workspace.")
    for field, prefixes in (("raw_files", None), ("audit_files", ("evidence/knowledge/audit/",)),
                            ("governed_documents", ("knowledge/", "evidence/knowledge/findings/"))):
        entries = baseline.get(field)
        if not isinstance(entries, dict):
            raise ValueError("The baseline file inventory is invalid.")
        for name, digest in entries.items():
            name = _relative(name)
            if ((prefixes is not None and not name.startswith(prefixes))
                    or (field == "raw_files" and name.startswith("knowledge/"))
                    or not isinstance(digest, str) or not _HASH.fullmatch(digest)):
                raise ValueError("The baseline file inventory is invalid.")
    manifest = baseline.get("manifest", {})
    data = base64.b64decode(manifest["bytes_base64"], validate=True)
    if _digest(data) != manifest.get("sha256") or _yaml(data.decode("utf-8")).get("sources") != manifest.get("records"):
        raise ValueError("The baseline manifest bytes and records disagree.")
    return baseline, data


def _plan(path, root):
    plan = _yaml(_external_file(path).read_text(encoding="utf-8"))
    if (set(plan) != {"schema_version", "documents", "repositories", "executions"}
            or type(plan["schema_version"]) is not int or plan["schema_version"] != 1):
        raise ValueError("Use schema_version 1, documents, repositories, and executions in the plan.")
    documents = plan["documents"]
    if not isinstance(documents, list) or not documents or any(not isinstance(name, str) for name in documents) or len(set(documents)) != len(documents):
        raise ValueError("Select a nonempty list of unique Markdown document paths.")
    for name in documents:
        path = _local(root, name)
        if not path.is_file() or path.suffix.lower() != ".md":
            raise ValueError("Select existing regular Markdown documents.")
    if not isinstance(plan["repositories"], dict) or not isinstance(plan["executions"], list):
        raise ValueError("Repositories must be an object, and executions must be a list.")
    repositories = {}
    for identifier, location in plan["repositories"].items():
        if not isinstance(identifier, str) or not _ID.fullmatch(identifier) or not isinstance(location, str) or not location.strip() or "\x00" in location:
            raise ValueError("Use a valid repository ID and a local checkout path.")
        path = Path(location).expanduser()
        if "://" in location or location.startswith(("//", "\\\\")):
            raise ValueError("Repository maps must select local checkouts.")
        path = path.resolve() if path.is_absolute() else _local(root, location).resolve()
        if not path.is_dir():
            raise ValueError("The mapped repository checkout does not exist.")
        repositories[identifier] = path
    for execution in plan["executions"]:
        if not isinstance(execution, dict) or set(execution) != {"result", "repository_id", "revision"}:
            raise ValueError("Each execution needs result, repository_id, and revision.")
        _local(root, execution["result"])
        if (not isinstance(execution["revision"], str) or not _REVISION.fullmatch(execution["revision"])
                or execution["repository_id"] not in repositories):
            raise ValueError("Each execution needs a mapped repository and a full forty-character Git revision.")
    return plan, repositories


def _visible(body):
    lines, fence = [], None
    for line in body.splitlines():
        marker = _FENCE.match(line)
        if marker:
            token, suffix = marker.groups()
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not suffix.strip():
                fence = None
            lines.append("")
        elif fence is None:
            lines.append(re.sub(r"(`+).*?\1", "", line))
        else:
            lines.append("")
    return "\n".join(lines)


def _destinations(body):
    """Read inline and reference destinations without treating code fences as links."""
    text = _visible(body)
    definitions = {}
    for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:\s*(<[^>\n]*>|\S+)", text, re.M):
        definitions[match[1].strip().casefold()] = match[2].strip("<>")
    for match in re.finditer(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]*>|(?:\\.|[^()\n]|\([^()\n]*\))*)\)", text):
        target = match[1].strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        else:
            target = re.sub(r"\s+(['\"]).*\1\s*$", "", target)
        yield target, text.count("\n", 0, match.start()) + 1
    for match in re.finditer(r"!?\[([^\]\n]+)\](?:\[([^\]\n]*)\])?", text):
        if text[match.end():].startswith(("(", ":")):
            continue
        label = (match[2] or match[1]).strip().casefold()
        if label in definitions:
            yield definitions[label], text.count("\n", 0, match.start()) + 1
        elif match[2] is not None:
            yield None, text.count("\n", 0, match.start()) + 1


def _git_blob(repositories, identifier, revision, source_path, cache):
    _relative(source_path)
    if not isinstance(revision, str) or not _REVISION.fullmatch(revision):
        raise ValueError("Git evidence requires a full forty-character hexadecimal revision.")
    key = identifier, revision, source_path
    if key not in cache:
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        result = subprocess.run(["git", "--no-pager", "--no-replace-objects", "-c", "core.fsmonitor=false",
                                 "-C", str(repositories[identifier]), "show", revision + ":" + source_path],
                                capture_output=True, timeout=20, env=environment)
        if result.returncode:
            raise ValueError("The exact Git blob could not be read: " + source_path)
        cache[key] = result.stdout
    return cache[key]


def _retention(report, baseline, before, old_manifest, root):
    for field, prefix in (("raw_files", "raw_file"), ("audit_files", "audit_file")):
        for name, digest in baseline[field].items():
            if name == "evidence/knowledge/manifest.yaml":
                continue
            actual = before[field].get(name)
            if actual != digest:
                _finding(report, prefix + ("_missing" if actual is None else "_changed"), name,
                         {"baseline_sha256": digest, "current_sha256": actual},
                         "Previously retained evidence was changed or removed.", "Restore the retained bytes and add new evidence separately.")
    for name in sorted(set(baseline["governed_documents"]) - set(before["governed_documents"])):
        _finding(report, "governed_document_missing", name,
                 {"baseline_sha256": baseline["governed_documents"][name], "current_sha256": None},
                 "Previously retained knowledge was removed.", "Restore the retained knowledge document before checking again.")
    current = _local(root, "evidence/knowledge/manifest.yaml").read_bytes()
    old_records = baseline["manifest"]["records"]
    current_records = before["manifest"]["records"]
    # An initialized empty list must become a block list before its first addition.
    first_records = not old_records and bool(current_records)
    if ((not current.startswith(old_manifest) and not first_records)
            or current_records[:len(old_records)] != old_records):
        _finding(report, "manifest_prefix_changed", "evidence/knowledge/manifest.yaml",
                 {"baseline_sha256": _digest(old_manifest), "current_sha256": _digest(current)},
                 "The original source manifest history is not preserved.", "Restore the exact manifest prefix before appending records.")


def _links_and_code(report, root, plan, repositories, records, projections, cache):
    snapshots = {}
    triples = {}
    for item in records:
        triples[(item["resource"], item["revision"], item["sha256"])] = item
        if item.get("snapshot"):
            snapshots.setdefault(item["snapshot"], []).append(item)
    cited = {}
    for name, (metadata, body) in projections.items():
        declared = {tuple(source.get(key) for key in ("resource", "revision", "sha256"))
                    for source in metadata.get("sources", []) if isinstance(source, dict)}
        for triple in declared:
            if triple in triples:
                item = triples[triple]
                cited[item["id"], item["revision"]] = item
        for destination, line in _destinations(body):
            report["counts"]["local_links"] = report["counts"].get("local_links", 0) + 1
            if destination is None:
                _finding(report, "link_reference_missing", name, {"line": line})
                continue
            split = urlsplit(destination)
            if split.scheme or split.netloc:
                report["unchecked_limits"].append({"code": "external_destination_unchecked", "path": name, "destination": destination})
                report["counts"]["local_links"] -= 1
                continue
            path_text = unquote(split.path).replace("\\(", "(").replace("\\)", ")")
            base = root / name
            if path_text:
                if Path(path_text).is_absolute() or PureWindowsPath(path_text).drive or "\x00" in path_text or "\\" in path_text:
                    raise ValueError("Local Markdown destinations must stay inside the workspace.")
                target = (base.parent / path_text).absolute()
                # Relative Markdown links can use '..', but their resolved target must remain confined.
                normalized = Path(os.path.normpath(target))
                if not normalized.is_relative_to(root):
                    raise ValueError("Local Markdown destinations must stay inside the workspace.")
                relative = normalized.relative_to(root).as_posix()
                target = _local(root, relative, required=False)
            else:
                target, relative = base, name
            if not target.exists():
                _finding(report, "link_missing", name, {"line": line, "destination": destination})
                continue
            for item in snapshots.get(relative, []):
                cited[item["id"], item["revision"]] = item
                triple = item["resource"], item["revision"], item["sha256"]
                if metadata.get("type") in DOCUMENT_SCHEMAS and triple not in declared:
                    _finding(report, "linked_source_not_declared", name, {"destination": destination, "source_id": item["id"]})
            fragment = unquote(split.fragment)
            if not fragment:
                continue
            locator = re.fullmatch(r"L([1-9]\d*)(?:-L([1-9]\d*))?", fragment)
            if locator:
                first, last = int(locator[1]), int(locator[2] or locator[1])
                valid = target.is_file() and 1 <= first <= last <= len(target.read_bytes().splitlines())
                report["counts"]["line_fragments"] = report["counts"].get("line_fragments", 0) + 1
                if not valid:
                    _finding(report, "line_fragment_invalid", name, {"destination": destination, "line": line})
            elif fragment.startswith("L") and re.match(r"L\d", fragment):
                _finding(report, "line_fragment_invalid", name, {"destination": destination, "line": line})
            else:
                report["unchecked_limits"].append({"code": "heading_fragment_unchecked", "path": name, "destination": destination})
    for item in cited.values():
        identifier = item.get("repository_id")
        if not identifier:
            continue
        if identifier not in repositories:
            report["unchecked_limits"].append({"code": "code_scope_unchecked", "path": item.get("snapshot"), "repository_id": identifier})
            continue
        try:
            data = _git_blob(repositories, identifier, item["revision"], item["source_path"], cache)
            captured = _local(root, item["snapshot"]).read_bytes()
            first, last = item.get("source_start_line"), item.get("source_end_line")
            if item.get("capture") == "full":
                expected = data
            elif item.get("capture") == "excerpt" and type(first) is int and type(last) is int and 1 <= first <= last <= len(data.splitlines()):
                expected = b"".join(data.splitlines(keepends=True)[first - 1:last])
            else:
                raise ValueError("Record a supported full or excerpt code capture and valid source range.")
            if expected != captured or ("original_sha256" in item and _digest(data) != item["original_sha256"]):
                _finding(report, "code_capture_mismatch", item["snapshot"], {"revision": item["revision"], "source_path": item["source_path"]})
            report["counts"]["code_captures"] = report["counts"].get("code_captures", 0) + 1
        except (KeyError, ValueError, OSError, subprocess.SubprocessError) as error:
            _finding(report, "code_capture_invalid", item.get("snapshot", ""), str(error))


def _executions(report, root, plan, repositories, records, cache):
    for chosen in plan["executions"]:
        name = chosen["result"]
        try:
            path = _local(root, name)
            result = _json(path)
            hashes = result.get("source_sha256")
            if result.get("status") != "PASSED" or not isinstance(hashes, dict) or not hashes:
                raise ValueError("Choose a PASSED result with a nonempty source_sha256 map.")
            if not any(item.get("snapshot") == name and item["revision"] == chosen["revision"] and item["sha256"] == _file_hash(path) for item in records):
                raise ValueError("The retained result hash must be registered at the declared revision.")
            for source_path, digest in hashes.items():
                if not isinstance(digest, str) or not _HASH.fullmatch(digest):
                    raise ValueError("Executed source hashes must be lowercase SHA256 values.")
                data = _git_blob(repositories, chosen["repository_id"], chosen["revision"], source_path, cache)
                actual = _digest(data)
                report["counts"]["execution_source_hashes"] = report["counts"].get("execution_source_hashes", 0) + 1
                if actual != digest:
                    _finding(report, "execution_source_hash_mismatch", name,
                             {"source_path": source_path, "revision": chosen["revision"], "executed_sha256": digest, "git_sha256": actual},
                             "The saved result does not cover these final source bytes.", "Retain a matching execution result or limit the execution claim.")
            report["counts"]["execution_results"] = report["counts"].get("execution_results", 0) + 1
        except (KeyError, ValueError, OSError, subprocess.SubprocessError) as error:
            _finding(report, "execution_invalid", name, str(error))


def _audit_targets(report, root, baseline, before, projections, changed, phase):
    targets = {}
    for name in before["governed_documents"]:
        metadata, _ = projections.get(name) or _projection(_local(root, name))
        if metadata.get("type") in DOCUMENT_SCHEMAS:
            targets[metadata["id"], metadata["version"]] = name
    events, new = {}, set()
    for name in before["audit_files"]:
        if Path(name).suffix.lower() not in {".yaml", ".yml"}:
            continue
        event = _yaml(_local(root, name).read_text(encoding="utf-8"))
        events[event["id"]] = (name, event)
        if name not in baseline["audit_files"]:
            new.add(event["id"])
    replaced = set()
    children = {}
    for identifier in sorted(events):
        name, event = events[identifier]
        previous = event.get("previous_event_id")
        if previous is None:
            continue
        valid = isinstance(previous, str) and previous in events and previous != identifier
        if valid:
            old = events[previous][1]
            valid = (old["item_id"] == event["item_id"] and old["item_version"] <= event["item_version"]
                     and _timestamp(old["at"]) <= _timestamp(event["at"]) and previous not in children)
        if not valid:
            _finding(report, "audit_correction_invalid", name, {"previous_event_id": previous})
        else:
            replaced.add(previous)
            children[previous] = identifier
        visited, current = set(), identifier
        while current in events and events[current][1].get("previous_event_id") is not None:
            if current in visited:
                _finding(report, "audit_correction_invalid", name, "The correction chain contains a cycle.")
                break
            visited.add(current)
            current = events[current][1]["previous_event_id"]
            if not isinstance(current, str):
                break
    matching = set()
    for identifier in sorted(new - replaced):
        name, event = events[identifier]
        target = event.get("item_path") or targets.get((event["item_id"], event["item_version"]))
        actual = None
        if target is not None:
            path = _local(root, target)
            if not path.is_file():
                raise ValueError("An audit item_path must identify a regular file.")
            actual = _file_hash(path)
            if target in before["governed_documents"]:
                metadata, _ = projections.get(target) or _projection(path)
                if (metadata["id"], metadata["version"]) != (event["item_id"], event["item_version"]):
                    _finding(report, "audit_target_identity_mismatch", name, {"target": target})
                    continue
        if target is None or actual != event["content_sha256"]:
            _finding(report, "audit_target_hash_mismatch", name, {"target": target, "recorded_sha256": event["content_sha256"]},
                     "The new audit event does not bind final document bytes.", "Append an explicit correction event for the final bytes.")
        elif event["action"] == "transition" and target in before["governed_documents"]:
            metadata, _ = projections.get(target) or _projection(_local(root, target))
            if event["to_state"] == metadata["governance_state"]:
                matching.add(target)
    for name in sorted(changed - matching):
        finding = {"code": "changed_document_audit_missing", "path": name,
                   "evidence": {"sha256": report["prepared_content"][name]}, "owner": "unknown",
                   "consequence": "Changed knowledge lacks a new event for its final bytes.",
                   "next_action": "Add a matching new audit event, then run the final check."}
        report["deferred_findings" if phase == "prepare" else "findings"].append(finding)
    report["counts"]["new_audit_events"] = len(new)


def check(root, baseline_path, plan_path, *, phase="final", seal=None):
    report = _report("check", root, phase)
    try:
        if phase not in {"prepare", "final"}:
            raise ValueError("Choose prepare or final for the check phase.")
        baseline, manifest_bytes = _baseline(baseline_path, root)
        plan, repositories = _plan(plan_path, root)
        before = _capture(root)
        _retention(report, baseline, before, manifest_bytes, root)
        projections = {name: _projection(_local(root, name)) for name in plan["documents"]}
        report["prepared_content"] = {name: _file_hash(_local(root, name)) for name in plan["documents"]}
        changed = {name for name in plan["documents"] if name in before["governed_documents"]
                   and before["governed_documents"][name] != baseline["governed_documents"].get(name)}
        validation = validate_workspace(root)
        report["workspace_validation"] = validation
        for finding in validation["findings"]:
            if phase == "prepare" and finding["code"] == "audit_state_missing" and finding["path"] in changed:
                report["deferred_findings"].append({**finding, "evidence": finding["message"], "owner": "unknown",
                    "consequence": "The final audit gate remains open.",
                    "next_action": "Add a matching audit event before the final check."})
            else:
                _finding(report, finding["code"], finding["path"], finding["message"])
        cache = {}
        _links_and_code(report, root, plan, repositories, before["manifest"]["records"], projections, cache)
        _executions(report, root, plan, repositories, before["manifest"]["records"], cache)
        _audit_targets(report, root, baseline, before, projections, changed, phase)
        if seal:
            prior = _json(seal)
            hashes = prior.get("prepared_content")
            if (prior.get("operation") != "check" or prior.get("workspace") != str(root)
                    or prior.get("status") not in {"PREPARED", "PASSED"} or prior.get("automated_check") != "PASSED"
                    or not isinstance(hashes, dict) or set(hashes) != set(plan["documents"])):
                raise ValueError("Use a successful checkpoint for the same selected documents and workspace.")
            for name, digest in hashes.items():
                if not isinstance(digest, str) or not _HASH.fullmatch(digest) or report["prepared_content"][name] != digest:
                    _finding(report, "seal_content_changed", name, {"prepared_sha256": digest, "current_sha256": report["prepared_content"][name]},
                             "The checkpoint does not cover these final bytes.", "Review the changed bytes and prepare a new checkpoint.")
        after = _capture(root)
        if before != after or any(_file_hash(_local(root, name)) != digest for name, digest in report["prepared_content"].items()):
            _finding(report, "workspace_changed_during_check", "knowledge", "Evidence changed while the check was running.")
        report["counts"].update(raw_files=len(before["raw_files"]), manifest_records=len(before["manifest"]["records"]),
                                 audit_files=len(before["audit_files"]), selected_documents=len(plan["documents"]),
                                 changed_governed_documents=len(changed), git_blobs=len(cache))
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, yaml.YAMLError, RecursionError, WorkbenchError, subprocess.SubprocessError) as error:
        _finding(report, "input_invalid", "", str(error))
    report["findings"].sort(key=lambda item: (item["path"], item["code"]))
    if not report["findings"]:
        report["status"] = "PREPARED" if phase == "prepare" else "PASSED"
        report["automated_check"] = "PASSED"
    return report


def _output_path(value):
    path = Path(value).expanduser().absolute()
    # System directories can have aliases, such as /var on macOS.
    # Resolve the parent while retaining exclusive creation of the output file.
    if path.is_symlink() or path.exists():
        raise ValueError("Refuse to overwrite an existing harness output.")
    return path.parent.resolve() / path.name


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    for command in ("start", "check"):
        sub = commands.add_parser(command)
        sub.add_argument("--workspace", required=True)
        sub.add_argument("--output", required=True)
        if command == "check":
            sub.add_argument("--baseline", required=True)
            sub.add_argument("--plan", required=True)
            sub.add_argument("--seal")
            sub.add_argument("--phase", choices=("prepare", "final"), default="final")
    args = parser.parse_args(argv)
    report = _report(args.operation, args.workspace, getattr(args, "phase", None))
    output = None
    try:
        output = _output_path(args.output)
        root = Path(args.workspace).expanduser().resolve()
        report["workspace"] = str(root)
        if Path(args.workspace).expanduser().is_symlink() or not root.is_dir():
            raise ValueError("Select an existing regular workspace directory.")
        if args.operation == "start":
            report.update(_capture(root))
            report["counts"] = {"raw_files": len(report["raw_files"]), "audit_files": len(report["audit_files"]),
                                "governed_documents": len(report["governed_documents"]), "manifest_records": len(report["manifest"]["records"])}
            report.update(status="PASSED", automated_check="PASSED")
        else:
            report = check(root, args.baseline, args.plan, phase=args.phase, seal=args.seal)
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, yaml.YAMLError, RecursionError, WorkbenchError) as error:
        _finding(report, "input_invalid", "", str(error))
    if output is not None:
        try:
            _output_path(output)
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("x", encoding="utf-8") as stream:
                json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
                stream.write("\n")
        except (OSError, ValueError) as error:
            report.update(status="FAILED", automated_check="FAILED")
            _finding(report, "output_invalid", str(args.output), str(error), next_action="Choose a new writable output path.")
    print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
    return 0 if report["automated_check"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
