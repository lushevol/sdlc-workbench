# **Background and Prod Approach**

- [FMRP Trade Migration - Ratan Cash Settlement - PROD Approach]
- [FXO Tech Readiness - 8.0 - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/FXO+Tech+Readiness+-+8.0)

Release Work Item: NA

# **Scope:**

- ![image-2026-7-30_19-32-49.png](attachments/image-2026-7-30_19-32-49.png)
- 100 + trades (130 on 3th Aug)
- **Portfolio** - | OP_GBL_THO | OP_GBL_THO_STL | | --- | --- | | OP_BTB_THAI | OP_BTB_THAI_STL | | OP_GBL_CNY | OP_GBL_CNY_STL | | OP_BTB_TANZNIA | OP_BTB_TANZNIA_STL | | OP_GBL_ZAR | OP_GBL_ZAR_STL |

# **Whole Project ****Runbook**

- [Runbook_MiniMigration_FXO.xlsx](https://standardcharteredbank-my.sharepoint.com/:x:/r/personal/1521275_zone1_scb_net/_layouts/15/Doc.aspx?sourcedoc=%7B96537F3C-69C0-4DD0-8A71-219D80E98DA3%7D&file=Runbook_MiniMigration_FXO.xlsx&action=default&mobileredirect=true)
- ![image-2026-8-3_14-38-23.png](attachments/image-2026-8-3_14-38-23.png)

# **Ratan Settlement Runbook**

| Steps | Date | Events | TODO | By | By Date | Status | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | VD-7BD: Thur. - VD: Next Monday - 2026-08-06 | **BAU Behavior** - Murex2.11 cashflows **feeding **into Ratan Settlement | Provide In-Scope **Portfolio **List | Migration Team @Yonggang Carter Deng | 2026-08-06 | | |
| 2 | VD-6BD: Fri. - 2026-08-07 | NA | Setup **Murex High Risk NSTP rule: FXO-Mini_TM_Murex_Cfs ** before Materialization Date - **Data Source System in (MUREX, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - **In-Scope Portfolio** | - @Cordelia Sumita K Thirunavukarasu - Rule User | 2026-08-07 | | |
| 3 | **UVT to Murex High Risk NSTP rule: FXO-Mini_TM_Murex_Cfs** | @Kuan Wang (Elena) | | | Elena: 2026-08-07 done by @Bin Abdul Kadir Abdullah ![image-2026-8-10_14-32-26.png](attachments/image-2026-8-10_14-32-26.png) |
| 4 | Each day until Migration Weekend | | **Monitor **cashflows(until 14th Aug - Friday 9PM) in Pending Auto Netting / Pending Netting / Pending Another Leg which will not hit Above High risk NSTP rule. Ops user not do net in advance. - Check the list if there are any In-Scope Murex cashflows wrongly RELEASED/SETTLED **Note**: If Murex cashflows **wrongly** RELEASED/SETTLED, the cashflow will be WAITING + Reversal after Murex Cancellation feeding in. **Next Step**: Release the withdraw murex cashflows and Stella cashflows. | @Kuan Wang (Elena) | | | ** **By Create filter or by sql in sql_byPort.txt |
| 5 | VD-5BD: Mon. - 2026-08-10 | **BAU Behavior** - Murex Cashflows **materialized**, then STP'd or NSTP | **Create Filter: 00Elena_TM_Murex_NSTP_Cfs** to get Murex2.11 cashflows hit above NSTP rule | @Kuan Wang (Elena) | | | **No Reversal Payment from Murex feeding in** |
| 6 | **Migration Weekend** - **Saturday** - 2026-05-16 | NA | 1. Provide **Cancelled Trade Id list** - final version - Murex_ratan_cancel_report.csv** - 9:30?** - **Mapping **between FXD trade id and Parent NDS trade id(for future 7 days recon) if there is 2. **Murex → Ratan** **Settlement**** cashflow list** - murex_ratan_cashflow_report.csv 3. Pending Cash Cancellation List.csv | Murex Team @Linzhen Wu (Wythe) | | | |
| 7 | 1. **Stella → Ratan** **Settlement Cashflow List - 9:30?** 2. **Mapping** between Murex Trade Id and Stella Trade Id | Migration Team @Nagaraj Ponnuchamy | | | |
| 8 | Export cashflows in **Filter: 00Elena_TM_Murex_NSTP_Cfs** - Get cashflow id list for **Cashflow Suppress & un-Suppress** | @Kuan Wang (Elena) | | | |
| 9 | Export Murex future 7 days cashflows by Trade ID(original trade id) for future 7 days recon - 10am stand by? | - @Kuan Wang (Elena) - PSS | | | |
| 10 | Update **Murex High Risk NSTP rule** - - **Data Source System in (MUREX, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - ~~**In-Scope Portfolio**~~ - **Cancelled Trade Id / Original Trade Id List** - **Stand by 11am?** | - Ops User - Rule User | | | |
| 11 | Setup **Stella High Risk NSTP rule:** FXO-Mini_TM_Stella_Cfs - **Data Source System in (Stella, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - **In-Scope Portfolio** | - Ops User - Rule User | | | |
| 12 | **Cashflow Suppress & un-Suppress** the cashflows in **Filter: 00Elena_TM_Murex_NSTP_Cfs **so that the out of scope cashflows can be processed as normal BAU behavior - STP'd - **NSTP'd cashflows** – (Elena provide out of migration scope cf list) | - Ops User - @Kuan Wang (Elena) | | | Elena: 2026-08-15 Done by Babu on 14th Aug - Friday |
| 14 | **Migration Behavior:** - **Stella cashflows**** feeding** into Ratan Settlement ** ** | Monitor Stella cashflows feeding in | - PSS - @Kuan Wang( Elena) | | | ** ** |
| 15 | NA | Export future 7 days cashflows for Stella by Trade ID | - PSS | | | ** ** |
| 18 | NA | **Recon Report**: Stella vs RATAN Cashflow feed Recon - Total Number in Group Blotter & Cashflow Blotter - No Pending cfs in Group Blotter - etc... | - @Kuan Wang( Elena) | | | |
| 19 | **Recon Report:** Stella vs Murex2.11 7 days Cashflow Recon | - @Kuan Wang( Elena) | | | |
| 20 | **Disable **Murex & Stella NSTP rule - FXO-Mini_TM_Murex_Cfs - FXO-Mini_TM_Stella_Cfs **Stand By 4 pm** | - Ops User - Rule User | | | Murex Rule: done on 14th Aug - Friday |
| 21 | **Migration Behavior:** - **Murex cashflows feeding** into Ratan Settlement ** ** | ** **Monitor Cancellation feeding | PSS | | | |
| 22 | NA | Export future 7 days cashflows for Murex by Trade ID | - PSS | | | |
| 23 | ** **NA | Murex2.11 vs RATAN Cancellation Recon - Murex cashflows **cancelled naturally **along with Trade Cancellation | - @Kuan Wang( Elena) | | | |
| 24 | ** **NA | Create Filter: 00Elena_TM_Stella_NSTP_Cfs to get Cashflow list with Stella High Risk NSTP Exception - Export excel | - @Kuan Wang( Elena) | | | e.g. ![image-2026-1-21_17-38-21-1.png](attachments/image-2026-1-21_17-38-21-1.png) |
| 25 | ** **NA | 1. Recon reports review 2. Bulk cashflow_suppress & un-cashflow_suppress Stella cashflows in Filter: 00Elena_TM_Stella_NSTP_Cfs so that cashflows can be processed as normal BAU behavior. | - Ops User | | | |