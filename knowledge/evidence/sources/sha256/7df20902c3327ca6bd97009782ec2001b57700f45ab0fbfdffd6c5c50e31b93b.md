CR：CHG0888466

TSK: CTASK1906613

AIG：

# 1.1 Release Work Item:

[Release 10475786 CHG0821842: RATAN Settlement MB Upgrade](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10475786)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-message-bridge | release/v5.0.0 | ![image-2025-11-12_16-21-20.png](attachments/image-2025-11-12_16-21-20.png) | ![image-2025-11-12_16-20-40.png](attachments/image-2025-11-12_16-20-40.png) | [Pipelines - Run 20251112.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9162212&view=results) | 5.0.0-20251112.2 | [Pull request 2054162: enhancement for uber - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-message-bridge/pullrequest/2054162) | @Yonghua Li |
| 2 | 51358-ratanone-db-repository | main | N/A | N/A | [Pipelines - Run 20251118.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9265867&view=results) | ratanone-db-repository-20251118.9 | [Pull request 2181273: message-bridge add sql - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2181273) | @Yonghua Li |
| 3 | 51358-ratanone-db-repository | main | N/A | N/A | FXU2RT：[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9306634&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9306634&view=results) | ratanone-db-repository-20251119.21 | [Pull request 2214052: add rb sql - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2214052) | @Yonghua Li |
| 4 | 51358-ratanone-db-repository | main | N/A | N/A | RT2FXU：[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9306950&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9306950&view=results) | ratanone-db-repository-20251119.22 | [Pull request 2214052: add rb sql - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2214052) | @Yonghua Li |
| 5 | 51358-ratanone-db-repository | main | N/A | N/A | UBER2RT：[https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9307072&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9307072&view=results) | ratanone-db-repository-20251119.23 | [Pull request 2214052: add rb sql - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-db-repository/pullrequest/2214052) | @Yonghua Li |
| 6 | 51358-ratanone-command | develop | N/A | N/A | [Pipelines - Run 20251119.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9291488&view=results) | CHG0888466-20251119.2 | [Pull request 2211347: #10250996 UVT commands for FXU ACK - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-command/pullrequest/2211347?_a=files&path=/CRs/CHG0888466/send_fxu_ack_dummy_message.yaml) | @Fengke Wu |
| 7 | 51358-ratanone-ansible_opensearchEnhance | | | | [Pipelines - Run 20251118.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9276747&view=results) | | | @Zeyu Zhou |
| 8 | 51358-ratanone-ansible_clusterRestartDeploy | | | | [Pipelines - Run 20251120.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9317692&view=results) | | | @Zeyu Zhou |
| 9 | 51358-ratanone-ansible_clusterRestartRollback | | | | [Pipelines - Run 20251119.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9298663&view=results) | 20250617.2 | | @Zeyu Zhou |
| 10 | 51358-ratan-service-properties | master | N/A | N/A | [Pipelines - Run 20251113.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9183259&view=results) | 20251113.1 | [Pull request 2126804: #5362379: change opensearch access password - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2126804) | @Song Wan |
| 11 | 51358-ratanone-service | master | N/A (restart agent) | N/A | [Pipelines - Run 20251118.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9275845&view=results) | | | @Zeyu Zhou |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-11-22 | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7881144](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7881144) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | Execute SQL to check database configuration SQL： select * from ratanone.ratan_bridge_flow where id in ('dksjsh39-4b4f-4088-b161-0odkcj4h3214','sod0fk3s-16a4-47db-ad23-40dksk39j5fd','sodjz12r-a74e-44bc-9169-423ofskw5039','0kdj4uss-a973-4b82-be64-fosd9v9ckxjd','75f8a63a-7253-4d13-cba4-d9516fcda344','e648a927-5244-4b77-815a-64eda9ab2e89','75f8a63a-7299-4d13-cba4-d9516fcda345', 'e648a927-5299-4b77-815a-64eda9ab2f89'); select * from ratanone.ratan_bridge_filter where id in ('7efeb888-ae30-46f8-b9ad-c473bd3e4305'); select * from ratanone.ratan_bridge_flow_filter_status where id in ('e230b135-5d4a-4191-990b-67956596c104'); | ratan_bridge_flow: eight records was retrieved; ratan_bridge_filter: one record was retrieved; ratan_bridge_flow_filter_status: one record was retrieved; | | |
| 2 | Eureka check service version | 5.0.0-20251112.2 | | |
| 3 | check uber flow log | current flow name: uber-flow | | |
| 4 | check uber suppression log | json body suppression processor starts with flow: [uber-flow] | | |
| 5 | check fxu flow log | | | ![image-2025-11-22_19-30-36.png](attachments/image-2025-11-22_19-30-36.png) ![image-2025-11-22_19-34-32.png](attachments/image-2025-11-22_19-34-32.png) |