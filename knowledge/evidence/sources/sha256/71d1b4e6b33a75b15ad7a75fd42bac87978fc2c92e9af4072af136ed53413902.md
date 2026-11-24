CR: CHG0821842

TSK: [CTASK1762737](https://scbnow01.service-now.com/change_task.do?sys_id=c08f3179fb9f26d45054f8225eefdc6c&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3D43eebd31fb9f26d45054f8225eefdc21%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 9880774 CHG0821842: Tranche3 Technical Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9880774)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Pull Request | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | main/feature/cn-golive-27-Sep-2025 | NA | NA | [Pipelines - Run 20250922.7](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8307835&view=results) | [Pull request 1989619: #9905158 tranche3 static data - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/1989619) [Pull request 2000846: #9905158 tranche3 static data for nostro - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2000846) | install: CHG0821842- 20250922.6 rollback: CHG0821842_Rollback-20250922.3 | @Chongxuan Li |
| 2 | 51358-ratan-service-properties | master | N/A | N/A | [Pipelines - Run 20250918.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8251608&view=results) | [Pull request 1986783: #10451390 add CPT configuration for tranche3 - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/1986783) | 20250918.1 | @Chongxuan Li |
| 3 | 51358-mfe-cashflow-blotter | release/v1.38.3 | ![image-2025-9-18_12-28-7.png](attachments/image-2025-9-18_12-28-7.png)![image-2025-9-18_12-28-29.png](attachments/image-2025-9-18_12-28-29.png) ![image-2025-9-18_12-28-57.png](attachments/image-2025-9-18_12-28-57.png) | ![image-2025-9-18_11-50-48.png](attachments/image-2025-9-18_11-50-48.png) | [Pipelines - Run 20250922.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8304700&view=results) | [Pull request 1989725: Entity setup for tranche3 - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter/pullrequest/1989725?path=/src/Cashflow_CN/Main/config/ratanConfig/local/BookingEntity.ts) | 1.38.3-v1.38.3-20250922.5 | @Guiling Wang |
| 4 | 51358-ratan-cash-settlement-accounting-service | release/v1.2.6 | ![image-2025-9-23_13-13-26.png](attachments/image-2025-9-23_13-13-26.png) | ![image-2025-9-23_13-13-41.png](attachments/image-2025-9-23_13-13-41.png) | [Pipelines - Run 20250923.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8327668&view=results) | [Pull request 1982015: #9731554 add JERSEY fmid for accounting - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-accounting-service/pullrequest/1982015) [Pull request 1985266: #9731554 fix vulnerability - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-accounting-service/pullrequest/1985266?_a=files) [Pull request 1986730: #9731554 fix vulnerability - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-accounting-service/pullrequest/1986730?_a=files) | 1.2.6-20250923.2 | @Chongxuan Li |
| 5 | 51358-ratan-cash-settlement-lms-service | release/v2.2.2 | ![image-2025-9-23_13-46-56.png](attachments/image-2025-9-23_13-46-56.png) | ![image-2025-9-23_13-46-30.png](attachments/image-2025-9-23_13-46-30.png) | [Pipelines - Run 20250923.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8326048&view=results) | [Pull request 1967581: #9920605 upgrade package - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-lms-service/pullrequest/1967581) [Pull request 1875170: #9920605 tranche3 filter JERSEY - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-lms-service/pullrequest/1875170?_a=files) [Pull request 2004985: #9920605 add UT - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-lms-service/pullrequest/2004985?_a=files) | 2.2.2-[20250923.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8326048&view=results) | @Chongxuan Li |
| 6 | 51358-ratanone-service_restartSettOrchServices | master | NA | NA | [Pipelines - Run 20250924.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8356655&view=results) | | | @Zeyu Zhou |
| 7 | 51358-RATAN-W-ControlM-RAT | JE jobs | | | [Pipelines - Run 20250923.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8330548&view=results) | | | @Jie Cai |
| 8 | 51358-ratanone-command | main | | | [Pipelines - Run 20250922.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8321480&view=results) | | CHG0834341-20250922.1 | @Chongxuan Li |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-09-27 | [cn-release-20250927 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/d696d1bd-dd1b-4d91-a0d7-df3bb01e6286/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | select * from ratan_cash_accounting_service.ratan_accounting_aspire_execution raae where raae .id = '7316514119793098751'; select * from ratanone.ratan_static__cashflow_ebbs_txn_code where id = '60'; select * from ratanone.ratan_static__cashflow_ebbs_bridge_account where id = '60'; | ![image-2025-9-23_15-23-24.png](attachments/image-2025-9-23_15-23-24.png) ![image-2025-9-23_15-23-38.png](attachments/image-2025-9-23_15-23-38.png) ![image-2025-9-23_15-23-49.png](attachments/image-2025-9-23_15-23-49.png) | | ![image-2025-9-27_9-45-3.png](attachments/image-2025-9-27_9-45-3.png) ![image-2025-9-27_9-45-25.png](attachments/image-2025-9-27_9-45-25.png) ![image-2025-9-27_9-44-36.png](attachments/image-2025-9-27_9-44-36.png) |
| 2 | select * from ratanone_swift_service.swift_static_data_correspondent_bic where k_fmid in ('400910415', '400516442', '400516443'); select * from ratanone_swift_service.swift_static_data_sender_bic where k_fmid in ('400910415'); | ![image-2025-9-23_15-24-43.png](attachments/image-2025-9-23_15-24-43.png) ![image-2025-9-23_15-24-52.png](attachments/image-2025-9-23_15-24-52.png) | | ![image-2025-9-27_9-44-9.png](attachments/image-2025-9-27_9-44-9.png) ![image-2025-9-27_9-44-0.png](attachments/image-2025-9-27_9-44-0.png) |
| 3 | select * from ratanone_rule_service.ratan_rule_engine rre where [rre.id](http://rre.id) in ('7374420229233111040', '7369258354199584768'); | ![image-2025-9-23_15-25-7.png](attachments/image-2025-9-23_15-25-7.png) | | ![image-2025-9-27_9-47-33.png](attachments/image-2025-9-27_9-47-33.png) |
| 4 | select count(1) from ratanone.nostro_manipulation_audit nma where nostro_id like 'tranche3%'; select count(1) from ratanone.ratan_static__cashflow_nostro where id like 'tranche3%'; | ![image-2025-9-23_15-25-27.png](attachments/image-2025-9-23_15-25-27.png) ![image-2025-9-23_15-25-39.png](attachments/image-2025-9-23_15-25-39.png) | | ![image-2025-9-27_9-43-15.png](attachments/image-2025-9-27_9-43-15.png) ![image-2025-9-27_9-43-35.png](attachments/image-2025-9-27_9-43-35.png) |
| 5 | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9905654](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9905654) 1. Login to PTP, open cashflow blotter. 2. Click on booking entity, will see the dropdown list. | Expect dropdown list contains tranche3 new entities | | ![image-2025-9-27_9-43-44.png](attachments/image-2025-9-27_9-43-44.png) |
| 6 | login 590p server and input cd ~/services/ratan-service-properties/config-repo cat application-prod.yml | ![image-2025-9-25_10-1-3.png](attachments/image-2025-9-25_10-1-3.png) | | ![image-2025-9-27_9-30-3.png](attachments/image-2025-9-27_9-30-3.png) |
| 7 | [uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-accounting-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-accounting-service/actuator/info) | 1.2.6-20250923.2 | | ![image-2025-9-27_9-47-5.png](attachments/image-2025-9-27_9-47-5.png) |
| 8 | [uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-lms-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-lms-service/actuator/info) | 2.2.2-[20250923.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8326048&view=results) | | ![image-2025-9-27_9-47-23.png](attachments/image-2025-9-27_9-47-23.png) |
| 9 | Control-M | ![image-2025-9-27_9-49-18.png](attachments/image-2025-9-27_9-49-18.png)![image-2025-9-27_9-50-0.png](attachments/image-2025-9-27_9-50-0.png)![image-2025-9-27_9-50-28.png](attachments/image-2025-9-27_9-50-28.png) | | |