---
type: Summary
description: "Records candidate receive-side Cross Border Debit MT202 eligibility, mapping, and overlap questions."
doc_type: short
full_text: sources/KT-day2-cross-border-debit.md
---

> **Candidate/draft only:** Cross-debit precedence, static BICs, and current applicability remain unresolved. Owner is unknown; `verified` is empty.

# Cross-border debit MT202 intent

The requirement replaces MT202Flip for receive-side cross-border debit when another SCB entity holds the client account. It uses a Vostro settlement account in `CCY CROSSDEBIT` format to trigger MT202 CROSSDEBIT and explicitly excludes MT103 CROSSDEBIT. Pay-side flows retain ordinary MT103/MT202 mapping. Accounting remains as described, and the cashflow feed goes to LMS. A January 2026 note checks cross-debit before Flip, while earlier Nostro/OverAccount overlap text remains open.

The selected mapping uses Vostro BIC in sender and receiver blocks; Vostro beneficiary details in fields 52 and 53B; Nostro-agent BIC in field57A; and a backend legal-entity BIC in field58, with an optional Nostro account. The source rejects a separate GMO BIC substitution. It does not supply current maintained static mappings or establish the LMS contract.

Related candidate static-data context: [[summaries/KT-ratan-nostro-golden-source-proposal]].

## Canonical sections

- [Eligibility and scope](../../../records/candidates/settlement/KT-day2-cross-border-debit.md#eligibility-and-scope)
- [Message mapping](../../../records/candidates/settlement/KT-day2-cross-border-debit.md#message-mapping)

## Related candidate topics

- [[summaries/KT-day2-hkcs-hau-settlement]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
