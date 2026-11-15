---
type: "Summary"
description: "Summarizes proposed Cash Settlement lifecycle and netting services, APIs, persistence, and rule mappings."
doc_type: short
full_text: "sources/KT-day2-auto-netting-service-design.md"
---

> Derived from [candidate record version 1](../../../records/candidates/architecture/KT-day2-auto-netting-service-design.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Auto-netting service and rule lifecycle

## Service boundaries

The selected refactor designs assign cashflow initialization and lifecycle status changes to a lifecycle service. They assign netting, un-netting, rule checks, component status, and renetting to a netting service. These are proposed boundaries, not a verified deployed architecture. [Candidate claims](../../../records/candidates/architecture/KT-day2-auto-netting-service-design.md#documented-knowledge)

## APIs and persistence proposals

The technical design proposes a scheduled job endpoint and a rule-check endpoint. The rule-check response distinguishes matched from unmatched rules. Its persistence tables cover rule identity, grouping, execution status, and resultant mappings. [Candidate claims](../../../records/candidates/architecture/KT-day2-auto-netting-service-design.md#documented-knowledge)

## Rule event mapping

The selected mapping lists event, stored status, frontend action, and rule action values for create, update, enable, disable, and delete operations. Several action cells remain blank. The candidate preserves these blanks and leaves their meaning unresolved; it does not treat them as approved no-ops. [Rule mapping and evidence limits](../../../records/candidates/architecture/KT-day2-auto-netting-service-design.md#documented-knowledge) [Open questions](../../../records/candidates/architecture/KT-day2-auto-netting-service-design.md#open-questions)

The proposed ordering of status changes and resultant generation also remains unresolved. The sources do not establish current approval, implementation, deployment, or execution.

## Related topics

- [[summaries/KT-settlement-auto-netting|Scheduled Cash Settlement auto-netting]] covers rule selection and scheduled outcomes.
- [[concepts/auto-netting-rule-selection]] and [[concepts/auto-netting-scheduling]] provide related context.

The candidate owner is unknown. Review its [evidence limits](../../../records/candidates/architecture/KT-day2-auto-netting-service-design.md#evidence-limits) and [open questions](../../../records/candidates/architecture/KT-day2-auto-netting-service-design.md#open-questions) before relying on the proposal.
