# Defect report

## Purpose

Describe a reproducible behavioral difference with evidence, impact, ownership, and a resolution plan.

## AI instructions

1. Required inputs: expected behavior source, reproduction conditions, actual observations, and retained evidence.
2. Required inputs: exact code revision, environment identity, affected criteria, and affected users when known.
3. Label hypothetical reproductions clearly. Do not classify them as confirmed defects.
4. Keep suspected cause separate from observed behavior.
5. A confirmed defect requires a regression that asserts the corrected behavior.
6. Assign severity from supported impact evidence and applicable classification rules.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "defect-report"
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

# {{defect_title}}

## Classification and scope

- Defect ID: {{defect_id}}
- Confirmation: {{hypothetical_or_suspected_or_confirmed_with_evidence}}
- Requirement / criterion: {{requirement_id_and_criterion_id}}
- Affected users: {{affected_population_or_unknown}}
- Severity: {{classification_and_evidence_or_unassessed}}
- Priority: {{priority_and_decision_source_or_unassessed}}

## Reproduction conditions

```yaml
repository_id: "{{repository_id}}"
repository_revision: null
test_revision: null
environment_identity: null
reproduction_status: NOT_RUN
execution_id: null
actual_results: null
retained_execution_refs: []
```

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| {{step_number}} | {{condition_or_action}} | {{source_supported_result}} | null |

## Hypothesis and impact

- Hypothetical mismatch: {{hypothetical_result_or_not_applicable}}
- Observed impact: {{retained_evidence_or_none}}
- Suspected cause: {{hypothesis_and_basis_or_unknown}}
- Evidence limits: {{unobserved_conditions_or_missing_evidence}}

## Resolution and regression

- Proposed investigation: {{next_evidence_to_collect}}
- Fix scope: {{inspected_affected_interfaces_or_unknown}}
- Regression test: {{test_id_and_required_assertion_or_pending}}
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

## Facts, inferences, and unresolved questions

- Facts: {{source_supported_facts}}
- Inferences: {{inferences_and_basis_or_none}}
- Unresolved questions: {{questions_and_resolution_owner}}

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| {{evidence_or_explicit_gap}} | {{consequence}} | unknown | {{specific_next_action}} |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_evidence_limits}} |
````

## Illustrative sample

This sample describes proposed invoice portal work.
It records no actual approval or execution.

````markdown
---
artifact_kind: "defect-report"
id: "SAMPLE-DEFECT-001"
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

## Classification and scope

- Defect ID: SAMPLE-DEFECT-001.
- Confirmation: Hypothetical reproduction. No defect is confirmed.
- Requirement / criterion: SAMPLE-REQ-002 / SAMPLE-AC-002.
- Affected users: unknown. No actual users or system observations exist.
- Severity: unassessed. No observed impact or severity policy exists.
- Priority: unassessed. No prioritization decision exists.

## Reproduction conditions

```yaml
repository_id: SAMPLE-REPO-001
repository_revision: null
test_revision: null
environment_identity: null
reproduction_status: NOT_RUN
execution_id: null
actual_results: null
retained_execution_refs: []
```

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| 1 | Authenticate customer B with no permission for INV-001 | Fixture matches the denied access condition | null |
| 2 | Customer B requests INV-001 | Response contains zero invoices and message "Access denied" | null |

## Hypothesis and impact

- Hypothetical mismatch: A denied response could contain invoice content. This possibility has not been observed.
- Observed impact: None. No retained execution evidence exists.
- Suspected cause: unknown. No implementation revision has been inspected.
- Evidence limits: This example supplies a reproduction design without an actual result.

## Resolution and regression

- Proposed investigation: Execute SAMPLE-TEST-002 after inspecting exact implementation and assertion revisions.
- Fix scope: unknown. No confirmed defect or inspected implementation exists.
- Regression test: SAMPLE-TEST-002 should assert zero invoices and the denial message if the defect is confirmed.
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

## Facts, inferences, and unresolved questions

- Facts: SAMPLE-AC-002 expects zero invoices and the message "Access denied".
- Inferences: Returned invoice content would contradict the proposed criterion.
- Unresolved questions: Actual behavior, impact, cause, and the responsible owner are unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | The hypothetical mismatch cannot establish a confirmed defect | unknown | Inspect the assertions and retain a reproduction result |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- The report distinguishes hypothetical, suspected, and confirmed behavior.
- Expected behavior cites a requirement or authoritative source.
- Observed results cite retained evidence at an exact revision.
- Cause, severity, and impact claims state their evidence limits.
- A confirmed defect has a regression plan and retest evidence.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
