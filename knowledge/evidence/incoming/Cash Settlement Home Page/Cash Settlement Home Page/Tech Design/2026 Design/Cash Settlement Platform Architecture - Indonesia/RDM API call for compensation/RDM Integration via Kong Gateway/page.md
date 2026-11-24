| Owner | @Xinmiao Huang |
| --- | --- |
| Update Time | 2026-08-04 |
| Status | SIT Done |
| Story | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13292988](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13292988) |

# Reference

[Consumer Onboarding - Consumer's Guide - IAG Dev Factory/Catalyst - Application Platforms - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3141654628#ConsumerOnboardingConsumer%27sGuideIAGGreenfield/Catalyst-ConsumerIdentification:ADServiceAccount)

IAG role & responsibilities: [IAG Change Release Process via ADO - Application Platforms - Confluence](https://confluence.global.standardchartered.com/display/APPPLAT/IAG+Change+Release+Process+via+ADO)

[API V2 Functionality - IAG Greenfield/Catalyst - Application Platforms - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3147694564#APIV2FunctionalityIAGGreenfield/Catalyst-HowtoConfigure.2)

# Kong Environments

| Env | URL |
| --- | --- |
| SIT | [https://gateway-stg.51242.app.standardchartered.com](https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/rdmdata?api=v1/countries) |
| UAT | [https://gateway-uat-stg.51242.app.standardchartered.com](https://gateway-uat-stg.51242.app.standardchartered.com) |
| PROD | [https://gateway.51242.app.standardchartered.com](https://gateway.51242.app.standardchartered.com/rdm_api/service/rdmdata?api=v1/countries) |

# Integration Endpoints

| Currency Holiday | /rdm_api/service/rdmdata?api=v2/holidayCalendarCurrencyHldyWkend?dateFrom={startDate}&dateTo={endDate} |
| --- | --- |
| Special Holiday | /rdm_api/service/rdmdata?api=v2/holidayCalendarSpecial&dateFrom={startDate}&dateTo={endDate} |
| Country Code | /rdm_api/service/rdmdata?api=v1/countries |

# Kong Onboarding As a Consumer

## Prerequisite

### AD account

As Ratan already has an consumer integrated with Kong gateway for Portfolio query , we can reuse it:  **EDMILDAP_RATAN_EDMI_PROD_Ratanone-PCT2**

### IAG repo&pipeline access

How to apply access, refer to this page:

<u>[IAG - Write access to CIO application teams repository in ADO  - Terms and Conditions - Application…](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2973129831)</u>

If no response, join this channel:

<u>[General | API-4-Everyone](https://teams.microsoft.com/l/team/19%3AR8pmCuOIiRzg9GLJWXqcf5_ZB_83jJ_mSpcu2r3FeK81%40thread.tacv2/conversations?groupId=f487a633-9249-45d0-bade-a00b881b72cc&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e)</u>

Which repo access do you need:

<u>[51242-iag-catalyst-kong-helm - Repos](https://dev.azure.com/sc-ado/TTOQPR/_git/51242-iag-catalyst-kong-helm)</u>

<u>[51242-iag-catalyst-idp-service-records - Repos](https://dev.azure.com/sc-ado/TTOQPR/_git/51242-iag-catalyst-idp-service-records)</u>

### Service name & Scope

Ask producer to provide service name and scope, normally can be found in the repos above.

### Producer grant access

Ask producer to grant access to specific **consumer id(**EDMILDAP/RATAN_EDMI_PROD**)**

## Actions to make it happen

### Non-Production

**PR**: [Pull request 3141169: #15362330 Ratan integrate with RDM Query API - Repos](https://dev.azure.com/sc-ado/TTOQPR/_git/51242-iag-catalyst-idp-service-records/pullrequest/3141169)

**Pipeline**: [Pipelines - Run 20260804.1](https://dev.azure.com/sc-ado/TTOQPR/_build/results?buildId=14003210&view=results)

### Production(TBD)

# Integration Flow

# Request Sample

## Step A: Query Client Info

### Request

```bash
GET /api/identity/oauth2/dcr/v1.0/register?client_name=EDMILDAP_RATAN_EDMI_PROD_Ratanone-PCT2 HTTP/1.1
Host: gateway-stg.51242.app.standardchartered.com
Authorization Type: Basic Auth
Username: EDMILDAP/RATAN_EDMI_PROD
password: #Get from OneVault
```

### Response

```text
{
    "client_id": "dummy client id", #Username for step B - getting access token
    "client_s[remove me]ecret": "dummy client s[]ecret", #password for step B - getting access token
    "client_s[remove me]ecret_expires_at": 0,
    "redirect_uris": [
        null
    ],
    "grant_types": [
        "client_credentials" #grant_type for step B - getting access token
    ],
    "client_name": "EDMILDAP_RATAN_EDMI_PROD_Ratanone-PCT2"
}
```

## Step B: Get Access Token

### Request

```bash
POST /oauth2/token?grant_type=client_credentials&scope=RDMApiService_GET HTTP/1.1
Host: gateway-stg.51242.app.standardchartered.com
Authorization Type: Basic Auth
Username: #client_id returned in Step A
password: #client_s[remove me]ecret returned in Step A
```

### Response

```text
{
    "access_token": "XXX", #token for step C - fire API call
    "scope": "RDMApiService_GET",
    "token_type": "Bearer",
    "expires_in": 900
}
```

## Step C: Fire API Call

### Request

```bash
GET /rdm_api/service/rdmdata?api=v2/holidayCalendarCurrencyHldyWkend&dateFrom=20220301&dateTo=20220315 HTTP/1.1
Host: gateway-stg.51242.app.standardchartered.com
Authorization Type: Bearer Token
Token: #access_token returned in Step B
```

### Response

```text
{
    "response": {
        "code": "200",
        "status": "Success",
        "header": {
            "serviceName": "holidayCalendarCurrencyHldyWkend",
            "serviceVersion": "v2",
            "requestParams": "dateTo=20220315&api=v2/holidayCalendarCurrencyHldyWkend&page=1&dateFrom=20220301",
            "generatedTimestamp": "2026-08-05 16:03:54 HKT",
            "trackingId": "20260805T1603547301",
            "totalRecords": "541550",
            "pageNo": "1",
            "pageSize": "2000",
            "columnAttributes": [
                {
                    "columnName": "centerId",
                    "dataType": "INTEGER",
                    "maxSize": "4",
                    "mandatory": "Y"
                },
                {
                    "columnName": "isoCurrencyCode",
                    "dataType": "VARCHAR",
                    "maxSize": "3",
                    "mandatory": "N"
                },
                {
                    "columnName": "isoCountryCode",
                    "dataType": "VARCHAR",
                    "maxSize": "2",
                    "mandatory": "N"
                },
                {
                    "columnName": "relatedFinancialCenter",
                    "dataType": "VARCHAR",
                    "maxSize": "200",
                    "mandatory": "N"
                },
                {
                    "columnName": "eventYear",
                    "dataType": "INTEGER",
                    "maxSize": "4",
                    "mandatory": "N"
                },
                {
                    "columnName": "eventDate",
                    "dataType": "DATE",
                    "maxSize": "0",
                    "mandatory": "Y"
                },
                {
                    "columnName": "eventDayOfWeek",
                    "dataType": "VARCHAR",
                    "maxSize": "3",
                    "mandatory": "N"
                },
                {
                    "columnName": "eventName",
                    "dataType": "VARCHAR",
                    "maxSize": "250",
                    "mandatory": "Y"
                },
                {
                    "columnName": "dayType",
                    "dataType": "VARCHAR",
                    "maxSize": "3",
                    "mandatory": "N"
                },
                {
                    "columnName": "fileType",
                    "dataType": "VARCHAR",
                    "maxSize": "1",
                    "mandatory": "Y"
                },
                {
                    "columnName": "entityState",
                    "dataType": "VARCHAR",
                    "maxSize": "25",
                    "mandatory": "Y"
                },
                {
                    "columnName": "createdTime",
                    "dataType": "TIMESTAMP",
                    "maxSize": "0",
                    "mandatory": "N"
                },
                {
                    "columnName": "modifiedTime",
                    "dataType": "TIMESTAMP",
                    "maxSize": "0",
                    "mandatory": "N"
                }
            ]
        },
        "dqGrading": {
            "dataQuality": "Amber",
            "dqRemarks": ""
        },
        "data": [
            {
                "centerId": 1,
                "isoCurrencyCode": "GBP",
                "isoCountryCode": "GB",
                "relatedFinancialCenter": "London",
                "eventYear": 2031,
                "eventDate": "18/05/2031",
                "eventDayOfWeek": "Sun",
                "eventName": "Weekend",
                "dayType": "WKD",
                "fileType": "C",
                "entityState": "ACTIVE",
                "createdTime": "10/03/2022 14:02",
                "modifiedTime": ""
            },
            {
                "centerId": 1,
                "isoCurrencyCode": "GBP",
                "isoCountryCode": "GB",
                "relatedFinancialCenter": "London",
                "eventYear": 2037,
                "eventDate": "04/05/2037",
                "eventDayOfWeek": "Mon",
                "eventName": "Early May Bank Holiday",
                "dayType": "HDY",
                "fileType": "C",
                "entityState": "ACTIVE",
                "createdTime": "10/03/2022 14:02",
                "modifiedTime": ""
            },
			...
        ]
    }
}
```