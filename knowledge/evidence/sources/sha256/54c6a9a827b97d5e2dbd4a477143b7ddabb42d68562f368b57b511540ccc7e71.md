CR：CHG0701593

TSK:  CTASK1506220

AIG：

# 1.1 Release Work Item:

[Release 7634734 CHG0701593: March 22th change](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7634734)

[Release 7726083 CHG0701593: March 22th change db repo rollback](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7726083)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ~~51358-mfe-cashflow-blotter~~ | ~~[release/v1.16.0](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter?version=GBrelease/v1.15.0)~~ cashflow blotter package release will be covered by BAU [Release On 2025-03-29 CR: CHG0696052 BAU](https://confluence.global.standardchartered.com/display/DSP/Release+On+2025-03-29+CR%3A+CHG0696052+BAU) | ~~![image-2025-3-21_9-28-35.png](attachments/image-2025-3-21_9-28-35.png)~~ | ~~![image-2025-3-21_9-27-58.png](attachments/image-2025-3-21_9-27-58.png)~~ | ~~[Pipelines - Run 20250320.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5480265&view=results)~~ | ~~1.16.0-v1.16.0-20250320.5~~ | ~~@Guiling Wang ~~ ~~@Shuai Lu ~~ |
| 2 | 51358-ratan-cashflow-lifecycle-service | release/v3.1.3 | ![image-2025-4-8_11-19-29.png](attachments/image-2025-4-8_11-19-29.png) | ![image-2025-3-18_11-4-58.png](attachments/image-2025-3-18_11-4-58.png) | ~~[Pipelines - Run 20250318.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5439360&view=results)~~ [Pipelines - Run 20250327.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5589063&view=results) | ~~3.1.3-20250318.1~~ 3.1.3-20250327.5 | @Quill Li @Chen Yang |
| 3 | 51358-ratan-cash-settlement-netting-service | release/v1.5.2 | ![image-2025-3-17_15-31-55.png](attachments/image-2025-3-17_15-31-55.png) | ![image-2025-3-17_15-33-0.png](attachments/image-2025-3-17_15-33-0.png) | [Pipelines - Run 20250317.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5425446&view=results) | 1.5.2-20250317.5 | @Xinmiao Huang |
| 4 | 51358-ratan-cash-settlement-group-management-service | release/v2.1.6 | ![image-2025-3-18_14-24-16.png](attachments/image-2025-3-18_14-24-16.png) | ![image-2025-3-18_14-24-35.png](attachments/image-2025-3-18_14-24-35.png) | [Pipelines - Run 20250318.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5438822&view=results) | 2.1.6-20250318.1 | @Xinmiao Huang |
| 5 | 51358-ratanone-db-repository | develop | NA | NA | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5425137&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5425137&view=results) | CHG0701593-20250317.4 CHG0701593_Rollback-20250317.5 ratanone-db-repository-20250317.6.zip | @Mingyang Zhong |
| 6 | 51358-ratanone-db-repository **ONLY FOR ROLLBACK!** | develop | NA | NA | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5459590&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5459590&view=results) | CHG0701593_Rollback-20250317.5 ratanone-db-repository-20250319.1.zip | @Mingyang Zhong |
| 7 | 51358-ratanone-ansible | main | NA | NA | [Pipelines - Run 20250318.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5447473&view=results) | 20250318.8 | @Zeyu Zhou |

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
| 1 | | |
| 2 | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-03-22 | [cn-release-20250322 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/de39a226-ddcf-4cbb-8395-f1cf5f12d6bf/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff:** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Ratan put file in Ratan NAS path, send message request to trigger FileIT | Aspire can receive file in Aspire NAS path. | **PASS** | ![image-2025-3-29_12-56-21.png](attachments/image-2025-3-29_12-56-21.png) |
| 2 | 1. Customer Views-> load view list names 2. Input "CN" | Include "CN" name options should display the views in list | **PASS** | ![2025-03-29 16_52_24-.png](attachments/2025-03-29 16_52_24-.png) ![2025-03-29 09_41_08.png](attachments/2025-03-29 09_41_08.png) |
| 3 | 1.In cashflow blotter, Filter -> load filters list names 2.Input "UK" 3.Check Setting Button name 4. In dashboard, check Setting Button name | 1.Include "UK" name options should display the filters in list 2. Button name should change to Create Or Modify | **PASS** | ![2025-03-29 09_42_31.png](attachments/2025-03-29 09_42_31.png) ![2025-03-29 09_43_17.png](attachments/2025-03-29 09_43_17.png) |
| 4 | 1,Open Dashboard 2. Check Failed VD Today loading time | Dashboard Failed VD Today loading time <5s | **PASS** | ![2025-03-29 10_06_27-.png](attachments/2025-03-29 10_06_27-.png) |
| 5 | 1. Open Dashboard 2. See status number is rendering 3. close the tile before first round of query end. 4. wait 2 mins, check the queries whether start again. | dashboard query should stop while tile closed | **PASS** | ![2025-03-29 10_00_20-.png](attachments/2025-03-29 10_00_20-.png) |