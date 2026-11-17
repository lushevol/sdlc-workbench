# Bulk Right Menu

Conditions show bulk right menu:

1. At least select 2 cashflows
2. All cashflows matches states below could lead to specific action.

| User Profile | Cashflow State | Cashflow Sub State | Cashflow Sub State Type | Action |
| --- | --- | --- | --- | --- |
| Initial | WAITING | Pending Operator | Pending Exception | Bulk Submit |
| Verify | WAITING | Pending Verification | Pending Exception | Bulk Approve |

After click bulk right menu button, will do validation below

| Action | Counterparty | Booking Entity | Payment Date |
| --- | --- | --- | --- |
| Bulk Submit | all selected cashflows should be the same. | all selected cashflows should be the same. | all selected cashflows should be the same. |
| Bulk Approve | all selected cashflows should be the same. | all selected cashflows should be the same. | all selected cashflows should be the same. |

Otherwise, popup error alert without going to bulk preview.

# Bulk Preview

| Case | If eligible for bulk | |
| --- | --- | --- |
| checker stage, and is submitted by current checker. | No | |
| no exceptions for current cashflow sub state | No | |
| contains uneligible exception for current cashflow sub state | No | |
| has high risk exception for current cashflow sub state but no permission | No | |
| When checker making approve, but cashflow auth limits is blocked. | No | |