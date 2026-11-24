---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-payment-rounding-intent",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-602405de895b77475ae322b2",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Static Data/Rounding Rule - Tactical solution for H1 2024 Cashflow Migration/page.md",
      "revision": "sha256:7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79",
      "sha256": "7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79",
      "snapshot": "knowledge/evidence/sources/sha256/7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:31:00.556493+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "Dated payment-rounding intent",
  "summary": "The H1 2024 source requests RATAN rounding from original Murex amounts.",
  "related": [],
  "open_questions": [
    "Confirm current rounding responsibility and the effective currency table.",
    "Resolve negative amounts, tie handling, missing currencies, and floor-versus-truncation semantics."
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Automated checks do not establish complete writing review.",
    "Retained intent does not establish current approval, execution or rollout."
  ]
}
---
# Dated payment-rounding intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Dated payment-rounding intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The H1 2024 source requests RATAN rounding from original Murex amounts.

## Documented knowledge

### Dated responsibility

The H1 2024 source requests RATAN rounding from original Murex amounts. Stella rounding remains the strategic target. The source requests a tactical RATAN solution until Stella supplies rounded amounts. Its backlog statement is reported historical context, not current delivery evidence.

[Source 40, lines 3-8](../../../../knowledge/evidence/sources/sha256/7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79.md#L3-L8)

### Source and destination

Take the original Murex MxML `/MxPayML/flowAmount`, or Stella SCBML payment amount. Query precision and rounding type by `Cashflow.Payment_Currency`. Round, remove trailing zeros, and persist `Cashflow.Payment_Amount`. That rounded field becomes the sole subsequent amount for GUI, Swift, and accounting. The source example converts 3.102 to 3.10, then displays/persists 3.1.

[Source 40, lines 15-25](../../../../knowledge/evidence/sources/sha256/7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79.md#L15-L25) [Source 40, lines 27-35](../../../../knowledge/evidence/sources/sha256/7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79.md#L27-L35)

### Rounding semantics limit

The source describes Round Off as four down and five up. It labels Round Down as floor, but also describes decimal truncation. All shown numeric examples are positive. Negative-amount behavior therefore remains unresolved. The large currency table remains the source reference; this candidate does not replace or validate every currency row.

[Source 40, lines 10-13](../../../../knowledge/evidence/sources/sha256/7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79.md#L10-L13) [Source 40, lines 27-35](../../../../knowledge/evidence/sources/sha256/7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79.md#L27-L35) [Source 40, lines 37-38](../../../../knowledge/evidence/sources/sha256/7018268e0d9e1dc574ce1abd7a6baab4bb2d5c5069666b57fd8b0a0d00bf0c79.md#L37-L38)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm current rounding responsibility and the effective currency table.
- Resolve negative amounts, tie handling, missing currencies, and floor-versus-truncation semantics.
