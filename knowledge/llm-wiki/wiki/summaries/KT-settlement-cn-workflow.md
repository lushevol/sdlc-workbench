---
type: Summary
description: "Maps historical CN workflow, demo expectations, and migration proposals while keeping dates, conflicts, and execution limits visible."
doc_type: short
full_text: sources/KT-settlement-cn-workflow.md
---

> **Candidate/draft only:** These historical and undated proposals have no confirmed current authority or execution evidence.

# Historical CN Workflow and Migration

The selected CN material combines an undated workflow, 2022 Sprint 13/14 demos, an undated Sprint 17 page, operations notes, a migration proposal that assumes a May 2024 cutover, and a separate status machine. It describes producer-specific New, Amend, and Withdrawal events, delayed materialization, maker-checker actions, netting, and migration controls.

Demo rows state expected results for mocked or manual submissions, including PROJECTED-to-QUEUED transitions and netting/un-netting outcomes. They are not retained test results. Sprint 17 combines mocked Stella inputs with Murex booking steps.

Migration comparisons disagree between a nine-day horizon and T+7. Reversal suppression, early-settlement treatment, aggregate-flow predicates, LMS handling, and withdrawal transitions also conflict. One source uses DEAD/VALIDATED for a pre-release withdrawal; the status machine uses CANCELLED. The record preserves those distinctions and open questions. It does not establish completed migration, current scope, acceptance, or production behavior.

See [[concepts/cashflow-netting-grouping-and-outcomes]] for the existing scheduled-netting topic; its scope does not settle these CN migration questions.

## Canonical sections

- [Workflow and event handling](../../../records/candidates/settlement/KT-settlement-cn-workflow.md#workflow-and-event-handling)
- [Dated demo expectations](../../../records/candidates/settlement/KT-settlement-cn-workflow.md#dated-demo-expectations)
- [Operations discussion](../../../records/candidates/settlement/KT-settlement-cn-workflow.md#operations-discussion)
- [Migration reconciliation and proposed controls](../../../records/candidates/settlement/KT-settlement-cn-workflow.md#migration-reconciliation-and-proposed-controls)
- [Concrete lifecycle conflict](../../../records/candidates/settlement/KT-settlement-cn-workflow.md#concrete-lifecycle-conflict)


## Related candidate topics

- [[summaries/KT-ratan-trade-migration-controls]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
