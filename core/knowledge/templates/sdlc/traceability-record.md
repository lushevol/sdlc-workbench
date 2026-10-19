# Requirements traceability record

## Purpose

Trace declared requirements through criteria, inspected assertions, and retained execution evidence.

## AI instructions

1. Required inputs: requirement records, acceptance criteria, related design IDs, and source revisions.
2. Required inputs: repository identities, exact inspected code and test revisions, assertion locations, and retained execution records.
3. Record many-to-many links as separate relationship rows with supporting evidence.
4. Separate a declared test mapping from an inspected assertion mapping.
5. Separate knowledge review from passing behavior evidence.
6. Do not infer runtime coverage from names, imports, metadata, or passing command status.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "traceability-record"
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

# {{traceability_title}}

## Scope and identities

- Capability IDs: {{capability_ids}}
- Requirement IDs: {{requirement_ids}}
- Repository IDs: {{repository_ids}}
- Service and contract IDs: {{service_ids_and_contract_ids}}
- Scope limit: {{included_behavior_and_exclusions}}

## Requirement and criterion declarations

| Requirement ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| {{requirement_id}} | {{criterion_id}} | {{conditions_action_result_and_limit}} | {{revision_or_null}} | pending |

## Relationship evidence

| From ID | Relationship | To ID | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| {{requirement_id}} | has criterion | {{criterion_id}} | {{source_ref}} | declaration | {{limit}} |
| {{criterion_id}} | proposed test coverage | {{test_id}} | {{test_definition_ref}} | proposed mapping | {{limit}} |
| {{test_id}} | asserts through | {{assertion_id_or_null}} | {{inspected_assertion_ref_or_null}} | {{inspection_state}} | {{limit}} |

## Inspected implementation and assertions

| Criterion ID | Repository ID | Code revision | Code location | Test ID | Test revision | Assertion ID and location | Assertion contents |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{criterion_id}} | {{repository_id}} | null | null | {{test_id}} | null | null | {{assertion_summary_or_unknown}} |

## Retained execution and verification

| Criterion ID | Assertion ID | Execution ID | Exact tested revision | Actual result | Execution status | Retained evidence | Verification claim and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{criterion_id}} | null | null | null | null | NOT_RUN | null | {{claim_supported_by_inspection_and_execution_or_unverified}} |

## Coverage gaps

| Missing link | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{missing_relationship_or_execution}} | {{evidence_or_gap}} | {{coverage_limit}} | unknown | {{specific_next_action}} |

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
artifact_kind: "traceability-record"
id: "SAMPLE-TRACE-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CAP-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-AC-001, SAMPLE-AC-002, SAMPLE-TEST-001, SAMPLE-TEST-002, SAMPLE-REPO-001, SAMPLE-SVC-001, SAMPLE-CONTRACT-001]
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

# Invoice access traceability

## Scope and identities

- Capability IDs: SAMPLE-CAP-001.
- Requirement IDs: SAMPLE-REQ-001 and SAMPLE-REQ-002.
- Repository IDs: SAMPLE-REPO-001.
- Service and contract IDs: SAMPLE-SVC-001 and SAMPLE-CONTRACT-001.
- Scope limit: Two proposed customer access examples. Staff access remains unresolved.

## Requirement and criterion declarations

| Requirement ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 | SAMPLE-AC-001 | Customer A requests owned INV-001; response contains exactly one invoice with identifier INV-001 | sample-v1 | pending |
| SAMPLE-REQ-002 | SAMPLE-AC-002 | Customer B requests INV-001 without permission; response contains zero invoices and message "Access denied" | sample-v1 | pending |

## Relationship evidence

| From ID | Relationship | To ID | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 | has criterion | SAMPLE-AC-001 | SAMPLE-SRC-001#proposed-behavior | declaration | Illustrative intent only |
| SAMPLE-REQ-002 | has criterion | SAMPLE-AC-002 | SAMPLE-SRC-001#proposed-behavior | declaration | Illustrative intent only |
| SAMPLE-AC-001 | proposed test coverage | SAMPLE-TEST-001 | SAMPLE-SRC-001#verification-and-release | proposed mapping | No inspected assertion |
| SAMPLE-AC-002 | proposed test coverage | SAMPLE-TEST-002 | SAMPLE-SRC-001#verification-and-release | proposed mapping | No inspected assertion |
| SAMPLE-TEST-001 | asserts through | null | null | Not inspected | No assertion code exists in this context |
| SAMPLE-TEST-002 | asserts through | null | null | Not inspected | No assertion code exists in this context |

## Inspected implementation and assertions

| Criterion ID | Repository ID | Code revision | Code location | Test ID | Test revision | Assertion ID and location | Assertion contents |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-AC-001 | SAMPLE-REPO-001 | null | null | SAMPLE-TEST-001 | null | null | unknown |
| SAMPLE-AC-002 | SAMPLE-REPO-001 | null | null | SAMPLE-TEST-002 | null | null | unknown |

## Retained execution and verification

| Criterion ID | Assertion ID | Execution ID | Exact tested revision | Actual result | Execution status | Retained evidence | Verification claim and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-AC-001 | null | null | null | null | NOT_RUN | null | Unverified; no inspected assertion or retained run |
| SAMPLE-AC-002 | null | null | null | null | NOT_RUN | null | Unverified; no inspected assertion or retained run |

## Coverage gaps

| Missing link | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Criteria to executable assertions | Assertion locations and test revisions are null | Planned coverage does not establish implemented coverage | unknown | Inspect assertions at an exact test revision |
| Assertions to retained execution | Execution status is NOT_RUN | Behavior remains unverified | unknown | Retain an authorized execution with exact tested revisions |

## Facts, inferences, and unresolved questions

- Facts: The context declares two requirement-to-criterion links and two proposed criterion-to-test links.
- Inferences: None. Declared links do not establish implementation or execution.
- Unresolved questions: Code locations, assertion locations, test revisions, and execution owners remain unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | The traceability record cannot establish verified behavior | unknown | Inspect exact source revisions and retain assertion execution evidence |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Requirement, criterion, test, assertion, and execution identities remain distinct.
- Each relationship has evidence and a stated evidence class.
- Code inspection records exact revisions and assertion contents.
- Verification claims cite retained execution for the inspected assertions.
- Knowledge approval and behavior execution appear in separate fields.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
