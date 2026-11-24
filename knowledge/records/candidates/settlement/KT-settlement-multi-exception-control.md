---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-multi-exception-control",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-a26afbd9a37b90d12dff7a61",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Multi Exceptions/Bulk Process for Multi Exceptions/Bulk UI Technical Design/page.md",
      "revision": "sha256:66949e5364b7a5d318048d173c781959a3d2bb8e69846f2f3db6411c33b6fdc3",
      "sha256": "66949e5364b7a5d318048d173c781959a3d2bb8e69846f2f3db6411c33b6fdc3",
      "snapshot": "knowledge/evidence/sources/sha256/66949e5364b7a5d318048d173c781959a3d2bb8e69846f2f3db6411c33b6fdc3.md"
    },
    {
      "id": "SRC-2b350296d9cb5373bebe070c",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Multi Exceptions/Bulk Process for Multi Exceptions/page.md",
      "revision": "sha256:eabf48366829f9a49a02eb27e50fa657a54f2c4efd7f6ee82d7bb7797e5f3cae",
      "sha256": "eabf48366829f9a49a02eb27e50fa657a54f2c4efd7f6ee82d7bb7797e5f3cae",
      "snapshot": "knowledge/evidence/sources/sha256/eabf48366829f9a49a02eb27e50fa657a54f2c4efd7f6ee82d7bb7797e5f3cae.md"
    },
    {
      "id": "SRC-4f6da7cd9496b141d2f05b59",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Multi Exceptions/Bulk Processing for Multi Exception Demo/page.md",
      "revision": "sha256:0edc669194eedf92031133132cf650280d6a45c99515277865ef0b21c1c4a9f7",
      "sha256": "0edc669194eedf92031133132cf650280d6a45c99515277865ef0b21c1c4a9f7",
      "snapshot": "knowledge/evidence/sources/sha256/0edc669194eedf92031133132cf650280d6a45c99515277865ef0b21c1c4a9f7.md"
    },
    {
      "id": "SRC-b81af71ae7ead781a550cf9a",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Multi Exceptions/High Value Exception Scenario Analysis/page.md",
      "revision": "sha256:d8bed812dfafe635df24f63ca31c41132bd5b4580b1e577c01da91f923d3a581",
      "sha256": "d8bed812dfafe635df24f63ca31c41132bd5b4580b1e577c01da91f923d3a581",
      "snapshot": "knowledge/evidence/sources/sha256/d8bed812dfafe635df24f63ca31c41132bd5b4580b1e577c01da91f923d3a581.md"
    },
    {
      "id": "SRC-55689daf687bd05c944edf29",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Multi Exceptions/page.md",
      "revision": "sha256:2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2",
      "sha256": "2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2",
      "snapshot": "knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:42:43.134584+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Exception generation, maker/checker correction, high-value handling, and configurable bulk processing.",
  "summary": "Resolve supported exception sections independently and restrict bulk processing through eligibility and authorization checks.",
  "related": [
    "KT-settlement-profile-authorization-limits",
    "KT-settlement-cashflow-blotter-actions",
    "KT-settlement-trade-validation-and-confirmation",
    "KT-settlement-processing-controls"
  ],
  "open_questions": [
    "Which exception allowlist version and high-risk permission contracts govern bulk processing?",
    "Should mixed-key selections disable bulk actions or show an error after selection?",
    "How does a Maker-only exception trigger High Value when the headline rule requires checker action?",
    "Which Bad Business Day stage and accepted affirmation statuses are authoritative?"
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
# Multi-exception and bulk processing controls

## Scope

Exception generation, maker/checker correction, high-value handling, and configurable bulk processing.
These isolated proposals require canonical integration and authority review.

## Summary

Resolve supported exception sections independently and restrict bulk processing through eligibility and authorization checks.
These documents describe intended responsibilities and proposals. They do not establish current implementation or deployment.

## Documented knowledge

### WF-CF-045

Bulk Submit/Approve requires at least two cashflows, matching WAITING exception states, and common counterparty, booking entity, and payment date.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 1–20](../../../../knowledge/evidence/sources/sha256/66949e5364b7a5d318048d173c781959a3d2bb8e69846f2f3db6411c33b6fdc3.md#L1-L20)

Limit: No implementation, deployment, or business execution established.

### WF-CF-046

Bulk preview excludes self-submitted checker items, missing/ineligible exceptions, unauthorized high-risk exceptions, and cashflows exceeding checker authorization limits.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 22–30](../../../../knowledge/evidence/sources/sha256/66949e5364b7a5d318048d173c781959a3d2bb8e69846f2f3db6411c33b6fdc3.md#L22-L30)

Limit: No implementation, deployment, or business execution established.

### WF-CF-047

Bulk eligibility is configurable per NSTP rule; an ineligible exception excludes the cashflow, and bulk actions require common entity, counterparty, and value date.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 5–15](../../../../knowledge/evidence/sources/sha256/eabf48366829f9a49a02eb27e50fa657a54f2c4efd7f6ee82d7bb7797e5f3cae.md#L5-L15)

Limit: The source says disable bulk for mismatched fields, while UI design says error after click.

### WF-CF-048

Bulk previews show exceptions, eligible/ineligible cashflow details, and affirmation data before submission or approval.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 19–38](../../../../knowledge/evidence/sources/sha256/eabf48366829f9a49a02eb27e50fa657a54f2c4efd7f6ee82d7bb7797e5f3cae.md#L19-L38)

Limit: No implementation, deployment, or business execution established.

### WF-CF-049

Business-rule maker/approver profiles configure bulk eligibility; preview reevaluates latest rules, separates eligibility, supports partial selection, and limits affirmation entry to pending-affirmation cashflows.

Source status: demo design and expected cases, not executed results.
[Retained original, lines 8–14](../../../../knowledge/evidence/sources/sha256/0edc669194eedf92031133132cf650280d6a45c99515277865ef0b21c1c4a9f7.md#L8-L14)

Limit: No implementation, deployment, or business execution established.

### WF-CF-050

The demo's expected cases allow alerts after mixed-entity selection, show partial bulk success, refresh cashflow status, and leave remaining items eligible for single processing.

Source status: planned demo expectations; execution NOT_RUN.
[Retained original, lines 57–67](../../../../knowledge/evidence/sources/sha256/0edc669194eedf92031133132cf650280d6a45c99515277865ef0b21c1c4a9f7.md#L57-L67)

Limit: No retained execution establishes real-time results or partial-success behavior.

### WF-CF-051

The demo and bulk-design pages contain different exception-list names and scope; both make eligibility configurable.

Source status: historical/configurable exception examples.
[Retained original, lines 18–53](../../../../knowledge/evidence/sources/sha256/0edc669194eedf92031133132cf650280d6a45c99515277865ef0b21c1c4a9f7.md#L18-L53)

Limit: No effective allowlist version or production rule export is supplied.

### WF-CF-052

High Value should not block straight-through processing by itself; it persists while another exception requires manual checker action and clears when automatic resolution removes that need.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 1–7](../../../../knowledge/evidence/sources/sha256/d8bed812dfafe635df24f63ca31c41132bd5b4580b1e577c01da91f923d3a581.md#L1-L7) [Retained original, lines 17–23](../../../../knowledge/evidence/sources/sha256/d8bed812dfafe635df24f63ca31c41132bd5b4580b1e577c01da91f923d3a581.md#L17-L23)

Limit: No implementation, deployment, or business execution established.

### WF-CF-053

High Value generation examples include a Maker-only exception, although the headline rule requires another exception needing checker action.

Source status: conditional rule needing reconciliation.
[Retained original, lines 3–7](../../../../knowledge/evidence/sources/sha256/d8bed812dfafe635df24f63ca31c41132bd5b4580b1e577c01da91f923d3a581.md#L3-L7) [Retained original, lines 9–15](../../../../knowledge/evidence/sources/sha256/d8bed812dfafe635df24f63ca31c41132bd5b4580b1e577c01da91f923d3a581.md#L9-L15)

Limit: Generation-time Maker-only cases need interpretation alongside checker-action wording.

### WF-CF-054

Pending Affirmation is generated when neither parent-trade nor cashflow affirmation/confirmation satisfies the check; later matching trade confirmation can remove it.

Exceptions: Reversal, internal counterparty, and components sharing a confirmed trade ID do not trigger Pending Affirmation.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 3–7](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L3-L7)

Limit: The status table includes NONCONFIRMED among status examples and a TBD Stella cashflow locator; accepted statuses need owner confirmation.

### WF-CF-055

Maker affirmation input is mandatory only for Pending Affirmation; checker can approve or reject that information but cannot edit it.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 7–7](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L7-L7) [Retained original, lines 49–49](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L49-L49)

Limit: No implementation, deployment, or business execution established.

### WF-CF-056

Exception families include missing/multiple/mismatched SSI, Adhoc SSI, missing beneficiary BIC for MT202, GSAM/CORP classification, back value, netting, reversal/rebook, NSTP, and High Value.

Conditions: Back Value runs after SSI stamping/approval, skips Over Account, then compares value date and GMT release cutoff. High Value threshold is payment amount above USD 100 million after FX conversion.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 9–19](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L9-L19) [Retained original, lines 21–33](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L21-L33)

Limit: Bad Business Day appears in both maker/checker and checker-only sections; do not resolve the ownership from position alone.

### WF-CF-057

Multi-exception fix uses independent SSI and date input, backend revalidation, hard blocking on settlement-account/means mismatch, and comparison of maker/checker values.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 35–37](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L35-L37)

Limit: No implementation, deployment, or business execution established.

### WF-CF-058

Checker rejection reopens the rejected affirmation, date, or SSI exception while preserving resolved sections; Adhoc SSI retains prior maker input only for the same maker.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 38–41](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L38-L41)

Limit: No implementation, deployment, or business execution established.

### WF-CF-059

Exception-page editability follows exception state and maker/checker stage; NSTP/other sections depend on present exceptions, while comments and action buttons remain visible.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 43–54](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L43-L54)

Limit: No implementation, deployment, or business execution established.

### Additional exception predicates and correction limits

The source requires MT202 beneficiary validation when beneficiary BIC is blank.
GSAM classification queries SCI with counterparty FMID and checks `legalEntity.operationStatus1Value == REFER`; NSTP-reason use remains TODO.
Corporate classification queries SCI `fmAccount.fmType == CORP` using counterparty FMID.
Adhoc netting checks `Cashflow.Is_Adhoc_Net == true`.
Reversal and Rebook exceptions use their respective `Cashflow.Cashflow_Event_Reason` values.
NetOverAmend requires `Reversal_Rebook` and a nonnull netting ID.
Net Cashflow applies to a resultant of netting-client components held in Pending Netting.
Previously Netted checks `Status_Event_Type == Un-Net` and `Trade.Settlement_Method == Gross`, after Pending Netting/Auto Netting checks fail.
Settled as Gross applies to manual gross settlement from Pending Netting or Pending Another Leg.
The checker-only Bad Business Day rule uses RDM currency holidays with payment date and payment currency.
Re-Instate from FAILED returns through QUEUED and creates Replayed from Failed Status.
These exact predicates do not establish a current universal exception catalogue.
[Exception predicates](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L14-L33)

The backend repeats maker and checker validation.
A Nostro/Vostro settlement-account or settlement-means mismatch hard-blocks SSI submission.
Checker affirmation remains read-only; only the maker supplies mandatory Pending Affirmation information.
Rejecting affirmation reopens that section while SSI/date remain resolved.
A date mismatch preserves only Back Value after other sections close; rejected dates retain the maker's previous date for correction.
An SSI mismatch preserves the SSI exception after other sections close.
Adhoc SSI changes outside 70/72 create SSI Modified by Maker and require checker dual-blind input.
After rejection, prior adhoc input is available only to the same maker, not another maker.
[Independent correction paths](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L37-L41)

The layout keeps Vostro and Nostro sections on the left, with Nostro above affirmation.
Good stamping is read-only for maker and checker.
Missing/Multiple Vostro and mismatch forms are maker-editable in Pending Operator and checker-editable in Pending Verification.
Missing Nostro is read-only for both roles in Pending Verification.
The layout calls no-exception affirmation read-only and blank, while the narrative says its maker section is always available.
That distinction needs owner reconciliation before implementation.
Back Value appears only when generated; maker and checker edit it in their respective stages.
NSTP and other-exception sections appear only for present exceptions; comments and action buttons remain visible.
[Layout predicates](../../../../knowledge/evidence/sources/sha256/2040e99a03772af39435a80e861f4d3dc266d08e5b955cd38779a4b07ea2d2f2.md#L47-L54)

## Connections

Related proposed or existing records: `KT-settlement-profile-authorization-limits`, `KT-settlement-cashflow-blotter-actions`, `KT-settlement-trade-validation-and-confirmation`, `KT-settlement-processing-controls`.
The reconciliation file identifies integration overlaps.

## Evidence limits

Only the selected source views were read. Excluded original lines were not opened.
Linked diagrams, attachments, policies, configurations, and external destinations were not inspected.
Documented designs do not establish executed behavior or current rollout.
Source authority and current applicability remain unconfirmed.
No publication approval or business verification is recorded.

## Open questions

Owner: unknown.

- Which exception allowlist version and high-risk permission contracts govern bulk processing?
- Should mixed-key selections disable bulk actions or show an error after selection?
- How does a Maker-only exception trigger High Value when the headline rule requires checker action?
- Which Bad Business Day stage and accepted affirmation statuses are authoritative?
