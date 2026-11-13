#

# ADO task list

[ID tasks - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/6ed268c6-16e8-4272-af93-3ea129e6029c/)

# Development Plan(Prod Readiness)

<details>
<summary>Expand Details</summary>

| | Category | Task Description | Owner | Nginx LB server Status | App Server Status | Request CR/Detail Infomation | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DevOps | Infra – VIP | @Zeyu Zhou | | | | discuss with nginx team |
| 2 | Infra – DNS (Depends on VIP) | @Zeyu Zhou | server DNS manifest (in progressing, web team working) | app server DNS not require | | |
| 3 | Infra – Firewall (Depends on VIP) | @Zeyu Zhou | | | | if other server visit us, use our own nginx or the lb nginx |
| 4 | Infra – SSL cert, Keystore & truststore? | @Zeyu Zhou | | | | |
| 5 | Infra – NAS | @Zeyu Zhou | | | | wait after OAT, is fileIT still depends on NAS? data sync on GDC Kafka needed? pending on DR solution. |
| 6 | foundation setup – PG | @Zeyu Zhou | - | | | waiting for SAT/OAT stop, account setup |
| 7 | Auth – Hashicorp integration | @Zeyu Zhou | - | | | only db account, waiting for PG setup |
| 8 | foundation setup – Redis(manual) | @Zeyu Zhou | - | | | |
| 9 | foundation setup – Kafka(manual) | @Zeyu Zhou | - | | | |
| 10 | foundation setup – ELK(manual) | @Zeyu Zhou | - | | | |
| 11 | foundation setup – Nginx | @Zeyu Zhou | - | | | lb ansible |
| 12 | Service deployment | @Zeyu Zhou | - | | | |
| 13 | Generic service account creation | | - | | | |
| 14 | Entra integration (FMAA) ? not now | @Zeyu Zhou | - | | | |
| 15 | ADO – CICD get ready for both foundation component and microservices | @Zeyu Zhou | - | | | |
| 16 | BE dev | New solace topic + queue for Murex cashflow inbound | @Xinmiao Huang @Junli Gao | | | | |
| 17 | SSI+ engagement for new solace queue creation | @Xinmiao Huang | | | | |
| 18 | RDM FileIT engagement | @Xinmiao Huang | | | | |
| 19 | RDM real time message solace queue creation | @Xinmiao Huang | | | | |
| 20 | Service properties setup (depends on foundation setup ready) | @Xinmiao Huang | | | | |
| 21 | API gateway development – region validation | @Xinmiao Huang | | | | |
| 22 | API gateway and auth server combination | @Xinmiao Huang | | | | |

</details>

# Development Plan(Non-Prod Readiness)

Refer to ADO: [RATAN Settlement Indonesia Onshore (SQUAD) Onshore Sprint 2 Taskboard - Boards](https://dev.azure.com/sc-ado/FMQPR/_sprints/taskboard/RATAN%20Settlement%20Indonesia%20Onshore%20(SQUAD)/FMQPR/RATAN%20Settlement%20Indonesia%20Onshore%20(SQUAD)/Onshore%20Sprint%202)

<details>
<summary>Expand Details</summary>

| | Category | Task Description | Owner | Dev Status | UAT Status | Staging Status | Man day | Request CR/Detail Infomation | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DevOps | Infra – VIP | @Zeyu Zhou | | | | 15 | [https://scbnow01.service-now.com/onesc?id=ticket&table=sc_req_item&sys_id=b0780dc12b9c4b90c570febbec91bf0e&view=sp](https://scbnow01.service-now.com/onesc?id=ticket&table=sc_req_item&sys_id=b0780dc12b9c4b90c570febbec91bf0e&view=sp) | |
| 2 | Infra – DNS (Depends on VIP) | @Zeyu Zhou | | | | 15 | | |
| 3 | Infra – Firewall (Depends on VIP) | @Zeyu Zhou | | | | 15 | | |
| 4 | Infra – SSL cert, Keystore & truststore? | @Zeyu Zhou | | | | 15 | | |
| 5 | Infra – NAS | @Zeyu Zhou | | | | TBC | | |
| 6 | foundation setup – PG | @Zeyu Zhou | | | | | | |
| 7 | Auth – Hashicorp integration | @Zeyu Zhou | | | | | DEV： [My Request - RITM4503433 - oneSC](https://scbnow01.service-now.com/onesc?id=ticket&table=sc_req_item&sys_id=4830245ffbc6b6545054f8225eefdca2&view=sp) UAT： STG： | |
| 8 | foundation setup – Redis(manual) | @Zeyu Zhou | | | | | | |
| 9 | foundation setup – Kafka(manual) | @Zeyu Zhou | | | | 2 | | |
| 10 | foundation setup – ELK(manual) | @Zeyu Zhou | | | | 2 | | |
| 11 | foundation setup – Nginx | @Zeyu Zhou | | | | TBC | | depends Nginx admin account depends on ado pipeline |
| 12 | foundation setup – prometheus + grafana | @Zeyu Zhou | | | | 2 | | |
| 13 | Service deployment | @Zeyu Zhou | | | | TBC | | Depends on foundation setup |
| 14 | Generic service account creation | | | | | | | reuse GDC account |
| 15 | Entra integration (FMAA) ? not now | @Zeyu Zhou | | | | | | need to check whether need to add our hostname to their truststore |
| 16 | ADO – CICD get ready for both foundation component and microservices | @Zeyu Zhou | | | | | | |
| 17 | BE dev | New solace topic + queue for Murex cashflow inbound | @Xinmiao Huang @Junli Gao | NOT START | NOT START | NOT START | | | |
| 18 | SSI+ engagement for new solace queue creation | @Xinmiao Huang | NOT START | NOT START | NOT START | | | |
| 19 | RDM FileIT engagement | @Xinmiao Huang | NOT START | NOT START | NOT START | | | |
| 20 | RDM real time message solace queue creation | @Xinmiao Huang | NOT START | NOT START | NOT START | | | |
| 21 | Service properties setup (depends on foundation setup ready) | @Xinmiao Huang | NOT START | NOT START | NOT START | | | |
| 22 | API gateway development – region validation | @Xinmiao Huang | IN PROGRESS | NOT REQUIRED | NOT REQUIRED | | | |
| 23 | API gateway and auth server combination | @Xinmiao Huang | IN PROGRESS | NOT REQUIRED | NOT REQUIRED | | | |
| 24 | FE dev | UX design | @Guiling Wang | NOT START | NOT START | NOT START | | | involve Tech and Anbur, Geoffrey will head up first. |
| 25 | Routing logic development | @Guiling Wang | NOT START | NOT START | NOT START | | | |
| 26 | QA | Integration Testing | TBC | NOT START | NOT START | NOT START | | | |
| 27 | Regression Testing | TBC | NOT START | NOT START | NOT START | | | |
| 28 | Performance Testing | TBC | NOT START | NOT START | NOT START | | | |

</details>

# Surrounding System Integration Plan

[Cash Settlement Platform Architecture - Indonesia - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+Platform+Architecture+-+Indonesia#CashSettlementPlatformArchitectureIndonesia-SurroundingSystemIntegration)

# Services Install List(for UAT)

Release WI: [Release **15018293** RATAN Settlement Onshore dummy release wi](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15018293)

| | Services | Has Code Change | GDC deploy dependency | GDC prod version(updated on 10/6/2016) | ID STG Version | Pipeline/PR | UAT deploy Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ratan-service-properties-indonesia | No | | | 20260525.8 | | |
| 2 | ratanone-eureka-server | No | | 3.0.1-20240830.3 | | | |
| 3 | ratanone-config-server | No | | 3.0.1-20240830.3 | | | |
| 4 | ratanone-api-gateway | No | | 3.0.5-20260714.5 | | | |
| 5 | ratan-exception-platform | No | | 3.7.1-20260922.1 | | | |
| 6 | ratanone-auth-server | No | | 3.0.7-20260326.4 | | | |
| 7 | ratanone-message-event | No | | 3.1.1-20251017.12 | | | |
| 8 | ratanone-rule-service | Yes | Mandatory | 2.5.3-20260904.3 | 4.0.0-20261006.4 | [Pipelines - Run 20261006.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15396310&view=results) | @Fengke Wu |
| 9 | ratanone-static-data-service | Yes, (1)Rdm-api compensation (2)currency cutoff change | | 4.4.6-20260916.3 | 4.5.4-SNAPSHOT | merge main: [Pull request 3292759: merge main - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/3292759) update ado: [Pull request 3196468: ID ADO update - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/3196468) | |
| 10 | ratanone-audit-trial | Yes, eslog and change es key in yml | Not mandatory | | 3.1.2-20260709.2 | | |
| 11 | ratan-cash-settlement-orchestration | No | | 4.1.9-20260914.3 | | | |
| 12 | ratan-cash-settlement-accounting-service | No | | 3.0.1-20260831.8 | | | |
| 13 | ratan-cashflow-lifecycle-service | No | | 4.2.1-20260916.2 | | | |
| 14 | ratan-cash-settlement-fx-utilization-service | No | | 2.0.0-20260525.2 | | | |
| 15 | ratan-cash-settlement-group-management-service | yes, (1)status write back (2)id cf-cutoff change | Not mandatory | 3.2.8-20260915.7 | ~~3.2.3-20260617.1~~ 3.4.0-20260930.3 | | |
| 16 | ratan-cash-settlement-lms-service | yes, decouple adaptor trade | Not mandatory | 4.0.4-20260805.9 | 4.0.2-20260709.1 | | |
| 17 | ratan-cash-settlement-netting-service | Yes, resultant cf id prefix | Not mandatory | 3.1.7-20260915.7 | ~~3.0.10-20260601.1~~ 4.1.0-SNAPSHOT | | |
| 18 | ratan-cash-settlement-query-service | yes, filter & view query (migrate api from ratanone-query-service) | Not mandatory | 4.3.7.3-20260914.9 | 5.0.0-20260922.2 | [Pipelines - Run 20260717.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13620139&view=results) | |
| 19 | ratan-cash-settlement-ssi-stamping-service | No | | 4.2.3.1-20260915.12 | 4.2.1-20260624.1 | [Pull request 3067825: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-ssi-stamping-service/pullrequest/3067825) | |
| 20 | ratanone-data-ambassador | No | | 3.9.7.2-20260919.4 | 3.9.2-20260630.4 | [Pull request 3067992: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-data-ambassador/pullrequest/3067992) | |
| 21 | ratanone-swift-service | No | | 4.6.2.1-20260928.14 | 4.2.1-20260623.3 | [Pull request 3068794: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-swift-service/pullrequest/3068794) | |
| 22 | ratan-rule-service | No | | 3.2.1-20260911.8 | 3.1.5-20260522.8 | [Pull request 3068944: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-rule-service/pullrequest/3068944) | |
| 23 | ratanone-message-bridge | No | Mandatory | 5.0.7-20260727.1 | 5.0.5-20260604.2 | [Pull request 3069048: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-message-bridge/pullrequest/3069048) | |
| 24 | ratan-central-monitoring | No | | | 1.0.0-20250606.3 | | |
| 25 | 51358-mfe-admin-module | Yes, add ID route & tiles | | | | | |
| 26 | 51358-mfe-base | Yes, add ID handle for api | | | | | |
| 27 | 51358-mfe-container | Yes, add prefix for url, add route for ID, enhance global style | | | | | |
| 28 | 51358-mfe-cashflow-blotter | Yes, add prefix for url, add route for ID, booking entity fmid in drop down list should only include ID | | | | | |
| 29 | 51358-mfe-nostro-static | Yes, add prefix for url, add route for ID | | | | | |
| 30 | 51358-mfe-rules | Yes, add prefix for url, add route for ID | | | | | |
| 31 | 51358-mfe-trades | Yes, support redirect to GDC and ID based on trade booking entity | | | | | |
| 32 | 51358-ratan-cash-settlement-batch-service | Yes, Fixing flag changes | Mandatory | 2.0.0-20260326.4 | 2.0.1-20260703.1 | [Pull request 3069222: '#13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-batch-service/pullrequest/3069222) | @Haolin Song |
| 33 | 51358-ratanone-stella-ambassador | | | 3.2.15-20260805.1 | 3.2.13-20260408.2 | [Pull request 3069314: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-stella-ambassador/pullrequest/3069314) | |
| 34 | 51358-ratan-mxg-cashflow-adaptor | yes | Only GDC, | | | | @Haolin Song |

# Message Bridge Flow Definition

## GDC Existing

## GDC Changes

## Code change:

**Batch (GDC only)**

1. need to publish message to another topic Cash_Settlement_Mxg_Inbound_Batch_All for message bridge to consume.
2. ID doesn't have this service deployed

**Netting (ID drive)**

1. Netting resultant cashflow id prefix
2. Splitting resultant cashflow id prefix

## Indonesia Flow Definition

Question: Whether need to keep **folder** route type?