---
type: Summary
description: "Preserves HKCS HAU settlement, calendar, SWIFT-message, onboarding, and cancellation-source differences."
doc_type: short
full_text: sources/KT-day2-hkcs-hau-settlement.md
---

> **Candidate/draft only:** The HAU rules and static values require current authority review. Owner is unknown; `verified` is empty.

# HKCS HAU settlement and SWIFT intent

The requirement scopes HAU to FX booked in SCB Hong Kong, entity FMID 2. It suppresses the counter-currency cashflow, sets a value-date-minus-one-business-day cutoff at 10:00 GMT, and maps the Hong Kong calendar through an HKD calendar. The selected source states three decimal places with rounding off and no RATAN settlement-accounting publication; HAU messages still feed LMS.

MT604/605 and SCT/DVP branches specify receiver, field, amount, currency, lookup, and error behavior. Some mappings depend on an uninspected image. The Nostro-agent and SWIFT receiver BIC spellings differ, and PVP indicators are not reconciled with a separate DVP clarification. Do not normalize these values.

The later business requirement specifies MT692 cancellation, while an onboarding TBD lists MT605. Onboarding also proposes static changes and a missing-Vostro exception. Its “no change” label does not prove configured behavior. Linked samples were not inspected.

## Canonical sections

- [HKCS-01 — HAU settlement scope and lifecycle](../../../records/candidates/settlement/KT-day2-hkcs-hau-settlement.md#hkcs-01--hau-settlement-scope-and-lifecycle)
- [HKCS-02 — MT604 and MT605 generation](../../../records/candidates/settlement/KT-day2-hkcs-hau-settlement.md#hkcs-02--mt604-and-mt605-generation)
- [HKCS-03 — SCT and DVP instructions](../../../records/candidates/settlement/KT-day2-hkcs-hau-settlement.md#hkcs-03--sct-and-dvp-instructions)
- [HKCS-05 — Onboarding dependencies and unresolved cancellation item](../../../records/candidates/settlement/KT-day2-hkcs-hau-settlement.md#hkcs-05--onboarding-dependencies-and-unresolved-cancellation-item)

Related context: [[summaries/KT-settlement-lms-feed]] and [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]].
