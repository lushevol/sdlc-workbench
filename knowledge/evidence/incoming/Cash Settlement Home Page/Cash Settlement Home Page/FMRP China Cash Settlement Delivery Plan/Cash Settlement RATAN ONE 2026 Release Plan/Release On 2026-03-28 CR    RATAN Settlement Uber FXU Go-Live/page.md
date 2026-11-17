CR：CHG0875198

TSK: CTASK1878671

AIG：

# 1.1 Release Work Item:

[Release 10176713 CHG0875198: RATAN Cash Settlement Uber Go-Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10176713)

MB filter change:

1. UBER flow: accept only EG/NP/SA
2. SCBML flow: exclude EG/NP/SA
3. Trade SCBML flow: exclude EG/NP/SA

FXU settlement method stamping: keep empty without stamping, until 4 Apr

UBER Validation Flag: take when "true", ignore when "false"

# 1.2 Packages

| | Service | Branch | Vulnerability Report Summery Screenshot | Code Cover screenshot | ADO release pipeline | Package Version | PR | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51358-ratanone-message-bridge | release/v5.0.2 | ![image-2026-3-26_17-11-54.png](attachments/image-2026-3-26_17-11-54.png) | ![image-2026-3-26_17-12-15.png](attachments/image-2026-3-26_17-12-15.png) | [Pipelines - Run 20260326.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11228896&view=results) | 5.0.2-20260326.3 | | @Yonghua Li |
| 2 | 51358-ratan-cash-settlement-query-service | release/v3.2.1 | ![image-2025-11-24_9-35-30.png](attachments/image-2025-11-24_9-35-30.png) ![image-2025-11-24_9-36-40.png](attachments/image-2025-11-24_9-36-40.png) | ![image-2025-11-24_9-34-22.png](attachments/image-2025-11-24_9-34-22.png) | [Pipelines - Run 20251121.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9340764&view=results) | | | ~~@Fengke Wu ~~ |
| 3 | 51358-ratanone-command | main | NA | NA | [Pipelines - Run 20251124.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=9372661&view=results) | | | @Fengke Wu |
| 4 | 51358-ratanone-service_batchMbStop | main | NA | NA | [Pipelines - Run 20260330.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11295285&view=results) | | | @Zeyu Zhou |
| 5 | 51358-ratanone-service_otherServicesStop | main | NA | NA | [Pipelines - Run 20260330.7](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11313953&view=results) | | | @Zeyu Zhou |
| 6 | 51358-ratanone-service_bcsCashflowStart | main | NA | NA | [Pipelines - Run 20260330.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11295341&view=results) | | | @Zeyu Zhou |
| 7 | 51358-ratanone-service_mbStart | main | NA | NA | [Pipelines - Run 20260330.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11301205&view=results) | | | @Zeyu Zhou |
| 8 | 51358-ratanone-ansible_removeGroup | main | NA | NA | [Pipelines - Run 20260330.11](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=11303242&view=results) | | | @Zeyu Zhou |

# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2025-09-20 | [cn-release-20250920 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/a89769e7-2258-4b96-94ce-3c62209f908f/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |
| | | | | |