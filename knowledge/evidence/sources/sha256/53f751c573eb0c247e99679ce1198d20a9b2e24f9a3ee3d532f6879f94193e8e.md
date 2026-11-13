1. Settlement method amendment where will be done 1. Blade - New profile to be created for Ops 2. Ratan - New event to be triggered to Stella
2. Need capability for FMO to change Settlement Method from Gross to UTIL or vice versa at a trade level 1. Hard Block for FMO users if trade is fully / partially utilized (including one cashflow of the trade or one leg of fx swap)
3. Early Utilization workflow to be created
4. Cancellation Charges workflow (RCS integration for India)
5. Auto Cancellation workflow for Unutilized trades.
6. Time Option workflow.
7. Future cashflows will not have materialized and hence will not be stamped as UTIL - need to stamp UTIL even for forward trades
8. Remaining amount must be visible in same trade ticket in BLADE
9. There is a window period in FXU for forward trades to be utilized if utilized within that window Ratan should move the status to Utilized but the ebbs entry to be passed only on value date.
10. **Need to enable FXU to integrate both Ratan and Razor for single entity which is not available currently.** 1. Ability to identify whether the trade belongs to RAZOR or FMRP and trigger the request to correct system
11. Need to create a single view in Blade itself for the remaining amount for the FO stakeholders
12. Hard Block for Middle Office users
13. Display remaining amount in Blade