# Use case / user journey

## Purpose

Describe an actor's goal through preconditions, actions, alternatives, and observable outcomes.
Link policy and acceptance criteria instead of inventing missing behavior.

## AI instructions

1. Obtain actors, goals, triggers, system boundary, policy rules, requirements, and interface context.
2. Describe actor actions separately from system responses.
3. Give each alternative an exact branch condition and outcome.
4. Reference measurable acceptance criteria for the main and rejected flows.
5. Mark missing recovery, authentication, and role rules as unresolved questions.
6. Do not invent UI controls, permissions, deployed behavior, or successful execution.

## Template

````markdown
---
artifact_kind: "use-case"
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

# {{use_case_title}}

## Context and source facts

- Primary actor: {{primary_actor}}
- Supporting actors: {{supporting_actors_or_none}}
- Actor goal: {{goal}}
- System boundary: {{boundary}}
- Evidence limit: {{limit}}

## Proposed flow conditions

- Trigger: {{actor_or_external_trigger}}
- Preconditions: {{conditions_before_flow}}
- Success postconditions: {{observable_success_state}}
- Failure guarantees: {{observable_failure_state}}

## Main flow

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| {{step_number}} | {{action}} | {{response}} | {{ids}} | {{expected_observation}} |

## Alternative and exception flows

| Flow ID | Branch from step | Condition | Action and response | Outcome | Criterion IDs |
| --- | --- | --- | --- | --- | --- |
| {{flow_id}} | {{step_number}} | {{branch_condition}} | {{actions_and_responses}} | {{observable_outcome}} | {{criterion_ids_or_gap}} |

## Related artifacts

| Artifact ID | Relationship | Location |
| --- | --- | --- |
| {{artifact_id}} | {{relationship}} | {{locator}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unknowns and risks

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Review and execution status

- Required review scope: {{actors_flows_and_outcomes}}
- Actual review reference: {{reference_or_null}}
- Execution status: {{NOT_RUN_or_evidenced_status}}
- Execution evidence: {{reference_or_null}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "use-case"
id: "SAMPLE-USE-CASE-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-RULE-001, SAMPLE-RULE-002, SAMPLE-RULE-003]
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

# View a customer invoice

## Context and source facts

- Primary actor: An authenticated customer.
- Supporting actors: none defined; proposed internal service dependencies are outside the actor boundary.
- Actor goal: View an owned invoice.
- System boundary: The fictional invoice portal and proposed invoice service.
- Evidence limit: This describes proposed behavior, with no implemented UI or runtime observation.

## Proposed flow conditions

- Trigger: The customer requests an invoice by identifier.
- Preconditions: Customer A is authenticated and owns invoice INV-001 for the main flow.
- Success postconditions: The response contains exactly one invoice identified as INV-001.
- Failure guarantees: Denied access returns zero invoices and the message "Access denied".

## Main flow

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Customer A requests INV-001. | Evaluate identity and invoice access. | SAMPLE-RULE-001 | Access evaluation is required; internal evidence remains undefined. |
| 2 | No additional action is required. | Return the owned invoice. | SAMPLE-REQ-001 | Exactly one invoice with identifier INV-001, as SAMPLE-AC-001 specifies. |

## Alternative and exception flows

| Flow ID | Branch from step | Condition | Action and response | Outcome | Criterion IDs |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-ALT-001 | 1 | Customer B has no permission for INV-001. | Deny the request and omit invoice content. | Zero invoices and "Access denied" | SAMPLE-AC-002 |
| SAMPLE-ALT-002 | 1 | The requester is unauthenticated. | unknown; the context defines no authentication response. | unknown | gap |
| SAMPLE-ALT-003 | 1 | The invoice does not exist. | unknown; the context defines no missing-invoice rule. | unknown | gap |

## Related artifacts

| Artifact ID | Relationship | Location |
| --- | --- | --- |
| SAMPLE-REQ-001 | Defines main-flow acceptance. | [Requirement sample](requirement.md) |
| SAMPLE-REQ-002 | Defines denied-flow acceptance. | [Sample context](sample-context.md) |
| SAMPLE-RULE-001 | Supplies the ownership condition. | [Business rule](business-rule.md) |
| SAMPLE-CONTRACT-001 | Describes the proposed interface. | [Interface contract](interface-contract.md) |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Unknowns and risks

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Missing-invoice and authentication responses are undefined. | The context provides no corresponding rules. | These flows cannot have justified outcomes. | unknown | Obtain the rules before implementing their responses. |
| UI interaction details are unavailable. | The context defines requests but no screen. | A UI journey cannot identify controls. | unknown | Obtain the proposed UI specification. |

## Review and execution status

- Required review scope: Actors, access conditions, flow outcomes, and exception gaps.
- Actual review reference: null.
- Execution status: NOT_RUN.
- Execution evidence: null.
````

## Completion checks

- State an actor goal, trigger, system boundary, and preconditions.
- Separate actor actions from system responses.
- Give alternatives exact branch conditions and observable outcomes.
- Link defined outcomes to acceptance criterion IDs.
- Record undefined exceptions as gaps.
- Keep proposed flows separate from observed execution.
