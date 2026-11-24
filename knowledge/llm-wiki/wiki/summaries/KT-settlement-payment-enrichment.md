---
type: Summary
description: "Summarizes candidate Nostro refresh, receipt ordering enrichment, SCI mapping, and India LEI payment rules."
doc_type: short
full_text: sources/KT-settlement-payment-enrichment.md
---

# Settlement payment enrichment

> **Source status:** Candidate/draft. The selected rules do not establish current regulatory approval or deployed payment behavior.

A fail/reinstate scenario requires held tasks to regenerate Nostro request data before accounting send. A separate netted/released/withdrawn example has no answer and remains unresolved. Receipt auto-stamping applies to selected SCB receipts with no Vostro and no SSI exception, and requires Notice to Receive `Y`; listed metals and ad-hoc SSI are excluded. Settlement means `NOS` remains an open condition. [Refresh Nostro data before accounting send](../../../records/candidates/settlement/KT-settlement-payment-enrichment.md#refresh-nostro-data-before-accounting-send) [Automatic receipt ordering information](../../../records/candidates/settlement/KT-settlement-payment-enrichment.md#automatic-receipt-ordering-information)

SCI enrichment prefers a source-defined bank BIC and falls back to SCI name, address, and country. Empty/error SCI results must not auto-populate. A separate India LEI request is limited to India branch FMID 4 and FMCODE `SCB BOMBAY*MMB` payments, INR/INO/INY with INR SWIFT currency, amount at least INR 500 million, and settlement means NOS; its SWIFT field placement retains exclusions. [SCI enrichment and empty-result behavior](../../../records/candidates/settlement/KT-settlement-payment-enrichment.md#sci-enrichment-and-empty-result-behavior) [India LEI payment scope](../../../records/candidates/settlement/KT-settlement-payment-enrichment.md#india-lei-payment-scope) [LEI sources and SWIFT layout](../../../records/candidates/settlement/KT-settlement-payment-enrichment.md#lei-sources-and-swift-layout)

Confirm effective regulatory scope, currency/field mappings, and missing-value behavior. See proposed [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]].
