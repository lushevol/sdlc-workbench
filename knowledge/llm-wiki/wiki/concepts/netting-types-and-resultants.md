---
type: Concept
description: "Connects type-specific grouping, resultant identity, approval, and release boundaries across netting proposals."
sources: ["summaries/KT-settlement-auto-netting.md", "summaries/KT-settlement-manual-netting.md", "summaries/KT-settlement-ccil-netting.md", "summaries/KT-settlement-cpn-netting.md", "summaries/KT-settlement-interest-and-nds-netting.md", "summaries/KT-settlement-cashflow-identity-and-stella-write-back.md"]
---

# Netting types and resultants

> Derived from candidate/draft canonical records. Current authority, implementation, execution, and publication remain unconfirmed.

## Grouping depends on the selected netting scope

Scheduled auto-netting combines cashflows only when rule identity and every configured execution-key value match. Its documented Bilateral key contains booking entity, counterparty, payment currency, and payment date. [[concepts/auto-netting-rule-selection]], [[concepts/auto-netting-scheduling]], and [[concepts/cashflow-netting-grouping-and-outcomes]] retain the scheduled workflow. [Grouping and outcome](../../../records/candidates/settlement/KT-settlement-auto-netting.md#grouping-and-outcome)

The manual matrix separates bilateral, ad-hoc, CCIL, and beneficiary-BIC actions. Bilateral adds counterparty; non-guaranteed CCIL omits it; BIC adds beneficiary BIC. A broader backend counterparty-equality proposal conflicts with CCIL's different-counterparty permission. Conflicting matrix expressions and GUI/API status gates remain unresolved. [Manual type keys](../../../records/candidates/settlement/KT-settlement-manual-netting.md#net-m-001). [CCIL counterparty conflict](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-031). [CCIL status gates](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-032)

CPN's business proposal requires equal entity, counterparty, currency, and value date. NDS additionally groups by NID and requires its source-specific eligible states. IRS aggregation and NDS fixing retain product and regional predicates. These scopes require their own canonical clauses. [CPN manual netting](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#manual-and-ad-hoc-netting). [NDS grouping](../../../records/candidates/settlement/KT-settlement-interest-and-nds-netting.md#l3-nds-01--nds-scope-and-scheduler)

## Resultant identity and approval

The identity design gives netting resultants an N prefix plus 11 digits and requires concurrent uniqueness. Indonesia's SID/NID proposal leaves namespace replacement and capacity unresolved. A common netting ID links components and resultants in the CPN design. Identifiers retain producer and workflow meaning. [Identity rules](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#identity-and-duplicate-handling). [CPN linkage](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#manual-and-ad-hoc-netting)

Resultant state and affirmation vary. Manual service proposals create Queued resultants, while Day 1 scheduled scenarios use WAITING/PendingException/PendingOperator. CCIL mapping proposes QUEUED/Unaffirmed, but its scenario expects an affirmed resultant. CPN business and technical examples differ between Pending Release and Reviewed after approval. These differences supply no universal resultant state. [Manual resultant review](../../../records/candidates/settlement/KT-settlement-manual-netting.md#calculation-resultant-and-review). [Scheduled Day 1 examples](../../../records/candidates/settlement/KT-settlement-auto-netting.md#day1-event-expectations). [CCIL mapping](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-027). [CCIL scenario](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-028). [CPN review sequence](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#manual-and-ad-hoc-netting)

## Released-payment boundary

The CPN technical draft preserves a released resultant and creates a linked reversal for Operations. The NDS proposal disallows system/manual un-net after payment release and routes reversal/rebook through manual handling. Other manual sources retain conflicting release guards. Event, product, and release state therefore determine the applicable path. [CPN component events](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#component-amendment-and-cancellation). [NDS release rules](../../../records/candidates/settlement/KT-settlement-interest-and-nds-netting.md#l3-nds-03--nds-amendment-and-resultant-rules). [Manual source differences](../../../records/candidates/settlement/KT-settlement-manual-netting.md#unresolved-source-differences)

## Retrieval and unresolved authority

Use this concept to select the correct specialist summary before comparing rules or resultant fields. [[entities/cash-settlement-ratan]] provides processing context. [[concepts/accounting-delivery-and-status-write-back]] retains downstream consequences. Effective type scope, rule precedence, state mappings, owner approval, and executed behavior remain unresolved. [Auto-netting questions](../../../records/candidates/settlement/KT-settlement-auto-netting.md#open-questions). [Manual-netting questions](../../../records/candidates/settlement/KT-settlement-manual-netting.md#open-questions)
