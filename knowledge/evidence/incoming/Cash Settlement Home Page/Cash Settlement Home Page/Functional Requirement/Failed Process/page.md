# Background:

When the cashflow is not settled in time, settlement platform need to move the cashflows to 'FAILED' status. Settlement Ops will pay additional attention to the 'FAILED' cashflows and a separate 'Failed Re-Process' flow will be followed to re-process the cashflows.

- ‘FAIELD’ is one of the cashflow main status for below purpose. 1. Highlight the cashflows which are not settled before the due date/time( the cutoff) 2. Ops can explicitly set a new ‘Swift Value Date’ for the swift message generation.
- 'FAILED' can be from the below 2 process: details are captured in **[Scheduled Failed Job/Manual Fail], the back value date cashflow won't be moved to FAILED immediately but waiting for the scheduled job today.** 1. Scheduled Job with pre-defined rules. 2. FM Ops manually move the cashflow to 'FAILED' from cashflow blotter, Maker/Checker required.
- No further actions( e.g. exception handling) can be done on the 'FAILED' cashflow, the only action in Ratan is 'Re-Instate' from Cashflow Blotter. But the new cashflow events from Stella can overwrite the cashflows.
- Dedicated exception 'Re-Instated from Failed' cashflow is defined for the cashflow Re-Instated from 'FAILED'.
- The 'Re-Instated from Failed' exception would be part of multi exception handling, FMO ops need to manually update the '**Swift Value Date**' ( used for swift generation) with below 3 options - Current System Date: This is the latest business day which calculated base on currency calendar, sample cases as below. | Currency | Cashflow Value Date | FAILED Date | User Action Date | System Date | Comment | | --- | --- | --- | --- | --- | --- | | USD | 20th April | 20th April EOD | 21th April(Fri) | 21th April | | | USD | 21th April | 21th April | 22th April(Sat) | 24th April | 22th - Sat 23th - Sun 24th - next working day | | CNY | 21th April | 21th April | 23th April(Sat) | 23th April | 22th - Sat 23th - working day | - Current cashflow value date - Manually select a new date.
- This 'Re-Instated from Failed' exception will be group with the ‘Back value date’ exception as they’re updating the same attributed ‘Swift Value Date’.
- Accounting requirement for ‘FAILED’ cashflow will be as below with the most common user case:

# Function flow

- [Failed Cashflow Accounting](https://confluence.global.standardchartered.com/display/DSP/Failed+Cashflow+Accounting)
- [Failed Re-Process - New Swift Value Date](https://confluence.global.standardchartered.com/display/DSP/Failed+Re-Process+-+New+Swift+Value+Date)
- [Scheduled Failed Job/Manual Fail](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2730027165)