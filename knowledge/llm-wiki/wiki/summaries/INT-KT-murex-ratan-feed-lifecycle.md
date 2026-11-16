---
type: Summary
description: "Preserves selected Murex 2.11 feed, conversion, eligibility, recovery, and migration proposals with cohort-specific conflicts."
doc_type: short
full_text: sources/INT-KT-murex-ratan-feed-lifecycle.md
---

> **Candidate/draft only:** Current authority, cohort applicability, publication approval, implementation, and rollout remain unconfirmed.

# Murex 2.11 Cashflow Feed and Lifecycle

The selected material assigns eligible non-precious settlement processing to RATAN and Razor while Murex continues trade accounting to Aspire. Precious-metal handling stays with Murex in the described scope. Entity cohorts have different feed windows: nine calendar days in one adaptor, weekday batches in an earlier DOI, and seven system business days in H2 material. Later revisions do not prove that earlier cohort rules were superseded.

RATAN receipt acknowledgement and release are distinct events. The sources disagree on RLSR versus RSLR and whether that status means released or settled. Manual recovery, missing-ACK handling, and republishing also vary between the technical design and DOI instructions.

The conversion material distinguishes original, parent, origin, and latest trade identifiers. It also contains amount-source, payer-direction, event-version, and field-name discrepancies. Eligibility and STP exclusions vary by entity, product, date, and source. The record preserves these rules and open questions; it does not establish an effective current contract or live behavior.

See [[concepts/auto-netting-scheduling]] and [[concepts/cashflow-netting-grouping-and-outcomes]] for the separate scheduled-netting context.

## Canonical sections

- [Responsibility and cohort boundaries](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#responsibility-and-cohort-boundaries)
- [Window and publishing variants](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#window-and-publishing-variants)
- [Status, acknowledgement, and manual recovery](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#status-acknowledgement-and-manual-recovery)
- [Identity, versions, and conversion](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#identity-versions-and-conversion)
- [Eligibility and STP exception variants](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#eligibility-and-stp-exception-variants)
- [Migration boundaries and reconciliation](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#migration-boundaries-and-reconciliation)
