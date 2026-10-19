# Test data and environment specification

## Purpose

Define reproducible test fixtures, environment needs, isolation, setup, and cleanup.

## AI instructions

1. Required inputs: test IDs, scenario conditions, ownership rules, dependency identities, and environment constraints.
2. Required inputs: authorized setup procedures, cleanup procedures, access controls, and data retention decisions.
3. Separate proposed configuration from observed environment facts.
4. Use fictional or authorized data. Never include secrets in this document.
5. Record deployed revisions and configuration evidence only after inspection.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "test-data-environment"
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

# {{specification_title}}

## Intended tests and scope

- Test IDs: {{test_ids}}
- Required behaviors: {{requirement_and_criterion_ids}}
- Environment purpose: {{purpose}}
- Data classification and authorization: {{classification_and_authorization_evidence}}

## Fixture specification

| Fixture ID | Entity | Required attributes | Relationship | Scenario use | Source |
| --- | --- | --- | --- | --- | --- |
| {{fixture_id}} | {{entity}} | {{attributes_without_secrets}} | {{declared_relationship}} | {{test_id_and_condition}} | {{source_ref}} |

## Environment specification

| Component identity | Required configuration | Observed identity | Exact revision | Evidence |
| --- | --- | --- | --- | --- |
| {{component_id}} | {{configuration_or_source_locator}} | null | null | null |

## Setup, isolation, and cleanup

| Phase | Procedure locator | Authorization | Observable completion condition | Status |
| --- | --- | --- | --- | --- |
| Setup | {{procedure_locator}} | {{authorization_ref_or_null}} | {{measurable_ready_condition}} | NOT_RUN |
| Isolation | {{procedure_locator}} | {{authorization_ref_or_null}} | {{observable_isolation_condition}} | NOT_RUN |
| Cleanup | {{procedure_locator}} | {{authorization_ref_or_null}} | {{measurable_cleanup_condition}} | NOT_RUN |

## Retention and access

- Permitted data users: {{roles_and_source}}
- Secret references: {{secret_reference_locations_without_values}}
- Retention period: {{duration_and_approved_source_or_unknown}}
- Evidence storage: {{location_and_access_controls}}
- Setup result: null
- Cleanup result: null

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
artifact_kind: "test-data-environment"
id: "SAMPLE-ENV-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-TEST-001, SAMPLE-TEST-002, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-SVC-001]
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

# Invoice access test fixtures

## Intended tests and scope

- Test IDs: SAMPLE-TEST-001 and SAMPLE-TEST-002.
- Required behaviors: SAMPLE-REQ-001/SAMPLE-AC-001 and SAMPLE-REQ-002/SAMPLE-AC-002.
- Environment purpose: Exercise the two proposed invoice access examples.
- Data classification and authorization: Fictional data only. Actual environment authorization is null.

## Fixture specification

| Fixture ID | Entity | Required attributes | Relationship | Scenario use | Source |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-FIXTURE-001 | Customer A | Authenticated | Owns INV-001 | SAMPLE-TEST-001 permitted access | SAMPLE-SRC-001 |
| SAMPLE-FIXTURE-002 | Customer B | Authenticated | No permission for INV-001 | SAMPLE-TEST-002 denied access | SAMPLE-SRC-001 |
| SAMPLE-FIXTURE-003 | Invoice INV-001 | Identifier INV-001 | Owned by customer A | Both access tests | SAMPLE-SRC-001 |

## Environment specification

| Component identity | Required configuration | Observed identity | Exact revision | Evidence |
| --- | --- | --- | --- | --- |
| SAMPLE-SVC-001 | Proposed isolated invoice service | null | null | null |
| SAMPLE-REPO-001 | Implementation repository remains unknown | null | null | null |

## Setup, isolation, and cleanup

| Phase | Procedure locator | Authorization | Observable completion condition | Status |
| --- | --- | --- | --- | --- |
| Setup | unknown | null | Both customer states and the ownership relation match the fixture table | NOT_RUN |
| Isolation | unknown | null | The environment separates the fictional fixture from customer data | NOT_RUN |
| Cleanup | unknown | null | The three sample fixtures no longer exist after cleanup | NOT_RUN |

## Retention and access

- Permitted data users: unknown. No access policy is supplied.
- Secret references: unknown. No secrets are supplied.
- Retention period: unknown. The context identifies retention as unresolved.
- Evidence storage: unknown. No retained execution exists.
- Setup result: null
- Cleanup result: null

## Facts, inferences, and unresolved questions

- Facts: Customer A owns INV-001. Customer B lacks permission for INV-001.
- Inferences: An isolated fixture could support both proposed tests.
- Unresolved questions: Environment ownership, access controls, setup, cleanup, and retention remain unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | The fixture specification cannot establish execution readiness | unknown | Identify the environment owner and obtain authorized procedures |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Fixture attributes and relationships support specific test conditions.
- Proposed configuration and observed configuration occupy separate fields.
- Setup and cleanup have measurable completion conditions.
- Access, retention, and isolation decisions cite sources or remain unresolved.
- The document contains no secret values.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
