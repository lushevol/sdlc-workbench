# Scheduled Failed job

- Job schedule frequency: - CN Day 1: Daily job including the weekend & holiday, job scheduled at fixed time prior to Razor accounting EOD ( **TBC the time**). - **Long term strategy: RATAN will move the cashflows to Failed status at different times for each currency, but the Settlement Accounting generation needs to be aligned with Aspire (Aspire will generate trade accounting at a single time across currencies). **
- Cashflows in scope to move to 'FAILED'. - Only specific cashflow status in scope for FAILED process. | Cashflow Status | Can move to Failed? | | --- | --- | | PROJECTED | Y | | QUEUED | Y | | WAITING | Y | | READY | Y | | ONHOLD | Y | | CANCELLED | N | | NETTED | N | | SPLIT | N | | DEAD | N | | SUPPRESSED | N | | PAYMENT SUPPRESSED | N | | RELEASED | N | | SETTLED | N | | NOSTRO MATCHED | N | - Value Date is current system date. - **The Failed cutoff is passed for the Currency : No need to run this rule for CN Day 1, for long term strategy solution will rely on the below static data.**

# 'FAILED' Cutoff Static (per Currency)

- For CN Day 1: Fixed time for a SCB Legal entity, across all currencies
- Long term strategy: | Attributes | Value | | --- | --- | | Currency | CNY/CNO/CNH | | Time | 10:00 am | | Time Zone | GMT | | Entity? | |

# Manual Failed

- FMO can right click on the cashflow from cashflow blotter and perform 'Manual Fail' action.
- Only specific cashflow status in scope for FAILED process.. | Cashflow Status | Can move to Failed? | | --- | --- | | PROJECTED | Y | | QUEUED | Y | | WAITING | Y | | READY | Y | | ONHOLD | Y | | CANCELLED | N | | NETTED | N | | SPLIT | N | | DEAD | N | | SUPPRESSED | N | | PAYMENT SUPPRESSED | N | | RELEASED | N | | SETTLED | N | | NOSTRO MATCHED | N |
- Cashflow will move to 'FAILED' status immediately after the user action.

# Post 'FAILED' process