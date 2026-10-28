# Project charter / product brief

## Purpose

Define the problem, proposed outcomes, and project boundary before detailed planning.
Link detailed requirements without replacing their canonical rules.

## AI instructions

1. Obtain the problem source, affected users, capability IDs, scope, sponsor, and outcome measures.
2. Identify which statements describe source facts and which statements propose future behavior.
3. Define each outcome's metric, target, measurement conditions, and evidence owner.
4. Mark unsupported targets, ownership, funding, and dates as unknown or null.
5. Reference the [requirements summary](business-product-requirements.md) and detailed requirements by stable IDs.
6. Do not invent customer research, commercial benefits, approvals, budgets, or delivery commitments.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "project-charter"
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

# {{project_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Problem and source facts

- Problem: {{supported_problem_statement}}
- Affected users: {{user_groups}}
- Existing behavior: {{observed_behavior_or_unknown}}
- Evidence limit: {{evidence_limit}}

## Proposed outcome and value

- Proposed outcome: {{desired_business_outcome}}
- Expected benefit: {{benefit_and_basis}}
- Capability IDs: {{capability_ids}}

| Outcome ID | Metric | Target and unit | Measurement conditions | Evidence owner |
| --- | --- | --- | --- | --- |
| {{outcome_id}} | {{metric}} | {{target_or_unknown}} | {{population_window_and_method}} | {{owner_or_unknown}} |

## Scope

| Included | Excluded | Boundary reason |
| --- | --- | --- |
| {{included_behavior}} | {{excluded_behavior}} | {{reason_and_source}} |

## Stakeholders and responsibilities

| Role | Identity | Responsibility | Decision authority evidence |
| --- | --- | --- | --- |
| {{role}} | {{identity_or_unknown}} | {{responsibility}} | {{source_or_unknown}} |

## Constraints and planning assumptions

| Type | Statement | Evidence or validation action |
| --- | --- | --- |
| {{constraint_or_assumption}} | {{statement}} | {{evidence_or_action}} |

## Related artifacts

| Artifact ID | Relationship | Location |
| --- | --- | --- |
| {{artifact_id}} | {{relationship}} | {{locator}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unresolved questions

| Question | Evidence limit | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{question}} | {{missing_evidence}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Review and publication

- Required business review: {{review_scope}}
- Decision evidence: {{actual_review_reference_or_null}}
- Publication condition: {{required_review_and_resolved_blockers}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "project-charter"
id: "SAMPLE-CHARTER-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CAP-001, SAMPLE-BPR-001, SAMPLE-REQ-001, SAMPLE-REQ-002]
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

# Invoice portal access brief

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Problem and source facts

- Problem: The fictional portal needs defined access behavior for customer invoices.
- Affected users: Customer A and Customer B in the illustrative context.
- Existing behavior: unknown; no implementation observation exists.
- Evidence limit: The context supplies illustrative intent only.

## Proposed outcome and value

- Proposed outcome: Customers can view owned invoices while unauthorized customers receive no invoice content.
- Expected benefit: Clear access expectations support design and test planning.
- Capability IDs: SAMPLE-CAP-001.

| Outcome ID | Metric | Target and unit | Measurement conditions | Evidence owner |
| --- | --- | --- | --- | --- |
| SAMPLE-OUTCOME-001 | Returned invoice count | Exactly 1 invoice | Proposed permitted scenario SAMPLE-AC-001; no execution exists. | unknown |
| SAMPLE-OUTCOME-002 | Returned invoice count | Exactly 0 invoices | Proposed denied scenario SAMPLE-AC-002; no execution exists. | unknown |

## Scope

| Included | Excluded | Boundary reason |
| --- | --- | --- |
| Customer invoice viewing | Invoice editing and payment | The context defines invoice viewing only. |
| Customer access checks | Staff access | The staff policy remains unknown. |

## Stakeholders and responsibilities

| Role | Identity | Responsibility | Decision authority evidence |
| --- | --- | --- | --- |
| Invoice policy owner | unknown | Review permitted and denied access rules. | unknown |
| Delivery owner | unknown | Coordinate requirement, design, and validation work. | unknown |

## Constraints and planning assumptions

| Type | Statement | Evidence or validation action |
| --- | --- | --- |
| Constraint | Important requirements need human review before publication. | Apply the shared authoring contract. |
| Assumption | The proposed service can enforce invoice access. | Inspect implementation before treating this assumption as fact. |

## Related artifacts

| Artifact ID | Relationship | Location |
| --- | --- | --- |
| SAMPLE-BPR-001 | Summarizes proposed requirements. | [Requirements summary](business-product-requirements.md) |
| SAMPLE-REQ-001 | Defines permitted access criteria. | [Requirement sample](requirement.md) |
| SAMPLE-REQ-002 | Defines denied access criteria. | [Sample context](sample-context.md) |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Unresolved questions

| Question | Evidence limit | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Who owns invoice policy? | The context names no policy owner. | Business review cannot be assigned. | unknown | Identify the business owner and obtain the policy source. |
| What commercial benefit is expected? | No business case exists. | Benefit estimates remain unavailable. | unknown | Obtain an evidence-backed business case. |

## Review and publication

- Required business review: Invoice access policy and proposed scope.
- Decision evidence: null.
- Publication condition: Record actual human review and resolve policy blockers.
````

## Completion checks

- Confirm the problem has a source and an explicit evidence limit.
- Confirm every outcome has a metric or a recorded missing input.
- Confirm scope exclusions do not contradict referenced requirements.
- Confirm stakeholder authority has evidence or remains unknown.
- Keep estimates separate from commitments.
- Record required human review before publication.
