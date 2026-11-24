#

# Background

User is expecting to distribute the payment message to different queue in FMSGW according to payment amount threshold which will require different level of approval to process. To support the process, Ratan is expected to send extra info to FMSGW.

# Requirement Details

### BCS cashflow

| Requirement | FMRP Solution | BCS Solution | Comments |
| --- | --- | --- | --- |
| Display 'High Value' exception in Cashflow detail | Already in BAU | Will not be built | |
| View 'USD' equivalent in the Cashflow Blotter | New field will be added in the cashflow blotter, but solution should not rely on users creating custom filters | Will not be build | |
| Ability to view filter options based on different cashflow thresholds | New field will be added in the cashflow blotter | Will not be built | |
| Apply Authorization Limits for Checker Actions | Already in BAU | 1. Authorize limit build will leverage FMRP existing static – static blotter & limit 1. NSTP Checker Approval ![image-2026-8-11_10-5-52.png](attachments/image-2026-8-11_10-5-52.png) | |
| | - Cashflow Affirmation - add auth limit check for single level "update affirmation status" for the initial release (scheduled in Sep) ![image-2026-8-11_10-1-53.png](attachments/image-2026-8-11_10-1-53.png) | |
| NA to FMRP | - Failed Cashflow Release - 1. ~~remove release failed cashflow option (OPS is using this in BAU)~~ 2. add the profile limt for checker approval ![image-2026-8-11_10-1-11.png](attachments/image-2026-8-11_10-1-11.png) | |
| Send STP/NSTP Flag to FMSGW | STP/NSTP flag – all user actions except add comment will be considered as NSTP | Same as FMRP, send to Razor | |
| Send Last Checker FMID to FMSGW | - Send last Checker PSID for all actions where there is maker+checker. - Send Maker PSID for all actions where there is single level (example: Affirmation) | Same as FMRP, send to Razor | |

1. Need to guarantee enough backup for BCS OPS -- [@Dinesh, Arockia](mailto:K.A.Dinesh@sc.com) to share the BCS OPS details - completed.

### FMRP/LOANIQ cashflow

1. RATAN must display the USD equivalent of each cashflow in the cashflow blotter
2. RATAN must provide ability to filter for USD equivalent amount 1. user is able to find the field in custom filter as an additional condition based on existing mandatory query condition. 2. user is able to filter the value in cashflow blotter.
3. RATAN must send STP / NSTP information to FMSGW. Need to add 2 fields to Swift message header: (confirmed with FMSGW in **** 1. **stpFlag**: Y for STP, and N for NSTP 1. NSTP: all manual touch action except "Add Comment" will be treated as NSTP 2. **lastUser**: user bank ID , leave blank if stpFlag is Y
4. RATAN must send the last Checker PSID to FMSGW 1. user id linked to the last manual action,
5. RATAN Profiles must be amended as below, need to update user profile together when release the change to prod 1. ~~need to confirm the impacted user list, dev will extract current live user list and PO @Deepak K will confirm the to-be profile~~

| **Profile** | **Current Limit** | **TOBE Limit (USD)** | **Remarks** |
| --- | --- | --- | --- |
| FMO_OPS_BOC | < 30 Million | <30 Million | |
| FMO_OPS_BO | < 100 Million | < 100 Million | |
| FMO_OPS_BOS | < 300 Million | < 500 Million | Change to 500 Million |
| FMO_OPS_BOL | < 1 Billion | < 1 Billion | |
| FMO_OPS_BOM | < 4 Billion | < 4 Billion | |
| ~~FMO_OPS_BOSM~~ | | ~~< 4 Billion~~ | ~~New Profile (band4), same view access as FMO_OPS_BOM~~ ~~to be confirmed if this still required~~ |

# User actions

**EXPAND: FMRP user actions**

| FMRP FLow |
| --- |
| Menu Item | Maker/Checker action? | Action in History | lastChecker | StpFlag (true STP) |
| Early Materialization | maker | Materialize | use maker id as the checker | N |
| ReInstate | maker | ReInstate | | N |
| Settle As Gross | maker | SettleAsGross | | N |
| Status Write Back | maker | ReplayStatusWriteBack | | N |
| Regenerate Swift | maker | ReGenerateSwift | | N |
| Resend To Razor | maker | ResendToRazor | | N |
| Early Release | maker | EarlyRelease | | N |
| Update Affirmation | maker | ManualAffirmed | use maker id as the checker | N |
| Swift Suppression | maker | ManualSwiftSuppress | | N |
| Verify Swift Suppression | checker | Approve | | N |
| Undo Swift Suppression | maker | ManualSwiftUnSuppress | | N |
| Verify Undo Swift Suppression | checker | Approve | | N |
| Suppress Cashflow | maker | ManualSuppress | | N |
| Confirm Suppression | checker | Approve | | N |
| Un-Suppress Cashflow | maker | ManualUnSuppress | | N |
| Confirm Un-Suppression | checker | Approve | checker id | N |
| Manual Fail | maker | Fail | | N |
| Confirm Manual Fail | checker | Approve | | N |
| BIC Net Selected Cashflow | maker | Net (for component cashflow) NetNew (for resultant cashflow) | | N |
| CCIL Net Selected Cashflow | maker | Net (for component cashflow) NetNew (for resultant cashflow) | | N |
| Net Selected Cashflow | maker | Net (for component cashflow) NetNew (for resultant cashflow) | | N |
| Un-Net Cashflow | maker | UnNet | | N |
| Hold | maker | Hold | | N |
| Unhold | maker | UnHold | | N |
| Send To WAITING | maker | ReInstate | | N |
| ~~View Swift Message~~ | NA | NA | | NA |
| ~~Manual Settle~~ | NA | NA | | NA |
| Bulk Submit | maker | Submit | | N |
| Bulk Approve | checker | Approve | | N |
| Split Cashflow | maker | Split (for parent cashflow) SplitNew(for child cashflow) | | N |
| Amend Split Amount | maker | Amendment | | N |
| Un-Split Cashflow | maker | UnSplit | ** ** | N |
| ~~Settlement Method Update~~ | maker | NA | | N |
| Comment | **NA** | ** **Comment | ** ** | **Y** |
| ~~adhoc SSI~~ | maker | NA | ** ** | **N** |
| Submit | maker | Submit | ** ** | **N** |
| Approve | checker | Approve | ** ** | **N** |

**EXPAND_END**

**EXPAND: BCS User Actions**

| BCS FLow |
| --- |
| Menu Name | Maker/Checker action? | lastChecker | StpFlag (true STP) |
| Reinstate | maker | | N |
| **Update Affirmation Status** | maker | **use maker id as the checker** | N |
| Net Selected Cashflow | maker | | N |
| Un-Net Cashflow | maker | | N |
| Verify Un-Net Cashflow | checker | checker id | N |
| Adhoc SSI Input - Maker | maker | | N |
| Adhoc SSI Input - Checker | checker | checker id | N |
| Release Cashflow | maker | | N |
| Confirm Release > Accept Release | checker | checker id | N |
| Confirm Release > Reject Release | checker | | N |
| Release Failed Cashflow > Set Value Date to Deal Value Date | maker | | N |
| Release Failed Cashflow > Set Value Date to Current System Date | maker | | N |
| Confirm Release Failed Cashflow > Accept Deal Value Date | checker | checker id | N |
| Confirm Release Failed Cashflow > Confirm Current System Date | checker | checker id | N |
| Confirm Release Failed Cashflow > Reject Release | checker | | N |
| Add Comment | maker | | Y |
| Suppress Cashflow | maker | | N |
| Confirm Suppression > Accept Suppression | checker | | N |
| Confirm Suppression > Reject Suppression | checker | | N |
| Un-Suppress Cashflow | maker | | N |
| Manual Fail | maker | | N |

**EXPAND_END**

# Open Questions

| | Description | Comment | | State |
| --- | --- | --- | --- | --- |
| 1 | Should BCS/LOANIQ/Korea(ENSIS) cashflow be exclude from the change scope - BCS is legacy flow, need much more effort - LOANIQ is part of FMRP flow, technically Ratan can support, need align the solution with Razor - murex →RATAN ->ENSIS MX flow, if required, need murex send the additional info, and ENSIS to support the process - future flow if Korea cashflow migrated to Ratan and follow the FMRP flow, technically Ratan can support, need ENSIS to support the process | need further confirmation from PO @Deepak K @Arockia Dinesh Confirmed BCS/LOANIQ/FMRP are in scope, Korea ENSIS flow is out of scope | | |
| 2 | Should auto split child cashflow be considered as STP? | Confirmed need to derive the STP/NSTP info from parent cashflow for the auto distribution scenario. | | |
| 3 | will FMO_OPS_BOSM still required or reuse the existing profile? | @Deepak K confirmed no need to create new profile in RATAN, only to update the auth limit for FMO_OPS_BOS | | |
| 4 | the definition of **stpFlag **and **lastUser** | @Arockia Dinesh to confirm 2026-08-25 Confirmed in meeting, mail attached | 📎 [RE_ Review RATAN Actions for HVP StpFlag.msg](attachments/RE_ Review RATAN Actions for HVP StpFlag.msg) | |
| 5 | Currently there is no auth limit check for cashflow affirmation, should this be added? - BCS | 2026-08-13 @David George Thomas @Arockia Dinesh confirmed to add auth limit check for BCS affirmation action. FMRP process to be confirmed by PO | | |
| 6 | Currently there is no auth limit check for cashflow affirmation, should this be added? - FMRP | 2026-08-21 to be confirmed by @Anna option 1: remove the update affirmation action from cashflow list option 2: add the limit check when user perform update affirmation action from cashflow list | | |
| 7 | For BCS cashflow, manual net generated netting resultant has no user ID attached to net action. | | | |

# Link

[High Value Payment Control - Razor Development - Confluence](https://confluence.global.standardchartered.com/display/Razor/High+Value+Payment+Control)