# Frontend and dependent consumer migration investigation

**No critical conclusions require user attention or action.**

This investigation identifies compatibility work and evidence gaps.
It does not establish a release failure or deployed user impact.
Owner: unknown for migration coordination.
Next action: reconcile these consumers with the auth server and BFF target contracts.

## Scope and source identity

The [user request](user-input-20261030-migration-plan.txt) authorizes migration investigation.
The [source manifest](frontend-sources-20261030.json) binds inspected file bytes and repository states.
No application source was changed. No business suite was executed.

The [recovered user inputs](historical-user-inputs-20261028-29.json) add explicit migration intent from 28–29 October 2026.
The user reports DEV migration completion and requests verification by Settlement, Trade Control, and FlowZero.
During testing, each tile can switch between CES and EMS2 independently.
The final November release must set all RATAN tiles to CES.
Service authorization must migrate to CES for testing, onboarding, and release.
The user requires zero EMS2 dependencies across RATAN after final release.
These statements record user intent and reported status. They do not verify deployment.

Legacy field names and normalized entity shapes are separate from upstream runtime dependencies.
An adapter can preserve those contracts while obtaining authorization entirely from CES.
Renaming every EMS2 identifier is not an evidenced migration requirement.

| Repository | Identity | Limit |
| --- | --- | --- |
| mfe-base | `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`; commit dated 28 October 2026 | Existing Home controller and build-info changes remain preserved. |
| mfe-root-config | `83091d85beff5306ca0cd643955d8ea6ed0a2d93`; commit dated 14 October 2026 | Clean source checkout. |
| ratan-test-engine | `9f83897e8e71f8afa524b260ffa3e809b281a2f0`; commit dated 28 October 2026 | Existing guide and log changes remain preserved. |
| mfe-ratan-container, mfe-cashflow-blotter, nginx | Filesystem copies; per-file SHA-256 in manifest | No independent Git history or deployment identity. |

## Confirmed source observations

### FE-01: The shell consumes a normalized BFF contract

Confidence: high for inspected source behavior.
The [service calls](../../../repos/ui/mfe-base/src/services/index.ts#L10-L24) use `/auth/v2/sso/login` and `/auth/v3/sso/login`.
The latter is named `loginEntra` in this frontend.
Its name does not prove that endpoint version selects CES authorization.
Logout still calls the v2 endpoint.

The [user decoder](../../../repos/ui/mfe-base/src/utils/login.ts#L65-L83) parses `userInfo` and optional `entitlementsToken` JSON claims.
It receives `entities` separately and can parse an `oud` JSON string.
The [entity model](../../../repos/ui/mfe-base/src/hooks/model/root.ts#L42-L59) requires entity, role, subject, and action fields.
It includes numeric identifiers and `roleName`.
No direct EMS2 or CES entitlement HTTP call was observed in the inspected frontend source search.

Consequence: provider changes can still break frontend decoding and permission checks.
Owner: unknown. Next action: version and test the normalized BFF response contract.
Limit: source search covered the four registered frontend directories, excluding tests and image assets.

### FE-02: Portal entry depends on entity names and configured tiles

Confidence: high for inspected source; deployment remains unknown.
The [entry check](../../../repos/ui/mfe-base/src/utils/login.ts#L142-L158) compares returned entity names with configured tile entities.
The [entity collector](../../../repos/ui/mfe-base/src/utils/entities.ts#L3-L12) derives names from drawer tiles.
A failed match clears stored session data and dispatches `No entitlements found.`.

Consequence: an incorrect CES application-to-entity mapping can deny the portal session.
This is a possible consequence, not an observed migration failure.
Owner: portal team for the user-stated entry policy; migration implementation owner unknown.
Next action: preserve approved entry semantics and test exact CES-to-tile mappings.

### FE-03: Admin configuration retains EMS2-shaped fields

Confidence: high for inspected source.
The [admin role helper](../../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L3-L11) selects exact entity name `FMO PORTAL ADMIN`.
It returns that entity's `roleName`.
The [tile editor](../../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L233-L259) edits `ems2Subject`, `ems2Entities`, and `ems2Role`.
The [tile audit view](../../../repos/ui/mfe-base/src/admin/Tile/common/useAudit.tsx#L125-L137) displays the corresponding legacy fields.
The [category editor](../../../repos/ui/mfe-base/src/admin/Category/common/useController.tsx#L43-L44) and [import-map editor](../../../repos/ui/mfe-base/src/admin/ImportMap/common/useController.tsx#L48-L49) reuse the role helper.
No `entitlementSource`, `ems3AppId`, or `ems3AppName` editor field was observed in this bounded frontend review.
The recovered per-tile switching requirement makes this an operational configuration surface to reconcile.

Consequence: backend migration metadata needs compatible update and audit paths.
Owner: unknown. Next action: reconcile editor payloads, CSV contracts, audit fields, and omitted-field behavior with the BFF.
Limit: the backend agent owns BFF update semantics and database mapping evidence.

### FE-04: Shared permissions affect many application actions

Confidence: high for inspected source.
The [shared authenticator](../../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L6-L105) reads several authorization representations.
It accepts flat `user.entitlement.actions` and entity-to-subject action maps.
It reads role from `dataEntitlementRoles`, `role`, or the `X_RATANONE` entity's `roleName`.
Entity conversion can overwrite earlier entries with the same entity name.

The helper checks `X_RATANONE` first, then legacy entity matching.
Legacy subject matching uses case conversion, underscores, and a settlement-rule special case.
Some [exception actions](../../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L303-L339) also depend on role `PSS_RO`.
The [ViewSelector](../../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/ViewName.tsx#L43-L59) carries an optional `ems2Subject` into permission checks.

The [cashflow import](../../../repos/ui/mfe-cashflow-blotter/src/Root/import/ratanutils/index.ts#L1-L7) consumes this shared authenticator through `@fm/ratan_container`.
The [authorization-limit helper](../../../repos/ui/mfe-cashflow-blotter/src/Cashflow_Authorization_Limits/Main/utils/index.ts#L5-L16) derives Maker, Checker, and Visitor roles from action codes.
The [utilization helper](../../../repos/ui/mfe-cashflow-blotter/src/Cashflow_Utilization_Static_Table/state/permission.ts#L5-L28) also distinguishes combined Maker_Checker access.
The [feature flag helper](../../../repos/ui/mfe-cashflow-blotter/src/Root/common/utils/featureFlagController.ts#L128-L141) compares user identifiers and entitlements.

Consequence: tile visibility alone cannot prove equivalent business action permissions.
Owner: unknown. Next action: inventory action-code mappings and verify each affected shared consumer.
Limit: these are compatibility surfaces, not confirmed new defects or runtime observations.

### FE-05: Existing CES proxy declarations are partial infrastructure evidence

Confidence: high for configuration bytes; low for effective deployment.
The [Nginx declaration](../../../repos/infra/nginx/config-ratan/non_ratan_proxy.conf#L1034-L1070) provides CES API and UI routes.
It declares `/api/fmces/p400/`, `/fmces_container/`, and `/fmces_tiles/`.
The [upstream](../../../repos/infra/nginx/config-ratan/non_ratan_upstream.conf#L323-L325) targets the named CES production host.
The [local root config](../../../repos/ui/mfe-root-config/webpack.config.js#L48-L74) declares API proxies and a localhost auth target.

Consequence: deployment routing, server-side API connectivity, and frontend assets need separate configuration checks.
Owner: unknown. Next action: identify effective environment routes and release artifacts.
Limit: existing proxy declarations prove neither backend CES authentication nor successful live requests.

## Existing intended rules already answered

These answers must not be requested again without a material source conflict.
The domain topic remains a candidate; owner approval and deployed enforcement remain separate.

| Rule | Answer and confidence | Direct source | Limit |
| --- | --- | --- | --- |
| Portal entry | High: deny entry without any registered application entity entitlement. | [Entry answer](../../ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-source.json) | No HTTP status or denial wording selected. |
| Entry environments | High: local, test, UAT, production. | [Scope answer](../../ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-scope-source.json) | Deployment not verified. |
| Missing tile entity | High: hide tile and deny direct launch until configured. | [Empty-entity answer](../../ui-test-coverage-20261022/evidence/clarification-20261022/empty-entity-source.json) | Original wording concerns EMS2 configuration. CES mapping needs explicit reconciliation. |
| Empty subject with one entity | High: allow visibility and launch through the entitled entity check. | [Empty-subject answer](../../ui-test-coverage-20261022/evidence/clarification-20261022/empty-subject-source.json) | Multiple-entity matching remains unanswered. |
| Empty-subject ownership and scope | High: portal team, all four environments. | [Owner and scope answer](../../ui-test-coverage-20261022/evidence/clarification-20261022/empty-subject-owner-scope-source.json) | Does not grant publication or deployment approval. |

The [domain topic](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-subject-rule) links these rules.
Application data permissions remain separate from portal entry and tile visibility.
The [architecture topic](../../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#ratan-authentication-and-authorization) contains stale Auth EMS3 absence wording.
The [later question record](../../ui-test-coverage-20261022/05-knowledge-questions.md#kq-arch-16) records newer Auth EMS3 source inspection.
Use exact current source when resolving this conflict.

## Test evidence and limits

### Inspected assertions

Confidence: high that these assertions exist; execution was NOT_RUN.
The [admin helper tests](../../../repos/ui/mfe-base/src/admin/common/utils/index.test.ts#L6-L55) assert `SUPER_USER` and undefined results.
The [shared authenticator tests](../../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.test.ts#L396-L442) assert role extraction and allowed or denied action checks.
They use controlled frontend fixtures.
They do not prove CES sample compatibility or deployed permission equivalence.

The [CES cashflow suite](../../../repos/testing/ratan-test-engine/Tests/ratan/workspace/api/STLM-API-OpenAPI-CESEntitlement.robot#L94-L108) asserts excluded cashflows, included cashflows, and matching total counts.
Its [setup](../../../repos/testing/ratan-test-engine/Tests/ratan/workspace/api/STLM-API-OpenAPI-CESEntitlement.robot#L333-L352) writes `ratanone:ces_data_entitlement:s:<user>` Redis keys directly.
Its [teardown](../../../repos/testing/ratan-test-engine/Tests/ratan/workspace/api/STLM-API-OpenAPI-CESEntitlement.robot#L354-L360) deletes those keys.
This bypasses the live CES-to-cache ingestion path.
The inspected suite therefore supplies data-permission assertions, not proof of the migration's complete data flow.

Source inspection identifies the cache producer.
The [Auth constant](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/util/Constant.java#L8) declares the same Redis key prefix.
The [Auth controller](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/Ems3EntitlementController.java#L23-L26) exposes `GET /v1/data-entitlement`.
The [service](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java#L93-L116) checks Redis, obtains an FMAA token, and reads CES on cache miss.
It [writes the mapped filter](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java#L142-L149) using `dataFilterTtlSeconds`.
The [configuration](../../../repos/services/ratan-auth-server/src/main/resources/application.yml#L181-L186) sets that TTL to 3600 seconds.
That configured value does not establish an approved freshness requirement.
The [reset endpoint](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/Ems3EntitlementController.java#L36-L47) supports one user or all users.
Confidence: high for inspected producer code; live ingestion and downstream consumption remain unverified.
The suite also creates business test data. No execution was requested or performed here.

### Coverage state

| Matrix | Applicable denominator | Current evidence | Result |
| --- | --- | --- | --- |
| Migration AC to tests | Unresolved: approved migration AC inventory unavailable. | Existing helper and cashflow assertions only. | Not calculable. |
| Migration AC to code change | Unresolved: approved migration AC and full change inventory unavailable. | Consumer source inspection only. | Not calculable. |
| Code change to tests | Unresolved: no frontend migration change set supplied. | Existing source tests are not direct migration-change proof. | Not calculable. |

No 100% conformance or passing-execution claim follows from these links.

## Material remaining evidence or decisions

| ID | Question or evidence need | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| FE-Q1 | Which CES applications map to each existing tile entity and admin role? | Wrong mappings can alter access decisions. | unknown | Reconcile an approved mapping table with source and samples. |
| FE-Q2 | Does any entity suffice when a tile lists multiple entities? | Multi-entity migration cases lack a stable expected result. | portal team for policy; confirmation pending | Check remaining migration report intent before asking the owner. |
| FE-Q3 | Auth produces the keys. Live ingestion, downstream consumption, and refresh or revocation limits remain unverified. | Direct cache mocks cannot prove full data authorization migration. | unknown | Trace exact downstream consumers and retain live CES-to-query evidence. |
| FE-Q4 | Which frontend, shared container, proxy, and downstream backend artifacts form the release? | Current filesystem copies cannot establish deployment coverage. | unknown | Supply exact release inventory and target environment identities. |

## Proposed sequence from these observations

This sequence is an inference, pending reconciliation with the user's migration report.

1. Freeze existing entry, tile, action, admin, and data-permission semantics against the recovered user intent.
2. Approve CES application, role, subject, and action mappings.
3. Preserve or version the normalized frontend contract during backend adoption.
4. Update configuration, CSV, audit, and shared permission consumers together.
5. Compare equivalent EMS2 and CES users through entry, launch, actions, and data queries.
6. Verify live CES ingestion separately from direct Redis fixtures.
7. Verify per-tile testing switches, final CES selections, and remaining EMS2 upstream calls.
8. Bind release routing and frontend shared modules to exact artifacts.
9. Cut over only after the applicable candidate unit suite passes completely.

## Writing checks

Local Markdown link paths and retained source hashes passed checks.
These checks do not validate complete ASD grammar or business conformance.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Source review does not establish deployed behavior or passing execution.
```
