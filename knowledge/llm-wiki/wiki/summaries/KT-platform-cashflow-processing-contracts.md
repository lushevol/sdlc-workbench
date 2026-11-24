---
type: Summary
description: "Collects historical lifecycle, holding, SSI, fixing, LIEN, IRS, confirmation, and payment-adjustment design proposals."
doc_type: short
full_text: sources/KT-platform-cashflow-processing-contracts.md
---

> **Candidate/draft only:** The selected designs do not establish current platform behavior, adopted interfaces, or approved policy.

# Platform Cashflow Processing Contracts

The lifecycle matrix lists event and state transitions but leaves many field sources and update conditions blank. It cannot define a complete persistence or permission contract. A separate holding design blocks selected in-progress states and proposes restoring the prior status on unhold; the maker-checker design assigns orchestration to Camunda and basic business logic to domain services.

Other design fragments cover hot NSTP rules, ad-hoc SSI, mandatory-field checks, fixing notifications, LIEN refresh, IRS leg matching, cashflow stamping, and confirmation-driven exception closure. Their conditions are specific. For example, the confirmation chain requires MATCHED plus Confirm/Affirm, a CN settlement link, and WAITING with isNstp; it does not close every confirmation event.

A small-payment adjustment proposal requires maker-checker approval before release, applies to eligible cashflows below a configured USD 1 equivalent threshold, and sends different amounts to Swift/LMS versus accounting. Eligible currencies, conversion rate, precision, and boundary behavior remain unspecified. The selected material also retains contradictory cancelled-fixing and LIEN alternatives.

## Canonical sections

- [Lifecycle transition source limits](../../../records/candidates/settlement/KT-platform-cashflow-processing-contracts.md#lifecycle-transition-source-limits)
- [Holding and process separation](../../../records/candidates/settlement/KT-platform-cashflow-processing-contracts.md#holding-and-process-separation)
- [Hot rules, SSI, and mandatory checks](../../../records/candidates/settlement/KT-platform-cashflow-processing-contracts.md#hot-rules-ssi-and-mandatory-checks)
- [Fixing notification and LIEN design](../../../records/candidates/settlement/KT-platform-cashflow-processing-contracts.md#fixing-notification-and-lien-design)
- [Confirmation-driven exception closure](../../../records/candidates/settlement/KT-platform-cashflow-processing-contracts.md#confirmation-driven-exception-closure)
- [Small payment adjustment requirement](../../../records/candidates/settlement/KT-platform-cashflow-processing-contracts.md#small-payment-adjustment-requirement)


## Related candidate topics

- [[summaries/KT-cashflow-group-validation-p3]]
- [[summaries/KT-settlement-processing-and-exception-controls]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
