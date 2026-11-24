## Problem statement

1. There is a concern from user that without bulk processing, it will impact **efficient** for user to use RATAN ONE.
2. There is **considerable time** spent by the team to process cashflows one by one, especially when there is high volume
3. Having Bulk Processing capability allows users to process multiple cashflows at the same time
4. There are built in controls to reduce the risk of manual errors: 1. Allowed only on same Value Date + Booking Entity + Counterparty 2. Allowed only on white listed exceptions

## Solutioning

1. Allow user to define NSTP exception is bulk eligible or not, as part of rule maintenance, through business rule profile (FMO_BR_APR & FMO_BR_MKR). 1. If there is NOT eligible exception in the payment, this payment will be taken as not eligible for bulk
2. Control build to reduce operation risk, as it only allow cashflow on same **Value Date + Booking Entity + Counterparty **to be bulk processed.
3. Build preview page before bulk submit/approve 1. This page will be loaded when user performs bulk submit/approve 2. System will compare cashflow exception with latest rule config. 3. **Eligible exception can be self-manageable, which is a self service.** 4. As a result, cashflow will be segregated into different section 'eligible' or 'not eligible' .
4. Bulk Eligible Fix 1. In eligible cashflow section, RATAN has flexibility to **select all or partially select cashflow for processing**. 2. If selected cashflow contains 'pending affirmation' exception, **user needs to manually fill in affirmation details**, which would be only applied to pending affirmation cashflow. 3. No action allowed for 'not eligible' section.
5. **Bulk processing result will be reflected real-time**, once user click on submit/approve/reject as maker-checker process.

**EXPAND: Bulk Eligible Exception**

| **Bulk processing allow** | **Bulk processing not allowed** |
| --- | --- |
| Adhoc Netting Client | DVP |
| Adhoc Netting FMCODE | Manual Deliver |
| Adhoc Netting FMID | AmendmentError |
| Adhoc_Netting | Portfolio reassignment |
| Bad Business Day | CCS: Check Validation Status |
| CHINA FDL Client | ReInstate |
| China Precious Metal | Previously Netted |
| CORP Client | NetOverAmend |
| GSAM Client | Withdrawal on component |
| India Adhoc Netting | Murex 2.11 Strategy CCS_DVP |
| India SCF | Murex 2.11 Strategy PAR FWD DVP |
| Murex 2.11 CRD CDS product | Reversal |
| Murex 2.11 CRD RTRS product | Rebook |
| Murex COM SWP/FWD | reversal |
| Murex IRS | Rebook |
| Net Cashflow | DVP Strategy |
| Pending Affirmation | LEI VA |
| Settled as gross | Back Value Date |
| Structure Trade | Stella_Corp_CCS |
| WHT Clients | Missing Vostro |
| WHT FMCODE | Missing Nostro |
| Secondary Vostro | Multiple Vostro |
| | High Value Payment |
| | NSTP |
| | Above Threshold |
| | Murex STP_HOLD |
| | CCY NSTP |
| | Murex SLT |
| | CS Linked IRS |
| | NDS Fixing |
| | INO IRS |
| | XAU |
| | FI Client - PoU Check |
| | Multi SSI |

**EXPAND_END**

## Demo Cases

| | Item | Scenario | Steps | Expected Behavior | Ready for Testing |
| --- | --- | --- | --- | --- | --- |
| 1 | NSTP exception configuration | Bulk Eligible configuration | 1. Go to NSTP Rule Tile 2. Open one sample rule and check the bulk eligible config | | |
| 2 | Precheck Control | Same Entity+ Same Counterparty + Same Value Date | 1. Go to Cashflow Blotter 2. Select predefined maker view 3. Select all cashflow, right click | Can see Bulk Submit Button | |
| 3 | | Different Entity + Same Counterparty + Same Value Date | Continue with Case 2 1. add another cashflow with different entity | Can see Bulk Submit Button, but show alert after click | |
| 4 | Bulk Preview | Eligible Cashflow + Not Eligible Cashflow | Continue with Case 2 1. Click bulk Submit Button 2. Introduce Bulk Processing preview: Eligible Section and nonEligible Section 3. Select cashflow with pending affirmation exceptions 4. Introduce Select all and partially select function | Take a look on bulk processing preview | |
| 5 | Bulk Submit | Eligible Cashflow + Pending Affirmation | Continue with Case 4 1. Select certain cashflow with pending affirmation exception 2. Fill in affirmation details 3. Submit | After Submit, Window auto closed. Process result will be popped out. Click on process result, can show detail Cashflow status auto refreshed. | |
| 6 | Bulk Approve | Eligible Cashflow + Pending Affirmation | Continue with Case 5 1. Select same data set with maker, with extra cashflow(checker only exception & case 6 cashflow) 2. Someone else can submit 1 cashflow offline, to demo partially success case 3. Click on Approve | 1. Can see eligible cashflow number difference 2. Can see maker bulk filled in affirmation only apply for case 5 cashflow 3. Demo partially success case. 4. After Approve, Window auto closed. Process result will be popped out. Cashflow status auto refreshed. | |
| 7 | Single Submit | Pending Affirmation | 1. Pick one cashflow with pending affirmation exception 2. Fill in different affirmation info and submit | Simulate scenario where cashflow is left over, but still can be single processed. | |