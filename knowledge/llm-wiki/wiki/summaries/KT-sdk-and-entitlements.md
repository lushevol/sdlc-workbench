---
type: "Summary"
description: "SDK integration, entitlement retrieval, CES migration, and portal entry rules."
doc_type: short
full_text: "sources/KT-sdk-and-entitlements.md"
---

> Derived from [KT-sdk-and-entitlements, version 8](../../../candidates/security/KT-sdk-and-entitlements.md), candidate/draft. [Source bindings](../../source-manifest.json).

# SDK and Entitlements

## Overview
This topic connects [[concepts/single-ui-sdk-authentication]] with [[concepts/entitlement-retrieval]] and the boundary between portal tile access and application data permissions. It separates documented SDK behavior from user-stated policy intent and from unverified deployment or approval evidence.

## Key concepts
- [[concepts/single-ui-sdk-authentication]]: The [[entities/single-ui-sdk]] injects an HTTP request filter that validates Single UI JWTs and exposes user context through the `userInfo` request attribute.
- [[concepts/entitlement-retrieval]]: Services can query [[entities/ems2]] through `AuthorizationService.getEntitlements` or extract a separate entitlement token through `JwtTokenUtil.getEntitlementsToken`. An entitlement token must not be used for authentication or login.
- Portal entry policy: An authenticated SC user with no entitlement for any registered application entity must be denied portal entry in local, test, UAT, and production. This is user-stated intent only.
- Tile security and empty configuration: Empty EMS2 entity configuration hides the tile and denies direct launch; empty subject configuration allows visibility and launch through the tile's one configured entity. Portal access remains separate from application data permissions.
- CES entitlement migration: EMS2 `X_RATANONE` was renamed to CES `RATAN_ENTITLEMENT_RULE`. The clarification confirms a name correspondence only, not identifier or role equivalence.

## Documented SDK behavior and versions
- Version 1.0.0 documents artifact `com.scb.ratan:single-ui-sdk-starter`, configuration prefix `single-ui-sdk.auth`, optional `user-login-max-duration`, and request context field `userEntitlements`.
- Version 1.1.1 renames the artifact to `com.scb.fmoportal:fmoportal-auth-sdk`, removes the duration property, and renames the field to `entitlements`.
- Version 1.1.2 adds `max_age` validation and `oud` in request context.
- Version 1.1.4 documents logout session rejection and configurable public certificates. Its Java guides expose `userId`, `entitlements`, `oud`, and `sessionId` through `userInfo`.
- Declared variants include Java 8 `1.1.4-java8` with Spring Boot 2.6.6 or higher, Java 17 `1.1.4-java17` with Spring Boot 3.1.2 or higher, and a Boot 4 migration note for `2.0.0-SNAPSHOT` on Spring Boot 4.0.6. An official `2.0.0` release remains conditional on regression testing.
- The URL algorithm checks exclusions first. With an empty inclusion list, all remaining paths are validated; otherwise only matching inclusion paths are validated. `skip-jwt-headers` can bypass JWT checks, but the documents do not identify a trusted replacement control.

## SDK 3.0.0 CES migration intent
The user selected SDK version `3.0.0`. The migration must preserve the old contract where possible and assess complete compatibility. The SDK caller supplies the FMAA token, and tests are required. Failure handling remains unresolved and open to engineering suggestions.

Acceptance criteria record the intent:
- `SDK-CES-INTENT-AC-001`: the returned permission map must contain zero missing and zero unsupported additional role-scoped permissions while preserving subject and action meaning.
- `SDK-CES-INTENT-AC-002`: the SDK must use the caller-supplied FMAA token as its bearer credential and make zero independent FMAA token-acquisition requests.

These criteria do not prove that [[entities/ces]] responses contain sufficient role information, and unmapped meaning remains a compatibility gap for explicit review.

## Portal and tile policy criteria
- `UI-ENTRY-AC-001`: deny entry when an authenticated SC user has no entitlement for any registered application entity. No HTTP status, denial wording, or timing limit is specified.
- `UI-EMPTY-ENTITY-AC-001`: hide the tile and deny direct launch when the tile has zero configured EMS2 entities.
- `UI-EMPTY-SUBJECT-AC-001`: when the tile has one configured EMS2 entity and zero configured subjects, show the tile and authorize launch when the user has entitlement for that entity.

All three are business criteria recording user-stated intent. They are not approved policy, executable results, or evidence of deployed enforcement. The [[entities/portal-team]] is identified as owner across local, test, UAT, and production, but authority and approval remain unconfirmed.

## Entitlement lifecycle and risks
The SDK overview recommends entitlement caching and mentions NGINX stickiness for multiple endpoints. It also announces removal of EMS2 details from authentication JWTs in DEV on 30 August 2024, but that announcement does not establish the present DEV state or any production token shape.

Caching creates unresolved questions about stale permissions, cache expiry, and cross-instance logout propagation. The guides describe validation and entitlement retrieval, but they do not establish automatic subject-and-action enforcement for every application API.

## Evidence limits and open questions
- No downstream service execution or SDK compatibility build was inspected. The artifact and configuration for each consumer remain unresolved.
- Portal-team authority, approval, and deployed enforcement of the entry, empty-entity, and empty-subject rules remain unverified.
- Which CES data preserves each legacy role-specific grant for SDK 3.0.0 compatibility?
- Which failure-handling contract should SDK 3.0.0 callers use?
- What trusted control replaces JWT validation on excluded paths or configured skip headers?
- Where does each downstream service enforce subject and action permissions?
- Which current environments remove entitlements from authentication tokens?

## Related pages
Authentication and sessions, admin and onboarding, the registered SDK source copy `single-ui-auth-sdk`, the contracts `single-ui-sdk-jwt-validation`, `single-ui-sdk-request-context`, `single-ui-sdk-entitlement-lookup`, the authentication runtime baseline, and the active session renewal requirement provide related context. See also [[concepts/portal-entry-and-tile-authorization]] and [[entities/fmo-post-trade-portal]].