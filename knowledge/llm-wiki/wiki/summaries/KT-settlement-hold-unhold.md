---
type: Summary
description: "Summarizes candidate cashflow hold, separate-user unhold, profile limits, and lifecycle conflicts."
doc_type: short
full_text: sources/KT-settlement-hold-unhold.md
---

# Cashflow hold and unhold

> **Source status:** Candidate/draft. These selected designs do not establish current eligibility or authorization.

The design places a cashflow in HOLD with a pending-verification exception and proposes restoring the prior state on unhold. A different user must unhold; named legacy profiles and a USD profile limit apply. The cashflow amount must be below the user profile limit in the selected text, so equality behavior remains open. These profile labels do not map to CES roles here. [WF-CF-025](../../../records/candidates/settlement/KT-settlement-hold-unhold.md#wf-cf-025) [WF-CF-026](../../../records/candidates/settlement/KT-settlement-hold-unhold.md#wf-cf-026) [WF-CF-027](../../../records/candidates/settlement/KT-settlement-hold-unhold.md#wf-cf-027)

Hold is described as suspending materialization, exception checks, and SSI stamping, yet a separate table permits explicit Adhoc SSI, net/un-net, suppression, and unhold actions. Its broader pre-release scope also conflicts with a narrower leading blotter matrix. The amendment example retains HOLD on the new cashflow. A direct withdrawal cancels the withdrawal version and makes the prior New inactive, while FAILED ends unhold eligibility. [Processing suspension and version scenarios](../../../records/candidates/settlement/KT-settlement-hold-unhold.md#processing-suspension-and-version-scenarios)

Current state scope, post-HOLD action precedence, amendment handling, and authorization need confirmation. See [[summaries/KT-settlement-cashflow-blotter-actions]] and proposed [[summaries/KT-settlement-multi-exception-control]].
