---
type: Product
description: "Named trade and cashflow snapshot contract with migration, validation, temporal, and recovery proposals."
sources: ["summaries/KT-uber-strategic-cash-settlement-p3.md", "summaries/KT-platform-uber-migration-contracts.md", "summaries/KT-settlement-cashflow-identity-and-stella-write-back.md"]
---

# Uber

> Derived from candidate/draft canonical records. Current authority, implementation, execution, and publication remain unconfirmed.

## Snapshot and retrieval model

The Uber proposal combines trade records, cashflows, fixing notices, and change information in protobuf snapshots. Transactions generate snapshots. The design permits non-atomic events and partial success. Optional asOf/effective queries default to NOW under defined temporal intervals. Timestamp/tracking-ID duplicate checks and missed-final-message monitoring remain design responsibilities. [Snapshot purpose](../../../records/candidates/interoperability/KT-uber-strategic-cash-settlement-p3.md#uber-001-snapshot-and-integration-purpose). [Temporal limits](../../../records/candidates/interoperability/KT-uber-strategic-cash-settlement-p3.md#uber-002-event-and-temporal-limits)

A companion analysis requests complete latest trade, fixing, cashflow, and schedule information. It corrects a business-event identifier request toward trade-tracking and cashflow versions. The exact version contract, sequence rules, and settlement-instruction inclusion remain unresolved. [Completeness and correlation](../../../records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md#proposed-uber-payload-completeness-and-correlation)

## Validation and migration consumers

The March 28 scope names three entity FMIDs. For those entities, a false cashflowCheckResult.passed drops the whole message. Other entities initially use hardcoded true and need additional configuration. This entity-specific gate does not establish universal validation. [Initial entity validation](../../../records/candidates/interoperability/KT-uber-strategic-cash-settlement-p3.md#uber-003-initial-entity-validation)

Standardization, lifecycle, workflow, SSI, and group management have proposed conversion and routing responsibilities. Retained alternatives include common JSON, isolated JSON/SCBML workflows, and incremental bridging. Existing [[entities/murex]] SCBML and historical cashflows need their own compatibility treatment. Mixed-message transactional operations remain unresolved. [Compatible alternatives](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#compatible-integration-alternatives). [Responsibility boundaries](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#migration-responsibility-boundaries). [Mixed-history routing](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#mixed-history-routing-remains-proposed)

## Recovery and compatibility limits

A remediation proposal defaults to five retry attempts, a 15,000-millisecond initial delay, and a multiplier of two. Its DLT path retains inbound, group, and group-message records. A separate query fallback uses three retries. These are different source-described operations. Historical SCBML compatibility and no-impact objectives have no measurable acceptance threshold in the selected objective section. [Persistent retries](../../../records/candidates/interoperability/KT-uber-strategic-cash-settlement-p3.md#uber-008-persistent-retries-and-recovery). [Performance objectives](../../../records/candidates/interoperability/KT-uber-strategic-cash-settlement-p3.md#uber-009-performance-objectives)

## Navigation and authority

[[summaries/KT-uber-strategic-cash-settlement-p3]] retains snapshot and operational proposals. [[summaries/KT-platform-uber-migration-contracts]] retains caller/action consistency and cutover questions. [[entities/cash-settlement-ratan]] supplies the settlement-processing context. Current schema, field filters, owner approval, selected architecture, and execution remain unconfirmed. [Open questions](../../../records/candidates/interoperability/KT-platform-uber-migration-contracts.md#open-questions)
