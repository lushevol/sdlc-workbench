---
type: Summary
description: "Summarizes beneficiary-BIC netting eligibility, matching, resultant, and affirmation proposals with key differences unresolved."
doc_type: short
full_text: sources/KT-settlement-beneficiary-bic-netting.md
---

> **Candidate/draft only:** Requirement, minutes, demo cases, and resultant fields do not establish approved or executed BIC-netting behavior.

# Beneficiary BIC Netting

The candidate proposes configurable beneficiary-BIC eligibility and operator-controlled manual grouping, with BIC netting before bilateral manual netting. The London description names beneficiary BIC through SCI mediumUsage=MXR; its Payment Date ≥ Today filter is struck through. Execution requires BIC_Net=Y and Pending Netting, with equal BIC, value date, currency, and entity across components.

The prototype key omits Family, Group, Type, Typology, and Strategy, which appear in July 2024 minutes. This product-key difference remains unresolved. The proposed resultant uses a generated ID, QUEUED status, GROSS settlement, and CASH delivery. Payment type is blank in the mapping, while a demo expects Ben BIC Netting. Counterparty selection is described as random. Other attributes copy from the first cashflow, whose order is unspecified.

The minutes place affirmation after resultant generation and require maker-checker verification; the demo also names operator profiles and expected un-net outcomes. A scenario labeled as released instead uses bilateral labels, and post-release component transitions are incomplete. See [[concepts/cashflow-netting-grouping-and-outcomes]] for the separate scheduled auto-netting grouping model.

## Canonical sections

- [NET-M-010](../../../records/candidates/settlement/KT-settlement-beneficiary-bic-netting.md#net-m-010)
- [NET-M-011](../../../records/candidates/settlement/KT-settlement-beneficiary-bic-netting.md#net-m-011)
- [NET-M-012](../../../records/candidates/settlement/KT-settlement-beneficiary-bic-netting.md#net-m-012)
- [NET-M-013](../../../records/candidates/settlement/KT-settlement-beneficiary-bic-netting.md#net-m-013)
- [NET-M-015](../../../records/candidates/settlement/KT-settlement-beneficiary-bic-netting.md#net-m-015)
- [NET-M-019](../../../records/candidates/settlement/KT-settlement-beneficiary-bic-netting.md#net-m-019)


## Related candidate topics

- [[summaries/KT-settlement-auto-netting-static-controls]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
