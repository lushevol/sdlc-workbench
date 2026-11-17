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
    expected = [item for item in schedule["trials"] if item["case_id"] == case_id]
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
                   "material_candidate_failure": any(item["material_candidate_failure"] for item in completed),
                   "variants": variants})

reader = [item for item in assessments if item["case_id"] == "reader-usefulness"]
scorecard = {
    "schema_version": 1, "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "schedule": str(ROOT / "schedule.json"), "baseline_commit": schedule["baseline_commit"],
    "candidate_commit": schedule["candidate_commit"], "candidate_local_changes": schedule["candidate_local_changes"],
    "catalog_sha256": schedule["catalog_sha256"], "rubric_sha256": schedule["rubric_sha256"],
    "expected_trials": len(schedule["trials"]), "assessed_trials": len(assessments),
    "stages": stages,
    "factual_findings": [{"trial_id": item["trial_id"], **item.get("factual_findings", {})} for item in assessments],
    "reader_dimensions": [{"trial_id": item["trial_id"], **item.get("usefulness", {})} for item in reader],
    "reader_final_answer_accounting": {
        "expected_responses": 6, "questions_per_response": 12, "expected_final_answers": 72,
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
               "Actual model, reasoning, client and token usage were not independently exposed.",
               "No general reliability or percentage savings conclusion is supported.",
               "Tool completion, semantic assessment, business verification and human authorization remain distinct."]
}
(ROOT / "scorecard.json").write_text(json.dumps(scorecard, indent=2) + "\n")
print(json.dumps({"assessed_trials": len(assessments), "expected_trials": len(schedule["trials"]),
                  "material_candidate_failures": [item["trial_id"] for item in assessments if item["material_candidate_failure"]]}))
