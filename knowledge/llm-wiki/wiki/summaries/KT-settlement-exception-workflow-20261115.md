---
type: Summary
description: "Summarizes candidate settlement exception workflow, affirmation, recovery, and batch contract differences."
doc_type: short
full_text: sources/KT-settlement-exception-workflow-20261115.md
---

# Settlement exception workflow

> **Source status:** Candidate/draft. Historical design and batch proposals are not evidence of current workflow execution.

The combined-exception design lets successful corrections remain effective when another section fails. Maker/checker states and cashflow identity bind the workflow; manual affirmation depends on which team performed manual touch and a stated high-value threshold. That amount alone does not prevent STP. Previously sent payments are directed to AMH for manual resend. [Combined exception resolution](../../../records/candidates/settlement/KT-settlement-exception-workflow-20261115.md#combined-exception-resolution) [Manual-touch affirmation and separation](../../../records/candidates/settlement/KT-settlement-exception-workflow-20261115.md#manual-touch-affirmation-and-separation) [Payment and instruction controls](../../../records/candidates/settlement/KT-settlement-exception-workflow-20261115.md#payment-and-instruction-controls)

The proposed envelope carries exception IDs and statuses through metadata, with separate maker/checker endpoints and synchronous updates. Recovery proposals assign missing-feed replay to operations and technical reconsumption after dependencies recover. [Workflow and exception contracts](../../../records/candidates/settlement/KT-settlement-exception-workflow-20261115.md#workflow-and-exception-contracts) [Historical recovery responsibilities](../../../records/candidates/settlement/KT-settlement-exception-workflow-20261115.md#historical-recovery-responsibilities)

One source prohibits cross-cashflow approval; another proposes bulk actions with a 1000-item affirmation threshold. Batch identity also changes from `referenceId` to `cashflowId`, and one example reports aggregate success with an item failure. These contracts require reconciliation. [Bulk processing remains a separate proposal](../../../records/candidates/settlement/KT-settlement-exception-workflow-20261115.md#bulk-processing-remains-a-separate-proposal) [Batch limitation contract ambiguity](../../../records/candidates/settlement/KT-settlement-exception-workflow-20261115.md#batch-limitation-contract-ambiguity)

See proposed [[summaries/KT-settlement-multi-exception-control]].
