CR：CHG0683420

TSK: CTASK1465271

AIG：

# 1.1 Release Work Item:

[Release 7366916 CHG0683420 Index creation to resolve the periodic high db cpu](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7366916)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | N/A | N/ | [Pipelines - Run 20250214.22](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5026838&view=results) | CHG0683420-20250214.20 CHG0683420_Rollback-20250214.21 | @Xinmiao Huang |

**EXPAND: Appendix**

## Shell Command

| Shell Comment | Execute Server | Command |
| --- | --- | --- |
| | | |
| | | |
| | | |
| | | |

**EXPAND_END**

# 1.3 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-01-25 | [cn-release-20250222 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/304eae27-f2d2-4a09-a82f-ec915af4de43/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: 📎 [Change CHG0683420 Index creation to resolve the periodic high db cpu.msg](attachments/Change CHG0683420 Index creation to resolve the periodic high db cpu.msg) **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.4 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | idx_cashflow_group_message_group_id; | existing in DB | **PASS** | ![image2025-2-19_10-58-13.png](attachments/image2025-2-19_10-58-13.png) |
| 2 | idx_cashflow_group_message_mxg_trade_id; | existing in DB | **PASS** | ![image2025-2-19_10-58-20.png](attachments/image2025-2-19_10-58-20.png) |
| 3 | idx_cashflow_group_message_cfid_bizversion; | existing in DB | **PASS** | ![image2025-2-19_10-58-24.png](attachments/image2025-2-19_10-58-24.png) |
| 4 | idx_cashflow_group_message_cfid_bizevent; | existing in DB | **PASS** | ![image2025-2-19_10-58-27.png](attachments/image2025-2-19_10-58-27.png) |
| 5 | cashflow_data_jsonb_cashflow_sub_state | existing in DB | **PASS** | ![image2025-2-19_11-5-59.png](attachments/image2025-2-19_11-5-59.png) |
| | cashflow_json_cashflow_id | existing in DB | **PASS** | ![image2025-2-19_11-6-2.png](attachments/image2025-2-19_11-6-2.png) |
| | idx_adaptor_trackingid_status_idx | existing in DB | **PASS** | ![image2025-2-19_11-8-49.png](attachments/image2025-2-19_11-8-49.png) |
| | idx_adaptor_flowid_status_idx | existing in DB | **PASS** | ![image2025-2-19_11-8-52.png](attachments/image2025-2-19_11-8-52.png) |
| | idx_adaptor_message_inboundid_trackingid | existing in DB | **PASS** | ![image2025-2-19_11-8-56.png](attachments/image2025-2-19_11-8-56.png) |