CR：CHG0361089

AIG：

## Release Work Item:

[Release 2645058: CHG0361089 - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/2645058)

## Packages

| Service | ADO release pipeline |
| --- | --- |
| 51358-mfe-cashflow-blotter | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=648125](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=648125) |
| 51358-ratan-cash-settlement-group-management-service | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=651232](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=651232) |
| 51358-ratan-mxg-cashflow-adaptor | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=737278&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=737278&view=results) |

| No | **Type** | **ADO** | Impact Scope | Critical Level | Issuer | Background | **Business Benefit** | **Technical Benefit** | UAT sign off | QA Sign off | **Package** | Status (QA/Pending Signoff/Ready) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Enhancement | 2546119 2546089 | Cashflow User | Low | Dev | a. Swift Message Tab display should be enhanced, 1. when state is Settled or Release, show tab 2. when previous state has Settled or Release, show tab. b. Miss matched exceptions in CN has the same settlement means / account with Nostro inform, but actually it's not. 1. if ssi id is present, vostro settlement means/account should fetch from vostro candidates by ssi id. | | | | | 51358-mfe-cashflow-blotter | |
| 2 | Enhancement | 2657214 | group-management-service | Low | Dev | [Prod] Non-eco Amend new message didn't tag parent cashflow status | | | | | 51358-ratan-cash-settlement-group-management-service | |
| 3 | Enhancement | 2301665 | mxg-cashflow-adaptor | Low | Dev | remove duplicate released msg to murex | | | | | 51358-ratan-mxg-cashflow-adaptor | |