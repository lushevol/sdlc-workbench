CR：CHG0743309

TSK: CTASK1562583

AIG：

# 1.1 Release Work Item:

[Release 8402774 Settlement Enhancement CHG0743309 for 21th June](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8402774)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | main | NA | NA | [Pipelines - Run 20250612.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=6637279&view=results) | CHG0743309-20250612.2.zip CHG0743309_Rollback-20250612.3.zip | @Chongxuan Li |

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
| CN | 2025-06-21 | [cn-release-20250621 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/3e8f0d06-5e22-40a6-b3fd-75a3610854b2/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | SELECT x.* FROM ratanone_swift_service.swift_static_udf_swf_ls x WHERE x.k_currency IN ('XG7'); | 1 record in total ![image-2025-6-12_10-20-31.png](attachments/image-2025-6-12_10-20-31.png) | | ![image-2025-6-21_9-22-18.png](attachments/image-2025-6-21_9-22-18.png) |
| 2 | SELECT x.* FROM ratanone_swift_service.swift_static_udf_strategy x WHERE x.k_strategy IN ('COM_BDF_DELIV_S','COM_BOE_DELIV_S','COM_LDN_DVP','COM_ZRH_DELIV_S'); | 4 records in total ![image-2025-6-12_10-20-41.png](attachments/image-2025-6-12_10-20-41.png) | | ![image-2025-6-21_9-22-40.png](attachments/image-2025-6-21_9-22-40.png) |
| 3 | select * from ratanone.ratan_static__cashflow_ebbs_bridge_account rsceba where id = '43'; | ![](https://confluence.global.standardchartered.com/download/attachments/3360145584/image-2025-6-11_14-29-22.png?version=1&modificationDate=1749623362000&api=v2) | | ![image-2025-6-21_9-24-16.png](attachments/image-2025-6-21_9-24-16.png) |
| 4 | | | | |