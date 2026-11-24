---
type: Summary
description: "Summarizes the candidate RATAN WAT-to-ARK and ARK-to-WAT recovery checklist and timing limits."
doc_type: short
full_text: sources/KT-ratan-dr-operations.md
---

# RATAN disaster recovery coordination

> **Source status:** Candidate/draft runbook content. The listed schedule and procedures do not establish current readiness or an executed failover.

The WAT-to-ARK path coordinates database, NAS, network, and VM failover before checking RATAN health and reporting completion. Network reinstatement requires a second health check and DR-page update. The return path expects active-active RATAN, checks EOD status with ETL squads, and restarts the A node after network restoration. Sunday MLZ jobs should be held when the P node is unavailable because they run only there. [WAT to ARK](../../../records/candidates/operations/KT-ratan-dr-operations.md#wat-to-ark) [ARK to WAT](../../../records/candidates/operations/KT-ratan-dr-operations.md#ark-to-wat)

Approximate entries of 04:00 for failover and 10:05 for network reinstatement depend on coordinated infrastructure status. They are not a fixed schedule or proof of a successful recovery. [Approximate timing](../../../records/candidates/operations/KT-ratan-dr-operations.md#approximate-timing)

The source does not identify the current runbook owner, topology revision, infrastructure readiness, or evidence required for EOD completion. See [[summaries/INT-KT-regional-recovery-and-payload-storage]] and proposed [[summaries/INT-KT-indonesia-regional-architecture]].
