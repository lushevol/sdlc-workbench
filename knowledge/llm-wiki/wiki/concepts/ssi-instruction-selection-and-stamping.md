---
type: Concept
description: "How candidate SSI data is owned, validated, selected, and stamped across settlement flows."
sources:
  - summaries/KT-settlement-ssi-form-validation.md
  - summaries/KT-platform-strategic-ssi-stamping.md
  - summaries/KT-day2-ssi-validation-and-selection.md
  - summaries/KT-ratan-nostro-golden-source-proposal.md
  - summaries/KT-day2-nostro-centralization-and-rfi.md
  - summaries/OPS-A-KT-SSI-AND-NOSTRO.md
  - summaries/KT-settlement-ssi-stamping-and-selection.md
  - summaries/KT-static-data-cache-p3.md
  - summaries/INT-KT-ratan-cashflow-settlement-interfaces.md
---

> **Candidate synthesis:** Supporting records remain candidate/draft with owner unknown and empty verified lists. This page selects no current authority.

# SSI instruction selection and stamping

The selected records describe distinct layers of settlement-instruction work. Static-data proposals address Nostro and Vostro ownership, SSI+ or NAMS-to-RDM distribution, caches, and effective dates. Selection and validation records use region-, product-, flow-, and exception-specific predicates. Form requirements add message-dependent fields and formats. Stamping proposals cover trade-result identity, cashflow reuse, concurrent requests, SSI refresh, and downstream Razor conversion.

These layers are related but do not define one universal path. A selected SSI ID can behave differently from manual input. For automatic or selected SI with an existing SSI ID, changes limited to fields70/72 retain that ID. Other edits clear it, including manual restoration of displayed values. Receive-side Vostro requirements differ from pay-side handling and from the strategic trade-stamping proposal. Account sourcing and RFI lookup proposals also leave ownership, no-match behavior, and migration unsettled.

The strategic proposal reuses trade results for cashflows. A separate product-template agreement explicitly rejects cashflow inheritance from trade stamping. Their precedence remains unresolved. [Strategic reuse](../../../records/candidates/settlement/KT-platform-strategic-ssi-stamping.md#cashflow-stamping-alternatives) [Separation agreement](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#trade-and-cashflow-separation)

Regional selection also differs. The scoped change retains existing matching for CN, SG, IN, MY, AG, EG, SA, NP, and LOANIQ. It proposes branch-first selection for UK, HK, TW, and TAIPEI. New entities and products require separate assessment. [Scoped selection](../../../records/candidates/settlement/KT-settlement-ssi-stamping-and-selection.md#scoped-vostro-selection-change)

Current approved source ownership, effective rules, version identity, precedence, refresh, and correction behavior remain unresolved. The source summaries below retain the separate conditions and conflicts; their relationship supplies no implementation or rollout evidence.

## Source records

- [[summaries/KT-ratan-nostro-golden-source-proposal]] and [[summaries/KT-day2-nostro-centralization-and-rfi]] describe distinct source and lookup proposals.
- [[summaries/KT-settlement-ssi-form-validation]] and [[summaries/KT-day2-ssi-validation-and-selection]] retain form, receive-flow, and correction predicates.
- [[summaries/KT-platform-strategic-ssi-stamping]] and [[summaries/KT-settlement-ssi-stamping-and-selection]] describe strategic and regional stamping proposals.
- [[summaries/OPS-A-KT-SSI-AND-NOSTRO]] preserves dated operations requests.
- [[summaries/KT-static-data-cache-p3]] and [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]] provide cache and integration context.
