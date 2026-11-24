---
type: Summary
description: "Preserves alternative Uber migration, lifecycle ownership, caller compatibility, and mixed-history transaction proposals."
doc_type: short
full_text: sources/KT-platform-uber-migration-contracts.md
---

> **Candidate/draft only:** The selected design alternatives are historical proposals. Owner is unknown; `verified` is empty.

# Platform Uber migration contracts

The selected designs retain several integration alternatives: common strategic JSON, isolated JSON and SCBML workflows, and incremental SCBML bridging. They do not approve one migration route. Proposed responsibility boundaries divide standardization, lifecycle status and persistence, and workflow routing. A separate 2.0 proposal moves stamping and cutoff decisions among services; the source set does not reconcile every boundary.

The documents call for existing callers to retain required API and observable behavior. They identify mixed-history routing, SSI refresh, and process-in publication as open contract areas. Transactional netting and component updates, persistence order, precheck failure, and SWIFT-status consistency remain proposals. The plan includes compatibility rehearsals and coordination, without retained execution evidence.

The active [[summaries/KT-day2-auto-netting-service-design]] describes related service boundaries and API proposals. The [[summaries/KT-settlement-cashflow-identity-and-stella-write-back]] page covers separate identity and write-back questions. Neither selects this migration or proves caller compatibility.

## Canonical sections

- [Compatible integration alternatives](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#compatible-integration-alternatives)
- [Existing caller and action consistency](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#existing-caller-and-action-consistency)
- [Mixed-history routing remains proposed](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#mixed-history-routing-remains-proposed)
- [Lifecycle transaction and workflow proposal](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#lifecycle-transaction-and-workflow-proposal)
