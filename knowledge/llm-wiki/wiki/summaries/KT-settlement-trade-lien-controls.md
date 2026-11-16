---
type: Summary
description: "Summarizes candidate LIEN propagation, maker-checker, cashflow-state, and reprocessing rules."
doc_type: short
full_text: sources/KT-settlement-trade-lien-controls.md
---

# Settlement trade lien controls

> **Source status:** Candidate/draft. Historical lien-process documents do not establish current approved controls.

The selected design treats LIEN as a trade-level exception that affects every underlying payment type, including interest and notional. Placement or amount update makes those cashflows NSTP and requires maker-checker handling. Removal permits STP only when no other exception remains. A resultant inherits LIEN when any component parent trade carries it; operations profiles cannot remove or edit the predefined exception. [Trade-level LIEN controls](../../../records/candidates/settlement/KT-settlement-trade-lien-controls.md#trade-level-lien-governs-cashflows)

New LIEN can reprocess WAITING/Pending Exception, HOLD, and READY cashflows that lack the exception. It can trigger unnetting only when the resultant lacks LIEN and remains outside protected released-like states. The source names READY/Pending Ack, RELEASED, and SETTLED as protected states. A later trade notification must account for cashflows received before the trade update. [Notification reprocessing](../../../records/candidates/settlement/KT-settlement-trade-lien-controls.md#lien-notification-reprocessing) [Open question](../../../records/candidates/settlement/KT-settlement-trade-lien-controls.md#open-questions)

Amounts, removal, post-release behavior, and notification ordering remain unresolved. Related proposals: [[summaries/KT-settlement-multi-exception-control]] and [[summaries/KT-settlement-interest-and-nds-netting]].
