---
type: Summary
description: Summarizes Korea Murex COMP proposals for the RATAN payment confirmation gate.
doc_type: short
full_text: sources/KT-settlement-korea-trade-confirmation.md
---

> Derived from [candidate record version 1](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md). Owner review and publication remain pending.

# Korea Murex COMP and settlement confirmation

The candidate covers Korea Murex trade COMP as a proposed input to the RATAN payment STP gate. The remaining tactical proposal sends MXML over IBM MQ. The source set also records rejected transport options. [Confirmation gate](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#confirmation-gate) [Transport options](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#transport-options).

Trade and version matching, duplicate and late messages, acknowledgements, replay, and the strategic switch criteria remain open. The shared RATAN interface page also covers ENISIS payment transport and recovery, which this candidate does not review. [Mapping and message retention](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#mapping-and-retained-message) [Scope limit](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#connections) [Open questions](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#open-questions).

The candidate records no approved transport, deployment, or execution evidence.

## Related topics

- [[summaries/KT-settlement-payment-amount-adjustment|Korea payment amount adjustment]] records a separate set of migration decisions.
- [[summaries/KT-settlement-group-blotter-controls|Group Blotter controls]] covers downstream cashflow selection and processing predicates.

## Cancellation and diagnostic boundaries

For an unconfirmed original trade, the recorded cancel-and-reissue answer cancels the old cashflow. The replacement waits for its own COMP. The mapping copies MXML validation level COMP to SCBML substate and validation action to transaction type. The missing-confirmation procedure searches RATAN for received COMP. An empty search result establishes no received COMP in that search scope. It supplies no current transport or execution proof. [Confirmation gate](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#confirmation-gate). [Mapping and diagnosis](../../../records/candidates/settlement/KT-settlement-korea-trade-confirmation.md#mapping-and-retained-message).
