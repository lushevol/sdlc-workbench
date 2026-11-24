---
type: Summary
description: "Summarizes candidate manual netting, resultant, validation, and un-net proposals with unresolved conflicts."
doc_type: short
full_text: sources/KT-settlement-manual-netting.md
---

# Manual netting and market-event reversal

> **Source status:** Candidate/draft. This summary does not establish approved policy, implementation, deployment, or acceptance.

The candidate separates bilateral, ad-hoc, CCIL, and beneficiary-BIC netting. It describes different grouping keys and marks bilateral auto-netting and CPN as backlog. [NET-M-001](../../../records/candidates/settlement/KT-settlement-manual-netting.md#net-m-001)

The bilateral API proposal requires matching entity, counterparty, currency, and payment date, with blank netting IDs and source-specific status allowlists. The GUI, API, and validation pages differ on eligible states, resultant settlement fields, DVP handling, split inputs, and identifier length. Treat these as unresolved variants. [Eligibility and preview](../../../records/candidates/settlement/KT-settlement-manual-netting.md#eligibility-and-preview) [Unresolved source differences](../../../records/candidates/settlement/KT-settlement-manual-netting.md#unresolved-source-differences)

The designs propose maker-checker review, a queued resultant, and a distinct un-net path. Economic component events can trigger automatic un-netting; released resultants follow a separate withdrawal lifecycle. Rounding, zero-total direction, accounting, reconciliation, value-date cutoffs, and Stella write-back remain open. [Calculation, resultant, and review](../../../records/candidates/settlement/KT-settlement-manual-netting.md#calculation-resultant-and-review) [Manual un-net and economic amendments](../../../records/candidates/settlement/KT-settlement-manual-netting.md#manual-un-net-and-economic-amendments)

This topic concerns manual and event-driven flows; scheduled auto-netting has separate candidate rules. See [[concepts/cashflow-netting-grouping-and-outcomes]] and the proposed [[summaries/KT-settlement-interest-and-nds-netting]].
