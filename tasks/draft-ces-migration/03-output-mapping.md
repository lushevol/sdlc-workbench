---
artifact_kind: interface-contract
id: CES-OUTPUT-MAPPING
version: 1
status: draft
owner: unknown
source_refs: [USER-MAPPING-20261030, EMS2-CES-SAMPLES, AUTH-MAPPER, BFF-MAPPER]
related_ids: [CES-MIGRATION]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
    - Samples and source inspection do not establish approved permission equivalence or passing business execution.
---

# EMS2 to CES output mapping

> **Confirm the unresolved semantic mappings before implementation.**
> Action: resolve service roles, the `Global` data role, and the `FLOW_ZERO` naming correspondence.
> Consequence: those mappings remain incomplete despite confirmed output structures.
> Owner: unknown. Evidence: [mapping limits](#findings-and-actions).

High-priority source: [exact mapping request](evidence/user-input-20261030-output-mapping.txt), 30 October 2026.
This source-query stage follows the [migration intake](01-intake.md).
It preserves earlier intent and the original API sample bytes.
No application code, approved policy, or deployed configuration changed.

## Contract identity and boundary

| Field | Value |
| --- | --- |
| Contract ID and type | CES-OUTPUT-MAPPING; candidate HTTP response and adapter mapping. |
| Contract maturity | Documented sample structures; candidate semantic equivalence. |
| Provider IDs | EMS2 and CES; external service catalog identities unresolved. |
| Consumer IDs | `ratan-auth-server`, `single-ui-bff`; shared frontend consumers are supporting evidence. |
| Relationship evidence | Retained response samples and exact local provider/consumer source. No live relationship execution. |
| Repository IDs | `ratan-auth-server`, `single-ui-bff`, `mfe-base`, `mfe-ratan-container`, `mfe-cashflow-blotter`. |
| Source path and lines | [Sample facts and pointers](evidence/output-mapping-sample-facts-20261030.json); [code facts and locators](evidence/output-mapping-code-facts-20261030.json). |
| Full Git commits | Auth `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2`; BFF `134a340472f29d2a4136e07e516690de6a18e323`. |
| Documentation gap | Approved role equivalence, CES service-account response, FlowZero alias, and complete data enforcement bindings. |

The three EMS2 entities describe different authorization responsibilities.
CES distributes these responsibilities across role grants, profile metadata, and data filters.
They are not three demonstrated CES application-name replacements.

Confidence is HIGH for retained field values and inspected conversion code.
Confidence in unresolved semantic equivalence is UNKNOWN.

## Operations and delivery

| Operation | Transport and address | Trigger | Side effects | Ordering, retry, timeout, and idempotency |
| --- | --- | --- | --- | --- |
| EMS2 account lookup | GET `/ems2/rest/account/{accountName}`. | Read human or service-account assignments. | Runtime consumers may cache projections. | Operational contract not established by samples. |
| EMS2 functional grants | Supplied entitlement-list response; exact capture query unavailable. | Read entity, role, subject, and action records. | No execution in this stage. | Capture parameters and pagination unknown. |
| CES effective grants | Current code uses GET `/fmces/v1/entitlement/app/{appId}/{appName}/user/{userId}`. | Read one account's application grants and data scope. | Runtime consumers may cache projections. | Current implementation settings differ from authoritative CES delivery rules. |
| CES catalog and role details | Supplied application catalog and role-detail response shapes. | Inspect role definitions and membership. | No execution in this stage. | Complete endpoint contracts and effective-membership rules unknown. |

The current effective response sample uses app name `RATAN_ENTITLEMENT_RULE` and ITAM identifier `51358`.
That application name contains grants for several features, including both requested blotters.
It must not be replaced with `X_RATANONE` solely because EMS2 uses that entity name.

## Inputs

| Name and location | Type or schema | Required | Validation and limits | Example |
| --- | --- | --- | --- | --- |
| EMS2 account name | String path parameter. | For account lookup. | Account status and service identity need separate validation. | `1481696`; `srv.ratan.001`. |
| CES user ID | String path parameter and `user_data.user_id`. | Current effective lookup. | A CES service-account ID mapping is not supplied. | `1481696`. |
| CES application scope | App ID and app name. | Current effective lookup. | ITAM ID and internal app UID are distinct. | External `51358`; sampled internal `appUID` is `10`. |
| EMS2 entity mapping | Caller configuration and response entity names. | Compatibility projection. | CES effective grants contain no literal EMS2 entity field. | `X_RATANONE`. |
| Service-account mode | Boolean converter input. | Selects normalized action format. | It is caller context, not inferred from a human response. | `systemAccount=true`. |

## Authentication and authorization

Current backend CES retrieval uses an FMAA bearer token.
CES feature/action grants describe functional access.
CES profile and policy names describe assignment context; data rules provide returned field/value scope.
Source: [code claims and exact locators](evidence/output-mapping-code-facts-20261030.json).

A catalog grant does not establish that a particular user receives that grant.
A human account sample does not establish service-account permissions.
The following mappings keep those evidence boundaries explicit.

## Outputs

### Entity-level mapping

| EMS2 entity | EMS2 output structure and observed example | CES output structure | Auth/BFF compatibility output | Status and limit |
| --- | --- | --- | --- | --- |
| `X_RATANONE` | Account `entitlementTypes[].uniqueName` identifies entity and role. Sample role: `FMO_OPS_BOM`. Functional rows contain `subject.name`, `role.name`, and `action.name`. | `entitlement_name[]` contains assigned role names. `role_entitlements[]` contains `feature` and `action`. | Auth maps role names through configuration and emits `feature:action`. BFF reconstructs configured entity names and subject/action arrays. | HIGH for structure. The entity is not a literal CES response field. |
| `RATAN_FUNC` | Service account `srv.ratan.001`, `accountType: Service`, assigned role `SYS_RO`. | Current system mapper consumes the same `entitlement_name[]` and feature/action structure. | Auth emits `RATAN_FUNC:<action>:<feature>`. Service role requires configured equivalence. | HIGH for assignment and code format. No CES service-account response proves actual grants or `SYS_RO` equivalence. |
| `RATAN_DATA_ENTITLEMENT` | Account assignment names role `Global`. The account sample contains no field/value data rule. | `data_policies.policy_rules[]`, `data_profiles.data_profile_rules[]`, and `data_entitlements[]`. | Profile names can map to legacy data-role names. Rule `key` becomes filter `field`; `values` remain strings. | HIGH for structure. `Global` equivalence and each application's data enforcement remain unbound. |

Exact assignment locators:

- `X_RATANONE`: [EMS2 human account](api/:ems2:rest:account:1481696.json), JSON pointer `/entitlementTypes/55`.
- `RATAN_FUNC`: [EMS2 service account](api/:ems2:rest:account:srv.ratan.001.json), pointer `/entitlementTypes/0`.
- `RATAN_DATA_ENTITLEMENT`: [EMS2 human account](api/:ems2:rest:account:1481696.json), pointer `/entitlementTypes/13`.

### Field-level mapping

CES paths below are relative to the aggregate response element `[0]`.
They do not describe the separate camelCase role-detail DTO.

| EMS2 field or concept | CES field or concept | Mapping rule and qualification |
| --- | --- | --- |
| Root user-key `1481696`; account `accountName` | `user_data.user_id` | Preserve account identity through its approved mapping. Sample human IDs match. |
| `subject.entity.name`, `role.entity.name`, `action.entity.name` | No literal equivalent in effective grants. | Select CES application scope separately. Retain compatibility entity names through reviewed configuration. |
| `subject.name` | `entitlements.role_entitlements[].feature` | The requested blotter names match exactly in both samples. Other names require confirmation. |
| `action.name` | `entitlements.role_entitlements[].action` | Preserve the exact case-sensitive action identifier unless an approved mapping changes it. |
| `role.name`; `entitlementTypes[].roleName` | `entitlements.entitlement_name[]` | Names are not necessarily identical. Current Auth configuration maps `RATAN_ENTITLEMENT_COMMON` to `FMO_OPS_BOM`. |
| `entitlementTypes[].uniqueName` | Separate identity, role-name, and grant fields. | Do not reuse the composite EMS2 identifier as a CES entitlement ID. |
| Legacy entity, subject, role, action, and grant numeric IDs | No IDs in the aggregate feature/action rows. | Raw role details expose separate CES IDs. They are not legacy numeric identities. |
| `accountType`, `accountStatus`, `fullName`, `accountOwner` | No equivalent fields in supplied effective response. | Obtain account/profile contracts. BFF-derived owner values do not establish CES account ownership. |
| `RATAN_DATA_ENTITLEMENT` role name | `entitlements.data_profiles.data_profile_rules[].data_profile_name` | Requires explicit reviewed equivalence. Do not infer `Global` equals an all-access profile. |
| No matching policy metadata in supplied account sample | `entitlements.data_policies.policy_rules[]` | Policies carry names and owners. No direct EMS2 equivalent is demonstrated. |
| No field/value rule in supplied account assignment | `entitlements.data_entitlements[].key` and `.values` | Treat these as actual returned data scope, separate from functional grants. |
| No matching logical operator in supplied account assignment | `entitlements.data_entitlements_logical_indicator` | Current converter maps multiple-rule `AND` to `ALL`; `OR` or default becomes `ANY`. |

Current code links: [Auth conversion](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:28), [configured mappings](../../repos/services/ratan-auth-server/src/main/resources/application.yml:170), [BFF projection](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:62).

### CES response-shape differences

| Supplied CES response | Functional grant path | Role identity | Appropriate use |
| --- | --- | --- | --- |
| [Effective user/application response](api/-fmces-v1-entitlement-user-response-1481696.json) | `[0].entitlements.role_entitlements[].feature/action` | `[0].entitlements.entitlement_name[]`. | Current Auth/BFF aggregate model and the primary table above. |
| [User role-detail response](api/-fmces-v1-entitlement-user-1481696.json) | `[].featureActionDtos[].features.featureName` and `.actions.actionName`. | `[].entitlementId`, `[].entitlementName`. | Inspect individual assigned role definitions and CES feature/action IDs. |
| [Application catalog](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json) | `[].role_entitlements[].feature/action` | `[].entitlement_id`, `[].entitlement_name`; membership in `user_ids`. | Inspect defined roles. Catalog presence does not establish effective access. |
| [Role 588 detail](api/-fmces-v1-entitlement-588-app-51358-RATAN_ENTITLEMENT_RULE.json) | `featureActions[featureName][]`. | `entitlementId`, `entitlementName`. | Inspect one role's feature-to-action dictionary. |

### Requested application examples

The first two rows are exact shared sample pairs.
The third row is an actual catalog pair with an unresolved name correspondence.

| Requested application | EMS2 example | CES example | Auth human action projection | Evidence class and limit |
| --- | --- | --- | --- | --- |
| `RATAN_STRATEGIC_CASHFLOW_BLOTTER` | Entity `X_RATANONE`; role `FMO_OPS_BOM`; subject `RATAN_STRATEGIC_CASHFLOW_BLOTTER`; action `F_Export_Data`. | `{"feature":"RATAN_STRATEGIC_CASHFLOW_BLOTTER","action":"F_Export_Data"}` | `RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Export_Data` | HIGH: both sample pairs and current projection code. Complete role equivalence is unproved. |
| `RATAN_TRADE_BLOTTER` | Entity `X_RATANONE`; role `FMO_OPS_BOM`; subject `RATAN_TRADE_BLOTTER`; action `ACCESS_FMO_POST_TRADE_PORTAL`. | `{"feature":"RATAN_TRADE_BLOTTER","action":"ACCESS_FMO_POST_TRADE_PORTAL"}` | `RATAN_TRADE_BLOTTER:ACCESS_FMO_POST_TRADE_PORTAL` | HIGH: both sample pairs and current projection code. This is one access action, not all trade permissions. |
| `FLOW_ZERO` | No corresponding subject or entity appears in the supplied EMS2 account/grant samples. | Catalog: `{"feature":"RATAN_FLOW_ZERO","action":"ACCESS_FMO_POST_TRADE_PORTAL"}`. | If assigned and mapped: `RATAN_FLOW_ZERO:ACCESS_FMO_POST_TRADE_PORTAL`. | HIGH for catalog value; UNKNOWN for `FLOW_ZERO` alias. No such effective grant appears for user `1481696`. |

Exact example pointers:

| Example | EMS2 pointer | CES pointer | Source |
| --- | --- | --- | --- |
| Strategic export | `/1481696/entitlements/22`. | `/0/entitlements/role_entitlements/29`. | [EMS2 grants](api/:ems2:rest:entitlements:entitlementList%20.json); [CES effective grants](api/-fmces-v1-entitlement-user-response-1481696.json). |
| Strategic portal access | `/1481696/entitlements/60`. | `/0/entitlements/role_entitlements/19`. | Same [EMS2 source](api/:ems2:rest:entitlements:entitlementList%20.json) and [CES source](api/-fmces-v1-entitlement-user-response-1481696.json). |
| Trade export | `/1481696/entitlements/24`. | `/0/entitlements/role_entitlements/5`. | Same [EMS2 source](api/:ems2:rest:entitlements:entitlementList%20.json) and [CES source](api/-fmces-v1-entitlement-user-response-1481696.json). |
| Trade portal access | `/1481696/entitlements/61`. | `/0/entitlements/role_entitlements/22`. | Same [EMS2 source](api/:ems2:rest:entitlements:entitlementList%20.json) and [CES source](api/-fmces-v1-entitlement-user-response-1481696.json). |
| FlowZero catalog access | Unavailable. | `/22/role_entitlements/4`; parent role ID `194`, name `FMO_MO`. | [CES catalog](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json). |

The sample user has 20 EMS2 strategic actions and four CES effective strategic actions.
The trade counts are six and four.
Different role assignments and unknown capture conditions prevent interpreting these counts as permission loss.
Complete matching and differing actions remain in the [sample facts](evidence/output-mapping-sample-facts-20261030.json).

### Human-grant JSON example

This is an abridged EMS2 projection from `/1481696/entitlements/22`.
The labels below shorten nested fields for comparison; they are not the complete EMS2 response schema.

```json
{
  "entity": "X_RATANONE",
  "role": "FMO_OPS_BOM",
  "subject": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
  "action": "F_Export_Data"
}
```

The matching CES effective grant is the following exact object.
Application identity and assigned role names remain outside this object.

```json
{
  "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
  "action": "F_Export_Data"
}
```

Current Auth conversion emits `RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Export_Data` for this pair.
A matching pair does not establish complete permission parity.

### Service-account examples for RATAN_FUNC

Observed EMS2 assignment:

```json
{
  "accountName": "srv.ratan.001",
  "accountType": "Service",
  "assignment": {
    "uniqueName": "1514522250|RATAN_FUNC|1514522302|SYS_RO",
    "roleName": "SYS_RO"
  }
}
```

This projection shortens `/entitlementTypes/0` into the display label `assignment`.
No CES service-account response was supplied.
The table below shows code-defined output patterns, not observed service permissions.

| Requested application | CES service grant pattern | Auth system action pattern | Missing evidence |
| --- | --- | --- | --- |
| `RATAN_STRATEGIC_CASHFLOW_BLOTTER` | `feature=RATAN_STRATEGIC_CASHFLOW_BLOTTER`, `action=<approved-service-action>`. | `RATAN_FUNC:<approved-service-action>:RATAN_STRATEGIC_CASHFLOW_BLOTTER`. | Actual CES service role and action assignments. |
| `RATAN_TRADE_BLOTTER` | `feature=RATAN_TRADE_BLOTTER`, `action=<approved-service-action>`. | `RATAN_FUNC:<approved-service-action>:RATAN_TRADE_BLOTTER`. | Actual CES service role and action assignments. |
| `FLOW_ZERO` | `feature=<confirmed-flow-zero-feature>`, `action=<approved-service-action>`. | `RATAN_FUNC:<approved-service-action>:<confirmed-flow-zero-feature>`. | Exact feature identity, service role, and action assignments. |

The angle-bracket strings are symbolic placeholders. They are not configured permissions.
Human action identifiers must not be assumed to authorize the same service operations.
Source: [system conversion rule](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:147).

### Data-entitlement example

Observed EMS2 assignment:

```json
{
  "uniqueName": "11164654|RATAN_DATA_ENTITLEMENT|11515751|Global",
  "roleName": "Global",
  "roleDescription": "Global",
  "applicationName": "RATAN",
  "isPrivilege": "N"
}
```

The CES sample supplies these profile names separately:

- `RATAN- Back2Back FMID CN`.
- `RATAN - back2back FMID`.
- `RATAN - ALL ACCESS User`.

No source proves that `Global` equals any profile above.
The current configured profile outputs use the placeholder `approved-legacy-data-role`.
Those values do not establish an approved business mapping.
Source: [Auth configuration](../../repos/services/ratan-auth-server/src/main/resources/application.yml:174).

The following CES rule displays three of 129 observed values.
It is a reduced projection from `/0/entitlements/data_entitlements/0`.

```json
{
  "key": "Entity.Booking_Entity_SCI_FMID",
  "values": ["10040387", "FMIDBRAMX01", "FM ID TST 1"]
}
```

Current Auth filter conversion produces this corresponding reduced projection:

```json
{
  "enabled": true,
  "filters": [
    {
      "field": "Entity.Booking_Entity_SCI_FMID",
      "values": ["10040387", "FMIDBRAMX01", "FM ID TST 1"]
    }
  ],
  "condition": "ANY"
}
```

Preserve all values as strings, including numeric-looking values.
The supplied response has one data rule and no logical-indicator property.
The current converter uses `ANY` for that case.
Source: [filter conversion](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java:123).

These data filters are separate from the three applications' functional grants.
The sample does not bind each blotter or FlowZero to a specific downstream enforcement path.

## Errors

| Failure condition | Status or error code | Response content | Side effects and retry guidance |
| --- | --- | --- | --- |
| Missing CES account, empty grants, or dependency failure | Complete CES error contract unavailable. | No supplied error response. | Do not invent error shapes from successful examples. |
| No configured role mapping or conflicting mapped roles | Current mapper throws `IllegalStateException`. | Exact HTTP translation is outside this output comparison. | Source behavior, not an approved CES error contract. |
| Null or blank feature/action | Current mapper rejects the grant. | No verified external response or runtime result. | Resolve malformed grant behavior through the actual contract. |

## Compatibility and verification

The mapping table compares raw provider output and current compatibility projections separately.
It does not define new product acceptance criteria or executable test cases.
Business execution: NOT_RUN. No complete coverage denominator is established by this mapping stage.

Current EMS2 Auth code builds ordinary actions from `action.entity.name:action.name`.
The supplied legacy dump places `X_RATANONE` in that entity field and stores blotter names under `subject.name`.
Therefore, raw subject-to-feature mapping must not be described as universal current Auth string parity.
Endpoint-specific baseline responses and consumer expectations still need reconciliation.
Source: [legacy reader](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReader.java:94).

The BFF reconstructs configured entities and CES subject/action arrays.
Its CES mapper does not populate legacy numeric IDs or trusted `roleName`.
Auth's role-mapping configuration must not be assumed to fill that separate BFF field.
Source: [BFF mapping](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:62).

JWT data roles still use a separate EMS2 account read in every migration mode.
CES-derived filters and profile projections therefore do not establish complete JWT data-role migration.
Source: [JWT conversion](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/jwtparser/convertor/JwtConvertorForNewUse.java:128).

| Evidence scope | Check | Retained result | Limit |
| --- | --- | --- | --- |
| Eight source samples | Parse JSON, resolve retained pointers, and verify values. | [Sample checks](evidence/output-mapping-sample-facts-20261030.json). | Static source consistency only. |
| Source conversion | Inspect current mapper, consumer, configuration, and exact revisions. | [Code facts](evidence/output-mapping-code-facts-20261030.json). | No Java, browser, or service behavior execution. |
| Mapping examples | Compare abridged objects with retained raw values and code formulas. | [Example projections](evidence/output-mapping-examples-20261030.json). | Derived display projections; no approval or live access proof. |
| Document authoring | Lint structure, local references, and source fingerprints. | [Mapping document checks](evidence/output-mapping-checks-20261030.json). | Automated checks do not establish semantic equivalence. |

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| USER-MAPPING-20261030 | [Exact user input](evidence/user-input-20261030-output-mapping.txt). | User message, 30 October 2026. | [Mapping checks](evidence/output-mapping-checks-20261030.json). | User; high-priority requested scope. |
| EMS2-CES-SAMPLES | [Sample facts](evidence/output-mapping-sample-facts-20261030.json). | Supplied bytes; capture dates and environments unknown. | Full SHA-256 per sample. | Owner unknown; observed payload structures only. |
| AUTH-MAPPER | [Auth converter](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:28). | `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2`. | [Code source hashes](evidence/output-mapping-code-facts-20261030.json). | Owner unknown; implementation behavior. |
| BFF-MAPPER | [BFF converter](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:62). | `134a340472f29d2a4136e07e516690de6a18e323`. | [Code source hashes](evidence/output-mapping-code-facts-20261030.json). | Owner unknown; implementation behavior. |

Fact: both requested blotter names occur as EMS2 subjects and CES features.
Fact: `RATAN_FLOW_ZERO` occurs in five CES catalog roles.
Fact: none of those catalog roles lists sample user `1481696`.
Inference: `RATAN_FLOW_ZERO` may correspond to the user's `FLOW_ZERO` label.
Unknown: exact FlowZero legacy identifier, alias approval, and effective access.

The prior migration [mapping question](01-intake.md#mig-q3) remains the single policy clarification entry.
This document supplies concrete examples and narrows its remaining evidence needs.
No governed knowledge record or publication state changed.

## Findings and actions

These are mapping limits, not reproduced product defects or release blockers.

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| MAP-01 | [Service assignment and missing CES response](evidence/output-mapping-examples-20261030.json). | `SYS_RO` equivalence and actual service grants remain unknown. | unknown | Obtain the CES service-account response and approved role/action mapping. | OPEN |
| MAP-02 | [Global assignment and CES profiles](evidence/output-mapping-sample-facts-20261030.json). | A profile-name substitution could change data scope. | unknown | Confirm the intended profile/filter equivalence and each enforcement consumer. | OPEN |
| MAP-03 | [FlowZero catalog example](evidence/output-mapping-examples-20261030.json). | The requested name cannot yet be bound to an EMS2 subject or effective CES assignment. | unknown | Confirm the exact legacy and CES identifiers through [MIG-Q3](01-intake.md#mig-q3). | OPEN |
| MAP-04 | [Current legacy string construction](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReader.java:94). | The broad EMS2 dump cannot establish every endpoint's normalized action output. | unknown | Compare equivalent entity-scoped responses and consumer action checks. | OPEN |
