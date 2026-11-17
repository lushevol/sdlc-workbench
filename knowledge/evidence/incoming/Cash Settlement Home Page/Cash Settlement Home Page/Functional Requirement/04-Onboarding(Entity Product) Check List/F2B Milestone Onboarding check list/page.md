| | Function | Feature | Breakdown | Consideration |
| --- | --- | --- | --- | --- |
| 1 | GENERIC | SI INPUT | - Missing Vostro - Multi Vostro - Adhoc SI update - Missing Nostro | |
| 2 | SSI Auto Stamping | - SSI Auto Stamping Hierarchy (**Old **CN/SG/IN/MY/EG/SA/NP/AG/LOANIQ vs **New **UK & new onboarding) - CFI code Selection( Only looking up first 2 characters and special logic on IRS/CCS only) - Settlement Method (FEDWIRE / CASH) - Single Agent / Two Agent Supported (3 Agent not supported) - Trade SSI Stamping to CDUPS (XML + Product based) - Currency code transformation (when receive SGO, lookup SGD) - **Not supported yet** | Any new currency transformation required |
| 3 | Nostro Auto Stamping | - Default Nostro Stamping - Currency code transformation (when receive SGO, lookup SGD)- **Not supported yet** | |
| 4 | Dashboard | - New data statistic calculation requirement - Country code/Booking entity dropdown update if new entity onboarding | |
| 5 | Grouping Blotter | - New requirement adding more cashflow attributes for query & display | |
| 6 | Cashflow Blotter | - New Fields introduced for Murex Flow - Family/Group/Type/Strategy/Typology - Counterparty Murex Code - LIEN - Pending Fixing - Duplicate NDS - LTID, Structure ID, NID - Commodity Flag - Alpha Clearing - What's the equivalent FMRP fields | - New Fields Required - Murex Fields Equivalent in FMRP |
| 7 | SWIFT Generation | - MT Generation - MT103, 202, MT103+202COV, MT210, FlipMT202, MT192, MT292, MT604, MT605, MT692 - MX Generation - Pacs.008.001.08 (MT103) - Pacs.009.001.08 (MT202 & 202COV) - Camt.056.001.08(MT192 & MT292) - **camt.057(MT210)** | - New Message types required - Format changes required for new product / flow - Is there overlap or release dependency with ISO release |
| 8 | Accounting Generation | - EBBS - Real Time Feed - ASPIRE Integration - EOD Feed | - Keystone (HK): Feed Nostro & Over Account to EBBS, feed Suspense to Aspire - Move from Aspire to EBBS model - handling of historic cashflows & events on past value cashflows post cutover |
| 9 | Booking Model Impact | Package Bookings | B2B Package | |
| 10 | | Package Booking Model | |
| 11 | | RFR Booking Model (Netting based on LTID) | |
| 12 | | Swap Agent | |
| 13 | | ND Currency Handling (ND CCS / ND IRS) (Netting based on NID) | |
| 14 | | Structures (Netted based on Structure ID) | |
| 15 | Booking in new Non ISO ccys | | - SSI Replication is required - Nostro static to be setup in Non ISO ccy - NSTP rules update to be done - Netting will be a problem if some cashflows are in ISO ccy from Murex (SGD) and other cashflows are in SGO from Stella. |
| 16 | Rollover | | |
| 17 | Fixing | | |
| 18 | Option | Exercise & Expiry | |
| 19 | Strategy / Typology | | - How Strategy / Typology will be supported in FMRP - Settle to LOCO London vs ZURICH - Booked as XAU but meant for Physical delivery (BOE) - Strategy field mapping to field 26C (mapping exists in tradehub) |
| 20 | Clearing | | |
| 21 | LIEN | | How LIEN will be available as part of Trade Migration |
| 22 | Allocation | | |
| 23 | FX Replication | | - Razor FX Dev team to be engaged on Dev changes / UAT support required - Razor FX Settlement team needs to be engaged for UAT support |
| 24 | Financial Field check | | New field to be added as a financial field, else amendments will be dropped as non financial amend |
| 25 | FXU | | |
| 26 | Commodity Flag | | Net Resultant is updated as Commodity flag = Y | Need to add new commodity products into the logic so that cashflows will get captured as Comm flag = Y |
| 27 | PORTFOLIO | Nostro Stamping | RFI Stamping | - Portfolio will change when migrated to FMRP so need to update the existing Nostro Static with RFI portfolio |
| 28 | NETTING | BILATERAL MANUAL NETTING | | |
| 29 | BILATERAL AUTO NETTING - Not Supported Yet | | |
| 30 | CCIL MANUAL NETTING | - Murex products are used in the logic, need to update with STELLA attributes - Settlement Method is stamped only in RATAN, need to consider if STELLA will stamp | |
| 31 | BIC NETTING (MANUAL) | | |
| 32 | NDS AUTO NETTING | | - Supported Murex only, how this handle in FMRP |
| 33 | IRS AUTO NETTING | | - Support Stella IRS now, required for other Stella booking user cases e.g. Coupon & Notional auto netting - Another user case: Structure booking IRS & Loan Depo interest netting together( not supported now given it's different trades) |
| 34 | CROSS PRODUCT NETTING WITHIN RATAN | | |
| 35 | Auto Netting Feature | | - Any new rule created should not conflict with existing rules - Netting Rules created based on Murex values to be updated with STELLA values |
| 36 | Swap Agent Auto Netting | | - Any new rule created should not conflict with existing rules - Impact to this rule might create duplicate payment |
| 37 | Splitting | Update of Split Status to STELLA Generation of Split Cashflows | | |
| 38 | FXU | | | Dependency on FXU workflow to be considered |
| 39 | STATIC | BILATERAL NETTING | | |
| 40 | BIC NETTING | | |
| 41 | VOSTRO SSI | | - New Settlement Means & Settlement Account - Swift Generation logic - Include or exclude from LMS feeding? - Need to bypass accounting? |
| 42 | NOSTRO [Golden Source TBC ] | | New Settlement Means & Settlement Account |
| 43 | BUSINESS RULES | NSTP RULES | | - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity |
| 44 | SWIFT SUPPRESSION RULES | - Auto Debit by Agent - Nostros shared with other entity (example: China) | |
| 45 | CASFHLOW SUPPRESSION RULES | | - There're specific filter logic in Murex → RATAN cashflow interface to exclude auto suppression counterparties. Need to config these as RATAN suppression rule so that they can be suppressed for STELLA cashflows. Link below for tracking - [Murex to RATAN Cashflow Suppression Rules Translation to FMRP - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Murex+to+RATAN+Cashflow+Suppression+Rules+Translation+to+FMRP) - There's suppression rule define the onboarded entity white list: Need to update for new entity onboarding - Need to add cashflow suppression rule for FX products (exclude Egypt, Nepal, Saudi) |
| 46 | Authorization Limits | | |
| 47 | Settlement Method | CCIL | | - Implemented for Murex - How's the FMRP Stella design |
| 48 | | DVP | NSTP based on DVP | - New requirement on auto DVP? - Integration with eBBS RTA for auto DVP? |
| 49 | Trade Migration | - Murex to FMRP Migration - Prevent Duplicate payment - Cutover handling - New Function / Changes - Historical data handling - Write back Trades (B2B package trades where only one Booking Entity is in scope of migration and the other is not in scope. The trade will be cancelled as a package so cancellation & new trade will be flown **into Murex **for the Booking Entity which is not in scope | | ISO Migration: handling of near value cashflows & events on past value cashflows post cutover Write Back trades - prevention of **duplicate payment **on Murex trades if already paid using Murex trade on entities not in scope |
| 50 | FMRP Events | - BOOK - WITHDRAW - AMEND - EARLY TERMINATE - FIXING - REFIXING - CLEARING - NOVATION - CLOSE OUT - PORTFOLIO REASSIGNMENT - UNDO - MATURITY - EXPIRY | | - New Events that will be introduced - Payment Duplication Control - Support of Undo - Confirmation Match Status driving Settlement - STP / NSTP Control |
| 51 | FMRP Products | - IRS - CCS - FX - NDF - SCF - Loan Depo | | - New Products that will be introduced - Support of Undo - Confirmation Match Status driving Settlement - STP / NSTP Control |
| 52 | Touch Point Data | | | - Any New actions introduced need to be updated to FMMIS for STP / NSTP calculation |
| 53 | CONFIG | LMS Entity List | | |
| 54 | | [Murex Cash Migration Only] Entity list for the Batch Solution | | |
| 55 | | - BCS vs Strategic Routing - Entity whitelist for in scope entities (covered via Cashflow Suppression rule) - Entity whitelist setup to send to RAZOR or handle in RATAN (RATAN generates SWIFT & Accounting | | |
| 56 | | SWIFT Generation Changes - Booking Entity FMID - Booking Entity SWIFT BIC (Sender BIC in SWIFT) - Field 53 SWIFT BIC (for Local Currency LCY & Over Account) - Field 58 SWIFT BIC (for Flip MT202) - Branch code mapping for tag 20 calculation - Field 26 of MT604: Relying on Murex **Strategy **& **Allocation **table - Any other branch specific requirement on SWIFT | | |
| 57 | | Currency Release Time | | |
| 58 | | NDS Auto Netting | | |
| 59 | | Pending Fixing STP/NSTP Control( in case new product have fixing events) | | New STELLA products which require pending fixing - Loan Deposit: Principal and Interest netting together |
| 60 | | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | | |
| 61 | | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | | - Whether onshore currency is applicable |
| 62 | | Currency Transformation (example SGO to SGD) - Use SGD to lookup Vostro - Use SGD to lookup Nostro | | |
| 63 | | Settlement Accounting - Bridge Account # - EBBS Branch code - EBBS Transaction type - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | | Whether onshore currency is applicable and what should be sent to downstream |
| 64 | | Include new branch in GUI Drop down - Cashflow Blotter - Dashboard | | |
| 65 | | Vostro SI Input Screen - Include New Settlement Means | | |
| 66 | | Rounding | | |
| 67 | | Restriction on Netting over Netting - only IRS is allowed. ND IRS follows same ISDA taxonomy | | - Any new product that requires netting over netting to be supported - Need to update config to allow ND CCS |
| 68 | GO Live | | | - GO Decision Criteria - UVT Verification points |