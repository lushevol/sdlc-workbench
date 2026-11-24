#

# Login

## Login by username

## Single-UI login

```ruby
POST https://fmo-mfe.uk.dev.net:8453/api/auth/v2/sso/login
{
    "username": "1481696",
    "passwor"...
}

Single-UI-Authorization Bearer eyJ...
```

## Fetch function entitlements from EMS2

The bellow API is used to fetch func entitlements in single-ui-bff:

```ruby
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

And the entitlements is returned to frontend in the "entitlementsToke":

![image-2025-12-15_17-38-49.png](attachments/image-2025-12-15_17-38-49.png)

inside "entitlements":

![image-2025-12-15_17-39-25.png](attachments/image-2025-12-15_17-39-25.png)

# Function entitlement check flow

When calling API, the API gateway will check if the user has corresponding function entitlement. A simplified flow is shown as bellow:

## Fetch EMS2 entitlements from auth service

API gateway will call auth-service to verify token and fetch function entitlement every time a request is received:

```ruby
POST https://uklvadapp1345.uk.dev.net:3833/v3/authenticate
Single-UI-Authorization Bearer eyJ...

{
    "entitlement": "{\"role\":\"FMO_OPS_BOM\",\"actions\":[\"RATAN_TRADE_BLOTTER:ACCESS_FMO_POST_TRADE_PORTAL\"...],\"dataEntitlementRoles\":\"Global\"}",
    "userInfo": {
        "userId": "1481696",
        "fullName": "1481696",
        "country": "Global",
        "entitlementCountry": "China"
    }
}
```

The bellow EMS2 API is used:

```ruby
GET https://uklvauems01a.uk.standardchartered.com:16443/ems2/rest/entitlements/entity/name/RATAN_DATA_ENTITLEMENT/user/1481696

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