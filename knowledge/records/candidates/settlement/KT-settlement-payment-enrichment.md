---
type: KnowledgeTopic
id: KT-settlement-payment-enrichment
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Auto Populate Ordering Info for Notice
    to Receive Cashflow/page.md
  revision: sha256:a5aca52341b5c08c790fb9f69d8f6211ebddc90007298c67d1521466f9270413
  sha256: a5aca52341b5c08c790fb9f69d8f6211ebddc90007298c67d1521466f9270413
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Capture LEI/page.md
  revision: sha256:6be4ea90921e02ac058f229bcd9c06e4387181864a82c23ba86a00f9f51d8dc8
  sha256: 6be4ea90921e02ac058f229bcd9c06e4387181864a82c23ba86a00f9f51d8dc8
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/[Accounting Enhancement] Prepare Nstro
    Account Info before Sent/page.md
  revision: sha256:3b9dc4ad0cc4ea7fa69a3affe0de14cea9382c953397d2f936875b8deef31584
  sha256: 3b9dc4ad0cc4ea7fa69a3affe0de14cea9382c953397d2f936875b8deef31584
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:41:33.078711+08:00'
verified: []
scope: Historical selected-source design for settlement payment enrichment.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which Nostro values must held netted and withdrawn accounting tasks use after refresh?
- Does ordering auto-population exclude HAU, require NOS, and use Ordering_Customer_City
  for country?
- What approved SWIFT truncation and LEI ordering rules apply at field capacity?
- Which current regulatory authority, SCI mappings, templates, and effective scope
  approve this payment enrichment?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement payment enrichment

## Scope

Historical selected-source design for settlement payment enrichment.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Refresh Nostro data before accounting send

The answered fail/reinstate scenario requires each listed held task to regenerate its Nostro-related request information before sending.
The separate netted, released, and withdrawn cashflow example has no supplied answer.
The answered scenario does not resolve that example.

Sources: [original lines 9–14](../../../evidence/sources/sha256/3b9dc4ad0cc4ea7fa69a3affe0de14cea9382c953397d2f936875b8deef31584.md#L9-L14).

### Automatic receipt ordering information

The auto-stamping change applies to SCB receipts without stamped Vostro and without an SSI exception.
Notice to Receive must be Y.
The main requirement excludes XAU, XAG, XPD, XPT, and HAU.
Ad-hoc SSI remains outside the change.

Settlement means NOS remains an unresolved condition.

Sources: [original lines 9–12](../../../evidence/sources/sha256/a5aca52341b5c08c790fb9f69d8f6211ebddc90007298c67d1521466f9270413.md#L9-L12).

### SCI enrichment and empty-result behavior

For the source-defined bank types, use the SCI BIC when present.
If no BIC exists, use SCI name, address, and country.
For other client types, use those name and address fields directly.
If SCI returns nothing or raises an exception, do not auto-populate.

The ordering account number maps to the counterparty SCI FMID.

Sources: [original lines 13–14](../../../evidence/sources/sha256/a5aca52341b5c08c790fb9f69d8f6211ebddc90007298c67d1521466f9270413.md#L13-L14).

### Bank types and field mappings

The bank list is BANK, MULTDEV, INTEBCH, FININST, HDGEFND, INTLACC, INTECOM, INTDESK, FUNDMGR, CENTBK, and OSEASBK.
The BIC uses SCI fmSysContact.addrLine with SWIFT medium and MAIN usage.
The ordering name uses fmAccount.fmLongName.
The street address joins fmAddress.addressLine1 and city.

Converted SCI country maps to Ordering_Customer_City in the documented logical-model mapping.

Sources: [original lines 14–14](../../../evidence/sources/sha256/a5aca52341b5c08c790fb9f69d8f6211ebddc90007298c67d1521466f9270413.md#L14-L14).

### India LEI payment scope

The LEI requirement covers India branch FMID 4 and FMCODE SCB BOMBAY*MMB payments.
It excludes receipts.
Cashflow currency must be INR, INO, or INY, with INR SWIFT currency.
Amount must equal or exceed INR 500 million, and settlement means must be NOS.

Other settlement means remain excluded.

Sources: [original lines 11–11](../../../evidence/sources/sha256/6be4ea90921e02ac058f229bcd9c06e4387181864a82c23ba86a00f9f51d8dc8.md#L11-L11).

### LEI sources and SWIFT layout

Booking-entity and counterparty LEIs come from SCI regulatory information with MIFID and LEI selectors.
The source fixes the scoped booking-entity LEI as RILFO74KP1CM8P6PCT96.
LEIs occupy lines 1 and 2 of MT103 field 70 or MT202 field 72.
Existing SSI content moves to line 3 onward; the SI screen needs no LEI field.

MT103+202COV and MT202Flip remain excluded.
MT192/292 retain their logic and reflect the originating 103/202 values.

Sources: [original lines 12–17](../../../evidence/sources/sha256/6be4ea90921e02ac058f229bcd9c06e4387181864a82c23ba86a00f9f51d8dc8.md#L12-L17).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which Nostro values must held netted and withdrawn accounting tasks use after refresh?
- Does ordering auto-population exclude HAU, require NOS, and use Ordering_Customer_City for country?
- What approved SWIFT truncation and LEI ordering rules apply at field capacity?
- Which current regulatory authority, SCI mappings, templates, and effective scope approve this payment enrichment?
