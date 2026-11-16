---
type: KnowledgeTopic
id: KT-settlement-hold-and-manual-fail
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Actions on Hold/page.md
  revision: sha256:db4311d646b64306498a8f3a8940f943add99716f4d6fd1d5a89a74688cf8490
  sha256: db4311d646b64306498a8f3a8940f943add99716f4d6fd1d5a89a74688cf8490
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Bulk Fail/Bulk Fail Technical Design/page.md
  revision: sha256:f400c5cf824f3c8c6e2f5870257be3c1e4df18e7d0f9e0b1290613ca5e222de3
  sha256: f400c5cf824f3c8c6e2f5870257be3c1e4df18e7d0f9e0b1290613ca5e222de3
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Bulk Fail/page.md
  revision: sha256:c49abde51a4c40333f0da0590dc5aecbdb7b247dec9924c7f18d74272e545f93
  sha256: c49abde51a4c40333f0da0590dc5aecbdb7b247dec9924c7f18d74272e545f93
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:41:33.044396+08:00'
verified: []
scope: Historical selected-source design for settlement hold and manual fail.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which action checks the cashflow amount limit when leaving HOLD?
- Which current roles, eligible states, and maker/checker controls govern manual fail
  and scheduled AutoFail?
- Which effective source and approval establish these Hold and manual-fail changes?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement hold and manual fail

## Scope

Historical selected-source design for settlement hold and manual fail.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Hold exit alternatives

Unhold returns the cashflow to its previous QUEUED, WAITING, or READY status.
Send to WAITING returns it to the main flow with a Reinstate exception.
The popup warns that Unhold can automatically release payment downstream.
Send to WAITING requires a comment and records Reinstate in history.

Sources: [original lines 5–24](../../../evidence/sources/sha256/db4311d646b64306498a8f3a8940f943add99716f4d6fd1d5a89a74688cf8490.md#L5-L24).

### Hold actor restrictions

The requested access profile matches the Hold action.
The user who held the cashflow cannot Unhold it.
That user may select Send to WAITING.
The source amount-limit wording remains ambiguous.

Sources: [original lines 12–16](../../../evidence/sources/sha256/db4311d646b64306498a8f3a8940f943add99716f4d6fd1d5a89a74688cf8490.md#L12-L16).

### Manual fail approval and scope

Single and bulk manual fail require maker/checker approval.
Maker and checker must differ, and both must provide comments.
The bulk selection limit is 1000 cashflows.
The requirement leaves Reinstate unchanged.

The documented profiles are FMO_OPS_BOL, FMO_OPS_BOC, FMO_OPS_BO, FMO_OPS_INV, FMO_OPS_MKR, FMO_OPS_BOS, and FMO_OPS_BOM.

Sources: [original lines 5–14](../../../evidence/sources/sha256/c49abde51a4c40333f0da0590dc5aecbdb7b247dec9924c7f18d74272e545f93.md#L5-L14).

### Manual fail eligibility and transitions

Manual Fail is available for QUEUED, WAITING, and READY cashflows.
For SWIFT_SUPPRESSED or CASHFLOW_SUPPRESSED cashflows, current date must exceed payment date.
Pending Manual Fail cashflows cannot enter the action again.
Submission sets WAITING, Pending Verification, and Pending Manual Fail.

Approval sets FAILED; rejection restores the previous state.

Sources: [original lines 10–13](../../../evidence/sources/sha256/c49abde51a4c40333f0da0590dc5aecbdb7b247dec9924c7f18d74272e545f93.md#L10-L13), [original lines 20–23](../../../evidence/sources/sha256/c49abde51a4c40333f0da0590dc5aecbdb7b247dec9924c7f18d74272e545f93.md#L20-L23).

### Manual and scheduled failure separation

The technical proposal distinguishes manual Fail from scheduled AutoFail.
Its listed manual transitions require verification before FAILED.
Its listed AutoFail transitions go directly to FAILED.
The manual matrix includes additional states beyond the UI eligibility requirement.

HOLD and ERROR manual rows are marked unavailable in the frontend.

Sources: [original lines 1–3](../../../evidence/sources/sha256/f400c5cf824f3c8c6e2f5870257be3c1e4df18e7d0f9e0b1290613ca5e222de3.md#L1-L3), [original lines 5–43](../../../evidence/sources/sha256/f400c5cf824f3c8c6e2f5870257be3c1e4df18e7d0f9e0b1290613ca5e222de3.md#L5-L43).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which action checks the cashflow amount limit when leaving HOLD?
- Which current roles, eligible states, and maker/checker controls govern manual fail and scheduled AutoFail?
- Which effective source and approval establish these Hold and manual-fail changes?
