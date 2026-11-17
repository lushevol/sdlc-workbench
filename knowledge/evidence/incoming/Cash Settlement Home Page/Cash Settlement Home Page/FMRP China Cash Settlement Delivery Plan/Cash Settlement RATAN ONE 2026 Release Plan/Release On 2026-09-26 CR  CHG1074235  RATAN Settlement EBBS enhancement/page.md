CR：CHG1074235

TSK:  [CTASK2280204](https://scbnow01.service-now.com/change_task.do?sys_id=8d284ddc3bd70754f6935d0b16e45a0c&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3Dabe74d5c3bd70754f6935d0b16e45a14%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 16153066 CHG1074235: RATAN settlement EBBS](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16153066)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | | | [Pipelines - Run 20260914.5](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14923448&view=results) rollback pipeline: [Pipelines - Run 20260923.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15141338&view=results) | | [Pull request 3289436: #15971650: Add Indonesia ebbs ack flow - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/3289436) | @Haolin Song |
| 2 | 51358-solace-appconfig-deploy | main | NA | NA | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15099727&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15099727&view=results) | 51080-appconfig-main_20260921.16.tgz vpn-cb-transactions-51358-ratan-1.yaml | [Pull request 3296591: Feature/16044702 promote - Repos](https://dev.azure.com/sc-ado/TTOQPR/_git/51080-appconfig/pullrequest/3296591) | @Xinmiao Huang |
| 3 | 51358-ratanone-command | develop | NA | NA | [Pipelines - Run 20260921.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15073184&view=results) | NA | [Pull request 3365862: #15971650: dummy Indonesia ebbs message - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command/pullrequest/3365862?_a=files) [Pull request 3374416: #15971650: change to new api for dummy Indonesia ebbs message - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command/pullrequest/3374416?_a=files) | @Haolin Song |
| 4 | 51358-ratanone-service_stop | | | | [Pipelines - Run 20260924.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15171526&view=results) | | | |
| 5 | 51358-ratanone-service_start | | | | [Pipelines - Run 20260924.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15171529&view=results) | | | |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-09-26 | [Story 15943533 Indonesia RATAN implementation - EBBS ack flow onboard to GDC](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15943533) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| | | | | ![image-2026-9-27_8-58-48.png](attachments/image-2026-9-27_8-58-48.png) |
| | | | | ![image-2026-9-27_8-58-24.png](attachments/image-2026-9-27_8-58-24.png) |
| | | | | |
| | | | | |