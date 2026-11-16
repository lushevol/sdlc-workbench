---
type: Summary
description: "Summarizes candidate high-value payment scope, profile limits, STP metadata, and outbound service proposals."
doc_type: short
full_text: sources/KT-day2-high-value-payment-control.md
---

# High-value payment authorization and outbound control intent

> **Source status:** Candidate/draft. Profile assignment and service behavior have not been verified.

The proposal covers BCS, LOANIQ, and FMRP, while excluding Korea ENISIS. USD display/filter changes target FMRP and LOANIQ; BCS retains its existing authorization-limit process. FMRP affirmation retains two alternatives. A named BOS limit is below USD 500 million, while other checker profiles have separate thresholds; current assignments remain unverified. [HVP-01](../../../records/candidates/security/KT-day2-high-value-payment-control.md#hvp-01--scope-amount-display-and-approval-limits)

The proposed `stpFlag` is Y for STP and N for NSTP. Every manual action except Add Comment makes the flow NSTP. Add Comment does not establish an NSTP-to-STP reset. The `lastUser` tables contain blank user fields. Split children inherit parent STP/NSTP information; BCS net resultants lack a defined user identity. The source alternates FMID, PSID, and bank ID labels without defining their mapping. [HVP-02](../../../records/candidates/security/KT-day2-high-value-payment-control.md#hvp-02--stp-flag-and-last-user-contract)

The architecture proposal has Orchestration retrieve lifecycle metadata, add outbound headers, and route LOANIQ and FMRP through different transports. Netting responsibility is not supplied in the selected section. [HVP-03](../../../records/candidates/security/KT-day2-high-value-payment-control.md#hvp-03--proposed-service-responsibilities)

Confirm scope, thresholds, actor identity, and service boundaries. See [[summaries/KT-settlement-profile-authorization-limits]] and proposed [[summaries/KT-settlement-multi-exception-control]].
