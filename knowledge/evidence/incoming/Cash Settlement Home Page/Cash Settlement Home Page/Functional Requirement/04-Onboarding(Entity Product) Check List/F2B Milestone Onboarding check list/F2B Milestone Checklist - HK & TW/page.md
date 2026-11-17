Scope

![image-2025-4-11_11-28-39.png](attachments/image-2025-4-11_11-28-39.png)

![image-2025-4-11_11-29-19.png](attachments/image-2025-4-11_11-29-19.png)

1. anything required for dev
2. Anything required to be tested

| Function | Feature | | Consideration | Applicable to HK/TW | Comment | Test Cases / Scenarios |
| --- | --- | --- | --- | --- | --- | --- |
| GENERIC | SI INPUT | - Missing Vostro - Multi Vostro - Adhoc SI update - Missing Nostro | | | Common Logic | - |
| | SSI Auto Stamping | - SSI Auto Stamping Hierarchy (Old vs New) - CFI code Selection - Settlement Method (FEDWIRE / CASH) - Single Agent / Two Agent Supported (3 Agent not supported) - Trade SSI Stamping to CDUPS (XML + Product based) | | | | - SSI is Auto Attached for IRS, CCS, Loan Depo - Correct CFI code is captured for IRS, CCS, Loan Depo |
| | Nostro Auto Stamping | - Default Nostro Stamping | | | | - Correct nostro is auto attached |
| | Dashboard | | | | | |
| | Grouping Blotter | - Group Pending - Group Pending Validation | | | | - No Cashflows get stuck as Group Pending - Cashflows are stuck as Group Pending Validation prior to Validation & when validated they flow to Settlement Queue |
| | Cashflow Blotter | - New Fields introduced for Murex Flow - LIEN - Pending Fixing - Duplicate NDS - LTID, Structure ID, NID - Commodity Flag - Alpha Clearing | - New Fields Required - Murex Fields Equivalent in FMRP | No | None of these are part of scope | - |
| | SWIFT Generation | - MT Generation - MT103, 202, MT103+202COV, MT210, FlipMT202, MT192, MT292, MT604, MT605, MT692 - MX Generation - Pacs.008.001.08 (MT103) - Pacs.009.001.08 (MT202 & 202COV) - Camt.056.001.08(MT192 & MT292) - **camt.057(MT210)** | - New Message types required - Format changes required for new product / flow | | | - Cashflow moves to SETTLED status - Swift Generated successfully for MT103, 202, MT103+202COV, MT210, FlipMT202, MT192, MT292, MT604, MT605, MT692 |
| | Accounting Generation | - EBBS - Real Time Feed - ASPIRE Integration - EOD Feed | - Keystone (HK): Feed Nostro & Over Account to EBBS, feed Suspense to Aspire - Move from Aspire to EBBS model - handling of historic cashflows & events on past value cashflows post cutover | | - Special logic for CNH (check with Balaji) | - No Accounting Errors |
| Booking Model Impact | Package Bookings | B2B Package | | | - | |
| | | Package Booking Model | | | - | |
| | | RFR Booking Model (Netting based on LTID) | | | Not in scope | ~~If in scope, need to be verified comes in 1 trade or 3 trades~~ |
| | | Swap Agent | | | Not in scope | |
| | | ND Currency Handling (ND CCS / ND IRS) (Netting based on NID) | | Yes | ND IRS in scope. Behavior same as normal IRS. | - Verify SSI Stamping for IRS/CCS different CFI Code - Verify all legs get tagged as Pending another leg and get auto netted - Initial cashflow should be stopped as pending another leg for NDIRS/NDCCS ([Story 8244494 [Stella] ND CCS Auto Netting](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8244494)) - available for drop 2 |
| | | Structures (Netted based on Structure ID) | | | - | |
| | Rollover | | | | - | |
| | Fixing | | | | | Follow middle office pack |
| | Option | Exercise & Expiry | | | - | |
| | Strategy / Typology | | How Strategy / Typology will be supported in FMRP | | - NDIRS / OIS / Vanilla IR Swap - FWD_START_SWAP/RECALC - Per response from Candice, FWD_START_SWAP not in scope | |
| | Clearing | | | | -- | |
| | Allocation | | | Yes | Applicable for Markitwire IRS/ CCS | - Cashflows for ALOC name are not STP'd - Allocation in scope - available for drop 2 |
| NETTING | BILATERAL MANUAL NETTING | | | | | |
| | CCIL MANUAL NETTING | | | | - | |
| | BIC NETTING (MANUAL) | | | No | | |
| | NDS AUTO NETTING | | | No | USD will be directly generated, first leg will be held by RATAN as pending another leg | |
| | Interest AUTO NETTING (IRS) | | | | | - Fixed cashflow waiting as pending another leg & auto netted post floating leg received - Re-fixing breaks the previous netting and does re-netting with latest cashflow |
| | Principal + Interest Netting | | | No | - | |
| | CROSS PRODUCT NETTING WITHIN RATAN | | | | | - Net cashflows between IRS, CCS separately of STELLA with other Murex cashflow |
| STATIC | BILATERAL NETTING | | | | - | |
| | BIC NETTING | | | No | | |
| | VOSTRO SSI | | New Settlement Means & Settlement Account | | - | |
| | NOSTRO [Golden Source TBC ] | | New Settlement Means & Settlement Account | | - | |
| BUSINESS RULES | NSTP RULES | | - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity | | - - Per response from Candice, PRC_SCBHK_SGEI, PRC_USD_SGEI, PRC_SGE_SWP, PRC_HOC_SGE_SWP, PRC_HOSGE_N_IMA not in scope | - NSTP is triggered as expected - Murex Rules are replicated to work on STELLA cashflows |
| | SWIFT SUPPRESSION RULES | - Auto Debit by Agent - Nostros shared with other entity (example: China) | | | - | - 1. Swift Suppression done for expected cases - 2. Murex Rules are replicated to work on STELLA cashflows |
| | CASFHLOW SUPPRESSION RULES | | - There're specific filter logic to exclude some auto suppression counterparties in Murex → RATAN cashflow interface - Stella won't have such filter, need to config these as RATAN suppression rule | | - | - 1. Client Clearing Portfolios cashflows are auto suppressed - 2. Murex Rules are replicated to work on STELLA cashflows |
| | Authorization Limits | | | | - | |
| Settlement Method | CCIL | | | | - | |
| | DVP | NSTP based on DVP | | No | | |
| Migration | - Murex to FMRP Migration - Prevent Duplicate payment - Cutover handling - New Function / Changes - Historical data handling | | ISO Migration: handling of near value cashflows & events on past value cashflows post cutover | | Yes | Separate Test pack used |
| CONFIG | LMS Entity List | | | | - | |
| | [Murex Cash Migration Only] Entity list for the Batch Solution | | | | - | |
| | - BCS vs Strategic Routing - Entity whitelist for in scope entities (covered via Cashflow Suppression rule) - Entity whitelist setup to send to RAZOR or handle in RATAN (RATAN generates SWIFT & Accounting | | | | - | |
| | SWIFT Generation Changes - Booking Entity FMID - Booking Entity SWIFT BIC (Sender BIC in SWIFT) - Field 53 SWIFT BIC (for LCY & Over Account) - Field 58 SWIFT BIC (for Flip MT202) - Branch code mapping - Any other branch specific requirement on SWIFT | | | | - | |
| | Currency Release Time | | | | - | |
| | NDS Auto Netting | | | | - | |
| | Pending Fixing STP/NSTP Control( in case new product have fixing events) | | Loan Depo to be setup Pending Fixing | | - | |
| | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | | | | Follow UK model automatically | |
| | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | | | Yes | | - SGO currency generates swift and accounting as SGD - No Swift / Accounting failure for SGO - **SGO Nostro & Vostro are auto attached** |
| | Settlement Accounting - Bridge Account # - EBBS Branch code - EBBS Transaction type - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | | | | No changes | |
| | Include new branch / product in GUI Drop down - Cashflow Blotter - Dashboard | | | Yes | - | |
| | Vostro SI Input Screen - Include New Settlement Means | | | No | | |
| | Rounding | | | No | | |