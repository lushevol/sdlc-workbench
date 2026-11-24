CR：

AIG：

# 1.0 Steps:

1. Rule to NSTP stella cashflows on VD, 14, 15 Oct
2. Rule to Suppress Murex cancellation for VD, 14, 15 Oct
3. Orchestration config change on the 2 VDs for " - toList(VALUE_DATE_SCOPE),2023-10-14|2023-10-15 "

# 1.1 Release Work Item:

[Release 5036587: CHG0538827 CN Go live Sep 28th - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5036587)

# 1.2 Packages

| | Service | Branch | Hashicorp Enabled | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratan-cash-settlement-group-management-service | | Yes | | | @Xinmiao Huang |
| 2 | 51358-ratan-cashflow-lifecycle-service | release/v1.3.0 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3117269&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3117269&view=results) | | @Chen Yang |
| 3 | 51358-ratan-mxg-cashflow-adaptor | release/v1.8.2 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3113510&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3113510&view=results) | | @Chen Yang |
| 4 | 51358-ratan-rule-service | release/v2.0.0 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3113645&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3113645&view=results) | | @Pengpeng Li |
| 5 | 51358-ratan-cash-settlement-ssi-stamping-service | | Yes | | | @Xinmiao Huang |
| 6 | 51358-ratan-cash-settlement-accountng-service | | Yes | | | @Chongxuan Li |
| 7 | 51358-ratanone-swift-service | | Yes | | | @Mingyang Zhong |
| 8 | 51358-ratan-cash-settlement-query-service | release/v2.4.0 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3114142&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3114142&view=results) | | @Mingyang Zhong |
| 9 | 51358-ratan-cash-settlement-netting-service | release/v1.4.0 | Yes | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3114346&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=3114346&view=results) | | @Mingyang Zhong |
| 10 | 51358-ratanone-static-data-service | release/v3.3.3 | Yes | | | @Mingyang Zhong |
| 11 | 51358-mfe-cashflow-blotter | | Yes | | | @Shuai Lu |
| 12 | 51358-ratanone-db-repository | develop | N/A | | | @Chen Yang |
| 13 | 51358-ratan-service-properties | master | N/A | | | @Chen Yang |

| | Service | Branch | Hashicorp Enabled | ADO release pipeline | Package Version | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-db-repository | develop | NA | execute: rollback: | execute: rollback: | @Chongxuan Li |
| 2 | rules change | | | db: | | @Chongxuan Li |

# 1.3 Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2024-08-24 | | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |