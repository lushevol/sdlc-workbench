# Status & Action Matrix

- Status Action when it is in Waiting Status

| **Source Status** | **Action** | **Target Status** |
| --- | --- | --- |
| Cashflow Status | Sub Status Type | Sub Status | SSI Exception Type | Action | Cashflow Status | Sub Status Type | Sub Status | SSI Exception Type |
| WAITING | Pending Exception | Pending Operator | NA | Maker Adhoc SSI | WAITING | Pending Exception | Pending Verification | Adhoc SI |
| WAITING | Pending Exception | Pending Verification | NA | Checker Reject | WAITING | Pending Exception | Pending Operator | Adhoc SI |
| WAITING | Pending Exception | Pending Operator | Adhoc SI | Maker Input Adhoc SSI | WAITING | Pending Exception | Pending Verification | Adhoc SI |
| WAITING | Pending Exception | Pending Verification | Adhoc SI | Checker Approve | READY | NA | NA | NA |
| WAITING | Pending Exception | Pending Verification | Adhoc SI | Checker Reject | WAITING | Pending Exception | Pending Operator | Adhoc SI |
| READY | NA | NA | NA | Maker Adhoc SSI | READY | Pending Exception | Pending Verification | Adhoc SI |

- Status Action when it is in Ready Status

| **Source Status** | **Action** | **Target Status** |
| --- | --- | --- |
| Cashflow Status | Sub Status Type | Sub Status | SSI Exception Type | Action | Cashflow Status | Sub Status Type | Sub Status | SSI Exception Type |
| Ready | | | NA | Maker Adhoc SSI | Ready | | | Adhoc SI |
| Ready | Pending Exception | Pending Verification | NA | Checker Reject | Ready | | | |
| Ready | | | Adhoc SI | Maker Input Adhoc SSI | Ready | Pending Exception | Pending Verification | Adhoc SI |
| Ready | Pending Exception | Pending Verification | Adhoc SI | Checker Approve | Ready | | | |
| Ready | Pending Exception | Pending Verification | Adhoc SI | Checker Reject | Ready | | | |