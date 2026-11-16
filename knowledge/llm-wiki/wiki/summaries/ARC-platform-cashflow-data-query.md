---
type: Summary
description: "Summarizes candidate cashflow query modeling, projections, notifications, partial errors, and history proposals."
doc_type: short
full_text: sources/ARC-platform-cashflow-data-query.md
---

# Platform cashflow data query

> **Source status:** Candidate/draft. The designs do not establish an approved schema, current service behavior, or accepted performance target.

The proposal models UI queries around logical fields owned by Rule Service, with versioned logical-to-XPath mappings and a foundation transformer. It describes current/history read models and physical-name transformations, but duplicate, missing, typed, and nullable field contracts remain unresolved. [Query modeling responsibilities](../../../records/candidates/architecture/ARC-platform-cashflow-data-query.md#query-modeling-responsibilities) [Read model and mapping limits](../../../records/candidates/architecture/ARC-platform-cashflow-data-query.md#read-model-and-mapping-limits)

Notification proposals refresh the blotter and update detail views when cashflow versions change. One interaction asks whether to reopen the latest version; another blocks actions behind a Refresh-only overlay. Dashboard and exception projections add status counts, date buckets, and exception-code lookups, with event coverage and field relationships still open. [Cashflow notification behavior](../../../records/candidates/architecture/ARC-platform-cashflow-data-query.md#cashflow-notification-behavior) [Dashboard and exception projections](../../../records/candidates/architecture/ARC-platform-cashflow-data-query.md#dashboard-and-exception-projections)

Aggregation proposals retain failed paths for retry and leave empty-value typing and full-failure responses undefined. History slimming alternatives require null-safety, processing compatibility, and duration checks; they do not authorize deletion. See [[summaries/KT-platform-query-performance]]. [Aggregation and partial error contract](../../../records/candidates/architecture/ARC-platform-cashflow-data-query.md#aggregation-and-partial-error-contract) [History slimming proposal](../../../records/candidates/architecture/ARC-platform-cashflow-data-query.md#history-slimming-proposal)
