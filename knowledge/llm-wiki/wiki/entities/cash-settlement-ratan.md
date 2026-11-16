---
type: Product
description: "Settlement-processing system with source-scoped lifecycle, netting, instruction, query, and downstream accounting responsibilities."
sources: ["summaries/ARC-settlement-platform-p3.md", "summaries/INT-KT-ratan-cashflow-settlement-interfaces.md", "summaries/KT-settlement-cashflow-identity-and-stella-write-back.md", "summaries/INT-KT-payment-accounting-contracts.md"]
---

# Cash Settlement RATAN

> Derived from candidate/draft canonical records. Current authority, implementation, execution, and publication remain unconfirmed.

## Responsibilities

The retained architecture assigns cashflow creation, materialization, lifecycle, netting, and fail/reinstate to RATAN. Group management assembles messages and handles validation or confirmation. Camunda coordinates STP, exception review, and technical failures. These are historical proposed service boundaries. [Strategic service responsibilities](../../../records/candidates/architecture/ARC-settlement-platform-p3.md#strategic-service-responsibilities)

The legacy team and its CES application mapping have a separate page, [[entities/ratan]]. This Product page connects the settlement responsibilities described in [[summaries/ARC-settlement-platform-p3]].

## Producers and retrieval consumers

[[entities/murex]] supplies source-scoped cashflow input. [[entities/stella]] participates in cashflow creation, version ownership, and status write-back proposals. [[entities/uber]] connects snapshot input with standardization, lifecycle, and historical-message compatibility. Producer identity and event fields retain their own contracts. [Identity and producer distinctions](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#identity-and-duplicate-handling)

The interface inventory lists FMMIS, CIS, PacMan, MarketUDP/SSDR, and CNEDMp as RATAN REST-query consumers. FXU separately queries cashflow status and exchanges utilization messages. SSI+ provides instruction queries and change notifications. These declarations leave current schemas, access conditions, and deployed connectivity unresolved. [Accounting and query consumers](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#payment-accounting-and-downstream-reporting). [Cashflow, FXU, and SSI interfaces](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing)

## Downstream boundaries

Aspire, eBBS, and Korea OLTP have destination-specific accounting milestones, acknowledgement meanings, and recovery rules. The interim Korea TLM query uses accounting-task history and a three-day maximum span. [[concepts/accounting-delivery-and-status-write-back]] connects these conditions with producer-status updates. [Destination accounting contracts](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-07--korea-interim-tlm-query)

[[concepts/netting-types-and-resultants]] connects the manual, scheduled, CCIL, CPN, IRS, and NDS scopes. Type-specific grouping and released-payment controls require their cited canonical clauses. [Netting architecture](../../../records/candidates/architecture/ARC-settlement-platform-p3.md#strategic-service-responsibilities)

## Open authority and ownership

The architecture and interfaces describe intended responsibilities. Their current owners, effective revisions, runtime state, and acceptance evidence remain unresolved. Reopen the canonical clauses before selecting a producer, query, or accounting contract. [Architecture limits](../../../records/candidates/architecture/ARC-settlement-platform-p3.md#evidence-limits). [Interface questions](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#open-questions)
