# Defect report

Use this template for business behavior defects in existing repositories.
Harness setup, tooling, configuration upgrades, and template maintenance require no business task.

Keep one living `tasks/<task-id>/01-intake.md` with the latest supported understanding.
Use its six sections to explain the problem, evidence, answers, verification, cause, and proposed correction.
Keep claim-bearing raw logs and investigation records under the task's evidence directory.
Link supporting material instead of repeating reports or creating a document for each investigation round.
Keep the intake and short evidence index prominent. Apply the task guide's Necessary, Important, and Unimportant retention priorities.

Read the [task guide](../../../../tasks/README.md) and [intake procedure](../../../../.agents/skills/analyze-requirement/SKILL.md).
Follow the [authoring contract](README.md). The [sample context](sample-context.md) supplies fictional sample inputs only.
The schema also accepts the previous heading layout for retained documents.

1. Record the reported problem and previous answers before asking new questions.
2. Search domain knowledge, exact repository revisions, test assertions, and earlier evidence.
3. Ask focused questions only for material gaps. Keep each answer's source and limits.
4. Reproduce safely within authorized access. Retain controls, actual results, screenshots, and execution identity.
5. Separate observed symptoms, supported causal mechanisms, hypotheses, and unconfirmed production applicability.
6. Define proposed corrected behavior, measurable regression criteria, and remaining decisions before the next phase.

Define regression cases through the [canonical Gherkin rules](../../../../tasks/README.md#canonical-gherkin-test-cases).
Link each case heading from this intake. Keep detailed steps and assertions in the canonical catalog.

Use explicit unknowns. Do not invent policy, severity, timings, screenshots, execution, approvals, or owners.
Search existing sources before asking the user to restate intent.
Update affected domain knowledge after a material clarification completes. Keep required publication review separate.
Retain screenshot originals and hashes. Any annotated or redacted derivative needs its own source link and hash.
Label screenshots as business reproduction, synthetic tooling, or actual test output. Do not infer their origin from browser use.
Screenshots support visible claims. Logs and inspected assertions support timing, network, and service claims.
For browser issues, check relevant timing, visibility, sleep, connectivity, SSO, and browser configuration.
Use only applicable fields. Explain omitted controls and evidence limits beside the affected claims.

## Template

````markdown
---
artifact_kind: defect-report
id: "{{stable_defect_id}}"
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

## Problem description

{{reported_problem_and_business_consequence}}

- Reported scope: {{environment_users_frequency_and_trigger_or_unknown}}.
- Expected behavior: {{source_supported_rule_and_criterion_or_explicitly_proposed_expectation}}.
- Actual behavior: {{reported_result_or_direct_observation_with_source}}.
- Classification: {{hypothetical_suspected_or_confirmed_in_named_scope}}; {{severity_priority_and_evidence_or_unassessed}}.

## Existing knowledge and code facts

| Kind | Knowledge, code fact, or conflict | Source and exact locator | Authority, revision, and limits |
| --- | --- | --- | --- |
| {{documented_intent_or_code_fact_or_assertion_or_inference_or_conflict}} | {{claim_and_applicable_criterion}} | {{source_id_and_section_or_symbol_or_lines}} | {{exact_revision_or_hash_review_state_and_scope_limits}} |

Search scope: {{knowledge_repositories_tests_prior_reports_and_bounds}}.
Missing evidence: {{material_gaps_and_why_they_matter_or_none}}.

### Source references

| ID | Locator | Exact revision or hash | Owner, authority, and limits |
| --- | --- | --- | --- |
| {{source_id}} | {{source_path_or_resource}} | {{exact_revision_hash_or_explicit_unknown}} | {{source_owner_or_unknown}}; {{authority_and_limits}} |

## User clarifications

| ID | Question or supplied detail | Answer and source | Status | Consequence, owner, and next action |
| --- | --- | --- | --- | --- |
| {{question_id}} | {{material_question_or_prior_detail}} | {{answer_or_unknown_and_message_or_source_locator}} | {{answered_pending_or_conflicting}} | {{decision_effect}}; unknown; {{next_action}} |

### Knowledge updates

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| {{gap_or_question_id}} | {{record_and_prior_version_or_missing}} | {{clarification_source_scope_version_and_limits}} | {{record_version_criterion_or_pending}} | {{finding_and_new_audit_refs_or_not_applicable_with_reason}} | {{actual_review_state}}; unknown; {{next_action}} |

Use `not applicable` with a reason when answers change no domain knowledge.
Keep unresolved gaps open. Complete material knowledge updates before handing off the resolved scope.

## Reproduction and verification

- Run and environment: {{execution_id_status_environment_browser_and_platform_when_applicable}}.
- Exact code and tests: {{repository_ids_revisions_and_inspected_assertions}}.
- Preconditions and inputs: {{session_data_configuration_and_relevant_timestamps_with_timezone}}.
- Controls and limits: {{foreground_or_other_control_mocks_instrumentation_untested_differences_and_observer_effects}}.

| Step | Action or condition | Expected result and source | Actual result | Evidence |
| --- | --- | --- | --- | --- |
| {{step}} | {{reproducible_action_and_timing}} | {{observable_result_and_rule}} | {{observed_result_or_NOT_RUN}} | {{screenshot_trace_log_or_none}} |

### Screenshots and execution evidence

{{inline_screenshot_with_meaningful_caption_or_explicit_reason_no_screenshot_exists}}

| Evidence ID | File or exact locator | Run, time, phase, and capture method | Hash or manifest entry | Claim and limits |
| --- | --- | --- | --- | --- |
| {{evidence_id}} | {{task_relative_path_or_existing_source_locator}} | {{run_id_timestamp_timezone_phase_and_method_or_explicit_unknown}} | {{sha256_or_manifest_entry}} | {{what_it_proves_and_does_not_establish}} |

Evidence index: {{task_evidence_index}}.
Keep natural runs separate from forced failures and service fixtures.

## Root cause analysis

{{causal_chain_or_explicitly_unknown_cause_with_supported_scope}}

| Finding or hypothesis | Supporting evidence | Contradiction or missing check | Confidence and consequence | Owner and next action |
| --- | --- | --- | --- | --- |
| {{candidate_cause_or_confirmed_mechanism}} | {{source_and_execution_ids}} | {{counterevidence_or_missing_control}} | {{fact_inference_or_unresolved_and_scope}}; {{consequence}} | unknown; {{next_action}} |

Production applicability: {{deployed_parity_and_runtime_evidence_or_explicitly_unconfirmed}}.

## Proposed fix and acceptance criteria

- Corrected behavior: {{observable_before_and_after_with_policy_source_or_proposal_status}}.
- Preliminary fix scope: {{inspected_components_interfaces_risk_and_boundaries_or_unknown}}.
- Policy decisions: {{remaining_material_decisions_and_owner_or_none_with_basis}}.

Criteria remain proposed until applicable business decisions support them.
Use source limits or clearly labelled fixture values. Do not invent business thresholds.

```gherkin
Feature: {{corrected_behavior}}

  Scenario: {{criterion_id_and_condition}}
    Given {{relevant_environment_data_and_policy_condition}}
    When {{business_action_or_lifecycle_event}}
    Then {{observable_result_and_required_limit}}
```

| Criterion | Preliminary test case and level | Required assertion and control | Execution status and evidence |
| --- | --- | --- | --- |
| {{criterion_id}} | {{test_id_positive_negative_boundary_or_failure_case_and_level}} | {{assertion_and_comparison}} | {{NOT_RUN_or_actual_result_with_evidence}} |

### Readiness and closure

| Named next phase | Readiness | Evidence and material limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| {{next_phase}} | {{READY_or_READY_WITH_LIMITS_or_NEEDS_CLARIFICATION}} | {{scope_specific_rationale}} | {{blocked_actions_or_none_with_basis}} | unknown; {{next_action}} |

- Implementation authority: {{existing_authorization_and_scope_or_not_established}}.
- Retest and closure: {{NOT_RUN_or_retained_retest_evidence}}; {{actual_closure_decision_or_pending}}.

Only `READY` permits the named next phase.
`READY_WITH_LIMITS` permits further intake evidence collection only. `NEEDS_CLARIFICATION` blocks downstream work.
Readiness does not establish business approval, knowledge publication, or completed implementation.
````

## Illustrative sample

This fictional invoice case records no actual defect, user report, repository inspection, screenshot, or execution.

````markdown
---
artifact_kind: defect-report
id: SAMPLE-DEFECT-001
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

## Problem description

A denied invoice request could expose invoice content.
This example proposes an investigation. It records no observed exposure.

- Reported scope: unknown. No actual user report exists.
- Expected behavior: SAMPLE-AC-002 proposes zero invoices and the message "Access denied".
- Actual behavior: NOT_RUN. No runtime observation exists.
- Classification: hypothetical; severity and priority remain unassessed because no impact evidence exists.

## Existing knowledge and code facts

| Kind | Knowledge, code fact, or conflict | Source and exact locator | Authority, revision, and limits |
| --- | --- | --- | --- |
| Documented sample intent | Customer B lacks permission for INV-001. SAMPLE-AC-002 expects zero invoices and "Access denied". | SAMPLE-SRC-001; Product and identities; Proposed behavior | sample-v1; illustrative only; no business approval |
| Missing code and assertion evidence | No implementation revision or executable assertion was inspected. | SAMPLE-SRC-001; Verification and release | sample-v1; no execution exists |
| Inference | Returned invoice content would contradict the sample criterion. | SAMPLE-AC-002 | Applies to the illustrative rule only |

Search scope: The supplied sample context only. No actual repository or business source was available.
Missing evidence: Actual policy, implementation, impact, and execution remain unknown.

### Source references

| ID | Locator | Exact revision or hash | Owner, authority, and limits |
| --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1; no source hash supplied | unknown; illustrative only; no actual approval or execution |

## User clarifications

| ID | Question or supplied detail | Answer and source | Status | Consequence, owner, and next action |
| --- | --- | --- | --- | --- |
| SAMPLE-Q-001 | What denial result does the sample propose? | Zero invoices and "Access denied"; SAMPLE-SRC-001, Proposed behavior | answered from supplied material | Defines proposed assertions; unknown; obtain actual policy before business implementation |
| SAMPLE-Q-002 | Which implementation can execute the test? | unknown; no implementation source supplied | pending | Execution target remains unknown; unknown; inspect the registered repository |

No actual user answered these fictional questions.

### Knowledge updates

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-Q-001 | not applicable; no actual record | Illustrative answer from SAMPLE-SRC-001; sample scope only | not applicable; no domain knowledge changed | not applicable; no governance change occurred | No publication; unknown; obtain actual policy |
| SAMPLE-Q-002 | unknown | No target source exists | pending | pending | Unresolved; unknown; identify implementation |

## Reproduction and verification

- Run and environment: NOT_RUN. No actual environment or execution ID exists.
- Exact code and tests: SAMPLE-REPO-001 and SAMPLE-TEST-002 are illustrative. Their revisions and assertions remain unknown.
- Preconditions and inputs: Authenticate customer B without permission for INV-001.
- Controls and limits: Plan an authorized customer A request. No setup, instrumentation, or actual control ran.

| Step | Action or condition | Expected result and source | Actual result | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Prepare customer B without access to INV-001 | Denied-access condition; SAMPLE-SRC-001 | NOT_RUN | none |
| 2 | Request INV-001 as customer B | Zero invoices and "Access denied"; SAMPLE-AC-002 | NOT_RUN | none |
| 3 | Request INV-001 as customer A | Exactly one invoice with ID INV-001; SAMPLE-AC-001 | NOT_RUN | none |

### Screenshots and execution evidence

No screenshot exists because no browser or service execution occurred.

| Evidence ID | File or exact locator | Run, time, and capture method | Hash or manifest entry | Claim and limits |
| --- | --- | --- | --- | --- |
| none | No execution capture exists | NOT_RUN | not applicable | The example establishes no observed behavior |

Evidence index: not applicable. This fictional sample creates no task or evidence files.

## Root cause analysis

The cause remains unknown. No inspected code or retained execution supports a causal mechanism.

| Finding or hypothesis | Supporting evidence | Contradiction or missing check | Confidence and consequence | Owner and next action |
| --- | --- | --- | --- | --- |
| A denied response might contain invoice content | No runtime evidence | No response, implementation, or control was inspected | Unresolved hypothesis; no confirmed defect exists | unknown; inspect exact code and retain denied and permitted responses |

Production applicability: unconfirmed. No deployed revision or production evidence exists.

## Proposed fix and acceptance criteria

- Corrected behavior: Proposed only. A denied request returns zero invoices and "Access denied" under SAMPLE-AC-002.
- Preliminary fix scope: unknown. No component or interface was inspected. A runtime change would be premature.
- Policy decisions: The actual access-policy owner is unknown. Obtain applicable intent and implementation evidence.

The following criteria use illustrative rules. They record no execution or approval.

```gherkin
Feature: Apply the proposed invoice access rule

  Scenario: SAMPLE-AC-002 denies an unauthorized invoice request
    Given customer B has no permission for invoice INV-001
    When customer B requests invoice INV-001
    Then the response contains exactly 0 invoices
    And the response message is "Access denied"

  Scenario: SAMPLE-AC-001 preserves permitted invoice access
    Given customer A owns invoice INV-001
    When customer A requests invoice INV-001
    Then the response contains exactly 1 invoice
    And the invoice identifier is "INV-001"
```

| Criterion | Preliminary test case and level | Required assertion and control | Execution status and evidence |
| --- | --- | --- | --- |
| SAMPLE-AC-002 | SAMPLE-TEST-002; denied-access service regression | Assert invoice count 0 and exact denial message; compare authorized control | NOT_RUN; none |
| SAMPLE-AC-001 | SAMPLE-TEST-001; permitted-access service control | Assert invoice count 1 and identifier INV-001 | NOT_RUN; none |

### Readiness and closure

| Named next phase | Readiness | Evidence and material limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Implementation planning | NEEDS_CLARIFICATION | Actual policy, implementation, environment, and observed behavior remain unknown. | Downstream SDLC work | unknown; inspect actual sources and obtain a reproduction |

- Implementation authority: not established. The fictional sample authorizes no runtime change.
- Retest and closure: NOT_RUN; pending. No correction or closure occurred.

Readiness does not establish business approval or knowledge publication.
````

## Completion checks

- One living intake presents the latest understanding through the six sections.
- A short evidence index highlights useful support. Authorized cleanup removes clutter with traceable deletion records and repaired references.
- Existing facts and previous answers precede new questions. Every material claim identifies evidence and limits.
- Code, assertions, and executions retain exact revisions. Documented intent remains separate from implementation and observation.
- New evidence stays under the task. Existing authoritative sources and audit history retain their bytes and identities.
- User answers retain sources, statuses, consequences, owners, and next actions.
- Completed material clarifications update affected knowledge and provenance before handoff. Required publication reviews remain separate.
- Reproduction steps identify inputs, controls, actual outcomes, and evidence. Screenshots include provenance or an explicit absence reason.
- Root cause claims name supported scope, causal evidence, missing controls, and production applicability.
- Proposed corrected behavior has measurable Gherkin criteria and tests. Unresolved business decisions remain visible.
- Readiness names the next phase and its material limits. Closure requires actual retest evidence and a recorded decision.
- Replace every placeholder. Preserve unknowns, evidence limits, and pending reviews until supporting evidence resolves them.
