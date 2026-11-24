# Feature / epic brief

## Purpose

Group related requirements around one proposed user or business outcome.
Show the delivery boundary without replacing detailed acceptance criteria.

## AI instructions

1. Obtain the outcome, affected actors, scope, requirement IDs, dependencies, and intended release context.
2. Explain why the requirements belong together.
3. Reference canonical Gherkin acceptance criteria instead of creating inconsistent copies.
4. Define completion through requirement coverage and retained evidence.
5. Mark unknown value measures, release dates, owners, and priorities explicitly.
6. Do not invent customer demand, commitment, completed work, or approval.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "feature-epic"
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

# {{feature_or_epic_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Context and source facts

- Business problem: {{problem_and_source}}
- Primary actors: {{actors}}
- Current behavior: {{observed_behavior_or_unknown}}
- Evidence limit: {{limit}}

## Proposed outcome

- User outcome: {{observable_outcome}}
- Business value: {{benefit_and_basis}}
- Success measure: {{metric_target_conditions_or_unknown}}

## Scope and exclusions

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| {{included}} | {{excluded}} | {{reason}} |

## Requirement breakdown

| Requirement ID and version | Contribution to outcome | Acceptance criterion IDs | Canonical location | State |
| --- | --- | --- | --- | --- |
| {{requirement_id_and_version}} | {{contribution}} | {{criterion_ids}} | {{locator}} | {{actual_state}} |

## Dependencies and proposed sequence

| Dependency ID | Relationship | Required condition | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{dependency_id}} | {{relationship}} | {{condition}} | {{owner_or_unknown}} | {{action}} |

## Completion evidence

| Completion condition | Required evidence | Current evidence |
| --- | --- | --- |
| {{condition}} | {{evidence_requirement}} | {{reference_or_null}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unknowns and risks

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Review and planning decision

- Proposed release: {{release_id_or_unknown}}
- Required review: {{review_scope}}
- Actual decision reference: {{reference_or_null}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "feature-epic"
id: "SAMPLE-EPIC-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CAP-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-NFR-001, SAMPLE-REL-001]
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

# Customer invoice viewing feature

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Context and source facts

- Business problem: The fictional portal needs defined invoice access behavior.
- Primary actors: Customer A and Customer B.
- Current behavior: unknown; no implementation observation exists.
- Evidence limit: The sample supplies proposed intent only.

## Proposed outcome

- User outcome: Customers can view owned invoices; unauthorized customers receive no invoice content.
- Business value: Defined access behavior supports consistent implementation and validation.
- Success measure: Acceptance criteria SAMPLE-AC-001, SAMPLE-AC-002, and SAMPLE-NFR-AC-001; results remain unavailable.

## Scope and exclusions

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| Customer invoice viewing and access denial | Staff access, editing, and payment | The context provides no rules for these behaviors. |

## Requirement breakdown

| Requirement ID and version | Contribution to outcome | Acceptance criterion IDs | Canonical location | State |
| --- | --- | --- | --- | --- |
| SAMPLE-REQ-001; sample-v1 | Defines permitted invoice viewing. | SAMPLE-AC-001 | [Requirement sample](requirement.md) | proposed |
| SAMPLE-REQ-002; sample-v1 | Defines denied invoice access. | SAMPLE-AC-002 | [Sample context](sample-context.md) | proposed |
| SAMPLE-NFR-001; sample-v1 | Defines authorized response performance. | SAMPLE-NFR-AC-001 | [Nonfunctional requirement](nonfunctional-requirement.md) | proposed |

## Dependencies and proposed sequence

| Dependency ID | Relationship | Required condition | Owner | Next action |
| --- | --- | --- | --- | --- |
| SAMPLE-RULE-001 | Supplies access policy. | Record actual business review. | unknown | Identify the invoice policy owner. |
| SAMPLE-CONTRACT-001 | Describes the proposed invoice interface. | Resolve interface details before implementation. | unknown | Review the proposed contract. |
| SAMPLE-TEST-001 | Will assess SAMPLE-AC-001. | Retain code, test, and environment identities. | unknown | Implement and inspect the required assertions. |
| SAMPLE-TEST-002 | Will assess SAMPLE-AC-002. | Retain code, test, and environment identities. | unknown | Implement and inspect the required assertions. |

## Completion evidence

| Completion condition | Required evidence | Current evidence |
| --- | --- | --- |
| Important requirements receive human review. | Actual review for the current content | null |
| Access criteria have assertions and retained results. | Exact revisions and execution observations | null |
| Proposed response target is assessed. | Measurement conditions and retained performance observations | null |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Unknowns and risks

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Implementation and owners are unknown. | The context supplies no implementation revision or responsible owner. | Feature completion cannot be established. | unknown | Identify owners and inspect exact source revisions. |

## Review and planning decision

- Proposed release: SAMPLE-REL-001; no release date exists.
- Required review: Access scope, performance target, and completion evidence.
- Actual decision reference: null.
````

## Completion checks

- State one coherent user or business outcome.
- Map all included behavior to canonical requirement IDs.
- Keep acceptance criterion references consistent with their detailed requirements.
- Give dependencies owners and next actions.
- Define observable completion evidence.
- Keep planned release and actual release status separate.
