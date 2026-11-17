![image-2025-4-25_11-35-37.png](attachments/image-2025-4-25_11-35-37.png)

![image-2025-5-21_15-16-14.png](attachments/image-2025-5-21_15-16-14.png)

| | Function | Feature | | Consideration | Test Case/Scenario |
| --- | --- | --- | --- | --- | --- |
| 1 | GENERIC | SI INPUT | - Missing Vostro - Multi Vostro - Adhoc SI update - Missing Nostro | | |
| 2 | | SSI Auto Stamping | - SSI Auto Stamping Hierarchy (Old vs New) - CFI code Selection - Settlement Method (FEDWIRE / CASH) - Single Agent / Two Agent Supported (3 Agent not supported) - Trade SSI Stamping to CDUPS (XML + Product based) - Currency code transformation (when receive SGO, lookup SGD) | Any new currency transformation required | - To check whether is it all booked under inter entity for Loan; - if inter entity is expected, then should check SSI Stamping - FXO is expected to see SSI Stamping |
| 3 | | Nostro Auto Stamping | - Default Nostro Stamping - Currency code transformation (when receive SGO, lookup SGD) | | |
| 4 | | Dashboard | | | FX cashflows are in SUSPENDED status |
| 5 | | Grouping Blotter | | 1. FX cash (spot/forward/swap) should be in SUSPENED Status 2. Bypass MO validation for FX cash (spot/forward/swap) | |
| 6 | | Cashflow Blotter | - New Fields introduced for Murex Flow - LIEN - Pending Fixing - Duplicate NDS - LTID, Structure ID, NID - Commodity Flag - Alpha Clearing | - New Fields Required - Murex Fields Equivalent in FMRP | |
| 7 | | SWIFT Generation | - MT Generation - MT103, 202, MT103+202COV, MT210, FlipMT202, MT192, MT292, MT604, MT605, MT692 - MX Generation - Pacs.008.001.08 (MT103) - Pacs.009.001.08 (MT202 & 202COV) - Camt.056.001.08(MT192 & MT292) - **camt.057(MT210)** | - New Message types required - Format changes required for new product / flow | |
| 8 | | Accounting Generation | - EBBS - Real Time Feed - ASPIRE Integration - EOD Feed | - Keystone (HK): Feed Nostro & Over Account to EBBS, feed Suspense to Aspire - Move from Aspire to EBBS model - handling of historic cashflows & events on past value cashflows post cutover | |
| 9 | New Event | Exercise | | | will generate a FXD trade which in SUSPENDED status |
| 10 | | Expiry | | | Trade is settled with settlement fee |
| 11 | Booking Model Impact | Package Bookings | B2B Package | | |
| 12 | | | Package Booking Model | | |
| 13 | | | RFR Booking Model (Netting based on LTID) | | |
| 14 | | | Swap Agent | | |
| 15 | | | ND Currency Handling (ND CCS / ND IRS) (Netting based on NID) | | |
| 16 | | | Structures (Netted based on Structure ID) | | |
| 17 | | Rollover | | | |
| 18 | | Fixing | | | |
| 19 | | Option | Exercise & Expiry | | |
| 20 | | Strategy / Typology | | How Strategy / Typology will be supported in FMRP | |
| 21 | | Clearing | | | |
| 22 | | LIEN | | How LIEN will be available as part of Trade Migration | |
| 23 | | Allocation | | | |
| 24 | | FX Replication | | - Razor FX Dev team to be engaged on Dev changes / UAT support required - Razor FX Settlement team needs to be engaged for UAT support | |
| 25 | NETTING | BILATERAL MANUAL NETTING | | | |
| 26 | | CCIL MANUAL NETTING | | | |
| 27 | | BIC NETTING (MANUAL) | | | |
| 28 | | NDS AUTO NETTING | | | |
| 29 | | IRS AUTO NETTING | | | |
| 30 | | CROSS PRODUCT NETTING WITHIN RATAN | | | |
| 31 | STATIC | BILATERAL NETTING | | | |
| 32 | | BIC NETTING | | | |
| 33 | | VOSTRO SSI | | New Settlement Means & Settlement Account | |
| 34 | | NOSTRO [Golden Source TBC ] | | New Settlement Means & Settlement Account | |
| 35 | BUSINESS RULES | NSTP RULES | | - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity | |
| 36 | | SWIFT SUPPRESSION RULES | - Auto Debit by Agent - Nostros shared with other entity (example: China) | | |
| 37 | | CASFHLOW SUPPRESSION RULES | | - There're specific filter logic in Murex → RATAN cashflow interface to exclude auto suppression counterparties. Need to config these as RATAN suppression rule so that they can be suppressed for STELLA cashflows | |
| 38 | | Authorization Limits | | | |
| 39 | Settlement Method | CCIL | | | |
| 40 | | DVP | NSTP based on DVP | | |
| 41 | Migration | - Murex to FMRP Migration - Prevent Duplicate payment - Cutover handling - New Function / Changes - Historical data handling | | ISO Migration: handling of near value cashflows & events on past value cashflows post cutover | |
| 42 | CONFIG | LMS Entity List | | | |
| 43 | | [Murex Cash Migration Only] Entity list for the Batch Solution | | | |
| 44 | | - BCS vs Strategic Routing - Entity whitelist for in scope entities (covered via Cashflow Suppression rule) - Entity whitelist setup to send to RAZOR or handle in RATAN (RATAN generates SWIFT & Accounting | | | |
| 45 | | SWIFT Generation Changes - Booking Entity FMID - Booking Entity SWIFT BIC (Sender BIC in SWIFT) - Field 53 SWIFT BIC (for Local Currency LCY & Over Account) - Field 58 SWIFT BIC (for Flip MT202) - Branch code mapping - Any other branch specific requirement on SWIFT | | | |
| 46 | | Currency Release Time | | | |
| 47 | | NDS Auto Netting | | | |
| 48 | | Pending Fixing STP/NSTP Control( in case new product have fixing events) | | New STELLA products which require pending fixing - Loan Deposit: Principal and Interest netting together | |
| 49 | | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | | | |
| 50 | | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | | Whether onshore ccy is applicable | |
| 51 | | Currency Transformation (example SGO to SGD) - Use SGD to lookup Vostro - Use SGD to lookup Nostro | | | |
| 52 | | Settlement Accounting - Bridge Account # - EBBS Branch code - EBBS Transaction type - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | | Whether onshore ccy is applicable and what should be sent to downstream | |
| 53 | | Include new branch in GUI Drop down - Cashflow Blotter - Dashboard | | | |
| 54 | | Vostro SI Input Screen - Include New Settlement Means | | | |
| 55 | | Rounding | | | |
| 56 | | Restriction on Netting over Netting - only IRS is allowed. ND IRS follows same ISDA taxonomy | | Any new product that requires netting over netting to be supported Need to update config to allow ND CCS | |