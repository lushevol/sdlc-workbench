---
type: KnowledgeTopic
id: INT-KT-entity-and-reference-data-design
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-e7ff4dfa6448d8799e148f5a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Entity
    level static/page.md
  revision: sha256:d01722f9ce21f5c8d109c4c711a87ad4349ce580b91ba0f0ad1bf4660332407a
  sha256: d01722f9ce21f5c8d109c4c711a87ad4349ce580b91ba0f0ad1bf4660332407a
- id: SRC-a56274420c25b359a8f3881a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    holiday data process from RDM introduction/page.md
  revision: sha256:10a161ed76da791eadd9d0285e1aee4c37161e728ebd54b71e29cf6dd5407a3b
  sha256: 10a161ed76da791eadd9d0285e1aee4c37161e728ebd54b71e29cf6dd5407a3b
generated:
  by: agent:codex:sol-integrations-review
  at: '2026-11-16T01:23:25.366445+00:00'
verified: []
classification: settlement
scope: Proposed entity onboarding configuration and RDM holiday-record responsibilities
summary: Selected source descriptions preserve scoped intended responsibilities. Current
  authority and applicability remain unresolved.
related:
- KT-settlement-lms-feed
- INT-KT-ratan-reference-and-control-interfaces
open_questions:
- 'KDQ-63cf718228: Which consolidated entity fields and maintenance authority are
  approved, and how does LMS filter removal affect the proposed field?'
- 'KDQ-3f7b049931: Who validates entity/static changes and preserves existing configuration
  during migration?'
- 'KDQ-86a8db8385: How do RDM corrections, deletions, and special-holiday precedence
  apply to the four-part duplicate key?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Entity and holiday reference-data design

## Scope

Proposed entity onboarding configuration and RDM holiday-record responsibilities.
These source descriptions define separate contracts. They establish no deployed or tested behavior.

## Summary

The selected sources describe related responsibilities and conditions.
Their original authority, effective dates, and current applicability remain unresolved.

## Documented knowledge

### STATIC-01 — Entity configuration consolidation proposal

The proposal consolidates entity onboarding configuration into one table, excluding Nostro static.
Nostro keys remain entity FMID, currency, settlement means, and settlement method. Currency-release time uses entity FMID and currency.
The proposed entity table covers FMID/FMCODE, workflow flag, LMS filter, branch/country, accounting routing/codes, bridge account, currency, and sender/correspondent BIC.
Workflow examples list Strategic, Legacy, and CPT. Other populated values are examples, not mandatory defaults or approved account data.
The intended goal is less manual onboarding work and self-service maintenance.
BIC-netting static, FXU static, and profile limits appear only as additional thinking. They are not confirmed extensions.
This entity-filter proposal does not override the separately proposed LMS sender-side filter removal.

[Selected original evidence](../../../evidence/sources/sha256/d01722f9ce21f5c8d109c4c711a87ad4349ce580b91ba0f0ad1bf4660332407a.md#L3-L51).

### STATIC-02 — RDM holiday input and duplicate key

The holiday design separates raw messages from structured holiday records.
The proposed tables are `ratan_static_rdm_holiday_weekend_message` and `ratan_static_cashflow_currency_holiday`.
The structured duplicate key combines `center_id`, `event_date`, `event_name`, and `file_type`.
Ordinary holiday/weekend data uses Solace and a full BCDF through FileIT. Special holidays use Solace.
RATAN consumes FileIT notifications; the reference limits its relevant specification to Notification Message chapter 3.1.2.1.
Ordinary service IDs are RDM00463, RDM00493, and RDM00827 in production and test.
Special-holiday IDs differ: RDM00470 for production and RDM00846 for test.
Sample event dates, countries, identifiers, paths, and payload values are fixtures and do not establish holiday calendars.
The selected text does not define correction, deletion, or special-holiday precedence.

[Selected original evidence](../../../evidence/sources/sha256/10a161ed76da791eadd9d0285e1aee4c37161e728ebd54b71e29cf6dd5407a3b.md#L1-L13), [Selected original evidence](../../../evidence/sources/sha256/10a161ed76da791eadd9d0285e1aee4c37161e728ebd54b71e29cf6dd5407a3b.md#L41-L49), [Selected original evidence](../../../evidence/sources/sha256/10a161ed76da791eadd9d0285e1aee4c37161e728ebd54b71e29cf6dd5407a3b.md#L59-L129).

## Connections

Related canonical IDs: `KT-settlement-lms-feed`, `INT-KT-ratan-reference-and-control-interfaces`.

## Evidence limits

Source descriptions supply documented intent and historical proposals only.
They do not establish current approval, implementation, configuration, deployment, execution, or acceptance.
Unselected content and attachments were not used to fill gaps.

## Open questions

Owner: unknown. Answers remain pending in the single [task question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
