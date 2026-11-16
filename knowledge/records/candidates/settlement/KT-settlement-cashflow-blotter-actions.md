---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-cashflow-blotter-actions",
  "version": 2,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-225cd456a2fdf0082646be39",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Cashflow Blotter/Cashflow Details page/page.md",
      "revision": "sha256:6506cc83233668a82c3a0f434b62c05afebea0fc2d8a894a1d87f94c4908c56f",
      "sha256": "6506cc83233668a82c3a0f434b62c05afebea0fc2d8a894a1d87f94c4908c56f",
      "snapshot": "knowledge/evidence/sources/sha256/6506cc83233668a82c3a0f434b62c05afebea0fc2d8a894a1d87f94c4908c56f.md"
    },
    {
      "id": "SRC-18abc811bcede946810d360c",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Cashflow Blotter/Manual Fix Exception/page.md",
      "revision": "sha256:a2a38fae12b69aee82162b4c8b127967068a1e76808a9e460bbbb487d8105163",
      "sha256": "a2a38fae12b69aee82162b4c8b127967068a1e76808a9e460bbbb487d8105163",
      "snapshot": "knowledge/evidence/sources/sha256/a2a38fae12b69aee82162b4c8b127967068a1e76808a9e460bbbb487d8105163.md"
    },
    {
      "id": "SRC-29e240338779d97eca0bed84",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Cashflow Blotter/User Actions on Cashflow Blotter/page.md",
      "revision": "sha256:55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891",
      "sha256": "55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891",
      "snapshot": "knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md"
    },
    {
      "id": "SRC-8c415aa2feea96926e710ade",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/KTLO Requirement/8870075-Update counterparty BIC display in  i  icon/page.md",
      "revision": "sha256:c0b9f5d663e215c84f1e93f0f986f67e21a7061536aba2158d12cb06ec8d9f7f",
      "sha256": "c0b9f5d663e215c84f1e93f0f986f67e21a7061536aba2158d12cb06ec8d9f7f",
      "snapshot": "knowledge/evidence/sources/sha256/c0b9f5d663e215c84f1e93f0f986f67e21a7061536aba2158d12cb06ec8d9f7f.md"
    },
    {
      "id": "SRC-4ba1bb15ff50fdf8b1fb21c1",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/KTLO Requirement/9244022-Cashflow filter enhancement/page.md",
      "revision": "sha256:aeda1a2acd5c431e60ff0a4bb417fbca43d95696289a216afb6f2615c41ec4bf",
      "sha256": "aeda1a2acd5c431e60ff0a4bb417fbca43d95696289a216afb6f2615c41ec4bf",
      "snapshot": "knowledge/evidence/sources/sha256/aeda1a2acd5c431e60ff0a4bb417fbca43d95696289a216afb6f2615c41ec4bf.md"
    },
    {
      "id": "SRC-a2c684542892f02020a9b1e7",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/KTLO Requirement/9244054-Bug - UTC   Local ccy toggle doesnt work/page.md",
      "revision": "sha256:007466fd0f882fde0f6c1a4b0cd36ea7841fdea267c710639168f207c1d14c11",
      "sha256": "007466fd0f882fde0f6c1a4b0cd36ea7841fdea267c710639168f207c1d14c11",
      "snapshot": "knowledge/evidence/sources/sha256/007466fd0f882fde0f6c1a4b0cd36ea7841fdea267c710639168f207c1d14c11.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T00:54:23.316359+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Documented FMRP and BCS action eligibility, detail panels, and selected UI change proposals.",
  "summary": "Action availability depends on cashflow state, exceptions, source scope, and settlement method.",
  "related": [
    "KT-settlement-cashflow-lifecycle",
    "KT-settlement-hold-unhold",
    "KT-settlement-multi-exception-control",
    "KT-settlement-profile-authorization-limits"
  ],
  "open_questions": [
    "Which entity, date, and governing layout version apply to the details view?",
    "Which FMRP and BCS action-matrix versions govern each entity and date, including Hold eligibility and Manual Settle statuses?",
    "What value should display in the SCBLGB2LXXX exception case, and which UI owner confirms the SCI field behavior?",
    "Which unused filters should be removed, and who supplies the authoritative list?",
    "Which DateTime fields and timezone conversion rules should the UTC/local toggle apply?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Semantic review is bound separately to final draft bytes.",
    "Source/hash/range/citation checks do not establish complete ASD writing review.",
    "No current applicability, approval, implementation, execution or rollout established."
  ]
}
---
> **PROPOSED candidate:** Historical and proposed statements retain their source limits. Human publication review is pending.

# Cashflow blotter actions and display

## Scope

Documented FMRP and BCS action eligibility, detail panels, and selected UI change proposals.
These isolated proposals require canonical integration and authority review.

## Summary

Action availability depends on cashflow state, exceptions, source scope, and settlement method.
These documents describe intended responsibilities and proposals. They do not establish current implementation or deployment.

## Documented knowledge

### WF-CF-001

The layout lists trade ID, version, state, booking entity, counterparty, portfolio, taxonomy, and CFI.
Cashflow fields include ID, netting ID, business version, event, affirmation, value date, currency, amount, and state.
Payer party reference `party1` displays Pay; every other value displays Receive under this design.
Confirmation Status and Payment Cutoff have blank logical-model mappings.
Sub-status, action history, and exceptions are separate panels.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 1–7](../../../../knowledge/evidence/sources/sha256/6506cc83233668a82c3a0f434b62c05afebea0fc2d8a894a1d87f94c4908c56f.md#L1-L7)

Limit: No implementation, deployment, or business execution established.

### WF-CF-002

The panel shows Multi Vostro, Missing Vostro, SI Mismatch, Validate Bene Info, and Missing Nostro exceptions.
It also shows affirmation, back-value, NSTP, high-risk NSTP, hard-blocker, other, and comment exception families.
Their condition is Pending Operator or Pending Verification.
Several family codes are blank; do not invent them.
INACTIVE Per SSI Adhoc represents good stamping and is not an exception-panel item.
Its Adhoc action makes both Nostro and Vostro forms editable and changes their titles.
Missing Nostro adds a Nostro Edit action; that action also makes the Vostro form editable.

Conditions: Exception status Pending Operator or Pending Verification for displayed exceptions.

Exceptions: INACTIVE Per SSI Adhoc is not an exception-panel item.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 7–21](../../../../knowledge/evidence/sources/sha256/a2a38fae12b69aee82162b4c8b127967068a1e76808a9e460bbbb487d8105163.md#L7-L21)

Limit: No implementation, deployment, or business execution established.

### WF-CF-003

FMRP action visibility depends on cashflow state, sub-state, exception type, settlement method, and additional cashflow attributes.

Conditions: Most mutation rows exclude Settlement_Method UTIL.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 3–49](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L3-L49)

Limit: Merged table rows and blank cells require preservation; historical rows differ.

### WF-CF-004

FMRP netting and splitting actions have distinct eligibility; split requires New, no existing netting/split ID, non-LOANIQ source, and non-UTIL settlement.

Conditions: Split requires state WAITING or READY.

Exceptions: Un-split excludes RELEASED and SETTLED. Un-net requires a netting ID and excludes NETTED and SPLIT.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 27–42](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L27-L42)

Limit: No implementation, deployment, or business execution established.

### WF-CF-005

Historical action notes require maker-checker approval for suppression, unsuppression, netting exceptions, and reinstatement; failed cashflows resume through QUEUED exception evaluation.

Source status: explicitly historical action notes.
[Retained original, lines 56–71](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L56-L71)

Limit: Historical hold/net eligibility differs from the leading action matrix.

### WF-CF-006

Manual Settle is offered for RELEASED cashflows with one of the listed failed or checking SWIFT statuses.

Conditions: The leading matrix lists AMH Error, Check in FMSGW, Check in FMSRE, FMSGW Deleted, FMSGW Error,
FMSRE Deleted, FMSRE Error, Manual Delete, SCPAY Error, Pending FMSGW Disp, and Pending FMSRE Disp.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 35–36](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L35-L36) [Retained original, lines 75–75](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L75-L75)

Limit: The explicitly historical narrative omits the two Pending Disp statuses in the leading matrix.

### WF-CF-007

BCS uses a separate action and permission matrix for reinstate, affirmation, net/un-net, Adhoc SSI, release, suppression, comment, and viewing.

Conditions: The source uses action-specific `RATAN_CASHFLOW_BLOTTER` permissions. No CES or role equivalence is inferred.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 79–107](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L79-L107)

Limit: BCS and FMRP matrices cannot be merged into one effective permission contract.

### WF-CF-008

FMRP Hold appears only for WAITING and READY in the leading matrix, while historical notes allow broader pre-release states.

Source status: conflicting leading-matrix and explicitly historical design statements.
[Retained original, lines 32–34](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L32-L34) [Retained original, lines 60–61](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L60-L61)

Limit: Do not select historical broad eligibility as current policy.

### Historical suppression and recovery distinctions

Historical SWIFT suppression means payment is not required; cashflow suppression also excludes settlement accounting.
Maker initiation waits for checker verification before entering the corresponding suppressed state.
Undo suppression requires maker/checker approval and returns to QUEUED after verification.
These notes prohibit unsuppression beyond value date and direct required payments to AMH/Oscar as stated.
Reinstatement from FAILED returns to QUEUED and runs netting-client and exception checks.
It creates a maker/checker Cashflow Re-Instate exception, including SWIFT value-date selection.
The historical Hold note permits broader states than the leading matrix.
It prohibits the same user from unholding their own hold and restores the pre-hold status.
These historical rules are not declared current policy.
[Historical action distinctions](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L58-L71)

### Leading-matrix limits

The FMRP matrix distinguishes STRATEGIC Regenerate Swift from non-STRATEGIC Resend To Razor in READY/Pending Ack.
It separates BIC, CCIL, and ordinary netting by counterparty, booking entity, method, state, and split eligibility.
Its CCIL counterparty exception is not a general permission to bypass backend validation.
Bulk submit and approve use distinct operator/verification substates; other same-substate selections can show a disabled action.
Settlement Method Update has FX product, source, method, and state branches that require the original matrix.
Blank or shifted cells in the source do not establish unrestricted action eligibility.
The BCS matrix has its own release, failed-release, suppression, SSI, viewing, and literal permission conditions.
Its affirmation row records the maker as checker; no general maker/checker waiver is inferred.
This summary does not replace the complete FMRP or BCS matrix.
[Leading FMRP matrix](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L3-L49) [Separate BCS matrix](../../../../knowledge/evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L79-L107)

### WF-CF-031

The BIC display change proposes using SCI addrLine where mediumUsage is MAIN, with an explicit SCBLGB2LXXX exception condition.

Source status: To-Be change proposal.
[Retained original, lines 1–1](../../../../knowledge/evidence/sources/sha256/c0b9f5d663e215c84f1e93f0f986f67e21a7061536aba2158d12cb06ec8d9f7f.md#L1-L1) [Retained original, lines 11–13](../../../../knowledge/evidence/sources/sha256/c0b9f5d663e215c84f1e93f0f986f67e21a7061536aba2158d12cb06ec8d9f7f.md#L11-L13)

Limit: The sentence is ambiguous about the fallback and exact exception evaluation; sample payload is excluded.

### WF-CF-032

The cashflow filter enhancement proposes alphabetic ordering of filters/views and removal of unused filters after PO supplies the list.

Source status: enhancement proposal, removal inventory TBC.
[Retained original, lines 1–5](../../../../knowledge/evidence/sources/sha256/aeda1a2acd5c431e60ff0a4bb417fbca43d95696289a216afb6f2615c41ec4bf.md#L1-L5) [Retained original, lines 9–9](../../../../knowledge/evidence/sources/sha256/aeda1a2acd5c431e60ff0a4bb417fbca43d95696289a216afb6f2615c41ec4bf.md#L9-L9)

Limit: No filter-removal inventory is available.

### WF-CF-033

The UTC/local toggle correction requests that DateTime fields change to the corresponding selected datetime representation.

Source status: reported defect and requested intended correction.
[Retained original, lines 1–3](../../../../knowledge/evidence/sources/sha256/007466fd0f882fde0f6c1a4b0cd36ea7841fdea267c710639168f207c1d14c11.md#L1-L3) [Retained original, lines 7–7](../../../../knowledge/evidence/sources/sha256/007466fd0f882fde0f6c1a4b0cd36ea7841fdea267c710639168f207c1d14c11.md#L7-L7)

Limit: No actual UI reproduction, timezone conversion rule, or field inventory was inspected.

## Connections

The [Group Blotter controls](../../../../knowledge/records/candidates/settlement/KT-settlement-group-blotter-controls.md) candidate covers a separate workflow.
The [CCIL netting](../../../../knowledge/records/candidates/settlement/KT-settlement-ccil-netting.md) candidate records an overlapping Pending Netting gate. This candidate does not resolve its state differences.

## Evidence limits

Only the selected source views were read. Excluded original lines were not opened.
Linked diagrams, attachments, policies, configurations, and external destinations were not inspected.
Documented designs do not establish executed behavior or current rollout.
Source authority and current applicability remain unconfirmed.
No publication approval or business verification is recorded.

## Open questions

Owner: unknown.

- Which entity, date, and governing layout version apply to the details view?
- Which FMRP and BCS action-matrix versions govern each entity and date, including Hold eligibility and Manual Settle statuses?
- What value should display in the SCBLGB2LXXX exception case, and which UI owner confirms the SCI field behavior?
- Which unused filters should be removed, and who supplies the authoritative list?
- Which DateTime fields and timezone conversion rules should the UTC/local toggle apply?
