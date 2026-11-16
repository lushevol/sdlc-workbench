---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-cn-workflow",
  "version": 2,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-439a37df66edcd0c25513af3",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Business Flow/CN Cash Settlement Flow/page.md",
      "revision": "sha256:ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952",
      "sha256": "ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952",
      "snapshot": "knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md"
    },
    {
      "id": "SRC-23e9ba78716405df51f8f7fc",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/CN Settlement Demo Session/Sprint 13 (31th Oct 2022- 11th Nov 2022)/page.md",
      "revision": "sha256:7e6f8084fd28ce7814756e252b355b05acdaeabc9a25b170ff2eb3b75c18ed0e",
      "sha256": "7e6f8084fd28ce7814756e252b355b05acdaeabc9a25b170ff2eb3b75c18ed0e",
      "snapshot": "knowledge/evidence/sources/sha256/7e6f8084fd28ce7814756e252b355b05acdaeabc9a25b170ff2eb3b75c18ed0e.md"
    },
    {
      "id": "SRC-77ab4cdb798620947f7afc02",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/CN Settlement Demo Session/Sprint 14 (14th Nov 22 - 28th Nov 22)/page.md",
      "revision": "sha256:1dda74ce99dc24ec640babd4caf7869166dd3c0c8a450ed0b21a656a6e11d898",
      "sha256": "1dda74ce99dc24ec640babd4caf7869166dd3c0c8a450ed0b21a656a6e11d898",
      "snapshot": "knowledge/evidence/sources/sha256/1dda74ce99dc24ec640babd4caf7869166dd3c0c8a450ed0b21a656a6e11d898.md"
    },
    {
      "id": "SRC-b2f8a0597430836fffb5775d",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/CN Settlement Demo Session/Sprint 17/page.md",
      "revision": "sha256:d1b6db650d6af76e6b4dffdb6272d4659c5e8282002366c54d40ca34a5be34e9",
      "sha256": "d1b6db650d6af76e6b4dffdb6272d4659c5e8282002366c54d40ca34a5be34e9",
      "snapshot": "knowledge/evidence/sources/sha256/d1b6db650d6af76e6b4dffdb6272d4659c5e8282002366c54d40ca34a5be34e9.md"
    },
    {
      "id": "SRC-1da242f1473293825a75f1a8",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/CN Settlement Ops weekly session/2022-11-16/page.md",
      "revision": "sha256:cbb37ef19adbe4bf6a82d9514226771e62db9a7e35bad3787944a15f3e677198",
      "sha256": "cbb37ef19adbe4bf6a82d9514226771e62db9a7e35bad3787944a15f3e677198",
      "snapshot": "knowledge/evidence/sources/sha256/cbb37ef19adbe4bf6a82d9514226771e62db9a7e35bad3787944a15f3e677198.md"
    },
    {
      "id": "SRC-ceec58c6bc8e4c42dcb62eb4",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/CN Trade Migration - Settlement Process/page.md",
      "revision": "sha256:255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60",
      "sha256": "255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60",
      "snapshot": "knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md"
    },
    {
      "id": "SRC-57d75465860a6b9ff5d01e47",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/LifeCycle/Status Machine/page.md",
      "revision": "sha256:066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b",
      "sha256": "066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b",
      "snapshot": "knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T00:40:18.178987+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Undated proposed CN workflow; dated 2022 Sprint 13/14 and operations notes; undated Sprint 17; assumed May 2024 migration.",
  "summary": "Historical and undated CN proposals specify producer events, lifecycle examples, demo assertions and migration controls. Current authority is unresolved.",
  "related": [
    "KT-settlement-auto-netting",
    "KT-settlement-cashflow-identity-and-stella-write-back"
  ],
  "open_questions": [
    "Which state vocabulary and entity/version scope govern the historical workflow?",
    "Which reconciliation horizon and multiplicity apply to migration matching?",
    "Which agency portfolio, Field 20 routing, split, and exception rules remain applicable to current CN settlement, and who confirms them?",
    "Which final reversal, confirmation, LMS, and early-settlement mapping rules are approved?",
    "Which cutover dates, early-settlement handling, and later market-event rules remain approved? Should pre-effective-date aggregated cashflows change?",
    "When did temporary Murex reversal suppression begin and end, and which rule governs afterward?",
    "Can netting resultant cashflows be suppressed?",
    "Which source governs withdrawal: the CN flow DEAD/VALIDATED example or the status-machine CANCELLED transition?",
    "Which current approval and entity/date scope cover these historical and undated proposals?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Selected source passages support historical or proposed intent only.",
    "No implementation, execution, acceptance, publication, or deployment was verified.",
    "Semantic review is recorded separately against the final draft hash.",
    "Automated checks do not establish complete writing review."
  ]
}
---
# Historical CN workflow and migration

> **Draft proposal:** The sole integrator must review this merge. Human publication review remains pending.

## Scope

Undated CN workflow proposals, dated 2022 Sprint 13/14 and operations notes, undated Sprint 17, and assumed May 2024 migration proposals.

## Summary

The sources describe producer-specific events, materialization, maker/checker flows, demos, operations notes, and migration controls.
Current applicability, rule conflicts, and executed outcomes remain unresolved.

## Documented knowledge

### Workflow and event handling

The historical overview describes Murex cashflows as if only NEW events exist; it treats other events as incremental cashflows.
Its Stella table lists separate AMEND and WITHDRAWAL events.
After release, the source describes withdrawal followed by a new cashflow.
It says the replacement waits for linked withdrawal completion before release.
The source leaves reversal by SWIFT versus cancellation unresolved.
It also asks whether netting resultant cashflows can be suppressed.
These producer distinctions remain bounded to historical CN material.
[WF-MG-044: producer events](../../../../knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md#L3-L24) [WF-MG-044: state examples](../../../../knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md#L87-L109) [WF-MG-045: released replacement](../../../../knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md#L107-L128)

The undated flow proposes materialization at VD-5.
It uses maker/checker for NSTP release, suppression, and CPN netting.
The source examples describe linked withdrawal completion before replacement release.
Status names need reconciliation with later state models.
[WF-MG-045: workflow examples](../../../../knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md#L30-L38) [WF-MG-045: maker/checker and CPN](../../../../knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md#L44-L67) [WF-MG-045: linked withdrawal](../../../../knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md#L69-L85)

### Dated demo expectations

Sprint 13 and Sprint 14 have 2022 date ranges. Sprint 17 has no date in the retained page.
The pages describe manual or mocked inputs and expected results.
The following are expected assertions, without retained execution results:

| Source | Given / when | Expected observable result |
| --- | --- | --- |
| Sprint 13, rows 1–4 | Manually submit mocked Stella cashflows at VD-7, VD-5, or VD-4. | Persist and display PROJECTED at VD-7; persist and display QUEUED at VD-5 and VD-4. |
| Sprint 13, row 4 | Run materialization at VD-5 for a VD-7 booking. | Change PROJECTED to QUEUED. |
| Sprint 13 amendment; Sprint 14 row 5 | Submit NEW then AMEND for the same VD-4 cashflow. | Display the amendment only. “Discard the new” does not establish deletion of audit history. |
| Sprint 13 netting; Sprint 14 row 6 | Net mocked components through the API or GUI, respectively. | Set components NETTED and create a QUEUED resultant. |
| Sprint 14 row 6 | Net through the GUI. | Set resultant amount to the component sum; share one netting ID across components and resultant. |
| Sprint 14 row 7 | Un-net through the GUI. | Return components to QUEUED; set resultant DEAD. |
| Sprint 17 row 1 | Submit mocked CCS initial and final exchanges at T+2 and one year. | Set T+2 QUEUED; keep the one-year cashflow PROJECTED. |
| Sprint 17 rows 2–4 | Submit forwards at T+5, T+6, and T+7; materialize the T+7 flow at T+2. | Set T+5 QUEUED; keep T+6 PROJECTED; move T+7 from PROJECTED to QUEUED at VD-5. |
| Sprint 17 rows 5–6 | Submit mocked Stella spot NEW then AMEND or WITHDRAWAL. | Display only the latest event; retain both events in cashflow history. |
| Sprint 17 row 7 | Book Murex spot and perform C&R. | Display the latest amendment; retain NEW and AMEND history. |
| Sprint 17 rows 8–9 | Net Murex spot and mocked Stella spot cashflows, then un-net. | Apply the Sprint 14 amount, netting-ID, component-status, and resultant-status assertions. |

Sprint 17 mixes mocked Stella input with Murex booking steps.
It does not establish a wholly mocked or executed demonstration.
Current approval, entity scope, and applicability remain unknown.
[Demo 13](../../../../knowledge/evidence/sources/sha256/7e6f8084fd28ce7814756e252b355b05acdaeabc9a25b170ff2eb3b75c18ed0e.md#L10-L15) [Demo 14](../../../../knowledge/evidence/sources/sha256/1dda74ce99dc24ec640babd4caf7869166dd3c0c8a450ed0b21a656a6e11d898.md#L15-L17) [Demo 17](../../../../knowledge/evidence/sources/sha256/d1b6db650d6af76e6b4dffdb6272d4659c5e8282002366c54d40ca34a5be34e9.md#L5-L13)

### Operations discussion

A 2022 operations note describes agency-profile trades without China-agent queued payments or SWIFT messages.
It says portfolio identifies these payments and Field 72 marks agency payments.
It also says these portfolios have no settlement accounting.
The note reports no live production case test and frames reuse as a future requirement.
Field 20 format, prefix routing, its final A/B character, and Murex 2.11 logic reuse remain open.

Razor BAU auto-splits payments above preset thresholds for selected countries and currencies.
Its threshold data is currency-level, and Field 72 links split payments to parent payments.
The note says Murex 2.11 derivatives have no auto-split requirement.
It describes client-requested manual Opics splits without parent linkage.

The note names missing Vostro and Nostro as main business exceptions.
It also describes P2P portfolios without trade or settlement accounting.
Those P2P exceptions occur before trade and do not appear in the payment queue.
The source records follow-up contacts, but no current decision owner is established.
[WF-MG-049: 2022 operations discussion](../../../../knowledge/evidence/sources/sha256/cbb37ef19adbe4bf6a82d9514226771e62db9a7e35bad3787944a15f3e677198.md#L10-L13)

### Migration reconciliation and proposed controls

The migration proposal matches Stella trades to Murex 2.11 trades through an ID mapping.
It compares entity, counterparty, payment date, currency, direction, and amount.
One section scopes cashflows to the next nine days; another specifies T+7.
The conflicting horizons remain unresolved.
[WF-MG-050: reconciliation comparison](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L3-L3) [WF-MG-050: T+7 comparison](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L104-L107)

The migration notes assume 10 May 2024 as cutover and 11–12 May as the migration weekend.
Under that assumption, they assign value dates through 10 May to Murex and dates from 13 May to Stella.
The selected text assigns 12 May to the new Stella trade.
It places that date in the market-event effective-date discussion; it does not establish a booking timestamp.
The proposal says later market events leave earlier value dates unchanged.
It permits the effective date to move only later and leaves an 8 May aggregate question open.
The preferred option proposes SETTLED status without generating payment messages.
This is a historical assumption and proposal, not evidence of completed migration.
[WF-MG-051: cutover and effective-date assumptions](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L10-L15) [WF-MG-051: early-settlement option](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L47-L61) [WF-MG-051: status-only update](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L50-L51)

One proposed Murex reversal suppression rule applies to cancellations during migration weekend only.
The source says to remove that rule after migration activities.
Other sections describe suppressing a payment or withdrawal event, holding reversal cashflows, or moving status to CANCELLED.
These variants conflict and remain unresolved.
Stella confirmation and LMS handling also remain open.
[WF-MG-052: temporary suppression](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L3-L3) [WF-MG-052: reversal options](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L47-L61) [WF-MG-052: later handling](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L86-L98) [WF-MG-052: confirmation status](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L100-L102)

### Additional migration predicates and limits

The opening proposal suppresses Stella aggregated cashflows when `Cashflow Status == 'SUSPENDED'`.
The later rules instead identify aggregated payments by the `Migrated_Aggregated_` payment-type prefix.
Their equivalence is unproved. The later rules also suppress SCF bookings for Murex dead trades.
The proposal holds newly booked Stella cashflows as NSTP, using sender `STELLA` or source-system Stella.
It proposes a batch PROJECTED-to-SETTLED update with a programme-supplied cashflow list as a dynamic input.
[Migration predicates](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L3-L6) [Later predicates](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L86-L98)

The preferred early-settlement option changes status only, without Razor messages or SWIFT generation.
It preserves proposed hard blocking and subsequent amendment handling.
Individual fund recall and resettlement can still require manual Oscar settlement.
The LMS option is break handling or revision to feed only settled cashflows; no final choice is recorded.
[Preferred option and limits](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L47-L61)

The rejected or alternative approaches retain different consequences.
Avoiding early settlement requires weekend support, client agreement, and handling VD-1 demand.
Suppressing overlapping Stella flows leaves amendment, duplicate-payment, hard-blocking, and manual-settlement risks.
Both overlap options retain LMS dependencies. These are proposal assessments, not observed failures.
[Option trade-offs](../../../../knowledge/evidence/sources/sha256/255374f50479717c97c8c09bd5f77a4e1d5fe987bf7e1fa9b7f2b4fbc8b4ca60.md#L47-L51)

### Concrete lifecycle conflict

The CN flow's pre-release undo example uses WITHDRAWAL → DEAD and then VALIDATED.
Its event table and detailed examples are not a consistent transition authority.
The separate status-machine table uses PROJECTED/QUEUED WITHDRAWAL → CANCELLED.
It uses RELEASED/SETTLED/NOSTRO_MATCHED WITHDRAWAL → QUEUED.
The CN flow instead shows post-release WITHDRAWAL → CANCELLED.
Neither undated source establishes precedence or current approval.
[CN undo](../../../../knowledge/evidence/sources/sha256/ec035680b27d9031a384bf2ac3e13908bb2dc6799a2dbb8eb569b000dde78952.md#L87-L128) [State-machine conflict](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L46-L63) [Post-release conflict](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L209-L213)

## Connections

Related record IDs: `KT-settlement-auto-netting` and `KT-settlement-cashflow-identity-and-stella-write-back`.
These declarations preserve topic boundaries; they do not establish runtime integration.

## Evidence limits

Sprint 13 and Sprint 14 are dated 2022. The CN flow and Sprint 17 have no recorded date.
The migration proposal assumes a 2024 cutover and does not establish execution.
The operations note reports no live production case test.
Conflicting event, reconciliation, reversal, confirmation, and applicability questions remain open.
No implementation, acceptance, deployment, or production behavior was inspected.
Current applicability is unknown.

## Open questions

Owner: unknown.

- Which state vocabulary and entity/version scope govern the historical workflow?
- Which reconciliation horizon and multiplicity apply to migration matching?
- Which agency portfolio, Field 20 routing, split, and exception rules remain applicable to current CN settlement, and who confirms them?
- Which final reversal, confirmation, LMS, and early-settlement mapping rules are approved?
- Which cutover dates, early-settlement handling, and later market-event rules remain approved? Should pre-effective-date aggregated cashflows change?
- When did temporary Murex reversal suppression begin and end, and which rule governs afterward?
- Can netting resultant cashflows be suppressed?
- Which source governs withdrawal: the CN flow DEAD/VALIDATED example or the status-machine CANCELLED transition?
- Which current approval and entity/date scope cover these historical and undated proposals?
