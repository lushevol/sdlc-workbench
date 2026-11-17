CR：CHG1018363

TSK: [CTASK2170770](https://scbnow01.service-now.com/change_task.do?sys_id=41628b4c3b31c314f6935d0b16e45ad9&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3D5532c30c3b31c314f6935d0b16e45ac9%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 14641155 CHG1018363: RATAN Settlement enhancement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14641155)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-stamping-service | release/v3.0.6 | ![image-2026-7-2_17-18-54.png](attachments/image-2026-7-2_17-18-54.png) | ![image-2026-7-2_17-21-26.png](attachments/image-2026-7-2_17-21-26.png) | [Pipelines - Run 20260702.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13281713&view=results) | [3.0.6-20260702.3](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/ratan/ratanone-stamping-service/3.0.6-20260702.3/) | [Pull request 2497886: Add new api to query ssi daily usage by payment date - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-stamping-service/pullrequest/2497886) | @Haolin Song |
| 2 | 51358-ratanone-service_stop | | | | [Pipelines - Run 20260713.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13503866&view=results) | | | |
| 3 | 51358-ratanone-service_start | | | | [Pipelines - Run 20260713.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13503926&view=results) | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |
| 9 | | | | | | | | |
| 10 | | | | | | | | |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-08-01 | [Story 12068962 [Dormant SSI processing] RATAN Cash Settlement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12068962) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | 10:30 AM SGT, SSI+ PSS will hit the APIs using curl command to perform UVT to ensure we get the response and the data is consumed by SSI+. ![image-2026-7-16_19-26-4.png](attachments/image-2026-7-16_19-26-4.png) | | | |
| | | | | |
| | | | | |
| | | | | |