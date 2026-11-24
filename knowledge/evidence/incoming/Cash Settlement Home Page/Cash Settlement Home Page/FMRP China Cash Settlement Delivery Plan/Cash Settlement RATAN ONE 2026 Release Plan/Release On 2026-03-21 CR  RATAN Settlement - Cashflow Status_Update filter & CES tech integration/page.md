CR：CHG0912513

TSK: CTASK1958540

AIG：

# 1.1 Release Work Item:

[Release 11612390 CHG0912513: RATAN Settlement Upgrade](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11612390)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-opensearch-agent | release/v1.0.1 | [![image-2026-3-10_9-55-5.png](attachments/image-2026-3-10_9-55-5.png)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10281007&view=secops1.sc-security-extensionPROD.build-summary-report-tab) | ![image-2026-3-10_9-54-26.png](attachments/image-2026-3-10_9-54-26.png) | [Pipelines - Run 20260318.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11059787&view=results) | 1.0.1-20260318.4 | [Pull request 2542100: #2036027:fix version conflict and critical security issue - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-opensearch-agent/pullrequest/2542100) | @zhang jiangnan @Chen Yang |
| 2 | 51358-ratanone-service (Stop agent) | main | NA | NA | [Pipelines - Run 20260330.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11294631&view=results) | main | | @Zeyu Zhou |
| 3 | 51358-ratanone-ansible_opensearchEnhancement | main | OpenSearch REST APIs & Command of removing opensearch old consumer group 1. Opensearch cashflow historical data cleanup 2. Opensearch consumer group removal on topic "OPENSEARCH.INBOUND.CASHFLOW" 3. ccr restart | NA | [Pipelines - Run 20260330.9](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11302815&view=results) | main | [Pull request 2590493: 4th April Release - FSS Collare - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible/pullrequest/2590493?path=/ansible/cloud_env_setup.yaml&_a=files) | @Zeyu Zhou @zhang jiangnan |
| 4 | ~~51358-ratan-cash-settlement-group-management-service~~ ~~(Cashflow event filter)~~ | ~~release/v2.2.6~~ | ~~![image-2026-3-5_11-23-17.png](attachments/image-2026-3-5_11-23-17.png)~~ | ~~![image-2026-3-5_11-24-11.png](attachments/image-2026-3-5_11-24-11.png)~~ | ~~[Pipelines - Run 20260128.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10195832&view=results)~~ ~~[Pipelines - Run 20260305.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10792382&view=results)~~ | ~~2.2.6-20260305.1~~ | ~~[Pull request 2359895: #11894910 adding filtering logic for cashflow Status_Update from STELLA - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/2359895?path=/src/main/java/com/scb/ratan/cashflow/infra/feign/CashflowService.java)~~ | ~~@Chongxuan Li ~~ |
| 5 | ~~ratan-service-properties~~ | ~~staging-master~~ ~~master~~ | ~~N/A~~ | ~~N/A~~ | ~~[Pipelines - Run 20260202.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10282893&view=results)~~ ~~[Pipelines - Run 20260305.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10792972&view=results)~~ ~~[Pipelines - Run 20260306.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10829562&view=results)~~ | ~~N/A~~ | ~~[Pull request 2390419: #7177438: updated CES prod config - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2390419)~~ ~~[Pull request 2390484: #7177438: updated CES prod config - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties/pullrequest/2390484)~~ | ~~@Quill Li ~~ |
| 6 | ~~51358-ratanone-auth-server~~ | ~~release/v3.0.7~~ | ~~![image-2026-2-2_20-47-54.png](attachments/image-2026-2-2_20-47-54.png)~~ | ~~![image-2026-2-2_20-48-22.png](attachments/image-2026-2-2_20-48-22.png)~~ | ~~[Pipelines - Run 20260202.7](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10279917&view=results)~~ ~~[Pipelines - Run 20260305.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10792036&view=results)~~ | ~~3.0.7-[20260305.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10792036&view=results)~~ | | ~~@Quill Li ~~ |
| 7 | ~~51358-mfe-cashflow-blotter ~~ | ~~[release/v1.40.0](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter?version=GBrelease/v1.40.0)~~ | ~~![image-2026-2-27_15-24-32.png](attachments/image-2026-2-27_15-24-32.png)~~ | ~~![image-2026-2-27_15-22-41.png](attachments/image-2026-2-27_15-22-41.png)~~ | ~~[Pipelines - Run 20260312.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10933678&view=results)~~ | ~~1.40.0-v1.40.0-20260312.6~~ | ~~[Pull request 2382640: open search - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter/pullrequest/2382640)~~ ~~[Pull request 2468044: Enhance type - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter/pullrequest/2468044)~~ | ~~@Guiling Wang ~~ |
| 8 | ~~51358-ratan-cash-settlement-query-service ~~ | ~~release/v3.2.5~~ ~~（This release is not necessary since CES tech go live delayed）~~ ~~release/v3.2.6~~ ~~(CES disabled)~~ | ~~![image-2026-2-3_0-9-33.png](attachments/image-2026-2-3_0-9-33.png)~~ | ~~![image-2026-2-3_0-9-50.png](attachments/image-2026-2-3_0-9-50.png)~~ | ~~[Pipelines - Run 20260202.12](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10282742&view=results)[Pipelines - Run 20260202.14](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10282984&view=results)~~ ~~[Pipelines - Run 20260305.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10791839&view=results)~~ | ~~3.2.5-[20260202.12](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10282742&view=results)~~ ~~3.2.6-[20260305.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10791839&view=results)~~ | ~~[Pull request 2390697: CES integration - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2390697)~~ ~~[Pull request 2391408: #7177438: disable CES and this will fallback to previous impl - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2391408)~~ ~~[Pull request 2483194: Sync 3.2.5 change - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2483194)~~ | ~~@Quill Li ~~ ~~@zhang jiangnan @Xinmiao Huang ~~ |
| 9 | ~~51358-mfe-admin-module~~ | ~~release/v1.2.0~~ | ~~![image-2026-1-30_13-20-54.png](attachments/image-2026-1-30_13-20-54.png)~~ | ~~![image-2026-1-30_13-20-30.png](attachments/image-2026-1-30_13-20-30.png)~~ | ~~[Pipelines - Run 20260305.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10792308&view=results)~~ | ~~[20260305.](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=10239531&view=results)1~~ | ~~[Pull request 2382655: add cashflow blotter for open search - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-admin-module/pullrequest/2382655)~~ | ~~@Guiling Wang ~~ |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-04-04 | [cn-release-20260207 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/35e597b9-4773-43da-bc4f-a6ccafab3127/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| 1 | check fmo-cashflow bottler [opensearch] | have normal data | pass | ![image-2026-4-10_17-18-50.png](attachments/image-2026-4-10_17-18-50.png) |
| 2 | | | | |
| 3 | | | | |