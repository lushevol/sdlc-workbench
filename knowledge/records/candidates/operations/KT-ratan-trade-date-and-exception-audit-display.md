---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-trade-date-and-exception-audit-display",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-d744e650fc9ffa6d82e7fc1e",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2024 Release Plan/Release On 2024-01-20 CR  CHG0363082/page.md",
      "revision": "sha256:e7304ac8650bff7b13a9f5c8c6833ca6029c4398ce8a482f47a2b988fe36a094",
      "sha256": "e7304ac8650bff7b13a9f5c8c6833ca6029c4398ce8a482f47a2b988fe36a094",
      "snapshot": "knowledge/evidence/sources/sha256/e7304ac8650bff7b13a9f5c8c6833ca6029c4398ce8a482f47a2b988fe36a094.md"
    },
    {
      "id": "SRC-b5d0e977d16fce70137d0f7f",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Quality Assurance/Q&A/page.md",
      "revision": "sha256:6e04dc00f69cb8c2cf2e8524563ad0010ed0b9bb4cbff85e6f7e2918a4612b05",
      "sha256": "6e04dc00f69cb8c2cf2e8524563ad0010ed0b9bb4cbff85e6f7e2918a4612b05",
      "snapshot": "knowledge/evidence/sources/sha256/6e04dc00f69cb8c2cf2e8524563ad0010ed0b9bb4cbff85e6f7e2918a4612b05.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:34:00.178709+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "Trade-date and exception-comment display intent",
  "summary": "The January 2024 enhancement says that a null trade date must not display today.",
  "related": [],
  "open_questions": [
    "Confirm current trade-date fallback and exception-audit ownership.",
    "Resolve State versus Status naming without inferring the answer from uninspected screenshots."
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
# Trade-date and exception-comment display intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Trade-date and exception-comment display intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The January 2024 enhancement says that a null trade date must not display today.

## Documented knowledge

### Trade-date display

The January 2024 enhancement says that a null trade date must not display today. It does not supply another fallback or authorize rewriting the missing value.

[Source 4, lines 20-20](../../../../knowledge/evidence/sources/sha256/e7304ac8650bff7b13a9f5c8c6833ca6029c4398ce8a482f47a2b988fe36a094.md#L20-L20)

### Exception audit comments

The Q&A says comments entered while makers/checkers fix exceptions appear in the cashflow audit table. It assigns already-netted Murex IRS handling to Murex and says China need not handle that case. This does not establish a general cross-region prohibition. The State-versus-Status question remains unanswered in selected text.

[Source 43, lines 7-7](../../../../knowledge/evidence/sources/sha256/6e04dc00f69cb8c2cf2e8524563ad0010ed0b9bb4cbff85e6f7e2918a4612b05.md#L7-L7) [Source 43, lines 9-10](../../../../knowledge/evidence/sources/sha256/6e04dc00f69cb8c2cf2e8524563ad0010ed0b9bb4cbff85e6f7e2918a4612b05.md#L9-L10)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm current trade-date fallback and exception-audit ownership.
- Resolve State versus Status naming without inferring the answer from uninspected screenshots.
