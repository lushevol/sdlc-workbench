CR：CHG0516788

AIG：

# Release Work Item:

[Release 4727041: CHG0516788 July 27th CN Go-live - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/4727041)

# OLA

[Cash Settlement Ratan One 2024 OLA - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+Ratan+One+2024+OLA)

# Packages

| | Service | Branch | Hashicorp Enabled | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-group-management-service | release/v2.0.0 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2711208&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2711208&view=results) | 2.0.0-20240723.2 | @Xinmiao Huang |
| 2 | 51358-ratan-cashflow-lifecycle-service | release/v1.2.5 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2628633&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2628633&view=results) | 1.2.5-20240716.5 | @Chen Yang |
| 3 | 51358-ratan-mxg-cashflow-adaptor | release/v1.7.1 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2610274&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2610274&view=results) | 1.7.1-20240715.3 | @Chen Yang |
| 4 | 51358-ratan-rule-service | release/v2.0.1 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2625586&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2625586&view=results) | 2.0.1-20240716.2 | @Pengpeng Li |
| 5 | 51358-ratan-cash-settlement-ssi-stamping-service | release/v2.3.1 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2615791&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2615791&view=results) | 2.3.1-20240715.2 | @Xinmiao Huang |
| 6 | 51358-ratan-cash-settlement-accountng-service | release/v1.0.1 | Yes | [Pipelines - Run 20240715.6 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2613315&view=results) | 1.0.1-20240715.6 | @Chongxuan Li |
| 7 | 51358-ratanone-swift-service | release/v1.0.1 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2626219&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2626219&view=results) | 1.0.1-20240716.3 | @Mingyang Zhong |
| 8 | 51358-ratan-cash-settlement-netting-service | release/v1.2.2 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2638312&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2638312&view=results) | 1.2.2-20240717.4 | @Mingyang Zhong |
| 9 | 51358-ratan-cash-settlement-query-service | release.v2.2.2 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2685858&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2685858&view=results) | 2.2.2-20240722.2 | @Chen Yang |
| 10 | 51358-mfe-cashflow-blotter | release/v1.6.0 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2652408&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2652408&view=results) | 1.6.0-production-20240718.3 | @Shuai Lu |
| 11 | 51358-ratanone-db-repository | develop | N/A | | | @Chen Yang |
| 12 | 51358-ratan-service-properties | master | N/A | | | @Chen Yang |

| | 51358-ratan-service-properties | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- |
| 1 | 27th Package | [Pipelines - Run 20240718.5 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2657646&view=results) | 20240718.5 （CN strategy, CPT open） | @Chen Yang |
| 2 | Go Decision package | [Pipelines - Run 20240716.2 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2631613&view=results) | 20240716.2 (CN strategic, CPT close) | @Chen Yang |
| 3 | No-Go Decision Package | | 20240701.2 (CN non-strategic, CPT open) | @Chen Yang |

| | Service | Branch | ADO release pipeline | Owner |
| --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | execute: CHG0516788-20240717.2 rollback: CHG0516788_Rollback-20240717.3 | @Chen Yang |
| 2 | rules change | | db : **EXPAND: execute sql** UPDATE ratanone_rule_service.ratan_rule_engine SET meta_data='{"exceptions":[{"exceptionCode":"Net Cashflow","exceptionCategory":"OTHER","operationLevel":"MAKER_CHECKER","bulkEligible":true}]}' WHERE reason = 'Net Cashflow'; **EXPAND_END** **EXPAND: rollback sql** UPDATE ratanone_rule_service.ratan_rule_engine SET meta_data='{"exceptions":[{"exceptionCode":"Net Cashflow","exceptionCategory":"OTHER","operationLevel":"CHECKER_ONLY","bulkEligible":true}]}' WHERE reason = 'Net Cashflow'; **EXPAND_END** | @Chongxuan Li |

# Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2024-07-27 | [cn-release-20240727 - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_queries/query/227c8fc2-6a47-416d-b324-0413e3673ef8/) | [Test Plan 4979682 SMFRP-Release-20240727 - Test Plans (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=4979682&suiteId=4982139) | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: [Pipelines - Run 20240717.4 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2638312&view=sc-ado.sc-release-extension-prod.test-report-tab) More Details pls refer to email: **QA Signoff:** **UAT signoff: ** **** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# PT on the new API of querying trade status

| Service | Interface | Test tool | Test env | Time duration | Theads | QPS | RT(Average) | RT(TP90) | RT(TP95) | RT(TP99) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Group-Management-Service | Query Trade status | Jmeter | Dev | 10min | 100 | 402/s | 247ms | 279ms | 401ms | 575ms |
| Trade-Service | Query Trade status | Jmeter | Dev | 10min | 100 | 396/s | 251ms | 306ms | 359ms | 455ms |

![image2024-7-22_19-0-39.png](attachments/image2024-7-22_19-0-39.png)

# Rehearsal

| Cashflow Id | Cashflow Swift Message Standard | Cashflow Swift Status | Cashflow Accounting Status | Payment Date | Cashflow State | Booking Entity FMCODE | Counterparty FMCODE | CCY | Scenario | Actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M00240723996 | MT | Pending FMSGW Ack | | 2024-07-29 | RELEASED | SCB SG LTD*SIN | JP MORGAN SEC*LDN | XAU | To be released, stuck by CPT check | Script to Early Release |
| M00240723998 | MT | Pending FMSGW Ack | SENT | 2024-07-23 | RELEASED | SCB SG LTD*SIN | JP MORGAN SEC*LDN | XAU | To be released, stuck by CPT check | Script to Early Release |
| M00104975314 | MT | Pending FMSGW Ack | | 2024-07-26 | RELEASED | SCB CN CHO*CHO | SCB SHANGH*SHA | CNO | To be released, stuck by CPT check | Script to Early Release |
| M00104971922 | MT | Auto Settled by Ratan | | 2024-07-26 | SETTLED | SCB KL*KUL? | BNP PARIBAS MSIA*KUL | MYO | To be released, stuck by CPT check | Script to Early Release |
| M00107254792 | MT | Pending FMSGW Ack | | 2024-07-26 | RELEASED | SCB SG LTD*SIN | SCB HONGKON*HKG | USD | To be released, stuck by CPT check | Script to Early Release |
| M00107413076 | MT | Pending FMSGW Ack | SENT | 2024-07-18 | RELEASED | SCB SG LTD*SIN | GUEC00HSHK*HKG | XAU | To be released, stuck by CPT check | Script to Early Release |
| M00107411859 | | | SENT | 2024-07-18 | SWIFT_SUPPRESSED | SCB SG LTD*SIN | SCB HONGKON*HKG | XAG | To generate accounting, stuck by CPT check | Script to unsuppress & reject |
| 000016700344 | | | | 2024-07-24 | SWIFT_SUPPRESSED | SCB CN HANGZHOU*HNZ | SCB CN CHO*CHO | USD | To generate accounting, stuck by CPT check | Script to unsuppress & reject |
| N00000001100 | | | SENT | 2024-07-23 | SWIFT_SUPPRESSED | SCB BOMBAY*MMB | CLEARING CORP*MMB | INO | To generate accounting, stuck by CPT check | Script to unsuppress & reject |
| N00000001101 | | | | 2024-07-24 | SWIFT_SUPPRESSED | SCB BOMBAY*MMB | CLEARING CORP*MMB | INO | To be released, stuck by CPT check | Script to suppress & approve |
| M00104976330 | MT | Pending FMSGW Ack | | 2024-07-26 | RELEASED | SCB BOMBAY*MMB | SCB LONDON*LDN | EUR | To be released, stuck by CPT check | Manual Early Release |
| N00000001103 | | | | 2024-07-24 | SWIFT_SUPPRESSED | SCB BOMBAY*MMB | CLEARING CORP*MMB | INO | To be released, stuck by CPT check | Manual unsuppress & approve |
| N00000001102 | | | SENT | 2024-07-23 | SWIFT_SUPPRESSED | SCB BOMBAY*MMB | CLEARING CORP*MMB | INO | To generate accounting, stuck by CPT check | Manual unsuppress & reject |
| M00106873346 | MT | Pending FMSGW Ack | | 2024-07-26 | RELEASED | SCB CN CHO*CHO | BK OF SUZ CO LTD*SUZ | CNO | Post release handle exception | Manual maker/checker |
| M00240729995 | MT | Pending FMSGW Ack | | 2024-07-29 | RELEASED | SCB KL*KUL? | SCANIACREDIT*SAL | EUR | Post release STP | |