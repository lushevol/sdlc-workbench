---
type: Summary
description: Documents cashflow ID design and unresolved Stella write-back rules.
doc_type: short
full_text: sources/KT-settlement-cashflow-identity-and-stella-write-back.md
---

> Derived from [the Cash Settlement candidate, version 1](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md). Publication review remains pending. [Source bindings](../../source-manifest.json).

# Cashflow identity and Stella status write-back

The [identity design](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#identity-and-duplicate-handling) preserves Stella IDs. It defines prefixed IDs for Murex 2.11 and MxCash/Razor cashflows. Netting and split resultants receive unique new IDs. The [[summaries/KT-settlement-auto-netting|auto-netting topic]] explains when netting produces a resultant.

The [FX design](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#fx-status-write-back) calls for RATAN to update the matched Stella cashflow to `SUSPENDED-MATURED` after named Razor events. This update aims to reduce duplicate payments. The design does not require write-back for netting or split resultants, or for un-net or un-split events. The applicable match fields, tolerances, and trigger set need confirmation.

The [Stella lifecycle and acknowledgement sources](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#stella-lifecycle-and-acknowledgement) describe different version fields, parties, and steps. The FX assumption, the internal NACK, the Razor ACK, and the Stella booking response do not establish a single acknowledgement contract. Confirm effective scope, retries, and reconciliation before using this draft for acceptance tests. The candidate establishes no deployed behavior.
