---
type: Summary
description: "Preserves candidate static-data sources, cache-aside responsibilities, FileIT transfer behavior, and middleware alternatives."
doc_type: short
full_text: sources/KT-static-data-cache-p3.md
---

> **Candidate/draft only:** The source and cache designs are historical proposals with unresolved freshness and ownership rules. Owner is unknown; `verified` is empty.

# Static data cache p3

The selected design distinguishes externally owned reference data from Ratan-owned static data. It proposes golden-source dumps, EDMI updates, daily file changes, and end-of-day reconciliation. Vostro, Nostro, and counterparty datasets have different initialization and refresh routes; the selected SSI, account, and counterparty keys are examples, not a universal schema.

A stage-one cache-aside proposal covers settlement methods, Vostro SSI, and CES. Applications populate entries on misses and invalidate them after database writes. SSI reverse-index behavior and CES key/lifecycle details remain incomplete. Historical infrastructure alternatives include Redis for Day 1 and clustered Hazelcast as a later NFR improvement; the source set does not select a current environment architecture.

The FileIT contract proposes source-file removal after transfer. It distinguishes accepted/initiated responses from status 2000 and lists separate failure categories. Removal timing, retries, acknowledgement, retention, and reconciliation require decisions before treating this as an operating contract.

## Canonical sections

- [Reference-data ownership and reconciliation](../../../records/candidates/architecture/KT-static-data-cache-p3.md#reference-data-ownership-and-reconciliation)
- [Data-specific stamping responsibilities](../../../records/candidates/architecture/KT-static-data-cache-p3.md#data-specific-stamping-responsibilities)
- [Cache-aside service responsibility](../../../records/candidates/architecture/KT-static-data-cache-p3.md#cache-aside-service-responsibility)
- [Settlement file-transfer contract](../../../records/candidates/architecture/KT-static-data-cache-p3.md#settlement-file-transfer-contract)

## Related candidate topics

- [[summaries/KT-platform-strategic-ssi-stamping]]
- [[summaries/KT-ratan-nostro-golden-source-proposal]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.

## Historical field, key, and storage catalogs

The historical FileIT catalog distinguishes request and acknowledgement envelopes, field spelling, and transfer status codes. It separates ACCEPTED 1000, INITIATED 1100, and CFT_SUCCESSFUL 2000. Notification 5000 describes receiver-processing success; 5001 describes error-processing failure. Runtime schema compatibility remains unverified. [Canonical detail](../../../records/candidates/architecture/KT-static-data-cache-p3.md#historical-fileit-request-and-acknowledgement-fields)

The stage-one cache returns hits, fetches database values on misses, and invalidates entries after writes. The application controls population and freshness. Settlement-method keys combine booking entity, counterparty, taxonomy, and currency. SSI query hashes and reverse indexes need collision and update decisions. CES key and lifecycle details remain incomplete. [Canonical detail](../../../records/candidates/architecture/KT-static-data-cache-p3.md#stage-one-cache-population-and-key-contracts)

Storage branches depend on NFR sufficiency, dataset size, usage, ownership, and change frequency. The source leaves the exact one-hour boundary unspecified. Redis Day1 and later Hazelcast remain separate proposals. The six-node HA proposal leaves per-site allocation unconfirmed. [Canonical detail](../../../records/candidates/architecture/KT-static-data-cache-p3.md#historical-cache-storage-decision-branches)
