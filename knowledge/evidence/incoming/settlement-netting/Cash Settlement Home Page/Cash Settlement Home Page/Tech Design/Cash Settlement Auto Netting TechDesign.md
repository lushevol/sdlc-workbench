Service Change:

Front End

1. Reuse the netting rule blotter. Add a checkbox to indicate if it is a auto netting rule
2. If it's auto netting rule, booking entity, currency, shifter are mandatory fields
3. Shifter support to select hours and mins.
4. PendingAutoNetting status is not allowed to do SettleAsGross
5. Auto Netting resultant cashflow is not allowed to do

![image2024-7-31_13-53-38.png](attachments/image2024-7-31_13-53-38.png)

Static service

provide  a new API to calculate auto netting datetime

create a new static table for query

Example:

| id | booking_entity | home_currency |
| --- | --- | --- |
| 1 | SG | USD |
| 2 | UK | USD |

Ratanone Rule service

1. Add a indicator of isAutoNetting during netting rule creation
2. Support users to update or delete rule.
3. Validation of booking entity, currency, shifter.
4. Duplication check.
5. Support user to add exclusion criteria.
6. Rule check API should return VD+Shifter if hint.

Ratan rule service

1. If hint then call lifecycle status updae API , action is IsAutoNettingEligible, VD+Shifter should be involved in request
2. Add a NSTP rule, If scbml new indicator is SettleAsSingle, then create a "Single Cashflow" Exception.

Lifecycle service

1. Change status update request, add a new parameter, shifter
2. Scbml history table add a new field job_time
3. Add a new action : IsAutoNettingEligible. If action is this then calculate job time by VD + Shifter
4. Add a new action: SettleAsSingle. If action is this then back to QUEUED status.
5. Add a new indicator in scbml. SingleCashflow, xpath should be confirmed. This is for NSTP rule check
6. Add a new API for auto netting job. query cashflow in Waiting+PendingAutoNetting with the same booking entity + ccy + counterparty + valueDate + jobTime.

lock the target cashflows

if  cashflows >1 for each group and current time >= jobTime, then call netting service to net the cashflows in same group

if  cashflows > 1 and current time < jobTime, do nohting

if cashflows ==1 and current time >= jobTime then call status update and action is SettleAsSingle

if  cashflows == 1 and current time < jobTime, do nohting

7. Record job execution result in job table

ControlM

Add  a new job ,  execute every 15mins   0 */15 * * *

Orchestration

1. Add a new flow between 1_4_Netting_Eligible and 1_5_Ssi_Stamping like this

![image2024-7-30_20-3-33.png](attachments/image2024-7-30_20-3-33.png)