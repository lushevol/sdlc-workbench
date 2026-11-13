# 1. Requirement View

## 1.1 Requirement Analysis:

[Multi Exceptions]

## 1.2 Workflow Design:

[Multiple Exception Handling Design]

## 1.3 Prototype View

![image2023-2-23_16-40-25.png](attachments/image2023-2-23_16-40-25.png)

# 2. Function Description

**Rule Management:**

1. User is able to configure NSTP rule with self-defined expressions and specify its corresponding exception categories, exception operation level.

2. User is able to add special NSTP rule from a special rule config list which are pre-defined by rule service.

3. NSTP rule creation requires maker create and checker approve to take effect on message, and deletion is also the same

4. When any message inbounded, rule service will check message on each active NSTP rule and publish exceptions to exception platform if match the rule, and it will be visible to the users.

**Exception Management:**

1. Exception has three kinds of operations: maker only, maker checker and checker only.

2. Maker only exception means the exception status is PENDING_OPERATOR originally and change to CLOSED after maker submit successfully.

3. Checker only exception means the exception status is PENDING_VERIFICATION originally and change to CLOSED after checker approve successfully.

3. Differently, maker checker means exception status is PENDING_OPERATOR originally, maker fix will change it to PENDING_VERIFICATION, and then change to CLOSED after checker approve successfully.

4. User can view all exceptions that hit the rule via RATAN GUI and fix them according to the operation level and user role(maker or checker).

5. For some NSTP exceptions such as cashflow affirmation and back value, user input is required and rule service will do the double-blind verification when checker approve exception, after approve successfully, exception will be closed and user input will take effect on SCBML message.

# 3. NSTP Rule Overview and Status

![image2023-3-16_14-0-58.png](attachments/image2023-3-16_14-0-58.png)

## 3.1 Special Rule

| Rule Name | Rule Check Required Data | Rule Check Service Integration | Exception Fix Service Integration |
| --- | --- | --- | --- |
| GSAM Client | Counterparty | DQSL | - |
| Corp Client | Counterparty | DQSL | - |
| Affirmation | Trade | - | Cashflow Lifecycle Service |
| Back Value | Settlement Cutoff Time | Static Data Service | Cashflow Lifecycle Service |
| High Value Payment | FX Spot Rate | Static Data Service | - |
| Bad Business Day | Currency Canlendar | Static Data Service | - |

# 4. Workflow Design

## 4.1 Rule Check

## 4.2 Exception Fix

## 4.3 Exception Reject

## 4.4 Exception Approve

# 5. Status Machine

## 5.1 NSTP Rule

## 5.2 NSTP Exception

# 6. ER Diagram

![image2023-3-2_16-55-19.png](attachments/image2023-3-2_16-55-19.png)

# 7. Class Diagram

![image2023-4-25_10-10-18.png](attachments/image2023-4-25_10-10-18.png)

# 8. Use Case

| Step | Action |
| --- | --- |
| 1 | Rule service will pre-define and enable all rules required by user. |
| 2 | User make action via GUI to add NSTP rule, add confirm, delete, delete confirm NSTP rule |
| 3 | Cashflow inbound, then netting eligible check will use NETTING rule to check and cashflow is un-eligible. |
| 4 | Camunda NSTP check node will trigger the rule check with all enabled rules, generate exceptions if any, and publish to rep. |
| 5 | User query exceptions based on provided cashflow id and version |
| 6 | User fix exceptions which status is pending_operator. For back value date and pending affirmation exception, will provide additional input |
| 7 | User approve exceptions with pending_verification status. For back value date and pending affirmation exception, will provide additional input, exceptions can be closed only if double-blind verification is pass. |