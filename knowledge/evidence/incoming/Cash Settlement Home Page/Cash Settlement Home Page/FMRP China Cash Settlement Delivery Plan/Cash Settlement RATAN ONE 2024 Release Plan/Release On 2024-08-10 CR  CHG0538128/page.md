CR：CHG0538128

AIG：

# 1.1 Release Work Item:

[Release 5026063: CHG0538128 CN Go live Aug 10th - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5026063)

# 1.2 Packages

| | Service | Branch | Hashicorp Enabled | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-group-management-service | [release/v2.0.1](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service?version=GBrelease/v2.0.1) | Yes | [Pipelines - Run 20240808.3 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2899419&view=results) | 2.0.1-20240808.3 | @Xinmiao Huang |
| 2 | 51358-ratan-mxg-cashflow-adaptor | release/v1.7.2 | Yes | [Pipelines - Run 20240802.3 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2833414&view=results) | 1.7.2-20240802.3 | @Chen Yang |
| 3 | 51358-ratan-rule-service | release/2.1.0 | Yes | [Pipelines - Run 20240723.1 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2712287&view=results) | 2.1.0-20240723.1 | @Xinmiao Huang |
| 4 | 51358-ratan-cash-settlement-orchestration | release/v3.1.1 | Yes | [Pipelines - Run 20240806.1 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2867722&view=results) | 3.1.1-20240806.1 | @Xinmiao Huang |
| 5 | 51358-ratan-exception-platform | release/v3.1.0 | Yes | [Pipelines - Run 20240806.1 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2867793&view=results) | 3.1.0-20240806.1 | @Xinmiao Huang |
| 6 | 51358-ratan-cash-settlement-query-service | release/v2.3.2 | Yes | [Pipelines - Run 20240808.2 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2899565&view=results) | 2.3.2-20240808.2 | @Xinmiao Huang |
| 7 | 51358-mfe-cashflow-blotter | release/production | N/A | [Pipelines - Run 20240806.6 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2870398&view=results) | 1.7.0-production-20240806.6 | @Shuai Lu |
| 8 | 51358-ratanone-db-repository | develop | N/A | | CHG0563571-20240904.3 CHG0563571_Rollback-20240902.5 [Optional Step] CHG0563571_1-20240902.4 | @Chen Yang |
| 9 | 51358-ratanone-rule-service | release/v1.2.4 | Yes | [Pipelines - Run 20240807.2 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2882041&view=results) | 1.2.4-20240807.2 | @William Zhang |

| | Service | Branch | Hashicorp Enabled | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | NA | execute: [Pipelines - Run 20240802.1 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2826680&view=results) rollback: [Pipelines - Run 20240802.2 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2826905&view=results) | execute: CHG0538128-20240802.1 rollback: CHG0538128_Rollback-20240802.2 | @Chongxuan Li |
| 2 | rules change | | | db: | | @Chongxuan Li |

# 1.3 Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2024-08-10 | [cn-release-20240810 - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_queries/query/d4ec79e8-2621-4c5f-a18c-d16525a068db/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** **** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |