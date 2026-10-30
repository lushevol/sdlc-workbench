# EMS2 to CES Comparison

Before and after for user, service and data authorization, with concrete blotter mappings. The primary CES view returns permission names; numeric permission IDs and per-permission roles are absent.

```text
/fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/{userid}
```

## User authorization

| Before EMS2 | After CES |
|---|---|
| **Entity**  X_RATANONE<br>**Entity ID**  11274101<br>**Model**  Role, subject and action objects.<br>**Example role**  FMO_OPS_BOM, ID 11274177. | **Application**  RATAN_ENTITLEMENT_RULE<br>**External reference**  itam_id = "51358".<br>**Model**  entitlement_name[] and {feature, action} pairs.<br>**IDs**  Internal appUID, feature, role and action IDs are not returned. |

## Service authorization

| Before EMS2 | After CES |
|---|---|
| **Entity**  RATAN_FUNC<br>**Example account**  srv.ratan.001<br>**Example role**  SYS_RO. | **Functional grants**  Feature and action names.<br>**Auth output pattern**  `RATAN_FUNC:<action>:<feature>`<br>**Limit**  Actual CES service-account grants and SYS_RO equivalence remain unconfirmed. |

## Data authorization

| Before EMS2 | After CES |
|---|---|
| **Entity**  RATAN_DATA_ENTITLEMENT<br>**Example assignment**  Global.<br>**Model**  A data-role assignment in the account response. | **Model**  data_profiles, data_policies and data_entitlements[].<br>**Filter mapping**  key becomes field; values remain strings.<br>**Limit**  Global does not have a confirmed one-to-one profile mapping. |

## Field structure and correspondence

| Before EMS2 | After CES |
|---|---|
| subject {id, name, longName, entity} | feature: string. The two blotter names match; subject ID and longName are not returned. |
| role {id, name, entity} | entitlement_name: string[]. Role names are separate from permission pairs; role ID and pair-to-role links are absent. |
| action {id, name, entity} | action: string within role_entitlements[]. The action name is returned; action ID is absent. |
| One grant row with a grant ID and parent role. | Effective {feature, action} pairs across assigned roles. The complete structures do not map one-to-one. |

Name-based checks must retain application scope. Missing numeric IDs and role provenance cannot be reconstructed from this endpoint alone.

Earlier FlowZero example: the catalog contains RATAN_FLOW_ZERO with ACCESS_FMO_POST_TRADE_PORTAL. Its exact FLOW_ZERO alias and effective user grant remain unconfirmed.

## Blotter comparisons

The After columns below use only the effective user endpoint. “Not returned” means the numeric field is absent.

### Strategic cashflow blotter

| Before EMS2 | After CES |
|---|---|
| **Application**  X_RATANONE | **Application**  RATAN_ENTITLEMENT_RULE |
| **Entity ID**  11274101 | **Internal application ID**  Not returned.<br>**External reference**  itam_id = "51358". |
| **Subject**  RATAN_STRATEGIC_CASHFLOW_BLOTTER | **Feature**  RATAN_STRATEGIC_CASHFLOW_BLOTTER |
| **Subject ID**  11274215 | **Feature ID**  Not returned. |
| **Role**  FMO_OPS_BOM<br>**Role ID**  11274177 | **Role**  Names are listed separately; no per-feature link. FMO_OPS_BOM is absent for the sample user.<br>**Role ID**  Not returned. |
| **Portal access**  ACCESS_FMO_POST_TRADE_PORTAL<br>**Action ID**  11274984 | **Portal access**  ACCESS_FMO_POST_TRADE_PORTAL<br>**Action ID**  Not returned. |
| **Export**  F_Export_Data<br>**Action ID**  11274960 | **Export**  F_Export_Data<br>**Action ID**  Not returned. |
| **Portal-access grant ID**  410988 | **Grant ID**  Not returned. |

### Trade blotter

| Before EMS2 | After CES |
|---|---|
| **Application**  X_RATANONE | **Application**  RATAN_ENTITLEMENT_RULE |
| **Entity ID**  11274101 | **Internal application ID**  Not returned.<br>**External reference**  itam_id = "51358". |
| **Subject**  RATAN_TRADE_BLOTTER | **Feature**  RATAN_TRADE_BLOTTER |
| **Subject ID**  11274226 | **Feature ID**  Not returned. |
| **Role**  FMO_OPS_BOM<br>**Role ID**  11274177 | **Role**  Names are listed separately; no per-feature link. FMO_OPS_BOM is absent for the sample user.<br>**Role ID**  Not returned. |
| **Portal access**  ACCESS_FMO_POST_TRADE_PORTAL<br>**Action ID**  11274984 | **Portal access**  ACCESS_FMO_POST_TRADE_PORTAL<br>**Action ID**  Not returned. |
| **Export**  F_Export_Data<br>**Action ID**  11274960 | **Export**  F_Export_Data<br>**Action ID**  Not returned. |
| **Portal-access grant ID**  411003 | **Grant ID**  Not returned. |

### Earlier comparison using detailed CES views

| Before EMS2 | After CES |
|---|---|
| Entity ID 11274101<br>Strategic subject ID 11274215<br>Trade subject ID 11274226<br>FMO_OPS_BOM role ID 11274177<br>Portal-access action ID 11274984<br>Export action ID 11274960 | Internal appUID 10<br>Strategic feature ID 176<br>Trade feature ID 172<br>FMO_OPS_BOM catalog entitlement ID 593<br>Portal-access action ID 193<br>Export action ID 208 |

These IDs require other CES response views. The same-name catalog role matches the sampled 20 strategic and six trade action names. Its definition and the user’s effective assignments remain separate comparisons.

## Login API and Single UI BFF

The public login contract remains stable. The migration changes the authorization read and the contents of the normalized entitlement objects.

| Before EMS2 | After CES |
|---|---|
| Browser `/api/auth/v2/sso/login` and `/api/auth/v3/sso/login` proxy to BFF `POST /v2/sso/login` and `POST /v3/sso/login`. The BFF reads configured EMS2 entities, then calls `getEntitlements()` and `getDrawer()`. | The browser and BFF routes and request bodies remain the same. The BFF calls `TileAuthorizationService`; each CES tile is grouped by configured app ID/name and feature, then `getAuthorizedDrawer()` applies the grant. |
| Response fields remain `result`, `userInfo`, `oud`, `entitlementsToken`, `entities`, and `drawers`. The `Single-UI-Authorization` response header carries the JWT. | The response fields and header remain the same. `entities` still use the legacy DTO shape so MFBase does not need a route change. |
| EMS2 entity, role, subject, and action objects normally carry numeric IDs and a role name. | CES-derived objects carry configured entity names, feature names, action names, and `entitlementSource: EMS3`; the mapper leaves entity, role, subject, and action IDs unset. `roleName` is also unset unless a separate mapping supplies it. |
| `entitlementsToken` is built from `entityName:roleName` and subject-to-action arrays from EMS2 results. | The same projection is built from the combined result. A CES-only response therefore needs an explicit trusted role mapping before role-dependent token consumers use the `entityName:roleName` key. |
| Authorization is EMS2-only. | The BFF supports `EMS2_ONLY`, `EMS3_PRIMARY_DUAL_READ`, and `EMS3_ONLY`. The current local configuration selects `EMS3_PRIMARY_DUAL_READ`; a CES read failure preserves legacy results only for non-CES tile scopes. |

The BFF implementation is in [`JwtAuthenticationController`](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:100) and [`AuthorizationResultMapper`](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:62). The full local comparison is commit `834b415` to `134a340`.

## MFBase browser storage

MFBase has no CES-specific migration commit. It consumes the same normalized BFF response and writes the same storage keys before and after.

| Before EMS2 | After CES |
|---|---|
| `SET_TOKEN` and `SET_USER` are written to both `localStorage` and `sessionStorage`. `SET_USER` contains normalized user fields, EMS2 `entities`, and `user.entitlements` decoded from `entitlementsToken`. | The storage locations and key names are unchanged. `SET_USER` can now contain CES-derived entities with feature/action names, `entitlementSource: EMS3`, and missing numeric IDs or role fields. |
| Login handlers dispatch `SET_ENTITIES`, `SET_DRAWERS`, `SET_ENTITLEMENTS_TOKEN`, and `refreshToken` into runtime state. They do not call `storeData()` for these values. | They remain runtime state. Raw CES `user_data`, `role_entitlements`, app IDs, feature IDs, action IDs, role provenance, policies, and profiles are not persisted by MFBase. |
| Reload reads `SET_USER`, `SET_TOKEN`, `SET_ENTITIES`, theme, time type, and workspaces from local storage. | Reload behavior is unchanged. The persisted user payload must therefore tolerate the CES projection while consumers that require IDs or `roleName` still need reconciliation. |

The storage behavior is implemented in [`login.ts`](../../repos/ui/mfe-base/src/utils/login.ts:40), [`common.ts`](../../repos/ui/mfe-base/src/utils/common.ts:38), and [`root.ts`](../../repos/ui/mfe-base/src/hooks/model/root.ts:117). The current branch's session-refresh fixes are separate from the CES migration.

## Auth Service

| Before EMS2 | After CES |
|---|---|
| Full entitlement reads call EMS2 entity endpoints, build legacy action strings, cache the legacy projection, and read `RATAN_DATA_ENTITLEMENT` roles from the EMS2 account response. | Full reads support `EMS2_ONLY`, `EMS3_PRIMARY_DUAL_READ`, and `EMS3_ONLY`. CES calls `/fmces/v1/entitlement/app/{appId}/{appName}/user/{userId}` with an FMAA bearer token, then maps feature/action pairs into the legacy projection. |
| User actions are derived from EMS2 action/entity names. Service-account actions append the EMS2 subject name. | Human actions become `feature:action`; system actions become `RATAN_FUNC:action:feature`. Configured role mappings, such as `RATAN_ENTITLEMENT_COMMON → FMO_OPS_BOM`, supply legacy role names. |
| One legacy cache stores the EMS2 `RatanEntitlement` projection. | CES uses source-checked envelopes and separate user/system keys, plus user-action and data-filter caches. Current configured TTLs are 3600 seconds for the legacy projection and data filter, and 900 seconds for user actions. |
| JWT conversion receives data roles from the EMS2 account read. | The full JWT action/role read can be CES primary, but `readDataEntitlement()` still calls the EMS2 reader in every migration mode. `Ems3LegacyEntitlementReader` returns an empty data-role projection. Full EMS2 retirement is therefore incomplete. |
| Data authorization is represented as a legacy role name. | The separate CES data-filter path returns profiles, policies, and field/value filters. It maps each CES `key` to `field` and preserves values as strings with an `ANY` or `ALL` relation. |

See [`EntitlementMigrationFacade`](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:35), [`JwtConvertorForNewUse`](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/jwtparser/convertor/JwtConvertorForNewUse.java:113), and [`RedisEntitlementCacheService`](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheService.java:30). The full local comparison is commit `7e8cbfa` to `dd6ebe8`.

## Runtime verification limits

No live browser or real API response was available in this workspace. Ports `8088`, `8000`, `8002`, `8003`, and `8015` were not listening. The BFF test attempt stopped before compilation because private Maven starters were unavailable, and the documented startup also requires private database, LDAP, signing-key, EMS2/CES, FMAA, and identity settings. The comparisons above are source and supplied-dump results; they do not claim deployed login behavior.

## Raw JSON examples

Expand the examples below. Selected records retain their original fields and values; the CES response is complete.

<details>
<summary>Before EMS2 — assignments for the three entities</summary>


Original `entitlementTypes` entries. The first two belong to human account `1481696`; the third belongs to service account `srv.ratan.001`.

**X_RATANONE**

```json
{
  "uniqueName": "11274101|X_RATANONE|11274177|FMO_OPS_BOM",
  "roleName": "FMO_OPS_BOM",
  "roleDescription": "",
  "applicationName": "RATAN",
  "isPrivilege": "N"
}
```

**RATAN_DATA_ENTITLEMENT**

```json
{
  "uniqueName": "11164654|RATAN_DATA_ENTITLEMENT|11515751|Global",
  "roleName": "Global",
  "roleDescription": "Global",
  "applicationName": "RATAN",
  "isPrivilege": "N"
}
```

**RATAN_FUNC**

```json
{
  "uniqueName": "1514522250|RATAN_FUNC|1514522302|SYS_RO",
  "roleName": "SYS_RO",
  "roleDescription": "",
  "applicationName": "RATAN",
  "isPrivilege": "N"
}
```

</details>

<details>
<summary>Before EMS2 — strategic cashflow portal-access grant</summary>


One original record from `1481696.entitlements[]`.

```json
{
  "id": 410988,
  "subject": {
    "id": 11274215,
    "name": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
    "longName": "/RATAN_STRATEGIC_CASHFLOW_BLOTTER",
    "entity": {
      "id": 11274101,
      "name": "X_RATANONE",
      "systemName": "RATAN",
      "locked": true
    }
  },
  "role": {
    "id": 11274177,
    "name": "FMO_OPS_BOM",
    "entity": {
      "id": 11274101,
      "name": "X_RATANONE",
      "systemName": "RATAN",
      "locked": true
    },
    "roleDescription": null,
    "isPrivilege": null
  },
  "action": {
    "id": 11274984,
    "name": "ACCESS_FMO_POST_TRADE_PORTAL",
    "entity": {
      "id": 11274101,
      "name": "X_RATANONE",
      "systemName": "RATAN",
      "locked": true
    }
  }
}
```

</details>

<details>
<summary>Before EMS2 — trade blotter portal-access grant</summary>


One original record from `1481696.entitlements[]`.

```json
{
  "id": 411003,
  "subject": {
    "id": 11274226,
    "name": "RATAN_TRADE_BLOTTER",
    "longName": "/RATAN_TRADE_BLOTTER",
    "entity": {
      "id": 11274101,
      "name": "X_RATANONE",
      "systemName": "RATAN",
      "locked": true
    }
  },
  "role": {
    "id": 11274177,
    "name": "FMO_OPS_BOM",
    "entity": {
      "id": 11274101,
      "name": "X_RATANONE",
      "systemName": "RATAN",
      "locked": true
    },
    "roleDescription": null,
    "isPrivilege": null
  },
  "action": {
    "id": 11274984,
    "name": "ACCESS_FMO_POST_TRADE_PORTAL",
    "entity": {
      "id": 11274101,
      "name": "X_RATANONE",
      "systemName": "RATAN",
      "locked": true
    }
  }
}
```

</details>

<details>
<summary>After CES — complete effective endpoint response</summary>


`/fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/1481696`

This response includes all returned role names, functional permissions, policies, profiles and data-filter values. It contains no internal application, feature, role, action or grant IDs.

```json
[
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
      "data_policies": {
        "policy_rules": [
          {
            "data_policy_name": "RATAN - GBS CN PSS",
            "policy_owner": "2021102"
          }
        ]
      },
      "data_profiles": {
        "data_profile_rules": [
          {
            "data_profile_name": "RATAN- Back2Back FMID CN",
            "data_profile_owner": "1666699"
          },
          {
            "data_profile_name": "RATAN - back2back FMID",
            "data_profile_owner": "2021102"
          },
          {
            "data_profile_name": "RATAN - ALL ACCESS User",
            "data_profile_owner": "2021102"
          }
        ]
      },
      "data_entitlements": [
        {
          "key": "Entity.Booking_Entity_SCI_FMID",
          "values": [
            "10040387",
            "400568282",
            "10038345",
            "400516442",
            "400516443",
            "400667486",
            "10020899",
            "FMIDBRAMX01",
            "400683682",
            "400327728",
            "400107029",
            "300010872",
            "401053411",
            "300036368",
            "400910415",
            "15",
            "400075752",
            "400609343",
            "400058959",
            "400677737",
            "10041902",
            "300010633",
            "400011581",
            "10041903",
            "2",
            "123",
            "3",
            "400130178",
            "4",
            "400095464",
            "5",
            "400452428",
            "10038468",
            "6",
            "10054931",
            "7",
            "8",
            "9",
            "400131263",
            "401081696",
            "FINNKOREA01",
            "400040353",
            "300010782",
            "400170359",
            "10041530",
            "300011470",
            "MUXBZ01",
            "10036981",
            "401037180",
            "300084297",
            "123M",
            "10075222",
            "400013111",
            "400960089",
            "1234",
            "400041070",
            "400001378",
            "400045551",
            "10062461",
            "300011345",
            "400032489",
            "400451508",
            "400033177",
            "400931959",
            "10037164",
            "10032025",
            "10063428",
            "400045549",
            "300075472",
            "400991880",
            "400617263",
            "235003861",
            "400192940",
            "300089409",
            "400059978",
            "10078716",
            "400077046",
            "400077044",
            "400057714",
            "400798477",
            "400209000",
            "401036553",
            "FM ID TST 1",
            "400088463",
            "400085753",
            "400220273",
            "400218197",
            "400007847",
            "300063361",
            "300011525",
            "400077978",
            "10036647",
            "400054708",
            "10036642",
            "10036645",
            "10038667",
            "400193370",
            "400090093",
            "10022098",
            "400994973",
            "400521212",
            "400130180",
            "400013557",
            "10037477",
            "10036382",
            "400227738",
            "400054741",
            "400172181",
            "10036775",
            "400054737",
            "10036655",
            "400044944",
            "400625349",
            "400823493",
            "400229749",
            "400093619",
            "10036430",
            "400018439",
            "400906330",
            "400017223",
            "300010730",
            "400147183",
            "10036428",
            "400022800",
            "400185419",
            "400899993",
            "195000930",
            "400823482",
            "400823485"
          ]
        }
      ],
      "role_entitlements": [
        {
          "feature": "RATAN_SETTLEMENT_EXCEPTION",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_AUTO_NETTING_RULE",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_OPTION_EXPIRY_BLOTTER",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "Entitlement",
          "action": "View"
        },
        {
          "feature": "RATAN_CASHFLOW_BLOTTER",
          "action": "F_Custom_Query_Builder"
        },
        {
          "feature": "RATAN_TRADE_BLOTTER",
          "action": "F_Export_Data"
        },
        {
          "feature": "Reports",
          "action": "View"
        },
        {
          "feature": "RATAN_MO_EXCEPTION",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_VALIDATION_EXCEPTION",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
          "action": "F_Custom_View_Builder_Private"
        },
        {
          "feature": "RATAN_FM_COO_RULE",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_TRADE_BLOTTER",
          "action": "F_Custom_View_Builder_Private"
        },
        {
          "feature": "RATAN_OPTION_EXPIRY_BLOTTER",
          "action": "F_Option_Expiry_Read"
        },
        {
          "feature": "RATAN_TRADE_BLOTTER",
          "action": "F_Custom_Query_Builder"
        },
        {
          "feature": "RATAN_CASHFLOW_BLOTTER",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_CASHFLOW_BLOTTER",
          "action": "F_Export_Data"
        },
        {
          "feature": "RATAN_FM_COO_EXCEPTION",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
          "action": "F_Custom_Query_Builder"
        },
        {
          "feature": "RATAN_ENTITLEMENT_RULE",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_PROFILE_LIMITS",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_MO_RULE",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_TRADE_BLOTTER",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_CASHFLOW_BLOTTER",
          "action": "F_Custom_View_Builder_Private"
        },
        {
          "feature": "RATAN_SUPPRESSION_RULE",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_SETTLEMENT_STP_RULE",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_CASHFLOW_GROUP_BLOTTER",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_NETTING_RULE",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_NOSTRO_BLOTTER",
          "action": "ACCESS_FMO_POST_TRADE_PORTAL"
        },
        {
          "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
          "action": "F_Export_Data"
        }
      ]
    }
  }
]
```

</details>

[Open full EMS2 grant JSON](api/:ems2:rest:entitlements:entitlementList%20.json) · [Open full CES response JSON](api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json)
