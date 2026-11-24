---
type: KnowledgeTopic
id: KT-settlement-exception-workflow-20261115
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Exception
    Handling/page.md
  revision: sha256:2f8bcf6aa3d39be8f369b85dc8a81d7603ffd1262ea4a6b232968a915eb077b2
  sha256: 2f8bcf6aa3d39be8f369b85dc8a81d7603ffd1262ea4a6b232968a915eb077b2
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Multiple
    Exception Handling Design/page.md
  revision: sha256:700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb
  sha256: 700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Multi-Exception Handling - Bulk Submit Approve
    Reject Tech Design/Batch Limitation Check API Doc/page.md
  revision: sha256:93154cdf31ba0b250c05d954a697b6cb0db47bc6560ee09f23392d57b36ccfee
  sha256: 93154cdf31ba0b250c05d954a697b6cb0db47bc6560ee09f23392d57b36ccfee
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Multi-Exception Handling - Bulk Submit Approve
    Reject Tech Design/Bulk Approve performance check result/page.md
  revision: sha256:dc8c2d7475f75bd042301ec771eb109b8d18be86a8e9c4033451e0b96306fbb5
  sha256: dc8c2d7475f75bd042301ec771eb109b8d18be86a8e9c4033451e0b96306fbb5
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Multi-Exception Handling - Bulk Submit Approve
    Reject Tech Design/page.md
  revision: sha256:bada207c2effbc004824d3f30f0eb87e1313382768455c78569f9f7a9da051ed
  sha256: bada207c2effbc004824d3f30f0eb87e1313382768455c78569f9f7a9da051ed
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    common Compensation Solution/page.md
  revision: sha256:67b4e58a130d3dd164236844ab3844a0c9e49fc20c73d41a1affe44ed9076cd0
  sha256: 67b4e58a130d3dd164236844ab3844a0c9e49fc20c73d41a1affe44ed9076cd0
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:28:03.144076+08:00'
verified: []
scope: Historical selected-source design for settlement exception workflow 20261115.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which exception workflow revision governs each business flow, including cross-cashflow
  approval and the 1000-item bulk proposal?
- What are the batch identity field, aggregate-success meaning, authorization rules,
  and applicable amount comparison?
- Which recovery owners, alert thresholds, compensation actions, and reinstatement
  conditions are approved?
- Which maker/checker state behavior governs cancel-deleting rules, adhoc SSI changes
  during other pending exceptions, and partial failures?
- Is asynchronous Camunda task completion intended, or must completion coordinate
  synchronously?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement exception workflow 20261115

## Scope

Historical selected-source design for settlement exception workflow 20261115.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Combined exception resolution

The historical design presents business exceptions together in cashflow details and the blotter.
Makers submit changes. Checkers approve or reject them.
Successful fixes remain effective when another exception fails.
Failed exceptions remain pending for the operator.

Sources: [original lines 1–34](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L1-L34), [original lines 40–81](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L40-L81).

### Manual-touch affirmation and separation

The historical design allows single-level affirmation.
Above USD 100 million, checker-only affirmation applies after settlements manual touch.
Confirmation-team manual touch does not satisfy that condition.
Without other exceptions, the amount alone does not prevent STP.

The user who unnets a gross-client cashflow cannot accept its unnet exception.

Sources: [original lines 40–81](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L40-L81).

### Payment and instruction controls

Previously sent payments must not regenerate through exception resolution.
The design directs manual resend through AMH.
Cover flags and mandatory currency validation belong at settlement-instruction input.
They are not separate exceptions in this design.

Sources: [original lines 40–81](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L40-L81).

### Workflow and exception contracts

The domain workflow envelope carries exception identifiers and statuses through metadataList.
Common statuses are PENDING_OPERATOR, PENDING_VERIFICATION, and CLOSED.
The maker and checker endpoints use /v1/camunda/task/{businessType}/maker and /checker.
The design requires synchronous exception creation and updates.

Exception records bind cashflow identity, business version, version, and optional minor version.

Sources: [original lines 96–142](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L96-L142), [original lines 203–211](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L203-L211), [original lines 283–306](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L283-L306), [original lines 308–526](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L308-L526).

### Adhoc instruction amendment

The design creates a CLOSED Adhoc SSI dummy exception after successful instruction stamping.
This includes stamping with only secondary or not-match conditions.
Maker Submit requests verification. Checker Reject returns the exception to the operator.
The workflow must allow the specified actions on this closed exception.

Sources: [original lines 308–526](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L308-L526).

### Historical recovery responsibilities

The recovery matrix assigns missing upstream cashflow replay to operations.
It proposes alerts and investigation for delayed groups and failed status writeback.
It requires dependency recovery before reinstating affected technical failures.
For lifecycle, adapter, or Camunda failures, the proposed recovery avoids Kafka commit and reconsumes after restart.

The common-compensation note requests graceful recovery after maximum retries, without defining a complete compensation contract.

Sources: [original lines 1–17](../../../evidence/sources/sha256/2f8bcf6aa3d39be8f369b85dc8a81d7603ffd1262ea4a6b232968a915eb077b2.md#L1-L17), [original lines 1–3](../../../evidence/sources/sha256/67b4e58a130d3dd164236844ab3844a0c9e49fc20c73d41a1affe44ed9076cd0.md#L1-L3), [original lines 9–9](../../../evidence/sources/sha256/67b4e58a130d3dd164236844ab3844a0c9e49fc20c73d41a1affe44ed9076cd0.md#L9-L9).

### Bulk processing remains a separate proposal

The multiple-exception design prohibits approval across cashflows.
A separate bulk proposal targets submit, approve, and reject across cashflows.
It proposes batched downstream lookups and a 1000-item affirmation threshold.
These source-specific designs do not establish which rule supersedes the other.

Sources: [original lines 1–34](../../../evidence/sources/sha256/700c9e221057a27071103b716296f82ae17fc4971451ac0a2952a1635918e8eb.md#L1-L34), [original lines 5–19](../../../evidence/sources/sha256/bada207c2effbc004824d3f30f0eb87e1313382768455c78569f9f7a9da051ed.md#L5-L19), [original lines 41–43](../../../evidence/sources/sha256/bada207c2effbc004824d3f30f0eb87e1313382768455c78569f9f7a9da051ed.md#L41-L43), [original lines 52–52](../../../evidence/sources/sha256/bada207c2effbc004824d3f30f0eb87e1313382768455c78569f9f7a9da051ed.md#L52-L52).

### Batch limitation contract ambiguity

The batch limitation proposal uses POST /v1/profileLimitation/checkLimitationsBatch.
Each item supplies currency and decimal amount.
The contract initially names referenceId, while later examples use cashflowId.
The response provides item results and an aggregate result.

One example reports aggregate success despite an item failure.
Empty input returns success false and the reason Request items cannot be empty.

Sources: [original lines 1–142](../../../evidence/sources/sha256/93154cdf31ba0b250c05d954a697b6cb0db47bc6560ee09f23392d57b36ccfee.md#L1-L142).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which exception workflow revision governs each business flow, including cross-cashflow approval and the 1000-item bulk proposal?
- What are the batch identity field, aggregate-success meaning, authorization rules, and applicable amount comparison?
- Which recovery owners, alert thresholds, compensation actions, and reinstatement conditions are approved?
- Which maker/checker state behavior governs cancel-deleting rules, adhoc SSI changes during other pending exceptions, and partial failures?
- Is asynchronous Camunda task completion intended, or must completion coordinate synchronously?
