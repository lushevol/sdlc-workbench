# How the portal knowledge fits together

**Derived synthesis: all linked records remain candidate/draft. The wiki establishes no publication, deployment, or business acceptance.**

Generated 6 November 2026.
The wiki connects intended platform behavior across the current 12 structured knowledge records.
Start from the business journey, then follow the relevant responsibilities, policies, and unresolved boundaries.

## From common entry to application work

The portal provides a common workspace for post-trade applications while application teams retain their domain functions.
Its documented capabilities connect entry, authentication, tiles, workspaces, administration, and cross-application context.
These examples do not establish a complete application inventory.
See [portal purpose](../../candidates/background/KT-portal-purpose.md#business-purpose), candidate/draft, version 2.

Frontend composition separates Root Config, Base shell, application containers, and feature tiles.
Loading a module and requesting another application's business action are separate responsibilities.
Independent delivery still depends on agreed interfaces, context, authorization, and coordinated readiness.
See [composition and interoperability](../concepts/portal-composition-and-interoperability/index.md) and [service responsibilities](../entities/portal-service-responsibilities/index.md).

## Keep session continuity and permission meaning separate

Authentication, portal entry, tile access, and application data permissions answer different questions.
The requested session behavior supports continued eligible activity and successful renewal across the initial refresh-token expiry.
It does not authorize renewal with expired or revoked credentials.
See the [session lifecycle](../concepts/session-lifecycle/index.md) and [canonical renewal requirement](../../candidates/requirements/REQ-active-session-renewal.md#description), candidate/draft, version 7.

CES migration must preserve scoped permission meaning across different authorization concepts.
Entitlement definitions, account assignments, combined permissions, and data restrictions require separate comparison evidence.
The dated FMO exception also keeps non-production scope outside production denominators.
See [entitlements and CES migration](../concepts/entitlements-and-ces-migration/index.md) and [migration intent](../../candidates/security/KT-ces-migration-parity.md#documented-knowledge), candidate/draft, version 1.

## Connect administration to delivery

Onboarding links frontend assets, backend routing, authentication, entitlement configuration, and portal catalog records.
Administrative maker-checker review and configuration promotion are distinct from completed release or business activation.
Upload success alone cannot establish connectivity, sign-off, UVT, or business readiness.
See [administration and release](../concepts/admin-onboarding-and-release/index.md) and [activation boundaries](../../candidates/operations/KT-release-operations.md#technical-and-business-activation), candidate/draft, version 2.

Analytics describes user interactions and UI context, while performance evidence needs separate workload and measurement limits.
Architecture research and service proposals must retain their experimental or proposed status.
See [observability](../../candidates/observability/KT-observability-and-performance.md#documented-knowledge) and [architecture evolution](../../candidates/evolution/KT-architecture-evolution.md#documented-knowledge), both candidate/draft, version 2.

## Questions that remain open

| Boundary | Why it matters | Existing question source |
| --- | --- | --- |
| Policy authority and current timing | Historical session durations do not select an applicable approved timeout policy. | [Session questions](../../candidates/security/KT-authentication-and-sessions.md#open-questions). |
| Permission mapping and failure handling | Matching names cannot establish equivalent restrictions or select an SDK failure policy. | [SDK questions](../../candidates/security/KT-sdk-and-entitlements.md#open-questions) and [migration questions](../../candidates/security/KT-ces-migration-parity.md#open-questions). |
| Shared compatibility and handoff contracts | Missing contract versions and POC evidence limit application interoperability. | [Composition questions](../../candidates/architecture/KT-frontend-composition.md#open-questions) and [interoperability questions](../../candidates/interoperability/KT-application-interoperability.md#open-questions). |
| Operating controls and service targets | Release durations, urgent-release agreement, analytics limits, and retention remain unresolved. | [Release questions](../../candidates/operations/KT-release-operations.md#open-questions) and [observability questions](../../candidates/observability/KT-observability-and-performance.md#open-questions). |

Owners remain unknown unless the canonical clarification names one for a specific rule.
This overview preserves existing questions and supplies no missing policy answer.
Return to the [wiki index](../index.md) for all source summaries and topic routes.
