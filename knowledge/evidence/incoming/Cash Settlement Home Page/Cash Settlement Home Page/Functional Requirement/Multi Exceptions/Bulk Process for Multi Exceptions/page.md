## Problem statement

1. There is considerable time spent by the team to process cashflows one by one, especially when there is high volume

## Suggested Operation Process

1. Having Bulk Processing capability allows users to process multiple cashflows at the same time
2. There are built in controls to reduce the risk of manual errors: 1) Allowed only on same Value Date + Booking Entity + Counterparty 2) Allowed only on white listed exceptions

## Solutioning

1. Pending affirmation to be changed to maker/checker.
2. Exception/NSTP can/can't be bulk processed, list should be configurable in NSTP rule.
3. If there is N in the exception configuration, this exception will be taken as not eligible for bulk **EXPAND: Exception List** | **Bulk processing allow ** | Updated json script | **Bulk processing not allowed** | Updated json script | | --- | --- | --- | --- | | | | | | | Adhoc Netting Client | Yes | DVP | Yes | | Adhoc Netting FMCODE | Yes | Manual Deliver | Yes | | Adhoc Netting FMID | Yes | AmendmentError | Yes | | Adhoc_Netting | Yes | Portfolio reassignment | Yes | | Bad Business Day | Yes | CCS: Check Validation Status | Yes | | CHINA FDL Client | Yes | ReInstate | Yes | | China Precious Metal | Yes | Previously Netted | Yes | | CORP Client | Yes | NetOverAmend | Yes | | GSAM Client | Yes | Withdrawal on component | Yes | | India Adhoc Netting | Yes | Murex 2.11 Strategy CCS_DVP | Yes | | India SCF | Yes | Murex 2.11 Strategy PAR FWD DVP | Yes | | Murex 2.11 CRD CDS product | Yes | Reversal | Yes | | Murex 2.11 CRD RTRS product | Yes | Rebook | Yes | | Murex COM SWP/FWD | Yes | reversal | Yes | | Murex IRS | Yes | Rebook | Yes | | Net Cashflow | Yes | DVP Strategy | Yes | | Pending Affirmation | Yes | LEI required | Yes | | Settled as gross | Yes | Back Value Date | Yes | | Structure Trade | Yes | Stella_Corp_CCS | Yes | | WHT Clients | Yes | Missing Vostro | NA | | WHT FMCODE | Yes | Missing Nostro | NA | | Secondary Vostro | NA | Multiple Vostro | NA | | | | High Value Payment | Yes | **EXPAND_END** ![MicrosoftTeams-image.png](attachments/MicrosoftTeams-image.png)
4. Cashflow Multi-selection: a. Control for same counterparty/booking entity/value date. ->If not the same, disable the bulk. b. Bulk Submit will be available if cashflow in WAITING - pending operator; c. Bulk Approve will be available if cashflow in WAITING -pending verification d. Bulk Approve/Submit will only appear when cashflow sub state are all in Pending Operator/Pending Verification.

![image2024-7-17_10-55-14.png](attachments/image2024-7-17_10-55-14.png)

4. Bulk Submit Preview:
   a. Exception summary
   b. Cashflow summary (Trade ID, Cashflow ID, Counterparty, Entity, Currency, Amount, Value Date, Pay/Receive, Exception)
   c. Not eligible exception summary
   d. Not eligible cashflow detail
   e. Affirmation details

![image2024-5-20_11-48-31.png](attachments/image2024-5-20_11-48-31.png)

5. Bulk Approve Preview:
   a. Exception summary
   b. Cashflow summary (Trade ID, Cashflow ID, Counterparty, Entity, Currency, Amount, Value Date, Pay/Receive, Affirmation Email ID, Exception)
   c. Not eligible exception summary
   d. Not eligible cashflow detail
   e. Affirmation Email ID

![image2024-5-20_11-48-53.png](attachments/image2024-5-20_11-48-53.png)

6. Bulk Submit:
   a. Process result

![image2024-5-20_11-38-25.png](attachments/image2024-5-20_11-38-25.png)

## Potential Limitation or Constrains

## User Story

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/2298013](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/2298013)

## Tech Design

[https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3048144376](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3048144376)