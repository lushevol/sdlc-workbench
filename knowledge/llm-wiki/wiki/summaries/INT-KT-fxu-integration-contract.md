---
type: Summary
description: "Summarizes FX utilization phases, controls, interfaces, accounting, and unresolved contract variants."
doc_type: short
full_text: sources/INT-KT-fxu-integration-contract.md
---

# FX utilization phases and integration contract

> **Source status:** Candidate/draft. The source set records proposals and historical designs; it does not establish current approval or deployed behavior.

The proposed MVP covers FX Spot, Forward, and Swap, and accepts full-utilization requests. UTIL settlement is blocked from gross settlement; partial, reversal, early, and past-due flows are assigned to later phases. Remaining amounts, eligibility, maker/checker context, and downstream accounting or reporting are shared across FXU, RATAN, Blade, TLM, and other named consumers. [FXU-03](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-03--mvp-utilization-scope) [FXU-04](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-04--phase-2-accounting-and-time-scope)

Method-change actions have state, product, source, and amount predicates. Phase-specific validator tables must remain separate; their retry, NACK, and exception paths do not form one timeless contract. State terminology also differs between the glossary and transition table. [FXU-05](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-05--settlement-method-action-predicates) [FXU-06](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-06--validation-and-rejection-contract) [FXU-09](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-09--utilization-processing-and-state-design)

The designs propose accounting identities, ACK/NACK messages, and recovery controls, but leave acceptance boundaries, timing precedence, integration topology, and some state outcomes unresolved. Blade's data-access option is also unselected. [FXU-02](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-02--blade-data-access-decision-remains-open) [FXU-10](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-10--pastdue-and-accounting-identity-design) [FXU-RECOVERY](../../../records/candidates/settlement/INT-KT-fxu-integration-contract.md#fxu-recovery--technical-readiness-recovery-requirements)

Related pages: [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]], [[entities/fmaa]], and proposed [[summaries/KT-settlement-fx-utilization-responsibilities]].
