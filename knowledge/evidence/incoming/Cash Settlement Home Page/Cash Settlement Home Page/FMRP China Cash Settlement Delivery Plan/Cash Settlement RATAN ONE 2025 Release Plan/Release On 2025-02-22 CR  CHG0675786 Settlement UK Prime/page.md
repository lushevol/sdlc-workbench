CR：CHG0675786

TSK: CTASK1450674

AIG：

# 1.1 Release Work Item:

[Release 7161057 RATAN Settlement Feb 22th CHG0675786](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7161057)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-group-management-service | release/v2.1.5 | ![image2025-2-12_11-5-26.png](attachments/image2025-2-12_11-5-26.png) | ![image2025-2-12_11-5-44.png](attachments/image2025-2-12_11-5-44.png) | [Pipelines - Run 20250204.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=4871633&view=results) | 2.1.5-20250204.8 | @Xinmiao Huang |
| 2 | 51358-ratan-cashflow-lifecycle-service | release/v3.0.4 | ![image2025-2-12_11-8-2.png](attachments/image2025-2-12_11-8-2.png) | ![image2025-2-12_11-7-28.png](attachments/image2025-2-12_11-7-28.png) | [Pipelines - Run 20250210.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=4943003&view=results) | 3.0.4-20250210.5 | @Xinmiao Huang |
| 3 | 51358-ratan-cash-settlement-query-service | release/v3.0.3 | ![image2025-2-12_11-10-7.png](attachments/image2025-2-12_11-10-7.png) | ![image2025-2-12_11-10-26.png](attachments/image2025-2-12_11-10-26.png) | [Pipelines - Run 20250206.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=4904588&view=results) | 3.0.3-20250206.2 | @Xinmiao Huang |
| 4 | 51358-ratanone-db-repository | feature/cn_go_live_Feb22 | N/A | N/ | [Pipelines - Run 20250219.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5079608&view=results) | ratanone-db-repository-20250219.4 | @Xinmiao Huang |
| 5 | 51358-ratan-cash-settlement-ssi-stamping-service | [release/v2.4.4](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-ssi-stamping-service?version=GBrelease/v2.4.4) | ![image2025-2-14_10-13-24.png](attachments/image2025-2-14_10-13-24.png) | ![image2025-2-14_10-12-52.png](attachments/image2025-2-14_10-12-52.png) | [Pipelines - Run 20250213.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=4992300&view=results) | 2.4.4-20250213.3 | @Quill Li |

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
| Full Ratan Performance test | [RATAN One - Backend Performance Test Plan Feb 2025 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+-+Backend+Performance+Test+Plan+Feb+2025) [RATAN One FMO GUI - Performance Test Plan Feb 2025 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+FMO+GUI+-+Performance+Test+Plan+Feb+2025) | [RATAN One - Backend Performance Test Result Feb 2025 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+-+Backend+Performance+Test+Result+Feb+2025) [RATAN One FMO GUI - Performance Test Result Feb 2025 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+FMO+GUI+-+Performance+Test+Result+Feb+2025) |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-02-22 | [cn-release-20250222 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/304eae27-f2d2-4a09-a82f-ec915af4de43/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** **** **** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Check index creation result | index created | **PASS** | ![image-2025-2-25_11-22-40.png](attachments/image-2025-2-25_11-22-40.png) |
| 2 | Continuous monitoring prod db CPU usage | CPU less than before | **PASS** | db cpu usage remains under 62% ![image-2025-2-25_11-23-27.png](attachments/image-2025-2-25_11-23-27.png) |
| 3 | Prime bullion trade ssi stamping | Bullion trade (spot/forward/swap) stamp success | **PASS** | ![image-2025-2-25_11-57-53.png](attachments/image-2025-2-25_11-57-53.png) queried from daily dump: ```sql select tsm.trade_id , product_type , (near_leg_result::jsonb ->> 0)::jsonb -> 'message' as nearleg_buyer_result, (near_leg_result::jsonb ->> 1)::jsonb -> 'message' as nearleg_seller_result, (far_leg_result::jsonb ->> 0)::jsonb -> 'message' as farleg_buyer_result, (far_leg_result::jsonb ->> 1)::jsonb -> 'message' as farleg_seller_result from cash_settlement_ssi_cn.trade_stamping_message tsm where tsm.created_at >= '2025-02-22' and product_type like 'bullion%' order by tsm.created_at desc; ``` |