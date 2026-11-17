CR：CHG0687872

TSK: CTASK1474302

AIG：

# 1.1 Release Work Item:

[Release 7440744 CHG0687872: RATAN Settlement 2025 Tranche 1 Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7440744)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository_1 | | NA | NA | Install ： [Pipelines - Run 20250421.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5900312&view=results) | Install: CHG0687872-20250421.2 CHG0687872_Rollback-20250421.3 | @Chongxuan Li @Chen Yang |
| 2 | 51358-ratanone-db-repository | | NA | NA | service up: [Pipelines - Run 20250417.12](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5868139&view=results) | Service up: CHG0687872_ServiceUp-20250417.6 CHG0687872_ServiceUp_Rollback-20250417.7 | |
| 3 | 51358-ratanone-static-data-service | release/v3.4.4 | ![image-2025-4-15_14-28-59.png](attachments/image-2025-4-15_14-28-59.png) | ![image-2025-4-15_14-29-24.png](attachments/image-2025-4-15_14-29-24.png) | [Pipelines - Run 20250415.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5828642&view=results) | 3.4.4-20250415.2 | @Chongxuan Li @Mingyang Zhong |
| 4 | 51358-ratan-cash-settlement-netting-service | release/v1.5.3 | ![image-2025-4-18_0-13-13.png](attachments/image-2025-4-18_0-13-13.png) | ![image-2025-4-18_0-13-32.png](attachments/image-2025-4-18_0-13-32.png) | [Pipelines - Run 20250417.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5879536&view=results) | 1.5.3-20250417.8 | @Xinmiao Huang |
| 5 | 51358-ratan-cash-settlement-orchestration | release/v3.3.0 | ![image-2025-4-18_9-23-16.png](attachments/image-2025-4-18_9-23-16.png) | NA | [Pipelines - Run 20250418.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5881067&view=results) | 3.3.0-20250418.5 | @Xinmiao Huang |
| 6 | 51358-ratan-mxg-cashflow-adaptor | release/v1.8.8 | ![image-2025-4-17_13-37-11.png](attachments/image-2025-4-17_13-37-11.png) | ![image-2025-4-17_13-36-37.png](attachments/image-2025-4-17_13-36-37.png) | [Pipelines - Run 20250417.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5864108&view=results) | 1.8.8-20250417.2 | @Chen Yang |
| 7 | 51358-ratan-service-properties | master | N/A | N/A | [Pipelines - Run 20250417.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5866345&view=results) | 20250417.4 | @Chen Yang @Chongxuan Li |
| 8 | 51358-mfe-cashflow-blotter | release/v1.21.0 | ![2025-04-21 16_30_00-Pipelines - Run 20250421.20 and 15 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-21 16_30_00-Pipelines - Run 20250421.20 and 15 more pages - Work - Microsoft​ Edge.png) | ![2025-04-21 16_31_36-Program Manager.png](attachments/2025-04-21 16_31_36-Program Manager.png) ![image-2025-4-21_16-47-31.png](attachments/image-2025-4-21_16-47-31.png) | [Pipelines - Run 20250421.20](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5897726&view=results) | 1.21.0-v1.21.0-20250421.20 | @Guiling Wang |
| 9 | 51358-mfe-cashflow | release/v1.5.3 | ![2025-04-21 16_41_44-Pipelines - Run 20250421.17 and 15 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-21 16_41_44-Pipelines - Run 20250421.17 and 15 more pages - Work - Microsoft​ Edge.png) | ![2025-04-21 16_40_52-Pipelines - Run 20250421.17 and 15 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-21 16_40_52-Pipelines - Run 20250421.17 and 15 more pages - Work - Microsoft​ Edge.png) ![2025-04-21 16_48_22-51358-mfe-cashflow - Measures - SonarQube and 16 more pages - Work - Microsoft​ .png](attachments/2025-04-21 16_48_22-51358-mfe-cashflow - Measures - SonarQube and 16 more pages - Work - Microsoft​ .png) | [Pipelines - Run 20250421.17](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5897614&view=results) | 1.5.3-v1.5.3-20250421.17 | @Guiling Wang |
| 10 | 51358-ratan-cash-settlement-accounting-service | release/v1.2.0 | ![image-2025-4-18_12-7-57.png](attachments/image-2025-4-18_12-7-57.png) | ![image-2025-4-18_12-8-18.png](attachments/image-2025-4-18_12-8-18.png) | ~~[Pipelines - Run 20250418.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5881383&view=results)~~ [Pipelines - Run 20250418.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5881842&view=results) | rollback version: 1.1.2-20241230.3 new version: ~~1.2.0-20250418.2~~ 1.2.0-20250418.5 | @Chongxuan Li |
| 11 | 51358-ratanone-swift-service | release/v1.1.8 | ![image-2025-4-17_14-11-31.png](attachments/image-2025-4-17_14-11-31.png) | ![image-2025-4-17_14-11-11.png](attachments/image-2025-4-17_14-11-11.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5836693&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5836693&view=results) | 1.1.8-20250415.5 | @Mingyang Zhong |
| 12 | 51358-ratan-cash-settlement-lms-service | release/v2.1.2 | ![image-2025-4-17_14-12-4.png](attachments/image-2025-4-17_14-12-4.png) | ![image-2025-4-17_14-12-23.png](attachments/image-2025-4-17_14-12-23.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5836754&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5836754&view=results) | 2.1.2-20250415.3 | @Mingyang Zhong |
| 13 | 51358-ratan-cash-settlement-batch-service | release/v1.0.4 | ![image-2025-4-17_13-33-54.png](attachments/image-2025-4-17_13-33-54.png) | ![image-2025-4-17_13-34-14.png](attachments/image-2025-4-17_13-34-14.png) | [Pipelines - Run 20250417.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5864447&view=results) | 1.0.420250417.4 | @Chen Yang |
| 14 | [51358-ratanone-ansible](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible?path=/&version=GBfeature/cn-20250322-release-command) (Use to cleanup current batch services) | master | NA | NA | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5863729&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5863729&view=results) | NA | @Zeyu Zhou |
| 15 | [51358-ratanone-command](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command?path=/&version=GBmain) (Use to send ebbs services) | master | NA | NA | [Pipelines - Run 20250418.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5881829&view=results) | CHG0687872-20250418.5 | @Zeyu Zhou |
| 16 | [51358-ratanone-service](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible?path=/&version=GBfeature/cn-20250322-release-command)_stopServcies | master | NA | NA | [Pipelines - Run 20250417.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5868577&view=results) | NA | @Zeyu Zhou |
| 17 | 51358-ratanone-service_restart600Services | master | NA | NA | [Pipelines - Run 20250417.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5868043&view=results) | NA | @Zeyu Zhou |

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
| CN | 2025-04-26 | [cn-release-20250426 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/d6b839db-b69a-4a74-b23a-a7feb89b36f5/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** **** **** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | select count(1) from ratanone.ratan_bridge_flow where route_id in('90','91','93'); | 6 | | ![image-2025-4-26_9-20-57.png](attachments/image-2025-4-26_9-20-57.png) |
| 2 | select count(1) from ratanone.ratan_static__cashflow_nostro rscn where id like 'id-hk8%'; | 212 | **PASS** | ![image-2025-4-26_9-24-54.png](attachments/image-2025-4-26_9-24-54.png) |
| 3 | select count(1) from ratanone.ratan_static_cashflow_currency_cut_off rsccco where id like 'id-hk1%'; | 938 | **PASS** | ![image-2025-4-26_9-25-26.png](attachments/image-2025-4-26_9-25-26.png) |
| 4 | select count(1) from ratanone.ratan_static__cashflow_ebbs_txn_code where id in ('42','43','44','45','46'); select count(1) from ratanone.ratan_static__cashflow_ebbs_bridge_account where id in ('42','43','44','45','46'); | 5 | **PASS** | ![image-2025-4-26_9-25-46.png](attachments/image-2025-4-26_9-25-46.png) ![image-2025-4-26_9-26-5.png](attachments/image-2025-4-26_9-26-5.png) |
| 5 | select count(1) from ratanone_rule_service.ratan_rule_engine where id in ('7317540653172248576','7310652238726848512','7302270059618988032','7298180864649396224','7298180745215156224','7298180134244909056', '7298179840895287296','7298178735520022528','7312735397309550592','7312735905648074752','7298220809117380608','7304432580322254848','7304428167377575936', '7298524392885780480','7317546863142719488','7317544575228170240','7310640133021786112','7298521698400542720','7300448515962634240','7298523968693411840','7298232266125934592'); | 21 | **PASS** | ![image-2025-4-26_9-26-19.png](attachments/image-2025-4-26_9-26-19.png) |
| 6 | select count(1) from ratan_rule_service.ratan_validation_rule where rules like '%NOX%' and field='settlementMeans' and entity = 'EXCEPTION_SSI'; select count(1) from ratan_rule_service.ratan_validation_rule where created_at > '9999-10-20' and field='accountWithInstitutionBic' and entity = 'EXCEPTION_SSI'; | 1 | ** ** | ![image-2025-4-26_9-26-38.png](attachments/image-2025-4-26_9-26-38.png) ![image-2025-4-26_9-27-8.png](attachments/image-2025-4-26_9-27-8.png) |
| 7 | after accounting service start up select count(1) from ratan_cash_accounting_service.ratan_accounting_aspire_execution ; | 3 | ** ** | ![image-2025-4-26_9-46-32.png](attachments/image-2025-4-26_9-46-32.png) |
| 8 | select count(1) from ratanone_swift_service.swift_static_data_correspondent_bic where k_fmid in ('6', '2', '300075472'); | 3 | ** ** | ![image-2025-4-26_9-27-23.png](attachments/image-2025-4-26_9-27-23.png) |
| 9 | select count(1) from ratanone_swift_service.swift_static_data_sender_bic where k_fmid in ('6', '2', '300075472', '10038345', '300011345'); | 5 | ** ** | ![image-2025-4-26_9-27-33.png](attachments/image-2025-4-26_9-27-33.png) |
| 10 | cat /apps/ratanrt/services/ratan-service-properties/config-repo/application-prod.yml | | ** ** | ![image-2025-4-26_9-28-12.png](attachments/image-2025-4-26_9-28-12.png) |
| 11 | Check Tranche1 Entity if display on UI screen | Tranch1entity successfully add UI screen | **PASS** | ![2025-04-26 09_48_24-FMO Post Trade Portal and 19 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-26 09_48_24-FMO Post Trade Portal and 19 more pages - Work - Microsoft​ Edge.png) |
| 12 | Check Cashflow Blotter amount field to show as per actual payment value，whether remove rounding and trim 0 | About UI amount have removed rounding and trim 0 | **PASS** | ![2025-04-26 09_49_36-FMO Post Trade Portal and 19 more pages - Work - Microsoft​ Edge.png](attachments/2025-04-26 09_49_36-FMO Post Trade Portal and 19 more pages - Work - Microsoft​ Edge.png) |
| 13 | ls -l /apps/ratanrt/bin/services/ | batch servics script shoud start with 600 | **PASS** | ![image-2025-4-28_14-9-36.png](attachments/image-2025-4-28_14-9-36.png) |