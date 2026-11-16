---
type: KnowledgeTopic
id: KT-settlement-event-sequencing
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Trade & Cashflow Events Control/Cashflow Events Control/page.md
  revision: sha256:b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c
  sha256: b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:50:02.815956+08:00'
verified: []
scope: Historical selected-source design for settlement event sequencing.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which event mappings and concurrent amendment, release, or netting ordering are
  approved?
- Are multicurrency netted resultants amended or cancelled jointly or independently?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement event sequencing

## Scope

Historical selected-source design for settlement event sequencing.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Event identity and sequencing

The design uses New and Withdrawal events.
Stella trade ID, cashflow major version, and BatchId_Sequence_Count identify and sequence events.
Incomplete batches stay outside the blotter and settlement flow.
A later batch waits until the earlier batch reaches STP or NSTP.

This completion point does not mean settlement.
New/Withdrawal and New/Withdrawal/New sequences execute in order.
Repeated New events process only the first event.

Sources: [original lines 1–10](../../../evidence/sources/sha256/b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c.md#L1-L10), [original lines 12–15](../../../evidence/sources/sha256/b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c.md#L12-L15), [original lines 27–40](../../../evidence/sources/sha256/b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c.md#L27-L40).

### Post-release lifecycle branches

Post-release cancellation or amendment uses NSTP reversal and rebooking.
Closeout uses a new NSTP trade and manual netting.
Portfolio reassignment requires duplicate-payment inspection and suppression.
Revival restores an unreleased original cancellation.

When the original was released, an unreleased cancellation is ignored.
FO/MO cannot undo a cancellation after MTx92 release.
Fixing after payment release in the same period uses NSTP.
Expiry events are discarded.

Sources: [original lines 46–57](../../../evidence/sources/sha256/b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c.md#L46-L57).

### Murex event mapping and limits

The mapping converts RPL, RPL_M, MOD, CNCL, and XIT to Withdrawal plus New.
RPL_D maps to Withdrawal, EXR to New, and NET to NA.
The examples show version transitions without execution evidence.
The source leaves linked versus independent multicurrency resultant cancellation unresolved.

Sources: [original lines 57–57](../../../evidence/sources/sha256/b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c.md#L57-L57), [original lines 77–97](../../../evidence/sources/sha256/b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c.md#L77-L97), [original lines 126–128](../../../evidence/sources/sha256/b0ca7168fda2aeefad5f3fb61a7976d5eef9df457045be16b0dd1842b1c5154c.md#L126-L128).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which event mappings and concurrent amendment, release, or netting ordering are approved?
- Are multicurrency netted resultants amended or cancelled jointly or independently?
