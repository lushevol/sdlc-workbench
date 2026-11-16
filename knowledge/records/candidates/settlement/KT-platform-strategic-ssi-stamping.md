---
type: KnowledgeTopic
id: KT-platform-strategic-ssi-stamping
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Strategic SSI Stamping
    Design/SSI Stamping Implementation(SCBML)/page.md
  revision: sha256:929f9ae77d4d1a413b060444fd07defa70e964bd82f6daeda282a614d6317c2f
  sha256: 929f9ae77d4d1a413b060444fd07defa70e964bd82f6daeda282a614d6317c2f
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Strategic SSI Stamping
    Design/page.md
  revision: sha256:1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650
  sha256: 1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:33:59.608564+08:00'
verified: []
scope: Historical selected-source design for platform strategic ssi stamping.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- What identifies a reusable trade-stamping result, and when must a repeated request
  restamp or persist a new record?
- Which cashflow stamping placement, matching fields, failure states, and concurrency
  behavior are approved?
- What SSI refresh scope, time windows, ad-hoc exclusions, event ordering, and trade/cashflow
  impact rules are intended?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Platform strategic ssi stamping

## Scope

Historical selected-source design for platform strategic ssi stamping.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Unified strategic stamping objective

The strategic proposal requests a product-agnostic SSI stamping API with one responsibility.
It seeks reuse of trade stamping results for cashflows and Uber exchange with CDUPS.
Trade data maps into a RATAN logical model extending Uber.
Standardized currency, product, identity, counterparty, CFI, settlement method/type, and debit/credit data support stamping.

Sources: [original lines 16–22](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L16-L22), [original lines 44–75](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L44-L75).

### Version identity remains contradictory

One proposal stores trade stamping per tradeId and majorVersion and reuses an existing result.
It limits SSI refresh to the latest major version.
Query misses use ad-hoc stamping without persistence.
The same document questions major-version identity and proposes storing every repeated stamping request with newest-result queries.

These statements remain separate alternatives until their identity and retention contract is resolved.

Sources: [original lines 77–88](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L77-L88), [original lines 147–170](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L147-L170).

### Cashflow stamping alternatives

Cashflow stamping reuses a good trade result by matching currency, direction, and other required attributes.
Otherwise, the proposal raises an exception and NSTP.
Option A batches stamping in Group service.
Option B stamps cashflows through orchestration while reusing the trade result.

The document requires protection against concurrent access to the same cashflow.

Sources: [original lines 92–116](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L92-L116).

### Proposed concurrency and recovery

The proposal uses a unique tradeId/majorVersion constraint to arbitrate concurrent stamping.
After a key conflict, retry reuses the saved result.
It proposes sequential SSI notifications through one partition.
After failed or partial trade stamping, cashflow processing retries batch stamping.

Cashflow-based batch stamping also serves as compensation for products not yet onboarded.

Sources: [original lines 135–145](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L135-L145), [original lines 158–170](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L158-L170).

### Downstream exchange responsibility

The proposal stores SSI information in the RATAN model.
It converts that information to SCBML before sending it to Razor.
SSI refresh scope, impact addressing, and complete exception handling remain unfinished in the selected design.

Sources: [original lines 1–14](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L1-L14), [original lines 120–145](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L120-L145), [original lines 172–174](../../../evidence/sources/sha256/1ce73fbe145ef98cf019654b8451e818c54680173c36fcf912274adb099ad650.md#L172-L174).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

The existing OPS-A-KT-SSI-AND-NOSTRO version 3 was inspected as regional intent context. This proposal does not supersede it.

## Open questions

Owner: unknown.

- What identifies a reusable trade-stamping result, and when must a repeated request restamp or persist a new record?
- Which cashflow stamping placement, matching fields, failure states, and concurrency behavior are approved?
- What SSI refresh scope, time windows, ad-hoc exclusions, event ordering, and trade/cashflow impact rules are intended?
