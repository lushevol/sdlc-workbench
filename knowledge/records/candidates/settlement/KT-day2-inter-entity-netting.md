---
type: KnowledgeTopic
id: KT-day2-inter-entity-netting
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-e1af56d2e0ac39bf0c1c6379
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Inter Entity Netting.md
  revision: sha256:90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e
  sha256: 90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e
- id: SRC-0a94ec69d2a9600fc7f74202
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Inter Entity Netting/page.md
  revision: sha256:90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e
  sha256: 90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e
- id: SRC-e1af56d2e0ac39bf0c1c6379
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Inter Entity Netting.md
  revision: sha256:90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e
  sha256: 90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e
- id: SRC-e3e68022dd0582aa76ec1d0b
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Inter Entity Netting/Inter
    Entity Netting Design.md
  revision: sha256:b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb
  sha256: b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb
- id: SRC-ebe7fccafca8afc25863c39d
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Inter Entity Netting/Inter Entity Netting
    Design/page.md
  revision: sha256:b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb
  sha256: b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb
- id: SRC-e3e68022dd0582aa76ec1d0b
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Inter Entity Netting/Inter Entity Netting
    Design.md
  revision: sha256:b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb
  sha256: b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb
- id: SRC-9cc6bb253217e2b6fff9825c
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Inter Entity STP/page.md
  revision: sha256:856d8c791d94461bf4044a112e5e831aa3d7057e8bec99177dca3cdb5d77c2bc
  sha256: 856d8c791d94461bf4044a112e5e831aa3d7057e8bec99177dca3cdb5d77c2bc
classification: settlement
scope: Inter-entity matching, netting, and linked withdrawal intent
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-settlement-manual-netting
- KT-settlement-auto-netting
- KT-ratan-settlement-integration-checklist-scope
open_questions:
- 'KDQ-492d176abd: Which phase-one branch pairs, reciprocal mapping static, USD threshold,
  and deterministic resultant counterparty selection are approved?'
- 'KDQ-7f1208deec: Which exact linked release boundary and manual-withdrawal state
  transitions govern inter-entity un-net?'
- 'KDQ-a2f354f72f: Which internal identifier, exception bypass, and auto-affirmation
  policy govern Murex STP and linked netting?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:47:34.274710+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Inter-entity matching, netting, and linked withdrawal intent

## Scope

Inter-entity matching, netting, and linked withdrawal intent.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### IEN-01 — Phase-one eligibility and USD enrichment

The changed inter-entity requirement covers gross flows and IRS-aggregation resultants.
It limits eligible cashflows to at most USD 100000 equivalent.
USD-equivalent enrichment occurs after materialization at VD-5 and refreshes on Reinstate.
Phase one nets USD only. Other currencies are later scope; precious metals require CIS involvement.
The source lists specific branch pairs and marks China head office/Hong Kong for initial enablement.
The embedded rule excludes LOANIQ. Its full production static membership requires a scoped owner decision.
The source states that ADO needs updating. The requirement text is not proof of an approved deployed rule.

[Original evidence](../../../evidence/sources/sha256/90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e.md#L20-L31).

### IEN-02 — Reciprocal pre-match and resultant rules

Pre-match requires equal currency, value date, amount, and opposite directions.
Each booking-entity FMID must match the opposite counterparty mapped FMID.
Default mapping is the original FMID; special mappings require backend static.
Matched linked flows are eligible for automatic netting with affirmation. Unmatched flows, including unmatched singleton groups, go gross without affirmation.
The netting key is booking entity, value date, currency, and mapped counterparty.
The resultant payment type is Inter Entity Netting. Counterparty FMID/BIC derives from one component without deterministic selection.
The source expects resultants and gross flows to be full STP, but retains an auto-affirmation-removal dependency.
Those statements require reconciliation; they do not justify universal exception bypass.

[Original evidence](../../../evidence/sources/sha256/90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e.md#L24-L31). [Original evidence](../../../evidence/sources/sha256/90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e.md#L66-L71).

### IEN-03 — Direction-specific pre-match key design

The design enriches cashflows with USD Transferred Amount.
Pay pre-match keys use entity FMID, counterparty FMID, and amount.
Receive keys reverse the first two terms: counterparty FMID, entity FMID, and amount.
The examples are candidate matches, not authoritative counterparty mapping values.
The complete business key still includes the separately required value date and currency.

[Original evidence](../../../evidence/sources/sha256/b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb.md#L1-L13). [Original evidence](../../../evidence/sources/sha256/b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb.md#L27-L34).

### IEN-04 — Design alias scope

The sibling design identity has byte-identical source and selected-view hashes.
It supplies the same direction-specific key and enrichment proposal.
Both source identities remain declared; they are not separate evidence of implementation.

[Original evidence](../../../evidence/sources/sha256/b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb.md#L1-L13). [Original evidence](../../../evidence/sources/sha256/b4ba316c4bae3b58965a9b29431698cb218d2c9c264e110a8bd7a2aab0653cdb.md#L27-L34).

### IEN-05 — Linked withdrawal and release boundary

Option 1 is struck out. Option 2 links both inter-entity resultants for withdrawal handling.
Automatic un-net applies only when neither side crossed the specified release boundary.
The table includes READY/Pending Ack, Released, Settled, and corresponding SPLIT states in that boundary.
If either side crossed it, neither side auto-un-nets; the withdrawal waits for manual handling.
Before that boundary, withdrawal can kill both resultants, cancel the withdrawn component, and regroup the remaining components.
The selected scenario sends the unmatched counterpart gross.
Manual un-net of one side does not un-net the other. Operators must handle both to restore a matched pair.
The scenario after a received withdrawal marks that component DEAD on manual un-net and sends remaining components gross.
These target outcomes are distinct from the table current-behavior descriptions.

[Original evidence](../../../evidence/sources/sha256/90d7977d8db99e77ed17a2a211ecdcb9553b5de021d787f6f121bee28c2dd89e.md#L33-L60).

### IEN-06 — Separate internal-counterparty STP request

The separate STP request is limited to Murex 2.11 inter-entity cashflows.
It asks for an internal-counterparty identifier that can bypass exceptions.
It does not define the identifier, bypassed exception list, or relationship to linked-netting affirmation.
The request cannot establish unrestricted STP for all inter-entity sources.

[Original evidence](../../../evidence/sources/sha256/856d8c791d94461bf4044a112e5e831aa3d7057e8bec99177dca3cdb5d77c2bc.md#L1-L8).

## Connections

Related canonical IDs: `KT-settlement-manual-netting`, `KT-settlement-auto-netting`, `KT-ratan-settlement-integration-checklist-scope`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
