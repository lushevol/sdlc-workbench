---
type: Summary
description: "Summarizes candidate FX utilization, accounting, SWIFT suppression, status, and remaining-amount duties."
doc_type: short
full_text: sources/KT-settlement-fx-utilization-responsibilities.md
---

# Settlement FX utilization responsibilities

> **Source status:** Candidate/draft. Historical FX utilization design does not establish current responsibilities or controls.

The design assigns FX utilization settlement to Transaction Banking systems while RATAN generates accounting. It classifies utilization using booking entity and counterparty. Utilization cashflows suppress RATAN SWIFT but retain accounting; utilization status returns to FXU and TDS3 to lock trade amendments. [FX utilization responsibility](../../../records/candidates/settlement/KT-settlement-fx-utilization-responsibilities.md#fx-utilization-responsibility)

A remaining-amount query supports further utilization and reverse-trade booking. Past-due automatic utilization and partial accounting are identified as Day 2 proposals. These historical Day 2 proposals do not establish current approval or rollout. Eligibility, remaining-amount calculation, accounting-date rules, and amendment-lock behavior remain open in the source. [Open questions](../../../records/candidates/settlement/KT-settlement-fx-utilization-responsibilities.md#open-questions)

Confirm the split between settlement and accounting systems, classification keys, status consumers, and remaining-balance semantics before relying on this design. Related: [[summaries/INT-KT-fxu-integration-contract]], [[summaries/ARC-settlement-platform-p3]], and [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]].
