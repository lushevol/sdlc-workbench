---
type: KnowledgeTopic
id: KT-settlement-payment-amount-adjustment
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2026 Changes/Cash Settlement -- Korea Migration/Increase Payment Amount
    within USD 1 Threshold/page.md
  revision: sha256:b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2
  sha256: b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:54:46.010049+08:00'
verified: []
scope: Historical selected-source design for settlement payment amount adjustment.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which rejection, unsplit, withdrawal, and repeated-adjustment state contract is
  approved?
- What exchange-rate source, valuation instant, precision, and UAT owner establish
  the strict USD1 limit?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement payment amount adjustment

## Scope

Historical selected-source design for settlement payment amount adjustment.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Adjustment scope and threshold

The proposed adjustment permits a change strictly below USD1 equivalent before downstream release.
Currencies beginning with X are excluded.
Eligible flows include gross, net resultants, aggregation resultants, and split parents.
Split resultants cannot be adjusted.

Adjusted cashflows cannot be netted.
Reverting the same cashflow to QUEUED preserves its adjustment.
Economic replacement cashflows do not inherit the old adjustment.

Sources: [original lines 3–12](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L3-L12), [original lines 16–18](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L16-L18), [original lines 20–49](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L20-L49).

### Maker-checker and amount responsibility

Only makers edit the adjusted amount.
Eligible states are READY/NA/NA or WAITING/Pending Operator/Pending Exception without Pending NDS Netting.
Submission requires checker approval or rejection and highlights the adjustment.
Backend validation covers currency, range, and decimal precision.

TweakAmount and unTweakAmount actions record changes and cancellation.
Payments and LMS use adjusted amounts, while accounting retains original amounts.

Sources: [original lines 51–60](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L51-L60), [original lines 62–94](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L62-L94), [original lines 110–166](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L110-L166).

### Split and withdrawal contradiction

The closed clarification permits adjustment only on split parents.
One test table nevertheless describes adjustment of a split resultant.
That test table has no recorded result.
Withdrawal examples require adjusted payment and LMS amounts with original accounting.

Repeated netting after reversal/rebooking must not inherit the prior resultant difference.

Sources: [original lines 20–49](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L20-L49), [original lines 110–166](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L110-L166), [original lines 220–229](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L220-L229).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which rejection, unsplit, withdrawal, and repeated-adjustment state contract is approved?
- What exchange-rate source, valuation instant, precision, and UAT owner establish the strict USD1 limit?
