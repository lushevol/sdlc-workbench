# Role-specific CES compatibility design

> **The role-detail response supports the old map shape, but supplied account permissions are not equivalent.**
> Action: use assigned-role details and explicit scope aliases. Verify mappings against comparable account assignments.
> Consequence: this sample set cannot establish 100% deployed permission compatibility.
> Owner: Codex for adapter design; business mapping owner unknown.
> Evidence: [user clarification](user-clarification-implementation.md) and [sample comparisons](#sample-comparisons).

## Source identity and authority

Assessment date: 1 November 2026, Asia/Singapore.
SDK baseline: `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`; the checkout was clean during source inspection.
The [implementation clarification](user-clarification-implementation.md) prioritizes compatibility, version `3.0.0`, caller-owned FMAA tokens, and tests.
The [stage record](../10-change-review.md) preserves that authority separately from deployment or acceptance approval.
No application source, knowledge record, or Git commit was changed for this design review.
No business execution or live endpoint call occurred.

Confidence: HIGH for the inspected structures and baseline behavior.
Confidence: MEDIUM for complete semantic compatibility until mappings and comparable assignments are established.

## Old SDK contract

The public [interface](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java#L5) exposes `Map<String, Object> getEntitlements(String userId)`.
The [implementation](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L30) performs account lookup before grant retrieval.
Account `entitlementTypes[].uniqueName` supplies entity and role identities.
The method filters configured legacy entity names before requesting grant rows.
It joins grants by numeric role ID and subjects by numeric subject ID.
The final map contains `legacyEntity:legacyRole -> subjectName -> List<actionName>`.
Numeric IDs do not appear in this public map.

The old method retains assigned roles with no grants as empty maps.
Its action lists retain input order and duplicate action names.
HashMap key iteration order is not a public guarantee.
The [exception paths](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L65) return an empty map after failures.
This provides no grants, but cannot distinguish upstream failure from valid no-permission results.

## Supported CES source choice

Use the assigned-role response modeled by [the user-role sample](../../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-user-1481696.json).
Its filename identifies `/fmces/v1/entitlement/user/{userId}`.
Its array entries contain `entitlementName`, `appId`, `appName`, `appUID`, and `featureActionDtos`.
Each feature/action pair remains under its assigned entitlement.
That grouping supplies the role provenance missing from the aggregate endpoint.

The sample alone does not establish the endpoint's supported method, current deployment, or service-account behavior.
A configurable endpoint template and live integration check must keep this limit visible.
Neither catalog `user_ids` nor an application role definition alone proves effective user membership.
Do not replace the assigned-role endpoint with a catalog scan merely because a role exists there.

The role-detail response does not echo a user ID.
Validate requested-user URI construction, configured application selectors, and nested application identity.
Do not claim response-user identity verification from absent response data.
The aggregate response can validate user identity, but cannot restore each pair's role attribution.

## Precise adapter rules

| Source field or boundary | Required adapter behavior | Evidence and limit |
| --- | --- | --- |
| Requested `userId`. | Expand one URI path variable and encode it. Reject blank input before HTTP. | No response user field exists in assigned-role sample. |
| `appId`, `appName`. | Match configured application scope before producing any legacy entity key. | `appId` is the external selector `51358` in this sample. |
| `appUID`. | Treat it as an opaque internal CES identity. Check consistency with nested identities when supplied. | Do not equate it with old EMS2 entity IDs. |
| `entitlementName`. | Preserve a same-name role or apply an explicit reviewed alias. | Do not derive a legacy role from profile or application names. |
| `featureActionDtos[].features.featureName`. | Map to the old subject name inside that role and entity scope. | Use identity names unless an explicit scoped alias is required. |
| `featureActionDtos[].actions.actionName`. | Map to the old action name. Preserve source order and duplicates for strict list compatibility. | Do not convert data-filter values into action grants. |
| Nested `applicationDto`. | Reject selected grant rows that contradict their parent role application. | Compare app name and internal UID where supplied. |
| Empty `featureActionDtos`. | Preserve the assigned role key with an empty subject map. | This matches old account-assignment behavior. |
| Legacy `entityList`. | Apply exact legacy alias filtering to output scopes. | Do not silently reinterpret entity names as CES application names. |
| Alias collisions. | Reject or require an explicit documented merge rule. | Distinct roles must not silently overwrite or union under one key. |
| Unsupported aggregate-shaped rows. | Report an invalid-response failure on the explicit API. | Never copy all merged grants to every entitlement name. |

An implementation can represent mappings through scoped configuration records.
A scope identifies CES application ID/name and one legacy entity alias.
It can restrict CES role names and feature names.
Optional role, subject, and action aliases apply only inside that scope.
Do not populate tenant-specific defaults inside the library.

### RATAN mappings and their limits

| Legacy scope | Sourced target meaning | Safe implementation treatment | Remaining decision |
| --- | --- | --- | --- |
| `X_RATANONE`. | CES application `RATAN_ENTITLEMENT_RULE`. | Configure an application-to-legacy-entity alias. Preserve each assigned role's own pairs. | Role aliases and allowed historical role changes remain unreviewed. |
| `RATAN_FUNC`. | User states this scope is consolidated as a CES feature. | Configure feature-scoped legacy entity routing and explicit subject aliases when required. | Raw SYS_RO catalog sample instead uses `Ratan_Function_*` feature names. The exact target feature convention needs environment evidence. |
| `RATAN_DATA_ENTITLEMENT`. | User states this scope is consolidated under the same application. | Preserve a legacy data-role key only with an explicit supported assignment mapping. | No approved `RATAN_ENTITLEMENT_GLOBAL -> Global` mapping exists. Do not infer it from similar names. |

Sources: [rename clarification](../../ces-entitlement-migration-20261102/evidence/user-input-20261030-field-equivalence.txt) and [feature consolidation](../../ces-entitlement-migration-20261102/evidence/user-input-20261030-api-samples-and-feature-consolidation.txt).
The library should not invent `RATAN_FUNC` or data grants when their source rows are absent.
Application-specific feature routing remains configuration, rather than a shared-library assumption.

## Sample comparisons

All eight retained samples parsed as JSON.
The two aggregate response files are byte-identical.
These are static payload comparisons, not actual old/new SDK execution.

| Comparison | Observed result | Consequence and limit |
| --- | --- | --- |
| EMS2 human account. | `X_RATANONE:FMO_OPS_BOM` and `RATAN_DATA_ENTITLEMENT:Global` appear among 69 assignments. | This is the old account's scope, not the CES assigned-role set. |
| CES assigned-role response. | Six roles: `RATAN_ENTITLEMENT_GLOBAL`, `RATAN_ENTITLEMENT_COMMON`, `FM Read Only`, `FM Trading Plus - FX Cash`, `RATAN_ENTITLEMENT_DEV_USERS`, and `NON_FMO_RO`. | `FMO_OPS_BOM` is absent. Equality for the sampled user cannot be claimed. |
| Assigned-role union versus aggregate. | Both contain the same 30 unique feature/action pairs. | Role grouping is lost in aggregate, although union values match this sample. |
| EMS2 `FMO_OPS_BOM` versus CES catalog role. | Old: 63 unique pairs. Catalog: 68 pairs. All old pairs appear in the catalog. | Catalog definition differs and does not establish user assignment. |
| Strategic cashflow scope. | Both same-name role definitions contain the same 20 pairs. | This bounded definition comparison supports a compatibility fixture. It does not prove assignment. |
| Trade blotter scope. | Both same-name role definitions contain the same six pairs. | The same assignment limit applies. |

The five catalog-only pairs all belong to `RATAN_VALIDATION_EXCEPTION`:

- `F_Custom_View_Builder_Private`.
- `F_Custom_View_Builder_Public`.
- `F_Manually_Close_Exception`.
- `F_Replay_Exception`.
- `F_Trade_Affirmation_Status_Change`.

The old service account sample assigns `RATAN_FUNC:SYS_RO`.
The catalog contains `SYS_RO` with three `Query` grants under `Ratan_Function_*` features.
No service-account assigned-role response or old service-account grant response is supplied.
That prevents a service-account output equality claim.

## Java and failure compatibility

Preserve `getEntitlements(String)` and the existing implementation's public three-argument constructor where possible.
Add a new token overload as an interface default method to avoid breaking third-party implementations.
The SDK implementation can override that overload with explicit classified errors.
A caller-provided token interface can serve the old single-argument method.
Acquire a token once per lookup. Keep token refresh and storage with the caller.

Recommended failure policy:

1. Preserve empty-map behavior for the existing method.
2. Return an empty map for a valid empty assigned-role array on both paths.
3. Report missing token, invalid configuration, malformed response, HTTP, and transport failures through the explicit API.
4. Do not log token values or upstream response bodies that might contain credentials.
5. Do not add automatic retry, credential refresh, stale-permission fallback, or caching without a supported requirement.

These are implementation suggestions under the user's request for failure-handling advice.
They do not establish approved production operational policy.

## Compatibility conclusion

| Dimension | Assessment |
| --- | --- |
| Existing Java lookup signature. | Can be preserved. |
| Nested map structure. | Can be preserved. |
| Per-role feature/action provenance. | Available in the assigned-role sample; absent from aggregate. |
| Exact role/entity names. | Requires scoped aliases and reviewed assignment mappings where names changed. |
| Duplicate and ordered action values. | Can be preserved by list construction. |
| Numeric IDs in public result. | Not applicable; the old public map does not expose them. |
| Same user permissions across supplied dumps. | Not equivalent; different assigned roles and catalog-only grants are visible. |
| All production consumers and service/data roles. | Unknown until exact assignments, supported endpoints, and consumer builds are verified. |

Do not report 100% migration compatibility from these payloads or complete traceability links.
A passing same-fixture comparison can establish only the stated mapping and Java contract boundaries.
Owner: unknown for business mapping. Next action: compare approved same-user, same-scope assignments before acceptance.

## Source hashes

| Source | SHA-256 |
| --- | --- |
| [AuthorizationService.java](<../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java>) | `cc81a872b3565aa58175e6f8630667e776d102e0ebc160d488f4ce0691f5edab` |
| [AuthorizationImpl.java](<../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java>) | `74587cf78a69e0c9b7b3920d510248acd5501dbaa7ac27035b3b9c5fc91bc2d1` |
| [AuthProperties.java](<../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java>) | `d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f` |
| [-fmces-v1-entitlement-user-response-1481696.json](<../../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-user-response-1481696.json>) | `871f59e5492605af54ab62cd9343f74c6bba24ef8df2298db59946a80cf11aaa` |
| [-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json](<../../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json>) | `871f59e5492605af54ab62cd9343f74c6bba24ef8df2298db59946a80cf11aaa` |
| [:ems2:rest:account:1481696.json](<../../ces-entitlement-migration-20261102/api/:ems2:rest:account:1481696.json>) | `1fd6e24c0bfbd564f775883646af4132588a2b08180de5e09850885b954e41ed` |
| [-fmces-v1-entitlement-user-1481696.json](<../../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-user-1481696.json>) | `8f841cc6573449027db65a97ad26a01d2720f4f60c565e6dd9e18314651d32f3` |
| [:ems2:rest:entitlements:entitlementList .json](<../../ces-entitlement-migration-20261102/api/:ems2:rest:entitlements:entitlementList .json>) | `837253a6ac860af9fee9e3527cc0831efa969a22ee585810781f247bd263aa92` |
| [:ems2:rest:account:srv.ratan.001.json](<../../ces-entitlement-migration-20261102/api/:ems2:rest:account:srv.ratan.001.json>) | `9493d84003d8145cda7d9b16dae74a2d9d1d80b36ece05a8736758ae3882a788` |
| [-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json](<../../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json>) | `6fac90317b842a50070d49cd87c87a0301d3bc1163fde9d47c90eb9a679d7940` |
| [-fmces-v1-entitlement-588-app-51358-RATAN_ENTITLEMENT_RULE.json](<../../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-588-app-51358-RATAN_ENTITLEMENT_RULE.json>) | `11b8665f589489bb74defa0d7f0794629706816354807df2fbbe4fbc315227a5` |

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Static payload comparisons do not establish live permissions, deployment, or approval.
```
