**Changes **

| SN | Module | Changes | Description |
| --- | --- | --- | --- |
| 1 | ratan-cash-settlement-netting-service | 1. Cron job to scan cashflow candidates and netting | Code change |
| 2 | ratan-cashflow-lifecycle-service | 1. Precheck refactoring, decouple data persistence and attribute stamping. | Code change Lifecycle stamping logic refer to design page: [Cashflow Lifecycle Stamping Logic - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Cashflow+Lifecycle+Stamping+Logic) |
| 3 | ratan-rule-service | 1. Add a new rule to NSTP cashflows has non-NDIRS parent typology and NID exists 2. update existing rule on demand to bypass cashflows has NDIRS parent typology | DB change only |
| 4 | ratan-mxg-cashflow-adaptor | 1. Be able to map NID from MXML to SCBML for downstream processing. | Minor code change |
| 5 | ratan-cash-settlement-orchestration | 1. Add new node after Pre-check | Flow change |

**Data modeling change**

| Logical model | Xpath | Description | Change Flag |
| --- | --- | --- | --- |
| Cashflow.ND_Parent_Trade_Id | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:NDParentTradeId | NID | Internal Adding |
| Cashflow.ND_Parent_Typology | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:NDParentTradeTypology | ND parent trade typology | Internal Adding |