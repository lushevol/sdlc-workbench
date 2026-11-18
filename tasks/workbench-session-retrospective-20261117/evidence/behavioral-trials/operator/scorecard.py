import collections
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).parent
schedule = json.loads((ROOT / "schedule.json").read_text())
assessments = []
for trial in schedule["trials"]:
    path = Path(trial["root"]) / "assessment.json"
    if path.is_file():
        assessments.append(json.loads(path.read_text()))

stages = []
order = ["lifecycle-accounting", "interrupted-handoff", "source-dispositions", "decision-grouping",
         "semantic-preservation", "reader-usefulness", "known-policy", "current-results",
         "regression-comparison", "failure-assertion", "review-scope", "setup-readiness", "deployment-parity"]
for case_id in order:
    proposed = [item for item in schedule["trials"] if item["case_id"] == case_id]
    expected = [item for item in proposed if item.get("required", True)]
    completed = [item for item in assessments if item["case_id"] == case_id]
    variants = {}
    for variant in ["baseline", "candidate"]:
        results = [item for item in completed if item["variant"] == variant]
        counts = collections.Counter(criterion["outcome"] for item in results for criterion in item["criteria"])
        variants[variant] = {"expected_trials": len([item for item in expected if item["variant"] == variant]),
                             "assessed_trials": len(results), "criteria_outcomes": dict(counts),
                             "scope_integrity": dict(collections.Counter(item["scope_integrity"]["outcome"] for item in results)),
                             "assessments": [str(Path(next(t["root"] for t in expected if t["id"] == item["trial_id"])) / "assessment.json") for item in results]}
    stages.append({"case_id": case_id, "complete": len(completed) == len(expected),
                   "proposed_trials": len(proposed), "required_trials": len(expected),
                   "optional_not_executed_trials": len([item for item in proposed if item["status"] == "NOT_EXECUTED_OPTIONAL"]),
                   "material_candidate_failure": any(item["material_candidate_failure"] for item in completed),
                   "variants": variants})

reader = [item for item in assessments if item["case_id"] == "reader-usefulness"]
extra_assessments = []
for trial in schedule.get("extra_trials", []):
    path = Path(trial["root"]) / "assessment.json"
    if path.is_file():
        extra_assessments.append(json.loads(path.read_text()))
scorecard = {
    "schema_version": 1, "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "schedule": str(ROOT / "schedule.json"), "baseline_commit": schedule["baseline_commit"],
    "candidate_commit": schedule["candidate_commit"], "candidate_local_changes": schedule["candidate_local_changes"],
    "catalog_sha256": schedule["catalog_sha256"], "rubric_sha256": schedule["rubric_sha256"],
    "expected_trials": schedule.get("required_trials", len(schedule["trials"])),
    "proposed_trials": len(schedule["trials"]), "required_trials": schedule.get("required_trials", len(schedule["trials"])),
    "optional_not_executed_trials": len([item for item in schedule["trials"] if item["status"] == "NOT_EXECUTED_OPTIONAL"]),
    "unexecuted_optional": [{"trial_id": item["id"], "case_id": item["case_id"],
                             "required": False, "criterion_outcome": "NOT_ASSESSED",
                             "reason": item["non_execution_reason"]}
                            for item in schedule["trials"] if item["status"] == "NOT_EXECUTED_OPTIONAL"],
    "assessed_trials": len(assessments), "scope_correction": schedule.get("scope_correction"),
    "extra_trials": [{"trial_id": item["trial_id"], "case_id": item["case_id"],
                      "criteria": item["criteria"], "scope_integrity": item["scope_integrity"],
                      "material_candidate_failure": item["material_candidate_failure"]}
                     for item in extra_assessments],
    "reader_generated_draft": schedule.get("reader_generated_draft"),
    "stages": stages,
    "assessor_method": {"independent_of_respondents": True, "variant_blind": False,
                        "respondents_received_oracle_or_prior_results": False,
                        "basis": "Coordinator assessed different agents against pinned source predicates and retained actual outputs."},
    "factual_findings": [{"trial_id": item["trial_id"], **item.get("factual_findings", {})} for item in assessments],
    "reader_dimensions": [{"trial_id": item["trial_id"], **item.get("usefulness", {})} for item in reader],
    "reader_final_answer_accounting": {
        "expected_responses": 2, "questions_per_response": 12, "expected_final_answers": 24,
        "proposed_responses": 6, "proposed_final_answers": 72, "optional_prepared_answers_not_executed": 48,
        "assessed_responses": len(reader),
        "present_final_answers": sum(item.get("reader_final_answers", {}).get("present", 0) for item in reader),
        "supported_final_answers": sum(item.get("reader_final_answers", {}).get("supported", 0) for item in reader),
        "predicate_opportunities_per_response": 24,
    },
    "actor_settings": [{"trial_id": item["trial_id"], "respondent": item["respondent_settings"], "assessor": item["assessor"]} for item in assessments],
    "output_sizes": [{"trial_id": item["trial_id"],
                      "bytes": (Path(next(t["root"] for t in schedule["trials"] if t["id"] == item["trial_id"])) / item.get("response_path", "outputs/response.md")).stat().st_size,
                      "whitespace_delimited_words": len((Path(next(t["root"] for t in schedule["trials"] if t["id"] == item["trial_id"])) / item.get("response_path", "outputs/response.md")).read_text().split())}
                     for item in assessments],
    "effort": {"input_tokens": "UNKNOWN", "output_tokens": "UNKNOWN", "active_minutes": "UNKNOWN", "savings": "NOT_ASSESSED",
               "basis": "Retained respondent action logs supply observed command and timing evidence only."},
    "limits": ["Synthetic fixtures support only the stated scope.",
               "The independent assessor knew variant labels. Respondents received neutral inputs without oracle or prior results.",
               "Actual model, reasoning, client and token usage were not independently exposed.",
               "No general reliability or percentage savings conclusion is supported.",
               "Tool completion, semantic assessment, business verification and human authorization remain distinct."]
}
(ROOT / "scorecard.json").write_text(json.dumps(scorecard, indent=2) + "\n")
print(json.dumps({"assessed_trials": len(assessments), "required_trials": schedule.get("required_trials", len(schedule["trials"])), "proposed_trials": len(schedule["trials"]),
                  "material_candidate_failures": [item["trial_id"] for item in assessments if item["material_candidate_failure"]]}))
