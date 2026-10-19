# Retirement / decommission plan

## Purpose

Define dependency removal, data handling, and measurable retirement completion.

Read the [AI authoring contract](README.md) before use.
Read the [sample context](sample-context.md) before interpreting the example.

## AI instructions

- Inspect consumers, contracts, deployments, data obligations, and responsible owners.
- Obtain applicable retention and disposal decisions before destructive actions.
- Define a reversible migration stage and its validation.
- Name the last reversible point and recovery limit.
- Require actual authorization before irreversible removal.

## Template

Copy this block. Replace placeholders and retain the required sections.

````markdown
---
artifact_kind: retirement-plan
id: "{{artifact_id}}"
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

# {{retirement_title}}

## Scope and reason

{{retired_service_contract_data_and_business_reason}}

## Dependency inventory

| Resource ID | Consumer or provider | Relationship | Evidence state | Exact evidence | Coverage limit | Migration owner |
| --- | --- | --- | --- | --- | --- | --- |
| {{resource_id}} | {{related_resource_id}} | {{relationship}} | {{proposed_declared_static_or_runtime}} | {{revision_and_locator}} | {{coverage_limit}} | unknown |

## Data disposition

| Data set | Retention authority | Required period | Migration or disposal action | Verification |
| --- | --- | --- | --- | --- |
| {{dataset}} | {{approved_source_or_unknown}} | {{period_or_unknown}} | {{authorized_action}} | {{observable_check}} |

## Migration and removal stages

| Stage | Preconditions | Action | Stop condition | Completion evidence |
| --- | --- | --- | --- | --- |
| {{stage}} | {{conditions}} | {{action}} | {{condition}} | {{evidence}} |

## Recovery and authorization

{{last_reversible_point_recovery_procedure_actual_authorization_reference_and_decision_owner}}

## Completion criteria

```gherkin
Feature: {{retirement_scope}}

Scenario: {{retirement_completion}}
  Given {{approved_dependencies_and_data_obligations}}
  When {{authorized_retirement_stage_finishes}}
  Then {{observable_result_with_required_limit}}
```

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| {{source_id}} | {{locator}} | {{revision_or_null}} | {{hash_or_null}} | {{actual_owner_and_authority_or_unknown}} | {{evidence_limit}} |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| {{fact_inference_or_unknown}} | {{statement}} | {{source_or_missing_evidence}} | {{effect}} | unknown | {{action}} |
````

## Illustrative sample

This sample is fictional. It records no actual approval or execution.

````markdown
---
artifact_kind: retirement-plan
id: "SAMPLE-RETIREMENT-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
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

# Proposed invoice portal retirement assessment

## Scope and reason

Assess possible retirement of SAMPLE-SVC-001.
No business retirement decision exists.

## Dependency inventory

| Resource ID | Consumer or provider | Relationship | Evidence state | Exact evidence | Coverage limit | Migration owner |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-SVC-001 | Invoice portal | Invoice request interface. | proposed | SAMPLE-SRC-001 at sample-v1; no runtime evidence. | Actual consumer coverage is unknown. | unknown |

## Data disposition

| Data set | Retention authority | Required period | Migration or disposal action | Verification |
| --- | --- | --- | --- | --- |
| Customer invoices | unknown | unknown | null; authorization and obligations are missing. | Compare approved retention obligations with actual retained data. |

## Migration and removal stages

| Stage | Preconditions | Action | Stop condition | Completion evidence |
| --- | --- | --- | --- | --- |
| Dependency assessment | Authorized read access to exact source revisions. | Inventory consumers and record coverage limits. | Missing scope or source access. | Reviewed consumer inventory; currently null. |
| Removal | Actual retirement decision and data disposition approval. | null; no removal is authorized. | Any unresolved consumer or retention obligation. | Actual completion evidence; currently null. |

## Recovery and authorization

The recovery procedure and last reversible point remain unknown.
No removal, migration, or disposal occurred.
Execution status is NOT_RUN.

## Completion criteria

```gherkin
Feature: Assess invoice portal retirement

Scenario: Assess dependencies before proposing removal
  Given the consumer inventory has unresolved entries
  When an agent prepares a retirement recommendation
  Then the recommendation lists every unresolved entry
  And it records zero completed removal actions
```

This criterion describes the sample assessment only.
Actual retirement criteria require approved scope and obligations.

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only. | No actual retirement decision, consumer coverage, or retention authority. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Unknown | Invoice retention obligations are unavailable. | Applicable retention decision is missing. | Disposal cannot be specified. | unknown | Obtain the applicable decision. |
| Unknown | Current consumers are unconfirmed. | Exact source and runtime observations are missing. | Removal could interrupt an unknown consumer. | unknown | Inspect consumers before selecting retirement stages. |
````

## Completion checks

- The scope names every resource considered for retirement.
- Dependency claims include source revisions and coverage limits.
- Data actions follow recorded retention authority.
- Irreversible steps have actual authorization and stop conditions.
- Completion uses observable checks and retained evidence.
