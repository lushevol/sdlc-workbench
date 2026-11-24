---
type: "Concept"
sources: ["summaries/KT-settlement-auto-netting.md"]
description: "How matching cashflows are assigned to a rule for scheduled auto-netting."
---

# Auto-Netting Rule Selection

Auto-netting rule selection identifies the live rule for a matching cashflow. A match queues the cashflow for scheduled processing. If multiple rules match, precedence determines which rule the job uses for grouping.

## Documented selection logic

The Day 2 requirement ranks matching netting types by the lowest configured priority number. When multiple matching rules have the same netting type, it selects the rule created most recently. A September 2026 flow summary additionally says that evaluation ends at the first match in priority order.

These statements describe candidate behavior, not a confirmed effective policy. An earlier entry in the Day 2 clarification history gives creation time as the selection basis without the same netting-type priority detail. The 2024 Day 1 requirement instead prioritizes the earliest scheduled job. The source set therefore leaves precedence dependent on which requirement and scope apply.

## Operational implications

A live rule match sends the cashflow to Pending Auto Netting for the scheduled job. Rule identity then matters during grouping: cashflows are combined only when they match the same rule and have identical values for all configured execution-key fields. See [[concepts/cashflow-netting-grouping-and-outcomes]] for grouping and outcome details, and [[concepts/auto-netting-scheduling]] for scheduling differences.

The Day 2 requirement lists refresh behavior for rule creation, update, and disable. Its clarification history records a no-refresh alternative. Day 2 permits a reinstated single cashflow to match again. The September summary says cashflows produced by an un-net do not re-enter auto-netting evaluation. The applicable behavior for each trigger remains unresolved.

## Open policy questions

- Does netting-type priority, rule creation time, or scheduled-job time govern competing matches in each scope?
- Does evaluation stop at the first match, and how are ties resolved?
- Which rule changes refresh existing evaluation, and can reinstated or un-netted cashflows re-enter?

For the source distinctions and evidence limits, see [[summaries/KT-settlement-auto-netting]].

## Source-scoped static and refresh controls

The Day 2 type list orders SALMTM, SALCoupon, ClearingSwiftSuppress, CCIL, BIC, and Bilateral. Selection still uses configured priority and latest creation within one type. This list supplies no universal priority for other netting workflows. CCIL and BIC static require their documented method or flag conditions. Booking-entity-only creation hard-blocks. Missing booking entity warns about all-location scope. Missing blank/null netting-ID filtering also warns. [Static predicates](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day2-static-control-details). [Type scope](../../../records/candidates/settlement/KT-settlement-auto-netting.md#refresh-and-type-scope).

Creation, disabling, and updates have different refresh populations. Creation excludes PendingAutoNetting, while disable refreshes only tagged WAITING/PendingAutoNetting. The update wording both includes and excludes that state. Its no-refresh alternative remains unresolved. Day 1 instead limits changes to new cashflows and leaves queued items to Operations. These differences do not establish one current refresh policy. [Refresh branches](../../../records/candidates/settlement/KT-settlement-auto-netting.md#refresh-and-type-scope). [Day 1 boundary](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day1-differences-preserved).
