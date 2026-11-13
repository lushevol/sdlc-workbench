CR：CHG0898614

TSK: CTASK1928719

AIG：

# 1.1 Release Work Item:

[Release 11389908 CHG0898614: RATAN Settlement Query Services Upgrade](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11389908)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-query-service | release/v3.2.1 | ![image-2025-11-25_15-40-17.png](attachments/image-2025-11-25_15-40-17.png) ![image-2025-11-25_15-42-18.png](attachments/image-2025-11-25_15-42-18.png) | ![image-2025-11-25_15-39-43.png](attachments/image-2025-11-25_15-39-43.png) | [Pipelines - Run 20251125.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9408420&view=results) | 3.2.1-20251125.5 | [Pull request 2219255: fxu mock api - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2219255) | @Fengke Wu |
| 2 | 51358-ratanone-command | main | N/A | N/A | [Pipelines - Run 20251124.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9374861&view=results) | CHG0888466-20251119.2 | [Pull request 2211347: #10250996 UVT commands for FXU ACK - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command/pullrequest/2211347) | @Fengke Wu |
| 3 | ~~51358-ratan-cash-settlement-query-service~~ | ~~back to original production version~~ | | | ~~[Pipelines - Run 20251125.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9408495&view=results)~~ | ~~3.2.0-[20251125.](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9401904&view=results)6~~ | | ~~@Fengke Wu~~ |
| 4 | 51358-ratanone-ansible | main | | | [Pipelines - Run 20251125.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9410537&view=results) | 3.2.0-20251119.1 | | |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-11-29 | [Story 11359770 [FXU] Mockup API tool for tech release](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11359770) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | mock API version query service version check [uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-query-service/actuator/info](https://uklvapapp590.gdc.standardchartered.com:8868/ratan-cash-settlement-query-service/actuator/info) | 3.2.1-20251125.5 | 3.2.1-20251125.5 | ![image-2025-11-29_9-39-17.png](attachments/image-2025-11-29_9-39-17.png) |
| 2 | MB fxu message: Send to solace: SELECT eh.*, er."content" FROM ratanone.event_history eh, ratanone.event_record er WHERE [eh.id](http://eh.id) = er.event_history_id AND eh.create_timestamp BETWEEN '2025-11-29 00:00:00' AND '2025-11-30 08:00:00' AND eh."comment" LIKE '%settlement-fxu-1%' ORDER BY create_timestamp DESC; Receive from solace: SELECT eh.*, er."content" FROM ratanone.event_history eh, ratanone.event_record er WHERE [eh.id](http://eh.id) = er.event_history_id AND eh.create_timestamp BETWEEN '2025-11-29 00:00:00' AND '2025-11-30 08:00:00' AND eh."comment" LIKE '%settlement-fxu-2%' ORDER BY create_timestamp DESC; | ![image-2025-11-24_16-37-5.png](attachments/image-2025-11-24_16-37-5.png) ![image-2025-11-26_11-27-49.png](attachments/image-2025-11-26_11-27-49.png) | | ![image-2025-11-30_16-29-23.png](attachments/image-2025-11-30_16-29-23.png) ![image-2025-11-30_16-29-43.png](attachments/image-2025-11-30_16-29-43.png) ![image-2025-11-30_16-30-26.png](attachments/image-2025-11-30_16-30-26.png) |
| 3 | query service rollback by ansible pipeline | 3.2.0-20251119.1 | | ![image-2025-11-30_16-40-33.png](attachments/image-2025-11-30_16-40-33.png) |