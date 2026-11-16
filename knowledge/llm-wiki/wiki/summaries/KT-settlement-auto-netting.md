---
type: "Summary"
description: "Documents scheduled cash settlement auto-netting rules, grouping, outcomes, and unresolved policy differences."
doc_type: short
full_text: "sources/KT-settlement-auto-netting.md"
---

> Derived from [KT-settlement-auto-netting, version 3](../../../records/candidates/settlement/KT-settlement-auto-netting.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Cash Settlement Auto-Netting

## Overview

This summary covers the scheduled cash settlement auto-netting workflow. It draws on candidate requirements and flow descriptions for rule evaluation, queueing, execution, grouping, and resultant cashflow handling.

## Key concepts

- **Rule selection:** A cashflow matching a live rule is placed in Pending Auto Netting for scheduled processing. The Day 2 requirement selects the lowest-priority-number netting type, then the most recently created rule among matches of the same type. A September flow summary says evaluation ends at the first match in priority order. [[concepts/auto-netting-rule-selection]]
- **Scheduling and calendars:** The scheduled job processes queued cashflows according to configured netting dates and times, but the sources differ on calendar basis. Day 1 specifies the booking entity’s home-currency calendar; Day 2 specifies the cashflow-currency calendar and retains the payment date for a value-date rule. A later discussion proposes skipping weekends only. [[concepts/auto-netting-scheduling]]
- **Grouping:** Cashflows can net together only when they share the same rule identity and have identical values for every configured execution-key field. The documented Bilateral Netting key is booking entity, counterparty, payment currency, and payment date. [[concepts/cashflow-netting-grouping-and-outcomes]]
- **Result handling.** The netting type defines the mapping for creating the resultant cashflow. Day 2 directs the job to release a cashflow with no matching partner from the queue after the scheduled time. The job applies the rule’s straight-through processing level and leaves the Settle as Gross flag unset. The September summary treats single cashflows as exceptions. Confirm the outcome by netting type and rule configuration. [[concepts/cashflow-netting-grouping-and-outcomes]]

## Findings and unresolved differences

The effective policy remains open for calendars, late arrivals, rule precedence, refresh, and re-entry. Day 1 sends late arrivals to manual netting. The 16 May 2025 Day 2 decision records queueing eligible cashflows before or after the scheduled time. A later discussion proposes configurable handling. The Day 2 requirement describes refresh after rule changes, and its clarification history records a no-refresh alternative. Day 2 permits a reinstated single cashflow to match again. The September flow says cashflows produced by an un-net do not re-enter auto-netting.

## Portal connection

The [[summaries/KT-portal-purpose|Post Trade Portal]] provides a shared entry and workspace for post-trade applications. Cash Settlement rules belong to the application domain.

## Evidence and status

The candidate cites the Function Flow and its attachment, the Day 2 requirement, the 2024 requirement, and the datetime-calculation discussion. The owner is unknown. Effective business scope, single-cashflow policy, and publication approval still need domain-owner evidence.

### Source-scoped static and affirmation additions

Day 2 gives DataOps static create/update responsibility and read-only access to other users. Its refresh branches conflict for PendingAutoNetting. A later enhancement proposes removing automatic affirmation for specified resultants and gross flows. IRS stays separate. Named clearing-rule proposals retain their own schedules and entity scope. These additions do not resolve current precedence. [Canonical details](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day2-static-control-details).

### Static predicates and refresh scope

Day 2 hard-blocks a rule containing booking entity alone. Missing booking entity warns that all locations are covered. CCIL and BIC rules require their named method or flag conditions. Missing blank/null netting-ID filtering warns. Missing-filter warnings do not become hard blocks. Minute precision defaults to 00:00. FULL_STP bypasses NetCashflow, PendingAffirmation, and HighValue in its documented design, but remains disabled in the Day 1 UI. Maker/checker and checker-only levels retain distinct paths. [Static controls](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day2-static-control-details).

Creation refreshes eligible blank/null-netting-ID matches in specified WAITING or READY branches. It excludes PendingAnotherLeg, PendingAutoNetting, READY/PendingAck, HOLD, SUPPRESSED, NETTED, RELEASED, and SETTLED. Disable refreshes only tagged WAITING/PendingAutoNetting. Update both includes and excludes PendingAutoNetting in the source. The no-refresh alternative remains open. Day 2 permits automatic net-over-IRS-resultant despite generic no-net-over-net wording. [Refresh branches](../../../records/candidates/settlement/KT-settlement-auto-netting.md#refresh-and-type-scope).

### Dated flow and affirmation variants

Day 1 changes apply to new cashflows, with existing queues needing Operations attention. Its PendingAutoNetting controls allow warned SettleGross and manual netting, while bulkGross remains questioned. This differs from later technical restrictions. Its scenario resultants become WAITING/PendingException/PendingOperator, and components become NETTED. Manual un-net makes the resultant DEAD and returns components to WAITING/PendingException. These are expected scenarios, without execution proof. [Day 1 scope](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day1-differences-preserved). [Event expectations](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day1-event-expectations).

The affirmation-removal proposal distinguishes Interentity, Other, CCS, Clearing, and gross flows. Same-trade match can close PendingAffirmation in specified branches. Different-trade components need Operations approval. Clearing remains SwiftSuppressed while Unaffirmed. Interentity gross remains unchanged, and IRS remains unaffected. PendingNettingAffirmation is good-to-have. Mandatory manual-net affirmation removal remains undecided. Rebook exclusion and one-side-released interentity handling remain TBC. [Affirmation variants](../../../records/candidates/settlement/KT-settlement-auto-netting.md#proposed-affirmation-removal). [Outstanding scope](../../../records/candidates/settlement/KT-settlement-auto-netting.md#outstanding-enhancement-scope).

Named clearing proposals allow LCH/HKEX/ECLIPS IRS aggregation with other matching flows. TAIFEX/CITIC remain IRS-only. Previously SwiftSuppressed cashflows are unchanged. The setup sequence adds IRSNetting to netting rules before excluding it from suppression rules. Named times are HKEX/ECLIPS at VD 01:00 GMT and LCH at VD 12:00 GMT. Populated entity/counterparty scope requires owner confirmation. The ECLIPS existing-suppression concern remains source-reported and unverified. [Named clearing scope](../../../records/candidates/settlement/KT-settlement-auto-netting.md#named-clearing-rule-proposal).
