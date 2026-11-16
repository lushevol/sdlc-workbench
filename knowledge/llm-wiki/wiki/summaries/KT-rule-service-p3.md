---
type: Summary
description: "Summarizes archived NSTP rule governance, domain boundaries, versioned APIs, engine choices, and migration risks."
doc_type: short
full_text: sources/KT-rule-service-p3.md
---

# Rule Service P3

> **Source status:** Candidate/draft drawn from historical and archived proposals; current ownership and applicability remain unresolved.

The NSTP design separates maker/checker rule changes from message evaluation and user resolution. Maker-only and checker-only operations use different initial states; affirmation and back-value changes require double-blind checker verification. The reconstruction proposal routes domain facts through domain services and reserves shared rule service for reusable rule families. [Historical NSTP governance](../../../records/candidates/architecture/KT-rule-service-p3.md#historical-nstp-governance) [Domain fact and rule-engine separation](../../../records/candidates/architecture/KT-rule-service-p3.md#domain-fact-and-rule-engine-separation)

Archived syntax uses AND for ungrouped conditions and OR within groups, with separate rules also related by OR. Versioned APIs distinguish logical-model from additional facts; a batch proposal caps requests at 400. Drools is proposed, but source-rule inventories, adapters, v1 retention, and endpoint retirement are not approved migration facts. [Rule syntax and effective status](../../../records/candidates/architecture/KT-rule-service-p3.md#rule-syntax-and-effective-status) [Rule storage and versioned interfaces](../../../records/candidates/architecture/KT-rule-service-p3.md#rule-storage-and-versioned-interfaces) [Engine selection and migration are proposals](../../../records/candidates/architecture/KT-rule-service-p3.md#engine-selection-and-migration-are-proposals)

Redis/database consistency and failed Kafka publication remain open; an outbox is only suggested for investigation. No implementation or compatibility execution was inspected. See proposed [[summaries/KT-ratan-static-maker-checker-controls]].
