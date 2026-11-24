---
type: Summary
description: "Separates candidate Hold exit, manual-fail approval, eligibility, and scheduled AutoFail transitions."
doc_type: short
full_text: sources/KT-settlement-hold-and-manual-fail.md
---

> **Candidate/draft only:** The selected matrices disagree on state coverage and do not establish current roles or authority. Owner is unknown; `verified` is empty.

# Settlement hold and manual fail

The Hold requirement offers two exits. Unhold returns the previous QUEUED, WAITING, or READY state and may release payment downstream. Send to WAITING records Reinstate and requires a comment. The user who set Hold cannot Unhold, but may choose Send to WAITING. The source leaves the amount-limit check unclear.

Manual and bulk Fail require distinct maker and checker users, comments, and up to 1,000 selected cashflows. The requirement allows QUEUED, WAITING, and READY, with date conditions for suppressed cashflows. Submission enters WAITING/Pending Verification/Pending Manual Fail; approval sets FAILED and rejection restores the previous state.

The technical matrix includes extra states and separates verified manual Fail from scheduled AutoFail, which directly sets FAILED. HOLD and ERROR manual rows are unavailable in the frontend. Do not merge these matrices or infer current authorization from the listed profiles.

## Canonical sections

- [Hold exit alternatives](../../../records/candidates/settlement/KT-settlement-hold-and-manual-fail.md#hold-exit-alternatives)
- [Manual fail approval and scope](../../../records/candidates/settlement/KT-settlement-hold-and-manual-fail.md#manual-fail-approval-and-scope)
- [Manual fail eligibility and transitions](../../../records/candidates/settlement/KT-settlement-hold-and-manual-fail.md#manual-fail-eligibility-and-transitions)
- [Manual and scheduled failure separation](../../../records/candidates/settlement/KT-settlement-hold-and-manual-fail.md#manual-and-scheduled-failure-separation)

Related candidate context: [[summaries/KT-settlement-processing-and-exception-controls]] and [[summaries/KT-settlement-failed-cashflow-recovery]].
