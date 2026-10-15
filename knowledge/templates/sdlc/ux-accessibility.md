# UX and accessibility specification

## Purpose

Specify user actions, screen states, content, and accessibility behavior.
Connect each interaction to observable acceptance criteria.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: personas, task goals, journeys, screen references, content rules, accessibility target, and requirement IDs.

Read the referenced design version before describing current screens.
State the accessibility standard, version, and conformance target when the project defines them.
Keep an absent target unresolved.
Specify keyboard behavior, focus, names, errors, and status announcements for each applicable interaction.
Distinguish proposed accessibility checks from measured conformance.

## Template

````markdown
---
artifact_kind: "ux-accessibility"
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

# {{experience_name}}

## Audience and task

| Field | Value |
| --- | --- |
| User and need | {{persona_and_task_goal}} |
| Preconditions | {{identity_permissions_and_initial_state}} |
| Scope and exclusions | {{included_steps_and_excluded_paths}} |
| Design source | {{design_locator_exact_version_and_frames_or_unknown}} |
| Accessibility target | {{standard_version_conformance_level_and_source_or_unknown}} |
| Supported contexts | {{devices_input_modes_languages_and_assistive_technology_scope}} |

## Journey and states

| Step or state | Trigger | Content and controls | Next state | Observable outcome |
| --- | --- | --- | --- | --- |
| {{initial_loading_success_empty_denied_or_error}} | {{user_or_system_trigger}} | {{labels_data_and_actions}} | {{next_state}} | {{measurable_result}} |

## Interaction and content rules

| Element | Accessible name and semantics | Keyboard and focus behavior | Validation or feedback | Source or proposal |
| --- | --- | --- | --- | --- |
| {{element_id}} | {{name_role_state_and_relationship}} | {{keys_focus_entry_exit_and_order}} | {{message_timing_and_recovery_action}} | {{evidence_or_proposed}} |

Sensitive content: {{visibility_masking_and_denied_content_rules}}.
Content rules: {{exact_messages_terms_and_localization_requirements}}.

## Accessibility verification

| Concern | Expected behavior or measure | Method and environment | Actual evidence | Result |
| --- | --- | --- | --- | --- |
| Keyboard | {{complete_task_and_focus_expectations}} | {{manual_method_and_environment}} | {{evidence_ref_or_null}} | NOT_RUN |
| Assistive technology | {{names_roles_status_and_reading_expectations}} | {{technology_version_and_method}} | {{evidence_ref_or_null}} | NOT_RUN |
| Visual presentation | {{contrast_zoom_reflow_and_target_limits_or_unknown}} | {{measurement_method}} | {{evidence_ref_or_null}} | NOT_RUN |

## Acceptance criteria and review

```gherkin
Feature: {{user_task}}
  @{{requirement_id}} @{{criterion_id}}
  Scenario: {{observable_interaction}}
    Given {{user_context_and_initial_state}}
    When {{one_user_action}}
    Then {{observable_result_with_measure}}
    And {{focus_content_or_error_result}}
```

Design review: {{pending_or_actual_review_reference}}.
Accessibility review: {{pending_or_actual_review_reference}}.
Known coverage limits: {{untested_contexts_and_missing_targets}}.

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
artifact_kind: "ux-accessibility"
id: "SAMPLE-UX-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-CONTRACT-001]
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

# View an invoice

## Audience and task

| Field | Value |
| --- | --- |
| User and need | Customer requests an owned invoice. |
| Preconditions | Customer identity available; ownership rule proposed. |
| Scope and exclusions | Owned and denied invoice requests; staff flow excluded. |
| Design source | unknown; no screen or design version inspected. |
| Accessibility target | unknown; obtain the project target. |
| Supported contexts | unknown; determine devices, languages, and assistive technology scope. |

## Journey and states

| Step or state | Trigger | Content and controls | Next state | Observable outcome |
| --- | --- | --- | --- | --- |
| Ready | Customer selects an invoice. | Invoice selection control; label requires design review. | Loading | Request addresses INV-001. |
| Loading | Request starts. | Proposed status message; exact text unknown. | Success, denied, or error | Completion state depends on response. |
| Success | Customer A receives permitted response. | Invoice INV-001. | Success | Exactly one invoice visible. |
| Denied | Customer B requests INV-001. | "Access denied"; no invoice content. | Denied | Zero invoices visible. |
| Empty | No invoice selection available. | Behavior unknown. | unknown | Obtain the empty-state requirement. |
| Error | Service request fails. | Recovery action and message unknown. | unknown | Obtain the failure-state requirement. |

## Interaction and content rules

| Element | Accessible name and semantics | Keyboard and focus behavior | Validation or feedback | Source or proposal |
| --- | --- | --- | --- | --- |
| Invoice selection | Proposed name includes invoice identifier; semantics require design. | Proposed keyboard activation; focus sequence unresolved. | Loading feedback requires design. | Illustrative design proposal. |
| Invoice result | Proposed heading identifies INV-001. | Focus movement requires reviewed interaction rules. | Display exactly one permitted invoice. | SAMPLE-REQ-001; interaction details proposed. |
| Access message | Proposed programmatic status; exact semantics unresolved. | Proposed discoverable feedback without a keyboard trap. | "Access denied"; zero invoices. | SAMPLE-REQ-002; interaction details proposed. |

Sensitive content: Do not display invoice content after denied access.
Content rules: Use "Access denied" for the illustrative denied result; localization rules remain unknown.

## Accessibility verification

| Concern | Expected behavior or measure | Method and environment | Actual evidence | Result |
| --- | --- | --- | --- | --- |
| Keyboard | Proposed: complete invoice selection and locate its result. | Manual method and environment unknown. | null | NOT_RUN |
| Assistive technology | Proposed: expose invoice names and access feedback. | Technology versions and test method unknown. | null | NOT_RUN |
| Visual presentation | Contrast, zoom, reflow, and target limits unknown. | Method requires an agreed accessibility target. | null | NOT_RUN |

## Acceptance criteria and review

```gherkin
Feature: View an invoice
  @SAMPLE-REQ-002 @SAMPLE-AC-002
  Scenario: Customer requests another customer's invoice
    Given Customer B has no permission to view INV-001
    When Customer B requests INV-001
    Then the portal displays zero invoices
    And the portal displays "Access denied"
```

Design review: pending; reviewer null.
Accessibility review: pending; reviewer null.
Known coverage limits: No screens, device tests, or accessibility measurements exist in this sample.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: The portal needs accessible feedback; detailed interactions require design review.
Unresolved questions: Which accessibility target and supported contexts apply? Owner unknown; obtain the project specification.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-UX-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | Accessibility acceptance cannot be measured against an agreed target. | unknown | Identify the accessibility owner and define testable interaction criteria. | open |
````

## Completion checks

- Cover loading, success, empty, denied, and failure states where applicable.
- Specify keyboard, focus, names, feedback, and sensitive content behavior.
- Use observable Gherkin outcomes and source-backed accessibility targets.
- Keep manual review, automated checks, and conformance claims separate.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
