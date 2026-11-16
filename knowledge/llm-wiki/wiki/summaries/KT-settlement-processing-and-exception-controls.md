---
type: Summary
description: "Collects historical settlement exception, suppression, precheck, acknowledgement, and last-mile control descriptions."
doc_type: short
full_text: sources/KT-settlement-processing-and-exception-controls.md
---

> **Candidate/draft only:** These historical control descriptions do not establish current approved operating behavior.

# Settlement Processing and Exception Controls

The selected NSTP design describes exception-specific maker, checker, authority-limit, and auto-resolution rules. Rejected SSI input preserves maker values, and previously netted cashflows require an approver distinct from the unnetting user. A historical table names extra handling above USD 100 million. These limits are source-specific.

Cashflow suppression removes payment and accounting; payment or Swift suppression retains accounting. Manual suppression uses maker-checker, and historical unsuppression stops at value date. Released or settled items cannot be manually failed. The selected China status table distinguishes FMSRE acknowledgement as Released from AMH/SCPAY acknowledgement as Settled, and keeps BCS/Egypt on a separate model.

Precheck uses currency calendars, active versions, and cutoffs. READY cashflows with no substatus wait for release cutoff before payment generation through the FM Swift Gateway. IRS count checks and pending-fixing flags are also described. Last-mile checks block previous sends and matching economics, but the example and query differ on trade identity. None of these statements verifies live configuration or execution.

## Canonical sections

- [Maker-checker exception handling](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#maker-checker-exception-handling)
- [Suppression and failure boundaries](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#suppression-and-failure-boundaries)
- [China status and acknowledgement model](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#china-status-and-acknowledgement-model)
- [Precheck and payment generation intent](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#precheck-and-payment-generation-intent)
- [Stamping and last-mile controls](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#stamping-and-last-mile-controls)


## Related candidate topics

- [[summaries/KT-platform-cashflow-processing-contracts]]
- [[summaries/INT-KT-cashflow-amendment-and-release-controls]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
