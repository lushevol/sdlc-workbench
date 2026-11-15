---
type: "Summary"
description: "Covers proposed reversal and rebook exceptions and the missing cashflow link after amendment."
doc_type: short
full_text: "sources/KT-settlement-amendment-reversal-rebook-exceptions.md"
---

> Derived from [candidate record version 1](../../../records/candidates/settlement/KT-settlement-amendment-reversal-rebook-exceptions.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Released amendment reversal and rebook exceptions

The selected design covers an amendment after the original cashflow has been released from RATAN. It calls for additional operations validation before releasing the withdrawal and replacement. It proposes a reversal exception for the withdrawal and a rebook exception for the new cashflow. [Candidate claims](../../../records/candidates/settlement/KT-settlement-amendment-reversal-rebook-exceptions.md#documented-knowledge)

The source says there is no direct link between the original and replacement cashflows. It therefore cannot reliably identify amendment-driven new cashflows for rebook exception generation. Adding direction to query criteria and considering a trade event after Uber is enabled remain proposed alternatives. The candidate does not select an accepted implementation path.

## Related topics

- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity]] covers source IDs and versioning.
- [[summaries/KT-settlement-cpn-netting|CPN netting]] covers separate released-resultant reversal scenarios.
- [[summaries/KT-settlement-auto-netting|Auto-netting]] and [[summaries/KT-settlement-payment-amount-adjustment|Payment adjustment]] provide related context.

The source does not define the binding event and identifier, exception states, or owner. Approval, implementation, and deployment remain unverified. See the candidate's [evidence limits](../../../records/candidates/settlement/KT-settlement-amendment-reversal-rebook-exceptions.md#evidence-limits) and [open questions](../../../records/candidates/settlement/KT-settlement-amendment-reversal-rebook-exceptions.md#open-questions).
