CR：CHG1006731

TSK: [CTASK2147407](https://scbnow01.service-now.com/change_task.do?sys_id=6bd1a0c7fb51c3d8b250fd284eefdcc5&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3Dee812403fb51c3d8b250fd284eefdc39%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 14315682 CHG1006731: Korea OLTP UVT](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14315682)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | NA | NA | SG_DUMMY：[Pipelines - Run 20260610.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12782878&view=results) （optional） MB_SWITCH_OFF：[Pipelines - Run 20260610.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12782903&view=results) | | | @Yonghua Li |
| 2 | 51358-ratanone-command | develop | NA | NA | [OLTP_PAY:Pipelines - Run 20260610.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12782963&view=results) OLTP_RECEIVE: [Pipelines - Run 20260610.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12782976&view=results) | | | @Yonghua Li |
| 3 | 51358-ratanone-service_start | main | NA | NA | [Pipelines - Run 20260610.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12788031&view=results) | | | @Zeyu Zhou |
| 4 | 51358-ratanone-service_stop | mian | NA | NA | [Pipelines - Run 20260610.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12787985&view=results) | | | @Zeyu Zhou |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |
| 9 | | | | | | | | |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-06-13 | [Story 13719470 [FMRP 8.0] Production Uber to be tested in test envrionment](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13719470) [Story 11839497 [Korea]Integration for OLTP via Solace Korea](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11839497) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | sg target flow | 1 flow row | ![image-2026-6-13_11-32-58.png](attachments/image-2026-6-13_11-32-58.png) | |
| 2 | sg flow fliter | 1 filter row | ![image-2026-6-13_11-33-7.png](attachments/image-2026-6-13_11-33-7.png) | |
| 3 | kafka topic | | ![image-2026-6-13_12-13-31.png](attachments/image-2026-6-13_12-13-31.png) | |