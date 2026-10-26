# Change request

## Purpose

Describe a proposed or implemented baseline change and its affected engineering artifacts.
Keep the requested decision separate from actual authorization and implementation.

## AI instructions

1. Obtain the current baseline, proposed difference, rationale, requester evidence, and affected artifact IDs.
2. Inspect referenced revisions before claiming impact on code or interfaces.
3. Show before and after behavior without rewriting canonical rules silently.
4. Identify requirement, test, data, release, and operational effects.
5. Keep estimates and impact inferences explicit until evidence confirms them.
6. Do not invent requester identity, approval, effort, deadlines, implementation, or execution results.
7. Preserve an existing frozen intake. Record unavailable earlier requirements or baseline evidence explicitly.
   Use the [entry routes](../../../../tasks/README.md#lifecycle-entry-routes) when supplied implementation precedes requirements or bounded exploration applies.
8. Use [the post-change procedure](../../../../.agents/skills/impact-analysis/references/post-change-review.md) for impact, review, and browser verification.
9. Keep user impact, system impact, and named stage readiness separate. Do not infer release approval from readiness.

## Template

````markdown
---
artifact_kind: "change-request"
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

# {{change_request_title}}

## Request and source facts

- Requester: {{requester_or_unknown}}
- Current baseline: {{artifact_ids_versions_and_locators}}
- Request source: {{source_id_and_locator}}
- Supported rationale: {{rationale}}
- Evidence limit: {{limit}}
- Entry route and basis: {{requirements_first_implementation_supplied_or_bounded_exploration_with_reason}}.
- Actual chronology: {{registration_date_implementation_dates_and_evidence_or_unknown}}.

## Stage boundary and readiness

Record readiness for the named decision, including bounded exploration before full product criteria exist.
Record unavailable baseline evidence as `unknown`, with its decision consequence.
Use `not applicable` only when baseline fields do not apply. Do not invent earlier intake or approval.

- Stage: {{named_stage_or_not_applicable_reason}}
- Frozen intake: {{path_exact_git_revision_and_sha256_or_not_applicable_reason}}
- Compared implementation: {{repository_ids_full_base_and_head_commits_and_local_diff_hashes}}
- Readiness: {{READY_READY_WITH_LIMITS_or_NEEDS_CLARIFICATION_for_named_stage}}
- Assessor and time: {{actual_assessor_and_timestamp}}
- Rationale and evidence: {{scope_specific_rationale_and_evidence_refs}}
- Blocked actions: {{actions_and_resolution_evidence_needed_or_none}}
- Resolution owner and next action: {{owner_or_unknown_and_specific_next_action}}
- Intake integrity result: {{before_and_after_hash_check_or_NOT_RUN}}

## Proposed change

State whether each difference is proposed or implemented. Support implemented differences with exact source locators.

| Aspect | Current baseline | Proposed replacement or addition | Basis |
| --- | --- | --- | --- |
| {{aspect}} | {{current_behavior_or_unknown}} | {{proposed_behavior}} | {{source_or_explicit_proposal}} |

## Scope and affected artifacts

| Artifact ID | Exact version or revision | Proposed effect | Evidence | Risk and basis | Owner |
| --- | --- | --- | --- | --- | --- |
| {{artifact_id}} | {{version_or_null}} | {{effect}} | {{evidence_or_missing_input}} | {{qualitative_risk_and_basis}} | {{owner_or_unknown}} |

## User impact

| Actor and journey | Trigger | Before and after behavior | Benefit or adverse consequence | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| {{actor_and_journey}} | {{condition_or_action}} | {{observable_before_and_after}} | {{user_effect}} | {{source_refs_and_inference_limits}} | unknown | {{validation_or_decision}} |

## System impact

| Changed path | Affected caller or consumer | Interface or state effect | Failure or concurrency risk | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| {{commit_path_symbol}} | {{inspected_caller_importer_or_dependency}} | {{contract_data_timing_or_resource_effect}} | {{qualitative_risk_and_basis}} | {{source_refs_and_uninspected_boundaries}} | unknown | {{required_check_or_decision}} |

## Options and consequences

| Option | Expected consequence | Evidence or inference | Required decision |
| --- | --- | --- | --- |
| {{option}} | {{consequence}} | {{basis_and_limit}} | {{decision}} |

## Proposed acceptance and validation

| Changed requirement or criterion ID | Canonical change location | Required validation | Current result | Evidence reference |
| --- | --- | --- | --- | --- |
| {{requirement_or_criterion_id}} | {{locator}} | {{validation_method}} | {{NOT_RUN_or_evidenced_result}} | {{reference_or_null}} |

## Implementation and release proposal

- Proposed implementation scope: {{scope_or_unknown}}
- Proposed release: {{release_id_or_unknown}}
- Estimate and basis: {{estimate_or_unknown}}
- Reversal approach: {{approach_or_unknown}}

### Bounded exploration

Complete these fields when the named stage is exploration. Otherwise record `not applicable` and its reason.

- Goal and measurable outcomes: {{experiment_question_observable_success_conditions_and_evidence_needed}}.
- Boundaries and permitted edits: {{affected_paths_interfaces_allowed_actions_and_constraints}}.
- Owner and authorization: {{accountable_owner_or_unknown_and_existing_authorization_source_and_scope}}.
- Stop condition and artifact disposition: {{stopping_condition_and_preserve_revise_or_discard_decision_with_owner}}.

`READY` covers only the named exploration. Product acceptance requires reconciled intent and matching verification evidence.
`READY_WITH_LIMITS` permits intake evidence collection only.

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unknowns and blockers

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Stage evidence and completion

| Stage | Required evidence | Record or execution locator | Current result | Remaining blocker and next action |
| --- | --- | --- | --- | --- |
| Impact analysis | User and system effects at exact revisions | {{record_locator}} | {{NOT_RUN_or_evidenced_result}} | {{gap_owner_and_next_action_or_none}} |
| Code review | Findings and suggestions for the selected diff | {{review_locator}} | {{NOT_RUN_or_evidenced_result}} | {{gap_owner_and_next_action_or_none}} |
| E2E expansion | Original and new case inventory with assertions | {{plan_and_test_code_locators}} | {{NOT_RUN_or_evidenced_result}} | {{gap_owner_and_next_action_or_none}} |
| Browser execution | Every inventoried case, result, and evidence | {{run_report_locator}} | {{NOT_RUN_or_evidenced_result}} | {{gap_owner_and_next_action_or_none}} |

## Requested decision and actual disposition

- Requested decision: {{decision_request}}
- Authorized decision owner: {{owner_with_authority_evidence_or_unknown}}
- Actual decision: {{pending_or_evidenced_decision}}
- Actual decision reference: {{reference_or_null}}
- Implementation status and source: {{proposed_or_evidenced_status_and_exact_revision_or_local_hash}}.
- Intent review: {{sourced_proposed_conflicting_or_reviewed_intent_and_authority}}.
- Execution outcome: {{NOT_RUN_or_retained_result_with_source_bindings_and_limits}}.
- Business acceptance: {{pending_or_actual_evidenced_decision_with_owner_and_scope}}.

Requirements inferred from implementation or tests remain proposed until intent evidence and required review support them.
Matching code and tests cannot supply business approval.
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "change-request"
id: "SAMPLE-CHANGE-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-NFR-001, SAMPLE-NFR-AC-001, SAMPLE-REL-001]
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

# Add a measurable invoice response target

## Request and source facts

- Requester: unknown; no real request was submitted.
- Current baseline: No actual approved baseline exists; sample-v1 supplies illustrative proposed requirements.
- Request source: SAMPLE-SRC-001; Proposed behavior.
- Supported rationale: Authorized invoice viewing needs explicit performance conditions for reproducible assessment.
- Evidence limit: This is a hypothetical authoring example, with no observed performance defect.

## Proposed change

| Aspect | Current baseline | Proposed replacement or addition | Basis |
| --- | --- | --- | --- |
| Authorized response target | Actual baseline unknown; no production objective exists. | Introduce SAMPLE-NFR-001 using its complete measurement contract. | Illustrative proposed target in sample-v1 |
| Acceptance criteria | Actual baseline unknown. | Add SAMPLE-NFR-AC-001 through the canonical nonfunctional requirement. | Proposed measurable criterion |

## Scope and affected artifacts

| Artifact ID | Exact version or revision | Proposed effect | Evidence | Risk and basis | Owner |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-NFR-001 | sample-v1; illustrative only | Add the response target and measurement conditions. | SAMPLE-SRC-001; Proposed behavior | Moderate authoring risk; incomplete measurement details can mislead assessment. | unknown |
| SAMPLE-SVC-001 | null | Assess authorized response performance after identifying the implementation. | No code revision is available. | unknown; implementation impact cannot be inspected. | unknown |
| SAMPLE-REL-001 | null | Include performance evidence in proposed readiness assessment. | The sample release remains proposed. | unknown; release criteria are unavailable. | unknown |

## Options and consequences

| Option | Expected consequence | Evidence or inference | Required decision |
| --- | --- | --- | --- |
| Add the proposed requirement after review. | Performance assessment gains an explicit target. | Inference from the proposed measurement contract | Review target and complete missing conditions. |
| Retain the unspecified actual baseline. | Performance acceptance remains unresolved. | No actual baseline source exists. | Obtain the actual objective before choosing this option. |

## Proposed acceptance and validation

| Changed requirement or criterion ID | Canonical change location | Required validation | Current result | Evidence reference |
| --- | --- | --- | --- | --- |
| SAMPLE-NFR-AC-001 | [Nonfunctional requirement](nonfunctional-requirement.md) | Complete measurement conditions and retain raw observations. | NOT_RUN | null |

## Implementation and release proposal

- Proposed implementation scope: unknown; inspect the service repository at an exact revision first.
- Proposed release: SAMPLE-REL-001; no date exists.
- Estimate and basis: unknown; implementation and capacity are unavailable.
- Reversal approach: Retain earlier requirement versions; actual deployment reversal remains undefined.

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Unknowns and blockers

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| The actual baseline is unavailable. | The context supplies illustrative intent only. | A real before-and-after change cannot be established. | unknown | Obtain the current approved baseline. |
| Measurement conditions remain incomplete. | Environment and percentile method are unknown. | Performance acceptance cannot be reproduced. | unknown | Complete and review the measurement contract. |

## Requested decision and actual disposition

- Requested decision: Review whether the illustrative response requirement should enter a real baseline.
- Authorized decision owner: unknown; no authority evidence exists.
- Actual decision: pending.
- Actual decision reference: null.
- Implementation status: proposed; no implementation has occurred.
````

## Completion checks

- Entry route and actual chronology distinguish supplied implementation from requirements-first work.
- Missing historical intent remains explicit. Existing frozen intake and earlier approvals retain their original scope.
- Implementation, intent review, execution outcome, and acceptance have independent evidence states.
- Bounded exploration has measurable outcomes, permitted edits, authorization, stop conditions, and artifact disposition.
- Draft lint limits remain visible when product ACs are unresolved. No inferred requirement approves itself through matching code.

- Post-change records preserve intake hashes and give separate user and system impact.
- Named readiness decisions cite current evidence and keep missing browser execution open.
- Identify the exact baseline or state that it is unavailable.
- Describe the proposed difference without silently changing canonical rules.
- Inspect exact revisions before claiming implementation impact.
- Separate facts, impact inferences, and estimates.
- Define validation for every changed acceptance criterion.
- Record actual authorization before treating the request as approved.
- Preserve earlier versions and real governance audit events.
