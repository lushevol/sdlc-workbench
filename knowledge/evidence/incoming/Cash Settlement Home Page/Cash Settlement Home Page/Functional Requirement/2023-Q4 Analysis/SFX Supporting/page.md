Involved in the support from migration cycle 2 test, TDS3 only send the last version of historical data to Ratan which is not production-like behavior. Only the rebook event  received and processed from Ratan

2024-01-11 DR actitivity, data cut will be Feb.23rd, expect to be load in March(date will be confirmed)

2023-11-09

- Support OPS (Karthik) required test scenarios, cashflow got ack from Razor without other status, replied mail to Karthik to confirm if it's OK or need to rebook cashflow for test

📎 [RE_ SFX-Cycle2_ Life Cycle Testing updates - FMO FXMM Equities Settlement (Equity Derivs).msg](attachments/RE_ SFX-Cycle2_ Life Cycle Testing updates - FMO FXMM Equities Settlement (Equity Derivs).msg)

- Support lifecycle test to check cashflow received in Ratan and sent to Razor after ops user processed. Checked the lates list shared by upstream, some are pending for ops manual processing, some has been sent to LMS/Razor, replied mail.

📎 [RE_ Project SFX - Lifecycle Testing 1 - BCSSTELLA - Test Trade_Connectivity.msg](attachments/RE_ Project SFX - Lifecycle Testing 1 - BCSSTELLA - Test Trade_Connectivity.msg)

- Aligned with LMS on the DR test approach and replied to Shyam (SFX PM) - **Items to be confirmed with Dinesh/Karthik** 1. LMS will ignore all the past value date event generated in the migration weekend which reply on the assumption that all the cashflow with payment date before migration date should be settled, any concern on this point? 2. Currently we have enable partial STP process in BCS flow, any possibility to trigger unexpected STP during the migration weekend? do we need to add extra NSTP rule to hold all cashflow and remove it after migration? – enable NSTP rule to hold all unaffirmed cashflow during the migration weekend. 3. Expected result from DR 1. Withdrawal ACU event received in Ratan and hold in NSTP queue for past value date cashflow, future cashflow will be directly canceled in Ratan 2. Withdrawal ACU event should be sent to LMS if it has been sent to LMS before 3. Rebook DBU event received in Ratan and hold in NSTP queue. Ops will ignore the past value date ones, only process future cashflow in BAU process. Q: if the future cashflow are hold in SSI exception, will ops user process that for test or no need to cover in test phase?

![image2023-11-10_16-17-37.png](attachments/image2023-11-10_16-17-37.png)
📎 [RE_ Sample data for DR test approach.msg](attachments/RE_ Sample data for DR test approach.msg)