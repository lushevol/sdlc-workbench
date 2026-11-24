---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-failed-cashflow-recovery",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-fca998817cc9a1928c02160d",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Failed Process/Failed Cashflow Accounting/page.md",
      "revision": "sha256:7db43f248bbf098cc95cf41a4f9bfa38086bbe3d77c8ba56236d65ff7e8e24df",
      "sha256": "7db43f248bbf098cc95cf41a4f9bfa38086bbe3d77c8ba56236d65ff7e8e24df",
      "snapshot": "knowledge/evidence/sources/sha256/7db43f248bbf098cc95cf41a4f9bfa38086bbe3d77c8ba56236d65ff7e8e24df.md"
    },
    {
      "id": "SRC-4366f36bd55d711740b4d7ca",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Failed Process/Failed Re-Process - New Swift Value Date/page.md",
      "revision": "sha256:b013e9d4c20672a279346794e7e980b44eb70e9f6d08473f6f5ca1ca44b143c1",
      "sha256": "b013e9d4c20672a279346794e7e980b44eb70e9f6d08473f6f5ca1ca44b143c1",
      "snapshot": "knowledge/evidence/sources/sha256/b013e9d4c20672a279346794e7e980b44eb70e9f6d08473f6f5ca1ca44b143c1.md"
    },
    {
      "id": "SRC-f4dece4abcf27fac09ec3139",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Failed Process/Scheduled Failed Job Manual Fail/page.md",
      "revision": "sha256:a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef",
      "sha256": "a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef",
      "snapshot": "knowledge/evidence/sources/sha256/a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef.md"
    },
    {
      "id": "SRC-f3bfe2498e83c6da8a07ebe9",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Failed Process/page.md",
      "revision": "sha256:938aa614ba38fae4058931aba85290ad064b442d60e54378f2edb69d075dd6ca",
      "sha256": "938aa614ba38fae4058931aba85290ad064b442d60e54378f2edb69d075dd6ca",
      "snapshot": "knowledge/evidence/sources/sha256/938aa614ba38fae4058931aba85290ad064b442d60e54378f2edb69d075dd6ca.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:54:24.346253+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Failure scheduling, manual failure, reinstatement, SWIFT value date, and historical Razor accounting.",
  "summary": "Reinstate failed cashflows through exception checking and independent maker/checker payment-date selection.",
  "related": [
    "KT-settlement-cashflow-lifecycle",
    "KT-settlement-accounting",
    "KT-settlement-multi-exception-control"
  ],
  "open_questions": [
    "Does manual fail change state immediately or require checker approval first?",
    "Which calendar and cutoff govern each entity and currency?",
    "Does reinstatement offer two or three explicit value-date choices?",
    "How does historical Razor failed accounting reconcile with newer RATAN accounting and reversal rules?"
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
# Failed cashflow recovery

## Scope

Failure scheduling, manual failure, reinstatement, SWIFT value date, and historical Razor accounting.
These isolated proposals require canonical integration and authority review.

## Summary

Reinstate failed cashflows through exception checking and independent maker/checker payment-date selection.
These documents describe intended responsibilities and proposals. They do not establish current implementation or deployment.

## Documented knowledge

### WF-CF-017

At value-date EOD, FAILED cashflows go to Razor for accounting while SWIFT generation is bypassed; later reinstatement generates SWIFT only unless an amendment or cancellation needs accounting reversal.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 1–4](../../../../knowledge/evidence/sources/sha256/7db43f248bbf098cc95cf41a4f9bfa38086bbe3d77c8ba56236d65ff7e8e24df.md#L1-L4)

Limit: No implementation, deployment, or business execution established.

### WF-CF-018

Reinstatement moves a FAILED cashflow to QUEUED, reruns netting-client and exception checks, and creates a Pending Operator Cashflow Re-Instate exception.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 3–10](../../../../knowledge/evidence/sources/sha256/b013e9d4c20672a279346794e7e980b44eb70e9f6d08473f6f5ca1ca44b143c1.md#L3-L10)

Limit: No implementation, deployment, or business execution established.

### WF-CF-019

Maker and checker independently select the SWIFT value date; mismatch warns the checker, who can reject and return the exception to the maker.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 12–17](../../../../knowledge/evidence/sources/sha256/b013e9d4c20672a279346794e7e980b44eb70e9f6d08473f6f5ca1ca44b143c1.md#L12-L17)

Limit: The parent Failed Process page also offers Current System Date as a third explicit option.

### WF-CF-020

CN Day 1 proposes a daily failed job including weekends and holidays before Razor accounting EOD; the exact time remains TBC.

Conditions: Current-system-date value date and listed eligible cashflow states.

Source status: CN Day 1 requirement plus unconfirmed long-term strategy.
[Retained original, lines 1–9](../../../../knowledge/evidence/sources/sha256/a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef.md#L1-L9)

Limit: 10:00 GMT is a sample static-data row, not an established universal cutoff.

### WF-CF-021

The scheduled/manual-fail design includes PROJECTED, QUEUED, WAITING, READY, and ONHOLD and excludes listed terminal or settled states; manual action immediately changes to FAILED.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 4–4](../../../../knowledge/evidence/sources/sha256/a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef.md#L4-L4) [Retained original, lines 11–15](../../../../knowledge/evidence/sources/sha256/a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef.md#L11-L15)

Limit: Parent Failed Process requires maker-checker, while this manual section does not describe verification.

### WF-CF-022

FAILED highlights cashflows unpaid by cutoff, limits normal actions to Re-Instate, and permits a new Stella cashflow event to overwrite the failed version.

Conditions: Back-value cashflows wait for the scheduled job instead of failing immediately.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 3–8](../../../../knowledge/evidence/sources/sha256/938aa614ba38fae4058931aba85290ad064b442d60e54378f2edb69d075dd6ca.md#L3-L8)

Limit: No implementation, deployment, or business execution established.

### WF-CF-023

The parent failed-flow design requires maker-checker for manual fail and groups reinstatement with Back Value Date to set the SWIFT value date.

Conditions: Current System Date follows the currency calendar and may be a future working day.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 6–10](../../../../knowledge/evidence/sources/sha256/938aa614ba38fae4058931aba85290ad064b442d60e54378f2edb69d075dd6ca.md#L6-L10)

Limit: The child reinstatement page lists two date choices, and the child manual-fail page says immediate FAILED.

### Exact failed-state and date boundaries

The scheduled and manual lists allow PROJECTED, QUEUED, WAITING, READY and ONHOLD.
They exclude CANCELLED, NETTED, SPLIT, DEAD, SUPPRESSED, PAYMENT SUPPRESSED, RELEASED, SETTLED and NOSTRO MATCHED.
Scheduled scope requires payment date equal to current system date.
CN Day1 skips the proposed per-currency failed-cutoff check; its daily job includes weekends and holidays.
The long-term proposal uses currency-specific failure times while accounting aligns with Aspire's common trade-accounting time.
The sample cutoff row does not establish one approved global schedule.
[Failed scope](../../../../knowledge/evidence/sources/sha256/a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef.md#L3-L9)
[Manual scope](../../../../knowledge/evidence/sources/sha256/a9494fd41fee6b447805a8a01498ac3d4de4cdd74e1118f23d1eade9501ba1ef.md#L11-L15)

The parent flow offers Current System Date, current cashflow value date, or a manually selected date.
Its Current System Date follows currency working-day rules, including a future business day after a closed weekend.
The child date-selection page lists only current cashflow value date and manual selection.
It warns on maker/checker disagreement and permits checker rejection; no silent date override is authorized.
The parent groups reinstatement and Back Value because both change Swift Value Date.
[Parent date semantics](../../../../knowledge/evidence/sources/sha256/938aa614ba38fae4058931aba85290ad064b442d60e54378f2edb69d075dd6ca.md#L6-L10)

## Connections

Related proposed or existing records: `KT-settlement-cashflow-lifecycle`, `KT-settlement-accounting`, `KT-settlement-multi-exception-control`.
The reconciliation file identifies integration overlaps.

## Evidence limits

Only the selected source views were read. Excluded original lines were not opened.
Linked diagrams, attachments, policies, configurations, and external destinations were not inspected.
Documented designs do not establish executed behavior or current rollout.
Source authority and current applicability remain unconfirmed.
No publication approval or business verification is recorded.

## Open questions

Owner: unknown.

- Does manual fail change state immediately or require checker approval first?
- Which calendar and cutoff govern each entity and currency?
- Does reinstatement offer two or three explicit value-date choices?
- How does historical Razor failed accounting reconcile with newer RATAN accounting and reversal rules?
