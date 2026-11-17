CR：CHG0820869

TSK: [CTASK1760807](https://scbnow01.service-now.com/change_task.do?sys_id=a206952dfb1be214dc16fed08eefdc5d&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3D3f7215e5fb97e214dc16fed08eefdc77%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 9867505 CHG0820869: RATAN Settlement --- Enabling Payment Swift & Accounting Generation](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9867505)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ~~51358-ratanone-swift-service~~ ~~Give up release, move it to 11 Oct~~ | ~~release/v2.1.0~~ | | ~~![image-2025-9-11_11-31-58.png](attachments/image-2025-9-11_11-31-58.png)~~ | ~~[Pipelines - Run 20250910.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8110446&view=results)~~ | ~~2.1.0-[20250910.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8110446&view=results)~~ | ~~[Pull request 1947700: EG\NP\SA entities on board & EG\SA mx configuration - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-swift-service/pullrequest/1947700?_a=files)~~ | ~~@Fengke Wu ~~ |
| 2 | 51358-ratan-cash-settlement-accounting-service Same package: NP in scope only | release/v1.2.5 | ![image-2025-9-10_16-57-33.png](attachments/image-2025-9-10_16-57-33.png) | ![image-2025-9-10_16-49-51.png](attachments/image-2025-9-10_16-49-51.png) | [Pipelines - Run 20250916.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8224042&view=results) | 1.2.5-[ ](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8112240&view=results)[20250916.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8224042&view=results) | [Pull request 1947534: Add EG\NP\SA scheduler - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-accounting-service/pullrequest/1947534?_a=files) | @Fengke Wu |
| 3 | 51358-ratanone-static-data-service Same package: Config 3 new branch codes add Jersey branch code | release/v3.6.6 | ![image-2025-9-10_17-3-11.png](attachments/image-2025-9-10_17-3-11.png) ![image-2025-9-15_14-14-8.png](attachments/image-2025-9-15_14-14-8.png) | ![image-2025-9-15_14-20-29.png](attachments/image-2025-9-15_14-20-29.png) | ~~[Pipelines - Run 20250910.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8112521&view=results)~~ [Pipelines - Run 20250915.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8182571&view=results) | ~~3.6.6-[20250910.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8112521&view=results)~~ 3.6.3-20250915.2 | ~~[Pull request 1948906: #9537668 add EG NP SA branchcode - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/1948906?_a=files)~~ [Branches - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/branchCompare?baseVersion=GBmain&targetVersion=GBrelease/v3.6.3&_a=files) | @Fengke Wu @Chongxuan Li |
| 4 | 51358-ratan-cash-settlement-orchestration Same package: RPL_D removal | release/v3.3.2.3 | | | [Pipelines - Run 20250910.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8103311&view=results) | 3.3.2.3-20250910.2 | [Pull request 1956706: #10236850: remove trade migration and RPL_D node from workflow 1_2 - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-orchestration/pullrequest/1956706?_a=files) | @Chen Yang |
| 5 | 51358-ratan-service-properties Adjustment required: move only NP, keep EG/SA back to legacy flow | master | NA | NA | ~~[Pipelines - Run 20250910.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8103401&view=results)~~ [Pipelines - Run 20250915.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8181993&view=results) | 20250910.2 20250915.2 | Pull request [Pull request 1970574: #9537668: remove NP from razor fmid - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/1970574) | @Chen Yang |
| 6 | 51358-ratanone-db-repository Same package | master | NA | NA | [Pipelines - Run 20250910.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8117722&view=results) | [20250910.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8117722&view=results) | [Pull request 1947952: #9537668 eg np sa entities static conifg - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/1947952?_a=files) | @Fengke Wu |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-09-20 | [cn-release-20250920 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/a89769e7-2258-4b96-94ce-3c62209f908f/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| | Open [https://uklvapapp590.gdc.standardchartered.com:8868/](https://uklvapapp590.gdc.standardchartered.com:8868/)ratan-cash-settlement-orchestration/actuator/info | version is 3.3.2.3-20250910.2 | | |
| | login 590p server and input cd ~/services/ratan-service-properties/config-repo cat application-prod.yml | FMID_LIST should be FM_LIST: 401036553|400991880 | | ![image-2025-9-20_9-35-13.png](attachments/image-2025-9-20_9-35-13.png) |
| | [uklvasapp676.gdc.standardchartered.com:8868/ratanone-static-data-service/actuator/info](https://uklvasapp676.gdc.standardchartered.com:8868/ratanone-static-data-service/actuator/info) | 3.6.3-20250915.2 | | ![image-2025-9-22_8-20-26.png](attachments/image-2025-9-22_8-20-26.png) |
| | [uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-accounting-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-accounting-service/actuator/info) | 1.2.5-20250916.3 | | ![image-2025-9-20_10-1-37.png](attachments/image-2025-9-20_10-1-37.png) |
| | Discover - Elastic | Have "Cron for countryCode" log from NP EG SA local time 6:00am | | |
| | SELECT * FROM RATANONE_SWIFT_SERVICE.SWIFT_STATIC_DATA_SENDER_BIC WHERE K_FMID ='401036553' AND V_BIC='SCBLEGCAXXX' AND V_COUNTRY_CODE='EG'; SELECT * FROM RATANONE_SWIFT_SERVICE.SWIFT_STATIC_DATA_SENDER_BIC WHERE K_FMID ='400007847' AND V_BIC='SCBLNPKAXXX' AND V_COUNTRY_CODE='NP'; SELECT * FROM RATANONE_SWIFT_SERVICE.SWIFT_STATIC_DATA_SENDER_BIC WHERE K_FMID ='400991880' AND V_BIC='SCBLSAR2XXX' AND V_COUNTRY_CODE='SA'; SELECT * FROM RATANONE_SWIFT_SERVICE.SWIFT_STATIC_DATA_CORRESPONDENT_BIC WHERE K_FMID ='401036553' AND V_CURRENCY='EGP' AND V_BIC='SCBLEGCAXXX'; SELECT * FROM RATANONE_SWIFT_SERVICE.SWIFT_STATIC_DATA_CORRESPONDENT_BIC WHERE K_FMID ='400007847' AND V_CURRENCY='NPR' AND V_BIC='SCBLNPKAXXX'; SELECT * FROM RATANONE_SWIFT_SERVICE.SWIFT_STATIC_DATA_CORRESPONDENT_BIC WHERE K_FMID ='400991880' AND V_CURRENCY='SAR' AND V_BIC='SCBLSAR2FMO'; | Have result. | | ![image-2025-9-20_10-2-5.png](attachments/image-2025-9-20_10-2-5.png) ![image-2025-9-20_10-2-26.png](attachments/image-2025-9-20_10-2-26.png) ![image-2025-9-20_10-2-50.png](attachments/image-2025-9-20_10-2-50.png) ![image-2025-9-20_10-3-13.png](attachments/image-2025-9-20_10-3-13.png) ![image-2025-9-20_10-3-40.png](attachments/image-2025-9-20_10-3-40.png) ![image-2025-9-20_10-3-57.png](attachments/image-2025-9-20_10-3-57.png) |
| | SELECT * FROM RATANONE.RATAN_STATIC__CASHFLOW_EBBS_BRIDGE_ACCOUNT WHERE ID IN ('57', '58', '59'); SELECT * FROM RATANONE.RATAN_STATIC__CASHFLOW_EBBS_TXN_CODE WHERE ID IN ('57', '58', '59'); | ![image-2025-9-16_14-50-54.png](attachments/image-2025-9-16_14-50-54.png) ![image-2025-9-16_14-51-22.png](attachments/image-2025-9-16_14-51-22.png) | | ![image-2025-9-20_10-4-15.png](attachments/image-2025-9-20_10-4-15.png) ![image-2025-9-20_10-4-29.png](attachments/image-2025-9-20_10-4-29.png) |