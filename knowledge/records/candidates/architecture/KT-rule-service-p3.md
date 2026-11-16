---
type: KnowledgeTopic
id: KT-rule-service-p3
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Ratan-rule-service reconstruction for rule-engine/page.md
  revision: sha256:080321ebfefdc499c603a9ebbee46a305cced36be66ac2f5f088cbedaf1fcbce
  sha256: 080321ebfefdc499c603a9ebbee46a305cced36be66ac2f5f088cbedaf1fcbce
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    Rule Service Technical Design/page.md
  revision: sha256:dd48feabb7b2cecd53cd6c5f400f093c06642507a86703fcb6d59d79f00cca58
  sha256: dd48feabb7b2cecd53cd6c5f400f093c06642507a86703fcb6d59d79f00cca58
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Technology
    Selection - Rule Engine/RATAN Rule Engine - [Archived]/Drools Implementation -
    CN Rule Service/page.md
  revision: sha256:ee649a9b29c6a45c7095c1b8f77d7454131f4434964ce343edaa2a6ceb66d3f3
  sha256: ee649a9b29c6a45c7095c1b8f77d7454131f4434964ce343edaa2a6ceb66d3f3
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Technology
    Selection - Rule Engine/RATAN Rule Engine - [Archived]/RATAN Rule Engine Overview/page.md
  revision: sha256:72294d0007738c2e3a0a888e19757645f78fece60bedbcc42e7ed27cf51e5cb7
  sha256: 72294d0007738c2e3a0a888e19757645f78fece60bedbcc42e7ed27cf51e5cb7
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Technology
    Selection - Rule Engine/RATAN Rule Engine - [Archived]/Rule Service Migration/page.md
  revision: sha256:6d2cb806abdafa2933f40c801a306efe947f49fc234e81c9d2827f261162bbb3
  sha256: 6d2cb806abdafa2933f40c801a306efe947f49fc234e81c9d2827f261162bbb3
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Technology
    Selection - Rule Engine/RATAN Rule Engine - [Archived]/Rule Service Tech Design/page.md
  revision: sha256:f965902ddc7793c23d5e4d0282c8feeb984431126036a0860533188f28f1cdae
  sha256: f965902ddc7793c23d5e4d0282c8feeb984431126036a0860533188f28f1cdae
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Technology
    Selection - Rule Engine/page.md
  revision: sha256:fb9b1fcc817d58c742296b04d417fc3436014bbf1620e52701710d277a155347
  sha256: fb9b1fcc817d58c742296b04d417fc3436014bbf1620e52701710d277a155347
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:31:50.739559+08:00'
verified: []
scope: Historical selected-source design for rule service p3.
classification: architecture
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which rule design, service ownership, rule vocabulary, and API revision govern each
  current flow?
- What exact adapters preserve existing SCBML callers, exception semantics, entitlements,
  and rule-result behavior during migration?
- What are the final execution-flag spelling, status enum, field omission, and version
  contracts?
- Which consistency, dry-run activation, cache freshness, and publication-retry guarantees
  are approved?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Rule service p3

## Scope

Historical selected-source design for rule service p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Historical NSTP governance

The NSTP design supports user expressions, exception categories, and operation levels.
Rule creation and deletion require maker/checker control before taking effect.
Inbound messages are checked against active NSTP rules.
Matched exceptions are published for user resolution.

Sources: [original lines 15–25](../../../evidence/sources/sha256/dd48feabb7b2cecd53cd6c5f400f093c06642507a86703fcb6d59d79f00cca58.md#L15-L25).

### Exception operation levels

Maker-only exceptions start PENDING_OPERATOR and close after successful maker submission.
Checker-only exceptions start PENDING_VERIFICATION and close after successful approval.
Maker/checker exceptions move from PENDING_OPERATOR to PENDING_VERIFICATION before approval closes them.
Affirmation and back-value input requires double-blind checker verification before changing the SCBML message.

Sources: [original lines 27–39](../../../evidence/sources/sha256/dd48feabb7b2cecd53cd6c5f400f093c06642507a86703fcb6d59d79f00cca58.md#L27-L39), [original lines 80–90](../../../evidence/sources/sha256/dd48feabb7b2cecd53cd6c5f400f093c06642507a86703fcb6d59d79f00cca58.md#L80-L90).

### Domain fact and rule-engine separation

The reconstruction proposal routes validation through domain services before the shared rule service.
Domains convert SCBML to JSON and supply additional facts for special rules.
The shared engine maintains NSTP, netting, suppression, and Swift-suppression rules.
NSTP maintenance carries exception information in metaData.

The archived overview separately proposes moving domain-specific data retrieval and validation outside the shared engine.

Sources: [original lines 15–50](../../../evidence/sources/sha256/080321ebfefdc499c603a9ebbee46a305cced36be66ac2f5f088cbedaf1fcbce.md#L15-L50), [original lines 176–203](../../../evidence/sources/sha256/72294d0007738c2e3a0a888e19757645f78fece60bedbcc42e7ed27cf51e5cb7.md#L176-L203).

### Historical consolidation boundaries

The archived migration proposes consolidating CN and BAU rule maintenance and validation in ratanone-rule-service.
Business flow and rule type distinguish rule sets.
Data entitlement remains a standalone service outside that migration.
The recorded responses place field services and frontend validation in static-data service.

They keep profile limitation in the rule domain.
These migration responses do not establish present ownership.

Sources: [original lines 1–48](../../../evidence/sources/sha256/6d2cb806abdafa2933f40c801a306efe947f49fc234e81c9d2827f261162bbb3.md#L1-L48), [original lines 78–132](../../../evidence/sources/sha256/6d2cb806abdafa2933f40c801a306efe947f49fc234e81c9d2827f261162bbb3.md#L78-L132).

### Rule syntax and effective status

The archived overview permits AND between ungrouped conditions and OR inside groups.
Different rules have an OR relationship.
Its running states are SAVE_CONFIRMED and DELETE_PENDING.
The syntax and state definitions remain historical source-specific intent.

Sources: [original lines 98–140](../../../evidence/sources/sha256/72294d0007738c2e3a0a888e19757645f78fece60bedbcc42e7ed27cf51e5cb7.md#L98-L140), [original lines 152–158](../../../evidence/sources/sha256/72294d0007738c2e3a0a888e19757645f78fece60bedbcc42e7ed27cf51e5cb7.md#L152-L158).

### Rule storage and versioned interfaces

The archived design separates user-maintained rules from generated Drools rule content.
Execution loads rule content by business flow and rule type.
The v2 validation request separates logical-model facts from additional facts.
An SCBML adaptor is proposed for cashflow and trade types.

The batch-validation proposal limits the request list to 400 entries.
Maintenance provides rule retrieval, histories, status changes, and special-rule enable/disable operations.

Sources: [original lines 18–28](../../../evidence/sources/sha256/f965902ddc7793c23d5e4d0282c8feeb984431126036a0860533188f28f1cdae.md#L18-L28), [original lines 53–138](../../../evidence/sources/sha256/f965902ddc7793c23d5e4d0282c8feeb984431126036a0860533188f28f1cdae.md#L53-L138).

### Engine selection and migration are proposals

The selected engine conclusion proposes Drools.
The archived CN PoC scopes NSTP rule implementation.
The migration documents require source-rule inventories and affected consumer adaptation.
The archived overview retains v1 initially while proposing later decommissioning.

These passages do not approve endpoint removal or prove migration compatibility.

Sources: [original lines 474–476](../../../evidence/sources/sha256/fb9b1fcc817d58c742296b04d417fc3436014bbf1620e52701710d277a155347.md#L474-L476), [original lines 46–48](../../../evidence/sources/sha256/ee649a9b29c6a45c7095c1b8f77d7454131f4434964ce343edaa2a6ceb66d3f3.md#L46-L48), [original lines 78–94](../../../evidence/sources/sha256/6d2cb806abdafa2933f40c801a306efe947f49fc234e81c9d2827f261162bbb3.md#L78-L94), [original lines 192–194](../../../evidence/sources/sha256/6d2cb806abdafa2933f40c801a306efe947f49fc234e81c9d2827f261162bbb3.md#L192-L194), [original lines 198–204](../../../evidence/sources/sha256/6d2cb806abdafa2933f40c801a306efe947f49fc234e81c9d2827f261162bbb3.md#L198-L204), [original lines 212–222](../../../evidence/sources/sha256/72294d0007738c2e3a0a888e19757645f78fece60bedbcc42e7ed27cf51e5cb7.md#L212-L222).

### Consistency responsibilities in the archived proposal

The archived CN discussion requires consistency if rules move from PostgreSQL loading to Redis cache loading.
It identifies database persistence followed by failed Kafka publication as an unresolved consistency case.
It suggests a transactional outbox for investigation.
That suggestion does not establish an adopted delivery guarantee.

Sources: [original lines 13–19](../../../evidence/sources/sha256/ee649a9b29c6a45c7095c1b8f77d7454131f4434964ce343edaa2a6ceb66d3f3.md#L13-L19), [original lines 38–44](../../../evidence/sources/sha256/ee649a9b29c6a45c7095c1b8f77d7454131f4434964ce343edaa2a6ceb66d3f3.md#L38-L44).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

Four selected source pages are explicitly archived. Their proposals do not establish current applicability.

## Open questions

Owner: unknown.

- Which rule design, service ownership, rule vocabulary, and API revision govern each current flow?
- What exact adapters preserve existing SCBML callers, exception semantics, entitlements, and rule-result behavior during migration?
- What are the final execution-flag spelling, status enum, field omission, and version contracts?
- Which consistency, dry-run activation, cache freshness, and publication-retry guarantees are approved?
