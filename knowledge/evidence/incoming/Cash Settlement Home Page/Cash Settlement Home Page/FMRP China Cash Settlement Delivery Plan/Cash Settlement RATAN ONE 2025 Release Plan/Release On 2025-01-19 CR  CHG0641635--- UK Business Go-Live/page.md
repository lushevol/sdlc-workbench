CR：CHG0641635

TSK: CTASK1379321

AIG：

# 1.1 Release Work Item:

[Release 6528954 CHG0641635: RATAN Settlement UK Business Go-Live (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6528954)

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-service-properties | master | N/A | | [Pipelines - Run 20250115.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=4634424&view=results) | 20250115.1 | @Chen Yang |

# 1.3 Run Book on 19th Jan 2025

| | Start Time | End Time | Activity | |
| --- | --- | --- | --- | --- |
| 1 | 10:00 | 11:00 | Deployment of the timeout configuration adjustment | |
| 2 | 11:00 | 11:30 | Provide the list of below to OPS 1. READY payments 2. SWIFT_SUPPRESSED payments | |
| 3 | 11:00 | | OPS verify data | |
| 4 | ?? | | CPT control removal deployment | |
| 5 | ?? | | 1. For READY payments: Release payments via script 2. For SWIFT_SUPPRESSED payments: 1. Un-Suppress via scripts 2. Reject via script | |
| 6 | ?? | | OPS verify released payments | |
| 7 | ?? | | Murex publish future payments post VD 22nd Jan | |

# 1.4 Emergency Case Handling

| | Activity | Owner |
| --- | --- | --- |
| 1 | Impact/Risk assessment | Geoffrey, Wayne, Lina |
| 2 | Release item preparation | Zoey |
| 3 | Code fix | Dev Team |
| 4 | Verification | Elena, Sherry |
| 5 | PSS | Teddy (Morning), Baolong (Afternoon) |

# 1.5 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-01-19 | [Story 6857938 UK - Biz Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6857938) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |