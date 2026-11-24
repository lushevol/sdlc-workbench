---
type: Summary
description: "Records candidate SSI form fields, conditional SWIFT formats, purpose rules, and adhoc transition conflicts."
doc_type: short
full_text: sources/KT-settlement-ssi-form-validation.md
---

> **Candidate/draft only:** These form rules await authority and applicability review. Owner is unknown; `verified` is empty.

# SSI form validation and adhoc correction controls

The form requires settlement account, settlement means, SSI type, message type, and eBBS Nostro account. Its selected page lists Primary/Secondary SSI types and MT103, MT103 SERIAL, and MT202 message types. Conditional beneficiary and ordering fields vary by message and currency. Several formats remain unknown; other rows disagree between prose and regex, including `Nostro` versus `NOS`. The source does not authorize normalization.

MT103 and MT202 branches carry distinct account and BIC requirements. MT103 charges permit OUR/SHA/BEN. For MT103 plus NOS, covered-payment behavior links field54 BIC to a selected checkbox. Adhoc/Vostro-exception input cannot populate fields54 and56 together. Fields70/72 use maker/checker handling. The Dubai purpose field has a source-specific entity, currency, settlement-means, account, and beneficiary predicate; current product or regional scope is unconfirmed.

Two adhoc tables disagree on the initial READY transition and checker rejection outcome. Keep those state descriptions separate pending a decision. The record establishes no current Swift dictionary, live form behavior, approval, or execution.

## Canonical sections

- [Mandatory form fields](../../../records/candidates/settlement/KT-settlement-ssi-form-validation.md#mandatory-form-fields)
- [Conditional beneficiary and ordering fields](../../../records/candidates/settlement/KT-settlement-ssi-form-validation.md#conditional-beneficiary-and-ordering-fields)
- [Dubai purpose predicate](../../../records/candidates/settlement/KT-settlement-ssi-form-validation.md#dubai-purpose-predicate)
- [Adhoc transition conflict](../../../records/candidates/settlement/KT-settlement-ssi-form-validation.md#adhoc-transition-conflict)

The existing [[concepts/maker-checker-verification-workflow]] covers two-person admin verification; it does not settle these SSI transitions.

Focused synthesis proposal: [[concepts/ssi-instruction-selection-and-stamping]].
