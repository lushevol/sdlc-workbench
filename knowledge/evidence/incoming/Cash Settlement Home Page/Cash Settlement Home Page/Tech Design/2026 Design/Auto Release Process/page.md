1. Simplify Process: To avoid potential conflict between payments, try removing the redundant actions on READY payments to simplify the process.
2. Remove Tactical Control: Remove the tactical control as the strategic solution will resolve the problem
3. Last Mile Control (To be tracked under Market Efficiency): To make the system robust to avoid any possibility of duplicated/wrong payment, a final control is planned before sending the payment out of Ratan to SWIFT network with proper internal recon on payment amount

# **Actions allowed post pending release:**

| | Source Cashflow Status | Source Cashflow SubStatus | Source Cashflow SubStatusType | Action | Target Cashflow Status | Target Cashflow SubStatus | Target Cashflow SubStatusType | OPS operation? | System job? | Control? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | READY | NA | NA | IsNstpChecker | WAITING | PendingVerification | PendingException | | No | , Status Machine Control |
| 2 | READY | NA | NA | IsNstp | WAITING | PendingOperator | PendingException | | No | , Status Machine Control |
| 3 | READY | NA | NA | SentToRazor | READY | NA | PendingAck | No | Yes, Specifically for LOANIQ now | , Release job as expected |
| 4 | READY | NA | NA | GenerateSwift | READY | NA | PendingAck | No | Yes, Withdrawal | , Release job as expected |
| 5 | READY | NA | NA | AutoSplitFail | READY | NA | PendingException | No | Yes | , Release job triggered exception |
| 6 | READY | NA | NA | EarlyRelease | READY | NA | NA | | No | , Status Machine Control |
| 7 | READY | NA | NA | UnNet | DEAD | NA | NA | | Yes, Withdrawal component | , Status Machine Control |
| 8 | READY | NA | NA | UnSplit | DEAD | NA | NA | | Yes, Withdrawal component | , Status Machine Control |
| 9 | READY | NA | NA | ReSplit | DEAD | NA | NA | | | |
| 10 | READY | NA | NA | Hold | HOLD | PendingVerification | NA | | No | , Status Machine Control |
| 11 | READY | NA | NA | ManualSwiftSuppress | WAITING | PendingVerification | SwiftSuppression | | No | , Status Machine Control |
| 12 | READY | NA | NA | Fail | WAITING | PendingVerification | PendingManualFail | | No | , Status Machine Control |
| 13 | READY | NA | NA | Withdrawal | CANCELLED | NA | NA | No | Yes, Withdrawal | , Status Machine Control |
| 14 | READY | NA | NA | FullUtilize | UTILIZED | NA | NA | | No | , Status Machine Control, No Payment generated |
| 15 | READY | NA | NA | PartialUtilize | PARTIALLY_UTILIZED | NA | NA | | No | , Status Machine Control, No Payment generated |
| 16 | READY | NA | NA | AutoUtilize | UTILIZED | NA | NA | No | Yes | , Release job won't take it UTIL payments |
| 17 | READY | NA | NA | Pastdue | PASTDUE | NA | NA | No | Yes | , Release job won't take it UTIL payments |
| 18 | READY | NA | NA | TechFail | QUEUED | NA | PendingException | No | Yes | , Status Machine Control |
| 19 | READY | NA | NA | Net | NETTED | NA | NA | | No | Added by Jan 2026, Only allowed 10 mins before cutoff |
| 20 | READY | NA | NA | RevertToQueued | QUEUED | NA | NA | No | Yes | , Status Machine Control |
| 21 | READY | NA | NA | Split | SPLIT | NA | NA | | Yes | Added by Jan 2026, Only allowed 10 mins before cutoff |
| 22 | READY | NA | NA | AutoFail | FAILED | NA | NA | No | Yes | , Status Machine Control and it won't happen |
| 23 | READY | NA | NA | ManualSuppress | WAITING | PendingVerification | CashflowSuppression | | No | , Status Machine Control |
| 24 | READY | NA | NA | New | QUEUED | NA | NA | No | Yes, Undo | |
| 25 | READY | NA | PendingException | Fail | WAITING | PendingVerification | PendingManualFail | | No | , Status Machine Control |
| 26 | READY | NA | PendingException | AutoFail | FAILED | NA | NA | No | Yes | , Status Machine Control |
| 27 | READY | NA | PendingAck | Release | RELEASED | NA | NA | No | Yes | , Release job as expected on swift generation |
| 28 | READY | NA | PendingAck | SwiftUpdate | READY | NA | PendingAck | No | Yes | , Release job as expected on swift generation |
| 29 | READY | NA | PendingAck | Settle | SETTLED | NA | NA | No | Yes | , Release job as expected on swift generation |
| 30 | READY | NA | PendingAck | ResendToRazor | READY | NA | PendingAck | | No | , Edge case, SWIFT do duplication check |
| 31 | READY | NA | PendingAck | ReGenerateSwift | READY | NA | PendingAck | | No | , Edge case, SWIFT do duplication check |
| 32 | READY | NA | PendingAck | Withdrawal | QUEUED | NA | NA | No | Yes, Withdrawal | , Worst case Status wrongly updated without SWIFT generation. Worth to assess making release job a sync flow. C1, 1, N, READY, Pending Ack → No SWIFT generation as Status write back failure C1, 2, W, QUEUED → WAITING (Reversal) → Expected to be CANCELLED, and the payment nothing can be done but only SUPPRESSED |
| 33 | READY | NA | PendingAck | TechFail | QUEUED | NA | PendingException | No | No | , Defined but redundant transaction |
| 34 | READY | NA | PendingAck | Fail | WAITING | PendingVerification | PendingManualFail | | No | , Status Machine Control |
| 35 | READY | NA | PendingAck | AutoFail | FAILED | NA | NA | No | Yes | , Status Machine Control, only happen when SWIFT generation failure, no concurrency issue |
| 36 | READY | NA | PendingAck | New | QUEUED | NA | NA | No | Yes, Undo | |

# **Diagram**

# **System process**

| Jobs | | Auto release (every 30 mins) | Auto Fail (21:00 GMT) | Auto Materialize (2:00 GMT) | SSI Refresh (adhoc) | Trade Confirmation (adhoc) |
| --- | --- | --- | --- | --- | --- | --- |
| | Scope | READY+NA+NA → Pending Ack | PROJECTED/QUEUED/WAITING/READY→ FAILED | PROJECTED→ WAITING | WAITING ↔ READY | WAITING → (READY) |
| Auto release (every 30 mins) | READY+NA+NA → Pending Ack | - | Yes, but workflow/Swift service control could resolve it Going forward to make job synchronized | NO | Yes, but workflow/Swift service control could resolve it Going forward to make job synchronized | NO |
| Auto Fail (21:00 GMT) | PROJECTED/QUEUED/WAITING/READY→ FAILED | | - | NO | NO | NO |
| Auto Materialize (2:00 GMT) | PROJECTED→ WAITING | - | - | - | NO | NO |
| SSI Refresh (adhoc) | WAITING ↔ READY | - | - | - | - | ?? |
| Trade Confirmation (adhoc) | WAITING → (READY) | - | - | - | - | - |
| User actions | Scope | | | | | |
| Net/Unnet | QUEUED/WAITING/READY → NETTED | Yes, but current control by 10 mins Going forward to make job synchronized | ?? rare | NO | NO | NO |
| Split/Unsplit | QUEUED/WAITING/READY → SPLIT | ?? rare | NO | NO | ?? |
| ManualSuppress/UnSuppress/Approve | PROJECTED/QUEUED/WAITING/READY/FAILED → CASHFLOW_SUPPRESSED | NO | NO | May break the manual action | NO |
| Submit/Approve/Reject | WAITING → READY | NO | NO | NO | May break the manual action | ?? Potential conflict that user submit and confirmation came |
| Adhoc SSI | READY → WAITING | NO | NO | ?? | NO | NO |
| SettleAsGross | WAITING | NO | NO | NO | NO | NO |
| Comment | Any | NO | NO | NO | NO | NO |
| Manual Fail/Approve | PROJECTED/QUEUED/WAITING/READY/HOLD → FAILED | ?? | NO | NO | May break the manual action | NO |

# **Internal Discussion on 21 Jan 2026**

Attendees: Davis, Liam, Nick

Enhancement we could do for future work:

1. Requirement wise going forward, always keep in mind asking what system should not do for more detailed validation control
2. Keep more attention on the edge/negative cases definition and testing

Some validation also discussed, to be taken into consideration for further solution:

1. Lifecycle additional check on current status, not only validating whether required action allowed or not
2. Workflow to guarantee only publish cashflow to SWIFT service with confirming current status is READY+NA+NA
3. Swift service to guarantee only generating SWIFT with confirming current status is READY+NA+PendingAck
4. We need to consider the scope of an additional check process before eventual publishing SWIFT out of RATAN as a gatekeeper

| ** ** | **OPS user A vs. OPS user B** | **OPS user vs. System process** | **System process A vs. System process B** | **Surrounding System Integration** |
| --- | --- | --- | --- | --- |
| **Concurrency control (Cache based lock)** | 1. Once OPS A trigger an action such as maker submit, not yet completed 2. Same time, OPS B's operates on same cashflow will be blocked as found it was locked by OPS A's operation | 1. When System start auto netting and processing on a cashflow OPS user's action on that cashflow will be rejected as it was locked by the auto netting process 2. When OPS user is doing settle as gross on a cashflow, then if system started auto netting on it, this will be rejected and try auto netted in next round job for the other cashflows | Scenario 1: 1. One stystem start handling trade confirmation status to drive payment STP, lock will be there until process complete. 2. Same time, SSI update comes and trigger another system processing, the action will be on hold until above processing completed. And vice versa. Scenario 2: 1. When system is processing version 1 event of new payment release, version 2 coming from upstream will be onhold until version 1 completed. 2. On contrary, when version 2 is being processed while version 1 to be auto processed later, it will be held and eventually the cashflow will be cancelled without processing. | NA |
| **Payment status control** | 1. When OPS A submitted a cashflow to WAITING + Pending Verification and complete processing, 2. Before notification arrived at OPS B's blotter, he can still see submit action as it is showing WAITING + Pending Operator 3. But when OPS B triggered submit again, action will be rejected as status move not allowed | 1. System started auto netting on cashflow and moved it to NETTED status 2. Before notification arrived at OPS blotter, OPS is still seeing WAITING+Pending Auto Netting, when he try to settle as gross, the action will be rejected as status move not allowed | When workflow A complete, status will be changed, which will be out of scope for workflow B, such as trade confirmation flow on WAITING pending affirmation + failue job | NA |
| **System level data duplication check** | NA | NA | Kafka rebalance some time will cause duplicate, Camunda workflow will filter based on the cache level lock on cashflow id + business version + minor version | Scenario1: Same message won't be consumed or published by component Message Bridge by the tracking id Scenario2: SWIFT publishing, unique id in msg header duplication check exists |
| **Cashflow events group control** | NA | NA | NA | Scenario 1. If upstream send more cashflows in a group, the additional one it will be blocked as ERROR and alert to OPS/PSS Scenario 2. Non economic amend detection to avoid unnecessary replacement on cashflow and additional OPS effort Scenario 3. Post payment release amendment, both reversal and rebook will be NSTP to avoid duplicated payments |
| **Swift service duplication check ** | NA | NA | 1. Auto release job will mark the process done in DB and prevent another round of job scanning it 2. SWIFT service duplication check on cashflow id + biz version | NA |
| **Trade Validation** | Payment won't be apprearing in cashflow blotter until trade validated |

# **Netting Issue: **

**Production:  netting over 357 component cashflows, 2 resultant generated: N00000267689,N00000266337**

user1: 02:07:39 trigger netting call life cycle check cashflow status 
user1: 02:07:43 lock by netting service

user2: 02:07:44 trigger netting call life cycle check cashflow status
user1: 02:07:49 net completion lock release (N00000266337)

user2: 02:07:52 lock by netting service 
user2: 02:07:58 net completion lock release (N00000267689) and N00000266337's netting id is losing component cashflows

# **Root Cause:**

1. NETTED status allow Net action as well, on specific context it means wrong/duplicate action
2. Status movement API does not validate minor version any longer
3. Lock space