---
type: Summary
description: "Summarizes selected trade-control expansion requests for FXO, C&A/Falcon, option expiry, detective rules, and scoped null-entity display."
doc_type: short
full_text: sources/KT-ratan-trade-control-expansion-intent.md
---

> **Candidate/draft only:** These dated requests do not establish live control behavior, complete retry handling, or broad access rights.

# RATAN Trade Control Expansion Requests

The June 2026 FXO request covers UK trade tickets and contract validation, including netted trades, with manual exceptions and validation. A separate C&A request covers several producer systems and proposes Falcon API retries, but its technical-error inventory and recovery ownership remain incomplete. Three retries apply only to selected codes; business/data-quality cases alert Ops.

The September option-expiry request asks for cut-level rate display, an exception when multiple rates exist for one pair and cut, and validation of generated spot tickets. The source does not define the authoritative rate, tolerance, timezone, or permission rule.

An undated checklist proposes real-time detective-rule integration with Apollo; dates and manual recovery are placeholders. A separate bug request asks to display null-booking-entity trades for a GBS India user. That bounded display request grants no unrestricted access. No source proves implementation or acceptance.

## Canonical sections

- [FXO manual validation](../../../records/candidates/operations/KT-ratan-trade-control-expansion-intent.md#fxo-manual-validation)
- [C&A and Falcon scope](../../../records/candidates/operations/KT-ratan-trade-control-expansion-intent.md#ca-and-falcon-scope)
- [Option expiry rate controls](../../../records/candidates/operations/KT-ratan-trade-control-expansion-intent.md#option-expiry-rate-controls)
- [Detective-rule orchestration draft](../../../records/candidates/operations/KT-ratan-trade-control-expansion-intent.md#detective-rule-orchestration-draft)
- [Null booking-entity display request](../../../records/candidates/operations/KT-ratan-trade-control-expansion-intent.md#null-booking-entity-display-request)


## Related candidate topics

- [[summaries/KT-ratan-data-entitlement-and-access]]
- [[summaries/KT-ratan-settlement-integration-checklist-scope]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
