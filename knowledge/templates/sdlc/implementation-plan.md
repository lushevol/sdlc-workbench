# Implementation plan

## Purpose

Translate reviewed intent into ordered engineering tasks and verification steps.
State dependencies, affected interfaces, risks, and recovery actions.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: requirement versions, acceptance criteria, design decisions, exact repository revisions, affected symbols, execution grants, and delivery constraints.

Inspect callers, importers, and interface paths before estimating affected scope.
Resolve missing business rules through responsible owners.
Define each task's output and completion evidence before implementation.
Use risk-based verification for consequential boundaries and confirmed defects.
Do not mark a planned assertion as executed.
Keep irreversible actions subject to the project's actual authorization rules.

## Template

````markdown
---
artifact_kind: "implementation-plan"
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

# {{change_title}} implementation plan

## Objective and baseline

| Field | Value |
| --- | --- |
| Outcome and requirement IDs | {{observable_outcome_and_ids}} |
| Included and excluded work | {{scope_and_exclusions}} |
| Repository baselines | {{repository_ids_and_full_commits_or_null}} |
| Design and decision references | {{design_and_reviewed_decision_ids}} |
| Delivery constraints | {{dates_environments_dependencies_or_unknown}} |
| Plan state | proposed |

## Affected scope and risk

| Symbol or boundary | Inspected revision and location | Callers and importers | Expected impact | Qualitative risk and reason |
| --- | --- | --- | --- | --- |
| {{symbol_or_interface}} | {{full_commit_path_and_lines}} | {{inspected_call_paths}} | {{behavior_data_or_compatibility_impact}} | {{risk_and_supported_reason}} |

## Preconditions

| Dependency or question | Required resolution | Owner | Evidence | State |
| --- | --- | --- | --- | --- |
| {{policy_design_access_or_environment_dependency}} | {{explicit_completion_condition}} | {{owner_or_unknown}} | {{source_or_null}} | {{open_or_satisfied}} |

## Ordered tasks

| Task ID | Depends on | Action and output | Owner | Completion evidence | State |
| --- | --- | --- | --- | --- | --- |
| {{task_id}} | {{task_ids_or_none}} | {{specific_change_and_deliverable}} | {{owner_or_unknown}} | {{review_diff_assertion_or_result}} | planned |

## Acceptance and verification

```gherkin
Feature: {{required_behavior}}
  @{{requirement_id}} @{{criterion_id}}
  Scenario: {{scenario_name}}
    Given {{initial_condition}}
    When {{action}}
    Then {{measurable_observable_result}}
```

| Criterion or boundary | Planned check and assertion | Exact test revision | Execution environment and grant | Actual result |
| --- | --- | --- | --- | --- |
| {{criterion_or_boundary}} | {{test_or_inspection_and_expected_result}} | {{revision_or_null}} | {{environment_and_grant_or_null}} | NOT_RUN |

## Recovery and completion

Rollback trigger: {{failure_condition_and_decision_owner}}.
Recovery action: {{reversible_change_or_restore_plan}}.
Irreversible actions: {{actions_and_required_actual_authorization_or_none_with_reason}}.
Completion gate: {{required_reviews_checks_and_retained_evidence}}.
Remaining limits: {{unresolved_behavior_evidence_or_environment_limits}}.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{document_or_repository_path_and_lines}} | {{exact_revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_content_read}} |

Facts: {{source_supported_facts}}.
Inferences: {{reasoned_conclusions_with_evidence_and_limits}}.
Unresolved questions: {{questions_owner_and_resolution_needed}}.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| {{finding_id}} | {{source_revision_and_locator}} | {{observable_effect_or_risk}} | {{owner_or_unknown}} | {{specific_action_and_completion_evidence}} | {{open_or_resolved}} |
````

## Illustrative sample

````markdown
---
artifact_kind: "implementation-plan"
id: "SAMPLE-PLAN-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-ARCH-001, SAMPLE-ADR-001]
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

# Plan controlled invoice access

## Objective and baseline

| Field | Value |
| --- | --- |
| Outcome and requirement IDs | Permit owned access; deny other access; SAMPLE-REQ-001 and SAMPLE-REQ-002. |
| Included and excluded work | Invoice access checks; staff behavior excluded until policy exists. |
| Repository baselines | SAMPLE-REPO-001; full commit null. |
| Design and decision references | SAMPLE-ARCH-001 and SAMPLE-ADR-001 remain proposed. |
| Delivery constraints | Environment and delivery schedule unknown. |
| Plan state | proposed |

## Affected scope and risk

| Symbol or boundary | Inspected revision and location | Callers and importers | Expected impact | Qualitative risk and reason |
| --- | --- | --- | --- | --- |
| Invoice request access boundary | null; source path unknown. | unknown | Controls whether invoice content is returned. | High potential consequence; unauthorized disclosure hypothesis. |
| SAMPLE-CONTRACT-001 response | null; source path unknown. | unknown | Proposed permitted and denied results. | Scope unknown until consumers are inspected. |

## Preconditions

| Dependency or question | Required resolution | Owner | Evidence | State |
| --- | --- | --- | --- | --- |
| Invoice access policy | Record policy authority and human review. | unknown | SAMPLE-SRC-001 lists policy ownership as unknown. | open |
| Repository baseline | Inspect instructions and source at a full commit. | unknown | null | open |
| Design decision | Record authorized review of SAMPLE-ADR-001. | unknown | null | open |
| Test environment | Identify environment, data, tools, and actual execution grants. | unknown | null | open |

## Ordered tasks

| Task ID | Depends on | Action and output | Owner | Completion evidence | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-TASK-001 | none | Resolve policy questions and record reviewed intent. | unknown | Source and real review references. | planned |
| SAMPLE-TASK-002 | SAMPLE-TASK-001 | Inspect request path, callers, imports, and assertions at one revision. | unknown | Source map with full commit and locations. | planned |
| SAMPLE-TASK-003 | SAMPLE-TASK-002 | Implement the reviewed service check at the confirmed boundary. | unknown | Reviewed diff and requirement mapping. | planned |
| SAMPLE-TASK-004 | SAMPLE-TASK-003 | Execute permitted and denied access checks in the authorized environment. | unknown | Assertions, environment, and retained results. | planned |

## Acceptance and verification

```gherkin
Feature: Controlled invoice access
  @SAMPLE-REQ-002 @SAMPLE-AC-002
  Scenario: Customer requests an invoice without permission
    Given Customer B has no permission to view INV-001
    When Customer B requests INV-001
    Then the response contains zero invoices
    And the response states "Access denied"
```

| Criterion or boundary | Planned check and assertion | Exact test revision | Execution environment and grant | Actual result |
| --- | --- | --- | --- | --- |
| SAMPLE-AC-001 | SAMPLE-TEST-001; invoice count 1; identifier INV-001. | null | null | NOT_RUN |
| SAMPLE-AC-002 | SAMPLE-TEST-002; invoice count 0; "Access denied". | null | null | NOT_RUN |
| Contract consumers | Inspect compatibility at the confirmed response boundary. | null | null | NOT_RUN |

## Recovery and completion

Rollback trigger: Proposed unexpected access result or contract incompatibility; decision owner unknown.
Recovery action: Determine the reviewed revert and deployment recovery steps after source inspection.
Irreversible actions: unknown; no execution or deployment is authorized by this plan.
Completion gate: Required reviews, inspected assertions, and retained results support the scoped behavior claims.
Remaining limits: No implementation, environment, test execution, or delivery date is established.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: Access changes affect a sensitive boundary; actual code scope remains unknown.
Unresolved questions: Which policy, repository, and environment authorize implementation? Owners unknown; resolve prerequisites.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-PLAN-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | The team cannot start a concrete implementation from supported evidence. | unknown | Resolve the policy and exact source baseline before changing code. | open |
````

## Completion checks

- Record affected symbols, callers, importers, and interfaces with evidence limits.
- Give each task dependencies, an owner, a deliverable, and completion evidence.
- Map planned checks to measurable acceptance criteria.
- Define recovery and completion gates before executing consequential changes.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
