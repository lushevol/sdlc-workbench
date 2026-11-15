---
type: KnowledgeTopic
id: KT-settlement-payment-amount-adjustment
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-f7a77181055251dcfe5c2c89
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Manual Rounding/page.md
  revision: sha256:eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13
  sha256: eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13
- id: SRC-fb095b467d64d97bae865108
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/2026 Changes/Cash Settlement -- Korea Migration/Increase Payment Amount within USD 1 Threshold/page.md
  revision: sha256:b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2
  sha256: b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2
generated:
  by: agent:codex
  at: '2026-11-15T08:53:00+00:00'
verified: []
classification: settlement
scope: Documented manual payment amount adjustments and their effect on settlement output.
summary: Both designs use a strict limit below USD 1 equivalent and maker/checker approval. The accounting rules and eligible states differ.
related:
- KT-settlement-auto-netting
- KT-settlement-cashflow-identity-and-stella-write-back
open_questions:
- Which adjustment design applies to each payment flow, entity, effective date, and cashflow state?
- Which accounting amount applies to each adjustment scope, and how does TLM reconcile the difference?
- Which exchange rate and timestamp determine the USD equivalent?
- Which downstream contracts and rebook linkage cover adjusted payments?
---
# Payment amount adjustment

## Scope

This topic covers manual changes to payment cashflow amounts before settlement. It records the Day 2 and Korea migration designs with their applicability limits.

## Summary

Both designs require maker/checker approval and a change below USD 1 equivalent. They differ on the accounting amount and eligible cashflow states.

## Documented knowledge

### Day 2 manual rounding

The Day 2 design allows a user to adjust a payment amount in cents in WAITING. It uses the upstream exchange rate. The current wording in the source uses the updated amount for SWIFT and accounting. The source asks the reconciliation team about possible TLM differences. It requires maker/checker approval. [Manual rounding](../../../evidence/sources/sha256/eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13.md#L9-L13) [Approval](../../../evidence/sources/sha256/eaecb8cf492b8847baf94dca02b61152f51176bc7e9368a98e17441b40cd0c13.md#L15)

### Korea migration adjustment

The Korea migration design permits changes before downstream release on gross cashflows, net resultants, and split parents. It excludes X-prefixed precious-metal currencies and split resultants. Cancel the adjustment before netting. A return to QUEUED retains the adjusted amount. [Eligibility and amount limit](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L22-L30) [Cancellation scenario](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L39-L46)

A maker can edit in the specified WAITING or READY states. The WAITING path excludes Pending NDS Netting. The backend validates currency, amount range, and decimal places. A submission enters Pending Verification. Checker approval returns READY. Rejection returns to WAITING with Pending Operator and Pending Exception. [Edit scope](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L53-L60) [Validation and transitions](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L64-L77)

The design sends the adjusted amount in SWIFT and uses the original amount for settlement accounting. Its open questions record a closed answer for split parents and a strict threshold below USD 1. The affected contract and effective scope still need review. [Downstream amounts](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L31-L33) [Recorded answers](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L224-L227)

## Connections

Review netting eligibility and cashflow identity when a payment amount changes. [Auto-netting](KT-settlement-auto-netting.md) [Cashflow identity](KT-settlement-cashflow-identity-and-stella-write-back.md)

## Evidence limits

The two sources give different accounting rules. Their respective effective scopes and any supersession require owner review. The Korea design also contains a test scenario that adjusts a split child. That scenario conflicts with the recorded split-parent answer. [Split child scenario](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L155-L160) [Split-parent answer](../../../evidence/sources/sha256/b4752705e8346717931ed280e8168a5a1e11870463974ecbbfbf0160d9ee79c2.md#L224)

## Open questions

- Which adjustment design applies to each payment flow, entity, effective date, and cashflow state?
- Which accounting amount applies to each adjustment scope, and how does TLM reconcile the difference?
- Which exchange rate and timestamp determine the USD equivalent?
- Which downstream contracts and rebook linkage cover adjusted payments?
