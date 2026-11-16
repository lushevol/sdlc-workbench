---
type: KnowledgeTopic
id: KT-day2-query-validation
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-7ae9f09ef4044e0114a80093
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Quick Search & Custom Filter FE Query
    Validation/page.md
  revision: sha256:e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d
  sha256: e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d
classification: query
scope: Quick-search and custom-filter validation proposal
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-advanced-search-p3
open_questions:
- 'KDQ-702252ac48: Which validation scope, operators, and messages govern quick search
  and custom filters?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:57:22.283692+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Quick-search and custom-filter validation proposal

## Scope

Quick-search and custom-filter validation proposal.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### L3-QUERY-01 — Bounded query validation

The proposal bypasses validation for trade original ID queries. Other described queries require value date and at least booking entity or counterparty. Payment date permits =, in, bet, <=, and >=. Booking entity FMID and cashflow state permit = and in. Multiple cashflow states need no extra field validation. Opening an invalid saved filter warns but keeps it visible. Invalid filters cannot be saved, created, or searched. Deletion remains allowed.

[Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L5). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L7-L8). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L13-L15). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L23-L25). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L29-L39). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L45-L50).

### L3-QUERY-02 — Search UI controls

Disable the search bar and clear it for query or filter searches. Navigation buttons highlight on first click and toggle off on another click. Value Today follows that toggle behavior. Cashflow Sub State is conditional on user confirmation, without a recorded confirmation here.

[Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L5). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L7-L8). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L13-L15). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L23-L25). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L29-L39). [Original evidence](../../../evidence/sources/sha256/e6722f2a45316c6889bf3b94a5ac38f0ffaeac95ee40b3aa5f8134a25525362d.md#L45-L50).

## Connections

Related canonical IDs: `KT-advanced-search-p3`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
