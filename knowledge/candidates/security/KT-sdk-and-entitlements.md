---
type: KnowledgeTopic
id: KT-sdk-and-entitlements
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single
    UI SDK V1.0.0/page.md
  revision: sha256:e5163aac85b0e1bbc346bb0405ed639e71bb7806850c20202352b7ab065c2a7d
  sha256: e5163aac85b0e1bbc346bb0405ed639e71bb7806850c20202352b7ab065c2a7d
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single
    UI SDK V1.1.1/page.md
  revision: sha256:4156b1d5319151e5a642d942f9777c675a40726ce82fdb1e29fade0a69b30302
  sha256: 4156b1d5319151e5a642d942f9777c675a40726ce82fdb1e29fade0a69b30302
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single
    UI SDK V1.1.2/page.md
  revision: sha256:11beac7892fec3e0f706059917d6c38a966880c4e31820348018afeceef58767
  sha256: 11beac7892fec3e0f706059917d6c38a966880c4e31820348018afeceef58767
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single
    UI SDK V1.1.4/page.md
  revision: sha256:7feb80396e60776c59b08cf322f87622f1b8484a4867d0caaaa9b0404fc873de
  sha256: 7feb80396e60776c59b08cf322f87622f1b8484a4867d0caaaa9b0404fc873de
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single
    UI SDK V1.1.4/Java 17/page.md
  revision: sha256:2f03fd4633f811b5157b63cd29c00b7164b812cb6d655bfb922e86551fcafe1b
  sha256: 2f03fd4633f811b5157b63cd29c00b7164b812cb6d655bfb922e86551fcafe1b
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single
    UI SDK V1.1.4/Java 8/page.md
  revision: sha256:3bb48be50df05fad5eccd6dad33a8d83aa96bf94390e020d42aac3451690fe72
  sha256: 3bb48be50df05fad5eccd6dad33a8d83aa96bf94390e020d42aac3451690fe72
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single
    UI SDK V1.1.4/Java 17/Migration to Boot 4.0.6/page.md
  revision: sha256:c593670a77fc1c64beda9d952190c9f15d206ebc0087f36192dde77cfc3be982
  sha256: c593670a77fc1c64beda9d952190c9f15d206ebc0087f36192dde77cfc3be982
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md
  revision: sha256:d02c07de868b566d9b2f48e011e25b1782ab63423a1bf7759c7a37278cabc3bf
  sha256: d02c07de868b566d9b2f48e011e25b1782ab63423a1bf7759c7a37278cabc3bf
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and
    Document/Tile Security Control - EMS2/page.md
  revision: sha256:c31667decd8004d56d2244353cfae71b4d3e3fbe4668d43b3cec2c34a4198613
  sha256: c31667decd8004d56d2244353cfae71b4d3e3fbe4668d43b3cec2c34a4198613
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Creating EMS2 Entity Role Subject Action/page.md
  revision: sha256:e55b2b4df69be6340dfd38f59083f31c71abb0464cbe152573f60079ab3dc4b7
  sha256: e55b2b4df69be6340dfd38f59083f31c71abb0464cbe152573f60079ab3dc4b7
generated:
  by: agent:codex
  at: '2026-10-15T00:38:52.657060+00:00'
verified: []
classification: security
scope: Downstream authentication SDK integration, entitlement retrieval, and documented application authorization
  boundaries.
summary: The SDK validates authentication tokens and exposes entitlement information; application permission enforcement
  remains a separate responsibility.
related:
- KT-authentication-and-sessions
- KT-admin-and-onboarding
- single-ui-auth-sdk
- single-ui-authentication
- single-ui-sdk-jwt-validation
- single-ui-sdk-request-context
- single-ui-sdk-entitlement-lookup
open_questions:
- Which SDK artifact and configuration apply to each downstream service?
- What trusted control replaces JWT validation on excluded paths or configured skip headers?
- Where does each downstream service enforce subject and action permissions?
- Which current environments remove entitlements from authentication tokens?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# SDK and entitlements

## Scope

This topic connects SDK integration instructions with entitlement retrieval and application permission responsibilities.
The materials cover several SDK generations and migration plans.
They do not establish the SDK versions or security controls deployed by individual services.

## Summary

The SDK guides describe a request filter that validates portal authentication tokens.
They expose user context and separate methods for entitlement retrieval.
The materials distinguish authentication tokens from entitlement tokens.
Application-level data permissions remain separate from portal tile visibility.

## Documented knowledge

### Integration purpose and responsibility boundary

The SDK injects an HTTP request filter into a downstream Spring application.
The guides describe automatic validation of JWTs generated by the Single UI authentication service.
Successful validation exposes user information through the request attribute `userInfo`.
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

The tile-security proposal distinguishes portal entry from permission to view individual tiles.
It assigns data access and editing permissions to each tile application.
A visible tile therefore does not establish permission to read or modify its business data.
This is a proposed responsibility boundary; current enforcement requires separate evidence.
[Tile security proposal, lines 1–23](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md>)

EMS2 setup defines entities, roles, subjects, and actions.
The procedure creates those objects and assigns actions to role-and-subject combinations.
Those objects provide entitlement context for application-specific checks.
The procedure alone does not prove that a backend performs those checks.
[EMS2 setup procedure, lines 1–12](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Creating EMS2 Entity Role Subject Action/page.md>)

### Version and configuration history

Version 1.0.0 documents artifact `com.scb.ratan:single-ui-sdk-starter` and configuration prefix `single-ui-sdk.auth`.
It includes optional `user-login-max-duration` and request context field `userEntitlements`.
Version 1.1.1 renames the artifact to `com.scb.fmoportal:fmoportal-auth-sdk`.
It removes that duration property and renames the field to `entitlements`.
[SDK version 1.0.0, lines 3–8, 14–51, 69–85](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.0.0/page.md>)
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

Version 1.1.2 documents `max_age` validation and adds `oud` to request context.
Version 1.1.4 documents logout session rejection and configurable public certificates.
Its Java guides expose `userId`, `entitlements`, `oud`, and `sessionId` through `userInfo`.
These version statements require matching against each consumer's actual dependency.
[SDK version 1.1.2, lines 5–15, 27–45](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.2/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

| Documented variant | Declared platform | Declared artifact version |
| --- | --- | --- |
| Java 8 guide | JDK 8; Spring Boot 2.6.6 or higher | `1.1.4-java8` |
| Java 17 guide | JDK 17; Spring Boot 3.1.2 or higher | `1.1.4-java17` |
| Boot 4 migration note | Spring Boot 4.0.6 | `2.0.0-SNAPSHOT` |

The Boot 4 note conditions an official `2.0.0` release on regression testing.
It describes separated JWT configuration, public-key configuration, and import changes.
It does not establish a completed release or consumer compatibility.
[Java 8 SDK guide, lines 3–21, 25–59](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 8/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)
[Boot 4 migration note, lines 1–28](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/Migration to Boot 4.0.6/page.md>)

### Protected requests and exceptions

The documented URL algorithm checks exclusions first.
With an empty inclusion list, it validates all remaining paths.
Otherwise, it validates matching inclusion paths.
Configuration therefore determines which requests receive SDK authentication checks.
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

The examples also configure `skip-jwt-headers`.
Earlier guides state that matching headers cause the SDK to skip JWT checks.
The supplied instructions do not identify a trusted replacement authentication control.
[SDK version 1.0.0, lines 3–8, 14–51, 69–85](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.0.0/page.md>)
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

### Entitlement retrieval and lifecycle

Version 1.1.4 provides two entitlement retrieval paths.
A service can query EMS2 through `AuthorizationService.getEntitlements`.
Alternatively, it can validate and extract a separate entitlement token through `JwtTokenUtil.getEntitlementsToken`.
The guide explicitly forbids using an entitlement token for authentication or login.
[SDK version 1.1.4, lines 7–46](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/page.md>)

Direct EMS2 consumers must maintain certificate and endpoint configuration.
The Java 17 guide documents account lookup and entitlement-list endpoints.
It permits an application entity list to constrain retrieval.
Its sample separates initial entitlement storage from later application requests.
[SDK version 1.1.4, lines 7–46](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

The SDK overview recommends entitlement caching and mentions NGINX stickiness for multiple endpoints.
It announces removal of EMS2 details from authentication JWTs in DEV on August 30, 2024.
That announcement cannot establish the present DEV state or any production state.
[SDK overview, lines 1–15](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md>)

## Connections

[Authentication and sessions](KT-authentication-and-sessions.md) explains portal token issuance and session concepts.
[Admin and onboarding](../operations/KT-admin-and-onboarding.md) explains EMS2 setup and tile configuration.

Repository `single-ui-auth-sdk` identifies the registered SDK source copy.
Contracts `single-ui-sdk-jwt-validation`, `single-ui-sdk-request-context`, and `single-ui-sdk-entitlement-lookup` provide declared implementation context.
Those identities do not establish deployed consumers, compatible keys, or application permission enforcement.

## Evidence limits

The version guides include examples and historical changes without confirmed original revisions or approval authority.
No downstream service execution or SDK compatibility build was inspected for this topic.
The applicable artifact and runtime behavior remain unresolved.
Owner: unknown.
Next action: map each consumer to its dependency, configuration, and retained verification evidence.

The tile-security proposal delegates data permissions to applications, but the SDK guides primarily describe validation and entitlement retrieval.
They do not establish automatic subject-and-action enforcement for every API.
Assuming enforcement can leave protected business actions unspecified.
Owner: unknown.
Next action: inspect each application's permission checks and denied-request assertions.
[Tile security proposal, lines 1–23](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

## Open questions

Which control authenticates requests when exclusions or skip headers bypass JWT validation?
The examples identify bypass settings without their trust boundary.
This prevents a complete account of protected-request behavior.
Owner: unknown.
Next action: document the trusted caller, replacement control, and bypass rejection tests.
[SDK version 1.0.0, lines 3–8, 14–51, 69–85](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.0.0/page.md>)
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

How do applications invalidate cached entitlements and reject logged-out sessions across instances?
The overview recommends caching; version 1.1.4 describes session rejection without distributed lifecycle guarantees.
Stale permissions and inconsistent logout remain unresolved possibilities.
Owner: unknown.
Next action: define cache expiry, revocation propagation, and observable cross-instance acceptance criteria.
[SDK overview, lines 1–15](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

Which environments currently omit entitlements from authentication tokens?
The overview announces a specific DEV migration in 2024.
It provides no retained proof of current production token shape.
Owner: unknown.
Next action: inspect redacted token contracts and environment-specific migration records.
[SDK overview, lines 1–15](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md>)
