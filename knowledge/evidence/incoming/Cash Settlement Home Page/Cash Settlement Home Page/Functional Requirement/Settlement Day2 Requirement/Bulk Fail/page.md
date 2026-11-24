# Background

Currently user is able to perform manual fail action for single cashflow which will resend the cashflow back to main flow to retrigger the workflow. But if the data volume is higher, it will be time consuming for ops users to process.

# Requirement Details

- Bulk Fail with Maker Checker, **single cashflow manual fail also need maker/checker approval**
- No impact to reinstate action
- User profile allowed for Bulk Fail: the same as current manual fail - FMO_OPS_BOL FMO_OPS_BOC FMO_OPS_BO FMO_OPS_INV FMO_OPS_MKR FMO_OPS_BOS FMO_OPS_BOM
- Menu item and display condition, please refer to [ [User Actions on Cashflow Blotter]] | Menu Item | Sub Menu | In Status | Out Status | | --- | --- | --- | --- | | Manual Fail | | Cashflow state in ("QUEUED", "WAITING", "READY") or (Cashflow state in ("SWIFT_SUPPRESSED", "CASHFLOW_SUPPRESSED") and (Current Date > Payment Date)) Cashflow Sub State Type != "Pending Manual Fail" | Cashflow State = "WAITING" Cashflow Sub State Type = "Pending Manual Fail" Cashflow Sub State ="Pending Verification" | | Confirm Manual Fail | Approve | Cashflow Sub State Type = "Pending Manual Fail" and Cashflow Sub State ="Pending Verification" | Cashflow State = "FAILED" | | Reject | Back to the state before manual fail |
- Maker need to input comment to submit manual fail action ((Comment is mandatory))
- Checker cannot be the same as maker, the "Confirm Manual Fail" menu item will be disabled for the maker with tooltip :"For Cashflow XXX , Maker and checker cannot be the same account" （similar as swift suppression ）
- Checker can approve or reject the action (Comment is mandatory)
- You can select up to 1000 cashflows for bulk fail. If you select more than this limit, an error message will be shown. ![image-2025-6-24_17-17-52.png](attachments/image-2025-6-24_17-17-52.png)![image-2025-6-24_17-34-56.png](attachments/image-2025-6-24_17-34-56.png)![image-2025-10-15_15-44-54.png](attachments/image-2025-10-15_15-44-54.png)

# Business User Case

| AC-No | Function | Scenario | Expected Result |
| --- | --- | --- | --- |
| 1 | single cashflow (WAITING), checker approve | 1. book cashflow and hit NSTP rule 2. maker manual fail the cashflow 3. checker approve manual fail 4. user reinstate the cashflow | 1. cashflow state ='WAITING', cashflow sub state type ='Pending Exception', Cashflow Sub State ="Pending Operator" 2. cashflow state ='WAITING', cashflow sub state type ='Pending Manual Fail', Cashflow Sub State ="Pending Verification" 3. cashflow state ='FAILED', cashflow sub state type ='NA', Cashflow Sub State ="NA" 4. cashflow state ='WAITING', cashflow sub state type ='Pending Exception', Cashflow Sub State ="Pending Operator" |
| 2 | single cashflow(READY), checker reject | 1. book cashflow and move it to READY status (before cutoff) 2. maker manual fail the cashflow 3. checker reject manual fail | 1. cashflow state ='READY', cashflow sub state type ='NA', Cashflow Sub State ="NA" 2. cashflow state ='WAITING', cashflow sub state type ='Pending Manual Fail', Cashflow Sub State ="Pending Verification" 3. cashflow state ='READY', cashflow sub state type ='NA', Cashflow Sub State ="NA" |
| 3 | Bulk Fail, checker approve | 1. book multiple cashflow and move cashflow to different status 2. maker select all above cashflow and manual fail the cashflow 3. checker approve manual fail 4. user reinstate the cashflow | 1. cashflow state in (QUEUED, WAITING, READY, SWIFT_SUPPRESSED, CASHFLOW_SUPPRESSED) 2. cashflow state ='WAITING', cashflow sub state type ='Pending Manual Fail', Cashflow Sub State ="Pending Verification" 3. cashflow state ='FAILED', cashflow sub state type ='NA', Cashflow Sub State ="NA" 4. cashflow resent to main flow and may stay to different status |
| 4 | Bulk Fail, checker reject | 1. book multiple cashflow and move cashflow to different status 2. maker select all above cashflow and manual fail the cashflow 3. checker reject manual fail | 1. cashflow state in (QUEUED, WAITING, READY, SWIFT_SUPPRESSED, CASHFLOW_SUPPRESSED) 2. cashflow state ='WAITING', cashflow sub state type ='Pending Manual Fail', Cashflow Sub State ="Pending Verification" 3. cashflow return to the state before manual fail |