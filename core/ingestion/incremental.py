"""Plan file-level knowledge work and retain only reviewed successful completions."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote, urlsplit

import yaml

from ..artifact_lint import _FRONTMATTER
from ..context.catalogs import UniqueKeyLoader
from ..governance.validation import _NAVIGATION, _timestamp, is_derived_knowledge_path
from ..models import WorkbenchError
from ..knowledge_layout import knowledge_layout
from ..validation import validate_workspace
from .harness import _destinations
from .sources import (
    _SOURCE_KEYS, _atomic, _collection, _contexts, _digest, _freshness, _hash, _index,
    _index_path, _inventory, _local, _lock, _manifest, _object, _policy,
    _ranges, _read, _relative, _snapshot, _text,
)


_KEPT = {"KEEP", "KEEP_SECTIONS"}
_DECISIONS = _KEPT | {"EXCLUDE", "EVIDENCE_ONLY"}
_INPUT_KEYS = {"source", "present", "decision", "ranges", "selected_sha256", "policy",
               "selection_policy_sha256", "context", "topic", "intent_status", "recipe", "dependencies"}
_DISPOSITIONS = {"updated", "no_change", "excluded", "missing_reviewed"}
_LIMITS = [
    "Affected scope follows declared source citations and canonical Markdown links; missing relationships require bounded topic discovery.",
    "Source hashes, review declarations, and deterministic checkpoints do not authenticate an actor or grant publication approval.",
    "File-level planning still requires complete changed-page review; section-level semantic reuse is not implemented.",
]


def _json(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _fingerprint(value):
    return _digest(_json(value))


def _receipt_path(root, source_id):
    _index_path(root, source_id)
    return (knowledge_layout(root)[1] / "processing" / f"{source_id}.json").relative_to(root).as_posix()


def _canonical_path(root, value):
    path = _local(root, value)
    if (not path.is_relative_to(knowledge_layout(root)[0]) or path.suffix.lower() != ".md"
            or is_derived_knowledge_path(path, root)):
        raise WorkbenchError("Processing outputs must be canonical Markdown paths outside the derived wiki.")
    return path


def _navigation(value):
    return Path(value).name in _NAVIGATION or Path(value).name.casefold() == "log.md"


def _hashes(root, value, *, missing=False):
    if not isinstance(value, dict):
        raise WorkbenchError("Processing bindings require canonical path/SHA-256 objects.")
    for name, digest in value.items():
        _canonical_path(root, name)
        if not _hash(digest) and not (missing and digest is None):
            raise WorkbenchError("Processing bindings require full lowercase SHA-256 values.")
    return value


def _review(value):
    if (not isinstance(value, dict) or set(value) != {"actor", "reviewed_at", "note"}
            or not _text(value["actor"]) or not _text(value["note"])):
        raise WorkbenchError("Record the actual review actor, timestamp, and supporting note.")
    _timestamp(value["reviewed_at"])
    return value


def _receipts(root, source_id, manifest):
    path = _local(root, _receipt_path(root, source_id))
    if not path.exists():
        return {"schema_version": 1, "source_id": source_id, "receipts": {}}
    state = _object(path)
    if (set(state) != {"schema_version", "source_id", "receipts"}
            or type(state.get("schema_version")) is not int or state["schema_version"] != 1
            or state["source_id"] != source_id or not isinstance(state["receipts"], dict)):
        raise WorkbenchError("Use a valid version 1 successful-processing receipt file for this collection.")
    identities = {tuple(item.get(key) for key in sorted(_SOURCE_KEYS))
                  for item in manifest["sources"] if "snapshot" in item}
    keys = {"fingerprint", "input", "starting_fingerprint", "starting_outputs", "disposition",
            "outputs", "review", "checkpoint", "plan_id"}
    for name, receipt in state["receipts"].items():
        _relative(name)
        if (not name.lower().endswith(".md") or not isinstance(receipt, dict) or set(receipt) != keys
                or not _hash(receipt["fingerprint"]) or not _hash(receipt["starting_fingerprint"])
                or not _hash(receipt["plan_id"])
                or not isinstance(receipt["disposition"], str) or receipt["disposition"] not in _DISPOSITIONS
                or not isinstance(receipt["input"], dict) or set(receipt["input"]) != _INPUT_KEYS):
            raise WorkbenchError("Successful-processing receipts require complete retained source identities and dispositions.")
        binding = receipt["input"]
        if (not isinstance(binding["source"], dict) or set(binding["source"]) != _SOURCE_KEYS
                or any(not isinstance(item, str) for item in binding["source"].values())
                or tuple(binding["source"].get(key) for key in sorted(_SOURCE_KEYS)) not in identities
                or type(binding["present"]) is not bool or not isinstance(binding["decision"], str)
                or binding["decision"] not in _DECISIONS or not _hash(binding["selected_sha256"])
                or not isinstance(binding["policy"], dict) or set(binding["policy"]) != {"path", "sha256"}
                or not _hash(binding["policy"]["sha256"])
                or binding["selection_policy_sha256"] != binding["policy"]["sha256"]
                or any(not _text(binding[key]) for key in ("recipe", "topic", "intent_status"))
                or _fingerprint(binding) != receipt["fingerprint"]):
            raise WorkbenchError("Successful-processing input fingerprints must bind complete reviewed selection metadata.")
        _local(root, binding["policy"]["path"])
        _contexts(root, binding["context"])
        raw = _snapshot(root, binding["source"])
        lines = raw.decode("utf-8").splitlines(keepends=True)
        _ranges(binding["decision"], binding["ranges"], len(lines))
        selected = "".join("".join(lines[first - 1:last]) for first, last in binding["ranges"]).encode("utf-8")
        if (_digest(selected) != binding["selected_sha256"]
                or (not binding["present"]) != (receipt["disposition"] == "missing_reviewed")
                or receipt["disposition"] == "excluded" and binding["decision"] not in {"EXCLUDE", "EVIDENCE_ONLY"}):
            raise WorkbenchError("Successful-processing dispositions must match their retained selected input bytes.")
        _hashes(root, receipt["outputs"])
        _hashes(root, receipt["starting_outputs"], missing=True)
        if not receipt["outputs"].keys() <= receipt["starting_outputs"].keys():
            raise WorkbenchError("Successful-processing receipts must retain each output's starting hash.")
        _hashes(root, binding["dependencies"], missing=True)
        if any(binding["dependencies"].get(path) != digest for path, digest in receipt["outputs"].items()
               if not _navigation(path)):
            raise WorkbenchError("Successful-processing fingerprints must include every domain output hash.")
        _review(receipt["review"])
        checkpoint = receipt["checkpoint"]
        if checkpoint is not None and (not isinstance(checkpoint, dict) or set(checkpoint) != {"final", "prepared"}
                or any(not isinstance(binding, dict) or set(binding) != {"path", "sha256"}
                       or not _hash(binding["sha256"]) for binding in checkpoint.values())):
            raise WorkbenchError("Receipt checkpoint bindings must contain exact final and prepared report hashes.")
        if checkpoint is not None:
            for binding in checkpoint.values():
                _local(root, binding["path"])
    return state


def _canonical(root):
    hashes, citations, links, ids = {}, {}, {}, {}
    base = _local(root, knowledge_layout(root)[0].relative_to(root).as_posix())
    for path in sorted(base.rglob("*")):
        if is_derived_knowledge_path(path, root):
            continue
        name = path.relative_to(root).as_posix()
        _local(root, name)
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        raw = _read(_canonical_path(root, name))
        hashes[name] = _digest(raw)
        match = _FRONTMATTER.match(raw.decode("utf-8"))
        metadata, body = {}, raw.decode("utf-8")
        if match:
            try:
                metadata = yaml.load(match.group(1), Loader=UniqueKeyLoader)
                json.dumps(metadata, allow_nan=False)
            except (yaml.YAMLError, TypeError, ValueError, RecursionError):
                raise WorkbenchError("Read valid canonical frontmatter before planning incremental work.") from None
            if not isinstance(metadata, dict):
                raise WorkbenchError("Canonical frontmatter must contain an object.")
            body = match.group(2)
        sources = metadata.get("sources", [])
        if not isinstance(sources, list) or any(not isinstance(item, dict) for item in sources):
            raise WorkbenchError("Canonical sources must list source reference objects.")
        citations[name] = {item["resource"] for item in sources if _text(item.get("resource"))}
        # Navigation is hashed for concurrency, but does not turn every indexed topic into a dependent.
        if _navigation(name):
            continue
        links[name] = {"body": body, "related": metadata.get("related", [])}
        if _text(metadata.get("id")):
            ids[metadata["id"]] = name
    graph = {name: set() for name in links}
    for name, declaration in links.items():
        for destination, _ in _destinations(declaration["body"]):
            if destination is None:
                continue
            try:
                split = urlsplit(destination)
            except ValueError:
                raise WorkbenchError("Use valid URLs in canonical Markdown links before planning incremental work.") from None
            if split.scheme or split.netloc or not split.path:
                continue
            target = unquote(split.path).replace("\\(", "(").replace("\\)", ")")
            if Path(target).is_absolute() or PureWindowsPath(target).drive or "\\" in target or "\x00" in target:
                raise WorkbenchError("Canonical Markdown links must remain inside the workspace.")
            normalized = Path(os.path.normpath((root / name).parent / target))
            if not normalized.is_relative_to(root):
                raise WorkbenchError("Canonical Markdown links must remain inside the workspace.")
            relative = normalized.relative_to(root).as_posix()
            if relative in graph:
                _canonical_path(root, relative)
                graph[name].add(relative)
        related = declaration["related"]
        if isinstance(related, list):
            graph[name].update(ids[item] for item in related if isinstance(item, str) and item in ids)
    return hashes, citations, graph


def _closure(seed, graph, *, reverse=False):
    result = set(seed)
    changed = True
    while changed:
        before = len(result)
        if reverse:
            result.update(name for name, targets in graph.items() if targets & result)
        else:
            result.update(target for name in tuple(result) for target in graph.get(name, ()))
        changed = len(result) != before
    return result


def _capture(root, source_id):
    _collection(root, source_id)
    manifest, manifest_raw = _manifest(root)
    index = _index(root, source_id, manifest)
    if index is None:
        raise WorkbenchError("Refresh the source collection before planning canonical work.")
    index_raw = _read(_local(root, _index_path(root, source_id)))
    receipts = _receipts(root, source_id, manifest)
    inputs = _local(root, index["input_root"])
    incoming = _inventory(root, index["input_root"]) if inputs.exists() else {}
    contexts = {}
    for row in index["sources"]:
        for context in row["context"]:
            target = _local(root, context["path"])
            contexts[context["path"]] = _digest(_read(target)) if target.exists() else None
    hashes, citations, graph = _canonical(root)
    bindings = {"selection_sha256": _digest(index_raw), "manifest_sha256": _digest(manifest_raw),
                "policy": _policy(root, index["policy"]["path"]), "contexts": contexts,
                "inventory_sha256": _fingerprint({name: _digest(raw) for name, raw in incoming.items()})}
    return {"index": index, "receipts": receipts, "bindings": bindings, "canonical_hashes": hashes,
            "citations": citations, "graph": graph, "freshness": _freshness(root, index)}


def _scope(state, row, outputs=()):
    receipt = state["receipts"]["receipts"].get(row["path"])
    direct = {name for name, resources in state["citations"].items() if row["source"]["resource"] in resources}
    direct.update(receipt["outputs"] if receipt else ())
    direct.update(outputs)
    direct = {name for name in direct if not _navigation(name)}
    affected = _closure(direct, state["graph"], reverse=True)
    dependencies = _closure(affected, state["graph"])
    return sorted(affected), {name: state["canonical_hashes"].get(name) for name in sorted(dependencies)}


def _input_binding(root, row, policy, recipe, dependencies):
    raw = _snapshot(root, row["source"])
    lines = raw.decode("utf-8").splitlines(keepends=True)
    selected = "".join("".join(lines[first - 1:last]) for first, last in row["ranges"]).encode("utf-8")
    return {"source": row["source"], "present": row["present"], "decision": row["decision"],
            "ranges": row["ranges"], "selected_sha256": _digest(selected), "policy": policy,
            "selection_policy_sha256": row["policy_sha256"], "context": row["context"],
            "topic": row["topic"], "intent_status": row["intent_status"],
            "recipe": recipe, "dependencies": dependencies}


def _queues(root, state, recipe):
    review, process, unchanged = [], [], 0
    known = {row["path"] for row in state["index"]["sources"]}
    for finding in state["freshness"]:
        if finding["code"] == "input_added":
            review.append({"path": finding["path"], "source": None, "reasons": ["input_added"]})
    for row in state["index"]["sources"]:
        stale = sorted({item["code"] for item in state["freshness"] if item["code"] != "input_missing"
                        and (item["path"] == row["path"] or item["code"] == "policy_changed"
                             or item["path"] in {context["path"] for context in row["context"]})})
        if row["decision"] in {"HOLD", "NEEDS_REVIEW"}:
            stale.append("selection_" + row["decision"].lower())
        if stale:
            review.append({"path": row["path"], "source": row["source"], "reasons": sorted(set(stale))})
            continue
        prior = state["receipts"]["receipts"].get(row["path"])
        affected, dependencies = _scope(state, row)
        fingerprint = _fingerprint(_input_binding(root, row, state["index"]["policy"], recipe, dependencies))
        changed_outputs = prior and any(state["canonical_hashes"].get(name) != digest
                                       for name, digest in prior["outputs"].items() if not _navigation(name))
        if prior and prior["fingerprint"] == fingerprint and not changed_outputs:
            unchanged += 1
            continue
        if (row["present"] and row["decision"] not in _KEPT and not affected
                and not (prior and prior["input"]["decision"] in _KEPT)):
            unchanged += 1
            continue
        reasons = ["not_completed" if prior is None else "inputs_or_dependencies_changed"]
        if not row["present"]:
            reasons.append("input_missing")
        if changed_outputs:
            reasons.append("output_changed_or_missing")
        process.append({"path": row["path"], "fingerprint": fingerprint, "source": row["source"],
                        "decision": row["decision"], "present": row["present"], "reasons": reasons,
                        "affected_knowledge": affected,
                        "starting_outputs": {name: state["canonical_hashes"].get(name) for name in affected}})
    return {"review_queue": review, "process_queue": process,
            "affected_knowledge": sorted({name for item in process for name in item["affected_knowledge"]}),
            "counts": {"documents": len(known), "review": len(review), "process": len(process), "unchanged": unchanged}}


def plan_sources(root: Path, source_id: str, recipe: str = "canonical-v1") -> dict:
    """Return only queued semantic work; keep complete unchanged inventories on disk."""
    root = Path(root).expanduser().resolve()
    if not _text(recipe) or len(recipe) > 160 or "\x00" in recipe:
        raise WorkbenchError("Use a nonempty processing recipe identifier of at most 160 characters.")
    with _lock(root):
        state = _capture(root, source_id)
        queues = _queues(root, state, recipe)
        baseline = {"schema_version": 1, "source_id": source_id, "workspace": str(root), "recipe": recipe,
                    "bindings": state["bindings"], "canonical_hashes": state["canonical_hashes"],
                    "receipt_hashes": {name: _fingerprint(value) for name, value in state["receipts"]["receipts"].items()},
                    **queues}
        raw = _json(baseline)
        digest = _digest(raw)
        name = f".workbench/ingestion/source-plans/{digest}.json"
        path = _local(root, name)
        if path.exists() and _read(path) != raw:
            raise WorkbenchError("A source plan baseline path contains different bytes.")
        if _capture(root, source_id) != state:
            raise WorkbenchError("Source preparation changed during planning; repeat the operation.")
        if not path.exists():
            _atomic(path, raw)
        plan = {"schema_version": 1, "operation": "source_plan", "source_id": source_id,
                "workspace": str(root), "recipe": recipe, "baseline": {"path": name, "sha256": digest},
                **queues, "limits": list(_LIMITS)}
        return {**plan, "generated_at": datetime.now(timezone.utc).isoformat(), "plan_id": _fingerprint(plan)}


def _load_plan(root, source_id, plan_path, *, allow_output_changes=False):
    plan = _object(_local(root, plan_path))
    required = {"schema_version", "operation", "source_id", "workspace", "recipe", "baseline", "review_queue",
                "process_queue", "affected_knowledge", "counts", "limits", "generated_at", "plan_id"}
    if (set(plan) != required or type(plan.get("schema_version")) is not int or plan["schema_version"] != 1
            or plan["operation"] != "source_plan" or plan["source_id"] != source_id or plan["workspace"] != str(root)
            or not _hash(plan["plan_id"]) or not isinstance(plan["baseline"], dict)
            or set(plan["baseline"]) != {"path", "sha256"} or not _hash(plan["baseline"]["sha256"])
            or _fingerprint({key: value for key, value in plan.items() if key not in {"plan_id", "generated_at"}}) != plan["plan_id"]):
        raise WorkbenchError("Use an unchanged source plan generated for this collection and workspace.")
    _timestamp(plan["generated_at"])
    if plan["baseline"]["path"] != f".workbench/ingestion/source-plans/{plan['baseline']['sha256']}.json":
        raise WorkbenchError("Source plans require their original local baseline binding.")
    baseline_path = _local(root, plan["baseline"]["path"])
    if _digest(_read(baseline_path)) != plan["baseline"]["sha256"]:
        raise WorkbenchError("The source plan baseline hash changed.")
    baseline = _object(baseline_path)
    if (set(baseline) != {"schema_version", "source_id", "workspace", "recipe", "bindings", "canonical_hashes",
                         "receipt_hashes", "review_queue", "process_queue", "affected_knowledge", "counts"}
            or any(baseline.get(key) != plan[key] for key in ("schema_version", "source_id", "workspace", "recipe",
                                                           "review_queue", "process_queue", "affected_knowledge", "counts"))):
        raise WorkbenchError("The source plan and its baseline disagree.")
    _hashes(root, baseline["canonical_hashes"])
    state = _capture(root, source_id)
    if state["bindings"] != baseline["bindings"]:
        raise WorkbenchError("Source, policy, or governing context changed after planning; create a new plan.")
    if not allow_output_changes and state["canonical_hashes"] != baseline["canonical_hashes"]:
        raise WorkbenchError("Canonical content changed after planning; create a new plan.")
    if not isinstance(baseline["receipt_hashes"], dict) or any(not _hash(value) for value in baseline["receipt_hashes"].values()):
        raise WorkbenchError("The source plan receipt baseline is invalid.")
    receipts = state["receipts"]["receipts"]
    for name in set(receipts) | set(baseline["receipt_hashes"]):
        receipt = receipts.get(name)
        if (receipt is not None and _fingerprint(receipt) == baseline["receipt_hashes"].get(name)):
            continue
        if not (allow_output_changes and receipt and receipt["plan_id"] == plan["plan_id"]
                and name in {item["path"] for item in plan["process_queue"]}):
            raise WorkbenchError("Successful processing changed after planning; reconcile with a new plan.")
    return plan, baseline, state


def load_plan(root: Path, source_id: str, plan_path: str, *, allow_output_changes=False) -> dict:
    """Read and revalidate a saved source plan without taking the source lock."""
    root = Path(root).expanduser().resolve()
    return _load_plan(root, source_id, plan_path, allow_output_changes=allow_output_changes)[0]


def _checkpoint(root, value, outputs):
    if not isinstance(value, dict) or set(value) != {"final", "prepared"}:
        raise WorkbenchError("Changed outputs require final and prepared ingestion checkpoint paths.")
    reports, bindings = {}, {}
    for phase, name in value.items():
        raw = _read(_local(root, name))
        report = _object(_local(root, name))
        if (report.get("operation") != "check" or report.get("schema_version") != 1
                or report.get("workspace") != str(root) or report.get("automated_check") != "PASSED"
                or report.get("status") != ("PASSED" if phase == "final" else "PREPARED")
                or report.get("phase") != ("final" if phase == "final" else "prepare")
                or not isinstance(report.get("prepared_content"), dict)):
            raise WorkbenchError("Use successful final and prepare ingestion checkpoints for this workspace.")
        for path, digest in report["prepared_content"].items():
            if _local(root, path).suffix.lower() != ".md" or not _hash(digest):
                raise WorkbenchError("Ingestion checkpoints require exact Markdown document hashes.")
        if any(report["prepared_content"].get(name) != digest for name, digest in outputs.items()):
            raise WorkbenchError("The ingestion checkpoint does not bind every reviewed output's current bytes.")
        reports[phase] = report
        bindings[phase] = {"path": name, "sha256": _digest(raw)}
    if (reports["final"].get("seal") != {"sha256": bindings["prepared"]["sha256"]}
            or reports["final"]["prepared_content"] != reports["prepared"]["prepared_content"]):
        raise WorkbenchError("Use a final checkpoint sealed to these exact prepared bytes.")
    return bindings


def complete_sources(root: Path, source_id: str, plan_path: str, results_path: str) -> dict:
    """Commit reviewed per-page successes; failed or omitted work remains retryable."""
    root = Path(root).expanduser().resolve()
    with _lock(root):
        plan, baseline, state = _load_plan(root, source_id, plan_path, allow_output_changes=True)
        results_file = _local(root, results_path)
        results_raw = _read(results_file)
        batch = _object(results_file)
        if (set(batch) != {"schema_version", "source_id", "plan_id", "results"}
                or type(batch.get("schema_version")) is not int or batch["schema_version"] != 1
                or batch["source_id"] != source_id or batch["plan_id"] != plan["plan_id"]
                or not isinstance(batch["results"], list) or not batch["results"]):
            raise WorkbenchError("Use a nonempty completion batch bound to this source plan.")
        queued = {item["path"]: item for item in plan["process_queue"]}
        rows = {row["path"]: row for row in state["index"]["sources"]}
        updates, seen, allowed = {}, set(), set()
        for receipt in state["receipts"]["receipts"].values():
            if receipt["plan_id"] == plan["plan_id"]:
                allowed.update(receipt["outputs"])
        for result in batch["results"]:
            if (not isinstance(result, dict) or not {"path", "disposition", "outputs", "review"} <= result.keys()
                    or result.keys() - {"path", "disposition", "outputs", "review", "checkpoint"}
                    or not isinstance(result["path"], str) or result["path"] not in queued or result["path"] in seen
                    or not isinstance(result["disposition"], str) or result["disposition"] not in _DISPOSITIONS
                    or not isinstance(result["outputs"], list)
                    or any(not isinstance(name, str) for name in result["outputs"])
                    or len(result["outputs"]) != len(set(result["outputs"]))):
                raise WorkbenchError("Complete unique queued source paths with supported dispositions and reviewed output paths.")
            name = result["path"]
            seen.add(name)
            row, item = rows[name], queued[name]
            disposition = result["disposition"]
            if ((not row["present"]) != (disposition == "missing_reviewed")
                    or disposition == "excluded" and row["decision"] not in {"EXCLUDE", "EVIDENCE_ONLY"}):
                raise WorkbenchError("Completion dispositions must agree with source presence and the reviewed selection.")
            review = _review(result["review"])
            outputs = {path: _digest(_read(_canonical_path(root, path))) for path in sorted(result["outputs"])}
            affected, dependencies = _scope(state, row, outputs)
            required_outputs = set(item["starting_outputs"]) | set(affected)
            if not required_outputs <= outputs.keys():
                raise WorkbenchError("Review every affected canonical output, including former and newly discovered dependents.")
            changed = any(baseline["canonical_hashes"].get(path) != digest for path, digest in outputs.items())
            if disposition == "no_change" and changed:
                raise WorkbenchError("A no-change completion must preserve the plan's exact starting output hashes.")
            if disposition == "updated" and not outputs:
                raise WorkbenchError("An updated completion requires at least one reviewed canonical output.")
            checkpoint = None
            if disposition == "updated" or changed:
                checkpoint = _checkpoint(root, result.get("checkpoint"), outputs)
            elif result.get("checkpoint") is not None:
                checkpoint = _checkpoint(root, result["checkpoint"], outputs)
            binding = _input_binding(root, row, state["index"]["policy"], plan["recipe"], dependencies)
            receipt = {"fingerprint": _fingerprint(binding), "input": binding,
                       "starting_fingerprint": item["fingerprint"],
                       "starting_outputs": {path: baseline["canonical_hashes"].get(path) for path in sorted(outputs)},
                       "disposition": disposition, "outputs": outputs, "review": review,
                       "checkpoint": checkpoint, "plan_id": plan["plan_id"]}
            previous = state["receipts"]["receipts"].get(name)
            if previous and previous["plan_id"] == plan["plan_id"] and previous != receipt:
                raise WorkbenchError("This plan already recorded a different completion for this page; create a new plan.")
            updates[name] = receipt
            allowed.update(outputs)
        changed_paths = {name for name in set(baseline["canonical_hashes"]) | set(state["canonical_hashes"])
                         if baseline["canonical_hashes"].get(name) != state["canonical_hashes"].get(name)}
        if changed_paths - allowed:
            raise WorkbenchError("Unrelated canonical content changed after planning; reconcile before completing this plan.")
        prior_receipts = state["receipts"]["receipts"]
        current = {**state, "receipts": {**state["receipts"], "receipts": {**prior_receipts, **updates}}}
        remaining = 0
        for name in queued:
            receipt = current["receipts"]["receipts"].get(name)
            dependencies = _scope(current, rows[name])[1]
            fingerprint = _fingerprint(_input_binding(root, rows[name], state["index"]["policy"], plan["recipe"], dependencies))
            if receipt is None or receipt["plan_id"] != plan["plan_id"] or receipt["fingerprint"] != fingerprint:
                remaining += 1
        validation = validate_workspace(root)
        if not validation["valid"]:
            raise WorkbenchError("Canonical processing requires current successful workspace integrity checks.")
        if _capture(root, source_id) != state or _read(results_file) != results_raw:
            raise WorkbenchError("Inputs or outputs changed during completion; repeat the operation.")
        for receipt in updates.values():
            for binding in (receipt["checkpoint"] or {}).values():
                if _digest(_read(_local(root, binding["path"]))) != binding["sha256"]:
                    raise WorkbenchError("An ingestion checkpoint changed during completion.")
        applied = sum(prior_receipts.get(name) != receipt for name, receipt in updates.items())
        if applied:
            value = {**state["receipts"], "receipts": {**prior_receipts, **updates}}
            _atomic(_local(root, _receipt_path(root, source_id)), _json(value))
        remaining_review = len(plan["review_queue"])
        return {"schema_version": 1, "status": "PARTIAL" if remaining or remaining_review else "COMPLETED", "source_id": source_id,
                "plan_id": plan["plan_id"], "receipts": _receipt_path(root, source_id), "completed": len(updates),
                "written": applied, "remaining": remaining, "remaining_process": remaining, "remaining_review": remaining_review,
                "limits": list(_LIMITS)}
