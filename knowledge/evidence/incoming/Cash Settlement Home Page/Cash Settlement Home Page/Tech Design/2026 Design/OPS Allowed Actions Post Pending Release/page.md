# **Issue Description**

A payment of CNH 1,989,276,383 (equivalent USD 285m) was unexpectedly processed as Gross and Net on a Forward Precious Metal trade and transferred to client on value date 13 Jan 2026.

Client had requested for an ad-hoc net settlement which was duly agreed to by FMO Settlements upon the completion of initiating the Netting request in the settlement system (RATAN). However, as the actions were performed after RATAN currency release time at 11:00:34 AM GMT, RATAN released the Gross and also the Netted amount expected by the Client CNH 95,857,685 (equivalent USD 13m).

The Gross payment was recalled and returned CNH 1,989,276,383 on 14-Jan 2026.

# **Root Cause**

**Systems and Technology | Inadequate Software Configuration | System / Technology - System does not have required feature/function (deficiency/limitation): **

A rare unknown edge case occurring within a very short time window. Within a 55 seconds timeframe the gross payment was being sent by RATAN automatically at currency release time while an Operations user was performing an ad-hoc netting action on the same gross cashflow in Ready status, RATAN did not block the ad-hoc netting even though the gross cashflow was simultaneously being released. This was an undocumented and unknown behavior of the system.

# **Error/Duplicated Payment Control**

See below what we have done as well as the proposed items, expect to be finalized in the review.

1. ** Control 1: Timing Control. **We put a timing control that it does not allow OPS to perform netting/splitting post 10 mins before release cutoff by 2026-01-17
2. ** Control 2: Status Check. **We placed a control on status when try releasing the payment to avoid the conflict of actions by 2026-01-31, details please refer to **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)**.

# **Appendix - Actions allowed post pending release**

**Conclusion**: for below allowed actions on pending release (READY) status. **Reviewers**: Prakash, Liam, Nick, Geoffrey

| | Source Cashflow Status | Action | Target Cashflow Status | Business Case | Risk On Duplication | Control |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | READY | Maker Submit | WAITING | Adhoc SSI stamping - Maker resubmit SI | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 2 | READY | Checker Reject | WAITING | SSI Adjustment - Checker Reject to Maker | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 3 | READY | Early Release | READY | OPS manual release payment | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 4 | READY | Un Net | DEAD | OPS Unnet resultant payment | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 5 | READY | UnSplit | DEAD | OPS Un Split payment | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 6 | READY | Hold | HOLD | OPS Hold the payment from auto releasing | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 7 | READY | Manual Swift Suppress | WAITING | Maker submit swift suppression to checker | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 8 | READY | Manual Fail | WAITING | Maker submit manual fail to checker | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 9 | READY | Full Utilize | UTILIZED | Either OPS manually process FX Full Utilization from FXU or by auto utilization process | , Status Machine Control, No Payment generated | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 10 | READY | Partial Utilize | PARTIALLY_UTILIZED | OPS manually process FX Partial Utilization from FXU | , Status Machine Control, No Payment generated | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 11 | READY | Net | NETTED | OPS net the payment | by Jan 2026, Strategic fix done | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 12 | READY | Split | SPLIT | OPS split the payment | by Jan 2026, Strategic fix done | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 13 | READY | Manual Suppress | WAITING | Maker submit cashflow suppression to checker | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 14 | READY | Resend To Razor | READY | Post release job, OPS manual retry when Razor did not receive the cashflow on edge exceptional case | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |
| 15 | READY | Regenerate Swift | READY | Post release job, OPS manual retry when Swift Service did not receive the cashflow on edge exceptional case | , Status Machine Control | Applied hard block that allow only READY payments sending to downstream, as explained by **[Section 5](https://confluence.global.standardchartered.com/display/DSP/OPS+Allowed+Actions+Post+Pending+Release#OPSAllowedActionsPostPendingRelease-DiagramForTheControl)** |

# **Diagram For The Control**

Applied hard block that allow only READY payments sending to downstream.

Whenever payment got processed to other status, release process will be stopped.