---
type: Summary
description: "Summarizes candidate clearing-payment safeguards, Swap Agent splits, accounting mappings, and empty-flow proposals."
doc_type: short
full_text: sources/KT-settlement-clearing-and-swap-agent-boundaries.md
---

# Settlement clearing and Swap Agent boundaries

> **Source status:** Candidate/draft. The source set contains historical proposals with unresolved accounting and netting rules.

The clearing objective blocks original bilateral payments from STP before novation. Post-novation clearing payments require accounting without bilateral settlement. A trade-level clearing marker or source-system NSTP rule is proposed; the latter requires evidence that legitimate non-clearing trades will not be stopped. [Clearing payment safety objective](../../../records/candidates/settlement/KT-settlement-clearing-and-swap-agent-boundaries.md#clearing-payment-safety-objective)

An earlier Swap Agent design settles initial/final principal bilaterally and accounts for interim coupon/principal through Main Nostro. It says no netting, while a later dated mapping requires netting for specified coupon/MTM flows without a netting ID. The SSI assignment also has inconsistent trade numbering. [Swap Agent payment split](../../../records/candidates/settlement/KT-settlement-clearing-and-swap-agent-boundaries.md#swap-agent-payment-split) [Dated payment mapping and accounting narrative](../../../records/candidates/settlement/KT-settlement-clearing-and-swap-agent-boundaries.md#dated-payment-mapping-and-accounting-narrative)

A separate empty-flow proposal uses RECALC/SWAP_AGENT, trade reference zero, and blank typology, and describes R-prefixed flow trade IDs alongside MTR-prefixed original IDs. Dummy-identity removal remains unresolved. Confirm clearing control and payment/SSI/accounting contracts before use. [Exceptional empty-flow proposal](../../../records/candidates/settlement/KT-settlement-clearing-and-swap-agent-boundaries.md#exceptional-empty-flow-proposal)
