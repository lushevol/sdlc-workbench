CR：CHG0667603

TSK: [CTASK1432930](https://scbnow01.service-now.com/change_task.do?sys_id=b98d0ae8fbdfde105054f8225eefdcd2&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=1&sysparm_record_list=change_request%3D28394aa0fb9fde105054f8225eefdcaa%5EORDERBYassignment_group)

AIG：

# 1.1 Release Work Item:

[Release 6985879 CHG0667603: Ratan Settlement issue fix](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6985879)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-mfe-cashflow-blotter | [release/v1.11.2](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-cashflow-blotter?version=GBrelease/v1.11.2) | ![image2025-1-22_12-9-37.png](attachments/image2025-1-22_12-9-37.png) | ![image2025-1-22_13-59-51.png](attachments/image2025-1-22_13-59-51.png) | [Pipelines - Run 20250122.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=4715104&view=results) | 1.11.2-v1.11.2-20250122.1 | @Shuai Lu |

# 1.3 Performance Test

## A. Test Plan

### A.1 NFR

| # | NFR | Comment |
| --- | --- | --- |
| 1 | Availability | 24x7* |
| 2 | API Latency : Expected average response time under normal load | 5 sec* |
| 3 | Stress Load : Max Concurrent User: | 50* |
| 4 | Stress Load : Max Concurrent Request (per hour): | 23769 |
| 5 | Endurance(Soak test) : response time under sustained load | Load % : 1x |

### A.2 Volumetrics and Flows

**We define peak hour as 3603 API calls based on Dashboard(QPS=1)**

| API | Count | Business | Percentage |
| --- | --- | --- | --- |
| /api/auth/v2/sso/login | 3 | common | 0.08% |
| [/api/auth/v2/sso/extend](http://fmo-shell.uk.dev.net:8453/api/v2/login) | 352 | common | 9.77% |
| [/api/ratan/stmcn/v1/cashflows](http://fmo-mfe-preprod.pi.dev.net:8453/api/ratan/stmcn/v1/cashflows) | 3248 | cn | 90.15% |

**We define 1x peak hour as 23769 API calls based on best estimation of combination of multiple different workflows.**

| API | Count | Business | Percentage |
| --- | --- | --- | --- |
| /api/auth/v2/sso/login | 3 | common | 0.01% |
| /api/auth/v2/sso/extend | 3147 | common | 13.24% |
| /api/analytics/v1/fmo/print | 2607 | common | 10.97% |
| /api/ratan/da/graphql | 2324 | bau | 9.78% |
| /api/ratan/da/v1/monitor | 51 | bau | 0.21% |
| /api/ratan/da/v1/swift/message | 4 | bau | 0.02% |
| /api/ratan/rule/v1/fields | 5 | common | 0.02% |
| /api/ratan/rule/v1/fields/versions | 45 | common | 0.19% |
| /api/ratan/rule/v1/validationRules/entities/EXCEPTION_SSI | 22 | cn | 0.09% |
| /api/ratan/rule/v1/validationRules/entities/NOSTRO_VALIDATE_RULES | 6 | cn | 0.03% |
| /api/ratan/stmcn/v1/cashflows | 16435 | cn | 57.66% |
| /api/ratan/v1/accounting/fetch | 130 | cn | 0.55% |
| /api/ratan/v1/cashflow/country/countryInfo | 134 | cn | 0.56% |
| /api/ratan/v1/cashflow/currency/holiday | 93 | common | 0.39% |
| /api/ratan/v1/profileLimitation/checkLimitation | 1 | cn | 0.00% |
| /api/ratan/v1/slt/custom | 968 | bau | 4.07% |
| /api/ratan/v1/static/fields | 4 | bau | 0.02% |
| /api/ratan/v1/static/fields/versions | 16 | bau | 0.07% |
| /api/ratan/v1/static/validationRules/entities/EXCEPTION_SSI | 3 | bau | 0.01% |
| /api/ratan/v1/static/validationRules/entities/NOSTRO_VALIDATE_RULES | 1 | bau | 0.00% |
| /api/ratan/v2/customview/filters | 73 | common | 0.31% |
| /api/ratan/v2/customview/views | 144 | common | 0.61% |
| /api/ratan/v2/rules | 4 | common | 0.02% |
| /api/ratan/v3/customview/filters | 73 | trade | 0.31% |
| /api/ratan/v1/static/bicNettingEligibleRule | 133 | cn | 0.56% |
| /api/ratan/v1/rep/exceptions/nstpExceptionCodes/byStatus | 73 | cn | 0.31% |

## B. Test Report

| **Legend** | GREEN | Can recommend release | AMBER | Concerns/Caveats signatory must accept | RED | Cannot recommend release |
| --- | --- | --- | --- | --- | --- | --- |

### B.1 Execution Overview

| Test | Time | Conclusions | Met/Not Met |
| --- | --- | --- | --- |
| Dashboard(QPS=1) of Prod peak 1 hour | Start Time (GMT) "1/21/25 3:26 PM" End Time (GMT) "1/21/25 4:26 PM" | API average response time is ***0.056s***, 95% of api call are within **0.105*****s***. The testing result matches the requirement of NFR threshold should be less than 5s | |
| Dashboard(QPS=30) of Prod peak 1 hour | Start Time (GMT) "1/22/25 9:07 AM" End Time (GMT) "1/22/25 10:07 AM" | API average response time is ***0.04s***, 95% of api call are within **0.059*****s***. The testing result matches the requirement of NFR threshold should be less than 5s | |
| 1X of Prod peak 1 hour | Start Time (GMT) "1/22/25 12:24 PM" End Time (GMT) "1/22/25 1:24 PM" | API average response time is ***0.087s***, 95% of api call are within **0.129*****s***. The testing result matches the requirement of NFR threshold should be less than 5s | |

### B.2 Test Evidence

| Test | Over Time Charts | APDEX | Statistics |
| --- | --- | --- | --- |
| Dashboard(QPS=1) of Prod peak 1 hour | ![1-1.png](attachments/1-1.png) | ![1-2.png](attachments/1-2.png) | ![1-3.png](attachments/1-3.png) |
| Dashboard(QPS=30) of Prod peak 1 hour | ![2-1.png](attachments/2-1.png) | ![2-2.png](attachments/2-2.png) | ![2-3.png](attachments/2-3.png) |
| 1X of Prod peak 1 hour | ![3-1.png](attachments/3-1.png) | ![3-2.png](attachments/3-2.png) | ![3-3-1.png](attachments/3-3-1.png) ![3-3-2.png](attachments/3-3-2.png) |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-01-22 | [Release 6985724 RATAN Settlement UI Enhance](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6985724) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Results | Results | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Refresh Page and open dashboard | dashboard has been disable | **PASS** | ![dashboard.png](attachments/dashboard.png) |