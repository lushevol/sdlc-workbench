# Test strategy and plan

## Purpose

Define test scope, methods, responsibilities, environments, and measurable completion conditions.

## AI instructions

1. Required inputs: requirement IDs, criterion IDs, risk evidence, and applicable interface specifications.
2. Required inputs: repository identities, inspected revisions, environment needs, and authorized executable tools.
3. Map each planned test to an observable criterion and a test level.
4. Obtain reviewed performance limits before defining performance acceptance.
5. Keep unavailable code and test revisions null. Do not infer coverage from test names.
6. After code changes, inventory original defect cases and additional cases derived from changed branches and review risks.
7. Inspect existing helper assertions before adding test code. Identify genuine gaps and unsupported business expectations.
8. Run every declared case when requested. Report omissions, failures, and blocked cases separately from passes.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "test-strategy-plan"
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

# {{plan_title}}

## Goal and scope

- Goal: {{engineering_question_and_required_evidence}}
- Included requirements: {{requirement_ids_and_scope}}
- Exclusions: {{excluded_behavior_and_reason}}
- Risk basis: {{source_refs_and_consequences}}

## Inputs and revisions

| Resource identity | Kind | Locator | Exact revision | Inspection evidence |
| --- | --- | --- | --- | --- |
| {{resource_id}} | {{repository_or_contract_or_source}} | {{locator}} | {{revision_or_null}} | {{evidence_ref_or_null}} |

## Planned coverage

| Test ID | Requirement / criterion | Test level | Conditions and action | Observable assertion | Limit | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| {{test_id}} | {{requirement_id}} / {{criterion_id}} | {{level}} | {{conditions_and_action}} | {{assertion}} | {{limit_or_not_applicable_reason}} | unknown |

## Change-derived case inventory

| Case ID | Origin | Changed path or review finding | Required predicate | Executable case and assertion locator | Browser execution requirement |
| --- | --- | --- | --- | --- | --- |
| {{case_id}} | {{original_defect_or_new_change_case}} | {{commit_path_symbol_or_finding_id}} | {{observable_positive_negative_boundary_or_race_predicate}} | {{test_revision_path_case_and_helper}} | {{real_target_browser_and_required_duration}} |

- Inventory total: {{original_count_new_count_and_combined_count}}
- Missing assertions: {{case_ids_and_missing_predicates_or_none}}
- Runtime substitutions: {{mocks_shortened_clocks_routes_and_claim_limits_or_none}}
- Completion rule: {{all_inventoried_cases_have_retained_browser_results_and_required_predicates_pass}}

## Environment and data

- Environment specification: {{environment_document_id_and_locator}}
- Data specification: {{fixture_document_id_and_locator}}
- Required tools: {{tool_ids_and_permission_evidence}}
- Isolation and cleanup: {{procedures_and_completion_conditions}}
- Dependencies: {{dependency_ids_and_evidence}}

## Entry and completion conditions

| Gate | Measurable condition | Required evidence | Current state |
| --- | --- | --- | --- |
| Entry | {{entry_condition}} | {{evidence_refs}} | pending |
| Completion | {{completion_condition}} | {{retained_results_and_assertions}} | pending |

## Execution planning

```yaml
execution_status: NOT_RUN
repository_revision: null
test_revision: null
environment_identity: null
planned_run_locator: "{{authorized_run_instruction_locator}}"
actual_results: null
retained_execution_refs: []
approval: null
```

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
artifact_kind: "test-strategy-plan"
id: "SAMPLE-PLAN-TEST-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-NFR-001, SAMPLE-TEST-001, SAMPLE-TEST-002]
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

# Invoice access test plan

## Goal and scope

- Goal: Obtain assertion evidence for permitted access, denied access, and the proposed response time target.
- Included requirements: SAMPLE-REQ-001, SAMPLE-REQ-002, and SAMPLE-NFR-001.
- Exclusions: Staff access lacks a supplied rule.
- Risk basis: SAMPLE-RULE-003 requires zero invoice content after denied access.

## Inputs and revisions

| Resource identity | Kind | Locator | Exact revision | Inspection evidence |
| --- | --- | --- | --- | --- |
| SAMPLE-REPO-001 | repository | unknown | null | null |
| SAMPLE-CONTRACT-001 | contract | sample-context.md#proposed-design | sample-v1 | Illustrative description only |

## Planned coverage

| Test ID | Requirement / criterion | Test level | Conditions and action | Observable assertion | Limit | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-TEST-001 | SAMPLE-REQ-001 / SAMPLE-AC-001 | Proposed service interface test | Customer A requests owned invoice INV-001 | Exactly one invoice; identifier INV-001 | One invoice | unknown |
| SAMPLE-TEST-002 | SAMPLE-REQ-002 / SAMPLE-AC-002 | Proposed service interface test | Customer B requests INV-001 without permission | Zero invoices; message "Access denied" | Zero invoices | unknown |
| SAMPLE-TEST-PERF-001 | SAMPLE-NFR-001 / criterion unresolved | Proposed performance test | 20 concurrent customers; 10 measured minutes after two warmup minutes | Measure successful authorized requests from service receipt through response completion | 95th percentile ≤500 milliseconds | unknown |

## Environment and data

- Environment specification: SAMPLE-ENV-001 in test-data-environment.md.
- Data specification: SAMPLE-ENV-001 defines the proposed ownership fixture.
- Required tools: unknown. No execution permission is established.
- Isolation and cleanup: Procedures are unknown. Use isolated fictional fixtures after authorization.
- Dependencies: SAMPLE-SVC-001 and its proposed store require inspection before execution.

## Entry and completion conditions

| Gate | Measurable condition | Required evidence | Current state |
| --- | --- | --- | --- |
| Entry | Review both access criteria and identify exact code and test revisions | Human review record and revision evidence | pending |
| Completion | Retain assertion results for both access tests and the performance measurement | Assertion locations, execution records, environment identity, and measurement data | pending |

## Execution planning

```yaml
execution_status: NOT_RUN
repository_revision: null
test_revision: null
environment_identity: null
planned_run_locator: unknown
actual_results: null
retained_execution_refs: []
approval: null
```

## Facts, inferences, and unresolved questions

- Facts: The context defines two access criteria and a proposed response time target.
- Inferences: Service interface tests could observe the stated access outcomes.
- Unresolved questions: The test framework, performance criterion ID, and responsible owners are unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | No access behavior is verified | unknown | Inspect code and assertions, then retain an authorized execution |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Post-change plans inventory every original defect case and each additional executable case.
- Completion conditions cover the complete declared browser suite.
- Every scoped criterion has planned assertions or an explicit coverage gap.
- Entry and completion conditions identify measurable evidence.
- Performance conditions name the interval, load, percentile, unit, and request population.
- Resource identities, revisions, and execution permissions remain distinct.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
