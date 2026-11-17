CR：CHG1003764

TSK: [CTASK2140957](https://scbnow01.service-now.com/change_task.do?sys_id=65158b9d0fd94f184294b2e800d1b296&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3Debb387190f994f184294b2e800d1b2bd%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 13464514 RATAN Settlement FMRP8.0 Go-Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13464514)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-mxg-cashflow-adaptor | release/v3.0.1.2 | ![image-2026-8-31_16-3-29.png](attachments/image-2026-8-31_16-3-29.png) | ![image-2026-8-31_15-5-51.png](attachments/image-2026-8-31_15-5-51.png) | [Pipelines - Run 20260831.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14610242&view=results) | 3.0.1.2-20260831.9 | [Pull request 3264651: #12660021: Korea trade auto comp - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-mxg-cashflow-adaptor/pullrequest/3264651?path=/src/main/java/com/scb/ratan/cashflowadaptor/domain/pocessor/KoreaTradeConfirmationProcessor.java) | @Chen Yang |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-09-05 | [Story 12660021 [Korea]Comp status to drive STP process](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12660021) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| | Check the link [uklvapapp590.gdc.standardchartered.com:8868/ratan-mxg-cashflow-adaptor/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-mxg-cashflow-adaptor/actuator/info) | Version should be 3.0.1.2-20260831.7 | | |
| | After deployment Murex will send UVT trade | Trade will persist in group service | | |
| | | | | |
| | | | | |