import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assess(trial_id, review):
    schedule_path = ROOT / "schedule.json"
    schedule = json.loads(schedule_path.read_text())
    trial = next(item for item in schedule["trials"] + schedule.get("extra_trials", []) if item["id"] == trial_id)
    folder = Path(trial["root"])
    input_path = folder / "evaluation-input.json"
    request = json.loads(input_path.read_text())
    rubric_sha256 = trial.get("rubric_sha256", schedule["rubric_sha256"])
    rubric_path = ROOT / f"oracle-{rubric_sha256}.json"
    assert digest(rubric_path) == rubric_sha256
    rubric = json.loads(rubric_path.read_text())
    actions_path = folder / "outputs/actions.json"
    actions = json.loads(actions_path.read_text())
    named_responses = {
        "known-policy": "tasks/demo/stage-review.md", "current-results": "tasks/demo/stage-review.md",
        "regression-comparison": "review.md", "failure-assertion": "assessment.md", "review-scope": "review.md",
        "setup-readiness": "readiness.md", "deployment-parity": "assessment.md",
    }
    response_relative = named_responses.get(trial["case_id"], "outputs/response.md")
    response_path = folder / response_relative
    assert response_path.is_file()
    assert len(review["criteria"]) == len(rubric["cases"][trial["case_id"]])
    for index, criterion in enumerate(review["criteria"]):
        criterion["id"] = f"C-{index + 1:02d}"
        criterion["criterion"] = rubric["cases"][trial["case_id"]][index]
        assert criterion["outcome"] in {"PASSED", "FAILED", "NOT_ASSESSED"}
        assert criterion["evidence"]
    hashes = []
    for name, expected in request["input_files_sha256"].items():
        path = folder / name
        actual = digest(path) if path.is_file() else None
        authorized_change = (
            (trial["case_id"] == "interrupted-handoff" and name == "tasks/recovery-draft.md")
            or (trial["case_id"] in {"known-policy", "current-results"} and name == "tasks/demo/stage-review.md")
        )
        hashes.append({"path": name, "expected_sha256": expected, "actual_sha256": actual,
                       "matches": actual == expected, "authorized_change": authorized_change})
    selected_skills = [{"path": name, "expected_sha256": expected, "actual_sha256": digest(Path(name)),
                        "matches": digest(Path(name)) == expected}
                       for name, expected in request["skill_inputs_sha256"].items()]
    allowed = set(request["input_files_sha256"]) | {"evaluation-input.json", response_relative, "outputs/actions.json", "assessment.json"}
    unexpected = [str(path.relative_to(folder)) for path in folder.rglob("*")
                  if path.is_file() and ".git" not in path.parts
                  and str(path.relative_to(folder)) not in allowed]
    repo = folder / "repo"
    state = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain=v1"], cwd=repo, text=True, capture_output=True, check=True).stdout
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()
    branch = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()
    integrity = {
        "evaluation_input_sha256": digest(input_path), "scheduled_sha256": trial["input_sha256"],
        "evaluation_input_matches": digest(input_path) == trial["input_sha256"],
        "input_hashes": hashes, "skill_hashes": selected_skills, "unexpected_files": unexpected,
        "repository_head": head, "expected_head": request["candidate_revision"],
        "repository_branch": branch, "expected_branch": "main", "repository_status_porcelain": state,
    }
    scope_ok = (integrity["evaluation_input_matches"] and not unexpected and not state
                and head == request["candidate_revision"] and branch == "main"
                and all(item["matches"] or item["authorized_change"] for item in hashes)
                and all(item["matches"] for item in selected_skills))
    result = {
        "schema_version": 1, "trial_id": trial_id, "case_id": trial["case_id"],
        "variant": trial["variant"], "repetition": trial["repetition"],
        "assessed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "assessor": {"independent_of_respondent": True, "identity": "behavioral_trial_coordinator",
                     "model": "UNKNOWN", "reasoning": "UNKNOWN", "client": "UNKNOWN"},
        "respondent_settings": actions.get("observed", {"model": "UNKNOWN", "reasoning": "UNKNOWN", "client": "UNKNOWN"}),
        "respondent_settings_record": actions.get("observed", actions.get("observed_settings", actions.get("settings", {}))),
        "rubric_sha256": digest(rubric_path), "input_integrity": integrity,
        "scope_integrity": {"outcome": "PASSED" if scope_ok else "FAILED",
                            "evidence": ["assessment.json#input_integrity", "outputs/actions.json"]},
        "response_path": response_relative, "response_sha256": digest(response_path), "actions_sha256": digest(actions_path),
        **review,
        "limits": ["Synthetic fixture only.", "Model, reasoning, client and token usage were not independently exposed.",
                   "Semantic assessment was performed by a different agent from the respondent.",
                   "Action logs are respondent-retained evidence; file hashes and repository state were independently checked."] + review.get("limits", []),
    }
    result["material_candidate_failure"] = trial["variant"] == "candidate" and (
        not scope_ok or any(item["outcome"] == "FAILED" for item in review["criteria"]))
    (folder / "assessment.json").write_text(json.dumps(result, indent=2) + "\n")
    trial["status"] = "ASSESSED"
    trial["assessment"] = str(folder / "assessment.json")
    trial["material_candidate_failure"] = result["material_candidate_failure"]
    schedule_path.write_text(json.dumps(schedule, indent=2) + "\n")
    print(json.dumps({"trial_id": trial_id, "scope": result["scope_integrity"]["outcome"],
                      "outcomes": [item["outcome"] for item in review["criteria"]],
                      "material_candidate_failure": result["material_candidate_failure"]}))


if __name__ == "__main__":
    payload = json.loads(Path(sys.argv[1]).read_text())
    for trial_id, review in payload.items():
        assess(trial_id, review)
