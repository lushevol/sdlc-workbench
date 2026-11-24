# Background

Currently if swift deleted in FMSGW, Ratan will synchronize the swift status while cashflow are still in RELEASED status which is a interim status, so trying to move it to a final status to avoid user unnecessary attention.

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6090337](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6090337)

# Requirement Details

- Update Cashflow status to SETTLED status if received swift status are: - FMSGW Deleted - FMSRE Deleted - Manual Delete - Released by SCPAY - Released by AMH
- For MT103/202 COV message, if both received the status in above list even not the exact same value, also need to set the cashflow state to SETTLED - if 103 received FMSGW Deleted while 202Cov received Manual Delete, set the cashflow state to SETTLED - if 103 received Released by AMH while 202Cov received Manual Delete, set the cashflow state to SETTLED - if 103 received Released by AMH while 202Cov received Released by SCPAY, set the cashflow state to SETTLED

# Open Questions

| | Raised Date | Description | Comment |
| --- | --- | --- | --- |
| 1 | 2025-10-09 | Currently these FMSGW deletion status are not involved in cashflow dashboard filter, what's the business impact without these function? | 2025-10-10 'RELEASED' is a interim status, so trying to move it to a final status to avoid user unnecessary attention |
| 2 | 2025-10-09 | Do we have to set the cashflow status to SWIFT_SUPPRESSED? this may trigger duplicate accounting Should these be moved to Settled status which is in sync with manual settle action | 2025-10-16 confirmed in teams group chat and OK to use settled instead of SWIFT_SUPPRESSED ![image-2025-10-16_16-52-53.png](attachments/image-2025-10-16_16-52-53.png) |
| 3 | 2025-10-22 | MT103/202Cov received deleted response but with different delete status for each message, what's the expectation? | ![image-2025-10-22_10-59-0.png](attachments/image-2025-10-22_10-59-0.png) |

# Business Use Case

| Scenario | Test Steps | Expected result |
| --- | --- | --- |
| Mt103/MT202/MT210/MT202Flip/MT192/MT292 /MT604/MT605/MT692 | 1. cashflow processed in Ratan and swift generated 2. Swift sent to FMSGW and got deleted response | 1. Cashflow moved to Released status 2. Cashflow moved to Settled status and swift status reflect the downstream response |
| MT103/202Cov | 1. cashflow processed in Ratan and swift generated 2. Swift sent to FMSGW and both msg got deleted response | 1. Cashflow moved to Released status 2. Cashflow moved to Settled status and swift status show as Check in FMSGW |
| MT103/202Cov | 1. cashflow processed in Ratan and swift generated 2. Swift sent to FMSGW and one msg got deleted response, the other got error response | 1. Cashflow moved to Released status 2. Cashflow still in Released status and swift status show as Check in FMSGW |
| MT103/202Cov | 1. cashflow processed in Ratan and swift generated 2. Swift sent to FMSGW and one msg got deleted response, the other Released by SCPay | 1. Cashflow moved to Released status 2. Cashflow moved to Settled status and swift status show as Check in FMSGW |

# Note

- The meaning of 'Check in FMSGW' is the situation where the values returned by the two FMSGW message of COV are different.