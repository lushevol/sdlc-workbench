---
type: KnowledgeTopic
id: KT-day2-ssi-validation-and-selection
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-edb91b75928eaf139a06453e
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/SCB Receive Cashflow Stamping/Cashflow
    Auto Stamping/page.md
  revision: sha256:0f593f1806e06471abf660808994c4139afb11457efdf961e51cfda6fb778e5f
  sha256: 0f593f1806e06471abf660808994c4139afb11457efdf961e51cfda6fb778e5f
- id: SRC-55b8e256cf04e3cd5a54ac03
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/SCB Receive Cashflow Stamping/page.md
  revision: sha256:3f7ce630e826d523d4600c172295b7d35def8a7f94af92a0ac38b73c7cd7a4f3
  sha256: 3f7ce630e826d523d4600c172295b7d35def8a7f94af92a0ac38b73c7cd7a4f3
- id: SRC-f597d10b177c2aa4274a076a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/SSI selection not treat as adhoc SSI/Adhoc
    SSI API/page.md
  revision: sha256:4ce1b0599364e590d4967771997343dc36fc8166d9248220507d08c9df5f00a2
  sha256: 4ce1b0599364e590d4967771997343dc36fc8166d9248220507d08c9df5f00a2
- id: SRC-81eef541682860fddb6f0a01
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/SSI selection not treat as adhoc SSI/page.md
  revision: sha256:cc76a535a53714bd911822576dd1152d2560395104805f0527a7271b39e2d9b0
  sha256: cc76a535a53714bd911822576dd1152d2560395104805f0527a7271b39e2d9b0
classification: settlement
scope: SSI receive validation and selected instruction identity
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- OPS-A-KT-SSI-AND-NOSTRO
- KT-day2-nostro-centralization-and-rfi
open_questions:
- 'KDQ-7f8639e07a: Which accepted exception state machine and API version govern SSI
  auto-stamping?'
- 'KDQ-a189ea2e60: Which null-SSI and 70/72 display/persistence semantics govern?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:55:24.889307+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# SSI receive validation and selected instruction identity

## Scope

SSI receive validation and selected instruction identity.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### L3-SSI-01 — Adhoc exception sequence

Generate PRE_ADHOC_ERROR after checker approval closes Vostro/Nostro exceptions, after auto-stamping with no such exceptions, or after auto-stamping exceptions when adleToSendPerSSIAdhocException is true. Close PRE_ADHOC_ERROR before ADHOC_SSI_EXCEPTION generation and regenerate it after that exception closes. Generate ADHOC_SSI_EXCEPTION on adhoc submit or reject. Preserve the source identifier spelling.

[Original evidence](../../../evidence/sources/sha256/0f593f1806e06471abf660808994c4139afb11457efdf961e51cfda6fb778e5f.md#L3-L13).

### L3-SSI-02 — Receive-side conditional mandatory fields

The target makes Vostro mandatory for receive cashflows in XAU, XAG, XPD, and XPT. Manual SSI retains pay-side validation. Receive precious-metal and Over-Account flows require mandatory Vostro fields and Vostro/Nostro means/account matching. Other receive flows bypass Vostro mandatory validation. When their Vostro SSI Type is null, align its settlement means and account to Nostro. The struck soft-warning proposal is not target behavior.

[Original evidence](../../../evidence/sources/sha256/3f7ce630e826d523d4600c172295b7d35def8a7f94af92a0ac38b73c7cd7a4f3.md#L1-L3). [Original evidence](../../../evidence/sources/sha256/3f7ce630e826d523d4600c172295b7d35def8a7f94af92a0ac38b73c7cd7a4f3.md#L11-L14).

### L3-SSI-03 — 70/72 maker-checker transport

The maker endpoint is /v3/adhoc/ssis/makerInput/{cashflowId}. fitVostro manualTag70/manualTag72 are Y only when an SSI ID exists and the corresponding field changed; otherwise N. Checker approval /v2/stamping/exception/{exceptionId}/approve carries the maker values. Reject retains its existing request body. During an Adhoc SSI exception, read flags from stashed Maker_Request_Body. After approval, read them from Settlement_Instruction. Existing cashflows have null flags; the source specifies no backfill.

[Original evidence](../../../evidence/sources/sha256/4ce1b0599364e590d4967771997343dc36fc8166d9248220507d08c9df5f00a2.md#L1-L12).

### L3-SSI-04 — Selection identity and display

Selecting available SI without edits preserves the selected SSI ID. Edits limited to 70/72 preserve it and highlight changes only when an ID exists. Other edits clear it; editing then manually restoring values still clears it. Maker selection and checker manual entry remain different paths, even with equal displayed values, and produce a mismatch. The checker cannot see the selected maker SSI ID. Approval in edit mode without changes preserves the ID. The 70/72 UI describes an empty SSI ID display with the stored ID in Reference ID; do not silently equate display fields and persisted identity.

[Original evidence](../../../evidence/sources/sha256/cc76a535a53714bd911822576dd1152d2560395104805f0527a7271b39e2d9b0.md#L3-L12). [Original evidence](../../../evidence/sources/sha256/cc76a535a53714bd911822576dd1152d2560395104805f0527a7271b39e2d9b0.md#L18-L36).

## Connections

Related canonical IDs: `OPS-A-KT-SSI-AND-NOSTRO`, `KT-day2-nostro-centralization-and-rfi`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
