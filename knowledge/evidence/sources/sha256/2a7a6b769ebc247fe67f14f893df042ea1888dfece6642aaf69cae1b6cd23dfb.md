# Introduction

- As part of FMRP (FM Re-Platforming), RATAN is being built as a Strategic Settlements Platform and will replace Murex2.11
- Settlement Migration will be done by feeding Cashflows of Murex to RATAN. **This was achieved by taking an innovative approach! **
- The payments processing migration off Murex 2.11 was accelerated by using cashflows from the Murex trade population together with cashflows from FMRP trades and centralising all downstream payments in RATAN. This was a more complex approach but ensured the dependency on Murex for settlements payments is removed whilst readying the migration of trades and cashflows/settlement payments on the new Strategic Platform.
- Settlement Migration is being done for each country ahead of Trade Migration to ensure Settlements can be done out of a single system (irrespective of cashflow received from MX2.11 or Strategic stack)

![image-2025-3-8_18-5-19.png](attachments/image-2025-3-8_18-5-19.png)

# Benefits

![image-2025-3-8_18-7-4.png](attachments/image-2025-3-8_18-7-4.png)

![image-2025-3-8_18-6-16-1.png](attachments/image-2025-3-8_18-6-16-1.png)

**Notes on Benefits:**

- Reduction in manual payment scenarios [Serial MT103 supported | No dependency to setup Beneficiary Agent BIC code | Third Party Payments supported | Auto Removal of special character | Selection of Value date while releasing payment]
- Improved STP (exact % TBC)
- Real Time Exceptions Dashboard
- Self Serve maintenance of Business Rules by Data Ops (avoid dependency on Change release)
- Risk Reduction through Dual Blind Input (though it increases Checker processing time)
- Ack / Nack Notification reducing dependency on emails from FMSRE / FMSGW
- Swift Suppression supported, reducing efforts
- Single queue across markets making follow the sun model easier

# Cashflow Monthly Volumes

![image-2025-3-8_18-17-14-1.png](attachments/image-2025-3-8_18-17-14-1.png)

**Note: Full Volume includes Cancelled Cashflows. Going forward, only Live Volumes will be reported from FMMIS**

# 2025 High Level Plan

![image2025-2-11_13-1-41.png](attachments/image2025-2-11_13-1-41.png)

# 2026 High Level Plan

| Deliverable | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Indonesia - Local Instance | | | | | | | | | | | | | Commitment to OJK (Central Bank) to setup RATAN local instance by end 2026 |
| MX2.11 Non Payment module entities | | | | | | | | | | | | | |
| | | | | | | | | | | | | | |
| | | | | | | | | | | | | | |

# Features

| Description | Live |
| --- | --- |
| Countries & Products | - Legacy: Equity Derivatives (BCS) - UK, SINGAPORE, HONGKONG, JERSEY - Via Razor: LOANIQ, FX - EGYPT, NEPAL, SAUDI - Strategic: All via Murex - CHINA, INDIA, MALAYSIA, SINGAPORE, GERMANY, UK - Strategic: Via FMRP - CHINA (IRS, CCS, NDF, SCF), UK (Prime Precious Metals) |
| Netting | - Bilateral Netting | BIC Netting | CCIL Netting | NDS Auto Netting | IRS Auto Netting |
| Settlement Method | - DVP (manual) |
| External Integration | - SSDR | FMMIS | RATAN EOD | SCI | SSI+ | RDM | CDUPS | EBBS | ASPIRE | FMSGW |
| STP / NSTP | - STP based on Confirmation (TDS3) status - NSTP based on exceptions defined |
| SI Stamping / Input | - Dual Blind Input - Block special characters - Auto populate SCI info - TPP Supported |
| Dashboard | - Realtime Exceptions Dashboard |
| Payment Generation | - Via RAZOR for BCS, LOANIQ, EG, NP, SA - Strategic: MT103, MT202, MT210, Flip MT202, MT192, MT292, MT604, MT605, MT692 - Serial MT103 supported - Rounding Logic - Swift Customization (Field 20, 53) |
| Settlement Accounting Generation | - Via RAZOR for BCS, LOANIQ, EG, NP, SA - Strategic Settlement Accounting Generation via EBBS / Aspire - Display Accounting Entries Generated |
| Exceptions Handling | - NSTP as per requirement - Trigger Reversal & Rebook exceptions for Maker & Checker |
| Business Rules | - Low code Self Service Maintenance of Rules - NSTP Rules - Cashflow Suppression - Swift Suppression - Authorization Limits |
| Static | - Bilateral Netting - BIC Netting - Nostro Static |
| Cashflow Events | - New - Withdrawal |
| Trade Events | - New Booking - Amendment - Cancellation - Early Termination (Partial / Full) - Portfolio Re-Assignment - Novation |
| Profiles | ![image-2025-3-10_8-16-42.png](attachments/image-2025-3-10_8-16-42.png) |
| Cashflow Status | - Multiple as per requirement - Sub Status - FM Swift Gateway / AMH / SCPAY Status |
| Settlement Affirmation | - Single / Bulk Cashflow Affirmation - Netting Affirmation |
| Auto Refresh | - Cashflow Blotter Refresh - Vostro SI Refresh on Cashflows - Nostro Refresh |
| Data Extraction & MIS | - Cashflow data available in SSDR (real time query) - Volume & Touchpoint data available in FMMIS (VD+2 basis) |

# Backlog

- FMRP Rollout dependencies: [RATAN Settlements FMRP Backlog - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/RATAN+Settlements+FMRP+Backlog)
- Settlement Day 2 Requirements: [RATAN Settlements Day 2 Backlog - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/RATAN+Settlements+Day+2+Backlog)