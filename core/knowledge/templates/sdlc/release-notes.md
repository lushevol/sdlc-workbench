# Release notes

## Purpose

Describe a release scope, user-visible changes, compatibility, and known limits with supporting evidence.

## AI instructions

1. Required inputs: release identity, exact artifact revisions, approved change scope, and intended audience.
2. Required inputs: verified change evidence, compatibility assessments, unresolved defects, and operational instructions.
3. Distinguish proposed changes from released behavior.
4. Do not describe a hypothetical defect as a shipped fix.
5. Keep publication and deployment details null until actual records exist.
6. Link each behavior claim to supporting requirements and retained verification evidence.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "release-notes"
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

# {{release_title}}

## Release identity and audience

```yaml
release_id: "{{release_id}}"
release_version: null
repository_revision: null
artifact_identity: null
deployment_identity: null
release_date: null
publication_state: pending
published_at: null
publication_approval: null
```

- Audience: {{intended_users_or_operators}}
- Scope state: {{proposed_or_released_with_evidence}}

## Features and changes

| Change | User-visible behavior | Requirement IDs | Verification evidence | Availability |
| --- | --- | --- | --- | --- |
| {{change_title}} | {{source_supported_behavior}} | {{requirement_ids}} | {{retained_evidence_or_null}} | {{proposed_or_observed_availability}} |

## Fixes

| Defect ID | Corrected behavior | Exact fix revision | Regression evidence | Limit |
| --- | --- | --- | --- | --- |
| {{confirmed_defect_id_or_none}} | {{verified_correction_or_none}} | null | null | {{evidence_limit}} |

## Compatibility and operator actions

- Interface changes: {{contract_changes_and_evidence_or_unknown}}
- Data changes: {{migration_requirements_and_evidence_or_unknown}}
- Required user action: {{action_and_source_or_unknown}}
- Deployment and recovery: {{reviewed_plan_locator_or_unknown}}
- Support owner: unknown

## Known issues and limits

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| {{issue_evidence_or_explicit_gap}} | {{user_or_operator_impact}} | unknown | {{specific_next_action}} |

## Verification summary

```yaml
execution_status: NOT_RUN
test_revision: null
actual_results: null
retained_execution_refs: []
```

- Claim limits: {{limits_on_release_behavior_claims}}

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
artifact_kind: "release-notes"
id: "SAMPLE-NOTES-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REL-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-DEPLOY-001, SAMPLE-DEFECT-001]
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

# Proposed invoice portal release notes

## Release identity and audience

```yaml
release_id: SAMPLE-REL-001
release_version: null
repository_revision: null
artifact_identity: null
deployment_identity: null
release_date: null
publication_state: pending
published_at: null
publication_approval: null
```

- Audience: Customers and invoice portal operators.
- Scope state: Proposed. No released behavior is established.

## Features and changes

| Change | User-visible behavior | Requirement IDs | Verification evidence | Availability |
| --- | --- | --- | --- | --- |
| Owned invoice viewing | Customer A receives one invoice with identifier INV-001 | SAMPLE-REQ-001 | null | Proposed only |
| Denied invoice viewing | Customer B receives zero invoices and message "Access denied" | SAMPLE-REQ-002 | null | Proposed only |

## Fixes

| Defect ID | Corrected behavior | Exact fix revision | Regression evidence | Limit |
| --- | --- | --- | --- | --- |
| None confirmed | None established | null | null | SAMPLE-DEFECT-001 describes a hypothetical reproduction only |

## Compatibility and operator actions

- Interface changes: SAMPLE-CONTRACT-001 proposes GET /invoices/{invoice_id}. Compatibility remains unassessed.
- Data changes: unknown. No migration specification exists.
- Required user action: unknown. No actual release or supported procedure exists.
- Deployment and recovery: SAMPLE-DEPLOY-001 in deployment-rollback.md remains draft.
- Support owner: unknown

## Known issues and limits

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| No reviewed artifact identity or compatibility evidence exists | User and operator impact remains unknown | unknown | Inspect the exact artifact and assess interface compatibility |

## Verification summary

```yaml
execution_status: NOT_RUN
test_revision: null
actual_results: null
retained_execution_refs: []
```

- Claim limits: Features describe proposed intent. No deployment, passing business execution, or publication has occurred.

## Facts, inferences, and unresolved questions

- Facts: SAMPLE-REL-001 remains proposed, and the context supplies no actual released artifact.
- Inferences: The two access requirements could provide future release note entries.
- Unresolved questions: Actual version, compatibility, support owner, and publication decision remain unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | The draft cannot establish released behavior | unknown | Inspect exact release evidence before publishing behavior claims |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Release identity and publication state match actual records.
- Feature claims cite requirements and retained verification evidence.
- Fixes cite confirmed defects, exact revisions, and regression evidence.
- Compatibility and required actions state evidence limits.
- Proposed behavior remains distinct from deployed availability.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
