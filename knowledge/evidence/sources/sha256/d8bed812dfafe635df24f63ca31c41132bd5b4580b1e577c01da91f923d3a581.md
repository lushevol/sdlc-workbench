**Requirement**

- High Value exception must be triggered only if there are exceptions which require a manual action by Checker
- If there are no other exceptions, then High Value exception should not be triggered and STPd
- If there was an exception previously which got auto resolved (example: Confirmation Match resolving 'Pending Affirmation' exception) system must auto remove the High Value Exception so that the cashflow can STP
- For pending affirmation exception, If manually affirmed, then high value exception still visible to checker; if auto affirmed, then high value exception will not be visible to checker.
- High value exception should be triggered as long as there is at least one other exception that requires checker action

**When Exception Generated:**

| # | Scenario | High Value Exception |
| --- | --- | --- |
| 1 | High Value Exception Only | Not Triggered |
| 2 | High Value Exception + Checker exception | Triggered |
| 3 | High Value Exception + Maker only Exception | Triggered |

**When any Exception Resolved:**

| # | High Value + Other Exception Scenario | Expected System Behavior for High Value Exception | Example |
| --- | --- | --- | --- |
| 1 | Maker only Exception | If manually resolved, then still visible to checker; If auto resolved, If no other checker exception (other than high value exception), then auto resolve. Else Still visible to checker. | Pending Affirmation + High Value when manual affirm, checker can see High Value when auto affirm, checker can see cashflow STPed Pending Affirmation + Missing Vostro + High Value when manual affirm, checker can see Missing Vostro + High Value when auto affirm, checker can see Missing Vostro + High Value |
| 2 | Exception Auto Resolved | If no other checker exception (other than high value exception) /pending affirmation exception, then auto resolve. Else Still visible to checker. | Missing Nostro + Net Cashflow + High Value when Missing Nostro auto resolved, check can see Net Cashflow + High Value Missing Nostro + High Value when Missing Nostro auto resolved, checker can see cashflow STPed |
| 3 | Exception Manually Resolved | If maker manually fix exception Still visible to checker If checker manually fix exception All exception closed as multi exception handling | |

**Technical Parameters:**

| # | Business term | Tech Parameter | Sample Value |
| --- | --- | --- | --- |
| 1 | Checker exception | operationLevel in (CHECKER_ONLY, MAKER_CHECKER) | CHECKER_ONLY/MAKER_ONLY/MAKER_CHECKER |
| 2 | Exception Auto/Manually resolved | TBD | |
| | | | |