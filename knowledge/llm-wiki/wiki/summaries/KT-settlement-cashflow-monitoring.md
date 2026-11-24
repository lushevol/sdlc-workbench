---
type: Summary
description: "Summarizes candidate settlement dashboard counters, group investigation paths, and timer predicates."
doc_type: short
full_text: sources/KT-settlement-cashflow-monitoring.md
---

# Cashflow dashboard and group monitoring

> **Source status:** Candidate/draft. Counter designs and timers do not establish current monitoring or production incidents.

Dashboard proposals route Group Pending and Group Pending Validation counters to filtered group views. Original trade ID and pending reasons support missing-payment investigation. Separate counters cover waiting or failed flows, future-window errors, accounting errors, SWIFT errors, and group states. The source gives date windows and status lists for some counters. [WF-CF-024](../../../records/candidates/settlement/KT-settlement-cashflow-monitoring.md#wf-cf-024) [WF-CF-063](../../../records/candidates/settlement/KT-settlement-cashflow-monitoring.md#wf-cf-063)

A timer proposal shows queued/pending-exception and group-pending indicators after more than five minutes. It still leaves group trade-validation mapping open. Queued and Hold counter predicates are blank, and local date/timezone are unspecified. [WF-CF-034](../../../records/candidates/settlement/KT-settlement-cashflow-monitoring.md#wf-cf-034) [Counter predicates and investigation context](../../../records/candidates/settlement/KT-settlement-cashflow-monitoring.md#counter-predicates-and-investigation-context)

The source distinguishes incomplete feed from trade-validation delay, but these are example investigation paths, not diagnosed production events. Entity/client/status dropdown inventories are incomplete. See [[summaries/ARC-platform-cashflow-data-query]] and proposed [[summaries/ARC-platform-cashflow-data-query]].

## Timer indicator scope

The timer proposal names QUEUED/pending-exception, Group Pending, and Group Pending Validation separately. All named indicators use the more-than-five-minutes condition. The Group Pending row retains its to-be-confirmed trade-validation mapping. [Canonical detail](../../../records/candidates/settlement/KT-settlement-cashflow-monitoring.md#timer-proposal-indicator-scope)
