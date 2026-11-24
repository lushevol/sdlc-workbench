---
type: Summary
description: "Summarizes candidate static-configuration onboarding, maker-checker APIs, versioning, and frontend freshness proposals."
doc_type: short
full_text: sources/KT-static-config-governance-p3.md
---

# Static configuration governance P3

> **Source status:** Candidate/draft. Alternatives and interface sketches do not establish an adopted architecture or production behavior.

The onboarding objective is UI-based branch/entity changes without production code deployment. Proposals compare service-owned stores, an aggregated static-data service, spreadsheet imports, and optional configuration-server use. Scope includes entity, currency, rounding, BIC, accounting, cutoff, and orchestration values, but no final architecture is selected. [Self-service onboarding objective](../../../records/candidates/operations/KT-static-config-governance-p3.md#self-service-onboarding-objective) [Alternative onboarding responsibilities](../../../records/candidates/operations/KT-static-config-governance-p3.md#alternative-onboarding-responsibilities)

Maker requests, checker actions, effective configuration, and audit snapshots are separated in some proposals; other versions use unified JSON or metadata-driven tables. A shared `/v1/static/config/{target_table}` API and versioned generic configuration schema are drafts. [Configuration management and audit intent](../../../records/candidates/operations/KT-static-config-governance-p3.md#configuration-management-and-audit-intent) [Proposed shared management interface](../../../records/candidates/operations/KT-static-config-governance-p3.md#proposed-shared-management-interface) [Versioned generic configuration draft](../../../records/candidates/operations/KT-static-config-governance-p3.md#versioned-generic-configuration-draft)

The cache-first frontend mode returns cached values while requesting updates. Without cache, dependent components wait. Normal mode depends on the latest configuration. Backend cache behavior and real-time subscriptions remain incomplete. Consumer freshness and rollback boundaries remain open. See proposed [[summaries/KT-rule-service-p3]].

## Draft field and workflow boundaries

The generic draft separates configuration, content, and audit fields, mandatory columns, and state catalogs. Content keys are unique within context. Version types differ between tables. The operator schema says string, while examples show arrays. These differences remain unresolved. [Canonical detail](../../../records/candidates/operations/KT-static-config-governance-p3.md#versioned-generic-configuration-field-contracts)

Onboarding options retain service-owned stores, aggregated Kafka distribution, and spreadsheet import with separate destination schemas. Remaining application.yml values require hot-update handling. No alternative establishes a selected architecture or approved entity inventory. [Canonical detail](../../../records/candidates/operations/KT-static-config-governance-p3.md#historical-self-service-onboarding-option-details)

While a maker update awaits checker approval, fetch returns previous effective configuration. Request and effective records remain separate proposals. Maker cancel and checker reject wording differs from checker confirm/cancel requirements. The HTTP action catalog grants no current permissions. [Canonical detail](../../../records/candidates/operations/KT-static-config-governance-p3.md#shared-maker-checker-workflow-and-effective-data-contract)
