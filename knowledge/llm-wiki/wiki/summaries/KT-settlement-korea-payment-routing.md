---
type: Summary
description: "Summarizes candidate Korea Murex-to-RATAN routing, ENISIS acknowledgements, and TIS payment-query conditions."
doc_type: short
full_text: sources/KT-settlement-korea-payment-routing.md
---

# Korea settlement payment routing

> **Source status:** Candidate/draft. Historical routes and query predicates do not establish current approval or connectivity.

The migration proposal assigns settlement processing to RATAN, SWIFT to ENISIS, real-time accounting to OLTP, instructions to SSI+, and reconciliation support to TLM. A functional checklist prefers country-specific SSI over global-entity/product-specific SSI. [Korea migration responsibilities](../../../records/candidates/settlement/KT-settlement-korea-payment-routing.md#korea-migration-responsibilities)

The ENISIS target replaces a received-MT/SFTP route with payment initiation and FM Solace; MT210 remains MT while other named output uses MX. ACK states distinguish technical acknowledgement, final success, and negative acknowledgement. [ENISIS target transport and acknowledgements](../../../records/candidates/settlement/KT-settlement-korea-payment-routing.md#enisis-target-transport-and-acknowledgements)

The manual TIS query is limited to entity `10036645`, Released or Settled nonreversal NOX cashflows, selected accounts, and requested settlement date. Manual categories must not generate RATAN SWIFT or accounting, and post-release SSI updates are unsupported. This candidate says NOX, while a separate interface candidate contains a different NOS/NOX allowlist; reconcile scope before use. [TIS payment query boundary](../../../records/candidates/settlement/KT-settlement-korea-payment-routing.md#tis-payment-query-boundary) [TIS request and response scope](../../../records/candidates/settlement/KT-settlement-korea-payment-routing.md#tis-request-and-response-scope)

See [[summaries/INT-KT-ratan-reference-and-control-interfaces]] and proposed [[summaries/INT-KT-indonesia-regional-architecture]].
