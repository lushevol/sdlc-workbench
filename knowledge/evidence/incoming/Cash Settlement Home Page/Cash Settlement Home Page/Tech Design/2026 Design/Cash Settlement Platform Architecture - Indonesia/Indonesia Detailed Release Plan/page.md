#

# Release Plan

| Phase | Description | Owner | Dependency | Planned Start Date | Planned End Date | Actual Complete Date | Status | | | Aug | Sep | Oct | Nov | DEC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Release preparation | UAT Signoff(Murex stream) 1. All surrounding system 2. Settlement Ops signoff 3. Data Ops signoff | Ops | Auto netting time zone(@Guiling Wang help to cross check) Only this function impact, raised story to cover the enhance requirement [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16400580](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16400580) | Sep.1st | Sep. 30th | Sep.17th | Signoff email from David. UI change can be closed along with FMRP UAT | | | | | | | | | | | | | | | | | | | | | | |
| UAT Signoff(FMRP stream) | Ops | ID - FXO(already go-lived) - new booking - already go-live on 3h Sep - [Squad RAG & Progress (2026/09/16) - Draft - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3867861163) - trade migration - already go-live on 12th Sep - [27 Trade Migration SOS - 14 Sep 2026 - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/27+Trade+Migration+SOS+-++14+Sep+2026) **UAT scope:** Rates - IRS, CCS, LNBR FXO - Include RATAN Suspended, PCD, DCD **Test case** - Sumita will check with Fan, Grace **MO support** - Dinesh will help Next catch up target to **Sep. 22nd** | Sep.1st | Sep. 30th | | UI change inherit from Murex UAT | | | | | | | | | | | | | | | | | | | | | | |
| RDM release agreement(Central solace, API release) | Caroline | Kelvin confirmed they will release APIs on Sep.25th, prior Ratan go-live we should tell Kelvin to grant access after getting scope access | | | | | | | | | | | | | | | | | | | | | | | | | | |
| EBBS release agreement(Central solace ack flow in GDC) | Caroline | PR merged, pipeline is ready to approve by Geoffrey. release WI: [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16153066](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16153066) | Sep.1st | Sep.26th | Sep.22nd | | | | | | | | | | | | | | | | | | | | | | | |
| Pipeline Ready(SSL, Kafka, AP) | DevOps | Development done, testing in progress | Sep.1st | Sep.16th | Sep.18th | Confirmed by @Zeyu Zhou with issues | | | | | | | | | | | | | | | | | | | | | | |
| Code freeze(UX design, RDM, Access control, Static sync) | Dev | static sync – new design reviewed, development in progress | 01-Sep | 11-Sep | | | | | | | | | | | | | | | | | | | | | | | | |
| Function Testing | QA @Wen Zhang | | 11-Sep | 30-Sep | | | | | | | | | | | | | | | | | | | | | | | | |
| Control-M job creation(existing + RDM compensation 3 jobs) | DevOps | control-M setup 1. 1. Non-prod control-m setup and testing(reuse GDC agent) and production go-live preparation -------- [@Cai1, Jie](mailto:Jie.Cai1@sc.com) help to support and [@Huang, Caroline Xinmiao](mailto:CarolineXinmiao.Huang@sc.com) provide API details later 2. Prod agent ideally not required already now, and created ID folder on GDC control-m can call the API to ID. 3. long term to decouple with control-M agent in GDC RATAN, need to migrate to air flow or setup control-M agent locally | 11-Sep | 30-Sep | | @Jie Cai help to support | | | | | | | | | | | | | | | | | | | | | | |
| Regression(both GDC and ID) Automation only for backend, how about FE | QA | | 11-Sep | 15-Oct | | | | | | | | | | | | | | | | | | | | | | | | |
| Day0 DB initialization | Dev | | 18-Sep | 25-Sep | | | | | | | | | | | | | | | | | | | | | | | | |
| Single UI bff DB change(separate pipeline ) | DEV | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| Data Migration plan | Dev | | 18-Sep | 30-Sep | | | | | | | | | | | | | | | | | | | | | | | | |
| DR - Mirror maker 2 release plan | Dev | | 01-Sep | 15-Oct | | | | | | | | | | | | | | | | | | | | | | | | |
| PT(GDC and ID, full Ratan) AP 2 DCs need to be covered? | DevOps | | 15-Oct | 31-Oct | | | | | | | | | | | | | | | | | | | | | | | | |
| BAU engagement | Dev | | 15-Sep | 31-Oct | | | | | | | | | | | | | | | | | | | | | | | | |
| PSS engagement | Dev | | 15-Sep | 31-Oct | | | | | | | | | | | | | | | | | | | | | | | | |
| Release | PROD DB setup and Hashi-Corp ready | DevOps | | 17-Aug | 21-Aug | 21-Aug | | | | | | | | | | | | | | | | | | | | | | | |
| APP servers SAT/OAT & PSS Hand Over | DevOps | | 15-Aug | 1-Sep | Sep.16th | | | | | | | | | | | | | | | | | | | | | | | |
| Firewall | DevOps | | 1-Sep | 6-Sep | | | | | | | | | | | | | | | | | | | | | | | | |
| EBBS ID integration on ACK on GDC | Haolin, Caroline | | 26-Sep | 26-Sep | target change to 26th | | | | | | | | | | | | | | | | | | | | | | | |
| **Services and Infra deployment - Round 1 **(deploy Redis, Kafka, ELK, Nginx, Prometheus, Grafana and all prod package) 1. 51358-mfe-ratan-container 2. 51358-ratanone-auth-server 3. ratan-service-properties-indonesia 4. ratanone-ansible_db_init 5. ratanone-ansible_infra 6. ratanone-ansible_backend 7. ratanone-ansible_lb | Dev | [https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-09-24+CR:CHG1077835+RATAN+Settlement+ID+prod+infra+install](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-09-24+CR:CHG1077835+RATAN+Settlement+ID+prod+infra+install) DB initialize dependency: /user/bin/psql | 7-Sep | 26-Sep | target change on Sep.24th | | | | | | | | | | | | | | | | | | | | | | | |
| VM and service level monitoring setup in Grafana | DevOps | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| **RDM enabling pipeline, Kong API grant access** | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| **Services Deployment - Round 2**(test firewall, API integration, static data initialization, Solace integration, F2B settlement processing) **ID**: 1. ratanone-static-data-service 2. ratanone-audit-trial 3. ratanone-rule-service 4. ratan-cash-settlement-group-management-service 5. ratan-cash-settlement-lms-service 6. ratan-cash-settlement-netting-service 7. ratan-cash-settlement-query-service 8. ratan-cash-settlement-batch-service 9. ratan-cash-settlement-ssi-stamping-service 10. ratanone-db-repository-indonesia 11. mfe-container 12. mfe-cashflow-blotter 13. mfe-nostro-static 14. mfe-rules **GDC**(**Mandatory**): 1. single-ui-bff 2. ratanone-db-repository 3. ratan-mxg-cashflow-adaptor 4. ratan-cash-settlement-batch-service 5. LB 6. mfe-admin-module 7. mfe-base 8. mfe-trades **Key points:** 1. Static data according to cutoff date 2. GDC need to deploy services in ID scope to keep version aligned 3. GDC inbound routing need to be deployed, data feeding open in 2 DCs 4. CPT control to avoid downstream feeding, downstream flow not enabling as well(EBBS, FMSGW, LMS) 5. Business still in GDC(downstream feeding&query) 6. Rule sync up function is live, data should be synced after go-live 7. UI is visible to all developers. 8. Keep monitoring two DC data until biz live. 9. API verification - SSI+, Stella, RDM, TL, FMCES, DQSL 10. FM Solace verification - SSI+, Ratan GDC 11. Central solace verification - RDM only | Dev | | 15-Oct | 21-Oct | | | | | | | | | | | | | | | | | | | | | | | | |
| Control-M go-live, verification | | | 15-Oct | 21-Oct | | | | | | | | | | | | | | | | | | | | | | | | |
| Dry Run & Issue Fix | | | 26-Oct | 6-Nov | | | | | | | | | | | | | | | | | | | | | | | | |
| Mirror maker 2 go-live and DR Rehearsal | | | 26-Oct | 6-Nov | | | | | | | | | | | | | | | | | | | | | | | | |
| Data Migration Test | | | 14-Nov | 14-Nov | | | | | | | | | | | | | | | | | | | | | | | | |
| RATAN GDC setup cutoff of processing ID payments(for UVT purpose, GDC need CPT control) | | | 21-Nov | 21-Nov | | | | | | | | | | | | | | | | | | | | | | | | |
| Business Go Live & Data Migration **Services Deployment - Round 3** **Key points: ** 1. Sync GDC code and DB change since round 2 2. Static data change since round 2 3. CPT removal 4. Open ID to downstream flow and remove GDC(LMS, FMSGW, EBBS) 5. Close GDC upstream flow(FMRP, Murex) 6. Data migration 1. **Truncate **existing cashflows 2. **Hold **all control-m jobs before migration 3. Add **GDC CPT** control for ID, instead of clean up data/clean up GDC directly 4. Ready CF in GDC should be suppressed after migration to avoid duplicate payment | | | 05-Dec | 05-Dec | | | | | | | | | | | | | | | | | | | | | | | | |

# ID Prod Service Metrics

| | Services | Has Code Change | GDC deploy dependency | GDC prod version(updated on 10/6/2016) | Pipeline | Planned Release Date | UAT deploy Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ratan-service-properties-indonesia | No | | | | | |
| 2 | ratanone-eureka-server | No | | 3.0.1-20240830.3 | | | |
| 3 | ratanone-config-server | No | | ~~3.0.1-20240830.3~~ 3.0.0-RC1.20231020 | | | |
| 4 | ratanone-api-gateway | No | | 3.0.5-20260714.5 | | | |
| 5 | ratan-exception-platform | No | | 3.7.1-20260922.1 | | | |
| 6 | ratanone-auth-server | No | | 3.0.7-20260326.4 | | | |
| 7 | ratanone-message-event | No | | 3.1.1-20251017.12 | | | |
| 8 | ratanone-rule-service | Yes | Mandatory | 2.5.3-20260904.3 | [Pipelines - Run 20261006.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=15396310&view=results) | | @Fengke Wu |
| 9 | ratanone-static-data-service | Yes, (1)Rdm-api compensation (2)currency cutoff change | | 4.4.6-20260916.3 | merge main: [Pull request 3292759: merge main - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/3292759) update ado: [Pull request 3196468: ID ADO update - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/3196468) | | |
| 10 | ratanone-audit-trial | Yes, eslog and change es key in yml | Not mandatory | | | | |
| 11 | ratan-cash-settlement-orchestration | No | | 4.1.9-20260914.3 | | | |
| 12 | ratan-cash-settlement-accounting-service | No | | 3.0.1-20260831.8 | | | |
| 13 | ratan-cashflow-lifecycle-service | No | | 4.2.1-20260916.2 | | | |
| 14 | ratan-cash-settlement-fx-utilization-service | No | | 2.0.0-20260525.2 | | | |
| 15 | ratan-cash-settlement-group-management-service | yes, (1)status write back (2)id cf-cutoff change (3)id uber message kafka | Not mandatory | 3.2.8-20260915.7 | | | |
| 16 | ratan-cash-settlement-lms-service | yes, decouple adaptor trade | Not mandatory | 4.0.4-20260805.9 | | | |
| 17 | ratan-cash-settlement-netting-service | Yes, resultant cf id prefix | Not mandatory | 3.1.7-20260915.7 | | | |
| 18 | ratan-cash-settlement-query-service | yes, filter & view query (1)id cf-cutoff change | Not mandatory | 4.3.7.3-20260914.9 | [Pipelines - Run 20260717.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13620139&view=results) | | |
| 19 | ratan-cash-settlement-ssi-stamping-service | No | | 4.2.3.1-20260915.12 | [Pull request 3067825: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-ssi-stamping-service/pullrequest/3067825) | | |
| 20 | ratanone-data-ambassador | No | | 3.9.7.2-20260919.4 | [Pull request 3067992: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-data-ambassador/pullrequest/3067992) | | |
| 21 | ratanone-swift-service | Yes (1)id cf-cutoff change | | 4.6.2.1-20260928.14 | [Pull request 3068794: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-swift-service/pullrequest/3068794) | | |
| 22 | ratan-rule-service | No | | 3.2.1-20260911.8 | [Pull request 3068944: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-rule-service/pullrequest/3068944) | | |
| 23 | ratanone-message-bridge | No | Mandatory | 5.0.7-20260727.1 | [Pull request 3069048: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-message-bridge/pullrequest/3069048) | | |
| 24 | ratan-central-monitoring | No | | | | | |
| 25 | 51358-mfe-admin-module | Yes, add ID route & tiles | | | | | |
| 26 | 51358-mfe-base | Yes, add ID handle for api | | | | | |
| 27 | 51358-mfe-container | Yes, add prefix for url, add route for ID, enhance global style | | | | | |
| 28 | 51358-mfe-cashflow-blotter | Yes, add prefix for url, add route for ID, booking entity fmid in drop down list should only include ID | | | | | |
| 29 | 51358-mfe-nostro-static | Yes, add prefix for url, add route for ID | | | | | |
| 30 | 51358-mfe-rules | Yes, add prefix for url, add route for ID | | | | | |
| 31 | 51358-mfe-trades | Yes, support redirect to GDC and ID based on trade booking entity | | | | | |
| 32 | 51358-ratan-cash-settlement-batch-service | Yes, (1)Fixing flag changes | Mandatory | 2.0.0-20260326.4 | [Pull request 3069222: '#13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-batch-service/pullrequest/3069222) | | @Haolin Song |
| 33 | 51358-ratanone-stella-ambassador | | | 3.2.15-20260805.1 | [Pull request 3069314: #13996712 ado pipeline for ID CICD enabling - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-stella-ambassador/pullrequest/3069314) | | |
| 34 | 51358-ratan-mxg-cashflow-adaptor | yes (1)Fixing flag changes (query cf fmid) | Only GDC, | | | | @Haolin Song |