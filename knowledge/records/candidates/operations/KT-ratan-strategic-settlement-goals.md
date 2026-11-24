---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-strategic-settlement-goals",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-b9d6aced9d9a9353573e847e",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Strategic Cash Settlements Features/Settlement Extension Dependencies/page.md",
      "revision": "sha256:17d770637e49b168d5378a08fc4db6fba42f3be064db08efa9042316e9c2f23c",
      "sha256": "17d770637e49b168d5378a08fc4db6fba42f3be064db08efa9042316e9c2f23c",
      "snapshot": "knowledge/evidence/sources/sha256/17d770637e49b168d5378a08fc4db6fba42f3be064db08efa9042316e9c2f23c.md"
    },
    {
      "id": "SRC-6bd24e969b741a5af6b79d56",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/page.md",
      "revision": "sha256:23e9c84905a4b8bed0f7b865051277456322aa834a3dceac145820f9d79f4ebc",
      "sha256": "23e9c84905a4b8bed0f7b865051277456322aa834a3dceac145820f9d79f4ebc",
      "snapshot": "knowledge/evidence/sources/sha256/23e9c84905a4b8bed0f7b865051277456322aa834a3dceac145820f9d79f4ebc.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:34:00.170573+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "Strategic settlement goals and attribute dependencies",
  "summary": "The project goal calls for an in-house strategic settlement platform that removes vendor dependency.",
  "related": [],
  "open_questions": [
    "Confirm the current strategic scope and accountable owner.",
    "Confirm effective currency/entity mappings in their owning contracts."
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
# Strategic settlement goals and attribute dependencies

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Strategic settlement goals and attribute dependencies. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The project goal calls for an in-house strategic settlement platform that removes vendor dependency.

## Documented knowledge

### Strategic goals

The project goal calls for an in-house strategic settlement platform that removes vendor dependency. It should address existing pain points and support complicated scenarios with stability and flexibility. It proposes reuse within TPT. The comparison identifies desired post-trade ownership, a payment lake for actions/data/audit, removal of NSP creation, reuse or extension of existing services, and one settlement release-timing source. These are source-stated goals and benefits; they are not measured outcomes.

[Source 42, lines 25-46](../../../../knowledge/evidence/sources/sha256/23e9c84905a4b8bed0f7b865051277456322aa834a3dceac145820f9d79f4ebc.md#L25-L46)

### Attribute dependencies

The dependency table links currency to precious-metal versus other Swift message types, rounding, payment Swift, and settlement accounting. It links entity to entity-specific rounding and Murex2.11 NSTP rules. The table declares dependencies; it does not define a complete mapping or establish implementation coverage.

[Source 48, lines 1-4](../../../../knowledge/evidence/sources/sha256/17d770637e49b168d5378a08fc4db6fba42f3be064db08efa9042316e9c2f23c.md#L1-L4)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm the current strategic scope and accountable owner.
- Confirm effective currency/entity mappings in their owning contracts.
