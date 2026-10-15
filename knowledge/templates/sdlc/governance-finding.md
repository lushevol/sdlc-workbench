# Governance finding

## Purpose

Record a knowledge gap or conflict with evidence, consequence, responsibility, and a resolution action.

Read the [AI authoring contract](README.md) before use.
Read the [sample context](sample-context.md) before interpreting the example.

## AI instructions

- Name the affected artifact and version.
- Use the supported finding categories and severity values when transferring to Workbench.
- Distinguish missing evidence from a confirmed contradiction.
- Define the evidence needed to resolve the finding.
- Preserve unresolved findings until investigation supports resolution.

## Template

Copy this block. Replace placeholders and retain the required sections.

````markdown
---
artifact_kind: governance-finding
id: "{{artifact_id}}"
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

# {{finding_title}}

## Subject

| Artifact ID | Version | Category | Severity | Resolution |
| --- | --- | --- | --- | --- |
| {{subject_id}} | {{version}} | {{category}} | {{severity}} | open |

## Evidence

{{inspected_sources_revisions_locators_and_missing_evidence}}

## Consequence

{{specific_engineering_or_business_effect_with_evidence_limits}}

## Proposed action

| Action | Owner | Required evidence | Measurable resolution condition |
| --- | --- | --- | --- |
| {{action}} | unknown | {{evidence}} | {{observable_completion}} |

## Resolution

{{open_or_actual_resolution_with_evidence_and_review_reference}}

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| {{source_id}} | {{locator}} | {{revision_or_null}} | {{hash_or_null}} | {{actual_owner_and_authority_or_unknown}} | {{evidence_limit}} |

## Facts, inferences, and open questions

| Kind | Statement | Evidence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{fact_inference_or_unknown}} | {{statement}} | {{evidence_or_missing_source}} | unknown | {{action}} |
````

## Illustrative sample

This sample is fictional. It records no actual approval or execution.

````markdown
---
artifact_kind: governance-finding
id: "SAMPLE-FINDING-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
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

# Missing access policy owner

## Subject

| Artifact ID | Version | Category | Severity | Resolution |
| --- | --- | --- | --- | --- |
| SAMPLE-REQ-001 | 1 | review_required | info | open |

## Evidence

SAMPLE-SRC-001 contains illustrative access rules.
It identifies no actual business owner or approval authority.

## Consequence

The sample cannot establish approved access policy for engineering use.
This is a source-authority gap.

## Proposed action

| Action | Owner | Required evidence | Measurable resolution condition |
| --- | --- | --- | --- |
| Identify the access policy owner and request the applicable source. | unknown | Actual policy, owner identity, revision, and review evidence. | All required source and review references are recorded. |

## Resolution

open
No investigation result or human review is recorded.

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md | sample-v1 | null | unknown; illustrative only. | No actual policy owner or review is established. |

## Facts, inferences, and open questions

| Kind | Statement | Evidence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Fact about sample | The source states illustrative authority only. | SAMPLE-SRC-001, Authority. | unknown | Obtain the applicable business source. |
| Unknown | Actual approval authority is unavailable. | No actual reviewer or owner exists in this sample. | unknown | Identify the responsible owner. |
````

## Completion checks

- The finding identifies its subject and version.
- Evidence distinguishes absence from contradiction.
- The consequence stays within the inspected scope.
- The next action has an owner or explicit unknown owner.
- Resolution requires actual evidence and preserves the earlier finding.
