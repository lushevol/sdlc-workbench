---
type: Summary
description: "Summarizes candidate self-service entity configuration, review, API, data ownership, and country-specific fields."
doc_type: short
full_text: sources/KT-day2-self-service-entity-onboarding.md
---

# Self-service entity onboarding proposal

> **Source status:** Candidate/draft. These API and UI decisions do not establish migration, implementation, or acceptance.

The proposal seeks one form and maker/checker flow while preserving business functions. It moves branch-code configuration from application settings to a database-backed table. The FAQ excludes historical-data migration and Nostro from this form. Currency mapping temporarily uses group-service before a later static-service migration. That staging differs from the main target. [L3-SELF-01](../../../records/candidates/operations/KT-day2-self-service-entity-onboarding.md#l3-self-01--preserving-onboarding-interfaces) [L3-SELF-02](../../../records/candidates/operations/KT-day2-self-service-entity-onboarding.md#l3-self-02--ownership-and-one-review-flow) [L3-SELF-03](../../../records/candidates/operations/KT-day2-self-service-entity-onboarding.md#l3-self-03--faq-decisions-and-staged-alternatives)

Draft, submit, update, approve, reject, query, delete, and history APIs are proposed. Static Ops may edit while other users read; FMID and FMCode are immutable in the described UI. Currency rounding, cutoff time, SWIFT, accounting, and country-specific fields have separate conditions. Branch-code source, local-time conversion, and post-confirmation controls remain open. [L3-SELF-04](../../../records/candidates/operations/KT-day2-self-service-entity-onboarding.md#l3-self-04--api-design-scope) [L3-SELF-05](../../../records/candidates/operations/KT-day2-self-service-entity-onboarding.md#l3-self-05--business-input-and-backend-boundary) [L3-SELF-06](../../../records/candidates/operations/KT-day2-self-service-entity-onboarding.md#l3-self-06--conditional-swift-and-accounting-fields)

No migrated data, authorization, or API behavior was verified. Related entity controls appear in [[summaries/KT-day2-manual-entity-settlement]] and proposed [[summaries/KT-rule-service-p3]].
