# Knowledge topic / source assessment

## Purpose

Connect documented claims while assessing source authority, freshness, consistency, and evidence limits.

Read the [AI authoring contract](README.md) before use.
Read the [sample context](sample-context.md) before interpreting the example.

## AI instructions

- Read each cited source at its recorded revision.
- Retain raw bytes and manifest records before deriving knowledge.
- Separate source ownership, classification, and approval authority.
- Keep competing claims and unresolved findings visible.
- Use the supported KnowledgeTopic record for governed Workbench knowledge.

## Template

Copy this block. Replace placeholders and retain the required sections.

````markdown
---
artifact_kind: knowledge-source-assessment
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

# {{topic_title}}

## Scope

{{question_domain_and_exclusions}}

## Summary

{{supported_summary_with_claim_references}}

## Source assessment

| Source ID | Locator and revision | Hash or missing value | Owner and authority | Freshness | Limits |
| --- | --- | --- | --- | --- | --- |
| {{source_id}} | {{source_location_and_revision}} | {{hash_or_null}} | {{actual_authority_or_unknown}} | {{assessment_and_date}} | {{limits}} |

## Documented knowledge

| Claim ID | Kind | Claim | Supporting source and locator | Contradiction or limit |
| --- | --- | --- | --- | --- |
| {{claim_id}} | {{fact_proposed_intent_or_inference}} | {{claim}} | {{citation}} | {{limit}} |

## Connections

| Related ID | Relationship | Evidence |
| --- | --- | --- |
| {{related_id}} | {{relationship}} | {{supporting_reference}} |

## Evidence limits

{{coverage_missing_sources_authority_and_execution_limits}}

## Open questions

| Question or finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{question}} | {{available_or_missing_evidence}} | {{effect}} | unknown | {{action}} |
````

## Illustrative sample

This sample is fictional. It records no actual approval or execution.

````markdown
---
artifact_kind: knowledge-source-assessment
id: "SAMPLE-KNOWLEDGE-001"
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

# Invoice access knowledge

## Scope

Connect proposed customer access rules for the illustrative invoice portal.
Exclude staff policy and actual implementation behavior.

## Summary

The sample permits owned-invoice access and denies access without permission.
These claims describe illustrative intent only.

## Source assessment

| Source ID | Locator and revision | Hash or missing value | Owner and authority | Freshness | Limits |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | sample-context.md; sample-v1 | null | unknown; illustrative only. | Real applicability is unknown. | No business authority or registered snapshot. |

## Documented knowledge

| Claim ID | Kind | Claim | Supporting source and locator | Contradiction or limit |
| --- | --- | --- | --- | --- |
| SAMPLE-CLAIM-001 | Proposed intent | Permit owned-invoice access. | SAMPLE-SRC-001, Proposed behavior, SAMPLE-RULE-001. | Actual policy is missing. |
| SAMPLE-CLAIM-002 | Proposed intent | Denied access returns zero invoices. | SAMPLE-SRC-001, Proposed behavior, SAMPLE-RULE-003. | No execution evidence exists. |

## Connections

| Related ID | Relationship | Evidence |
| --- | --- | --- |
| SAMPLE-REQ-001 | Describes permitted access. | SAMPLE-RULE-001 in SAMPLE-SRC-001. |
| SAMPLE-REQ-002 | Describes denied access. | SAMPLE-RULE-002 and SAMPLE-RULE-003 in SAMPLE-SRC-001. |

## Evidence limits

No actual source authority, current implementation, or behavior verification is established.
No knowledge publication occurred.

## Open questions

| Question or finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Who owns access policy? | Owner is absent from the illustrative source. | Actual intent cannot be approved. | unknown | Identify the owner and obtain the applicable policy. |
| Does implementation enforce the policy? | Code revisions and execution are unavailable. | Behavior remains unverified. | unknown | Inspect exact code and retained assertions. |
````

## Completion checks

- Every significant claim has a source locator and revision.
- Source authority and freshness have explicit evidence limits.
- Facts, proposed intent, and inferences remain separate.
- Conflicting claims and missing sources remain visible.
- Governed records use actual provenance and required review.
