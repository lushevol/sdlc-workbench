---
type: Summary
description: "Summarizes candidate non-economic comparison fields, settlement identity handling, and later economic amendment behavior."
doc_type: short
full_text: sources/KT-settlement-non-economic-amendments.md
---

> **Candidate/draft only:** Identity, comparison, and product scope need owner confirmation. Owner is unknown; `verified` is empty.

# Settlement non-economic amendments

The sources compare booking FMID, counterparty FMID, currency, amount, value date, and pay/receive. When all six match, the design treats replacements as non-economic: originals remain active for settlement while replacement identities are hidden operationally. The trade still receives a new version and replacement cashflow identities.

Original settlement identities remain in Razor, LMS, and the EOD cashflow API; replacements are excluded. Stella status updates target replacement identities. A later economic amendment withdraws original settlement identities before creating new cashflows. Trade confirmation uses the latest CDU trade ID and version for both economic and non-economic amendments.

These are source-specific proposals. The record does not resolve repeated non-economic amendments followed by economic change, effective product versions, or feed behavior. The active [[summaries/KT-settlement-amendment-reversal-rebook-exceptions]] covers released amendment exceptions. [[summaries/KT-settlement-cashflow-identity-and-stella-write-back]] covers identity and status write-back. The proposed [[summaries/INT-KT-cashflow-amendment-and-release-controls]] covers separate economic/key-field classification.

## Canonical sections

- [Non-economic comparison](../../../records/candidates/settlement/KT-settlement-non-economic-amendments.md#non-economic-comparison)
- [Settlement identity and external status identity](../../../records/candidates/settlement/KT-settlement-non-economic-amendments.md#settlement-identity-and-external-status-identity)
- [Trade confirmation identity](../../../records/candidates/settlement/KT-settlement-non-economic-amendments.md#trade-confirmation-identity)

Focused synthesis proposal: [[concepts/cashflow-amendment-classification-and-release]].
