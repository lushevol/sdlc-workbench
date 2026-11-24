CR：CHG0668173

TSK:  CTASK1469670

AIG：

# 1.1 Release Work Item:

[Release 6993485 CHG0668173: RATAN Settlement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6993485)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-swift-service | release/v1.1.6 | ![image2025-2-20_17-44-52.png](attachments/image2025-2-20_17-44-52.png) | ![image2025-2-20_17-45-7.png](attachments/image2025-2-20_17-45-7.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5101112&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5101112&view=results) | 1.1.6-20250220.5 | @Mingyang Zhong |
| 2 | 51358-ratan-cash-settlement-ssi-stamping-service | release/v2.4.4.1 | ![image-2025-2-26_10-50-20.png](attachments/image-2025-2-26_10-50-20.png) | ![image-2025-2-26_10-50-48.png](attachments/image-2025-2-26_10-50-48.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5172056&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5172056&view=results) | 2.4.4.1-20250226.2 | @Mingyang Zhong |
| 3 | 51358-ratan-cashflow-lifecycle-service | release/v3.0.5 | ![image-2025-2-26_19-54-47.png](attachments/image-2025-2-26_19-54-47.png) | ![image-2025-2-26_19-55-15.png](attachments/image-2025-2-26_19-55-15.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5181505&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5181505&view=results) | 3.0.5-20250226.4 | @Mingyang Zhong |
| 4 | 51358-mfe-cashflow-blotter | [release/v1.15.0](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter?version=GBrelease/v1.15.0) | ![Screenshot (2210).png](attachments/Screenshot (2210).png) | ![Screenshot (2212).png](attachments/Screenshot (2212).png) | [Pipelines - Run 20250225.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5152940&view=results) | 1.15.0-v1.15.0-20250225.2 | @Guiling Wang @Shuai Lu |
| 5 | 51358-ratanone-db-repository | develop | NA | NA | [Pipelines - Run 20250226.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5182310&view=results) | CHG0668173-20250226.3 CHG0668173_Rollback-20250226.4 ratanone-db-repository-20250226.5.zip | @Xinmiao Huang |

**EXPAND: Appendix**

## Shell Command

| Shell Comment | Execute Server | Command |
| --- | --- | --- |
| | | |
| | | |
| | | |
| | | |

**EXPAND_END**

# 1.3 Release PT

### Dashboard Auto Refresh PT

[https://confluence.global.standardchartered.com/x/b54Ywg](https://confluence.global.standardchartered.com/x/b54Ywg)

### Cashflow Blotter Page Size PT

[https://confluence.global.standardchartered.com/x/V123wQ](https://confluence.global.standardchartered.com/x/V123wQ)

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-03-01 | [cn-release-20250301 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/8b1eb57f-8d0f-4c82-8363-f2f4497e207c/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff:** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Check DB repo has been executed successfully | totally 24 records | **PASS** | ![image-2025-3-1_9-30-28.png](attachments/image-2025-3-1_9-30-28.png) |
| 2 | check backend service package version | same as above | **PASS** | ![image-2025-3-1_9-44-27.png](attachments/image-2025-3-1_9-44-27.png) ![image-2025-3-1_9-44-32.png](attachments/image-2025-3-1_9-44-32.png) |
| 3 | - Open Cashflow Blotter tile - Hover on the icon. - Click on "set to 5000" option. - Click on "Load Next 5000" button | - has setting icon on the right of "Load Next 1000" - popover a "set to 5000" section - auto refresh the page with 5000 size - load next page with size 5000 | **PASS** | ![image-2025-3-3_9-23-19.png](attachments/image-2025-3-3_9-23-19.png) ![image-2025-3-3_9-24-33.png](attachments/image-2025-3-3_9-24-33.png) |
| 4 | - Open Cashflow Dashboard tile, wait for 2 mins | - dashboard refresh every 2 mins. | **PASS** | ![image-2025-3-3_9-24-42.png](attachments/image-2025-3-3_9-24-42.png) |
| 5 | - quick search by "currency" + "amount Range" - search by Customer filter | "currency" + "amount Range" container should be cleared | **PASS** | ![Screenshot (2263).png](attachments/Screenshot (2263).png) ![Screenshot (2261).png](attachments/Screenshot (2261).png) |