---
type: KnowledgeTopic
id: KT-platform-cashflow-processing-contracts
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Hot NSTP Rule Exception Generation/page.md
  revision: sha256:ed246628e1e592913d560f4aaeaa496cad38029034f9c8db7e48b3d9496b60da
  sha256: ed246628e1e592913d560f4aaeaa496cad38029034f9c8db7e48b3d9496b60da
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Performance/Batch Status Update API Tuning/lifecycle service - state
    machine/page.md
  revision: sha256:b306678b9f0eb74534dc1c84616f66d8c97ee767d544bc90afdb6d6707b737d7
  sha256: b306678b9f0eb74534dc1c84616f66d8c97ee767d544bc90afdb6d6707b737d7
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/SSI Stamping Service Design/SSI Stamping Design/page.md
  revision: sha256:1c14cbc2b29fe2dd1a12b5078531426b0079e00b7210553b28a6b5df67ebe71f
  sha256: 1c14cbc2b29fe2dd1a12b5078531426b0079e00b7210553b28a6b5df67ebe71f
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Fixing
    flag notification/page.md
  revision: sha256:bba65e15216242c8903abf8505b1aa713e61af2cd65375bc069cf7a50650db14
  sha256: bba65e15216242c8903abf8505b1aa713e61af2cd65375bc069cf7a50650db14
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/IRS
    Cashflow Processing Design/page.md
  revision: sha256:d98bc91b009533357c70026cd59dd94401b4e95b729564806b27ac34895f9a14
  sha256: d98bc91b009533357c70026cd59dd94401b4e95b729564806b27ac34895f9a14
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Increase
    Payment Amount within USD 1 Threshold Tech Design/page.md
  revision: sha256:8a4d795b18539ad3ad7649cd41343da50e73d4564488c6fa790884b5b03b38c4
  sha256: 8a4d795b18539ad3ad7649cd41343da50e73d4564488c6fa790884b5b03b38c4
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/LIEN
    Processing & Pending Fixing Flag Technical Design/page.md
  revision: sha256:433ec1031f2637c2c99fac0d49f0c3c3949432042f60081d5fb3594a602c068c
  sha256: 433ec1031f2637c2c99fac0d49f0c3c3949432042f60081d5fb3594a602c068c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/NSTP
    Maker-Checker Separation From Code/NSTP exception auto close design-Confirmation
    status handling/page.md
  revision: sha256:39efd157c7de91e3026f585f22dd7f64070a13221e485b851d182438d956075c
  sha256: 39efd157c7de91e3026f585f22dd7f64070a13221e485b851d182438d956075c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/NSTP
    Maker-Checker Separation From Code/page.md
  revision: sha256:54f80ca6dd85f2fdfe55f8718da1f09fdc20bd097720f17a79f5fe45591e304b
  sha256: 54f80ca6dd85f2fdfe55f8718da1f09fdc20bd097720f17a79f5fe45591e304b
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Cashflow Lifecycle Stamping Logic/page.md
  revision: sha256:94a25d66f13dd44ac329b7d3f377da2d90314ed531a00f61768a7263f70aaa50
  sha256: 94a25d66f13dd44ac329b7d3f377da2d90314ed531a00f61768a7263f70aaa50
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Manual Holding Process Tech Design/page.md
  revision: sha256:1d0eee28f9e36c0a170092c2c4ce2ee9cd15dd96903f1470990b48051e4abaac
  sha256: 1d0eee28f9e36c0a170092c2c4ce2ee9cd15dd96903f1470990b48051e4abaac
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Unresolved
    exception & mandatory field check/page.md
  revision: sha256:d29f787171181907f30629b782820ee12cdebac0e25ec3995cd27654b783b9a9
  sha256: d29f787171181907f30629b782820ee12cdebac0e25ec3995cd27654b783b9a9
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:16:56.103374+08:00'
verified: []
scope: Historical selected-source design for platform cashflow processing contracts.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which versioned transition and persistence contract completes the lifecycle matrix?
- How should cancelled fixing notifications update flags, and which LIEN/fixing design
  is selected?
- Which eligible currencies/cashflows, USD conversion rule, and strict threshold govern
  payment adjustment?
- Which effective SSI, IRS, confirmation, mandatory-field, and maker/checker contracts
  apply?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Platform cashflow processing contracts

## Scope

Historical selected-source design for platform cashflow processing contracts.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Lifecycle transition source limits

The matrix separates new IDs, business-version downgrade, upgrade, and unchanged-version persistence.
It specifies event, history, current-message, cutoff, holding, and affirmation-table operations.
The detailed field-source and update-condition cells are largely blank.
Its status table gives source/action/target triples for processing, netting, split, suppression, holding, settlement, and exception states.

Examples include PROJECTED Materialize to QUEUED and READY Release to RELEASED.
It also sends NETTED/SPLIT New to ERROR, while many ordinary states return to QUEUED on New.
The matrix cannot establish a universal permission allowlist, fallback, or complete field-generation contract.

Sources: [original lines 1–426](../../../evidence/sources/sha256/b306678b9f0eb74534dc1c84616f66d8c97ee767d544bc90afdb6d6707b737d7.md#L1-L426).

### Holding and process separation

The manual-hold design selects main status and strikes through the attribute and exception alternatives.
Hold blocks in-progress pending exception, pending netting, ready, queued, and projected operations.
Unhold restores the prior status to avoid duplicated work.
The maker/checker separation proposal puts process logic in Camunda and basic business logic in domain services.

It proposes maker-start, checker-complete, user-operation storage, and lifecycle status APIs.
Its 2023 Sprint 1 target does not establish adoption.

Sources: [original lines 1–5](../../../evidence/sources/sha256/1d0eee28f9e36c0a170092c2c4ce2ee9cd15dd96903f1470990b48051e4abaac.md#L1-L5), [original lines 9–9](../../../evidence/sources/sha256/1d0eee28f9e36c0a170092c2c4ce2ee9cd15dd96903f1470990b48051e4abaac.md#L9-L9), [original lines 5–44](../../../evidence/sources/sha256/54f80ca6dd85f2fdfe55f8718da1f09fdc20bd097720f17a79f5fe45591e304b.md#L5-L44).

### Hot rules, SSI, and mandatory checks

Hot NSTP rules should apply to cashflows still in workflow before Razor release and generate or remove exceptions accordingly.
The ad-hoc SSI requirement lets a READY cashflow start input without an existing SSI exception.
Successful maker submission generates an exception and Pending Verification.
Checker rejection generates an exception and Pending Operator.

The CN comparison restricts SSI API calls to Camunda and notes changed notification handling.
The mandatory-field fragment adds verification between multi-exception checking and holding release, with orchestration configuration.
It does not identify the actual mandatory field set.

Sources: [original lines 3–3](../../../evidence/sources/sha256/ed246628e1e592913d560f4aaeaa496cad38029034f9c8db7e48b3d9496b60da.md#L3-L3), [original lines 13–17](../../../evidence/sources/sha256/1c14cbc2b29fe2dd1a12b5078531426b0079e00b7210553b28a6b5df67ebe71f.md#L13-L17), [original lines 115–126](../../../evidence/sources/sha256/1c14cbc2b29fe2dd1a12b5078531426b0079e00b7210553b28a6b5df67ebe71f.md#L115-L126), [original lines 3–6](../../../evidence/sources/sha256/d29f787171181907f30629b782820ee12cdebac0e25ec3995cd27654b783b9a9.md#L3-L6).

### Fixing notification and LIEN design

Batch processing validates fixing notifications and publishes Kafka notifications.
Lifecycle persists batch and real-time notifications and reprocesses eligible cashflows with the latest flag.
The narrative says cancelled cashflows do nothing, but its cancellation scenario updates the visible flag while retaining cancellation.
Earlier notifications, failed/reinstated cashflows, and simultaneous arrivals retain the latest flag in the stated scenarios.

The LIEN proposal refreshes component LIEN amounts before resultant generation and restamps when lifecycle returns to QUEUED.
It retains alternative workflow designs and an unresolved Pending Fixing transition.
CANCELLED and DEAD breakpoint rows are struck through.

Sources: [original lines 1–3](../../../evidence/sources/sha256/bba65e15216242c8903abf8505b1aa713e61af2cd65375bc069cf7a50650db14.md#L1-L3), [original lines 15–77](../../../evidence/sources/sha256/bba65e15216242c8903abf8505b1aa713e61af2cd65375bc069cf7a50650db14.md#L15-L77), [original lines 1–54](../../../evidence/sources/sha256/433ec1031f2637c2c99fac0d49f0c3c3949432042f60081d5fb3594a602c068c.md#L1-L54).

### IRS pairing and stamping responsibility

The IRS design inserts a subprocess before netting eligibility after exception/suppression checks.
It proposes matching another leg by value date, currency, client, and trade ID in Waiting/PendingAnotherLeg.
Matched pairs net with SUCCESS; missing legs move to waiting and return FILTERED.
Exceptions also return FILTERED with a description.

The IRS rule is not shown in the GUI dropdown.
The stamping design moves attribute stamping from persistence into a reusable lifecycle API/action.
Entity and counterparty FMCODE are mandatory; client type and later attributes are not mandatory in its table.

Sources: [original lines 5–8](../../../evidence/sources/sha256/d98bc91b009533357c70026cd59dd94401b4e95b729564806b27ac34895f9a14.md#L5-L8), [original lines 1–24](../../../evidence/sources/sha256/94a25d66f13dd44ac329b7d3f377da2d90314ed531a00f61768a7263f70aaa50.md#L1-L24).

### Confirmation-driven exception closure

The closure design listens to Trade_Service__Trade_Events.
It requires MATCHED with confirmation status Confirm or Affirm, a CN settlement linkage, and WAITING with action isNstp.
It then calls orchestration syncSummary to close exceptions, synchronize summaries, and update status.
Tracking_version maps to trade_version; rule entity identity/version maps to cashflow identity/business version.

This specific chain does not establish closure for every confirmation event.

Sources: [original lines 1–7](../../../evidence/sources/sha256/39efd157c7de91e3026f585f22dd7f64070a13221e485b851d182438d956075c.md#L1-L7), [original lines 9–9](../../../evidence/sources/sha256/39efd157c7de91e3026f585f22dd7f64070a13221e485b851d182438d956075c.md#L9-L9).

### Small payment adjustment requirement

The summary requires maker/checker adjustment before release, limited to eligible cashflows and currencies below a configured USD 1 equivalent threshold.
SWIFT and LMS use the adjusted amount; Accounting retains the original.
Further netting or splitting is blocked until removal and approval of the adjustment.
The design reuses the existing Camunda flow and APIs without a separate user-task creation flow.

Eligibility, conversion time/rate, precision, and exact boundary rules are not supplied in this selected summary.

Sources: [original lines 1–26](../../../evidence/sources/sha256/8a4d795b18539ad3ad7649cd41343da50e73d4564488c6fa790884b5b03b38c4.md#L1-L26).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which versioned transition and persistence contract completes the lifecycle matrix?
- How should cancelled fixing notifications update flags, and which LIEN/fixing design is selected?
- Which eligible currencies/cashflows, USD conversion rule, and strict threshold govern payment adjustment?
- Which effective SSI, IRS, confirmation, mandatory-field, and maker/checker contracts apply?
