In the prod version, the Fail action is used for manual fail and schedule job auto fail. when a cashflow is updated by the Fail Action, its status will change to failed.

Based on the bulk fail requirement, the cashflow's status can not change to failed directly by manual fail action. In order to make the fewest code changes, in the manual fail scenario, we still use the Fail Action, but in the schedule job auto fail scenario, we will use AutoFail action.

1、fail and autofail status matchine

| | Source Cashflow Status | Source Cashflow Sub Status | Source Cashflow Sub Status Type | Action | Target Cashflow Status | Target Cashflow Sub Status | Target Cashflow Sub Status Type | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PROJECTED | NA | NA | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 2 | QUEUED | NA | NA | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 3 | QUEUED | NA | Pending Exception | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 4 | WAITING | Pending Operator | Pending Exception | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 5 | WAITING | Pending Verification | Pending Exception | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 6 | WAITING | Pending Operator | Pending Netting | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 7 | WAITING | Pending Verification | Netting Review | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 8 | WAITING | NA | Pending Another Leg | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 9 | WAITING | Pending Verification | Reversal Rebook | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 10 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 11 | READY | NA | NA | **Fail** | WAITING | Pending Verification | Pending Manual Fail | |
| 12 | READY | NA | Pending Ack | Fail | WAITING | Pending Verification | Pending Manual Fail | |
| 13 | HOLD | Pending Verification | NA | **Fail** | WAITING | Pending Verification | Pending Manual Fail | will not happen as it is forbidden to operate in the FE. |
| 14 | ERROR | NA | NA | **Fail** | WAITING | Pending Verification | Pending Manual Fail | will not happen as it is forbidden to operate in the FE. |
| 15 | SWIFT_SUPPRESSED | NA | NA | Fail | WAITING | Pending Verification | Pending Manual Fail | |
| 16 | CASHFLOW_SUPPRESSED | NA | NA | Fail | WAITING | Pending Verification | Pending Manual Fail | |
| 17 | WAITING | Pending Verification | Pending Manual Fail | Approve | FAILED | NA | NA | |
| 18 | WAITING | Pending Verification | Pending Manual Fail | Reject | NA | NA | NA | rollback previous status |
| 19 | PROJECTED | NA | NA | **AutoFail** | FAILED | NA | NA | |
| 20 | QUEUED | NA | NA | **AutoFail** | FAILED | NA | NA | |
| 21 | QUEUED | NA | Pending Exception | **AutoFail** | FAILED | NA | NA | |
| 22 | WAITING | Pending Operator | Pending Exception | **AutoFail** | FAILED | NA | NA | |
| 23 | WAITING | Pending Verification | Pending Exception | **AutoFail** | FAILED | NA | NA | |
| 24 | WAITING | Pending Operator | Pending Netting | **AutoFail** | FAILED | NA | NA | |
| 25 | WAITING | Pending Verification | Netting Review | **AutoFail** | FAILED | NA | NA | |
| 26 | WAITING | NA | Pending Another Leg | **AutoFail** | FAILED | NA | NA | |
| 27 | WAITING | Pending Verification | Reversal Rebook | **AutoFail** | FAILED | NA | NA | |
| 28 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | **AutoFail** | FAILED | NA | NA | |
| 29 | READY | NA | NA | **AutoFail** | FAILED | NA | NA | |
| 30 | READY | NA | Pending Ack | **AutoFail** | FAILED | NA | NA | |
| 31 | NOSTRO_MATCHED | NA | NA | **AutoFail** | FAILED | NA | NA | |
| 32 | HOLD | Pending Verification | NA | **AutoFail** | FAILED | NA | NA | |
| 33 | ERROR | NA | NA | **AutoFail** | FAILED | NA | NA | |
| 34 | SWIFT_SUPPRESSED | NA | NA | **AutoFail** | FAILED | NA | NA | |
| 35 | CASHFLOW_SUPPRESSED | NA | NA | **AutoFail** | FAILED | NA | NA | |

2、api

## API Information

| | Function | URL | Parameters | Response | Notes |
| --- | --- | --- | --- | --- | --- |
| 10 | Manual Fail | [http://uklvadapp1340.uk.dev.net:8453/api](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update)/v1/camunda/task/fail | [ { "cashflowId": "eddie2023022301", "cashflowVersion": 0, "businessVersion": 0, "minorVersion": "2" }, { "cashflowId": "eddie2023022303", "cashflowVersion": 0, "businessVersion": 0, "minorVersion": "2" } ] | { "status": "", "errorCode": "", "errorMessage": "" } | |
| 12 | Swift Suppress Maker | [http://uklvadapp1340.uk.dev.net:8453/api](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update)/v1/ratan/lifecycle/suppress/maker | { "action": "ManualSwiftSuppress", "comment": "123", "cashflows": [ { "cashflowId": "123", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" }, { "cashflowId": "456", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" } ] } | { "status": "", "errorCode": "", "errorMessage": "" } | |
| 13 | Swift Suppress Checker | [http://uklvadapp1340.uk.dev.net:8453/ap](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update)i/v1/ratan/lifecycle/suppress/checker | { "action": "Approve / Reject", "comment": "123", "cashflows": [ { "cashflowId": "123", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" }, { "cashflowId": "456", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" } ] } | { "status": "", "errorCode": "", "errorMessage": "" } | |

## Events