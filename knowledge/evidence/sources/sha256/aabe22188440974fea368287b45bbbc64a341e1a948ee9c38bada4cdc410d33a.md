# CR Details:

CR for OpenSearch:

CR：[CHG0912513](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3605671448)

TSK: CTASK1958540

Release WI: [Release 11612390 CHG0912513: RATAN Settlement —— opensearch agent updated](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11612390)

AIG：

CR for Uber & FXU:

CR：[CHG0875198](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3472177284)

TSK:CTASK1878671

Release WI: [Release 10176713 CHG0875198: RATAN Cash Settlement Uber Go-Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10176713)

AIG：

# Packages

[Uber & FXU Technical Live Plan - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3616617459)

# Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| Full Ratan PT | [Test Plan for April 4th - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Test+Plan+for+April+4th) | [Test Result on April 4th - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Test+Result+on+April+4th) |

# Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-04-04 | [cn-release-20260321 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/af468370-cad9-49d4-bc10-af9fc510f724/) [cn-release-20260328 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/49d66803-65cc-4419-a9fd-2809073abde0/) | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# UVT Steps

| **Action Date** | **Booking** | **Booking Entity** | **Counterparty** | **Product** | **Value date** | **CCY 1** |
| --- | --- | --- | --- | --- | --- | --- |
| 3 Apr (Friday) | Book New Trade 1 (SCBML) | SCB SAUDI*RYD | SCB LONDON*LDN | ForeignExchange:Spot | 6 Apr | Pay USD 1 Receive SAR |
| **4 Apr (Saturday)** | Book New Trade 2 (UBER) | SCB SAUDI*RYD | SCB LONDON*LDN | ForeignExchange:Spot | 6 Apr | Pay USD 1 Receive SAR |
| **4 Apr (Saturday)** | Amend Trade **1 & **2 (UBER) | SCB SAUDI*RYD | SCB LONDON*LDN | ForeignExchange:Spot | 6 Apr | Amend Pay to USD 1.5 Receive SAR |
| 6 Apr (Monday) | Cancel Trades 1 & 2 (UBER) | No change to financials |

# Signoff email

| | attachment |
| --- | --- |
| Biz Signoff | |
| Tech Signoff | |