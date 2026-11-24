# **Background and Prod Approach**

- [FMRP Trade Migration - Ratan Cash Settlement - PROD Approach]
- [FXO Tech Readiness - FXO Phase1, Phase2, Phase3 & Phase4 - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3817572021)

Release Work Item: NA

# **Scope:**

- ![image-2026-10-8_11-21-3.png](attachments/image-2026-10-8_11-21-3.png)

# **Portfolio**

- **FXO: [DR RATES IN + FXO (AE, DE, JP, SG, UK, US) - Migration Artefacts - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3904823250)**
- **India Rates**: [DR RATES IN + FXO (AE, DE, JP, SG, UK, US) - MO Review - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3904823223)

# **Whole Project ****Runbook**

- **[Runbook_IN_FXO.xlsx](https://standardcharteredbank-my.sharepoint.com/:x:/g/personal/1521275_zone1_scb_net/IQDo4gOayinsQogFC4UiBAFjAT4AAodkd2PdK1gMq1sIBLs?email=Elena.Wang%40sc.com&e=13Nqrv&wdExp=TEAMS-TREATMENT&web=1)** - **IN_Migration_RunBook** - **![image-2026-10-8_16-18-16.png](attachments/image-2026-10-8_16-18-16.png)** - **FXO_Migration_RunBook** - **![image-2026-10-8_16-20-47.png](attachments/image-2026-10-8_16-20-47.png)**

# **Ratan Settlement Runbook**

| Steps | Date | Events | TODO | By | By Date | Status | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | VD-7BD: Thur. 2026-10-08 - VD is Next Monday - 2026-10-19 | **BAU Behavior** - Murex2.11 cashflows **feeding **into Ratan Settlement | Provide In-Scope **Portfolio **List | Migration Team @Yonggang Carter Deng | 2026-10-09 | | |
| 2 | VD-6BD: Fri. - 2026-10-09 | NA | Setup **Murex High Risk NSTP rule: TM_Murex_Cfs ** before Materialization Date - **Data Source System in (MUREX, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - **In-Scope Portfolio** | - @Cordelia Sumita K Thirunavukarasu - @Bin Abdul Kadir Abdullah - Rule User | | | |
| 3 | **UVT to Murex High Risk NSTP rule: TM_Murex_Cfs** | @Bin Abdul Kadir Abdullah @Cordelia Sumita K Thirunavukarasu | | | |
| 4 | VD-5BD: Mon. - 2026-09-07 | **BAU Behavior** - Murex Cashflows **materialized**, then STP'd or NSTP | **Create Filter: 00Elena_TM_Murex_NSTP_Cfs** to get Murex2.11 cashflows hit above NSTP rule | @Kuan Wang (Elena) | | | |
| 5 | Each day until Migration Weekend 2026-09-07 - 2026-09-12 | | **Monitor **cashflows(until 14th Aug - Friday 9PM) in Pending Auto Netting / Pending Netting / Pending Another Leg which will not hit Above High risk NSTP rule. Ops user not do net in advance. - Check the list if there are any In-Scope Murex cashflows wrongly RELEASED/SETTLED **Note**: If Murex cashflows **wrongly** RELEASED/SETTLED, the cashflow will be WAITING + Reversal after Murex Cancellation feeding in. **Next Step**: Release the withdraw murex cashflows and Stella cashflows. | @Kuan Wang (Elena) | | | ** **By Create filter or by sql in 00_monitorSql |
| 6 | **Migration Weekend** - **Saturday** - 2026-05-16 | NA | 1. Provide **Cancelled Trade Id list** - final version - Murex_ratan_cancel_report.csv** - 9:30?** - **Mapping **between FXD trade id and Parent NDS trade id(for future 7 days recon) if there is 2. **Murex → Ratan** **Settlement**** cashflow list** - murex_ratan_cashflow_report.csv 3. Pending Cash Cancellation List.csv | Murex Team @Linzhen Wu (Wythe) | | | |
| 7 | 1. **Stella → Ratan** **Settlement Cashflow List - 9:30?** 2. **Mapping** between Murex Trade Id and Stella Trade Id | Migration Team @Nagaraj Ponnuchamy | | | 13:13 pm cf list file provided. |
| 8 | Export cashflows in **Filter: 00Elena_TM_Murex_NSTP_Cfs** - Get cashflow id list for **Cashflow Suppress & un-Suppress** | @Kuan Wang (Elena) | | | |
| 9 | Export Murex future 7 days cashflows by Trade ID(original trade id) for future 7 days recon - 10am stand by? | - @Kuan Wang (Elena) - PSS | | | |
| 10 | Update **Murex High Risk NSTP rule** - - **Data Source System in (MUREX, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - ~~**In-Scope Portfolio**~~ - **Cancelled Trade Id / Original Trade Id List** - **Stand by 11am?** | - Ops User - Rule User | | | |
| 11 | Setup **Stella High Risk NSTP rule:** TM_Stella_Cfs - **Data Source System in (Stella, Ratan)** - **Payment Date in (Next Mon. , Next Tue.)** - **In-Scope Portfolio** | - Ops User - Rule User | | | |
| 12 | **Cashflow Suppress & un-Suppress** the cashflows in **Filter: 00Elena_TM_Murex_NSTP_Cfs **so that the out of scope cashflows can be processed as normal BAU behavior - STP'd - **NSTP'd cashflows** – (Elena provide out of migration scope cf list) | - Ops User - @Kuan Wang (Elena) | | | |
| 14 | **Migration Behavior:** - **Stella cashflows**** feeding** into Ratan Settlement ** ** | Monitor Stella cashflows feeding in | - PSS - @Kuan Wang( Elena) | | | ** ** |
| 15 | NA | Export future 7 days cashflows for Stella by Trade ID | - PSS | | | ** ** |
| 18 | NA | **Recon Report**: Stella vs RATAN Cashflow feed Recon - Total Number in Group Blotter & Cashflow Blotter - No Pending cfs in Group Blotter - etc... | - @Kuan Wang( Elena) | | | |
| 19 | **Recon Report:** Stella vs Murex2.11 7 days Cashflow Recon | - @Kuan Wang( Elena) | | | |
| 20 | **Disable **Murex & Stella NSTP rule - TM_Murex_Cfs - TM_Stella_Cfs **Stand By 18 pm** | - Ops User - Rule User | | | |
| 21 | **Migration Behavior:** - **Murex cashflows feeding** into Ratan Settlement ** ** | ** **Monitor Cancellation feeding | PSS | | | |
| 22 | NA | Export future 7 days cashflows for Murex by Trade ID | - PSS | | | |
| 23 | ** **NA | Murex2.11 vs RATAN Cancellation Recon - Murex cashflows **cancelled naturally **along with Trade Cancellation | - @Kuan Wang( Elena) | | | |
| 24 | ** **NA | Create Filter: 00Elena_TM_Stella_NSTP_Cfs to get Cashflow list with Stella High Risk NSTP Exception - Export excel | - @Kuan Wang( Elena) | | | |
| 25 | ** **NA | 1. Recon reports review 2. Bulk cashflow_suppress & un-cashflow_suppress Stella cashflows in Filter: 00Elena_TM_Stella_NSTP_Cfs so that cashflows can be processed as normal BAU behavior. | - Ops User | | | |