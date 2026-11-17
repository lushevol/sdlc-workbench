CR:  CHG0834341

TSK: CTASK1789241

AIG：

# 1.1 Release Work Item:

[Release 10507713 CHG0834341: RATAN Tranche 3 Biz Go-Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10507713)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | PR LINK | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-service-properties | master | N/A | | [Pull request 2028688: #10645153 update for tranche3 business go live - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2028688?_a=files) | [Pipelines - Run 20250929.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8429727&view=results) | 20250929.2 | @Chongxuan Li |
| 2 | 51358-ratan-service-properties_tranche3_only | master | | | [Pull request 2033420: #10645153 rollback EG and SA once UVT not success - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2033420?_a=files) | [Pipelines - Run 20250930.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8451342&view=results) | 20250930.5 | @Chongxuan Li |
| 3 | 51358-ratan-cash-settlement-group-management-service | release/v2.1.12 | ![image-2025-9-25_18-32-50.png](attachments/image-2025-9-25_18-32-50.png) | ![image-2025-9-25_18-33-7.png](attachments/image-2025-9-25_18-33-7.png) | [Pull request 1796386: #9541548 rm validate status - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/1796386?_a=files) [Pull request 1879037: #9540240 [FMRP 6.0] MO Validation Remodel - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/1879037?_a=files) | [Pipelines - Run 20250924.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8359951&view=results) | 2.1.12-20250924.4 | @Xinmiao Huang @Fengke Wu |
| 4 | 51358-ratanone-swift-service | ISO change | | | | | | |
| 5 | 51358-ratanone-db-repository | main | | | [Pull request 2028533: #9905158 remove cutoff datas for SG - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2028533?_a=files) | [Pipelines - Run 20250929.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8429566&view=results) | execute: CHG0834341_20251011-20250929.2.zip rollback: CHG0834341_20251011_Rollback-20250929.3.zip | @Chongxuan Li |
| 6 | 51358-ratanone-command | main | | | [Pull request 1950803: #9671664 add EBBS UVT commands for EG - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command/pullrequest/1950803?_a=files) | [Pipelines - Run 20250929.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8436046&view=results) | CHG0834341-20250922.1 | @Chongxuan Li |
| 7 | 51358-ratanone-service_restartSett400Services | main | NA | NA | | [Pipelines - Run 20250929.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8436017&view=results) | NA | @Zeyu Zhou |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-10-11 | [cn-release-20251011 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/d390068c-d819-4bb7-bd9d-7db20f8e20e1/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | login 590p server and input cd ~/services/ratan-service-properties/config-repo cat application-prod.yml | ![image-2025-9-29_11-35-24.png](attachments/image-2025-9-29_11-35-24.png) | PASS | ![image-2025-10-11_9-38-5.png](attachments/image-2025-10-11_9-38-5.png) |
| 2 | select * from ratanone.ratan_static_cashflow_currency_cut_off rsccco where [rsccco.id](http://rsccco.id) in ('july6-d3e7-41ee-ae84-91cac4120834','july6-d3e7-41ee-ae84-91cac4120994','july6-d3e7-41ee-ae84-91cac3115954','july6-d3e7-41ee-ae84-91cac3116065'); | no records | PASS | ![image-2025-10-11_9-32-7.png](attachments/image-2025-10-11_9-32-7.png) |
| | | | | |
| | | | | |