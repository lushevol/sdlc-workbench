# Pull request and code review

## Purpose

Present a concrete change and record evidence-based reviewer findings.
Keep proposed descriptions separate from inspected diffs and actual review decisions.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: change purpose, requirement IDs, PR locator, exact base and head commits, diff, owning instructions, tests, and retained results.

Read changed symbols and affected callers, importers, and interfaces.
Write the description around final behavior and the actual diff.
For a proposed change, mark the diff unavailable and review pending.
Give actionable findings a source location, consequence, owner, and next action.
Record review approval only when an actual reviewer supplies it.
Do not infer behavior verification from a passing command.

## Template

````markdown
---
artifact_kind: "pull-request-review"
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

# {{pull_request_title}}

## Change identity

| Field | Value |
| --- | --- |
| PR locator | {{url_or_null}} |
| Repository ID | {{repository_id}} |
| Base commit | {{full_base_commit_or_null}} |
| Head commit | {{full_head_commit_or_null}} |
| Requirements and decisions | {{ids_and_versions}} |
| Change state | {{proposed_open_merged_or_closed_with_evidence}} |

## Problem and behavior

Trigger: {{specific_user_or_system_condition}}.
Before: {{observed_current_behavior_and_evidence_or_unknown}}.
After: {{actual_or_proposed_observable_behavior_with_scope}}.
Reason: {{source_supported_problem_and_expected_benefit}}.

## Change scope and risks

| File or symbol | Exact diff location | Change | Callers, importers, and interfaces inspected | Risk and mitigation |
| --- | --- | --- | --- | --- |
| {{file_or_symbol}} | {{head_commit_path_and_lines}} | {{concrete_change}} | {{affected_paths_and_scope_limits}} | {{qualitative_risk_and_action}} |

Compatibility and data impact: {{contract_schema_migration_and_consumer_effects}}.
Recovery: {{revert_rollback_and_irreversible_limits}}.

## Validation evidence

| Requirement or check | Command or inspected assertion | Revision and environment | Retained evidence | Actual result | Claim limit |
| --- | --- | --- | --- | --- | --- |
| {{requirement_or_check}} | {{exact_command_or_test_assertion}} | {{revision_and_environment}} | {{execution_or_inspection_ref_or_null}} | {{NOT_RUN_or_retained_result}} | {{unverified_behavior_or_coverage_limit}} |

## Review findings

| Finding ID and priority | Evidence location | Consequence | Owner | Next action | Resolution evidence |
| --- | --- | --- | --- | --- | --- |
| {{finding_id_and_priority}} | {{commit_path_lines_and_assertion_or_source_gap}} | {{concrete_behavior_or_maintenance_effect}} | {{owner_or_unknown}} | {{specific_fix_or_required_inspection}} | {{evidence_or_null}} |

## Review disposition

Reviewer: null.
Decision: pending.
Review date: null.
Reviewed commits: {{base_and_head_commits_or_null}}.
Review scope limits: {{uninspected_areas_and_missing_execution}}.
Merge or publication authority: {{actual_authority_reference_or_null}}.

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
artifact_kind: "pull-request-review"
id: "SAMPLE-PR-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REPO-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-ADR-001]
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

# Proposed invoice access enforcement

## Change identity

| Field | Value |
| --- | --- |
| PR locator | null; no PR exists in this sample. |
| Repository ID | SAMPLE-REPO-001. |
| Base commit | null |
| Head commit | null |
| Requirements and decisions | SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-ADR-001; illustrative sample-v1. |
| Change state | proposed; no implementation diff. |

## Problem and behavior

Trigger: A customer requests INV-001 through SAMPLE-CONTRACT-001.
Before: unknown; no current implementation inspected.
After: Proposed authorized responses contain INV-001; denied responses contain zero invoices and "Access denied".
Reason: The illustrative rules require invoice access control before content disclosure.

## Change scope and risks

| File or symbol | Exact diff location | Change | Callers, importers, and interfaces inspected | Risk and mitigation |
| --- | --- | --- | --- | --- |
| Invoice request access check | null; source location unknown. | Proposed service access enforcement. | No source paths inspected. | Sensitive access boundary; inspect code and test denied access. |
| Invoice response mapping | null; source location unknown. | Proposed HTTP 200 and HTTP 403 results. | Consumer mapping unknown. | Compatibility unknown; inspect consumers and contract. |

Compatibility and data impact: unknown; no diff or schema evidence exists.
Recovery: Revert and deployment recovery steps remain unknown until a concrete change exists.

## Validation evidence

| Requirement or check | Command or inspected assertion | Revision and environment | Retained evidence | Actual result | Claim limit |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 | Planned SAMPLE-TEST-001: invoice count 1 and ID INV-001. | null; environment unknown. | null | NOT_RUN | No assertion implementation inspected. |
| SAMPLE-REQ-002 | Planned SAMPLE-TEST-002: invoice count 0 and "Access denied". | null; environment unknown. | null | NOT_RUN | No assertion implementation inspected. |
| Repository checks | Commands unknown; inspect repository instructions. | null; environment unknown. | null | NOT_RUN | Build and test behavior unknown. |

## Review findings

| Finding ID and priority | Evidence location | Consequence | Owner | Next action | Resolution evidence |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-PR-F01; priority unassigned | Base, head, and diff unavailable. | Reviewer cannot assess implementation correctness or impact. | unknown | Supply exact commits and inspect the complete diff. | null |

## Review disposition

Reviewer: null.
Decision: pending.
Review date: null.
Reviewed commits: null.
Review scope limits: No source review, test execution, or deployment inspection occurred.
Merge or publication authority: null.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: The proposed behavior needs code and assertion review before any merge assessment.
Unresolved questions: What are the PR and exact compared revisions? Owner unknown; supply the concrete diff.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-PR-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | Code review cannot establish correctness or safe merge scope. | unknown | Provide exact base and head commits, then inspect affected paths and retained results. | open |
````

## Completion checks

- Match the description to the final diff and observable behavior.
- Inspect changed symbols and affected callers, importers, and interfaces.
- Give every actionable finding evidence, consequence, owner, and next action.
- Record actual validation results and limit any behavior verification claim.
- Keep reviewer identity and approval empty until real review occurs.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
