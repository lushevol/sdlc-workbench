---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-portal-purpose.md", "summaries/ARC-portal-service-relationships.md", "summaries/KT-sdk-and-entitlements.md"]
description: "How downstream services obtain a user's entitlements from EMS2 or CES, including provider-union checks and entity fields."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Entitlement retrieval

## Definition

Entitlement retrieval is the process by which a downstream service obtains a user's entitlement data — the application entities, roles, subjects, and actions that define what the user may access. It is distinct from [[concepts/single-ui-sdk-authentication]], which establishes *who* the caller is; entitlement retrieval establishes *what* the caller may reach.

## Two retrieval paths

The [[entities/single-ui-sdk]] version 1.1.4 document provides two documented paths:

1. **Direct service query** — a service calls EMS2 through `AuthorizationService.getEntitlements`. The service must maintain its own certificate and endpoint configuration, including account lookup and entitlement-list endpoints.
2. **Entitlement token extraction** — a service validates and extracts a separate entitlement token through `JwtTokenUtil.getEntitlementsToken`.

The guides explicitly forbid using an entitlement token for authentication or login. This mirrors the wider rule that authentication tokens and entitlement tokens are different artifacts with different trust roles.

The [[entities/ems2]] object model supplies the vocabulary: entities, roles, subjects, and actions. The onboarding procedure creates those objects and assigns actions to role-and-subject combinations, which together form the entitlement context for application-specific checks. Creating the objects does not by itself prove that any backend evaluates them.

## Access through request context

The SDK's request filter exposes user context through the `userInfo` request attribute. Across versions the entitlement field evolved:

- Version 1.0.0 exposed `userEntitlements`.
- Version 1.1.1 renamed it to `entitlements`.
- Version 1.1.4 exposes `userId`, `entitlements`, `oud`, and `sessionId` through `userInfo`.

A service may also constrain retrieval by supplying an application entity list, and the documented sample separates initial entitlement storage from later application requests.

## Caching and lifecycle

The SDK overview recommends entitlement caching and mentions NGINX stickiness for multiple endpoints. Version 1.1.4 documents logout session rejection and configurable public certificates.

The current candidate requires UI permission revocation at the next login. Protected API calls must reflect revocation after expiry of the applicable Auth Server Redis entry. The entitlement cache expires after one hour and the JWT parsing cache after two hours. Cache selection and interaction for each API, entitlement freshness at UI validation events, and revocation in an already-open tab remain open. [UI-ENTITLEMENT-REVOCATION-AC-001](../../../records/candidates/security/KT-sdk-and-entitlements.md#ui-entitlement-revocation-ac-001) · [API-ENTITLEMENT-REVOCATION-AC-001](../../../records/candidates/security/KT-sdk-and-entitlements.md#api-entitlement-revocation-ac-001)

Logout separately targets immediate revocation of all of the user's portal sessions. Verification across service instances requires deployment and execution evidence. [PORTAL-LOGOUT-AC-001](../../../records/candidates/security/KT-authentication-and-sessions.md#portal-logout-ac-001)

## Migration to CES

During the CES migration, EMS2 entity `X_RATANONE` was renamed to [[entities/ces]] application `RATAN_ENTITLEMENT_RULE`. The user clarification confirms a *name correspondence only*. It does not establish equivalent entity, application, subject, or role numeric identifiers, and it does not establish role equivalence, deployment status, or publication approval.

For SDK version `3.0.0`, the user requires the old contract be preserved where possible with a full compatibility assessment. Concretely:

- The returned permission map must contain zero missing and zero unsupported additional role-scoped permissions, with each subject and action retaining its required legacy meaning.
- The SDK caller supplies the FMAA token; the SDK uses it as the bearer credential and makes zero independent FMAA token-acquisition requests.

Unmapped or unsupported meaning remains a compatibility gap for explicit review. The compatibility objective does not authorize invented role attribution or a silently changed permission contract.

Mapped definitions are compared through the [[concepts/ems2-to-ces-permission-mapping]]: EMS2 Role maps to CES Entitlement, Entity to Application, Subject to Feature, and Action to Action. Names shared by different applications do not establish equivalent permissions, and numeric source identifiers may differ without changing mapped permission meaning. See [[summaries/KT-ces-migration-parity]].

### Provider-union reads through existing calls

The provider-union clarification of 9 November 2026 extends retrieval intent: an existing `hasPermission(code)` call may accept a mapped grant supplied by either EMS2 or CES, or by both. The caller passes only the code, and the number of required additional caller arguments stays at zero. Every accepted decision must log which provider supplied the matching grant; a denial logs no accepted-grant source because neither provider matched.

This shared functional check is governed by [[concepts/permission-check-provider-union]] and is separate from tile admission. Whether a tile is admitted is decided per provider under [[concepts/per-tile-provider-selection]], so a provider-union permission result does not by itself select or change a tile's admission provider. Reviewed application, feature, and action mappings are required to read either provider; the union rule does not supply them.

### CES entitlement names and application identity in returned entities

The BFF field decision requires two new fields on EMS3 entities returned downstream:

- `roleList` carries the corresponding CES `entitlements.entitlement_name` values, bound to that entity's own application; names belonging to another application must not populate it.
- `applicationId` carries the corresponding CES application `itam_id`, for example `"51358"` for the RATAN mapping.

For that mapping, the existing `name` field is `RATAN_ENTITLEMENT_RULE`, the existing `applicationName` field retains the legacy team label `RATAN`, and the new `applicationId` field is `"51358"`. CES `user_data.app_name` supplies the CES authorization name, not the legacy team label. The additions must remove zero existing entity fields and change zero legacy EMS2 decisions. They expose assignment names and application identity; they do not resolve scalar role semantics.

### Role multiplicity in retrieved data

Multiple CES assignments may name several entitlements. Retrieval must not present that set as one proven assigned role, and no arbitrary or inferred scalar role may be fabricated from effective action membership. Callers that require a single role need a sourced business mapping under [[concepts/ces-role-multiplicity]]. Consequently, CES saved-view and filter writes that require one owner role remain deferred pending an ownership rule, while existing EMS2 role-owned write behavior is preserved.

## Relationship to portal and tile authorization

Entitlement retrieval feeds [[concepts/portal-entry-and-tile-authorization]], but the two are not the same decision. Portal entry and tile visibility are portal-side decisions; data access and editing permissions belong to each tile application. A visible tile does not establish permission to read or modify its business data.

This boundary matters because the SDK guides primarily describe validation and entitlement retrieval. They do not establish automatic subject-and-action enforcement for every API. Assuming enforcement exists can leave protected business actions unspecified. The per-tile provider rule reinforces the boundary: an EMS2 tile retains its existing admission logic while a CES tile uses CES admission logic, configured application identity, and CES permission structure, and one tile's change forces zero provider changes on the others.

## Evidence limits

- No downstream service execution or compatibility build was inspected for the source topic.
- The applicable artifact and configuration for each consumer remain unresolved — versions range from `1.1.4-java8` and `1.1.4-java17` to a conditional `2.0.0-SNAPSHOT` for Spring Boot 4.0.6.
- The overview announces removal of EMS2 details from authentication JWTs in DEV on 30 August 2024, but no retained proof establishes the present DEV or production token shape.
- Which CES data preserves each legacy role-specific grant for SDK 3.0.0 is an open question.
- The provider-union clarification states intended rule behavior only. It does not prove implementation or deployed log collection, and its expectation about returned legacy entities remains an implementation question.
- The `roleList` and `applicationId` decision states target metadata. It does not establish implemented, tested, or deployed response behavior.
- CES role-owned writes are deferred, not defined; CES ownership, query, and exclusion semantics remain open.

Owner: unknown. Next action: map each consumer to its artifact, configuration, and retained verification evidence, confirm where each application performs its own subject-and-action checks, and bind the provider-union and entity-field rules to reviewed application, feature, and action mappings.

## Related

- [[summaries/KT-sdk-and-entitlements]]
- [[summaries/KT-ces-migration-parity]]
- [[concepts/single-ui-sdk-authentication]]
- [[concepts/ems2-to-ces-permission-mapping]]
- [[concepts/permission-check-provider-union]]
- [[concepts/per-tile-provider-selection]]
- [[concepts/ces-role-multiplicity]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[entities/single-ui-sdk]]
- [[entities/ems2]]
- [[entities/ces]]
- [[entities/ems3]]
- [[entities/mfe-base]]
- [[entities/mfe-ratan-container]]
- [[entities/fmo-post-trade-portal]]
- [[entities/portal-team]]

See also: [[summaries/ARC-portal-service-relationships]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-admin-and-onboarding]]

See also: [[summaries/KT-release-operations]]

See also: [[summaries/KT-authentication-and-sessions]]
