# Requirement:

LIEN:

Confluence Page: [RATAN Cashflow Process with Lien - Function Specs]

ADO Link: [Story 6165570 Assessment on TDSX API latency and performance impact of cashflow processing (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6165570)

PendingFixingFlag:

Confluence Page: [IRS Fix Leg & Floating leg payment handling - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2726685251)

ADO Link: [Story 5967648 Waiting Fixing Flag handling (Jan 25) (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5967648)

Tech Design:  [Fixing flag notification - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Fixing+flag+notification)

# Solution 1:

## High Level Design Diagram:

## Low Level Design Diagram:

# Solution 2:

Comparison:

| | Solution 1 | Solution 2 |
| --- | --- | --- |
| Pros | No change on workflow, LIEN stamping can be together with other attributes stamping as long as target status is QUEUD + NA + NA | Simplify Trade Event Notification logic, there is no re-stamping only case, workflow node change would be reuse in the future. |
| Cons | Trade Event notification is more complicated, | |

| SN | Breakpoint | LIEN Stamping/Re-stamping Action | Next Status |
| --- | --- | --- | --- |
| 1 | PROJECTED | Auto Materialize | QUEUED |
| 2 | QUEUED + TechFail | Reinstate | QUEUED |
| 3 | WAITING + Pending Netting | Net/RevertToQueued | NETTED/QUEUED |
| | WAITING + Pending AnotherLeg | Net/RevertToQueued | NETTED/QUEUED |
| 4 | WAITING + Pending Fixing | ?? | ?? |
| 5 | WAITING + Pending Exception | RevertToQueued | QUEUED/Ready |
| 6 | CASHFLOW_SUPPRESSED | UnSuppress | QUEUED |
| 7 | SWIFT_SUPPRESSED | ManualSwiftUnSuppress/Approve | QUEUED |
| 8 | READY+NA+NA | RevertToQueued | QUEUED |
| 9 | NETTED | UnNet | QUEUED |
| 10 | HOLD | UnHold | Nil(status roll back) |
| ~~11~~ | ~~CANCELLED~~ | | |
| ~~12~~ | ~~DEAD~~ | | |

**Changes **

| SN | Module | Changes | Description |
| --- | --- | --- | --- |
| 1 | ratan-cash-settlement-netting-service | 1. Resultant generation should pick LIEN amount field from component 2. Query LIEN amount for each component before generate resultant to get latest LIEN amount | Code change |
| 2 | ratan-cashflow-lifecycle-service | 1. Precheck api change, cover New event unnet withdrawal component. 2. Status update change: try to restamping as long as target status is QUEUED 3. Reuse existing connection with DA to query trade LIEN amount and stamp to cashflow SCBML | Code change Lifecycle stamping logic refer to design page: [Cashflow Lifecycle Stamping Logic - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Cashflow+Lifecycle+Stamping+Logic) |
| 3 | ratan-rule-service | 1. Add a new rule to NSTP cashflows with LIEN amount and generate LIEN on trades exceptions | DB change or user cover? |

**Data modeling change**

| Logical model | Xpath | Description | Change Flag |
| --- | --- | --- | --- |
| | | | |
| | | | |