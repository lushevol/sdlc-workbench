---
type: Summary
description: "Summarizes candidate regional failover, messaging recovery, object payload storage, and recovery target alternatives."
doc_type: short
full_text: sources/INT-KT-regional-recovery-and-payload-storage.md
---

# Regional recovery and payload-storage proposals

> **Source status:** Candidate/draft. Topologies, targets, and POCs are not approved or verified recovery capabilities.

Active-passive proposals compare VIP switching with isolated dual profiles and several Kafka replication or reconciliation options. Middleware analysis targets RTO at most two hours and RPO zero, but asynchronous MirrorMaker can lag and cannot alone prove zero loss. The MirrorMaker test matrix and DR rehearsal remain incomplete. [DR-01](../../../records/candidates/settlement/INT-KT-regional-recovery-and-payload-storage.md#dr-01--active-passive-topology-alternatives) [DR-02](../../../records/candidates/settlement/INT-KT-regional-recovery-and-payload-storage.md#dr-02--messaging-recovery-objectives-and-options) [DR-03](../../../records/candidates/settlement/INT-KT-regional-recovery-and-payload-storage.md#dr-03--mirrormaker-poc-scope)

The object-storage proposal separates raw payloads from PostgreSQL metadata, with checksums, streamed reads, retries, orphan cleanup, and reference checks. Storage-site targets differ from messaging targets: the selected full-site values are RPO below 30 seconds and RTO below 15 minutes. Security roles and outage handling remain unresolved. Migration's backfill-clear step conflicts with retaining legacy data for rollback. [DR-04](../../../records/candidates/settlement/INT-KT-regional-recovery-and-payload-storage.md#dr-04--object-storage-and-consistency-proposal) [DR-05](../../../records/candidates/settlement/INT-KT-regional-recovery-and-payload-storage.md#dr-05--storage-security-and-recovery-scope)

Benchmarks and targets are proposed values, not measured results. See [[summaries/KT-ratan-dr-operations]] and proposed [[summaries/INT-KT-indonesia-regional-architecture]].
