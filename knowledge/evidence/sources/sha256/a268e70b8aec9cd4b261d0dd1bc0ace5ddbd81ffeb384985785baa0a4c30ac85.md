Background and Prod Approach pls refer to [FMRP Trade Migration - Ratan Cash Settlement - PROD Approach]

Release Work Item: NA

# **Scope:**

- 8th & 9th Oct (17th Oct runbook for Rates India Onshore + FXO Phase 3a) ~50k
- 9th & 10th Oct (24th Oct runbook for Rates India offshore + Gift city Mum + FXO Phase 3a) ~77k

# **Whole Project ****Runbook**

- **[Runbook_IN_FXO.xlsx](https://standardcharteredbank-my.sharepoint.com/:x:/g/personal/1521275_zone1_scb_net/IQDo4gOayinsQogFC4UiBAFjAT4AAodkd2PdK1gMq1sIBLs?email=Elena.Wang%40sc.com&e=13Nqrv&wdExp=TEAMS-TREATMENT&web=1)**
- ****DR_FXO_Migration_RunBook**** - ![image-2026-10-8_17-22-3.png](attachments/image-2026-10-8_17-22-3.png)
- ****DR_IN_Migration_RunBook**** - **![image-2026-10-8_17-24-34.png](attachments/image-2026-10-8_17-24-34.png)**

# **RunBook**

| Steps | Date | Events | TODO | By | Status | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-25 | **Secure Data Dump** - COBE Date: 2026-09-25 | | Cai1, Jie | | |
| 2 | 2026-10-08 | NA | Provide In-Scope **Portfolio **List | @Yonggang Carter Deng @Guna | | |
| 3 | 2026-10-08 | NA | Analyze future 7 days Murex2.11 cashflows to check if any Break points based on current Prod Approach. | @Kuan Wang (Elena) | | |
| 4 | **Migration Day** | NA | Setup Cashflow Suppression Rule to suppress Murex Cancellation cashflow **Note: only for UAT / DR** | @Kuan Wang (Elena) | | Data_Flow.Data_Source_System == "MUREX" AND Cashflow.Cashflow_Event_Type == "Withdrawal" AND (Cashflow.Payment_Date = "2026-09-28" OR Cashflow.Payment_Date = "2026-09-29") - Priority of CANCELLED higher than CASHFLOW_SUPPRESSED - RELEASED/SETTLED → CASHFLOW_SUPPRESSED |
| 5 | NA | Setup **Stella High Risk NSTP rule:** FMRP80_TM_Stella_Cfs - **Data Source System in (Stella, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - **In-Scope Portfolio** | @Kuan Wang (Elena) | | Mock cf: |
| 6 | NA | 1. Provide **Cancelled Trade Id list** - final version - e.g. **UAT**: cancellation Summary_TradeList.xlsx - by 1pm 2. **Murex → Ratan** **Settlement**** cashflow list** - e.g. UAT: FMRP7.0_Murex_RatanResult_PaymentList.xlsx - **Cashflows From Trade Cancellation because of Trade Migration** - cashflows in Migrated scope - cashflows In-cancellation-Scope but not migrated scope - FXD trades from NDS Fixing - cashflows will feed into Ratan Settlement Next Monday e.g. 104034168 - **Total num** - If recon broken, then Cashflows list from BAU behavior needed. 3. **Mapping **between FXD trade id and Parent NDS trade id(for future 7 days recon) | @Linzhen Wu (Wythe) | | |
| 7 | 1. **Stella → Ratan** **Settlement Cashflow List** 2. **Mapping** between Murex Trade Id and Stella Trade Id | @Nagaraj Ponnuchamy | | |
| 8 | Export future 7 days cashflows by Murex Trade ID | @Kuan Wang (Elena) | | |
| 9 | **Migration Behavior:** - **Stella cashflows**** feeding** into Ratan Settlement ** ** | Monitor Stella cashflows feeding in | @Kuan Wang( Elena) | | ** ** |
| 10 | NA | Export future 7 days cashflows by Stella Trade ID | @Kuan Wang( Elena) | | |
| | **Start** Auto Netting Job (Invoke Auto Job API) | | |
| 11 | **Recon Report**: Stella vs RATAN Cashflow feed Recon - Total Number in Group Blotter & Cashflow Blotter - No Pending cfs in Group Blotter - etc... | | |
| 12 | **Recon Report:** Stella vs Murex2.11 7 days Cashflow Recon | | |
| 13 | **Disable **Stella NSTP rule - FMRP70_TM_Stella_ASENCfs | @Kuan Wang( Elena) | | |
| 14 | **Migration Behavior:** - **Murex cashflows feeding** into Ratan Settlement ** ** | ** **Monitor Cancellation feeding | Joey @Kuan Wang( Elena) | | |
| 15 | NA | Murex2.11 vs RATAN Cancellation Recon - Murex cashflows CASHFLOW_SUPPRESSED | @Kuan Wang( Elena) | | |
| 16 | NA | Create Filter: 00Elena_TM_Stella_NSTP_Cfs to get Cashflow list with Stella High Risk NSTP Exception - Export excel | @Kuan Wang( Elena) | | e.g. ![image-2026-1-21_17-38-21-1.png](attachments/image-2026-1-21_17-38-21-1.png) |
| 17 | NA | Bulk cashflow_suppress & un-cashflow_suppress Stella cashflows in Filter: 00Elena_TM_Stella_NSTP_Cfs so that cashflows can be processed as normal BAU behavior. | - Ops User | | |