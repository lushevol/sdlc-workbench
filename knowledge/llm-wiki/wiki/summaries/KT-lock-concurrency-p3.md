---
type: Summary
description: "Compares candidate cashflow-lock ownership, atomicity, retry, timeout, and migration contracts."
doc_type: short
full_text: sources/KT-lock-concurrency-p3.md
---

> **Candidate/draft only:** Lock alternatives, APIs, and configuration lack current approval and consumer verification. Owner is unknown; `verified` is empty.

# Cashflow lock concurrency p3

The selected process keys locks by cashflow ID. UI retry is manual, while listed workflow and status updates retry automatically; the source does not set delay, maximum attempts, or terminal handling. Redesign options require atomic lock/unlock, explicit owner responsibilities, exceptional release, and batch acquisition across netting components. Partial acquisitions should release when a batch fails. Enhanced Redis and Redisson alternatives differ in validation and renewal behavior.

The design identifies parent/child timeout and partial batch-processing risks. It proposes idempotent APIs with last-result retrieval and aligned request and rebalance timeouts; those proposals do not prove consistency or retry safety.

The migration guide changes the second argument from expiry milliseconds to wait-time seconds, while the watchdog manages duration. Existing call shapes can therefore change meaning. Release notes also name a Foundation feature and Spring Boot 3.4.4 dependency. No consumer migration, mixed-version compatibility, or deployed lock behavior was inspected.

## Canonical sections

- [Lock ownership and atomicity design](../../../records/candidates/architecture/KT-lock-concurrency-p3.md#lock-ownership-and-atomicity-design)
- [Timeout and interservice consistency limits](../../../records/candidates/architecture/KT-lock-concurrency-p3.md#timeout-and-interservice-consistency-limits)
- [Migration API semantics](../../../records/candidates/architecture/KT-lock-concurrency-p3.md#migration-api-semantics)
- [Shared event and Redis configuration proposals](../../../records/candidates/architecture/KT-lock-concurrency-p3.md#shared-event-and-redis-configuration-proposals)

## Related candidate topics

- [[summaries/INT-KT-cashflow-amendment-and-release-controls]]
- [[summaries/KT-platform-uber-migration-contracts]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
