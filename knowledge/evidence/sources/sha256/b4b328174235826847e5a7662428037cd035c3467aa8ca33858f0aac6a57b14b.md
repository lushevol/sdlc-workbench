CR：CHG1022603

TSK: [CTASK2179644](https://scbnow01.service-now.com/change_task.do?sys_id=430e6242fbb18390b250fd284eefdc17&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3Db1eda28efb718390b250fd284eefdcd4%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 14760869 CHG1022603: Korea MQ config and OLTP/Enisis UVT](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14760869)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-command | main | NA | NA | [OLTP_Debit：](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13347733&view=results)[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390131&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390131&view=results) OLTP_Credit：[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390134&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390134&view=results) [ENISIS-MT210：](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13376676&view=results)[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390137&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390137&view=results) ENISIS-pacs009：[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390138&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390138&view=results) ENISIS-pacs008：[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390140&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13390140&view=results) | | [Pull request 3008692: #14165086 oltp/enisis uvt - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command/pullrequest/3008692) | @Yonghua Li |
| 2 | 51358-ratanone-ansible | main | NA | NA | OLTP_ACK：[Pipelines - Run 20260707.8](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13373107&view=results) ENISIS_MX_ACK：[Pipelines - Run 20260707.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13374840&view=results) ENISIS_MT_ACK：[Pipelines - Run 20260707.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13374888&view=results) | | [Pull request 3001429: #11839497 query kafka message - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible/pullrequest/3001429) | @Yonghua Li |
| 3 | 51358-ratanone-db-repository | develop | NA | NA | ENISIS_MX: [Pipelines - Run 20260706.14](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13347190&view=results) MX_SWITCH_OFF: [Pipelines - Run 20260706.15](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13347241&view=results) | | [Pull request 3007937: #13666667 modify korea enisis mx config - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/3007937) | @Yonghua Li |
| 4 | 51358-ratanone-db-repository | develop | NA | NA | [Pipelines - Run 20260706.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13342716&view=results) MQ_SWITCH_OFF: [Pipelines - Run 20260706.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13342870&view=results) | | [Pull request 3001012: #14779459: Add new MQ for Korea - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/3001012) | @Chen Yang |
| 5 | 51358-ratanone-service_stop | main | | | [Pipelines - Run 20260707.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13375846&view=results) | | | @Zeyu Zhou |
| 6 | 51358-ratanone-service_start | main | | | [Pipelines - Run 20260707.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13375971&view=results) | | | @Zeyu Zhou |
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
| CN | 2026-07-11 | | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Korea MQ Flow | six datas about korea mq | pass | ![image-2026-7-12_19-28-16.png](attachments/image-2026-7-12_19-28-16.png) |
| 2 | message_format forenisis mx flow | message_format is xml | pass | ![image-2026-7-12_19-31-19.png](attachments/image-2026-7-12_19-31-19.png) |
| 3 | | | | |