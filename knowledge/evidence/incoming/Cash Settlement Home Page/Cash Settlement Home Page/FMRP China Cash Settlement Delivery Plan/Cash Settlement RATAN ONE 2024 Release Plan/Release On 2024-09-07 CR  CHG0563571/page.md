CR：CHG0563571

AIG：

# 1.1 Release Work Item:

[Release 5382929: CN Release On 2024-09-07 CR: CHG0563571 - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5382929)

# 1.2 Packages

| | Service | Branch | Hashicorp Enabled | Vulnerability Report Summery Screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-orchestration | release/v3.1.2 | true | ![image2024-8-29_11-2-1.png](attachments/image2024-8-29_11-2-1.png) | [Pipelines - Run 20240828.2 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3109677&view=results) | 3.1.2-20240828.2 | @Chen Yang |
| 2 | 51358-mfe-cashflow-blotter | release/production | NA | ![image2024-8-30_7-49-40.png](attachments/image2024-8-30_7-49-40.png) | [Pipelines - Run 20240829.6 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3132218&view=results) | 1.8.3-production-20240829.6 | @Shuai Lu |
| 3 | 51358-ratan-cashflow-lifecycle-service | release/v1.2.7 | true | ![image2024-9-4_15-2-9.png](attachments/image2024-9-4_15-2-9.png) ![image2024-9-4_15-1-4.png](attachments/image2024-9-4_15-1-4.png) | [Pipelines - Run 20240904.4 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3200406&view=results) | 1.2.7-20240904.4 | @Chongxuan Li |
| 4 | 51358-ratan-cash-settlement-accounting-service | release/v1.0.4 | true | ![image2024-8-28_17-2-15.png](attachments/image2024-8-28_17-2-15.png)![image2024-8-28_17-11-28.png](attachments/image2024-8-28_17-11-28.png) | [Pipelines - Run 20240828.5 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3116367&view=results) | 1.0.4-20240828.5 | @Chongxuan Li |
| 5 | 51358-ratan-cash-settlement-query-service | release/v2.3.4 | true | ![image2024-8-30_10-33-20.png](attachments/image2024-8-30_10-33-20.png) ![image2024-8-30_10-34-28.png](attachments/image2024-8-30_10-34-28.png) | [Pipelines - Run 20240830.1 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3142674&view=results) | 2.3.4-20240830.1 | @Song Wan |
| 6 | 51358-ratanone-db-repository | | | | | | @Chen Yang |
| 7 | 51358-ratanone-swift-service | release/v1.0.3 | Yes | ![image2024-8-28_11-38-27.png](attachments/image2024-8-28_11-38-27.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3086987&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3086987&view=results) | 1.0.3-20240826.2 | @Mingyang Zhong |

| | Service | Branch | Hashicorp Enabled | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | NA | execute: CHG0563571-20240902.3 rollback: CHG0563571_Rollback-20240902.5 [Optional Step] CHG0563571_1-20240902.4 | execute: rollback: | @Chen Yang |

# 1.3 Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [x] DM | Test Progress - [x] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2024-09-07 | [cn-release-20240907 - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_queries/query/4329c1e0-9653-4622-bcc4-4b27cc20c482/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |