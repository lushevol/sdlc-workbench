This document outlines the integration of CES (strategic data entitlement solution) into our system to manage data entitlements. The integration will leverage CES APIs for entitlement checks, ensure authentication via FMAA tokens, and include mechanisms for service resilience, selective enablement, and caching.

Note: the CES management, including user onboarding, entitlement configuration should be guided by CES team, thus not considered in this page.

# CES introduction

Reference:

- <u>[FM User and Data Entitlement Solution - FM Operations Technology - Confluence](https://confluence.global.standardchartered.com/display/FXRCCPE/FM+User+and+Data+Entitlement+Solution)</u>
- <u>[FM-CES - Downstream Integration Changes - FM Operations Technology - Confluence](https://confluence.global.standardchartered.com/display/FXRCCPE/FM-CES+-+Downstream+Integration+Changes)</u>

CES (formerly known as EMS3) is the strategic entitlement solution in FM. It aims to provide a centric approach for FM system to manage data entitlement and provides a consolidated view on data accessing rules.

![](https://confluence.global.standardchartered.com/download/attachments/2817947133/image2023-7-20_22-31-46.png?version=6&modificationDate=1738317965000&api=v2)

## Core concepts

- **Data Policy**: A set of rules are linked user’s HR profile. This will be automatically inherited by a new user. The data policy is managed by Policy Owner / COO.
- **Data Profile**: A set of rules linked to user’s Role profile. Data profile is assigned to a user based on his role by the EMS3 operator.
- **Role**: Role is a representation of the specific activities that a user is allowed to perform within the Business functions that he/she has access to within an application.

Data Profile (Role based) rules will take precedence as a general rule over Data Policy (HR Profile) rules.  Example:

Data policy constraints Korea trading by non Korea users, and to allow users from GB to trade Korea trades in non Korea trading hours a Data Profile override need to be setup.

A comparation between Data policy and Data profile:

| Type | Connected to | Maintained by | Note | Example |
| --- | --- | --- | --- | --- |
| Data policy | Location | Policy Owner / COO | | |
| Data profile | user role | | | |
| User role | | | | |

## CES Consumer API

CES provides restful API to get data entitlements of a user, what we need to provide in request is only the PSID of user:

```ruby
GET /fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/1538147 HTTP/1.1
Authorizatio...
Host: fmcesuat.gdc.standardchartered.com
```

The response will contain an evaluated conditions for given user:

```js
"entitlements": {
  "data_entitlements_logical_indicator": "OR",
  "data_entitlements": [
    {
      "key": "Entity.Counterparty_Country_ISO_Code",
      "values": ["JP"]
    }, {
      "key": "Entity.Booking_Entity_SCI_FMID",
      "values": ["10036382","300010633"]
    }],
}
```

# Assumptions

| Assumption | Impacts |
| --- | --- |
| No change on EMS2 | No code change of function entitlements |
| Only supported fields will be configured in CES. According to known cases, all possible fields are: - Entity.Booking_Entity_SCI_FMID - Entity.Counterparty_SCI_DOMICILE_COUNTRY | For other fields, we must confirm whether it's supported before configure it |
| Data latency is tolerated, eg. 1h | We can configure longer cache expiration time |
| SSDR sql will only support to query from cashflow_data table. Sample sql: Input: Select Data_Flow.Data_Source_System from cash_settlement_query_cn.cashflow_data LIMIT 1 OFFSET 0 Converted: SELECT data_flow__data_source_system FROM cash_settlement_query_cn.cashflow_data LIMIT 1 OFFSET 0 | We'll only support jsonb query using |

# System Architecture

# Integration Design

## Authentication

ＦＭＡＡ is already integrated in RATAN:

- The ＦMAA Ｔoken is cached in redis in auth service
- Ｔoken will be renewed if it's not available in redis
- This is already implemented in auth service

## Data entitlement condition interpretation

There're basically two scenarios that will be returned from CES. First case is that accessible entities are returned:

```js
{
  "data_entitlements": [{
      "key": "Entity.Booking_Entity_SCI_FMID",
      "values": ["10036382","300010633"]
    }]
}
```

And the second case is that multiple conditions returned:

```js
{
  "data_entitlements_logical_indicator": "OR",
  "data_entitlements": [
    {
      "key": "Entity.Counterparty_Country_ISO_Code",
      "values": ["JP"]
    }, {
      "key": "Entity.Booking_Entity_SCI_FMID",
      "values": ["10036382","300010633"]
    }]
}
```

The data entitlement conditions will be translated into query conditions based on query implementation:

- for JPA specification based query (in cashflow blotter), we'll convert the condition into JPA conditions, which is already implemented in cashflow blotter query
- for SQL based query (in SSDR report), we'll convert the condition into SQL conditions directly.

| Notation | Interpret flow | Target field |
| --- | --- | --- |
| Specification | CES condition → Specification JSON → JPA specification → JSONB query | cashflow_data.cashflow |
| SQL | CES condition → JSONB query | cashflow_data.cashflow |
| Direct | CES condition → JSONB condition → evaluate | cashflow_data.cashflow |

### JPA specification based query

First, the conditions will be converted to a JPA specification condition definition(it's implemented by RATAN, not JPA standard):

```js
// for simple case
{"field":"Entity.Booking_Entity_SCI_FMID","values":["401036553","400994973"]}

// for complex case with multiple conditions
{"or": [
  {"field":"Entity.Booking_Entity_SCI_FMID","values":["401036553","400994973"]},
  {"field":"Entity.Counterparty_Country_ISO_Code","values":["JP"]}
]}
```

and the final query will be like:

```js
select *
from cashflow_data c 
where
  jsonb_extract_path_text(c.cashflow, 'Cashflow', 'Cashflow_State')=? 
  and ( -- data entitlement conditions
      jsonb_extract_path_text(c.cashflow, 'Entity', 'Booking_Entity_SCI_FMID') in (?, ?) 
      or jsonb_extract_path_text(c.cashflow, 'Entity', 'Counterparty_SCI_DOMICILE_COUNTRY')=?
  ) 
```

### SQL based query

Example of SSDR query:

```sql
SELECT cashflow__pay_receive_indicator, cashflow__cashflow_state, portfolio__booking_entity_trade_portfolio_name, entity__counterparty_sci_fmid, ssi__account__beneficiary_account_name, trade_id, cashflow__payment_date, instrument_common__isda_taxonomy, cashflow__payment_currency, cashflow__payment_amount, cashflow__cashflow_id 
FROM cash_settlement_query_cn.cashflow_data 
WHERE cashflow__payment_date = '2026-01-02' 
LIMIT 96391 OFFSET 0, current loop=20, total loops=20
```

The SQL based query is currently used in SSDR report, which accepts the SQL conditions from RATAN entitlement api:

```js
// Before integration with CES, the condition will be: Entity.Booking_Entity_SCI_FMID IN ('400007847')
// After: jsonb_extract_path_text(cashflow, 'Entity', 'Booking_Entity_SCI_FMID') IN ('400007847')
String condition = ... 

if (plainSelect.getWhere() != null) {
    plainSelect.setWhere(CCJSqlParserUtil.parseCondExpression(
      plainSelect.getWhere().toString() + " AND " + condition));
} else {
    plainSelect.setWhere(CCJSqlParserUtil.parseCondExpression(condition));
}
```

So we need to convert the data entitlement conditions to JSONB query conditions and inject it into the original SQL.

### Single cashflow filtering(for Notification)

For websocket message broadcasting, we need to check if a single cashflow matches the conditions.

## Data filtering

### Transparent filtering for GraphQL

For GraphQL query, the data entitlement condition will be added automatically and transparently to the query.

### Conditional filtering for LoopController APIs

### WebSocket cashflow change event broadcasting

We have existing new cashflow notification implementation based on web socket. However, existing implementation subscribes new cashflow with /cashflow/notification, which could not be controlled according to user entitlements. So we need to change a little bit on current solution:

1. Frontend should now subscribe to user specific topic, aka "/user/{psid}/cashflow/notification"
2. Server will send to user specific topic and check data entitlement in outbound interceptor

Note that Spring uses a special convention for user destinations. When you call:

```java
messagingTemplate.convertAndSendToUser(username, "/cashflow/notification", event);
```

Spring internally rewrites the destination to something like:

```java
/cashflow/notification-user{sessionId}
```

This is a temporary, internal destination that maps to the user's session. The -userlkztkft0 part is a unique suffix for the user's session.

Clients should **not** subscribe to the rewritten destination. Instead, they should subscribe to:

```java
/user/{username}/cashflow/notification
```

Spring will route messages from the internal destination to the correct user subscription.

## Caching

We'll use same cache strategy that is is used for EMS2 currently:

1. CES result will be stored in redis, the expiry time is configurated to 1 hour by default
2. No cache will be added in query service.

```js
scb:
  ems2:
    expiryTime: 3600 #seconds
    cachingEnabled: true
```

## Fallback mechanism

Our fallback strategy is that, if any error happens, the user query fails. We'll prompt that it's CES error and should notice CES to fix it. The cases that might happen are listed bellow:

- User not onboarded in CES
- CES internal error, returns wrong data
- CES unavailable

- [ ] Work with PSS for CES monitoring

If it takes too long to fix it, then we can temporarily disable CES in RATAN, see next section.

## CES downgrade & Selective enablement/disablement

A dynamic configuration must be implemented to control data entitlement control in RATAN to prevent unavailability of RATAN in following emergency cases:

- CES service down for long time
- Wrong data is responding by CES
- Wrong configuration is applied (unexpected global policies, etc)

Basically, we should be able to:

- Toggle on/off data entitlement control (globally) on demand
- Toggle on/off data entitlement control for single user

This is actually downgrade of CES and should only be used until CES is recovered. To avoid additional complexity, we'll not involve technical such as ** **circuit breaker mechanism.

By default, CES will be enabled and data entitlement will be enabled, thus the following behaviors are expected:

- If user is not onboarded in CES, he/she will not be able to query any cashflows

### Option 1: Static config + UI (Maker/Checker)

We should be able to selectively enable or disable CES for specific user. A configuration table is designed in static data service:

![image-2025-12-10_15-14-30.png](attachments/image-2025-12-10_15-14-30.png)

Additional UI need to be implemented to modify the configuration.

### Option 2: Dynamic configuration in UI

Ref: <u>[https://confluence.global.standardchartered.com/display/DSP/%5BBAU%5D+Config+Server+Enhancement](https://confluence.global.standardchartered.com/display/DSP/%5BBAU%5D+Config+Server+Enhancement)</u>

We've designed a dynamic configuration feature (Not in prod yet) that could possibly be used for entitlement configuration:

[https://confluence.global.standardchartered.com/rest/gliffy/1.0/embeddedDiagrams/d659e905-d1e4-4acd-8a6b-3c2cd7616e5e.png?utm_medium=live&utm_source=confluence](https://confluence.global.standardchartered.com/rest/gliffy/1.0/embeddedDiagrams/d659e905-d1e4-4acd-8a6b-3c2cd7616e5e.png?utm_medium=live&utm_source=confluence)

![](https://confluence.global.standardchartered.com/rest/gliffy/1.0/embeddedDiagrams/d659e905-d1e4-4acd-8a6b-3c2cd7616e5e.png?utm_medium=live&utm_source=confluence)

Key takeaways:

- Fetch config from config server at application startup
- Listen to Kafka to apply new configuration change

### Option 3: Bypass data entitlement via URL

Bypass data entitlement control through some special url, such as  <u>[https://fmo-mfe-dev.uk.dev.net:8453](https://fmo-mfe-dev.uk.dev.net:8453)?disable-data-entitlement=true</u>

1. UI receives a special url param, and sends some toggle to backend
2. When the toggle is present in API, then enable/disable data entitlement control

| | A: Static config | B: Config server | C: Bypass URL |
| --- | --- | --- | --- |
| Can toggle on/off data entitlement control globally? | Yes | Yes | No SSDR/Notification will not be impacted |
| Can toggle on/off for single user? | Yes | Yes | Yes but limited (same reason as above) |
| Effort | +++ | +++++ | + |
| Security | / | / | Potential security risk, need additional design to mitigate it |
| Complexity | ++ | +++++ | + |

### Decision

- Exclude Option 3 because it cannot fulfill our requirement
- Trying to use B first, because it's more general/full functional solution

### Option 4: Configuration (Chosen)

Configure a two layer toggle in services:

- query-service: CES enable/disable toggle. If disabled, fallback to existing behavior(no data entitlement, or RATAN own impl)
- au..-service: Global CES toggle and per-user disabled list. If disabled, then will not fetch CES and returns with "disabled: true", consumer will then applying no data entitlement (privileged)

The configuration could be illustrated as bellow:

```yml
scb:
  ems3:
    enabled: true
    disabled-users:
      - 2022123
```

# Error handling

## CES API errors

| Error type | Error handling | End user result | Note |
| --- | --- | --- | --- |
| { "errorClass": "com.fmces.shared.exception.ResourceNotFoundException", "message": "User Not found-2022123", "status": 404, "timestamp": "2025-12-10T07:26:32.750335381" } | Throw error | Query failed | Wait for CES to fix it. For emergency, we can disable it in RATAN temporarily. |
| Missing data entitlement in the response | Throw error | Query failed |
| CES 500 internal error | Retry | |
| CES unavailable connect ECONNREFUSED 10.198.72.135:443 | Retry | |
| CES 4xx errors | Retry | | Expiration should be handled in auth service. We assume that it's always not expired. |
| Unrecognized fields | Do nothing | | The SQL condition will be translated into jsonb query, if the field does not exists, no error will be thrown. So we can't do anything here. |
| Empty values | Throw error | Query failed | |

# Change scope

## PR overview

| Service | Branch | ENV | PR |
| --- | --- | --- | --- |
| [51358-ratan-service-properties](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2314113) | feature/ems3-non-prod | dev,uat,stg | - [x] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2314113](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2314113) |
| [51358-ratan-service-properties](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2314113) | feature/ems3-fmrp2 | fmrp2 | - [x] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2314161](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2314161) |
| 51358-ratanone-auth-server | feature/ems3-integration | fmrp2 | - [x] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2313389](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2313389) - [x] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2316939](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2316939) - [x] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2317106](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2317106) - [ ] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2346113](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-auth-server/pullrequest/2346113) |
| [51358-ratan-cash-settlement-query-service](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2346108) | feature/ems3-integration | fmrp2 | - [x] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2313355](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2313355) - [x] [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2346108](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2346108) |
| ~~51358-ratanone-static-data-service~~ | ~~feature/ems3-and-fxu-rebased~~ | N/A | - [x] ~~[https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/2011113](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/2011113)~~ (change cancelled because we moved CES integration from static-service to auth-service. The code is also emitted from UBER/FXU) |
| 51358-mfe-cashflow-blotter | feature/11795072-ces-notification | fmrp2 | [Pull request 2363464: notification for ces - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter/pullrequest/2363464) |

## Code changes

| Query name | Feature | Related class | Existing impl (before CES) | Change Scope | Fallback Behavior (CES disabled) | Query Type |
| --- | --- | --- | --- | --- | --- | --- |
| cashflowAuditTrailNew | Group service, Account service | | N/A | Out of scope | | |
| cashflowsNew | Deprecated(in blotter) SSI refresh | CashflowJsonbQueryServiceImpl#getEntitlementCondition | | | | Specification |
| cashflowUltraQueryCount | Cashflow blotter |
| cashflowUltraQuery |
| componentCashflow |
| cashflowDashboard |
| groupMessages | Cashflow blotter | | N/A | Out of scope | | |
| graphCashFlowDetails | Group service | | N/A | Out of scope | | |
| /v1/query/cashflows | Unconfirmed | CashflowQueryServiceImpl#queryCashFlowData | | | | Specification |
| /v2/data/provider/query/cashflows | SSDR | ReportQueryServiceImpl#checkRequestSql | | | | SQL |
| /v2/data/provider/query/jsonb/cashflows |
| websocket | Notification | DataEntitlementOutboundChannelInterceptor#preSend | Mock/Disabled | | | Direct |

## API change

### Get data entitlement by userId

```js
GET /v1/data-entitlement?userId=2006999' HTTP/1.1
Host: 10.198.199.160:9255

200 OK
{
  "enabled": true,
  "filters": [
    {
      "field": "Entity.Booking_Entity_SCI_FMID",
      "values": [
        "4",
        "400960089"
      ]
    }
  ],
  "condition": "ANY"
}

If fetch CES error:
{
  "status": 500,
  "errorCode": "SERVICE_INTERNAL_ERROR",
  "errorMessage": "Failed to get ems3 entitlements: 404 Not Found: \"{\"errorClass\":\"com.fmces.shared.exception.ResourceNotFoundException\",\"message\":\"User Not found-2006991\",\"status\":404,\"timestamp\":\"2026-01-05T07:57:41.867826445\"}\"",
  "metadata": null
}
```

### Clear data entitlement cache(for internal maintenance only)

This API is intended for internal usage only, mainly to clear cache during go live, to avoid waiting if CES has any update.

Note: if the api is invoked from api gateway, then must provide basic athuentication with user=ratanone-rundeck, which is hard coded in athu server.

```js
POST http://10.198.199.160:8868/v1/auth/reset-data-entitlement?userId=*
Basic ratanone-rundeck...

if userId=*, then clear all data entitlement caches
otherwise only clear single user by userId

returns deleted users
```

# Performance

## Concurrency estimation

| | Value | Remark |
| --- | --- | --- |
| Maximum users | 636 | Existing EMS2 prod users count as of 3th, Feb |
| Number of concurrent user | 60 * 1.3≈80 req/min | |
| User locations | Global | |

### Maximum QPS estimation

```js
# query total qps of graphql + ssdr requests
sum(rate(http_server_requests_seconds_count{uri=~"/graphql|/v2/data/provider/query/cashflows|/v2/data/provider/query/jsonb/cashflows", instance=~".*query-service.*"}[5m]))
```

## ![image-2026-3-3_14-11-4.png](attachments/image-2026-3-3_14-11-4.png)

## Total requests per minute

```js
# query total requests per minute
sum(increase(http_server_requests_seconds_count{uri=~"/graphql|/v2/data/provider/query/cashflows|/v2/data/provider/query/jsonb/cashflows", instance=~".*query-service.*", error="none"}[1m]))
```

## ![image-2026-3-3_14-8-52.png](attachments/image-2026-3-3_14-8-52.png)

```js
SELECT
  DATE_TRUNC('minute', timestamp) AS minute,
  COUNT(*) AS requests_per_minute
FROM audit a 
WHERE request_url IN (
  '/graphql',
  '/v2/data/provider/query/cashflows',
  '/v2/data/provider/query/jsonb/cashflows'
)
AND timestamp >= '2025-02-16'
AND timestamp <= '2025-02-21'
GROUP BY minute
ORDER BY minute;
```

![image-2026-2-3_16-58-50.png](attachments/image-2026-2-3_16-58-50.png)

## ![image-2026-2-3_17-8-14.png](attachments/image-2026-2-3_17-8-14.png)

## Performance testing

### Environment

FMRP2 is used for PT. FMRP2 is based on prod dump on July~Aug 2025, and the total size of cashflow is around:

![image-2026-1-27_11-44-58.png](attachments/image-2026-1-27_11-44-58.png)

### Test users

| PID | Role | Remark |
| --- | --- | --- |
| 1129381 | CES disabled | Base line |
| 1481696 | GLOBAL | Able to view all entities (100+) |
| 2006999 | ONSHORE_ID | Can only see data of ID |
| 1549476 | GBS_IN | Can view most data except a few countries such as PK, TZ, etc. |

### Test steps

1. Login user in UI
2. Set query conditions and capture the query condition, token
3. Modify query conditions and create jmeter test plan
4. Execute jmeter test suit with different users (in local compute)

The test plan will contain basic assertions to ensure that http status is success and the total count of cashflows returned matches expected.

For example, the bellow command will be used to test a default search case of GBS_KL role:

```js
%GV%/apache-jmeter-5.5/bin/jmeter -n -t default-query.jmx -Jthreads=10 -Jrampup=10 -Jloops=100 -Jtotal=61 -l default-KL-1x.csv -e -o default-KL-1x
```

### Test cases

| Business scenario | Explanation | Result size | Round2 | Size | Test configuration |
| --- | --- | --- | --- | --- | --- |
| User default query | When user login and open cashflow blotter, we'll fetch recent cashflows within T+6 and in WAITING status: { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" }, { "field": "Cashflow.Payment_Date", "operator": "BET", "values": [ "2026-01-22", "2026-01-28" ] } | 800+ (without data entitlement filtering) | { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" }, { "field": "Cashflow.Payment_Date", "operator": "BET", "values": [ "2026-04-11", "2026-04-17" ] } | 55 | -Jthreads=10 -Jrampup=10 -Jloops=100 |
| User default query with medium result set | { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "SETTLED" }, { "field": "Cashflow.Payment_Date", "operator": "BET", "values": [ "2025-09-22", "2025-09-28" ] } | 17000+ | Same | 34775 | -Jthreads=10 -Jrampup=40 -Jloops=50 |
| User default query with large result set | { "field": "Cashflow.Cashflow_State", "operator": "NE", "values": "CANCELLED" }, { "field": "Cashflow.Payment_Date", "operator": "BET", "values": [ "2025-09-22", "2025-09-28" ] } | 160000+ | Same | 355008 | -Jthreads=5 -Jrampup=40 -Jloops=10 |
| Search by cashflow id | { "field": "Cashflow.Cashflow_Id", "operator": "IN", "values": [ "M00122296023" ] } | 1 | Same | 1 | -Jthreads=10 -Jrampup=20 -Jloops=50 |

### Testing Result

Raw results:<u></u>

The result could be visualized by bellow diagrams( created by <u></u>):

| Case | Result Overview |
| --- | --- |
| User default query | ![image-2026-1-28_11-30-16.png](attachments/image-2026-1-28_11-30-16.png) |
| User default query with medium result set | ![image-2026-1-28_11-32-42.png](attachments/image-2026-1-28_11-32-42.png) |
| User default query with large result set | ![image-2026-1-28_11-33-33.png](attachments/image-2026-1-28_11-33-33.png) |
| Search by cashflow id | ![image-2026-1-28_11-34-3.png](attachments/image-2026-1-28_11-34-3.png) |

| Case | Throughput comparation |
| --- | --- |
| User default query | ![image-2026-1-28_11-39-17.png](attachments/image-2026-1-28_11-39-17.png) |
| User default query with medium result set | ![image-2026-1-28_11-40-45.png](attachments/image-2026-1-28_11-40-45.png) |
| User default query with large result set | ![image-2026-1-28_11-41-43.png](attachments/image-2026-1-28_11-41-43.png) |
| Search by cashflow id | ![image-2026-1-28_11-44-30.png](attachments/image-2026-1-28_11-44-30.png) |

| Case | Timeline comparation |
| --- | --- |
| User default query | ![image-2026-1-28_11-40-7.png](attachments/image-2026-1-28_11-40-7.png) |
| User default query with medium result set | ![image-2026-1-28_11-41-3.png](attachments/image-2026-1-28_11-41-3.png) |
| User default query with large result set | ![image-2026-1-28_11-42-4.png](attachments/image-2026-1-28_11-42-4.png) |
| Search by cashflow id | ![image-2026-1-28_11-45-8.png](attachments/image-2026-1-28_11-45-8.png) |

# Performance testing - round2

in staging

![image-2026-4-17_12-17-51.png](attachments/image-2026-4-17_12-17-51.png)

![image-2026-4-17_12-21-59.png](attachments/image-2026-4-17_12-21-59.png)

| Scenario | | |
| --- | --- | --- |
| default | | |
| by fmid | | |
| by cashflow state | | |
| custom view (BABU) | | |

```bash
%GV%/apache-jmeter-5.5/bin/jmeter -n -t default-query.jmx -Jthreads=10 -Jrampup=10 -Jloops=100 -Jtotal=318 -l default-onshore-10x.csv -e -o default-onshore-10x

{"query":"\n  query SettlementCashflowDataUltraQuery($payload: RatanUltraQuery!) {\n    cashflowUltraQuery(payload: $payload) {\n      totalResult\n      pageIndex\n      itemsPerPage\n      lastPage\n      results {\n        BCS_Trade_Id,BCS_Parent_Trade_Id,FMO_Comments{FMO_Comment,FMO_Comment_Timestamp,FMO_Comment_Updater},Cashflow{Cashflow_Id,Cashflow_Business_Version,Cashflow_Version,Cashflow_State,Cashflow_Affirmation_Status,Cashflow_Event_Type,Cashflow_Minor_Version,Payment_Currency,Payment_Date,Payment_Type,Payment_Cutoff_Time,Pay_Receive_Indicator,Payment_Amount,Netting_Id,Splitting_Id,Netting_Cuttoff_Date,Payment_Receiver_Party_Reference,Payment_Payer_Party_Reference,Cashflow_Sub_State,Cashflow_Sub_State_Type,Cashflow_Sub_State_Updater,Status_Event_Type,Cashflow_Swift_Message_Standard,Event_Date,Cashflow_Event_Reason},Delivery_Method,Settlement_Method,Trade_Id,Trade_Version,Entity{Booking_Entity_SCI_FMID,Booking_Entity_SCI_FMCODE,Counterparty_SCI_FMID,Counterparty_SCI_FMCODE,Counterparty_SCI_BIC_Net_Flag},Instrument_Common{ISDA_Taxonomy,Source_System_Instrument_Sub_Type,Murex_Product_Strategy},Trade_Original_Source_System_Name,Data_Flow{Data_Source_System},Trade_State,Parent_Trade_Id,Portfolio{Booking_Entity_Trade_Portfolio_Name}\n      }\n    }\n  }\n  ","variables":{"payload":{"filters":{"and":[{"filters":[{"field":"Cashflow.Cashflow_State","operator":"EQ","values":"WAITING"},{"field":"Cashflow.Payment_Date","operator":"BET","values":["2026-04-16","2026-04-22"]}]}]},"itemsPerPage":1000,"orderArgs":[],"pageIndex":0,"pagingOption":"PAGE_INDEX"}},"operationName":"SettlementCashflowDataUltraQuery"}

%GV%/apache-jmeter-5.5/bin/jmeter -n -t default-query.jmx -Jthreads=10 -Jrampup=10 -Jloops=100 -Jtotal=358 -l by-fmid-onshore-10x.csv -e -o by-fmid-onshore-10x

{"query":"\n  query SettlementCashflowDataUltraQuery($payload: RatanUltraQuery!) {\n    cashflowUltraQuery(payload: $payload) {\n      totalResult\n      pageIndex\n      itemsPerPage\n      lastPage\n      results {\n        BCS_Trade_Id,BCS_Parent_Trade_Id,FMO_Comments{FMO_Comment,FMO_Comment_Timestamp,FMO_Comment_Updater},Cashflow{Cashflow_Id,Cashflow_Business_Version,Cashflow_Version,Cashflow_State,Cashflow_Affirmation_Status,Cashflow_Event_Type,Cashflow_Minor_Version,Payment_Currency,Payment_Date,Payment_Type,Payment_Cutoff_Time,Pay_Receive_Indicator,Payment_Amount,Netting_Id,Splitting_Id,Netting_Cuttoff_Date,Payment_Receiver_Party_Reference,Payment_Payer_Party_Reference,Cashflow_Sub_State,Cashflow_Sub_State_Type,Cashflow_Sub_State_Updater,Status_Event_Type,Cashflow_Swift_Message_Standard,Event_Date,Cashflow_Event_Reason},Delivery_Method,Settlement_Method,Trade_Id,Trade_Version,Entity{Booking_Entity_SCI_FMID,Booking_Entity_SCI_FMCODE,Counterparty_SCI_FMID,Counterparty_SCI_FMCODE,Counterparty_SCI_BIC_Net_Flag},Instrument_Common{ISDA_Taxonomy,Source_System_Instrument_Sub_Type,Murex_Product_Strategy},Trade_Original_Source_System_Name,Data_Flow{Data_Source_System},Trade_State,Parent_Trade_Id,Portfolio{Booking_Entity_Trade_Portfolio_Name}\n      }\n    }\n  }\n  ","variables":{"payload":{"filters":{"and":[{"filters":[{"field":"Entity.Booking_Entity_SCI_FMID","operator":"EQ","values":"400085753"},{"field":"Cashflow.Payment_Date","operator":"BET","values":["2026-03-19","2026-04-17"]}]}]},"itemsPerPage":1000,"orderArgs":[],"pageIndex":0,"pagingOption":"PAGE_INDEX"}},"operationName":"SettlementCashflowDataUltraQuery"}

%GV%/apache-jmeter-5.5/bin/jmeter -n -t default-query.jmx -Jthreads=10 -Jrampup=10 -Jloops=100 -Jtotal=602 -l by-state-onshore-10x.csv -e -o by-state-onshore-10x

{"query":"\n  query SettlementCashflowDataUltraQuery($payload: RatanUltraQuery!) {\n    cashflowUltraQuery(payload: $payload) {\n      totalResult\n      pageIndex\n      itemsPerPage\n      lastPage\n      results {\n        BCS_Trade_Id,BCS_Parent_Trade_Id,FMO_Comments{FMO_Comment,FMO_Comment_Timestamp,FMO_Comment_Updater},Cashflow{Cashflow_Id,Cashflow_Business_Version,Cashflow_Version,Cashflow_State,Cashflow_Affirmation_Status,Cashflow_Event_Type,Cashflow_Minor_Version,Payment_Currency,Payment_Date,Payment_Type,Payment_Cutoff_Time,Pay_Receive_Indicator,Payment_Amount,Netting_Id,Splitting_Id,Netting_Cuttoff_Date,Payment_Receiver_Party_Reference,Payment_Payer_Party_Reference,Cashflow_Sub_State,Cashflow_Sub_State_Type,Cashflow_Sub_State_Updater,Status_Event_Type,Cashflow_Swift_Message_Standard,Event_Date,Cashflow_Event_Reason},Delivery_Method,Settlement_Method,Trade_Id,Trade_Version,Entity{Booking_Entity_SCI_FMID,Booking_Entity_SCI_FMCODE,Counterparty_SCI_FMID,Counterparty_SCI_FMCODE,Counterparty_SCI_BIC_Net_Flag},Instrument_Common{ISDA_Taxonomy,Source_System_Instrument_Sub_Type,Murex_Product_Strategy},Trade_Original_Source_System_Name,Data_Flow{Data_Source_System},Trade_State,Parent_Trade_Id,Portfolio{Booking_Entity_Trade_Portfolio_Name}\n      }\n    }\n  }\n  ","variables":{"payload":{"filters":{"and":[{"filters":[{"field":"Cashflow.Payment_Date","operator":"BET","values":["2026-03-19","2026-04-18"]},{"field":"Cashflow.Cashflow_State","operator":"IN","values":["SETTLED","PROJECTED","QUEUED","WAITING","READY","HOLD","RELEASED","CASHFLOW_SUPPRESSED","SWIFT_SUPPRESSED","CANCELLED","ERROR","DEAD","NETTED","SPLIT","FAILED","NOSTROMATCH","UTILIZED","PARTIALLY_UTILIZED","PASTDUE"]},{"field":"Entity.Booking_Entity_SCI_FMID","operator":"EQ","values":"10075222"}]}]},"itemsPerPage":1000,"orderArgs":[],"pageIndex":0,"pagingOption":"PAGE_INDEX"}},"operationName":"SettlementCashflowDataUltraQuery"}

%GV%/apache-jmeter-5.5/bin/jmeter -n -t default-query.jmx -Jthreads=10 -Jrampup=10 -Jloops=100 -Jtotal=333 -l customview-onshore-10x.csv -e -o customview-onshore-10x
{"query":"\n  query SettlementCashflowDataUltraQuery($payload: RatanUltraQuery!) {\n    cashflowUltraQuery(payload: $payload) {\n      totalResult\n      pageIndex\n      itemsPerPage\n      lastPage\n      results {\n        BCS_Trade_Id,BCS_Parent_Trade_Id,FMO_Comments{FMO_Comment,FMO_Comment_Timestamp,FMO_Comment_Updater},Cashflow{Cashflow_Id,Cashflow_Business_Version,Cashflow_Version,Cashflow_State,Cashflow_Affirmation_Status,Cashflow_Event_Type,Cashflow_Minor_Version,Payment_Currency,Payment_Date,Payment_Type,Payment_Cutoff_Time,Pay_Receive_Indicator,Payment_Amount,Netting_Id,Splitting_Id,Netting_Cuttoff_Date,Payment_Receiver_Party_Reference,Payment_Payer_Party_Reference,Cashflow_Sub_State,Cashflow_Sub_State_Type,Cashflow_Sub_State_Updater,Status_Event_Type,Cashflow_Swift_Message_Standard,NSTP_Exception,Event_Date,Cashflow_Swift_Status,Is_Commodity,Is_Pending_Fixing,Clearing_Alpha,Cashflow_Event_Reason},Delivery_Method,Settlement_Method,Trade_Id,Trade_Version,Entity{Booking_Entity_SCI_FMID,Booking_Entity_SCI_FMCODE,Counterparty_SCI_FMID,Counterparty_SCI_FMCODE,Counterparty_SCI_BIC_Net_Flag,Counterparty_Murex_Display_Shortcode,Counterparty_SCI_BIC_Code,Counterparty_Client_Type,Counterparty_SCI_DOMICILE_COUNTRY},Instrument_Common{ISDA_Taxonomy,Source_System_Instrument_Sub_Type,Murex_Product_Strategy,Murex_Product_Typology},Trade_Original_Source_System_Name,Data_Flow{Data_Source_System},Trade_State,Settlement_Instruction{SSI_Unique_Id,Swift_Message_Type,Account{Beneficiary_BIC_code,Beneficiary_Account_Number,Beneficiary_Bank_BIC_code,Beneficiary_Correspondent_BIC_code,Intermediary_BIC_code}},Parent_Trade_Id,Portfolio{Booking_Entity_Trade_Portfolio_Name},Linked_Trade_ID\n      }\n    }\n  }\n  ","variables":{"payload":{"filters":{"and":[{"filters":[{"field":"Cashflow.Payment_Date","operator":"BET","values":["2026-03-19","2026-04-17"]},{"field":"Entity.Counterparty_SCI_FMCODE","operator":"IN","values":["SCB TH GRP*LDN"]}]}]},"itemsPerPage":1000,"orderArgs":[],"pageIndex":0,"pagingOption":"PAGE_INDEX"}},"operationName":"SettlementCashflowDataUltraQuery"}
```

![2.png](attachments/2.png)![1.png](attachments/1.png)![4.png](attachments/4.png)![3.png](attachments/3.png)

original report:

📎 [r4.zip](attachments/r4.zip)

# Known limitations

Some limitations are known based on current solution:

- Only supports query of **cashflow_data **table
- Since we use JSONB query, only fields exists in the **cashflow_data.cashflow **are available for filtering.
- CES will return all values (whitelist) of values, and will be appended in SQL when querying. PG has *max_allowed_packet *configuration of max allowed SQL length, which can be set up to 1G. In our case, total count of entitles is < 100, so there's no such concern.
- A latency is expected since we have some cache.

# Go live & Migration plan

## Go live plan

**GO Live Approach**: will be phased with 1 Global rule to ensure all existing access is preserved and 1 ID specific rule to restrict data access for ID users alone
**GO Live Dependency**: All applicable rules will need to UAT verified & signed off

| Checkpoint | Action | Owner | Remark |
| --- | --- | --- | --- |
| Dependencies | - [x] CES prod URL, onboard RATAN - [ ] Firewall? Connectivity between CES/RATAN - [ ] PROD EMS2 users, identify entitlement, country - [ ] CES onboard all existing EMS2 users - [ ] UAT signoff for 7th Feb (scope?) | | |
| | | | |
| | | | |
| | | | |
| | | | |
| 7th, Feb | CES Tech go live RATAN Tech go live: Deploy all services, blotter and then perform UVT, and then disable it - A: Normal pipeline (CES enabled) - Rollback pipeline(to PROD version) - B: CES disable pipeline Steps: 1. Deploy A 2. Wait until CES tech go live done 3. Recon 4. UVT – CES entitlement 5. If UVT success, then deploy B 6. UVT – just verify query works, can see all data | | |
| 28th, Feb | Business Go live Dependencies: - [ ] OLA agreement with CES - [ ] OLA with SSDR - [ ] create CES interface details in PSS KB - [ ] CES API PT/limitation/response time - [ ] Finalize rules in CES | | |
| | | | |
| | | | |
| | | | |

## EMS2 data migration

EMS2 existing users of RATAN will be populated via bellow apis:

[https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/entity/X_RATANONE](https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/entity/X_RATANONE)

[https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/entity/11491550/roles](https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/entity/11491550/roles)

[https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/user/role/11491607](https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/user/role/11491607)

Note:

We need to dump users under X_RATANONE (main RATAN users) and also RATAN_DATA_ENTITLEMENT(should already include all X_RATANONE users and contains more SSDR only users).

Because limitation of EMS2 design, multiple EMS2 entities are used in same application, RATAN_DATA_ENTITLEMENT is used for SSDR query in RATAN, and SSDR has hundreds of entities, but we don't need to care SSDR entities because:

- Not all SSDR users has RATAN access
- The SSDR users with RATAN access is onboarded with role of RATAN_DATA_ENTITLEMENT

## Recon

| Target | Reference data | |
| --- | --- | --- |
| User data entitlement roles | see "EMS2 data migration" section | |
| Country FMIDs in CES response | [FM-CES Entitlement Policy (Data Sovereignty) - Country Requirements - FM COO - Conduct and Controls - Confluence](https://confluence.global.standardchartered.com/display/FMCOOCC/FM-CES+Entitlement+Policy+%28Data+Sovereignty%29+-+Country+Requirements) | |
| User country codes | Will be provided by CES | |

Recon steps:

- [x] Dump ems2 users using script <u></u>
- [ ] Run script to fetch user data entitlements (via Auth server api), see bellow script
- [ ] Dump the results into local
- [ ] Run compare program to analysis the data

```bash
CSV_FILE="ems2_users.csv"
# this is the auth-server address (need to confirm if this need to be dynamically fetched from Eureka?)
BASE_URL="http://10.198.199.160:26519"
API_PATH="/v1/data-entitlement?userId="
RESULTS_DIR="/tmp/results"

mkdir -p "$RESULTS_DIR"

# Get all PSIDs into an array
mapfile -t psids < <(awk -F, 'NR>1 {print $NF}' "$CSV_FILE")
total=${#psids[@]}

for ((i=0; i<total; i++)); do
  psid="${psids[$i]}"
  psid="${psid//$'\r'/}"  # Remove carriage return
  if [ -n "$psid" ]; then
    echo "Processing PSID: $psid ($((i+1))/$total)"
    RESPONSE_FILE="${RESULTS_DIR}/${psid}.json"
    HTTP_RESPONSE=$(curl -v -s -w "HTTPSTATUS:%{http_code}" --request GET --url "${BASE_URL}${API_PATH}${psid}" 2>&1)
    STATUS=$(echo "$HTTP_RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    # Extract body before HTTPSTATUS and filter JSON line
    BODY=$(echo "$HTTP_RESPONSE" | sed -e 's/HTTPSTATUS:.*//' | grep -Eo '^\{.*\}$')
    LOGS=$(echo "$HTTP_RESPONSE" | sed -e 's/HTTPSTATUS:.*//' | grep -vE '^\{.*\}$')
    echo "{\"status\": $STATUS}" > "$RESPONSE_FILE"
    echo "$BODY" >> "$RESPONSE_FILE"
    echo "$LOGS" >> "$RESPONSE_FILE"
  fi
done
```

# Appendix

## Related references

- [Ratan and CES - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/Ratan+and+CES)
- [RATAN - Data entitlement test cases - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+-+Data+entitlement+test+cases)
- [FM-CES Entitlement Policy (Data Sovereignty) - Country Requirements - FM COO - Conduct and Controls - Confluence](https://confluence.global.standardchartered.com/display/FMCOOCC/FM-CES+Entitlement+Policy+%28Data+Sovereignty%29+-+Country+Requirements)

## Tracking list

| Category | Task | Provider | Dead line | Description |
| --- | --- | --- | --- | --- |
| Signoff | - [x] RATAN QA signoff | RATAN QA | | |
| - [ ] PSS signoff | RATAN PSS | 25 Apr | |
| - [ ] UAT signoff | RATAN users | | |
| - [ ] Downstream testing signoff - [x] EOD - [ ] SSDR/DQSL - [ ] CIS | Downstream systems | | |
| Recon | - [ ] Expected user country/business unit | CES | | |
| - [x] Recon script | Quill | | |
| | - [x] CES prod connectivity verify | PSS/Quill | | Verified the prod url is accessible in PROD Verified we can get response |
| | - [ ] Health check url | CES | | Need to remove auth check |
| PT | - [x] PT - [ ] PT under large dataset | | | |

## UAT & Downstream integration testing

UAT testing cases: [RATAN - Data entitlement test cases - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+-+Data+entitlement+test+cases)

| **Downstream ** | **SPOCs** | **Expected behaviour** | **Remark** | **Testing signoff** |
| --- | --- | --- | --- | --- |
| DQSL | [@Saminathan, Rajkannan](mailto:Rajkannan.Saminathan@sc.com) [@Wang, Hallie](mailto:Hallie.Wang@sc.com) [@Wang, Junwei](mailto:Junwei.Wang@sc.com) | No impact | | |
| CIS | [@Aggarwal, Vivek](mailto:Vivek.Aggarwal@sc.com) | No impact | | |
| RATAN EOD | [@Feng, Jerry Bin](mailto:Jerry-Bin.Feng@sc.com) | No impact | | - [x] done |
| FMMIS | [@Ahmed1, Mubeen](mailto:Mubeen.Ahmed1@sc.com) @Kishore, Kisalay | No impact | | |
| SSDR | [@Zhang, Cherry Ying](mailto:CherryYing.Zhang@sc.com) | Data entitlement applied | Data will be filtered according to the data entitlement settings in CES. If user is not onboarded in CES then query will fail with error. Note: As per BAU flow, SSDR user must apply role of RATAN_DATA_ENTITLEMENT in EMS2, otherwise cannot access cashflows. After migrated to CES, same rules in CES will be applied for RATAN/CES. | |

## BCS blotter data entitlement support assessment

The BCS blotter is querying from TDS via graphql endpoint in DA:

![image-2026-3-9_11-34-52.png](attachments/image-2026-3-9_11-34-52.png)

The query is:

```sql
SELECT /*+ QUERY_TRADES, INCLUDE_DUPLICATES */
*
from tl_sit_cashflows
WHERE 1 = 1
AND  Cashflow.Cashflow_State NOT IN ('NETTED', 'DEAD')
and Data_Flow.Source_Stack_Flow_Name NOT IN ('FMRP', 'FMRPSTELLA', 'FMRPSTELLA-LOANIQ')
ORDER BY Data_Flow.Data_Publication_Date_Time desc
LIMIT 1
```

However, the tl_sit_cashflows only contains around 130 fields, not all fields in Logic Model are supported:

- For known cases using Entity.Booking_Entity_SCI_FMID are supported
- JP case is not supported because Entity.Counterparty_Country_ISO_Code does not exist in the index

All fields in cashflow index could be found in <u></u>

Conclusion:

| | | |
| --- | --- | --- |
| Technical feasible? | Partial | This is acceptable from business perspective currently |
| Development effort | 3 | Including: - Integrate auth-service in data-ambassador (new service in current impl) - Validate CES filters – only support know fields, ignore unknown fields - Add filtering in TDS query - Retry of API - Unit testing |

### performance issue diagnose

In local we found that it takes super long time to query(around 60+s), while if we execute the sql directly it only takes 3 seconds:

```sql
SELECT /*+ QUERY_TRADES, INCLUDE_DUPLICATES */ BCS_Trade_Id,BCS_Parent_Trade_Id,Delivery_Method,Settlement_Method,Trade_Id,Trade_Version,Parent_Trade_Id,Trade_State,Cashflow.Cashflow_Id,Cashflow.Cashflow_Business_Version,Cashflow.Cashflow_Version,Cashflow.Cashflow_State,Cashflow.Cashflow_Event_Type,Cashflow.Payment_Currency,Cashflow.Payment_Date,Cashflow.Payment_Type,Cashflow.Pay_Receive_Indicator,Cashflow.Payment_Amount,Cashflow.Netting_Id,Cashflow.Payment_Receiver_Party_Reference,Cashflow.Payment_Payer_Party_Reference,Cashflow.Status_Event_Type,Cashflow.Event_Date,Entity.Booking_Entity_SCI_FMID,Entity.Counterparty_SCI_FMID,Instrument_Common.ISDA_Taxonomy,Instrument_Common.Source_System_Instrument_Sub_Type,Portfolio.Booking_Entity_Trade_Portfolio_Name 
from tl_prodreplica_cashflows 
WHERE 1 = 1 
AND (Entity.Booking_Entity_SCI_FMID IN ('10040387', '400568282', '10038345', '400516442', '400516443', '400667486', '10020899', 'FMIDBRAMX01', '400683682', '400327728', '400107029', '300010872', '401053411', '300036368', '400910415', '15', '400075752', '400609343', '400058959', '400677737', '10041902', '300010633', '400011581', '10041903', '2', '123', '3', '400130178', '4', '400095464', '5', '400452428', '10038468', '6', '10054931', '7', '8', '9', '400131263', '401081696', 'FINNKOREA01', '400040353', '300010782', '400170359', '10041530', '300011470', 'MUXBZ01', '10036981', '401037180', '300084297', '123M', '10075222', '400013111', '400960089', '1234', '400041070', '400001378', '400045551', '10062461', '300011345', '400032489', '400451508', '400033177', '400931959', '10037164', '10032025', '10063428', '400045549', '400991880', '400617263', '235003861', '400192940', '300089409', '400059978', '10078716', '400077046', '400077044', '400057714', '400798477', '400209000', '401036553', 'FM ID TST 1', '400088463', '400085753', '400220273', '400218197', '400007847', '300063361', '300011525', '400077978', '10036647', '400054708', '10036642', '10036645', '10038667', '400193370', '400090093', '400994973', '400130180', '400013557', '10037477', '10036382', '400227738', '400054741', '400172181', '10036775', '400054737', '10036655', '400625349', '400044944', '400823493', '400229749', '400093619', '10036430', '400018439', '400906330', '400017223', '300010730', '400147183', '10036428', '400022800', '400185419', '400899993', '195000930', '400823482', '400823485')) AND ( Cashflow.Cashflow_State NOT IN ('NETTED', 'DEAD') 
and Data_Flow.Source_Stack_Flow_Name NOT IN ('FMRP', 'FMRPSTELLA', 'FMRPSTELLA-LOANIQ')) 
ORDER BY Data_Flow.Data_Publication_Date_Time desc 
LIMIT 1000
```

Looking at the log, the actual bottleneck here is FmCodeQueryStrategy, not RatanOneCashflowDataQueryStrategy as I described for prod. The timings tell the story:

- RatanOneCashflowDataQueryStrategy cost: 868ms (fast)
- FmCodeQueryStrategy cost: 62,561ms — the real culprit
- step2 executes: 77924 ms (total join phase)

Why FmCodeQueryStrategy is slow locally:

The log shows it received 82 counterparty fmIds and processes them sequentially, one at a time. For each fmId:

- If in cache → fast (~600ms polling interval)
- If NOT in cache → tries to connect to [https://api-dqslrtdev.uk.dev.net/cp/graphql](https://api-dqslrtdev.uk.dev.net/cp/graphql), which fails with PKIX path building failed (SSL cert not trusted in your local JVM), each attempt taking ~450–635ms before failing
- With ~30+ cache misses × ~500ms each = ~20s just from SSL failures, and the rest from sequential cache hits, you get 62 seconds total.

Root cause: The CounterPartyFetcher.fetchByFmId() calls DQSL RT individually for each uncached fmId — no batching. Combined with SSL failures on [api-dqslrtdev.uk.dev.net](http://api-dqslrtdev.uk.dev.net) locally, this dominates.

This is a local-only issue — in prod, either the DQSL RT SSL cert is trusted, or more fmIds are already in cache. The RatanOneCashflowDataQueryStrategy is the prod bottleneck (large bulk query), while FmCodeQueryStrategy is the local bottleneck (sequential SSL-failing calls).

verified in DEV:

![image-2026-4-3_14-58-59.png](attachments/image-2026-4-3_14-58-59.png)

local:

![image-2026-4-3_15-0-38.png](attachments/image-2026-4-3_15-0-38.png)

## Daily recon design(draft)

It's important to know when whether it's intended when user's entitlement changed. If somehow the the user is missing some branches, then it's possible that the user will not be able to handle some pending cashflows. Since we're building the data entitlement system for the first time, it's recommended to run a daily recon so that we know what happens.

To verify user's data entitlement, we need CES to provide a report on user's data entitlements. However we can still get a diff report of what user's entitlement has changed (by comparing with previous data).

### Option 1: integrate into business logic

- Implement a daily job in auth-service, persist data into PG (or redis, persisted)
- diff data with previous day
- send email to PO if found any change

Note that we don't have PG in auth service currently. Alternatively, we could implement this job in query service.

### Option 2: Control-M job (business agnostic)

- Implement a python (or shell) script to fetch all entitlement from CES
- save the result into file
- compare with data of previous day and send diff to PO if found any

Since we'll directly call CES with ~700 users, we must limit the concurrency of the calls and agree the time, frequency with CES in advance.

## Review notes

| No | Issues/Question | Decision/Answer |
| --- | --- | --- |
| 1 | The scope of entitlement control: - SSDR report API: switch from our own data entitlement impl to CES - Cashflow blotter: New - Cashflow notification in cashflow blotter: New RATAN is targeting to go live before end of Mar 2026. And we'll call CES PROD once it's technical go live to do the recon. | Notification is sent in ws api in query service: /api/ratan/notification/subscriptions it's using mock entitlements currently in DataEntitlementOutboundChannelInterceptor - [ ] Currently, it's published to /cashflow/notification, the frontend need to subscribe to /user/{username}/queue/cashflow/notification |
| 2 | Consider mixing user query with entitlement condition into a nested "filter" object, which should also be compatible in OpenSearch: ``` {"and":[ {"field":"Cashflow.Cashflow_State","values":["Pending Operator"]}, {"or": [ {"field":"Entity.Booking_Entity_SCI_FMID","values":["401036553","400994973"]}, {"field":"Entity.Counterparty_Country_ISO_Code","values":["JP"]} ]} ]} ``` | Not mandatory |
| 3 | We need to consider a smooth way to toggle on/off CES in case that CES is unavailable. A possible approach is the dynamic configuration in RATAN portal, which is not live yet. Need to talk with Lu Shuai to understand if this is an option, so that we could: - Toggle on/off CES globally - Selectively enable/disable CES for single user Another approach is to bypass the entitlement control via URL. | Approaches: - [ ] Dynamic configuration via UI - [ ] Bypass data entitlement via URL |
| 4 | Consider moving the data entitlement responsibility from static-data-service to auth-service: - Aligned with current EMS2 flow - More clear responsibility since data entitlement is closer to authentication/authorization from functionality perspective - Benefit from the possibility that data entitlement could be included in JWT token when it's issued | - [x] Move to auth service |
| 5 | We should throw explicit error in frontend so that user know what happens and what to do, in the cases that: - CES unavailable - Wrong data/ User not onboarded We could retry on our side, and a proper retry strategy should be used. | |
| 6 | We should confirm the following technical objectives of CES: - SLA of CES. The api invocation could be estimated according to RATAN audit data. - API error codes | |
| 7 | We should start early engagement with PSS on the monitoring of CES. | |
| 8 | Confirm which FMAA account is using in v3/token endpoint | - [x] Confirmed: "user_name": "RATAN_PROD" |
| 9 | cashflowNew query uses plain SQL to query data entitlement | - [x] （frontend) should migrated to cashflowUltraQuery |
| 10 | Reuse EMS2 role? userId: 1481696, ems2Result: EntitlementList(count=1, entitlements=[Entitlement(id=11514754, subject=Subject(longName=/RATAN_DATA_ENTITLEMENT, name=RATAN_DATA_ENTITLEMENT, id=11164752, entity=Entity(systemName=RATAN, name=RATAN_DATA_ENTITLEMENT, locked=true, id=11164654)), role=Role(name=**Global**, id=11515751, entity=Entity(systemName=RATAN, name=RATAN_DATA_ENTITLEMENT, locked=true, id=11164654)), action=Action(name=VIEW_ENTITLEMENT, id=11164807, entity=Entity(systemName=RATAN, name=RATAN_DATA_ENTITLEMENT, locked=true, id=11164654)))]) | |
| 11 | Should the api in auth-service be whitelisted? (the login api is whitelisted) | It's already whitelisted for non-dev envs, see the following config: API_WHITELIST: 10.9.161.118,10.198.24.59,10.198.24.247,10.198.24.248,10.198.24.249,10.198.24.250,10.198.24.251 The api will respond following error if the client is not in the list: ![image-2026-1-8_14-8-33.png](attachments/image-2026-1-8_14-8-33.png) |
| 12 | Some SSDR query does not provide a bankId ![image-2026-1-6_10-34-29.png](attachments/image-2026-1-6_10-34-29.png) | This api is used not only by SSDR but also other systems: - SSDR -> DQSL -> RATAN API (System id + user id + Country), data entitlement enabled - TLM -> DQSL -> RATAN API (System id) - FMMIS, EOD, CIS -> RATAN API (System id) Ref to: [Expose The Cashflow Data Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Expose+The+Cashflow+Data+Design) |
| | - Query from cashflow_data fields instead of jsonb query? Review sql by DBA? | |
| | ASRM to be updated about new user onboarding SRM request Inform action owner if user profile changes cause user can't view expected data. | |
| | Call auth service in api gateway and pass to downstream services? | |

### Fetch entitlement in service Vs Fetch entitlement in api gateway

Comments: 1.    Given gateway is interacting with auth for 2As, I would prefer to pass the entitlements to Query service directly instead of querying to auth directly from there

![image-2026-1-30_16-9-24.png](attachments/image-2026-1-30_16-9-24.png)

| | Pros | Cons |
| --- | --- | --- |
| Option 1: api gateway pass data entitlement to backend services in header | - Ready-to-use data entitlement in backend services - Possible to implement more centralized caching of data entitlement | - Data entitlement is structured and must be encoded in header - Increases http request size (around 1k for 100 entity fmids) - **Can not handle the case if call is not invoked from GW → service, eg. Websocket notification** - **All request will be impacted - even if the backend api does not require data entitlement control** - **Restricted in error handling ** - **Services must pass data entitlement headers to nested calls** |
| | **Cons** | **Pros** |
| Option 2: each service call auth server to get entitlement on demand | - Backend service need to integrate with auth service - Each service need to call auth service separately | - More straightforward on processing data entitlement payload - No concern on data entitlement payload size - Can handle api calls that is directly requested from service discovery - Only in-scope api/features will be impacted - Service can decide how to handle error, eg. return CES error in graphql response |