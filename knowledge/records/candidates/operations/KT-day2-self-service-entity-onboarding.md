---
type: KnowledgeTopic
id: KT-day2-self-service-entity-onboarding
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-25d15442fba734d600ffb35d
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Self‑service new entity & branch onboarding/1.Self
    Service Tech Design/1.Detail Design/page.md
  revision: sha256:19e4b951045620b19e2d04effb36f43b6962a0292d9bf3b89b7c41e3cb63d157
  sha256: 19e4b951045620b19e2d04effb36f43b6962a0292d9bf3b89b7c41e3cb63d157
- id: SRC-0cff776de2018bb647154886
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Self‑service new entity & branch onboarding/1.Self
    Service Tech Design/page.md
  revision: sha256:cd045d8449ec8fd8c101e33c8401a45881f561cdde272809f254a627a300e48a
  sha256: cd045d8449ec8fd8c101e33c8401a45881f561cdde272809f254a627a300e48a
- id: SRC-1af3620608188b09f03926d7
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Self‑service new entity & branch onboarding/10.FAQ/page.md
  revision: sha256:35f121e944b7a609e9c2fdc8e81c2f65804e755fdf760433acda9c59ab1be930
  sha256: 35f121e944b7a609e9c2fdc8e81c2f65804e755fdf760433acda9c59ab1be930
- id: SRC-693668920df68e1f471fa66d
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Self‑service new entity & branch onboarding/2.API
    Design(Self Service)/page.md
  revision: sha256:c9e99b4fcb012504690e7ae31b4a866ba17fa724158f13be567a775a1c189ac5
  sha256: c9e99b4fcb012504690e7ae31b4a866ba17fa724158f13be567a775a1c189ac5
- id: SRC-65effb589e167010b50f260c
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Self‑service new entity & branch onboarding/page.md
  revision: sha256:9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0
  sha256: 9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0
classification: operations
scope: Self-service entity onboarding proposal
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-ratan-entity-and-currency-onboarding-controls
open_questions:
- 'KDQ-5eedd8ca27: Which configuration architecture governs the temporary currency
  mapping and final static-service ownership?'
- 'KDQ-af71abeb99: Which roles and static tables are in final scope?'
- 'KDQ-7b40cdd16c: What controls apply after a confirmed update and for new-country
  backend configuration?'
- 'KDQ-ce26fce650: Can the API design be provided as a schema-only view with representative
  placeholders?'
- 'KDQ-353c6ed28b: Can the FAQ retain decisions without static database row values?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:53:59.787777+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Self-service entity onboarding proposal

## Scope

Self-service entity onboarding proposal.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### L3-SELF-01 — Preserving onboarding interfaces

The proposal must preserve existing business functions and integrate unified maker/checker review. It moves branch-code configuration from application.yml to ratanone.branch_code_config and changes consumers to read the database.

[Original evidence](../../../evidence/sources/sha256/19e4b951045620b19e2d04effb36f43b6962a0292d9bf3b89b7c41e3cb63d157.md#L3-L9). [Original evidence](../../../evidence/sources/sha256/19e4b951045620b19e2d04effb36f43b6962a0292d9bf3b89b7c41e3cb63d157.md#L11-L17).

### L3-SELF-02 — Ownership and one review flow

The design proposes one form and one maker/checker operation across related static configuration. Its temporary conclusion assigns static-service maintenance and query responsibility. Alternatives using separate domain storage, events, or distributed transactions are comparison options, not selected parallel architectures.

[Original evidence](../../../evidence/sources/sha256/cd045d8449ec8fd8c101e33c8401a45881f561cdde272809f254a627a300e48a.md#L3-L35).

### L3-SELF-03 — FAQ decisions and staged alternatives

The FAQ selects one form and one review flow. It requests CRUD while keeping bookingEntityFmid immutable. It excludes historical-data migration and excludes Nostro from this self-service form. It proposes ACTIVE to SAVE_CONFIRMED conversion and deprecation of the old cutoff API. It selects merging SWIFT sender/correspondent tables and unified review. Currency mapping temporarily uses group-service, with later static-service migration. This staging differs from the main design target. Country-zone warmup must complete before accounting jobs run. These are design decisions, without inspected migration or execution.

[Original evidence](../../../evidence/sources/sha256/35f121e944b7a609e9c2fdc8e81c2f65804e755fdf760433acda9c59ab1be930.md#L5-L27).

### L3-SELF-04 — API design scope

The API proposal uses POST /v1/onboard-config/draft, /submit, /update, /approve, /reject, /query, /delete, and /history. Draft saves to the database; submit starts review. Update starts from SAVE_CONFIRMED. Query supports statuses, pagination, and sorting. History uses mainTableId. The separate /v1/rounding-config family provides draft, submit, update, query, delete, bulk-approve, bulk-reject, and history. The rounding update example strikes out currency editing. Successful saves return 200; invalid parameters return 400; internal errors return 500 where specified. Example identifiers and history snapshots establish no grants, actual operations, or complete error contract.

[Original evidence](../../../evidence/sources/sha256/c9e99b4fcb012504690e7ae31b4a866ba17fa724158f13be567a775a1c189ac5.md#L3-L23).

### L3-SELF-05 — Business input and backend boundary

The chosen UI uses a blotter and subtiles. Static Ops can edit; other users are read-only. FMID is numeric and immutable; FMCode is populated and immutable. Branch-code golden-source handling remains open. Currency mapping is a separate optional global blotter, with required precision and ROUNDING_OFF, ROUNDING_DOWN, or ROUNDING_UP. ISO mapping is optional. Release cutoff uses currency, GMT time, VD-2/VD-1/VD, and business-day default. Local-time conversion remains a question. SWIFT and accounting sections are optional when applicable. Backend teams retain MX bifurcation, new-country EBBS connectivity and jobs, CPT, and country-specific analysis.

[Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L5). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L13-L18). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L22-L27). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L31-L57). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L72-L85).

### L3-SELF-06 — Conditional SWIFT and accounting fields

Sender BIC and its editable country default belong to the SWIFT section. Field 53 uses an 8- or 11-character BIC for the stated OverAccount or NOS currency/message branches, with Nostro fallback. Field 58 BIC applies to MT202 Flip. Accounting captures bridge account, posting branch, transaction type, debit/credit codes, accounting country, and ZoneId. SWIFT country and accounting country remain distinct. Post-confirmed-update controls and backend suppression currency handling remain unresolved.

[Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L5). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L13-L18). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L22-L27). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L31-L57). [Original evidence](../../../evidence/sources/sha256/9efe5eda704afc9ed9860ee9d2b459f8c9e0a2eb67641a1d8302a37211b925a0.md#L72-L85).

## Connections

Related canonical IDs: `KT-ratan-entity-and-currency-onboarding-controls`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
