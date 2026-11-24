****

# **1.  Background**

Now,  the Ratan changement for new branch/entity onboarding contains FE code change、service config file change and DB table data change , which will be done by developers. The changement details are as below:

[Enabling Settlement for Manual Entities(12 entities) - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3556617849)

[Enabling Settlement for Manual Entities - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Enabling+Settlement+for+Manual+Entities#EnablingSettlementforManualEntities-CPT)

# **2. Requirements**

Developers no longer release features to add a new entity/branch, users use the UI Blotter to do it  by themselves.

# **3. Principle**

No need to deploy any code change in production env for new entity/branch on boarding.  Switch hard coding to configuration-based,  move the code change from FE local file and backend service config file to the database or configserver.

# **4. High Level Design**

There are four design options to support a new branch/entity onboarding :

**Option1 design：**

**save different static config into corresponding DB table and Config Server, multiple UI blotter to manage static configs of new branch onboarding.**

**FE read service API to show static config,  service read config from DB and config server.**

1.Create multiple blotters from the backend service perspective.  As much as possible one backend service, one blotter.  Save the blotter's data to the corresponding backend service or config server.

2..Create some tables in  ratan-static-data-service to save FE hard code config

3. Backend service get static config from DB and config server,FE get static config via calling backend service API.

****

**Option2 design：**

**save different static config into corresponding DB table, multiple UI blotter to manage static configs of new branch onboarding.**

**FE read service API to show static config,  service read config from DB.**

1.Create multiple blotters from the backend service perspective. As much as possible one backend service, one blotter.  Save the blotter's data to the corresponding backend service.

2.Create some tables in diferent backend service to save FE hard code config and application.yml data, FE get static config via calling backend service API, backend service get static config from DB.

****

**Option3 design：**

**save whole static configs  into ratan-static-data-service DB table,  only one aggregated UI blotter to manage static configs of new branch onboarding.**

**FE read service API to show static config,  service read config from DB.**

1.Create one blotter which aggregate all static configs.

2.Create one table in ratan-static-data-service DB to save the Blotter data. ** **

3.Ratan-static-data-service distributed the static configs to other backend service via Kafka message.

4.Other services save corresponding static config as needed into DB table

**Option4 design：**

1.Create one blotter which can upload all new entity excel data, download template file(add\update\delete) and result excel.

2.Ratan-static-data-service parsed excel data and insert them to different db schema

(if static configs in application.yml do not be transfered to db,  need config server  to hot update  config)

question:

1.  invloved config server to support dynamic config？ Or transfer application.yml config to DB?

2.  how to verify data for user ?

****

# **5. Low Level Design**

**option1：**

code change summary:

1. integrate config server,  use config server manage swift-service、 accounting-service 、static-data-service and orchestration-service config file

integrate config server link:    [3.How To Integrate - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/3.How+To+Integrate)

2. create new table(ratanone.ratan_static__common_metadata_dict、ratanone.ratan_static__country_conf、ratanone.ratan_static__entity_conf）to store blotter config data,

migrate UI blotter local file data to table

3. add CRUD API and audit function for the multiple new  blotters.

The code changes to the FE and backend services are shown in the table below：

| config source | service/db schema name | blotter/table/config name | FE static config blotter | BE code change |
| --- | --- | --- | --- | --- |
| Blotter Config | FE | Cashflow Blotter-SCB Booking Entity | new entity static config blotter | migrate blotter data to ratan_static__entity_conf; |
| Cashflow Blotter-Currency | migrate blotter data to ratan_static__common_metadata_dict; |
| Cashflow Dashboard-Booking Entity | migrate blotter data to ratan_static__entity_conf; |
| Cashflow Dashboard-Country/Region | migrate blotter data to ratan_static__country_conf; |
| Nostro Static Blotter-Currency | migrate blotter data to ratan_static__common_metadata_dict; |
| Settlement Means | migrate blotter data to ratan_static__common_metadata_dict; |
| DB table data | ratan_cashflow_lifecycle_service | ratan_cashflow_rounding_config | rounding static config blotter | 1.add a new blotter 2.add CRUD API 3.add audit function |
| ratan_cashflow_static_new_entity_config(new) | |
| ratanone_swift_service | swift_static_data_correspondent_bic | swfit bic static config blotter | 1.add a new blotter 2.add CRUD API 3.add audit function |
| swift_static_data_sender_bic | |
| swift_static_new_entity_config(new) | |
| ratanone | ratan_bridge_flow | new entity static config blotter | 1.add a new blotter 2.add CRUD API 3.add audit function |
| ratan_static__cashflow_ebbs_txn_code | |
| ratan_static__cashflow_ebbs_bridge_account | |
| ratan_static__cashflow_currency_cut_off | |
| ratan_static__new_entity_config(new) | |
| service config file | accouting-service | time-zone.mappings | config server blotter | integrate with config server, read from config server |
| swift-service | mx-generation.entity-scope-conditions | integrate with config server, read from config server |
| static-data-service | sd.branch-code.mappings | integrate with config server, read from config server |
| orchestration-service | STRATEGIC_FM_LIST | integrate with config server, read from config server |

**option2：**

code change summary:

1. create new table（ratanone.ratan_static__common_metadata_dict、ratanone.ratan_static__country_conf、ratanone.ratan_static__entity_conf、ratanone.ratan_static__isocurrency_mapping、swift_static_mx_generation_condition）

to store blotter config data and backend service config data, migrate UI blotter local file data and backend service config data  to table

2. change backend service read config file logic to read DB

3. add CRUD API and audit function for the multiple new  blotters.

The code changes to the FE and backend services are shown in the table below：

| config source | service/db schema name | blotter/table/config name | FE static config blotter | BE code change |
| --- | --- | --- | --- | --- |
| Blotter Config | FE | Cashflow Blotter-SCB Booking Entity | new entity static config blotter | migrate blotter data to ratan_static__entity_conf; |
| Cashflow Blotter-Currency | migrate blotter data to ratan_static__common_metadata_dict; |
| Cashflow Dashboard-Booking Entity | migrate blotter data to ratan_static__entity_conf; |
| Cashflow Dashboard-Country/Region | migrate blotter data to ratan_static__country_conf; |
| Nostro Static Blotter-Currency | migrate blotter data to ratan_static__common_metadata_dict; |
| Settlement Means | migrate blotter data to ratan_static__common_metadata_dict; |
| DB table data | ratan_cashflow_lifecycle_service | ratan_cashflow_rounding_config | rounding static config blotter | 1.add a new blotter 2.add CRUD API 3.add audit function |
| ratan_cashflow_static_new_entity_config(new) | |
| ratanone_swift_service | swift_static_data_correspondent_bic | swfit bic static config blotter | 1.add a new blotter 2.add CRUD API 3.add audit function |
| swift_static_data_sender_bic | |
| ratanone_swift_service.swift_mx_generation_condition(new) | |
| swift_static_new_entity_config(new) | |
| ratanone | ratan_bridge_flow | new entity static config blotter | 1.add a new blotter 2.add CRUD API 3.add audit function |
| ratan_static__cashflow_ebbs_txn_code | |
| ratan_static__cashflow_ebbs_bridge_account | |
| ratan_static_cashflow_currency_cut_off | |
| ratan_static__country_conf(new) | |
| ratan_static__entity_conf(new) | |
| ratan_static__common_metadata_dict(new) | |
| ratan_static__new_entity_config(new) | |
| service config file | accouting-service | time-zone.mappings（remove） | no need | migrate config to ratan_static__country_conf; |
| swift-service | mx-generation.entity-scope-conditions（remove） | migrate config to ratanone_swift_service.swift_[mx](http://ratanone.mx/)_generation_condition |
| static-data-service | sd.branch-code.mappings（remove） | migrate config to ratan_static__entity_conf; |
| orchestration-service | STRATEGIC_FM_LIST（remove） | migrate config to ratan_static__common_metadata_dict; |

**option3：**

Below sequence diagram shows interaction process between multiple systems after user operates UI blotter

Below activity diagram shows internal logic processing details of ratan-static-data-service and downstream systems.

****

code change summary:

1. create new table（ratanone.ratan_static__entity_onboarding_config、ratanone.ratan_static__common_metadata_dict、ratanone.ratan_static__country_conf、ratanone.ratan_static__entity_conf、ratanone.ratan_static__isocurrency_mapping、swift_static_mx_generation_condition）

to store blotter config data and backend service config data, migrate UI blotter local file data and backend service config data  to table

DB table details link:  [Database table design](#db)

2.  add CRUD API and audit function for new blotter （static-data-service table ratanone.ratan_static__entity_onboarding_config）

3.   static-data-service distribute static config to kafka

4.   backend service consume kafka topic and save static config into DB, read config file logic change to read DB

The code changes to the FE and backend services are shown in the table below：

| config source | service/db schema name | blotter/table/config name | FE static config blotter | BE code change |
| --- | --- | --- | --- | --- |
| Blotter Config | FE | Cashflow Blotter-SCB Booking Entity | new entity static config blotter | migrate blotter data to ratan_static__entity_conf; |
| Cashflow Blotter-Currency | migrate blotter data to ratan_static__common_metadata_dict; |
| Cashflow Dashboard-Booking Entity | migrate blotter data to ratan_static__entity_conf; |
| Cashflow Dashboard-Country/Region | migrate blotter data to ratan_static__country_conf; |
| Nostro Static Blotter-Currency | migrate blotter data to ratan_static__common_metadata_dict; |
| Settlement Means | migrate blotter data to ratan_static__common_metadata_dict; |
| DB table data | ratan_cashflow_lifecycle_service | ratan_cashflow_rounding_config | |
| ratanone_swift_service | swift_static_data_correspondent_bic | |
| swift_static_data_sender_bic | |
| ratanone_swift_service.swift_mx_generation_condition(new) | |
| ratanone | ratan_bridge_flow | 1.add a new blotter 2.add CRUD API 3.add audit function |
| ratan_static__cashflow_ebbs_txn_code | |
| ratan_static__cashflow_ebbs_bridge_account | |
| ratan_static_cashflow_currency_cut_off | |
| ratan_static__country_conf(new) | |
| ratan_static__entity_conf;(new) | |
| ratan_static__common_metadata_dict(new) | |
| ratan_static__entity_onboarding_config(new) | |
| | ratan_static__entity_onboarding_config_sync_result(new) | |
| service config file | accouting-service | time-zone.mappings（remove） | no need | migrate config to ratan_static__country_conf; |
| swift-service | mx-generation.entity-scope-conditions（remove） | migrate config to ratanone_swift_service.swift_[mx](http://ratanone.mx/)_generation_condition |
| static-data-service | sd.branch-code.mappings（remove） | migrate config to ratan_static__entity_conf; |
| orchestration-service | STRATEGIC_FM_LIST（remove） | migrate config to ratan_static__common_metadata_dict; |

# **6. API Design**

**option 1,2:**

6.1 settlementMeans、currency list

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/static/metadata/{type}/list | GET | | [{ "id": 11111, "fieldType": "currency", "fieldValue": "USD", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | type: currency or settlementMeans |
| add | /v1/static/metadata/{type} | POST | { "fieldType": "currency", "fieldValue": "CNO" } | { "code": 200, "message": "xxx" } | |
| update | /v1/static/metadata/{type} | POST | { "id": 11111, "fieldType": "currency", "fieldValue": "CNO" } | { "code": 200, "message": "xxx" } | |
| delete | /v1/static/metadata/{type}/{id} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/static/metadata/{type}/audit/{id} | GET | | [{ "id": 11111, "fieldType": "currency", "fieldValue": "USD", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/static/metadata/{type}/audit | GET | page={page}&size={size} | [{ "id": 11111, "fieldType": "currency", "fieldValue": "USD", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/static/metadata/{type}/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/static/metadata/{type}/cancel/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

6.2 country detail

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/static/country/list | GET | | [{ "id": 11111, "code": "CN", "country": "CHINA", "zoneId": "Asia/Shanghai", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| add | /v1/static/country | POST | { "code": "currency", "country": "CNO", "zoneId": "Asia/Shanghai" } | { "code": 200, "message": "xxx" } | |
| update | /v1/static/country | POST | { "id": 11111, "code": "currency", "country": "CNO", "zoneId": "Asia/Shanghai" } | { "code": 200, "message": "xxx" } | |
| delete | /v1/static/country/{id} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/static/country/audit/{id} | GET | | [{ "id": 11111, "code": "CN", "country": "CHINA", "zoneId": "Asia/Shanghai", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/static/country/audit | GET | page={page}&size={size} | [{ "id": 11111, "code": "CN", "country": "CHINA", "zoneId": "Asia/Shanghai", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/static/country/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/static/country/cancel/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

6.3 entity detail

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/static/entity/filter | POST | { "id": 11111, "fmid": "10008755", "bookingEntity": "SCB xxxx", "countryCode": "CN", "branchCode": "123", } | [{ "id": 11111, "fmid": "10008755", "bookingEntity": "SCB xxxx", "countryCode": "CN", "branchCode": "123", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| add | /v1/static/country | POST | { "fmid": "10008755", "bookingEntity": "SCB xxxx", "countryCode": "CN", "branchCode": "123"} | { "code": 200, "message": "xxx" } | |
| update | /v1/static/country | POST | { "id": 11111, "fmid": "10008755", "bookingEntity": "SCB xxxx", "countryCode": "CN", "branchCode": "123"} | { "code": 200, "message": "xxx" } | |
| delete | /v1/static/country/{id} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/static/country/audit/{id} | GET | | [{ "id": 11111, "fmid": "10008755", "bookingEntity": "SCB xxxx", "countryCode": "CN", "branchCode": "123" "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/static/country/audit | GET | page={page}&size={size} | [{ "id": 11111, "fmid": "10008755", "bookingEntity": "SCB xxxx", "countryCode": "CN", "branchCode": "123" "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/static/country/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/static/country/cancel/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

6.4 currecy cut off

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/static/currency/cutoff/filter | POST | { "id": 11111, "fmid": "10008755", "legalEntity": "SCB xxxx", "currency": "CN" } | [{ "id": 11111, "fmid": "10008755", "legalEntity": "SCB xxxx", "currency": "CN", "cutoffTime": "SCB xxxx", "cutoffTimeZone": "CN", "cutoffShifter": "SCB xxxx", "cutoffShifterUnit": "CN", "queueShifter": "SCB xxxx", "queueShifterUnit": "CN", "nettingShifter": "SCB xxxx", "nettingShifterUnit": "CN", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| add | /v1/static/currency/cutoff | POST | { "fmid": "10008755", "legalEntity": "SCB xxxx", "currency": "CN", "cutoffTime": "SCB xxxx", "cutoffTimeZone": "CN", "cutoffShifter": "SCB xxxx", "cutoffShifterUnit": "CN", "queueShifter": "SCB xxxx", "queueShifterUnit": "CN", "nettingShifter": "SCB xxxx", "nettingShifterUnit": "CN",} | { "code": 200, "message": "xxx" } | |
| update | /v1/static/currency/cutoff | POST | { "id": 11111, "fmid": "10008755", "legalEntity": "SCB xxxx", "currency": "CN", "cutoffTime": "SCB xxxx", "cutoffTimeZone": "CN", "cutoffShifter": "SCB xxxx", "cutoffShifterUnit": "CN", "queueShifter": "SCB xxxx", "queueShifterUnit": "CN", "nettingShifter": "SCB xxxx", "nettingShifterUnit": "CN",} | { "code": 200, "message": "xxx" } | |
| delete | /v1/static/currency/cutoff/{id} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/static/currency/cutoff/audit/{id} | GET | | [{ "id":111111, "fmid": "10008755", "legalEntity": "SCB xxxx", "currency": "CN", "cutoffTime": "SCB xxxx", "cutoffTimeZone": "CN", "cutoffShifter": "SCB xxxx", "cutoffShifterUnit": "CN", "queueShifter": "SCB xxxx", "queueShifterUnit": "CN", "nettingShifter": "SCB xxxx", "nettingShifterUnit": "CN", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/static/currency/cutoff/audit | GET | page={page}&size={size} | [{ "id": 11111, "fmid": "10008755", "legalEntity": "SCB xxxx", "currency": "CN", "cutoffTime": "SCB xxxx", "cutoffTimeZone": "CN", "cutoffShifter": "SCB xxxx", "cutoffShifterUnit": "CN", "queueShifter": "SCB xxxx", "queueShifterUnit": "CN", "nettingShifter": "SCB xxxx", "nettingShifterUnit": "CN", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/static/currency/cutoff/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/static/currency/cutoff/cancel/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

6.5 isocurrency mapping

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/static/isocurrency/{currency} | GET | | { "id": 11111, "currency": "CN", "isocurrency": "CHINA", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" } | |
| list | /v1/static/isocurrency/list | GET | | [{ "id": 11111, "currency": "CN", "isocurrency": "CHINA", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| add | /v1/static/isocurrency | POST | { "currency": "currency", "isocurrency": "CNO",} | { "code": 200, "message": "xxx" } | |
| update | /v1/static/isocurrency | POST | { "id": 11111, "currency": "currency", "isocurrency": "CNO"} | { "code": 200, "message": "xxx" } | |
| delete | /v1/static/isocurrency/{id} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/static/isocurrency/audit/{id} | GET | | [{ "id": 11111, "currency": "currency", "isocurrency": "CNO", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/static/isocurrency/audit | GET | page={page}&size={size} | [{ "id": 11111, "currency": "currency", "isocurrency": "CNO", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/static/isocurrency/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/static/isocurrency/cancel/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

6.6 swift bic

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/ratan/swift/static/bic/filter | POST | { "fmid": "currency", "senderBic": "CNO", countryCode": "currency", "currency": "CNO", "correspondentBic": "CNO", } | [{ "fmid": "currency", "senderBic": "CNO", countryCode": "currency", "currency": "CNO", "correspondentBic": "CNO", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| add/update | /v1/ratan/swift/static/bic | POST | { "fmid": "currency", "senderBic": "CNO", countryCode": "currency", "currency": "CNO", "correspondentBic": "CNO", } | { "code": 200, "message": "xxx" } | |
| delete | /v1/ratan/swift/static/bic/{id} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/ratan/swift/static/bic/audit/{id} | GET | | [{ "fmid": "currency", "senderBic": "CNO", countryCode": "currency", "currency": "CNO", "correspondentBic": "CNO", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/ratan/swift/static/bic/audit | GET | page={page}&size={size} | [{ "fmid": "currency", "senderBic": "CNO", countryCode": "currency", "currency": "CNO", "correspondentBic": "CNO", "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/ratan/swift/static/bic/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/ratan/swift/static/bic/cancel/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

6.7 accounting ebbs

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/static/accounting/ebbs/filter | POST | { "fmid": "currency", "ebbsBridgeAccount": "CNO", "legalEntity": "currency", "closingEntity": "CNO", "country": "CN", "postingBranch": "02505", "txnTypeCode": "RTN", "txnDrCode": "100, "txnCrCode": "200 } | [{ "fmid": "currency", "ebbsBridgeAccount": "CNO", "legalEntity": "currency", "closingEntity": "CNO", "country": "CN", "postingBranch": "02505", "txnTypeCode": "RTN", "txnDrCode": "100, "txnCrCode": "200, "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| add/update | /v1/static/accounting/ebbs | POST | { "fmid": "currency", "ebbsBridgeAccount": "CNO", "legalEntity": "currency", "closingEntity": "CNO", "country": "CN", "postingBranch": "02505", "txnTypeCode": "RTN", "txnDrCode": "100, "txnCrCode": "200 } | { "code": 200, "message": "xxx" } | |
| delete | /v1/static/accounting/ebbs/{fmid} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/static/accounting/ebbs/audit/{fmid} | GET | | [{ "fmid": "currency", "ebbsBridgeAccount": "CNO", "legalEntity": "currency", "closingEntity": "CNO", "country": "CN", "postingBranch": "02505", "txnTypeCode": "RTN", "txnDrCode": "100, "txnCrCode": "200 "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/static/accounting/ebbs/audit | GET | page={page}&size={size} | [{ "fmid": "currency", "ebbsBridgeAccount": "CNO", "legalEntity": "currency", "closingEntity": "CNO", "country": "CN", "postingBranch": "02505", "txnTypeCode": "RTN", "txnDrCode": "100, "txnCrCode": "200 "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/static/accounting/ebbs/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/static/accounting/ebbs/cancel/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

6.8 currency rounding

**option3:**

6.1 entity on boarding static config

<details>
<summary>Expand Details</summary>

| name | url | http method | request params/body | response body | comment |
| --- | --- | --- | --- | --- | --- |
| query | /v1/static/entity/onboarding/config/filter | POST | { "id": 11111, "fmid": "10008755", "legalEntity": "SCB xxxx" } | [{ "id": 11111, "entityId": "string", "entityName": "string", "contryCode": "string", "currencyCutoffs": [ { "currency": "string", "cutoffTime": "string", "cutoffTimeZone": "string", "cutoffShifter": "string", "cutoffShifterUnit": "string", "queueShifter": "string", "queueShifterUnit": "string", "nettingShifter": "string", "nettingShifterUnit": "string" } ], "currencyMappings": [ { "currency": "string", "isocurrency": "string" } ], "swiftBicList": [ { "senderBic": "string", "countryCode": "string", "currency": "string", "correspondentBic": "string" } ], "accountingEBBSList": [ { "ebbsBridgeAccount": "string", "legalEntity": "string", "closingEntity": "string", "country": "string", "postingBranch": "string", "txnTypeCode": "string", "txnDrCode": "string", "txnCrCode": "string" } ], "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| add | /v1/static/entity/onboarding/config | POST | { "entityId": "string", "entityName": "string", "contryCode": "string", "currencyCutoffs": [ { "currency": "string", "cutoffTime": "string", "cutoffTimeZone": "string", "cutoffShifter": "string", "cutoffShifterUnit": "string", "queueShifter": "string", "queueShifterUnit": "string", "nettingShifter": "string", "nettingShifterUnit": "string" } ], "currencyMappings": [ { "currency": "string", "isocurrency": "string" } ], "swiftBicList": [ { "senderBic": "string", "countryCode": "string", "currency": "string", "correspondentBic": "string" } ], "accountingEBBSList": [ { "ebbsBridgeAccount": "string", "legalEntity": "string", "closingEntity": "string", "country": "string", "postingBranch": "string", "txnTypeCode": "string", "txnDrCode": "string", "txnCrCode": "string" } ] } | { "code": 200, "message": "xxx" } | |
| update | /v1/static/entity/onboarding/config | POST | { "id": 12456, "entityId": "string", "entityName": "string", "contryCode": "string", "currencyCutoffs": [ { "currency": "string", "cutoffTime": "string", "cutoffTimeZone": "string", "cutoffShifter": "string", "cutoffShifterUnit": "string", "queueShifter": "string", "queueShifterUnit": "string", "nettingShifter": "string", "nettingShifterUnit": "string" } ], "currencyMappings": [ { "currency": "string", "isocurrency": "string" } ], "swiftBicList": [ { "senderBic": "string", "countryCode": "string", "currency": "string", "correspondentBic": "string" } ], "accountingEBBSList": [ { "ebbsBridgeAccount": "string", "legalEntity": "string", "closingEntity": "string", "country": "string", "postingBranch": "string", "txnTypeCode": "string", "txnDrCode": "string", "txnCrCode": "string" } ] } | { "code": 200, "message": "xxx" } | |
| delete | /v1/static/entity/onboarding/config/{id} | DELETE | | { "code": 200, "message": "xxx" } | |
| audit | /v1/static/entity/onboarding/config/audit/{id} | GET | | [{ "id":111111, "entityId": "string", "entityName": "string", "contryCode": "string", "currencyCutoffs": [ { "currency": "string", "cutoffTime": "string", "cutoffTimeZone": "string", "cutoffShifter": "string", "cutoffShifterUnit": "string", "queueShifter": "string", "queueShifterUnit": "string", "nettingShifter": "string", "nettingShifterUnit": "string" } ], "currencyMappings": [ { "currency": "string", "isocurrency": "string" } ], "swiftBicList": [ { "senderBic": "string", "countryCode": "string", "currency": "string", "correspondentBic": "string" } ], "accountingEBBSList": [ { "ebbsBridgeAccount": "string", "legalEntity": "string", "closingEntity": "string", "country": "string", "postingBranch": "string", "txnTypeCode": "string", "txnDrCode": "string", "txnCrCode": "string" } ], "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| history | /v1/static/entity/onboarding/config/audit | GET | page={page}&size={size} | [{ "id": 11111, "entityId": "string", "entityName": "string", "contryCode": "string", "currencyCutoffs": [ { "currency": "string", "cutoffTime": "string", "cutoffTimeZone": "string", "cutoffShifter": "string", "cutoffShifterUnit": "string", "queueShifter": "string", "queueShifterUnit": "string", "nettingShifter": "string", "nettingShifterUnit": "string" } ], "currencyMappings": [ { "currency": "string", "isocurrency": "string" } ], "swiftBicList": [ { "senderBic": "string", "countryCode": "string", "currency": "string", "correspondentBic": "string" } ], "accountingEBBSList": [ { "ebbsBridgeAccount": "string", "legalEntity": "string", "closingEntity": "string", "country": "string", "postingBranch": "string", "txnTypeCode": "string", "txnDrCode": "string", "txnCrCode": "string" } ], "dataStatus": "SAVE_CONFIRMED", "makerId": "1593571", "checkerId": "1434424", "createdAt": "2025-12-12T01:18:47.584477Z", "updatedAt": "2025-12-12T01:19:02.642124Z" }] | |
| confirm | /v1/static/entity/onboarding/config/confirm/{id} | POST | | { "code": 200, "message": "xxx" } | |
| cancel | /v1/static/entity/onboarding/config/{id} | POST | | { "code": 200, "message": "xxx" } | |

</details>

# **

**ANCHOR: db**
7****.Database Table ****Design**

| tableName | columnName | columnType | index | comment | desciption |
| --- | --- | --- | --- | --- | --- |
| ratanone.ratan_static__common_metadata_dict | id | bigserial | PK | | save settlementMeans、currency list for FE blotter config. |
| field_value | text | | |
| field_type | text | | |
| created_at | timestamp | | |
| updated_at | timestamp | | |
| ratanone.ratan_static__country_conf | id | bigserial | PK | | save country zoneId for FE blotter config and accounting service |
| code | text | | |
| country | text | | |
| zoneId(use config server, remove the field) | text | | |
| created_at | timestamp | | |
| updated_at | timestamp | | |
| ratanone.ratan_static__entity_conf | id | bigserial | PK | | 1.save entity and country mapping 2. save entity and branch code mapping 3. save fmid and entity mapping (FE 、swift service and accountting service use it, now store in local config file and FE hard code) |
| fmId | text | | |
| booking_entity | text | | |
| country_code | text | | |
| branch_code(use config server, remove the field) | text | | |
| created_at | timestamp | | |
| updated_at | timestamp | PK | |
| ratanone.ratan_static__isocurrency_mapping (use config server, remove this table) | id | bigserial | | | save currency and iso currency mapping (swift service and accountting service use it, now store in local config file) |
| currency | text | | |
| iso_currency | text | | |
| created_at | timestamp | | |
| updated_at | timestamp | | |
| ratanone_swift_service.swift_[mx](http://ratanone.mx/)_generation_condition (use config server, remove this table) | id | bigserial | | | save [mx](http://ratanone.mx/)_generation_condition (swift service use it, now store in local config file) |
| entity | text | | |
| sender | text | | |
| receiver | text | | |
| currency | text | | |
| mtTypes | text | | |
| created_at | timestamp | | |
| updated_at | timestamp | | |
| ratan_static__entity_onboarding_config | id | bigserial | PK | | save the whole entity static config |
| fmId | text | | |
| booking_entity | text | | |
| country_code | text | | |
| country | text | | |
| content | jsonb | gin | |
| sync_status | int | | 0 processing 1 success 2 fail |
| sync_success_count | int | | |
| data_status | text | | |
| maker_id | text | | |
| checker_id | text | | |
| created_at | timestamp | | |
| updated_at | timestamp | | |
| ratan_static__entity_onboarding_config_sync_result | id | bigserial | | | save service sync result |
| config_id | bigint | | |
| service_name | text | | |
| exec_status | bool | | 1 success 0 fail |
| reason | text | | |
| created_at | timestamp | | |
| updated_at | timestamp | | |

# **8.Question**

1.Should the blacklist config or few changes config for backend service support self service?

| service name | table /config | comment |
| --- | --- | --- |
| accouting-service | precious-metal.fmidList precious-metal.currencyList | |
| ratanone_swift_service | swift_static_pm_currency swift_static_udf_strategy swift_static_udf_swf_ls | |
| rantan_mxg_cashflow_adaptor | static_data_cfi_code | |

2.If all blotters about new entity/branch batch support？

# **9. Audit Function**

****

## **update：**

swift-service:

ratanone_swift_service.swift_static_data_correspondent_bic
     ratanone_swift_service.swift_static_data_sender_bic

ratanone_swift_service.swift_[mx](http://ratanone.mx/)_generation_condition（TBC）

audit

accounting-service:

ratan_static__country_conf （time zoneId  application.yml）

audit

static-data-service：

ratanone.ratan_static__cashflow_ebbs_bridge_account

ratanone.ratan_static_cashflow_currency_cut_off

ratanone.ratan_static__cashflow_ebbs_txn_code

ratanone.ratan_static__isocurrency_mapping

ratanone.ratan_static__entity_conf（ branch-code   application.yml STRATEGIC_FM_LIST（TBC fmid →branchCode all）  service-properties）

audit

lifecycle-service:

ratan_cashflow_rounding_config

audit

orchestration-service：

add a service task to filter fmid

code change:

1. management line: CRUD audit from all table
2. trade line: API for application.yml move to table;
3. orchestration-service: refactor to add a service task to filter fmid
4. accounting-service: refactor cron job
5. history data handle