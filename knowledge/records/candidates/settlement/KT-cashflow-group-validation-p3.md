---
type: KnowledgeTopic
id: KT-cashflow-group-validation-p3
version: 3
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/H1
    -  H2 booking model historical data analyse/page.md
  revision: sha256:54bbdba96b430484c23bad067317cd0d045bd0f6fc8e54608cdfe73b88a03d3b
  sha256: 54bbdba96b430484c23bad067317cd0d045bd0f6fc8e54608cdfe73b88a03d3b
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Ratan processing on cashflow events/Group Management
    Service - Non-Eco Amendment Technical Design/page.md
  revision: sha256:129507722b7986a380ca7039b8e63fdf587a4f61a6ea2e1be79461a62946cad3
  sha256: 129507722b7986a380ca7039b8e63fdf587a4f61a6ea2e1be79461a62946cad3
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Ratan processing on cashflow events/Trade Validation
    Confirmation Process Tech Design/page.md
  revision: sha256:8adcc39be9a985c5c32d3e4bc1db41d3cad779084f20a0aeed1dc4d3b8d70bdf
  sha256: 8adcc39be9a985c5c32d3e4bc1db41d3cad779084f20a0aeed1dc4d3b8d70bdf
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Ratan processing on cashflow events/page.md
  revision: sha256:89f7f53c3b2251d3580b9d5d43105c52a576dfec2638207cc76ba6315b1d6fa5
  sha256: 89f7f53c3b2251d3580b9d5d43105c52a576dfec2638207cc76ba6315b1d6fa5
- id: SRC-5cbe745c795e25c01bb377e7
  resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  0.1_Grouping/page.md
  revision: sha256:183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794
  sha256: 183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:58:31.904869+00:00'
verified: []
scope: Historical selected-source design for cashflow group validation p3.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which missing-group-flag behavior and amendment mapping/withdrawal linkage are approved?
- Which validation scope, Murex linkage, and late-amendment hold control apply by
  version?
- Which H1/H2 transition dates and cancelled-component completion rules supersede
  the examples?
- 'KDQ-18f3ca6087: Which source version and owner govern SCBML and Uber grouping?'
- 'KDQ-bf92171d66: What authority and recovery controls permit manual delivery of
  an incomplete group?'
- 'KDQ-e31f1f7906: Which parent validation and predecessor-message ordering rules
  govern each source?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
previous_content_sha256: 16e7478409b1fbc7e7d614e458fdc0ff14131000dfa2fc3cf375ee5ca7f1bbb7
---
# Cashflow group validation p3

## Scope

Historical selected-source design for cashflow group validation p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Grouping and ordered release

The design groups events by trade ID and major version, using the declared event count for completeness.
It waits for the group and preceding pending major-version groups.
Group states distinguish pending arrivals, prior-group dependency, ready, pending withdrawal, completed, and pending trade validation.
Group-message states distinguish pending, delivered, end, and offset.

One module row says missing group flags use the current flow, but its nested consumer wording says otherwise stop.
Missing-flag behavior therefore remains ambiguous.

Sources: [original lines 3–13](../../../evidence/sources/sha256/89f7f53c3b2251d3580b9d5d43105c52a576dfec2638207cc76ba6315b1d6fa5.md#L3-L13), [original lines 57–64](../../../evidence/sources/sha256/89f7f53c3b2251d3580b9d5d43105c52a576dfec2638207cc76ba6315b1d6fa5.md#L57-L64).

### Amendment and non-economic pairing

Withdrawal/New groups are amendments.
Non-economic pairs match booking entity, counterparty FMID, currency, amount, value date, and direction, with opposite events.
Other amendment cashflows are economic amendments.
The design keeps original/replaced cashflow versions and mapping history, with message-I/O keys including trade, major version, and cashflow.

The June 14, 2024 enhancement sends non-economic amendments through workflow when the replaced payment is PROJECTED or QUEUED.
The broader ignored-if-touched-or-settled wording does not settle every other state.

Sources: [original lines 1–86](../../../evidence/sources/sha256/129507722b7986a380ca7039b8e63fdf587a4f61a6ea2e1be79461a62946cad3.md#L1-L86), [original lines 3–13](../../../evidence/sources/sha256/89f7f53c3b2251d3580b9d5d43105c52a576dfec2638207cc76ba6315b1d6fa5.md#L3-L13).

### Trade validation gate

The May 29, 2024 preferred design keeps validation gating in group service.
Publish requires a complete group and validated trade.
Manual STP is disabled for unvalidated items.
FMRP validation uses trade ID, major version, and SENT, AFFIRMED, CONFIRMED, or TOBESENT with Validate action.

FMRP validation applies backward to earlier major versions.
Murex validation uses trade ID and VALD or COMP, without the FMRP version rule.
The alternative lifecycle TOBEVALIDATED state is struck through.
Murex trade/cashflow linkage and LIEN effects remain open.

The source treats the late-validation amendment hold control as desirable, rather than mandatory.

Sources: [original lines 1–27](../../../evidence/sources/sha256/8adcc39be9a985c5c32d3e4bc1db41d3cad779084f20a0aeed1dc4d3b8d70bdf.md#L1-L27).

### POC and H1/H2 scenarios

The non-economic POC expects mapped IDs in status-sync queues, failed-sync exception closure on replay, and deferred unnet synchronization after success.
Its trade-confirmation scenarios expect pending-affirmation exceptions to close, but one scenario changes trade IDs inconsistently.
The H1/H2 analysis illustrates group continuity across a model switch and a cancelled component forcing completion.
Its dates and weekday labels are inconsistent and do not define a release schedule.

These are design examples, without passing execution or a complete transition rule.

Sources: [original lines 66–86](../../../evidence/sources/sha256/129507722b7986a380ca7039b8e63fdf587a4f61a6ea2e1be79461a62946cad3.md#L66-L86), [original lines 1–39](../../../evidence/sources/sha256/54bbdba96b430484c23bad067317cd0d045bd0f6fc8e54608cdfe73b88a03d3b.md#L1-L39).

### L3-GROUP-01 — Producer-specific validation and completeness

For SCBML, hide cashflows from Settlement Ops while incomplete or pending trade validation. If cashflow trade state is unvalidated, inspect parent trade validation. Hold an unvalidated parent and resume affected cashflows from the TDS3 validation update. Uber checks for an existing group; create one only when absent. Offset matching cashflows, otherwise save messages pending. Uber resolves pending trade validation through the validated Uber version without a query. These are separate producer paths.

[Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L3-L10). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L13-L23). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L29-L45). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L51). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L56).

### L3-GROUP-02 — Group ordering and search identity

A declared cashflow count gates normal group processing until all expected messages arrive. Even a complete batch can remain pending_pre_group until previous groups consume necessary messages. The page mentions manual delivery without defining grants or recovery. FMRP uses trade ID for all-version Group Blotter searches. Murex uses original trade ID and maps upstream flow ID to its RATAN cashflow identity. Examples are explanatory, without executed completeness or identity assertions.

[Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L3-L10). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L13-L23). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L29-L45). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L51). [Original evidence](../../../evidence/sources/sha256/183a86d21e8e7a6cf30d97e9d00844dfae46fa06d64d73bea6565ec0eaf34794.md#L56).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which missing-group-flag behavior and amendment mapping/withdrawal linkage are approved?
- Which validation scope, Murex linkage, and late-amendment hold control apply by version?
- Which H1/H2 transition dates and cancelled-component completion rules supersede the examples?
