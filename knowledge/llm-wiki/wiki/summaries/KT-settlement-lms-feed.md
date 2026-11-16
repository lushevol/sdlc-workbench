---
type: Summary
description: Summarizes the LMS feed baseline and later status, entity, and payload proposals.
doc_type: short
full_text: sources/KT-settlement-lms-feed.md
---

> Derived from [candidate record version 1](../../../records/candidates/settlement/KT-settlement-lms-feed.md). Owner review and publication remain pending.

# Settlement cashflow feeds to LMS

The candidate records a 2023 release and settlement baseline. Later proposals add receive-only Swift Suppressed receipt events and broaden RATAN entity delivery. [Baseline](../../../records/candidates/settlement/KT-settlement-lms-feed.md#release-and-settlement-baseline) [Receipt proposal](../../../records/candidates/settlement/KT-settlement-lms-feed.md#proposed-receive-only-swift-suppression) [Entity scope](../../../records/candidates/settlement/KT-settlement-lms-feed.md#entity-scope-and-downstream-delivery).

Selected designs also propose source-stack, Field 20 prefix, and netting-resultant values. Effective dates, downstream consumer scope, payload behavior, and blank taxonomy handling remain open. [Source mappings](../../../records/candidates/settlement/KT-settlement-lms-feed.md#source-values-netting-and-field-20) [Evidence limits](../../../records/candidates/settlement/KT-settlement-lms-feed.md#evidence-limits).

The candidate does not establish an approved or deployed feed contract.

## Related topics

- [[summaries/KT-settlement-cpn-netting|CPN netting]] includes the related resultant and component lifecycle proposals.
- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity]] records additional source-stack and resultant identity questions.

## Baseline predicates and later proposals

The July 2023 page records agreement for its then-current baseline. RELEASED or SETTLED and settlement means NOS are required. Beneficiary BIC REJECTXXALL excludes the cashflow. SCB pay requires Nostro and Vostro; receive requires Nostro. A released withdrawal can feed after maker/checker action. WAITING/PendingException withdrawal does not feed at that step. The settled-receipt example has Notice to Receive N. This dated agreement does not resolve later changes or current applicability. [Baseline conditions](../../../records/candidates/settlement/KT-settlement-lms-feed.md#release-and-settlement-baseline).

The receive-only Swift Suppressed proposal leaves undo and withdrawal-to-CANCELLED events pending LMS confirmation despite an internal request. Template, FAILED transitions, and unavailable stamping data remain open. The entity proposal removes the RATAN sender filter while retaining the template. It does not establish every downstream consumer's entity scope. [Receipt events](../../../records/candidates/settlement/KT-settlement-lms-feed.md#proposed-receive-only-swift-suppression). [Sender and consumer scope](../../../records/candidates/settlement/KT-settlement-lms-feed.md#entity-scope-and-downstream-delivery).

The prefix table maps STELLA→EQ, LOANIQ→LQ, and FMRP→DV, while prose names MX for Razor's FMRP China SWIFT. Consumer and period need confirmation. The stack design excludes NativeSTELLA from RATAN. Its rejected extra-field alternative cannot establish an accepted payload. Netting stack inheritance and mixed-component fallback remain unresolved. The cross-product N-prefixed resultant has a proposed blank-allotment fallback NETTING RESULTANT. General null-taxonomy behavior remains open. Event listeners do not establish send predicates because that table leaves them blank. [Source and resultant mappings](../../../records/candidates/settlement/KT-settlement-lms-feed.md#source-values-netting-and-field-20). [Event scope](../../../records/candidates/settlement/KT-settlement-lms-feed.md#event-sources).
