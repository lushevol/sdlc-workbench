# Repository profile

## Purpose

Describe repository responsibilities and interfaces from exact source evidence.
Help AI locate relevant code without confusing declarations with execution permission.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: repository identity, remote locator, exact commit, language manifests, entry points, caller paths, interfaces, tests, and instructions.

Read the owning repository's instructions before proposing changes.
Inspect symbols, callers, importers, and affected interface paths at the same revision.
Use direct source inspection when no usable project index exists.
Record searched paths and excluded areas to limit coverage claims.
Keep portable identities separate from local machine paths.
Do not execute commands solely because this profile lists them.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "repository-profile"
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

# {{repository_name}} profile

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Repository identity and inspection

| Field | Value |
| --- | --- |
| Repository ID | {{repository_id}} |
| Remote locator | {{remote_url_or_unknown}} |
| Full inspected Git commit | {{full_commit_hash_or_null}} |
| Worktree state | {{clean_or_recorded_changes_or_unknown}} |
| Owning instructions | {{instruction_paths_revisions_and_scope}} |
| Inspection scope | {{paths_symbols_searches_and_exclusions}} |
| Responsible owner | {{owner_or_unknown}} |
| Local location | {{ignored_local_mapping_ref_or_unknown}} |

## Responsibilities and relationships

| Resource ID | Kind | Relationship | Evidence state | Exact source location and limits |
| --- | --- | --- | --- | --- |
| {{service_capability_contract_or_repository_id}} | {{resource_kind}} | {{implements_provides_consumes_or_depends_on}} | {{declared_static_or_runtime_observed}} | {{commit_path_lines_and_observation_or_null}} |

## Source map and affected symbols

| Area or symbol | Source path and lines | Responsibility | Callers and importers | Interface impact |
| --- | --- | --- | --- | --- |
| {{entrypoint_or_symbol}} | {{exact_path_lines_and_commit}} | {{observed_responsibility}} | {{inspected_caller_and_import_paths_or_unknown}} | {{affected_boundary_or_none_with_evidence}} |

## Build, tests, and tools

| Purpose | Exact command | Working directory | Preconditions and execution grant | Result and evidence |
| --- | --- | --- | --- | --- |
| Build | {{documented_command_or_unknown}} | {{repository_relative_directory}} | {{runtime_dependencies_and_actual_grant_or_null}} | NOT_RUN |
| Test | {{documented_command_or_unknown}} | {{repository_relative_directory}} | {{configuration_data_and_actual_grant_or_null}} | NOT_RUN |
| Analysis | {{documented_command_or_unknown}} | {{repository_relative_directory}} | {{index_scope_and_actual_grant_or_null}} | NOT_RUN |

## Implementation and verification evidence

| Requirement or contract | Implementation location | Assertion location | Execution evidence | Coverage limit |
| --- | --- | --- | --- | --- |
| {{requirement_or_contract_id}} | {{commit_path_and_lines_or_null}} | {{test_commit_path_and_assertion_or_null}} | {{retained_execution_ref_or_null}} | {{what_the_evidence_does_not_establish}} |

## Change guidance

Affected scope: {{symbols_callers_importers_contracts_and_data_paths}}.
Qualitative risk: {{low_moderate_or_high_with_reason}}.
Required checks: {{tests_builds_contract_checks_and_reasons}}.
Open implementation boundaries: {{unresolved_paths_and_required_inspection}}.

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
artifact_kind: "repository-profile"
id: "SAMPLE-REPO-PROFILE-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REPO-001, SAMPLE-SVC-001, SAMPLE-CAP-001, SAMPLE-CONTRACT-001]
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

# Invoice repository profile candidate

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Repository identity and inspection

| Field | Value |
| --- | --- |
| Repository ID | SAMPLE-REPO-001. |
| Remote locator | unknown |
| Full inspected Git commit | null |
| Worktree state | unknown |
| Owning instructions | unknown; repository access not established. |
| Inspection scope | Fictional context only; no source paths or symbols inspected. |
| Responsible owner | unknown |
| Local location | unknown; no clone or machine path declared. |

## Responsibilities and relationships

| Resource ID | Kind | Relationship | Evidence state | Exact source location and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SVC-001 | service | Implementation association candidate. | declared candidate | Source location null; relationship unproven. |
| SAMPLE-CAP-001 | capability | Invoice viewing context. | declared | SAMPLE-SRC-001, sample-v1; no implementation mapping. |
| SAMPLE-CONTRACT-001 | contract | Candidate invoice lookup boundary. | proposed | No contract path or full repository commit. |

## Source map and affected symbols

| Area or symbol | Source path and lines | Responsibility | Callers and importers | Interface impact |
| --- | --- | --- | --- | --- |
| Invoice request entry point | unknown; commit null. | Proposed invoice access handling. | unknown | SAMPLE-CONTRACT-001; mapping unproven. |
| Access check | unknown; commit null. | Proposed ownership decision. | unknown | SAMPLE-REQ-002; mapping unproven. |

## Build, tests, and tools

| Purpose | Exact command | Working directory | Preconditions and execution grant | Result and evidence |
| --- | --- | --- | --- | --- |
| Build | unknown | unknown | Dependencies unknown; grant null. | NOT_RUN; evidence null. |
| Test | unknown | unknown | Configuration unknown; grant null. | NOT_RUN; evidence null. |
| Analysis | unknown | unknown | No index or source scope available; grant null. | NOT_RUN; evidence null. |

## Implementation and verification evidence

| Requirement or contract | Implementation location | Assertion location | Execution evidence | Coverage limit |
| --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 | null | SAMPLE-TEST-001 planned; revision null. | null | No assertions or execution inspected. |
| SAMPLE-REQ-002 | null | SAMPLE-TEST-002 planned; revision null. | null | No assertions or execution inspected. |
| SAMPLE-CONTRACT-001 | null | null | null | Proposed HTTP behavior only. |

## Change guidance

Affected scope: Request entry point, access check, callers, imports, and response boundary require inspection.
Qualitative risk: unknown; no repository evidence supports an assessment.
Required checks: Determine supported build, tests, and contract checks from the owning repository.
Open implementation boundaries: Repository ownership, source location, full commit, and deployment mapping remain unknown.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: The repository may implement invoice access; no source evidence confirms that mapping.
Unresolved questions: Which exact repository revision implements the service? Owner unknown; inspect the registered source.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-REPO-PROFILE-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | AI cannot identify safe implementation or verification locations. | unknown | Obtain repository access and inspect entry points, callers, importers, and tests at one full commit. | open |
````

## Completion checks

- Record the exact inspected commit and source paths for implementation claims.
- Inspect callers, importers, entry points, and affected interfaces before change guidance.
- Record search scope and evidence exclusions.
- Keep commands, tool grants, and retained execution as separate facts.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
