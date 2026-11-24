---
type: Summary
description: "Summarizes dated RATAN payment-rounding responsibility, source amounts, persisted values, and unresolved semantics."
doc_type: short
full_text: sources/KT-ratan-payment-rounding-intent.md
---

# Dated payment-rounding intent

> **Source status:** Candidate/draft. H1 2024 material records historical intent, not current authority or implementation.

The source asks RATAN to round original Murex values tactically while Stella remains the strategic rounding target. It proposes querying precision and rounding type by payment currency, rounding the Murex or Stella source amount, removing trailing zeroes, and persisting the result as `Cashflow.Payment_Amount` for GUI, SWIFT, and accounting. Its 3.102-to-3.1 example does not validate the full currency table. [Dated responsibility](../../../records/candidates/operations/KT-ratan-payment-rounding-intent.md#dated-responsibility) [Source and destination](../../../records/candidates/operations/KT-ratan-payment-rounding-intent.md#source-and-destination)

The proposal describes four-down/five-up rounding and labels Round Down as floor, but also describes decimal truncation. All shown examples are positive, so negative amounts and tie handling remain unresolved. Missing currencies and effective configuration are also open. [Rounding semantics limit](../../../records/candidates/operations/KT-ratan-payment-rounding-intent.md#rounding-semantics-limit)

Confirm the current rounding owner, effective precision table, negative-amount behavior, and missing-value policy before applying this source. Related: [[summaries/KT-day2-manual-entity-settlement]] and proposed [[summaries/KT-day2-self-service-entity-onboarding]].
