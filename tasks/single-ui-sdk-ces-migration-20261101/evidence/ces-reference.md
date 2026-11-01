# CES implementation references for the SDK migration

> **Critical conclusion: CES transport is reusable, but the SDK role-key contract needs a mapping decision.**
> Action: define role provenance or version the SDK authorization output before implementation.
> Consequence: changing the EMS2 base URL cannot preserve the SDK contract.
> Owner: unknown. Evidence: [SDK map keys](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:132).

## Scope and identity

The [user input](user-input.md) authorizes this source assessment on 1 November 2026.
This assessment changes no application source, configuration, or governed knowledge.
Both reference worktrees were clean during inspection.

| Reference | Exact revision | Commit date | Authority and limits |
| --- | --- | --- | --- |
| Auth Service | `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2` | 2026-10-30T07:49:37+08:00 | Current local implementation. No deployment or approved mapping proof. |
| Single UI BFF | `134a340472f29d2a4136e07e516690de6a18e323` | 2026-10-30T07:52:24+08:00 | Current local implementation. No deployment or approved mapping proof. |

Confidence is HIGH for cited source behavior.
Runtime outcomes, production reachability, and approved business equivalence remain unverified.
No business tests or external calls ran.

## Resolved migration meaning

The [prior user clarification](../../draft-ces-migration/evidence/user-input-20261030-field-equivalence.txt) states that `X_RATANONE` became `RATAN_ENTITLEMENT_RULE`.
The [feature clarification](../../draft-ces-migration/evidence/user-input-20261030-api-samples-and-feature-consolidation.txt) places `RATAN_FUNC` and `RATAN_DATA_ENTITLEMENT` under that CES application.
Confidence is HIGH for these recorded user statements.
These answers resolve the application rename and feature consolidation.
They do not define each legacy role's feature/action membership.

The SDK account reader uses only `entitlementTypes`, `uniqueName`, and `applicationName`.
Evidence: [SDK reader](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:71).
It does not inspect `accountStatus`, `accountType`, `fullName`, or `accountOwner`.
Those metadata replacements therefore do not block this SDK migration assessment.

## Transport and authentication

| Concern | Inspected implementation | SDK implication |
| --- | --- | --- |
| Effective user endpoint | GET `/fmces/v1/entitlement/app/{appId}/{appName}/user/{userId}`. See [Ems3Repository.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java:40). | Add a CES client and separate application configuration. |
| Safe URI construction | The BFF expands and encodes path variables. See [Ems3EntitlementService.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java:106). | Use URI templates instead of string concatenation. |
| Service authentication | Both clients use `Authorization: Bearer <FMAA token>`. See [Ems3EntitlementService.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java:123). | Supply an outbound service token provider. An incoming Single UI JWT is a different credential. |
| Token acquisition | Auth calls `FMAAAuthService.getFmaaToken()` before CES. See [Ems3LegacyEntitlementService.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3LegacyEntitlementService.java:44). | Prefer a host-provided token abstraction. Avoid adding Redis and token acquisition internals without an SDK requirement. |
| FMAA flow | The reference uses `fmaa-client` client credentials and certificate configuration. See [FmaaAuth.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/FmaaAuth.java:78). | Runtime onboarding needs an authorized service identity, token endpoint, and trust configuration. |
| Timeouts | Auth uses dedicated CES connect/read timeout properties. See [EntitlementHttpConfiguration.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/configuration/EntitlementHttpConfiguration.java:23). | Give CES requests bounded timeouts. Actual accepted limits remain an operations decision. |
| Retry classification | Network and 5xx become retryable exceptions. 4xx and invalid responses become nonretryable exceptions. See [Ems3Repository.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java:38). | Define bounded retry and denial behavior. Do not copy annotations without checking proxy invocation. |

The existing FMAA helper logs token values at source lines 68 and 105.
This is a reuse limitation, not a verified incident or release blocker.
Use the authentication concept without copying token logging.
Owner: unknown. Next action: provide an SDK token interface with tests that prevent token disclosure.

## Response models and compatibility

The effective-user endpoint returns a JSON array.
Each result contains `user_data` and `entitlements`.
The DTO uses explicit snake_case properties in [Ems3DataEntitlementDto.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/dto/Ems3DataEntitlementDto.java:9).

| CES field | Meaning in current code | Compatibility consideration |
| --- | --- | --- |
| `user_data.user_id` | Selects the requested user from the array. | Reject mismatched or missing identities. |
| `user_data.app_name`, `itam_id` | Describe application scope. | Keep ITAM identity separate from internal CES application IDs. |
| `entitlements.role_entitlements[]` | Flat `feature` and `action` strings. | Map to SDK subjects/actions through reviewed application scopes. |
| `entitlements.entitlement_name[]` | Effective entitlement names. | It is not an EMS2 composite role ID. |
| `entitlements.data_profiles` | Data profile names and owners. | Data profiles need separate legacy-role mappings where required. |
| `entitlements.data_entitlements[]` | Keys and string-value arrays. | Preserve values as strings. These are data filters, not functional grants. |
| `entitlements.data_policies` | Policy rule payload. | Do not interpret unrecognized rules as additional permissions. |

Functional authorization and data filtering use different validation paths.
The BFF functional path requires nonempty `role_entitlements` in [Ems3EntitlementService.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java:202).
Its data path requires nonempty `data_entitlements` at line 191.
Do not require data entitlements merely to return functional SDK authorization.

## Mapping references and their limits

| Reference behavior | Evidence | Reuse limit and next action |
| --- | --- | --- |
| BFF groups requests by CES application ID and name. | [TileAuthorizationServiceImpl.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:115) | Use the confirmed application rename and feature consolidation. Preserve scopes for other SDK consumers explicitly. |
| BFF maps features into subjects and actions into action names. | [AuthorizationResultMapper.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:43) | Use the shape as a reference. Approve equivalent names separately. |
| BFF copies all application feature grants into each supplied entity. | [AuthorizationResultMapper.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:62) | Do not copy this blindly. The SDK needs entity-specific grant scopes and isolation tests. |
| BFF omits legacy numeric IDs and role provenance. | [AuthorizationResultMapper.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:72) | Inventory SDK consumers of IDs and role names. The current SDK does not consume account status or owner fields. |
| Auth maps entitlement names through configurable role mappings. | [DefaultEms3EntitlementMapper.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:77) | Unmapped roles remain unresolved. Current code rejects absent or conflicting mapped roles. |
| Auth maps data profile names through separate data-role mappings. | [DefaultEms3EntitlementMapper.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:114) | Do not equate profiles with functional roles. |
| Auth projects human actions as `feature:action`. | [DefaultEms3EntitlementMapper.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:147) | This Auth token format differs from the SDK object graph. |
| Auth projects system actions as `RATAN_FUNC:action:feature`. | Same mapper at line 159. | A service-account mapping requires explicit consumer requirements. |

These are source facts, not approved migration policy.
Mapping choices can grant or remove access when applied to different consumers.
The SDK output uses `entityName:roleName` keys. The effective endpoint merges functional pairs across assigned entitlements.
Its flattened response does not bind each pair to a particular legacy role.
Owner: unknown. Next action: approve a role-key mapping, use a supported role-detail contract, or version the output.

## Error and empty-result behavior

The Auth repository rejects empty arrays, unmatched users, absent entitlements, and responses without functional or data grants.
Evidence: [Ems3Repository.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java:80).
The BFF functional path separately rejects missing or empty functional grants.
Evidence: [Ems3EntitlementService.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java:202).

The BFF treats one specific user-not-found response as no application grants.
Its test compares both the error type and `User Not found-<requested user>` message.
Evidence: [Ems3UnRetryableException.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/exception/Ems3UnRetryableException.java:23).
Other CES errors propagate from [TileAuthorizationServiceImpl.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:139).
The SDK denial contract requires an explicit decision; these references use different policies.

## Remaining dependency outside the SDK

Auth `EMS3_ONLY` still calls EMS2 for JWT data roles.
Evidence: [EntitlementMigrationFacade.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:58) and [JwtConvertorForNewUse.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/jwtparser/convertor/JwtConvertorForNewUse.java:128).
Migrating SDK calls alone therefore cannot establish zero EMS2 runtime dependencies across RATAN.
This is a source planning gap. Production impact remains unproved.
Owner: unknown. Next action: track that independent Auth dependency in the existing migration task.

## Inspected assertions

Execution status is `NOT_RUN` for every assertion below.

| Test source | Inspected assertion | Limits |
| --- | --- | --- |
| [Ems3RepositoryTest.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/repo/Ems3RepositoryTest.java:102) | Empty responses and mismatched users throw nonretryable exceptions. | Mock transport only. |
| Same test at lines 152, 172, and 190. | 4xx, 5xx, and transport errors have separate exception classes. | Retry execution and live service behavior remain unproved. |
| [AuthorizationResultMapperTest.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java:28) | Features/actions map to every supplied entity, with distinct actions. | This asserts implementation; it does not approve SDK semantics. |
| Same test at line 79. | Feature and action names remain case-sensitive. | Confirm canonical business spelling before cutover. |
| [Ems3EntitlementsSeparationTest.java](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3EntitlementsSeparationTest.java:51) | Unrelated CES failures propagate in CES-only mode. | Local mocks; no live denial or outage proof. |

## Raw sample review

The retained [CES effective-user sample](../../draft-ces-migration/api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json) has one array element and 30 functional pairs.
Its `user_data` contains application name, ITAM ID, and user ID.
It contains no EMS2 `accountStatus`, `accountType`, `fullName`, or `accountOwner` replacement.
The [EMS2 account sample](../../draft-ces-migration/api/:ems2:rest:account:1481696.json) contains those four fields.
The [CES role-detail sample](../../draft-ces-migration/api/-fmces-v1-entitlement-user-1481696.json) instead uses camelCase and `featureActionDtos`.
These endpoint responses need separate DTOs.
Sample filenames do not establish an authoritative or deployed API contract.


| Retained source | SHA-256 |
| --- | --- |
| [-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json](../../draft-ces-migration/api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json) | `871f59e5492605af54ab62cd9343f74c6bba24ef8df2298db59946a80cf11aaa` |
| [:ems2:rest:account:1481696.json](../../draft-ces-migration/api/%3Aems2%3Arest%3Aaccount%3A1481696.json) | `1fd6e24c0bfbd564f775883646af4132588a2b08180de5e09850885b954e41ed` |
| [-fmces-v1-entitlement-user-1481696.json](../../draft-ces-migration/api/-fmces-v1-entitlement-user-1481696.json) | `8f841cc6573449027db65a97ad26a01d2720f4f60c565e6dd9e18314651d32f3` |

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Source inspection does not establish approved mappings, deployment, or passing execution.
```
