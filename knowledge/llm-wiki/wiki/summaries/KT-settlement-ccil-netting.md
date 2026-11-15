---
type: Summary
description: Documents CCIL workflow proposals, dated IRS examples, and unresolved rule conflicts.
doc_type: short
full_text: sources/KT-settlement-ccil-netting.md
---

> Derived from [India CCIL netting, version 1](../../../records/candidates/settlement/KT-settlement-ccil-netting.md), candidate/draft. Owner review and publication approval remain pending. [Source bindings](../../source-manifest.json).

# India CCIL Netting

## Scope

This draft covers guaranteed and non-guaranteed CCIL workflows, tactical stamping, and staged IRS netting. Its proposals do not establish current production behavior.

## Documented proposals

- **Workflow:** The requirement targets a central-counterparty resultant, suppresses SWIFT generation, and retains accounting. A dated scenario later expects manual SWIFT suppression. Confirm handling for each flow. [NET-M-021](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-021)
- **Routing:** A tactical matrix routes CCIL flows with FMID `400021949` to bilateral netting. Other counterparties use the CCIL action. Generic bilateral rows use a different settlement method. These predicates apply to that matrix only. [NET-M-023](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-023)
- **Operations and onboarding:** Examples describe discrepancy review, MO novation, and four-eye gross exceptions. A historical onboarding flow uses a CR or temporary NSTP hold. Its lead times do not authorize current releases. [NET-M-024](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-024) [NET-M-025](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-025)
- **Staged IRS:** June and August 2026 examples route IRS resultants into Pending Auto Netting. A later scheduled pass marks intermediate resultants DEAD and creates a gross resultant. The examples do not establish current scope or settlement-method inheritance. [NET-M-026](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-026)
- **Tactical mapping:** The functional proposal uses family `IRD` and group `IRS`; the technical design reverses these values. The tactical mapping also proposes CASH fields, `QUEUED`, and Unaffirmed, while scenarios expect NETTED components and an affirmed resultant. The owner must reconcile these outcomes. [NET-M-027](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-027) [NET-M-028](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-028) [NET-M-029](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-029)
- **Lookup failure:** The Stella design maps lookup exceptions to settlement `UNKNOWN`, then maps `UNKNOWN` to `TechFail`. No retry policy, implementation, or deployed configuration was inspected. [NET-M-030](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-030)

## Unresolved cross-source conflicts

The general backend proposal requires matching counterparty FMIDs. The CCIL technical proposal allows different counterparties. It defines no exception or precedence. [NET-M-031](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-031)

The general GUI, backend, CCIL matrix, and Cashflow Blotter proposals list different status gates. They do not establish one governing predicate or processing order. [NET-M-032](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#net-m-032)

## Open questions and evidence limits

Owner review must resolve SWIFT handling, client-list ownership, onboarding controls, counterparty and status gates, staged IRS scope, resultant fields, scenario corrections, and lookup recovery. The full questions remain in the [canonical draft](../../../records/candidates/settlement/KT-settlement-ccil-netting.md#open-questions).

The candidate uses reviewed selected views. Missing images, populated static tables, and external stories remain unavailable. Scenario sheets give expected behavior, not executed assertions. Source dates alone establish neither authority nor supersession.

## Related topics

- [[summaries/KT-settlement-auto-netting|Scheduled auto-netting]] covers the separate scheduled workflow and its unresolved rules.
- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity and Stella]] covers resultant identity and downstream status proposals.
- [[summaries/KT-settlement-group-blotter-controls|Group Blotter controls]] records related action-eligibility and processing proposals.
