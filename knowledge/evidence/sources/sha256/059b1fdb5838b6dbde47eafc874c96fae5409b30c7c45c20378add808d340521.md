~~CR：CHG0912513~~

~~TSK: CTASK1958540~~

AIG：

# 1.1 Release Work Item:

[Release On 2026-01-24 CR: CHG0909482 BAU - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-01-24+CR%3A+CHG0909482+BAU)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-netting-service | ~~release/v1.7.4~~ release/v1.7.5 | ![image-2026-1-13_13-57-9.png](attachments/image-2026-1-13_13-57-9.png)![image-2026-1-13_13-57-9-1.png](attachments/image-2026-1-13_13-57-9-1.png) ![image-2026-1-12_11-34-50.png](attachments/image-2026-1-12_11-34-50.png) | ![image-2026-1-12_11-33-17.png](attachments/image-2026-1-12_11-33-17.png) | [Pipelines - Run 20260119.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10045715&view=results) | [20260119.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10045715&view=results) | [Pull request 2279540: #11557240 trade confirmation status - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-netting-service/pullrequest/2279540) [Pull request 2317411: Add major version parameter to api call - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-netting-service/pullrequest/2317411) [Pull request 2325040: #11557240 move method out & set default value to empty instead of zero - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-netting-service/pullrequest/2325040?_a=files) | @Fengke Wu |
| 2 | 51358-ratanone-db-repository | develop | | | ~~[Pipelines - Run 20260109.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9931226&view=results)~~ ~~[Pipelines - Run 20260113.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9968258&view=results)~~ ~~[Pipelines - Run 20260114.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9996138&view=results)~~ [Pipelines - Run 20260114.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10000185&view=results) | [Pipelines - Run 20260114.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10000185&view=results) execute package: CHG0912513-20260113.2 rollback package: CHG0912513_Rollback-20260109.5 | [Pull request 2324670: #11737534 update IRS rule - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2324670) [Pull request 2328045: #11737534 update IRS rule - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2328045) | @Chongxuan Li [Story 11112087 Exclude RTRS and LNBR from Pending Another Leg Logic](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11112087) |
| 3 | 51358-ratan-cashflow-lifecycle-service | [release/v3.4.2](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cashflow-lifecycle-service?version=GBrelease/v3.4.2) | ![image-2026-1-12_11-43-59.png](attachments/image-2026-1-12_11-43-59.png) ![image-2026-1-12_11-44-35.png](attachments/image-2026-1-12_11-44-35.png) | ![image-2026-1-12_11-42-24.png](attachments/image-2026-1-12_11-42-24.png) | ~~[Pipelines - Run 20260107.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9886110&view=results)~~ [Pipelines - Run 20260114.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10002092&view=results) | 3.4.2-20260107.4 | [Pull request 2287090: 11292683 Trade Confirmation Status to be updated on Aggregated resultant cashflows - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cashflow-lifecycle-service/pullrequest/2287090) | @Xinmiao Huang |
| 4 | 51358-ratan-cash-settlement-group-management-service | [release/v2.2.3](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service?version=GBrelease/v2.2.3) | ![image-2026-1-12_12-35-51.png](attachments/image-2026-1-12_12-35-51.png)![image-2026-1-12_12-36-7.png](attachments/image-2026-1-12_12-36-7.png) | ![image-2026-1-12_11-50-42.png](attachments/image-2026-1-12_11-50-42.png) | ~~[Pipelines - Run 20260105.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9855762&view=results)~~ [Pipelines - Run 20260114.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10000681&view=results) | 2.2.3-20260105.2 | [Pull request 2287083: 11292683 Trade Confirmation Status to be updated on Aggregated resultant cashflows - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/2287083) | @Xinmiao Huang |
| 5 | 51358-ratan-rule-service | release/v2.4.0 | ![image-2026-1-14_17-9-15.png](attachments/image-2026-1-14_17-9-15.png) | ![image-2026-1-13_10-10-38.png](attachments/image-2026-1-13_10-10-38.png) | ~~[Pipelines - Run 20260113.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9968602&view=results)~~ ~~[Pipelines - Run 20260114.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9996460&view=results)~~ [Pipelines - Run 20260114.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10000942&view=results) | 2.4.0-20260114.3 | [Pull request 2301839: check if trade is affirmed if tradeId is present in netting resultant cashflow - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-rule-service/pullrequest/2301839) [Pull request 2312451: #11292683: bump to 2.4.0 - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-rule-service/pullrequest/2312451) | @Quill Li |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-11-29 | | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | select * from ratanone_rule_service.ratan_rule_engine rre where [rre.id](http://rre.id) = '7251072786288422912'; | ![image-2026-1-12_13-35-40.png](attachments/image-2026-1-12_13-35-40.png) | | |
| 2 | | | | |
| 3 | | | | |