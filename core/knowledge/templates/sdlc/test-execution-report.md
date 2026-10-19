# Test execution and verification report

## Purpose

Record actual test evidence and state the exact behaviors that the evidence supports.

## AI instructions

1. Required inputs: test definitions, requirement IDs, criterion IDs, inspected assertions, and exact code and test revisions.
2. Required inputs: execution identity, environment identity, timestamps, retained results, and available evidence hashes.
3. Use NOT_RUN when no execution exists. Keep actual results and timestamps null.
4. Inspect assertion contents and retained execution before claiming behavior verification.
5. A passing command alone does not prove that a criterion passed.
6. Report evidence limits beside the verification claim.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "test-execution-report"
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

# {{execution_report_title}}

## Run identity and provenance

```yaml
execution_id: null
execution_status: NOT_RUN
repository_id: "{{repository_id}}"
repository_revision: null
test_revision: null
environment_identity: null
started_at: null
completed_at: null
command_or_tool_reference: "{{authorized_run_instruction_locator}}"
process_exit_status: null
actual_results: null
retained_execution_refs: []
```

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion location | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {{test_id}} | {{requirement_id}} / {{criterion_id}} | {{file_line_revision_or_null}} | {{measurable_expected_result}} | null | NOT_RUN | null |

## Retained evidence inventory

| Evidence ID | Locator | Hash | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| {{evidence_id_or_null}} | {{locator_or_null}} | {{hash_or_null}} | {{execution_id_or_null}} | {{limit}} |

## Verification conclusion

- Behavior claim: {{evidence_supported_claim_or_no_verification}}
- Covered conditions: {{conditions_supported_by_evidence}}
- Uncovered conditions: {{conditions_without_evidence}}
- Evidence limits: {{missing_revisions_or_assertions_or_results}}

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
artifact_kind: "test-execution-report"
id: "SAMPLE-REPORT-EXEC-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-TEST-001, SAMPLE-TEST-002, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-ENV-001]
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

# Invoice access execution report

## Run identity and provenance

```yaml
execution_id: null
execution_status: NOT_RUN
repository_id: SAMPLE-REPO-001
repository_revision: null
test_revision: null
environment_identity: null
started_at: null
completed_at: null
command_or_tool_reference: unknown
process_exit_status: null
actual_results: null
retained_execution_refs: []
```

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion location | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-TEST-001 | SAMPLE-REQ-001 / SAMPLE-AC-001 | null | Exactly one invoice with identifier INV-001 | null | NOT_RUN | null |
| SAMPLE-TEST-002 | SAMPLE-REQ-002 / SAMPLE-AC-002 | null | Zero invoices and message "Access denied" | null | NOT_RUN | null |

## Retained evidence inventory

| Evidence ID | Locator | Hash | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| null | null | null | null | No execution evidence exists |

## Verification conclusion

- Behavior claim: No business behavior is verified.
- Covered conditions: None. Both access tests remain NOT_RUN.
- Uncovered conditions: Permitted access, denied access, and runtime boundaries lack execution evidence.
- Evidence limits: Repository revision, test revision, assertion locations, environment identity, and retained results are null.

## Facts, inferences, and unresolved questions

- Facts: The sample context states that no test has executed.
- Inferences: None. Expected results do not establish actual behavior.
- Unresolved questions: The implementation, assertion code, and execution owner are unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | The report cannot support release acceptance | unknown | Inspect exact code and assertion revisions, then retain an authorized run |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Run metadata identifies exact code and test revisions, environment, and execution when available.
- Expected results and actual results occupy separate fields.
- Each verification claim cites inspected assertions and retained execution.
- Exit status, test outcome, and behavior verification remain separate.
- Missing evidence limits each associated claim.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
