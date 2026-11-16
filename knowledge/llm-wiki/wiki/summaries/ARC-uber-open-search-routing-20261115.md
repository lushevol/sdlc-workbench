---
type: Summary
description: "Preserves proposed OpenSearch query budgets, staged PostgreSQL fallback, reconciliation, model alignment, and recovery."
doc_type: short
full_text: sources/ARC-uber-open-search-routing-20261115.md
---

> **Candidate/draft only:** Query targets, fallback, and migration controls remain design proposals. Owner is unknown; `verified` is empty.

# Uber OpenSearch routing

The selected plan aims to reduce relational-database pressure and improve cashflow, detail, and dashboard queries. It proposes two-second budgets for 20,000-record cashflow/group pages and dashboard loads, and a volume bound instead of a 30-day date limit. An earlier proposal retains one-month value-date language; targets are not accepted SLAs.

The staged design defaults internal queries to OpenSearch while retaining PostgreSQL persistence and a production switchback. Historical migration uses a cutoff and idempotent processing. Real-time reconciliation compares lifecycle history, query PostgreSQL, and OpenSearch. A separate proposal calls for parallel operation before removing database dependency; neither proves a completed migration or authorizes decommissioning.

The plan requires aligned protobuf, GraphQL, and OpenSearch models, and separates internal from planned V2 external queries. It proposes a DLT index and replay for missing data. Reconciliation should identify exact missing cashflows. Execution and the cross-cluster replication contract remain unverified. The active [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]] describes related cashflow query APIs, not this OpenSearch design.

## Canonical sections

- [Business-live query target](../../../records/candidates/architecture/ARC-uber-open-search-routing-20261115.md#business-live-query-target)
- [Staged adoption and fallback](../../../records/candidates/architecture/ARC-uber-open-search-routing-20261115.md#staged-adoption-and-fallback)
- [Models, external consumers, and recovery](../../../records/candidates/architecture/ARC-uber-open-search-routing-20261115.md#models-external-consumers-and-recovery)

## Related candidate topics

- [[summaries/KT-advanced-search-p3]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
