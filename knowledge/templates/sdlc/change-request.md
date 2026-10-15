# Change request

## Purpose

Describe a proposed baseline change and its affected engineering artifacts.
Keep the requested decision separate from actual authorization and implementation.

## AI instructions

1. Obtain the current baseline, proposed difference, rationale, requester evidence, and affected artifact IDs.
2. Inspect referenced revisions before claiming impact on code or interfaces.
3. Show before and after behavior without rewriting canonical rules silently.
4. Identify requirement, test, data, release, and operational effects.
5. Keep estimates and impact inferences explicit until evidence confirms them.
6. Do not invent requester identity, approval, effort, deadlines, implementation, or execution results.

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

## Proposed change

| Aspect | Current baseline | Proposed replacement or addition | Basis |
| --- | --- | --- | --- |
| {{aspect}} | {{current_behavior_or_unknown}} | {{proposed_behavior}} | {{source_or_explicit_proposal}} |

## Scope and affected artifacts

| Artifact ID | Exact version or revision | Proposed effect | Evidence | Risk and basis | Owner |
| --- | --- | --- | --- | --- | --- |
| {{artifact_id}} | {{version_or_null}} | {{effect}} | {{evidence_or_missing_input}} | {{qualitative_risk_and_basis}} | {{owner_or_unknown}} |

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

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unknowns and blockers

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Requested decision and actual disposition

- Requested decision: {{decision_request}}
- Authorized decision owner: {{owner_with_authority_evidence_or_unknown}}
- Actual decision: {{pending_or_evidenced_decision}}
- Actual decision reference: {{reference_or_null}}
- Implementation status: {{proposed_or_evidenced_status}}
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

- Identify the exact baseline or state that it is unavailable.
- Describe the proposed difference without silently changing canonical rules.
- Inspect exact revisions before claiming implementation impact.
- Separate facts, impact inferences, and estimates.
- Define validation for every changed acceptance criterion.
- Record actual authorization before treating the request as approved.
- Preserve earlier versions and real governance audit events.
