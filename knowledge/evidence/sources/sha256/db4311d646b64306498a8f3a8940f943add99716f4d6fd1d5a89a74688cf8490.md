# Background

Currently user is only able to select unhold action if the cashflow is in HOLD statue. For some cases, cashflow were put in HOLD before cut off, user unhold it after cutoff it may directly STP to downstream which not allow user to update SSI or suppress the cashflow if needed.

# Available actions with cashflow 'HOLD' status

| | | User profile | Comment |
| --- | --- | --- | --- |
| Unhold (send to previous status) | revert back to the previous status before HOLD | | |
| **Send to WAITING** | **resend the cashflow back to main flow and will be hold in WAITING status with "<u>*Reinstate*</u>" exception** | ** ** | |

**User Access**:

- user profile is the same as HOLD action
- user who performed hold is not allowed to select "Unhold", but allow to select "Send to Waiting"
- cashflow amount limit - unhold will check this, apply the same as reinstate: no need to check amount limitation

**UI Change**:

- add tooltip for "Unhold" menu item: Unhold action will send cashflow to previous status(QUEUED/WAITING/READY)
- add i icon in the Unhold popup: Unhold action will send cashflow to previous status(QUEUED/WAITING/READY)
- Add Warning Message in the Unhold popup: Warning: Unhold action can auto release payment to downstream
- after user select ""Send to Waiting", display popup as below, comment is mandatory.
- Action in history list will be "Reinstate"

![image-2025-6-18_10-28-4.png](attachments/image-2025-6-18_10-28-4.png)![image-2025-6-24_14-37-26.png](attachments/image-2025-6-24_14-37-26.png)

# Business User Case

| | AC-No | Function | Scenario | Expected Result |
| --- | --- | --- | --- | --- |
| 1 | | Unhold action | 1. book cashflow STP to READY status, current time < release cut off 2. user hold the cashflow 3. user unhold the cashflow 4. trigger the release cutoff job | 1. cashflow state ='READY', cashflow sub state type = 'NA' 2. cashflow state ='HOLD' 3. cashflow state ='READY' 4. cashflow state = RELEASED/SETTLED |
| 2 | | Send to WAITING + Adhoc SSI | 1. book cashflow STP to READY status, current time < release cut off 2. user hold the cashflow 3. user select "Send to WAITING" action 4. user perform adhoc SSI and release the cashflow | 1. cashflow state ='READY', cashflow sub state type = 'NA' 2. cashflow state ='HOLD' 3. cashflow state ='WAITING' with "Reinstate" exception 4. cashflow SSI updated and cashflow state = RELEASED/SETTLED |
| 3 | | Send to WAITING + cashflow suppress | 1. book cashflow STP to READY status, current time < release cut off 2. user hold the cashflow 3. user select "Send to WAITING" action 4. user perform cashflow suppress | 1. cashflow state ='READY', cashflow sub state type = 'NA' 2. cashflow state ='HOLD' 3. cashflow state ='WAITING' with "Reinstate" exception 4. cashflow state = CASHFLOW_SUPPRESSED |
| 4 | | Send to WAITING + swift suppress | 1. book cashflow STP to READY status, current time < release cut off 2. user hold the cashflow 3. user select "Send to WAITING" action 4. user perform cashflow suppress | 1. cashflow state ='READY', cashflow sub state type = 'NA' 2. cashflow state ='HOLD' 3. cashflow state ='WAITING' with "Reinstate" exception 4. cashflow state = SWIFT_SUPPRESSED |
| 5 | | Send to WAITING + Net | 1. book cashflow STP to READY status, current time < release cut off 2. user hold the cashflow 3. user select "Send to WAITING" action 4. user perform net | 1. cashflow state ='READY', cashflow sub state type = 'NA' 2. cashflow state ='HOLD' 3. cashflow state ='WAITING' with "Reinstate" exception 4. cashflow state = NETTED |

# Links

[Hold/UnHold]