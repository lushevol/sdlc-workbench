# Test execution and verification report

## Purpose

Record actual test evidence and state the exact behaviors that the evidence supports.

## AI instructions

1. Required inputs: test definitions, requirement or defect IDs, criterion IDs, assertions, and exact code and test revisions.
2. Required inputs: execution identity, environment identity, timestamps, retained results, and available evidence hashes.
3. Use NOT_RUN when no execution exists. Keep actual results and timestamps null.
4. Inspect assertion contents and retained execution before claiming behavior verification.
5. A passing command alone does not prove that a criterion passed.
6. Report evidence limits beside the verification claim.
7. For browser E2E, inspect actual target revisions, browser identity, launch settings, fixtures, and substitutions.
8. Bind every original and new case to a retained result. Do not exclude failed, blocked, or skipped cases.
9. Follow [browser evidence rules](../../../../docs/BROWSER_INVESTIGATIONS.md#retain-key-screenshots) for captures and scenario bindings.
10. Show AC-to-test, AC-to-code-change, and code-change-to-test tables with explicit inventories and denominators.
11. Separate canonical definitions, inspected assertions, conforming source, and matching passing execution.
12. Keep missing, extra, contradictory, unknown, stale, failed, and unrun behavior visible.

Follow the [coverage procedure](../../../../.agents/skills/verify-implementation/references/behavior-review.md#report-coverage) for counting and behavioral equivalence.
The target `TC >= AC = Code Change` concerns behavior, not equal numbers of cases, criteria, or changed files.

Follow the [authoring contract](README.md) and read the [sample context](sample-context.md).
Keep facts, inferences, and unresolved questions separate.
Keep execution status separate from document maturity and knowledge review.

## Template

````markdown
---
artifact_kind: "test-execution-report"
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

# {{execution_report_title}}

## Run identity and provenance

```yaml
execution_id: null
execution_status: NOT_RUN
repository_id: "{{repository_id}}"
repository_revision: null
test_revision: null
environment_identity: null
started_at: null
completed_at: null
command_or_tool_reference: "{{authorized_run_instruction_locator}}"
process_exit_status: null
actual_results: null
retained_execution_refs: []
```

## Browser environment and suite completeness

- Case inventory and revision: {{inventory_locator_revision_and_hash_or_not_applicable_reason}}
- Original defect cases: {{total_passed_failed_errored_skipped_blocked_not_run}}
- Additional cases: {{total_passed_failed_errored_skipped_blocked_not_run}}
- Actual target and deployed revisions: {{frontend_service_configuration_ids_and_source_binding_evidence}}
- Browser identity: {{product_version_engine_os_profile_and_launch_arguments}}
- Clock and lifecycle: {{actual_duration_clock_source_visibility_freeze_sleep_and_observer_effects}}
- Fixtures and substitutions: {{real_services_mocks_route_controls_shortened_clocks_and_limits}}
- Source integrity: {{before_after_source_hashes_and_matching_commit_evidence}}
- Missing executions: {{case_ids_blocker_owner_and_next_action_or_none}}

Use `not applicable` with a reason for non-browser runs.
A real browser with substituted services supports only the disclosed integration boundaries.

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion location | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {{test_id}} | {{requirement_id}} / {{criterion_id}} | {{file_line_revision_or_null}} | {{measurable_expected_result}} | null | NOT_RUN | null |

## Coverage inventories and summary

- Intent inventory: {{requirement_defect_versions_each_active_ac_and_atomic_predicate_link}}
- Test inventory: {{canonical_case_links_versions_test_levels_and_assertion_revisions}}
- Change inventory: {{all_meaningful_change_ids_base_head_commits_symbols_or_hunks_and_maintenance_rationales}}
- Required boundaries: {{test_levels_affected_existing_behavior_exclusions_and_reasons}}

| Metric | Qualified / total | Percentage | Incomplete or failed IDs | Evidence and limit |
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

Count each denominator item once. A compound AC qualifies only when every applicable predicate qualifies.
Report partial predicate counts separately. Use `N/A` for a known empty inventory.
Use `UNKNOWN` when the complete inventory is unavailable. Do not calculate its percentage.
List unknown, stale, blocked, skipped, and not-run IDs alongside failed IDs.
Separate instrumented line and branch coverage from behavioral coverage.

### AC to test case coverage

| Requirement/defect and AC version | Applicable predicate | Canonical case and required level | Inspected assertion and test revision/hash | Definition / assertion completeness | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- |
| {{separate_linked_source_and_ac_ids}} | {{predicate_and_expected_outcome}} | {{case_definition_link_or_missing}} | {{assertion_link_or_unknown}} | {{complete_partial_missing_unknown_for_each}} | {{result_link_or_not_run}} | {{gap_owner_and_next_action_or_none}} |

### AC to code change coverage

| Requirement/defect and AC version | Intended predicate | Change ID or UNCHANGED | Exact old/new source locations | Conformance | Missing, extra, contradictory, or unknown behavior | Evidence and limit |
| --- | --- | --- | --- | --- | --- | --- |
| {{separate_linked_source_and_ac_ids}} | {{predicate_and_expected_outcome}} | {{change_definition_link_or_unchanged}} | {{repository_base_head_file_symbol_and_hash_links}} | {{match_missing_extra_contradictory_unknown}} | {{gap_or_none}} | {{source_evidence_and_scope_limit}} |

### Code change to test case coverage

| Change ID and repository base/head | Changed symbol or hunk | AC links or maintenance rationale | Affected predicate | Canonical case and required level | Inspected assertion | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{change_definition_link_and_exact_revisions}} | {{source_link_and_hash}} | {{each_ac_link_or_sourced_maintenance_rationale}} | {{predicate_and_boundary}} | {{case_definition_links_or_missing}} | {{assertion_links_and_test_hashes_or_unknown}} | {{result_links_or_not_run}} | {{gap_owner_and_next_action_or_none}} |

Link definitions, code, assertions, and execution separately. Retain original result bindings when current source differs.
Keep every unmapped AC and meaningful code change visible.
Relevant unchanged source can satisfy an AC without a new change.
An absent mapping remains `UNKNOWN` until inspection establishes omitted, contradictory, or additional unsupported behavior.

## Retained evidence inventory

| Evidence ID | Locator | Hash | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| {{evidence_id_or_null}} | {{locator_or_null}} | {{hash_or_null}} | {{execution_id_or_null}} | {{limit}} |

## Browser evidence bindings

| Case and step | Capture time and phase | Screenshot or trace | SHA-256 | Assertion or request evidence | Supported claim and limit |
| --- | --- | --- | --- | --- | --- |
| {{case_id_and_step_or_not_applicable_reason}} | {{timestamp_clock_and_phase_or_null}} | {{retained_locator_or_capture_failure}} | {{hash_or_null}} | {{assertion_event_or_correlation_locator_or_null}} | {{observed_predicate_and_omitted_boundary}} |

## Verification conclusion

- Behavior claim: {{evidence_supported_claim_or_no_verification}}
- Covered conditions: {{conditions_supported_by_evidence}}
- Uncovered conditions: {{conditions_without_evidence}}
- Evidence limits: {{missing_revisions_or_assertions_or_results}}
- Behavioral equality: {{match_missing_extra_contradictory_or_unknown_with_predicate_evidence}}
- Missing required behavior: {{predicate_links_evidence_owner_and_next_action_or_none}}
- Additional unsupported behavior: {{change_links_intent_search_evidence_owner_and_next_action_or_none}}

Claim 100% equivalence only when all included predicates match within the declared revision and evidence scope.
No material missing, extra, contradictory, or unknown behavior can remain.
Passing tests alone do not prove exact implementation conformance.

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
artifact_kind: "test-execution-report"
id: "SAMPLE-REPORT-EXEC-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-TEST-001, SAMPLE-TEST-002, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-ENV-001]
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

# Invoice access execution report

## Run identity and provenance

```yaml
execution_id: null
execution_status: NOT_RUN
repository_id: SAMPLE-REPO-001
repository_revision: null
test_revision: null
environment_identity: null
started_at: null
completed_at: null
command_or_tool_reference: unknown
process_exit_status: null
actual_results: null
retained_execution_refs: []
```

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion location | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-TEST-001 | SAMPLE-REQ-001 / SAMPLE-AC-001 | null | Exactly one invoice with identifier INV-001 | null | NOT_RUN | null |
| SAMPLE-TEST-002 | SAMPLE-REQ-002 / SAMPLE-AC-002 | null | Zero invoices and message "Access denied" | null | NOT_RUN | null |

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

### AC to test case coverage

| Requirement/defect and AC version | Applicable predicate | Canonical case and required level | Inspected assertion and test revision/hash | Definition / assertion completeness | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 / SAMPLE-AC-001, sample-v1 | Return exactly owned INV-001 | Proposed SAMPLE-TEST-001; level unknown | unknown | Proposed / unknown | NOT_RUN | No executable assertion evidence |
| SAMPLE-REQ-002 / SAMPLE-AC-002, sample-v1 | Deny unpermitted access | Proposed SAMPLE-TEST-002; level unknown | unknown | Proposed / unknown | NOT_RUN | No executable assertion evidence |

### AC to code change coverage

| Requirement/defect and AC version | Intended predicate | Change ID or UNCHANGED | Exact old/new source locations | Conformance | Missing, extra, contradictory, or unknown behavior | Evidence and limit |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 / SAMPLE-AC-001, sample-v1 | Return exactly owned INV-001 | unknown | unknown | UNKNOWN | Implementation unavailable | No source inspection exists |
| SAMPLE-REQ-002 / SAMPLE-AC-002, sample-v1 | Deny unpermitted access | unknown | unknown | UNKNOWN | Implementation unavailable | No source inspection exists |

### Code change to test case coverage

The complete code-change inventory is unknown. This direction is `UNKNOWN`; no denominator can be calculated.
No code-to-test relationship or equivalence claim is established.

## Retained evidence inventory

| Evidence ID | Locator | Hash | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| null | null | null | null | No execution evidence exists |

## Verification conclusion

- Behavior claim: No business behavior is verified.
- Covered conditions: None. Both access tests remain NOT_RUN.
- Uncovered conditions: Permitted access, denied access, and runtime boundaries lack execution evidence.
- Evidence limits: Repository revision, test revision, assertion locations, environment identity, and retained results are null.
- Behavioral equality: UNKNOWN. No source comparison establishes missing or additional business behavior.

## Facts, inferences, and unresolved questions

- Facts: The sample context states that no test has executed.
- Inferences: None. Expected results do not establish actual behavior.
- Unresolved questions: The implementation, assertion code, and execution owner are unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| sample-context.md records no implementation revision or execution evidence | The report cannot support release acceptance | unknown | Inspect exact code and assertion revisions, then retain an authorized run |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only; no actual approval, implementation, or execution |
````

## Completion checks

- Browser reports bind every declared original and new case to its actual result.
- AC-to-test, AC-to-code-change, and code-change-to-test tables expose all included items and missing links.
- Declared inventories support each numerator, denominator, percentage, and test-level boundary.
- Definition coverage, inspected assertions, source conformance, and matching passing execution remain separate.
- Missing and additional unsupported behavior appear before any 100% equivalence claim.
- Browser identity, target revisions, source hashes, screenshots, and substitutions support each claimed boundary.
- Run metadata identifies exact code and test revisions, environment, and execution when available.
- Expected results and actual results occupy separate fields.
- Each verification claim cites inspected assertions and retained execution.
- Exit status, test outcome, and behavior verification remain separate.
- Missing evidence limits each associated claim.
- Replace every placeholder before use.
- Preserve evidence limits and pending reviews until supporting evidence exists.
