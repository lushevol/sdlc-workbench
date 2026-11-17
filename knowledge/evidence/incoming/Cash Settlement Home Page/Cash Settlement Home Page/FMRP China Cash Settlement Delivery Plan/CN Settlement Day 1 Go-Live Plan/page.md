This Wiki records the timeline for CN Settlement Day1 go-live details. Includes services will be deployed, the services release sequence, test requirement and the timeline for release.

- # Environment
- # Services to Release - Services list | Services Name | Final Release Version | Service Type | Shared Service | Fixed Listening Port | Services Owner | Release Date | Release Ready | Code Frozen Checklist (Deployed to UAT) (Date & Release Branch) | Release JDK Version | Comments | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | ratan-cashflow-lifecycle-service | **1.1.1.RELEASE** | Backend | FALSE | FALSE | @Chongxuan Li | 2023-10-21 | | Deployed Date:2023-10-17 Release Version: 1.0.5-RC24.20230918 ADO release Version: 1.1.1-RC1.20231017 **Prod release version: 1.1.1.RELEASE** | 17 | | | ratan-cash-settlement-orchestration | **2.0.8.RELEASE** | Backend | FALSE | FALSE | @Chen Yang | 2023-10-21 | | Deployed Date:2023-11-06 Release Version: 2.0.9-RC1.20231106 ADO release Version: N/A **Prod release version: ****2.0.8.RELEASE** | 1.8 | | | ratan-cash-settlement-query-service | **2.1.7.RELEASE** | Backend | FALSE | **TRUE** | @Eric Wang | 2023-10-21 | | Deployed Date:2023-11-04 Release Version: 2.1.7-RC1.20231023 **Prod release version: ****2.1.7.RELEASE** | 17 | [2.1.8-RC1.20231114](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/ratan/ratan-cash-settlement-query-service/2.1.8-RC1.20231114/ratan-cash-settlement-query-service-2.1.8-RC1.20231114.jar) on uat | | ratan-cash-settlement-group-management-service | **1.1.0.RELEASE** | Backend | FALSE | FALSE | @Xinmiao Huang | 2023-10-21 | | Deployed Date:2023-09-28 Release Version: 1.1.0-RC1.20230915 ADO release Version: [1.1.0-RC10.20231013](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/ratan/ratan-cash-settlement-group-management-service/1.1.0-RC10.20231013/ratan-cash-settlement-group-management-service-1.1.0-RC10.20231013.jar) **Prod release version: ****1.1.0.RELEASE** | 17 | | | ratan-cash-settlement-netting-service | **1.1.0.RELEASE** | Backend | FALSE | FALSE | @Chongxuan Li | 2023-10-21 | | Deployed Date:2023-09-21 Release Version: 1.0.3-RC5.20230915 ADO release Version:1.1.0-RC3.20230920 **Prod release version: ****1.1.0.RELEASE** | 17 | | | ratan-cash-settlement-ssi-stamping-service | **2.1.7.RELEASE** | Backend | FALSE | FALSE | @Eric Wang | 2023-10-21 | | Deployed Date:2023-10-04 Release Version: 2.1.7-RC1.cib.20231026 **Prod release version: ****2.1.7.RELEASE** | 17 | [2.1.8-RC6.20231120](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/ratan/ratan-cash-settlement-ssi-stamping-service/2.1.8-RC6.20231120/ratan-cash-settlement-ssi-stamping-service-2.1.8-RC6.20231120.zip) on uat | | ratan-mxg-cashflow-adaptor | **1.6.0.RELEASE** | Backend | FALSE | FALSE | @Guangqing Wang | 2023-10-21 | | Deployed Date:2023-09-28 Release Version: 1.5.0-RC12.20230915 ADO release Version: 1.6.0-RC4.20230928 **Prod release version: ****1.6.0.RELEASE** | 17 | | | ratan-cash-settlement-lms-service | **1.1.1.RELEASE** | Backend | FALSE | FALSE | @Zhaolei Li | 2023-10-21 | | Deployed Date:2023-09-16 Release Version: 1.0.1-RC12.20230920 ADO release Version:1.1.1-RC9.20231013 **Prod release version: ****1.1.1.RELEASE** | 17 | | | ratan-exception-platform | **2.1.0.RELEASE** | Backend | FALSE | FALSE | @Xinmiao Huang | 2023-10-21 | | Deployed Date:2023-09-21 Release Version: 2.0.0-RC2.20230915 ADO release Version: [2.1.0-RC4.20231016](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/ratan/ratan-exception-platform/2.1.0-RC4.20231016/ratan-exception-platform-2.1.0-RC4.20231016.jar) **Prod release version: ****2.1.0.RELEASE** | 17 | | | ratan-rule-service | **1.2.2.RELEASE** | Backend | FALSE | FALSE | @Xinmiao Huang | 2023-10-21 | | Deployed Date:2023-10-26 Release Version: 1.1.2-RC19.20230915 ADO release Version: 1.2.4-RC2.cib.20231026 **Prod release version: ****1.2.2.RELEASE** | 17 | | | single-ui-bff | **`1.4.0.RELEASE`** | Common Backend | **TRUE** | FALSE | @Chen Yang | 2023-10-21 | | Deployed Date:2023-10-21 Release Version: **`1.4.0.RELEASE`** | 1.8 | | | ratanone-trade-service | 2.0.1.RELEASE | Common Backend | **TRUE** | FALSE | @Chongxuan Li | 2023-10-21 | | Deployed Date:2023-07-08 RC Version: 2.0.1-RC4.cib.20231011 Release Version: | 1.8 | | | ratanone-message-bridge | **[2.0.1.RELEASE](https://artifactory.global.standardchartered.com/artifactory/generic-release/com/scb/ratan/ratanone-message-bridge/2.0.1.RELEASE/ratanone-message-bridge-2.0.1.RELEASE.zip)** | Common Backend | **TRUE** | FALSE | @Ruiheng Cao | 2023-10-14 | | Deployed Date:2023-09-28 Release Version: 2.0.1-RC4.20230928 **Prod release version: [2.0.1.RELEASE](https://artifactory.global.standardchartered.com/artifactory/generic-release/com/scb/ratan/ratanone-message-bridge/2.0.1.RELEASE/ratanone-message-bridge-2.0.1.RELEASE.zip)** | 1.8 | | | ratanone-stella-ambassador | 2.0.0.RELEASE | Common Backend | **TRUE** | FALSE | @Ruiheng Cao | 2023-10-14 | | Deployed Date:2023-09-28 Release Version: 2.0.0-RC2.20230928 | 1.8 | | | ratanone-data-ambassador | **2.0.0.RELEASE** | Common Backend | **TRUE** | FALSE | | | | Deployed Date:2023-09-06 Release Version: 2.0.0-RC8.20231012 | 1.8 | | | [ratanone-auth-server](https://bitbucket.global.standardchartered.com/projects/RATANRT/repos/ratanone-auth-server/browse) | 2.0.0.RELEASE | Common Backend | **TRUE** | FALSE | @1632093 | 2023-10-21 | | Deployed Date:2023-09-22 Release Version: 2.0.0-RC4.20231010 | 1.8 | | | [ratanone-api-gateway](https://bitbucket.global.standardchartered.com/projects/RATANRT/repos/ratanone-api-gateway/browse) | 2.0.0.RELEASE | Common Backend | **TRUE** | **TRUE** | | 2023-10-21 | | Deployed Date:2023-09-22 Release Version: 2.0.0-RC3.20230922 | 1.8 | | | ratanone-static-data-service | **[2.0.0.RELEASE](https://artifactory.global.standardchartered.com/artifactory/generic-release/com/scb/ratan/ratanone-static-data-service/2.0.0.RELEASE/ratanone-static-data-service-2.0.0.RELEASE.zip)** | Common Backend | **TRUE** | FALSE | @Guangqing Wang | 2023-10-14 | | Deployed Date:2023-10-06 Release Version: 2.0.0-RC15.20231006 **Prod release version: [2.0.0.RELEASE](https://artifactory.global.standardchartered.com/artifactory/generic-release/com/scb/ratan/ratanone-static-data-service/2.0.0.RELEASE/ratanone-static-data-service-2.0.0.RELEASE.zip)** | 1.8 | | | ratanone-static-data-service | 2.0.1.RELEASE | Common Backend | **TRUE** | FALSE | @Zhang, William | 2023-10-21 | | Deployed Date:2023-10-19 Release Version: 2.0.1-RC1.20231012 **Prod release version: 2.0.1.RELEASE** | 1.8 | | | ratanone-cashflow-service | 1.7.7.RELEASE | BAU Backend | FALSE | FALSE | @Zhang, William | 2023-10-21 | | Release Version: 1.7.7-RC5.20231010 | | | | ratanone-stamping-service | 1.3.1.RELEASE | BAU Backend | **TRUE** | FALSE | @Zhang, William | 2023-10-21 | | Release Version: 1.3.1-RC7.20231012 | 1.8 | | | ratanone-suppression-service | 1.7.2.RELEASE | BAU Backend | **TRUE** | **TRUE** | @Zhang, William | 2023-10-21 | | Release Version:1.7.2-RC3.20231012 | 1.8 | | | ratan-service-gui-bff | 1.6.4.RELEASE | BAU Backend | FALSE | **TRUE** | @Zhang, William | 2023-10-21 | | Release Version: 1.6.4-RC1.20231010 | | | | ratanone-foundation | N/A | **Basic Packages** | **TRUE** | - | @Chen Yang | | | Deployed Date:2023-11-06 Release Version: 5.1.1 ADO release Version: 6.0.0.2 | | | | mfe-ratan-container | 1.5.0-RELEASE | Frontend | | TRUE | @Shuai Lu | 2023-10-21 | | Deployed Date:2023-10-21 RC: 1.5.0-20231013.27.RELEASE Release Version: 1.5.0-RELEASE | | | | ~~mfe-rules~~ | Already On PROD | Frontend | | TRUE | @Shuai Lu | 2023-10-21 | | NA | | | | mfe-cashflow-blotter | 1.2.2-RELEASE | Frontend | FALSE | TRUE | @Shuai Lu | 2023-10-21 | | Deployed Date:2023-10-21 RC: 1.2.2-20231010.4.RELEASE Release Version: 1.2.2-RELEASE | | | | mfe-authorization-limits | 1.1.0-RELEASE | Frontend | | TRUE | @Shuai Lu | 2023-10-21 | | Deployed Date:2023-10-21 RC: 1.1.0-20231010.2.RELEASE Release Version: 1.1.0-RELEASE | | | | ~~mfe-nostro-static~~ | NA | Frontend | TRUE | TRUE | @Zhonghui Feng | 2023-10-21 | | NA | | | | ratan-service-properties | | **Config** | TRUE | - | @Ruiheng Cao | 2023-10-21 | | | | | | control-m jobs - auto fail | | Control-m (DEVOPS) | - | - | @Jie Cai | 2023-10-20 | | | | | | control-m jobs - auto payment account | | Control-m (DEVOPS) | - | - | @Jie Cai | 2023-10-20 | | | | | | control-m jobs - auto Materialization | | Control-m (DEVOPS) | - | - | @Jie Cai | 2023-10-20 | | | | | Murex Related Change: [CN Settlement - Murex2.11 Technical Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex2.11+Technical+Design) <u>*[CN Settlement - Murex 2.11 workflow change](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex+2.11+workflow+change)*</u>
- # Release sequence

CR Release sequence

| | Sequence | CR Owner | services Name | RC version | Release version | CR Number | Release Date | PTP Link | RAT Number Tracehorizon Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| First Sequence | | - | ratanone-foundation | | | | 2023-10-20 | | |
| Related Supported CRs | | @Jie Cai | Control-M Jobs | | | CHG0323976 | 2023-10-20 | | |
| | @Zeyu Zhou | MQ channels | | | CHG0308441 (CR1) | 2023-10-14 |
| | Solace channel | | | CHG0308441 (CR1) | 2023-10-14 |
| | ansible package | | | CHG0308441 (CR1) | 2023-10-14 |
| | @Zeyu Zhou | Rundeck Jobs | | | | 2023-10-20 |
| CR1 | 1 | @Zeyu Zhou | ratanone-message-bridge | | **[2.0.1.RELEASE](https://artifactory.global.standardchartered.com/artifactory/generic-release/com/scb/ratan/ratanone-message-bridge/2.0.1.RELEASE/ratanone-message-bridge-2.0.1.RELEASE.zip)** | CHG0308441 (CR1) | 2023-10-14 - [x] @Chen Yang Configuration PR: | Deployment: Rollback: | [https://rat.vx.standardchartered.com/releases/53301](https://rat.vx.standardchartered.com/releases/53301) [https://tracehorizon.cloud.sc.net/traceability/releases/TH019849/dashboard](https://tracehorizon.cloud.sc.net/traceability/releases/TH019849/dashboard) |
| 2 | ratanone-static-data-service | | **[2.0.0.RELEASE](https://artifactory.global.standardchartered.com/artifactory/generic-release/com/scb/ratan/ratanone-static-data-service/2.0.0.RELEASE/ratanone-static-data-service-2.0.0.RELEASE.zip)** |
| CR 2 | | | ratan-service-properties (config PR) | | | CHG0241918 (CR2) | 2023-10-21 - [x] @Chen Yang Configuration PR: | | [https://rat.vx.standardchartered.com/releases/48813](https://rat.vx.standardchartered.com/releases/48813) [https://tracehorizon.cloud.sc.net/traceability/releases/TH017150/config](https://tracehorizon.cloud.sc.net/traceability/releases/TH017150/config) |
| 1 | @zhang william | ratanone-autentication | | |
| 2 | kevin | ratanone-trade-service | | |
| 3 | ben | ratanone-data-ambassador | | |
| 4 | @wang Eric | [ratanone-api-gateway](https://bitbucket.global.standardchartered.com/projects/RATANRT/repos/ratanone-api-gateway/browse) | | |
| 5 | william | ratanone-stella-ambassador | | |
| 6 | tech | single-ui-bff | 1.4.0-RC1.20231012 | `1.4.0.RELEASE` |
| 7 | william | ratanone-cashflow-service | | |
| 8 | william | ratanone-stamping-service | | |
| 9 | william | ratanone-suppression-service | | |
| 10 | william | ratan-service-gui-bff | | |
| 11 | | ratan-cash-settlement-query-service | | |
| 12 | | ratan-cashflow-lifecycle-service | | |
| 13 | | ratan-cash-settlement-netting-service | | |
| 14 | | ratan-cash-settlement-ssi-stamping-service | | |
| 15 | | ratan-mxg-cashflow-adaptor | | |
| 16 | | ratan-cash-settlement-orchestration | | |
| 17 | | ratan-exception-platform | | |
| 18 | | ratan-cash-settlement-group-management-service | | |
| 19 | | ratan-rule-service | | |
| 20 | | ratan-cash-settlement-lms-service | | |
| Frontend | |
| 1 | Tech in dev,done on 12th Oct | mfe-ratan-container | 1.5.0-20231013.27.RELEASE | | |
| 2 | | ~~mfe-rules~~ | NA | | |
| 3 | | mfe-cashflow-blotter | 1.2.2-20231010.4.RELEASE | | |
| 4 | | mfe-authorization-limits | 1.1.0-20231010.2.RELEASE | | |
| 5 | Judy | ~~mfe-nostro-static~~ | NA | | |
| CR 3 | 1 | Tech | mfe-base | 1.5.1-20231012.20.RELEASE | `1.5.1-RELEASE` | CHG0331949 | 2023-10-21 | | [https://rat.vx.standardchartered.com/releases/54909](https://rat.vx.standardchartered.com/releases/54909) [https://tracehorizon.cloud.sc.net/traceability/releases/TH020685/config](https://tracehorizon.cloud.sc.net/traceability/releases/TH020685/config) |
| 2 | Nginx config | | |

MQ ( channel ): <MQ name>

CF.MXG.RATAN.RQST – QREMOTE at Murex
                     CF.MXG.RATAN.RQSTIN – RATAN messages received local queue at Ratan
                     CF.RATAN.MXG.RESP – Ratan message post queue name – QREMOTE
                     CF.RATAN.MXG.RESPIN – Murex response received local queue name

Configurations:

TBD

Murex confirmation topic mapping

Topic:
                    v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-fx/status-match/pub

v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-fx/status-oth/pub

v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-irs/status-match/pub

v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-irs/status-oth/pub

v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-cre/status-match/pub

v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-cre/status-oth/pub

v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-com/status-match/pub

v1/conf/50505-cdu-cl/cdu-xceptor/json-1.0/paper-com/status-oth/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-fx/status-match/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-fx/status-oth/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-irs/status-match/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-irs/status-oth/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-cre/status-match/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-cre/status-oth/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-com/status-match/pub

v1/conf/50505-cdu-cl/citinet/json-1.0/elec-com/status-oth/pub

Queue:
                   q-51358-ratanone-cdu-cofstatus-ratan

Create Solase : New topic for  IMS

EMS2 data import

- # Test requirement and status - Test requirement list | Test Type | Description | Automation | Test Environment | Test Owner | Comments | | --- | --- | --- | --- | --- | --- | | Unit Testing | | TRUE | - | Dev team | 80% | | System Testing | | TRUE | - | @Shimeng Ma | Done | | Integration Testing | There are changes to application interfaces and/ or changes that have the potential to impact upstream or downstream systems. | FALSE | UAT | @Shimeng Ma | No Need | | Acceptance Testing | UAT | FALSE | UAT | @Shimeng Ma | Waiting for Sign-off | | Performance Testing | Backend performance test | FALSE | UAT | @Chen Yang | Test Plan: [RATAN One - Backend Performance Test Plan July 2023 - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+-+Backend+Performance+Test+Plan+July+2023) Test Results: [RATAN One - Backend Performance Test Result July 2023 - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+-+Backend+Performance+Test+Result+July+2023) | | Frontend performance test | FALSE | UAT | @Guiling Wang | Test Plan: [RATAN One FMO GUI - Performance Test Plan SEP 2023 - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+FMO+GUI+-+Performance+Test+Plan+SEP+2023) Test Results: [RATAN One FMO GUI - Performance Test Result SEP 2023 - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/RATAN+One+FMO+GUI+-+Performance+Test+Result+SEP+2023) | | Regression Testing | | TRUE | Demo | @Guiling Wang | Done Test result: https://[tracehorizon.cloud.sc.net/traceability/releases/TH019849/dashboard](http://tracehorizon.cloud.sc.net/traceability/releases/TH019849/dashboard) | Runbook Discuss with zoey Fx rate - we need init data, DML get from script to execute <Rundeck>
- # Release Checklist - Checklist table | Date | Works to be done | CR1 Done list | CR2 Done list | Solace Tracking | MQ Tracking | | --- | --- | --- | --- | --- | --- | | Sep.11th | Raise **CR1** for 14th, and related RAT, Tracehorizon and SIA | - [x] @Zeyu Zhou 2023-09-11 | - [x] @Shuai Lu 2023-09-11 | | | | Sep.14th | Tracehorzion Traceability All Green (all requirements has been coverd) for **CR1 and CR2** | - [x] @Shimeng Ma 2023-09-14 | - [x] @Shimeng Ma 2023-09-14 | | | | Sep.15th | Performance Test done and submitted for **CR1 and CR2** | - [x] @Zeyu Zhou 2023-09-15 - [x] @Guiling Wang 2023-09-15 | - [x] @Zeyu Zhou 2023-09-15 - [x] @Guiling Wang 2023-09-15 | | | | Sep.20th | **CR1** AIG Prepared | - [x] @Zeyu Zhou 2023-09-20 | - | | | | Sep.22th | OLA documents | | - [ ] @Lina Feng 2023-09-22 | | | | | User bulk request | | - [ ] @Gary Jianguo Xia 2023-09-22 | | | | Sep.24th | UAT Signoff | | | | | | Sep.26th | Regression test results upload for **CR1 and CR2** | - [x] @Zeyu Zhou 2023-09-26 | - [x] @Zeyu Zhou 2023-09-26 | | | | | Tracehorizon Evidence done for **CR1 and CR2** | - [x] @Zeyu Zhou 2023-09-26 | - [x] @Zeyu Zhou 2023-09-26 | | | | Sep.27th | Rehearsal Test **CR1** | - [x] @Ruiheng Cao 2023-09-27 | | | | | | Independent Test **CR1** | - [x] @Zeyu Zhou 2023-09-27 | | | | | Sep.28th | Raise SIA** CR1** | - [x] @Zeyu Zhou 2023-09-28 | | | | | | Release Pkg prepared **CR1** | - [x] @Chen Yang 2023-09-28 - [x] @Ruiheng Cao 2023-09-28 | | | | | | PTP Prepared **CR1** | - [x] @Zeyu Zhou 2023-09-28 | | | | | | RAT Prepared **CR1** | - [x] @Zeyu Zhou 2023-09-28 | - | | | | | CR Prepared **CR1** | - [x] @Zeyu Zhou 2023-09-28 | - | | | | Oct.12th | Pre-review **CR1** with PSS | - [x] @Chen Yang 2023-09-28 - [x] @Ruiheng Cao 2023-09-28 | - | | | | Oct.13th | Rehearsal Test **CR2** | | - [ ] @Ruiheng Cao 2023-09-27 | | | | | Pre-review **CR2** with PSS | | - [x] @Zeyu Zhou 2023-09-20 | | | | Oct.14th | **CR1** release | - [ ] @Ruiheng Cao 2023-10-14 | - | | | | Oct.16th | Independent Test **CR2** | | - [ ] @Chen Yang 2023-10-13 - [ ] @Ruiheng Cao 2023-10-13 | | | | | Control-M CR Submit | | - [ ] @Jie Cai 2023-10-16 | | | | | Raise SIA** CR2** | | - [ ] @Zeyu Zhou 2023-10-06 | | | | | Release Pkg prepared **CR2** | - | - [ ] @Chen Yang 2023-10-06 - [ ] @Ruiheng Cao 2023-10-06 | | | | | PTP Prepared **CR2** | | - [ ] @Zeyu Zhou 2023-10-06 | | | | | RAT Prepared **CR2** | | - [ ] @Zeyu Zhou 2023-10-06 | | | | | CR Prepared **CR2** | | - [ ] @Zeyu Zhou 2023-10-06 | | | | Oct.18th | Submit** CR2** | | | | | | Oct.21th | **CR2** release | - | - [ ] @Ruiheng Cao 2023-10-21 | | | - Murex 2.11 Change List | | release date | Pre-Cab | Description | Object | Functionality | Progress | | --- | --- | --- | --- | --- | --- | --- | | 1 | 14-Oct | 5-Oct | MQ Testing | workflow MQ Task | Test MQ connectivity | WIP | | 2 | 21-Oct | 12-Oct | Main Change (Bulk Box 30 Oct and CPT 1$) | 1.DB : SCB_FMRP_DBF, FMRP_ENTITY_DBF,scb_payfmrp (30 Oct) 2.Payment Status: SNTR, RSLR 3.Data Publisher : PAY_VALD, PAY_INS_ND 4.Payment Q : FMRP:INIT2SNTR AUTO (bulk box) FMRP:INIT2SNTR MAN , (manual Q) FMRP:SNTR2INIT (manual Q) INIT2SNTR (cpt) SNTR2RLSR (cpt) FMRP - Rollback (rollback) 5.Processing : PAY_FMRP_STP (bulk box) 6.User Monitor : Filter & Viewer 7.Workflow : Inbound & Outbound 8.Control M (One Time) | 1.Bulk Box push value date=30 Oct payment(one time order, only be triggered in release day) 2.CPT $1 trade booking 3.User Monitor on MX Side 4.Rollback payment, move status from SNTR to INIT 5.Manual Q | WIP | | 3 | 4-Nov | 24-Oct | Main Change (Bulk Box 13-14 Nov) | 1.DB : scb_payfmrp (13-14 Nov) 2.Control M (standard) : FMRP Daily pushing, SCB_FMRP_DBF Purge | 1.Bulk Box push value date=13 - 14 Nov 2.PRC change on TABLE#LIST#PAYSTP_M_DBF to stop CN Entity 3.Recovery the Control M to BAU Process 4.Realize the staging table purge process | | | 4 | 11-Nov | 2-Nov | Recovery to BAU | 1.DB : scb_payfmrp (standard),sp_pre_stp,SCB_VW_PAY_INIT_TO_SUPP 2. Consistency Rule: NoMKTOP on Fut. Flow. 3.Workflow : client.scb.fmrp.inbound.payInsertionFilter -Modify client.scb.fmrp.isCPT - delete client.scb.fmrp.cptCheck - delete | 1. Recovey the payment scanner to BAU Process 2. Exclude CN Payment on STP and Auto Supp process 3. PRC change on TABLE#LIST#PAYSTP_M_DBF to start CN Entity PRC change on TABLE#LIST#PAY_SUPP_DBF to exclude CN Process 4. Hardblock Released CN Payment. 5. Removed CPT function 6. PSS ITRS Function | |

- # Tech Go Live Protection

1. Business Go live date is 13th Nov 2023
2. Cashflows in Ratan VD before above date should never got a chance to be 1. published to Razor 2. published to LMS
3. Exception for CPT, amount == 1

![image2023-9-22_14-9-1.png](attachments/image2023-9-22_14-9-1.png)

- # Release Timeline