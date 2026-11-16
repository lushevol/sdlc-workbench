---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-nostro-golden-source-proposal",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-29b5ddb89afbf065d4f70af7",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Static Data/Nostro SSI/Nostro Static Golden Source/page.md",
      "revision": "sha256:786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457",
      "sha256": "786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457",
      "snapshot": "knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md"
    },
    {
      "id": "SRC-e69114335ac8469c23bef40f",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Knowledge Base/What is VOSTRO NOSTRO/page.md",
      "revision": "sha256:2137b8498952e395307fa65b27e83f9b6611da5def18819469d9fbcdc19f2efb",
      "sha256": "2137b8498952e395307fa65b27e83f9b6611da5def18819469d9fbcdc19f2efb",
      "snapshot": "knowledge/evidence/sources/sha256/2137b8498952e395307fa65b27e83f9b6611da5def18819469d9fbcdc19f2efb.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:31:00.554506+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "Nostro concepts and golden-source proposal",
  "summary": "A Nostro account holds this bank\u2019s funds at another bank.",
  "related": [],
  "open_questions": [
    "Confirm whether the NAMS\u2192RDM proposal was approved and its effective scope.",
    "Resolve suspense storage, cache ownership, matching keys, and one-account-to-many-ledger rules."
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
# Nostro concepts and golden-source proposal

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Nostro concepts and golden-source proposal. This candidate retains the source-specific conditions and applicability limits below.

## Summary

A Nostro account holds this bank’s funds at another bank.

## Documented knowledge

### Account distinctions

A Nostro account holds this bank’s funds at another bank. A Vostro account holds another bank’s funds at this bank. The source connects these accounts with settlement positions and reconciliation. The golden-source proposal distinguishes Nostro accounts held with another legal entity, over accounts within the same legal entity, and internal suspense accounts without payment or receipt. It groups all three under Nostro static.

[Source 51, lines 1-6](../../../../knowledge/evidence/sources/sha256/2137b8498952e395307fa65b27e83f9b6611da5def18819469d9fbcdc19f2efb.md#L1-L6) [Source 51, lines 10-11](../../../../knowledge/evidence/sources/sha256/2137b8498952e395307fa65b27e83f9b6611da5def18819469d9fbcdc19f2efb.md#L10-L11) [Source 51, lines 22-24](../../../../knowledge/evidence/sources/sha256/2137b8498952e395307fa65b27e83f9b6611da5def18819469d9fbcdc19f2efb.md#L22-L24) [Source 38, lines 3-11](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L3-L11)

### Proposed distribution and fields

The proposal nominates NAMS as the golden source, with RATAN piloting consumption through RDM. Other FMO systems would follow. Metal-currency Nostros would require direct RDM maintenance. Proposed matching/static fields include agent SCI, status, currency, settlement means/account, effective dates, FMO-use indicator, and FMO system. SSI relevance and correspondent-type relevance remain undecided. Agent SCI maps to `SCI.SCI_ID` plus `/` plus `SUB_PROFILE_SCID`; agent BIC maps to `SCI.ATLAS_CODE`. No populated account examples are retained here.

[Source 38, lines 13-17](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L13-L17) [Source 38, lines 21-26](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L21-L26) [Source 38, lines 31-38](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L31-L38) [Source 38, lines 46-50](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L46-L50) [Source 38, lines 53-53](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L53-L53)

### Unresolved ownership and matching

Suspense searching keys list settlement account and means. Legal entity and currency remain questioned additions. Source questions leave suspense storage ownership, RATAN caching, and one-account-to-many-ledger mapping unresolved. These are proposal gaps, not approved defaults. The proposal does not establish current source ownership or implementation.

[Source 38, lines 59-69](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L59-L69) [Source 38, lines 93-97](../../../../knowledge/evidence/sources/sha256/786f6ebb718bc1ce6bd3eab6c5d4650ef46171db6ee1725449018a176770c457.md#L93-L97)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm whether the NAMS→RDM proposal was approved and its effective scope.
- Resolve suspense storage, cache ownership, matching keys, and one-account-to-many-ledger rules.
