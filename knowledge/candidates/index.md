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
All nine topics have `governance_state: candidate`, `status: draft`, and `owner: unknown`.
No topic has recorded human approval or verified business execution.

The batch contains 102 original Markdown files and 445,711 bytes.
The [raw manifest](../raw/manifest.yaml) identifies each retained source by its exact byte hash.
The collection uses filesystem source `portal-document-export` in the [source catalog](../../registry/sources.yaml).
Original page revisions, authorship, approval, and present applicability remain unconfirmed.

## Classified topics

| Classification | Topic and ID | Retrieval purpose | Main material limit |
| --- | --- | --- | --- |
| Background | [Portal purpose](background/KT-portal-purpose.md) — `KT-portal-purpose` | Understand capability boundaries, terms, and the portal journey. | Draft principles and roadmap proposals need applicable decisions. |
| Architecture | [Frontend composition](architecture/KT-frontend-composition.md) — `KT-frontend-composition` | Understand containers, tiles, shared modules, ownership, and onboarding. | Exact implementing revisions and accepted dependency rules require review. |
| Security | [Authentication and sessions](security/KT-authentication-and-sessions.md) — `KT-authentication-and-sessions` | Trace login, session concepts, and Entra migration boundaries. | Session timing, flag values, and persistence rules remain unresolved. |
| Security | [SDK and entitlements](security/KT-sdk-and-entitlements.md) — `KT-sdk-and-entitlements` | Understand downstream validation, entitlement handling, and application permission responsibilities. | Version applicability, bypass controls, and revocation behavior need evidence. |
| Operations | [Admin and onboarding](operations/KT-admin-and-onboarding.md) — `KT-admin-and-onboarding` | Connect tenant provisioning, configuration, roles, and maker-checker review. | Current procedures, tenant isolation, and release controls require evidence. |
| Operations | [Release operations](operations/KT-release-operations.md) — `KT-release-operations` | Connect readiness, configuration promotion, and technical versus business activation. | Release duration and urgent-release approval rules remain unresolved. |
| Interoperability | [Application interoperability](interoperability/KT-application-interoperability.md) — `KT-application-interoperability` | Understand OpenFin, contexts, intents, and application handoff. | POC status, contract versions, and compatibility remain unconfirmed. |
| Observability | [Observability and performance](observability/KT-observability-and-performance.md) — `KT-observability-and-performance` | Connect interaction events, dashboards, performance plans, and cache design. | Attribute limits conflict; historical summaries lack inspected execution evidence. |
| Evolution | [Architecture evolution](evolution/KT-architecture-evolution.md) — `KT-architecture-evolution` | Understand library research, notification experiments, and platform proposals. | Adoption, supersession, licensing, and decision authority remain unresolved. |

Each topic links related topics and cites source sections or line ranges.
Registry references provide declared context.
They do not establish runtime integration.

## Use the map for a new requirement

For a new tenant application, start with frontend composition and admin onboarding.
Follow security links for login, token validation, entitlements, and application permission responsibilities.
Use release operations for promotion and activation context.
Use observability for measurement intent and interoperability when applications exchange context.

Derive measurable Gherkin scenarios only after resolving relevant rules and source applicability.
Keep new intent separate from historical source statements.
Use [govern-knowledge](../../skills/govern-knowledge/SKILL.md) to investigate and review a candidate before publication.

## Coverage and review limits

The topics directly cite 83 distinct source documents.
The other 19 originals remain registered for retrieval and further investigation.
Registration does not mean their content has a synthesized explanation or established authority.

| Retained without direct topic citation | Files | Retrieval limit |
| --- | --- | --- |
| Empty pages or placeholders | 9 | They supply no substantive claims. |
| Attachment-dependent material | 5 | The absent artifacts hold needed detail. |
| Navigation indexes | 3 | Their substantive child pages already support topics. |
| Historical team register | 1 | Personal entries do not establish current ownership. |
| Repeated microfrontend introduction | 1 | Its main concepts already appear in frontend composition. |

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
