CR：CHG0771118

TSK: CTASK1656340

AIG：

# 1.1 Release Work Item:

[Release 8952639 CHG0771118: RATAN Settlement Tranche 2 Go-Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8952639)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | | NA | NA | [Pipelines - Run 20250717.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7198725&view=results) | install: CHG0771118-20250717.2 rollback: CHG0771118_Rollback-20250714.5 | @Chen Yang |
| 2 | 51358-ratanone-static-data-service | release/v3.5.0 | ![image-2025-7-15_14-27-31.png](attachments/image-2025-7-15_14-27-31.png) | ![image-2025-7-15_14-26-54.png](attachments/image-2025-7-15_14-26-54.png) | [Pipelines - Run 20250711.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7111231&view=results) | 3.5.0-20250711.4 | @Chongxuan Li |
| 3 | 51358-ratan-service-properties | master | N/A | N/A | [Pipelines - Run 20250715.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7164672&view=results) | 20250715.2 | @Chen Yang |
| 4 | 51358-mfe-cashflow-blotter | release/v1.35.1 | ![image-2025-7-22_10-6-59.png](attachments/image-2025-7-22_10-6-59.png) | ![image-2025-7-22_10-6-16.png](attachments/image-2025-7-22_10-6-16.png) | [Pipelines - Run 20250721.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7260215&view=results) | 20250721.3 | @Guiling Wang @Shuai Lu |
| 5 | 51358-ratan-cash-settlement-accounting-service | release/v1.2.2 | ![image-2025-7-15_14-7-25.png](attachments/image-2025-7-15_14-7-25.png) | ![image-2025-7-15_14-6-56.png](attachments/image-2025-7-15_14-6-56.png) | [Pipelines - Run 20250715.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7156048&view=results) | 1.2.2-20250715.2 | @Chongxuan Li |
| 6 | 51358-ratan-cash-settlement-lms-service | release/v2.1.3 | ![image-2025-7-8_15-58-56.png](attachments/image-2025-7-8_15-58-56.png) | ![image-2025-7-8_15-59-13.png](attachments/image-2025-7-8_15-59-13.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7152809&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7152809&view=results) | 2.1.3-20250715.1 | @Mingyang Zhong |
| 7 | 51358-ratan-cash-settlement-ssi-stamping-service | release/v2.4.9 | ![image-2025-7-9_10-4-5.png](attachments/image-2025-7-9_10-4-5.png) | ![image-2025-7-9_10-3-50.png](attachments/image-2025-7-9_10-3-50.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7152812&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7152812&view=results) | 2.4.9-20250715.3 | @Mingyang Zhong |
| 8 | 51358-ratan-cash-settlement-query-service | release/v3.0.10 | ![image-2025-7-9_10-4-43.png](attachments/image-2025-7-9_10-4-43.png) | ![image-2025-7-9_10-4-23.png](attachments/image-2025-7-9_10-4-23.png) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7152821&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7152821&view=results) | 3.0.10-20250715.4 | @Mingyang Zhong |
| 9 | [51358-ratanone-command](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command?path=/&version=GBmain) (Use to send ebbs services - for Catalyst UK 27th July) | main | NA | NA | [Pipelines - Run 20250722.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7281814&view=results) | CHG0771118-20250722.2 | @Chongxuan Li |
| 10 | 51358-ratanone-command_us (use to test US 26th July) | main | NA | NA | [Pipelines - Run 20250722.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7281966&view=results) | CHG0771118-20250722.2 | @Chongxuan Li |
| 11 | ~~[51358-ratanone-service](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible?path=/&version=GBfeature/cn-20250322-release-command)_stopServcies~~ | master | NA | NA | | | @Zeyu Zhou |
| 12 | 51358-ratanone-service_restartSettOrchServices | master | NA | NA | [Pipelines - Run 20250722.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7282505&view=results) | | @Zeyu Zhou |
| 13 | 51358-mfe-ratan-container | [release/v1.7.40.2](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-ratan-container?version=GBrelease/v1.7.40.2) | ![image-2025-7-21_9-7-6.png](attachments/image-2025-7-21_9-7-6.png) | ![image-2025-7-21_9-7-20.png](attachments/image-2025-7-21_9-7-20.png) | [Pipelines - Run 20250718.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7236290&view=results) | 20250718.4 | @Shuai Lu @Guiling Wang |
| 14 | 51358-RATAN-W-ControlM-RAT | main | | | [Pipelines - Run 20250724.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7320666&view=results) | | Cai ,Jie |

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
| CN | 2025-07-26 | [cn-release-20250726 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query-edit/5bf059a4-dd65-4059-9440-a274ce626f0e/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** **** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | select count(1) from ratanone_swift_service.swift_static_data_correspondent_bic where k_fmid in ('7', '400077978', '10036428', '400018439', '400032489', '8', '10036382', '5', '400045551'); | 9 | | ![image-2025-7-26_9-24-11.png](attachments/image-2025-7-26_9-24-11.png) |
| 2 | select count(1) from ratanone_swift_service.swift_static_data_sender_bic where k_fmid in ('7', '400077978', '10036428', '400018439', '400032489', '8', '10036382', '5', '400045551'); | 9 | | ![image-2025-7-26_9-24-47.png](attachments/image-2025-7-26_9-24-47.png) |
| 3 | select count(1) from ratan_rule_service.ratan_validation_rule where field='popDubai'; | 1 | | ![image-2025-7-26_9-25-10.png](attachments/image-2025-7-26_9-25-10.png) |
| 4 | select count(1) from ratanone.ratan_static__cashflow_nostro rscn where id like 'tranche2-e417%'; select count(1) from ratanone.nostro_manipulation_audit rscn where nostro_id like 'tranche2-e417%'; select count(1) from ratanone.ratan_static_cashflow_currency_cut_off where id like 'tranche1da4e%' | 414 414 1971 | | ![image-2025-7-26_9-25-34.png](attachments/image-2025-7-26_9-25-34.png) ![image-2025-7-26_9-25-45.png](attachments/image-2025-7-26_9-25-45.png) ![image-2025-7-26_9-25-52.png](attachments/image-2025-7-26_9-25-52.png) |
| 5 | select count(1) from ratanone.ratan_static__cashflow_ebbs_txn_code where id in ('48', '49', '50', '51', '52', '53', '54', '55', '56'); | 9 | | ![image-2025-7-26_9-26-4.png](attachments/image-2025-7-26_9-26-4.png) |
| 6 | select count(1) from ratanone.ratan_static__cashflow_ebbs_bridge_account where id in ('48', '49', '50', '51', '52', '53', '54', '55', '56'); | 9 | | ![image-2025-7-26_9-26-11.png](attachments/image-2025-7-26_9-26-11.png) |
| 7 | select count(1) FROM ratanone_rule_service.ratan_rule_engine WHERE id in ('7325724381374210048','7325725428051587072','7347911008947220480','7348010347694587904','7348984795667038208', '7348011160626200576','7348011873748709376','7325760398989504512','7348012306399555584','7349266391873060864','7348543908291252224','7349266842732756992','7347904680783908864', '7349266660316905472','7326437680231374848', '7347909373157314560','7325719718654533632'); | 17 | | ![image-2025-7-26_9-26-23.png](attachments/image-2025-7-26_9-26-23.png) |
| 12 | check properties-prod.yaml for CPT | | | ![image-2025-7-26_9-28-7.png](attachments/image-2025-7-26_9-28-7.png) |
| 8 | 1. Login to PTP, open cashflow dashboard. 2. Fuzzy input match on horizontal search bar. | Expect input search in quick filters | PASS | ![image-2025-7-26_9-55-30.png](attachments/image-2025-7-26_9-55-30.png) |
| 9 | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8368145](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8368145) 1. Login to PTP, open cashflow blotter. 2. Click on booking entity, will see the dropdown list. | Expect dropdown list contains new entities | | ![image-2025-7-26_10-45-52.png](attachments/image-2025-7-26_10-45-52.png)![image-2025-7-26_10-46-9.png](attachments/image-2025-7-26_10-46-9.png) |
| 10 | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8742633](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8742633) 1. Login to PTP, open cashflow blotter. 2. Search with booking entity=xxx. | Expect auto applied VD=Today | PASS | ![image-2025-7-26_12-39-18.png](attachments/image-2025-7-26_12-39-18.png) |
| 11 | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9426892](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9426892) 1. Login to PTP, open cashflow blotter 2. Open custom search dialog 3. create a new filter contains VD=Current Date and Cashflow State = WAITING 4. Trigger search. 5. Click Duplicate button. | Expect to query VD with today. Expect to duplicate the filter | PASS | ![image-2025-7-26_10-43-54.png](attachments/image-2025-7-26_10-43-54.png) ![image-2025-7-26_10-44-41.png](attachments/image-2025-7-26_10-44-41.png) ![image-2025-7-26_10-44-52.png](attachments/image-2025-7-26_10-44-52.png) ![image-2025-7-26_12-38-14.png](attachments/image-2025-7-26_12-38-14.png) |