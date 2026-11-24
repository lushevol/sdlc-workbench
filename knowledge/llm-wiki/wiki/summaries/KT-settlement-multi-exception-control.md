---
type: Summary
description: "Summarizes candidate multi-exception review and bulk-processing conditions, limits, and open conflicts."
doc_type: short
full_text: sources/KT-settlement-multi-exception-control.md
---

# Multi-exception and bulk processing controls

> **Source status:** Candidate/draft. Most material is documented design or expected scenarios, not verified current behavior.

Bulk submit or approval proposals require at least two cashflows with matching waiting exceptions and shared entity, counterparty, and value date. Preview excludes self-submitted checker items, ineligible exceptions, unauthorized high-risk cases, and amounts above checker limits. Eligibility is configurable per rule, and preview is expected to reevaluate current rules before partial selection. [WF-CF-045](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#wf-cf-045) [WF-CF-046](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#wf-cf-046) [WF-CF-049](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#wf-cf-049)

Other proposals define conditional High Value and Pending Affirmation exceptions, independent SSI/date corrections, backend revalidation, and preservation of resolved sections after rejection. These do not provide a universal exception catalogue or current permission export. [WF-CF-052](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#wf-cf-052) [WF-CF-054](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#wf-cf-054) [WF-CF-057](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#wf-cf-057)

The scenario sheet marks execution `NOT_RUN`. It does not verify partial success or real-time refresh. Mixed-key selection may either disable the action or report an error after selection. A Maker-only exception also conflicts with the stated High Value checker condition. Bad Business Day ownership and accepted affirmation statuses need owner review. [WF-CF-050](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#wf-cf-050) [Additional exception predicates and correction limits](../../../records/candidates/settlement/KT-settlement-multi-exception-control.md#additional-exception-predicates-and-correction-limits)

Related proposed pages: [[summaries/KT-settlement-cashflow-blotter-actions]] and [[summaries/KT-settlement-cashflow-blotter-actions]].
