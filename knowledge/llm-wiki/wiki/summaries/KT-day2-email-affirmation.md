---
type: Summary
description: "Summarizes candidate trade and email affirmation publication, response classification, correction, and transport rules."
doc_type: short
full_text: sources/KT-day2-email-affirmation.md
---

# Email and trade-driven affirmation control intent

> **Source status:** Candidate/draft. Email publication and AI response handling are proposals, without verified dispatch or business acceptance.

The outbound proposal publishes selected cashflows and SSI/Nostro detail to CDUPS, with configurable entity, client, product, portfolio, source, payment, and settlement filters. Status scopes differ, and dated refinements exclude several product or portfolio classes. Scheduling, contacts, resend, and failure notices are proposed; encryption details, sender identity, and recipient-change handling remain open. [AFF-01](../../../records/candidates/settlement/KT-day2-email-affirmation.md#aff-01--outbound-publication-scope) [AFF-02](../../../records/candidates/settlement/KT-day2-email-affirmation.md#aff-02--scheduling-contacts-and-distribution-audit)

A positive AI-classified reply may clear Pending Affirmation through maker automation, but other exceptions remain NSTP and still require resolution. Negative or ambiguous responses need manual handling. Email transport and message fields remain subject to business confirmation; the net-resultant counterparty allowance conflicts with its mandatory marker. [AFF-03](../../../records/candidates/settlement/KT-day2-email-affirmation.md#aff-03--inbound-ai-response-control) [AFF-04](../../../records/candidates/settlement/KT-day2-email-affirmation.md#aff-04--proposed-email-fields-and-transport)

Trade-state trigger inputs lack result-state mappings, and the use-case expected-result cell is empty. Dispatch success and AI classification cannot fill that gap. See [[summaries/KT-settlement-multi-exception-control]] and proposed [[summaries/KT-settlement-multi-exception-control]]. [AFF-05](../../../records/candidates/settlement/KT-day2-email-affirmation.md#aff-05--scheduled-outbound-versus-inbound-trigger) [AFF-06](../../../records/candidates/settlement/KT-day2-email-affirmation.md#aff-06--separate-trade-state-input-and-affirmation-predicate)
