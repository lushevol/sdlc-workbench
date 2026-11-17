---
type: Summary
description: "Summarizes separate candidate C&A, FX-replication, option-fixing, and trade-validation proposals."
doc_type: short
full_text: sources/KT-settlement-trade-control-utilities.md
---

# Trade-control proposals for C&A, FX replication, option fixing, and validation

> **Source status:** Candidate/draft. These source views describe separate proposals, not one shared policy or current implementation.

C&A PV review compares trade versions using prior-day market data. Its first scope is China Linear Rates FMRP Blade; later coverage and nine non-PV checks are proposals. The batch schedule contains an unresolved GMT/UKT label conflict, and the user output is undecided. [WF-EV-058](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#wf-ev-058-ca-pv-review) [WF-EV-059](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#wf-ev-059-ca-phases) [WF-EV-060](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#wf-ev-060-ca-dependencies-and-schedule)

Other records propose eligible FX trade replication, expiry-fixing comparison with tolerance rules, and TDS3 trade-rule validation that opens or closes version-linked exceptions. The selected FX view lacks predicates; fixing tolerances and timezone remain unknown. The review table for trade rules is blank. [WF-EV-061](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#wf-ev-061-fx-replication) [WF-EV-062](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#wf-ev-062-option-expiry-and-exercise-fixing) [WF-EV-063](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#wf-ev-063-trade-rule-validation)

Linked policies, full rule data, and execution evidence were not inspected. See proposed [[summaries/KT-rule-service-p3]].

## Version 2 C&A scope and timing detail

The source includes undo, meaning removal of the last market operation, within cancellation and amendment scope.
It reviews booking-change genuineness and P&L impact to reduce fraudulent-trade risk.
MVP1 identifies `SOURCE_SYSTEM=SABRE` and this literal hierarchy:

`|Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|Rates|EM Rates|EM Rates - Greater China`

The source gives these historical expected timings:

| Batch | Expected feed to OVV | Expected exception generation |
| --- | --- | --- |
| Batch 1 | T 03:00 PM SGT, shown as 6:00AM UTC | T 04:00 PM SGT, shown as 7:00AM UTC |
| Batch 2 | T 03:00 PM UKT, shown as 2:00PM UTC | T 04:00 PM UKT, shown as 3:00PM UTC |
| Batch 3 | T 03:00 PM UST, shown as 6:00PM UTC | T 04:00 PM UST, shown as 7:00PM UTC |
| Batch EOD | T+1 00:00AM UTC | T+1 01:00AM UTC, for previous-version trade PV |

The SGT-to-UTC pairs are inconsistent. UKT/UST seasonal clock rules remain unconfirmed.
The MRB paragraph separately names SGT, GMT, and UST, and requires effective timestamps on sub-trade PV feeds.
RATAN EOD exposes an OVV view to RATAN ONE and DQSL; DQSL also receives a new C&A T0 PV view.
RATAN ONE joins TDS3 trades and PV, then applies filters, aggregation, and seven Middle Office control rules.
The seven rules remain distinct from the nine proposed non-PV checks.
UI versus report output and user actions remain open.
These expected timings establish no executed schedule or current service guarantee.
[Selected C&A scope and literal expected timings](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#selected-ca-scope-and-literal-expected-timings)

## Historical FX replication boundary

The source describes pre-FMRP Rates-desk Murex FX cash replication into Razor Non-Standard Portfolios, for settlement only.
It proposes continued Razor settlement under FMRP with real-time eligibility filtering.
Exact predicates remain unavailable; historical NSP placement establishes no universally current portfolio contract.
[Historical FX replication boundary](../../../records/candidates/settlement/KT-settlement-trade-control-utilities.md#historical-fx-replication-boundary)
