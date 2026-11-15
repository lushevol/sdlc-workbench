---
type: KnowledgeTopic
id: KT-settlement-amendment-reversal-rebook-exceptions
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-0158e2dc7d405c5a9379e540
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Ingenuine Rebook Exception in Ratan/page.md
  revision: sha256:6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5
  sha256: 6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5
generated:
  by: agent:codex
  at: '2026-11-15T11:41:47Z'
verified: []
classification: settlement
scope: Proposed reversal and rebook exception handling for amendments to released cashflows.
summary: The design pairs an original cashflow withdrawal with its replacement but says the current system lacks direct linkage to identify the pair reliably.
related:
- KT-settlement-cashflow-identity-and-stella-write-back
- KT-settlement-cpn-netting
- KT-settlement-auto-netting
- KT-settlement-payment-amount-adjustment
open_questions:
- Which source event and identifier bind a released cashflow withdrawal to the replacement cashflow for exception generation?
- Does the proposed direction filter or post-Uber trade event define the accepted implementation path?
---
# Released amendment reversal and rebook exceptions

## Scope

This candidate records proposed exception handling for an amendment after the original cashflow has been released from RATAN.

## Summary

The source proposes a reversal exception for the withdrawal of the released cashflow and a rebook exception for its replacement.
It also identifies a missing direct link between the two cashflows.

## Documented knowledge

The problem statement describes an amendment that withdraws the original cashflow and creates a new one.
For a released original, it calls for additional operations validation before release.
It proposes a reversal exception for the withdrawal and a rebook exception for the new cashflow.
[Amendment and exception requirement](../../../evidence/sources/sha256/6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5.md#L1-L13)

The source says the system lacks a direct link between the original and new cashflows.
It says the system therefore cannot reliably identify amendment-driven new cashflows for rebook exception generation.
It lists adding direction to the query criteria and considering a trade event after Uber is enabled as potential enhancements.
[Linkage gap and proposed enhancements](../../../evidence/sources/sha256/6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5.md#L45-L48)

## Connections

The [cashflow identity topic](KT-settlement-cashflow-identity-and-stella-write-back.md) covers source IDs, versioning, and duplicate handling.
The [CPN netting topic](KT-settlement-cpn-netting.md) describes separate released-resultant reversal scenarios.
The [auto-netting topic](KT-settlement-auto-netting.md) covers rule-driven resultant handling.
The [payment adjustment topic](KT-settlement-payment-amount-adjustment.md) records an unresolved question about downstream rebook linkage.

## Evidence limits

The source records a design proposal and a system limitation.
It does not establish approval, implementation, deployment, or current behavior.
It does not specify the identity contract, qualifying trade events, exception states, or owner.

## Open questions

Owner: unknown.

- Which source event and identifier bind a released cashflow withdrawal to the replacement cashflow for exception generation?
- Does the proposed direction filter or post-Uber trade event define the accepted implementation path?
