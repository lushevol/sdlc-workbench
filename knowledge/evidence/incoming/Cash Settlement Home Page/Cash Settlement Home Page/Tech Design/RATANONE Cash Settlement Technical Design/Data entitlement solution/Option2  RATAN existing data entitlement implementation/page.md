# Existing implementation introduction

Reference: <u>[RATANONE Data Entitlement Solution - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATANONE+Data+Entitlement+Solution)</u>

Existing solution involves two kind of entitlement:

- Function entitlement checks if a user is permitted to access an API
- Data entitlement controls the data that is visible to this user

### Authentication

User sso login with username or sso, and get a jwt token.

### Fetching EMS2 data

```bash
GET https://uklvauems01a.uk.standardchartered.com:16443/ems2/rest/account/1481696
{
    "accountStatus": "A",
    "accountName": "1481696",
    "accountType": "User",
    "fullName": "IIQ1481696,User",
    "accountOwner": "1481696",
    "entitlementTypes": [
        {
            "uniqueName": "1511446402|MXMLS_FILEUPLOAD_BSM|1511446459|DPS_MLS",
            "roleName": "DPS_MLS",
            "roleDescription": "",
            "applicationName": "MUREX G2000",
            "isPrivilege": "N"
        }
        ...
    ],
    "status": ""
}
```

```bash
POST https://uklvadapp1345.uk.dev.net:3833/v3/authenticate
single-ui-authorization Bearer eyJ...
{
    "entitlement": "{\"role\":\"FMO_OPS_BOM\",\"actions\":[\"RATAN_TRADE_BLOTTER:ACCESS_FMO_POST_TRADE_PORTAL\", ...],\"dataEntitlementRoles\":\"Global\"}",
    "userInfo": {
        "userId": "1481696",
        "fullName": "1481696",
        "country": "Global",
        "entitlementCountry": "China"
    }
}
```

### EMS2 func entitlement

We get user entitlements when login from EMS2, which defines the allowed actions in a structure as bellow:

{
    " id " : 11274101 ,
    " name " : "X_RATANONE" ,
    " applicationName " : "RATAN" ,
    " roleId " : 11274177 ,
    " roleName " : "FMO_OPS_BOM" ,
    " subjects " : [
        {
            " longName " : "/RATAN_CASHFLOW_BLOTTER" ,
            " name " : "RATAN_CASHFLOW_BLOTTER" ,
            " id " : 11274218 ,
            " actions " : [
                {
                    " name " : "F_Ad_Hoc_Nostro_Initiate" ,
                    " id " : 11274299 ,
                    " entitlementId " : 11806798
                },
                // ...
            ]
        }
    ]
}

The data is then cached in frontend and will be checked when user perform an action, also there's check inside API.

Existing roles and actions are defined as bellow table:

| Role | RATAN_AUTO_NETTING_RULE | Subject.. |
| --- | --- | --- |
| FMO_OPS_BO | F_Ad_Hoc_Nostro_Initiate, … | … |
| FMO_OPS_BOC | F_Ad_Hoc_Nostro_Initiate, … | … |
| FMO_OPS_BOL | F_Ad_Hoc_Nostro_Initiate, … | … |
| FMO_OPS_BOM | F_Ad_Hoc_Nostro_Initiate, … | … |
| FMO_OPS_MKR | F_Ad_Hoc_Nostro_Initiate, … | … |
| FMO_OPS_INV | ACCESS_FMO_POST_TRADE_PORTAL | … |
| FMO_RO | F_Custom_Query_Builder… | … |
| NON_FMO_RO | F_Custom_Query_Builder… | … |
| PSS_RO | F_Custom_Query_Builder… | … |

Each API is registered with func entitlements in API gateway:

![image-2025-7-24_15-13-25.png](attachments/image-2025-7-24_15-13-25.png)

### Data entitlement

The entitlement filtering logic has already been implemented in v2/data/provider/query/cashflows (LoopQueryController.java) in query service. Additional request is invoked in order to get filtering condition:

GET <static-data-service>/v2/rule/entitlement?role=Onshore&country=Nepal

Entity.Booking_Entity_SCI_FMID IN ('400007847')

The country data is obtained from OUD¹, and it's set to the token when login.

Currently we've the following entitlement roles:

| Role | Intension | Description |
| --- | --- | --- |
| Global | Able to view all RATAN data | Able to view all data |
| GBS | Used by India & Malaysia GBS Ops who is not Onshore user only | Apply forbidden rules |
| OnShore | supporting onshore business | Apply permitted rules |

# ![image-2025-7-23_18-12-17.png](attachments/image-2025-7-23_18-12-17.png)

# Feasibility Assessment

The requirement is fulfilled as current solution already supports:

| Requirement | Supported by Current Design? | Configuration or Gap |
| --- | --- | --- |
| **Onshore users can access only their location's data.** | Yes | Use `permitted_rule` for each country. Example: `Entity.Booking_Entity_SCI_FMID IN (...)`. |
| **Users in one country need access to another country's data.** | Yes | Add `permitted_rule` for cross-country access. Example: Dubai users accessing Egypt and Saudi data. |
| **Prohibit specific access (e.g., India vs Pakistan).** | Yes | Use `forbidden_country` and `forbidden_rule`. Example: India users cannot access Pakistan data. |
| **Taiwan data restrictions (approved locations, role-based exceptions).** | Partially | Approved locations can be configured using `permitted_rule`. Role-based exceptions need additional logic. |
| **Region-based access (e.g., ASEAN Regional Head).** | No | Requires grouping of countries into regions and assigning roles for regional access. |
| **Function-based access (e.g., ETD users).** | No | Requires tagging users with functions and applying function-specific rules. |
| **Global access with restrictions (e.g., GBS users).** | Partially | Global roles can be configured, but exceptions (e.g., India-Pakistan) need explicit `forbidden_rule`. |
| **Hierarchy-based access (e.g., senior management).** | No | Requires additional logic to define hierarchy and assign enhanced entitlements. |
| **Multiple entitlement tagging for backup purposes.** | No | Current design does not support multiple entitlements per user. |

## Assumption

- [x] We can get the country codes and distinguish them, eg. for Taiwan we can get Taiwan as country code

```
{"lastName":"Song","country":"Taiwan","firstName":"Sybil", ...
```

- We'll use current onboarding flow: for non-prod environments, we need to configure database manually. For prod environment, it's maintained in EMS2, and if want to add rules we need new deployment.

## Estimation

| Change | Component | Effort | Remark |
| --- | --- | --- | --- |
| Onboard taiwan rules | static-data-service | 2 | Insert new data and unit test |
| SSDR report | query service | 1 | Existing code, add unit test |
| Cashflow blotter | query service | 1 | Existing logic uses mocked entitlements |
| Cashflow history | query service | 2 | New logic |
| Group blotter | group management service | 3 | New logic |