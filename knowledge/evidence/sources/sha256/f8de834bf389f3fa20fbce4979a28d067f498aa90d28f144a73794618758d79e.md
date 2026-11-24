| | Function | Feature | Breakdown | Consideration | Comment |
| --- | --- | --- | --- | --- | --- |
| 1 | GENERIC | SI INPUT | - Missing Vostro - Multi Vostro - Adhoc SI update - Missing Nostro | | No changes |
| 2 | SSI Auto Stamping | - SSI Auto Stamping Hierarchy (**Old **CN/SG/IN/MY/EG/SA/NP/AG/LOANIQ vs **New **UK & new onboarding) - CFI code Selection( Only looking up first 2 characters and special logic on IRS/CCS only) - Settlement Method (FEDWIRE / CASH) - Single Agent / Two Agent Supported (3 Agent not supported) - Trade SSI Stamping to CDUPS (XML + Product based) - Currency code transformation (when receive SGO, lookup SGD) | Any new currency transformation required | KRO to KRW |
| 3 | Nostro Auto Stamping | - Default Nostro Stamping - ~~Currency code transformation (when receive SGO, lookup SGD)~~ | | follow default |
| 4 | Dashboard | - New data statistic calculation requirement - Country code/Booking entity dropdown update if new entity onboarding | | Add Korea in dash board |
| 5 | Grouping Blotter | - New requirement adding more cashflow attributes for query & display | | NA |
| 6 | Cashflow Blotter | - New Fields introduced for Murex Flow - Family/Group/Type/Strategy/Typology - Counterparty Murex Code - LIEN - Pending Fixing - Duplicate NDS - LTID, Structure ID, NID - Commodity Flag - Alpha Clearing - [UK - Murex -> RATAN cashflow feeding - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/UK+-+Murex+-%3E+RATAN+cashflow+feeding) | - New Fields Required | |
| 7 | SWIFT Generation | - MT Generation - MT103, 202, MT103+202COV, MT210, FlipMT202, MT192, MT292, MT604, MT605, MT692 - MX Generation - Pacs.008.001.08 (MT103) - Pacs.009.001.08 (MT202 & 202COV) - Camt.056.001.08(MT192 & MT292) - **camt.057(MT210)** | - New Message types required - Format changes required for new product / flow - Is there overlap or release dependency with ISO release | pacs008, 009, Camt.056 MT210 TBC with ISO when they migration MT210 |
| 8 | Accounting Generation | - EBBS - Real Time Feed - ASPIRE Integration - EOD Feed | - Move from Aspire to EBBS model - handling of historic cashflows & events on past value cashflows post cutover | |
| 9 | Booking Model Impact | Package Bookings | B2B Package | | No dependency |
| 10 | | Package Booking Model | | No dependency |
| 11 | | RFR Booking Model (Netting based on LTID) | | No |
| 12 | | Swap Agent | | No |
| 13 | | ND Currency Handling (ND CCS / ND IRS) (Netting based on NID) | | Yes, net in RATAN |
| 14 | | Structures (Netted based on Structure ID) | | No dependency |
| 15 | Rollover | | | |
| 16 | Fixing | | | |
| 17 | Option | Exercise & Expiry | | No dependency |
| 18 | Strategy / Typology/Portfolio | | - Are there any special handling for Strategy/Typology - Are there any special handling for portfolio | |
| 19 | Clearing | | | Yes, KRX ot be added as netting counterparty |
| 20 | LIEN | | Will LIEN be required as part of Cashflow Migration? | No Liend |
| 21 | Allocation | | | |
| 22 | FX Replication | | Is it applicable? | Yes |
| 23 | FXU | | | Yes, but no dependency on FXU |
| 24 | NETTING | BILATERAL MANUAL NETTING | | | no dependency |
| 25 | CCIL MANUAL NETTING | - Murex products are used in the logic, need to update with STELLA attributes - Settlement Method is stamped only in RATAN, need to consider if STELLA will stamp | | no dependency |
| 26 | BIC NETTING (MANUAL) | | | No |
| 27 | NDS AUTO NETTING | | - Do we have NDS auto netting in Murex | Yes |
| 28 | IRS AUTO NETTING | - Support Stella IRS now, required for other Stella booking user cases e.g. Coupon & Notional auto netting - Another user case: Structure booking IRS & Loan Depo interest netting together( not supported now given it's different trades) | - IRS net resultant needs to STP/NSTP? | Yes, follow current |
| 29 | CCS AUTO NETTING | - Principle and coupon net - NDCCS net between 2 legs | - Net resultant needs to STP/NSTP? | Yes, follow current |
| 30 | Auto Netting Feature | - Any new rule created should not conflict with existing rules - Netting Rules created based on Murex values to be updated with STELLA values | | No dependency |
| 31 | Swap Agent Auto Netting | - Any new rule created should not conflict with existing rules | | No |
| 32 | Restriction on Netting over Netting - only IRS is allowed. ND IRS follows same ISDA taxonomy | | - Any new product that requires netting over netting to be supported | follow current |
| 33 | Splitting | Update of Split Status to STELLA Generation of Split Cashflows | | | no dependency |
| 34 | FXU | | Dependency on FXU workflow to be considered | | no dependency |
| 35 | STATIC | BILATERAL NETTING | | | Yes |
| 36 | BIC NETTING | | | No |
| 37 | VOSTRO SSI | | - New Settlement Means & Settlement Account - Swift Generation logic - Include or exclude from LMS feeding? - Need to bypass accounting? | Yes, new Sett means to be agreed. LMS not onboarded yet need to generate sett accounting for all sett account |
| 38 | NOSTRO [Golden Source TBC ] | | New Settlement Means & Settlement Account | New sett acct required |
| 39 | BUSINESS RULES | NSTP RULES | | - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity | to be agreed |
| 40 | SWIFT SUPPRESSION RULES | - Auto Debit by Agent - Nostros shared with other entity (example: China) | | to be agreed |
| 41 | CASFHLOW SUPPRESSION RULES | - There're specific filter logic in Murex → RATAN cashflow interface to exclude auto suppression counterparties. Need to config these as RATAN suppression rule so that they can be suppressed for STELLA cashflows - There's suppression rule define the onboarded entity white list: Need to update for new entity onboarding - Need to add cashflow suppression rule for FX products (exclude Egypt, Nepal, Saudi) | | to be agreed |
| 42 | Authorization Limits | | | no change |
| 43 | Settlement Method | CCIL | | - Implemented for Murex - How's the FMRP Stella design | NA |
| 44 | DVP | NSTP based on DVP | - New requirement on auto DVP? - Integration with eBBS RTA for auto DVP? | setup NSTP rule, no other dependency |
| 45 | Trade Migration | - Murex to FMRP Migration - Prevent Duplicate payment - Cutover handling - New Function / Changes - Historical data handling - Write back Trades (B2B package trades where only one Booking Entity is in scope of migration and the other is not in scope. The trade will be cancelled as a package so cancellation & new trade will be flown **into Murex **for the Booking Entity which is not in scope | | ISO Migration: handling of near value cashflows & events on past value cashflows post cutover Write Back trades - prevention of **duplicate payment **on Murex trades if already paid using Murex trade on entities not in scope | not applicable for cashflow migration |
| 46 | FMRP Events | - BOOK - WITHDRAW - AMEND - EARLY TERMINATE - FIXING - REFIXING - CLEARING - NOVATION - CLOSE OUT - PORTFOLIO REASSIGNMENT - UNDO - MATURITY - EXPIRY | | - New Events that will be introduced - Payment Duplication Control - Support of Undo - Confirmation Match Status driving Settlement - STP / NSTP Control | not applicable for cashflow migration |
| 47 | FMRP Products | - IRS - CCS - FX - NDF - SCF - Loan Depo | | - New Products that will be introduced - Support of Undo - Confirmation Match Status driving Settlement - STP / NSTP Control | not applicable for cashflow migration |
| 48 | Touch Point Data | | | - Any New actions introduced need to be updated to FMMIS for STP / NSTP calculation | not applicable for cashflow migration |
| 49 | CONFIG | LMS Entity List | | | LMS entity filter will be removed |
| 50 | | SWIFT Generation Changes - Booking Entity FMID - Booking Entity SWIFT BIC (Sender BIC in SWIFT) - Field 53 SWIFT BIC (for Local Currency LCY & Over Account) - Field 58 SWIFT BIC (for Flip MT202) - Branch code mapping for tag 20 calculation - Field 26 of MT604: Relying on Murex **Strategy **& **Allocation **table - Any other branch specific requirement on SWIFT | | | required |
| 51 | | Currency Release Time | | | no special criteria |
| 52 | | Pending Fixing STP/NSTP Control( in case new product have fixing events) | | New STELLA products which require pending fixing - Loan Deposit: Principal and Interest netting together | use murex flag |
| 53 | | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | | - Whether onshore currency is applicable | KRO to KRW required for payment and accounting |
| 54 | | Settlement Accounting - Bridge Account # - EBBS Branch code - EBBS Transaction type - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | | Whether onshore currency is applicable and what should be sent to downstream | balaji to confirm |
| 55 | | Vostro SI Input Screen - Include New Settlement Means | | | no new sett means |
| 56 | | Rounding | | | trunaction, to be agreed. |
| 57 | Open Firewall for users in new location | | | | |
| 58 | TDS3 Integration dependency | Trade confirmation status (TDS3?) | | | Required |
| 59 | | NDS auto netting | | | yes |
| 60 | | LIEN | | | No |
| 61 | Korea customized features? | MT/MX? | | | MX for all except MT210 |
| 62 | | Integration with Murex Korea by solace? | | | ??? |
| 63 | | Korea language issue? Require to support in SSI, SCI, cashflow data? | | | no dependency on korean characters SSDR report dependency - Yes |
| 64 | GO Live | | | - GO Decision Criteria - UVT Verification points | N/A for analysis |