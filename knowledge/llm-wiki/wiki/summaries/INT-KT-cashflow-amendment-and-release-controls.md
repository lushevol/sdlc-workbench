---
type: Summary
description: "Summarizes candidate amendment classifications, READY action boundaries, and payment release gates."
doc_type: short
full_text: sources/INT-KT-cashflow-amendment-and-release-controls.md
---

> **Candidate/draft only:** The source revisions do not establish current authority, effective scope, or deployed controls. Owner is unknown; `verified` is empty.

# Cashflow amendment and release control intent

The January design separates workflow publication at `READY+NA+NA` from SWIFT generation at `READY+NA+PendingAck`. It proposes last-mile amount reconciliation, duplicate checks, and distinct workflow, message, and SWIFT identities. The detailed matrix assigns different transitions to READY substatuses; it also identifies conflicts among concurrent jobs and manual actions. The timing examples are proposals, not verified schedules.

The amendment examples distinguish economic changes, key-field changes, manual touch, and released state. They do not settle whether key-field checks precede manual-touch/release checks. The October notes retain a READY-only downstream gate and a near-cutoff net/split restriction. Their allowed actions and exact cutoff boundary need reconciliation with the January appendix. Referenced approvals, code, tests, and screenshots were not inspected, so these descriptions establish no implementation or execution.

## Canonical sections

- [CTRL-01 — Proposed layered release validation](../../../records/candidates/settlement/INT-KT-cashflow-amendment-and-release-controls.md#ctrl-01--proposed-layered-release-validation)
- [CTRL-02 — Detailed READY-state transitions and concurrency scope](../../../records/candidates/settlement/INT-KT-cashflow-amendment-and-release-controls.md#ctrl-02--detailed-ready-state-transitions-and-concurrency-scope)
- [CTRL-03 — Economic and key-field amendment classification](../../../records/candidates/settlement/INT-KT-cashflow-amendment-and-release-controls.md#ctrl-03--economic-and-key-field-amendment-classification)
- [CTRL-04 — October release-control intent](../../../records/candidates/settlement/INT-KT-cashflow-amendment-and-release-controls.md#ctrl-04--october-release-control-intent)

Related candidates: [[summaries/KT-settlement-processing-and-exception-controls]] and [[summaries/KT-settlement-amendment-reversal-rebook-exceptions]].

Focused synthesis proposal: [[concepts/cashflow-amendment-classification-and-release]].
