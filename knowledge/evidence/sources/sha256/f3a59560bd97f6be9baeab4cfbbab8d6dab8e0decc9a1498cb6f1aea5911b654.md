CR：CHG0872414

TSK: [CTASK1872574](https://scbnow01.service-now.com/change_task.do?sys_id=86ec44303b38ba507b50390eb3e45aea&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3D86ac0c7c3bf4ba507b50390eb3e45ab0%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 10932677 2025-11-01 CR: RATAN Settlement Enhancement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10932677)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-static-data-service | release/v3.6.4 | ![image-2025-10-23_10-36-39.png](attachments/image-2025-10-23_10-36-39.png) ![image-2025-10-23_10-37-54.png](attachments/image-2025-10-23_10-37-54.png) | ![image-2025-10-23_10-21-36.png](attachments/image-2025-10-23_10-21-36.png) | [Pipelines - Run 20251023.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8805015&view=results) | 3.6.3-20251023.1 | [Pull request 2106123: #7530684 add SGO-SGD mapping - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/2106123) | @Chongxuan Li |
| 2 | 51358-RATAN-W-ControlM-RAT | main | | | [Pipelines - Run 20251027.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8859811&view=results) | | | @Jie Cai |
| 3 | 51358-ratanone-service_stopServices | main | | | [Pipelines - Run 20251028.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8881890&view=results) | | | @Zeyu Zhou |
| 4 | 51358-ratanone-service_restartServices | main | | | [Pipelines - Run 20251028.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8881992&view=results) | | | @Zeyu Zhou |
| 5 | | | | | | | | |
| 6 | | | | | | | | |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-09-20 | [cn-release-20251101 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/ffd961ea-3f03-458e-95c4-254c3e4bc4d6/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | check service version | 3.6.3-20251023.1 | PASS | ![image-2025-11-1_9-17-43.png](attachments/image-2025-11-1_9-17-43.png) |
| | | | | |
| | | | | |
| | | | | |