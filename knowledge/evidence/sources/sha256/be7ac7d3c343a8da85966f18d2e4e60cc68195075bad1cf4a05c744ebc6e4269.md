CR：CHG1066352

TSK: [CTASK2265834](https://scbnow01.service-now.com/change_task.do?sys_id=f17a40a5fb8bc710b959fd284eefdcea&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3D041a8c6dfb4bc710b959fd284eefdc84%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 15957898 CHG1066352: RATAN Settlement enhancement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15957898)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | NA | NA | data: [Pipelines - Run 20260916.11](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14983945&view=results) Index: [Pipelines - Run 20260916.12](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14984018&view=results) | | [Pull request 3354950: Feature/cn May 24th - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/3354950?path=/CRs/CHG1066352/settlement_method_static_data.sql) | @Chen Yang |
| 2 | 51358-ratanone-static-data-service | release/v4.4.6 | ![image-2026-9-16_17-24-4.png](attachments/image-2026-9-16_17-24-4.png) | | [Pipelines - Run 20260916.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14974195&view=results) | 4.4.6-20260916.3 | [Pull request 3339329: #15765034: change fxu static data to a generic static data - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/3339329) | @Chen Yang |
| 3 | 51358-ratan-cash-settlement-group-management-service | release/v3.2.8 | ![image-2026-9-15_19-47-59.png](attachments/image-2026-9-15_19-47-59.png) | ![image-2026-9-15_19-52-51.png](attachments/image-2026-9-15_19-52-51.png) | [Pipelines - Run 20260915.7](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14958655&view=results) | 3.2.8-20260915.7 | [Pull request 3337819: #15765034: uber message CCIL identify - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/3337819) | @Chen Yang |
| 4 | 51358-ratan-cash-settlement-ssi-stamping-service | release/v4.2.3.1 | ![image-2026-9-15_19-57-7.png](attachments/image-2026-9-15_19-57-7.png) | | [Pipelines - Run 20260915.12](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14958752&view=results) | 4.2.3.1-20260915.12 | [Pull request 3339290: #15765034: change static data fxu api - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-ssi-stamping-service/pullrequest/3339290) | @Chen Yang |
| 5 | ~~51358-ratan-cashflow-lifecycle-service~~ | ~~release/v4.1.8~~ | ~~![image-2026-9-15_19-57-48.png](attachments/image-2026-9-15_19-57-48.png)~~ | | ~~[Pipelines - Run 20260916.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14987455&view=results)~~ | ~~4.1.8-[20260916.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14987455&view=results)~~ | [Pull request 3351361: #15765034: fix vulnerability - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cashflow-lifecycle-service/pullrequest/3351361) [Pull request 3361571: #15765034 reverse rebook enhancement - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cashflow-lifecycle-service/pullrequest/3361571?_a=files) | @Chen Yang @Fengke Wu |
| 6 | 51358-ratan-cashflow-lifecycle-service | release/v4.2.1 | | | [Pipelines - Run 20260916.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14985832&view=results)（BAU） | 4.2.1-[20260916.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14985832&view=results) | | |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-09-19 | [cn-release-20260919 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/ee85baae-cce7-4273-afae-f40981ee93b6/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| | Check the link [uklvapapp590.gdc.standardchartered.com:8868/ratan-mxg-cashflow-adaptor/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-mxg-cashflow-adaptor/actuator/info) | Version should be 3.0.1.2-20260831.7 | | |
| | Check the link [uklvapapp590.gdc.standardchartered.com:8868/ratan-cashflow-lifecycle-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cashflow-lifecycle-service/actuator/info) | Version should be 4.1.8-xxx or 4.2.1-xxx | | |
| | select count(1) from ratanone.ratan_settlement_method_config where settlement_method ='UTIL'; | 72 | | |
| | select count(1) from ratanone.ratan_settlement_method_config where settlement_method ='CCIL'; | 57 | | |
| | check link [https://uklvapapp590.gdc.standardchartered.com:8868/ratanone-static-data-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratanone-static-data-service/actuator/info) | Version should be 4.4.6-20260916.3 | | |
| | check link [https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-group-management-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-group-management-service/actuator/info) | Version should be 3.2.8-20260915.7 | | |
| | check link [https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-ssi-stamping-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-ssi-stamping-service/actuator/info) | Version should be 4.2.3.1-20260915.12 | | |
| | | | | |