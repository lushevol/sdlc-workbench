---
type: Summary
description: "Keeps Aspire, eBBS, Korea OLTP, interim TLM, and accounting API proposals separate by destination and milestone."
doc_type: short
full_text: sources/INT-KT-payment-accounting-contracts.md
---

> **Candidate/draft only:** Destination contracts, effective dates, current routes, and operating evidence remain unresolved.

# Payment Accounting Contracts by Destination and Milestone

The record separates accounting proposals for Aspire files, eBBS real-time messages, Korea OLTP, and an interim TLM query. Aspire describes weekday EOD files and lifecycle reversals; eBBS describes value-date timing, ACK-based status, retries, and dashboard behavior. Korea OLTP has separate account eligibility, acknowledgements, recovery ownership, and a 2026 no-automatic-retry answer. Those differences must not be collapsed into one accounting contract.

The routing sources also disagree by milestone. One matrix moves Hong Kong Main Nostro to eBBS after Keystone while Hong Kong Suspense, Taiwan, and Thailand stay with Aspire. A separate accounting overview adds Jersey to the Aspire route. No effective date reconciles the alternatives.

The BAU handover documents two accounting-job APIs and current-versus-previous response-schema alternatives. Their current version and invocation authority are unknown. Withdrawal reversal predicates also conflict between “previous event sent” and released-only wording. The selected statements describe intent and historical proposals, not deployed behavior or successful postings.

## Canonical sections

- [INT-ACC-01 — Aspire scope and daily files](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-01--aspire-scope-and-daily-files)
- [INT-ACC-04 — eBBS dated eligibility and timing](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-04--ebbs-dated-eligibility-and-timing)
- [INT-ACC-07 — Korea interim TLM query](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-07--korea-interim-tlm-query)
- [INT-ACC-08 — Korea OLTP payment and account eligibility](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-08--korea-oltp-payment-and-account-eligibility)
- [INT-ACC-API — Accounting-job API contracts](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#int-acc-api--accounting-job-api-contracts)
- [L3-ACC-SUP-02 — Withdrawal predicate conflict](../../../records/candidates/settlement/INT-KT-payment-accounting-contracts.md#l3-acc-sup-02--withdrawal-predicate-conflict)


## Related candidate topics

- [[summaries/KT-settlement-feeds-p3]]
- [[summaries/INT-KT-uk-murex-batch-contract]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
