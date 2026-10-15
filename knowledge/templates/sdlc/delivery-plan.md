# Delivery plan

## Purpose

Sequence deliverables, dependencies, ownership, and completion evidence.
Keep forecasts separate from actual completion and business approval.

## AI instructions

1. Obtain agreed scope, requirement versions, capacity assumptions, dependencies, and planning constraints.
2. Define deliverables through observable completion evidence.
3. Use dates only when their source or explicit planning assumption exists.
4. Record forecast dates separately from actual dates.
5. Link verification work to requirement and acceptance criterion IDs.
6. Do not invent staffing, elapsed effort, completed work, releases, or approval.

## Template

````markdown
---
artifact_kind: "delivery-plan"
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

# {{delivery_plan_title}}

## Planning basis and source facts

- Scope baseline: {{scope_artifact_ids_and_versions}}
- Planning horizon: {{horizon_or_unknown}}
- Available capacity: {{capacity_and_source_or_unknown}}
- Current completion evidence: {{evidence_or_none}}

## Proposed deliverables and milestones

| Deliverable ID | Observable result | Requirement IDs | Dependencies | Owner | Forecast date | Actual date | Completion evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{deliverable_id}} | {{deliverable_result}} | {{requirement_ids}} | {{dependency_ids_or_none}} | {{owner_or_unknown}} | {{date_or_null}} | {{date_or_null}} | {{evidence_or_null}} |

## Sequence and dependency handling

| Predecessor | Successor | Required condition | Failure consequence | Next action |
| --- | --- | --- | --- | --- |
| {{predecessor_id}} | {{successor_id}} | {{dependency_condition}} | {{consequence}} | {{dependency_action}} |

## Completion and acceptance gates

| Gate | Required evidence | Decision owner | Actual decision reference |
| --- | --- | --- | --- |
| {{gate}} | {{required_evidence}} | {{owner_or_unknown}} | {{reference_or_null}} |

## Planning assumptions and proposals

| Assumption or proposal | Basis | Validation action | Owner |
| --- | --- | --- | --- |
| {{assumption_or_proposal}} | {{basis_or_unknown}} | {{action}} | {{owner_or_unknown}} |

## Related artifacts

| Artifact ID | Relationship | Location |
| --- | --- | --- |
| {{artifact_id}} | {{relationship}} | {{locator}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Risks and unresolved questions

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Change and review control

- Replanning trigger: {{trigger}}
- Required review: {{review_scope}}
- Latest actual decision reference: {{reference_or_null}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "delivery-plan"
id: "SAMPLE-PLAN-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CHARTER-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-REL-001]
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

# Invoice portal delivery plan

## Planning basis and source facts

- Scope baseline: Proposed requirements SAMPLE-REQ-001 and SAMPLE-REQ-002 in sample-v1.
- Planning horizon: unknown.
- Available capacity: unknown; no staffing source exists.
- Current completion evidence: none; no implementation or execution exists.

## Proposed deliverables and milestones

| Deliverable ID | Observable result | Requirement IDs | Dependencies | Owner | Forecast date | Actual date | Completion evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-DELIVERABLE-001 | Reviewed invoice access criteria | SAMPLE-REQ-001, SAMPLE-REQ-002 | Identify the policy owner. | unknown | null | null | null |
| SAMPLE-DELIVERABLE-002 | Implemented access checks | SAMPLE-REQ-001, SAMPLE-REQ-002 | SAMPLE-DELIVERABLE-001 | unknown | null | null | null |
| SAMPLE-DELIVERABLE-003 | Retained access test results | SAMPLE-REQ-001, SAMPLE-REQ-002 | SAMPLE-DELIVERABLE-002 | unknown | null | null | null |

## Sequence and dependency handling

| Predecessor | Successor | Required condition | Failure consequence | Next action |
| --- | --- | --- | --- | --- |
| SAMPLE-DELIVERABLE-001 | SAMPLE-DELIVERABLE-002 | Actual human review supports the current requirement versions. | Unresolved intent can produce incorrect access behavior. | Identify the policy owner and request review. |
| SAMPLE-DELIVERABLE-002 | SAMPLE-DELIVERABLE-003 | Exact code and test revisions are available. | Results cannot identify the implementation assessed. | Retain exact revision identities before execution. |

## Completion and acceptance gates

| Gate | Required evidence | Decision owner | Actual decision reference |
| --- | --- | --- | --- |
| Requirement publication | Human review for the current requirement content | unknown | null |
| Behavior assessment | Assertions and retained executions for SAMPLE-AC-001 and SAMPLE-AC-002 | unknown | null |
| Proposed release SAMPLE-REL-001 | Release readiness and an actual release decision | unknown | null |

## Planning assumptions and proposals

| Assumption or proposal | Basis | Validation action | Owner |
| --- | --- | --- | --- |
| Sequence review before implementation. | Important requirements need recorded human review. | Confirm the project's review process. | unknown |
| Estimate dates after scope and capacity are known. | Both inputs remain unavailable. | Obtain scope and capacity evidence. | unknown |

## Related artifacts

| Artifact ID | Relationship | Location |
| --- | --- | --- |
| SAMPLE-CHARTER-001 | Defines proposed scope. | [Project charter](project-charter.md) |
| SAMPLE-REQ-001 | Defines permitted behavior. | [Requirement sample](requirement.md) |
| SAMPLE-REQ-002 | Defines denied behavior. | [Sample context](sample-context.md) |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Risks and unresolved questions

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Capacity and ownership are unknown. | The context supplies neither staffing nor owners. | Delivery dates cannot be justified. | unknown | Obtain a staffed delivery proposal. |
| Implementation revisions are unavailable. | The context records no repository revision. | Completion cannot be demonstrated. | unknown | Inspect the owning repository at an exact revision. |

## Change and review control

- Replanning trigger: A reviewed scope change or new dependency affects the proposed sequence.
- Required review: Scope, sequence, capacity, and release gates.
- Latest actual decision reference: null.
````

## Completion checks

- Give each deliverable an observable result and completion evidence field.
- Confirm dependencies reference existing deliverables or explicit external inputs.
- Keep forecast and actual dates separate.
- Confirm capacity supports forecasts or mark forecasts unavailable.
- Link behavior assessment to acceptance criterion IDs.
- Keep pending gates separate from actual decisions.
