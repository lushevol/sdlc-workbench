---
type: KnowledgeTopic
id: KT-settlement-regional-swift-customization
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2024 changes/Swift Customization Details/page.md
  revision: sha256:1dd72316aed56b38058e26b2f7992060e4a8bd428f067a082b4f1a42db3de0fe
  sha256: 1dd72316aed56b38058e26b2f7992060e4a8bd428f067a082b4f1a42db3de0fe
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:54:45.991204+08:00'
verified: []
scope: Historical selected-source design for settlement regional swift customization.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which regional customization versions and complete field-level contracts are authoritative?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement regional swift customization

## Scope

Historical selected-source design for settlement regional swift customization.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Conditional regional payment mappings

India INR NOS payments at or above500 million require sender and counterparty LEI in MT103 field70 or MT202 field72.
Egypt RTGS NOS rules customize receiver BIC and correspondent account by message type.
Egypt notice-to-receive camt.057 and withdrawal camt.058 conditions contain inconsistent entity FMID text.
Precious-metal receiver routing uses enumerated entities and currencies.

Dubai AED NOS MT103 and cover flows use26T TOF.
Dubai non-AED MAIN NOS payments have a separate77B purpose-of-payment condition.

Sources: [original lines 4–5](../../../evidence/sources/sha256/1dd72316aed56b38058e26b2f7992060e4a8bd428f067a082b4f1a42db3de0fe.md#L4-L5), [original lines 7–7](../../../evidence/sources/sha256/1dd72316aed56b38058e26b2f7992060e4a8bd428f067a082b4f1a42db3de0fe.md#L7-L7), [original lines 11–15](../../../evidence/sources/sha256/1dd72316aed56b38058e26b2f7992060e4a8bd428f067a082b4f1a42db3de0fe.md#L11-L15).

### Regional MX and commodity conditions

UK GBP purpose and LEI customization has duplicated sender predicates and unspecified target paths.
KWD purpose customization names currency without a complete target mapping.
HK same-BIC pacs.008 uses local instrument FMS.
TH internal payments preserve SPRO on line1 and separate later codewords.

VN SBV MT103/202 uses a specific correspondent BIC.
VN MX instruction rebuilding excludes202COV.
HAU MT604/605 uses commodity units and DVPTRF or SCRTRF instructions by PVP conditions.

Sources: [original lines 11–15](../../../evidence/sources/sha256/1dd72316aed56b38058e26b2f7992060e4a8bd428f067a082b4f1a42db3de0fe.md#L11-L15), [original lines 17–19](../../../evidence/sources/sha256/1dd72316aed56b38058e26b2f7992060e4a8bd428f067a082b4f1a42db3de0fe.md#L17-L19).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which regional customization versions and complete field-level contracts are authoritative?
