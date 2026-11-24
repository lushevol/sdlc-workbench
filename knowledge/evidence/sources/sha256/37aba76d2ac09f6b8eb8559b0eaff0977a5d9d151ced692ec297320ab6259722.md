| | Lock Scenario | Feature Flow | Purpose | Lock Key | Services |
| --- | --- | --- | --- | --- | --- |
| 1 | Lock and retry manually | UI features: 1. Suppression (Swift/Cashflow) 2. Netting 3. Fail 4. Reinstate 5. Comment 6. Business exception handling (Submit/Approve) | Manually retry after seeing the alert, which means some other process are handling the cashflow. | Cashflow Id | Cashflow Lifecycle Service |
| 2 | Lock and retry | 1. Workflow consume and process cashflows | Auto retry until succeeded for new cashflow events. | Cashflow Id | 1. Camunda 2. Netting 3. NSTP 4. SSI service 5. Lifecycle |
| 3 | | | Auto retry until succeeded for status update of SWIFT. | Cashflow Id | Swift Service |
| 4 | | | Auto retry until succeeded for status update of Accounting. | Cashflow Id | Accounting Service |
| 5 | | | Auto retry until succeeded for new | Original Trade Id | Adaptor |

| Issue | Date | Details | Solution | Status |
| --- | --- | --- | --- | --- |
| Affirmation exception auto close conflict post netting [Bug 6526173 [Regression] Affirmation Exception Auto close handling issue](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6526173/?view=edit) | 2024-11-26 | N00000007808 ,005785521844,005794428598, 005785521851, 005785521844, 005785521587, 005785521581, 005785521575, 005785521569, 005785521563, 005785521555, 005785521549 1. N00000007808 Failed to be released 2. 005785521844 netted -> tech fail 3. Unnet N00000007808 and 005785521844 wrong ly become DEAD 4. User net the rest 9 payments and settle as N00000007809 5. Manual Draft in OSCAR for 005785521844 "RE: Saudi Ratan SAR 73 mio net payment value today ( Urgent)" | When try moving payment status to READY, check and confirm only when cashflow is in WAITING + Pending Exception | To be released by 2025-01-11 |
| Force Complete conflict vs. Payments of next batch [Bug 6617079 [Regression] Murex Feeding - Cancelled cashflow didn't get auto closed in group pending](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6617079/?view=edit) | 2024-12-04 | Auto STP blocked by the Optimistic log of DB update on handling force complete event and payment of next batch. ![](https://dev.azure.com/sc-ado/777f0ba6-cfdf-4f44-99dd-ae1dc434f5c5/_apis/wit/attachments/f8dcdb31-1b26-4df3-9032-c0b7a8e57cbd?fileName=image.png) | Remove the reentrant lock in Group service after consuming messages from adaptor, ensure force complete msg and payments can be locked with each other. | To be released by 2025-01-11 |
| | | | | |
| | | | | |