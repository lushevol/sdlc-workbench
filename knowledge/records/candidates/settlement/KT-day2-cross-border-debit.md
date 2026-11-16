---
{
  "type": "KnowledgeTopic",
  "id": "KT-day2-cross-border-debit",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-7eceb63f82ef7996571c70c7",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cross Border Debit/page.md",
      "revision": "sha256:3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8",
      "sha256": "3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8",
      "snapshot": "knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:49:39.893606+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Cross-border debit MT202 intent",
  "summary": "The requirement replaces MT202Flip for receive-side cross-border debit when another SCB entity holds the client account.",
  "related": [],
  "open_questions": [
    "Confirm current cross-debit/Flip priority and settlement-means/account predicate.",
    "Confirm maintained legal-entity BIC mapping, field58 account rule and LMS impact."
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
# Cross-border debit MT202 intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Cross-border debit MT202 intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The requirement replaces MT202Flip for receive-side cross-border debit when another SCB entity holds the client account.

## Documented knowledge

### Eligibility and scope

The requirement replaces MT202Flip for receive-side cross-border debit when another SCB entity holds the client account. A Vostro settlement account in CCY CROSSDEBIT format triggers MT202 CROSSDEBIT. MT103 CROSSDEBIT is explicitly excluded. Pay-side flows retain normal MT103/MT202 mapping. Accounting remains as-is and the cashflow feed goes to LMS. A dated January2026 note checks cross-debit before Flip. Earlier Nostro-versus-OverAccount overlap wording remains a condition requiring confirmation.

[Source 26, lines 3-7](../../../../knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md#L3-L7) [Source 26, lines 11-11](../../../../knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md#L11-L11) [Source 26, lines 13-19](../../../../knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md#L13-L19) [Source 26, lines 38-39](../../../../knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md#L38-L39) [Source 26, lines 45-49](../../../../knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md#L45-L49)

### Message mapping

Block1 sender and Block2 receiver use Vostro57BIC. Field52 uses Vostro58 beneficiary details:52A for BIC,otherwise52D. Field53B uses Vostro58 beneficiary account. Field57A uses Nostro-agent BIC. Field58 uses the legal-entity BIC from backend static, with optional Nostro account. The dated notes reject a separate GMO BIC substitution and require the documented beneficiary BIC/account. Field72 needs no extra logic beyond SSI setup. The exact maintained legal-entity mapping and LMS contract remain outside this source.

[Source 26, lines 21-28](../../../../knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md#L21-L28) [Source 26, lines 45-50](../../../../knowledge/evidence/sources/sha256/3e328b1cd9040475ff254b3ebd3a1fb35cc6f81e0a0a55dddb51f373fb6e1bb8.md#L45-L50)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm current cross-debit/Flip priority and settlement-means/account predicate.
- Confirm maintained legal-entity BIC mapping, field58 account rule and LMS impact.
