CR：CHG0834341

TSK: CTASK1789241

AIG：

# 1.1 Release Work Item:

[Release 10176713 CHG0834341: RATAN Settlement enhancement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10176713)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-command | main | | | [Pipelines - Run 20250909.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8077774&view=results) | CHG0834341-20250909.2.zip | @Chongxuan Li |
| 2 | 51358-ratanone-db-repository | main | | | [Pipelines - Run 20250903.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=7988975&view=results) | | @Fengke Wu |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |

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
| Performance of submit/approve for 1000 cashflow operations | 1, 1000 cashflows in a single batch and verifying the checker under 20 core threads 2, 20 batches, and verify the checker under 50 core threads and 4 database connections | [Bulk Approve performance check result - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Bulk+Approve+performance+check+result) |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-09-13 | [cn-release-20250913 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/e689ea9f-8290-4d7f-86c8-340215590c82/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Check logs and search for "can't be stamping since input with error: settlementMethod must not be blank", level is ERROR: <u>Discover - Elastic</u> | No such errors after deployed | No errors | |
| 2 | Check ssi stamping service version: [uklvadrat0001a.pi.dev.net:37443/actuator/info](https://uklvadrat0001a.pi.dev.net:37443/actuator/info) | 2.5.1-20250815.1 | - [x] Correct | |
| 3 | PSS login 590p server cd /share/imft054/ratanone/aspire | 51358-ratan-HK_Aspire_Dummy.txt 51358-ratan-TH_Aspire_Dummy.txt 51358-ratan-TW_Aspire_Dummy.txt do not exist | | |
| 4 | Check the log | Send message to FileIT successfully | | |
| | BAU job for HK/ TW/ TH | | | pire received files: |
| | RATAN logs for ssi UVT | all success | Successfully stamped | |
| 1 | DB-repo | | | ![image-2025-9-13_9-24-9.png](attachments/image-2025-9-13_9-24-9.png) ![image-2025-9-13_9-24-28.png](attachments/image-2025-9-13_9-24-28.png) ![image-2025-9-13_9-28-40.png](attachments/image-2025-9-13_9-28-40.png) |