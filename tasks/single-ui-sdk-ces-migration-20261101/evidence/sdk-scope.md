# SDK migration source findings

> **CES migration requires a client and a reviewed response mapping.**
> Action: Resolve role mapping before implementation. Consequence: Existing permission-map consumers can lose or receive incorrect grants.
> Owner: unknown. Evidence: [map construction](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:132).

## Source identity and limits

The SDK checkout is clean at `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
The commit date is 14 October 2026. Investigation date: 1 November 2026, Asia/Singapore.
No ancestor or SDK-local `AGENTS.md` was found below `repos/` on the selected path.
The Workbench project guide applies. No application source was changed.

Confidence: HIGH for the inspected source behavior and edit scope.
Deployment identity, installed downstream SDK binaries, and effective runtime configuration remain unknown.
No business execution or Java compilation was performed.
The default `java -version` command failed because macOS could not locate a Java runtime.
This observation does not prove that no separately configured JDK exists.

## Current call and data path

1. A caller invokes [AuthorizationService.getEntitlements(userId)](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java:5).
2. [AuthorizationImpl](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:30) reads EMS2 account entitlements through `getEntities`.
3. The [GET request](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:71) calls `ems2Host + userRolesEndpoint`, formatted with `userId`.
4. [getEntity](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:94) splits `uniqueName` into numeric entity ID, entity name, numeric role ID, and role name.
5. The configured `entityList` filters entity names at [lines 34–36](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:34).
6. [getRawEntitlements](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:118) posts JSON `{"<userId>":["<entityName>"]}` to the entitlement-list endpoint.
7. [role and subject joins](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:40) join returned grants by numeric role and subject IDs.
8. [buildEntitlements](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:132) returns `{"entityName:roleName":{"subjectName":["actionName"]}}`.

The default endpoints are `/ems2/rest/account/%s` and `/ems2/rest/entitlements/entitlementList`.
Source: [AuthProperties](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java:26).
The GET request has no explicit request authorization header in this implementation.
The POST request sets JSON content type only.

Changing `ems2Host` cannot adapt a CES response to these EMS2 DTOs and numeric joins.
This is a source-supported incompatibility prediction. It is not a retained live failure.

## Concrete edit map

| Component | Required migration work | Consequence and next action | Owner |
| --- | --- | --- | --- |
| [AuthProperties](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java:26) | Add CES base URL, application identity, entitlement endpoint, and authentication settings. | Keep project mappings in configuration. Resolve canonical CES settings before implementation. | unknown |
| [AuthConfiguration](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java:39) | Wire a CES client and approved token provider. Preserve configured connection and read timeouts. | Existing bean always creates the EMS2 implementation. Select a CES implementation explicitly. | unknown |
| [AuthorizationImpl](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:30) | Replace the account GET and entitlement-list POST with CES reads and normalization. | CES-only operation must produce zero EMS2 calls. Confirm approved role and feature mappings. | unknown |
| [AuthorizationService](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java:5) | Preserve the Java signature where compatibility remains required. | The signature hides the nested map contract. Inventory actual consumers before changing keys. | unknown |
| `entity/` package | Add CES response DTOs. Separate transport DTOs from the public normalized representation. | CES feature and action data cannot satisfy EMS2 numeric joins. Do not fabricate legacy identifiers. | unknown |
| [buildEntitlements](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:132) | Review the candidate mapping: CES application to scoped legacy entity alias; CES feature to legacy subject; CES action to legacy action. | Per-grant role provenance remains unresolved. `entitlement_name[]` and union grants cannot reconstruct each legacy role grant. | unknown |
| Parent and module POMs | Confirm target framework, artifact version, CES authentication dependency, and tests. | Publish and consume one explicit version after compatibility validation. | unknown |
| Consumer configuration | Replace EMS2 settings with CES settings and reviewed application mappings. | Setting an EMS3 property elsewhere does not change this SDK. Verify effective bean configuration. | unknown |

Retain legacy DTOs only while supported callers or migration modes still consume them.
No current caller of `Ems2Result` was found inside the SDK.
An external binary consumer can still exist.

## JWT and filter boundary

[AuthTokenFilter](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java:83) validates `Single-UI-Authorization: Bearer <JWT>`.
It copies token fields into the `userInfo` request attribute.
The copied fields are `sessionId`, `entitlements`, `oud`, `userId`, and `version`.
The emitted `version` value is `3`.
The filter never invokes `AuthorizationService` or performs CES permission checks.
Changing the lookup bean alone cannot add endpoint permission enforcement.
This is an architectural boundary, not a confirmed access-control defect.

[JwtTokenUtil](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java:20) verifies RSA512 tokens and expects issuer `single-ui-bff` for request tokens.
[getEntitlementsToken](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java:63) expects issuer `single-ui-bff-entitlement` and reads the `entitlements` claim as text.
[validateSession](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java:82) maintains local logout session state.
Preserve these contracts unless a separate approved token migration changes them.
CES service authentication must not reuse a browser token without contract evidence.

## Failure and compatibility boundaries

[getEntities](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:71) catches exceptions and returns an empty entity list.
[getEntitlements](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:105) catches exceptions and returns an empty grant list.
[public lookup](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:65) catches exceptions and returns an empty map.
A CES implementation needs an explicit no-grants and upstream-failure contract.
Do not silently reinterpret a CES outage as a verified successful no-grants response.
No downstream enforcement or user impact was executed in this investigation.

The SDK currently ignores EMS2 account-status fields when selecting grants.
The `Ems2Role` DTO has those fields, but `getEntities` reads only `entitlementTypes`.
Whether CES account status requires a new check needs policy evidence.

## Known consumer and version mismatch

The registered Auth Service checkout is clean at `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2`.
Its [dependency declaration](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/pom.xml:98) requests `com.scb.fmoportal:fmoportal-auth-sdk:1.1.1`.
The supplied SDK [parent POM](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/pom.xml:10) declares `2.0.0-SNAPSHOT`.
A local SDK build does not replace the requested `1.1.1` artifact.
The supplied Auth Service imports `JwtTokenUtil` in two controllers.
No direct `AuthorizationService` import was found in the selected service sources.
The BFF has a separate authorization interface and implementation.
Do not assume a BFF migration also updates this library.

The SDK declares Java 17 and Spring Boot `4.0.6`.
Its module uses Jackson 2 `ObjectMapper` and declares `jackson-databind:2.21.2`.
The module excludes Jackson 3 databind from the JSON starter.
These declarations need compatibility checks in the actual consumer environment.
They do not establish a passing build.

## Test and build evidence

The SDK has 27 tracked files. No tracked tests, README, or test source directory were found.
The module POM declares no test starter.
The pipeline requests Java 17, Maven `3.8.1`, and `clean install`.
The pipeline also disables JaCoCo and excludes the SDK from Sonar coverage.
Source: [pipeline configuration](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/azure-pipelines-maven.yml:20).
A successful existing build would not demonstrate migrated authorization behavior.

Required verification boundaries include mapped grants, denied actions, absent grants, duplicate grants, and several roles.
They also include malformed responses, CES authentication failure, timeout, and zero EMS2 calls in final mode.
Verify JWT validation, request attributes, and downstream artifact selection separately.
These are verification recommendations, not executed cases or approved business criteria.

## Source hashes

| Source | SHA-256 |
| --- | --- |
| [repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java) | `74587cf78a69e0c9b7b3920d510248acd5501dbaa7ac27035b3b9c5fc91bc2d1` |
| [repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java) | `d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f` |
| [repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java) | `48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba` |
| [repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java) | `dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d` |
| [repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java) | `09d8595302dd702b8f38c298ff9e5a91f6107678ffd61714b540253605bcc161` |
| [repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java) | `cc81a872b3565aa58175e6f8630667e776d102e0ebc160d488f4ce0691f5edab` |
| [repos/libraries/single-ui-sdk-starter/pom.xml](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/pom.xml) | `757c76776c7530b9dc60f9a3b7d58beb061d52181e3c9ec671ba6a64d4739317` |
| [repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/pom.xml](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/pom.xml) | `88c5d40332aa1cc97a9a90509c1263c5d0911642cd014f26369bca015dd27d67` |
| [repos/libraries/single-ui-sdk-starter/azure-pipelines-maven.yml](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/azure-pipelines-maven.yml) | `d94496d71459b44200c5027bc98c852a116016bb0b0eb25c321089a6676b75fb` |
| [repos/services/ratan-auth-server/pom.xml](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/pom.xml) | `f0bc362c43022486411df25e399406f866ebcfa9be5e8698693ebdd02a403021` |

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
