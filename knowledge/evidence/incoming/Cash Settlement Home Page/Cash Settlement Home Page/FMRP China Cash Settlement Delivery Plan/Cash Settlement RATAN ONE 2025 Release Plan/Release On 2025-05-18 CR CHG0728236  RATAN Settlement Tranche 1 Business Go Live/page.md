CR：CHG0728236

TSK: CTASK1562583

AIG：

# 1.1 Release Work Item:

[Release 8078678 2025-05-18 CR:CHG0728236 RATAN Settlement Tranche 1 Business Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8078678)

# 1.2 Packages

| 1 | 51358-ratanone-db-repository | main | NA | NA | [Pipelines - Run 20250505.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6074141&view=results) | CHG0728236-20250505.2.zip CHG0728236_Rollback-20250505.3.zip | @Xinmiao Huang Updated At 2025-05-05 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | ~~51358-ratan-cashflow-lifecycle-service~~ | ~~release/v3.2.1~~ | ![image-2025-5-7_15-58-4.png](attachments/image-2025-5-7_15-58-4.png) | ![image-2025-5-7_15-58-19.png](attachments/image-2025-5-7_15-58-19.png) | ~~[Pipelines - Run 20250507.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6111995&view=results)~~ | ~~3.2.1-20250507.8~~ ~~rollback version: 3.2.0-20250411.1~~ | @Chongxuan Li |
| 3 | 51358-ratan-cash-settlement-accounting-service | release/v1.2.1 | ![image-2025-5-7_15-58-39.png](attachments/image-2025-5-7_15-58-39.png) | ![image-2025-5-7_15-59-1.png](attachments/image-2025-5-7_15-59-1.png) | [Pipelines - Run 20250507.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6112012&view=results) | 1.2.1-20250507.8 rollback version: 1.2.0-20250418.5 | @Chongxuan Li |
| 4 | 51358-ratan-service-properties | master | | | [Pipelines - Run 20250508.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6127309&view=results) | 20250508.6 rollback version: 20250505.5 | @Chongxuan Li |
| 5 | 51358-mfe-cashflow-blotter | release/v1.22.0 | ![2025-05-09 17_08_37-Pipelines - Run 20250508.6 and 1 more page - Work - Microsoft​ Edge.png](attachments/2025-05-09 17_08_37-Pipelines - Run 20250508.6 and 1 more page - Work - Microsoft​ Edge.png) | ![2025-05-09 17_07_17-Pipelines - Run 20250508.6 and 1 more page - Work - Microsoft​ Edge.png](attachments/2025-05-09 17_07_17-Pipelines - Run 20250508.6 and 1 more page - Work - Microsoft​ Edge.png) | [Pipelines - Run 20250508.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6127674&view=results) | 1.22.0-v1.22.0-20250508.6 | @Shuai Lu @Guiling Wang |
| 6 | 51358-ratan-cash-settlement-query-service | release/v3.0.9 | ![image-2025-5-8_8-57-18.png](attachments/image-2025-5-8_8-57-18.png) | ![image-2025-5-8_8-56-34.png](attachments/image-2025-5-8_8-56-34.png) | [Pipelines - Run 20250505.5 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6075330&view=results) | 3.0.9-20250505.5 rollback version: 20250416.16.1 | @Fengke Wu |
| 7 | 51358-ratanone-service_stopServcies | main | NA | NA | [Pipelines - Run 20250512.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6164951&view=results) | NA | @Zeyu Zhou |
| 8 | 51358-ratanone-service_restart600Services | main | NA | NA | [Pipelines - Run 20250512.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6164956&view=results) | NA | @Zeyu Zhou |
| 9 | 51358-ratanone-service_restart400Services | main | NA | NA | [Pipelines - Run 20250512.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6165043&view=results) | NA | @Zeyu Zhou |

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
| CN | 2025-05-18 | [cn-release-20250518 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/de961625-0e9e-45e0-8edb-96ff5f7e6470/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | cat /apps/ratanrt/services/ratan-service-properties/config-repo/application-prod.yml | CPT_ENTITY_LIST is empty | **PASS** | ![image-2025-5-18_9-22-59.png](attachments/image-2025-5-18_9-22-59.png) |
| 2 | 1. Login to FMTPT 2. Open "Cashflow Blotter" 3. Open "Advanced Search" | Only one filter records call triggered | **PASS** | ![image-2025-5-20_9-34-46.png](attachments/image-2025-5-20_9-34-46.png) |
| 3 | 1. Login to FMTPT 2. Open "Cashflow Blotter" 3. Search with amount is "323204", currency is "USD" and vd is March 5th. | Get right result | **PASS** | ![image-2025-5-20_9-45-35.png](attachments/image-2025-5-20_9-45-35.png) |
| 4 | 1. Login to FMTPT 2. Open "Cashflow Blotter" 3. Open "Advanced Search" 4. Search with amount is "323204", currency is "USD" and vd is March 5th. | Get right result the same with No.3 | **PASS** | ![image-2025-5-20_9-48-58.png](attachments/image-2025-5-20_9-48-58.png) |
| 5 | 1. Login to FMTPT 2. Open "Bic Netting Static" 3. Wait after all data loaded | No break lines in family and other columns | **PASS** | ![image-2025-5-20_9-47-9.png](attachments/image-2025-5-20_9-47-9.png) |
| 6 | 1. Login to FMTPT 2. Open "Grouping Blotter" 3. Filter on column currency with "USD". 4. Scroll down to bottom to load next page | Step3: Display count shows correctly Step4: Display count show correctly | **PASS** | ![image-2025-5-20_9-52-38.png](attachments/image-2025-5-20_9-52-38.png) ![image-2025-5-20_9-52-43.png](attachments/image-2025-5-20_9-52-43.png) |