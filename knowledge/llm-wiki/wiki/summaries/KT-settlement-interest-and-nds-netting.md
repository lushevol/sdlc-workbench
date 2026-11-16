---
type: Summary
description: "Summarizes candidate IRS fixing gates, interest aggregation, and NDS netting scope and lifecycle proposals."
doc_type: short
full_text: sources/KT-settlement-interest-and-nds-netting.md
---

# IRS leg completeness and NDS netting proposal

> **Source status:** Candidate/draft. Regional rules and scenarios do not establish current implementation, approval, or executed results.

IRS fixing gates vary by region, source, and value-date window. Selected branches hold pending-fixing legs or mark Fixing Unknown, then process correcting files under listed states. FMRP's unequal-schedule proposal is separate from Murex rules. Within-trade and cross-trade aggregation are proposed, but example arithmetic is inconsistent and must not supply corrected accounting values. [L3-IRS-01](../../../records/candidates/settlement/KT-settlement-interest-and-nds-netting.md#l3-irs-01--regional-murex-fixing-gates) [L3-IRS-03](../../../records/candidates/settlement/KT-settlement-interest-and-nds-netting.md#l3-irs-03--aggregation-and-scenario-limits) [L3-IRS-05](../../../records/candidates/settlement/KT-settlement-interest-and-nds-netting.md#l3-irs-05--fmrp-unequal-schedule-exception)

The NDS proposal moves specified products from Murex netting to RATAN, groups by entity, counterparty, date, currency, and NID, and scans every 30 minutes across a stated horizon. It requires a live NSTP rule. NDIRS has a separate USD fixing path. Before-release amendment or refixing can un-net and re-net; after payment release, reversal/rebook and manual handling apply. Resultant fields and payment-type precedence remain inconsistent. [L3-NDS-01](../../../records/candidates/settlement/KT-settlement-interest-and-nds-netting.md#l3-nds-01--nds-scope-and-scheduler) [L3-NDS-03](../../../records/candidates/settlement/KT-settlement-interest-and-nds-netting.md#l3-nds-03--nds-amendment-and-resultant-rules)

See [[concepts/auto-netting-scheduling]], [[summaries/KT-settlement-manual-netting]], and proposed [[summaries/KT-settlement-manual-netting]].
