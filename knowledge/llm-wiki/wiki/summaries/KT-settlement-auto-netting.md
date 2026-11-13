---
type: "Summary"
description: "Documents scheduled cash settlement auto-netting rules, grouping, outcomes, and unresolved policy differences."
doc_type: short
full_text: "sources/KT-settlement-auto-netting.md"
---

> Derived from [KT-settlement-auto-netting, version 1](../../../records/candidates/settlement/KT-settlement-auto-netting.md), candidate/draft. [Source bindings](../../source-manifest.json).

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
