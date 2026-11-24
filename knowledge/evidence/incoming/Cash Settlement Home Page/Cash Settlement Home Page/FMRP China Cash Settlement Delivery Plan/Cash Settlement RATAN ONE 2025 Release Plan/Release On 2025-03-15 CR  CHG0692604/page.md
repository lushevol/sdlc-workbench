CR：CHG0692604

TSK:  CTASK1486337

AIG：

# 1.1 Release Work Item:

[Release 7496927 CHG0692604: RATAN Settlement Enhancement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7496927)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Rollback Info | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-swift-service | release/v1.1.7 | ![image-2025-3-13_15-14-38.png](attachments/image-2025-3-13_15-14-38.png) | ![image-2025-3-13_15-15-14.png](attachments/image-2025-3-13_15-15-14.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5377732&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5377732&view=results) | 1.1.7-20250313.5 | | @Mingyang Zhong |
| 2 | 51358-ratan-cash-settlement-query-service | release/v3.0.5 | ![image-2025-3-11_11-59-45.png](attachments/image-2025-3-11_11-59-45.png) | ![image-2025-3-11_12-0-7.png](attachments/image-2025-3-11_12-0-7.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5292231&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5292231&view=results) | 3.0.5-20250306.3 | | @Xinmiao Huang |
| 3 | ~~51358-ratan-cash-settlement-netting-service~~ | ~~release/v1.5.1~~ ~~release/v1.4.7~~ | ~~![image-2025-3-11_16-49-53.png](attachments/image-2025-3-11_16-49-53.png)~~ | ~~![image-2025-3-11_16-47-31.png](attachments/image-2025-3-11_16-47-31.png)~~ | ~~[Pipelines - Run 20250311.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5346557&view=results)~~ | ~~1.4.7-20250311.2~~ | ~~[Pipelines - Run 20250124.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=4749550&view=results)~~ ~~20250124.2~~ ~~1.4.6-20250124.2~~ | ~~@Xinmiao Huang ~~ |
| 4 | 51358-ratanone-ansible | main | NA | NA | [Pipelines - Run 20250310.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5327303&view=results) | | | @Jie Cai |

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

| | Item | Link |
| --- | --- | --- |
| 1 | PT testing (total: 9725 payment feeding) | [RATAN One Performance Test For Release On Mar 15 2025 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+Performance+Test+For+Release+On+Mar+15+2025) |
| 2 | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-03-15 | [cn-release-20250315 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/c0c961d2-4c36-48ca-bc19-ac37e3d803a5/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff:** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Check Eureka for Application readiness and package version | 6 live with the correct package name above | **PASS** | ![image-2025-3-15_9-32-14.png](attachments/image-2025-3-15_9-32-14.png) ![image-2025-3-15_9-38-45.png](attachments/image-2025-3-15_9-38-45.png) ![image-2025-3-15_9-32-44.png](attachments/image-2025-3-15_9-32-44.png) ![image-2025-3-15_9-38-7.png](attachments/image-2025-3-15_9-38-7.png) |
| 2 | Check ERROR logs from Kibana | no ERROR logs | **PASS** | ![image-2025-3-15_9-31-46.png](attachments/image-2025-3-15_9-31-46.png) ![image-2025-3-15_9-35-9.png](attachments/image-2025-3-15_9-35-9.png) |
| 3 | CheckUI | Work as normal | **PASS** | ![image-2025-3-15_9-34-3.png](attachments/image-2025-3-15_9-34-3.png) ![image-2025-3-15_9-34-30.png](attachments/image-2025-3-15_9-34-30.png) |
| 4 | Control-M | | **PASS** | ![image-2025-3-15_10-27-43.png](attachments/image-2025-3-15_10-27-43.png) Before purge: ![image-2025-3-15_10-28-17.png](attachments/image-2025-3-15_10-28-17.png) After purge: ![image-2025-3-15_10-28-36.png](attachments/image-2025-3-15_10-28-36.png) |
| 5 | | | **PASS** | |