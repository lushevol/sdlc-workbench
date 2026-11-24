| Target release | Sep. / Nov. |
| --- | --- |
| ADO | [Story 14159448 Murex Pending Fixing Flag integration via solace](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14159448) |
| Document status | DRAFT |
| Document owner | @Xinmiao Huang |
| Designer | @Xinmiao Huang |
| Developers | @Haolin Song |
| QA | |

# Background

Pending fixing flag handling is a functional requirement in Ratan GDC who is consuming the Murex fixing flag batch file from NAS, as cross country NAS is not allowed, the solution is not feasible for Ratan Indonesia. So we need find a way to make it happen.

# Business Requirement

[IRS Fix Leg & Floating leg payment handling - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2726685251)

# Ratan GDC technical Design

[Fixing flag notification - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Fixing+flag+notification)

# Indonesia Data provisioning

# Change Scope

| | Service Name | Change Type | Description |
| --- | --- | --- | --- |
| 1 | batch-service | code change | 1. [GDC take effect]batch file processing add logic 1. Query adaptor API to get FM entity 2. Publish to new Kafka topic if identified as an Indonesia cashflow 2. [ID take effect]consume real time message from Kafka topic and follow existing revert logic |
| 2 | mxg-adaptor | code change | 1. provide API to query cashflow and booking entity fmid |
| 3 | message-bridge | config flow change | 1. [GDC take effect] source Kafka topic target is FM solace topic 2. [ID take effect] source FM solace queue target is Kakfa |
| 4 | | | Solace topic & creation form |