---
type: Product
description: "Upstream cashflow and version owner in source-scoped lifecycle and FX status-write-back proposals."
sources: ["summaries/KT-settlement-cashflow-identity-and-stella-write-back.md", "summaries/KT-settlement-fx-utilization-responsibilities.md", "summaries/INT-KT-fxu-integration-contract.md"]
---

# Stella

> Derived from candidate/draft canonical records. Current authority, implementation, execution, and publication remain unconfirmed.

## Cashflow and version responsibilities

The China onboarding proposal assigns cashflow generation and business/cashflow version ownership to Stella. RATAN advances an internal minor version and resets it for a new Stella business version. The proposal sends Released and Settled back to Stella. Payment Date supports SWIFT scheduling while Stella Value Date stays unchanged. These dated responsibilities retain unresolved applicability. [Lifecycle and acknowledgement](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#stella-lifecycle-and-acknowledgement)

The identity proposal retains Stella's 12-character cashflow ID. Uber duplicate handling and Stella business-version/status-event filtering describe separate version contracts. Original trade-ID stability has a source-reported Murex Counterparty Assignment exception. [Identity and duplicate handling](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#identity-and-duplicate-handling)

## FX write-back and concurrency

The FX proposal routes Razor statuses through [[entities/cash-settlement-ratan]] to Stella. Named events can mark a matched cashflow SUSPENDED-MATURED to reduce duplicate-payment risk. Fee handling, resultant exclusions, matching fields, tolerances, and currency-removal proposals retain separate scope. Concurrent amendment with release or netting can reject write-back. Atomicity and recovery remain unresolved. [FX status write-back](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#fx-status-write-back). [Concurrent lifecycle limits](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#stella-lifecycle-and-acknowledgement)

## Utilization and Blade alternatives

One FX-utilization responsibility source returns status to FXU and TDS3 for trade-amendment locking. The detailed FXU design separately proposes domain-event synchronization of Utilize, PartiallyUtilize, and Unutilize to Stella. Their exact event and acceptance contracts require reconciliation. [Utilization responsibilities](../../../records/candidates/settlement/KT-settlement-fx-utilization-responsibilities.md#fx-utilization-responsibility). [FXU state design](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-09--utilization-processing-and-state-design)

The Blade analysis compares replication through Stella/TDS3, direct RATAN query, and OpenFin display. The retained analysis selects no option. Human visibility through OpenFin supplies no Blade backend control. [Blade data-access alternatives](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-02--blade-data-access-decision-remains-open)

## Retrieval and unresolved contracts

[[summaries/KT-settlement-cashflow-identity-and-stella-write-back]] retains identity, FX matching, and acknowledgement questions. [[concepts/accounting-delivery-and-status-write-back]] connects producer updates with their separate accounting milestones. Source approval, applicable flows, current ownership, version-conflict recovery, and execution remain unconfirmed. [Open questions](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#open-questions)
