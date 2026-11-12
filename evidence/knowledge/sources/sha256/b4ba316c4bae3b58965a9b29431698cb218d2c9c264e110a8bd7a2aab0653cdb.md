# 1.[ Requirements](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3556617786#SelfServicenewbranch/entityonboardingDesign-2.Requirements)

[  Inter Entity Netting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Inter+Entity+Netting)

# 2. Design Details

There are 2 nodes which have code changes in the cashflow process .

**1. Cashflow Enrichment：**

set *USD Transfered Amount into cashflow *

**2. Auto Netting Job:**

**Samples:**

| CashflowId | Entity FMID | Direction | Counterparty FMID | Amount | PreMatchKey | Currency | VD | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 400906330 | Pay | 7 | 100 | 400906330-7-100 | USD | 2026-03-01 | Match |
| 2 | 400906330 | Receive | 7 | 200 | 7-400906330-200 | USD | 2026-03-01 | Match |
| 3 | 400906330 | Receive | 7 | 600 | 7-400906330-600 | USD | 2026-03-01 | Not Match |
| 4 | 7 | Receive | 400906330 | 100 | 400906330-7-100 | USD | 2026-03-01 | Match |
| 5 | 7 | Pay | 400906330 | 200 | 7-400906330-200 | USD | 2026-03-01 | Match |
| 6 | 7 | Pay | 400906330 | 200 | 7-400906330-200 | USD | 2026-03-01 | Not Match |
| 7 | 10075222 | Pay | 400906330 | 200 | 10075222-400906330-200 | USD | 2026-03-01 | Not Match |

| Map Type (according to direction) | PreMatchKey Format | PreMatchKey | CashflowId(Match Result) |
| --- | --- | --- | --- |
| **Pay Map ** | **EntityFMID-CounterPartyFMID-Amount** | 400906330-7-100 | 1 (match) |
| 7-400906330-200 | 5 (match) 6 (not match) |
| 10075222-400906330-200 | 7 (not match) |
| **Receive Map** | **CounterPartyFMID-EntityFMID-Amount** | 7-400906330-200 | 2 (match) |
| 7-400906330-600 | 3 (not match) |
| 400906330-7-100 | 4 (match) |

# 3. Relevant Service

| service | feature branch | release version |
| --- | --- | --- |
| ratanone-foundation | feature/autonetting-interEntity | |
| ratan-cash-settlement-netting-service | feature/autonetting-interEntity | |
| ratan-cash-settlement-group-management-service | feature/autonetting-interEntity | |
| ratan-rule-service | feature/autonetting-interEntity | |