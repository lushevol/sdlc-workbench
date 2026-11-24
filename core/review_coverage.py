"""Derive case inventories and traceability views without replacing original evidence."""

from __future__ import annotations

from collections import Counter
import hashlib
from pathlib import Path
import re

from jsonschema import Draft202012Validator

from .assurance import _json, _read, local_path, record_sha256
from .models import WorkbenchError
from .review_index import analyze_index


_LIMITS = [
    "Counts describe declared records and inspected references, not complete business behavior or approval.",
    "Passing execution is distinct from assertion completeness, intended behavior conformance, and acceptance.",
    "Shared criterion associations never establish a direct change-to-test assertion chain.",
]
_OUTCOMES = {"PASSED": "PASSED", "FAILED": "FAILED", "PARTIALLY_EXECUTED": "PARTIAL",
             "PARTIAL": "PARTIAL", "BLOCKED": "BLOCKED", "NOT_RUN": "NOT_RUN", "ERROR": "ERROR",
             "passed": "PASSED", "failed": "FAILED", "pending": "NOT_RUN", "todo": "NOT_RUN",
             "skipped": "NOT_RUN", "disabled": "NOT_RUN"}
_REFERENCE = {"type": "object", "properties": {"path": {"type": "string", "minLength": 1},
              "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"}},
              "required": ["path", "sha256"], "additionalProperties": False}
_MANIFEST = {"type": "object", "properties": {
    "schema_version": {"const": 1}, "scope_id": {"type": "string", "minLength": 1},
    "sources": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string", "minLength": 1},
        "format": {"enum": ["BROWSER_INVENTORY", "JEST_JSON"]},
        "path": _REFERENCE["properties"]["path"], "sha256": _REFERENCE["properties"]["sha256"],
        "task_root": {"type": "string", "minLength": 1}, "binding": _REFERENCE},
        "required": ["id", "format", "path", "sha256"], "additionalProperties": False}}},
    "required": ["schema_version", "scope_id", "sources"], "additionalProperties": False}


def _freshness(states):
    values = list(states)
    return "STALE" if "STALE" in values else "UNKNOWN" if not values or "UNKNOWN" in values else "CURRENT"


def _denominator(count, scope):
    return {"declared_items": count, "inventory_scope": scope,
            "whole_scope_denominator": count if scope == "COMPLETE" else None,
            "status": "EMPTY" if not count and scope == "COMPLETE" else scope,
            "empty_declared_inventory": count == 0}


def _metric(numerator, count, scope):
    return {"numerator": numerator, "denominator": _denominator(count, scope),
            "whole_scope_percent": round(100 * numerator / count, 2) if count and scope == "COMPLETE" else None}


def analyze_coverage(payload: dict, root: str | Path) -> dict:
    """Build three matrices from a checked index; retain unknown and selected denominators."""
    checked = analyze_index(payload, root)
    report = {"schema_version": 1, "scope_id": checked.get("scope_id"), "valid": checked["valid"],
              "freshness": checked["freshness"], "verification": "NOT_VERIFIED", "index_check": checked,
              "matrices": {}, "metrics": {}, "limitations": list(_LIMITS)}
    if not checked["valid"]:
        return report
    states = {item["id"]: item["freshness"] for category in checked["records"].values() for item in category}
    records = {category: {item["id"]: item for item in payload[category]}
               for category in ("criteria", "changes", "cases", "assertions", "executions")}
    executions = {}
    for item in payload["executions"]:
        executions.setdefault(item["case_id"], []).append(item)
    relations = {name: [] for name in ("AC_CASE", "AC_CHANGE", "CHANGE_CASE")}
    for link in payload["links"]:
        relations[link["relationship"]].append(link)
    for relation, source_category, target_category in (("AC_CASE", "criteria", "cases"),
                                                      ("AC_CHANGE", "criteria", "changes"),
                                                      ("CHANGE_CASE", "changes", "cases")):
        rows = []
        for identifier, source in records[source_category].items():
            row = {"id": identifier, "freshness": states[identifier], "links": [],
                   "has_current_definition_link": False, "has_current_assertion_link": False,
                   "has_declared_complete_assertion_link": False, "has_declared_complete_match": False,
                   "has_matching_passing_execution": False}
            required = source.get("required_levels", [])
            passing_levels = set()
            for link in relations[relation]:
                if link["from_id"] != identifier:
                    continue
                assertion_ids = link["assertion_ids"]
                current = states[link["id"]] == "CURRENT"
                asserted = current and bool(assertion_ids) and link["predicate_scope"] != "UNKNOWN"
                asserted = asserted and all(records["assertions"][aid]["predicate_scope"] != "UNKNOWN"
                                            for aid in assertion_ids)
                complete = asserted and source.get("predicate_scope", "COMPLETE") == "COMPLETE" and link["predicate_scope"] == "COMPLETE" and all(
                    records["assertions"][aid]["predicate_scope"] == "COMPLETE" for aid in assertion_ids)
                matched = (current and source.get("predicate_scope", "COMPLETE") == "COMPLETE"
                           and link["predicate_scope"] == "COMPLETE" and link["conformance"] == "MATCH")
                entry = {**link, "freshness": states[link["id"]], "assertions": [records["assertions"][a] for a in assertion_ids],
                         "target": records[target_category][link["to_id"]], "executions": [],
                         "matching_passing_execution_ids": [], "nonpassing_execution_ids": []}
                if relation != "AC_CHANGE":
                    for execution in executions.get(link["to_id"], []):
                        execution_state = states[execution["id"]]
                        # A run must explicitly bind every linked assertion. A shared AC is insufficient.
                        matches = asserted and set(assertion_ids).issubset(execution["assertion_ids"])
                        eligible = (matches and execution_state == "CURRENT" and not execution["characterization"]
                                    and execution["mode"] in {"ACTUAL_IMPLEMENTATION", "CONTROLLED_SOURCE"}
                                    and execution["level"] != "UNKNOWN" and "source_binding" in execution
                                    and execution["environment_id"] is not None)
                        passed = eligible and execution["outcome"] == "PASSED"
                        entry["executions"].append({**execution, "freshness": execution_state,
                                                    "matches_linked_assertions": matches,
                                                    "eligible_passing_evidence": passed})
                        if passed:
                            entry["matching_passing_execution_ids"].append(execution["id"])
                            passing_levels.add(execution["level"])
                        if execution["outcome"] != "PASSED":
                            entry["nonpassing_execution_ids"].append(execution["id"])
                row["links"].append(entry)
                row["has_current_definition_link"] |= current
                row["has_current_assertion_link"] |= asserted
                row["has_declared_complete_assertion_link"] |= complete
                row["has_declared_complete_match"] |= matched
            row["required_levels"] = required
            row["passing_levels"] = sorted(passing_levels)
            row["missing_required_levels"] = sorted(set(required) - passing_levels)
            row["has_matching_passing_execution"] = bool(passing_levels) and not row["missing_required_levels"]
            rows.append(row)
        scope = payload["inventory_completeness"][source_category]
        report["matrices"][relation] = rows
        report["metrics"][relation] = {
            name: _metric(sum(bool(row[name]) for row in rows), len(rows), scope)
            for name in ("has_current_definition_link", "has_current_assertion_link",
                         "has_declared_complete_assertion_link", "has_declared_complete_match",
                         "has_matching_passing_execution") if relation != "AC_CHANGE" or name not in {
                             "has_current_assertion_link", "has_declared_complete_assertion_link", "has_matching_passing_execution"}}
    linked_changes = {link["to_id"] for link in relations["AC_CHANGE"]}
    linked_cases = {link["to_id"] for link in relations["AC_CASE"]}
    report["untraced_changes"] = [c["id"] for c in payload["changes"] if c["id"] not in linked_changes]
    report["unsupported_extra_behavior_candidates"] = [c["id"] for c in payload["changes"]
        if c["id"] not in linked_changes and c["classification"] == "BUSINESS"]
    report["cases_without_criteria"] = [c["id"] for c in payload["cases"] if c["id"] not in linked_cases]
    report["change_classifications"] = dict(Counter(c["classification"] for c in payload["changes"]))
    report["change_groups"] = {}
    for classification in ("BUSINESS", "MAINTENANCE", "TEST_ONLY", "UNCHANGED"):
        identifiers = {c["id"] for c in payload["changes"] if c["classification"] == classification}
        rows = [row for row in report["matrices"]["CHANGE_CASE"] if row["id"] in identifiers]
        report["change_groups"][classification] = {"ids": sorted(identifiers), "metrics": {
            name: _metric(sum(bool(row[name]) for row in rows), len(rows), payload["inventory_completeness"]["changes"])
            for name in report["metrics"]["CHANGE_CASE"]}}
    report["conformance_declarations"] = dict(Counter(link["conformance"] for link in payload["links"]))
    report["execution_outcomes"] = dict(Counter(e["outcome"] for e in payload["executions"]))
    report["characterization_passes"] = [e["id"] for e in payload["executions"]
                                          if e["characterization"] and e["outcome"] == "PASSED"]
    report["limitations"] += [
        "A metric counts source records with at least one declared link; it does not measure all predicates.",
        "Matching passing evidence requires declared assertion and source bindings, a named environment, current references, and every required level.",
        "A matching pass does not erase another failed, partial, blocked, or interrupted attempt.",
        "Complete match counts are review declarations. The tool does not establish semantic equivalence.",
        "Unsupported extra behavior candidates lack declared AC links; their business disposition requires review.",
    ] + payload["limits"]
    return report


def build_case_ledger(manifest: dict, root: str | Path) -> dict:
    """Import retained browser and Jest records, preserving duplicates and original outcomes."""
    errors = sorted(Draft202012Validator(_MANIFEST).iter_errors(manifest), key=lambda e: str(list(e.path)))
    if errors:
        raise WorkbenchError("Invalid case-ledger manifest: " + errors[0].message)
    identifiers = [s["id"] for s in manifest["sources"]]
    if len(set(identifiers)) != len(identifiers):
        raise WorkbenchError("Case-ledger import IDs must be unique; repeated sources use distinct import IDs.")
    root = Path(root).resolve()
    report = {"schema_version": 1, "scope_id": manifest["scope_id"], "valid": True,
              "verification": "NOT_VERIFIED", "imports": [], "entries": [], "diagnostics": [],
              "limitations": list(_LIMITS), "freshness": "UNKNOWN"}
    cache, snapshots, first_attempt = {}, {}, {}

    def evidence(reference):
        path = local_path(root, reference["path"])
        key = (reference["path"], reference["sha256"])
        if key not in cache:
            state, data, digest = "UNKNOWN", None, None
            try:
                raw = _read(path)
                digest = hashlib.sha256(raw).hexdigest()
                snapshots[path] = digest
                state = "CURRENT" if digest == reference["sha256"] else "STALE"
                data = _json(raw)
            except (OSError, ValueError, UnicodeError, RecursionError, WorkbenchError) as error:
                report["diagnostics"].append({"path": reference["path"], "code": "evidence_unavailable",
                                               "detail": type(error).__name__})
                if isinstance(error, (ValueError, UnicodeError, RecursionError)):
                    report["valid"] = False
                    state = "UNKNOWN"
            cache[key] = {"path": reference["path"], "expected_sha256": reference["sha256"],
                          "actual_sha256": digest, "freshness": state, "data": data}
        return cache[key]

    def browser_reference(source, value, checksum, workspace=False):
        if not isinstance(value, str) or not isinstance(checksum, str) or not re.fullmatch(r"[a-f0-9]{64}", checksum):
            return {"path": value, "expected_sha256": checksum, "freshness": "UNKNOWN", "data": None}
        relative = value if workspace else str(Path(source.get("task_root", "")) / value)
        return evidence({"path": relative, "sha256": checksum})

    def add_entry(entry, identity, source):
        entry["attempt_id"] = "ATTEMPT-" + record_sha256(identity)
        entry["entry_id"] = source["id"] + ":" + str(entry["ordinal"])
        entry["import_id"] = source["id"]
        entry["duplicate_of"] = first_attempt.get(entry["attempt_id"])
        first_attempt.setdefault(entry["attempt_id"], entry["entry_id"])
        entry["verification"] = "NOT_VERIFIED"
        report["entries"].append(entry)

    for source in manifest["sources"]:
        retained = evidence(source)
        binding = evidence(source["binding"]) if "binding" in source else None
        imported = {"id": source["id"], "format": source["format"],
                    "source": {k: v for k, v in retained.items() if k != "data"},
                    "binding": {k: v for k, v in binding.items() if k != "data"} if binding else None,
                    "freshness": _freshness([retained["freshness"]] + ([binding["freshness"]] if binding else []))}
        report["imports"].append(imported)
        data = retained["data"]
        if data is None:
            continue
        start = len(report["entries"])
        if source["format"] == "BROWSER_INVENTORY":
            if not isinstance(data.get("rows"), list) or not all(isinstance(row, dict) and isinstance(row.get("id"), str)
                                                                for row in data["rows"]):
                raise WorkbenchError("A browser inventory must contain rows with string case IDs.")
            imported["original_summary"] = {key: data.get(key) for key in (
                "status", "total", "counts", "source_definition_mismatch_count", "source_definition_mismatch_ids",
                "characterization_passed_ids", "scope_limits")}
            for ordinal, row in enumerate(data["rows"]):
                result = browser_reference(source, row.get("result_workspace_path") or row.get("result"),
                                           row.get("result_sha256"), workspace=bool(row.get("result_workspace_path")))
                bound = browser_reference(source, row.get("source_binding"), row.get("source_binding_sha256"))
                result_data = result["data"] or {}
                original = row.get("original_status")
                status = row.get("status")
                if not isinstance(status, (str, type(None))) or not isinstance(original, (str, type(None))):
                    raise WorkbenchError("Browser statuses must remain strings or null.")
                entry = {"ordinal": ordinal, "case_id": row["id"], "case_namespace": "BROWSER_INVENTORY",
                    "case_instance_identity": row["id"], "case_identity_basis": "DECLARED_CASE_ID",
                    "original_status": original, "aggregate_status": status, "runner_original_status": result_data.get("status"),
                    "outcome": _OUTCOMES.get(status, "UNKNOWN"), "characterization": row.get("characterization"),
                    "basis": row.get("basis"), "business_acceptance": row.get("business_acceptance"),
                    "assertion_count": row.get("assertion_count"), "failed_assertions": row.get("failed_assertions"),
                    "blocked_predicates": row.get("blocked_predicates"), "ac_ids": row.get("ac_ids"),
                    "definition": row.get("definition"), "definition_identity": row.get("definition_identity"),
                    "definition_sources": row.get("definition_sources"), "source_revision": row.get("revision"),
                    "execution_level": row.get("execution_level"), "execution_status": row.get("execution_status"),
                    "status_normalization": row.get("status_normalization"), "limits": row.get("limits", []),
                    "result": {k: v for k, v in result.items() if k != "data"},
                    "source_binding": {k: v for k, v in bound.items() if k != "data"},
                    "runner_source_identity": {k: result_data.get(k) for k in ("revision", "source_revision", "execution_mode",
                        "execution_class", "executed_source_identity", "definition_source_limit", "source_binding")},
                    "freshness": _freshness([imported["freshness"], result["freshness"], bound["freshness"]]),
                    "runner_progress": {k: result_data.get(k) for k in ("stage", "started_at", "completed_at")},
                    "interrupted": result_data.get("wasInterrupted", result_data.get("interrupted"))}
                identity = {"format": source["format"], "case_id": row["id"],
                            "result_path": result["path"], "result_sha256": result.get("expected_sha256"),
                            "aggregate_record_sha256": record_sha256(row)}
                if not result.get("expected_sha256"):
                    identity.update(inventory_path=source["path"], inventory_sha256=source["sha256"], ordinal=ordinal)
                add_entry(entry, identity, source)
        else:
            if not isinstance(data.get("testResults"), list):
                raise WorkbenchError("A Jest result must contain a testResults list.")
            imported["original_summary"] = {key: value for key, value in data.items() if key != "testResults"}
            imported["suite_diagnostics"] = []
            if binding and binding["data"] and binding["data"].get("results_sha256") != source["sha256"]:
                imported["freshness"] = "STALE"
                report["diagnostics"].append({"path": source["path"], "code": "binding_result_mismatch",
                                               "detail": "The execution binding identifies different result bytes."})
            for suite_index, suite in enumerate(data["testResults"]):
                if not isinstance(suite, dict) or not isinstance(suite.get("assertionResults"), list):
                    raise WorkbenchError("A Jest suite must contain an assertionResults list.")
                imported["suite_diagnostics"].append({key: value for key, value in suite.items() if key != "assertionResults"})
                for case_index, case in enumerate(suite["assertionResults"]):
                    if not isinstance(case, dict) or not isinstance(case.get("status"), (str, type(None))):
                        raise WorkbenchError("A Jest case must contain an original string or null status.")
                    invocations = case.get("invocations")
                    retry_count = invocations - 1 if isinstance(invocations, int) and not isinstance(invocations, bool) and invocations > 0 else None
                    entry = {"ordinal": len(report["entries"]) - start, "case_namespace": "JEST_JSON",
                        "case_id": str(suite.get("name")) + "::" + str(case.get("fullName")),
                        "case_instance_identity": str(suite.get("name")) + "::" + str(suite_index) + ":" + str(case_index),
                        "case_identity_basis": "RUNNER_POSITION_WITHIN_RETAINED_RESULT",
                        "suite": suite.get("name"), "original_status": case.get("status"),
                        "outcome": _OUTCOMES.get(case.get("status"), "UNKNOWN"), "characterization": None,
                        "source_revision": binding["data"].get("revision") if binding and binding["data"] else None,
                        "execution_level": "UNIT", "freshness": imported["freshness"],
                        "interrupted": data.get("wasInterrupted"), "invocations": invocations,
                        "retry_count": retry_count, "prior_attempt_outcomes": "UNKNOWN" if retry_count else "NOT_DECLARED",
                        "original_case": case, "suite_index": suite_index, "case_index": case_index}
                    add_entry(entry, {"format": source["format"], "path": source["path"], "sha256": source["sha256"],
                                      "suite_index": suite_index, "case_index": case_index}, source)
            count = len(report["entries"]) - start
            total = data.get("numTotalTests")
            imported["unrepresented_declared_tests"] = max(total - count, 0) if isinstance(total, int) and not isinstance(total, bool) else None
        imported["imported_records"] = len(report["entries"]) - start
    unique = [entry for entry in report["entries"] if entry["duplicate_of"] is None]
    report["counts"] = {"imported_records": len(report["entries"]), "unique_attempts": len(unique),
        "duplicate_import_records": len(report["entries"]) - len(unique),
        "unique_case_instances": len({(entry["case_namespace"], entry["case_instance_identity"]) for entry in unique}),
        "distinct_case_names": len({(entry["case_namespace"], entry["case_id"]) for entry in unique}),
        "outcomes": dict(Counter(entry["outcome"] for entry in unique)),
        "characterization_passes": sum(entry["outcome"] == "PASSED" and entry["characterization"] is True for entry in unique),
        "interrupted_records": sum(entry["interrupted"] is True for entry in unique),
        "retried_case_records": sum(bool(entry.get("retry_count")) for entry in unique),
        "freshness": dict(Counter(entry["freshness"] for entry in unique))}
    report["freshness"] = _freshness([item["freshness"] for item in report["imports"]] + [e["freshness"] for e in unique])
    for path, digest in snapshots.items():
        try:
            changed = hashlib.sha256(_read(path)).hexdigest() != digest
        except (OSError, WorkbenchError):
            changed = True
        if changed:
            report.update(valid=False, freshness="STALE")
            report["diagnostics"].append({"path": str(path.relative_to(root)), "code": "evidence_changed_during_check"})
    report["limitations"] += [
        "Import records retain duplicates. Unique-attempt counts exclude only identical retained attempt identities.",
        "Browser aggregate dispositions and raw runner statuses remain separate, including absent raw statuses.",
        "A Jest final pass does not establish prior retry outcomes. Retry metadata and interrupted runs remain visible.",
        "Repeated Jest names retain separate runner positions; those positions do not establish canonical cross-run case identity.",
        "Source freshness checks retained bytes and wrapper bindings. It does not compare deployed or current checkout identity.",
        "Missing result bytes and unknown statuses remain unknown. They are not inferred product failures or passes.",
        "A completed importer or an aggregate PASSED status does not establish that every business case passed.",
    ]
    return report
