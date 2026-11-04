---
artifact_kind: interface-contract
id: CES-OUTPUT-MAPPING
version: 5
status: draft
owner: unknown
source_refs: [USER-ENDPOINT-TABLE-20261030, USER-CONSOLIDATION-20261030, USER-ENDPOINT-20261030, USER-FIELD-20261030, USER-MIGRATION-20261030, EMS2-GRANTS, CES-ROLE-DETAILS, CES-CATALOG, CES-EFFECTIVE, ENDPOINT-CONSUMERS, RATAN-BACKEND]
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
    - Source correspondence does not establish approved role equivalence, deployment, or passing business execution.
---

# Ratan EMS2 to CES migration: consolidated comparison

> **The effective endpoint supports name-based permissions but cannot recreate the complete numeric EMS2 structure.**
> Action: adapt consumers or provide an authoritative crosswalk where numeric IDs remain mandatory.
> Consequence: missing IDs and role provenance cannot be recovered from the effective response alone.
> Owner: unknown. Evidence: [combined mapping](#field-correspondence-and-cardinality) and [consumer effects](#ratan-specific-migration-differences).
>
> **Final Ratan migration still requires remaining EMS2 dependencies to be addressed.**
> Action: reconcile Auth data-role reads, deployed SDK consumers, and trusted admin-role mappings.
> Consequence: selecting `EMS3_ONLY` does not establish complete EMS2 independence.
> Owner: unknown. Evidence: [current backend findings](evidence/backend-analysis-20261030.md#remaining-legacy-dependencies).

Latest high-priority scope: [update the blotter table using only the effective endpoint](evidence/user-input-20261030-endpoint-only-table.txt).

This document combines the detailed field mapping and the effective-endpoint comparison for Ratan.
It covers identity, structure, cardinality, concrete blotter examples, and migration effects across current consumers.

The user confirms **`X_RATANONE → RATAN_ENTITLEMENT_RULE`** as the EMS2-to-CES name migration.
Source: [exact clarification](evidence/user-input-20261030-field-equivalence.txt), 30 October 2026.
Numeric IDs, permission sets, and user assignments retain separate evidence requirements.

The requested consolidation is preserved as a [high-priority reference](evidence/user-input-20261030-consolidated-comparison.txt).
Earlier document versions remain available at commits `605fe48f4` and `cf4794bac`, using this same path.
This document replaces their presentation. It preserves the original samples and historical evidence.

## Contract identity and boundary

| Field | Value |
| --- | --- |
| Contract ID and type | CES-OUTPUT-MAPPING; provider response and Ratan consumer compatibility comparison. |
| Contract maturity | Confirmed name migration and inspected structures; unresolved semantic equivalence remains explicit. |
| Provider IDs | EMS2 and CES; external registry identities unresolved. |
| Consumer IDs | Ratan Auth Server, Single UI BFF, shared frontend permissions, and downstream SDK consumers. |
| Repository IDs | `ratan-auth-server`, `single-ui-bff`, `mfe-base`, `mfe-ratan-container`, `single-ui-auth-sdk`. |
| Relationship evidence | Retained API samples and exact local source inspection; no live CES request in this stage. |
| Full Git commits | Auth `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2`; BFF `134a340472f29d2a4136e07e516690de6a18e323`. |
| Source path and lines | [Field facts and JSON pointers](evidence/field-equivalence-facts-20261030.json); [consumer locators](evidence/effective-endpoint-consumers-20261030.json). |
| Documentation gap | Complete approved role/assignment equivalence, authoritative numeric crosswalk, and deployed consumer inventory. |

Scope includes `RATAN_STRATEGIC_CASHFLOW_BLOTTER` and `RATAN_TRADE_BLOTTER` within the confirmed renamed application.
It also explains the separate service and data-authorization migration boundaries.
Confidence is HIGH for exact sample fields, recorded clarification, and inspected implementation.
Confidence in complete deployed equivalence remains UNKNOWN.

## Operations and delivery

| Operation or view | Address or source | Returned structure | Relevant difference |
| --- | --- | --- | --- |
| EMS2 account assignments | `/ems2/rest/account/{accountName}`; supplied human and service samples. | Account metadata and `entitlementTypes[]` with composite `uniqueName`. | Entity and role IDs appear together in the composite assignment. |
| EMS2 functional grants | [Supplied entitlement-list dump](api/:ems2:rest:entitlements:entitlementList%20.json). | `[userId].entitlements[]`, containing nested subject, role, action, and entity references. | One row describes one role/subject/action grant. Exact capture query unavailable. |
| CES assigned-role details | [Supplied user-role response](api/-fmces-v1-entitlement-user-1481696.json). | Role objects containing `featureActionDtos[]`. | Retains feature/action IDs and their parent role. |
| CES application catalog | [Supplied application catalog](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json). | Role definitions with name-based `role_entitlements[]` and `user_ids`. | Defines roles; presence does not establish effective access for a user. |
| CES effective user grants | `/fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/{userid}`. | Application/user context, assigned role names, flattened permissions, and data scope. | Omits numeric permission IDs and each pair's parent role. |

These are response comparisons, not a complete CES delivery contract.
Capture dates, environments, pagination, error contracts, and synchronized deployment evidence remain unavailable.
No external request, retry, or business mutation ran during consolidation.

## Inputs

| Input | Type | Use | Limit |
| --- | --- | --- | --- |
| User/account identity | String; sample `1481696`. | Select effective human permissions. | CES service-account identity mapping requires separate evidence. |
| External application/ITAM reference | String; `51358`. | Select the CES application route and retain scope. | It is separate from internal application ID and legacy entity ID. |
| CES application name | String; `RATAN_ENTITLEMENT_RULE`. | Confirmed destination name for `X_RATANONE`. | Other EMS2 entities do not automatically share this rename. |
| Sample and source identity | Exact file hash or Git revision. | Bind each field and implementation claim. | Hashes establish bytes, not authority or deployment. |

## Authentication and authorization

Current backend CES retrieval uses an FMAA bearer token.
Effective feature/action pairs support functional permission checks within the returned application scope.
Assigned role names remain a collection, separate from each flattened permission pair.
Data profiles and policies remain separate from functional permissions.
Source: [backend investigation](evidence/backend-analysis-20261030.md#confirmed-auth-server-behavior).

Ratan's migration covers three distinct responsibilities:

| EMS2 scope | CES representation | Ratan migration implication |
| --- | --- | --- |
| `X_RATANONE` | Renamed application `RATAN_ENTITLEMENT_RULE`, with role names and feature/action grants. | Preserve intended portal entry, tile, and business-action permissions through reviewed mappings. |
| `RATAN_FUNC` | System mapper consumes CES role names and feature/action pairs. Output pattern: `RATAN_FUNC:<action>:<feature>`. | Verify actual service-account assignments. No CES service-account response was supplied. |
| `RATAN_DATA_ENTITLEMENT` | Data profiles, policies, and returned field/value filters. | Confirm legacy `Global` equivalence and actual downstream data enforcement. |

The final objective requires zero EMS2 dependencies across Ratan.
Tiles can switch independently during testing; final service authorization uses CES exclusively.
Source: [preserved user direction](evidence/historical-user-inputs-20261028-29.json).

## Outputs

### Field correspondence and cardinality

This table combines detailed CES correspondence with availability from the effective endpoint.
EMS2 paths are relative to one grant row.
CES detail paths are relative to one assigned-role object.
Effective paths are relative to response element `[0]`.

| EMS2 field and type | CES detail equivalent and type | Effective endpoint field | One-to-one mapping and Ratan consequence |
| --- | --- | --- | --- |
| `subject.entity.name`: string. | `appName`: string; repeated in `featureActionDtos[].features.applicationDto.appName` and the action's application context. | `user_data.app_name`. | **Confirmed name pair:** `X_RATANONE → RATAN_ENTITLEMENT_RULE`. |
| `subject.entity.id`: integer. | Internal `appUID`: integer; repeated within `applicationDto`. | **Absent.** `user_data.itam_id` is a separate string reference. | One application scope corresponds here. Numeric IDs differ and cannot be copied. |
| `subject`: object containing `id`, `name`, `longName`, and `entity`. | `featureActionDtos[].features`: object containing `featureId`, `featureName`, and `applicationDto`. | A string `feature` on each permission pair. | One logical subject corresponds to one feature in both examples; object structure changes. |
| `subject.name`: string. | `featureActionDtos[].features.featureName`: string. | `entitlements.role_entitlements[].feature`. | **Names match** for both requested blotters. Names must retain application scope. |
| `subject.id`: integer. | `featureActionDtos[].features.featureId`: integer. | **Absent.** | One observed logical ID pair per blotter; values are regenerated. The effective response cannot supply them. |
| `role`: object repeated per EMS2 grant row. | Assigned-role object, or catalog entitlement definition containing a grant collection. | Assigned role-name collection, separate from permission pairs. | Role/feature relationships are many-to-many. Regrouping is not one-to-one by row. |
| `role.name`: string. | Detail `entitlementName`; catalog `entitlement_name`: string. | `entitlements.entitlement_name[]`: string array. | A same-name `FMO_OPS_BOM` definition exists. Its assignment must be checked separately. |
| `role.id`: integer. | Detail `entitlementId`: string in supplied samples. Catalog `entitlement_id`: integer. | **Absent.** | Candidate definition correspondence: `11274177 → 593`. It does not establish whole-role or user-assignment equivalence. |
| `action.name`: string. | `featureActionDtos[].actions.actionName`: string. | Each pair's `action`: string. | Matching action names correspond within the inspected blotters and application scope. |
| `action.id`: integer. | `featureActionDtos[].actions.actionId`: integer. | **Absent.** | Logical action correspondence is observed; numeric values change. |
| Grant-row `id`: integer. | No direct equivalent demonstrated for this individual combination. | **Absent.** | **No demonstrated one-to-one field.** CES `entitlementId` identifies a role, not the EMS2 grant row. |
| `subject.longName`: string. | No separate field in the supplied feature object. | **Absent** as a separate field. | No direct equivalent demonstrated. Feature names remain available. |
| Account metadata: status, type, full name, owner. | Complete CES account/profile equivalent not supplied. | No equivalent full account fields in this sample. | Preserve required account behavior through an authoritative source or a revised contract. |
| Legacy data-role assignment, such as `Global`. | `data_profiles.data_profile_rules[].data_profile_name` and separate policies/data rules. | `data_profiles`, `data_policies`, and `data_entitlements`. | Approved profile equivalence remains unknown. A role name alone does not define returned data scope. |

### Concrete blotter mappings

This table uses **only** `/fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/{userid}` for CES values.
Numeric IDs from role details and the application catalog are excluded from this table.
The retained effective-response sample is for user `1481696`.

| Field | `RATAN_STRATEGIC_CASHFLOW_BLOTTER` | `RATAN_TRADE_BLOTTER` |
| --- | --- | --- |
| Entity/application name | `X_RATANONE → RATAN_ENTITLEMENT_RULE`; returned in `user_data.app_name`. | `X_RATANONE → RATAN_ENTITLEMENT_RULE`; returned in `user_data.app_name`. |
| Entity/internal application ID | `11274101` → **Not returned**; no `appUID`. | `11274101` → **Not returned**; no `appUID`. |
| Available CES application reference | `user_data.itam_id: "51358"`; separate external string reference. | `user_data.itam_id: "51358"`; separate external string reference. |
| Subject/feature name | `RATAN_STRATEGIC_CASHFLOW_BLOTTER`, unchanged; returned as `feature`. | `RATAN_TRADE_BLOTTER`, unchanged; returned as `feature`. |
| Subject/feature ID | `11274215` → **Not returned**. | `11274226` → **Not returned**. |
| Same-name role | `FMO_OPS_BOM` is absent from the supplied CES role-name list. No per-feature role association is returned. | `FMO_OPS_BOM` is absent from the supplied CES role-name list. No per-feature role association is returned. |
| Role/catalog entitlement ID | `11274177` → **Not returned**. | `11274177` → **Not returned**. |
| Portal-access action | `ACCESS_FMO_POST_TRADE_PORTAL`, unchanged; returned as `action`. | `ACCESS_FMO_POST_TRADE_PORTAL`, unchanged; returned as `action`. |
| Portal-access action ID | `11274984` → **Not returned**. | `11274984` → **Not returned**. |
| Export action name | `F_Export_Data`, unchanged; returned as `action`. | `F_Export_Data`, unchanged; returned as `action`. |
| Export action ID | `11274960` → **Not returned**. | `11274960` → **Not returned**. |
| EMS2 portal-access grant ID | `410988` → **Not returned**. | `411003` → **Not returned**. |

Each effective permission object contains only `feature` and `action` strings.
Role names exist separately in `entitlements.entitlement_name[]`.
That collection does not identify which role supplies a particular feature/action pair.
Missing IDs and per-pair role provenance cannot be reconstructed from this endpoint alone.

This response can support application-scoped checks using feature/action names.
Consumers requiring numeric identities need an authoritative crosswalk or another CES response view.
Source: [effective endpoint response](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json).
Current table verification: [endpoint-only table checks](evidence/endpoint-only-table-checks-20261030.json).

### Structure transformation

| View | Data structure | Information retained |
| --- | --- | --- |
| EMS2 grant list | `userId → entitlements[] → {id, subject, role, action}`. | Each row retains grant ID and nested subject, role, action, and entity identities. |
| CES assigned-role details | `roles[] → {entitlementId, entitlementName, appName, appUID, featureActionDtos:[{features, actions}]}`. | Groups pairs beneath roles; retains feature/action IDs and role provenance. |
| CES catalog | `roles[] → {entitlement_id, entitlement_name, role_entitlements:[{feature, action}], user_ids}`. | Retains role IDs and definitions; each feature/action pair uses names. |
| CES effective response | `[{user_data, entitlements:{entitlement_name:[], role_entitlements:[{feature, action}], ...}}]`. | Supplies role-name collection, effective name pairs, and data scope. Numeric permission IDs and per-pair roles are omitted. |

One role contains many feature/action pairs, and one feature can occur in many roles.
The effective view flattens the returned permissions across assigned roles.
Therefore, entire responses do **not** map one-to-one by row, nesting, or retained information.

### Role definition versus user assignment

The sampled EMS2 grants use `FMO_OPS_BOM`, role ID `11274177`.
CES catalog pointer `/56` contains the same-name role with integer ID `593`.
Its 20 strategic and six trade actions match the sampled EMS2 grant sets exactly.

The supplied CES user's role-detail response instead includes `NON_FMO_RO`, string ID `"601"`.
That role supplies four effective actions for each requested blotter in the sample.
The supplied user's CES assignments do not include `FMO_OPS_BOM`.

**`FMO_OPS_BOM → NON_FMO_RO` is not a demonstrated migration mapping.**
Catalog definitions and effective user assignments must be compared separately.

Across all features, the sampled EMS2 role has 63 unique feature/action pairs.
CES catalog role `593` has 68, including five additional validation-exception pairs.
Thus, the requested blotters match while complete role equivalence remains unresolved.

### Using only the effective user endpoint

Endpoint:

```text
/fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/{userid}
```

This endpoint can support permission checks based on returned feature/action names within its application scope.
It cannot independently recreate the complete numeric EMS2 structure.
Its completeness for other applications, service-account identities, or full account attributes remains unproved.

The following is an abridged projection of the supplied effective response.
It displays all six returned role names, two observed permission pairs, and three of 129 data values.
Other permissions, policy metadata, and profile metadata are omitted from this display only.

```json
{
  "user_data": {
    "app_name": "RATAN_ENTITLEMENT_RULE",
    "itam_id": "51358",
    "user_id": "1481696"
  },
  "entitlements": {
    "entitlement_name": [
      "RATAN_ENTITLEMENT_COMMON",
      "NON_FMO_RO",
      "RATAN_ENTITLEMENT_GLOBAL",
      "FM Read Only",
      "RATAN_ENTITLEMENT_DEV_USERS",
      "FM Trading Plus - FX Cash"
    ],
    "role_entitlements": [
      {
        "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
        "action": "F_Export_Data"
      },
      {
        "feature": "RATAN_TRADE_BLOTTER",
        "action": "F_Export_Data"
      }
    ],
    "data_entitlements": [
      {
        "key": "Entity.Booking_Entity_SCI_FMID",
        "values": ["10040387", "FMIDBRAMX01", "FM ID TST 1"]
      }
    ]
  }
}
```

This response contains user/application references and policy/profile owner references.
Its missing IDs are the permission-object IDs and internal application ID discussed above.
The numeric values `176`, `172`, `208`, and `593` cannot be derived from these name pairs alone.

Ratan's current Auth converter can project the two returned pairs into these human permission strings:

```text
RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Export_Data
RATAN_TRADE_BLOTTER:F_Export_Data
```

Keep application scope when evaluating either string.
A proposed permission key is `(itam_id, app_name, feature, action)`.
Names require controlled rename handling; this is not a claim of immutable identity.

The role-name collection does not identify which role supplied a particular pair.
Do not assign every grant to every listed role or select the first role arbitrarily.

### Ratan-specific migration differences

| Ratan area | EMS2 coupling or existing behavior | CES difference and required treatment | Evidence |
| --- | --- | --- | --- |
| Auth functional entitlements | Legacy readers build role/action projections from EMS2 responses. | Current CES mapper uses configured role mappings and `feature:action` for humans. Preserve required action semantics. | [Backend behavior](evidence/backend-analysis-20261030.md#confirmed-auth-server-behavior). |
| Auth JWT data roles | A separate account read supplies legacy data-role names. | Current `EMS3_ONLY` still performs this EMS2 read. Complete retirement requires a reviewed replacement. | [Remaining dependency](evidence/backend-analysis-20261030.md#remaining-legacy-dependencies). |
| Single UI BFF response | Frontend receives entity, role, subject, action, and token structures. | CES mapper reconstructs configured entity names and subject/action names. Numeric IDs and `roleName` remain unset. | [Consumer facts](evidence/effective-endpoint-consumers-20261030.json). |
| Shared frontend permissions | Most inspected checks use names or flat action strings. | Effective name pairs can support these checks, subject to equivalent application and action mappings. | [Current checks](evidence/effective-endpoint-consumers-20261030.json). |
| Profile and TypeScript models | Types require numeric fields; Profile rendering uses entity/subject IDs. | Revise optional-field contracts and rendering keys where permitted. Missing IDs are not universally harmless. | [Current consumers](evidence/effective-endpoint-consumers-20261030.json). |
| Admin authorization | Entity scope and trusted `roleName` drive token and ownership checks. | Assigned CES role names need explicit trusted mappings. This one application's response does not establish other admin scopes. | [Admin consumers](evidence/effective-endpoint-consumers-20261030.json). |
| Tile configuration | Existing source defaults to EMS2 and legacy entity/subject settings. | Current BFF supports source, CES app ID/name/features, per-tile grants, CSV fields, and audit columns. Configure every applicable tile. | [BFF behavior](evidence/backend-analysis-20261030.md#confirmed-bff-behavior). |
| Tile IDs | Portal configuration uses its own tile identities. | These IDs remain separate from absent CES entitlement IDs. Do not remove configuration IDs with permission IDs. | [Consumer investigation](evidence/effective-endpoint-consumers-20261030.json). |
| Data scope | Legacy `Global` role is an assignment name. | CES returns profiles, policies, and field/value filters. Preserve string values and verify enforcement separately. | [Data examples](evidence/output-mapping-examples-20261030.json). |
| Shared Auth SDK | The inspected older SDK revision calls EMS2 endpoints. | Identify deployed versions and migrate actual consumers. Local older source cannot disprove a newer deployed SDK. | [SDK boundary](evidence/backend-analysis-20261030.md#remaining-legacy-dependencies). |

Source inspection establishes these compatibility boundaries.
It does not establish deployed failure, user disruption, or passing business behavior.

### Suggested migration treatment

This sequence is a proposal derived from the inspected differences.
It is not implementation approval or a release decision.

1. Bind the application rename, selected CES response contract, and complete Ratan consumer inventory.
2. Use application-scoped feature/action names for consumers that support effective grants.
3. Preserve complete role-name collections and define trusted mappings for role-dependent operations.
4. Make absent permission IDs optional only where the consumer contract permits that change.
5. Revise Profile rendering keys and related numeric-field assumptions when necessary.
6. Maintain an authoritative crosswalk if unchanged consumers require numeric identity.
7. Obtain CES detail data when exact IDs or role provenance are mandatory and no crosswalk exists.
8. Complete separate data-role, service-account, SDK, tile-configuration, and account-attribute migration boundaries.
9. Compare equivalent users and role definitions, then verify permissions and business workflows at exact candidate revisions.

A generated hash or sequence number is a local identifier; it cannot recover the missing authoritative ID.
A managed crosswalk requires scope, source authority, versioning, and update ownership.
Keeping normalized legacy field names does not itself create an EMS2 runtime dependency.

### Exact sample locators

| Fact | Source | JSON pointer |
| --- | --- | --- |
| EMS2 strategic portal-access row | [EMS2 grants](api/:ems2:rest:entitlements:entitlementList%20.json). | `/1481696/entitlements/60`. |
| EMS2 trade portal-access row | [EMS2 grants](api/:ems2:rest:entitlements:entitlementList%20.json). | `/1481696/entitlements/61`. |
| CES strategic feature `176`, portal action `193` | [CES role details](api/-fmces-v1-entitlement-user-1481696.json). | `/5/featureActionDtos/3`. |
| CES trade feature `172`, portal action `193` | [CES role details](api/-fmces-v1-entitlement-user-1481696.json). | `/5/featureActionDtos/14`. |
| CES same-name role `593` | [CES catalog](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json). | `/56`. |
| Effective application identity and grants | [CES effective sample](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json). | `/0/user_data`; `/0/entitlements/role_entitlements`. |

## Errors

The supplied samples do not establish a complete CES error contract.
Missing numeric IDs in effective output are a response-shape limitation, not evidence of an API failure.
Code failure handling must remain separate from approved outage and revocation policy.
No new error defaults or permission rules were selected during consolidation.

## Compatibility and verification

Consolidation changes this document and task navigation only.
Application implementation and existing knowledge records remain unchanged in this stage.

| Check or evidence | Result | Limit |
| --- | --- | --- |
| Exact field IDs and same-role action-set comparisons | [Retained field facts](evidence/field-equivalence-facts-20261030.json). | The 20/6 match does not establish whole-role or account-assignment equivalence. |
| Effective response fields and consumer dependencies | [Endpoint checks](evidence/effective-endpoint-checks-20261030.json). | No live CES request or behavior execution. |
| Consolidated document lint, source hashes, links, and embedded example | [Current document checks](evidence/consolidated-comparison-checks-20261030.json). | Automated checks do not establish semantic equivalence or complete ASD compliance. |
| Previously recorded rename and provenance | [Knowledge validation](evidence/field-equivalence-knowledge-validation-20261030.json). | Candidate knowledge remains unpublished. No new governance transition occurred. |

Business execution: NOT_RUN. No new product ACs, test definitions, or implementation changes were introduced.
Migration AC-to-test and AC-to-code denominators remain incomplete in the [intake](01-intake.md#traceability).
Code-to-test evidence remains partial; this document supplies no new passing-execution or conformance percentage.

## Evidence and uncertainty

| Source ID | Locator | Exact revision or identity | Hash | Authority and limit |
| --- | --- | --- | --- | --- |
| USER-ENDPOINT-TABLE-20261030 | [Latest endpoint-only table request](evidence/user-input-20261030-endpoint-only-table.txt). | User message, 30 October 2026. | [Table checks](evidence/endpoint-only-table-checks-20261030.json). | User; high-priority output scope. |
| USER-CONSOLIDATION-20261030 | [Consolidation request](evidence/user-input-20261030-consolidated-comparison.txt). | User message, 30 October 2026. | [Current checks](evidence/consolidated-comparison-checks-20261030.json). | High-priority document scope. |
| USER-ENDPOINT-20261030 | [Endpoint-only question](evidence/user-input-20261030-effective-endpoint-only.txt). | User message, 30 October 2026. | [Endpoint checks](evidence/effective-endpoint-checks-20261030.json). | Hypothetical implementation scope, not an approved deployment choice. |
| USER-FIELD-20261030 | [Confirmed rename and requested fields](evidence/user-input-20261030-field-equivalence.txt). | User clarification, 30 October 2026. | [Field checks](evidence/field-equivalence-checks-20261030.json). | High-priority authority for name correspondence only. |
| USER-MIGRATION-20261030 | [Migration request](evidence/user-input-20261030-migration-plan.txt) and [historical direction](evidence/historical-user-inputs-20261028-29.json). | Preserved user messages. | [Original source register](evidence/source-register-20261030.json). | Final zero-EMS2 intent; current deployment remains unverified. |
| EMS2-GRANTS | [EMS2 grants](api/:ems2:rest:entitlements:entitlementList%20.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Observed fields and values only. |
| CES-ROLE-DETAILS | [CES assigned-role details](api/-fmces-v1-entitlement-user-1481696.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Feature/action IDs and sampled assignments. |
| CES-CATALOG | [CES catalog](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Role definitions do not prove effective access. |
| CES-EFFECTIVE | [CES effective response](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json). | Capture revision unknown. | [Field facts](evidence/field-equivalence-facts-20261030.json). | Flattened names and data scope; IDs and pair-to-role provenance omitted. |
| ENDPOINT-CONSUMERS | [Consumer facts](evidence/effective-endpoint-consumers-20261030.json). | Exact revisions and file hashes retained. | Per-source SHA-256. | Inspected implementation, not execution. |
| RATAN-BACKEND | [Backend analysis](evidence/backend-analysis-20261030.md) and [manifest](evidence/backend-source-manifest-20261030.json). | Auth/BFF revisions listed above; older SDK revision identified separately. | Per-source SHA-256. | Local implementation and deployment limits remain separate. |

### Knowledge-update log

The confirmed rename remains recorded in [KT-sdk-and-entitlements v7](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#user-confirmed-ems2-to-ces-name-migration).
Its [audit event](../../evidence/knowledge/audit/AUD-20261030-KT-sdk-and-entitlements-v7.yaml) and source provenance remain unchanged.
This request consolidates existing findings and adds no new business-policy answer.
No additional governed record update or publication is required for this presentation change.

## Findings and actions

These are mapping and compatibility limits, not reproduced product failures or release-blocking decisions.

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| FIELD-01 | [User clarification](evidence/user-input-20261030-field-equivalence.txt). | Entity/application name correspondence is resolved. | User supplied clarification; record owner unknown. | Use `X_RATANONE → RATAN_ENTITLEMENT_RULE` within this migration scope. | RESOLVED |
| FIELD-02 | [Role and action comparisons](evidence/field-equivalence-facts-20261030.json). | Whole-role and account-assignment equivalence remain unconfirmed. | unknown | Reconcile the five additional pairs and intended user assignments. | OPEN |
| FIELD-03 | [Effective response and consumer dependencies](evidence/effective-endpoint-consumers-20261030.json). | Missing IDs and role provenance affect existing contracts. | unknown | Adapt permitted consumers or supply authoritative enrichment. | OPEN |
| RATAN-01 | [Remaining backend dependencies](evidence/backend-analysis-20261030.md#remaining-legacy-dependencies). | Complete EMS2 retirement is not established by current local source. | unknown | Resolve Auth data roles, deployed SDK consumers, and trusted admin-role mappings. | OPEN |
