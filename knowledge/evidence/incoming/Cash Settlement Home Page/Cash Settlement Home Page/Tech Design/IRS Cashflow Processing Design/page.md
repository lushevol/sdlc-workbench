Changes

| Module | Changes | Description |
| --- | --- | --- |
| ratan-cash-settlement-orchestration | 1.1 Add a new sub process for IRS as above orchestration aisle. ( Done ) | after 1_2 CloseException&&SuppressionCheck and before 1_3 NettingEligibleCheck |
| ratan-cashflow-lifecycle-servie | 2.1 Provide a new API to query the cashflow is a withdrawal & new cashflow and if it has been released to Razor before ( Pending ) 2.2 Provide a trade query API to query the trade id related cashflows list. ( **Done **) 2.3 Add a new action 'WaitingLeg' to change status from QUEUED to WAITING + PendingAnotherLeg ( Done ) | 1. Query stella message table, if it is a withdrawal & new cashflow, its event is 'Withdrawal_New', 'pre_cashflow_id' not null. Query scbml history table, check if it has been released before |
| ratan-rule-service | 3.1 Provide a new rule type 'IRS' to check if it is IRS product and if netting id is null. (In Progress) | New rule type should not show in GUI drop down list. |
| ratan-cash-settlement-netting-service | 4.1 Provide a API to query it another leg is already in system. (**In Progress**) | Same VD / CCY / Client / TradeId (call 2.2 API to query) and status in Waiting + PendingAnotherLeg, if existing Net both cashflows. Return CamundaApiResponse with SUCCESS if not existing Call status update action refer to 2.3 to change current cashflow to Waiting + PendingAnotherLeg. Return camunda response with 'FILTERED' if any exception Return camunda response with FILTERED. Error message in description |

Critical Test Case

| Case No | | | |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |