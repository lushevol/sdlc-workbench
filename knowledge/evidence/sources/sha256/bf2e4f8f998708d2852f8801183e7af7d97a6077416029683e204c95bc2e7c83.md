Background and Prod Approach pls refer to [FMRP Trade Migration - Ratan Cash Settlement - PROD Approach]

Release Work Item: NA

# **Runbook**

| Steps | Date | Events | TODO | By | By Date | Status | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | VD-7BD - VD: Next Monday - 2026-05-07 | **BAU Behavior** - Murex2.11 cashflows **feeding **into Ratan Settlement | Provide In-Scope **Portfolio **List | Migration Team @Yonggang Carter Deng | 2026-05-06 | | |
| 2 | VD-6BD - 2026-05-08 | NA | Setup **Murex High Risk NSTP rule: FMRP70_TM_Murex_Cfs **before Materialization Date - **Data Source System = MUREX** - **Payment Date in (Next Mon. , Next Tue.)** - **In-Scope Portfolio** | - @Cordelia Sumita K Thirunavukarasu - Rule User | 2026-05-07 | | |
| 3 | **UVT to Murex High Risk NSTP rule: FMRP70_TM_Murex_Cfs** | @Cordelia Sumita K Thirunavukarasu @Kuan Wang (Elena) | | | Elena: 2026-05-08 Replicated Prod Data: M00126110525 and Murex High Risk NSTP rule into Non-Prod env. The rule working ![image-2026-5-8_17-28-58.png](attachments/image-2026-5-8_17-28-58.png) |
| 4 | Each day until Migration Weekend | | **Monitor **cashflows(until 15th May - Friday 9PM) in Pending Auto Netting / Pending Netting / Pending Another Leg which will not hit Above High risk NSTP rule. Ops user not do net in advance. - Check the list if there are any In-Scope Murex cashflows wrongly RELEASED/SETTLED **Note**: If Murex cashflows **wrongly** RELEASED/SETTLED, the cashflow will be WAITING + Reversal after Murex Cancellation feeding in. **Next Step**: Release the withdraw murex cashflows and Stella cashflows. | @Kuan Wang (Elena) | | | ** **By Create filter or by sql in sql_byPort.txt |
| 5 | VD-5BD - 2026-05-11 | **BAU Behavior** - Murex Cashflows **materialized**, then STP'd or NSTP | **Create Filter: 00Elena_TM_Murex_NSTP_Cfs** to get Murex2.11 cashflows hit above NSTP rule | @Kuan Wang (Elena) | | | **![image-2026-1-21_17-38-21-1.png](attachments/image-2026-1-21_17-38-21-1.png)** |
| 6 | **Migration Weekend** - **Saturday** - 2026-05-16 | NA | 1. Provide **Cancelled Trade Id list** - final version - e.g. **UAT**: cancellation Summary_TradeList.xlsx - by 1pm 2. **Murex → Ratan** **Settlement**** cashflow list** - e.g. UAT: FMRP7.0_Murex_RatanResult_PaymentList.xlsx - **Cashflows From Trade Cancellation because of Trade Migration** - cashflows in Migrated scope - cashflows In-cancellation-Scope but not migrated scope - FXD trades from NDS Fixing - cashflows will feed into Ratan Settlement Next Monday e.g. 104034168 - **Total num** - If recon broken, then Cashflows list from BAU behavior needed. 3. **Mapping **between FXD trade id and Parent NDS trade id(for future 7 days recon) 4. Migration Trade Details (for NDCCS / NDIRS) | Murex Team @Linzhen Wu (Wythe) | | | |
| 7 | 1. **Stella → Ratan** **Settlement Cashflow List** 2. **Mapping** between Murex Trade Id and Stella Trade Id | Migration Team @Nagaraj Ponnuchamy | | | |
| 8 | Export cashflows in **Filter: 00Elena_TM_Murex_NSTP_Cfs** - Get cashflow id list for **Cashflow Suppress & un-Suppress** | - @Kuan Wang (Elena) | | | |
| 9 | Export Murex future 7 days cashflows by Trade ID(original trade id) for future 7 days recon - 3pm stand by | - @Kuan Wang (Elena) - PSS | | | |
| 10 | Update **Murex High Risk NSTP rule** - - **Data Source System = MUREX** - **Payment Date in (Next Mon. , Next Tue.)** - ~~**In-Scope Portfolio**~~ - **Cancelled Trade Id / Original Trade Id List** - **Stand by 2pm** | - Ops User - Rule User | | | |
| 11 | Setup **Stella High Risk NSTP rule:** FMRP70_TM_Stella_ASENCfs - **Data Source System in (Stella, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - **In-Scope Portfolio** | - Ops User - Rule User | | | |
| 12 | **Cashflow Suppress & un-Suppress** the cashflows in **Filter: 00Elena_TM_Murex_NSTP_Cfs **so that the out of scope cashflows can be processed as normal BAU behavior - STP'd - **NSTP'd cashflows** – (Elena provide out of migration scope cf list) | - Ops User - @Kuan Wang (Elena) | | | **Elena: 2026-05-16 ** | | ByPortfolio | ByTradeIdOrOriginalTradeId | NarrowDown | | --- | --- | --- | --- | | Total Num Of Cfs | 2135 | 1702 | 433 | | Total Num Of Cfs with NSTP Exception | 316 | 157 | 159 | |
| | ByPortfolio | ByTradeIdOrOriginalTradeId | NarrowDown |
| Total Num Of Cfs | 2135 | 1702 | 433 |
| Total Num Of Cfs with NSTP Exception | 316 | 157 | 159 |
| 13 | **Migration Weekend** - **Sunday** - 2026-05-17 | NA | **Stop Auto Netting Job** - planned at 12am, real time, pls contact Elena | - PSS - Devops | | | |
| 14 | **Migration Behavior:** - **Stella cashflows**** feeding** into Ratan Settlement ** ** | Monitor Stella cashflows feeding in | - PSS - @Kuan Wang( Elena) | | | ** ** |
| 15 | NA | Export future 7 days cashflows for Stella by Trade ID | - PSS | | | ** ** |
| 16 | NA | **Start** Auto Netting Job | - PSS | | | |
| 17 | Export future 7 days cashflows for Stella by Trade ID after running Auto Netting Job | - PSS | | | |
| 18 | **Recon Report**: Stella vs RATAN Cashflow feed Recon - Total Number in Group Blotter & Cashflow Blotter - No Pending cfs in Group Blotter - etc... | - @Kuan Wang( Elena) | | | |
| 19 | **Recon Report:** Stella vs Murex2.11 7 days Cashflow Recon | - @Kuan Wang( Elena) | | | |
| 20 | **Disable **Murex & Stella NSTP rule - FMRP70_TM_Murex_ASENCfs - FMRP70_TM_Stella_ASENCfs **Stand By 8 pm ** | - Ops User - Rule User | | | |
| 21 | **Migration Behavior:** - **Murex cashflows feeding** into Ratan Settlement ** ** | ** **Monitor Cancellation feeding | PSS | | | |
| 22 | NA | Export future 7 days cashflows for Murex by Trade ID | - PSS | | | |
| 23 | ** **NA | Murex2.11 vs RATAN Cancellation Recon - Murex cashflows **cancelled naturally **along with Trade Cancellation | - @Kuan Wang( Elena) | | | |
| 24 | ** **NA | Create Filter: 00Elena_TM_Stella_NSTP_Cfs to get Cashflow list with Stella High Risk NSTP Exception - Export excel | - @Kuan Wang( Elena) | | | e.g. ![image-2026-1-21_17-38-21-1.png](attachments/image-2026-1-21_17-38-21-1.png) |
| 25 | ** **NA | 1. Recon reports review 2. Bulk cashflow_suppress & un-cashflow_suppress Stella cashflows in Filter: 00Elena_TM_Stella_NSTP_Cfs so that cashflows can be processed as normal BAU behavior. | - Ops User | | | |