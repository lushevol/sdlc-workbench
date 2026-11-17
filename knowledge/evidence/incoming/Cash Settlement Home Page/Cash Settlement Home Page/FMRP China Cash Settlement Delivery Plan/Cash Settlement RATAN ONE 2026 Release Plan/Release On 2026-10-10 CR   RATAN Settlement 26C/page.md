CR：CHG1090309

TSK:  CTASK2312867

AIG：

# 1.1 Release Work Item:

[Release 16587573 CHG1098371: RATAN Settlement 26C feature](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16587573)

Release brief:

1. Support FMRP Precious Metal payment processing against SWIFT field 26C via strategic fields
2. Upgrade data modelling lib for the strategic fields (most of the services is to update library only)

3. Query enhancement to enable data entitlement on group blotter

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | | | [Pipelines - Run 20261009.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15487216&view=results) Rollback: [Pipelines - Run 20261009.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15487227&view=results) | | [Pull request 3418772: #14562333 add 26C fields and update FMO_Comments field - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/3418772) [Pull request 3473305: #14451094 Add Commodity Product Taxonomy - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/3473305) | @Guiling Wang |
| 2 | 51358-ratan-cash-settlement-netting-service | release/v3.1.8 | ![image-2026-9-29_17-53-37.png](attachments/image-2026-9-29_17-53-37.png)![image-2026-9-29_17-54-1.png](attachments/image-2026-9-29_17-54-1.png) | | [Pipelines - Run 20260929.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15273151&view=results) | [3.1.8-](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15263086&view=results)[20260929.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15273151&view=results) | [Pull request 3386826: Feature/custodian fmid uber - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-netting-service/pullrequest/3386826?_a=files&path=/src/main/java/com/cn/ratan/netting/application/service/NettingService.java) | @Fengke Wu |
| 3 | 51358-ratanone-swift-service | release/v4.6.3 | ![image-2026-9-29_18-47-19.png](attachments/image-2026-9-29_18-47-19.png) | | [Pipelines - Run 20260930.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15309295&view=results)(optional) | 4.6.3-[20260930.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15309295&view=results) | [Pull request 3383209: Feature/precious metals 26C - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-swift-service/pullrequest/3383209?_a=files) | @Fengke Wu |
| 4 | 51358-ratan-cashflow-lifecycle-service | release/v4.2.3 | ![image-2026-9-29_17-54-53.png](attachments/image-2026-9-29_17-54-53.png)![image-2026-9-29_17-55-13.png](attachments/image-2026-9-29_17-55-13.png) | | [Pipelines - Run 20260929.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15276210&view=results) | 4.2.3-[20260929.](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15263332&view=results)5 | [Pull request 3381932: Feature/custodian fmid uber & settlement method update enhancement - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cashflow-lifecycle-service/pullrequest/3381932) | @Fengke Wu |
| 5 | 51358-ratan-cash-settlement-fx-utilization-service | release/v2.0.1 | ![image-2026-9-29_18-21-51.png](attachments/image-2026-9-29_18-21-51.png) ![image-2026-9-29_18-22-12.png](attachments/image-2026-9-29_18-22-12.png) | | [Pipelines - Run 20260929.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15279714&view=results) | 2.0.1-[20260929.](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15263384&view=results)4 | [Pull request 3278315: FXU settlement update include SAVE_CONFIRMED & DELETE_PENDING status for fxu static config - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-fx-utilization-service/pullrequest/3278315?_a=files) | @Fengke Wu |
| 6 | 51358-ratanone-static-data-service | release/v4.4.7 | ![image-2026-9-29_18-7-8.png](attachments/image-2026-9-29_18-7-8.png) | | [Pipelines - Run 20260929.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15279170&view=results) | 4.4.7-20260929.10 | [Pull request 3381844: Feature/fxu static config new api - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/3381844) [Pull request 3423739: #15351030: add clean cache api - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/3423739) | @Fengke Wu @Chen Yang |
| 7 | 1358-ratan-cash-settlement-ssi-stamping-service | release/v4.4.3 | ![image-2026-9-29_17-58-14.png](attachments/image-2026-9-29_17-58-14.png) ![image-2026-9-29_18-8-38.png](attachments/image-2026-9-29_18-8-38.png) | | [Pipelines - Run 20260929.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15275350&view=results) | 4.4.3-[20260929.](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15263413&view=results)4 | [Pull request 3381981: Feature/v4.4.3 upgrade foundation to 8.0.9.1 to add custodian fmid - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-ssi-stamping-service/pullrequest/3381981) | @Fengke Wu |
| 8 | 51358-ratanone-rule-service | release/v2.6.0 | ![image-2026-9-29_18-0-25.png](attachments/image-2026-9-29_18-0-25.png)![image-2026-9-29_18-9-58.png](attachments/image-2026-9-29_18-9-58.png) | | [Pipelines - Run 20261009.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15493551&view=results) [Pipelines - Run 20261009.11](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15498027&view=results)(optional) | 2.6.1-[20261009.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15493551&view=results) 2.6.0-[20261009.11](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15498027&view=results) | [Pull request 3385163: #16407231 and Fact fields - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-rule-service/pullrequest/3385163?_a=files) | @Fengke Wu |
| 9 | 51358-ratan-rule-service | release/v3.2.2 | ![image-2026-9-30_9-32-38.png](attachments/image-2026-9-30_9-32-38.png)![image-2026-9-30_9-33-9.png](attachments/image-2026-9-30_9-33-9.png) | | [Pipelines - Run 20260929.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15277720&view=results) | 3.2.2-[20260929.](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15263543&view=results)5 | [Pull request 3388146: #16420777 add trade field config - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-rule-service/pullrequest/3388146?_a=files) | @Fengke Wu |
| 10 | 51358-ratan-cash-settlement-query-service | release/v4.3.8.4 | ![image-2026-9-29_17-48-29.png](attachments/image-2026-9-29_17-48-29.png) | | [Pipelines - Run 20260929.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15269168&view=results) | 4.3.8.4-20260929.8 | [Pull request 3419603: Feature/group blotter ces - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/3419603) | @Chen Yang |
| 11 | 51358-ratan-cash-settlement-group-management-service | release/v3.2.8.1 | ![image-2026-10-9_16-19-7.png](attachments/image-2026-10-9_16-19-7.png) | | [Pipelines - Run 20261009.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15495676&view=results) | 3.2.8.1-20261009.5 | [Pull request 3421203: Feature/custody stamping - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/3421203) | @Chen Yang |
| 12 | 51358-ratan-cash-settlement-orchestration | release/v4.1.9.1 | ![image-2026-9-29_18-51-37.png](attachments/image-2026-9-29_18-51-37.png) | | [Pipelines - Run 20260929.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15279746&view=results) | 4.1.9.1-20260929.3 | [Pull request 3421030: Feature/416 upgrade foundation - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-orchestration/pullrequest/3421030?_a=files) | @Chen Yang |
| 13 | 51358-ratanone-message-bridge | release/v5.0.7.1 | | | [Pipelines - Run 20260929.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15281580&view=results) | 5.0.7.1-20260929.5 | [Pull request 3421464: Feature/507 upgrade foundation - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-message-bridge/pullrequest/3421464) | @Chen Yang |
| 14 | 51358-mfe-cashflow-blotter | release/1.48.4 | ![image-2026-9-29_18-35-37.png](attachments/image-2026-9-29_18-35-37.png) | | [Pipelines - Run 20260929.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15280321&view=results) | 1.48.4-v1.48.4-20260929.10 | [Pull request 3418818: Feature/16178807 soft block - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter/pullrequest/3418818) | @Guiling Wang |
| 15 | 51358-mfe-cashflow-blotter | release/1.48.5 | ![image-2026-9-30_12-58-12.png](attachments/image-2026-9-30_12-58-12.png) | | [Pipelines - Run 20260930.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15297481&view=results) | 1.48.5-v1.48.5-20260930.4 | [Pull request 3430279: Feature/1010 release - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter/pullrequest/3430279?path=/package.json) | @Guiling Wang |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-10-10 | | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | [uklvapapp590.gdc.standardchartered.com:8868/ratan-cashflow-lifecycle-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cashflow-lifecycle-service/actuator/info) [uklvapapp590.gdc.standardchartered.com:8868/ratanone-swift-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cashflow-lifecycle-service/actuator/info) ratan-cash-settlement-netting-service ratan-cash-settlement-fx-utilization-service ratanone-static-data-service ratan-cash-settlement-ssi-stamping-service ratan-rule-service ratanone-rule-service | | | |
| 2 | SELECT * FROM ratanone_swift_service.swift_static_udf_strategy; SELECT * FROM ratanone_swift_service.swift_static_udf_strategy_fmrp; SELECT * FROM ratanone_swift_service.swift_static_udf_strategy_fmrp_mapping; | | | |
| 3 | | | | |
| | | | | |