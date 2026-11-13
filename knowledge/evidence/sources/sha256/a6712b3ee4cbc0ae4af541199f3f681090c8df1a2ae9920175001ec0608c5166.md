#

# Background

In one word, there are static configs hardcoded in UI project, which involves changes/release even minor modification on them. Here are configs we have,

| | UI Config | Shared UI Config |
| --- | --- | --- |
| Description | Configs only for UI usage. | Configs Shared Cross UI Applications |
| Samples | - Query Builder Operators Map - Blotter Column Definition - UI Dropdown Options (e.g. CCY) | - Booking Entity FMCODE/FMID. |
| | ![image-2025-5-7_10-3-26.png](attachments/image-2025-5-7_10-3-26.png)![image-2025-5-7_10-4-21.png](attachments/image-2025-5-7_10-4-21.png) | ![image-2025-5-7_10-2-16.png](attachments/image-2025-5-7_10-2-16.png) |

In additional, some service may depends on the booking entities.

# Assumption

- Static Data Service can be extended and provides graphql APIs.

# Cases

## Filter Builder Operator Mapping

| Case | Example |
| --- | --- |
| Config Sample | ```js { "text": ["=", "!=", "in", "notIn"], "number": ["=", "!=", ">=", "<=", "between"], "date": ["=", "!=", ">=", "<=", "between"], "datetime": ["=", "!=", ">=", "<=", "between"], "time": ["=", "!=", ">=", "<=", "between"], } ``` |
| Involving Applications | web:mfe-cashflow-blotter |
| Change Frequency | Low |

## Settlement On Board Entities (CPT & System White List & UI Entities Options)

| Case | Example |
| --- | --- |
| UI Config Sample | ```js [ { label: "SCB SHANGH*SHA", value: "10036642", country: "CHINA", }, { label: "SCB CN CHO*CHO", value: "400899993", country: "CHINA", }, ... ] ``` |
| BE Service Config Sample | ```js { FM_LIST: "401036553|400991880|400007847", STRATEGIC_FM_LIST: "10075222|400041070|400906330|300036368|3|400452428 ...", CPT_ENTITY_LIST: "6|2|10038345|300011345|300075472" } ``` |
| Involving Applications | web:mfe-cashflow-blotter, service:ratanone-settlement-orchestration-service |
| Change Frequency | High |

# Principle

We may follow some principles to ensure design meet the final requirements,

1. Move mutable configurations to database instead of hard code, provides service for query.

2. Should provides institutive API query for certain config by name or domain.

3. Should store generic type of config data.

4. Should have version control and audit.

# Proposal

I proposal a strategic solution for static config maintains.

## Architecture Diagram

## Data Structure & Persisted

### Config Table

| Key | Type | Mandatory | Description |
| --- | --- | --- | --- |
| id | VARCHAR | Yes | unique id |
| context | VARCHAR | Yes | name of config |
| domain | VARCHAR | No | belonging of config. multiple domains separate by comma. |
| schema | VARCHAR | No | schema definition of content, validate the fomat. Use **JSON-Schema**. |
| state | VARCHAR | Yes | LIVE/DISABLED |
| version | VARCHAR | Yes | version |

### Config Content Table

| Key | Type | Mandatory | Description |
| --- | --- | --- | --- |
| id | VARCHAR | Yes | unique id |
| context | VARCHAR | Yes | name of config |
| key | VARCHAR | Yes | key, unique under context |
| value | VARCHAR | Yes | value |
| type | VARCHAR | No | |
| sub_type | VARCHAR | No | |
| metadata | VARCHAR | No | metadata, normally it's a JSON string. |
| state | VARCHAR | Yes | LIVE/DISABLED/UPDATE_PENDING/DEAD/ADD_PENDING |
| version | INT | Yes | |

### Audit Table

| Key | Type | Description |
| --- | --- | --- |
| id | VARCHAR | unique id of audit |
| config_id | VARCHAR | id of config |
| content_id | VARCHAR | id of config content |
| context | VARCHAR | context of config |
| domain | VARCHAR | domain of config. multiple domains separate by comma. |
| state | VARCHAR | UPDATE/ADDED/DELETED/PENDING_UPDATE/PENDING_ADDED/PENDING_DELETED |
| key | VARCHAR | key |
| value | VARCHAR | value |
| type | VARCHAR | type |
| metadata | VARCHAR | metadata |
| schema | VARCHAR | schema definition of content, validate the fomat. Use **JSON-Schema**. |
| version | INT | |
| updated_at | VARCHAR | |
| updated_by | VARCHAR | |

### Cases

#### Operator Mapping

| Table | Field | Value |
| --- | --- | --- |
| Config Table | context | settlement_field_type_operator_mapping |
| domain | mfe-cashflow-blotter,mfe-cashflow-dashboard |
| schema | <details> <summary>Expand Details</summary> ```js { "$schema": "http://json-schema.org/draft-07/schema#", "type": "object", "properties": { "key": { "title": "fieldType", "type": "string" }, "value": { "title": "operators", "type": "string" } }, "required": ["key", "value"], "additionalProperties": false } ``` </details> |
| Config Content Table | context | settlement_field_type_operator_mapping | settlement_field_type_operator_mapping |
| key | text | number |
| value | ["=", "!=", "in", "notIn"] | ["=", "!=", ">=", "<="] |
| type | | |
| sub_type | | |
| metadata | | |
| version | 0 | 0 |

#### Booking Entities

| Table | Field | Value |
| --- | --- | --- |
| Config Table | context | settlement_booking_entities |
| domain | mfe-cashflow-blotter,mfe-cashflow-dashboard,mfe-trades, ratanone-settlement-orchestration-service |
| schema | <details> <summary>Expand Details</summary> ```js { "$schema": "http://json-schema.org/draft-07/schema#", "type": "object", "properties": { "key": { "title": "fmId", "type": "string" }, "value": { "title": "fmCode", "type": "string" }, "type": { "title": "flow", "type": "string", "enum": ["NORMAL", "STRATEGIC", "CPT"] }, "metadata": { "type": "object", "properties": { "country": { "type": "string" } } } }, "required": ["key", "value", "type", "metadata"], "additionalProperties": false } ``` </details> |
| Config Content Table | context | settlement_booking_entities | settlement_booking_entities |
| key | 10036642 | 400899993 |
| value | SCB SHANGH*SHA | SCB CN CHO*CHO |
| type | STRATEGIC | CPT |
| sub_type | | |
| metadata | {"country":"CHINA"} | {"country":"CHINA"} |
| version | 0 | 0 |

## Management

Instead of manage configs by directly sql, we can use API or GUI to manage them,

### API

### GUI

# Integration

## Web

| Methods | Examples |
| --- | --- |
| Query With Plain Fetch | <details> <summary>Expand Details</summary> ```js fetch("/api/ratan/staticconfig", { method: "POST", body: { query: "" } }) ``` </details> |
| Query With Hook | <details> <summary>Expand Details</summary> ```js const { data, isLoading, error } = useStatisConfigByNames(["settlement_booking_entities"], { cache: true }); // data { totalResults: 2, results: [ ], } ``` </details> |

## Service

TBD

## Cache

### Web

For UI, when using hook query, we recommend use **cache-first mode**. If use plain query api, then should handle cache and loading manually.

| Case | Behavior |
| --- | --- |
| **Cache First Mode** | When cache exist, always read from cache and return, meanwhile query for the latest config, return the latest once query done. |
| **Normal Mode** (Not Cache First) | Always depends on the latest config. |
| First Call or Cache be Cleared | Dependent components loading till latest config returns, meanwhile updates cache. |

### Service

Radis

# Realtime Subscription

In traditional config usage, we only use query for configs, which can't detect changes on configs.

## Feature Flag

Feature Flag is a good use case for subscription, it requires real-time reaction for any changes on feature flags.

# Release Timeline (Draft)

## Phase 1

## Phase 2

## Phase 3