CR：CHG0582263

TSK: CTASK1244505

AIG：

# 1.1 Release Work Item:

[Release 5631796 RATAN CN Sep 21th CHG0582263 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5631796)

# 1.2 Packages

| | Service | Branch | Hashicorp Enabled | Vulnerability Report Summery Screenshot | ADO release pipeline | Package Version | Rollback Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-message-bridge | release/v4.0.2 | true | ![image2024-9-12_16-26-50.png](attachments/image2024-9-12_16-26-50.png) | [Pipelines - Run 20240912.1 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3301778&view=results) | 4.0.2-20240912.1 | 4.0.0-20240730.3 | @Pengpeng Li |
| 2 | 51358-mfe-trades | release/v1.8.2 | NA | ![image2024-9-18_13-10-0.png](attachments/image2024-9-18_13-10-0.png) | [Pipelines - Run 20240918.8 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3363842&view=results) | 1.8.2-adhoc-20240918.8 | 1.7.6-production-20240827.8 | @Liang Zhang |
| 3 | db repo | | | | | CHG0582263-20240918.2 | CHG0582263_Rollback-20240918.3 | @Chen Yang |
| 4 | | | | | | | | |

# 1.3 Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [x] DM | Test Progress - [x] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2024-09-21 | [Story 5557243 Cashflow stuck in Group Pending for edge case (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5557243) [Story 5402371 MB defect when message filtered kafka offset not commit (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5402371) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff (regression only):** 📎 [RE Message bridge need verify in UAT1.msg](attachments/RE Message bridge need verify in UAT1.msg) | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |
| Trade Control | 2024-09-21 | [Story 4371642 [Trade Blotter] - User can get Multi Fees cashflows in Payment schedule other cashflow (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/4371642) [Story 4864676 [Trade Blotter] - User can get Multi Fee in trade ticket and Amendment version compare (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/4864676) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |