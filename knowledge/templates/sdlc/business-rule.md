# Business rule specification

## Purpose

Define one domain rule through conditions, outcomes, exceptions, and examples.
Keep policy authority separate from implementation observations.

## AI instructions

1. Obtain the policy source, rule owner, actors, terms, applicability conditions, outcomes, and exceptions.
2. Specify one stable rule ID for each independently changeable rule.
3. Define precedence when multiple rules can apply.
4. Link requirement IDs and glossary terms to the canonical rule.
5. Use concrete examples to expose ambiguity without inventing additional policy.
6. Do not infer business authority from code, sample data, or a passing test.

## Template

````markdown
---
artifact_kind: "business-rule"
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

# {{rule_title}}

## Source facts and authority

- Domain: {{domain}}
- Policy authority: {{authority_or_unknown}}
- Source facts: {{supported_facts}}
- Evidence limit: {{limit}}

## Proposed rule

- Rule ID: {{rule_id}}
- Applies to: {{actors_objects_and_context}}
- Required condition: {{precise_condition}}
- Required outcome: {{observable_outcome}}
- Forbidden outcome: {{forbidden_outcome_or_not_applicable}}
- Precedence: {{precedence_or_unknown}}
- Exceptions: {{exceptions_or_unknown}}

## Decision examples

| Example ID | Input conditions | Expected outcome | Rule IDs | Evidence or proposal basis |
| --- | --- | --- | --- | --- |
| {{example_id}} | {{conditions}} | {{observable_outcome}} | {{rule_ids}} | {{basis}} |

## Terms and related requirements

| Term or artifact ID | Meaning or relationship | Canonical location |
| --- | --- | --- |
| {{term_or_artifact_id}} | {{meaning_or_relationship}} | {{locator}} |

## Application and change boundary

- Effective conditions: {{effective_context_or_unknown}}
- Implementation observations: {{observations_with_exact_revision_or_none}}
- Change trigger: {{policy_or_context_trigger}}

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Unknowns and conflicts

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Human review

- Required review scope: {{policy_conditions_exceptions_and_precedence}}
- Actual decision reference: {{reference_or_null}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "business-rule"
id: "SAMPLE-RULE-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-REQ-001, SAMPLE-REQ-002, SAMPLE-RULE-002, SAMPLE-RULE-003]
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

# Permit customer access to an owned invoice

## Source facts and authority

- Domain: Customer invoice viewing.
- Policy authority: unknown; the context has illustrative authority only.
- Source facts: Customer A owns invoice INV-001.
- Evidence limit: No real invoice access policy exists in this sample.

## Proposed rule

- Rule ID: SAMPLE-RULE-001.
- Applies to: An authenticated customer requesting an invoice.
- Required condition: The customer owns the requested invoice.
- Required outcome: Permit the customer to view the owned invoice.
- Forbidden outcome: unknown for additional access paths; obtain policy evidence.
- Precedence: unknown; conflicting policy is unavailable.
- Exceptions: unknown; staff access and delegated access are undefined.

## Decision examples

| Example ID | Input conditions | Expected outcome | Rule IDs | Evidence or proposal basis |
| --- | --- | --- | --- | --- |
| SAMPLE-RULE-EXAMPLE-001 | Authenticated customer A requests owned invoice INV-001. | Permit viewing; SAMPLE-AC-001 defines the response. | SAMPLE-RULE-001 | Proposed behavior in sample-v1 |
| SAMPLE-RULE-EXAMPLE-002 | Customer B lacks permission for INV-001. | Deny viewing; SAMPLE-AC-002 defines the response. | SAMPLE-RULE-002, SAMPLE-RULE-003 | Related proposed rules in sample-v1 |

## Terms and related requirements

| Term or artifact ID | Meaning or relationship | Canonical location |
| --- | --- | --- |
| owned invoice | An invoice assigned to the requesting customer in this context. | [Domain glossary](domain-glossary.md) |
| SAMPLE-REQ-001 | Defines permitted access acceptance criteria. | [Requirement sample](requirement.md) |
| SAMPLE-REQ-002 | Defines denied access acceptance criteria. | [Sample context](sample-context.md) |

## Application and change boundary

- Effective conditions: Illustrative customer requests only; no production effective date exists.
- Implementation observations: none; no repository revision exists.
- Change trigger: A reviewed policy adds roles, exceptions, or a different ownership condition.

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Unknowns and conflicts

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Delegated and staff access are undefined. | The context provides no reviewed rule for these roles. | Their requests cannot receive a justified policy outcome. | unknown | Obtain the applicable policy before adding outcomes. |
| Policy authority is unknown. | The context identifies no actual owner. | The rule cannot establish approved intent. | unknown | Identify the policy owner and record human review. |

## Human review

- Required review scope: Ownership condition, applicability, exceptions, and precedence.
- Actual decision reference: null.
````

## Completion checks

- Define conditions and outcomes without ambiguous terms.
- Give each independently changeable rule a stable ID.
- State exceptions and precedence or record their absence as an unknown.
- Link each example to applicable rules.
- Keep policy authority separate from code evidence.
- Obtain required human review before publication.
