# Business / product requirements document

## Purpose

Summarize business needs, scope, and requirement coverage for a product or capability.
Reference detailed requirements as the canonical behavior definitions.

## AI instructions

1. Obtain the product brief, user groups, capability IDs, business objectives, and detailed requirement versions.
2. Summarize needs without copying conflicting versions of detailed business rules.
3. Map each business need to requirement IDs and their acceptance criterion IDs.
4. Record missing requirements, unresolved conflicts, and exclusions explicitly.
5. Use the [requirement template](requirement.md) for detailed descriptions and measurable Gherkin criteria.
6. Do not invent demand, priorities, sources, business approval, or implementation status.

## Template

````markdown
---
artifact_kind: "business-product-requirements"
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

# {{requirements_summary_title}}

## Business context and source facts

- Problem: {{supported_business_problem}}
- Users and stakeholders: {{users_and_stakeholders}}
- Capability IDs: {{capability_ids}}
- Source facts: {{supported_context}}
- Evidence limit: {{source_limit}}

## Proposed business objectives

| Objective ID | Desired outcome | Measure and target | Basis | Owner |
| --- | --- | --- | --- | --- |
| {{objective_id}} | {{outcome}} | {{measure_or_unknown}} | {{source_or_proposal}} | {{owner_or_unknown}} |

## Scope

| Included capability | Excluded capability | Reason |
| --- | --- | --- |
| {{included_capability}} | {{excluded_capability}} | {{reason}} |

## Requirement index and coverage

| Business need ID | Need summary | Detailed requirement ID and version | Acceptance criterion IDs | Priority and basis | Canonical location |
| --- | --- | --- | --- | --- | --- |
| {{need_id}} | {{need_summary}} | {{requirement_id_and_version}} | {{criterion_ids}} | {{priority_and_source_or_unknown}} | {{canonical_locator}} |

## Rules and constraints index

| Rule or constraint ID | Relationship to requirements | Canonical location | Status |
| --- | --- | --- | --- |
| {{rule_or_constraint_id}} | {{requirement_relationship}} | {{canonical_locator}} | {{actual_status}} |

## Dependencies and related artifacts

| Artifact ID | Relationship | Location | Evidence limit |
| --- | --- | --- | --- |
| {{artifact_id}} | {{relationship}} | {{locator}} | {{limit}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Conflicts and unresolved questions

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Review and change control

- Required review scope: {{objectives_scope_coverage_and_priority}}
- Actual review reference: {{reference_or_null}}
- Change trigger: {{trigger_for_requirement_baseline_review}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "business-product-requirements"
id: "SAMPLE-BPR-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CHARTER-001, SAMPLE-CAP-001, SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-NFR-001]
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

# Invoice portal requirements summary

## Business context and source facts

- Problem: The fictional portal needs a defined customer invoice viewing capability.
- Users and stakeholders: Customer A, Customer B, and an unidentified invoice policy owner.
- Capability IDs: SAMPLE-CAP-001.
- Source facts: Customer A owns INV-001; Customer B has no permission to view INV-001.
- Evidence limit: These facts describe the fictional context only.

## Proposed business objectives

| Objective ID | Desired outcome | Measure and target | Basis | Owner |
| --- | --- | --- | --- | --- |
| SAMPLE-OBJECTIVE-001 | Permit owned invoice viewing. | SAMPLE-AC-001 | Proposed intent in sample-v1 | unknown |
| SAMPLE-OBJECTIVE-002 | Prevent invoice content after denied access. | SAMPLE-AC-002 | Proposed intent in sample-v1 | unknown |

## Scope

| Included capability | Excluded capability | Reason |
| --- | --- | --- |
| Customer invoice viewing | Invoice editing, payment, and staff access | The context defines no reviewed behavior for these capabilities. |

## Requirement index and coverage

| Business need ID | Need summary | Detailed requirement ID and version | Acceptance criterion IDs | Priority and basis | Canonical location |
| --- | --- | --- | --- | --- | --- |
| SAMPLE-NEED-001 | View an owned invoice. | SAMPLE-REQ-001; illustrative version sample-v1 | SAMPLE-AC-001 | unknown; no ranking exists. | [Requirement sample](requirement.md) |
| SAMPLE-NEED-002 | Deny unauthorized invoice access. | SAMPLE-REQ-002; illustrative version sample-v1 | SAMPLE-AC-002 | unknown; no ranking exists. | [Sample context](sample-context.md) |
| SAMPLE-NEED-003 | Define authorized response performance. | SAMPLE-NFR-001; illustrative version sample-v1 | SAMPLE-NFR-AC-001 | unknown; no ranking exists. | [Nonfunctional requirement](nonfunctional-requirement.md) |

## Rules and constraints index

| Rule or constraint ID | Relationship to requirements | Canonical location | Status |
| --- | --- | --- | --- |
| SAMPLE-RULE-001 | Supports SAMPLE-REQ-001. | [Business rule sample](business-rule.md) | proposed |
| SAMPLE-RULE-002 | Supports SAMPLE-REQ-002. | [Sample context](sample-context.md) | proposed |
| SAMPLE-RULE-003 | Supports SAMPLE-REQ-002. | [Sample context](sample-context.md) | proposed |

## Dependencies and related artifacts

| Artifact ID | Relationship | Location | Evidence limit |
| --- | --- | --- | --- |
| SAMPLE-CHARTER-001 | Supplies proposed scope. | [Project charter](project-charter.md) | No actual sponsor decision exists. |
| SAMPLE-CAP-001 | Identifies the invoice viewing capability. | [Sample context](sample-context.md) | The ID establishes no deployed relationship. |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Conflicts and unresolved questions

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Staff access policy is missing. | The context lists staff access as unknown. | Staff scenarios cannot be defined. | unknown | Obtain a reviewed staff access rule. |
| Requirement priorities are unavailable. | The context supplies no ranking. | Delivery order cannot be justified by priority. | unknown | Obtain a reviewed priority decision. |

## Review and change control

- Required review scope: Business objectives, scope, requirement coverage, and priority.
- Actual review reference: null.
- Change trigger: A source, rule, or referenced requirement changes.
````

## Completion checks

- Map every stated business need to detailed requirements or an explicit gap.
- Link acceptance criteria by stable IDs.
- Keep detailed rules in their canonical artifacts.
- Check referenced versions and locations.
- Keep proposed priorities separate from actual decisions.
- Obtain required human review before publishing important requirements.
