# Open Issues

| # | Issue description | **Status** | System | Type | Priority | Test case | Email subject | Ado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 423 | Cashflows VD<effective date are touched in the trade amendment, Cashflow VD>effective date doesn’t generate new cashflow in trade amendment | OPEN | Stella | Defect | Critical | MTC17 | FW: Trade 4330350484 & 4354404271- Amendment information unable to locate in Trade details - MTC17 | [3875467](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/3875467) ETA 23rd Apr |

# Open Actions

| # | Actions | Assignee | Status | Comment |
| --- | --- | --- | --- | --- |
| 1 | Settlement Scenarios | Pradeesh | | |
| 2 | Retest of E2E test cases | Pradeesh | | |
| 3 | Portfolio Reassignment- retest PR following by eco-amend/PR | Pradeesh | | For Tactical solution, Blade should not allow portfolio reassignment to have an effective date (time) different to trade date |
| 4 | Stella Regression Package Review | Lina | | Email from Divya for Olexiy signoff |
| 5 | Refixing (After released) +Expire test | Pradeesh | | Manual refixing done, Auto refixing to be booked, Expired is not processed |
| 6 | HZ duplicate payment issue | | | Email from Divya to be included in regression test package. |
| 7 | Test undo after settled withdrawal FT | Pradeesh | | Cashflow will not be revived if in released/settled/netted/split status Expectation to be discussed? |
| 8 | Ratan Regression test package (undo) review | Lina | | To add a few cases for undo |