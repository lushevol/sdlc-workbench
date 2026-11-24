CR：CHG0363082

AIG：

## Release Work Item:

[Release 2545208: CHG0363082 - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/2545208)

## Packages

| Service | ADO release pipeline |
| --- | --- |
| 51358-mfe-cashflow-blotter | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=648125](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=648125) |
| 51358-ratan-cash-settlement-group-management-service | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=651232](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=651232) |
| 51358-ratan-cashflow-lifecycle-service | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=648125](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=648125) |
| 51358-ratanone-db-repository | CHG0363082-20240116.2 |

| No | **Type** | **ADO** | Impact Scope | Critical Level | Issuer | Background | **Business Benefit** | **Technical Benefit** | UAT sign off | QA Sign off | **Package** | Status (QA/Pending Signoff/Ready) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Enhancement | 2484507 | Cashflow User | Low | Dev | When trade date is null, should not display today. | | | | | 51358-mfe-cashflow-blotter | |
| 2 | Enhancement | 2536439 | query lifecycle | Low | Dev | 1. User manuals deliver all withdrawal messages when all group message not arrive yet. 2. after group ready, the remaining messages are all new, group service was trying to query withdrawal message status but nothing to query. - group service didn't consider this kind of case so when do the response handling, so report an index out of bound error | | | | | 51358-ratan-cash-settlement-group-management-service | |
| 3 | Enhancement | 2320945 | Suppression | Low | Dev | can not unnet the cashflow which is waiting+suppression+Pending_Verification or suppressed | | | | | 51358-ratan-cashflow-lifecycle-service | |
| 4 | Feature | - | Rule | Low | User | Add new rule | | | | | db repo | |