CR：CHG0699845

TSK: CTASK1502809

AIG：

# 1.1 Release Work Item:

[Release 7609239 CHG0699845: ratan settlement change for april](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7609239)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-query-service | release/v3.0.7 | ![image-2025-4-9_15-50-29.png](attachments/image-2025-4-9_15-50-29.png) | ![image-2025-4-9_15-51-47.png](attachments/image-2025-4-9_15-51-47.png) | ~~[Pipelines - Run 20250403.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5674545&view=results)~~ [Pipelines - Run 20250409.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5755774&view=results) | 3.0.7-20250403.3 3.0.7-20250409.3 | @Chen Yang |
| 2 | 51358-ratanone-db-repository | develop | N/A | N/A | [Pipelines - Run 20250407.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5716952&view=results) | | @Guiling Wang |
| 3 | 51358-mfe-cashflow-blotter | [release/v1.18.0](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter?version=GBrelease/v1.18.0) | ![2025-04-10 15_54_09-Task View.png](attachments/2025-04-10 15_54_09-Task View.png) | ![2025-04-10 15_54_29-.png](attachments/2025-04-10 15_54_29-.png) | [Pipelines - Run 20250410.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5776201&view=results) | 1.18.0-v1.18.0-20250410.6 | @Guiling Wang @Shuai Lu |
| 4 | 51358-mfe-ratan-container | [release/v1.7.28](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-ratan-container?version=GBrelease/v1.7.28) | ![image-2025-4-3_14-14-48.png](attachments/image-2025-4-3_14-14-48.png) | ![image-2025-4-3_14-15-15.png](attachments/image-2025-4-3_14-15-15.png) | [Pipelines - Run 20250403.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5668190&view=results) | 1.7.28-v1.7.28-20250403.1 | @Guiling Wang @Shuai Lu |
| 5 | 51358-ratanone-ansible | main | | | [Pipelines - Run 20250401.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5631388&view=results) | | @Jie Cai |

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
| 1 | PT plan and results | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-03-15 | [cn-release-20250405 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/d9723d9e-99ee-4fdc-95c3-f1e8463660ad/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff:** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | 1. Open "Cashflow Blotter" 2. Open "Cashflow Dashboard" | 1. Cashflow Blotter elements visible 2. Cashflow Dashboard elements visible | **PASS** | ![image-2025-4-12_10-25-14.png](attachments/image-2025-4-12_10-25-14.png) ![image-2025-4-12_10-25-21.png](attachments/image-2025-4-12_10-25-21.png) |
| 2 | 1. Open "Cashflow Blotter" 2. Open Custom Search 3. Create a new filter for UK Commodity, and trigger search. | 1. Default loading works well 2. Custom Search displayed as Advaned Search 3. New filter works well | **PASS** | ![image-2025-4-12_10-25-52.png](attachments/image-2025-4-12_10-25-52.png) default loading ![image-2025-4-12_10-27-10.png](attachments/image-2025-4-12_10-27-10.png) |
| 3 | 1. Open Cashflow Blotter, check the Prime PM, Murex and Stella Product on quick search, quick filter, customer search | Prime PM, Murex and Stella Product will successfully display to screen | **PASS** | ![2025-04-12 09_45_00-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 09_45_00-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png) ![2025-04-12 09_44_28-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 09_44_28-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png) ![2025-04-12 09_47_10-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 09_47_10-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png) ![2025-04-12 09_46_46-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 09_46_46-FMO Post Trade Portal and 14 more pages - Work - Microsoft​ Edge.png) |
| 4 | 1. Open cashflow Blotter->Customer Filter-> input label value "4944" on select box 2. Customer View-> input label value "bc9b" on select box | Search will only based on list name, type value then no data. | **PASS** | ![2025-04-12 09_49_50-Program Manager.png](attachments/2025-04-12 09_49_50-Program Manager.png) ![2025-04-12 09_52_00-.png](attachments/2025-04-12 09_52_00-.png) |
| 5 | 1. Customer Filter-> create a new filter named "test filter", then click the input box by "test filter", 2. Customer View-> create a new filter named "test view", then click the input box by "test view", | Search can see have a "test filter" and "test view" option | **PASS** | ![2025-04-12 10_01_28-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 10_01_28-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png) ![2025-04-12 10_01_50-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 10_01_50-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png) ![2025-04-12 09_59_40-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 09_59_40-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png) ![2025-04-12 10_00_05-Program Manager.png](attachments/2025-04-12 10_00_05-Program Manager.png) |
| 6 | 1. Quick search -> choose "COM|SWAP" on production taxonomy | The resultant cashflows will be successfully loaded on screen | **PASS** | ![2025-04-12 09_55_08-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 09_55_08-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png) |
| 7 | 1. Quick search ->type COM in product taxonomy | Search engine will get pop-up commodity ISDA details without input the full information | **PASS** | ![2025-04-12 09_53_17-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-12 09_53_17-FMO Post Trade Portal and 13 more pages - Work - Microsoft​ Edge.png) |