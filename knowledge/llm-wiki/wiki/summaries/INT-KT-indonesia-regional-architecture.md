---
type: Summary
description: "Summarizes candidate Indonesia regional data, access, integration, UI, and cutover proposals."
doc_type: short
full_text: sources/INT-KT-indonesia-regional-architecture.md
---

# Indonesia regional architecture and access intent

> **Source status:** Candidate/draft. These descriptions do not establish an approved architecture, current configuration, or completed rollout.

The proposal keeps the portal and GBS KL processing while placing scoped local back-office data onshore. It describes Indonesia-only access for Indonesia users, approval for other local-country users, and permitted group-user access. Later solutioning calls for isolation of rules and static data, but the selected GDC adaptor design also mentions database persistence; compatibility remains open. [ID-01](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-01--regional-business-scope) [ID-02](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-02--later-isolation-and-provisioning-choice)

For fixing events, the proposal avoids cross-country NAS and routes GDC batch output through Message Bridge, FM Solace, and Indonesia Kafka. Other proposals use `/idns/` API routing, separate netting/splitting identifiers, and regional tile or drawer filters. A failure table says to show a drawer when its filter mismatches, leaving a fail-open case unresolved. [ID-03](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-03--fixing-flag-delivery-without-cross-country-nas) [ID-05](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-05--api-routing-and-regional-identifiers) [ID-07](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-07--regional-drawer-filtering-proposal)

UI routing, data entitlement, infrastructure handover, and cutover safeguards are distinct proposed scopes. The selected release row includes suppression and truncation steps; it grants no execution authority and its date lacks a year. [ID-09](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-09--regional-ui-behavior) [ID-11](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-11--uat-reporting-and-data-entitlement-intent) [ID-13](../../../records/candidates/settlement/INT-KT-indonesia-regional-architecture.md#id-13--planned-cutover-safeguards)

Related context: [[entities/ces]] and [[concepts/portal-entry-and-tile-authorization]]. See proposed [[summaries/KT-day2-manual-entity-settlement]].
