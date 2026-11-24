# F2B milestones

| **Mile****s****tone** | **Products** | **Market Events** | **Entities** | **Trade Migration** | **Requirement For Settlement** | **UAT & Release Plan** | **ADO** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Loan Depo (Drop 4.0) | Loan Depo | Events built for CN Rates | CN | NA | UAT & Release support | Release in Jan | [Feature 6469299 F2B: CN Loan Depo Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469299/) |
| Prime PM | | | UK | NA | | Release in Feb | [Feature 6469316 F2B: UK Prime PM Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469316/) |
| Prime Rates | | | UK | Yes | UAT & Release support | Release in Apr | [Feature 6469341 F2B: UK Prime Rates Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469341/) |
| CN CCS Trade Migration | CCS | Events built for CN Rates | CN | Yes | UAT & Release support | Q1 | [dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469344/](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469344/) |
| FXO | TBC | TBC | TBC | TBC | TBC | TBC | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469382/](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469382/) |
| Global Rates - HK - TW - IN(LK, BD) - ASEAN(SG, MY, TH, VN) - G10 | * * | | | | | | [Feature 6469360 F2B: Global Rates Go Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469360/) |
| E- Precious(products same as Prime PM) | Same as Prime PM | Same as Prime PM | UK | Yes | UAT & Release support | Q2 | |
| Central Entitlements | | | | | | | [Feature 6469387 F2B: Central Entitlements](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469387/) |
| Keystone (Hongkong) | | | | | | | 6470013 |
| F2B: Continuous Testing | | | | | | | 6469401 |
| F2B: Build & Maintain | | | | | | | 6469448 |
| Strategic CPN | | | | | | | 5848448 |
| FXU | | | | | | | |
| CLS | | | | | | | |
| LOANIQ Day2 | | | | | | | |

# Murex Cashflow Migration

| Milestone | Entity | Requirement | ADO |
| --- | --- | --- | --- |
| Tranche 1 | HONGKONG SCS HK BANGKOK TAIPEI OBU TAIPEI NEWYORK | 1. New Accounting Interface: RATAN->Aspire 2. Static Data setup 3. UAT support & release process | [6469476 ](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469476/) |
| Tranche 2 | MAURITIUS DUBAI JAKARTA MANILA TOKYO JOBURG PHILIP FCU DIFC | 2. Static Data setup 3. UAT support & release process | 6469488 |
| Tranche 3 | JERSEY_BR Others | 2. Static Data setup 3. UAT support & release process | 6469527 |
| Manual Entities | | | |

# Day 2 New Feature

| Function | Priority | Entity & Business flow | ADO |
| --- | --- | --- | --- |
| Auto Netting | | Swap Agent Clearing Payment | [6469617](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469617/) |
| Split | | | [6469564](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469564/) |
| Concurrent User Warning | | Global | [6469584](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469584/) |
| Automate DVP | | Phase 1: Over Account DVP Phase 2: Precious Metals DVP (via CIS) Phase 3: External Nostro (can move to 2026) | [6469622](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469622/) |
| Auto Deduct WHT | | | [6469632](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6469632/) |
| CDUPS - Trade SI (Strategic) | | | 3624175 |
| Swap Agent Clearing ID | | Swap Agent Clearing Payment | |
| New Feature: Public Filter Creation / Modification Controls | | Global | 6470023 |
| New Feature: Swift MT101 | | | 6470024 |
| New Feature: Save SI | | | 6470035 |
| New Feature: CHATS / PvP | | | |
| SI Hierarchy Change | | | 6470039 |

# KTLO

- Settlement method change & exception handling: [Feature 2659506 [1] CN: Settlement Method change to be considered as a Financial Amendment](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/2659506/)
- Stella Event filter( e.g. expiry): [Stella Inbond cashflow filter - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Stella+Inbond+cashflow+filter)

- M: 6472953: Enable NDS Auto Netting for SG
- M: 6472969: Bulk Fail with Maker Checker
- M: 6472976: Bulk in Group Blotter
- M: 6472987: Remove Upper / Lower Case match between Maker & Checker for SI Input
- M: 6472996: Allow other actions on HOLD (SI input, netting, suppression)
- M: 6473001: Receipt Cashflow should not require Vostro if Adhoc Nostro SI is done (to ensure control exists for PM receipts & over account)
- M: 6275726: Notice to receive flag not ticked for SCB receive cashflow (bug)
- M: 5967610: Set Vostro as mandatory for Precious Metal receipts
- M: 6473021: Remove the BIC netting tagging after 'settle as gross' is done
- M:6286998: Egypt / Saudi: Auto select Nostro SI based on currency pair
- M: 6473032: Duplication check in RATAN (Same financials under Trade ID)
- S:6473039: BCS: Support Settlement for CN / MY for Equity Derivatives BCS
- S: 6473043: Nepal: New High Risk Approval Profile for USD 300 Mio
- S: 6473045: FX: Consume Confirmation Match status for FX Swap near leg for Cashflow STP
- M: 6473051: Static: Make business rules case agnostic (to prevent risk of failure)
- S: 6473055: Static: Make Business Rules Static Screen user friendly
- S: 6473062: COB feature for UAT purpose
- S: 6473065: Nostro duplication check - allow multiple nostro setup for FXBRREC when Ebbs account number is different
- S: 6473080: Display exceptions for Checker when Suppression is done
- 6419293: [China Group Pending] Offset the new/withdrawal on same payment within same group
- S: 6473084: Block Netting on Netting except for netting on IRS Fixed + Floating auto netted payments
- S: 6473089: Allow user who did netting to act as Checker
- S: 6473093: Include Debit / Credit indicator on SSI stamping
- S: 5997360: Auto Cashflow Suppress Zero amount cashflows
- S: 6473025: Break STP for Settlement using Blade Comments [subject to BLADE prioritization]
- S: 6473009: STP SCB counterparty cashflows
- S: 6343884: Ratan Release cutoff shifter refinement
- S: 5997797: 103&202Cov: swift status “Released by AMH” but cashflow are still in “Released” status
- S: 6473019: Update Dashboard SWIFT Error criteria to include MT103+202COV
- S:6090337: Update Cashflow status a Swift Suppressed for auto deleted cases in FMSGW
- M: 6040818: Add InterestRate:IRSwap:FixedFixed into IRS pending another leg check
- S: Generate warning for net resultant cancellation that user must manually send Swift cancellation