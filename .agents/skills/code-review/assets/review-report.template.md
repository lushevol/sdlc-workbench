---
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Code review: {{change_title}}

{{critical_callout_or_No_critical_conclusions_require_user_attention_or_action}}

## Findings

### {{finding_id}}: [{{priority}}] {{actionable_title}}

Evidence: {{exact_changed_source_link_and_revision}}.
Trigger: {{concrete_input_or_state}}.
Consequence: {{observable_failure_and_supporting_source_link}}.
Owner: {{owner_or_unknown}}.
Next action: {{specific_correction}}.
Validation: {{focused_case_and_assertion_link_or_NOT_RUN}}.
Confidence and limits: {{fact_or_inference_and_unverified_condition}}.
Resolution: {{open_or_linked_correction_and_recheck_evidence}}.

## Comparison identity

| Field | Value |
| --- | --- |
| Repository | {{repository_id_and_locator}} |
| PR or issue | {{locator_or_unavailable}} |
| Review mode | {{worktree_staged_branch_range_or_supplied_patch}} |
| Requested base | {{ref_or_not_applicable}} |
| Base commit | {{full_commit_or_unborn}} |
| Comparison base | {{merge_base_or_exact_base_commit_or_empty_tree}} |
| Candidate | {{full_head_commit_or_worktree_or_index}} |
| Change fingerprint | {{sha256_or_patch_hash}} |
| Purpose and requirements | {{individual_definition_links_and_versions_or_unavailable}} |
| Task intake and current stage | {{links_and_revisions_or_not_applicable}} |
| Unrelated local changes | {{scope_and_exclusion_evidence_or_none}} |

## Review coverage

| Path or boundary | Exact source identity | Inspected behavior and consumers | Disposition and limit |
| --- | --- | --- | --- |
| {{individual_path_link}} | {{commit_or_content_hash}} | {{behavior_and_consumer_links}} | {{inspected_generated_binary_excluded_or_unavailable}} |

## Validation evidence

| Check | Command or inspected assertion | Revision and environment | Result | Retained evidence | Claim limit |
| --- | --- | --- | --- | --- | --- |
| {{check_name}} | {{exact_command_or_assertion_link}} | {{identity_and_environment}} | {{PASSED_FAILED_ERROR_NOT_RUN_UNAVAILABLE_or_NOT_APPLICABLE}} | {{individual_result_link_or_unavailable}} | {{scope_limit}} |

Compare coverage only when scope, tool configuration, and measurements are compatible.
Keep baseline failures and candidate failures separate.

## Open questions and actions

| Question or gap | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{question_or_gap}} | {{individual_source_link_or_missing_source}} | {{limited_claim_or_blocked_action}} | {{owner_or_unknown}} | {{resolution_action}} |

## Review outcome

Assessment: {{findings_present_no_actionable_findings_or_incomplete}}.
Material limits: {{uninspected_paths_missing_intent_unavailable_execution_and_skipped_scans_or_none}}.
Final identity check: {{matching_fingerprint_and_source_hashes_or_explained_change}}.
Human review decision: pending.
Approval evidence: null.

Replace all placeholders and remove unused repeated rows before saving.
For task reports, place the critical callout directly below the title.
Include its required action, consequence, owner, and evidence links.
Otherwise state: `No critical conclusions require user attention or action.`
Set writing review fields only from checks actually completed.
