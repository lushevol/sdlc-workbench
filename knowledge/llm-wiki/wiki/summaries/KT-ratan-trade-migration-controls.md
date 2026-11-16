---
type: Summary
description: "Summarizes proposed Murex and Stella migration payment controls, environment differences, and reconciliation gates."
doc_type: short
full_text: sources/KT-ratan-trade-migration-controls.md
---

> **Candidate/draft only:** Runbook wording, sample counts, and status cells do not establish completed migration or authorization.

# RATAN Trade Migration Payment Controls

The selected 2025–2026 runbooks aim to avoid duplicate payments, accounting, and LMS feeds while Murex and Stella cashflows overlap. The 2026 PROD approach proposes blocking in-scope Murex flows with NSTP, cancelling them after trade migration, and holding Stella payments until reconciliation passes. Rules are narrowed from portfolio to cancelled trade or original-trade IDs when the required identifiers arrive.

The DR/UAT procedure is different: it permits a controlled suppression rule for Murex withdrawals and can handle previously released or settled cashflows. PROD inputs and starting states differ, so the DR steps cannot be generalized to production.

The records identify NDS fixing FXD trades as a duplicate-payment risk because their identities differ from parent trades and they arise near value date. Reconciliation spans future-seven-day feeds, totals, mappings, auto-netting, and cancellation lists. Release of the Stella block depends on reconciliation review; retained runbook steps do not prove that gate passed.

## Canonical sections

- [Overlap and target principle](../../../records/candidates/operations/KT-ratan-trade-migration-controls.md#overlap-and-target-principle)
- [NDS fixing identity gap and environment boundary](../../../records/candidates/operations/KT-ratan-trade-migration-controls.md#nds-fixing-identity-gap-and-environment-boundary)
- [DR sequence](../../../records/candidates/operations/KT-ratan-trade-migration-controls.md#april-2026-dr-sequence)
- [PROD sequence](../../../records/candidates/operations/KT-ratan-trade-migration-controls.md#may-2026-prod-sequence)
- [Tranche 1 controlled-payment testing](../../../records/candidates/operations/KT-ratan-trade-migration-controls.md#tranche-1-controlled-payment-testing)


## Related candidate topics

- [[summaries/KT-ratan-dated-migration-runbooks]]
- [[summaries/KT-settlement-cn-workflow]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
