---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-hold-unhold",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-238d7bf2c6c8e31621194c12",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Hold UnHold/page.md",
      "revision": "sha256:a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50",
      "sha256": "a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50",
      "snapshot": "knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:57:14.969570+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Manual hold, separate-user unhold, USD authorization, event behavior, and eligible actions.",
  "summary": "Hold suspends automatic processing and unhold restores prior state under separate-user and profile-limit controls.",
  "related": [
    "KT-settlement-cashflow-blotter-actions",
    "KT-settlement-cashflow-lifecycle",
    "KT-settlement-profile-authorization-limits"
  ],
  "open_questions": [
    "Which Hold state scope supersedes the broader historical design?",
    "Does amendment retain HOLD or move the cashflow to QUEUED?",
    "Must UnSplit wait for unhold, and how do explicit post-HOLD actions relate to suspended processing?",
    "What happens when the cashflow amount equals the unhold profile limit?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Automated checks do not establish complete writing review.",
    "Authority, applicability, and human publication review remain pending."
  ]
}
---
# Cashflow hold and unhold

## Scope

Manual hold, separate-user unhold, USD authorization, event behavior, and eligible actions.
These isolated proposals require canonical integration and authority review.

## Summary

Hold suspends automatic processing and unhold restores prior state under separate-user and profile-limit controls.
These documents describe intended responsibilities and proposals. They do not establish current implementation or deployment.

## Documented knowledge

### WF-CF-025

Hold changes a cashflow to HOLD with Cashflow Hold/Pending Verification; unhold restores the previous state and sub-state.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 16–24](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L16-L24) [Retained original, lines 43–58](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L43-L58)

Limit: The broad pre-release eligibility wording conflicts with the narrower leading blotter action matrix.

### WF-CF-026

Both maker and checker can hold; only the stated checker/Ops profiles can unhold, and the holding user cannot unhold the same cashflow.

Conditions: Literal profiles BOC, BO, BOL, BOM; FMO_OPS_MKR cannot unhold.

Exceptions: The source note allows the checker who approves unhold to release cashflows and generate SWIFT.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 19–19](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L19-L19) [Retained original, lines 30–41](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L30-L41) [Retained original, lines 26–28](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L26-L28)

Limit: No mapping from these legacy labels to CES roles is established.

### WF-CF-027

Hold has no amount-limit check; unhold requires the cashflow amount below the user's USD profile limit. Both actions require comments and support bulk use.

Conditions: Below profile limit is the literal boundary; equality behavior requires clarification.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 19–24](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L19-L24) [Retained original, lines 171–180](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L171-L180)

Limit: No implementation, deployment, or business execution established.

### WF-CF-028

The hold design retains HOLD on an amendment's new cashflow and processes withdrawal through the lifecycle; FAILED ends unhold eligibility.

Source status: documented design; unconfirmed current authority.
Source date scope: Case 5 says to do in 2024..
[Retained original, lines 93–104](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L93-L104) [Retained original, lines 124–141](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L124-L141)

Limit: The China 7pm EOD note is local source context, not a universal cutoff.

### WF-CF-029

The hold design permits Adhoc SSI, netting, un-net, suppression, and unhold on HOLD, while separately saying hold stops processing and bars un-split until removed.

Source status: documented design with internal tension.
[Retained original, lines 20–24](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L20-L24) [Retained original, lines 62–71](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L62-L71) [Retained original, lines 115–122](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L115-L122)

Limit: Post-HOLD actions may begin a new lifecycle; exact precedence and current applicability are unconfirmed.

### Processing suspension and version scenarios

Hold stops automatic materialization, exception checking and SSI stamping under this source's general rule.
The separate allowed-action table still permits explicit Adhoc SSI, net, un-net, suppression and unhold.
That table maps Adhoc SSI to WAITING and net/un-net to a new lifecycle.
Its former requirement to unhold before un-net is struck through; un-split remains separately blocked until unhold.
The old source's Hold eligibility excludes RELEASED, NET and SPLIT, while the current leading action matrix is narrower.
Do not expand current action eligibility from this historical wording.
[Hold constraints](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L16-L24)
[Explicit actions](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L62-L71)

The event example cancels the old amendment withdrawal and puts the newly referenced cashflow on HOLD.
A direct withdrawal of a held New flow makes the prior New inactive and cancels the withdrawal version.
Bulk cases preserve separate-user unhold and each cashflow's prior status/substates.
The over-limit example displays Unhold but prevents proceeding after amount validation.
It does not imply that hiding the action is the only authorization control.
The source header names owners but provides no retained publication approval in this review.
[Amendment and withdrawal examples](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L124-L141)
[Bulk and authorization examples](../../../../knowledge/evidence/sources/sha256/a219f2f5c37a5a4f79a4edc8acab7565b686c1d8d0fda207182f6049ad143f50.md#L143-L180)

## Connections

Related proposed or existing records: `KT-settlement-cashflow-blotter-actions`, `KT-settlement-cashflow-lifecycle`, `KT-settlement-profile-authorization-limits`.
The reconciliation file identifies integration overlaps.

## Evidence limits

Only the selected source views were read. Excluded original lines were not opened.
Linked diagrams, attachments, policies, configurations, and external destinations were not inspected.
Documented designs do not establish executed behavior or current rollout.
Source authority and current applicability remain unconfirmed.
No publication approval or business verification is recorded.

## Open questions

Owner: unknown.

- Which Hold state scope supersedes the broader historical design?
- Does amendment retain HOLD or move the cashflow to QUEUED?
- Must UnSplit wait for unhold, and how do explicit post-HOLD actions relate to suspended processing?
- What happens when the cashflow amount equals the unhold profile limit?
