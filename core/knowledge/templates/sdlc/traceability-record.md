# Requirements traceability record

## Purpose

Trace declared requirements through criteria, inspected assertions, and retained execution evidence.

## AI instructions

1. Required inputs: requirement or defect records, acceptance criteria, related design IDs, and source revisions.
2. Required inputs: repository identities, exact inspected code and test revisions, assertion locations, and retained execution records.
3. Record many-to-many links as separate relationship rows with supporting evidence.
4. Separate a declared test mapping from an inspected assertion mapping.
5. Separate knowledge review from passing behavior evidence.
6. Do not infer runtime coverage from names, imports, metadata, or passing command status.
7. Show AC-to-test, AC-to-code-change, and code-change-to-test coverage in separate tables.
8. Declare inventories before mapping. Include unmapped ACs, changes, failed results, and evidence gaps.
9. Interpret `TC >= AC = Code Change` as behavior coverage and equivalence, not equal record counts.
10. Compare missing, extra, and contradictory behavior. Report material unknowns before any 100% conformance claim.

Follow the [coverage procedure](../../../../.agents/skills/verify-implementation/references/behavior-review.md#report-coverage) for definitions and counting rules.
Separate canonical test definitions, inspected assertions, conforming implementation, and matching passing execution.

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
- Defect IDs: {{defect_ids_or_not_applicable_reason}}
- Repository IDs: {{repository_ids}}
- Service and contract IDs: {{service_ids_and_contract_ids}}
- Scope limit: {{included_behavior_and_exclusions}}

## Requirement and criterion declarations

| Requirement or defect ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| {{requirement_id}} | {{criterion_id}} | {{conditions_action_result_and_limit}} | {{revision_or_null}} | pending |

## Coverage inventories and summary

Target: `TC >= AC = Code Change` means tests cover intended predicates and relevant boundaries.
Changed business behavior must match intended behavior without omissions or additional unsupported outcomes.
Counts alone do not establish equivalence. This report requires semantic source and assertion review.

- Intent inventory: {{requirement_and_defect_versions_all_active_ac_and_atomic_predicate_links}}
- Canonical test inventory: {{case_definition_links_versions_levels_and_exclusions}}
- Change inventory: {{all_meaningful_changes_base_head_commits_symbols_or_hunks_and_maintenance_rationales}}
- Preserved behavior: {{applicable_existing_requirements_and_relevant_unchanged_paths}}
- Execution scope: {{exact_code_test_hashes_environment_and_required_test_levels}}

| Metric | Qualified / total | Percentage | Partial, missing, unknown, failed, stale, or not-run IDs | Evidence and limit |
| --- | --- | --- | --- | --- |
| AC to canonical test definitions | {{ac_with_all_predicates_defined}} / {{all_active_ac}} | {{percent_or_na}} | {{ids_or_none}} | {{definition_evidence}} |
| AC to inspected assertions | {{ac_with_all_required_assertions}} / {{all_active_ac}} | {{percent_or_na}} | {{ids_or_none}} | {{assertion_evidence}} |
| AC to passing execution | {{ac_with_all_required_matching_passes}} / {{all_active_ac}} | {{percent_or_na}} | {{ids_or_none}} | {{execution_evidence}} |
| AC to inspected implementation mapping | {{ac_with_all_predicates_linked_to_inspected_paths}} / {{all_active_ac}} | {{percent_or_na}} | {{ids_or_none}} | {{implementation_mapping_evidence}} |
| AC to conforming implementation | {{ac_with_all_predicates_matching_source}} / {{all_active_ac}} | {{percent_or_na}} | {{ids_or_none}} | {{conformance_evidence}} |
| Change to canonical test definitions | {{changes_with_all_affected_predicates_defined}} / {{all_meaningful_implementation_changes}} | {{percent_or_na}} | {{ids_or_none}} | {{definition_evidence}} |
| Change to inspected assertions | {{changes_with_all_required_assertions}} / {{all_meaningful_implementation_changes}} | {{percent_or_na}} | {{ids_or_none}} | {{assertion_evidence}} |
| Change to passing execution | {{changes_with_all_required_matching_passes}} / {{all_meaningful_implementation_changes}} | {{percent_or_na}} | {{ids_or_none}} | {{execution_evidence}} |
| Behavioral change justification | {{behavioral_changes_with_supported_intent}} / {{all_business_behavior_changes}} | {{percent_or_na}} | {{unexplained_change_ids_or_none}} | {{intent_evidence}} |

Count each inventory item once. Expand compound ACs into a linked predicate breakdown below each summary.
Use `N/A` for a known empty denominator. Use `UNKNOWN` when the complete inventory is unavailable.
Do not calculate a percentage from an incomplete inventory.
Report instrumented line and branch coverage separately when available.

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

### AC to test case coverage

| Requirement/defect and AC version | Applicable predicate | Canonical case and level | Inspected assertion and test revision/hash | Definition / assertion completeness | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- |
| {{separate_linked_source_and_ac_ids}} | {{predicate_id_and_expected_outcome}} | {{case_definition_link_or_missing}} | {{assertion_link_or_unknown}} | {{complete_partial_missing_unknown_for_each}} | {{result_link_or_not_run}} | {{gap_owner_and_next_action_or_none}} |

### AC to code change coverage

| Requirement/defect and AC version | Intended predicate | Change ID or UNCHANGED | Exact old/new source locations | Conformance | Missing, extra, contradictory, or unknown behavior | Evidence and limit |
| --- | --- | --- | --- | --- | --- | --- |
| {{separate_linked_source_and_ac_ids}} | {{predicate_id_and_expected_outcome}} | {{change_definition_link_or_unchanged}} | {{repository_base_head_file_symbol_and_hash_links}} | {{match_missing_extra_contradictory_unknown}} | {{gap_or_none}} | {{inspected_evidence_and_scope_limit}} |

### Code change to test case coverage

| Change ID and repository base/head | Changed symbol or hunk | AC links or maintenance rationale | Affected predicate | Canonical case and required level | Inspected assertion | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{change_definition_link_and_exact_revisions}} | {{source_link_and_hash}} | {{each_ac_link_or_sourced_maintenance_rationale}} | {{predicate_and_boundary}} | {{case_definition_links_or_missing}} | {{assertion_links_and_test_hashes_or_unknown}} | {{result_links_or_not_run}} | {{gap_owner_and_next_action_or_none}} |

Keep unsupported changes visible even when no AC maps to them.
An absent relationship means unknown coverage until source inspection establishes missing or extra behavior.
Necessary unchanged implementation can satisfy an AC without a new code change.

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

## Coverage inventories and summary

Intent includes two sample ACs. Two proposed tests exist; their executable assertions and test levels remain unknown.
The implementation and complete change inventory are unavailable. The code-change denominator is unknown.

| Metric | Qualified / total | Percentage | Incomplete or failed IDs | Evidence and limit |
| --- | --- | --- | --- | --- |
| AC to inspected assertions | 0 / 2 | 0% | SAMPLE-AC-001, SAMPLE-AC-002 | No executable assertions were inspected |
| AC to passing execution | 0 / 2 | 0% | SAMPLE-AC-001, SAMPLE-AC-002 | Both tests remain NOT_RUN |
| AC to inspected implementation mapping | 0 / 2 | 0% | SAMPLE-AC-001, SAMPLE-AC-002 | No implementation paths were inspected |
| AC to conforming implementation | 0 / 2 | 0% | SAMPLE-AC-001, SAMPLE-AC-002 | No source conformance evidence exists |
| Change to inspected assertions | UNKNOWN | UNKNOWN | unknown | Complete change inventory unavailable |
| Change to passing execution | UNKNOWN | UNKNOWN | unknown | No retained execution or change inventory exists |

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

### AC to test case coverage

| Requirement/defect and AC version | Applicable predicate | Canonical case and level | Inspected assertion and test revision/hash | Definition / assertion completeness | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 / SAMPLE-AC-001, sample-v1 | Return exactly owned INV-001 | Proposed SAMPLE-TEST-001; level unknown | unknown | Proposed / unknown | NOT_RUN | No executable assertion was inspected |
| SAMPLE-REQ-002 / SAMPLE-AC-002, sample-v1 | Deny unpermitted access | Proposed SAMPLE-TEST-002; level unknown | unknown | Proposed / unknown | NOT_RUN | No executable assertion was inspected |

### AC to code change coverage

| Requirement/defect and AC version | Intended predicate | Change ID or UNCHANGED | Exact old/new source locations | Conformance | Missing, extra, contradictory, or unknown behavior | Evidence and limit |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 / SAMPLE-AC-001, sample-v1 | Return exactly owned INV-001 | unknown | unknown | UNKNOWN | Implementation unavailable | No source inspection exists |
| SAMPLE-REQ-002 / SAMPLE-AC-002, sample-v1 | Deny unpermitted access | unknown | unknown | UNKNOWN | Implementation unavailable | No source inspection exists |

### Code change to test case coverage

The complete code-change inventory is unknown. This direction is `UNKNOWN`; no denominator can be calculated.
No code-to-test relationship or equivalence claim is established.

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
- AC-to-test, AC-to-code-change, and code-change-to-test tables expose all included items and missing links.
- Declared inventories support each numerator, denominator, percentage, and test-level boundary.
- Definition coverage, assertion coverage, source conformance, and matching execution remain separate.
- Both missing behavior and additional unsupported behavior limit the equivalence conclusion.
- Each relationship has evidence and a stated evidence class.
- Code inspection records exact revisions and assertion contents.
- Verification claims cite retained execution for the inspected assertions.
- Knowledge approval and behavior execution appear in separate fields.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
