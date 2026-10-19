# Threat model and security review

## Purpose

Identify security boundaries, plausible misuse, proposed controls, and unresolved risks.
State evidence limits beside each threat and security claim.

## AI instructions

Read the [catalog contract](README.md) and [sample context](sample-context.md) before drafting.
Use the envelope as authoring metadata, without treating it as a supported Workbench record.
Read cited source contents and record their exact revisions.
Use `unknown`, `null`, and `NOT_RUN` when evidence is absent.
Separate proposals, source facts, and observed execution.
Keep findings actionable through evidence, consequence, owner, and next action.

Required inputs: data flows, trust boundaries, assets, identity rules, deployment context, security requirements, and inspected implementation revisions.

Model threats against a named asset and entry point.
Mark hypothetical threats as hypotheses.
Do not label a system vulnerable without supporting evidence.
Trace each control to an assertion and retained execution when available.
Keep residual risk decisions pending until the authorized owner records review.
Do not include real credentials or sensitive customer data.

## Template

````markdown
---
artifact_kind: "threat-model"
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

# {{system_or_change}} security review

## Scope and assumptions

| Field | Value |
| --- | --- |
| Included components and interfaces | {{ids_and_scope}} |
| Environment and revision | {{environment_and_exact_commits_or_unknown}} |
| Security requirements | {{requirement_ids_and_policy_sources}} |
| Exclusions and evidence limits | {{uninspected_components_and_missing_sources}} |
| Assumptions needing confirmation | {{assumptions_with_owners}} |

## Assets and trust boundaries

| Asset ID | Asset and sensitivity | Entry point | Trust boundary | Protection objective |
| --- | --- | --- | --- | --- |
| {{asset_id}} | {{data_identity_or_resource}} | {{interface_or_event}} | {{lower_to_higher_trust_transition}} | {{confidentiality_integrity_or_availability_goal}} |

## Threats and controls

| Threat ID | Misuse and preconditions | Evidence state | Consequence | Proposed or existing control | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| {{threat_id}} | {{actor_action_asset_and_conditions}} | {{hypothesis_or_observed_with_revision}} | {{concrete_effect}} | {{control_and_enforcement_point}} | {{owner_or_unknown}} | {{specific_validation_or_mitigation_action}} |

## Security verification

| Threat or requirement | Planned input or attack | Observable assertion | Test revision | Execution evidence | Result |
| --- | --- | --- | --- | --- | --- |
| {{threat_or_requirement_id}} | {{safe_test_input_and_authorized_scope}} | {{expected_result_and_limit}} | {{exact_test_revision_or_null}} | {{evidence_ref_or_null}} | NOT_RUN |

## Residual risks and review

| Risk | Remaining exposure and evidence limit | Decision owner | Decision | Review evidence |
| --- | --- | --- | --- | --- |
| {{risk}} | {{remaining_exposure}} | {{owner_or_unknown}} | pending | null |

Operational controls: {{logging_secret_handling_monitoring_and_incident_actions_or_unknown}}.
Review boundary: {{reviewed_scope_and_unreviewed_scope}}.

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
artifact_kind: "threat-model"
id: "SAMPLE-SEC-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-ARCH-001, SAMPLE-CONTRACT-001, SAMPLE-REQ-002]
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

# Invoice access security review

## Scope and assumptions

| Field | Value |
| --- | --- |
| Included components and interfaces | Proposed portal, SAMPLE-SVC-001, SAMPLE-STORE-001, and SAMPLE-CONTRACT-001. |
| Environment and revision | unknown; repository commit null. |
| Security requirements | SAMPLE-REQ-002 proposes denied access with zero invoices. |
| Exclusions and evidence limits | No implementation, deployment, identity provider, or logging source inspected. |
| Assumptions needing confirmation | Service receives trustworthy identity; owner unknown. |

## Assets and trust boundaries

| Asset ID | Asset and sensitivity | Entry point | Trust boundary | Protection objective |
| --- | --- | --- | --- | --- |
| SAMPLE-ASSET-001 | Invoice content; classification unknown. | GET /invoices/{invoice_id} | Requester to invoice service. | Prevent content disclosure after denied access. |
| SAMPLE-ASSET-002 | Customer identity and access relationship. | Identity mechanism unknown. | Identity source to invoice service. | Use valid identity and access information. |

## Threats and controls

| Threat ID | Misuse and preconditions | Evidence state | Consequence | Proposed or existing control | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-THREAT-001 | Customer B requests invoice INV-001 without permission. | Hypothesis based on SAMPLE-REQ-002; no defect observed. | Unauthorized invoice disclosure if access checks fail. | Proposed service check before content response. | unknown | Inspect access enforcement and execute denied-access assertions. |
| SAMPLE-THREAT-002 | Request supplies an untrusted customer identity. | Hypothesis; authentication design unknown. | Incorrect access decision if identity is trusted incorrectly. | Identity validation remains unspecified. | unknown | Inspect identity boundary and define rejection criteria. |
| SAMPLE-THREAT-003 | Diagnostic logs retain denied invoice content. | Hypothesis; no logs inspected. | Sensitive content could remain outside response controls. | Logging protection policy unknown. | unknown | Review log fields and retention policy. |

## Security verification

| Threat or requirement | Planned input or attack | Observable assertion | Test revision | Execution evidence | Result |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-THREAT-001; SAMPLE-REQ-002 | Customer B requests INV-001 in an authorized test environment. | HTTP 403; invoice count 0; "Access denied". | null | null | NOT_RUN |
| SAMPLE-THREAT-002 | Invalid identity input; exact case unresolved. | Expected rejection behavior unknown. | null | null | NOT_RUN |
| SAMPLE-THREAT-003 | Capture denied-request diagnostics in an authorized test environment. | Required masking and retention limits unknown. | null | null | NOT_RUN |

## Residual risks and review

| Risk | Remaining exposure and evidence limit | Decision owner | Decision | Review evidence |
| --- | --- | --- | --- | --- |
| Access enforcement unverified. | No source revision or execution confirms the control. | unknown | pending | null |
| Identity and logging controls unspecified. | Protection boundaries cannot be assessed. | unknown | pending | null |

Operational controls: Secret handling, monitoring, and incident procedures remain unknown.
Review boundary: This sample identifies hypotheses; no real security review or risk acceptance occurred.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative only; context read for this sample. |

Facts: The context defines proposed invoice access behavior.
Inferences: Missing access checks could disclose invoices; no vulnerability has been observed.
Unresolved questions: Who owns identity and logging policy? Owner unknown; obtain policy and implementation evidence.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-SEC-001-F01 | SAMPLE-SRC-001, sample-v1, Unknowns | Security hypotheses cannot be resolved or accepted. | unknown | Identify control owners and inspect exact revisions before security approval. | open |
````

## Completion checks

- Name each threat's asset, entry point, preconditions, and consequence.
- Distinguish hypotheses from confirmed weaknesses and observed exploitation.
- Assign each control an owner, next action, and measurable assertion.
- Keep security review and residual risk acceptance pending without real evidence.
- Replace all placeholders and explain each irrelevant section.
- Resolve all identifiers and source references within the stated evidence scope.
- Keep missing owners, revisions, review evidence, and execution results explicit.
- Keep review pending until an actual reviewer records a decision.
- Check links and writing; record only checks actually performed.
