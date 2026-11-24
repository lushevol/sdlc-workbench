---
type: Summary
description: "Summarizes a deprecated Indonesia gateway consolidation option and a separate gateway resilience proposal."
doc_type: short
full_text: sources/INT-KT-regional-gateway-design-alternatives.md
---

# Regional gateway design alternatives

> **Source status:** Candidate/draft. One option is explicitly deprecated; approval and execution evidence for the resilience design remain unestablished.

The deprecated proposal combines gateway and authorization server for Indonesia and lists older entitlement, token, and Entra/FMAA alternatives. Its Q3 2026 decommission date is a plan, not completion evidence. Its expansion of FMAA is source-specific and should not be merged with other authentication terminology. This historical option does not supersede later migration direction. [GW-01](../../../records/candidates/settlement/INT-KT-regional-gateway-design-alternatives.md#gw-01--deprecated-consolidation-alternative)

A separate resilience proposal uses configurable rate-limit keys and per-route circuit breakers with fallback response metadata. `deny-empty-key` can be permissive or strict; no choice is selected. Environment-specific threshold tuning remains proposed without accepted values. The source lists proposed timeout, 5xx, recovery, and fallback tests without any results. [GW-02](../../../records/candidates/settlement/INT-KT-regional-gateway-design-alternatives.md#gw-02--gateway-resilience-upgrade-proposal)

No gateway topology, error payload, rate-limit policy, or test result is approved here. The deprecated option remains historical context only. See [[summaries/KT-sdk-and-entitlements]] and proposed [[summaries/INT-KT-indonesia-regional-architecture]].
