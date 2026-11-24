4

**RATAN:**

**FMSGW**:

| [S.no](http://S.no) | Squads | Type/Functions | Test Case/Scenario | Test Steps | Expected Result | Test Result(Pass / Fail/ Blocked/ Descoped) | Test Evidence | Tested By |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FMSGW | Inbound Message | MT103/202COV | Settlement message MT103/202COV received from RATAN and sent to AMH. ACK message is sent back to RATAN. | MT103/202COV is sent to AMH and ACK message is sent back to RATAN. | Pass | ![image-2026-7-14_17-22-42.png](attachments/image-2026-7-14_17-22-42.png) ![image-2026-7-14_17-23-6.png](attachments/image-2026-7-14_17-23-6.png) | Shalini Fonseka |
| MT202 Cov should be released upon MT103 getting ACK successfully. |
| 2 | FMSGW | Inbound Message | MT202 | Settlement message MT202 received from RATAN and sent to AMH. ACK is message is sent back to RATAN. | MT202 is sent to AMH and ACK is message is sent back to RATAN. | Pass | ![image-2026-7-14_17-29-5.png](attachments/image-2026-7-14_17-29-5.png) | Shalini Fonseka |
| 3 | FMSGW | Inbound Message | MT192/292 | Settlement message MT192/292 received from RATAN and sent to AMH. ACK is message is sent back to RATAN. | MT192/292 is sent to AMH and ACK is message is sent back to RATAN. | Pass | ![image-2026-7-14_17-29-54.png](attachments/image-2026-7-14_17-29-54.png) ![image-2026-7-14_17-31-3.png](attachments/image-2026-7-14_17-31-3.png) | Shalini Fonseka |
| 4 | FMSGW | Inbound Message | ANY | Back Value Dated message received from RATAN and listed in Back Valued Messages Queue when processed ACK message is sent to inbound system and notification will be sent | Transaction should be present in Back Valued Messages Queue with Validation Failure details and ACK should be sent to inbound system and notification will be sent | Pass | ![image-2026-7-15_15-56-13.png](attachments/image-2026-7-15_15-56-13.png) ![image-2026-7-15_15-56-57.png](attachments/image-2026-7-15_15-56-57.png) | Shalini Fonseka |
| 6 | FMSGW | Inbound Message | MT103,MT202 | Settlement message hit DEF rule with High Value payment (MT103/MT202) received from RATAN is listed in High value payment Queue once approved then sent to AMH. ACK is message is sent back to RATAN and notification will be sent | MT103/MT202 is sent to AMH and ACK is message is sent back to RATAN and notification will be sent | Pass | ![image-2026-7-15_15-58-48.png](attachments/image-2026-7-15_15-58-48.png) ![image-2026-7-15_15-59-21.png](attachments/image-2026-7-15_15-59-21.png) ![image-2026-7-15_16-0-5.png](attachments/image-2026-7-15_16-0-5.png) ![image-2026-7-15_16-0-33.png](attachments/image-2026-7-15_16-0-33.png) | Shalini Fonseka |
| 7 | FMSGW | Inbound Message | MT103, MT202 | Settlement for Cancel Trade where Original message released | 1. MT202/MT103 is sent to AMH and ACK is message is sent back to RATAN. | Pass | ![image-2026-7-14_17-31-51.png](attachments/image-2026-7-14_17-31-51.png) ![image-2026-7-14_17-33-1.png](attachments/image-2026-7-14_17-33-1.png) | Shalini Fonseka |
| 2. As the trade is cancelled so the transaction will be available in Manual Cancellation Queue, |
| an ACK is sent to inbound system and User is sent notification through email |
| 3. In Manual Cancellation Queue user can further process or terminate the transaction |
| 8 | FMSGW | Validation Queue | MTn92 | Swift Payment message where message type is MTn92 will flow to "Manual Cancellation" queue and User will perform Process action on the payment transaction to next Eligible currency validation check | 1. User should be able to login and should be able to open the queue | Pass | Cash flow is-M00127114523 | |
| 2.Search will display Single or Multiple entries depending on the validation check |
| 3.Detail screen popup window should be opened with tabs - "Data" and "Action audit" |
| 4.User should be able to add comment and Payment transaction should be released for next Eligible currency validation check and it should be disappeared from the Manual cancellation queue. |
| 9 | FMSGW | Duplicate Message | MT103/MT202/ MT202COV | Processing of Duplicate payment message from Duplicate message Queue | 1) Login to Manual Queue -> Navigate to Validation->Duplicate Message Queue and search for the trade in the queue | Pass | Cash flow id-M00127114976 | |
| 2) Perform Process action on the transaction |
| Expectation: |
| 1) Transaction message should be found in Duplicate Message Queue. |
| 2) On Process, Transaction will move to next validations i.e., check for SCB Specific Validations |