CR：CHG0454259

AIG：

## Release Work Item:

[Release 3722043: CHG0454259: April 6th CR for CN - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/3722043)

## Packages

| Service | ADO release pipeline | Package Version |
| --- | --- | --- |
| 51358-ratan-cash-settlement-group-management-service | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1422351&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1422351&view=results) | 1.2.2-20240329.3 |
| 51358-ratan-cash-settlement-ssi-stamping-service | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1436394&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1436394&view=results) | 2.2.1-20240401.4 |
| 51358-ratan-service-properties | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1437843&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1437843&view=results) | 20240401.4 |
| 51358-ratanone-db-repository | NA | CHG0454259_1-20240402.5.zip CHG0454259_Rollback-20240402.6 |
| 51358-mfe-rules | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1447433&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1447433&view=results) | 1.4.0-production-20240402.1 |
| 51358-ratan-mxg-cashflow-adaptor | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1469870&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=1469870&view=results) | 1.6.6-20240403.4 |

| No | **Type** | **ADO** | Impact Scope | Critical Level | Issuer | Background | **Business Benefit** | **Technical Benefit** | UAT sign off | QA Sign off | **Package** | Status (QA/Pending Signoff/Ready) | Assignee |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Enhancement | 3721993 | Group message inbound | Medium | Dev | Group service is required to add a filter to accept cashflows with valid status only | | | | | 51358-ratan-cash-settlement-group-management-service | | @Xinmiao Huang |
| 2 | Enhancement | 3605375 | FX status write back | High | User | FX status write back change the matching condition which should remove CCY | | | | | 51358-ratan-cash-settlement-group-management-service | | @Xinmiao Huang |
| 2 | Bug Fix | 3734240 | SSI Refresh | High | Dev | Vostro refresh typo change incorrectly impact SSI event handling error. | | | | | 51358-ratan-cash-settlement-ssi-stamping-service | | @Xinmiao Huang |
| 3 | Bug Fix | 3346329 | Lifecycle domain event subscriber | Low | Dev | queue capacity change in thread pool, only properties change. | | | | | 51358-ratan-service-properties | | @Xinmiao Huang |
| 4 | Feature | - | Rule | Low | User | Group historical data update | | | | | 51358-ratanone-db-repository | | @Xinmiao Huang |
| 5 | Bug Fix | 3727035 | Rule | Low | Dev | Fix useless rule builder in special rule config | | | | | 51358-mfe-rules | | @Shuai Lu |
| 6 | Bug Fix | 3781853 | adaptor | Medium | Dev | Murex OLA break for Ack message | | | | | 51358-ratan-mxg-cashflow-adaptor | | @Chen Yang |