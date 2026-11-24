---
type: Summary
description: "Summarizes candidate external cashflow query, entitlement, transport, field, and SSI-usage data contracts."
doc_type: short
full_text: sources/ARC-platform-cashflow-data-exposure.md
---

# Platform cashflow data exposure

> **Source status:** Candidate/draft. Interfaces, capacity phases, and transport choices are proposals without runtime evidence.

The data-provider design accepts a SQL-shaped query and distinguishes invalid SQL, unsupported fields, entitlement failures, and busy or oversized requests. Its phases use different error codes; no safe query grammar or final error contract is selected. Caller headers combine FMAA identity with Bank-Id/Country routing, but this source supplies no current authorization proof. [External data access contract](../../../records/candidates/architecture/ARC-platform-cashflow-data-exposure.md#external-data-access-contract) [Caller and entitlement boundary](../../../records/candidates/architecture/ARC-platform-cashflow-data-exposure.md#caller-and-entitlement-boundary)

Capacity phases range from below 100,000 records to million-record scale, but these are objectives rather than measured guarantees. The preferred large-volume design streams repeated query slices; concurrency, stable ordering, refresh, and retention remain open. [Phased capacity and storage alternatives](../../../records/candidates/architecture/ARC-platform-cashflow-data-exposure.md#phased-capacity-and-storage-alternatives) [Large-volume transport design](../../../records/candidates/architecture/ARC-platform-cashflow-data-exposure.md#large-volume-transport-design)

The field catalog defines cashflow/version and withdrawal-link semantics, while some field types remain unresolved. Position_Id carries an explicit do-not-use restriction pending modeling-team contact. A dormant SSI-usage proposal supplies daily updates to SSI+ and a 24-month inactivity rule, without defining last-use calculation or day boundary. [Exposed business field semantics](../../../records/candidates/architecture/ARC-platform-cashflow-data-exposure.md#exposed-business-field-semantics) [Dormant SSI usage feed](../../../records/candidates/architecture/ARC-platform-cashflow-data-exposure.md#dormant-ssi-usage-feed)

See proposed [[summaries/ARC-platform-cashflow-data-query]].
