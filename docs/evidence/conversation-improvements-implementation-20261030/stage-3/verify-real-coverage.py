"""Adapt the retained assertion map and verify selected coverage without broadening its claims."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from ai_sdlc_workbench.review_coverage import analyze_coverage


root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
relative_out = out.relative_to(root)
task = Path("tasks/portal-background-session-20261019")
mapping_path = task / "evidence/comprehensive-renewal-20261028/assertion-map.json"
mapping = json.loads((root / mapping_path).read_text())
payload = json.loads((out.parent / "stage-2/session-refresh-index.json").read_text())
payload["id"] = "session-refresh-coverage-pilot"
payload["title"] = "Selected assertion and file-change evidence with the full retained browser inventory"
payload.pop("assessment", None)
artifacts = {a["id"]: a for a in payload["artifacts"]}
catalog = next(a for a in artifacts.values() if a["path"] == (task / "06-test-cases.md").as_posix())
cases = {c["id"]: c for c in payload["cases"]}
mapping_artifact = next(a for a in artifacts.values() if a["path"] == mapping_path.as_posix())
repositories = {"mfe-base": Path("repos/ui/mfe-base"), "ratan-test-engine": Path("repos/testing/ratan-test-engine")}


def artifact(path, kind, **binding):
    path = Path(path).as_posix()
    identifier = "COV-ART-" + hashlib.sha256((path + kind).encode()).hexdigest()[:20]
    artifacts[identifier] = {"id": identifier, "kind": kind, "path": path,
                             "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(), **binding}
    return {"artifact_id": identifier}


def exact_source(reference, kind):
    path = Path(reference["path"])
    if "revision" not in reference:
        assert hashlib.sha256((root / path).read_bytes()).hexdigest() == reference["sha256"]
        return artifact(path, kind) | {"start_line": reference["lines"][0], "end_line": reference["lines"][1]}
    repository = next(name for name, location in repositories.items() if path.is_relative_to(location))
    source_path = path.relative_to(repositories[repository]).as_posix()
    raw = subprocess.check_output(["git", "show", reference["revision"] + ":" + source_path],
                                  cwd=root / repositories[repository])
    assert hashlib.sha256(raw).hexdigest() == reference["sha256"], reference
    destination = relative_out / "source" / repository / reference["revision"] / source_path
    (root / destination).parent.mkdir(parents=True, exist_ok=True)
    (root / destination).write_bytes(raw)
    loc = artifact(destination, kind, repository_id=repository, revision=reference["revision"], source_path=source_path)
    if "lines" in reference:
        loc.update(start_line=reference["lines"][0], end_line=reference["lines"][1])
    return loc


def case(identifier, definition=None):
    if identifier not in cases:
        cases[identifier] = {"id": identifier, "definition": definition or {
            "artifact_id": catalog["id"], "anchor": identifier.lower()},
            "limits": ["A selected source-defined case; canonical source and retained execution remain separate."]}
    return identifier


def link(identifier, relationship, source, target, assertions, conformance="UNKNOWN"):
    payload["links"].append({"id": identifier, "relationship": relationship, "from_id": source,
        "to_id": target, "evidence": [{"artifact_id": mapping_artifact["id"]}], "assertion_ids": assertions,
        "predicate_scope": "SELECTED", "conformance": conformance,
        "limits": ["Imported selected predicate relationship from the retained assertion map.",
                   "This association does not establish full changed-behavior coverage or equivalence."]})


def assertion(identifier, case_id, source):
    payload["assertions"].append({"id": identifier, "case_id": case_id, "source": source,
        "predicate_scope": "SELECTED", "limits": ["Exact selected source range; complete case predicates remain unproved."]})
    return identifier


# The map declares groups, not individual assertion-to-case joins.
# Preserve each group as a derived reference instead of inventing a cross-product.
for entry in mapping["ac_to_assertions"]:
    cid = case("MAP-GROUP-" + entry["ac_id"], {"artifact_id": mapping_artifact["id"]})
    cases[cid]["limits"] = ["Derived assertion-map group; not a new canonical business test case.",
        "Original declared cases: " + ", ".join(entry["cases"]),
        "The original group does not assign each assertion to each individual case."]
    assertions = [assertion("COV-ASSERT-" + entry["ac_id"] + "-" + str(n), cid, exact_source(ref, "TEST"))
                  for n, ref in enumerate(entry["assertions"])]
    original_conformance = entry["conformance"]
    conformance = "MATCH" if original_conformance.startswith("MATCH_WITHIN_") else original_conformance
    link("COV-AC-CASE-" + entry["ac_id"], "AC_CASE", entry["ac_id"], cid, assertions, conformance)

representatives = {"CH-RN-01": "PEND-01", "CH-RN-02": "PEND-07", "CH-RN-03": "OWN-01",
    "CH-RN-04": "DEL-14", "CH-RN-05": "UT-REFRESH-OVERLAP", "CH-RN-06": "OWN-03",
    "CH-RN-07": "DEL-14", "CH-RN-08": "PEND-03", "CH-RN-09": "OWN-08",
    "CH-RN-10": "SR11", "CH-RN-11": "OWN-01", "CH-RN-12": "OWN-01"}
representative_lines = {"CH-RN-01": [149, 159], "CH-RN-02": [195, 203], "CH-RN-03": [201, 208],
    "CH-RN-04": [14, 35], "CH-RN-05": [134, 156], "CH-RN-06": [219, 225],
    "CH-RN-07": [14, 35], "CH-RN-08": [176, 193], "CH-RN-09": [276, 286],
    "CH-RN-10": [540, 607], "CH-RN-11": [201, 208], "CH-RN-12": [201, 208]}
unit_path = task / "evidence/remaining-execution-20261029/full-unit-results.json"
unit = json.loads((root / unit_path).read_text())
unit_ref = artifact(unit_path, "EXECUTION")
binding_path = task / "evidence/remaining-execution-20261029/full-unit-execution.json"
binding_ref = artifact(binding_path, "SOURCE")
binding = json.loads((root / binding_path).read_text())
assert binding["results_sha256"] == hashlib.sha256((root / unit_path).read_bytes()).hexdigest()

for entry in mapping["code_changes"]:
    changed = {"path": (repositories["mfe-base"] / entry["path"]).as_posix(),
               "revision": entry["head"], "sha256": entry["head_sha256"]}
    payload["changes"].append({"id": entry["id"], "classification": "BUSINESS" if entry["classification"] == "behavioral" else "MAINTENANCE",
        "evidence": [exact_source(changed, "CODE"), {"artifact_id": mapping_artifact["id"]}],
        "predicate_scope": "SELECTED", "limits": [entry["limits"],
            "This record is one selected changed file. The complete changed-predicate denominator is UNKNOWN."]})
    test_ref = entry["direct_assertion"]
    selected = representative_lines[entry["id"]]
    assert test_ref["lines"][0] <= selected[0] <= selected[1] <= test_ref["lines"][1]
    test = exact_source({**test_ref, "lines": selected}, "TEST")
    cid = representatives[entry["id"]]
    case(cid, test if cid in {"UT-REFRESH-OVERLAP", "SR11"} else None)
    aid = assertion("COV-ASSERT-" + entry["id"], cid, test)
    link("COV-CHANGE-CASE-" + entry["id"], "CHANGE_CASE", entry["id"], cid, [aid])
    for ac_id in entry["ac_ids"]:
        ac = next(row for row in mapping["ac_to_assertions"] if row["ac_id"] == ac_id)
        declared = "MATCH" if ac["conformance"].startswith("MATCH_WITHIN_") else ac["conformance"]
        link("COV-AC-CHANGE-" + ac_id + "-" + entry["id"], "AC_CHANGE", ac_id, entry["id"], [], declared)
    suite_path = test_ref["path"].removeprefix("repos/ui/mfe-base/")
    matches = [(suite_index, case_index, result) for suite_index, suite in enumerate(unit["testResults"])
        if suite["name"].endswith("/" + suite_path)
        for case_index, result in enumerate(suite["assertionResults"])
        if ("[" + cid + "]") in result["fullName"] or (
            cid == "UT-REFRESH-OVERLAP" and "shares one pending request across overlapping triggers without aborting it" in result["fullName"])]
    assert len(matches) == 1, (entry["id"], cid, matches)
    suite_index, case_index, original = matches[0]
    assert original["status"] == "passed"
    assert binding["revision"] == test_ref["revision"]
    payload["executions"].append({"id": "COV-EXEC-" + entry["id"], "case_id": cid, "source": unit_ref,
        "source_binding": binding_ref, "original_status": original["status"], "outcome": "PASSED",
        "characterization": False, "level": "UNIT", "mode": "CONTROLLED_SOURCE", "assertion_ids": [aid],
        "environment_id": "SESSION-JEST-" + hashlib.sha256((root / binding_path).read_bytes()).hexdigest()[:20],
        "limits": ["Imported result at testResults[%s].assertionResults[%s]." % (suite_index, case_index),
                   "Exact source revision, jsdom, controlled clocks, synthetic credentials, and Axios adapters.",
                   "Only the selected explicit assertion binding is represented. Production acceptance remains unverified."]})

payload["cases"] = list(cases.values())
payload["artifacts"] = list(artifacts.values())
payload["inventory_completeness"].update(changes="SELECTED", cases="SELECTED")
payload["limits"] += ["Twelve selected changed files include six business changes and six supporting maintenance files.",
    "The complete changed-behavior and predicate denominators are UNKNOWN.",
    "The retained browser inventory remains 467 instances. Added source-defined unit cases are selected representatives.",
    "At least one direct selected assertion per changed file does not establish complete assertion coverage."]
(out / "session-coverage-index.json").write_text(json.dumps(payload, indent=2) + "\n")
report = analyze_coverage(payload, root)
assert report["valid"], report["index_check"]["diagnostics"]
assert report["freshness"] == "CURRENT", report["index_check"]["diagnostics"]
assert len(report["matrices"]["AC_CASE"]) == 7
assert len(report["matrices"]["CHANGE_CASE"]) == 12
assert report["change_classifications"] == {"BUSINESS": 6, "MAINTENANCE": 6}
assert report["metrics"]["AC_CASE"]["has_current_assertion_link"]["numerator"] == 7
assert report["metrics"]["CHANGE_CASE"]["has_current_assertion_link"]["numerator"] == 12
assert report["metrics"]["CHANGE_CASE"]["has_matching_passing_execution"]["numerator"] == 12
assert report["metrics"]["CHANGE_CASE"]["has_current_assertion_link"]["whole_scope_percent"] is None
assert report["metrics"]["CHANGE_CASE"]["has_declared_complete_assertion_link"]["numerator"] == 0
assert report["metrics"]["AC_CASE"]["has_matching_passing_execution"]["numerator"] == 0
(out / "session-coverage.json").write_text(json.dumps(report, indent=2) + "\n")
(out / "session-coverage-case.json").write_text(json.dumps({
    "case": "REAL-COVERAGE-01", "recorded_at": datetime.now(timezone.utc).isoformat(), "result": "PASSED",
    "given": "Seven real AC definitions, twelve selected exact file changes, retained assertions, and the 467-instance browser inventory.",
    "when": "Validate the shared index and derive all three coverage matrices.",
    "then": {"metrics": report["metrics"], "classifications": report["change_classifications"],
             "complete_changed_predicate_denominator": "UNKNOWN", "business_verification": report["verification"]},
    "source_sha256": hashlib.sha256((root / "core/review_coverage.py").read_bytes()).hexdigest(),
    "limits": report["limitations"]
}, indent=2) + "\n")
print(json.dumps({"case": "REAL-COVERAGE-01", "result": "PASSED", "changes": len(payload["changes"]),
                  "cases": len(payload["cases"]), "metrics": report["metrics"]}))

# Save the completed Session Refresh case before checking the separate CES scope.
ces = json.loads((out.parent / "stage-1/ces-migration-index.json").read_text())
ces_report = analyze_coverage(ces, root)
assert ces_report["valid"]
assert ces_report["freshness"] == "CURRENT"
assert ces_report["metrics"]["AC_CASE"]["has_current_definition_link"]["denominator"]["inventory_scope"] == "UNKNOWN"
assert ces_report["metrics"]["AC_CASE"]["has_current_definition_link"]["whole_scope_percent"] is None
assert ces_report["metrics"]["CHANGE_CASE"]["has_current_definition_link"]["denominator"]["status"] == "UNKNOWN"
(out / "ces-coverage.json").write_text(json.dumps(ces_report, indent=2) + "\n")
(out / "ces-coverage-case.json").write_text(json.dumps({
    "case": "REAL-COVERAGE-02", "recorded_at": datetime.now(timezone.utc).isoformat(), "result": "PASSED",
    "given": "A real CES draft criterion and unknown approved inventories.",
    "when": "Calculate coverage through the shared index.",
    "then": {"metrics": ces_report["metrics"], "verification": ces_report["verification"]},
    "source_sha256": hashlib.sha256((root / "core/review_coverage.py").read_bytes()).hexdigest(),
    "limits": ["Zero declared changes is not a complete empty denominator. Approved scope remains UNKNOWN."]
}, indent=2) + "\n")
print(json.dumps({"case": "REAL-COVERAGE-02", "result": "PASSED", "metrics": ces_report["metrics"]}))
