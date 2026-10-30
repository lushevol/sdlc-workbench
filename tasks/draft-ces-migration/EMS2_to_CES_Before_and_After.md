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

The login API contract remains stable. The authorization data schema changes.

| Before EMS2 | After CES |
|---|---|
| Browser calls `/api/auth/v2/sso/login` or `/api/auth/v3/sso/login`; the BFF receives `/v2/sso/login` or `/v3/sso/login`. | Routes, request bodies, JWT header, and response envelope remain unchanged. |
| `entities` contains EMS2 entity, role, subject, and action objects, usually with numeric IDs. | `entities` retains the same outer schema, but CES rows expose application/entity names, feature names, action names, and `entitlementSource: EMS3`; numeric IDs and role provenance are absent. |
| `drawers` reflect EMS2 entity-based access. | `drawers` reflect CES application/feature grants for migrated tiles. |
| `entitlementsToken` contains the legacy entity/role and subject/action projection. | The legacy token field remains, but CES role names must be mapped before role-dependent consumers can rely on it. |

## MFBase browser storage

MFBase keeps the same storage contract. Only the entitlement payload changes.

| Before EMS2 | After CES |
|---|---|
| `SET_TOKEN` and `SET_USER` are stored in both `localStorage` and `sessionStorage`. `SET_USER` contains normalized user data, EMS2 entities, and decoded entitlement actions. | The same keys and storage locations are used. `SET_USER` may contain CES feature/action names, `entitlementSource: EMS3`, and missing numeric IDs or role fields. |
| Runtime state includes `entities`, `drawers`, `entitlementsToken`, and `refreshToken`. | The same runtime fields are used. Raw CES response sections, app IDs, permission IDs, role provenance, policies, and profiles are not stored by MFBase. |
| Reload uses the existing stored user and token schema. | Reload behavior is unchanged. Consumers that require numeric IDs or role names need a compatible mapping. |

## Auth Service

| Before EMS2 | After CES |
|---|---|
| Full entitlement API calls read EMS2 entity data. The output is a legacy role/action projection. | Full entitlement reads use CES through `/fmces/v1/entitlement/app/{appId}/{appName}/user/{userId}` and project CES feature/action pairs into the existing role/action output. |
| Functional authorization and data roles both originate from EMS2. | Functional authorization can be CES primary, dual-read, or CES-only. CES data filters expose profiles, policies, and field/value filters. |
| Data authorization is a legacy role name from `RATAN_DATA_ENTITLEMENT`. | The current Auth Service still reads JWT data roles from EMS2. Complete EMS2 retirement is therefore not finished. |
| Cache data is an EMS2 legacy projection. | CES cache records include source and version metadata, with separate user, system, action, and data-filter projections. |

## Runtime verification limits

No live browser or real API response was available in this workspace. The comparisons above use supplied dumps and local API/schema definitions; they do not claim deployed login behavior.

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
