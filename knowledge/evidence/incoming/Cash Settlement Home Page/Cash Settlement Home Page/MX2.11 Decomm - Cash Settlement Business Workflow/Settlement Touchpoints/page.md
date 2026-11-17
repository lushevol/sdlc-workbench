<<<Erroneous Payment Incidents to be added>>>

| # | Process | Touchpoint | Day 1 (China) | Target State | Dependency |
| --- | --- | --- | --- | --- | --- |
| 1 | NSTP Criteria | Cashflow Affirmation done before payment release | - NSTP capability for Corporate clients. Client Type to be consumed from SCI and group as Interbank / FIs / Corporate - Affirmation is required or we can enable STP based on Confirmation Full Match status / Full Affirmation (Trade Level) - Tag specific clients as NSTP as required - Ability to break STP at a cashflow level (by MO / TCG / Conf / Sett users) - Ability to break STP at a Client / Product taxonomy / Strategy Currency level / all cashflows of a Structured transaction | - Enable STP based on Confirmation Match status (Trade Level) - Trigger Email Notification in lieu of Affirmation - Full Automation for eligible clients via S2B NG | - Day1: Elimination of mandatory Cashflow Affirmation as a process with communication to clients - TBC on Reg Reporting requirements as Bank / Non_Bank (whether RATAN will be used) - Equivalent of Strategy TBC |
| 2 | Manual Payment outside MX2.11 (Opics / AMH) | Manual Payment done via Opics due to Agent Bank not setup in MX2.11 | Can process via RATAN as no dependency on Agent bank setup | -do- | |
| Nostro Static not setup (multiple Nostros) | Multiple Nostros supported | -do- | |
| Manual Payment due to no RMA | Continue current state | Embed RMA status check via AMH integration - SSI+ (For SSI setup) - RATAN (manual input) | Prioritization / API's from AMH |
| Rounding Differences | TBC on rounding logic & CCY's used by STELLA | - Use RDM as the golden source for CCY Rounding rules - RATAN to subscribe to RDM for Net cashflows | |
| Special Characters in Beneficiary Name | - Control in RATAN to stop capture of Special character - Trigger Exception in RATAN if special character is present in SSI (or) use a field which does not contain special characters - Do a one-time cleanup of special character in SSI+ | - Implement control in SSI+ and RATAN to stop capture of special characters | - Determine if a separate field can be used for Bene name - Alignment with RTS on Target state |
| Pay the differential in case of amendments post payment release | Continue current state | - Ability to net the reversal cashflow and the new payment to pay the differential | - Stella to support differential payment - Check Impact on LMS |
| Past Value Date payments | - Ability to support Past Value date payment - NSTP the cashflow - User select the Value date of the SWIFT (not the cashflow) | -do- | |
| Split Payment | Support Split Payment | -do- | |
| Switching of funds | Handle via Payment generation module in OSCAR | Ability to auto attach SSI based on Counterparty instead of keying in the full SSI | |
| Claims Processing for back value / interest claim | Handle via Payment generation module in OSCAR | -do- | |
| Beneficiary Long Name character limitation | TBC on characters supported in MX2.11 vs RATAN | | |
| Payment Module not enabled in certain Legal Entities | All Legal Entities are supported | | |
| Payment amount above threshold | Auto split if above threshold | | |
| Flip debit across entities | Support debit across entities | | |
| MT101 / 104 to debit client account held with another bank | Continue current state | Ability to support generation of MT101 / 104 | TBC on support model |
| 3 | Affirmation | Email Affirmation with Clients via Outlook (Gross / Net) [Macro used for generating the email draft and released at a single level] | Continue current state | - Trigger Email Affirmation from RATAN (NET / GROSS). - Auto release for some clients (both NET / GROSS) - STP for Affirmation done by clients via S2B NG | - New Static - Client Contact List maintained with Maker / Checker - Static to determine which clients need affirmation - Templates to be used (Example: NET vs GROSS and Notification vs Response required) - Explore CDU PS / MDIS to leverage fixing notice |
| 4 | Netting | Bilateral Netting - Netting of cashflows (Maker / Checker) | Partial Automation: Setup Auto Netting at Client level based on pre-defined Netting time. Checker validation will be manual | - Full Automation for eligible clients via integration with external venues (S2B NG / CLSNET / BATON etc) | Granularity of client static - CCY pair based netting etc |
| Cross Product Netting |
| 5 | SI Input | Manual input of SI with Maker / Checker | Continue current state | - Full Automation for eligible clients via S2B NG - Auto selection from Multiple SSI based on incoming confirmation (triggered by user in CDU PS) | Build in CDU PS to feed the SSI to be selected |
| 6 | Settlement Method Change | Change from one settlement method to another (CLS / NET to GROSS) | TBC if required for Day1 | - Stamp Settlement Method on pre-Trade - Support to change from one Settlement Method to another | Golden source to be established for Settlement Method values and Criteria |
| 7 | DVP / Overnight deposits | Rare | Continue current state | - Auto release payment based on funds receipt confirmation from EBBS / Nostro Agent - Integration with CIS for Metal CCY? | |
| 8 | DVP / BOE on Commodity Trades | Payment released after advise from Onshore team | Continue current state | Target state to be defined along with CTMU team | |
| 9 | Commodity Trades Handling | Settlement done in SGE platform, Murex cashflow for precious metal will push to SUPP. Murex csahflow for non precious metal is push to SENT status with SSI as SUPPRESSXXX Manual post an GLTE (DVSUS vs Nostro) to clear the break via OPICS. | Continue current state | Target state to be defined along with CTMU team | |
| Gold Purchased: USD Payment under Murex FX facing SCB London must be suppressed, in order to avoid duplicate payment as local FMO CC will arrange for it. | Continue current state | Target state to be defined along with CTMU team | |
| 10 | CDS Premium Settlement | Settlement done in SCH platform, Murex cashflow will push to SUPP/push to SENT as SUPPRESXXX. Manual post an GLTE (Suspense vs PBOC Nostro) to clear the break via OPICS. | TBD with Clearing team Identifier TBC | Target state to be defined along with Clearing team | |
| 11 | Mandatory Currency Requirements | IRS FCY if IRS Profit- Capture POP in F72 manually | IRS BOP will be a standard code to be populated in field 72 of payment for certain vanilla IRS. 'FDL IRS Profit' is the code irrespective of CCY Identifier TBC <<<TBC if applies to other products>>> | Control to ensure capture of mandatory ote, | |
| | | CNY / other CCY requirements to be enriched | | | |
| 13 | CCS Trades Handling (China only) | CCS for Corporate clients - check if Settlement is done by CMS team; suppressed in MX2.11 | - NSTP in RATAN for China entities and Continue current state - STP for other entities | Target state for China to be defined along with CMS team | |
| | Maturity PCD | If client account is capital need to engage CMS for settlement | NSTP in RATAN and Continue current state | Target state to be defined along with CMS team | |
| | Structured Deposit | Strategy = 'IR_DEPO_CNOENH' | Discuss in Recon workshop | TBC based on F2B booking model | |
| | Insufficient Funds in Client account | Debit the existing client ebbs account balance, the shortfall the client will purchase an FX to settle. Therefore, manual settle via OPICS | If always for COM SWAP, then current state | TBC based on driver for Opics usage | |
| | Bond Handling | All cashflows where group = 'Bond' trades are payment suppressed/ TYPOLOGY SLT_CUS or SLT_Bank will be handled by Deriv Setts, rest are suppressed | NSTP in RATAN and Continue current state | TBC as Potential overlap with LoanIQ. | |
| | TPP | TPP Approval (Email) | Continue current state | Interface with ONE SALES for TPP approval workflow | |
| | TPP Reporting - Manual Flag capture in MX2.11? | 1) A SSI can be flagged as TPP in SSI+ and flown into RATAN 2) Settlement User can manually flag a Cashflow as TPP | Include RATAN as a source into Tableau TPP report | Add RATAN data into TPP Tableau Report |
| | Payment Auto Suppression | HUCUN Client - Payment is suppressed in MX2.11 | Add to Payment suppression table Identifier TBC | -do- | |
| | Payment & Accounting Auto Suppression | ?? | Add to Cashflow Suppression table | -do- | |
| | Manual Validation | Eyeball check of - Mandatory Currency Information | - Automatic Validation & Highlight Exceptions in RATAN | Currency Information to be made mandatory in SSI+ | |
| | Payment Release Exceptions | Payments stuck in FMSRE | Continue current state | 1) For Feasible scenarios, fully automate by enhancing RATAN Directly integrate with FMSRE / equivalent to take required action from RATAN itself (or) Integrate via OpenFIN | Further analysis required on all manual handling scenarios |
| | Payments stuck in AMH | | | |
| | Potential Netting / Rollover Client | NSTP for Corporates | STP after a pre-defined cutoff time | -do- | New Static - Potential Netting / Rollover Client |
| | GSAM Client | | NSTP with 'GSAM' exception | Potential workflow for GSAM Approval | |
| | Settlement Method Amends | Email approval from TRM team to change from CLS/NET/DVP/BOE to Gross | Continue current state | Approval workflow with HORIZON | |
| | LIEN | Email approval from ??? | Continue current state | Lien placement / removal workflow with ??? | |
| | GLTE Posting | For CPN??? | | | |
| | Failed Trades | | Reprocess via RATAN | -do- | |
| | Return of Funds | | | | |
| | Nostro Fund Transfer | | | | |
| | CFETS | | | | |
| | Clearing Process | | | | |
| | Strategies that result in NSTP | | | | |
| | [FMRP Open Items - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/FMRP+Open+Items) | | | | |