---
type: Summary
description: Documents cashflow ID design and unresolved Stella write-back rules.
doc_type: short
full_text: sources/KT-settlement-cashflow-identity-and-stella-write-back.md
---

> Derived from [the Cash Settlement candidate, version 3](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md). Publication review remains pending. [Source bindings](../../source-manifest.json).

# Cashflow identity and Stella status write-back

The [identity design](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#identity-and-duplicate-handling) preserves Stella IDs. It defines prefixed IDs for Murex 2.11 and MxCash/Razor cashflows. Netting and split resultants receive unique new IDs. The [[summaries/KT-settlement-auto-netting|auto-netting topic]] explains when netting produces a resultant.

The [FX design](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#fx-status-write-back) calls for RATAN to update the matched Stella cashflow to `SUSPENDED-MATURED` after named Razor events. This update aims to reduce duplicate payments. The design does not require write-back for netting or split resultants, or for un-net or un-split events. The applicable match fields, tolerances, and trigger set need confirmation.

The [Stella lifecycle and acknowledgement sources](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#stella-lifecycle-and-acknowledgement) describe different version fields, parties, and steps. The FX assumption, the internal NACK, the Razor ACK, and the Stella booking response do not establish a single acknowledgement contract. Confirm effective scope, retries, and reconciliation before using this draft for acceptance tests. The candidate establishes no deployed behavior.

### Producer-specific identity and payload conditions

Murex distinguishes original, creator, payment-originating and latest trade identities. Its adaptor mappings do not create a universal producer identity alias. The Uber analysis requests complete latest trade, fixing, cashflow and schedule information with correlation. Its business-event identifier was corrected toward trade-tracking and cashflow versions, but the exact version contract remains unresolved. [Payload conditions](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#proposed-uber-payload-completeness-and-correlation).

### Identifier widths and producer boundaries

The identity proposal keeps Stella's 12-character IDs. Murex 2.11 and MxCash/Razor use M/R prefixes and zero padding to 12 characters. Resultants use N/S plus 11 digits, unique across services and concurrent requests. Swift field 20 permits 16 characters. Indonesia separately proposes SID/NID with a stated 12-character width. It does not establish replacement of the N/S namespace. Capacity and applicability remain unresolved. [Identity and duplicate handling](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#identity-and-duplicate-handling).

Original trade identity stability is a source agreement with a reported Murex Counterparty Assignment exception. Uber cashflow ID/version filtering and Stella business-version/status-event filtering use separate contracts. A March 2026 SCBML duplicate-filter row says other group cashflows continue. Its Verified label supplies no execution result, and its paired release summary conflicts. [Producer identity and duplicate scope](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#identity-and-duplicate-handling).

### Write-back matching and retained observations

The FX design includes booking entity, counterparty, currency, amount, value date, and direction in matching. An April 2024 request removes currency, leaving effective precedence unresolved. The tolerance proposal compares the first two currency characters and states amount tolerance as “within decimal for non JPY and within 100 for JPY.” The decimal meaning and equality boundaries remain unresolved. Fees remain PROJECTED and outside this hard block. One SUSPENDED-MATURED cashflow among the trade's two FX cashflows blocks the trade. Update or cancellation lifts that block until another matching update. [FX matching and limits](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#fx-status-write-back).

A May 2024 Undo row describes a NETTED component with a READY/Pending Ack resultant. It requests reversal tagging on the new inbound component, a regression case, and reports a UAT pass. The selected source contains no execution result. This retained observation establishes no current passing assertion. [Dated Undo observation](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#fx-status-write-back).

### Lifecycle and acknowledgement limits

The Stella proposal keeps Payment Date separate from Value Date. Business-version changes reset RATAN minor version. Concurrent amendment/release or amendment/netting can reject write-back. Atomicity, rollback, and automatic reversal remain questions. Component-ID write-back cardinality differs for netted and gross flows. The regional Murex adaptor excludes SETTLED synchronization, so general synchronization wording cannot establish universal propagation. [Lifecycle and acknowledgement](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#stella-lifecycle-and-acknowledgement).
