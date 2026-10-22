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

Start here to understand the supplied portal and UI platform materials.
Read each topic's evidence limits before using its claims for new work.
All listed domain records remain candidates after source locator and content updates.
All retain `status: draft` and `owner: unknown`.
No record has recorded human approval or verified business execution.

These records explain the portal and its business-system responsibilities.
Source snapshots and review metadata remain outside this directory.
Original source authority and current applicability require review.

## Classified topics

| Classification | Topic and ID | Retrieval purpose | Main material limit |
| --- | --- | --- | --- |
| Background | [Portal purpose](background/KT-portal-purpose.md) — `KT-portal-purpose` | Understand capability boundaries, terms, and the portal journey. | Draft principles and roadmap proposals need applicable decisions. |
| Architecture | [Frontend composition](architecture/KT-frontend-composition.md) — `KT-frontend-composition` | Understand the four MFE layers, shared modules, ownership, and onboarding. | Deployment and accepted dependency rules require review. |
| Architecture | [Portal service relationships](architecture/ARC-portal-service-relationships.md) — `ARC-portal-service-relationships` | Trace reported ingress, BFF, SDK, and RATAN authentication responsibilities. | Reported topology and local implementation have explicit differences. |
| Security | [Authentication and sessions](security/KT-authentication-and-sessions.md) — `KT-authentication-and-sessions` | Trace login, session concepts, and Entra migration boundaries. | Source parsing and timing paths are documented; effective deployment and policy review remain open. |
| Security | [SDK and entitlements](security/KT-sdk-and-entitlements.md) — `KT-sdk-and-entitlements` | Understand downstream validation, entitlement handling, and application permission responsibilities. | Source checks and bypasses are documented; consumer enforcement and global revocation remain unproved. |
| Operations | [Admin and onboarding](operations/KT-admin-and-onboarding.md) — `KT-admin-and-onboarding` | Connect tenant provisioning, configuration, roles, and maker-checker review. | Current procedures, tenant isolation, and release controls require evidence. |
| Operations | [Release operations](operations/KT-release-operations.md) — `KT-release-operations` | Connect readiness, configuration promotion, and technical versus business activation. | Release duration and urgent-release approval rules remain unresolved. |
| Interoperability | [Application interoperability](interoperability/KT-application-interoperability.md) — `KT-application-interoperability` | Understand OpenFin, contexts, intents, and application handoff. | POC status, contract versions, and compatibility remain unconfirmed. |
| Observability | [Observability and performance](observability/KT-observability-and-performance.md) — `KT-observability-and-performance` | Connect interaction events, dashboards, performance plans, and cache design. | Attribute limits conflict; historical summaries lack inspected execution evidence. |
| Evolution | [Architecture evolution](evolution/KT-architecture-evolution.md) — `KT-architecture-evolution` | Understand library research, notification experiments, and platform proposals. | Adoption, supersession, licensing, and decision authority remain unresolved. |

Each topic links related topics and cites source sections or line ranges.
Registry references provide declared context.
They do not establish runtime integration.

## Portal-entry clarification

The user selected [entry denial](security/KT-sdk-and-entitlements.md#current-user-stated-portal-entry-rule) without a registered application entity entitlement.
The user selected all portal environments: local, test, UAT, and production.
The [clarification stage](../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#ui-q-002) preserves both answers and the conflicting historical proposal.
The user identifies `portal team` as the entry-policy owner only. Owner approval and deployed enforcement remain unconfirmed.
When a tile has no configured EMS2 entity, the user selected [hidden tiles and denied direct launch](security/KT-sdk-and-entitlements.md#current-user-stated-empty-entity-rule).

The user identifies `portal team` as that rule's owner across local, test, UAT, and production.
Owner approval and deployed enforcement remain unconfirmed.
The user also selected [empty-subject access through one configured entity](security/KT-sdk-and-entitlements.md#current-user-stated-empty-subject-rule).
The portal team owns this rule across local, test, UAT, and production.
Multiple-entity matching remains unresolved.
Both security topics and the onboarding successor retain unknown topic-wide owners and candidate/draft state.

## Session policy

[Active-session renewal](requirements/REQ-active-session-renewal.md) records the requested session behavior and seven measurable scenarios.
The requirement remains a candidate. Publication requires the applicable human review.

## Use the map for a new requirement

For a new tenant application, start with frontend composition and admin onboarding.
Follow security links for login, token validation, entitlements, and application permission responsibilities.
Use release operations for promotion and activation context.
Use observability for measurement intent and interoperability when applications exchange context.

Derive measurable Gherkin scenarios only after resolving relevant rules and source applicability.
Keep new intent separate from historical source statements.
Use [govern-knowledge](../../.agents/skills/govern-knowledge/SKILL.md) to investigate and review a candidate before publication.

## Coverage and review limits

The collection mainly covers the portal and UI platform.
It does not establish complete coverage of the brownfield business domain.

Missing local attachments limit diagrams, scan reports, screenshots, examples, and retained execution evidence.
External destinations were not fetched.
The [earlier review](../../docs/reviews/MARKDOWN_IMPORT_REVIEW.md) covered 118 files before this ingestion.
Its historical inventory includes 16 `Bin` files absent from the current batch.
This ingestion does not restore or cite those absent files.

Owner: unknown for source authority, unresolved rules, and coverage gaps.
Next action: identify responsible owners and resolve each topic's questions against applicable decisions and evidence.
Classification supports retrieval; actual review establishes which claims can support project sources of truth.
