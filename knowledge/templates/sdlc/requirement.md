# Requirement / user story

## Purpose

Define one required behavior and its observable acceptance conditions.

Read the [AI authoring contract](README.md) before use.
Read the [sample context](sample-context.md) before interpreting the example.

## AI instructions

- Create `tasks/<task-id>/` before discovery. Copy this Template block into its `intake.md`.
- Follow the [task contract](../../../tasks/README.md) and [intake procedure](../../../.agents/skills/analyze-requirement/SKILL.md).
- Record supplied facts and prior answers. Search existing knowledge before asking users to restate intent.
- Inspect registered code, test assertions, and investigation results to establish the current state.
- Read reports as secondary evidence. Repositories can use optional `repos/` clones or configured locations.
- Drill material ambiguities through small question rounds and evidence checks until the named next phase is clear.
- Retain new evidence under the task's `evidence/` directory. Index sources, hashes, exact revisions, claims, and limits.
- Reference existing raw snapshots and audit history at their original paths. Never move or rewrite them.
- Use `READY` only when no unresolved material uncertainty affects the named next phase. Record the rationale.
- `READY_WITH_LIMITS` permits evidence collection only. `NEEDS_CLARIFICATION` blocks downstream work.
- Read the requested outcome, business rules, and applicable source revisions.
- State the required behavior before choosing an implementation.
- Use the user story sentence only when it clarifies the actor and benefit.
- Give every acceptance criterion a stable ID and an observable result.
- Cover successful behavior, boundaries, rejected actions, and failures where the requirement applies.
- Use a separate requirement when a scenario specifies a different business rule.
- Keep structured criteria and readable Gherkin consistent.
- Keep all structured criteria in one acceptance_criteria list. Add matching scenarios within the same Gherkin Feature.
- Replace numeric target placeholders with numbers. Use only the supported comparison operators.
- Remove quotes around numeric YAML targets after replacing their placeholders.
- Obtain missing business thresholds from the responsible owner.
- Use the supported Requirement record when transferring this content into Workbench.

## Template

Copy this block. Replace placeholders and retain the required sections.

````markdown
---
artifact_kind: requirement
id: "{{artifact_id}}"
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

# {{requirement_title}}

## Description

As {{actor}}, I need {{required_behavior}} so that {{business_benefit}}.
{{required_inputs_and_observable_outputs}}

## Rationale

{{business_need_and_source_reference}}

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| {{included_behavior}} | {{excluded_behavior}} | {{scope_reason}} |

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| {{next_phase}} | {{READY_or_READY_WITH_LIMITS_or_NEEDS_CLARIFICATION}} | {{material_uncertainty_and_phase_rationale}} | {{blocked_actions_or_none_with_basis}} | unknown; {{next_action}} |

- Expected behavior authority: {{documented_intent_source_approval_state_and_limits}}
- Existing authorization: {{actual_authorization_source_and_scope_or_not_established}}
- Evidence index: {{task_evidence_index_path}}
- Business review: pending. Readiness does not grant approval.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| {{actor}} | {{rule_id}} | {{condition}} | {{behavior}} | {{source_locator_and_revision}} |

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| {{related_artifact_id}} | {{depends_on_or_constrains}} | {{source_reference}} | {{impact_or_none_with_evidence}} |

## Acceptance criteria

```gherkin
@{{requirement_id}} @{{criterion_id}}
Feature: {{required_behavior}}

  Scenario: {{condition_action_and_result}}
    Given {{initial_state}}
    When {{action}}
    Then {{observable_outcome_with_required_limit}}
```

```yaml
acceptance_criteria:
  - id: "{{criterion_id}}"
    given: "Given {{initial_state}}"
    when: "When {{action}}"
    then: "Then {{observable_outcome_with_required_limit}}"
    measure:
      metric: "{{metric}}"
      operator: "{{equals_or_at_least_or_at_most_or_less_than_or_greater_than}}"
      value: "{{numeric_target}}"
      unit: "{{unit}}"
```

Add each applicable criterion to this YAML list.
Add its matching scenario to the Gherkin Feature above.

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| {{criterion_id}} | {{assertion_or_measurement_method}} | {{conditions}} | {{conditions_or_not_applicable_reason}} | {{retained_result_reference}} |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| {{criterion_id}} | {{design_id}} | {{repository_id_commit_and_path_or_null}} | {{assertion_locator_or_null}} | {{execution_reference_or_null}} |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| {{source_id}} | {{locator}} | {{revision_or_null}} | {{hash_or_null}} | {{actual_owner_and_authority_or_unknown}} | {{evidence_limit}} |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| {{fact_inference_or_unknown}} | {{statement}} | {{source_or_missing_evidence}} | {{effect}} | unknown | {{action}} |

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| {{knowledge_repository_test_report_or_investigation_source}} | {{revision_or_hash}} | {{rule_and_criterion_ids_or_no_match}} | {{authority_and_limits}} | {{gap_or_none}} |

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| {{round_and_question_id}} | {{material_question_or_known_detail}} | {{answer_or_unknown}} | {{source_locator_or_none}} | {{answered_pending_or_conflicting}} | unknown | {{consequence_and_next_action}} |

### Intake investigation plan

- Current state: {{source_supported_current_behavior_or_unknown}}
- Evidence needed: {{decision_relevant_gap_and_required_observation}}
- Method and controls: {{browser_service_flow_or_test_assertion_checks_with_environment_and_limits}}
- Retention: {{new_task_evidence_paths_and_existing_source_references}}
- Next decision: {{evidence_required_to_resolve_material_uncertainty_for_named_next_phase}}
````

## Illustrative sample

This sample is fictional. It records no actual approval or execution.

````markdown
---
artifact_kind: requirement
id: "SAMPLE-REQ-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
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

# View an owned invoice

## Description

As a customer, I need to view an owned invoice to check its details.
Return exactly one invoice when the authenticated customer has permission.

## Rationale

SAMPLE-RULE-001 proposes access to an owned invoice in SAMPLE-SRC-001.
This sample records proposed intent only.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| Authenticated customer views an owned invoice. | Staff access and denied access. | Staff policy is unknown. SAMPLE-REQ-002 covers denied access. |

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Implementation planning | NEEDS_CLARIFICATION | The rule is illustrative. Actual policy and current implementation remain unknown. | Downstream SDLC work | unknown; inspect actual policy and implementation |

- Expected behavior authority: SAMPLE-RULE-001 is illustrative. No actual business approval exists.
- Existing authorization: none. This sample authorizes no system access or business change.
- Evidence index: not applicable. This fictional example creates no actual task or evidence.
- Business review: pending. Readiness does not grant approval.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| Customer A | SAMPLE-RULE-001 | Customer A is authenticated and owns INV-001. | Return invoice INV-001. | SAMPLE-SRC-001 at sample-v1 |

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| SAMPLE-REQ-002 | Defines denied access. | SAMPLE-SRC-001 at sample-v1 | Policy ownership remains unknown. |

## Acceptance criteria

```gherkin
@SAMPLE-REQ-001 @SAMPLE-AC-001
Feature: View an owned invoice

  Scenario: Customer requests an owned invoice
    Given customer "A" is authenticated and owns invoice "INV-001"
    When customer "A" requests invoice "INV-001"
    Then the response contains exactly one invoice with identifier "INV-001"
```

```yaml
acceptance_criteria:
  - id: SAMPLE-AC-001
    given: 'Given customer "A" is authenticated and owns invoice "INV-001"'
    when: 'When customer "A" requests invoice "INV-001"'
    then: 'Then the response contains exactly one invoice with identifier "INV-001"'
    measure:
      metric: response invoice count
      operator: equals
      value: 1
      unit: count
```

The matching identifier assertion is required in addition to the numeric count.

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| SAMPLE-AC-001 | Assert invoice count and identifier in the response. | Proposed test environment with customer A and INV-001. | One request. Concurrency is not applicable to this criterion. | Actual response and assertion results; currently null. |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| SAMPLE-AC-001 | SAMPLE-ARCH-001 | SAMPLE-REPO-001; commit and path null. | SAMPLE-TEST-001; assertion and revision null. | null; NOT_RUN |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only. | No actual policy, approval, or registered snapshot. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Proposed intent | Permit owned invoice access. | SAMPLE-RULE-001 in illustrative source SAMPLE-SRC-001. | Defines the sample acceptance expectation only. | unknown | Obtain the actual access policy. |
| Unknown | No actual code or execution evidence exists. | Exact revision, assertions, and retained results are missing. | Behavior verification cannot proceed. | unknown | Inspect implementation and execute applicable assertions. |

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| sample-context.md | sample-v1 | SAMPLE-RULE-001; SAMPLE-AC-001 | Fictional context only. No actual repository or investigation exists. | Actual policy and implementation remain unknown. |

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1; SAMPLE-Q-001 | Which source defines actual access policy? | unknown | No actual source supplied | pending | unknown | Downstream work remains blocked; identify actual policy |

### Intake investigation plan

- Current state: unknown. The sample contains no actual system observations.
- Evidence needed: actual policy, current implementation, concrete test assertions, and relevant retained results.
- Method and controls: inspect identified sources before selecting authorized runtime checks.
- Retention: not applicable. The sample creates no actual task or evidence.
- Next decision: resolve actual policy and current behavior before implementation planning.
````

## Completion checks

- Intake and new evidence remain under the same task. Existing source and audit paths remain unchanged.
- Known answers have sources. Each material question has a status, owner, consequence, and next action.
- Knowledge review precedes questions that ask users to restate intent.
- Current behavior, actual test assertions, and required investigation results have explicit evidence limits.
- Readiness names the next phase and explains why no unresolved material uncertainty can change its decision.
- Limited readiness permits only evidence collection. Business approval and execution remain separate.
- Each criterion names conditions, an action, and an observable result.
- Each numeric limit has a metric, operator, value, unit, and measurement conditions.
- Gherkin and structured clauses express the same behavior.
- Scenario coverage follows the requirement's scope.
- Traceability distinguishes planned tests from actual retained execution.
- Publication uses actual human review and a new audit event.
