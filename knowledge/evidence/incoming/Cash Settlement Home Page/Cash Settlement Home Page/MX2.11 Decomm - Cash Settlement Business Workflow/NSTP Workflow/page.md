# NSTP Workflow

# Murex2.11 Exceptions

Link: [CN Settlement - Murex 2.11 Payment Non-STP Exception - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex+2.11+Payment+Non-STP+Exception)

# Exceptions Handling in RATAN

- All cashflows must have net button (unless it's a net cashflow) and split button (unless it's a split cashflow)
- In case of Checker rejecting an SI input by Maker, if the same Maker updates SI again, system must display the SI values previously input by him / her. Similarly after Maker corrects the SI, if same Checker does SI input, system must require dual blind input only for the fields which are mismatched between Maker and Checker or fields that were additionally enriched by Maker
- Nice to have: All exceptions to show Tool Tip on what is expected to resolve the exception

| | Process | Exception | China Day 1? | Identifier | Auto Resolution | Manual Action if not Auto Resolved | Button on Cashflow | Sub-status | Auth Limit Required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SSI Enrichment | **Missing Nostro** | **Y** | - No Nostro attached | - Attach Nostro if setup/refreshed & remove exception | - Lookup and Attach Nostro once setup | Maker : Select Nostro → Checker Dual Blind selection | Pending Operator | N |
| 2 | SSI Enrichment | **Missing Vostro** | **Y** | - No Vostro attached for Payments. - **For receipts, no exception required. System should stamp the default Nostro.** | - Attach Vostro if flown from SSI+ & remove exception | - Input Vostro - **System must trigger hard warning 'Nostro vs Vostro SI mismatch' during SI input if they are mismatched** | Maker : Input Vostro → Checker Input Vostro Dual Blind Input | Pending Operator | N |
| 3 | SSI Enrichment | **Secondary Vostro** | **Y** | - Single Secondary Vostro auto attached | Remove exception if Primary attached | Checker to Approve / Reject | 1. Checker - Approve 2. Checker - Reject with comment | Pending Verification | **Y** |
| 4 | SSI Enrichment | **Multi Nostro ** | N/A | - More than one eligible Nostro found and none are setup as Primary - This exception will not be triggered as Primary SSI should get auto attached | - Attach if any Nostro is tagged as Primary & remove exception | - Select Nostro | Maker - Select Nostro | Pending Operator | N |
| 5 | SSI Enrichment | **Multi Vostro** | **Y** | - More than one eligible Vostro found and none are setup as Primary - Primary SSI should get auto attached | - Attach if any Vostro is tagged as Primary & remove exception | - Select Vostro / Input Vostro (in case required to input a different SI) | Maker - Input Vostro / Select Vostro | Pending Operator | N |
| 6 | SSI Enrichment | **Nostro vs Vostro Mismatch** | **Y** | - Settlement Means / Settlement Account is mismatched between Nostro / Vostro | - If Vostro / Nostro if setup/refreshed & remove exception | - Maker to change Nostro / Vostro - Dual Blind check applies | Maker - Input Vostro / Select Vostro / Select Nostro Dual Blind Input | Pending Operator | N |
| 7 | SSI Enrichment | **Adhoc SI** | **Y** | SSI auto attached on cashflow was modified by Maker | - (retain the maker input even if there is a new SSI flown from upstream since the SI on the cashflow was affirmed with client) | - Checker to Select SI and overwrite required fields - Dual Blind check applies - If rejected by checker, Maker will also see 'Adhoc SI' exception | Maker - Edit Vostro Checker - Input SI (blind input) / Reject SI | Pending Verification | N |
| 8 | Affirmation | **Pending Confirmation / Affirmation** | **Y** | Trade Unaffirmed / Unconfirmed + Cashflow Unaffirmed | Remove Exception if trade affirmed or confirmed / cashflow affirmed | Affirm Cashflow Affirm can be single level and separate exception triggered if above 100 Mio | Single level - Affirm Cashflow | Pending Operator | N |
| 9 | Netting | **Net Cashflow** | **Y** | Cashflow generated through Netting operation | If Netting was triggered / validated by external venue | Checker to Approve / Reject (or) Un-net Maker - Un-net - Un-net can be single level and separate exception triggered if above 100 Mio - If it is a Gross Client, cashflows should not STP after un-net - Same user who did un-net cannot release the cashflows in Gross | 1. Checker - Approve 2. Checker - Reject with comment 3. Note: Maker / Checker can perform Un-net | Pending Verification | Checker -** Y** (for release of Net cashflow. Not required for Un-net action) |
| **Previously Netted** | **Y** | Cashflows that were previously netted and the netting was cancelled either by user or by system | - | Checker to Approve Same user who did un-net cannot approve | Checker - Approve | Pending Verification | **Y** |
| **NET to Gross** | **Y** | Cashflow that is pending as 'Pending Netting' or 'Pending another leg'. Maker manually selects 'Settle as Gross' | - | Checker to Approve if it was wrongly done, both Maker and Checker can perform adhoc netting | Checker - Approve | Pending Verification | **Y** |
| 10 | Bad Business Day | **Bad Business Day** | **Y** | Feed from RDM | Remove exception if Holiday is removed | Checker to release Single level is fine aligned to user Authority Limits | Checker - Approve | Pending Verification | **Y** |
| 11 | Failed Payment | **Replayed from Failed status ** | **Y** | Cashflow was replayed from Failed status by Maker | - | - Maker to choose payment value date - Checker to choose payment value date in line with Maker | Checker - Pay as per original booking / current system date / select value date | Pending Verification | **Y** |
| 12 | NSTP Scenarios | **NSTP Client** | **Y** | NSTP Static Table in RATAN | if client is removed from table | Checker to Approve | Checker - Approve | Pending Verification | **Y** |
| **NSTP Product** | **Y** | NSTP Static Table in RATAN | if product is removed from table | Checker to Approve | Checker - Approve | Pending Verification | **Y** |
| **NSTP Currency** | **Y** | NSTP Static table in RATAN | if CCY is removed from table | Checker to Approve | Checker - Approve | Pending Verification | **Y** |
| **NSTP Cashflow***** *****Exception description based on NSTP Table** | **Y** | NSTP Criteria defined in the NSTP Table | if criteria is removed from table | Checker to Approve | Checker - NSTP Release | Pending Verification | **Y** |
| **NSTP Settlement Method** | **N** | Specific Settlement Method | if Settlement Method is removed from table | Checker to Approve | Checker - Approve | Pending Verification | **Y** |
| **Corporate Client** | **Y** | SCI - Client Type Whitelist Configurable as part of NSTP Table based on client type and product | - | Checker to Approve | Checker - Approve | Pending Verification | **Y** |
| 13 | GSAM | **GSAM Client** | **Y** | Use SCI values to determine GSAM tagging (Logic TBC) | if client removed from GSAM status | Maker to Approve the exception (based on email approval from GSAM team) | Maker - Approve → Checker - Approve | Pending Operator | **Y** **(for Checker)** |
| 14 | Splitting | **Split Payment** | **N** | Cashflow is generated by splitting | - | Checker to Approve | Checker - Approve | Pending Verification | **Y** |
| 15 | Amend / Cancel | **Cancel / Amend after payment release** | **Y** | Cancel / Amend post payment release Both reversal and new payment should stop for manual handling | - | 1) Net the reversal and new payment and release the difference (Maker & Checker) (or) 2) Checker to release cancellation first to cancel original payment & subsequently release new payment. System to trigger soft warning to Checker while releasing New Payment | Checker - Approve Any other actions (SI input / Netting / splitting should trigger Maker / Checker control) | Pending Verification | **Y** |
| 16 | High Value Payment Handling | **High Value Payment** | **Y** | Amount of Cashflow > USD 100 Mio + a manual touch occurred on the cashflow | - | Checker to Approve (Based on user Auth Limit) | Checker - Approve | Pending Verification | **Y** |
| 17 | Back Value Payments | **Back Value** | **Y** | - New trade is booked with back value date. - Value date on cashflow is less than current Business Date (based on currency cutoff time) - System should release the payment for cashflow value date if it's over account settlement (without any exception) | If value date is amended | - Maker to choose payment value date - Checker to choose payment value date in line with Maker | Maker - Pay as per original booking / current system date / select value date Checker - As above | Pending Operator | **Y** |
| 18 | Cashflow pending Fixing | **Pending Other Leg** | **Y** | - - Only one cashflow found for IRS trade during auto netting script | When fixing is completed on the floating leg system to auto net this cashflow | Checker to release payment if client asks to release the fixed cashflow separately | Checker - Approve | Pending Verification | **Y** |
| 19 | | MX2.11 Exceptions to be added | **Y** | [CN Settlement - Murex 2.11 Payment Non-STP Exception - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex+2.11+Payment+Non-STP+Exception) | | <<<To be reviewed against for next country rollouts>>> | | | TBC |
| 20 | Netting / Rollover | **Potential Netting / Rollover Client** | **N** | New Static table in RATAN, configurable by Legal Entity | Auto Release if not rolled over within a certain time | - No exception required, automatic deferred release is required - Ability to early release is required |
| 21 | SSI Enrichment | SSI Modified by Maker | **N** | SSI auto attached on cashflow was modified by Maker | - (retain the maker input even if there is a new SSI flown from upstream since the SI on the cashflow was affirmed with client) | Checker to Approve a) Field 70 / 72: system to highlight to Checker what was changed by Maker on the SSI b) All other fields: Blind input by Checker only for the fields that are updated by Maker Agreed as Day 2 | a) Checker - Approve / Reject with comments b) Checker - Input SI (blind input) | Pending Verification | **Y** |
| 22 | SSI Enrichment | **SI Manually Input** **Checker will receive 'Missing Vostro/Nostro' exception for dual blind input** | **N/A** | SI manually input by Maker | - | Checker to input SI / Reject Dual Blind Input by Checker | Checker - Input SI / Reject with comments Dual Blind Input by Checker | Pending Verification | **Y** |
| 23 | SSI Enrichment | **SI Rejected by Checker** | **N/A** | Reject action by Checker **Checker comments should be made available** | If Netting was done (or) primary SSI was auto attached | Maker to rectify the issue | Maker - Input Vostro / Select Vostro Maker - Select Nostro | Pending Operator | N |
| 24 | Payment Release | **Pending in FMSWIFT Gateway** **Day 1 flow will be via FMSRE** | **N** | Status feed from FM SWIFT Gateway | when action taken in FM SWIFT Gateway | 1) Explore possibility to trigger action (release / delete) from RATAN to the new system 2) If too complex, user to handle directly in FMSRE / new system | TBC | | 1) **Y** 2) N |
| 25 | TPP | **Third Party Beneficiary (TPP)** **TPP not supported in Deriv** | **N** | For SSI flown: Value from SSI+ For manual input of SI: Auto tagging by comparing Bene vs Counterparty | - | Checker to Approve | Checker - Approve | Pending Verification | **Y** |
| 26 | Amend / Cancel | **Pending Reversal Ack** **Day 1 flow will be via FMSRE** | **N** | Resultant of a reversal and New event | | Hard block to release new payment until reversal payment is Ackd by FM SWIFT Gateway System to trigger soft warning to Checker while releasing Payment "Releasing a New Payment might result in duplicate payment. Has the Original Payment cancelled / funds have been recalled?" with Yes, Proceed to release New payment / Exit buttons | | | |
| 27 | Lien | **Lien on Payment** | **N** | ??? | Auto release when Lien is removed | Maker & Checker to Approve | Maker - Approve → Checker - Approve | | **Y** |
| 28 | DVP | **DVP** | **N** | Client / Trade is tagged as DVP | Funds receipt confirmation from EBBS / TLM | Maker & Checker to Approve | Maker - Approve with comments Checker - Approve | Pending Operator | **Y ** **(for checker)** |
| 29 | Non-Nostro | **Non-Nostro** | **N** | Nostro setup as 'Non-Nostro' | | Checker to Approve | Single level - Approve (To be agreed with Jon / Arun) | | **Y** |
| 30 | No RMA | **No RMA** | **N** | RMA Data from AMH | RMA setup / User amends the SI | User to manually update the SI | Maker -Input / Select Vostro | | N |
| 31 | Netting | **Cash Netting** | **N** | Generated from Cash Netting | - | Checker to Approve | Checker - Approve | | **Y** |
| 32 | Settlement Method Amendment | **Net to Gross** | **N** | Changed from Net to Gross | If changed to NET / Cash Net | Checker to Approve | Checker - Approve | | **Y** |
| **Cash Net to Gross** | **N** | Changed from Cash Net to Gross | If changed to Cash Net | Checker to Approve | Checker - Approve | | **Y** |
| 33 | Netting | **CLS Net Cashflow** | **N** | Cashflow is generated by CLS Netting | Auto Release if system can validate from external source | Checker to Manually verify and release | Checker - Approve | | **Y** |

**Note: **Cover Flag Missing and Mandatory CCY information missing (example: routing info for RUB / MXN) should be part of SI input screen validation itself instead of a separate exception.

# **Cashflow Suppression**

- To be used for scenarios where **<u>payment and settlement accounting is not required</u>**
- Cashflow Suppress Rules Table will be used to auto suppress Cashflows
- If a client was incorrectly added to Cashflow suppression table, it has to be removed from Cashflow suppression table to resolve that
- Users can manually suppress a cashflow with Maker / Checker
- If Cashflow suppression was done in error, Un-suppression can be done until Value date.
- Un-suppression cannot be done beyond value date. If payment + accounting is required, it has to be handled via Oscar
- If there is any amendment / cancellation on the trade, then it will be handled as a new version by system and go through new lifecycle.

# **Payment Suppression**

- To be used for scenarios where we know that **<u>payment is not required</u>**
- Payment Suppress Rules Table will be created to auto suppress for scenarios where every single cashflow will be payment suppressed (clearing deals as an example)
- If a client was incorrectly added to Payment suppression table, it has to be removed from Payment suppression table to resolve that
- Manual suppression will go through Maker-Checker
- If suppression was done in error, Un-suppression can be done until Value date.
- Un-suppression cannot be done beyond value date. If payment required, it has to be handled via AMH / Oscar
- If there is any amendment / cancellation on the trade, then it will be handled as a new version by system and go through new lifecycle.

# **Cashflow Fail Process**

- To be used for scenario **<u>where payment is normally expected, but Ops are unable to process the cashflow on value date</u>** (instructions not received, dispute etc) with expectation to make payment subsequently
- System will auto fail at EOD any cashflows that were not RELEASED from RATAN.
- Can be manually marked as Failed via Maker / Checker during the day (if required)
- Maker can reinstate the cashflow after value date (when advised by Investigations as good to pay) and will go through Checker validation. Both Maker and Checker will have to select the value date of payment since Cashflow is now back value
- If a cashflow went to RELEASED / SETTLED status, it cannot be manually marked as Failed. This is to avoid risk of duplicate payment on a Cashflow that was already settled.
- If any failed settlement is identified after value date based on Nostro statement, then it has to be handled via AMH / Oscar.
- If there is any amendment / cancellation on the trade, then it will be handled as a new version by system and go through new lifecycle.