---
type: Summary
description: "Summarizes candidate strategic business-rule approval, maintenance, suppression, and dated release scope."
doc_type: short
full_text: sources/KT-ratan-business-rule-governance.md
---

# Business-rule governance and maintenance intent

> **Source status:** Candidate/draft. The rule lifecycle and June 2024 release notes do not establish current policy or rollout.

The governance proposal ringfences strategic rule maintenance. It calls for maker/checker control, UAT testing, MT approval, DataOps setup, recorded approval dates, and annual review. Rule removal should consider payment failure, reconciliation breaks, NSTP volume, and STP effects. [Approval and review](../../../records/candidates/operations/KT-ratan-business-rule-governance.md#approval-and-review)

New rules require reasons and checker review, except dry-run rules. Updates require a reason and checker approval or rejection. Authorized operators may disable live rules or activate a live dry-run rule immediately for subsequent processing. The source does not resolve precedence between general approval and immediate operator actions. Cashflow suppression prevents downstream payment/accounting; SWIFT suppression has a separate payment-routing effect. Profile names are source-specific and do not establish current entitlements. [Rule maintenance contract](../../../records/candidates/operations/KT-ratan-business-rule-governance.md#rule-maintenance-contract) [Rule-class scope](../../../records/candidates/operations/KT-ratan-business-rule-governance.md#rule-class-scope)

A June 2024 list includes China rule tiles and other integrations; its development-pass labels are not deployment evidence. Confirm owner, authority, effective profiles, annual review, and scope before treating this as current. [Dated June 2024 scope](../../../records/candidates/operations/KT-ratan-business-rule-governance.md#dated-june-2024-scope)

See proposed [[summaries/KT-rule-service-p3]].
