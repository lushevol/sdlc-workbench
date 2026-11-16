---
type: Summary
description: "Summarizes candidate query, batch, queue, UI, and database performance proposals with unresolved measures."
doc_type: short
full_text: sources/KT-platform-query-performance.md
---

# Platform query performance

> **Source status:** Candidate/draft. The proposals do not establish accepted SLAs, deployed tuning, or verified capacity.

A value-date search proposal defaults missing dates to today for non-ID searches and blocks ranges over one month; exactly one month is unresolved. A separate page-size analysis limits its NFR scope to selected indexed predicates and leaves page-size turnaround and `pg_hint_plan` unresolved. [Value-date search proposal](../../../records/candidates/performance/KT-platform-query-performance.md#value-date-search-proposal) [Blotter performance and SLA scope](../../../records/candidates/performance/KT-platform-query-performance.md#blotter-performance-and-sla-scope)

Batch proposals move lifecycle work into a transaction, fetch and persist in batches, and offer alternative lock strategies or asynchronous completion. Separate Uber proposals describe eight queues and seven topics. Their queue/topic topology remains unreconciled. Kafka listener tracking, environment timeouts, and UI timing/config-loading approaches remain designs. [Batch transaction responsibilities](../../../records/candidates/performance/KT-platform-query-performance.md#batch-transaction-responsibilities) [Uber processing and capacity proposals](../../../records/candidates/performance/KT-platform-query-performance.md#uber-processing-and-capacity-proposals) [Environment and listener tracking design](../../../records/candidates/performance/KT-platform-query-performance.md#environment-and-listener-tracking-design)

A PostgreSQL proposal suggests session `work_mem` and JSONB expression-index changes, subject to database-memory review. Historical UI timings are examples, not current targets. This canonical review establishes no executed effect. Reported memory estimates and test results remain separate task evidence. [L3-PG-01](../../../records/candidates/performance/KT-platform-query-performance.md#l3-pg-01--cashflow-query-service-optimization-proposal) [UI timing and loading proposals](../../../records/candidates/performance/KT-platform-query-performance.md#ui-timing-and-loading-proposals)

See [[concepts/frontend-performance]] for separate portal performance evidence and proposed [[summaries/ARC-platform-cashflow-data-query]].
