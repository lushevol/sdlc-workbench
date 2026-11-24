# Background

There're some ratan configurations live in static data service and are used by other services, such as bicnetting config, fxu config, etc. These configurations can also be updated by user through maker/checker process in blotter:

![image-2025-10-7_16-11-49.png](attachments/image-2025-10-7_16-11-49.png)

It's likely that we'll add similar configurations in future to fit for various business cases, and the flow for the configurations are actually same. The requirements could be summarized as bellow:

- API endpoint for other services to fetch the configuration, might require to filter by some columns
- UI interface for configuration management, including: - List page for searching - Allow maker to create/update/delete configurations - Allow checker to confirm/cancel the configuration - Get the audit logs of configurations

## Current implementation

| | Nostro main table | Nostro audit table | BicNetting main table | BicNetting audit table |
| --- | --- | --- | --- | --- |
| Maker create | Insert, status=ADD_PENDING | Insert ADD_PENDING | Insert, status=ADD_PENDING checker=System， id=784 | Insert ADD_PENDING |
| Maker update | set status=UPDATE_PENDING | Insert UPDATE_PENDING | Insert, status=UPDATE_PENDING id=785, updateRecordId=784 | Insert UPDATE_PENDING id=785 |
| Maker delete | set status=DELETE_PENDING | Insert DELETE_PENDING | | |
| Checker reject creation | set status=DISCARDED | Insert DISCARDED | | |
| Checker confirm creation | set status=SAVE_CONFIRMED | Insert SAVE_CONFIRMED | set status=SAVE_CONFIRMED | Insert SAVE_CONFIRMED |
| Checker reject update | set status=SAVE_CONFIRMED | Insert SAVE_CONFIRMED | set 785=DISCARDED | Insert DISCARDED id=785 |
| Checker confirm update | set status=SAVE_CONFIRMED, update data | Insert SAVE_CONFIRMED | set 784=SAVE_CONFIRMED, and update data set 785=DISCARDED | Insert SAVE_CONFIRMED id=784 |
| Checker reject deletion | set status=SAVE_CONFIRMED | Insert SAVE_CONFIRMED | | |
| Checker confirm deletion | set status=DELETE_CONFIRMED | Insert DELETE_CONFIRMED | | |

### Nostro

Nostro coniguration shows a list of current data, and each item has the action to update, delete or to be confirmed by checker.

![image-2025-10-13_15-6-7.png](attachments/image-2025-10-13_15-6-7.png)

In database it remains two tables:

### ![image-2025-10-13_15-4-33.png](attachments/image-2025-10-13_15-4-33.png)

### BicNetting

The bicNetting configuration edit page is different compared with nosto, there's no action button in the list and user need to click detail to update or delete. And checker uses menu to verify:

![image-2025-10-13_15-29-45.png](attachments/image-2025-10-13_15-29-45.png)

The main design difference is that bicnetting updates the data of main record directly when maker update, a new record is generated when you update an existing record. Bellow screenshot shows that update 786 will actually create a new record 789:

![image-2025-10-13_16-8-14.png](attachments/image-2025-10-13_16-8-14.png)

Since 786 is still SAVE_CONFIRMED state, checker cannot make any change to 786, but need to confirm 789. Once 789 is confirmed, that change will be write to 786 again, and 789 is discarded, which could be quite confusing. Besides, since we have multiple records, the audit logs will have multiple record id:

![image-2025-10-13_16-3-4.png](attachments/image-2025-10-13_16-3-4.png)

This makes it very hard to get related audit logs of a single record.

## Issues

| Issue | Priority | |
| --- | --- | --- |
| The code design is not reusable when creating new configuration, the develop/test effort is quite big | HIGH | Current implementation is not designed to be reusable for similar cases, as a result, there's some drawbacks if we duplicate existing solution to add new configuration: - We need to duplicate 5 APIs for CRUD, register then in API gateway, with data entitlements - We need to implement maker/checker status management inside each configuration, including status transformation, audit log recoding, and also data validation. This could be complex and require significant effort. - We also need to adapt APIs in frontend |
| Inconsistent user experience | MEDIUM | |
| Known issues in BicNetting config page | MEDIUM | - New record is created when update existing record, which is different with Nostro editing - Audit log is incomplete since multiple records are connected - List page is not refreshed after user operation - User could delete the original record even if an update pending record exists, which causes unpredictable behavior |

Besides, there're some problems:

- To get the effective data, we must carefully filter the data by status in SAVE_CONFIRMED, DELETE_PENDING
- There's no version control for configuration data, for example, maker updated the data but checker haven't approved yet, then we should get previous configuration through fetch API
- It will be complicated if we want to import data directly to database, since we need to filter data to query current state and then import data with additional maker/checker fields

Inconsistent user experience in UI:

![image-2025-10-13_11-5-50.png](attachments/image-2025-10-13_11-5-50.png)

# Objectives

- Reduce the effort when adding similar configuration item
- Make the design reusable and robust and avoid the chances to make mistakes while doing copy/paster

# Proposed solutions

## Option1:  Separated config tables + shared audits

The core idea is to create an engine for maker/checker flow and manage the audit histories automatically.  This solution is similar to the current Nostro configuration implementation.

## Database design

```sql
CREATE TABLE ratan_static_config_maker_request (
    id bigserial NOT NULL PRIMARY KEY,
    maker_id TEXT NOT NULL,
    checker_id TEXT NULL,
    target_table TEXT NOT NULL,   -- target configuration table, eg. ratan_fxu_config
    target_id BIGINT,             -- id for update/delete
    operation_type TEXT NOT NULL, -- insert, update, delete
    data_status TEXT NOT NULL,    -- pending, confirmed, rejected, cancelled
    payload TEXT NOT NULL,        -- configuration json, differs accroding target table
    created_at timestamp NOT NULL DEFAULT now(),
	updated_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE ratan_static_config_audit_log  (
    id SERIAL PRIMARY KEY,
    operator TEXT NOT NULL,
    role TEXT NOT NULL,           -- maker/checker
    operation_type TEXT NOT NULL,
    target_table TEXT NOT NULL,
    target_id BIGINT,
    target_snapshot TEXT NOT NULL, 
    created_at timestamp NOT NULL DEFAULT now(),
);

CREATE TABLE IF NOT EXISTS ratan_fxu_config (
	id SERIAL PRIMARY KEY,
	booking_entity_fmid TEXT NOT NULL,
	counterparty_fmid TEXT NOT NULL,
	booking_entity_fmcode TEXT NOT NULL,
	counterparty_fmcode TEXT NOT NULL,
	is_auto_utilize BOOLEAN NOT NULL,
	settlement_means TEXT NOT NULL,
	settlement_account TEXT NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	updated_at timestamp NOT NULL DEFAULT now()
);
```

## Option2: Unified configuration with JSON

Config table:

| ID | type | data | maker | checker |
| --- | --- | --- | --- | --- |
| 1 | nostro | {"nostroId": 123, "ebbsAccount":...} | 1440119 | 2022123 |
| 2 | nostro | {"nostroId": 456, "ebbsAccount":...} | 2022123 | 1440119 |
| 3 | fxu | {"entityFmId": 123, "autoUtil":...} | System | System |

Audit table:

| ID | entity_id | type | snapshot | operator | created_at | status |
| --- | --- | --- | --- | --- | --- | --- |
| a1 | 1 | nostro | {"nostroId": 123, "ebbsAccount":...} | 2022123 | 2025-10-10 | ADD_PENDING |
| a2 | 1 | nostro | {"nostroId": 456, "ebbsAccount":...} | 1440119 | 2025-10-11 | SAVE_CONFIRMED |
| a3 | 3 | fxu | {"entityFmId": 123, "autoUtil":...} | 1440119 | 2025-10-10 | ADD_PENDING |

## Option2 Variant: Unified configuration via data table

Meta data table:

| ID | type | field | description | type | format | mandatory |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | nostro | nostroId | | string | | true |
| 2 | nostro | nostroId | | string | \d{6} | true |
| 3 | fxu | autoUtil | | boolean | | true |
| 4 | fxu | entityFmID | | string | FMID | true |

Config table:

| ID | type | maker | checker |
| --- | --- | --- | --- |
| 1 | nostro | 1440119 | 2022123 |
| 2 | nostro | 2022123 | 1440119 |
| 3 | fxu | System | System |

Config value table:

| ID | entity_id | field | value |
| --- | --- | --- | --- |
| 1 | 1 | nostroId | 123 |
| 2 | 1 | nostroId | 456 |
| 3 | 2 | autoUtil | true |

Audit table:

| ID | entity_id | type | snapshot | operator | created_at | status |
| --- | --- | --- | --- | --- | --- | --- |
| a1 | 1 | nostro | {"nostroId": 123, "ebbsAccount":...} | 2022123 | 2025-10-10 | ADD_PENDING |
| a2 | 1 | nostro | {"nostroId": 456, "ebbsAccount":...} | 1440119 | 2025-10-11 | SAVE_CONFIRMED |
| a3 | 3 | fxu | {"entityFmId": 123, "autoUtil":...} | 1440119 | 2025-10-10 | ADD_PENDING |

| | Copy/Paste existing solution(Nostro impl) | Copy/Paste existing solution (BicNetting impl) | Option A: Separated config table + shared engine | Option B: Unified configuration via JSON | Option B variant: via table |
| --- | --- | --- | --- | --- | --- |
| Backend development effort | +++++ | +++++ | +++ ++(for new config) | ++++ +(for new config) | +++++ +(for new config) |
| Frontend development effort | +++ | ++++ | ++++ | + | + |
| Test effort | +++++ | | +++ | +++ | +++++ +(for new config) |
| APIs | at least 5xN(for UI)+ N(for service) | | 5 + N | 5+ 1 | 5 + 1 |
| Allow basic validation (not null, regex, etc) | ✔️ | ✔️ | ✔️ | ❌(Yes if add meta data) | ✔️(Need meta table) |
| Allow add customized validation | ✔️ | ✔️ | ✔️ | ❌ | ❌ |
| Algorithm to get effective items | Filter by status | Filter by status | WYSIWYG | Filter by type | Filter by type, select values by id |
| Consistency guarantee | ❌Database unique constraints (Strong) ✔️Front end validation(Weak) ✔️Status check(Weak) | ❌Database unique constraints (Strong) ✔️Front end validation(Weak) ✔️Status check(Weak) | ✔️Database unique constraints (Strong) ✔️Front end validation(Weak) ✔️Status check(Weak) | ❌Database unique constraints (Strong) ✔️Front end validation(Weak) ✔️Status check(Weak) | ❌Database unique constraints (Strong) ✔️Front end validation(Weak) ✔️Status check(Weak) |
| Manual import/export via SQL | ✔️ | ✔️(Need to check if data already exists) | ✔️ | ❌(Need to generate sql with JSON) | ❌(Need to generate multiple sql inserts) |
| Dynamic UI generate | ❌ | ❌ | ❌ | ❌ | ✔️ |
| Additional config value(eg. settlementAccount in FXU) | ✔️ | ✔️ | ✔️ | ❌ | ❌ |
| Additional UI control(eg. limit editable fields, auto populate fmCode) | ✔️ | ✔️ | ✔️ | ✔️ | ❌(If use dynamic UI from meta) |

## API design

### Shared APIs( For UI)

List requests:

```py
GET /v1/static/config/{target_table}
```

Maker create new configuration request:

```py
POST /v1/static/config/{target_table}
{
    (payload...)
}
```

Maker update:

```py
POST /v1/static/config/{target_table}/{target_id}/update
{
    (payload...)
}
```

Maker delete:

```py
POST /v1/static/config/{target_table}/{target_id}/delete
```

Maker cancel:

```py
POST /v1/static/config/{target_table}/{target_id}/cancel
```

Checker confirm:

```py
POST /v1/static/config/{target_table}/{target_id}/approve
```

Checker reject:

```py
POST /v1/static/config/{target_table}/{target_id}/reject
```

Audit log:

```py
GET /v1/static/config-audit-logs/{target_table}?page=0&size=5
```

# Fetch API(for service & UI)

Must be implemented independently according each feature.

# Breaking change

1. Currently the pending request is shown together with records in the list, if we want to make a common solution the request and record should be separated in UI, otherwise the pagination will be hard to implement