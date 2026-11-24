---
type: "Concept"
sources: ["summaries/KT-settlement-auto-netting.md"]
description: "How eligible cashflows are queued and processed by scheduled auto-netting jobs."
---

# Auto-Netting Scheduling

Auto-netting scheduling determines when eligible cashflows are held for processing and when a scheduled job picks them up. A live rule match sends a cashflow to Pending Auto Netting; the job then processes queued cashflows using the configured netting date and time. Scheduling is distinct from [[concepts/auto-netting-rule-selection]], which determines which rule applies, and [[concepts/cashflow-netting-grouping-and-outcomes]], which covers grouping and resultant cashflow handling.

## Scheduling details and policy differences

The source records do not establish one effective scheduling policy across all scopes:

- **Calendar basis:** A Day 1 requirement uses the booking entity’s home-currency calendar. The Day 2 requirement uses the cashflow-currency calendar and retains the payment date for a value-date rule. A later design discussion proposes skipping weekends only.
- **Late arrivals.** Day 1 sends late arrivals to manual netting. The 16 May 2025 Day 2 decision records queueing eligible cashflows before or after the scheduled time. A later discussion proposes a configurable action.
- **Rule changes and queue refresh:** Day 2 lists refresh behavior for rule creation, update, and disable, but its clarification history also records a no-refresh alternative.

These differences are unresolved; the applicable policy needs confirmation for each scope. See [[summaries/KT-settlement-auto-netting]] for the source comparison and evidence limits.

## Scope

This concept describes scheduling aspects of the candidate scheduled cash settlement auto-netting workflow. It does not establish approved production policy or cover other netting workflows.

## Timing granularity and named scopes

Day 2 static supports minute precision with a 00:00 default. That default supplies no universal production execution time. Named clearing proposals use VD 01:00 GMT for HKEX/ECLIPS and VD 12:00 GMT for LCH. TAIFEX/CITIC remain IRS-only. Exact populated entity/counterparty scope still needs owner confirmation. [Static timing](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day2-static-control-details). [Named clearing schedules](../../../records/candidates/settlement/KT-settlement-auto-netting.md#named-clearing-rule-proposal).

The later calendar discussion accepts holidays in a source-reported response and proposes manual netting before holiday leave. It allows release date to precede auto-netting date. Its configurable withdrawal/new re-netting or manual-queue options conflict with the 16 May 2025 Day 2 decision. No general calendar or late-arrival precedence is established. [Calendar discussion](../../../records/candidates/settlement/KT-settlement-auto-netting.md#calendar-and-late-arrival-discussion).
