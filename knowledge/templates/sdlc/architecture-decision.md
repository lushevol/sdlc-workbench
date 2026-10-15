# Architecture decision record

## Purpose

Record an engineering choice, its evidence, alternatives, and consequences.
Keep proposed decisions separate from accepted decisions.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: decision question, affected requirements, constraints, alternatives, source evidence, and responsible decision authority.

Compare alternatives against the same criteria.
Record the proposed choice without inventing agreement.
Keep `decision_state` proposed until recorded human review supports acceptance.
Record supersession through a successor reference and a new audit event.
Separate expected consequences from observed outcomes.

## Template

````markdown
---
artifact_kind: "architecture-decision"
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

# {{decision_title}}

## Decision identity

| Field | Value |
| --- | --- |
| Decision state | proposed |
| Decision question | {{specific_question}} |
| Affected requirement and design IDs | {{related_ids_and_relationships}} |
| Decision authority | {{authority_or_unknown}} |
| Effective date | null |
| Supersedes | {{decision_id_or_null}} |
| Audit event reference | {{event_ref_or_null}} |

## Context and criteria

Context: {{problem_existing_behavior_and_evidence_limits}}.
Constraints: {{required_constraints_and_source_refs}}.

| Criterion | Measure or assessment rule | Evidence |
| --- | --- | --- |
| {{criterion}} | {{how_each_option_is_compared}} | {{source_ref}} |

## Options

| Option | Description | Benefits | Costs and risks | Criterion assessment |
| --- | --- | --- | --- | --- |
| {{option_id}} | {{specific_option}} | {{expected_benefits}} | {{expected_costs_and_risks}} | {{supported_assessment_or_unknown}} |

## Proposed decision

Choice: {{selected_option_and_scope}}.
Rationale: {{evidence_supported_reason_for_selection}}.
Rejected alternatives: {{alternatives_and_specific_reasons}}.
Revisit trigger: {{measurable_condition_or_new_evidence}}.

## Consequences and implementation

| Consequence | Expected or observed | Evidence or assumption | Owner | Action |
| --- | --- | --- | --- | --- |
| {{consequence}} | {{expected_or_observed}} | {{source_or_observation}} | {{owner_or_unknown}} | {{implementation_or_mitigation_action}} |

Implementation dependencies: {{prerequisite_decisions_code_changes_and_permissions}}.
Verification: {{test_assertions_and_retained_execution_or_NOT_RUN}}.

## Decision review

| Decision | Reviewer | Review date | Evidence | Publication state |
| --- | --- | --- | --- | --- |
| pending | null | null | null | draft |

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
artifact_kind: "architecture-decision"
id: "SAMPLE-ADR-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-ARCH-001, SAMPLE-REQ-001, SAMPLE-REQ-002]
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

# Check invoice access in the service

## Decision identity

| Field | Value |
| --- | --- |
| Decision state | proposed |
| Decision question | Which component checks access for each invoice request? |
| Affected requirement and design IDs | SAMPLE-REQ-001 and SAMPLE-REQ-002 inform SAMPLE-ARCH-001. |
| Decision authority | unknown |
| Effective date | null |
| Supersedes | null |
| Audit event reference | null; no real governance change. |

## Context and criteria

Context: Customers request invoices through the proposed portal and service.
Constraints: Denied requests must return zero invoices under the illustrative access rules.

| Criterion | Measure or assessment rule | Evidence |
| --- | --- | --- |
| Access enforcement | Check permission before every invoice response. | SAMPLE-SRC-001, sample-v1, Proposed behavior. |
| Denied content | Return zero invoices after denied access. | SAMPLE-RULE-003. |
| Performance | Assess against SAMPLE-NFR-001 under its stated load. | No execution evidence. |

## Options

| Option | Description | Benefits | Costs and risks | Criterion assessment |
| --- | --- | --- | --- | --- |
| SAMPLE-OPTION-001 | Check access in the service for each request. | Expected enforcement at the data response boundary. | Policy integration and request cost require assessment. | Proposed; effectiveness untested. |
| SAMPLE-OPTION-002 | Check access only in the portal. | May reduce service logic; unmeasured. | Direct service requests could bypass portal checks. | Hypothesis requires boundary analysis. |

## Proposed decision

Choice: Propose SAMPLE-OPTION-001 for SAMPLE-SVC-001.
Rationale: The service returns invoice content and can check access before that response.
Rejected alternatives: SAMPLE-OPTION-002 lacks evidence that every requester must pass through the portal.
Revisit trigger: Review new access policy or interface boundary evidence.

## Consequences and implementation

| Consequence | Expected or observed | Evidence or assumption | Owner | Action |
| --- | --- | --- | --- | --- |
| Service checks access for every request. | expected | Proposed design only. | unknown | Identify policy inputs and access assertions. |
| Access checks add request work. | expected | Engineering inference; cost unmeasured. | unknown | Measure the complete request interval. |

Implementation dependencies: Policy source, responsible authority, and exact implementation revision remain unknown.
Verification: SAMPLE-TEST-001 and SAMPLE-TEST-002 remain NOT_RUN.

## Decision review

| Decision | Reviewer | Review date | Evidence | Publication state |
| --- | --- | --- | --- | --- |
| pending | null | null | null | draft |

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: A service check could prevent portal bypass; no implementation was inspected.
Unresolved questions: Who can accept this decision? Owner unknown; identify the decision authority.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-ADR-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | The proposal cannot establish an accepted architecture decision. | unknown | Obtain recorded human review before acceptance or publication. | open |
````

## Completion checks

- Compare at least two viable options, or justify why only one exists.
- Tie the proposed choice to documented criteria and constraints.
- Record consequences, owners, implementation dependencies, and revisit triggers.
- Require actual review evidence before changing the decision state.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
