##

## 1. Background

Today settlement ops perform cross-product netting across multi desks in Murex G2000. As part of Murex G2000 decommission, RATAN will be the place to perform CPN in the target state.  This is phased program so our design need to support cross product netting when specific desks are migrated to strategic system by phase within the same entity. i.e. For China entity, cash flow for Rates desk generated from strategic system when remaining desks are in Murex G2000.

## 2. Murex2.11 Cashflow Integration Strategy

### 2.1 High Level Flow

### 2.2 Ops Requirement & Practice

- 1. Murex will provide a monitor screen to settlement user to monitor cashflow sent to RATAN. 2. Cashflow marked as RATAN eligible will send to RATAN for swift & settlement accounting, murex won't generate swift to FMSRE nor settlement accounting. 3. In the case ops perform trade market operation impacting cashflow which has sent to RATAN, murex won't modify existing cashflow, but send Reversal and NEW to RATAN. *(Refer to section '<u>4 Murex trade event impacting cashflow</u>')* 4. Murex will setup hard block for **RLSR, **to restrict amendments on **RLSR **cashflows for front office staff. Amendments on trades can only be performed by Middle Office. 5. Upon cashflow insertion, VD-7 cashflow will send to Ratan in **Real-time** basis. Cashflow out of VD-7 will be kept in murex until it’s value date fall in VD-7. 6. Murex to exclude RATAN eligible cashflow from existing payment STP procedure. 7. Murex to disable/exclude from existing China BAU payment queue. If the queue is used exclusively for RATAN eligible cashflow, need to disable. If the queue is NOT RATAN eligible exclusive, or it shared with other entity, then need to add exclusion logic in payment queue. 8. For OBU TAIPEI, as the FMID is same with TAIPEI in Murex. To keep it consistency with FMRP, cashflow with entity name OBU TAIPEI that FMID will be updated from 10038345 to 300011345.

2.3 Accounting & TLM recon

Trade accounting

- 1. Still generate from murex to aspire.

Settlement accounting

- 1. Precious metal cashflow will retain in murex and follow as-is BAU process, no impact on existing accounting and TLM recon. (For China there is no settled precious metal cashflow, all suppressed) 2. Non precious metal cashflow will send to RATAN for NET/GROSS, swift & settlement accounting will be handled within RATAN and Razor. The accounting model to be driven as part Razor accounting design for FMRP. Murex to be involved only if change is required for Accounting &TLM recon (for example new/modify report to Aspire/ebbs/TLM).

### 2.4 Downstream Impact

For RATAN eligible cashflow, murex should

- 1. Suppress cashflow message to LMS, as RATAN will do so. 2. Suppress cashflow message to FMSRE, as RATAN &Razor will do so. 3. Don't generate settlement accounting via Aspire &EBBS, as target in Razor.

### 2.5 Impacted Report List

list of murex reports monitoring end status of payment, will be impacted because we created new end status (SNTR/RLSR) which to be enriched post cashflow integration.

Down steam report:

- - | Owner | Report Name | Logic | Remarks and Questions | | --- | --- | --- | --- | | System Report | | | EBBS | CNYYYYMMDD0001Req.TXT | (STATUS="SENT".OR.STATUS="PEND") | [EBBS report will be generated from Razor? @Dinesh, Arockia - YES](mailto:K.A.Dinesh@sc.com) | | ASPIRE | MXG_PAYMENTTRANSACTION.csv | M_PF_STATUS IN ('SENT','PEND') | [PAYMENT BCDF will be generated from Razor? @Dinesh, Arockia - YES](mailto:K.A.Dinesh@sc.com) | | OR M_PF_STATUS = 'RLSD' | | TLM | MUREX_TLM_NOS_GB_NEW_YYYYMMDD.dat | TAB_SCB_NOS.REP -> (M_STATUS IN ('RLSD', 'SENT','PEND') DM_SCB_MLS_REP SCB_NOSHIS_DBF | [Will this TLM_NOS_GB_NEW report be replaced by Ratan or Razor according to TLM design? @Ramasamy, Karthick – Is this applicable for China entities or only London ? This should continue for Precious Metal from Murex 2.11 RATAN EOD will be for FMRP enrichment ](mailto:Karthick.Ramasamy@sc.com) | | User Report | | | CRRS | SD_INT.csv | M_CNTRP<>'SGE/SHA' and portfolio under CHINA_ALL_ON') Payment Information | [Does those end user report going to be migrated out and use TDS data instead? @Mishra, Nrusingha](mailto:Nrusingha.Mishra@sc.com) | | | - SD_INT.csv and SD_XB.csv is already in our inventory. | | CCRS | SD_XB.csv | and M_ENTITY='SHANGHAI' | - EXT_PAY_ACT_OP.csv, derivatives_settlements.csv, EXT_PAY_FW_TAB.csv, they are even not in RR. Can you help check from Murex 2.11 who is the interface or user need it? | | and M_STATUS<>'CNCL' | | | PAYMENT information | <<Mishra>> : RATAN EOD will generate the feeds to CRRS (SD_INT and SD_XB) after retrieving payment info from RATAN ONE (for non-PM) and MUREX (for PM) | | User Report | EXT_PAY_ACT_OP.csv | M_O_CPU_DATE <= convert(datetime, convert(char(8), dateadd(day, -6, getdate()), 112)) | <<Amy>>: FMMIS Report generated in RATAN ONE | | | | | payment Operation | | | User Report | derivatives_settlements.csv | M_GROUP= 'GBL_DO_SET' and M_VALUE_DATE>=7 | <<Amy>> :Checked with RATAN RR DPS, this weekly report no user download record. | | | | | Payment Operation | | | User Report | EXT_PAY_FW_TAB.csv | PAY_FLOW_DBF | <<Amy>>: FMMIS Report generated in RATAN ONE | | | | | CN payment will be shows in the NSTP monitor payment | |

## 3. RATAN Eligibility Check

Cashflow is marked as RATAN Eligible based on below criteria. Murex only send RATAN eligible cashflow to RATAN

| # | Criteria | Murex Filter Logic | Comment |
| --- | --- | --- | --- |
| 1 | China entity | entity in the list of fmrp enabled entities | |
| 2 | Cashflow in initial status | Payment.status = 'INIT' | |
| 3 | ~~Trade is validated~~ | ~~Trade.valid_status in (VALD,COMP)~~ | sync with trade insertion |
| 4 | Value Date condition | Bringing cashflows as early immediately after its generation in Murex 2.11 into RATAN will create additional overhead when there are changes due to trade amendments/cancellation & others Agreed with PO will take VD-7 cashflow flow to Ratan | Tracking Jira [RATAN-10820](https://jira.global.standardchartered.com/browse/RATAN-10820) Email agree with PO: *<u></u>**<u> </u>* |
| 5 | Exclude precious metal deal cashflow | We have got generic approach for all entities and all product. If murex trade meet the conditions 1. Entity in scope 2. trade CCY, underlying CCY, Instrument first 3 character is Bullion CCY Then trade is treated as ‘precious metal deal’, and all cashflow under this trade should continue settled from Mx2.11. Otherwise will send to Ratan. | Tracking Jira [R](https://jira.global.standardchartered.com/browse/RATAN-10820)ATAN-11017 Email agree with PO: ** |
| 6 | Exclude Non deliverable CCY | Agreed with PO to exclude Non deliverable CCY for NDS Trades. | [Tracking Jira:RATAN-13997](https://jira.global.standardchartered.com/browse/RATAN-13997) |
| 7 | Exclude zero payment | Payment.Amount = 0 | |
| 8 | FXD | Exclude the trade flow to Razor FXD logic is updated for H1 go live in Jul-2024 | |

**EXPAND: FXD Behavior**

Part of FXD Trades settle in Razor, below is the behavior:

| Settle System | Criteria | Murex Logic |
| --- | --- | --- |
| MX | typology in ('NDF','NDS Fixing','ND CDS Fixing','Phy_Precious','PayModeSett','Emissions FX','COM INDEX') | PAY.M_TYPOLOGY IN('NDF','NDS Fixing','ND CDS Fixing','Phy_Precious','PayModeSett','Emissions FX','COM INDEX') |
| MX | Early Terminate Fee | (PAY.M_FLOW_TYPE0='CAP' and (PAY.M_FLOW_TYPE1='XIT' or PAY.M_ACTION='XIT') and (PAY.M_MOP_ID<>0)) |
| MX | PayModeSett SMP generated FXD | PAY.M_TRN_ID in (select M_NB from TRN_HDR_DBF where M_TRN_GTYPE = 77 and M_CREATOR <> 0 and M_CREATOR in ( select M_NB from TRN_HDR_DBF where M_TRN_GTYPE = 84 and M_TRN_TYPO = 'PayModeSett')) |
| MX | typology in FX_PCD,FX_DCD,DCD & (external counterparty || counterparty country is JERSEY) | (PAY.M_STRATEGY in ('FX_PCD','FX_DCD','DCD') AND (CPTN.M_STATUS=0 AND (CP.M_CLASSIFY='EXTERNAL' OR CPTN.M_COUNTRY='JERSEY') )) |
| MX | Non PVB Bullion CCY Payment | PAY.M_CNTRP not in (select M_LABEL from MUREXDB.TABLE#DATA#COUNTERP_DBF where M_PB_CUST='Y' ) and (exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF CCY2 where (TRN.M_BRW_NOMU1=CCY2.M_LABEL or TRN.M_BRW_NOMU2=CCY2.M_LABEL or TRN.M_BRW_ODNC0=CCY2.M_LABEL or TRN.M_BRW_ODNC1=CCY2.M_LABEL) and CCY2.M_BUL_CUR_FL='Y') or exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF CCY3 where (substring(TRN.M_INSTRUMENT,1,3))= CCY3.M_LABEL and CCY3.M_BUL_CUR_FL='Y')) |
| MX | COM Payment | PAY_COMMODITY_VIEW |
| MX | SG MY Wealth Management Payment | PAY.M_PORTFOLIO in (select T1.M_REF from MUREXDB.TRN_PFLD_DBF T1 where M_LABEL in ('CMWM_COMBTB_SAC','CMWM_COMBTB_SDB','CB_COMMOSCB_ACU','CB_COMMOSCB_DBU','WM_MY_COMM')) |

**EXPAND_END**

## 4. Murex trade event impacting cashflow

Refer to: [CN Settlement - Analyse murex event impacting payment to Ratan - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Analyse+murex+event+impacting+payment+to+Ratan)

**EXPAND: Deprecated Analysis**

**EXPAND: New**

### New

> **INFO**
> Murex cashflow creation setup - Murex Cashflows are created upon deal insertion, if VD is below or equal to the limit date which is the last day of the current month plus 2 months. for eg. today is 22-Jul, then only flows whose VD <= 30-Sep will be generated.

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| when trade is booked | MC01 | INIT | ![image2022-8-10_16-54-20.png](attachments/image2022-8-10_16-54-20.png) |
| murex auto move status INIT → SNTR murex send SNTR flow to CashPlatform | MC01 | SNTR | ![image2022-8-10_16-58-29.png](attachments/image2022-8-10_16-58-29.png) |
| once CashPlatform Release from Ratan, murex auto move status SNTR → RLSR | MC01 | RLSR | |

**EXPAND_END**

**EXPAND: Amendment**

### Amendment

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| Flow been ack-ed/released from CashPlatform | MC01 | SNTR/RLSR | |
| Perform Cancel & Reissue in murex | MC01 - Original MC02 - Reversal of MC01 MC03 - New flow of Amendment | MC01 - SNTR/RLSR **MC02 - INIT** **MC03 - INIT** | ![image2022-8-10_17-5-17.png](attachments/image2022-8-10_17-5-17.png) |
| murex auto move status INIT → SNTR murex send SNTR flow to CashPlatform | MC01 - Original MC02 - Reversal of MC01 MC03 - New flow of Amendment | MC01 - SNTR/RLSR **MC02 - SNTR** **MC03 - SNTR** | ![image2022-8-10_17-9-39.png](attachments/image2022-8-10_17-9-39.png) |
| once CashPlatform released, murex auto move status SNTR → RLSR | MC01 - Original MC02 - Reversal of MC01 MC03 - New flow of Amendment | MC01 - SNTR/RLSR **MC02 - RLSR** **MC03 - RLSR** | |

**EXPAND_END**

**EXPAND: Cancellation**

### Cancellation

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| Flow been ack-ed from CashPlatform | MC01 - Original MC02 - Reversal of MC01 MC03 - New flow of Amendment | MC01 - RLSR MC02 - RLSR MC03 - RLSR | |
| Perform Cancellation in murex | MC01 - Original MC02 - Reversal of MC01 MC03 - New flow of Amendment MC04 - Reversal of MC03 | MC01 - RLSR MC02 - RLSR MC03 - RLSR **MC04 - INIT** | ![image2022-8-10_17-11-57.png](attachments/image2022-8-10_17-11-57.png) |
| murex auto move status INIT → SNTR murex send SNTR flow to CashPlatform | MC01 - Original MC02 - Reversal of MC01 MC03 - New flow of Amendment MC04 - Reversal of MC03 | MC01 - RLSR MC02 - RLSR MC03 - RLSR **MC04 - SNTR** | ![image2022-8-10_17-14-37.png](attachments/image2022-8-10_17-14-37.png) |
| once CashPlatform released, murex auto move status SNTR → RLSR | MC01 - Original MC02 - Reversal of MC01 MC03 - New flow of Amendment | MC01 - RLSR MC02 - RLSR MC03 - RLSR **MC04 - RLSR** | |

**EXPAND_END**

**EXPAND: Exercise (Option Deal)**

### Exercise (Option Deal)-Delivery

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| book a option deal with settlement mode is 'Delivery', make sure it is Exercise eligible murex auto move status INIT → SNTR murex send SNTR flow to Cash Platform | MC01 - Original (Premium) | SNTR | ![image2023-2-10_16-17-42.png](attachments/image2023-2-10_16-17-42.png) |
| On value date Perform Exercise on option deal which generate a FX trade. the FX trade initiate 2 cashflow on each currency MC02 and MC03 murex auto move MC02 MC03 status INIT->SNTR murex send SNTR flow to Cash Platform | MC01 - Original (Premium) MC02 - New FX CNO MC03 - New FX USD | MC01 - SNTR MC02 - SNTR MC03 - SNTR | ![image2023-2-10_16-18-27.png](attachments/image2023-2-10_16-18-27.png) |
| once Cash Platform Release from Ratan, murex auto move status SNTR → RLSR | MC01 - Original (Premium) MC02 - New FX CNO MC03 - New FX USD | MC01 - RLSR MC02 - RLSR MC03 - RLSR | |

### Exercise (Option Deal)-Cash

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| book a option deal with settlement mode is 'Cash', make sure it is Exercise eligible murex auto move status INIT → SNTR murex send SNTR flow to Cash Platform | MC01 - Original (Premium) | SNTR | ![image2023-2-10_11-53-32.png](attachments/image2023-2-10_11-53-32.png) |
| On value date Perform Exercise in murex which will generate XIT type cashflow | MC01 - Original (Premium) MC02 - New cashflow type of XIT | MC01 - SNTR MC02 - SNTR | ![image2023-2-10_11-54-0.png](attachments/image2023-2-10_11-54-0.png) |
| once Cash Platform Release from RATAN, murex auto move status SNTR → RLSR | MC01 - Original (Premium) MC02 - New cashflow type of XIT | MC01 - RLSR MC02 - RLSR | |

**EXPAND_END**

**EXPAND: Fixing**

### Fixing

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| book a new trade murex auto move status INIT → SNTR murex send SNTR flow to CashPlatform | MC01 - Original MC02 - Original MC03 - Original | SNTR | ![image2023-2-10_15-25-37.png](attachments/image2023-2-10_15-25-37.png) |
| Proceed fixing in Murex which generate Reverse and New payments | MC01 - Original MC02 - Reverse MC03 - New | SNTR | ![image2023-2-10_15-31-6.png](attachments/image2023-2-10_15-31-6.png) |
| once CashPlatform Release from Ratan, murex auto move status SNTR → RLSR | MC01 - Original MC02 - Reverse MC03 - New | RLSR | |

**EXPAND_END**

**EXPAND: Expire**

### Expire

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| book any type of new trade murex auto move status INIT → SNTR murex send SNTR flow to RATAN | MC01 - CNO MC02 - USD | MC01 - SNTR MC02 - SNTR | ![image2023-2-10_15-33-57.png](attachments/image2023-2-10_15-33-57.png) |
| Cashflow got released from RATAN, murex auto move status SNTR → RLSR | MC01 - CNO MC02 - USD | MC01 - RLSR MC02 - RLSR | |
| Trade by end of EOD maturity date got Expired in Murex (no Reverse and no New payments generated as expected) | MC01 - CNO MC02 - USD | MC01 - RLSR MC02 - RLSR | |

**EXPAND_END**

**EXPAND: Early termination**

### Early termination

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| book a new trade murex auto move status INIT → SNTR murex send SNTR flow to CashPlatform | MC01 - CNO MC02 - USD | SNTR | ![image2023-2-10_15-40-6.png](attachments/image2023-2-10_15-40-6.png) |
| Proceed Early termination in Murex which generate Reverse flow and Early Termination Fee murex auto move status INIT → SNTR and send to Ratan | MC01 - Original CNO MC02 - Original USD MC01 - Reversal CNO MC02 - Reversal USD MC05 - Early Termination Fee | SNTR | ![image2023-2-10_15-43-43.png](attachments/image2023-2-10_15-43-43.png) |
| once cashflow Release from Ratan, murex auto move status SNTR → RLSR | MC01 - Original MC02 - Reverse MC03 - New | RLSR | |

**EXPAND_END**

**EXPAND: Restructure**

### Restructure

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| book a new IRS trade murex auto move status INIT → SNTR murex send SNTR flow to CashPlatform | MC01 - Original MC02 - Original MC03 - Original | SNTR | ![image2023-2-17_16-0-18.png](attachments/image2023-2-17_16-0-18.png) |
| Proceed fixing in Murex which generate Reverse and New payments | MC01-MC03 - Original MC04-MC06 - Reversal MC07-MC09 - New | SNTR | ![image2023-2-17_16-14-39.png](attachments/image2023-2-17_16-14-39.png) |
| Push New payment SNTR-->RLSR | MC01-MC03 - Original MC04-MC06 - Reversal MC07-MC09 - New | MC01-MC06 -SNTR MC07-MC09 - RLSR | ![image2023-2-17_17-5-40.png](attachments/image2023-2-17_17-5-40.png) |
| Restructure is done by killing the original trade and creating a new trade. The new trade will have same cash flows for past and new calculated cash flows for future. | MC01-MC03 - Original MC04-MC06 - Reversal MC07-MC09 - New MC10-Reversal MC11-New | MC01-MC06 -SNTR MC07-MC09 - RLSR MC10-MC11 - SNTR | ![image2023-2-17_17-13-12.png](attachments/image2023-2-17_17-13-12.png) |
| once cashflow Release from Ratan, murex auto move status SNTR → RLSR | MC01-MC03 - Original MC04-MC06 - Reversal MC07-MC09 - New MC10-Reversal MC11-New | RLSR | |

### Restructure(future cashflow)

| Trigger Point | Cashflow ID | Status in Murex | Example Screenshot |
| --- | --- | --- | --- |
| book a new IRS trade murex auto move status INIT → SNTR murex send SNTR flow to CashPlatform | MC01 - Original MC02 - Original MC03 - Original | MC01 - SNTR MC02 - SNTR MC03 - INIT | ![image2023-2-24_16-59-49.png](attachments/image2023-2-24_16-59-49.png) |
| Proceed fixing in Murex which generate Reverse and New payments | MC01-MC02 - Original MC03-CNCL MC04 -MC07 Reversal MC08- INIT | | ![image2023-2-24_17-4-26.png](attachments/image2023-2-24_17-4-26.png) |
| Push New payment SNTR-->RLSR | MC01-MC03 - Original MC04-MC06 - Reversal MC07-MC09 - New | MC01-MC06 -SNTR MC07-MC09 - RLSR | |
| Restructure is done by killing the original trade and creating a new trade. The new trade will have same cash flows for past and new calculated cash flows for future. | MC01-MC03 - Original MC04-MC06 - Reversal MC07-MC09 - New MC10-Reversal MC11-New | MC01-MC06 -SNTR MC07-MC09 - RLSR MC10-MC11 - SNTR | |
| once cashflow Release from Ratan, murex auto move status SNTR → RLSR | MC01-MC03 - Original MC04-MC06 - Reversal MC07-MC09 - New MC10-Reversal MC11-New | RLSR | |

**EXPAND_END**

**EXPAND_END**

5. Interface Message Recon with RATAN

#### Realtime Recon

- For every cashflow murex send to RATAN, RATAN will response ACK to indicate message is received.
- Once murex receive ACK from RATAN, need to sync back ack status on murex cashflow - Ratan id, ACK timestamp, UDF as 'Ratan acknowledged'.
- In case cashflow send to RATAN but timeout to receive ACK from RATAN, need throw technical exception to stakeholder for handling.

#### Report Recon

- Murex need to provide with a screen/report to user whenever user want to view all cashflow to RATAN with cashflow status, outbound status, ACK status.

## 6. Cashflow Migration Activity

**Assume **Murex 2.11 Cashflow Migration (to Ratan) ahead of Trade Migration (to Stella)

### 6.1  CPT Murex Engagement

**CPT Period: **4-Sep~ 8-Sep (Mon - Fri)

| Date | Day | Activity | System | Runbook |
| --- | --- | --- | --- | --- |
| 2-Sep | Saturday | release for CPT | Mx2.11 | Release murex change, keep interface to Ratan enabled, make sure cashflow to Ratan only for those CPT eligible cashflow. Criteria for CPT eligibility: - - **one dollar trades booked for CPT, VD 4~8-Sep** (test case to be defined by ratan) - this is mainly to test payment swift generation. we expect accounting break for those 1 dollar trade as murex will send trade accounting but aspire is not ready for settlement accounting. aspire release on biz go live day only. - **production cashflow VD on 11,12-Sep** - this is mainly to test Ratan functionalities. murex to keep interface opened during whole CPT period in case mktops happen on those VD 11,12 Sep trades. |
| 4-Sep~ 8-Sep | Mon~ Fri | CPT | Mx2.11 Ratan Razor FMSRE EBBS TLM | user will book one dollar trade and cancel right after. |
| 10-Sep | Sunday | release for biz go live | Mx2.11 | Go decision - murex release for biz go live No go decision - rollback those VD 11,12-Sep cashflow from Ratan to murex (tbc if user or via script) |

**Process for scenarios**

| | **Scenario** | **Actual Murex to Ratan Date** | **Cashflow Value Date** | **Cashflow CutOff Date** | **Actions with Rollback plan** |
| --- | --- | --- | --- | --- | --- |
| 1 | cut off date equal to VD (normal case) | 2-Sep (Saturday) | 11-Sep & 12-Sep | 11-Sep & 12-Sep | If Go decision made by **3-Sep** (weekend): cashflow will release in ratan on **4,5-Sep**. settlement & accounting follow FMRP strategic flow. If No-go decision made by **3-Sep**: execute rollback plan by **3-Sep**, that cancel/suppress cashflow on Ratan GUI which will auto bring murex status back (from SNTR to INIT) by **3-Sep**. Those cashflow to be settled from murex on **4,5-Sep**. |
| 2 | cut off date in prior to VD | 2-Sep (Saturday) | 11-Sep & 12-Sep | **8-Sep (Friday)** | Dinesh confirmed with ops that ops is ok to release/settle this trade on early Mon (11-Sep) for by eod Sunday (10-Sep) which is post go decision made. so no rollback plan required. |

### 6.2  Scenarios with Actions

| **Timeline** | **#** | **Scenarios** | **Actions / Behaviors** |
| --- | --- | --- | --- |
| Before cashflow migration | 1 | cashflow has been settled/netted/cancelled/suppressed. (ie.status in SENT/NET/INV/CNCL/SUPP) | no action. |
| 2 | Non-STP: cashflow other than settled/netted/cancelled, and VD < T | ask ops to handle it within Murex, by EOD Friday. |
| 3 | Non-STP: cashflow other than settled/netted/cancelled, and VD >= T | ask ops to keep it in INIT (if not, ask ops to revert back to INIT) and refrain from handling it in murex. Those cashflow should be sent to RATAN on T, and ops should handle it in RATAN post go live. <Open point: if amended VD which cause reversal VD in past and new VD in future, will has duplicate pay risk if new handle in ratan in prior to reverse one. > - Ratan to identify it out and provide warning to ops to avoid duplicate pay. |
| 4 | STP: VD within 7 days cashflow fulfil murex payment STP rule | murex team to stop payment STP for China **one week ahead of migration** (static UDT update by RDM). This is to ensure VD>T cashflow to be settled in Ratan instead of by murex STP. Impacted weekly volume on average: CN: 26 (less impact but need to communicate FMO) UK:1422 - further discuss when uk go live |
| ![image2023-4-26_19-38-51.png](attachments/image2023-4-26_19-38-51.png)Cashflow migration go-live | | In murex only remain VD>=T cashflow which to be settled in Ratan | Murex release change, manual trigger control m job once on weekend, to flow remaining cashflow to ratan. then do recon. |
| Post cashflow migration day & Before trade migration day | 5 | New payment is generated by monthly PAYFIX script for VD in future 2 months | murex will send cashflow to Ratan once cashflow is produced and VD within 7 days. ratan will handle settlement. |
| 6 | New payment is generated once fixing done. | murex will send cashflow to Ratan once cashflow is fixed and VD within 7 days. ratan will handle settlement. |
| * | 6a * | *[Specific Scenario] fixed leg & floating leg cashflow process & settlement.* | Ratan to design process based on today murex behaviors as below 1. Both fixed leg and floating leg available to generate cashflow on same day - murex generate one payment with netted amount of fixed leg and floating leg. 2. Fixed leg available to generate cashflow in prior to floating leg - murex generate payment for fixed leg firstly. then generate payment with netted amount of fixed leg and floating leg once floating leg is available, meanwhile cancel/reverse original fixed leg payment (depends on cashflow status) 3. STP Process for #1 - process as a normal single payment. 4. STP Process for #2 - check if cashflow has corresponding estimation flow in future (by running murex native simulation function ), if so, hold it as NSTP for 5 days. cashflow will either be netted with floating leg in the 5 days, or be STPed as normal single cashflow after 5 days. <u>**[Click for samples](#scenario6a)**</u> (open point: ratan to identify out the netted the cashflow from murex coz ratan expect settle the netted one ) |
| * | 6b* | *[Specific Scenario] NDS cashflow process & settlement.* | Ratan to design process based on today murex behaviors Murex today behavior: In murex NDS will create FXD ticket for each calculation period once rate got fixed, and perform netting for Non-Deliverable currency, settle for Deliverable currency. Migration impact post migration, the netted flow may flow to Ratan before it got fixed with FXD. <Open point: Ratan expect receive deliverable ccy cashflow only. Those non-delivery ccy should be netted in murex as it is today. murex to make change here. > <u>**[Click for samples](#scenario6b)**</u> |
| 7 | Trade market operation happens post migration which generate reverse/new cashflow. market operation such as cancel&reissue, restructure, cancellation. | Cashflow status | Desc | Trade market operation impact | | --- | --- | --- | | SENT/NET/INV | cashflow was settled from murex before cashflow migration. | generate reversal & new against original cashflow. | | SNTR/RLSR | cashflow was settled from RATAN post cashflow migration. | generate reversal & new against original cashflow. <Open point: mktops on past VD cashflow which generate reverse in past VD, murex wont to ranta, in ratan is shown as settled but actually it was cancelled in murex. > | | INIT | future cashflow that VD beyond 7 days, to send to RATAN once VD within 7 days. | Cancel (CNCL) original cashflow, generate new. | | SUPP | cashflow was not settled, but suppressed in murex | Cancel (CNCL) original cashflow, nothing generated. | | check on VD of reversal and new. if VD < system date, ops to manually handle as per BAU process, ie. post from Oscar. if VD >= system date, murex will send to Ratan once cashflow is created and VD within 7 days. **<u>[Click for samples](#scenario7)</u>** |
| Cashflow status | Desc | Trade market operation impact |
| SENT/NET/INV | cashflow was settled from murex before cashflow migration. | generate reversal & new against original cashflow. |
| SNTR/RLSR | cashflow was settled from RATAN post cashflow migration. | generate reversal & new against original cashflow. <Open point: mktops on past VD cashflow which generate reverse in past VD, murex wont to ranta, in ratan is shown as settled but actually it was cancelled in murex. > |
| INIT | future cashflow that VD beyond 7 days, to send to RATAN once VD within 7 days. | Cancel (CNCL) original cashflow, generate new. |
| SUPP | cashflow was not settled, but suppressed in murex | Cancel (CNCL) original cashflow, nothing generated. |
| 8 | User customized/modified value of fixing, which generate reversal/new payments. |
| ![image2023-4-26_19-38-51.png](attachments/image2023-4-26_19-38-51.png)Trade migration go-live | 9 | On trade migration day, murex cancel migration trades impacting existing cashflows. | <u>**[Click to open details](#scenario9)**</u> |
| Post Trade Migrate | 10 | Post trade migrate to Stella, market operation happens on Migration trade in Stella impacting the cashflows. | TBD 1. Any difference when stella process migration trade and process new trade from Blade? 2. in Ratan any additional handler required for migration trade considering for same migration trade, cashflow in pre source from trade and in post source from stella. like reference between murex trade and stella trade. |

**ANCHOR: scenario6a**

**EXPAND: sample for scenario 6a**

**scenario-1:** both fixed leg and floating leg available to generate cashflow on same day -> murex generate one payment with netted amount of fixed leg and floating leg.

trade id: 85878356

![image2023-4-25_14-24-56.png](attachments/image2023-4-25_14-24-56.png)

![image2023-4-25_14-25-24.png](attachments/image2023-4-25_14-25-24.png)

**scenario-2**: Fixed leg available to generate cashflow in prior to floating leg - murex generate payment for fixed leg firstly. then generate payment with netted amount of fixed leg and floating leg once floating leg is available, meanwhile cancel original fixed leg payment

trade 77855086

fixed leg was generated on 07-Nov-2022, with status INIT. ( SUPP status also apply to this case. )

![image2023-4-26_18-38-29.png](attachments/image2023-4-26_18-38-29.png)

fixing event was performed on 10-Jan-2023, by when fixed leg was not settled.

system cancel original fixed leg payment and generate new payment with netted amount of fixed leg and floating leg.

![image2023-4-26_18-38-11.png](attachments/image2023-4-26_18-38-11.png)

![image2023-4-26_18-40-17.png](attachments/image2023-4-26_18-40-17.png)

![image2023-4-26_18-41-51.png](attachments/image2023-4-26_18-41-51.png)

**scenario-3**: Fixed leg available to generate cashflow in prior to floating leg - murex generate payment for fixed leg firstly. then generate payment with netted amount of fixed leg and floating leg once floating leg is available, meanwhile reverse original fixed leg payment

trade 85506175

![image2023-4-26_18-45-57.png](attachments/image2023-4-26_18-45-57.png)

![image2023-4-26_18-46-32.png](attachments/image2023-4-26_18-46-32.png)

post migration it will be much similar to scenario 3, that murex send fixed leg fistly to Ratan, then generate reverse and new. the new is with netted amt.

**EXPAND_END**

**ANCHOR: scenario6b**

**EXPAND: sample for scenario 6b**

NDS Trade

![image2023-4-26_18-53-10.png](attachments/image2023-4-26_18-53-10.png)

In murex NDS will create FXD ticket for each calculation period once rate got fixed, and perform NET/INV for ND ccy cashflows in NDS and FXD.

![image2023-4-26_18-54-26.png](attachments/image2023-4-26_18-54-26.png)

one of FXD ticket

![image2023-4-26_18-56-5.png](attachments/image2023-4-26_18-56-5.png)

**EXPAND_END**

**ANCHOR: scenario7**

**EXPAND: sample for scenario 7 & 8**

trade id: 85878356

27-Mar-2023 user performed cancel&reissue (amended entity), which create reverse and new

![image2023-4-25_14-33-6.png](attachments/image2023-4-25_14-33-6.png)

be noted. the payment is netted from fixed leg plus floating leg

![image2023-4-25_14-24-56.png](attachments/image2023-4-25_14-24-56.png)

![image2023-4-25_14-25-24.png](attachments/image2023-4-25_14-25-24.png)

user customized rate on flow level for VD 08-mar-2023

![image2023-4-25_14-25-58.png](attachments/image2023-4-25_14-25-58.png)

save trade

observed system cancel original flow, generate new flow for fixed leg. Floating cashflow is not generated until we trigger fixing procedure

![image2023-4-25_14-26-21.png](attachments/image2023-4-25_14-26-21.png)

run fixing procedure for trade fixing date  08 Mar 2023

system cancel original flow, and generate flow with netted value.

![image2023-4-25_14-26-47.png](attachments/image2023-4-25_14-26-47.png)

**EXPAND_END**

### **ANCHOR: scenario9**

**EXPAND: scenario #9**

**Assumption:**

Cashflow migration go live in **4-Sep-2023**
Today is **2-Oct-2023,** is trade migration go live day, system day has rolled to Mondy.

| | **Pre Trade Migration** | **Post Trade Migration (ie. post murex cancelled migration trades)** | **Trade Migration Activity** |
| --- | --- | --- | --- |
| **Cashflow Type** | Flow# | Murex Status | **Value Date** | Amount | C/D | Flow# | Murex Status | **Value Date** | Amount | C/D | Comment | If Stella re-generates | If Ratan receive from Stella | If Murex will send to Ratan on T |
| past settled cashflow | settlement happen in murex in prior to cashflow migraton | not exist in Ratan | #1 | SENT/NET/INV | 6-Jun-23 | 100 | D | #1 | SENT/NET/INV | 6-Jun-23 | 100 | D | | Y | N as past settled cashflow <comment 28-Apr> Stella will send to TDS with status to be confirmed, Ratan to check process for that. | na |
| | **#6** | INIT | 6-Jun-23 | 100 | C | reverse of #1, with past VD | na | na | N as VD in past |
| past settled cashflow | settlement happen in Ratan post cashflow migraton | been sent to Ratan | #2 | SNTR/RLSR | 6-Sep-23 | 150 | D | #2 | SNTR/RLSR | 6-Sep-23 | 150 | D | | Y | N as past settled cashflow and already flow to ratan form murex <comment 28-Apr> Stella will send to TDS with status to be confirmed, Ratan to check process for that. | na |
| | **#7** | INIT | 6-Sep-23 | 150 | C | reverse of #2, with past VD | na | na | N as VD in past |
| future cashflow (VD within 7 days) | settlement to handle in Ratan | been sent to Ratan | #3 | SNTR/RLSR | 6-Oct-23 | 200 | D | #3 | SNTR/RLSR | 6-Oct-23 | 200 | D | | Y | <Reviewed 28-Apr> Cashflow already flown to ratan from murex. on migration day murex will send reverse flow (flow #8) to ratan, base on which ratan could offset reverse with original flow (flow #3) from murex. Ratan receive new from stella. This option requires Ratan additional control to stop user settlement for murex VD>T cashflows which to be received from stella. | na |
| | **#8** | INIT | 6-Oct-23 | 200 | C | reverse of #3, VD > T (VD within 7 days) | na | na | Y, murex will send to Ratan on migration day once cashflow created |
| future cashflow (VD beyond 7 days) | murex going to send to Ratan once VD in 7 days | not exist in Ratan | #4 | INIT | 6-Nov-23 | 300 | D | #4 | CNCL | 6-Nov-23 | 300 | D | | Y | Not on migration day, but will send to Ratan when meet stella-ratan VD criteria | N as status is not INIT |
| past settled cashflow | not settled but suppressed in murex | not exist in Ratan | #5 | SUPP | 6-Jun-23 | 350 | D | #5 | CNCL | 6-Jun-23 | 350 | D | | Y | N as past suppressed cashflow | na |

**EXPAND_END**

### 6.3  Migration Recon Approach (to be reviewed)

1. **Extraction 1**: Ratan eligible cashflow, this is list to send to Ratan.
2. **Extraction 2: **Post migration cashflow in SNTR/RLSR, this is list murex should have sent to Ratan
3. **Extraction 3**: Ratan to provide cashflow list received from murex.
4. Compare **Extraction ****1,2,3**, expect match.

### 6.4  Issue/Risk to be closed for CPT/Go-live

| Category | Change Points | System | Comment | JIRA | Owner | ETA | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Assessment on Impacted reports | list of murex reports monitoring end status of payment, will be impacted because we created new end status (SNTR/RLSR) for cashflow migration | Murex | | | Amy | | OPEN |
| Change for CPT | 1.Release one week ahead of biz go live, murex enable interface to ratan during CPT period and only send CPT eligible cashflow to Ratan. | Murex | | | Amy | | OPEN |
| 2. In case of rollback, Ratan cancel/suppress cashflow which will trigger murex bring cashflow status back to INIT. | Murex/Ratan | | | Amy, Wayne | | OPEN |
| Address PSS concerns | 1.MQ support - Liam agreed with pss that reconciliation approach would need to be signed off by the operations owner i.e. they will need to confirm they are fine with an EOD recon to highlight any issues for payment flows. - any potential change here in murex and Ratan? | Murex | | | Amy, Liam | | OPEN |
| 2. Others concerns like perfromance test evidence etc. which is growing along catch-up with pss | Murex | | | Amy | | OPEN |
| New scenarios | 1.NDS - Ratan expect receive deliverable ccy cashflow only. Those non-delivery ccy should be netted in murex as it is today. murex to make change here, and test with ratan. | Murex/Ratan | - - Dinesh and Sumita confirmed >> The NDF currency netting is preferred to be done in MX2.11. For China, the PM and non PM cashflows are in the same queue, so it is fine to monitor the ND IRS cashflows in MX2.11 queue in case auto netting fails due to technical issues. - [@Li, Lyn Yi](mailto:LynYi.Li@sc.com), how will we ensure that on the FX booked for ND IRS the NDF currency leg remains in MX2.11 but the USD flows to RATAN ? | | Amy, Wayne | | OPEN |
| 2. if user amend VD to future date which cause reversal VD in past and new VD in future, will has duplicate pay risk if new handled in ratan in prior to reverse one handled in murex. > - Ratan to identify it out and provide warning to ops to avoid duplicate pay. | Murex/Ratan | | | Amy, Wayne | | OPEN |
| 3. for SNTR/RLSR cashflow, mktops on past VD cashflow which generate reverse in past VD, murex wont send to ranta by handled in murex manually, in this case ratan is shown as settled but actually it was cancelled in murex. | Murex/Ratan | | | Amy, Wayne | | OPEN |
| 4. Others growing along Amy's analysis | Murex/Ratan | | | Amy | | OPEN |
| Prod Issues | trade in murex is config-ed as 'Not generate payment' but system still generate payment. | Murex | | | Amy | | OPEN |
| XIT create cashflow VD beyond 2 months, PAY FIX will fail to produce the payments even when it reach out pay fix window | Murex | | | Amy | | OPEN |
| when Option (cash delivery) trades under MKT_OP status got exercised, will produce duplicate record for exercise payment, and payment got auto SENT thus duplicate pay issue | Murex | | | Amy | | OPEN |
| Migration Recon | Migration Recon Approach to be discussed and to added into Migration runbook | Murex/Ratan | TBC #6.3 | | Amy | | OPEN |
| UAT | UAT Test case design | Murex/Ratan | | | Amy | | OPEN |