"""Refresh inspected semantic mappings against final source and actual unit checkpoints."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

OUTPUT = Path(__file__).resolve().parent
WORKSPACE = OUTPUT.parents[4]
TASK = WORKSPACE / "tasks/portal-background-session-20261019"
APP = WORKSPACE / "repos/ui/mfe-base"
HEAD = "1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303"
OLD = TASK / "evidence/delivery-confidence-20261026/unit/traceability.json"
PREVIOUS = json.loads(OLD.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
relative = lambda path: str(path.relative_to(WORKSPACE))
results = []
RUN = OUTPUT / "test-only-final-2" if "--final-2" in sys.argv else (OUTPUT / "test-only-final" if "--final" in sys.argv else OUTPUT)
for case_path in sorted((RUN / "cases").glob("*.json")):
    result = json.loads(case_path.read_text())
    result["immediate_checkpoint"] = relative(case_path)
    results.append(result)

def executions(case_id):
    return [{"full_name": result["fullName"], "status": result["status"], "immediate_checkpoint": result["immediate_checkpoint"], "source_binding": relative(RUN / "source-binding.json")} for result in results if f"[{case_id}]" in result["fullName"]]

criteria = copy.deepcopy(PREVIOUS["criteria"])
for criterion in criteria:
    for case in criterion["cases"]:
        case["historical_candidate_results"] = case.pop("candidate_results", [])
        case["final_unit_executions"] = executions(case["id"])
        executable = case.get("executable")
        if executable:
            source = WORKSPACE / executable["path"]
            executable["historical_sha256"] = executable.get("sha256")
            executable["sha256"] = sha(source)
            executable["revision"] = HEAD
            executable["historical_assertion_bytes_unchanged"] = executable["sha256"] == executable["historical_sha256"]
            # Existing line locators are retained only when the literal assertion still matches.
            lines = source.read_text().splitlines()
            for site in executable.get("assertion_sites", []):
                if isinstance(site, dict):
                    site["final_line_matches"] = lines[site["line"] - 1].strip() == site["text"].strip()

new_cases = {}
for number in range(21, 25):
    case_id = f"DEL-{number}"
    source = APP / "src/hooks/service/cancellationPreservation.test.ts"
    lines = source.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if f'"[{case_id}]' in line)
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"  it\(", lines[i])), len(lines) - 1)
    new_cases[case_id] = {
        "id": case_id, "canonical_definition": relative(TASK / "06-test-cases.md") + "#" + case_id.lower(),
        "executable": {"path": relative(source), "revision": HEAD, "sha256": sha(source), "block_start": start + 1, "block_end": end,
                       "assertion_sites": [{"line": i + 1, "text": line.strip()} for i, line in enumerate(lines[start:end], start) if "expect(" in line],
                       "assertion_chain": "Actual shared Axios client -> actual synchronous request interceptor -> controlled transport -> actual response/error interceptor -> actual reducers -> loading, identity and returned-data assertions."},
        "final_unit_executions": executions(case_id),
    }
for criterion in criteria:
    additions = {"DC-AC-10": ["DEL-21", "DEL-23", "DEL-24"], "DC-AC-15": ["DEL-22"]}.get(criterion["id"], [])
    criterion["cases"].extend(new_cases[case_id] for case_id in additions)

if RUN != OUTPUT:
    for number in range(1, 11):
        case_id = f"FOUR-COV-{number:02}"
        source = APP / ("src/components/Timeout/common/coverageBoundaries.test.tsx" if number <= 6 or number == 10 else "src/pages/Home/common/sessionRefresh.test.tsx")
        lines = source.read_text().splitlines()
        start = next(i for i, line in enumerate(lines) if case_id in line)
        end = next((i for i in range(start + 1, len(lines)) if re.match(r"  it(?:\(|\.each)", lines[i])), len(lines) - 1)
        new_cases[case_id] = {"id": case_id, "canonical_definition": relative(TASK / "06-test-cases.md") + "#" + case_id.lower(),
            "executable": {"path": relative(source), "runtime_revision": HEAD, "test_revision": "worktree test-only overlay; exact bytes bound", "sha256": sha(source), "block_start": start + 1, "block_end": end,
                "assertion_sites": [{"line": i + 1, "text": line.strip()} for i, line in enumerate(lines[start:end], start) if "expect(" in line],
                "assertion_chain": "Actual controller/hook with controlled service/context/analytics collaborators; actual parser, epoch and timers. Direct state/callback/call-count assertions. No transport or browser claim."},
            "final_unit_executions": executions(case_id)}
    for criterion in criteria:
        additions = {"DC-AC-06": ["FOUR-COV-01", "FOUR-COV-02", "FOUR-COV-03", "FOUR-COV-04", "FOUR-COV-10"], "DC-AC-03": ["FOUR-COV-05", "FOUR-COV-06"], "DC-AC-08": ["FOUR-COV-07", "FOUR-COV-08"], "DC-AC-16": ["FOUR-COV-09"]}.get(criterion["id"], [])
        criterion["cases"].extend(new_cases[case_id] for case_id in additions)

units = [
    ("DC-CH-01", "src/components/Timeout/common/useController.ts", ["DC-AC-03", "DC-AC-04", "DC-AC-05", "DC-AC-06"], ["DEL-04", "DEL-05", "DEL-06", "DEL-07", "DEL-08"], "Actual Home renders actual Timeout; actual relogin interceptors and reducers run. Assertions check pending UI, success closure, retry, deadline and logout."),
    ("DC-CH-02", "src/components/Timeout/index.tsx", ["DC-AC-03", "DC-AC-04", "DC-AC-05"], ["DEL-04", "DEL-05", "DEL-06", "DEL-07"], "Actual rendered Extend/Logout controls invoke actual Timeout controller. DOM disabled/visible assertions and service counts establish those selected UI predicates."),
    ("DC-CH-03", "src/hooks/reducer/root0.reducers.ts", ["DC-AC-01", "DC-AC-08"], ["OWN-06", "DEL-10"], "Actual SET_TOKEN reducer runs after access rotation. Assertions check retained refresh, updated access and accepted same-session response."),
    ("DC-CH-04", "src/hooks/service/config.ts", ["DC-AC-01", "DC-AC-07", "DC-AC-10"], ["OWN-04", "DEL-01", "DEL-09", "DEL-14", "DEL-19"], "Actual exported Axios client executes its registered synchronous interceptors. Immediate empty-refresh assertions check ownership timing; deferred adapter assertions check current request loading."),
    ("DC-CH-05", "src/hooks/service/index.ts", ["DC-AC-03", "DC-AC-04", "DC-AC-05", "DC-AC-16"], ["PEND-01", "DEL-06", "DEL-07", "DEL-20"], "Actual acquisition/relogin helpers call actual shared client with controlled transport. Assertions check pending promise settlement, credentials, recovery and prompt closure."),
    ("DC-CH-06", "src/hooks/service/util/error.response.handler.ts", ["DC-AC-02", "DC-AC-06", "DC-AC-07", "DC-AC-10", "DC-AC-15"], ["DEL-03", "DEL-05", "DEL-11", "DEL-13", "DEL-14", "DEL-22", "DEL-23"], "Controlled adapter rejects through actual Axios error interceptor. Actual reducer/store assertions check preserved current identity, messages, loading and invalidation."),
    ("DC-CH-07", "src/hooks/service/util/succes.response.handler.ts", ["DC-AC-01", "DC-AC-02", "DC-AC-03", "DC-AC-06", "DC-AC-07", "DC-AC-10"], ["OWN-04", "DEL-02", "DEL-04", "DEL-09", "DEL-10", "DEL-21", "DEL-22", "DEL-24"], "Actual Axios success interceptor parses controlled responses and updates actual reducers. Assertions check stale rejection, access, refresh, returned payload, loading and parser-failure cleanup."),
    ("DC-CH-08", "src/hooks/service/util/success.request.handler.ts", ["DC-AC-01", "DC-AC-02", "DC-AC-07", "DC-AC-10"], ["OWN-04", "OWN-05", "DEL-01", "DEL-09", "DEL-21"], "Actual synchronous request interceptor runs before service call returns. Assertions check immediately cleared old refresh, protected request headers and silent-request loading isolation."),
    ("DC-CH-09", "src/pages/Home/common/useController.ts", ["DC-AC-04", "DC-AC-11", "DC-AC-12", "DC-AC-13", "DC-AC-14", "DC-AC-16"], ["DEL-15", "DEL-16", "DEL-17", "DEL-18", "DEL-20"], "Actual Home hook/effects/handlers run. Real store and localStorage assertions check selected workspace and persistence. DEL-20 runs actual service and reducers around the delayed timer."),
    ("DC-CH-10", "src/utils/common.ts", ["DC-AC-06"], ["OWN-01", "OWN-02", "OWN-03", "DEL-12"], "Actual authentication cleanup increments epoch and clears store/persistence. Late controlled responses exercise actual stale guards; assertions check current credentials and rejected old data."),
    ("DC-CH-11", "src/utils/sessionEpoch.ts", ["DC-AC-01", "DC-AC-02", "DC-AC-06", "DC-AC-08", "DC-AC-15"], ["OWN-06", "OWN-07", "DEL-02", "DEL-03", "DEL-10", "DEL-22"], "Actual epoch operations feed request/response guards. Same-session rotation and cross-session response/cancellation assertions distinguish access changes from session replacement."),
    ("DC-CH-12", "src/hooks/service/util/requestLoading.ts", ["DC-AC-10", "DC-AC-15"], ["DEL-14", "DEL-19", "DEL-21", "DEL-22", "DEL-23", "DEL-24"], "Actual shared client executes actual loading registry and reducers. Assertions check final cleanup, overlapping work, silent work, epoch replacement and configless/parser failures."),
]
if RUN != OUTPUT:
    for identifier, _name, _criteria, case_ids, _chain in units:
        if identifier == "DC-CH-01": case_ids.extend([*(f"FOUR-COV-{number:02}" for number in range(1, 7)), "FOUR-COV-10"])
        if identifier == "DC-CH-09": case_ids.extend(f"FOUR-COV-{number:02}" for number in range(7, 10))
change_rows = [{"id": identifier, "path": name, "candidate_revision": HEAD, "sha256": sha(APP / name), "criteria": criterion_ids,
                "direct_cases": [{"id": case_id, "definition": relative(TASK / "06-test-cases.md") + "#" + case_id.lower(), "executions": executions(case_id)} for case_id in case_ids],
                "inspected_assertion_chain": chain, "grade": "CONFIRMED_WITHIN_STATED_ASSERTIONS", "complete_behavior_equivalence": "NOT_ESTABLISHED"}
               for identifier, name, criterion_ids, case_ids, chain in units]
ac_to_code = [{"criterion": criterion["id"], "definition": criterion["definition"], "changed_units": [row["id"] for row in change_rows if criterion["id"] in row["criteria"]],
               "status": "MAPPED_SELECTED_BEHAVIOR; BUSINESS_REVIEW_PENDING"} for criterion in criteria]
result = {
    "candidate_commit": HEAD, "base_commit": PREVIOUS["main_revision"], "predecessor_mapping": relative(OLD), "predecessor_sha256": sha(OLD),
    "ac_to_test": criteria, "ac_to_changed_code": ac_to_code, "changed_code_to_test": change_rows,
    "denominators": {"additional_criteria": len(criteria), "changed_runtime_paths": len(change_rows)},
    "generator_sha256": sha(Path(__file__)),
    "backlog_authority": relative(TASK / "evidence/user-input-20261027-backlog-scope.txt"),
    "limits": ["The original seven ACs need fresh E2E reconciliation from the browser owner.", "DC-AC-14 requires browser sharing assertions; unit execution cannot supply that result.", "Semantic links reflect inspected fixture/assertion chains, not line counters.", "Complete intended behavior remains separate from these explicit selected behavior mappings.", "Business review and publication remain pending."],
}
(OUTPUT / ("final-2-traceability-with-boundaries.json" if "--final-2" in sys.argv else ("final-traceability-with-boundaries.json" if RUN != OUTPUT else "final-traceability.json"))).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"criteria": len(criteria), "changed_runtime_units": len(change_rows), "criterion_case_rows": sum(len(row["cases"]) for row in criteria), "new_cases": list(new_cases)}, indent=2))
