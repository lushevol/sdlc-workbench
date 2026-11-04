# SDK consumer compatibility assessment

> **Bind each consumer version before replacing its SDK dependency.**
> Action: inventory deployed artifacts and verify the two Auth Server call sites.
> Consequence: a direct dependency upgrade can require source changes.
> Owner: unknown. Evidence: [declared dependency](../../../repos/services/ratan-auth-server/pom.xml#L98) and [instance validator](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java#L42).

## Scope and source identities

The [user request](user-input.md) authorizes this source assessment.
The [source manifest](consumer-sources.json) records exact revisions, clean repository states, and inspected file hashes.

| Source | Exact revision | Status |
| --- | --- | --- |
| SDK | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | Clean source copy |
| Auth Server | `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2` | Clean source copy |
| BFF | `134a340472f29d2a4136e07e516690de6a18e323` | Clean source copy |
| Test engine | `9f83897e8e71f8afa524b260ffa3e809b281a2f0` | Source search only |

Searches included ignored repository checkouts through `rg -uuu`.
Searches excluded Git internals, build outputs, virtual environments, and installed JavaScript dependencies.
Search scope included registered services, UI, infrastructure, and testing repositories.
A source search cannot establish every deployed consumer or dependency.

## Confirmed consumers and compatibility

| Finding | Confidence and evidence | Consequence | Owner and next action |
| --- | --- | --- | --- |
| Auth Server declares SDK `1.1.1`. The supplied SDK source declares `2.0.0-SNAPSHOT`. | High; [consumer POM](../../../repos/services/ratan-auth-server/pom.xml#L98), [SDK POM](../../../repos/libraries/single-ui-sdk-starter/pom.xml#L10). | These source copies represent different SDK API generations. | unknown; bind the released artifact and supported Java/Spring line. |
| Auth Server calls `JwtTokenUtil.validateToken` statically at two endpoints. The supplied SDK method requires an instance. | High; [login user endpoint](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/LoginController.java#L147), [authenticate endpoint](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/AuthenticationController.java#L83), [SDK method](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java#L42). | A blind upgrade predicts source incompatibility. No compilation failure was executed here. | unknown; inject the configured validator or retain a supported compatibility API. Run the consumer build. |
| Only Auth Server declares this SDK dependency within the bounded source search. | High for searched files; [POM](../../../repos/services/ratan-auth-server/pom.xml#L98). | Other deployed services remain unbound. | unknown; obtain deployed application dependency inventories. |
| No registered application source directly calls this SDK's `AuthorizationService` in the bounded search. | Medium; source patterns covered the SDK package, artifact name, service type, and entitlement methods. | The direct lookup consumer population remains unknown. | unknown; identify owners and runtime call paths before changing the return contract. |

The [user architecture clarification](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L20) describes SDK use across application backend services.
That intended architecture extends beyond the one locally identified Maven consumer.
The clarification does not establish versions or current adoption for every service.

## Public contracts that the migration must assess

The SDK public method returns `Map<String, Object>`.
Its shape is `entityName:roleName -> subjectName -> [actionName]`.
[Interface](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java#L5) and [map construction](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L132) establish this contract.
`EntitlementList` is an EMS2 transport DTO, rather than this method's public result.
CES projection must preserve reviewed meaning or introduce a versioned API.
A role name must not be invented from a CES application or profile identifier.
Owner: unknown. Next action: define the approved role and feature projection for actual callers.

The request filter reads `Single-UI-Authorization: Bearer <token>`.
It publishes JSON under the request attribute `userInfo`.
Fields include `userId`, optional `entitlements`, `oud`, `sessionId`, and `version` equal to `3`.
[Filter source](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java#L83) establishes these fields.
The filter performs token and session checks. It does not call the entitlement service or enforce action permissions.
Owner: unknown. Next action: retain authentication behavior and inspect each application's action checks separately.

The SDK validates authentication issuer `single-ui-bff` and entitlement issuer `single-ui-bff-entitlement` separately.
[Validation source](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java#L42) rejects entitlement issuers for authentication.
The [SDK source guide](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/page.md#L14>) explicitly requires this separation.
CES bearer credentials must therefore remain separate from the portal authentication header.
Owner: unknown. Next action: include issuer separation in compatibility verification.

BFF creates a separate entitlement token from its normalized entity map.
Its authentication token carries `oud` and the session identifier.
[Token construction](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L114) and [entitlement map](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L131) establish these paths.
SDK consumers that use entitlement tokens need BFF projection compatibility as well as direct CES lookup compatibility.
Owner: unknown. Next action: inventory both retrieval paths and compare their approved effective grants.

## Assertion evidence and execution gaps

No SDK test source was found in the supplied SDK checkout.
This investigation executed no Java builds, unit tests, browser cases, or external CES calls.
All behavior conclusions above come from source inspection.

| Inspected source assertion | Established boundary | Limit |
| --- | --- | --- |
| [Auth JWT conversion test](../../../repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/jwtparser/convertor/JwtDataEntitlementCompatibilityTest.java#L42) | Asserts functional actions from the full read and data roles from the separate EMS2 read. | Tests the Auth converter with mocks. It does not execute the SDK filter or CES service. |
| [Auth data failure test](../../../repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/jwtparser/convertor/JwtDataEntitlementCompatibilityTest.java#L80) | Asserts PRECONDITION_FAILED when the separate data reader fails. | Does not establish current passing execution or SDK migration behavior. |
| [BFF login test](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationControllerTest.java#L149) | Asserts successful login after mocked authorization and token generation. | Does not assert SDK validation, token issuer separation, or direct CES lookup equivalence. |

Required verification includes consumer compilation and Spring startup with the exact released artifact.
It also includes grant equivalence, denied permissions, malformed responses, outages, and issuer separation.
Canonical Gherkin definitions must precede new case implementation in the task's test-case document.
No complete test coverage or business verification is claimed.

## Existing knowledge applicability

[KT-sdk-and-entitlements version 7](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#version-and-configuration-history) remains a candidate.
Its historical guides document multiple Java and Spring variants.
The [Boot 4 note](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/Migration to Boot 4.0.6/page.md#L3>) conditions release `2.0.0` on regression testing.
It does not establish release completion or deployed consumer compatibility.
The [current migration record](../../ces-entitlement-migration-20261102/01-intake.md#description) already leaves deployed SDK versions unresolved.
No new business clarification or governed knowledge change occurred in this assessment.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
