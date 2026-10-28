# System architecture and technical design

## Purpose

Describe system responsibilities, boundaries, interfaces, and proposed engineering decisions.
Use this artifact to assess requirement coverage and change impact.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: requirement IDs, constraints, component identities, interface sources, repository revisions, and current architecture evidence.

Identify the design scope before proposing components.
Label each relationship `proposed`, `declared`, `statically evidenced`, or `runtime observed`.
A runtime claim requires retained observations and an identified environment.
Describe successful, denied, and failed paths through the same boundaries.
Trace design controls to measurable requirements and planned assertions.
Do not identify repository declarations as deployed services.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "system-design"
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

# {{system_name}} design

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Scope and drivers

| Field | Value |
| --- | --- |
| Design state | {{proposed_or_current_with_evidence}} |
| Problem and outcome | {{problem_and_observable_outcome}} |
| Included behavior | {{requirements_and_capability_ids}} |
| Exclusions | {{excluded_behavior_and_reason}} |
| Constraints | {{technical_business_and_regulatory_constraints_with_sources}} |
| Current revision | {{design_revision_and_repository_commit_or_null}} |

## Components and boundaries

| Component ID | Resource kind | Responsibility | Owner | Source revision and locator |
| --- | --- | --- | --- | --- |
| {{component_id}} | {{service_repository_ui_or_store}} | {{single_responsibility}} | {{owner_or_unknown}} | {{evidence_or_null}} |

## Relationships and interfaces

| Consumer ID | Provider ID | Contract ID | Relationship state | Evidence and limits |
| --- | --- | --- | --- | --- |
| {{consumer_id}} | {{provider_id}} | {{contract_id}} | {{proposed_declared_static_or_observed}} | {{evidence_revision_environment_and_limits}} |

## Request and failure paths

| Path | Ordered actions | Observable result | Requirement or unresolved question |
| --- | --- | --- | --- |
| Permitted | {{identity_access_and_data_actions}} | {{permitted_result}} | {{requirement_id}} |
| Denied | {{denied_actions_and_stop_point}} | {{denied_result_and_data_exclusion}} | {{requirement_id}} |
| Dependency failure | {{timeout_or_failure_actions}} | {{failure_result_and_recovery}} | {{requirement_id_or_open_question}} |

## Data and quality controls

| Concern | Proposed control | Target and conditions | Verification evidence |
| --- | --- | --- | --- |
| Data protection | {{classification_access_retention_and_logging_controls}} | {{approved_limits_or_unknown}} | {{assertion_and_execution_ref_or_NOT_RUN}} |
| Performance | {{capacity_and_timeout_design}} | {{metric_unit_target_load_interval}} | {{measurement_ref_or_NOT_RUN}} |
| Operations | {{monitoring_recovery_and_rollback_controls}} | {{service_objectives_or_unknown}} | {{runbook_and_execution_ref_or_NOT_RUN}} |

## Decisions and verification

| Requirement ID | Design element | Decision ID | Planned assertion | Execution result |
| --- | --- | --- | --- | --- |
| {{requirement_id}} | {{component_or_control}} | {{decision_id_or_null}} | {{observable_assertion_and_test_id}} | {{NOT_RUN_or_retained_result}} |

Implementation prerequisites: {{missing_decisions_sources_and_permissions}}.
Alternatives: {{alternative_designs_tradeoffs_and_selection_state}}.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{document_or_repository_path_and_lines}} | {{exact_revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_content_read}} |

Facts: {{source_supported_facts}}.
Inferences: {{reasoned_conclusions_with_evidence_and_limits}}.
Unresolved questions: {{questions_owner_and_resolution_needed}}.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| {{finding_id}} | {{source_revision_and_locator}} | {{observable_effect_or_risk}} | {{owner_or_unknown}} | {{specific_action_and_completion_evidence}} | {{open_or_resolved}} |
````

## Illustrative sample

````markdown
---
artifact_kind: "system-design"
id: "SAMPLE-ARCH-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-NFR-001, SAMPLE-ADR-001, SAMPLE-CONTRACT-001]
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

# Invoice portal design

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Scope and drivers

| Field | Value |
| --- | --- |
| Design state | Proposed; no implementation evidence. |
| Problem and outcome | Customers need controlled invoice access. |
| Included behavior | SAMPLE-CAP-001; SAMPLE-REQ-001; SAMPLE-REQ-002. |
| Exclusions | Staff access; its policy remains unknown. |
| Constraints | Check customer access before returning invoice content. |
| Current revision | sample-v1; repository commit null. |

## Components and boundaries

| Component ID | Resource kind | Responsibility | Owner | Source revision and locator |
| --- | --- | --- | --- | --- |
| SAMPLE-UI-001 | ui | Request and display permitted invoice content. | unknown | SAMPLE-SRC-001, sample-v1, Proposed design. |
| SAMPLE-SVC-001 | service | Check identity and invoice access. | unknown | SAMPLE-SRC-001, sample-v1, Proposed design. |
| SAMPLE-STORE-001 | store | Supply requested invoice data. | unknown | SAMPLE-SRC-001, sample-v1, Proposed design. |
| SAMPLE-REPO-001 | repository | Implementation responsibility unknown. | unknown | No inspected commit or source location. |

## Relationships and interfaces

| Consumer ID | Provider ID | Contract ID | Relationship state | Evidence and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-UI-001 | SAMPLE-SVC-001 | SAMPLE-CONTRACT-001 | proposed | GET /invoices/{invoice_id}; no observed calls. |
| SAMPLE-SVC-001 | SAMPLE-STORE-001 | unknown | proposed | Internal dependency only; transport unknown. |
| SAMPLE-SVC-001 | SAMPLE-REPO-001 | not applicable | declared association candidate | Implementation mapping requires exact code inspection. |

## Request and failure paths

| Path | Ordered actions | Observable result | Requirement or unresolved question |
| --- | --- | --- | --- |
| Permitted | Receive request; check identity; check access; return invoice. | HTTP 200; exactly one invoice, INV-001. | SAMPLE-REQ-001. |
| Denied | Receive request; check identity; reject unauthorized access. | HTTP 403; zero invoices; "Access denied". | SAMPLE-REQ-002. |
| Dependency failure | Recovery behavior unknown. | Failure response unknown. | Obtain the dependency failure requirement. |

## Data and quality controls

| Concern | Proposed control | Target and conditions | Verification evidence |
| --- | --- | --- | --- |
| Data protection | Check access before returning content. | Denied responses contain zero invoices. | SAMPLE-TEST-002; NOT_RUN. |
| Performance | Capacity design unknown. | p95 <=500 ms; 20 customers; 10 minutes; two-minute warmup; successful requests only. | SAMPLE-NFR-001; NOT_RUN. |
| Operations | Monitoring and recovery design unknown. | Production objectives unknown. | Runbook unknown; NOT_RUN. |

Timing starts at service receipt and ends at response completion.

## Decisions and verification

| Requirement ID | Design element | Decision ID | Planned assertion | Execution result |
| --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 | SAMPLE-SVC-001 access check | SAMPLE-ADR-001 | SAMPLE-TEST-001 expects invoice count 1 and ID INV-001. | NOT_RUN |
| SAMPLE-REQ-002 | SAMPLE-SVC-001 access check | SAMPLE-ADR-001 | SAMPLE-TEST-002 expects invoice count 0 and "Access denied". | NOT_RUN |

Implementation prerequisites: Determine policy ownership, inspect implementation sources, and obtain required reviews.
Alternatives: Portal-only checking needs assessment; the service-check proposal remains unapproved.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: The service must enforce the proposed access rules; implementation remains unknown.
Unresolved questions: Who owns invoice access policy? Owner unknown; obtain the policy source.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-ARCH-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | Unreviewed policy prevents design acceptance. | unknown | Identify the policy owner and record the review decision. | open |
````

## Completion checks

- Cover successful, denied, and dependency failure paths.
- Keep resource identities separate and qualify every dependency claim.
- Trace each required quality target to measurement conditions and evidence.
- Record unresolved implementation and operational boundaries.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
