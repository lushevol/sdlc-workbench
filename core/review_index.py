"""Validate derived review references without replacing evidence or granting verification."""

from __future__ import annotations

import hashlib
from importlib.resources import files
import json
from pathlib import Path
import re
import subprocess

from jsonschema import Draft202012Validator

from .assurance import _git_blob, _json, _read, _relative, _repository_paths, local_path, record_sha256
from .models import WorkbenchError
from .workspace import load_workspace


_CATEGORIES = ("artifacts", "criteria", "changes", "cases", "assertions", "links", "executions")
_LIMITATIONS = [
    "Inventory completeness, predicate scope, conformance, and outcomes are declarations requiring source review.",
    "Artifact freshness compares retained bytes and declared Git revisions, not deployed builds or runtime acceptance.",
    "Original runner outcomes, characterization results, and intended business verification remain separate.",
    "Recorded outcomes and assessment decisions are source declarations; this check does not authenticate or recalculate them.",
    "Contract validity never grants business verification, knowledge publication, or deployment authorization.",
]


def schema() -> dict:
    """Return the installed derived review-index contract."""
    return json.loads(files("ai_sdlc_workbench").joinpath("schemas", "review-index.schema.json").read_text())


def read_index(path: str | Path) -> dict:
    """Read strict finite JSON from one stable regular file."""
    try:
        return _json(_read(Path(path)))
    except (ValueError, UnicodeError, OSError, RecursionError):
        raise WorkbenchError("Select a regular review-index file containing strict JSON.") from None


def _freshness(states) -> str:
    values = list(states)
    return "STALE" if "STALE" in values else "UNKNOWN" if not values or "UNKNOWN" in values else "CURRENT"


def _anchors(text: str) -> dict[str, int]:
    """Recognize explicit HTML IDs and GitHub-style Markdown heading anchors."""
    result, heading_counts = {}, {}
    fenced = False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for identifier in re.findall(r'\bid\s*=\s*[\"\']([^\"\']+)[\"\']', line):
            result[identifier] = result.get(identifier, 0) + 1
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", match.group(1)).replace("`", "").lower()
        value = re.sub(r"<[^>]+>", "", value)
        value = re.sub(r"[^\w\- ]", "", value).replace(" ", "-")
        count = heading_counts.get(value, 0)
        heading_counts[value] = count + 1
        identifier = value if count == 0 else f"{value}-{count}"
        result[identifier] = result.get(identifier, 0) + 1
    return result


def analyze_index(payload: dict, root: str | Path) -> dict:
    """Check identities, reference integrity, and source freshness without semantic approval."""
    root = Path(root).resolve()
    report = {"schema_version": 1, "id": payload.get("id") if isinstance(payload, dict) else None,
              "scope_id": payload.get("scope_id") if isinstance(payload, dict) else None,
              "valid": True, "contract_status": "VALID", "freshness": "UNKNOWN",
              "verification": "NOT_VERIFIED", "artifacts": [], "records": {},
              "diagnostics": [], "limitations": list(_LIMITATIONS)}

    def diagnostic(code, identifier, detail, *, invalid=False):
        report["diagnostics"].append({"code": code, "record_id": identifier, "detail": detail})
        if invalid:
            report.update(valid=False, contract_status="INVALID")

    try:
        json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (ValueError, TypeError, RecursionError, UnicodeError):
        diagnostic("invalid_json_values", "index", "Index values must contain finite JSON data.", invalid=True)
        return report
    errors = sorted(Draft202012Validator(schema()).iter_errors(payload), key=lambda item: str(list(item.path)))
    for error in errors[:100]:
        diagnostic("schema_error", "/".join(map(str, error.path)), error.message, invalid=True)
    if errors:
        return report
    report["inventory_completeness"] = payload["inventory_completeness"]
    report["limitations"].extend(payload["limits"])
    records, by_category = {}, {}
    for category in _CATEGORIES:
        by_category[category] = {item["id"]: item for item in payload[category]}
        for record in payload[category]:
            if record["id"] in records:
                diagnostic("duplicate_id", record["id"], "Core record IDs must be globally unique.", invalid=True)
            records[record["id"]] = record
    artifacts = by_category["artifacts"]
    data, snapshots, states, text_cache = {}, {}, {}, {}
    repositories, repository_ids, git_cache = {}, set(), {}
    if any("repository_id" in item for item in payload["artifacts"]):
        try:
            config, _ = load_workspace(root)
            repositories = _repository_paths(config, root)
            repository_ids = {item["id"] for item in config.get("_catalogs", {}).get("repositories", [])}
        except WorkbenchError as error:
            diagnostic("workspace_error", payload["id"], str(error), invalid=True)
    for artifact in payload["artifacts"]:
        identifier, state = artifact["id"], "CURRENT"
        try:
            path = local_path(root, artifact["path"])
            if not path.exists():
                state = "UNKNOWN"
                diagnostic("artifact_missing", identifier, "Retained evidence is unavailable.")
            else:
                raw = _read(path)
                data[identifier] = raw
                snapshots[path] = hashlib.sha256(raw).hexdigest()
                if snapshots[path] != artifact["sha256"]:
                    state = "STALE"
                    diagnostic("artifact_hash_mismatch", identifier, "Retained bytes differ from their declared hash.")
            if "repository_id" in artifact:
                _relative(artifact["source_path"])
                repository_id = artifact["repository_id"]
                if repository_id not in repository_ids:
                    diagnostic("repository_unknown", identifier, "The repository identity is not registered.", invalid=True)
                    state = _freshness([state, "UNKNOWN"])
                elif repository_id not in repositories:
                    state = _freshness([state, "UNKNOWN"])
                    diagnostic("repository_unavailable", identifier, "The registered repository has no local source location.")
                else:
                    key = repository_id, artifact["revision"], artifact["source_path"]
                    if key not in git_cache:
                        git_cache[key] = _git_blob(repositories[repository_id], key[1], key[2])
                    if hashlib.sha256(git_cache[key]).hexdigest() != artifact["sha256"]:
                        state = "STALE"
                        diagnostic("git_hash_mismatch", identifier, "Declared Git source bytes differ from the artifact hash.")
        except (OSError, subprocess.SubprocessError) as error:
            state = _freshness([state, "UNKNOWN"])
            diagnostic("source_unavailable", identifier, type(error).__name__)
        except WorkbenchError as error:
            if "unavailable" in str(error):
                state = _freshness([state, "UNKNOWN"])
                diagnostic("source_unavailable", identifier, str(error))
            else:
                state = "UNKNOWN"
                diagnostic("unsafe_evidence", identifier, str(error), invalid=True)
        states[identifier] = state
        report["artifacts"].append({"id": identifier, "freshness": state, "record_sha256": record_sha256(artifact)})

    def locator(owner, value, kind=None):
        identifier = value["artifact_id"]
        if identifier not in artifacts:
            diagnostic("invalid_artifact_reference", owner, "The locator references an absent artifact.", invalid=True)
            return "UNKNOWN"
        state = states[identifier]
        if kind is not None and artifacts[identifier]["kind"] != kind:
            diagnostic("artifact_kind_mismatch", owner, f"The locator must identify a {kind} artifact.", invalid=True)
            return _freshness([state, "UNKNOWN"])
        if "start_line" not in value and "anchor" not in value:
            return state
        if "start_line" in value and value["end_line"] < value["start_line"]:
            diagnostic("invalid_line_range", owner, "The ending line precedes the starting line.", invalid=True)
            return _freshness([state, "UNKNOWN"])
        if identifier not in data:
            return _freshness([state, "UNKNOWN"])
        if identifier not in text_cache:
            try:
                text = data[identifier].decode("utf-8")
                text_cache[identifier] = {"lines": len(text.splitlines()), "anchors": None, "text": text}
            except UnicodeError:
                text_cache[identifier] = None
        cached = text_cache[identifier]
        if cached is None:
            diagnostic("invalid_text_evidence", owner, "Text locators require UTF-8 evidence.", invalid=True)
            return _freshness([state, "UNKNOWN"])
        if "start_line" in value and value["end_line"] > cached["lines"]:
            diagnostic("invalid_line_range", owner, "The cited range exceeds the retained text.", invalid=True)
            return _freshness([state, "UNKNOWN"])
        if "anchor" in value:
            if cached["anchors"] is None:
                cached["anchors"] = _anchors(cached["text"])
            if cached["anchors"].get(value["anchor"], 0) != 1:
                diagnostic("invalid_anchor", owner, "The anchor is missing or ambiguous in retained evidence.", invalid=True)
                return _freshness([state, "UNKNOWN"])
        return state

    def reference(owner, identifier, category):
        if identifier not in by_category[category]:
            diagnostic("invalid_record_reference", owner, f"The reference must identify a declared {category} record.", invalid=True)
            return "UNKNOWN"
        return states.get(identifier, "UNKNOWN")

    for category in ("criteria", "changes", "cases", "assertions", "links", "executions"):
        rows = []
        for record in payload[category]:
            identifier, inputs = record["id"], []
            if category in {"criteria", "cases"}:
                inputs.append(locator(identifier, record["definition"], "INTENT" if category == "criteria" else None))
            if category == "changes":
                inputs.extend(locator(identifier, item) for item in record["evidence"])
            if category == "assertions":
                inputs += [reference(identifier, record["case_id"], "cases"), locator(identifier, record["source"], "TEST")]
            if category == "links":
                source, target = {"AC_CASE": ("criteria", "cases"), "AC_CHANGE": ("criteria", "changes"),
                                  "CHANGE_CASE": ("changes", "cases")}[record["relationship"]]
                inputs += [reference(identifier, record["from_id"], source), reference(identifier, record["to_id"], target)]
                inputs.extend(locator(identifier, item) for item in record["evidence"])
                for assertion_id in record["assertion_ids"]:
                    inputs.append(reference(identifier, assertion_id, "assertions"))
                    assertion = by_category["assertions"].get(assertion_id)
                    if assertion and target == "cases" and assertion["case_id"] != record["to_id"]:
                        diagnostic("assertion_case_mismatch", identifier, "The assertion belongs to a different target case.", invalid=True)
            if category == "executions":
                inputs += [reference(identifier, record["case_id"], "cases"), locator(identifier, record["source"], "EXECUTION")]
                if "source_binding" in record:
                    inputs.append(locator(identifier, record["source_binding"]))
                for assertion_id in record["assertion_ids"]:
                    inputs.append(reference(identifier, assertion_id, "assertions"))
                    assertion = by_category["assertions"].get(assertion_id)
                    if assertion and assertion["case_id"] != record["case_id"]:
                        diagnostic("assertion_case_mismatch", identifier, "Execution assertions must belong to its declared case.", invalid=True)
            states[identifier] = _freshness(inputs)
            row = {"id": identifier, "freshness": states[identifier], "record_sha256": record_sha256(record)}
            if category == "executions":
                row.update(original_status=record["original_status"], outcome=record["outcome"],
                           characterization=record["characterization"], verification="NOT_VERIFIED")
            rows.append(row)
        report["records"][category] = rows
    assessment = payload.get("assessment")
    assessment_state = []
    if assessment is not None:
        assessment_states = [locator("assessment", assessment["source"])]
        seen = set()
        for issue in assessment["issues"]:
            if issue["id"] in seen:
                diagnostic("duplicate_issue_id", issue["id"], "Assessment issue IDs must be unique.", invalid=True)
            seen.add(issue["id"])
            assessment_states.extend(locator(issue["id"], item) for item in issue["evidence"])
        report["assessment"] = {"freshness": _freshness(assessment_states),
                                "recommendation": assessment["recommendation"], "review_state": assessment["review_state"],
                                "verification": "NOT_VERIFIED"}
        assessment_state.append(report["assessment"]["freshness"])
    report["freshness"] = _freshness([*states.values(), *assessment_state])
    for path, checksum in snapshots.items():
        try:
            changed = hashlib.sha256(_read(path)).hexdigest() != checksum
        except (OSError, WorkbenchError):
            changed = True
        if changed:
            diagnostic("evidence_changed_during_check", payload["id"], "Evidence changed during index inspection.", invalid=True)
            report["freshness"] = "STALE"
    return report
