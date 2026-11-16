---
type: Summary
description: "Summarizes candidate trade and cashflow SSI selection, notification, correction, and interface proposals."
doc_type: short
full_text: sources/KT-settlement-ssi-stamping-and-selection.md
---

# Trade and cashflow SSI stamping and selection

> **Source status:** Candidate/draft. The retained designs do not establish current authority, implementation, or rollout.

The candidate separates trade lookup, cashflow stamping, notification, and user correction. A scoped proposal adds branch-first Vostro selection for listed regions while preserving existing matching for other scopes. Notification eligibility depends on exception state and instruction changes. These predicates are source-specific and do not create a universal rule. [Scoped Vostro selection change](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#scoped-vostro-selection-change) [Notification eligibility](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#notification-eligibility)

The central-stamping proposal and product-template agreement differ on trade-to-cashflow inheritance and CDUPS publication. Trade response tables also disagree on which party receives incomplete sell-side results. Egypt's HTTP interface is a separate design. Preserve each contract rather than selecting a winner. [Central stamping proposal](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#central-stamping-proposal) [Trade and cashflow separation](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#trade-and-cashflow-separation) [Trade response conflicts](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#trade-response-conflicts)

Maker/checker correction and effective-date proposals retain blank values, identity-sensitive prior inputs, and start/end-date filtering. Editability, timezone, both-bound behavior, deletion, refresh, and notification coverage remain unresolved. The listed product/event set is test scope only; no execution result is supplied. [Correction identity and layout](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#correction-identity-and-layout) [Effective-date proposal](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#effective-date-proposal)

See the related cashflow interfaces in [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]] and proposed [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]].
