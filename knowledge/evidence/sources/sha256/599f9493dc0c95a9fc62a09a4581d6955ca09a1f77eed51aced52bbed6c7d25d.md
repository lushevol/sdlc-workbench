CR：CHG0807461

TSK: CTASK1731737

AIG：

# 1.1 Release Work Item:

[Release 9613830 CHG0807461: RATAN Settlement Tranche 2 Business Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9613830)

No Go Decision : [Release 9733516 CHG0807461: RATAN Settlement Tranche 2 Business Go Live --- No Go Decision](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9733516)

# 1.2 Packages

8.1-8.8 ： Murex publish VD 8.11/12 payments

8.4-8.8: Recon on SSI @Chen Yang @Kuan Wang

8.10:

**Go decision:**

1. Config change to open the gate
2. Accounting to apply “allow-insufficient-fund=Y”
3. ~~Swift Service to close Murex flow on MU, ZA, UAE~~
4. DB repo for making currency as empty in below table for entity 5 Dubai, to be confirmed with @Wayne Wang
5. User is supposed to perform below action. Rundeck for status movement as backup [@Zhou, Zeyu](mailto:Zeyu.Zhou@sc.com) [@Yang3, Chen](mailto:Chen.Yang3@sc.com)
6. MB config/Command to publish EBBS feed for EB/NP @Chongxuan Li

**Potential rollback:**

Create another WI and roll back the service property to enable CPT back, [@Zhou, Zeyu](mailto:Zeyu.Zhou@sc.com) [@Yang3, Chen](mailto:Chen.Yang3@sc.com)

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-service-properties | master | N/A | N/A | [Pipelines - Run 20250801.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7464230&view=results) ( Optional )No go [Pipelines - Run 20250801.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7473126&view=results) | 20250801.2 ( Optional )No go 20250801.5 | @Chen Yang |
| 2 | 51358-ratan-cash-settlement-accounting-service | release/v1.2.2.1 | ![image-2025-8-4_10-35-4.png](attachments/image-2025-8-4_10-35-4.png) | ![image-2025-8-4_10-35-17.png](attachments/image-2025-8-4_10-35-17.png) | [Pipelines - Run 20250731.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7449625&view=results) | 1.2.2.1-20250731.3 | @Chongxuan Li |
| 3 | ~~51358-ratanone-swift-service~~ | ~~release/v2.0.5~~ | ![image-2025-7-28_14-17-51.png](attachments/image-2025-7-28_14-17-51.png) | ![image-2025-7-28_14-17-21.png](attachments/image-2025-7-28_14-17-21.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7373703&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7373703&view=results) | 2.0.5-20250728.5 | @Mingyang Zhong |
| 4 | [51358-ratanone-service](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible?path=/&version=GBfeature/cn-20250322-release-command)_stopServcies | master | NA | NA | [Pipelines - Run 20250805.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7517613&view=results) No-GO: [Pipelines - Run 20250806.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7545028&view=results) | | @Zeyu Zhou |
| 5 | [51358-ratanone-service](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible?path=/&version=GBfeature/cn-20250322-release-command)_restartServices | master | NA | NA | [Pipelines - Run 20250805.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7517811&view=results) No-GO: [Pipelines - Run 20250806.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7545069&view=results) | | |
| 6 | 51358-ratanone-service_restartSettOrchServices | master | NA | NA | [Pipelines - Run 20250805.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7517883&view=results) No-GO( Rename: restart400Services) : [Pipelines - Run 20250806.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7544526&view=results) | | @Zeyu Zhou |
| 7 | 51358-ratanone-command | main / CHG0807461-20250804.2 | | | [Pipelines - Run 20250804.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7501596&view=results) | CHG0807461-20250804.2 | @Chongxuan Li |
| 8 | 51358-ratanone-db-repository | develop | NA | NA | [Pipelines - Run 20250801.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7474724&view=results) | CHG0807461-20250801.6 CHG0807461_Rollback-20250801.7 | @Chen Yang |
| 9 | 51358-mfe-cashflow-blotter | [release/v1.36.1](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter?version=GBrelease/v1.36.1) | ![image-2025-8-5_20-24-59.png](attachments/image-2025-8-5_20-24-59.png) | ![image-2025-8-5_20-24-43.png](attachments/image-2025-8-5_20-24-43.png) | [Pipelines - Run 20250805.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7524511&view=results) | | @Shuai Lu @Guiling Wang |
| 10 | 51358-mfe-ratan-container | [release/v1.7.41.1](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-ratan-container?version=GBrelease/v1.7.41.1) | ![image-2025-8-5_20-23-53.png](attachments/image-2025-8-5_20-23-53.png) | ![image-2025-8-5_20-23-30.png](attachments/image-2025-8-5_20-23-30.png) | [Pipelines - Run 20250801.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7480003&view=results) | | @Shuai Lu @Guiling Wang |

**EXPAND: Appendix**

## Shell Command

| Shell Comment | Execute Server | Command |
| --- | --- | --- |
| | | |
| | | |
| | | |
| | | |

**EXPAND_END**

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | | [cn-release-20250809 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/2bafbb9a-ffae-416a-862e-e2bf4b41d4ea/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** **** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | select v_currency from ratanone_swift_service.swift_static_data_correspondent_bic where k_fmid ='5'; | Empty | | |
| 2 | select count(1) from ratanone.ratan_bridge_flow where route_id in (98,99) | 4 | | |
| 3 | [Story 9659106 [Frontend] Quick Search supports free typing ccy and taxonomy](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9659106) 1. Login to PTP, open cashflow blotter. 2. Type ccy and taxonomy on Quick Search. | Except can free typing ccy and taxonomy on quick search | PASS | ![image-2025-8-10_14-31-2.png](attachments/image-2025-8-10_14-31-2.png) |
| 4 | check log for NP EBBS integration testing | | PASS | ![image-2025-8-10_15-0-12.png](attachments/image-2025-8-10_15-0-12.png) |