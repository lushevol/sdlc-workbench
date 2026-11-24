---
type: Summary
description: "Preserves candidate SSI receive predicates, adhoc exception sequence, maker-checker fields, and selected-ID behavior."
doc_type: short
full_text: sources/KT-day2-ssi-validation-and-selection.md
---

> **Candidate/draft only:** These receive and selection rules are source-specific. Owner is unknown; `verified` is empty.

# SSI receive validation and selection

The selected requirement makes Vostro mandatory for receive cashflows in XAU, XAG, XPD, and XPT. It retains pay-side validation for manual SSI. Receive precious-metal and Over-Account cases require Vostro fields and matching means/account; other receive flows have separate null-SSI handling. A struck soft-warning option is not retained as target behavior.

The adhoc flow generates PRE_ADHOC_ERROR and ADHOC_SSI_EXCEPTION under different exception and approval conditions. The sources preserve identifier spelling. Maker requests set each 70/72 flag to Y only when an SSI ID exists and that field changed, and otherwise to N; checker approval carries maker values. Existing rows have null flags and no backfill is specified.

Selecting an unchanged SI retains its SSI ID. Changes limited to 70/72 preserve it when an SSI ID exists, while other edits clear it even if the user restores displayed values. Maker selection and checker re-entry remain distinct paths. The record establishes no current API behavior or execution.

## Canonical sections

- [L3-SSI-01 — Adhoc exception sequence](../../../records/candidates/settlement/KT-day2-ssi-validation-and-selection.md#l3-ssi-01--adhoc-exception-sequence)
- [L3-SSI-02 — Receive-side conditional mandatory fields](../../../records/candidates/settlement/KT-day2-ssi-validation-and-selection.md#l3-ssi-02--receive-side-conditional-mandatory-fields)
- [L3-SSI-03 — 70/72 maker-checker transport](../../../records/candidates/settlement/KT-day2-ssi-validation-and-selection.md#l3-ssi-03--7072-maker-checker-transport)
- [L3-SSI-04 — Selection identity and display](../../../records/candidates/settlement/KT-day2-ssi-validation-and-selection.md#l3-ssi-04--selection-identity-and-display)

Related candidates: [[summaries/OPS-A-KT-SSI-AND-NOSTRO]] and [[summaries/KT-day2-nostro-centralization-and-rfi]]. Focused synthesis proposal: [[concepts/ssi-instruction-selection-and-stamping]].
