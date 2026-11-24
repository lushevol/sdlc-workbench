# Data design and migration plan

## Purpose

Describe data structures and a controlled transition between data versions.
Use explicit checks, stop conditions, and recovery evidence.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: current and target schemas, data ownership, classifications, transformation rules, volumes, deployment constraints, and recovery requirements.

Inspect schema and migration sources at exact revisions.
Document destructive operations and recovery limits before proposing execution.
Define data checks before and after each migration stage.
Keep backup creation, restore validation, and production execution NOT_RUN until retained evidence exists.
Do not infer a retention period from storage configuration.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "data-design-migration"
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

# {{data_change_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Scope and data model

| Field | Value |
| --- | --- |
| Change objective | {{business_outcome_and_requirement_ids}} |
| Current schema and revision | {{schema_locator_and_exact_revision_or_unknown}} |
| Target schema and revision | {{proposed_schema_locator_and_revision}} |
| Store and service IDs | {{separate_store_service_and_repository_ids}} |
| Volume and migration window | {{record_volume_size_window_and_sources_or_unknown}} |
| Data classification and owner | {{classification_and_owner_or_unknown}} |
| Retention and disposal | {{policy_source_and_period_or_unknown}} |

| Entity or field | Type and nullability | Key or relationship | Constraint | Source or proposal |
| --- | --- | --- | --- | --- |
| {{entity_field}} | {{type_nullability_default}} | {{key_or_relationship}} | {{uniqueness_integrity_or_access_constraint}} | {{evidence_or_proposed}} |

## Transformation mapping

| Source field | Target field | Transformation | Invalid data handling | Reversible |
| --- | --- | --- | --- | --- |
| {{source_field}} | {{target_field}} | {{deterministic_mapping}} | {{reject_quarantine_or_review_rule}} | {{yes_no_and_reason}} |

## Preconditions and stages

| Stage | Preconditions | Action | Owner | Stop condition | Evidence and result |
| --- | --- | --- | --- | --- | --- |
| Backup | {{scope_access_and_consistency_conditions}} | {{backup_and_restore_check}} | {{owner_or_unknown}} | {{failed_check_or_missing_evidence}} | NOT_RUN |
| Migrate | {{required_backup_and_schema_checks}} | {{ordered_migration_steps}} | {{owner_or_unknown}} | {{measured_limit_or_integrity_failure}} | NOT_RUN |
| Validate | {{completed_stage_and_stable_observation_window}} | {{data_and_business_checks}} | {{owner_or_unknown}} | {{failed_expected_result}} | NOT_RUN |

## Data checks

| Check | Before measurement | Expected after result | Method and exact revision | Actual result |
| --- | --- | --- | --- | --- |
| Count reconciliation | {{baseline_count_or_null}} | {{reconciliation_formula_and_allowed_difference}} | {{query_or_tool_revision}} | NOT_RUN |
| Referential integrity | {{baseline_or_null}} | {{permitted_orphan_count}} | {{query_or_tool_revision}} | NOT_RUN |
| Business behavior | {{baseline_or_null}} | {{requirement_assertion}} | {{test_revision}} | NOT_RUN |

## Rollback and recovery

Rollback trigger: {{observable_failure_and_decision_owner}}.
Recovery point: {{backup_identity_timestamp_and_consistency_scope_or_null}}.
Recovery steps: {{ordered_restore_schema_and_application_steps}}.
Irreversible boundary: {{operation_after_which_restore_or_reconciliation_is_required}}.
Recovery target: {{approved_recovery_time_and_data_loss_limits_or_unknown}}.

| Restore check | Expected result | Retained evidence | Result |
| --- | --- | --- | --- |
| {{restore_or_reconciliation_check}} | {{measurable_result}} | {{evidence_ref_or_null}} | NOT_RUN |

## Execution authorization and record

Environment: {{environment_identity_or_null}}.
Execution authorization: {{actual_grant_or_null}}.
Execution revision: {{full_migration_commit_or_null}}.
Execution start and end: null.
Final disposition: {{not_run_completed_or_rolled_back_with_evidence}}.

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
artifact_kind: "data-design-migration"
id: "SAMPLE-DATA-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-ARCH-001, SAMPLE-REQ-001, SAMPLE-REQ-002]
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

# Invoice ownership data design

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Scope and data model

| Field | Value |
| --- | --- |
| Change objective | Support SAMPLE-REQ-001 and SAMPLE-REQ-002 through invoice access information. |
| Current schema and revision | unknown; no repository commit inspected. |
| Target schema and revision | Illustrative proposed invoice ownership model; sample-v1. |
| Store and service IDs | SAMPLE-STORE-001; SAMPLE-SVC-001; repository mapping unknown. |
| Volume and migration window | unknown |
| Data classification and owner | Invoice content; classification and owner unknown. |
| Retention and disposal | unknown; obtain the retention decision. |

| Entity or field | Type and nullability | Key or relationship | Constraint | Source or proposal |
| --- | --- | --- | --- | --- |
| Invoice identifier | Identifier format unknown; proposed required value. | Identifies one invoice. | Uniqueness proposal requires schema review. | INV-001 in illustrative context. |
| Customer access relationship | Representation unknown. | Connects a customer to permitted invoices. | Customer A owns INV-001; Customer B lacks access. | Proposed behavior only. |

## Transformation mapping

| Source field | Target field | Transformation | Invalid data handling | Reversible |
| --- | --- | --- | --- | --- |
| unknown | Invoice identifier | unknown; inspect current schema first. | Stop planning affected records until mapping exists. | unknown |
| unknown | Customer access relationship | unknown; identify authoritative access data. | Hold unresolved access mappings for review. | unknown |

## Preconditions and stages

| Stage | Preconditions | Action | Owner | Stop condition | Evidence and result |
| --- | --- | --- | --- | --- | --- |
| Backup | Store identity, consistency method, and access grant known. | Define backup and validate restore in an authorized environment. | unknown | Missing recovery evidence. | NOT_RUN |
| Migrate | Reviewed mapping and validated recovery path. | No executable migration exists in this sample. | unknown | Unmapped records or failed integrity checks. | NOT_RUN |
| Validate | Baselines and expected data changes recorded. | Reconcile data and inspect invoice access assertions. | unknown | Unexpected record difference or access result. | NOT_RUN |

## Data checks

| Check | Before measurement | Expected after result | Method and exact revision | Actual result |
| --- | --- | --- | --- | --- |
| Count reconciliation | null | Proposed: after count equals baseline plus approved additions minus approved deletions. | null; query not authored. | NOT_RUN |
| Referential integrity | null | Proposed: zero ownership links referencing absent invoices. | null; query not authored. | NOT_RUN |
| Business behavior | null | Customer A receives INV-001; Customer B receives zero invoices. | SAMPLE-TEST-001 and SAMPLE-TEST-002; revisions null. | NOT_RUN |

## Rollback and recovery

Rollback trigger: Proposed integrity or access assertion failure; decision owner unknown.
Recovery point: null; no backup exists in this sample.
Recovery steps: Restore sequence remains unknown until storage and schema details exist.
Irreversible boundary: unknown; inspect every proposed transformation before execution.
Recovery target: unknown; obtain approved recovery time and data loss limits.

| Restore check | Expected result | Retained evidence | Result |
| --- | --- | --- | --- |
| Restore data and access relationships. | Proposed: match the recorded backup baseline and access assertions. | null | NOT_RUN |

## Execution authorization and record

Environment: null.
Execution authorization: null.
Execution revision: null.
Execution start and end: null.
Final disposition: NOT_RUN; this artifact contains no executable migration.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: An ownership representation is needed; its storage schema remains unspecified.
Unresolved questions: What is the current schema and recovery policy? Owner unknown; inspect sources and obtain reviewed constraints.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-DATA-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | Migration safety and reversibility cannot be assessed. | unknown | Inspect the current schema and document a validated recovery method before migration. | open |
````

## Completion checks

- Specify current and target schemas before authorizing migration execution.
- Define count, integrity, transformation, and business behavior checks.
- Record rollback triggers, recovery point, irreversible boundaries, and restore validation.
- Keep proposed checks separate from actual data measurements.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
