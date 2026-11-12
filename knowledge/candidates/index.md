---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
- Source authority, current applicability, and business execution require separate review.
---

# Portal knowledge map

Start here to understand the supplied portal, UI platform, and Cash Settlement materials.
Read each topic's evidence limits before using its claims for new work.
The [derived knowledge wiki](../llm-wiki/wiki/index.md) provides summaries, concepts, and entities for compiled records.
Use the canonical records below for the 12 November 2026 policy clarification. The compiled wiki may reflect earlier versions.

All listed domain records remain candidates after source locator and content updates.
All retain `status: draft`. The RATAN team owns the authentication and session policy; topic-wide ownership remains unknown where stated.
No record has recorded human publication approval.
Session knowledge describes intended target behavior. Its independent gap record contains implementation and observation comparisons.

These records explain the portal and its business-system responsibilities.
Source snapshots and review metadata remain outside this directory.
Original source authority and current applicability require review.

## Classified topics

| Classification | Topic and ID | Retrieval purpose | Main material limit |
| --- | --- | --- | --- |
| Background | [Portal purpose](background/KT-portal-purpose.md) — `KT-portal-purpose` | Understand capability boundaries, terms, and the portal journey. | Draft principles and roadmap proposals need applicable decisions. |
| Architecture | [Frontend composition](architecture/KT-frontend-composition.md) — `KT-frontend-composition` | Understand the four MFE layers, shared modules, ownership, and onboarding. | Target composition and dependency rules require review. |
| Architecture | [Portal service relationships](architecture/ARC-portal-service-relationships.md) — `ARC-portal-service-relationships` | Trace documented ingress, BFF, SDK, and RATAN authentication responsibilities. | Intended architecture authority and supported scope require review. |
| Security | [Authentication and sessions](security/KT-authentication-and-sessions.md) — `KT-authentication-and-sessions` | Trace sign-in policy, session ceilings, renewal, and the portal logout target. | Obtain the ICS policy source and review the target with RATAN. Actual conformance belongs in the task gap record. |
| Security | [SDK and entitlements](security/KT-sdk-and-entitlements.md) — `KT-sdk-and-entitlements` | Trace entitlement handling, tile validation triggers, and permission changes in the UI and APIs. | Effective cache configuration and deployed behavior require verification. |
| Security | [CES migration parity](security/KT-ces-migration-parity.md) — `KT-ces-migration-parity` | Map permission identities, frontend compatibility, tile provider selection, account scope, and the FMO exception. | Candidate intent does not establish executed migration parity or publication approval. |
| Operations | [Admin and onboarding](operations/KT-admin-and-onboarding.md) — `KT-admin-and-onboarding` | Connect tenant provisioning, administrator read access, tile reference rules, and maker-checker review. | Reference rules for metadata without tile ownership and current operating procedures require review. |
| Operations | [Release operations](operations/KT-release-operations.md) — `KT-release-operations` | Connect readiness, configuration promotion, and technical versus business activation. | Release duration and urgent-release approval rules remain unresolved. |
| Interoperability | [Application interoperability](interoperability/KT-application-interoperability.md) — `KT-application-interoperability` | Understand OpenFin, contexts, intents, and application handoff. | POC status, contract versions, and compatibility remain unconfirmed. |
| Observability | [Observability and performance](observability/KT-observability-and-performance.md) — `KT-observability-and-performance` | Trace API loading, user activity analytics, CPO usage review, and production retention. | Measurement conditions, analytics fields, and the full reader policy require review. |
| Evolution | [Architecture evolution](evolution/KT-architecture-evolution.md) — `KT-architecture-evolution` | Understand library research, notification experiments, and platform proposals. | Adoption, supersession, licensing, and decision authority remain unresolved. |
| Settlement | [Cash Settlement auto-netting](settlement/KT-settlement-auto-netting.md) — `KT-settlement-auto-netting` | Trace rule matching, scheduled execution, grouping, and resultant cashflow handling. | Calendar, late-arrival, and exception variants need domain-owner review. |

Each topic links related topics and cites source sections or line ranges.
Registry references provide declared context.
They do not establish runtime integration.

## Portal-entry clarification

The user selected [entry denial](security/KT-sdk-and-entitlements.md#current-user-stated-portal-entry-rule) without a registered application entity entitlement.
The user selected all portal environments: local, test, UAT, and production.
The [clarification stage](../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#ui-q-002) preserves both answers and the conflicting historical proposal.
The user identifies `portal team` as the entry-policy owner only. Owner approval remains unconfirmed.
When a tile has no configured EMS2 entity, the user selected [hidden tiles and denied direct launch](security/KT-sdk-and-entitlements.md#current-user-stated-empty-entity-rule).

The user identifies `portal team` as that rule's owner across local, test, UAT, and production.
Owner approval remains unconfirmed.
The user also selected [empty-subject access through one configured entity](security/KT-sdk-and-entitlements.md#current-user-stated-empty-subject-rule).
The portal team owns this rule across local, test, UAT, and production.
Multiple-entity matching remains unresolved.
The security topics and onboarding record remain candidate drafts.

## Intended session renewal

[Active-session renewal](requirements/REQ-active-session-renewal.md#intended-scope) defines the requested ideal target behavior.
The 12 November clarification sets a 15-minute idle ceiling and a 60-minute absolute ceiling. Eligible activity can renew the session within those limits.
The [session topic](security/KT-authentication-and-sessions.md#intended-session-renewal) connects that target with documented session concepts.
The requirement and topic remain candidate drafts. Human publication review remains pending.
The independent [intent-to-reality gap record](../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md) holds implementation comparisons, observations, and operational disposition.
Those facts do not redefine the intended behavior.

## Use the map for a new requirement

Use the [single question document](../../tasks/ui-test-coverage-20261022/05-knowledge-questions.md) for current knowledge clarification.
It preserves earlier user answers and links the 12 November decisions to candidate versions and remaining review limits.

For a new tenant application, start with frontend composition and admin onboarding.
Follow security links for login, token validation, entitlements, and application permission responsibilities.
Use release operations for promotion and activation context.
Use observability for measurement intent and interoperability when applications exchange context.

Derive measurable Gherkin scenarios only after resolving relevant rules and source applicability.
Keep new intent separate from historical source statements.
Use [govern-knowledge](../../.agents/skills/govern-knowledge/SKILL.md) to investigate and review a candidate before publication.

## Coverage and review limits

The collection mainly covers the portal and UI platform, with an initial Cash Settlement auto-netting topic.
The wider Settlement domain and other Netting workflows need canonical review.

Missing local attachments limit diagrams, scan reports, screenshots, examples, and retained execution evidence.
External destinations were not fetched.
The [earlier review](../../docs/reviews/MARKDOWN_IMPORT_REVIEW.md) covered 118 files before this ingestion.
Its historical inventory includes 16 `Bin` files absent from the current batch.
This ingestion does not restore or cite those absent files.

Owner: unknown for source authority, unresolved rules, and coverage gaps.
Next action: identify responsible owners and resolve each topic's questions against applicable decisions and evidence.
Classification supports retrieval; actual review establishes which claims can support project sources of truth.
