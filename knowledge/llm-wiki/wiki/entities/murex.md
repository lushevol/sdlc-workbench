---
type: Product
description: "Producer with distinct Murex 2.11, regional adaptor, operational DOI, and Korea settlement contracts."
sources: ["summaries/INT-KT-murex-ratan-feed-lifecycle.md", "summaries/KT-settlement-korea-trade-confirmation.md", "summaries/KT-settlement-cashflow-identity-and-stella-write-back.md"]
---

# Murex

> Derived from candidate/draft canonical records. Current authority, implementation, execution, and publication remain unconfirmed.

## Settlement and trade boundaries

The Murex 2.11 migration sources retain trade accounting to Aspire. Eligible non-precious settlement flows use [[entities/cash-settlement-ratan]] and Razor. The proposal suppresses the corresponding Murex settlement accounting, LMS, and FMSRE output to avoid duplication. Precious-metal and migration-cohort boundaries retain separate conditions. [Responsibility and cohort boundaries](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#responsibility-and-cohort-boundaries)

## Feed windows and publishing cohorts

The retained sources describe several windows. The CN/SG/IN/MY adaptor uses nine calendar days. The earlier operational DOI uses weekday batches of 110 every 15 minutes. The H2 DOI uses seven system business days. Near-date batches contain 500 payments every five minutes. Future batches contain 6,000 payments every two hours. Each cohort has its own operating window and calendar. Later document revisions supply no blanket supersession decision. [Window and publishing variants](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#window-and-publishing-variants)

## Identity, status, and recovery

Original lineage, creator transaction, payment-originating trade, and latest trade have distinct meanings. The adaptor's Parent_Trade_Id mapping uses TrnOrginalID, creating a naming mismatch with creator-parent terminology. Defaults and withdrawal versions retain their specific mapping scope. [[entities/stella]] has a separate version-ownership proposal. [Identity and conversion](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#identity-versions-and-conversion)

The regional adaptor updates Murex on RATAN RELEASED and excludes SETTLED synchronization. Sources disagree on RLSR/RSLR spelling and whether the monitor label denotes release or settlement. DOI guidance caps manual publication at 30 payments and differs from older automatic-republication recovery. Receipt ACK, release, and settlement therefore require exact source selection. [Status, acknowledgement, and recovery](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#status-acknowledgement-and-manual-recovery)

## Korea confirmation scope

The Korea proposal uses MXML over IBM MQ to deliver COMP for the RATAN payment-STP gate. Cancel-and-reissue cancels the old unconfirmed cashflow and makes the replacement wait for its own COMP. Trade/version association and the strategic switch remain open. [Confirmation gate](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#confirmation-gate). [Tactical transport](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#transport-options)

## Retrieval and evidence limits

[[summaries/INT-KT-murex-ratan-feed-lifecycle]] retains the cohort matrix, exclusions, mappings, recovery, and retention clauses. [[concepts/accounting-delivery-and-status-write-back]] explains destination and producer acknowledgement boundaries. Current authority, mapping versions, eligible entities, and execution evidence remain unresolved. [Open questions](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#open-questions)
