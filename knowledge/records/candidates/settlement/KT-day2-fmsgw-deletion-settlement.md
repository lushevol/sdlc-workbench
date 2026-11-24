---
{
  "type": "KnowledgeTopic",
  "id": "KT-day2-fmsgw-deletion-settlement",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-1173610232d5d0b357a411cf",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow status sync with FMSGW deletion/page.md",
      "revision": "sha256:fd4a494e567e521b3a751b50a519909a27bd8f2f6502010a649b94f5ece12afc",
      "sha256": "fd4a494e567e521b3a751b50a519909a27bd8f2f6502010a649b94f5ece12afc",
      "snapshot": "knowledge/evidence/sources/sha256/fd4a494e567e521b3a751b50a519909a27bd8f2f6502010a649b94f5ece12afc.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:49:39.889552+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "FMSGW deletion and final cashflow status intent",
  "summary": "The requirement sets cashflow SETTLED for FMSGW Deleted,FMSRE Deleted,Manual Delete,Released by SCPAY or Released by AMH.",
  "related": [],
  "open_questions": [
    "Confirm effective source authority and applicable gateways/message types.",
    "Confirm ordering/idempotency when one COV response is delayed or later changes."
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
# FMSGW deletion and final cashflow status intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

FMSGW deletion and final cashflow status intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The requirement sets cashflow SETTLED for FMSGW Deleted,FMSRE Deleted,Manual Delete,Released by SCPAY or Released by AMH.

## Documented knowledge

### Final status trigger

The requirement sets cashflow SETTLED for FMSGW Deleted,FMSRE Deleted,Manual Delete,Released by SCPAY or Released by AMH. It explicitly chooses SETTLED instead of SWIFT_SUPPRESSED, citing duplicate-accounting concern. That concern is a source rationale, not an observed failure in this review.

[Source 25, lines 9-12](../../../../knowledge/evidence/sources/sha256/fd4a494e567e521b3a751b50a519909a27bd8f2f6502010a649b94f5ece12afc.md#L9-L12) [Source 25, lines 18-20](../../../../knowledge/evidence/sources/sha256/fd4a494e567e521b3a751b50a519909a27bd8f2f6502010a649b94f5ece12afc.md#L18-L20)

### Cover-message aggregation

For MT103/MT202COV, both responses must belong to that allowed final-status set, although their exact values can differ. A delete plus error leaves the cashflow RELEASED. Two allowed but different responses settle the cashflow while Swift status remains Check in FMSGW. That label means the two COV message statuses differ. Listed expected cases cover MT103,MT202,MT210,MT202Flip,MT192,MT292,MT604,MT605 and MT692. These are expected scenarios, not passing execution.

[Source 25, lines 11-12](../../../../knowledge/evidence/sources/sha256/fd4a494e567e521b3a751b50a519909a27bd8f2f6502010a649b94f5ece12afc.md#L11-L12) [Source 25, lines 22-33](../../../../knowledge/evidence/sources/sha256/fd4a494e567e521b3a751b50a519909a27bd8f2f6502010a649b94f5ece12afc.md#L22-L33)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm effective source authority and applicable gateways/message types.
- Confirm ordering/idempotency when one COV response is delayed or later changes.
