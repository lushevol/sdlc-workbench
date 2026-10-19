# Risk and issue register

## Purpose

Track possible adverse events, observed problems, and their resolution evidence.
A risk concerns uncertainty. An issue concerns an observed condition.

## AI instructions

1. Obtain source evidence, affected artifact IDs, impact conditions, responsible owners, and decision limits.
2. Classify each entry as risk or issue using its evidence.
3. Explain likelihood and impact qualitatively unless an approved scoring method exists.
4. Record missing evidence as a limit, not an observed failure.
5. Link each response to an owner, action, trigger, and closure evidence.
6. Do not invent incidents, numerical scores, acceptance decisions, deadlines, or completed mitigations.

## Template

````markdown
---
artifact_kind: "risk-issue-register"
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

# {{register_title}}

## Scope and source facts

- Assessed scope: {{scope_and_artifact_versions}}
- Assessment basis: {{source_scope}}
- Scoring method: {{approved_method_or_qualitative_only}}
- Observation limit: {{coverage_limit}}

## Risk and issue entries

| ID | Type | Finding or uncertain event | Evidence | Consequence | Likelihood and basis | Impact and basis | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{entry_id}} | {{risk_or_issue}} | {{finding}} | {{evidence}} | {{consequence}} | {{likelihood_or_not_applicable}} | {{impact}} | {{owner_or_unknown}} | {{open_or_evidenced_state}} |

## Proposed responses

| Entry ID | Response | Next action | Trigger | Action owner | Target date | Closure condition | Actual closure evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{entry_id}} | {{avoid_reduce_transfer_or_accept_proposal}} | {{action}} | {{trigger}} | {{owner_or_unknown}} | {{date_or_null}} | {{observable_closure_condition}} | {{reference_or_null}} |

## Decisions and residual exposure

| Entry ID | Proposed decision | Actual decision reference | Residual exposure | Review condition |
| --- | --- | --- | --- | --- |
| {{entry_id}} | {{decision_proposal}} | {{reference_or_null}} | {{remaining_consequence}} | {{review_trigger}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unresolved questions

| Question | Evidence limit | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{question}} | {{missing_evidence}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Review control

- Required reviewers: {{roles_or_unknown}}
- Actual review reference: {{reference_or_null}}
- Next review trigger: {{trigger}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "risk-issue-register"
id: "SAMPLE-RISK-REGISTER-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-RISK-001, SAMPLE-ISSUE-001]
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

# Invoice portal risk and issue register

## Scope and source facts

- Assessed scope: Proposed invoice access requirements SAMPLE-REQ-001 and SAMPLE-REQ-002.
- Assessment basis: The illustrative context at sample-v1.
- Scoring method: Qualitative only; no scoring scale is supplied.
- Observation limit: No deployed behavior or execution evidence exists.

## Risk and issue entries

| ID | Type | Finding or uncertain event | Evidence | Consequence | Likelihood and basis | Impact and basis | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-RISK-001 | risk | An implementation could omit the proposed access check. | The context proposes checks but provides no implementation. | Another customer could receive invoice content. | unknown; implementation is unavailable. | Potential confidentiality loss from invoice disclosure. | unknown | open |
| SAMPLE-ISSUE-001 | issue | The policy owner is unidentified in the sample. | The context explicitly marks policy ownership unknown. | Required business review cannot be assigned. | not applicable; this is a documented input gap. | Requirement publication remains blocked. | unknown | open |

## Proposed responses

| Entry ID | Response | Next action | Trigger | Action owner | Target date | Closure condition | Actual closure evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-RISK-001 | reduce | Inspect access checks and denied-access assertions at exact revisions. | Implementation becomes available. | unknown | null | Retained evidence establishes denied content for the assessed cases. | null |
| SAMPLE-ISSUE-001 | reduce | Identify the business owner and obtain the policy source. | Before requirement publication | unknown | null | Record the actual owner and review evidence. | null |

## Decisions and residual exposure

| Entry ID | Proposed decision | Actual decision reference | Residual exposure | Review condition |
| --- | --- | --- | --- | --- |
| SAMPLE-RISK-001 | Require access evidence before release assessment. | null | Unassessed paths can still contain access defects. | New access paths or policy changes |
| SAMPLE-ISSUE-001 | Hold publication until required review exists. | null | Missing authority can leave policy conflicts unresolved. | Owner or source becomes available. |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Unresolved questions

| Question | Evidence limit | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Which roles can accept residual access risk? | No authority record exists. | Risk acceptance cannot be attributed. | unknown | Obtain the project's decision authority record. |

## Review control

- Required reviewers: Invoice policy owner and delivery owner; identities remain unknown.
- Actual review reference: null.
- Next review trigger: Owner identification, implementation evidence, or a policy change.
````

## Completion checks

- Classify uncertain events as risks and observed conditions as issues.
- Give each entry evidence, consequence, owner, and next action.
- State the basis for every likelihood or impact rating.
- Do not invent numeric scores without an approved method.
- Give each response an observable closure condition.
- Close entries only with retained evidence and the required decision.
