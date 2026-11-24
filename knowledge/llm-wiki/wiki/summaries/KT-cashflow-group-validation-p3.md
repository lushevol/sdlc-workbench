---
type: Summary
description: "Summarizes proposed cashflow-group completeness, ordered release, amendment pairing, and producer-specific trade validation."
doc_type: short
full_text: sources/KT-cashflow-group-validation-p3.md
---

> **Candidate/draft only:** Grouping and validation examples are design statements; no current configuration or execution is established.

# Cashflow Group Validation P3

The group design combines trade ID, major version, and declared event count. Processing waits for all expected messages and for earlier major-version groups. Group and message states distinguish arrival, dependency, readiness, withdrawal, delivery, and completion. Missing group-flag behavior conflicts between a module row and nested consumer wording.

Withdrawal/New pairs are treated as amendments. Non-economic pairing compares booking entity, counterparty, currency, amount, value date, and direction, with opposite New/Withdrawal events; other amendments are economic. The June 2024 enhancement routes selected non-economic changes through workflow when the replaced payment is PROJECTED or QUEUED.

Validation differs by producer: FMRP uses trade ID, major version, and stated validation statuses; Murex uses trade ID with VALD or COMP. SCBML and Uber have separate completeness and validation paths. Manual delivery of incomplete groups has no defined grant or recovery rule. H1/H2 dates and scenario rows are not passing execution evidence.

## Canonical sections

- [Grouping and ordered release](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#grouping-and-ordered-release)
- [Amendment and non-economic pairing](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#amendment-and-non-economic-pairing)
- [Trade validation gate](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#trade-validation-gate)
- [L3-GROUP-01 — Producer-specific validation and completeness](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#l3-group-01--producer-specific-validation-and-completeness)
- [L3-GROUP-02 — Group ordering and search identity](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#l3-group-02--group-ordering-and-search-identity)


## Related candidate topics

- [[summaries/KT-settlement-non-economic-amendments]]
- [[summaries/KT-settlement-event-sequencing]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.

## Historical scenario and validation boundaries

H1/H2 examples use MxSystemDate <= VD <= MxSystemDate +9. Partial arrivals wait for component completeness. The cancellation example counts the cancelled component and sends force-complete. Conflicting dates and weekday labels remain unresolved. [Canonical detail](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#h1-and-h2-selected-scenario-catalog)

The POC expects failed netting synchronization to block unnet synchronization. Exception replay closes the netting exception and returns its record to IN_PROGRESS. Successful netting acknowledgement then triggers unnet synchronization. These are expected assertions, with execution unverified. [Canonical detail](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#non-economic-amendment-poc-expectation-catalog)

Withdrawal completion drives New-event STP after the source-specific cancellation, Nostro-matching, or netted-matching conditions. COMPLETED and PENDING_WITHDRAWAL trigger attempts on later PENDING_PRE_GROUP groups. OFFSET scope differs between the grouping and validation documents. Checker-only Manual STP remains an option; unvalidated-trade gating still disables Manual STP. [Canonical detail](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#historical-amendment-release-and-service-responsibilities)

Trade-status sourcing uses TDS3 for FMRP and Murex. CDUPS dependency is limited to FX SWAP near-leg confirmation with TBD qualification. Incomplete groups remain PENDING; complete unvalidated groups remain PENDING_TRADE_VALIDATION. Linkage, LIEN effects, and accepted applicability remain unresolved. [Canonical detail](../../../records/candidates/settlement/KT-cashflow-group-validation-p3.md#historical-trade-status-sourcing-and-validation-scope)
