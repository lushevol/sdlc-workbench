CR：CHG1018358

TSK: [CTASK2170762](https://scbnow01.service-now.com/change_task.do?sys_id=461143403b31c314f6935d0b16e45a33&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3Df2e0cbcc3bfd8314f6935d0b16e45a5a%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 14641062 CHG1018358: RATAN Settlement Uber phase 2](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14641062)

# 1.2 Packages

| | Service | Branch | Scope | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ratanone-message-bridge | | stop/start | | | | | | @Zeyu Zhou |
| 2 | 51358-ratanone-db-repository | develop | 1. 1 queue → 7 queue 2. filter change | | | UBER_SPLIT: [Pipelines - Run 20260716.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13590401&view=results) [UBER_SWITCH_OFF:](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13532823&view=results) [Pipelines - Run 20260716.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13590426&view=results) | | [Pull request 2977223: #13423904 uber queue split - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2977223) | @Yonghua Li |
| 3 | ratan-cash-settlement-group-management-service | release/v3.0.12 | 1. Consumer 1→ 8 on uber 2. Enhance API downgrading process | **![image-2026-7-20_13-30-13.png](attachments/image-2026-7-20_13-30-13.png)** | ![image-2026-7-20_13-30-51.png](attachments/image-2026-7-20_13-30-51.png) | [Pipelines - Run 20260720.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13656091&view=results) | 3.0.12-20260720.1 | [Pull request 2987346: uber kafka topic change to 7 and enhance uber consume - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/2987346) [Pull request 3042968: fix vulnerability - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/3042968) | @Yonghua Li |
| 4 | ratanone-ansible | main | Change the number of topic partitions to 12 | | | UBER_PARTITION: [Pipelines - Run 20260714.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13520328&view=results) | ansible-20260714.2 | [Pull request 3041848: Batch creation of Kafka topics and modification of partition numbers - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible/pullrequest/3041848) | @Yonghua Li |
| 5 | | | | | | | | | |
| 6 | | | | | | | | | |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| Uber queue split PT | The consumption performance of the split queue | [Uber queue Spliting PT - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Uber+queue+Spliting+PT) |
| Uber topic split PT | group service consumes uber messages from split topic | [Release On 2026-08-01 CR: RATAN Settlement Korea & FMRP FXO Tech Go-Live] |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-07-25 | [cn-release-20260725 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query-edit/8b11c877-e754-4a75-804d-cc300a3375fc/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | query flow select * from ratanone.ratan_bridge_flow where flow_name in('uber-flow') order by flow_name desc, route_id asc; | ![image-2026-7-24_14-44-22.png](attachments/image-2026-7-24_14-44-22.png) | pass | ![image-2026-7-26_16-10-42.png](attachments/image-2026-7-26_16-10-42.png) |
| 2 | query filter select rbf.flow_name, rbf.route_id, rbf.route_name , rbf.route_type, rbf.route_topic, f.* from ratanone.ratan_bridge_filter f, ratanone.ratan_bridge_flow rbf where rbf.id = f.flow_id and rbf.flow_name in('uber-flow') order by rbf.flow_name desc, rbf.route_id asc; | ![image-2026-7-24_14-45-22.png](attachments/image-2026-7-24_14-45-22.png) | pass | ![image-2026-7-26_16-10-54.png](attachments/image-2026-7-26_16-10-54.png) |
| 3 | query trade event select eh.*, er."content" from ratanone.event_history eh, ratanone.event_record er where eh.id = er.event_history_id and eh.trade_id in('7700172646','5815968769','6564762190','5971248834','6222273506','7278072775','8527866967') order by eh.create_timestamp desc ; | | | |
| 4 | | | | |

6. UVT Step

1. MB receives Uber messages from upstream.

2. It searches the MB logs using keywords such as "fx-spot" (queue name) and the keyword "receives message".

3. The searched logs are used as the sign-off.