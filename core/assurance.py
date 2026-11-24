"""Check behavior evidence and compare immutable baselines without granting verification."""

from __future__ import annotations

import hashlib
from importlib.resources import files
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess

from jsonschema import Draft202012Validator

from .models import WorkbenchError
from .workspace import load_workspace


_MAX_BYTES = 16 * 1024 * 1024
_LIMITATIONS = [
    "Contract validity does not establish source meaning, approval, or assertion coverage.",
    "Source freshness compares retained bytes with declared Git revisions, not deployed services.",
    "Assertion bindings are review declarations; original runs do not contain these baseline bindings.",
    "These operations never grant VERIFIED business behavior or authenticate execution results.",
    "Knowledge publication and human approval use the existing knowledge governance contracts.",
]


def schema() -> dict:
    return json.loads(files("ai_sdlc_workbench").joinpath("schemas", "behavior-review.schema.json").read_text())


def record_sha256(record: dict) -> str:
    """Identify metadata separately from retained file bytes."""
    data = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(data.encode()).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON keys must be unique.")
        result[key] = value
    return result


def _json(data: bytes) -> dict:
    def reject_constant(_):
        raise ValueError("JSON numbers must be finite.")
    value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=reject_constant)
    if not isinstance(value, dict):
        raise ValueError("JSON must contain an object.")
    json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
    return value


def _read(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise WorkbenchError("Evidence must use a regular local file.")
    def identity():
        stat = path.stat()
        return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns
    before = identity()
    with path.open("rb") as stream:
        data = stream.read(_MAX_BYTES + 1)
    if len(data) > _MAX_BYTES:
        raise WorkbenchError("Evidence files must not exceed sixteen MiB.")
    if before != identity():
        raise WorkbenchError("An evidence file changed during inspection.")
    return data


def read_baseline(path: Path) -> dict:
    try:
        return _json(_read(Path(path)))
    except (ValueError, UnicodeError, OSError, RecursionError):
        raise WorkbenchError("Select a regular baseline file containing strict JSON.") from None


def _relative(value: str) -> str:
    if (not isinstance(value, str) or not value or "\x00" in value or "\\" in value
            or Path(value).is_absolute() or PureWindowsPath(value).drive
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise WorkbenchError("Use workspace-relative paths without traversal or drive prefixes.")
    return value


def local_path(root: Path, value: str) -> Path:
    """Constrain evidence and save destinations, including missing child paths."""
    target = root
    for part in _relative(value).split("/"):
        target = target / part
        if target.is_symlink():
            raise WorkbenchError("Evidence paths must not contain symbolic links.")
    if not target.resolve().is_relative_to(root):
        raise WorkbenchError("Evidence must stay inside the workspace.")
    return target


def _repository_paths(config: dict, root: Path) -> dict:
    catalogs = config.get("_catalogs", {})
    result = {}
    for repository in catalogs.get("repositories", []):
        location = repository.get("location")
        if not location:
            locations = {item["location"] for item in catalogs.get("sources", [])
                         if item.get("repository_id") == repository["id"] and item["type"] == "git"}
            location = next(iter(locations)) if len(locations) == 1 else None
        if location:
            path = Path(location).expanduser()
            result[repository["id"]] = (path if path.is_absolute() else root / path).resolve()
    return result


def _git_blob(repository: Path, revision: str, source_path: str) -> bytes:
    _relative(source_path)
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0",
                       GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    result = subprocess.run(["git", "--no-pager", "--no-replace-objects", "-c", "core.fsmonitor=false",
                             "-C", str(repository), "show", revision + ":" + source_path],
                            capture_output=True, timeout=20, env=environment)
    if result.returncode or len(result.stdout) > _MAX_BYTES:
        raise WorkbenchError("The exact Git source bytes are unavailable.")
    return result.stdout


def _state(states) -> str:
    values = list(states)
    return "STALE" if "STALE" in values else "UNKNOWN" if not values or "UNKNOWN" in values else "CURRENT"


def analyze_baseline(baseline: dict, root: Path) -> dict:
    """Separate contract errors, freshness diagnostics, and unverified business claims."""
    root = Path(root).resolve()
    report = {"schema_version": 1, "baseline_id": baseline.get("baseline_id") if isinstance(baseline, dict) else None,
              "story_id": baseline.get("story_id") if isinstance(baseline, dict) else None,
              "contract_status": "VALID", "valid": True, "verification": "NOT_VERIFIED",
              "freshness": "UNKNOWN", "artifacts": [], "executions": [], "behaviors": [],
              "metrics": {}, "diagnostics": [], "limitations": list(_LIMITATIONS)}

    def diagnostic(code, identifier, detail, *, invalid=False):
        report["diagnostics"].append({"code": code, "record_id": identifier, "detail": detail})
        if invalid:
            report.update(contract_status="INVALID", valid=False)

    try:
        json.dumps(baseline, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (ValueError, TypeError, RecursionError, UnicodeError):
        diagnostic("invalid_json_values", "baseline", "Baseline values must contain finite JSON data.", invalid=True)
        return report
    errors = sorted(Draft202012Validator(schema()).iter_errors(baseline), key=lambda item: str(list(item.path)))
    for error in errors[:100]:
        diagnostic("schema_error", "/".join(map(str, error.path)), error.message, invalid=True)
    if errors:
        return report
    report["limitations"].extend(baseline["limitations"])
    records = {}
    for category in ("artifacts", "behaviors", "links", "executions", "findings"):
        for record in baseline[category]:
            if record["id"] in records:
                diagnostic("duplicate_id", record["id"], "Record IDs must be globally unique.", invalid=True)
            records[record["id"]] = record
    artifacts = {item["id"]: item for item in baseline["artifacts"]}
    behaviors = {item["id"]: item for item in baseline["behaviors"]}
    links = {item["id"]: item for item in baseline["links"]}
    active = [item for item in baseline["behaviors"] if item["state"] == "ACTIVE"]
    if not active:
        diagnostic("empty_active_scope", baseline["baseline_id"], "Declare at least one active behavior.", invalid=True)
    for behavior in behaviors.values():
        if not behavior["id"].startswith(baseline["story_id"] + ":"):
            diagnostic("behavior_scope", behavior["id"], "Behavior IDs must start with story_id and a colon.", invalid=True)
    try:
        config, _ = load_workspace(root)
        repository_ids = {item["id"] for item in config.get("_catalogs", {}).get("repositories", [])}
        repositories = _repository_paths(config, root)
    except WorkbenchError as error:
        diagnostic("workspace_error", baseline["baseline_id"], str(error), invalid=True)
        return report
    data, snapshots, freshness, stale_records, outdated_records = {}, {}, {}, set(), set()
    git_cache = {}
    for artifact in artifacts.values():
        identity = artifact["id"]
        state = "CURRENT"
        try:
            path = local_path(root, artifact["path"])
            if not path.exists():
                state = "UNKNOWN"
                diagnostic("artifact_missing", identity, "Retained evidence is unavailable.")
            else:
                raw = _read(path)
                data[identity] = raw
                snapshots[path] = hashlib.sha256(raw).hexdigest()
                if snapshots[path] != artifact["sha256"]:
                    state = "STALE"
                    diagnostic("artifact_hash_mismatch", identity, "Retained bytes differ from the declared hash.")
            if "repository_id" in artifact:
                _relative(artifact["source_path"])
                repository_id = artifact["repository_id"]
                if repository_id not in repository_ids:
                    diagnostic("repository_unknown", identity, "The repository ID is not registered.", invalid=True)
                elif repository_id not in repositories:
                    state = _state([state, "UNKNOWN"])
                    diagnostic("repository_unavailable", identity, "The registered repository has no usable local location.")
                else:
                    key = repository_id, artifact["revision"], artifact["source_path"]
                    if key not in git_cache:
                        git_cache[key] = _git_blob(repositories[repository_id], key[1], key[2])
                    if hashlib.sha256(git_cache[key]).hexdigest() != artifact["sha256"]:
                        state = "STALE"
                        diagnostic("git_hash_mismatch", identity, "The selected Git revision has different source bytes.")
        except (OSError, subprocess.SubprocessError) as error:
            state = _state([state, "UNKNOWN"])
            diagnostic("source_unavailable", identity, type(error).__name__)
        except WorkbenchError as error:
            if "unavailable" in str(error):
                state = _state([state, "UNKNOWN"])
                diagnostic("source_unavailable", identity, str(error))
            else:
                diagnostic("unsafe_evidence", identity, str(error), invalid=True)
                state = "UNKNOWN"
        freshness[identity] = state
        if state != "CURRENT":
            stale_records.add(identity)
        if state == "STALE":
            outdated_records.add(identity)
        report["artifacts"].append({"id": identity, "freshness": state, "record_sha256": record_sha256(artifact)})

    def reference(owner, artifact_id, record_hash, start=None, end=None, kind=None):
        target = artifacts.get(artifact_id)
        if target is None or (kind is not None and target["kind"] != kind):
            diagnostic("invalid_artifact_reference", owner, "The artifact reference is absent or has the wrong kind.", invalid=True)
            stale_records.add(owner)
            return
        if record_hash != record_sha256(target):
            diagnostic("artifact_record_changed", owner, "The referenced artifact metadata changed.")
            stale_records.add(owner)
            outdated_records.add(owner)
        if artifact_id in stale_records:
            stale_records.add(owner)
        if artifact_id in outdated_records:
            outdated_records.add(owner)
        if start is not None:
            if end < start:
                diagnostic("invalid_line_range", owner, "The ending line precedes the starting line.", invalid=True)
            elif artifact_id in data:
                try:
                    count = len(data[artifact_id].decode("utf-8").splitlines())
                    if end > count:
                        diagnostic("invalid_line_range", owner, "The cited range exceeds the retained text.", invalid=True)
                except UnicodeError:
                    diagnostic("invalid_text_evidence", owner, "Cited source must contain UTF-8 text.", invalid=True)

    for behavior in behaviors.values():
        locator = behavior["intent"]
        reference(behavior["id"], locator["artifact_id"], locator["record_sha256"],
                  locator["start_line"], locator["end_line"], "INTENT")
    for link in links.values():
        identity = link["id"]
        behavior = behaviors.get(link["behavior_id"])
        if behavior is None:
            diagnostic("invalid_behavior_reference", identity, "The linked behavior does not exist.", invalid=True)
        elif link["behavior_record_sha256"] != record_sha256(behavior) or behavior["id"] in stale_records:
            stale_records.add(identity)
            if link["behavior_record_sha256"] != record_sha256(behavior) or behavior["id"] in outdated_records:
                outdated_records.add(identity)
            diagnostic("behavior_record_changed", identity, "The behavior or its intent dependency changed.")
        reference(identity, link["artifact_id"], link["artifact_record_sha256"], link["start_line"], link["end_line"],
                  "CODE" if link["relationship"] == "IMPLEMENTED_BY" else "TEST")
    for finding in baseline["findings"]:
        if finding["behavior_id"] not in behaviors or any(identifier not in records for identifier in finding["evidence_ids"]):
            diagnostic("invalid_finding_reference", finding["id"], "Finding references must resolve to declared records.", invalid=True)

    for execution in baseline["executions"]:
        identity = execution["id"]
        reference(identity, execution["artifact_id"], execution["artifact_record_sha256"], kind="EXECUTION")
        states = [freshness.get(execution["artifact_id"], "UNKNOWN")]
        result_status, checks = "UNKNOWN", {}
        try:
            result = _json(data[execution["artifact_id"]])
            source_hashes = result.get("source_sha256")
            if (not isinstance(source_hashes, dict) or not source_hashes
                    or any(not isinstance(path, str) or not isinstance(digest, str)
                           or re.fullmatch(r"[a-f0-9]{64}", digest) is None for path, digest in source_hashes.items())):
                raise ValueError("Execution needs a nonempty source_sha256 map.")
            result_status = result.get("status") if result.get("status") in {"PASSED", "FAILED"} else "UNKNOWN"
            for check in result.get("checks", []):
                if (not isinstance(check, dict) or not isinstance(check.get("name"), str)
                        or check["name"] in checks or check.get("status") not in ("PASSED", "FAILED")):
                    raise ValueError("Execution check names must be unique strings.")
                checks[check["name"]] = check.get("status")
            code_by_path = {}
            for identifier in execution["code_artifact_ids"]:
                artifact = artifacts.get(identifier)
                if artifact is None or artifact["kind"] != "CODE":
                    diagnostic("invalid_execution_code", identity, "Execution code references must identify CODE artifacts.", invalid=True)
                    continue
                key = artifact["source_path"]
                if key in code_by_path:
                    diagnostic("ambiguous_execution_code", identity, "One execution cannot bind two versions of one source path.", invalid=True)
                code_by_path[key] = artifact
                states.append(freshness[identifier])
            if len({(item["repository_id"], item["revision"]) for item in code_by_path.values()}) > 1:
                diagnostic("ambiguous_execution_revision", identity, "One source map needs one repository and exact revision.", invalid=True)
            if set(source_hashes) != set(code_by_path):
                states.append("UNKNOWN")
                diagnostic("execution_inventory_incomplete", identity, "Every executed source and bound code artifact needs a matching path.")
            for path, digest in source_hashes.items():
                _relative(path)
                artifact = code_by_path.get(path)
                if artifact is not None and digest != artifact["sha256"]:
                    states.append("STALE")
                    diagnostic("execution_source_hash_mismatch", identity, "Executed source differs at " + path)
            if result_status == "UNKNOWN":
                states.append("UNKNOWN")
        except (KeyError, ValueError, UnicodeError, WorkbenchError, TypeError, RecursionError):
            states.append("UNKNOWN")
            diagnostic("execution_unreadable", identity, "The retained execution does not provide a usable source map and checks.")
        seen_bindings = set()
        for binding in execution["assertion_bindings"]:
            link = links.get(binding["link_id"])
            if link is None or link["relationship"] != "ASSERTED_BY" or binding["link_id"] in seen_bindings:
                diagnostic("invalid_assertion_binding", identity, "Execution bindings need unique assertion links.", invalid=True)
                continue
            seen_bindings.add(binding["link_id"])
            if binding["link_record_sha256"] != record_sha256(link) or link["id"] in stale_records:
                states.append("STALE" if binding["link_record_sha256"] != record_sha256(link)
                              or link["id"] in outdated_records else "UNKNOWN")
                diagnostic("assertion_record_changed", identity, "The declared assertion binding changed.")
            if binding["check_name"] not in checks or checks[binding["check_name"]] not in {"PASSED", "FAILED"}:
                states.append("UNKNOWN")
                diagnostic("execution_check_missing", identity, "The declared check is absent from the original report.")
        if identity in stale_records:
            states.append("STALE" if freshness.get(execution["artifact_id"]) == "STALE" else "UNKNOWN")
        state = _state(states)
        report["executions"].append({"id": identity, "source_freshness": state, "result": result_status,
                                     "mode": execution["mode"], "level": execution["level"],
                                     "assertion_bindings": "DECLARED", "verification": "NOT_VERIFIED",
                                     "limitations": execution["limitations"]})

    execution_states = {item["id"]: item["source_freshness"] for item in report["executions"]}
    for behavior in active:
        current_links = [link for link in links.values() if link["behavior_id"] == behavior["id"]
                         and link["grade"] == "CONFIRMED" and link["id"] not in stale_records]
        code = any(item["relationship"] == "IMPLEMENTED_BY" for item in current_links)
        assertions = any(item["relationship"] == "ASSERTED_BY" for item in current_links)
        required_code = {item["artifact_id"] for item in current_links if item["relationship"] == "IMPLEMENTED_BY"}
        executed = bool(required_code) and any(execution_states[item["id"]] == "CURRENT"
            and required_code <= set(item["code_artifact_ids"]) and any(
            binding["link_id"] in {link["id"] for link in current_links if link["relationship"] == "ASSERTED_BY"}
            for binding in item["assertion_bindings"]) for item in baseline["executions"])
        report["behaviors"].append({"id": behavior["id"], "version": behavior["version"],
                                    "code_mapped": code, "test_mapped": assertions,
                                    "current_source_execution": executed, "verification": "NOT_VERIFIED"})
    denominator = len(active)
    for name, field in (("behavior_to_code", "code_mapped"), ("behavior_to_test", "test_mapped"),
                        ("current_source_execution", "current_source_execution")):
        numerator = sum(row[field] for row in report["behaviors"])
        report["metrics"][name] = {"numerator": numerator, "denominator": denominator,
                                   "percentage": round(100 * numerator / denominator, 2) if denominator else None}
    report["freshness"] = _state([*freshness.values(), *execution_states.values()] if execution_states else ["UNKNOWN", *freshness.values()])
    for path, digest in snapshots.items():
        try:
            if hashlib.sha256(_read(path)).hexdigest() != digest:
                diagnostic("evidence_changed_during_check", baseline["baseline_id"], "Evidence changed during this operation.", invalid=True)
        except (OSError, WorkbenchError):
            diagnostic("evidence_changed_during_check", baseline["baseline_id"], "Evidence became unavailable during this operation.", invalid=True)
    return report


def save_baseline(baseline: dict, root: Path) -> Path:
    root = Path(root).resolve()
    report = analyze_baseline(baseline, root)
    if not report["valid"]:
        raise WorkbenchError("Correct the baseline contract before saving it.")
    destination = local_path(root, "relationships/requirement-code/baselines/" + baseline["baseline_id"] + ".json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(baseline, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    except FileExistsError:
        raise WorkbenchError("The baseline ID already exists. Preserve it and use a new ID.") from None
    return destination


def compare_baselines(before: dict, after: dict, root: Path) -> dict:
    first, second = analyze_baseline(before, root), analyze_baseline(after, root)
    if not first["valid"] or not second["valid"]:
        raise WorkbenchError("Both baseline contracts must be valid before comparison.")
    if before["story_id"] != after["story_id"] or before["baseline_id"] == after["baseline_id"]:
        raise WorkbenchError("Compare distinct baseline IDs from the same story.")
    prior = {item["id"]: item for item in before["behaviors"]}
    current = {item["id"]: item for item in after["behaviors"]}
    if prior.keys() - current.keys():
        raise WorkbenchError("Preserve removed behavior IDs as retired records.")
    for identifier in prior.keys() & current.keys():
        if current[identifier]["version"] < prior[identifier]["version"] or (
                record_sha256(current[identifier]) != record_sha256(prior[identifier])
                and current[identifier]["version"] <= prior[identifier]["version"]):
            raise WorkbenchError("Changed behavior records require increased versions.")
    changes, changed = {}, set()
    for category in ("artifacts", "behaviors", "links", "executions", "findings"):
        left = {item["id"]: item for item in before[category]}
        right = {item["id"]: item for item in after[category]}
        modified = {key for key in left.keys() & right.keys() if record_sha256(left[key]) != record_sha256(right[key])}
        ids = left.keys() ^ right.keys() | modified
        changes[category] = sorted(ids)
        changed.update(ids)
    affected = {identifier for identifier in changed if identifier in prior or identifier in current}
    for baseline in (before, after):
        dependencies = {}
        for behavior in baseline["behaviors"]:
            dependencies[behavior["id"]] = {behavior["intent"]["artifact_id"]}
        for link in baseline["links"]:
            dependencies[link["id"]] = {link["behavior_id"], link["artifact_id"]}
        for execution in baseline["executions"]:
            dependencies[execution["id"]] = {execution["artifact_id"], *execution["code_artifact_ids"],
                                             *(item["link_id"] for item in execution["assertion_bindings"])}
        for finding in baseline["findings"]:
            dependencies[finding["id"]] = set(finding["evidence_ids"])
        impacted = set(changed)
        while True:
            expanded = impacted | {identifier for identifier, inputs in dependencies.items() if inputs & impacted}
            if expanded == impacted:
                break
            impacted = expanded
        affected.update(item["id"] for item in baseline["behaviors"] if item["id"] in impacted)
        affected.update(item["behavior_id"] for item in baseline["links"] if item["id"] in impacted)
        affected.update(item["behavior_id"] for item in baseline["findings"] if item["id"] in impacted)
        for execution in baseline["executions"]:
            if execution["id"] in impacted:
                linked = {binding["link_id"] for binding in execution["assertion_bindings"]}
                affected.update(link["behavior_id"] for link in baseline["links"] if link["id"] in linked)
    return {"schema_version": 1, "story_id": before["story_id"], "changed_records": changes,
            "affected_behaviors": sorted(affected), "before": first, "after": second,
            "verification": "NOT_VERIFIED", "limitations": [
                "Both analyses inspect current retained files; counts do not establish historical assurance improvement.",
                "Changed or removed finding records do not establish approved resolution.", *_LIMITATIONS]}
