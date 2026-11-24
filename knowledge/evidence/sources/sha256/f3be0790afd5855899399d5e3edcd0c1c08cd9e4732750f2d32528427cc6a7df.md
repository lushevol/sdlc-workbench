# Murex 2.11 booking model

- 3 trades booked with same LtiID
- Strategy 'RECALC' / 'SWAP_AGENT' generate for these 3 trades & underlying payments
- Interim MTM & Coupon in SWAP_AGENT would be manually netting and SWIFT Suppressed in RATAN as it would be settled in clearing house

# Murex 2.11 RFR payments details

| System Date | Actions | Trade No. | Payment Desc | Payment Activities | Elibible for RATAN Settlement | Murex Status | STRATEGY | TYPOLOGY | FLOW_TYPE2 | X_DUMMY2 | TRN_REF | FLOW_ID | CURRENCY | CREDIT | AMOUNT | VALUE_DATE | LTI_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2-Feb-2024 | Trade Insertion | Trade1 | Initial Dummy Notional | Fully netted off by Murex | N | INV | RECALC | Vanilla X-ccy swap | INIT | 0 | 92104838 | 101972751 | JPY | C | 6,000,000,000.00 | 2024-02-08 | 5560580 |
| Trade1 | Initial Dummy Notional | N | INV | RECALC | Vanilla X-ccy swap | INIT | 0 | 92104838 | 101972750 | USD | D | 40,997,608.47 | 2024-02-08 | 5560580 |
| Trade3 | Initial Dummy Notional | N | INV | RECALC | RFR CCS MTM Fixing | INIT | 0 | 92104840 | 101972755 | JPY | D | 6,000,000,000.00 | 2024-02-08 | 5560580 |
| Trade3 | Initial Dummy Notional | N | INV | RECALC | RFR CCS MTM Fixing | INIT | 0 | 92104840 | 101972754 | USD | C | 40,997,608.47 | 2024-02-08 | 5560580 |
| Trade2 | Initial Notional | Bilateral settled on 2024-02-05 | Y | SNTR | RECALC | RFR CCS MTM Fixing | INIT | 0 | 92104839 | 101972753 | JPY | C | 6,000,000,000.00 | 2024-02-06 | 5560580 |
| Trade2 | Initial Notional | Y | SNTR | RECALC | RFR CCS MTM Fixing | INIT | 0 | 92104839 | 101972752 | USD | D | 40,997,608.47 | 2024-02-06 | 5560580 |
| |
| 4-Mar-2024 | PAY FIX WINDOW | Trade1 | Dummy MTM | Canclled on 2024-05-01 | N | INIT->CNCL | RECALC | Vanilla X-ccy swap | RTRN | 0 | 92104838 | 102817725 | USD | C | 74,101.33 | 2024-05-09 | 5560580 |
| Trade3 | Dummy MTM | N | INIT->CNCL | RECALC | RFR CCS MTM Fixing | RTRN | 0 | 92104840 | 102818905 | USD | D | 74,101.33 | 2024-05-09 | 5560580 |
| Trade2 | Dummy MTM | N | INIT->CNCL | RECALC | RFR CCS MTM Fixing | RTRN | 0 | 92104839 | 102818904 | USD | C | 74101.33 | 2024-05-07 | 5560580 |
| |
| 1-May-2024 | MTM Fixing | Trade1 | Fixed MTM | Fully netted off | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 0 | 92104838 | 104837040 | USD | C | 3,003,687.50 | 2024-05-09 | 5560580 |
| Trade3 | Fixed MTM | N | INV | RECALC | RFR CCS MTM Fixing | RTRN | 0 | 92104840 | 104837043 | USD | D | 3,003,687.50 | 2024-05-09 | 5560580 |
| Trade2 | Fixed MTM | Bilateral settled | Y | SNTR | RECALC | RFR CCS MTM Fixing | RTRN | 0 | 92104839 | 104837041 | USD | C | 3,003,687.50 | 2024-05-07 | 5560580 |
| |
| 7-May-2024 | JPY USD Rates Indexes Fixing | Trade1 | Interim Counpon | Bilaterl settled | Y | SNTR | RECALC | Vanilla X-ccy swap | VAR | 0 | 92104838 | 105059562 | JPY | C | 4,874,508.00 | 2024-05-09 | 5560580 |
| Trade1 | Reversal of fixed MTM | Netted to 105067680 | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 0 | 92104838 | 105061913 | USD | D | 3,003,687.50 | 2024-05-09 | 5560580 |
| Trade1 | Counpon + Initial MTM | N | INV | RECALC | Vanilla X-ccy swap | VAR | 0 | 92104838 | 105061914 | USD | C | 3,557,928.38 | 2024-05-09 | 5560580 |
| Trade1 | Netted Coupon(Incremental Amount) | Bilaterl settled | Y | SNTR | RECALC | Vanilla X-ccy swap | | 0 | 92104838 | 105067680 | USD | C | 554,240.88 | 2024-05-09 | 5560580 |
| |
| 10-Jun-2024 | PAY FIX WINDOW | Trade1 | Final Dummy Notional | Fully netted off | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 106106732 | JPY | D | 6,000,000,000.00 | 2024-08-08 | 5560580 |
| Trade1 | Final Dummy Notional | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 106106731 | USD | C | 37,993,920.97 | 2024-08-08 | 5560580 |
| Trade3 | Final Dummy Notional | N | INV | RECALC | RFR CCS MTM Fixing | RTRN | 1 | 92104840 | 106107558 | JPY | C | 6,000,000,000.00 | 2024-08-08 | 5560580 |
| Trade3 | Final Dummy Notional | N | INV | RECALC | RFR CCS MTM Fixing | RTRN | 1 | 92104840 | 106107557 | USD | D | 37,993,920.97 | 2024-08-08 | 5560580 |
| Trade2 | Final Notional | Bilateral settled | Y | SNTR | RECALC | RFR CCS MTM Fixing | RTRN | 1 | 92104839 | 106107556 | JPY | D | 6,000,000,000.00 | 2024-08-06 | 5560580 |
| Trade2 | Final Notional | Bilateral settled | Y | SNTR | RECALC | RFR CCS MTM Fixing | RTRN | 1 | 92104839 | 106107555 | USD | C | 37,993,920.97 | 2024-08-06 | 5560580 |
| |
| 6-Aug-2024 | JPY USD Rates Indexes Fixing | Trade1 | Final Dummy Notional(Reverse) | Netted to 108148051 | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147037 | JPY | C | 6,000,000,000.00 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon + Notional | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147039 | JPY | D | 5,995,858,478.00 | 2024-08-08 | 5560580 |
| Trade1 | Final Dummy Notional(Reverse) | Netted to 108148059 | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147036 | USD | D | 37,993,920.97 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon + Notional | N | INV | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147038 | USD | C | 38,509,086.31 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon | Bilateral settled(108148051) | Y | SNTR | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108148051 | JPY | C | 4,141,522.00 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon | Bilateral settled(108148059) | Y | SNTR | RECALC | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108148059 | USD | C | 515,165.34 | 2024-08-08 | 5560580 |

# SWAP_AGENT

| System Date | Actions | Trade No. | Payment Desc | Payment Type | Payment Activities | Elibible for RATAN Settlement | Murex Status | STRATEGY | TYPOLOGY | FLOW_TYPE2 | X_DUMMY2 | TRN_REF | FLOW_ID | CURRENCY | CREDIT | AMOUNT | VALUE_DATE | LTI_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2-Feb-2024 | Trade Insertion | Trade1 | Initial Dummy Notional | Not send to Ratan | Fully netted off by Murex | N | INV | SWAP_AGENT | Vanilla X-ccy swap | INIT | 0 | 92104838 | 101972751 | JPY | C | 6,000,000,000.00 | 2024-02-08 | 5560580 |
| Trade1 | Initial Dummy Notional | Not send to Ratan | N | INV | SWAP_AGENT | Vanilla X-ccy swap | INIT | 0 | 92104838 | 101972750 | USD | D | 40,997,608.47 | 2024-02-08 | 5560580 |
| Trade3 | Initial Dummy Notional | Not send to Ratan | N | INV | SWAP_AGENT | RFR CCS MTM Fixing | INIT | 0 | 92104840 | 101972755 | JPY | D | 6,000,000,000.00 | 2024-02-08 | 5560580 |
| Trade3 | Initial Dummy Notional | Not send to Ratan | N | INV | SWAP_AGENT | RFR CCS MTM Fixing | INIT | 0 | 92104840 | 101972754 | USD | C | 40,997,608.47 | 2024-02-08 | 5560580 |
| Trade2 | Initial Notional | Initial Notional | Bilateral settled on 2024-02-05 | Y | SNTR | SWAP_AGENT | RFR CCS MTM Fixing | INIT | 0 | 92104839 | 101972753 | JPY | C | 6,000,000,000.00 | 2024-02-06 | 5560580 |
| Trade2 | Initial Notional | Initial Notional | Y | SNTR | SWAP_AGENT | RFR CCS MTM Fixing | INIT | 0 | 92104839 | 101972752 | USD | D | 40,997,608.47 | 2024-02-06 | 5560580 |
| |
| 4-Mar-2024 | PAY FIX WINDOW | Trade1 | Dummy MTM | Not send to Ratan | Canclled on 2024-05-01 | N | INIT->CNCL | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 0 | 92104838 | 102817725 | USD | C | 74,101.33 | 2024-05-09 | 5560580 |
| Trade3 | Dummy MTM | Not send to Ratan | N | INIT->CNCL | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 0 | 92104840 | 102818905 | USD | D | 74,101.33 | 2024-05-09 | 5560580 |
| Trade2 | Dummy MTM | Not send to Ratan | N | INIT->CNCL | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 0 | 92104839 | 102818904 | USD | C | 74101.33 | 2024-05-07 | 5560580 |
| |
| 1-May-2024 | MTM Fixing | Trade1 | Fixed MTM | Not send to Ratan | Fully netted off | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 0 | 92104838 | 104837040 | USD | C | 3,003,687.50 | 2024-05-09 | 5560580 |
| Trade3 | Fixed MTM | Not send to Ratan | N | INV | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 0 | 92104840 | 104837043 | USD | D | 3,003,687.50 | 2024-05-09 | 5560580 |
| Trade2 | Fixed MTM | Interim MTM | Swift Suppression | Y | SNTR | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 0 | 92104839 | 104837041 | USD | C | 3,003,687.50 | 2024-05-07 | 5560580 |
| |
| 7-May-2024 | JPY USD Rates Indexes Fixing | Trade1 | Interim Counpon | Coupon | Swift Suppression | Y | SNTR | SWAP_AGENT | Vanilla X-ccy swap | VAR | 0 | 92104838 | 105059562 | JPY | C | 4,874,508.00 | 2024-05-09 | 5560580 |
| Trade1 | Reversal of fixed MTM | Not send to Ratan | Netted to 105067680 | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 0 | 92104838 | 105061913 | USD | D | 3,003,687.50 | 2024-05-09 | 5560580 |
| Trade1 | Counpon + Fixed MTM | Not send to Ratan | N | INV | SWAP_AGENT | Vanilla X-ccy swap | VAR | 0 | 92104838 | 105061914 | USD | C | 3,557,928.38 | 2024-05-09 | 5560580 |
| Trade1 | Netted Coupon(Incremental Amount) | Coupon | Swift Suppression | Y | SNTR | SWAP_AGENT | Vanilla X-ccy swap | | 0 | 92104838 | 105067680 | USD | C | 554,240.88 | 2024-05-09 | 5560580 |
| |
| 10-Jun-2024 | PAY FIX WINDOW | Trade1 | Final Dummy Notional | Not send to Ratan | Fully netted off | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 106106732 | JPY | D | 6,000,000,000.00 | 2024-08-08 | 5560580 |
| Trade1 | Final Dummy Notional | Not send to Ratan | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 106106731 | USD | C | 37,993,920.97 | 2024-08-08 | 5560580 |
| Trade3 | Final Dummy Notional | Not send to Ratan | N | INV | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 1 | 92104840 | 106107558 | JPY | C | 6,000,000,000.00 | 2024-08-08 | 5560580 |
| Trade3 | Final Dummy Notional | Not send to Ratan | N | INV | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 1 | 92104840 | 106107557 | USD | D | 37,993,920.97 | 2024-08-08 | 5560580 |
| Trade2 | Final Notional | Final Notional | Bilateral settled | Y | SNTR | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 1 | 92104839 | 106107556 | JPY | D | 6,000,000,000.00 | 2024-08-06 | 5560580 |
| Trade2 | Final Notional | Final Notional | Bilateral settled | Y | SNTR | SWAP_AGENT | RFR CCS MTM Fixing | RTRN | 1 | 92104839 | 106107555 | USD | C | 37,993,920.97 | 2024-08-06 | 5560580 |
| |
| 6-Aug-2024 | JPY USD Rates Indexes Fixing | Trade1 | Final Dummy Notional(Reverse) | Not send to Ratan | Netted to 108148051 | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147037 | JPY | C | 6,000,000,000.00 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon + Notional | Not send to Ratan | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147039 | JPY | D | 5,995,858,478.00 | 2024-08-08 | 5560580 |
| Trade1 | Final Dummy Notional(Reverse) | Not send to Ratan | Netted to 108148059 | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147036 | USD | D | 37,993,920.97 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon + Notional | Not send to Ratan | N | INV | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108147038 | USD | C | 38,509,086.31 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon | Coupon | Swift Suppression(108148051) | Y | SNTR | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108148051 | JPY | C | 4,141,522.00 | 2024-08-08 | 5560580 |
| Trade1 | Final counpon | Coupon | Swift Suppression(108148059) | Y | SNTR | SWAP_AGENT | Vanilla X-ccy swap | RTRN | 1 | 92104838 | 108148059 | USD | C | 515,165.34 | 2024-08-08 | 5560580 |

# Technical Design

According to below logic, define payment type correspondingly:

~~Initial mapping, which is not fully completed by the new findings in UAT on ~~2025-01-07~~ ~~

- ~~Initial Notional(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology=‘RFR CCS MTM Fixing’ && FLOW_TYPE2==’INIT’~~
- ~~Interim MTM(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology=‘RFR CCS MTM Fixing’ && FLOW_TYPE2!=’INIT’ && X_DUMMY2=='0'~~
- ~~Coupon(Trade 1): Strategy == ‘SWAP_AGENT’ && （Typology=’Vanilla X-ccy swap’ or Typology=’FWD_START_SWAP' or Typology=’’)~~
- ~~Final Notional(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology=‘RFR CCS MTM Fixing’ && X_DUMMY2==’1’~~

New mapping 2025-01-07 given there's new typology found in UAT booking, latest mapping as below.

- Initial Notional(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology=‘RFR CCS MTM Fixing’ && FLOW_TYPE2==’INIT’
- Interim MTM(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology=‘RFR CCS MTM Fixing’ && FLOW_TYPE2!=’INIT’ && X_DUMMY2==’0’
- Coupon(Trade 1): Strategy in (‘SWAP_AGENT,'RECALC') && Typology=’Vanilla X-ccy swap’
- Final Notional(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology=‘RFR CCS MTM Fixing’ && X_DUMMY2==’1’

Payment Type:

Logic Model: Cashflow.Payment_Type
Physical Model: /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentType

**NSTP**: Instrument_Common.Murex_Product_Strategy == "SWAP_AGENT"

**Netting**: Cashflow.Payment_Type in ("Interim MTM", "Coupon") AND Instrument_Common.Murex_Product_Strategy == "SWAP_AGENT" AND (Cashflow.Netting_Id == "" OR Cashflow.Netting_Id == null)

# Accounting Requirement

Clearing team request RATAN to feed the Strategy & payment types information to TLM for recon purpose, need to add the fields Instrument_Common.Murex_Product_Strategy & Cashflow.Payment_Type to payment accounting entry & feed to eBBS.

- Target eBBS Path: data/attributes/request/transaction entry/extended-narratives
- Target eBBS field: EXTENDEDNARRATIVE1
- Latest format of the eBBS field EXTENDEDNARRATIVE1 : Instrument_Common.Murex_Product_Strategy#Cashflow.Payment_Type#Cashflow.Netting_Id, 3 fields segregated by # and just put the value as blank( no space) if the field value is not available from cashflow.
- In case if the full length of Instrument_Common.Murex_Product_Strategy#Cashflow.Payment_Type#Cashflow.Netting_Id exceeding 65, then truncate from the trailing side to 65 characters.
- Sample values of different use cases: | **Remarks** | **extended-narration1** | | --- | --- | | Netting with Strategy | Swap_Agent#Bilateral netting#3297d3a6-b122-11ef-ac77-005056ac4ab7 | | Net without Strategy | #Bilateral Netting#3297d3a6-b122-11ef-ac77-005056ac4ab7 | | Gross Payment with Strategy & Payment type | Swap_Agent#Interim MTM# | | Gross Payment with Strategy without Payment type | Swap_Agent## | | Gross Payment without Strategy with Payment type | #CouponFloat# | | Gross Payment without Strategy & Payment type | ## |

# <Flows></Flows> is blank + VAL_STATUS update

There're special cases the <Flows></Flows> is blank for special scenarios, <Flows></Flows> is mandatory for RATAN and we need special control on this case. 
Details of this criterial is as below:

- It’s from the RFR & Swap Agent auto netting between trade 1 & trade 3 only, the netted amount is the coupon amount from trade 1
- This case is only applicable when there’s MTM re-fixing happen, the monthly MTM re-fixing is below 10
- The indicator to identify this case is 1. Strategy in(( RECALC, SWAP_AGENT), field path is as below 1. Strategy path in MxML: **/MxPayML/strategy** 2. Strategy header in Batch file: **STRATEGY** 2. Trade REF==0 1. Trade REF path in MxML: **/MxPayML/transactionID** 2. Trade REF header in batch file: **TRN_REF** 3. Typology == ‘’ 1. Typology path in MxML: **/MxPayML/transactionTypology** 2. Typology header in batch file:** TYPOLOGY**

Special control: Add new pre process to enrich the trade id & flows & VAL_STATUS → VALD

- **MxML Real time feeding**: 1. The <Flows><Flows> would be blank | Filed Name | MxML Path | Murex Original Value | RATAN Enriched Value | | --- | --- | --- | --- | | Payment ID | /MxPayML/flowID | 112517395 | 112517395 | | Original Transaction Id | /MxPayML/scbExtraInfoBlock/TrnOrginalID | 0 | | | Parent transaction Id | /MxPayML/scbExtraInfoBlock/TrnParentID | 0 | | | Trade id of payment generated | /MxPayML/transactionOriginID | 0 | | | Latest Trade Id | /MxPayML/transactionID | 0 | | | Flows | /MxPayML/scbExtraInfoBlock/Flows | | <flow>Flowid:112517395, status:SNTR, value_date:20241211</flow> | 2. RATAN to enrich the blank fields as below: The trade id 0 would be replaced by the dummy trade id R112517395. **Note: RATAN enriched trade ids would be 'R'+Murex flow id, adding the prefix 'R' to avoid any conflict with the normal Murex trade id.** | Filed Name | MxML Path | Murex Original Value | RATAN Enriched Value | | --- | --- | --- | --- | | Payment ID | /MxPayML/flowID | 112517395 | 112517395 | | Original Transaction Id | /MxPayML/scbExtraInfoBlock/TrnOrginalID | 0 | MTR112517395 | | Parent transaction Id | /MxPayML/scbExtraInfoBlock/TrnParentID | 0 | 0 | | Trade id of payment generated | /MxPayML/transactionOriginID | 0 | 0 | | Latest Trade Id | /MxPayML/transactionID | 0 | 0 | | Flows | /MxPayML/scbExtraInfoBlock/Flows | | <flow>Flowid:112517395, status:SNTR, value_date:20241211</flow> |
- **Batch Feeding - Enrich the Batch base file**: To enrich the trade id 1. The original file received from Murex 2.11 | Field Name | Murex Original Value | RATAN Enriched Value | | --- | --- | --- | | FLOW_ID | 112517395 | 112517395 | | TRN_ORGID | 0 | | | CREATOR | 0 | | | TRN_ID | 0 | | | TRN_REF | 0 | | 2. Copy the flow id to the trade id fields: The trade id 0 would be replaced by the dummy trade id R112517395. **Note: RATAN enriched trade ids would be 'R'+Murex flow id, adding the prefix 'R' to avoid any conflict with the normal Murex trade id.** | Field Name | Murex Original Value | RATAN Enriched Value | | --- | --- | --- | | FLOW_ID | 112517395 | 112517395 | | TRN_ORGID | 0 | MTR112517395 | | CREATOR | 0 | 0 | | TRN_ID | 0 | 0 | | TRN_REF | 0 | 0 |
- **Batch Feeding - Enrich the snapshot file**: Insert one new role to the snapshot file **Note: RATAN enriched trade ids would be 'R'+Murex flow id, adding the prefix 'R' to avoid any conflict with the normal Murex trade id.** | TRN_REF | FLOW_ID | STATUS | VALUE_DATE | | --- | --- | --- | --- | | R112517395 | 112517395 | SNTR | 20241211 |
- **Dummy trade id removal: **The above dummy trade id R112517395 is not mean to send to downstream of RATAN( LMS, eBBS, FMSWG), there're 2 options discussed with below pros & cons | **Options** | **Pros** | **Cons** | | --- | --- | --- | | Remove the dummy trade id in the first workflow task | Data clean up at single point | Potential risk on the lock control with trade id | | Keep the dummy id in all RATAN service, remove the trade id dynamically in LMS/Accountingg service | No need to consider the lock control with trade id | Need to implement the customized logic in different services(LMS, Accounting) |

Business cases:

- MTM Re-Fixing
- Multi MTM Re-Fixing