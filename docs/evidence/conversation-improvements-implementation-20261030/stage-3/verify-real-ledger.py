"""Verify imports of original retained Session Refresh browser and Jest formats."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from ai_sdlc_workbench.review_coverage import build_case_ledger


root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
task = Path("tasks/portal-background-session-20261019")


def reference(path):
    return {"path": path.as_posix(), "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest()}


browser = {"id": "session-browser", "format": "BROWSER_INVENTORY", "task_root": task.as_posix(),
           **reference(task / "evidence/remaining-execution-20261029/aggregate/final-inventory.json")}
unit = {"id": "session-unit", "format": "JEST_JSON",
        **reference(task / "evidence/remaining-execution-20261029/full-unit-results.json"),
        "binding": reference(task / "evidence/remaining-execution-20261029/full-unit-execution.json")}
manifest = {"schema_version": 1, "scope_id": "portal-background-session-20261019", "sources": [browser, unit]}
(out / "session-ledger-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
report = build_case_ledger(manifest, root)
expected = {"PASSED": 653, "FAILED": 15, "PARTIAL": 199, "BLOCKED": 71}
assert report["valid"], report["diagnostics"]
assert report["freshness"] == "CURRENT", report["diagnostics"]
assert report["counts"]["imported_records"] == 938
assert report["counts"]["unique_attempts"] == 938
assert report["counts"]["outcomes"] == expected, report["counts"]
assert report["counts"]["characterization_passes"] == 25
assert report["imports"][0]["original_summary"]["source_definition_mismatch_count"] == 26
security = next(row for row in report["entries"] if row["case_id"] == "RN-S002")
assert security["runner_original_status"] is None
assert security["outcome"] == "FAILED"
assert report["imports"][1]["original_summary"]["numTotalTestSuites"] == 123
assert report["imports"][1]["unrepresented_declared_tests"] == 0
assert report["verification"] == "NOT_VERIFIED"
(out / "session-ledger.json").write_text(json.dumps(report, indent=2) + "\n")
(out / "session-ledger-case.json").write_text(json.dumps({
    "case": "REAL-LEDGER-01", "recorded_at": datetime.now(timezone.utc).isoformat(), "result": "PASSED",
    "given": "Original 467-instance browser inventory and 471-test Jest result with exact retained hashes.",
    "when": "Import both original formats through build_case_ledger.",
    "then": {"counts": report["counts"], "source_definition_mismatches": 26,
             "unit_suites": 123, "security_raw_status": None, "security_aggregate_outcome": "FAILED"},
    "source_sha256": reference(Path("core/review_coverage.py"))["sha256"],
    "limits": ["This verifies the importer against real retained executions. It starts no business test runner.",
               "The 471 unit outcomes and 467 business instances have separate namespaces and are not combined as business coverage."]
}, indent=2) + "\n")
print(json.dumps({"case": "REAL-LEDGER-01", "result": "PASSED", "counts": report["counts"]}))

# Retain this completed case before starting the repeated-import case.
repeated = {**manifest, "sources": [browser, {**browser, "id": "session-browser-repeat"}, unit]}
repeat_report = build_case_ledger(repeated, root)
assert repeat_report["counts"]["imported_records"] == 1405
assert repeat_report["counts"]["unique_attempts"] == 938
assert repeat_report["counts"]["duplicate_import_records"] == 467
assert repeat_report["counts"]["outcomes"] == expected
(out / "session-repeat-import-case.json").write_text(json.dumps({
    "case": "REAL-LEDGER-02", "recorded_at": datetime.now(timezone.utc).isoformat(), "result": "PASSED",
    "given": "The same retained browser inventory is supplied twice under distinct import IDs.",
    "when": "Import both browser copies with the original Jest result.",
    "then": repeat_report["counts"], "source_sha256": reference(Path("core/review_coverage.py"))["sha256"],
    "limits": ["The repeated input is a controlled importer probe using unchanged real source bytes.",
               "All duplicate provenance remains visible; unique outcome counts remain unchanged."]
}, indent=2) + "\n")
print(json.dumps({"case": "REAL-LEDGER-02", "result": "PASSED", "counts": repeat_report["counts"]}))
