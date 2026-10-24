#!/usr/bin/env python3
"""Validate release evidence integrity without changing cases, progress, or fixtures.

The default permits explicitly pending browser cases. --final requires usable
selected attempts for all 22 cases. Execution errors and invalid comparisons do
not count. Valid test failures remain evidence; this grants no release approval.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tarfile
from urllib.parse import unquote, urlsplit


STAGE = Path(__file__).resolve().parent
ROOT = STAGE.parents[3]
TASK = STAGE.parents[1]
APP = ROOT / "repos/ui/mfe-base"
TEST_REPO = ROOT / "repos/testing/ratan-test-engine"
FINAL_REVISION = "ae8213f2963047e7c126d01f4003cee1236abc25"
EXPECTED_IDS = {f"E2E-{number:02d}" for number in range(1, 23)}
CHECKS = []


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def load(path):
    return json.loads(path.read_text())


def check(name, passed, **detail):
    CHECKS.append({"check": name, "passed": bool(passed), **detail})
    return bool(passed)


def git_bytes(repository, revision, path):
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=repository)


def bound_file(binding, base, label):
    path = (base / binding["path"]).resolve()
    exists = path.is_file() and not path.is_symlink()
    actual = sha(path) if exists else None
    check(label, exists and actual == binding["sha256"], path=str(path.relative_to(ROOT))
          if path.is_relative_to(ROOT) else str(path), expected_sha256=binding["sha256"], actual_sha256=actual)
    return path if exists else None


def case_definition(text, case_id):
    found = re.search(rf"(?ms)^### {re.escape(case_id)}\n.*?(?=^### |^## |\Z)", text)
    return found.group().encode() if found else b""


def invalid_comparison(*records):
    """Recognize explicit invalidation without interpreting business assertions."""
    for record in records:
        if not isinstance(record, dict):
            continue
        if any(record.get(key) is False for key in ["comparison_valid", "comparisonValid", "valid_comparison"]):
            return True
        if any(record.get(key) is True for key in ["invalid_comparison", "invalidComparison"]):
            return True
        if any(str(record.get(key, "")).upper() in {"INVALID", "INVALID_COMPARISON", "UNUSABLE",
                                                  "SETUP_FAILED", "EXECUTION_ERROR", "INVALID_SETUP", "INVALID_CONTROL"}
               for key in ["comparison_validity", "comparison_status", "evidence_validity", "execution_validity"]):
            return True
    return False


def cleanup_execution_error(*records):
    return any(str(record.get("error", "")).startswith("ENOTEMPTY:")
               for record in records if isinstance(record, dict))


def classify(case_id, status, *records):
    if invalid_comparison(*records) or cleanup_execution_error(*records):
        return "EXECUTION_ERROR"
    if (status == "FAILED" and case_id in {"E2E-15", "E2E-19", "E2E-21"}
            and any(isinstance(record, dict)
                    and str(record.get("error", "")).startswith("page.waitForFunction: Timeout")
                    for record in records)):
        return "EXECUTION_ERROR"
    if (case_id == "E2E-07" and any(isinstance(record, dict)
            and any(event.get("event") == "visibilitychange" and event.get("visibility") == "hidden"
                    for event in (record.get("controlLifecycle") or {}).get("events", []))
            for record in records)):
        return "EXECUTION_ERROR"
    if case_id in {"E2E-21", "E2E-22"}:
        return "OBSERVATION_ONLY" if status == "PASSED" else "OBSERVATION_FAILED"
    if case_id == "E2E-12":
        return "DIAGNOSTIC_PASSED" if status == "PASSED" else "DIAGNOSTIC_FAILED"
    return status


def locked_scope_reasons(case, selected):
    """Keep locked runs within their reviewed DOM and service scope."""
    context_path = STAGE / "setup/locked-mac-case-scope.json"
    context = load(context_path) if context_path.is_file() else {}
    context_ids = {row["id"] for row in context.get("eligible_cases", [])}
    scoped = (case["id"] in context_ids or any(record.get("scope_evidence")
              or record.get("execution_scope") == "DOM_SERVICE_ONLY" for record in [case, selected]))
    if not scoped:
        return []
    reasons = []
    if case.get("execution_scope") != "DOM_SERVICE_ONLY" or selected.get("execution_scope") != "DOM_SERVICE_ONLY":
        reasons.append("LOCKED_SCOPE_CONFLICT")
    expected_limit = "macOS locked; no physical user UI or lifecycle verification"
    if case.get("environment_limit") != expected_limit or selected.get("environment_limit") != expected_limit:
        reasons.append("LOCKED_ENVIRONMENT_LIMIT_MISSING")
    binding = selected.get("scope_evidence")
    if not binding or case.get("scope_evidence") != binding:
        reasons.append("LOCKED_SCOPE_BINDING_MISSING")
        return reasons
    path = STAGE / binding["path"]
    if not path.is_file() or sha(path) != binding.get("sha256"):
        reasons.append("LOCKED_SCOPE_HASH_MISMATCH")
        return reasons
    scope = load(path)
    row = next((row for row in scope.get("eligible_cases", []) if row["id"] == case["id"]), None)
    if scope.get("readiness") != "READY" or not row or row.get("mode") != case.get("mode"):
        reasons.append("CASE_OUTSIDE_READY_LOCKED_SCOPE")
    elif row.get("native_visibility_transition_required") is not False:
        reasons.append("LOCKED_NATIVE_VISIBILITY_REQUIRED")
    if case.get("comparison_valid") is not True or selected.get("comparison_valid") is not True:
        reasons.append("LOCKED_SETUP_AND_COMPARISON_NOT_VALIDATED")
    if case.get("evidence_validity") != "VALID" or selected.get("evidence_validity") != "VALID":
        reasons.append("LOCKED_ASSERTION_SCOPE_NOT_VALIDATED")
    return reasons


def case_eligibility(case):
    """Only a usable selected attempt counts toward the final 22 cases."""
    accepted = {"PASSED", "FAILED", "OBSERVATION_ONLY", "OBSERVATION_FAILED",
                "DIAGNOSTIC_PASSED", "DIAGNOSTIC_FAILED"}
    reasons = []
    result_binding = case.get("candidate_result")
    attempts = case.get("candidate_attempts", [])
    selected = attempts[-1] if attempts else {}
    if not result_binding:
        reasons.append("NO_RETAINED_ASSERTION_RESULT")
    if case.get("candidate_business_outcome") not in accepted:
        reasons.append("SELECTED_OUTCOME_IS_NOT_USABLE")
    if not selected:
        reasons.append("NO_SELECTED_ATTEMPT")
    elif (selected.get("result") != result_binding or selected.get("run") != case.get("candidate_run")):
        reasons.append("SELECTED_ATTEMPT_BINDING_MISMATCH")
    if selected and selected.get("business_outcome") != case.get("candidate_business_outcome"):
        reasons.append("SELECTED_OUTCOME_CONFLICT")
    result_path = STAGE / result_binding["path"] if result_binding else None
    result = load(result_path) if result_path and result_path.is_file() else {}
    run_binding = case.get("candidate_run")
    run_path = STAGE / run_binding["path"] if run_binding else None
    run = load(run_path) if run_path and run_path.is_file() else {}
    if invalid_comparison(case, selected, result, run):
        reasons.append("INVALID_COMPARISON")
    if cleanup_execution_error(case, selected, result, run):
        reasons.append("CLEANUP_EXECUTION_ERROR")
    if result and classify(case["id"], result.get("status"), case, selected, result, run) != case.get("candidate_business_outcome"):
        reasons.append("SELECTED_CLASSIFICATION_CONFLICT")
    reasons.extend(locked_scope_reasons(case, selected))
    return {"id": case["id"], "eligible": not reasons, "reasons": reasons,
            "selected_outcome": case.get("candidate_business_outcome", "NOT_RUN"),
            "execution_scope": case.get("execution_scope"), "environment_limit": case.get("environment_limit"),
            "scope_evidence": case.get("scope_evidence")}


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def png_ok(path):
    data = path.read_bytes()
    return (len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n"
            and data[12:16] == b"IHDR" and all(struct.unpack(">II", data[16:24])))


def validate_candidate(case):
    attempts = case.get("candidate_attempts", [])
    for index, attempt in enumerate(attempts, 1):
        label = f"candidate:{case['id']}:attempt:{index}"
        run_path = bound_file(attempt["run"], STAGE, label + ":run-hash")
        retention_path = bound_file(attempt["retention"], STAGE, label + ":retention-hash")
        result_path = bound_file(attempt["result"], STAGE, label + ":result-hash") if attempt.get("result") else None
        if not run_path or not retention_path:
            continue
        run, retention = load(run_path), load(retention_path)
        check(label + ":identity", run.get("mode") == case["mode"] and retention.get("id") == case["id"])
        check(label + ":original-assertions", run.get("extensionSha256") == case["assertion_module_sha256"]
              == retention.get("original_assertion_sha256"))
        check(label + ":completed-run", bool(run.get("completedAt")) and run.get("status") in {"PASSED", "FAILED"})
        context_path = STAGE / "setup/locked-mac-case-scope.json"
        context = load(context_path) if context_path.is_file() else {}
        scoped_ids = {row["id"] for row in context.get("eligible_cases", [])}
        if attempt.get("execution_scope") == "DOM_SERVICE_ONLY" or case["id"] in scoped_ids:
            check(label + ":locked-scope-declared", attempt.get("execution_scope") == "DOM_SERVICE_ONLY")
            scope_binding = attempt.get("scope_evidence")
            scope_path = bound_file(scope_binding, STAGE, label + ":locked-scope-hash") if scope_binding else None
            check(label + ":locked-scope-retained", bool(scope_path),
                  execution_scope="DOM_SERVICE_ONLY", environment_limit=attempt.get("environment_limit"))
            if attempt.get("business_outcome") != "EXECUTION_ERROR":
                # Compare this attempt with its own metadata; earlier attempts
                # remain independent after another attempt becomes selected.
                attempt_case = {**case, **{key: attempt.get(key) for key in
                    ["execution_scope", "environment_limit", "scope_evidence", "comparison_valid", "evidence_validity"]}}
                check(label + ":locked-original-conditions", not locked_scope_reasons(attempt_case, attempt),
                      limitations=locked_scope_reasons(attempt_case, attempt))
        files = {entry["path"]: entry for entry in retention.get("files", [])}
        for binding in files.values():
            bound_file(binding, STAGE, label + ":artifact-hash")
        check(label + ":no-profiles", retention.get("profile_directories_copied") is False
              and all(Path(name).suffix in {".json", ".png"} for name in files))
        if result_path is None:
            check(label + ":execution-error-disclosed", attempt.get("business_outcome") == "EXECUTION_ERROR")
            continue
        result = load(result_path)
        check(label + ":result-identity", result.get("caseId") == case["case_id"])
        check(label + ":result-assertions", result.get("testSourceSha256") == case["assertion_module_sha256"])
        check(label + ":result-status", result.get("status") == run.get("status")
              and (attempt.get("business_outcome") == "EXECUTION_ERROR"
                   or attempt.get("business_outcome") == classify(case["id"], result.get("status"), attempt, result, run)))
        check(label + ":clock", result.get("clock") == run.get("clock") == "REAL_WALL_CLOCK")
        check(label + ":time-binding", bool(result.get("completedAt"))
              and timestamp(run["startedAt"]) <= timestamp(result["startedAt"])
              <= timestamp(result["completedAt"]) <= timestamp(run["completedAt"]))
        shots = result.get("screenshots", [])
        check(label + ":screenshots-listed", bool(shots))
        for shot in shots:
            name = shot["file"]
            target = result_path.parent / name
            relative = str(target.relative_to(STAGE))
            safe = Path(name).name == name and target.suffix.lower() == ".png"
            check(label + ":screenshot", safe and target.is_file() and relative in files
                  and png_ok(target), path=relative, phase=shot.get("phase"))
    if case.get("candidate_result"):
        check(f"candidate:{case['id']}:latest-result", bool(attempts)
              and case["candidate_result"] == attempts[-1].get("result")
              and case.get("candidate_run") == attempts[-1].get("run"))


def markdown_checks(path):
    content = path.read_text()
    failures, count = [], 0
    for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content):
        target = target.strip("<>")
        if urlsplit(target).scheme or target.startswith("//"):
            continue
        count += 1
        name, _, anchor = unquote(target).partition("#")
        located = (path.parent / name).resolve() if name else path
        if not located.is_file():
            failures.append({"label": label, "target": target, "reason": "missing-file"})
            continue
        if not anchor:
            continue
        text = located.read_text(errors="replace")
        line = re.fullmatch(r"L(\d+)(?:-L?(\d+))?", anchor)
        if line:
            first, last = int(line[1]), int(line[2] or line[1])
            if not 1 <= first <= last <= len(text.splitlines()):
                failures.append({"label": label, "target": target, "reason": "invalid-line-locator"})
            continue
        headings = []
        for heading in text.splitlines():
            if heading.startswith("#"):
                slug = re.sub(r"[^\w -]", "", heading.lstrip("#").strip().lower()).replace(" ", "-")
                headings.append(slug)
        explicit = re.findall(r'(?:id|name)=["\']([^"\']+)["\']', text)
        if anchor not in headings + explicit:
            failures.append({"label": label, "target": target, "reason": "missing-heading-anchor"})
    check("markdown-links:" + str(path.relative_to(ROOT)), not failures,
          checked_links=count, failures=failures, sha256=sha(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true", help="Require all 22 completed retained assertion results")
    parser.add_argument("--output", type=Path, default=STAGE / "implementation-validation.json")
    args = parser.parse_args()
    initial_files = {name: sha(STAGE / name) for name in ["case-inventory.json", "progress.json"]}
    inputs, binding, inventory, progress = [load(STAGE / name) for name in
                                           ["inputs.json", "commit-binding.json", "case-inventory.json", "progress.json"]]
    source = load(STAGE / "setup/source-binding.json")
    check("final-commit-identity", binding["candidate_revision"] == inventory["candidate_application_revision"]
          == progress["current_candidate_revision"] == FINAL_REVISION)
    check("three-committed-files", len(binding["files"]) == 3)
    committed_names = subprocess.check_output(["git", "diff", "--name-only", binding["base_revision"],
                                              FINAL_REVISION], cwd=APP, text=True).splitlines()
    check("commit-scope", set(committed_names) == {entry["path"] for entry in binding["files"]}, paths=committed_names)
    for entry in binding["files"]:
        actual = digest(git_bytes(APP, FINAL_REVISION, entry["path"]))
        check("commit-binding:" + entry["path"], actual == entry["sha256"]
              == sha(APP / entry["path"]) == inventory["candidate_source_hashes"][entry["path"]], actual_sha256=actual)

    archive = subprocess.check_output(["git", "archive", "--format=tar", FINAL_REVISION, "--", "src"], cwd=APP)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        committed = {item.name: tar.extractfile(item).read() for item in tar if item.isfile()}
    exported_root = Path(source["runtime"]) / "mfe/source"
    manifest = {entry["path"]: entry for entry in source["source_files"]}
    check("exported-source-count", len(manifest) == len(committed) == 339
          and set(manifest) == set(committed), manifest_count=len(manifest), commit_count=len(committed))
    for name, entry in manifest.items():
        exported = exported_root / name
        actual = sha(exported) if exported.is_file() else None
        check("exported-source:" + name, actual == entry["sha256"] == digest(committed.get(name, b"")),
              actual_sha256=actual, matches_commit=FINAL_REVISION)

    frozen = {
        TASK / "01-intake.md": inputs["frozen_intake_sha256"],
        ROOT / "knowledge/candidates/requirements/REQ-active-session-renewal.md": inputs["requirement_v4_sha256"],
        APP / "tsconfig.tsbuildinfo": inputs["application"]["preexisting_cache_sha256"],
        STAGE / "user-request.txt": inputs["user_request_sha256"],
    }
    for path, expected in frozen.items():
        check("preserved:" + str(path.relative_to(ROOT)), sha(path) == expected,
              expected_sha256=expected, actual_sha256=sha(path))

    check("original-inventory", inventory["total_cases"] == len(inventory["cases"]) == 22
          and {case["id"] for case in inventory["cases"]} == EXPECTED_IDS)
    for name in ["source_manifest", "source_definitions"]:
        bound_file(inventory[name], STAGE, "historical:" + name)
    parity = load(STAGE / "setup/comparison-parity.json")["assertions_and_driver"]
    for name in ["prior_snapshot", "candidate_frozen_module", "candidate_driver_snapshot"]:
        bound_file(parity[name], STAGE / "setup", "assertion-and-driver:" + name)
    check("original-assertion-identity", parity["assertion_sha256"] == inventory["assertion_module_sha256"]
          and parity["test_revision"] == inventory["test_revision"])
    module_cache = {}
    unique_assertions = set()
    for case in inventory["cases"]:
        for kind in ["prior_run", "prior_result"]:
            prior = bound_file(case[kind], STAGE, f"historical:{case['id']}:{kind}")
            if prior:
                data = load(prior)
                key = "extensionSha256" if kind == "prior_run" else "testSourceSha256"
                check(f"historical:{case['id']}:{kind}:assertion-sha", data.get(key) == case["assertion_module_sha256"]
                      == inventory["assertion_module_sha256"])
                if kind == "prior_result":
                    check(f"historical:{case['id']}:case-identity", data.get("caseId") == case["case_id"])
        for assertion in [case["assertion_binding"], *case["helper_assertions"]]:
            relative = assertion["path"].removeprefix("repos/testing/ratan-test-engine/")
            identity = (assertion["source_revision"], relative)
            if identity not in module_cache:
                module_cache[identity] = git_bytes(TEST_REPO, *identity)
            raw = module_cache[identity]
            check(f"historical:{case['id']}:module", digest(raw) == case["assertion_module_sha256"])
            lines = raw.decode().splitlines()
            selected = "\n".join(lines[assertion["line"] - 1:assertion["end_line"]]).encode()
            unique_assertions.add((identity, assertion["line"], assertion["end_line"]))
            check(f"historical:{case['id']}:function:{assertion['function']}", digest(selected) == assertion["function_sha256"]
                  and all(assertion["line"] <= line <= assertion["end_line"] for line in assertion["assertion_lines"]))
        validate_candidate(case)

    definitions = load(STAGE / "original-definitions-integrity.json")
    check("original-definition-inventory", len(definitions["cases"]) == 22
          and {entry["id"] for entry in definitions["cases"]} == EXPECTED_IDS
          and definitions["baseline_workbench_revision"] == inputs["workbench_head"])
    old = git_bytes(ROOT, definitions["baseline_workbench_revision"], str(TASK.relative_to(ROOT) / "06-test-cases.md")).decode()
    current = (TASK / "06-test-cases.md").read_text()
    for entry in definitions["cases"]:
        before, now = case_definition(old, entry["id"]), case_definition(current, entry["id"])
        check("unchanged-definition:" + entry["id"], bool(before) and before == now
              and digest(before) == entry["before_sha256"] == entry["current_sha256"])

    eligibility = [case_eligibility(case) for case in inventory["cases"]]
    completed = [case["id"] for case in eligibility if case["eligible"]]
    pending = sorted(EXPECTED_IDS - set(completed))
    check("progress-completed-count", progress["completed_cases"] == len(completed)
          and {case["id"] for case in progress["completed_results"]} == set(completed))
    check("progress-inventory-hash", progress["inventory_sha256"] == initial_files["case-inventory.json"])
    check("progress-pending-cases", set(progress["pending_cases"]) == set(pending))
    if args.final:
        check("final-browser-completeness", len(completed) == 22 and not pending,
              completed_cases=len(completed), pending_cases=pending)

    documents = [TASK / "08-active-cutoff-fix-20261024.md", TASK / "06-test-cases.md", TASK / "10-change-review.md"]
    for document in [*documents, STAGE / "unit/report.md"]:
        markdown_checks(document)
    command = [str(ROOT / ".venv/bin/ai-sdlc"), "--workspace", str(ROOT), "lint", *map(str, documents)]
    lint = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lint_data = json.loads(lint.stdout)
    (STAGE / "implementation-artifact-lint.json").write_text(json.dumps({"command": command,
         "exit_code": lint.returncode, "result": lint_data, "stderr": lint.stderr}, indent=2) + "\n")
    check("selected-artifact-lint", lint.returncode == 0 and lint_data.get("valid") is True,
          warnings=sum(item.get("severity") == "warning" for item in lint_data.get("findings", [])),
          retained_result="implementation-artifact-lint.json")
    for name, initial in initial_files.items():
        check("read-only-snapshot:" + name, sha(STAGE / name) == initial,
              expected_sha256=initial, actual_sha256=sha(STAGE / name))

    failed = [item for item in CHECKS if not item["passed"]]
    status = "FAILED" if failed else "PASSED" if not pending else "PASSED_WITH_PENDING_BROWSER_CASES"
    report = {
        "id": "VALIDATION-active-cutoff-implementation-20261024",
        "recorded_at": datetime.now(timezone.utc).isoformat(), "mode": "FINAL" if args.final else "IMPLEMENTATION",
        "status": status, "candidate_revision": FINAL_REVISION,
        "implementation_integrity": "FAILED" if any(item["check"] != "final-browser-completeness" for item in failed) else "PASSED",
        "browser_comparison": "COMPLETE" if not pending else "PENDING",
        "completed_browser_cases": len(completed), "pending_browser_cases": pending,
        "retained_browser_results": sum(bool(case.get("candidate_result")) for case in inventory["cases"]),
        "candidate_case_eligibility": eligibility,
        "browser_outcomes": dict(Counter(case.get("candidate_business_outcome", "NOT_RUN") for case in inventory["cases"])),
        "source_files_checked": len(manifest), "unique_assertion_functions_checked": len(unique_assertions),
        "checked": len(CHECKS), "failed": len(failed), "failures": failed, "checks": CHECKS,
        "standard": "ASD-STE100", "automated_check": "FAILED" if failed else "PASSED",
        "asd_review": "PENDING", "reviewer": None, "reviewed_at": None,
        "limitations": [
            "Automated checks do not check the complete approved dictionary or grammar rules.",
            "Integrity checks preserve failing results. They do not establish passing business behavior or release approval.",
            "Final mode requires all 22 usable selected attempts. Execution errors and invalid comparisons remain pending despite retained JSON.",
            "Valid failed, diagnostic, and observation outcomes remain usable evidence. Earlier invalid attempts remain retained.",
            "Locked DOM/service attempts require reviewed setup validity, exact scope binding, and a nearby environment limit.",
            "Validity markers record source-backed review. This validator does not infer every setup condition from runner status.",
            "Source manifest declares the pre-commit base. Compared source bytes establish the final commit identity independently.",
            "Markdown checks cover local paths, heading anchors, and line bounds. They do not prove cited semantic meaning.",
            "No runtime tests, wheel builds, browser actions, inventories, progress, or active fixtures were changed.",
        ],
    }
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["status", "mode", "checked", "failed", "completed_browser_cases",
                                                 "pending_browser_cases", "source_files_checked"]}))
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
