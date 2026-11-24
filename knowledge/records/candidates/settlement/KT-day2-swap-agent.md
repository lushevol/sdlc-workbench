---
type: KnowledgeTopic
id: KT-day2-swap-agent
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-675bf34c9ff0fc22442b8681
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Swap Agent Day2/page.md
  revision: sha256:74bf8b994022b427e999626ab1d3cc3cf5cbb0101af6367525835bfc9cb6bb8f
  sha256: 74bf8b994022b427e999626ab1d3cc3cf5cbb0101af6367525835bfc9cb6bb8f
- id: SRC-238521c68615694521d64665
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Swap Agent Payment Enhancement/page.md
  revision: sha256:e4064ff9510fc8f03be1906c6a45923d3a9528741de9c8971b2c4162e44b31f5
  sha256: e4064ff9510fc8f03be1906c6a45923d3a9528741de9c8971b2c4162e44b31f5
- id: SRC-7bffb4b33c3da8ee08846097
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Hard Blocker/Hard Blocker Tech Design/page.md
  revision: sha256:556711e962a661e88670bed3360d320fb76faa75d545eddacc4a3c5997dce82c
  sha256: 556711e962a661e88670bed3360d320fb76faa75d545eddacc4a3c5997dce82c
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:53:59.758856+00:00'
verified: []
classification: settlement
scope: Proposed Swap Agent netting, SWIFT suppression, and release-blocker behavior.
summary: Day 2 sources propose payment-type netting, selected-client principal settlement,
  suppression, and a separate hard blocker for Coupon and Interim MTM flows.
related:
- KT-settlement-auto-netting
- KT-settlement-lms-feed
open_questions:
- Which owner confirms the effective scope and applicability of this candidate?
- Which implementation, environment and acceptance evidence is still required?
- How does the hard blocker apply to Coupon and Interim MTM flows, and how does it
  interact with scheduled netting and SWIFT suppression?
- 'KDQ-d33e2b5bb4: Which client, payment-type, and source scope governs the Swap Agent
  enhancement?'
- 'KDQ-b3f9557fc8: Which indicator source and missing-indicator treatment govern selected
  clients?'
- 'KDQ-c397490819: Which authority resolves scheduling, suppression, and hard-blocker
  interaction?'
previous_content_sha256: 6ff9b22d53f4ef1bdbe76981e66cafe2e42f0fbc9723377c7d848cfcbf528e3d
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Swap Agent netting and release controls

## Scope

This candidate records Day 2 Swap Agent netting, suppression, and release-blocker proposals.

## Summary

The sources propose separate netting rules for Coupon and Interim MTM flows.
They also discuss principal exchanges for selected clients and a hard blocker for Coupon and Interim MTM release.

## Documented knowledge

The Day 2 design separates Coupon and Interim MTM netting predicates.
It proposes a 30-minute retry after job failure, payment-type-specific resultants, and SWIFT suppression.
It excludes Initial and Final Notional from the existing rule.
[Day 2 predicates and outcomes](../../../evidence/sources/sha256/74bf8b994022b427e999626ab1d3cc3cf5cbb0101af6367525835bfc9cb6bb8f.md#L9-L14) [Day 2 scenarios](../../../evidence/sources/sha256/74bf8b994022b427e999626ab1d3cc3cf5cbb0101af6367525835bfc9cb6bb8f.md#L21-L24)

The enhancement proposes principal exchanges for selected clients.
It allows cross-payment-type netting and Murex/Stella cashflows in that scope.
It proposes a Swap Agent Netting resultant and suppression for both resultants and single cashflows.
The enhancement says the existing SAL Coupon and SAL MTM rules continue for out-of-scope clients.
[Principal enhancement](../../../evidence/sources/sha256/e4064ff9510fc8f03be1906c6a45923d3a9528741de9c8971b2c4162e44b31f5.md#L7-L17) [Enhancement scenarios](../../../evidence/sources/sha256/e4064ff9510fc8f03be1906c6a45923d3a9528741de9c8971b2c4162e44b31f5.md#L23-L27)

A separate technical design says to add a hard blocker against releasing SWAP_AGENT Coupon and Interim MTM cashflows from RATAN.
It does not define the trigger, the permitted exit path, or the interaction with the netting and suppression designs.
[Hard-blocker requirement](../../../evidence/sources/sha256/556711e962a661e88670bed3360d320fb76faa75d545eddacc4a3c5997dce82c.md#L5-L7)

### L3-SWAP-01 — Existing payment-type rules

The Day2 design uses separate Coupon and Interim MTM rules. Their keys include booking entity, counterparty, currency, value date, and payment type. Netting ID must be empty. Coupon and MTM must not net together. Initial and Final Notional remain excluded. Use the parent trade clearing organization and external trade identifiers from the documented parent/Murex fields. Retry a failed job after 30 minutes. Suppressed cashflows do not feed LMS.

[Original evidence](../../../evidence/sources/sha256/74bf8b994022b427e999626ab1d3cc3cf5cbb0101af6367525835bfc9cb6bb8f.md#L1-L14). [Original evidence](../../../evidence/sources/sha256/74bf8b994022b427e999626ab1d3cc3cf5cbb0101af6367525835bfc9cb6bb8f.md#L17-L26).

### L3-SWAP-02 — Selected-client enhancement

The enhancement targets selected clients and CCS principal settlement. Murex identifies strategy SWAP_AGENT; Stella requires SwapAgentID. The proposed rule has no currency filter. It allows cross-payment-type and cross-Murex/Stella netting in this selected scope. The unchecked payment-type list does not establish approval for every entry. SwapAgentNetting has priority above SALMTM. The job time is VD 01:00 GMT. Suppress singleton and resultant SWIFT. Exclude these selected clients from old SAL rules; retain old SAL rules for other clients. Missing-indicator risk is a design concern, without inspected release evidence.

[Original evidence](../../../evidence/sources/sha256/e4064ff9510fc8f03be1906c6a45923d3a9528741de9c8971b2c4162e44b31f5.md#L1-L21). [Original evidence](../../../evidence/sources/sha256/e4064ff9510fc8f03be1906c6a45923d3a9528741de9c8971b2c4162e44b31f5.md#L23-L40).

## Connections

The [auto-netting topic](KT-settlement-auto-netting.md) describes scheduled rule selection and resultant handling.
The [LMS feed topic](KT-settlement-lms-feed.md) records downstream feed and SWIFT suppression proposals.

## Evidence limits

The Day 2 sources contain proposed rules and test scenarios.
The client scope, authority, effective date, current implementation, and deployment were not verified.
The release-blocker design does not resolve whether the block applies before or after netting.

## Open questions

Owner: unknown.

- Which owner confirms the effective scope and applicability of this candidate?
- Which implementation, environment and acceptance evidence is still required?
- How does the hard blocker apply to Coupon and Interim MTM flows, and how does it interact with scheduled netting and SWIFT suppression?
