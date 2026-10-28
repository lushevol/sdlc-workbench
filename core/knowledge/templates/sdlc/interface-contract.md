# API, event, and integration contract

## Purpose

Specify an interface so independent consumers and providers can implement compatible behavior.
State validation, access, output, and failure behavior explicitly.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: provider and consumer IDs, interface type, operations, schemas, authentication rules, failure rules, and compatibility expectations.

Inspect existing contracts at exact repository revisions before describing current behavior.
Use a complete Git commit hash for repository contract evidence.
Keep undocumented interfaces as candidates with a documentation gap.
Describe each input, output, error, permission, and delivery condition.
State unresolved rules instead of choosing undocumented defaults.
Separate expected responses from contract test results.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "interface-contract"
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

# {{interface_name}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Contract identity and boundary

| Field | Value |
| --- | --- |
| Contract ID and type | {{contract_id_and_http_graphql_messaging_ui_data_or_deployment}} |
| Contract maturity | {{candidate_or_documented_with_evidence}} |
| Provider IDs | {{provider_service_ids}} |
| Consumer IDs | {{consumer_ids}} |
| Relationship evidence | {{declared_static_or_runtime_evidence_and_limits}} |
| Repository ID | {{repository_id_or_unknown}} |
| Source path and lines | {{exact_contract_location_or_unknown}} |
| Full Git commit | {{full_commit_hash_or_null}} |
| Documentation gap | {{gap_or_not_applicable_with_reason}} |

## Operations and delivery

| Operation | Transport and address | Trigger | Side effects | Ordering, retry, timeout, and idempotency |
| --- | --- | --- | --- | --- |
| {{operation_id}} | {{method_path_topic_or_boundary}} | {{request_or_event_trigger}} | {{effects_or_none_with_source}} | {{explicit_delivery_rules_or_unknown}} |

## Inputs

| Name and location | Type or schema | Required | Validation and limits | Example |
| --- | --- | --- | --- | --- |
| {{input_name_and_path_header_body_or_message_location}} | {{type_and_schema_revision}} | {{yes_or_no}} | {{allowed_values_size_and_missing_behavior}} | {{nonsecret_example}} |

## Authentication and authorization

Authentication: {{identity_mechanism_credentials_and_expiry_rules_or_unknown}}.
Authorization: {{required_permission_scope_resource_rule_and_enforcement_point}}.
Sensitive data: {{fields_masking_logging_and_retention_rules_or_unknown}}.

## Outputs

| Condition | Status or event | Schema and required fields | Observable count or effect | Example |
| --- | --- | --- | --- | --- |
| {{success_condition}} | {{status_code_or_event_name}} | {{schema_and_nullability}} | {{observable_result}} | {{response_example}} |

## Errors

| Failure condition | Status or error code | Response content | Side effects and retry guidance |
| --- | --- | --- | --- |
| {{unauthenticated_unauthorized_invalid_missing_or_dependency_failure}} | {{code_or_unknown}} | {{schema_message_and_data_exclusions}} | {{effects_retry_rules_and_limits}} |

## Compatibility and verification

Version policy: {{version_negotiation_and_breaking_change_definition}}.
Deprecation policy: {{notice_period_migration_owner_and_end_condition_or_unknown}}.
Quality target: {{metric_target_unit_load_interval_and_sources_or_unknown}}.

| Requirement or rule | Contract assertion | Test revision | Retained execution | Result |
| --- | --- | --- | --- | --- |
| {{requirement_or_rule_id}} | {{input_and_observable_output_assertion}} | {{test_path_and_exact_revision_or_null}} | {{execution_ref_or_null}} | NOT_RUN |

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
artifact_kind: "interface-contract"
id: "SAMPLE-CONTRACT-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-SVC-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-NFR-001]
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

# Invoice lookup interface

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Contract identity and boundary

| Field | Value |
| --- | --- |
| Contract ID and type | SAMPLE-CONTRACT-001; http. |
| Contract maturity | candidate; illustrative proposal. |
| Provider IDs | SAMPLE-SVC-001. |
| Consumer IDs | SAMPLE-UI-001; proposed portal. |
| Relationship evidence | Proposed design only; no runtime observation. |
| Repository ID | SAMPLE-REPO-001; implementation mapping unknown. |
| Source path and lines | unknown |
| Full Git commit | null |
| Documentation gap | No inspected implementation contract or schema. |

## Operations and delivery

| Operation | Transport and address | Trigger | Side effects | Ordering, retry, timeout, and idempotency |
| --- | --- | --- | --- | --- |
| SAMPLE-OP-001 | GET /invoices/{invoice_id} | Customer requests an invoice. | Intended read operation; implementation unknown. | unknown; obtain explicit rules. |

## Inputs

| Name and location | Type or schema | Required | Validation and limits | Example |
| --- | --- | --- | --- | --- |
| invoice_id; path | Identifier representation unknown. | yes; proposed operation address. | Format, maximum length, and missing behavior unknown. | INV-001 |
| Customer identity; mechanism unknown | Schema unknown. | Required by proposed access rule. | Identity validation and expiry unknown. | Customer A; no real credentials. |
| Request body | Schema unknown. | unknown | Confirm whether the operation permits a body. | null |

## Authentication and authorization

Authentication: Identity mechanism, credentials, and expiry rules remain unknown.
Authorization: SAMPLE-SVC-001 checks invoice access before returning content.
Sensitive data: Invoice content needs protection; logging and retention rules remain unknown.

## Outputs

| Condition | Status or event | Schema and required fields | Observable count or effect | Example |
| --- | --- | --- | --- | --- |
| Customer A requests owned invoice INV-001. | HTTP 200 | Invoice identifier required; complete schema unknown. | Exactly one invoice. | Invoice identifier INV-001. |

## Errors

| Failure condition | Status or error code | Response content | Side effects and retry guidance |
| --- | --- | --- | --- |
| Customer B lacks invoice permission. | HTTP 403; proposed. | Zero invoices; "Access denied". | Mutation and retry policy unknown. |
| Identity absent or expired. | unknown | unknown; obtain reviewed rule. | unknown |
| Identifier invalid or invoice missing. | unknown | unknown; obtain reviewed rule. | unknown |
| Invoice store unavailable. | unknown | unknown; obtain failure contract. | unknown |

## Compatibility and verification

Version policy: unknown; no deployed contract exists in this sample.
Deprecation policy: unknown; obtain the responsible owner's policy.
Quality target: p95 <=500 ms with 20 concurrent customers after a two-minute warmup, measured for 10 minutes.
Measure successful authorized requests from service receipt to response completion.

| Requirement or rule | Contract assertion | Test revision | Retained execution | Result |
| --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 | HTTP 200; invoice count 1; identifier INV-001. | null | null | NOT_RUN |
| SAMPLE-REQ-002 | HTTP 403; invoice count 0; "Access denied". | null | null | NOT_RUN |

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: The proposed operation needs explicit identity and failure schemas before independent implementation.
Unresolved questions: What handles invalid identifiers and unavailable storage? Owner unknown; obtain the failure contract.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-CONTRACT-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | Consumers cannot implement consistent failure handling. | unknown | Resolve failure rules and inspect the contract at a full repository commit. | open |
````

## Completion checks

- Describe every operation's inputs, outputs, access rules, errors, and delivery semantics.
- Distinguish candidate contract documentation from inspected code evidence.
- Record a complete repository commit when claiming an existing contract version.
- Keep compatibility policy and contract test execution separate.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
