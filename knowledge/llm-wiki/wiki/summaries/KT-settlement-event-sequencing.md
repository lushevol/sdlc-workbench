---
type: Summary
description: "Summarizes candidate trade and cashflow event order, batch completion, post-release branches, and mapping gaps."
doc_type: short
full_text: sources/KT-settlement-event-sequencing.md
---

> **Candidate/draft only:** Event mappings and concurrent-order behavior remain unapproved. Owner is unknown; `verified` is empty.

# Settlement event sequencing

The design uses New and Withdrawal events identified by Stella trade ID, cashflow major version, and batch sequence. Incomplete batches stay outside the blotter and settlement flow. A later batch waits until the previous batch reaches STP or NSTP; this is a processing checkpoint, not settlement. The source expects New/Withdrawal sequences to execute in order and repeated New events to process only the first.

Post-release cancellation or amendment follows NSTP reversal/rebooking proposals. Closeout uses a new NSTP trade and manual netting. Portfolio reassignment calls for duplicate-payment inspection and suppression. Revival restores an unreleased original cancellation. Other branches distinguish already-released cashflows, same-period fixing after release, and expiry.

Murex mappings translate RPL, RPL_M, MOD, CNCL, and XIT into Withdrawal plus New; RPL_D, EXR, and NET have separate mappings. Examples do not prove execution. The record leaves linked versus independent multicurrency resultant cancellation open.

## Canonical sections

- [Event identity and sequencing](../../../records/candidates/settlement/KT-settlement-event-sequencing.md#event-identity-and-sequencing)
- [Post-release lifecycle branches](../../../records/candidates/settlement/KT-settlement-event-sequencing.md#post-release-lifecycle-branches)
- [Murex event mapping and limits](../../../records/candidates/settlement/KT-settlement-event-sequencing.md#murex-event-mapping-and-limits)

Related candidates: [[summaries/KT-settlement-non-economic-amendments]] and [[summaries/KT-settlement-cashflow-identity-and-stella-write-back]].
