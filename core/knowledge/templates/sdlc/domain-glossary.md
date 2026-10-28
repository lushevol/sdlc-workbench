# Domain glossary

## Purpose

Define stable business terms and identity boundaries for people and AI agents.
Resolve conflicting meanings through cited sources and responsible review.

## AI instructions

1. Obtain domain sources, their revisions, term owners, related concepts, and relevant requirement IDs.
2. Record the source meaning before proposing normalized wording.
3. Distinguish aliases from terms with different meanings.
4. Define repository, service, capability, contract, source, and tool identities separately.
5. Record ambiguous or conflicting definitions with consequences and next actions.
6. Do not invent accepted terminology, source authority, reviewer identity, or resolved conflicts.

## Template

Use the callout for each critical decision or blocker.
If none exists, use **No critical conclusions require user attention or action.**

````markdown
---
artifact_kind: "domain-glossary"
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

# {{domain_glossary_title}}

> **Critical conclusions: {{decision_or_blocker_requiring_attention}}.**
> Action: {{required_action}}. Consequence: {{impact_or_blocked_stage}}.
> Owner: {{accountable_owner_or_unknown}}. Evidence: {{supporting_evidence_link}}.

## Scope and source facts

- Domain: {{domain}}
- Included context: {{scope}}
- Excluded context: {{exclusions_and_reasons}}
- Evidence limit: {{coverage_limit}}

## Terms

| Term ID | Preferred term | Definition | Aliases | Excluded meanings | Source ID and locator | Review state |
| --- | --- | --- | --- | --- | --- | --- |
| {{term_id}} | {{preferred_term}} | {{precise_definition}} | {{aliases_or_none}} | {{excluded_meanings}} | {{source_reference}} | {{actual_review_state}} |

## Concept relationships

| Subject ID | Relationship | Object ID | Evidence | Limit |
| --- | --- | --- | --- | --- |
| {{subject_id}} | {{relationship}} | {{object_id}} | {{evidence}} | {{limit}} |

## Proposed wording and usage

| Term ID | Proposed usage rule | Rationale | Affected artifact IDs |
| --- | --- | --- | --- |
| {{term_id}} | {{usage_rule}} | {{rationale}} | {{artifact_ids}} |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| {{source_id}} | {{source_locator}} | {{revision_or_null}} | {{hash_or_null}} | {{source_owner_or_unknown}}; {{authority_and_limit}} |

## Ambiguities and unresolved questions

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| {{finding_or_question}} | {{evidence_or_missing_input}} | {{consequence}} | {{owner_or_unknown}} | {{action}} |

## Review and change control

- Required review scope: {{definitions_aliases_and_relationships}}
- Actual decision reference: {{reference_or_null}}
- Change trigger: {{source_or_domain_change}}
````

## Illustrative sample

Read [the sample context](sample-context.md) before using this example.
This sample records proposed content only.

````markdown
---
artifact_kind: "domain-glossary"
id: "SAMPLE-GLOSSARY-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: [SAMPLE-CAP-001, SAMPLE-SVC-001, SAMPLE-REPO-001, SAMPLE-CONTRACT-001]
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

# Invoice portal domain glossary

> **Critical conclusions: This example does not establish a real decision.**
> Action: obtain actual evidence and review before a real decision.
> Consequence: the sample cannot support that decision.
> Owner: unknown. Evidence: [illustrative sample context](sample-context.md).

## Scope and source facts

- Domain: Customer invoice viewing.
- Included context: The fictional portal, invoice ownership, and proposed service identities.
- Excluded context: Payment, invoice editing, and staff access; their meanings are unspecified.
- Evidence limit: Definitions apply only to sample-v1.

## Terms

| Term ID | Preferred term | Definition | Aliases | Excluded meanings | Source ID and locator | Review state |
| --- | --- | --- | --- | --- | --- | --- |
| SAMPLE-TERM-001 | customer | A portal user who requests an invoice in the sample. | none defined | Staff roles remain undefined. | SAMPLE-SRC-001; Product and identities | pending |
| SAMPLE-TERM-002 | owned invoice | An invoice assigned to the requesting customer in the sample. | none defined | Ownership does not define delegated access. | SAMPLE-SRC-001; Customer A owns INV-001. | pending |
| SAMPLE-TERM-003 | invoice service | The proposed service identified by SAMPLE-SVC-001. | none defined | It is separate from repository SAMPLE-REPO-001. | SAMPLE-SRC-001; Proposed design | pending |
| SAMPLE-TERM-004 | invoice viewing capability | The business responsibility identified by SAMPLE-CAP-001. | none defined | It does not identify deployed software. | SAMPLE-SRC-001; Product and identities | pending |
| SAMPLE-TERM-005 | invoice interface | The proposed interface identified by SAMPLE-CONTRACT-001. | none defined | It does not identify an execution tool. | SAMPLE-SRC-001; Product and identities | pending |

## Concept relationships

| Subject ID | Relationship | Object ID | Evidence | Limit |
| --- | --- | --- | --- | --- |
| Customer A | owns | INV-001 | SAMPLE-SRC-001; Product and identities | Fictional ownership only |
| SAMPLE-SVC-001 | proposes to provide | SAMPLE-CONTRACT-001 | SAMPLE-SRC-001; Proposed design | No deployment or runtime relationship is established. |
| SAMPLE-REPO-001 | remains distinct from | SAMPLE-SVC-001 | SAMPLE-SRC-001; Product and identities | No implementation mapping is available. |

## Proposed wording and usage

| Term ID | Proposed usage rule | Rationale | Affected artifact IDs |
| --- | --- | --- | --- |
| SAMPLE-TERM-002 | Use owned invoice for the customer ownership condition. | Stable wording reduces ambiguity. | SAMPLE-RULE-001, SAMPLE-REQ-001 |
| SAMPLE-TERM-003 | Use the service ID for service references. | Repository identity answers a different question. | SAMPLE-ARCH-001, SAMPLE-CONTRACT-001 |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SAMPLE-SRC-001 | [Illustrative context](sample-context.md) | sample-v1 | null | unknown; Illustrative intent only; no actual business approval. |

## Ambiguities and unresolved questions

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Delegated access has no definition. | The context defines customer ownership only. | Delegated scenarios cannot be interpreted reliably. | unknown | Obtain a reviewed delegated access definition. |
| Staff roles have no definition. | The context explicitly leaves staff access unknown. | Staff permissions remain unresolved. | unknown | Obtain the staff policy and role definitions. |

## Review and change control

- Required review scope: Domain terms, aliases, identity boundaries, and relationships.
- Actual decision reference: null.
- Change trigger: A source adds roles, changes ownership meaning, or changes identity relationships.
````

## Completion checks

- Give each term a stable ID and a precise definition.
- Cite each definition's source and applicable revision.
- Distinguish aliases from different concepts.
- Keep resource identities separate.
- Give every ambiguity evidence, consequence, owner, and next action.
- Update dependent artifacts when a reviewed meaning changes.
