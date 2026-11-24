---
type: Summary
description: "Summarizes proposed inter-entity eligibility, reciprocal matching, netting, and linked withdrawal rules with scope unresolved."
doc_type: short
full_text: sources/KT-day2-inter-entity-netting.md
---

> **Candidate/draft only:** Phase scope, branch mapping, STP, and withdrawal outcomes remain proposed and unapproved.

# Inter-Entity Matching and Netting

Phase one covers selected gross flows and IRS aggregation resultants, nets USD only, and limits value to at most USD 100,000 equivalent. The source places amount enrichment after VD-5 materialization and refreshes it on reinstatement. It lists branch pairs and excludes LOANIQ in embedded rules; production membership still needs owner confirmation.

Pre-match requires equal currency, value date, amount, and opposite directions. Each booking-entity FMID must equal the opposite counterparty mapped FMID. The key then uses booking entity, value date, currency, and mapped counterparty. The source describes matched groups as eligible for automatic netting with affirmation; unmatched singletons go gross without affirmation. Full-STP and auto-affirmation statements need reconciliation.

Linked withdrawal rules apply to both resultants. Before the stated release boundary, the design can remove both resultants and regroup remaining flows. The boundary includes READY/Pending Ack, RELEASED, SETTLED, and corresponding SPLIT states. If either side crosses it, automatic un-netting stops and manual handling is required. A separate Murex 2.11 STP request leaves the identifier and exception-bypass list undefined. The existing [[concepts/auto-netting-rule-selection]] and [[concepts/cashflow-netting-grouping-and-outcomes]] pages cover a distinct scheduled workflow.

## Canonical sections

- [IEN-01 — Phase-one eligibility and USD enrichment](../../../records/candidates/settlement/KT-day2-inter-entity-netting.md#ien-01--phase-one-eligibility-and-usd-enrichment)
- [IEN-02 — Reciprocal pre-match and resultant rules](../../../records/candidates/settlement/KT-day2-inter-entity-netting.md#ien-02--reciprocal-pre-match-and-resultant-rules)
- [IEN-03 — Direction-specific pre-match key design](../../../records/candidates/settlement/KT-day2-inter-entity-netting.md#ien-03--direction-specific-pre-match-key-design)
- [IEN-05 — Linked withdrawal and release boundary](../../../records/candidates/settlement/KT-day2-inter-entity-netting.md#ien-05--linked-withdrawal-and-release-boundary)
- [IEN-06 — Separate internal-counterparty STP request](../../../records/candidates/settlement/KT-day2-inter-entity-netting.md#ien-06--separate-internal-counterparty-stp-request)
