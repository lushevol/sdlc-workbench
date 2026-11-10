# Portal knowledge wiki

**Derived navigation: all 12 source records remain candidate/draft. No record has publication approval from wiki generation.**

Generated 6 November 2026. Refreshed 10 November 2026 with the project [llm-wiki skill](../../.agents/skills/llm-wiki/SKILL.md).
Start with the [living overview](overview/index.md) to understand how the topics connect.
Reopen each canonical record before using its claims for engineering decisions.
The [classified knowledge map](../candidates/index.md) retains the original topic organization and current clarification links.

## Read by question

| Question | Wiki route |
| --- | --- |
| What does the portal provide, and how do applications join it? | [Composition and interoperability](concepts/portal-composition-and-interoperability/index.md). |
| Which components own the intended frontend and backend responsibilities? | [Portal service responsibilities](entities/portal-service-responsibilities/index.md). |
| How do authentication, entry, renewal, and token boundaries connect? | [Session lifecycle](concepts/session-lifecycle/index.md). |
| How do portal access and CES migration preserve permission meaning? | [Entitlements and CES migration](concepts/entitlements-and-ces-migration/index.md). |
| How do onboarding, configuration review, release, and activation connect? | [Administration, onboarding, and release](concepts/admin-onboarding-and-release/index.md). |

## Source summaries

Each source page summarizes one canonical structured record.
The term source here identifies a knowledge record, rather than every retained raw snapshot behind it.
All source pages preserve their canonical ID, version, state, useful rules, and unresolved questions.

| Record | Source summary | Canonical record |
| --- | --- | --- |
| KT-portal-purpose | [Portal purpose](sources/KT-portal-purpose/index.md) | [Versioned topic](../candidates/background/KT-portal-purpose.md). |
| KT-frontend-composition | [Frontend composition](sources/KT-frontend-composition/index.md) | [Versioned topic](../candidates/architecture/KT-frontend-composition.md). |
| ARC-portal-service-relationships | [Service relationships](sources/ARC-portal-service-relationships/index.md) | [Versioned architecture](../candidates/architecture/ARC-portal-service-relationships.md). |
| KT-authentication-and-sessions | [Authentication and sessions](sources/KT-authentication-and-sessions/index.md) | [Versioned topic](../candidates/security/KT-authentication-and-sessions.md). |
| REQ-active-session-renewal | [Active-session renewal](sources/REQ-active-session-renewal/index.md) | [Versioned requirement](../candidates/requirements/REQ-active-session-renewal.md). |
| KT-sdk-and-entitlements | [SDK and entitlements](sources/KT-sdk-and-entitlements/index.md) | [Versioned topic](../candidates/security/KT-sdk-and-entitlements.md). |
| KT-ces-migration-parity | [CES migration and frontend compatibility](sources/KT-ces-migration-parity/index.md) | [Versioned topic](../candidates/security/KT-ces-migration-parity.md). |
| KT-admin-and-onboarding | [Administration and onboarding](sources/KT-admin-and-onboarding/index.md) | [Versioned topic](../candidates/operations/KT-admin-and-onboarding.md). |
| KT-release-operations | [Release operations](sources/KT-release-operations/index.md) | [Versioned topic](../candidates/operations/KT-release-operations.md). |
| KT-application-interoperability | [Application interoperability](sources/KT-application-interoperability/index.md) | [Versioned topic](../candidates/interoperability/KT-application-interoperability.md). |
| KT-observability-and-performance | [Observability and performance](sources/KT-observability-and-performance/index.md) | [Versioned topic](../candidates/observability/KT-observability-and-performance.md). |
| KT-architecture-evolution | [Architecture evolution](sources/KT-architecture-evolution/index.md) | [Versioned topic](../candidates/evolution/KT-architecture-evolution.md). |

## Coverage and evidence limits

Record navigation coverage: 12 of 12 current structured domain records.
Cross-source synthesis: four concept pages and one entity page connect the selected topics.
This coverage does not establish complete business-domain knowledge or a fresh review of all raw snapshots.
Source authority, policy applicability, publication, and implementation verification remain separate decisions.

Keep unanswered policy in the [existing living question document](../../tasks/ui-test-coverage-20261022/05-knowledge-questions.md).
Current intent-to-implementation gaps remain in their owning tasks, accessible through canonical records.
Owner: unknown for unresolved source authority and policy; use each record's open questions to identify the required decision.
The [refresh report](../../docs/reviews/LLM_WIKI_REFRESH_20261110.md) records the current input comparison and navigation checks.
The [generation report](../../docs/reviews/LLM_WIKI_ADOPTION_20261105.md) records scope, checks, integration coverage, and material limits.
