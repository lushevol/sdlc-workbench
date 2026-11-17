#

# Background

Linked story: [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13473901](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13473901)

Consider login function is provided by single-ui-bff, auth server only responsible for authorization function only. API gateway always call auth server when receive a request. So team plan to combine the code and provide only single service.

## OneMFA decommission

Standard Chartered Bank is migrating its enterprise Identity & Access Management (IAM) platform from ForgeRock (OneMFA / OneDS) to Microsoft Entra ID. The legacy ForgeRock platform is scheduled for full decommission by end of Q3 2026.

Key drivers for the migration:

| Driver | Detail |
| --- | --- |
| **Standardisation** | Entra ID is now the Bank's global SaaS SSO and MFA standard |
| **Modern protocols** | ForgeRock's RADIUS, Web Agent, and IG patterns are deprecated; Entra supports only SAML and OIDC |
| **User experience** | Windows Hello for Business (WHfB) enables seamless MFA — token refreshes silently within 60 minutes of workstation unlock |
| **Security posture** | Centralised Conditional Access policies, stronger MFA enforcement (FIDO2, Authenticator push) |

## ID isolated deployment

Ratan needs to be deployed for **Indonesia (ID)** as a regulatory-compliant instance with isolated data storage, separate from the global deployment. This introduces additional architectural constraints and objectives beyond the core Entra migration.

**Regulatory Requirement:** Indonesian financial regulation mandates that customer and transaction data must reside within in-country infrastructure. RatanOne's data storage (PostgreSQL, Redis) and session management must be provisioned as isolated, country-scoped instances.

## System components

| Component | Tech Stack | Role |
| --- | --- | --- |
| **SPA (Frontend)** | React / MFE | Browser-based client |
| **ratanone-api-gateway** | Spring Cloud Gateway (WebFlux, Java 17) | Edge gateway — routing, auth, audit |
| **single-ui-bff** | Spring Boot MVC (Java 17) | BFF — login, JWT issuance, session management |
| **ratanone-auth-server** | Spring Boot MVC (Java 17) | Token validation, Redis session store |
| **ForgeRock OpenAM** | External IdP | OIDC provider (current, being replaced) |
| **OUD (LDAP)** | Oracle Unified Directory | User directory (username/password auth) |
| **EMS2** | External REST service | Entitlements / RBAC |
| **Redis** | In-memory store | Session cache, token store |
| **PostgreSQL** | Relational DB | Session blacklist, app config |

## Objectivities

| # | Objective | Description |
| --- | --- | --- |
| 1 | **Merge API Gateway & Auth Server** | Consolidate `ratanone-api-gateway` and `ratanone-auth-server` into a single component to reduce system integration overhead and simplify the ID deployment topology |
| 2 | **Data Entitlement Token Optimisation** | Reduce payload size and improve performance of the `Single-UI-Entitlement` JWT — review claim structure, caching strategy, and TTL settings |
| 3 | **Functional Entitlement via FMCES** | Replace the current EMS2 dependency with **FMCES** as the entitlement source for functional RBAC, aligning with the Bank's target entitlement platform |
| 4 | **Entra Onboarding Interface Design** | Define the integration interface for Microsoft Entra ID, with particular focus on **system-to-system (service account) authentication** — determining the appropriate flow (Client Credentials vs Managed Identity) for non-human workloads |
| 5 | **Fallback: Entra vs FMAA** | Design a fallback strategy so that if Entra ID is unavailable, authentication can fall back to **FMAA** (ForgeRock Mobile Authentication App / OneMFA) without service disruption |

# Current Authentication Flows

Reference:

[Authentication flow - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Authentication+flow)

## Login

The `/v2/sso/login` endpoint in the BFF handles **both** authentication methods via a single API. The routing logic is determined by the presence of the `code` field in the request body:

```bash
POST /api/auth/v2/sso/login
Content-Type: application/json

// Username / Password (OUD/LDAP)
{ "username": "1196411", "password": "*********" }

// SSO / OIDC
{ "code": "DsFdQ0hLlWzS6ijvQYTGXAzDimo", "clientId": "51358ratan",
  "iss": "https://mfaig.global.standardchartered.com:443/openam/oauth2/realms/root/realms/sso" }
```

### Diagram

### Key Code & Properties

```text
Non-prod:

POST 
https://{ENV}.pi.dev.net:8453/api/auth/v2/sso/login
{"username":"1633330","password":"******"}

prod:
--- 1. Sign In With SSO ---
GET 
https://mfaig.global.standardchartered.com/openam/oauth2/realms/root/realms/sso/authorize?client_id=51358ratan&redirect_uri=https://fmo-mfe.gdc.standardchartered.com:8453/mfa/callback&response_type=code

GET
https://mfaig.global.standardchartered.com/openam/UI/Login?realm=/sso&authIndexType=service&authIndexValue=mfatree&goto=https://mfaig.global.standardchartered.com:443/openam/oauth2/realms/root/realms/sso/authorize?client_id%3D51358ratan%26redirect_uri%3Dhttps://fmo-mfe.gdc.standardchartered.com:8453/mfa/callback%26response_type%3Dcode%26acr%3Dmfa%26acr_sig%3Dl7r-eescSG_2ZwiweyJ4hKlyKKj4n6evmsSfPJqZVZ4

GET
https://mfaig.global.standardchartered.com/openam/XUI/?realm=/sso&authIndexType=service&authIndexValue=mfatree&goto=https://mfaig.global.standardchartered.com:443/openam/oauth2/realms/root/realms/sso/authorize?client_id%3D51358ratan%26redirect_uri%3Dhttps://fmo-mfe.gdc.standardchartered.com:8453/mfa/callback%26response_type%3Dcode%26acr%3Dmfa%26acr_sig%3Dl7r-eescSG_2ZwiweyJ4hKlyKKj4n6evmsSfPJqZVZ4

GET
https://mfaig.global.standardchartered.com/openam/json/realms/root/realms/sso/serverinfo/*

POST
https://mfaig.global.standardchartered.com/openam/json/realms/root/realms/sso/authenticate?authIndexType=service&authIndexValue=mfatree&goto=https://mfaig.global.standardchartered.com:443/openam/oauth2/realms/root/realms/sso/authorize?client_id%3D51358ratan%26redirect_uri%3Dhttps://fmo-mfe.gdc.standardchartered.com:8453/mfa/callback%26response_type%3Dcode%26acr%3Dmfa%26acr_sig%3Dl7r-eescSG_2ZwiweyJ4hKlyKKj4n6evmsSfPJqZVZ4

--- 2. Login, Enter password, Submit ---
GET
https://mfaig.global.standardchartered.com/openam/oauth2/realms/root/realms/sso/authorize?client_id=51358ratan&redirect_uri=https://fmo-mfe.gdc.standardchartered.com:8453/mfa/callback&response_type=code&acr=mfa&acr_sig=l7r-eescSG_2ZwiweyJ4hKlyKKj4n6evmsSfPJqZVZ4

GET(enter to RATAN)
https://fmo-mfe.gdc.standardchartered.com:8453/mfa/callback?code=GAKDRO7FdTgPpD_d5KZgtnRG8Ek&iss=https%3A%2F%2Fmfaig.global.standardchartered.com%3A443%2Fopenam%2Foauth2%2Frealms%2Froot%2Frealms%2Fsso&client_id=51358ratan

GET
https://fmo-mfe.gdc.standardchartered.com:8453/api/auth/v1/fmo/admin/importmap/active

POST
https://fmo-mfe.gdc.standardchartered.com:8453/api/auth/v2/sso/login
Request: {"code":"GAKDRO7FdTgPpD_d5KZgtnRG8Ek","iss":"https://mfaig.global.standardchartered.com:443/openam/oauth2/realms/root/realms/sso","client_id":"51358ratan"}
Response:
	Header:
        single-ui-authorization: Bearer ${masked_token}
	Body:
	    {
    "entities": [
        {
            "id": 11491550,
            "name": "X_RATANONE",
            "applicationName": "RATAN",
            "roleId": 11491616,
            "roleName": "NON_FMO_RO",
            "subjects": [
                ...
            ]
        }
    ],
    "result": true,
    "expiration": null,
    "userInfo": "{\"max_age\":1776850766,\"sub\":\"1633330\",\"auth_time\":1776847166,\"iss\":\"single-ui-bff\",\"id\":\"B863130C9B6CA439279C666488D4B57D\",\"exp\":1776848066,\"iat\":1776847166,\"jti\":\"single-ui-bff-id\",\"oud\":\"{\\\"lastName\\\":\\\"Huang\\\",\\\"firstName\\\":\\\"Xinmiao\\\",\\\"country\\\":\\\"China\\\",\\\"fullName\\\":\\\"Huang, Xinmiao\\\",\\\"emailId\\\":\\\"CarolineXinmiao.Huang@sc.com\\\",\\\"locale\\\":null,\\\"userId\\\":\\\"1633330\\\"}\"}",
    "errorMessage": null,
    "oud": "{\"lastName\":\"Huang\",\"firstName\":\"Xinmiao\",\"country\":\"China\",\"fullName\":\"Huang, Xinmiao\",\"emailId\":\"CarolineXinmiao.Huang@sc.com\",\"locale\":null,\"userId\":\"1633330\"}",
    "entitlementsToken": "${token}",
    "drawers": [
        ...
    ]
}


```

```text
nginxadm@uklvadapp1340[DEV][ratan.d] $ pwd
/home/nginxadm/nginx/config-ratan/ratan.d

# mfe base backend: Auth Service
location /api/auth/ {
    rewrite ^/api/auth/(.*)$ /$1 break;
    proxy_redirect    off;
    proxy_set_header  Host $host;
    proxy_set_header  X-Real-IP $remote_addr;
    proxy_set_header  X-Forwarded-Proto http;
    proxy_set_header  X-Forwarded-For $remote_addr;
    proxy_set_header  X-Forwarded-Host $remote_addr;
    proxy_pass http://ratan_backend_api_gateway;
    # proxy_pass http://single_ui_bff;
}


```

```text
 @PostMapping(value = "v2/sso/login")
 public ResponseEntity<ResponseOfAuthenticate> authenticate(@RequestBody RequestOfAuthenticate request,
        HttpServletRequest httpServletRequest, HttpServletResponse response) throws JsonProcessingException {
	...
 }


```

## Authorization

Refer to

[Authentication flow - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Authentication+flow#Authenticationflow-Functionentitlementcheckflow)

APIs

```bash
GET
https://uklvauems01a.uk.standardchartered.com:16443/ems2/rest/entitlements/entity/name/RATAN_DATA_ENTITLEMENT/user/1481696

Response Sample:
{
    "entitlements": [
        {
            "id": 11514754,
            "subject": {
                "id": 11164752,
                "name": "RATAN_DATA_ENTITLEMENT",
                "longName": "/RATAN_DATA_ENTITLEMENT",
                "entity": {
                    "id": 11164654,
                    "name": "RATAN_DATA_ENTITLEMENT",
                    "systemName": "RATAN",
                    "locked": true
                }
            },
            "role": {
                "id": 11515751,
                "name": "Global",
                "entity": {
                    "id": 11164654,
                    "name": "RATAN_DATA_ENTITLEMENT",
                    "systemName": "RATAN",
                    "locked": true
                },
                "roleDescription": "Global",
                "isPrivilege": "No"
            },
            "action": {
                "id": 11164807,
                "name": "VIEW_ENTITLEMENT",
                "entity": {
                    "id": 11164654,
                    "name": "RATAN_DATA_ENTITLEMENT",
                    "systemName": "RATAN",
                    "locked": true
                }
            }
        }
    ],
    "count": 1
}
```

```bash
## Step A - get FMAA token
GET
http://10.198.199.160:13167/v3/token

## Step B - EMS3 Data Entitlement Query
GET
https://fmcesuat.gdc.standardchartered.com/fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/1481696
Bearer Token ...

Response Sample:
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
                "RATAN_ENTITLEMENT_GLOBAL"
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
                        "400625349",
                        "400044944",
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
            ]
        }
    }
]



```

# Proposal

## Diagram A

## Diagram B(TBD)

## Key logic change

EMS3 Data Sample: [API Gateway & Auth Server Combination - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3705988601#APIGateway&AuthServerCombination-Authorization)

| Option | EMS3 Field | Data Snippet | logic | Comments |
| --- | --- | --- | --- | --- |
| Option-1 | entitlements.entitlement_name | [ { "user_data": { ... }, "entitlements": { "entitlement_name": [ "RATAN_ENTITLEMENT_COMMON", "RATAN_ENTITLEMENT_GLOBAL" ], "data_policies": { ... }, "data_profiles": { ... }, "data_entitlements": [ ... ] } } ] | JWT generate: Enrich entitlements.entitlement_name to JWT; FE logic: entitlements.entitlement_name contains "RATAN_ENTITLEMENT_ID, JWT validation: if entitlements.entitlement_name contains "RATAN_ENTITLEMENT_ID"; ID gateway release request; if entitlements.entitlement_name contains "RATAN_ENTITLEMENT_GLOBAL"; GDC gateway release request; | Append limited string to JWT |
| Option-1 | entitlements.data_entitlements.values | [ { "user_data": { ... }, "entitlements": { ... "data_entitlements": [ { "key": "Entity.Booking_Entity_SCI_FMID", "values": [ "10040387", "400568282", "10038345", "400516442", "400516443", "400667486", "10020899", "FMIDBRAMX01", "400683682", "400327728", "400107029", "300010872", "401053411", "300036368", "400910415", "15", "400075752", "400609343", "400058959", "400677737", "10041902", "300010633", "400011581", "10041903", "2", "123", "3", "400130178", "4", "400095464", "5", "400452428", "10038468", "6", "10054931", "7", "8", "9", "400131263", "401081696", "FINNKOREA01", "400040353", "300010782", "400170359", "10041530", "300011470", "MUXBZ01", "10036981", "401037180", "300084297", "123M", "10075222", "400013111", "400960089", "1234", "400041070", "400001378", "400045551", "10062461", "300011345", "400032489", "400451508", "400033177", "400931959", "10037164", "10032025", "10063428", "400045549", "300075472", "400991880", "400617263", "235003861", "400192940", "300089409", "400059978", "10078716", "400077046", "400077044", "400057714", "400798477", "400209000", "401036553", "FM ID TST 1", "400088463", "400085753", "400220273", "400218197", "400007847", "300063361", "300011525", "400077978", "10036647", "400054708", "10036642", "10036645", "10038667", "400193370", "400090093", "10022098", "400994973", "400130180", "400013557", "10037477", "10036382", "400227738", "400054741", "400172181", "10036775", "400054737", "10036655", "400625349", "400044944", "400823493", "400229749", "400093619", "10036430", "400018439", "400906330", "400017223", "300010730", "400147183", "10036428", "400022800", "400185419", "400899993", "195000930", "400823482", "400823485" ] } ] } } ] | JWT generate: Enrich entitlements.data_entitlements.values to JWT; JWT validation: if entitlements.entitlement_name.values only contains "8"; ID gateway release request; else GDC gateway release request; | Token may be too large |