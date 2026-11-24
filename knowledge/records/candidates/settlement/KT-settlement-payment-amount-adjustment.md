---
type: KnowledgeTopic
id: KT-settlement-payment-amount-adjustment
version: 3
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2026 Changes/Cash Settlement -- Korea Migration/Increase Payment Amount
    within USD 1 Threshold/page.md
  revision: sha256:b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2
  sha256: b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Manual Rounding/page.md
  revision: sha256:eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13
  sha256: eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13
generated:
  by: agent:sol_portal_review
  at: '2026-11-16T02:30:44.320706+00:00'
verified: []
scope: Historical Day 2 manual rounding and Korea migration payment amount adjustment,
  preserving distinct accounting and state rules.
classification: settlement
summary: Both proposals use a strict change below USD 1 equivalent and maker/checker
  control. Accounting rules and applicability remain unresolved.
related:
- KT-settlement-auto-netting
- KT-settlement-cashflow-identity-and-stella-write-back
open_questions:
- Which rejection, unsplit, withdrawal, and repeated-adjustment state contract is
  approved?
- What exchange-rate source, valuation instant, precision, and UAT owner establish
  the strict USD1 limit?
- Which adjustment design applies to each payment flow, entity, effective date, and
  cashflow state?
- Which accounting amount applies to each adjustment scope, and how does TLM reconcile
  the difference?
- Which exchange rate and timestamp determine the USD equivalent?
- Which downstream contracts and rebook linkage cover adjusted payments?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
previous_version: 2
previous_content_sha256: 18985134beba4da61175aecdc9ecdcdef937dcace327564d20d9eaf825da9c89
---
<a id="payment-amount-adjustment"></a>

# Settlement payment amount adjustment

## Scope

Historical selected-source design for settlement payment amount adjustment.
The retained Day 2 and Korea variants have different accounting rules and unresolved applicability.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.
Both variants require maker/checker control and a change strictly below USD 1 equivalent.
The applicable accounting amount remains unresolved between their distinct scopes.

## Documented knowledge

### Day 2 manual rounding

The Day 2 proposal permits adding or decreasing a few cents on a payment cashflow.
The change must remain strictly below USD 1 equivalent.
It uses the upstream exchange rate and refers to the existing authorization-limit process.
The draft names WAITING for the action and requires maker/checker approval.
[Day 2 adjustment, threshold, FX, state, and approval](../../../evidence/sources/sha256/eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13.md#L9-L15)

The source replaces its struck-through original-accounting wording with updated amounts for both SWIFT and accounting.
It asks the reconciliation team to check possible TLM breaks between trades and cashflows.
The proposed popup contains the amount and its USD equivalent.
[Day 2 downstream amounts, reconciliation, and popup](../../../evidence/sources/sha256/eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13.md#L11-L15)

### Korea migration adjustment

The following subsections retain the separate Korea migration proposal.

#### Adjustment scope and threshold

The proposed adjustment permits a change strictly below USD1 equivalent before downstream release.
Currencies beginning with X are excluded.
Eligible flows include gross, net resultants, aggregation resultants, and split parents.
Split resultants cannot be adjusted.

Adjusted cashflows cannot be netted.
Reverting the same cashflow to QUEUED preserves its adjustment.
Economic replacement cashflows do not inherit the old adjustment.

Sources: [original lines 3–12](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L3-L12), [original lines 16–18](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L16-L18), [original lines 20–49](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L20-L49).

#### Maker-checker and amount responsibility

Only makers edit the adjusted amount.
Eligible states are READY/NA/NA or WAITING/Pending Operator/Pending Exception without Pending NDS Netting.
Submission requires checker approval or rejection and highlights the adjustment.
Backend validation covers currency, range, and decimal precision.

TweakAmount and unTweakAmount actions record changes and cancellation.
Payments and LMS use adjusted amounts, while accounting retains original amounts.

Sources: [original lines 51–60](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L51-L60), [original lines 62–94](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L62-L94), [original lines 110–166](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L110-L166).

#### Split and withdrawal contradiction

The closed clarification permits adjustment only on split parents.
One test table nevertheless describes adjustment of a split resultant.
That test table has no recorded result.
Withdrawal examples require adjusted payment and LMS amounts with original accounting.

Repeated netting after reversal/rebooking must not inherit the prior resultant difference.

Sources: [original lines 20–49](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L20-L49), [original lines 110–166](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L110-L166), [original lines 220–229](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L220-L229).

#### Korea submission and decision states

Maker submission moves an eligible cashflow to WAITING with Pending Verification and Pending Exception.
Checker approval returns it to READY.
Rejection returns it to WAITING with Pending Operator and Pending Exception.
The source table distinguishes adjustment rejection from cancellation rejection and their retained amount flags.
These table-specific conditions remain within the Korea proposal.
[Korea submission, approval, rejection, and cancellation transitions](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L74-L93)

The cancellation scenario removes the adjustment before netting previously adjusted components.
Its split scenario requires unsplitting before adjusting the parent and splitting it again.
[Korea cancellation-before-netting and split-parent scenario](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L43-L44)

The Korea design applies the adjusted amount to all SWIFT formats, including MT, MX, and Flip MT202.
Its interface analysis names FMSWG, ENISIS, and LMS as affected downstream systems.
That analysis leaves FXU outside this change because it generates no SWIFT message.
It also excludes LoanIQ amount amendment because RATAN does not feed LoanIQ payment amounts.
[Korea payment formats and downstream scope](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L31-L33)
[Korea LMS, FXU, SWIFT, and LoanIQ boundaries](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L103-L106)

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

Review netting eligibility and cashflow identity when a payment amount changes.
[Auto-netting](KT-settlement-auto-netting.md) and [cashflow identity](KT-settlement-cashflow-identity-and-stella-write-back.md) retain those related rules.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

The Day 2 proposal uses updated amounts for both SWIFT and accounting.
The Korea proposal uses adjusted payment amounts and original accounting amounts.
No inspected source establishes precedence or supersession between these variants.
Their applicable flow, entity, date, state, and reconciliation contracts require owner resolution.
[Day 2 variant](../../../evidence/sources/sha256/eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13.md#L9-L15)
[Korea variant](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L23-L33)

## Open questions

Owner: unknown.

- Which rejection, unsplit, withdrawal, and repeated-adjustment state contract is approved?
- What exchange-rate source, valuation instant, precision, and UAT owner establish the strict USD1 limit?

- Which adjustment design applies to each payment flow, entity, effective date, and cashflow state?
- Which accounting amount applies to each adjustment scope, and how does TLM reconcile the difference?
- Which exchange rate and timestamp determine the USD equivalent?
- Which downstream contracts and rebook linkage cover adjusted payments?
