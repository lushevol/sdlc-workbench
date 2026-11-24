# Background

For some exceptional cases, user may need to check in group blotter and select "manual STP" option to manually push the cashflow to cashflow blotter. Currently manual STP is only allowed for single record, it's time consuming if user need to manually handle multiple records.

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6472976](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6472976)

# Requirement Details

1. Load 1000 cashflows by default with option to load next 1000/5000 - refer to the function enabled in cashflow blotter, system will display 1000 records by default, user can manual change the page size to 5000 ![image-2025-10-24_16-44-38.png](attachments/image-2025-10-24_16-44-38.png)
2. Enable Bulk STP in Group Blotter with Pop-up warning for specific group status **NOTE**: currently if cashflow status in group blotter are PENDING or ERROR, user is able to select manual STP option with single cashflow ![](https://confluence.global.standardchartered.com/download/attachments/3501540317/image-2025-10-30_16-41-10.png?version=1&modificationDate=1761813670000&api=v2)** TOBE:** 1. If multiple cashflow selected and all selected cashflow group status are in **PENDING_TRADE_VALIDATION or PENDING_PRE_GROUP**, there will be "Manual STP" option in the right click menu 1. if selected cashflow are in PENDING_TRADE_VALIDATION or PENDING_PRE_GROUP ![image-2025-11-5_11-40-6.png](attachments/image-2025-11-5_11-40-6.png) 2. if user selected other status, system will popup error message: ![image-2025-11-5_11-30-6.png](attachments/image-2025-11-5_11-30-6.png) 2. after select "Manual STP", system will popup warning message with the "Please only perform bulk manual STP when informed by support team<br> [count] cashflow selected " + existing warning message as below ![image-2025-11-7_9-54-46.png](attachments/image-2025-11-7_9-54-46.png) Existing warning message: ![image-2025-10-13_19-25-55.png](attachments/image-2025-10-13_19-25-55.png)![image-2025-10-13_19-26-34.png](attachments/image-2025-10-13_19-26-34.png) 3. if all processed: ![image-2025-10-30_16-47-39.png](attachments/image-2025-10-30_16-47-39.png) 4. if all failed: ![image-2025-10-30_16-48-12.png](attachments/image-2025-10-30_16-48-12.png)

# Open Questions

| Raise Date | Description | Comment | Status |
| --- | --- | --- | --- |
| 2025-10-30 | if selected cashflow are in PENDING status, there will be potential risk to STP duplicated payment: ![image-2025-10-30_17-25-39.png](attachments/image-2025-10-30_17-25-39.png) | 2025-11-04 Cnfirmed with Dinesh and agree to add constrain that user will be able to do bulk manual STP only when cashflow group status are PENDING_TRADE_VALIDATION or PENDING_PREV_GROUP, | Closed |
| | | | |

# Business Use Case

| | Function | Scenario | Expected Result | Comment |
| --- | --- | --- | --- | --- |
| 1 | 1 Group in PENDING_TRADE_VALIDATION | 1. Group 1, count =3, C1,C2 C3 received and in PENDING TRADE VALIDATION 2. ops select all and manual STP C1, C2,C3 | 1. C1,C2,C3 status = 'PENDING', G1 group status = 'PENDING_TRADE_VALIDATION' 2. C1,C2,C3 status = 'END', group status = 'COMPLETED', bookingSystemEvent = 'ManualDeliver' | |
| 2 | 2 Group in PENDING_PRE_GROUP | 1. Group 1, count =2, C1 received and in PENDING, C2 not received Group 2 with the same trade id as Group 1, count =2, C3, C4 are in PENDING_PRE_GROUP 2. ops select all and manual STP C3,C4 | 1. C1 status = 'PENDING', group status = 'PENDING' C3 C4 status =PENDING. group status = 'PENDING PRE GROUP' 2. system popup error | |
| 3 | 1 Group in PENDING_TRADE_VALIDATION 2nd Group in PENDING_PRE_GROUP | 1. Group 1, count =2, C1 C2 received and in PENDING TRADE VALIDATION Group 2 count =2, C3,C4 received and in PENDING_PRE_GROUP 2. ops select all and manual STP C1,C2,C3,C4 | 1. C1,C2 status = 'PENDING', group status = 'PENDING TRADE VALIDATION' C3, C4 status = 'PENDING', group status = 'PENDING_PRE_GROUP' 2. C1, C2, C3,C4 status = 'END', group status = 'COMPLETED', bookingSystemEvent = 'ManualDeliver' | |