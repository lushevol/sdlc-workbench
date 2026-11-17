| Document status | Reviewed by business owners Approvals: |
| --- | --- |
| Document owner | Jill Du |
| Product Owner | Dinesh, Arockia |
| Business Owner | K Thirunavukarasu, Cordelia Sumita; Thomas, David George |
| Solution Designer | |
| Developers | Yang3, Chen |
| QA | Ma, Shimeng; Wang, Elena |

# Background

When the cashflow does not reach cashflow "cutoff day" yet, user may want to put the cashflow on hold due to any reason (e.g. user finds some issue or wants to supplement the cashflow/trade info later), but currently there is no such hold/unhold action buttons available on RatanOne. Settlement business users require to add such feature.

# Requirement

- Add HOLD as a new main status
- Hold status to be mapped with sub status ‘Pending Verification’
- Cashflow can be put on hold after any status (unless its RELEASED, NET or SPLIT)
- User permission control: - For Ops profiles: - Hold action is allowed to all users – regardless of profile access - Unhold action is only allowed to BOC, BO, BOL, BOM profiles - For Maker/Checker profiles - Both Maker & Checker can do Hold action - Only Checker is allowed to do Unhold action - Maker ‘FMO_OPS_MKR’ cannot perform Unhold (Unhold button not visible) - Same user who put a cashflow on Hold cannot perform Unhold (Same user id can't do the hold & unhold on the same cashflow) - Authorization limits apply for Unhold action based on Cashflow amount (which is the allowed cashflow amount is set by Ops profile) - No amount limit checking is required for Hold Action, but required for Unhold action - User can Unhold a Cashflow only if the Amount is below their Profile Limit (USD)
- Hold to be retain on new cashflow version in case of Trade amendment
- Action limitation after Hold: - Hold will stop any further processing (like materialization, exceptions checking, SSI stamping etc) - ~~Net resultant Cashflow cannot be Un-netted until Hold is removed~~ - Parent cashflow which was Split cannot be Un-split until Hold is removed
- Unhold will revert to previous status and continue processing from there
- Comments are mandatory for both Hold and Unhold
- Can support Bulk Hold / Bulk Unhold

**Note : **

Due to Derivative Settlement Team being a small team we would like to ensure that the check who approved the unhold can and will be allowed to release cashflows for settlement and generate swift

# Eligible User for Hold Action

- All users, regardless of profile access: e.g. MKR, BOC, BO, BOL, BOM
- Both Maker & Checker can do Hold action

# Eligible User for Unhold Action

- BOC, BO, BOL, BOM
- Only Checker can do Unhold action
- Maker ‘FMO_OPS_MKR’ cannot perform Unhold (Unhold button not visible)

Note: Same user who put on hold cannot do unhold action.

# User Action Matrix

- Hold Cashflow: After Hold action, main status will update to "ON HOLD" , sub status to ‘Pending Verification’
- Unhold Cashflow : After Unhold action, cashflow status will revert back to the previous status before Hold and continue processing from there

| | **HOLD** | **UNHOLD** |
| --- | --- | --- |
| **Source Status ** | **Action on Cashflow** | **Target Status ** | **Action on Cashflow** | **Target Status ** |
| **Cashflow Status** | **Sub Status Type** | **Sub Status** | **Cashflow Status** | **Sub Status Type** | **Sub Status** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| QUEUED | N/A | N/A | Hold | HOLD | Cashflow Hold | Pending Verification | Unhold | QUEUED | N/A | N/A |
| Pending Exception | N/A | Hold | HOLD | Cashflow Hold | Pending Verification | Unhold | QUEUED | Pending Exception | N/A |
| WAITING | Pending Another Leg | Pending Verification | Hold | HOLD | Cashflow Hold | Pending Verification | Unhold | WAITING | Pending Another Leg | Pending Verification |
| Pending Netting | Pending Verification | Hold | HOLD | Cashflow Hold | Pending Verification | Unhold | WAITING | Pending Netting | Pending Verification |
| Pending Exception | Pending Verification/Operator | Hold | HOLD | Cashflow Hold | Pending Verification | Unhold | WAITING | Pending Exception | Pending Verification/Operator |
| Reversal_Rebook | Pending Verification | Hold | HOLD | Cashflow Hold | Pending Verification | Unhold | WAITING | Reversal_Rebook | Pending Verification |
| READY | N/A | N/A | Hold | HOLD | Cashflow Hold | Pending Verification | Unhold | READY | N/A | N/A |

Reference:  [Status Machine - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Status+Machine)

# Available actions with cashflow 'HOLD' status

| Action allowed after 'HOLD' status | Status after action |
| --- | --- |
| Adhoc SSI | 'WAITING' |
| Netting | move to new lifecycle |
| Un-Net | move to new lifecycle |
| Swift Suppression - Maker/Checker | move to End status 'SWIFT SUPPRESSED' |
| Cashflow Suppression - Maker/Checker | move to End status 'CASHFLOW SUPPRESSED' |
| Unhold | revert back to the previous status before HOLD |

# Use Cases

Case 1: Hold/Unhold action by different users

| **User ID** | **Business Event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | New | C101 | New | 1 | WAITING | Pending Another Leg | Pending Verification |
| AAA | Rantan Hold | C101 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| BBB | Ratan Unhold | C101 | Unhold | 3 | WAITING | Pending Another Leg | Pending Verification |

- The above behavior is applicable for all status & sub status in above user action matrix.

Case 2: Hold/Unhold action by same user

| **User ID** | **Business Event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | New | C101 | New | 1 | WAITING | Pending Another Leg | Pending Verification |
| AAA | Rantan Hold | C101 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| AAA | ~~Raran Unhold~~ (Unhold disabled as the same user id with hold action) | | | | | | |

Case 3: No Unhold action allowed if cashflow value day passed

| **Day** | **User ID** | **Business Event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VD-5 | | New | C101 | New | 1 | WAITING | Pending Another Leg | Pending Verification |
| VD-5 | AAA | Ratan Hold | C101 | HOLD | 2 | HOLD | Cashflow Hold | Pending Verification |
| VD EOD | BBB | ~~Ratan Unhold~~ (Unhold disabled as the cashflow status "Failed" is not eligible for unhold ) | C101 | FAIL | 3 | FAILED | | |

Note:

- After failed, cashflow will handled by fail process.
- EOD means before China business hour 7pm.

~~Case 4: Net resultant cashflow cannot be Un-netted until Hold is removed~~

| ~~**User ID**~~ | ~~**Business Event**~~ | ~~**Cashflow ID**~~ | ~~**Cashflow event**~~ | ~~**Cashflow Status**~~ | ~~**Sub Status Type**~~ | ~~**Sub Status**~~ |
| --- | --- | --- | --- | --- | --- | --- |
| | ~~New~~ | ~~C101~~ | ~~New~~ | ~~WAITING~~ | ~~Pending exception ~~ | ~~Pending Verification~~ |
| ~~AAA~~ | ~~Rantan Hold~~ | ~~C101~~ | ~~Hold~~ | ~~HOLD~~ | ~~Cashflow Hold~~ | ~~Pending Verification~~ |
| ~~BBB~~ | ~~Rantan Unhold~~ | ~~C101~~ | ~~Unhold~~ | ~~WAITING~~ | ~~Pending exception ~~ | ~~Pending Verification~~ |
| ~~BBB~~ | ~~UnNet~~ | ~~C101~~ | ~~UnNet~~ | ~~DEAD ~~ | ~~N/A~~ | ~~N/A~~ |

Case 5: Parent cashflow which was Split cannot be Un-split until Hold is removed (to do in 2024)

| **User ID** | **Business Event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | New | C101 | New | 1 | Waiting | Pending exception | Pending Verification |
| AAA | Rantan Hold | C101 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| BBB | Rantan Unhold | C101 | Unhold | 3 | QUEUED | N/A | N/A |
| BBB | Rantan UnSplit | C101 | BBB | 4 | DEAD | N/A | N/A |

Case 6: When trade amendment happens, HOLD status to be retain on new cashflow version

| **Business event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- |
| New | C101 | New | 1 | WAITING | Pending Exception | Pending Verification |
| Rantan Hold | C101 | HOLD | 2 | HOLD | Cashflow Hold | Pending Verification |
| Trade amendment | C101 | Withdrawal (same reference) | 3 | Cancelled | N/A | N/A |
| C102 | New (new reference) | 4 | HOLD | Cashflow Hold | Pending Verification |

Case 7: When trade Withdrawal happens on a HOLD cashflow, new cashflow version flow in and Cashflow event withdrawal is pushed to the cashflow workflow.

- New + Withdrawal Step1: New cashflow(Version 1) is on hold Step 2: Cashflow withdrawal(Version 2) event flow in, cashflow event new(version 1) is moved to inactive. Cashflow event withdrawal is pushed to the cashflow workflow,

| **User ID** | **Business event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | New | C101 | New | 1 | WAITING | Pending Exception | Pending Verification |
| AAA | Rantan Hold | C101 | New | 2 | HOLD | Cashflow Hold | Pending Verification |
| | Withdrawal | C101 | Withdrawal | 3 | CANCELLED | N/A | N/A |

Case 8: Can support Bulk Hold

| **User ID** | **Business event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | New | C101 | New | 1 | WAITING | Pending Another Leg | Pending Verification |
| | New | C102 | New | 1 | WAITING | Pending Netting | Pending Verification |
| | New | C103 | New | 1 | READY | N/A | N/A |
| AAA | Ratan Hold | C101 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| C102 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| C103 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| BBB | Ratan Unhold | C101 | Unhold | 3 | WAITING | Pending Another Leg | Pending Verification |
| CCC | Ratan Unhold | C102 | Unhold | 3 | WAITING | Pending Netting | Pending Verification |
| C103 | Unhold | 3 | READY | N/A | N/A |

Case 9: Can support Bulk Unhold

| **User ID** | **Business event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | New | C101 | New | 1 | WAITING | Pending Another Leg | Pending Verification |
| | New | C102 | New | 1 | WAITING | Pending Netting | Pending Verification |
| | New | C103 | New | 1 | READY | N/A | N/A |
| AAA | Ranatn Hold | C101 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| BBB | Ranatn Hold | C102 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| CCC | Ranatn Hold | C103 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification |
| DDD | Ranatn Unhold | C101 | WAITING | 3 | WAITING | Pending Another Leg | Pending Verification |
| C102 | QUEUED | 3 | WAITING | Pending Netting | Pending Verification |
| C103 | READY | 3 | READY | N/A | N/A |

Case 10: Authorization limits apply for Unhold action based on Cashflow amount (which is the allowed cashflow amount is set by Ops profile)

- No amount limit checking is required for Hold Action, but required for Unhold action
- User can Unhold a Cashflow only if the Amount is below their Profile Limit (USD)

| **User ID** | **Business event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Version (Ratan)** | **Cashflow Status** | **Sub Status Type** | **Sub Status** | **Amount** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | New | C101 | New | 1 | WAITING | Pending Another Leg | Pending Verification | 1000 |
| AAA | Ratan Hold | C101 | Hold | 2 | HOLD | Cashflow Hold | Pending Verification | 1000 |
| BBB (under profile BOC, which allowed operation amount is 100) | ~~Ratan Unhold~~ - Unhold button can be seen by user, - After user press Unhold button, system will auto check the amount limitation of the user profile. - But user cannot proceed to next step if current cashflow amount exceeds user profile's granted operation amount. | | | | | | | |