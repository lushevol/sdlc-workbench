---
type: "Summary"
description: "Summarizes proposed Swap Agent netting, SWIFT suppression, and release-blocker behavior."
doc_type: short
full_text: "sources/KT-day2-swap-agent.md"
---

> Derived from [candidate record version 2](../../../records/candidates/settlement/KT-day2-swap-agent.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Swap Agent netting and release controls

The Day 2 design separates Coupon and Interim MTM netting predicates. It proposes a 30-minute retry after job failure, payment-type-specific resultants, and SWIFT suppression. It excludes Initial and Final Notional from the existing rule. [Candidate claims](../../../records/candidates/settlement/KT-day2-swap-agent.md#documented-knowledge)

The enhancement proposes principal exchanges for selected clients, cross-payment-type netting, and Murex/Stella cashflows within that scope. It says existing SAL Coupon and SAL MTM rules continue for out-of-scope clients. These scope and applicability statements remain proposals.

A separate selected design proposes a hard blocker against releasing SWAP_AGENT Coupon and Interim MTM cashflows from RATAN. It does not define the trigger, permitted exit path, or ordering with scheduled netting and SWIFT suppression. [Blocker and evidence limits](../../../records/candidates/settlement/KT-day2-swap-agent.md#documented-knowledge) [Open questions](../../../records/candidates/settlement/KT-day2-swap-agent.md#open-questions)

## Related topics

- [[summaries/KT-settlement-auto-netting|Scheduled auto-netting]] covers rule selection and scheduled processing.
- [[summaries/KT-settlement-lms-feed|LMS feed]] records downstream feed and suppression proposals.
- [[summaries/KT-settlement-clearing-and-swap-agent-boundaries|Clearing and Swap Agent boundaries]] records separate historical payment and accounting proposals.

Owner, client scope, effective date, current implementation, and deployment remain unverified. The candidate preserves its [open applicability and blocker questions](../../../records/candidates/settlement/KT-day2-swap-agent.md#open-questions).

### Distinct payment-type and selected-client rules

The Day 2 rule keeps Coupon and Interim MTM separate. The selected-client enhancement instead permits cross-payment-type and cross-producer netting. It proposes SwapAgentNetting above SALMTM priority at VD 01:00 GMT. Suppressed singletons and resultants remain scoped proposals. Other clients keep the older SAL rules. [Selected-client conditions](../../../records/candidates/settlement/KT-day2-swap-agent.md#l3-swap-02--selected-client-enhancement).

The selected-client proposal uses Murex strategy `SWAP_AGENT` or Stella `SwapAgentID`. It proposes no currency filter. An unchecked payment-type list supplies no approval for every entry. Suppressed cashflows do not feed LMS. The release-blocker trigger, exit, and ordering remain unresolved. [Existing rules](../../../records/candidates/settlement/KT-day2-swap-agent.md#l3-swap-01--existing-payment-type-rules). [Selected scope](../../../records/candidates/settlement/KT-day2-swap-agent.md#l3-swap-02--selected-client-enhancement).
