---
title: "SDK and entitlements"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/security/KT-sdk-and-entitlements.md
source: raw/workbench/knowledge/candidates/security/KT-sdk-and-entitlements.md
source_hash: 60ec27600b3c79ec
last_updated: 2026-11-11
candidate_id: KT-sdk-and-entitlements
candidate_version: 8
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: security
workbench_origin: knowledge/candidates/security/KT-sdk-and-entitlements.md
workbench_sha256: 60ec27600b3c79ec02b3dd5397e18037aed9d9857c7a30e6c6cc304822b93115
workbench_status: candidate-derived
---

# SDK and entitlements

## Scope

This topic connects SDK integration instructions with entitlement retrieval and application permission responsibilities.
The materials cover several SDK generations and migration plans.
They do not establish the SDK versions or security controls deployed by individual services.

## Summary

The [code baseline](../../../../tasks/portal-background-session-20261019/evidence/authentication/ARCH-authentication-runtime-baseline.md) records implemented behavior at exact repository revisions.
This topic retains document statements separately from that source-backed investigation.

The SDK guides describe a request filter that validates portal authentication tokens.
They expose user context and separate methods for entitlement retrieval.
The materials distinguish authentication tokens from entitlement tokens.
Application-level data permissions remain separate from portal tile visibility.

For all portal environments, the user selected denial when an authenticated SC user lacks any registered application entity entitlement.
The [entry answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-source.json) and [scope answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-scope-source.json) establish user-stated intent only.
Policy-owner authority and deployed enforcement remain unverified.

## Documented knowledge

### User-confirmed EMS2 to CES name migration

The user confirms that EMS2 `X_RATANONE` was renamed to CES `RATAN_ENTITLEMENT_RULE` during migration.
The [exact clarification](../../../../tasks/ces-entitlement-migration-20261102/evidence/user-input-20261030-field-equivalence.txt) is the high-priority reference, dated 30 October 2026.
This statement resolves the name correspondence for that migration scope.
It does not establish equivalent entity, application, subject, or role numeric identifiers.
It also does not establish role equivalence, deployment status, or publication approval.
The [field mapping](../../../../tasks/ces-entitlement-migration-20261102/03-output-mapping.md) separates these names from each system's identifier structures.
Owner: unknown. Next action: retain that distinction when mapping consumers and permission definitions.

### SDK 3.0.0 CES migration intent

The user selects `3.0.0` as the SDK migration version.
The SDK must preserve the old contract where possible and assess complete compatibility.
The SDK caller supplies the FMAA token. The user also requests tests.
The [exact clarification](../../../../evidence/knowledge/sources/user-clarifications/single-ui-sdk-ces-migration-20261101/user-clarification-implementation.md#exact-user-input) controls this scope from 1 November 2026.

This target preserves the meaning of existing role, subject, and action permission checks where supported CES evidence permits.
The compatibility objective does not authorize invented role attribution, extra grants, or a silently changed permission contract.
Unmapped or unsupported meaning remains a compatibility gap for explicit review.
The [migration task](../../../../tasks/single-ui-sdk-ces-migration-20261101/10-change-review.md) holds the separate implementation and conformance evidence.

#### SDK-CES-INTENT-AC-001

```gherkin
Feature: Preserve the SDK permission contract during CES migration
  @SDK-CES-INTENT-AC-001
  Scenario: Preserve equivalent role-scoped permissions
    Given CES supplies the same role-scoped permissions required by the old SDK contract
    When SDK version "3.0.0" returns the caller's permission map
    Then the map contains 0 missing role-scoped permissions
    And the map contains 0 unsupported additional role-scoped permissions
    And each subject and action retains its required legacy meaning
```

The missing and unsupported additional permission counts must each equal zero for the declared comparison scope.
This criterion does not assert that every CES response contains sufficient role information.

#### SDK-CES-INTENT-AC-002

```gherkin
Feature: Use the SDK caller's FMAA token
  @SDK-CES-INTENT-AC-002
  Scenario: Authenticate a CES request with the supplied token
    Given the SDK caller supplies one valid FMAA token for its CES request
    When SDK version "3.0.0" requests that caller's configured CES entitlement scope
    Then the request uses that supplied token as its bearer credential
    And the SDK makes 0 independent FMAA token-acquisition requests
```

The bearer credential must equal the caller-supplied token. Independent token-acquisition requests must total zero.
The input requests failure-handling suggestions. It does not select a failure policy or approve a proposed recommendation.
Owner: unknown. Next action: review the proposed caller contract without treating implementation choices as approved policy.

### Current user-stated portal-entry rule

An authenticated SC user with no entitlement for any registered application entity must be denied portal entry.
The user selected local, test, UAT, and production environments.
The selection defines no HTTP status, denial wording, or additional entity-versus-role semantics.
The [owner answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-owner-source.json) identifies `portal team` for this policy only.
User identity and applicable implementation version remain unknown. Portal-team authority and approval remain unconfirmed.

Empty-entity approval and enforcement remain a separate [open question](../../../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#empty-entity-configuration).

The [draft principles, line 14](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>) state the same denial direction.
The [older tile-security proposal, line 7](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L7>) permits entry for SC accounts.
That conflicting proposal remains historical evidence, not the selected user intent.
This clarification does not select other tile-security rules or grant publication approval.

#### UI-ENTRY-AC-001

This business criterion records user-stated intent only.
It is not a new executable case or an assertion of approved policy.

```gherkin
Feature: User-stated portal entry restriction
  @UI-ENTRY-AC-001
  Scenario: Deny entry without a registered application entity entitlement
    Given an authenticated SC user
    And the user has no entitlement for any application entity registered in the portal
    When the user attempts portal entry
    Then the portal denies entry to the user
    And the portal grants 0 entries for that attempt
```

```yaml
acceptance_criteria:
  - id: UI-ENTRY-AC-001
    given: Given an authenticated SC user has no entitlement for any registered application entity
    when: When the user attempts portal entry
    then: Then the portal grants 0 entries for that attempt
    measure:
      metric: portal entries granted for the attempt
      operator: equals
      value: 0
      unit: entries
```

Measure the entry decision for one attempt.
The observation binding remains unverified; no UI control, HTTP status, denial wording, or timing limit is specified.
The [canonical no-entity case](../../../../tasks/ui-test-coverage-20261022/06-test-cases.md#know-007) remains version 2 without byte changes.
The [clarification stage](../../../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#canonical-case-applicability) separates its historical execution from this criterion.


### Current user-stated empty-entity rule

When a tile has no configured EMS2 entity, hide the tile and deny direct tile launch.
Keep this restriction until an EMS2 entity is configured.
The [answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/empty-entity-source.json) records the user's selection.
The [recovered session](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/recovered-session-source.json) retains the exact response and message timestamp.
This rule leaves application data permissions separate.
The [owner and scope answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/empty-entity-owner-scope-source.json) identifies `portal team` across local, test, UAT, and production.

Owner approval and deployed enforcement remain unconfirmed.

The [historical proposal, lines 13–19](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L13-L19>) permits an empty role setting.
That example does not define an empty EMS2 entity setting.
No denial message, HTTP status, or timing limit was selected.

#### UI-EMPTY-ENTITY-AC-001

This business criterion records user-stated intent for local, test, UAT, and production environments.
It establishes no executable test result or policy approval.

```gherkin
Feature: User-stated tile restriction for missing entity configuration
  @UI-EMPTY-ENTITY-AC-001
  Scenario: Hide a tile without an EMS2 entity
    Given a user satisfies the portal-entry rule
    And the tile has 0 configured EMS2 entities
    When the portal presents available tiles to the user
    Then the portal displays 0 instances of that tile

  @UI-EMPTY-ENTITY-AC-001
  Scenario: Deny direct launch without an EMS2 entity
    Given a user satisfies the portal-entry rule
    And the tile has 0 configured EMS2 entities
    When the user attempts to launch that tile directly
    Then the portal grants 0 launches for that attempt
```

The tile count and launch count must each equal zero.
UI and service observation bindings remain unverified.
The [clarification stage](../../../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#empty-entity-configuration) records ownership, scope, approval limits, and historical case limits.

### Current user-stated empty-subject rule

The user selected tile visibility and launch through the entity check when the subject setting is empty.
The user must satisfy the portal-entry rule and hold entitlement for the tile's single configured EMS2 entity.
The [exact answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/empty-subject-source.json) is the first-priority reference for this intended behavior.
The [owner and scope answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/empty-subject-owner-scope-source.json) assigns the rule to `portal team` across local, test, UAT, and production.
These answers define no application data permission or multiple-entity matching rule.

Owner review, publication approval, and deployed enforcement remain unconfirmed.
The [historical SSDR discussion](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L17-L20>) describes skipping validation for an empty subject.
The explicit user clarification governs the selected scope.

#### UI-EMPTY-SUBJECT-AC-001

Apply this criterion in local, test, UAT, and production environments.
Tile visibility and portal launch authorization remain separate from application data permissions.

```gherkin
Feature: Tile access through one entity when its subject setting is empty
  @UI-EMPTY-SUBJECT-AC-001
  Scenario: Show the tile through its configured entity
    Given the user satisfies the portal-entry rule
    And the tile has 1 configured EMS2 entity
    And the user has entitlement for that configured entity
    And the tile has 0 configured subjects
    When the portal presents available tiles to the user
    Then the portal displays 1 instance of that tile

  @UI-EMPTY-SUBJECT-AC-001
  Scenario: Authorize launch through the configured entity
    Given the user satisfies the portal-entry rule
    And the tile has 1 configured EMS2 entity
    And the user has entitlement for that configured entity
    And the tile has 0 configured subjects
    When the user attempts to launch that tile
    Then the portal grants 1 launch authorization for that attempt
```

The visible tile count and launch authorization count must each equal one.
UI and service observation bindings remain unverified. No execution is claimed for this criterion.
The [task record](../../../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#canonical-case-applicability) preserves historical case limits.

### Integration purpose and responsibility boundary

The SDK injects an HTTP request filter into a downstream Spring application.
The guides describe automatic validation of JWTs generated by the Single UI authentication service.
Successful validation exposes user information through the request attribute `userInfo`.
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

The tile-security proposal distinguishes portal entry from permission to view individual tiles.
It assigns data access and editing permissions to each tile application.
A visible tile therefore does not establish permission to read or modify its business data.
This is a proposed responsibility boundary; current enforcement requires separate evidence.
[Tile security proposal, lines 1–23](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md>)

EMS2 setup defines entities, roles, subjects, and actions.
The procedure creates those objects and assigns actions to role-and-subject combinations.
Those objects provide entitlement context for application-specific checks.
The procedure alone does not prove that a backend performs those checks.
[EMS2 setup procedure, lines 1–12](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Creating EMS2 Entity Role Subject Action/page.md>)

### Version and configuration history

Version 1.0.0 documents artifact `com.scb.ratan:single-ui-sdk-starter` and configuration prefix `single-ui-sdk.auth`.
It includes optional `user-login-max-duration` and request context field `userEntitlements`.
Version 1.1.1 renames the artifact to `com.scb.fmoportal:fmoportal-auth-sdk`.
It removes that duration property and renames the field to `entitlements`.
[SDK version 1.0.0, lines 3–8, 14–51, 69–85](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.0.0/page.md>)
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

Version 1.1.2 documents `max_age` validation and adds `oud` to request context.
Version 1.1.4 documents logout session rejection and configurable public certificates.
Its Java guides expose `userId`, `entitlements`, `oud`, and `sessionId` through `userInfo`.
These version statements require matching against each consumer's actual dependency.
[SDK version 1.1.2, lines 5–15, 27–45](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.2/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

| Documented variant | Declared platform | Declared artifact version |
| --- | --- | --- |
| Java 8 guide | JDK 8; Spring Boot 2.6.6 or higher | `1.1.4-java8` |
| Java 17 guide | JDK 17; Spring Boot 3.1.2 or higher | `1.1.4-java17` |
| Boot 4 migration note | Spring Boot 4.0.6 | `2.0.0-SNAPSHOT` |

The Boot 4 note conditions an official `2.0.0` release on regression testing.
It describes separated JWT configuration, public-key configuration, and import changes.
It does not establish a completed release or consumer compatibility.
[Java 8 SDK guide, lines 3–21, 25–59](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 8/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)
[Boot 4 migration note, lines 1–28](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/Migration to Boot 4.0.6/page.md>)

### Protected requests and exceptions

The documented URL algorithm checks exclusions first.
With an empty inclusion list, it validates all remaining paths.
Otherwise, it validates matching inclusion paths.
Configuration therefore determines which requests receive SDK authentication checks.
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

The examples also configure `skip-jwt-headers`.
Earlier guides state that matching headers cause the SDK to skip JWT checks.
The supplied instructions do not identify a trusted replacement authentication control.
[SDK version 1.0.0, lines 3–8, 14–51, 69–85](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.0.0/page.md>)
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

### Entitlement retrieval and lifecycle

Version 1.1.4 provides two entitlement retrieval paths.
A service can query EMS2 through `AuthorizationService.getEntitlements`.
Alternatively, it can validate and extract a separate entitlement token through `JwtTokenUtil.getEntitlementsToken`.
The guide explicitly forbids using an entitlement token for authentication or login.
[SDK version 1.1.4, lines 7–46](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/page.md>)

Direct EMS2 consumers must maintain certificate and endpoint configuration.
The Java 17 guide documents account lookup and entitlement-list endpoints.
It permits an application entity list to constrain retrieval.
Its sample separates initial entitlement storage from later application requests.
[SDK version 1.1.4, lines 7–46](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

The SDK overview recommends entitlement caching and mentions NGINX stickiness for multiple endpoints.
It announces removal of EMS2 details from authentication JWTs in DEV on August 30, 2024.
That announcement cannot establish the present DEV state or any production state.
[SDK overview, lines 1–15](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md>)

## Connections

Authentication and sessions ([[wb-candidate-security-kt-authentication-and-sessions]]) explains portal token issuance and session concepts.
Admin and onboarding ([[wb-candidate-operations-kt-admin-and-onboarding]]) explains EMS2 setup and tile configuration.

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
[Tile security proposal, lines 1–23](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

## Open questions

What evidence confirms portal-team authority and approval across the user-stated environments?
The [retained answers](../../../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#ui-q-002) establish user-stated intent and owner identity only.
Consequence: Policy acceptance and publication remain blocked.
Owner: `portal team`, user-reported for entry policy only.
Next action: Obtain applicable authority and approval evidence.

What evidence confirms portal-team approval and deployed enforcement of the empty-entity tile rule?
The [owner and scope answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/empty-entity-owner-scope-source.json) identifies portal team across all portal environments.
Consequence: Policy publication requires applicable approval. Behavior acceptance requires deployed enforcement evidence.
Owner: `portal team`, user-reported for this rule.
Next action: Obtain the applicable approval and deployment evidence without repeating the answered ownership or scope question.

Which control authenticates requests when exclusions or skip headers bypass JWT validation?
The examples identify bypass settings without their trust boundary.
This prevents a complete account of protected-request behavior.
Owner: unknown.
Next action: document the trusted caller, replacement control, and bypass rejection tests.
[SDK version 1.0.0, lines 3–8, 14–51, 69–85](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.0.0/page.md>)
[SDK version 1.1.1, lines 5–17, 39–57, 74–89](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md>)

How do applications invalidate cached entitlements and reject logged-out sessions across instances?
The overview recommends caching; version 1.1.4 describes session rejection without distributed lifecycle guarantees.
Stale permissions and inconsistent logout remain unresolved possibilities.
Owner: unknown.
Next action: define cache expiry, revocation propagation, and observable cross-instance acceptance criteria.
[SDK overview, lines 1–15](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md>)
[Java 17 SDK guide, lines 3–21, 25–86, 135–154](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md>)

Which environments currently omit entitlements from authentication tokens?
The overview announces a specific DEV migration in 2024.
It provides no retained proof of current production token shape.
Owner: unknown.
Next action: inspect redacted token contracts and environment-specific migration records.
[SDK overview, lines 1–15](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md>)

The renewal requirement ([[wb-candidate-requirements-req-active-session-renewal]]) records the user's requested pilot behavior.
Its scenarios and deployment verification remain separate from these historical documents.
