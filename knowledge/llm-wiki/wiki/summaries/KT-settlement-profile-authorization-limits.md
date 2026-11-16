---
type: Summary
description: "Summarizes candidate legacy USD profile limits, FX conversion, static maintenance, and action-visibility proposals."
doc_type: short
full_text: sources/KT-settlement-profile-authorization-limits.md
---

# Settlement profile authorization limits

> **Source status:** Candidate/draft. Limits, labels, and visibility designs do not establish current grants or CES mappings.

A source lists checker thresholds below USD 30 million, USD 100 million, and USD 1 billion for clerk, officer, and lead, with manager up to USD 4 billion. Thresholds are described as maintainable static data. Legacy RATAN and RAZOR profile labels remain distinct and are not evidence of CES role equivalence. [WF-CF-060](../../../records/candidates/settlement/KT-settlement-profile-authorization-limits.md#wf-cf-060) [Profile identities and action distinctions](../../../records/candidates/settlement/KT-settlement-profile-authorization-limits.md#profile-identities-and-action-distinctions)

Profile-limit static changes require maker/checker. Non-USD conversion uses Stella FX spot rate with USD as quote currency, but rate date, EOD tag, precision, and failure handling are unspecified. A later proposal separates the fields `Profile`, `Currency`, `USDConverted`, and `Limit`, and hides submit/approve when authorization fails. It does not establish a deployed model or whether button visibility is sufficient. [WF-CF-061](../../../records/candidates/settlement/KT-settlement-profile-authorization-limits.md#wf-cf-061) [WF-CF-062](../../../records/candidates/settlement/KT-settlement-profile-authorization-limits.md#wf-cf-062)

Confirm limits and action grants by entity/date, conversion rules, and current ownership. See [[summaries/KT-ces-entitlement-control-20261115]] and proposed [[summaries/KT-settlement-multi-exception-control]].
