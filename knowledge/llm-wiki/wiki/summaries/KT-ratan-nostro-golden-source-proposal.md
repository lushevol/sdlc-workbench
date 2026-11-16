---
type: Summary
description: "Distinguishes Nostro account classes and records an unapproved NAMS-to-RDM golden-source proposal."
doc_type: short
full_text: sources/KT-ratan-nostro-golden-source-proposal.md
---

> **Candidate/draft only:** NAMS ownership, RDM distribution, and account matching remain proposals. Owner is unknown; `verified` is empty.

# Nostro concepts and golden-source proposal

The knowledge page distinguishes Nostro funds held by this bank at another bank from Vostro funds held here for another bank. The golden-source proposal groups external legal-entity Nostros, same-entity over accounts, and internal suspense accounts under Nostro static. Suspense accounts have no payment or receipt in the described scope.

The proposal nominates NAMS as golden source and RATAN as a pilot consumer through RDM; other FMO systems would follow. Metal-currency accounts would require direct RDM maintenance. Candidate fields include agent SCI, status, currency, settlement means/account, effective dates, FMO-use, and FMO system. Proposed SCI and BIC mappings are source-specific.

The sources leave suspense ownership and storage, caching, matching keys, SSI relevance, correspondent classification, and one-account-to-many-ledger behavior open. No populated account example is retained. The centralization source [[summaries/KT-day2-nostro-centralization-and-rfi]] addresses related upload and dedicated lookup proposals but does not establish this distribution decision. [[summaries/KT-static-data-cache-p3]] retains other reference-data and cache designs, not approval of this golden-source proposal.

## Canonical sections

- [Account distinctions](../../../records/candidates/operations/KT-ratan-nostro-golden-source-proposal.md#account-distinctions)
- [Proposed distribution and fields](../../../records/candidates/operations/KT-ratan-nostro-golden-source-proposal.md#proposed-distribution-and-fields)
- [Unresolved ownership and matching](../../../records/candidates/operations/KT-ratan-nostro-golden-source-proposal.md#unresolved-ownership-and-matching)

Focused synthesis proposal: [[concepts/ssi-instruction-selection-and-stamping]].
