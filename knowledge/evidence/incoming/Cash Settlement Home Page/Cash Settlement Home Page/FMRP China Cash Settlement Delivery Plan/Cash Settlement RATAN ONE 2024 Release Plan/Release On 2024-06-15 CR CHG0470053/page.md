CR：CHG0470053

AIG：

## Release Work Item:

[Release 4337197: CN 20240615 release - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/4337197)

## Release Work Story Query:

[Release-CN-20240615 - Boards (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_queries/query/50d03574-1975-4371-8614-e0d32584a6dc/)

Rule UI： [Release On 2024-06-15 CR: CHG0470053[Rule UI] - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3065022432)

## Packages

| Service | ADO release pipeline | Package Version |
| --- | --- | --- |
| 51358-ratan-rule-service | [Pipelines - Run 20240611.5 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2258778&view=results) | [2.0.0-20240611.5](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/ratan/ratan-rule-service/2.0.0-20240611.5/) |
| 51358-mfe-rules | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2191495&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2191495&view=results) | 1.5.0-production-20240605.3 |
| 51358-mfe-ratan-container | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2191487&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2191487&view=results) | 1.7.8-production-20240605.6 |
| 51358-ratanone-message-bridge | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2200836&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2200836&view=results) | 3.1.2-20240606.1 |
| 51358-ratan-service-properties | [Pipelines - Run 20240611.5 (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2259336&view=results) | 20240611.5 |
| 51358-ratanone-rule-service | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2167789&view=results](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=2167789&view=results) | 1.2.2-20240604.3 |

| No | **Type** | **ADO** | Impact Scope | Critical Level | Issuer | Background | **Business Benefit** | **Technical Benefit** | UAT sign off | QA Sign off | **Package** | Status (QA/Pending Signoff/Ready) | Assignee |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Ratan Rule Engine Enhancement | 4461101 4424206 | ratan rule engine | low | dev | 1. enhance special rule control by adding DISABLED status into our rule engine status machine 2. enhance rule update scenario | NA | enhance ratan rule engine status machine | NA | | ratanone-rule-service | | @William Zhang |
| 2 | Migration | 3949924 4004540 | MFE Rule Tiles | Low | dev | 1. Support enhancement for rule engine. 2. Enable supporting for CN rules. | NA | Enhance rule status display | NA | | 51358-mfe-rules | | @Shuai Lu |
| 3 | Migration | 4152418 4180292 4033882 | MFE Rule Tiles | Low | dev | 1. support Current Date variables in rule. | NA | Enhance rule builder | NA | | 51358-mfe-ratan-container | | @Shuai Lu |
| 4 | Migration | 3687777 | ratan-rule-service | High | dev | 1. integrate with ratanone-rule-engine 2. enhance rule check performance 3. Hashicorp integration | NA | enhance rule check performance, Hashicorp integration | NA | | 51358-ratan-rule-service | | @Chongxuan Li |
| 5 | New feature | [2658949](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/2658949) | message bridge | | NA | 1. Message Bridge to add a consumer to support EBBS connection(Another Enterprise Solace VPN 2. Hashicorp integration | Support sending accounting data | Hashicorp integration | 📎 [RE Ratan- EBBS interface UAT signoff.msg](attachments/RE Ratan- EBBS interface UAT signoff.msg) | Pending on the command for dummy feed with headers @Chen Yang 2024-06-11 Lina added 2024-06-12 test passed on dev env. | 51358-ratanone-message-bridge | | @Chen Yang |
| 6 | NSTP Rule | [2080292](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/2080292) | LOANIQ NSTP Rule | Medium | dev | 1. add NSTP rule to hold LOANIQ cashflow which requires netting 2. add NSTP rule to hold LOANIQ cashflow before business go live | LOANIQ business requirement | NA | 📎 [FW_ LoanIQ UAT Signoff.msg](attachments/FW_ LoanIQ UAT Signoff.msg) | [LoanIQ Test Case - SIT] | NA | | @Miki.Huang |
| 7 | Infra | | Infra | Low | dev | failover VIP, zk and redis to wat servers for next week server OS upgrade | NA | move VIP, zk and redis to wat servers | NA | NA | NA | | @Jie Cai |