# Background

For the FX deals which are booked in FM booking system(S2BX, BLADE) tend to make a payment to Transaction Banking Client(Trade Services, Cash Management, or Security Services) account by intervention of CMO/Trade/Securities OPS. This is known as FX Utilization.

In the current environment, prior to settlement/value date, the client will instruct TB on how to ‘utilize’ the settlement currency amount.  Transaction Banking Operations (Trade Services, Cash Management, or Security Services) then login into SCPAY/FX Util to retrieve the deal, and apply payment instructions by link with AA code. Once claimed, the utilization details will be updated to RATAN.

- RATAN would publish bridge and util accounting to EBBS on real time base.
- SWIFT will be generated in Transaction Banking systems, which would send util accounting to PSGL
- Utilization accounting recon will be performed in TLM.

Ratan also opens API for BLADE and FXU for remaining amount query.

- In FXU, remaining amount will be used for further utilization.
- In Blade, remaining amount will be used for booking reverse trade.

# Function Requirement & key agreement

## MVP Scope

**Requirements**

1. 1. Product Scope: 1. Only FX (Spot, Forward & Swap) product is eligible for Utilization 2. Static Setup: 1. Ability to setup Clients who are eligible for Utilization 2. Ability to setup Client who are eligible for Auto Utilization 3. Booking: 1. Auto Stamp Trade & Cashflow Settlement Method as 'UTIL' for trades flown from upstream (S2BX) based on UTIL Client Static 2. Ability for FO user to select Settlement method as 'UTIL' during manual booking 3. Hard Block (soft block not allowed) must be triggered if trade is utilized. If amendment is required, Utilization must be reversed before deal can be amended 4. FO user be able to view remaining amount on the trade 5. FO user must be able to view the Client ID (SCI LEID) 4. Querying of Utilization data: 1. User must be able to view trade / cashflows that are Eligible for Utilization in RATAN 2. User must be able to view trade / cashflows that are utilized / unutilized in RATAN 3. Users must be able to view the <u>**trades**</u>** in FXU** (utilized / unutilized / remaining amount) 5. Utilization: 1. For UTIL trades, RATAN must have control to prevent settlement in Gross 2. RATAN must consume query / utilization **request from FXU **(Only full utilization for MVP) 3. ~~RATAN must allow **manual **utilization **directly **in RATAN by performing adhoc SI update action~~ 4. Utilized cashflows must be tagged to a different status to indicate they have been utilized 5. If Unutilized until EOD, RATAN must auto utilize to FXBRREC** **Rajesh to check if account numbers will be different between FCY and LCY 6. If trade is cancelled / Already Utilized (Auto / Manual), Utilization request from FXU must be rejected 7. RATAN should store remaining amount information and expose to FXU and Blade 8. Audit Information of Utilization must capture whether it was utilized via FXU, Auto Utilized or Manual Utilized 9. Information must be sent to downstream systems - TLM, RATAN EOD, SSDR, FMMIS Rajesh to engage FMMIS 10. If user selected UTIL as settlement method in Blade booking, and client doesn't exist in utilization static, FXBRREC-M will be set as default value for manual utilization. 6. Notes: 1. Any attributes set as mandatory / Rejection of Util request for absence of mandatory fields by RATAN should be explicitly agreed.

**Solution Design**

- Full Utilization (To fully utilize the full amount of cashflow original amount on VD) - <u>Manual Utilization</u>: Manually initiated in FXU & sent request to RATAN - FXU would query RATAN API to get the remaining amount and other necessary info - FXU would send the util request to RATAN by Solace - RATAN would validate the util request from FXU and return ACK/NACK by Solace - <u>Auto Utilization</u>: Fully utilization required in RATAN on VD base on the below indicators - Trade level Auto Util indicator which is populated by Blade/Stella on the trade booking - Counterparty(Separate flag) and Vostro/Nostro(the settlement means is FXBRREC) - If <u>Un-utilization</u> till EOD on value date, RATAN should pass accounting entry to FXBRREC (equivalent to auto utilization). Can be at same time for Nepal / Egypt / Saudi.** **Proposed time is 1700 GMT TBC by Rajesh - Identification of Manual vs Auto Utilization - Proposal 1: Manual Utilization must be tagged as FXBRREC-M, Auto Utilization as FXBRREC in Settlement Means & Settlement Account - Proposal 2: Use separate flag (recommended) - <u>Pastdue Utilization</u>: FXU would support user to perform utilization post VD - When FXU query RATAN API if it past the VD, RATAN would response NACK - If FXU send pastdue utilization request, RATAN would response with reject - <u>Accounting model</u> for 'Util' cashflows - CR Bridge Account & DR FXBRREC Account: Utilization amount( Full)
- Blade would query the remaining amount information from RATAN
- Blade must have capability to select Settlement Method = UTIL
- STELLA must stamp the trade & cashflow as UTIL for both Blade booked as well as other upstream bookings
- Hard block required in Blade if there's utilization happen - RATAN would need to update status as "UTILIZED" or "PARTIALUTILIZED" to STELLA - Blade would trigger hard block above on above statuses - Trade market event would be **blocked for all profiles **if the cashflow is in UTILIZED or PARTIALUTIL status (i.e., even MO profile cannot perform the event)
- RATAN would have 3 main cashflow status help FMO identify the utilization status - UTILIZED**, **: Full amount is utilized and remaining amount is 0 - PARTIALLY-UTILIZED: Partial amount is utilized and remaining amount is not 0 **Not in MVP scope** - PASTDUE: No utilization happen until VD EOD - **Not in MVP scope**
- **Open Questions: ** - **Util Client Static- where would this sit - S2BX / BLADE / STELLA?**

![image-2025-6-18_14-22-44.png](attachments/image-2025-6-18_14-22-44.png)

#

# Phase 2 Requirement

1. Partial Utilization (Utilize partial amount of cashflow original amount) 1. When: as long as utilization amount is not full original cashflow amount, then it would be partial 2. Accounting model for 'Partial Util' cashflows - CR Bridge Account 40 & DR FXBRREC Account 40: Utilization amount(Partial) **- 1st Partial Util** - CR Bridge Account 60 & DR PastDue Account 60: remaining amount**- EOD pastdue ****Util** - Cashflow Status - **PARTIALLY-UTILIZED + PastDue** - CR PastDue 60 & DR Bridge Account 60: reverse the remaining amount **- reverse pastdue ****Util - No reverse request from FXU** - CR Bridge Account 20 & DR FXBRREC Account 20: Utilization amount(Partial) **- 2nd Partial Util - util request from FXU** - Cashflow Status -** PARTIALLY-UTILIZED + PastDue ** - CR Bridge Account 30 & DR FXBRREC Account 30: Utilization amount(Partial) **- 3rd Partial Util - util request from FXU** - CR Bridge Account 10 & DR PastDue Account 10: remaining amount**- EOD pastdue ****Util** - Cashflow Status -** PARTIALLY-UTILIZED + PastDue** 3. Only on contract level
2. PastDue Utilization (To cancel the previous Full or Partial Utilization event) 1. When: Configurable by different entity, no requirement by counterparty/currency. Timing to be confirmed by Rajesh. 2. Who: VD today or back value date cashflow. 3. Accounting model for 'Pastdue Util' cashflows - CR Bridge Account & DR PastDue Account: remaining amount( Full) **- on VD** - **Cashflow Status - PASTDUE + PastDue ** - DR Bridge Account & CR PastDue Account: Revere the remaining amount **- post VD Pastdue full/ Partial Util** - CR Bridge Account & DR FXBRREC Account: Utilization amount(Full) - **Cashflow Status - UTILIZED** 4. If cashflow has passed cutoff on VD, cashflow sub status should be always Pastdue, until it's full utilized (cashflow status = UTILIZED) 5. Only on contract level 6. Pastdue cashflow, a field aging should be showing the time length between current time and VD. 7. add Pastdue into sub status drop down 8. For cashflow status =Pastdue cashflow, if cashflow is cancelled, then reversed accounting entry will be generated. 9. enable remaining amount in cashflow API opened to DQSL/SSDR
3. Reverse Utilization 1. When: either partial/full to be reversed. 2. Accounting model for 'Reverse Util' cashflows - CR Bridge Account & DR FXBRREC Account: Utilization amount( Full or Partial) - DR Bridge Account & CR FXBRREC Account: Revere of utilization, remaining amount has to be added 3. Only on contract level
4. Early Utilization 1. Can support early utilization, same as full/partial/reverse utilization, while accounting will be sent on SOD VD 2. Early Utilization: FXU would support user to perform utilization early from VD-10 - FXU send the early utilization request to RATAN once user raised the request - RATAN will update remaining amount once receive the request - RATAN will generate accounting entry and send to EBBS on VD - For other countries: 1. Early util may happen beyond VD-10 2. Auto generate the SWAP from FXU → S2BX→ Ratan - to be further discussed
5. Timing to hit PASTDUE & Auto Utilization needs to be configurable by country, pastdue is the same time with auto utilization, but after auto utilization.

| Entity | Auto Util (GMT) | Auto Util (Local Timing) |
| --- | --- | --- |
| EG | 16:30 | 18:30 |
| SA | 16:30 | 19:30 |
| NP | 15:15 | 21:00 |

# Pending Priorities ADOs

| | Priority | Impacted Application | Requirement | Comment |
| --- | --- | --- | --- | --- |
| 1 | Must to Have | FXU | FXU should show the Auto Utilized trades in FXU GUI when Department query the trade in FXU. | MVP Leftover requirement |
| 2 | Must to Have | FXU, Ratan | Identify Client Leg for S2BX trade id. | MVP Leftover requirement |
| 3 | Must to Have | Ratan | **Push Util to Gross** - For hybrid customer (customer who can settle both as Gross/Util) in this case we should be able to settle as gross for util cashflows. Currently this is achieved by doing CnR in Razor and changing the settlement method. | ideally blade should amend settlement method on trade level? |
| 4 | Must to Have | Ratan | **Push Gross to Util** - Some client may be available for both gross and util, so if trade is booked as gross, but need to settle as Util ~~not for EG/NP/SA, ~~set FXBRREC-M as default settlement means | ideally blade should amend settlement method on trade level? |
| 5 | Must to Have | Ratan | Support **utilization window** beyond VD-10 for SA, VD-5 EG, directly materalize UTIL cashflow once received ** ** | @Chongxuan Li |
| 6 | Medium | Ratan, FXU | EOD report to FXU, which contains auto-utilization ~~and pastdue ~~trade info. | duplicate with No. 1 |
| 7 | Must to Have | Ratan, FXU | New API to provide utilization currency 2 and amount to FXU. | @Fengke Wu |
| 8 | Must to Have | Ratan, FXU | Utilization response API fields enrichment for FXU. Including utilization request and remaining amount | @Fengke Wu |
| 9 | | Ratan | Non-financial amendment, RATAN will not reject util request Validation for trade is amended, to be identified from 6 elements instead of trade major version. | |
| 10 | | Ratan | Consider cancellation fee/amendment fee in utilization trade, to be supported in FMRP. | |
| 11 | | Ratan | If post utilization, amendment happens, withdrawal and new need to be supported to process further utilization request. 1. 1. 1. Dependency on Rajesh to confirm no concern from FXU ops. | |
| 12 | Must to Have | FXU | FXU would validate any cashflow in ERROR status, FXU would block the util. (for scenario: If post utilization, amendment/ withdrawal happens) | |
| 13 | | Ratan | Static - Bulk uploader | |
| 14 | | Ratan | Static - Additional comments column to update source ref before approving | |
| 15 | | Ratan | Static - Differentiate the addition / deletion / amendment requests in colors under the verification queue | |
| 16 | | FXU | FXU-TLM Enrichment report, to check with Karthick/Gopi | |
| 17 | Must to Have | FXU | 1. Retry mechanize for util request with same util id? if timeout 2. Process late ACK/NACK message from Ratan post timeout. 3. Handle multi response from Ratan for the same util id, only process the ACK message no matter the sequence. | |
| 18 | Must to have | Ratan, FXU | IMS header to be added | |
| 19 | Medium | Ratan, FXU | Decimal tolerance handling in Ratan for ScPay -> FXU -> Ratan Maker ID will be ScPay, Checker ID will be empty. | identify SC Pay All full utilization? |
| 20 | | Ratan | Pastdue Dashboard for financial GRU team. | |
| 21 | | Ratan | Remaining amount API (In post trade portal, already done by a demo) in Blade. | |
| 22 | Medium | Ratan | Functionality to reverse of pastdue would be required in Ratan, as the action can be performed by FMO. Post reverse of pastdue, pastdue amount would be reversed and move to FXBRREC account. | |
| 23 | | FXU | Trade ID should be Blade trade id in utilization request | |

# User cases

| Scenarios | Cashflow level Changes | | | Accounting Entries |
| --- | --- | --- | --- | --- |
| Cashflow ID | Currency | Remaining Amount | Cashflow Status | Cashflow Sub Status | | EBBS Account | EBBS Unique Tran Ref | Currency | Cr/Dr | Transaction Amount | Value Date | Cashflow ID | Util Action | Source Pay Ref | Util Request ID |
| #1 Partial Util of 400K USD on Value Date | 101 | USD | 600,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 101.1 | USD | Dr | 400,000 | 19-Mar-2025 | 101 | Partial Utilization | SCPAY001 | 10001 |
| | Bridge Account | 101.1 | USD | Cr | 400,000 | 19-Mar-2025 | 101 | Partial Utilization | SCPAY001 | 10001 |
| 102 | SAR | 2,250,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 102.1 | ZAR | Cr | 1,500,000 | 19-Mar-2025 | 102 | Partial Utilization | SCPAY001 | 10001 |
| | Bridge Account | 102.1 | ZAR | Dr | 1,500,000 | 19-Mar-2025 | 102 | Partial Utilization | SCPAY001 | 10001 |
| #2 Partial Util of 200K USD on Value Date | 101 | USD | 400,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 101.2 | USD | Dr | 200,000 | 19-Mar-2025 | 101 | Partial Utilization | SCPAY002 | 10002 |
| | Bridge Account | 101.2 | USD | Cr | 200,000 | 19-Mar-2025 | 101 | Partial Utilization | SCPAY002 | 10002 |
| 102 | SAR | 1,500,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 102.2 | ZAR | Cr | 750,000 | 19-Mar-2025 | 102 | Partial Utilization | SCPAY002 | 10002 |
| | Bridge Account | 102.2 | ZAR | Dr | 750,000 | 19-Mar-2025 | 102 | Partial Utilization | SCPAY002 | 10002 |
| #3 Partial Util of 100 K USD #3 on Value Date | 101 | USD | 300,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 101.3 | USD | Dr | 100,000 | 19-Mar-2025 | 101 | Partial Utilization | SCPAY003 | 10003 |
| | Bridge Account | 101.3 | USD | Cr | 100,000 | 19-Mar-2025 | 101 | Partial Utilization | SCPAY003 | 10003 |
| 102 | SAR | 1,125,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 102.3 | ZAR | Cr | 375,000 | 19-Mar-2025 | 102 | Partial Utilization | SCPAY003 | 10003 |
| | Bridge Account | 102.3 | ZAR | Dr | 375,000 | 19-Mar-2025 | 102 | Partial Utilization | SCPAY003 | 10003 |
| #4 Util Reversal of 200K USD on Value Date | 101 | USD | 500,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 101.4 | USD | Cr | 200,000 | 19-Mar-2025 | 101 | Util Reversal Partial | SCPAY002 | 10002 |
| | Bridge Account | 101.4 | USD | Dr | 200,000 | 19-Mar-2025 | 101 | Util Reversal Partial | SCPAY002 | 10002 |
| 102 | SAR | 1,875,000 | PARTIALLY-UTILIZED | NA | | FXBR Account | 102.4 | ZAR | Dr | 750,000 | 19-Mar-2025 | 102 | Util Reversal Partial | SCPAY002 | 10002 |
| | Bridge Account | 102.4 | ZAR | Cr | 750,000 | 19-Mar-2025 | 102 | Util Reversal Partial | SCPAY002 | 10002 |
| #5 Past Due Settlement at EOD based on Remaining Amount at Cashflow | 101 | USD | 500,000 | PARTIALLY-UTILIZED | Pastdue | | Past Due Account | 101.5 | USD | Dr | 500,000 | 19-Mar-2025 | 101 | Past Due Settlement | | |
| | Bridge Account | 101.5 | USD | Cr | 500,000 | 19-Mar-2025 | 101 | Past Due Settlement | | |
| 102 | SAR | 1,875,000 | PARTIALLY-UTILIZED | Pastdue | | Past Due Account | 102.5 | ZAR | Cr | 1,875,000 | 19-Mar-2025 | 102 | Past Due Settlement | | |
| | Bridge Account | 102.5 | ZAR | Dr | 1,875,000 | 19-Mar-2025 | 102 | Past Due Settlement | | |
| #6 Partial Util of 100 K USD from Past Due post value date | 101 | USD | 400,000 | PARTIALLY-UTILIZED | Pastdue | | Past Due Account | 101.6 | USD | Cr | 500,000 | 20-Mar-2025 | 101 | Past Due Reversal | | |
| | Bridge Account | 101.6 | USD | Dr | 500,000 | 20-Mar-2025 | 101 | Past Due Reversal | | |
| | FXBR Account | 101.7 | USD | Dr | 100,000 | 20-Mar-2025 | 101 | Partial Utilization from Past Due | SCPAY004 | 10004 |
| | Bridge Account | 101.7 | USD | Cr | 100,000 | 20-Mar-2025 | 101 | Partial Utilization from Past Due | SCPAY004 | 10004 |
| 102 | SAR | 1,500,000 | PARTIALLY-UTILIZED | Pastdue | | Past Due Account | 102.6 | ZAR | Dr | 1,875,000 | 20-Mar-2025 | 102 | Past Due Reversal | | |
| | Bridge Account | 102.6 | ZAR | Cr | 1,875,000 | 20-Mar-2025 | 102 | Past Due Reversal | | |
| | FXBR Account | 102.7 | ZAR | Cr | 375,000 | 20-Mar-2025 | 102 | Partial Utilization from Past Due | SCPAY004 | 10004 |
| | Bridge Account | 102.7 | ZAR | Dr | 375,000 | 20-Mar-2025 | 102 | Partial Utilization from Past Due | SCPAY004 | 10004 |
| #7 Past Due Settlement at EOD based on Remaining Amount at Cashflow | 101 | USD | 400,000 | PARTIALLY-UTILIZED | Pastdue | | Past Due Account | 101.8 | USD | Dr | 400,000 | 20-Mar-2025 | 101 | Past Due Settlement | | |
| | Bridge Account | 101.8 | USD | Cr | 400,000 | 20-Mar-2025 | 101 | Past Due Settlement | | |
| 102 | SAR | 1,500,000 | PARTIALLY-UTILIZED | Pastdue | | Past Due Account | 102.8 | ZAR | Cr | 1,500,000 | 20-Mar-2025 | 102 | Past Due Settlement | | |
| | Bridge Account | 102.8 | ZAR | Dr | 1,500,000 | 20-Mar-2025 | 102 | Past Due Settlement | | |
| #8 Full Util of 400 K USD from Past Due post value date | 101 | USD | 400,000 | UTILIZED | NA | | Past Due Account | 101.6 | USD | Cr | 400,000 | 20-Mar-2025 | 101 | Past Due Reversal | | |
| | Bridge Account | 101.6 | USD | Dr | 400,000 | 20-Mar-2025 | 101 | Past Due Reversal | | |
| | FXBR Account | 101.7 | USD | Dr | 400,000 | 20-Mar-2025 | 101 | Partial Utilization from Past Due | SCPAY004 | 10005 |
| | Bridge Account | 101.7 | USD | Cr | 400,000 | 20-Mar-2025 | 101 | Partial Utilization from Past Due | SCPAY004 | 10005 |
| 102 | SAR | 1,500,000 | UTILIZED | NA | | Past Due Account | 102.6 | ZAR | Dr | 1,500,000 | 20-Mar-2025 | 102 | Past Due Reversal | | |
| | Bridge Account | 102.6 | ZAR | Cr | 1,500,000 | 20-Mar-2025 | 102 | Past Due Reversal | | |
| | FXBR Account | 102.7 | ZAR | Cr | 1,500,000 | 20-Mar-2025 | 102 | Partial Utilization from Past Due | SCPAY004 | 10005 |
| | Bridge Account | 102.7 | ZAR | Dr | 1,500,000 | 20-Mar-2025 | 102 | Partial Utilization from Past Due | SCPAY004 | 10005 |

# Tech Design

[FXU Tech Detail Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+Tech+Detail+Design)

# Static Data

| Entity | Branch Code | FMID | Sender's BIC (SCB Booking Entity BIC) | Field 53 BIC (Rule1) | Field 53 CCY to be Used | Field 58 BIC (Rule 2) |
| --- | --- | --- | --- | --- | --- | --- |
| Egypt | 34 | 401036553 | SCBLEGCAXXX | SCBLEGCAXXX | EGP | SCBLEGCAXXX |
| Nepal | 47 | 400007847 | SCBLNPKAXXX | SCBLNPKAXXX | NPR | SCBLNPKAXXX |
| Saudi | 16 | 400991880 | SCBLSAR2XXX | SCBLSAR2FMO | SAR | SCBLSAR2FMO |
| | | | | | | |

![](https://confluence.global.standardchartered.com/download/attachments/3244588508/image-2025-5-21_16-34-44.png?version=1&modificationDate=1747816484000&api=v2)