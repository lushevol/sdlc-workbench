---
type: Summary
description: "Summarizes candidate settlement service boundaries, orchestration, persistence, audit, and shared-infrastructure proposals."
doc_type: short
full_text: sources/ARC-settlement-platform-p3.md
---

# Settlement platform P3

> **Source status:** Candidate/draft from historical architecture material. It does not establish current service boundaries or implementation.

The design assigns lifecycle, group management, rules, netting, SSI, query, and Camunda orchestration separate responsibilities. Camunda coordinates STP, multi-exception review, and technical failures; lifecycle owns status and history changes. Several features are marked future scope, which does not establish their current absence. [Strategic service responsibilities](../../../records/candidates/architecture/ARC-settlement-platform-p3.md#strategic-service-responsibilities)

Persistence proposals separate PostgreSQL schemas by domain and list payment, workflow, SSI, exception, audit, and history data. Retention is stated for only selected records; other durations are blank. The design requires replication and real-time consistency without measurable bounds. These table assignments are not a verified database inventory. [Persistence and audit boundaries](../../../records/candidates/architecture/ARC-settlement-platform-p3.md#persistence-and-audit-boundaries)

Co-development notes describe shared Kafka, Redis, ELK, PostgreSQL, foundation services, and CI/CD, but retain alternative clusters and unresolved operations. The system inventory leaves some responsibility cells blank. No architecture choice, retention contract, deployment, or execution was verified. [Shared infrastructure agreement and limits](../../../records/candidates/architecture/ARC-settlement-platform-p3.md#shared-infrastructure-agreement-and-limits)

See proposed [[summaries/ARC-platform-cashflow-data-query]].
