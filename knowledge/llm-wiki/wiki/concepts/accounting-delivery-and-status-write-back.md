---
type: Concept
description: "Connects destination accounting milestones, producer updates, version correlation, and unresolved payment-amount contracts."
sources: ["summaries/INT-KT-payment-accounting-contracts.md", "summaries/INT-KT-ratan-cashflow-settlement-interfaces.md", "summaries/KT-settlement-cashflow-identity-and-stella-write-back.md", "summaries/INT-KT-murex-ratan-feed-lifecycle.md", "summaries/KT-settlement-payment-amount-adjustment.md"]
---

# Accounting delivery and status write-back

> Derived from candidate/draft canonical records. Current authority, implementation, execution, and publication remain unconfirmed.

## Destination-specific milestones

[[entities/cash-settlement-ratan]] has separate Aspire, eBBS, and Korea OLTP accounting proposals. Aspire SUCCESS means sent to Aspire. eBBS SUCCESS requires consumption and ACK. Korea OLTP SUCCESS requires OLTP ACK, while EDMI acknowledgement has a different boundary. A common status label therefore requires its destination contract. [Aspire lifecycle](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-02--aspire-accounting-lifecycle). [eBBS statuses](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-06--ebbs-statuses-retries-and-alerts). [OLTP acknowledgements](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-09--korea-oltp-acknowledgements-and-recovery)

The interim Korea TLM query selects accounting requests with task-history status SENT and a maximum span of three days. Its returned business states include SUCCESS, SENT, and REJECTED. That task-history filter and those response states describe different fields. Future OLTP→Aspire→TLM delivery remains a proposal. [Interim TLM query](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-07--korea-interim-tlm-query)

## Version, reversal, and retry scope

The eBBS proposal checks for earlier RELEASED accounting before generating SETTLED accounting. Matching cashflow ID, event, and business version prevent duplication. Component withdrawal can reverse a released resultant entry under specified SWIFT_SUPPRESSED or FAILED conditions. Selection among multiple resultant versions remains undefined. [eBBS eligibility](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-04--ebbs-dated-eligibility-and-timing). [Withdrawal accounting](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-05--ebbs-reversal-and-component-withdrawal)

eBBS retry rows differ between three auto-resends and at least three technical attempts spaced three minutes apart. Korea's dated answer requests no automatic retry. These source-specific rules require environment and authorization confirmation. [eBBS recovery](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-06--ebbs-statuses-retries-and-alerts). [Korea recovery](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-09--korea-oltp-acknowledgements-and-recovery)

## Producer-status write-back

[[entities/stella]] FX matching and lifecycle updates have separate trigger and acknowledgement proposals. Currency matching conflicts with a later removal request. Concurrent amendment/release or amendment/netting can reject version-based write-back. The regional [[entities/murex]] adaptor synchronizes RATAN RELEASED and excludes SETTLED, while operational monitor labels conflict. These contracts require producer-specific event and version correlation. [Stella FX matching](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#fx-status-write-back). [Stella lifecycle](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#stella-lifecycle-and-acknowledgement). [Murex acknowledgement and status](../../../records/candidates/settlement/INT-KT-murex-ratan-feed-lifecycle.md#status-acknowledgement-and-manual-recovery)

## Payment amount and accounting scope

Day 2 amount adjustment applies updated amounts to SWIFT and accounting. The Korea variant applies adjusted amounts to payment and LMS while retaining original accounting amounts. Their flow, entity, effective date, state, and reconciliation contracts remain unresolved. [[concepts/netting-types-and-resultants]] links the affected component/resultant context. [Day 2 variant](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#day-2-manual-rounding). [Korea amount responsibility](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#maker-checker-and-amount-responsibility). [Variant limits](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#evidence-limits)

## Retrieval and authority

Use [[summaries/INT-KT-payment-accounting-contracts]] for destination eligibility and recovery. Use [[summaries/KT-settlement-cashflow-identity-and-stella-write-back]] for producer matching and acknowledgement. The broader [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]] retains geography and transport alternatives. Current owners, approved revisions, external acceptance, and executed recovery remain unconfirmed. [Accounting evidence limits](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#evidence-limits). [Interface questions](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#open-questions)
