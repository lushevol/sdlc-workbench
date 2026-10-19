# Defect report

## Purpose

Capture an issue immediately and develop its evidence, impact, ownership, and investigation plan.

## AI instructions

1. Create `tasks/<task-id>/` before discovery. Copy this Template block into its `intake.md`.
2. Record expected behavior, its authority, reported observations, reproduction conditions, impact, and available evidence.
3. Record exact inspected revisions. Mark missing deployed revisions and policy sources explicitly.
4. Ask focused questions in small rounds. Record answers and their sources. Do not re-ask answered details without conflict.
5. Keep reported symptoms, demonstrated local failures, hypothetical reproductions, and suspected causes separate.
6. Assess readiness for the named next phase. Keep implementation approval and business review separate.
7. Use `READY` only when no unresolved material uncertainty can change that phase's scope, behavior, or decision.
8. A proposed expectation can support scoped investigation. It does not establish approved policy.
9. Permit safe, authorized evidence collection while unknowns remain. Unknown PROD revisions do not block local investigation.
10. A confirmed defect requires measurable Gherkin regression criteria and assertions for the corrected behavior.
11. Assign severity from supported impact evidence and applicable classification rules.

Before asking policy questions, search existing knowledge, linked requirements, previous answers, and cited source bytes.
Record applicable criterion IDs, revisions or hashes, conflicts, and search limits in the intake.
Pending publication review does not make documented user intent unavailable.

Record known facts and prior answers before asking questions.
Inspect registered code, test assertions, and investigation results. Repositories can use optional `repos/` clones or configured locations.
Read reports as secondary evidence alongside their cited sources.
Drill material ambiguities with small question rounds and evidence checks. Keep investigation within intake until the gate passes.
Retain new evidence under the task's `evidence/` directory. Index sources, hashes, exact revisions, claims, and limits.
Reference existing raw snapshots and audit events at their original paths. Never move or rewrite them.
`READY_WITH_LIMITS` permits evidence collection only. `NEEDS_CLARIFICATION` blocks downstream work.

Follow the [task contract](../../../tasks/README.md) for storage and readiness.
Use the [intake procedure](../../../.agents/skills/analyze-requirement/SKILL.md) for question rounds and readiness decisions.
Complete relevant reproduction fields only. Explain irrelevant fields and keep unavailable values null or `unknown`.
Retain each answer's source and status. Keep unresolved questions and hypotheses visible until evidence resolves them.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "defect-report"
id: "{{stable_artifact_id}}"
version: 1
status: draft
owner: unknown
source_refs: []
related_ids: []
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# {{defect_title}}

## Classification and scope

- Defect ID: {{defect_id}}
- Confirmation: {{hypothetical_or_suspected_or_confirmed_with_evidence}}
- Requirement / criterion: {{requirement_id_and_criterion_id}}
- Affected users: {{affected_population_or_unknown}}
- Severity: {{classification_and_evidence_or_unassessed}}
- Priority: {{priority_and_decision_source_or_unassessed}}

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| {{next_phase}} | {{READY_or_READY_WITH_LIMITS_or_NEEDS_CLARIFICATION}} | {{material_uncertainty_and_phase_rationale}} | {{blocked_actions_or_none_with_basis}} | unknown; {{next_action}} |

- Expected behavior: {{source_supported_or_explicitly_proposed_expectation}}
- Expected behavior authority: {{policy_source_or_owner_question}}
- Approval to implement: {{actual_authorization_source_and_scope_or_not_established}}
- Evidence index: {{task_evidence_index_path}}
- Business review: pending. Intake readiness does not grant approval.

### Existing knowledge review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and retrieval limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| {{index_requirement_prior_answer_and_source_bytes}} | {{exact_revision_or_available_hash}} | {{documented_rule_and_criterion_ids_or_no_match}} | {{documented_intent_approval_state_and_bounded_search_limits}} | {{unresolved_question_or_none}} |

## Reproduction conditions

```yaml
repository_id: "{{repository_id}}"
repository_revision: null
test_revision: null
environment_identity: null
reproduction_status: NOT_RUN
execution_id: null
actual_results: null
retained_execution_refs: []
reported_environment:
  deployment: null
  deployed_revisions: null
  browser_version: null
  operating_system: null
timing_and_actions:
  timezone: null
  login_at: null
  last_action_at: null
  hidden_at: null
  returned_at: null
  elapsed_time: null
  action_sequence: []
browser_lifecycle:
  tab_visibility: null
  browser_sleep_or_discard: null
  device_sleep_or_lock: null
  effective_settings_and_extensions: null
session_and_connectivity:
  expected_session_policy_ref: null
  observed_token_lifetimes: null
  network_or_vpn_changes: null
  sso_state: null
reproduction_controls:
  foreground_control: null
  mocks_and_instrumentation: null
  untested_differences: []
```

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| {{step_number}} | {{condition_or_action}} | {{source_supported_result}} | null |

## Hypothesis and impact

- Hypothetical mismatch: {{hypothetical_result_or_not_applicable}}
- Observed impact: {{retained_evidence_or_none}}
- Suspected cause: {{hypothesis_and_basis_or_unknown}}
- Evidence limits: {{unobserved_conditions_or_missing_evidence}}

| Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence or missing check | Status | Owner and next action |
| --- | --- | --- | --- | --- | --- |
| {{hypothesis_id}} | {{candidate_explanation}} | {{source_or_none}} | {{source_or_unknown}} | {{open_or_supported_in_named_scope_or_rejected}} | unknown; {{next_action}} |

## Resolution and regression

- Proposed investigation: {{next_evidence_to_collect}}
- Evidence plan: {{scope_inputs_exact_revisions_method_observations_controls_retention_and_limits}}
- Fix scope: {{inspected_affected_interfaces_or_unknown}}
- Regression test: {{test_id_and_required_assertion_or_pending}}
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

Regression criteria remain proposed until the responsible owner confirms expected policy.
Replace numeric limits only from evidence or an explicitly proposed test condition.

```gherkin
Feature: {{source_supported_or_proposed_corrected_behavior}}

  Scenario: {{condition_action_and_result}}
    Given {{environment_initial_state_and_policy_condition}}
    When {{action_or_lifecycle_event}}
    Then {{observable_result_with_measure_and_limit}}
```

## Facts, inferences, and unresolved questions

- Facts: {{source_supported_facts}}
- Inferences: {{inferences_and_basis_or_none}}
- Unresolved questions: {{questions_and_resolution_owner}}

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| {{round_and_question_id}} | {{material_question_or_known_detail}} | {{answer_or_unknown}} | {{message_or_source_locator_or_none}} | {{answered_or_pending_or_conflicting}} | unknown | {{consequence_and_next_action}} |

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| {{evidence_or_explicit_gap}} | {{consequence}} | unknown | {{specific_next_action}} |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_evidence_limits}} |
````

## Illustrative sample

This sample describes proposed invoice portal work.
It records no actual approval or execution.

````markdown
---
artifact_kind: "defect-report"
id: "SAMPLE-DEFECT-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-002, SAMPLE-AC-002, SAMPLE-TEST-002]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Hypothetical invoice content after denied access

## Classification and scope

- Defect ID: SAMPLE-DEFECT-001.
- Confirmation: Hypothetical reproduction. No defect is confirmed.
- Requirement / criterion: SAMPLE-REQ-002 / SAMPLE-AC-002.
- Affected users: unknown. No actual users or system observations exist.
- Severity: unassessed. No observed impact or severity policy exists.
- Priority: unassessed. No prioritization decision exists.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Implementation planning | NEEDS_CLARIFICATION | The proposed expectation is illustrative. Actual policy, implementation, environment, and impact remain unknown. | Downstream SDLC work | unknown; identify actual policy and current behavior |

- Expected behavior: Return zero invoices and the message "Access denied" for the denied request.
- Expected behavior authority: SAMPLE-AC-002 is illustrative. No approved business policy exists.
- Approval to implement: not established. The sample authorizes no business runtime change.
- Evidence index: not applicable. This fictional example creates no actual task or evidence.
- Business review: pending. Intake readiness does not grant approval.

## Reproduction conditions

```yaml
repository_id: SAMPLE-REPO-001
repository_revision: null
test_revision: null
environment_identity: null
reproduction_status: NOT_RUN
execution_id: null
actual_results: null
retained_execution_refs: []
```

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| 1 | Authenticate customer B with no permission for INV-001 | Fixture matches the denied access condition | null |
| 2 | Customer B requests INV-001 | Response contains zero invoices and message "Access denied" | null |

## Hypothesis and impact

- Hypothetical mismatch: A denied response could contain invoice content. This possibility has not been observed.
- Observed impact: None. No retained execution evidence exists.
- Suspected cause: unknown. No implementation revision has been inspected.
- Evidence limits: This example supplies a reproduction design without an actual result.

## Resolution and regression

- Proposed investigation: Execute SAMPLE-TEST-002 after inspecting exact implementation and assertion revisions.
- Evidence plan: Identify the target revision and fixture. Retain the denied response and an authorized-access control response.
- Fix scope: unknown. No confirmed defect or inspected implementation exists.
- Regression test: SAMPLE-TEST-002 should assert zero invoices and the denial message if the defect is confirmed.
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

The following regression criteria describe the proposed sample rule. They record no actual execution.

```gherkin
Feature: Enforce the proposed invoice access rule

  Scenario: Customer requests an invoice without permission
    Given customer B has no permission for invoice INV-001
    When customer B requests invoice INV-001
    Then the response contains exactly 0 invoices
    And the response message is "Access denied"
```

## Facts, inferences, and unresolved questions

- Facts: SAMPLE-AC-002 expects zero invoices and the message "Access denied".
- Inferences: Returned invoice content would contradict the proposed criterion.
- Unresolved questions: Actual behavior, impact, cause, and the responsible owner are unknown.

### Answer and question log

| ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-Q-001 | What is the proposed denied-access response? | Zero invoices and "Access denied" | sample-context.md, SAMPLE-AC-002 | answered | unknown | Prepare assertions against the proposed rule |
| SAMPLE-Q-002 | Which implementation and environment can execute the test? | unknown | No source supplied | pending | unknown | Execution remains blocked; identify the target |

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | The hypothetical mismatch cannot establish a confirmed defect | unknown | Inspect the assertions and retain a reproduction result |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Intake and new evidence remain under the same task. Existing source and audit paths remain unchanged.
- The report distinguishes hypothetical, suspected, and confirmed behavior.
- Known facts and answered details appear before new questions.
- Each answer identifies its source. Pending questions have owners and next actions.
- Expected behavior cites its authority or identifies a proposed expectation and owner question.
- Readiness names the next phase and explains why no unresolved material uncertainty can change its decision.
- Limited readiness permits evidence collection only. Material gaps block downstream SDLC work.
- Readiness remains separate from implementation approval and business review.
- Applicable browser, timing, policy, network, SSO, and reproduction-control fields state evidence or explicit unknowns.
- Observed results cite retained evidence at an exact revision.
- Cause, severity, and impact claims state their evidence limits.
- Regression criteria use measurable Gherkin and state pending policy decisions.
- A confirmed defect has a regression plan. Closure requires retest evidence and an actual closure decision.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
