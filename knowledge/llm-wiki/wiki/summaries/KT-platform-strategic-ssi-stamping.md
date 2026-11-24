---
type: Summary
description: "Summarizes candidate strategic SSI stamping, result identity, cashflow reuse, concurrency, and Razor exchange proposals."
doc_type: short
full_text: sources/KT-platform-strategic-ssi-stamping.md
---

> **Candidate/draft only:** The selected designs do not establish current stamping authority or rollout. Owner is unknown; `verified` is empty.

# Platform strategic SSI stamping

The strategic proposal requests one product-agnostic SSI API and a RATAN logical model extended from Uber. It aims to reuse trade stamping results for cashflows and exchange standardized data with CDUPS. One alternative stores trade results by `tradeId` and major version; another questions that identity and would retain every request. The document limits refresh to the latest major version and leaves repeated-request identity and persistence unresolved.

Cashflow alternatives place stamping in Group service or orchestration. Both rely on selected attributes, require exception handling when a reusable result is absent, and call for concurrency protection. The proposal uses uniqueness and retry to reuse a saved result, and sequentializes SSI notifications. These are recovery designs, not verified guarantees.

The resulting SSI information would be converted to SCBML for Razor. Refresh timing, affected-trade coverage, event ordering, and exception handling remain unfinished. The related [[summaries/OPS-A-KT-SSI-AND-NOSTRO]] records regional requests; [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]] covers the broader SSI+ interface. This source does not supersede either candidate.

## Canonical sections

- [Unified strategic stamping objective](../../../records/candidates/settlement/KT-platform-strategic-ssi-stamping.md#unified-strategic-stamping-objective)
- [Version identity remains contradictory](../../../records/candidates/settlement/KT-platform-strategic-ssi-stamping.md#version-identity-remains-contradictory)
- [Cashflow stamping alternatives](../../../records/candidates/settlement/KT-platform-strategic-ssi-stamping.md#cashflow-stamping-alternatives)
- [Proposed concurrency and recovery](../../../records/candidates/settlement/KT-platform-strategic-ssi-stamping.md#proposed-concurrency-and-recovery)

Focused synthesis proposal: [[concepts/ssi-instruction-selection-and-stamping]].
