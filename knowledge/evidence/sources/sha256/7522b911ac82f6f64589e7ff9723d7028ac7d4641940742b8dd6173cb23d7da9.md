CR：CHG0820869

TSK: [CTASK1760807](https://scbnow01.service-now.com/change_task.do?sys_id=a206952dfb1be214dc16fed08eefdc5d&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3D3f7215e5fb97e214dc16fed08eefdc77%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 9867505 CHG0820869: Aspire Connection Test](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9867505)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-ssi-stamping-service | release/v2.5.1 | ![image-2025-8-15_9-59-30.png](attachments/image-2025-8-15_9-59-30.png) | ![image-2025-8-15_9-59-2.png](attachments/image-2025-8-15_9-59-2.png) | [Pipelines - Run 20250815.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7700643&view=results) | 2.5.1-20250815.1 | @Quill Li |
| 2 | 51358-ratanone-ansible | main | NA | NA | [Pipelines - Run 20250812.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7638430&view=results) | NA | @Zeyu Zhou |

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
| CN | 2025-08-16 | [cn-release-20250816 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query-edit/fcd5d35b-ec23-4c84-9bd5-8733dcdf3f73/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Check logs and search for "can't be stamping since input with error: settlementMethod must not be blank", level is ERROR: <u>Discover - Elastic</u> | No such errors after deployed | No errors | ![image-2025-8-16_11-38-43.png](attachments/image-2025-8-16_11-38-43.png) |
| 2 | Check ssi stamping service version: [uklvadrat0001a.pi.dev.net:37443/actuator/info](https://uklvadrat0001a.pi.dev.net:37443/actuator/info) | 2.5.1-20250815.1 | - [x] Correct | ![image-2025-8-16_9-54-14.png](attachments/image-2025-8-16_9-54-14.png) |
| 3 | PSS login 590p server cd /share/imft054/ratanone/aspire | 51358-ratan-HK_Aspire_Dummy.txt 51358-ratan-TH_Aspire_Dummy.txt 51358-ratan-TW_Aspire_Dummy.txt do not exist | | ![image-2025-8-16_11-20-17.png](attachments/image-2025-8-16_11-20-17.png) |
| 4 | Check the log | Send message to FileIT successfully | | ![image-2025-8-16_11-24-41.png](attachments/image-2025-8-16_11-24-41.png) |
| | BAU job for HK/ TW/ TH | | | ![image-2025-8-16_11-51-55.png](attachments/image-2025-8-16_11-51-55.png) Aspire received files: ![image-2025-8-16_11-52-27.png](attachments/image-2025-8-16_11-52-27.png) |
| | RATAN logs for ssi UVT | all success | Successfully stamped | ![image-2025-8-16_13-1-38.png](attachments/image-2025-8-16_13-1-38.png) |