| | Scenario | Step |
| --- | --- | --- |
| 1 | "Confirmation_Message_Inbound_Status" : "Inbound Completed - Match Outside CDU" Dispatched_IBOutsideCDU.json---sample1 in the email | 1.Find a tradeid :BCS_3297952,cashflowid: 6257787319 in Cashflow Blotter[FX &Equity] ![image-2025-6-19_14-45-31.png](attachments/image-2025-6-19_14-45-31.png) ![image-2025-6-19_15-10-15.png](attachments/image-2025-6-19_15-10-15.png) ![image-2025-6-19_14-49-13.png](attachments/image-2025-6-19_14-49-13.png) 2.Input SI in Settlement Exceptions ![image-2025-6-19_14-50-38.png](attachments/image-2025-6-19_14-50-38.png) ![image-2025-6-19_15-11-34.png](attachments/image-2025-6-19_15-11-34.png) 3.Verify SI in Settlement Exceptions ![image-2025-6-19_15-12-36.png](attachments/image-2025-6-19_15-12-36.png) ![image-2025-6-19_15-18-49.png](attachments/image-2025-6-19_15-18-49.png) 4.Hit NSTP rule ![image-2025-6-19_15-19-29.png](attachments/image-2025-6-19_15-19-29.png) ![image-2025-6-19_15-20-7.png](attachments/image-2025-6-19_15-20-7.png) 5.Produce a CDU event with "Confirmation_Message_Inbound_Status" : "Inbound Completed - Match Outside CDU" message : ![image-2025-6-19_17-24-57.png](attachments/image-2025-6-19_17-24-57.png) select * from ratanone.event_record er where row_id in (select body_event_rowkey from ratanone.ratan_minor_version_history rmvh where cashflow_id ='6257787319') ![image-2025-6-19_21-0-42.png](attachments/image-2025-6-19_21-0-42.png) 6.Trigger STP ![image-2025-6-19_17-20-56.png](attachments/image-2025-6-19_17-20-56.png) ![image-2025-6-19_17-21-28.png](attachments/image-2025-6-19_17-21-28.png) |
| 2 | "Confirmation_Message_Inbound_Status" : "Inbound Completed - Inbound Not Required", Dispatched_IBsuppressed.json---sample2 in email | 1.Find a tradeid : BCS_3719646,cashflowid: 6261288851 in Cashflow Blotter[FX &Equity] ![image-2025-6-19_17-28-0.png](attachments/image-2025-6-19_17-28-0.png) ![image-2025-6-19_19-39-58.png](attachments/image-2025-6-19_19-39-58.png) ![image-2025-6-19_19-42-13.png](attachments/image-2025-6-19_19-42-13.png) 2.Input SI in Settlement Exceptions ![image-2025-6-19_19-45-31.png](attachments/image-2025-6-19_19-45-31.png) ![image-2025-6-19_19-46-20.png](attachments/image-2025-6-19_19-46-20.png) 3.Verify SI in Settlement Exceptions ![image-2025-6-19_19-47-19.png](attachments/image-2025-6-19_19-47-19.png) ![image-2025-6-19_19-53-16.png](attachments/image-2025-6-19_19-53-16.png) ![image-2025-6-19_19-54-1.png](attachments/image-2025-6-19_19-54-1.png) 4.Hit NSTP rule ![image-2025-6-19_19-54-54.png](attachments/image-2025-6-19_19-54-54.png) ![image-2025-6-19_19-56-25.png](attachments/image-2025-6-19_19-56-25.png) 5.Produce a CDU event with "Confirmation_Message_Inbound_Status" : "Inbound Completed - Inbound Not Required" message : ![image-2025-6-19_20-13-46.png](attachments/image-2025-6-19_20-13-46.png) select * from ratanone.event_record er where row_id in (select body_event_rowkey from ratanone.ratan_minor_version_history rmvh where cashflow_id ='6261288851') ![image-2025-6-19_20-59-53.png](attachments/image-2025-6-19_20-59-53.png) 6.Trigger STP ![image-2025-6-19_20-8-51.png](attachments/image-2025-6-19_20-8-51.png) ![image-2025-6-19_20-9-49.png](attachments/image-2025-6-19_20-9-49.png) |

---

Tips:

The Below status will trigger Trade_State changed

- Inbound Completed - Match Completed
- Inbound Completed - Inbound Not Required
- Inbound Completed - Match Outside CDU

![image-2025-6-18_10-22-54.png](attachments/image-2025-6-18_10-22-54.png)

"Trade/Cash not affirmed" NSTP Rule detail:

Trade_State != "AFFIRMED" && Trade_State != "CONFIRMED" && Cashflow__Cashflow_Affirmation_Status != "Affirmed"

---