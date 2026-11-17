# 1. Background

Cash Settlement Platform will maintain the payment lifecycle, including the status machine and the processing flow.

The sources include Murex2.11, Razor and STELLA/TDSS3, since the statuses should be synced back to STELLA/TDS3, we will keep the statuses similar to each other.

# 2. Status Machine

| Status | Trigger | Comments |
| --- | --- | --- |
| PROJECTED | Blade/Stella or Murex 2.11 trade booking/amendment/cancellation | Cashflow is initialized and published by STELLA or Murex 2.11, cashflow events can be as below - New - Withdrawal |
| QUEUED | Ratan scheduled job on VD-5, | Temporary status only |
| WAITING | Workflow NSTP rules or FMO GUI manual process, or Sub Status Type - Pending Netting - Pending Another Leg - Pending Exception | Pending user operations to STP cashflows Examples as below cases: | Status | Sub status Type | Sub Status | Description | | --- | --- | --- | --- | | WAITING | Pending Netting | Pending Operator | Pending FMO Maker to perform netting | | WAITING | Pending Exception | Pending Verification | Pending FMO Checker resolve business exceptions | |
| Status | Sub status Type | Sub Status | Description |
| WAITING | Pending Netting | Pending Operator | Pending FMO Maker to perform netting |
| WAITING | Pending Exception | Pending Verification | Pending FMO Checker resolve business exceptions |
| HOLD | Manual operation to hold the payment | Status to prevent auto STP the payment |
| READY | 1. Checker approved the payments 2. Auto READY if not exceptions generated | Status indicate payment ready to be STPed at release cutoff |
| CANCELLED | Withdrawal triggered from TP system like Murex/Stella | Payment got cancelled before releasing to downstream |
| RELEASED | Status post SWIFT published to FMSGW or in legacy flow, post payments published to Razor. | payment released from Ratan |
| SETTLED | AMH/SCPAY proceed the payment and ACK to Ratan | Payment ACKed from AMH/SCPAY |
| NOSTRO MATCHED (not in scope for now) | TLM recon succeeded | TLM notified match on payment, this is something to be built |
| CASHFLOW_SUPPRESSED | 1. Adhoc Suppression OR 2. Suppressed by suppression rule check | Cashflow that not eligible for settlement nor accounting |
| SWIFT_SUPPRESSED | 1. Adhoc Swift Suppression OR 2. Suppressed by swift suppression rule check | Eligible for accounting but skip swift generation |
| NETTED | 1. Scheduled auto netting job 2. FMO manual netting from cashflow blotter | Status for component cashflow post netting |
| DEAD | - FMO manual un-net from cashflow blotter - Trade amendment/cancellation from TP system( Stella/Murex 2.11) | Status for resultant cashflow post unnet |
| FAILED | 1. Scheduled EOD job on VD 2. Adhoc manual fail | Payment not valid to settle, but still got a chance to be reinstated. Eligible for accounting |
| UTILIZED | 1. Utilization request from FXU (for settlement means=FXBERREC_M)OR 2. Ratan auto utilization EOD job (for settlement means=FXBERREC) | Full amount is utilized and remaining amount is 0 |
| PARTIALLY-UTILIZED | Utilization request from FXU (for settlement means=FXBERREC_M) | Partial amount is utilized and remaining amount is not 0 |
| PASTDUE | Ratan auto pastdue job | No utilization happen until VD EOD |
| SPLIT | 1. user manually split the cashflow 2. system auto split the cashflow | status for parent cashflow post split action |

| | Source Cashflow Status | Source Cashflow Sub Status | Source Cashflow Sub Status Type | Action | Target Cashflow Status | Target Cashflow Sub Status | Target Cashflow Sub Status Type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NA | NA | NA | New | PROJECTED | NA | NA |
| 2 | NA | NA | NA | Amendment | PROJECTED | NA | NA |
| 3 | NA | NA | NA | NetNew | QUEUED | NA | NA |
| 4 | NA | NA | NA | SplitNew | QUEUED | NA | NA |
| 5 | PROJECTED | NA | NA | Amendment | PROJECTED | NA | NA |
| 6 | PROJECTED | NA | NA | Materialize | QUEUED | NA | NA |
| 7 | PROJECTED | NA | NA | Suppress | CASHFLOW_SUPPRESSED | NA | NA |
| 8 | PROJECTED | NA | NA | Affirmed | PROJECTED | NA | NA |
| 9 | PROJECTED | NA | NA | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 10 | PROJECTED | NA | NA | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 11 | PROJECTED | NA | NA | Net | NETTED | NA | NA |
| 12 | PROJECTED | NA | NA | Withdrawal | CANCELLED | NA | NA |
| 13 | PROJECTED | NA | NA | TechFail | QUEUED | NA | Pending Exception |
| 14 | PROJECTED | NA | NA | Fail | FAILED | NA | NA |
| 15 | QUEUED | NA | NA | Amendment | QUEUED | NA | NA |
| 16 | QUEUED | NA | NA | IsNettingEligible | WAITING | Pending Operator | Pending Netting |
| 17 | QUEUED | NA | NA | WaitingAnotherLeg | WAITING | NA | Pending Another Leg |
| 18 | QUEUED | NA | NA | IsAutoNettingEligible | WAITING | NA | Auto Netting |
| 19 | QUEUED | NA | NA | IsNstp | WAITING | Pending Operator | Pending Exception |
| 20 | QUEUED | NA | NA | IsNstpChecker | WAITING | Pending Verification | Pending Exception |
| 21 | QUEUED | NA | NA | ValidateDirect | READY | NA | NA |
| 22 | QUEUED | NA | NA | Net | NETTED | NA | NA |
| 23 | QUEUED | NA | NA | SwiftSuppress | SWIFT_SUPPRESSED | NA | NA |
| 24 | QUEUED | NA | NA | Suppress | CASHFLOW_SUPPRESSED | NA | NA |
| 25 | QUEUED | NA | NA | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 26 | QUEUED | NA | NA | UnNet | DEAD | NA | NA |
| 27 | QUEUED | NA | NA | Fail | FAILED | NA | NA |
| 28 | QUEUED | NA | NA | TechFail | QUEUED | NA | Pending Exception |
| 29 | QUEUED | NA | NA | Withdrawal | CANCELLED | NA | NA |
| 30 | QUEUED | NA | NA | SsiStamped | QUEUED | NA | NA |
| 31 | QUEUED | NA | NA | NostroStamped | QUEUED | NA | NA |
| 32 | QUEUED | NA | NA | VostroStamped | QUEUED | NA | NA |
| 33 | QUEUED | NA | NA | Split | SPLIT | NA | NA |
| 34 | QUEUED | NA | NA | Hold | HOLD | Pending Verification | NA |
| 35 | QUEUED | NA | Pending Exception | ReInstate | QUEUED | NA | NA |
| 36 | QUEUED | NA | Pending Exception | Fail | FAILED | NA | NA |
| 37 | QUEUED | NA | Pending Exception | UnNet | DEAD | NA | NA |
| 38 | QUEUED | NA | Pending Exception | Net | NETTED | NA | NA |
| 39 | QUEUED | NA | Pending Exception | Affirmed | QUEUED | NA | Pending Exception |
| 40 | QUEUED | NA | Pending Exception | Amendment | QUEUED | NA | NA |
| 41 | QUEUED | NA | Pending Exception | Withdrawal | CANCELLED | NA | NA |
| 42 | WAITING | Pending Operator | Pending Exception | Submit | WAITING | Pending Verification | Pending Exception |
| 43 | WAITING | Pending Operator | Pending Exception | ApproveOnlyMaker | READY | NA | NA |
| 44 | WAITING | Pending Verification | Pending Exception | Reject | WAITING | Pending Operator | Pending Exception |
| 45 | WAITING | Pending Verification | Pending Exception | SsiStamped | WAITING | Pending Verification | Pending Exception |
| 46 | WAITING | Pending Verification | Pending Exception | NostroStamped | WAITING | Pending Verification | Pending Exception |
| 47 | WAITING | Pending Verification | Pending Exception | VostroStamped | WAITING | Pending Verification | Pending Exception |
| 48 | WAITING | Pending Verification | Pending Exception | PaymentDateUpdate | WAITING | Pending Verification | Pending Exception |
| 49 | WAITING | Pending Verification | Pending Exception | Affirmed | WAITING | Pending Verification | Pending Exception |
| 50 | WAITING | Pending Operator | Pending Exception | Affirmed | WAITING | Pending Operator | Pending Exception |
| 51 | WAITING | Pending Operator | Pending Netting | Affirmed | WAITING | Pending Operator | Pending Netting |
| 52 | WAITING | Pending Operator | Pending Netting | NostroStamped | WAITING | Pending Operator | Pending Netting |
| 53 | WAITING | Pending Operator | Pending Netting | VostroStamped | WAITING | Pending Operator | Pending Netting |
| 54 | WAITING | Pending Operator | Pending Netting | SsiStamped | WAITING | Pending Operator | Pending Netting |
| 55 | WAITING | Pending Operator | Pending Netting | SettleAsGross | QUEUED | NA | NA |
| 56 | WAITING | Pending Verification | Pending Exception | Approve | READY | NA | NA |
| 57 | WAITING | Pending Verification | Netting Review | Approve | READY | NA | NA |
| 58 | WAITING | Pending Verification | Netting Review | UnNet | DEAD | NA | NA |
| 59 | WAITING | Pending Operator | Pending Exception | UnNet | DEAD | NA | NA |
| 60 | WAITING | Pending Verification | Pending Exception | UnNet | DEAD | NA | NA |
| 61 | WAITING | Pending Verification | Undo Cashflow Suppression | UnNet | DEAD | NA | NA |
| 62 | WAITING | Pending Verification | Cashflow Suppression | UnNet | DEAD | NA | NA |
| 63 | WAITING | Pending Verification | Undo Swift Suppression | UnNet | DEAD | NA | NA |
| 64 | WAITING | Pending Verification | Swift Suppression | UnNet | DEAD | NA | NA |
| 65 | WAITING | NA | Pending Another Leg | NostroStamped | WAITING | NA | Pending Another Leg |
| 66 | WAITING | NA | Pending Another Leg | VostroStamped | WAITING | NA | Pending Another Leg |
| 67 | WAITING | Pending Verification | Reversal Rebook | ManualStp | QUEUED | NA | NA |
| 68 | WAITING | Pending Verification | Reversal Rebook | AutoStp | QUEUED | NA | NA |
| 69 | WAITING | NA | Pending Another Leg | SsiStamped | WAITING | NA | Pending Another Leg |
| 70 | WAITING | NA | Pending Another Leg | SettleAsGross | QUEUED | NA | NA |
| 71 | WAITING | Pending Operator | Pending Exception | Net | NETTED | NA | NA |
| 72 | WAITING | Pending Verification | Pending Exception | Net | NETTED | NA | NA |
| 73 | WAITING | Pending Operator | Pending Netting | Net | NETTED | NA | NA |
| 74 | WAITING | Pending Verification | Netting Review | Net | NETTED | NA | NA |
| 75 | WAITING | NA | Pending Another Leg | Net | NETTED | NA | NA |
| 76 | WAITING | Pending Verification | Reversal Rebook | Net | NETTED | NA | NA |
| 77 | WAITING | Pending Operator | Pending Exception | Split | SPLIT | NA | NA |
| 78 | WAITING | Pending Verification | Pending Exception | Split | SPLIT | NA | NA |
| 79 | WAITING | Pending Operator | Pending Netting | Split | SPLIT | NA | NA |
| 80 | WAITING | Pending Verification | Netting Review | Split | SPLIT | NA | NA |
| 81 | WAITING | NA | Pending Another Leg | Split | SPLIT | NA | NA |
| 82 | WAITING | Pending Verification | Reversal Rebook | Split | SPLIT | NA | NA |
| 83 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | Net | NETTED | NA | NA |
| 84 | WAITING | Pending Operator | Pending Exception | TechFail | QUEUED | NA | Pending Exception |
| 85 | WAITING | Pending Verification | Pending Exception | TechFail | QUEUED | NA | Pending Exception |
| 86 | WAITING | Pending Operator | Pending Netting | TechFail | QUEUED | NA | Pending Exception |
| 87 | WAITING | Pending Verification | Netting Review | TechFail | QUEUED | NA | Pending Exception |
| 88 | WAITING | NA | Pending Another Leg | TechFail | QUEUED | NA | Pending Exception |
| 89 | WAITING | Pending Verification | Reversal Rebook | TechFail | QUEUED | NA | Pending Exception |
| 90 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | TechFail | QUEUED | NA | Pending Exception |
| 91 | WAITING | Pending Operator | Pending Exception | Hold | HOLD | Pending Verification | NA |
| 92 | WAITING | Pending Verification | Pending Exception | Hold | HOLD | Pending Verification | NA |
| 93 | WAITING | Pending Operator | Pending Netting | Hold | HOLD | Pending Verification | NA |
| 94 | WAITING | Pending Verification | Netting Review | Hold | HOLD | Pending Verification | NA |
| 95 | WAITING | NA | Pending Another Leg | Hold | HOLD | Pending Verification | NA |
| 96 | WAITING | Pending Verification | Reversal Rebook | Hold | HOLD | Pending Verification | NA |
| 97 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | Hold | HOLD | Pending Verification | NA |
| 98 | WAITING | Pending Operator | Pending Exception | RevertToQueued | QUEUED | NA | NA |
| 99 | WAITING | Pending Verification | Pending Exception | RevertToQueued | QUEUED | NA | NA |
| 100 | WAITING | Pending Operator | Pending Netting | RevertToQueued | QUEUED | NA | NA |
| 101 | WAITING | Pending Verification | Netting Review | RevertToQueued | QUEUED | NA | NA |
| 102 | WAITING | NA | Pending Another Leg | RevertToQueued | QUEUED | NA | NA |
| 103 | WAITING | Pending Verification | Reversal Rebook | RevertToQueued | QUEUED | NA | NA |
| 104 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | RevertToQueued | QUEUED | NA | NA |
| 105 | WAITING | Pending Operator | Pending Exception | Amendment | QUEUED | NA | NA |
| 106 | WAITING | Pending Verification | Pending Exception | Amendment | QUEUED | NA | NA |
| 107 | WAITING | Pending Operator | Pending Netting | Amendment | QUEUED | NA | NA |
| 108 | WAITING | Pending Verification | Netting Review | Amendment | QUEUED | NA | NA |
| 109 | WAITING | NA | Pending Another Leg | Amendment | QUEUED | NA | NA |
| 110 | WAITING | Pending Verification | Reversal Rebook | Amendment | QUEUED | NA | NA |
| 111 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | Amendment | QUEUED | NA | NA |
| 112 | WAITING | Pending Operator | Pending Exception | Withdrawal | CANCELLED | NA | NA |
| 113 | WAITING | Pending Verification | Pending Exception | Withdrawal | CANCELLED | NA | NA |
| 114 | WAITING | Pending Operator | Pending Netting | Withdrawal | CANCELLED | NA | NA |
| 115 | WAITING | Pending Verification | Netting Review | Withdrawal | CANCELLED | NA | NA |
| 116 | WAITING | NA | Pending Another Leg | Withdrawal | CANCELLED | NA | NA |
| 117 | WAITING | Pending Verification | Reversal Rebook | Withdrawal | CANCELLED | NA | NA |
| 118 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | Withdrawal | CANCELLED | NA | NA |
| 119 | WAITING | Pending Operator | Pending Exception | Fail | FAILED | NA | NA |
| 120 | WAITING | Pending Verification | Pending Exception | Fail | FAILED | NA | NA |
| 121 | WAITING | Pending Operator | Pending Netting | Fail | FAILED | NA | NA |
| 122 | WAITING | Pending Verification | Netting Review | Fail | FAILED | NA | NA |
| 123 | WAITING | NA | Pending Another Leg | Fail | FAILED | NA | NA |
| 124 | WAITING | Pending Verification | Reversal Rebook | Fail | FAILED | NA | NA |
| 125 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | Fail | FAILED | NA | NA |
| 126 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 127 | WAITING | Pending Verification | Pending Exception | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 128 | WAITING | Pending Operator | Pending Netting | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 129 | WAITING | Pending Verification | Netting Review | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 130 | WAITING | NA | Pending Another Leg | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 131 | WAITING | Pending Verification | Reversal Rebook | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 132 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 133 | WAITING | Pending Operator | Pending Exception | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 134 | WAITING | Pending Verification | Pending Exception | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 135 | WAITING | Pending Operator | Pending Netting | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 136 | WAITING | Pending Verification | Netting Review | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 137 | WAITING | NA | Pending Another Leg | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 138 | WAITING | Pending Verification | Reversal Rebook | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 139 | WAITING | Pending Operator | Pending Netting 4 Withdrawal | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 140 | WAITING | Pending Verification | Cashflow Suppression | Reject | NA | NA | NA |
| 141 | WAITING | Pending Verification | Cashflow Suppression | Approve | CASHFLOW_SUPPRESSED | NA | NA |
| 142 | WAITING | Pending Verification | Undo Cashflow Suppression | Reject | NA | NA | NA |
| 143 | WAITING | Pending Verification | Undo Cashflow Suppression | Approve | QUEUED | NA | NA |
| 144 | WAITING | Pending Verification | Swift Suppression | Reject | NA | NA | NA |
| 145 | WAITING | Pending Verification | Swift Suppression | Approve | SWIFT_SUPPRESSED | NA | NA |
| 146 | WAITING | Pending Verification | Undo Swift Suppression | Reject | NA | NA | NA |
| 147 | WAITING | Pending Verification | Undo Swift Suppression | Approve | QUEUED | NA | NA |
| 148 | READY | NA | NA | Amendment | QUEUED | NA | NA |
| 149 | READY | NA | NA | Release | RELEASED | NA | NA |
| 150 | READY | NA | NA | RevertPenVerfication | WAITING | Pending Verification | Pending Exception |
| 151 | READY | NA | NA | IsNstpChecker | WAITING | Pending Verification | Pending Exception |
| 152 | READY | NA | NA | IsNstp | WAITING | Pending Operator | Pending Exception |
| 153 | READY | NA | NA | SettleDirect | SETTLED | NA | NA |
| 154 | READY | NA | NA | SentToRazor | READY | NA | Pending Ack |
| 155 | READY | NA | NA | UnNet | DEAD | NA | NA |
| 156 | READY | NA | NA | Hold | HOLD | Pending Verification | NA |
| 157 | READY | NA | NA | ManualSwiftSuppress | WAITING | Pending Verification | Swift Suppression |
| 158 | READY | NA | NA | Withdrawal | CANCELLED | NA | NA |
| 159 | READY | NA | NA | TechFail | QUEUED | NA | Pending Exception |
| 160 | READY | NA | NA | RevertToQueued | QUEUED | NA | NA |
| 161 | READY | NA | NA | Net | NETTED | NA | NA |
| 162 | READY | NA | NA | Fail | FAILED | NA | NA |
| 163 | READY | NA | NA | ManualSuppress | WAITING | Pending Verification | Cashflow Suppression |
| 164 | READY | NA | Pending Ack | Release | RELEASED | NA | NA |
| 165 | READY | NA | Pending Ack | Settle | SETTLED | NA | NA |
| 166 | READY | NA | Pending Ack | ResendToRazor | READY | NA | Pending Ack |
| 167 | READY | NA | Pending Ack | Withdrawal | QUEUED | NA | NA |
| 168 | READY | NA | Pending Ack | TechFail | QUEUED | NA | Pending Exception |
| 169 | READY | NA | Pending Ack | Fail | FAILED | NA | NA |
| 170 | RELEASED | NA | NA | Settle | SETTLED | NA | NA |
| 171 | RELEASED | NA | NA | ManualSubmit | RELEASED | Manual Settle | Pending Verification |
| 172 | RELEASED | Manual Settle | Pending Verification | ManualApprove | SETTLED | Manual Settle | NA |
| 173 | RELEASED | Manual Settle | Pending Verification | ManualReject | RELEASED | NA | NA |
| 174 | RELEASED | NA | NA | ReplayStatusWriteBack | RELEASED | NA | NA |
| 175 | RELEASED | NA | NA | Withdrawal | QUEUED | NA | NA |
| 176 | SETTLED | NA | NA | Withdrawal | QUEUED | NA | NA |
| 177 | SETTLED | NA | NA | ReplayStatusWriteBack | SETTLED | NA | NA |
| 178 | SETTLED | NA | NA | NostroMatch | NOSTRO_MATCHED | NA | NA |
| 179 | NOSTRO_MATCHED | NA | NA | Withdrawal | QUEUED | NA | NA |
| 180 | NOSTRO_MATCHED | NA | NA | ReplayStatusWriteBack | NOSTRO_MATCHED | NA | NA |
| 181 | NOSTRO_MATCHED | NA | NA | Fail | FAILED | NA | NA |
| 182 | HOLD | Pending Verification | NA | UnHold | NA | NA | NA |
| 183 | HOLD | Pending Verification | NA | UnNet | DEAD | NA | NA |
| 184 | HOLD | Pending Verification | NA | TechFail | QUEUED | NA | Pending Exception |
| 185 | HOLD | Pending Verification | NA | RevertToQueued | QUEUED | NA | NA |
| 186 | HOLD | Pending Verification | NA | Amendment | QUEUED | NA | NA |
| 187 | HOLD | Pending Verification | NA | Withdrawal | CANCELLED | NA | NA |
| 188 | HOLD | Pending Verification | NA | Fail | FAILED | NA | NA |
| 189 | ERROR | NA | NA | Withdrawal | CANCELLED | NA | NA |
| 190 | ERROR | NA | NA | Fail | FAILED | NA | NA |
| 191 | | | | | | | |
| 192 | ~~SPLIT~~ | ~~NA~~ | ~~NA~~ | ~~Release~~ | SPLIT | NA | Released |
| 193 | ~~SPLIT~~ | ~~NA~~ | ~~Released~~ | ~~Settle~~ | SPLIT | NA | Settled |
| 194 | ~~SPLIT~~ | ~~NA~~ | ~~Settled~~ | ~~NostroMatch~~ | SPLIT | NA | NostroMatched |
| 195 | ~~SPLIT~~ | ~~NA~~ | ~~Released~~ | ~~Withdrawal~~ | QUEUED | NA | NA |
| 196 | ~~SPLIT~~ | ~~NA~~ | ~~Settled~~ | ~~Withdrawal~~ | QUEUED | NA | NA |
| 197 | ~~SPLIT~~ | ~~NA~~ | ~~NostroMatched~~ | ~~Withdrawal~~ | QUEUED | NA | NA |
| 198 | ~~SPLIT~~ | ~~NA~~ | ~~NA~~ | ~~TechFail~~ | QUEUED | NA | Pending Exception |
| 199 | ~~SPLIT~~ | ~~NA~~ | ~~Released~~ | ~~TechFail~~ | QUEUED | NA | Pending Exception |
| 200 | ~~SPLIT~~ | ~~NA~~ | ~~Settled~~ | ~~TechFail~~ | QUEUED | NA | Pending Exception |
| 201 | ~~SPLIT~~ | ~~NA~~ | ~~NostroMatched~~ | ~~TechFail~~ | QUEUED | NA | Pending Exception |
| 202 | FAILED | NA | NA | ReInstate | QUEUED | NA | NA |
| 203 | FAILED | NA | NA | AccountingAck | FAILED | NA | Accounting Acked |
| 204 | FAILED | NA | NA | Affirmed | FAILED | NA | NA |
| 205 | FAILED | NA | NA | Amendment | QUEUED | NA | NA |
| 206 | FAILED | NA | NA | Withdrawal | CANCELLED | NA | NA |
| 207 | FAILED | NA | NA | UnNet | DEAD | NA | NA |
| 208 | NETTED | NA | NA | UnNet | QUEUED | NA | NA |
| 209 | NETTED | NA | NA | Release | NETTED | NA | Released |
| 210 | NETTED | NA | NA | Net | NETTED | NA | NA |
| 211 | NETTED | NA | NA | Withdrawal | QUEUED | NA | NA |
| 212 | NETTED | NA | Released | Withdrawal | QUEUED | NA | NA |
| 213 | NETTED | NA | Released | Settle | NETTED | NA | Settled |
| 214 | NETTED | NA | Released | ReplayStatusWriteBack | NETTED | NA | Released |
| 215 | NETTED | NA | Settled | Withdrawal | QUEUED | NA | NA |
| 216 | NETTED | NA | Settled | NostroMatch | NETTED | NA | NostroMatched |
| 217 | NETTED | NA | Settled | ReplayStatusWriteBack | NETTED | NA | Settled |
| 218 | NETTED | NA | NostroMatched | ReplayStatusWriteBack | NETTED | NA | NostroMatched |
| 219 | NETTED | NA | NostroMatched | Withdrawal | QUEUED | NA | NA |
| 220 | NETTED | NA | NA | TechFail | QUEUED | NA | Pending Exception |
| 221 | NETTED | NA | Released | TechFail | QUEUED | NA | Pending Exception |
| 222 | NETTED | NA | Settled | TechFail | QUEUED | NA | Pending Exception |
| 223 | NETTED | NA | NostroMatched | TechFail | QUEUED | NA | Pending Exception |
| 224 | SWIFT_SUPPRESSED | NA | NA | ManualSwiftUnSuppress | WAITING | Pending Verification | Undo Swift Suppression |
| 225 | SWIFT_SUPPRESSED | NA | NA | Fail | FAILED | NA | NA |
| 226 | SWIFT_SUPPRESSED | NA | NA | AccountingAck | SWIFT_SUPPRESSED | NA | Accounting Acked |
| 227 | SWIFT_SUPPRESSED | NA | NA | SsiStamped | SWIFT_SUPPRESSED | NA | NA |
| 228 | SWIFT_SUPPRESSED | NA | NA | NostroStamped | SWIFT_SUPPRESSED | NA | NA |
| 229 | SWIFT_SUPPRESSED | NA | NA | VostroStamped | SWIFT_SUPPRESSED | NA | NA |
| 230 | SWIFT_SUPPRESSED | NA | NA | Withdrawal | CANCELLED | NA | NA |
| 231 | SWIFT_SUPPRESSED | NA | NA | UnNet | DEAD | NA | NA |
| 232 | CASHFLOW_SUPPRESSED | NA | NA | UnSuppress | QUEUED | NA | NA |
| 233 | CASHFLOW_SUPPRESSED | NA | NA | ManualUnSuppress | WAITING | Pending Verification | Undo Cashflow Suppression |
| 234 | CASHFLOW_SUPPRESSED | NA | NA | Fail | FAILED | NA | NA |
| 235 | CASHFLOW_SUPPRESSED | NA | NA | Amendment | QUEUED | NA | NA |
| 236 | CASHFLOW_SUPPRESSED | NA | NA | TechFail | QUEUED | NA | Pending Exception |
| 237 | CASHFLOW_SUPPRESSED | NA | NA | Withdrawal | CANCELLED | NA | NA |
| 238 | CASHFLOW_SUPPRESSED | NA | NA | UnNet | DEAD | NA | NA |
| 239 | READY | NA | NA | **FullUtilize** | UTILIZED | NA | NA |
| 240 | READY | NA | NA | **PartialUtilize** | PARTIALLY_UTILIZED | NA | NA |
| 241 | READY | NA | NA | **AutoUtilize** | UTILIZED | NA | NA |
| 242 | READY | NA | NA | **Pastdue** | PASTDUE | Pastdue | NA |
| 243 | PARTIALLY_UTILIZED | NA | NA | **FullUtilize** | UTILIZED | NA | NA |
| 244 | ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ | ~~**PartialUtilize**~~ | ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ |
| 245 | PARTIALLY_UTILIZED | NA | NA | **FullReverse** | READY | NA | NA |
| 246 | ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ | ~~**PartialReverse**~~ | ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ |
| 247 | PARTIALLY_UTILIZED | NA | NA | Pastdue | PARTIALLY_UTILIZED | Pastdue | NA |
| 248 | PARTIALLY_UTILIZED | NA | NA | **Withdrawal** | ERROR | NA | NA |
| 249 | PARTIALLY_UTILIZED | Pastdue | NA | **FullUtilize** | UTILIZED | NA | NA |
| 250 | PARTIALLY_UTILIZED | Pastdue | NA | **FullReverse** | READY | NA | NA |
| 251 | PARTIALLY_UTILIZED | Pastdue | NA | **PartialUtilize** | PARTIALLY_UTILIZED | NA | NA |
| 252 | PARTIALLY_UTILIZED | Pastdue | NA | **PartialReverse** | PARTIALLY_UTILIZED | NA | NA |
| 253 | PARTIALLY_UTILIZED | Pastdue | NA | **Withdrawal** | ERROR | Pastdue | NA |
| 254 | UTILIZED | NA | NA | **FullReverse** | READY | NA | NA |
| 255 | UTILIZED | NA | NA | **PartialReverse** | PARTIALLY_UTILIZED | NA | NA |
| 256 | UTILIZED | NA | NA | **Withdrawal** | ERROR | NA | NA |
| 257 | PASTDUE | Pastdue | NA | **FullUtilize** | UTILIZED | NA | NA |
| 258 | PASTDUE | Pastdue | NA | **PartialUtilize** | PARTIALLY_UTILIZED | NA | NA |
| 259 | PASTDUE | Pastdue | NA | **Withdrawal** | CANCELLED | NA | NA |
| 260 | SPLIT | NA | NA | UnSplit | QUEUED | NA | NA |
| 261 | READY | NA | NA | UnSplit | DEAD | NA | NA |
| 262 | QUEUED | ALL | ALL | UnSplit | DEAD | NA | NA |
| 263 | WAITING | ALL | ALL | UnSplit | DEAD | NA | NA |
| 264 | HOLD | ALL | ALL | UnSplit | DEAD | NA | NA |
| 265 | FAILED | ALL | ALL | UnSplit | DEAD | NA | NA |
| 266 | CASHFLOW_SUPPRESSED | ALL | ALL | UnSplit | DEAD | NA | NA |
| 267 | SWIFT_SUPPRESSED | ALL | ALL | UnSplit | DEAD | NA | NA |

## Status machine tech details

**EXPAND: Status machine tech details**

## Versions

1. Business Version: Upgrade when there is any actions on trade that impact on cashflow, such as trade booking, amendment and cancellation
2. Cashflow Version: 1. Upgrade when there is business version upgrade on trade operations 2. Upgrade when there is any cashflow status change in STELLA
3. Minor Version: Incremental on all actions, from STELLA/Murex, including Ratan STP/manual actions

## 2 kinds of requests:

1. External request, coming from STELLA or Murex, it will be work for STP only 1. Accept only 1. PROJECTED status with below events 1. New 2. Amendment 3. Withdrawal 2. RELEASED/SETTLED/NETTED status with below events 1. Withdrawal 2. Withdrawal & New 2. 3 versions will be updated 3. Request details: 1. Cashflow Id 2. Business Version 3. Cashflow Version 4. Action
2. Internal request, coming from Ratan on STP and manual actions, API will be exposed to Ratan services such as stamping service 1. No business/cashflow version change 2. Request details: 1. Cashflow Id 2. Minor Version 3. Action

Main table to record messages consumed from upstream:

![image2022-10-31_14-7-8.png](attachments/image2022-10-31_14-7-8.png)

History table to record actions derived from the messages above and the Ratan actions (STP and manual actions):

![image2022-10-31_14-9-7.png](attachments/image2022-10-31_14-9-7.png)

## API Information

| | Function | URL | Parameters | Response | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Ratan Service on cashflow status change | POST [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/update/status](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/update/status) Basic auth: ratanone-control-m / ratanone@controlm | LifecycleRequest{ "cashflowId": "002690235964", "businessVersion": "0", "cashflowVersion": "0", "minorVersion": "0", "ratanAction": "New", "updater": "System", "nstpReason": "", "bodyEventRowKey": "", "valueDate": "", "eventType", "New", "message": "SCBML", // Required for SSI stamped "swiftPaymentDate": "2023-02-28", // for PaymentDateUpdate action only "comment": "Affirmed by somebody", "affirmationDetails": { "affirmedBy": "Geoffrey", "phone_email": "geoffrey@[sc.com](http://sc.com)" } } | { "cashflowId": "002690235964", "businessVersion": "0", "cashflowVersion": "0", "action": "Materialize", "updater": "1481696", "previousCashflowIndex": { "minorVersion": "0", "cashflowStatus": { "cashflowEnumMainStatus": "PROJECTED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "nextCashflowIndex": { "minorVersion": "1", "cashflowStatus": { "cashflowEnumMainStatus": "QUEUED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "cashflowStatusResponseCode": "SUCCESS", "reason": null } | |
| 2 | Consumed message on cashflow status change Including creation | Not API, but a function: LifecycleService.statusUpdate | LifecycleRequest { "cashflowId": "002690235964", "businessVersion": "0", "cashflowVersion": "0", "minorVersion": "0", "ratanAction": "New", "updater": "System", "nstpReason": "", "bodyEventRowKey": "", "valueDate": "", "eventType", "New", "message": "SCBML", // required on New, Amendment, Withdrawal } | { "cashflowId": "002690235964", "businessVersion": "0", "cashflowVersion": "0", "action": "Create", "updater": "1481696", "previousCashflowIndex": { "cashflowStatus": { "cashflowEnumMainStatus": "NA", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "nextCashflowIndex": { "minorVersion": "0", "cashflowStatus": { "cashflowEnumMainStatus": "PROJECTED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "cashflowStatusResponseCode": "SUCCESS", "reason": null } | |
| 3 | Transactional Batch | POST [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/update/status/batch/transactional](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/update/status/batch/transactional) Basic auth: ratanone-control-m / ratanone@controlm | **EXPAND: Request** { "lifecycleRequests":[ { "cashflowId":"003690235976", "businessVersion":"0", "cashflowVersion":"0", "minorVersion":"1", "updater":"1481696", "nettingId": "11111111111-01", "ratanAction":"Net" }, { "cashflowId":"003690235975", "businessVersion":"0", "cashflowVersion":"0", "minorVersion":"0", "updater":"1481696", "nettingId": "11111111111-01", "ratanAction":"Net" }, { "cashflowId":"113690235975", "businessVersion":"0", "cashflowVersion":"0", "minorVersion":"0", "updater":"1481696", "nettingId": "11111111111-01", "ratanAction":"NetNew", "bodyEventRowkey":"STELLA_1816352_0_1829946-1_1001-113690235975-1-ratanone-lifecycle-cashflow-service-PROCESSED-New-8066f840-a1b7-4e86-8638-b4967b22ceaa", "valueDate": "2022-11-20", "eventType": "NetNew" } ] } **EXPAND_END** | **EXPAND: Response** { "cashflowStatusResponseCode": "SUCCESS", "cashflowStatusProcessingEntities": [ { "cashflowId": "003690235976", "businessVersion": "0", "cashflowVersion": "0", "action": "Net", "updater": "1481696", "previousCashflowIndex": { "minorVersion": "1", "cashflowStatus": { "cashflowEnumMainStatus": "QUEUED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "nextCashflowIndex": { "minorVersion": "2", "cashflowStatus": { "cashflowEnumMainStatus": "NETTED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "cashflowStatusResponseCode": "SUCCESS", "reason": null }, { "cashflowId": "003690235975", "businessVersion": "0", "cashflowVersion": "0", "action": "Net", "updater": "1481696", "previousCashflowIndex": { "minorVersion": "0", "cashflowStatus": { "cashflowEnumMainStatus": "PROJECTED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "nextCashflowIndex": { "minorVersion": "1", "cashflowStatus": { "cashflowEnumMainStatus": "NETTED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "cashflowStatusResponseCode": "SUCCESS", "reason": null }, { "cashflowId": "113690235975", "businessVersion": "0", "cashflowVersion": "0", "action": "NetNew", "updater": "1481696", "previousCashflowIndex": { "minorVersion": "NA", "cashflowStatus": { "cashflowEnumMainStatus": "NA", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "nextCashflowIndex": { "minorVersion": "0", "cashflowStatus": { "cashflowEnumMainStatus": "QUEUED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "cashflowStatusResponseCode": "SUCCESS", "reason": null } ] } **EXPAND_END** | |
| 4 | Batch | [POST ](http://10.198.199.160:26344/v1/ratan/lifecycle/update/status) [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/update/status/batch](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/update/status/batch) Basic auth: ratanone-control-m / ratanone@controlm | Same as above | | |
| 5 | Query | [POST ](http://10.198.199.160:26344/v1/ratan/lifecycle/update/status) [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/query](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/query) Basic auth: ratanone-control-m / ratanone@controlm | { "cashflowIds": [ "003690235976","003690235975" ] } | **EXPAND: Response** { "cashflowQueryDataList": [ { "cashflowId": "003690235976", "eventType": "Amendment", "action": "NA", "businessVersion": "2", "cashflowVersion": 2, "minorVersion": 1, "bodyEventRowkey": "STELLA_1816352_0_1829946-1_1001-003690235976-1-ratanone-lifecycle-cashflow-service-PROCESSED-Amendment-d354a9d8-80ca-4682-ad25-2a42ba3c1136", "subStatus": "NA", "nettingId": "11111111111-01", "subStatusEventType": "NA", "subStatusUpdater": "NA", "valueDate": "2022-11-30", "affirmationStatus": "NA", "cashflowStatus": "NETTED", "settlementCurrency": "USD", "settlementAmount": "100", "entityFmid": "10075222", "counterpartyFmid": "400640613", "cfiCode": "SEBXXX", "allotment": "Equity Swap", "productTaxonomy": "Equity:Other" }, { "cashflowId": "003690235975", "eventType": "New", "action": "NA", "businessVersion": "0", "cashflowVersion": 0, "minorVersion": 1, "bodyEventRowkey": "STELLA_1816352_0_1829946-1_1001-003690235975-1-ratanone-lifecycle-cashflow-service-PROCESSED-New-45a524ab-53bf-427b-93bd-76762bb4aa7a", "subStatus": "NA", "nettingId": "11111111111-01", "subStatusEventType": "NA", "subStatusUpdater": "NA", "valueDate": "2022-11-20", "affirmationStatus": "NA", "cashflowStatus": "NETTED", "settlementCurrency": "USD", "settlementAmount": "1008", "entityFmid": "10075222", "counterpartyFmid": "400640613", "cfiCode": "SEBXXX", "allotment": "Equity Swap", "productTaxonomy": "Equity:Other" } ] } **EXPAND_END** | |
| 6 | Job for materialization | POST [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/auto/materialization](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/auto/materialization) Basic auth: ratanone-control-m / ratanone@controlm | Nothing | { "cashflowStatusResponseCode": "SUCCESS", "cashflowStatusProcessingEntities": [...] } | |
| 7 | Hold cashflow | POST [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/hold](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/query) | { "action": "Hold", "comment": "123", "cashflows": [ { "cashflowId": "123", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" }, { "cashflowId": "456", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" } ] } | { "status": "", "errorCode": "", "errorMessage": "" } | |
| 8 | Un-hold cashflow | POST [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/lifecycle/unhold](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/query) | { "action": "UnHold", "comment": "123", "cashflows": [ { "cashflowId": "123", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" }, { "cashflowId": "456", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" } ] } | { "status": "", "errorCode": "", "errorMessage": "" } | |
| 9 | Early Materialization | POST [http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update) User authorization | **EXPAND: Request** { "lifecycleRequests":[ { "cashflowId": "002023032905", "businessVersion": "0", "cashflowVersion": "0", "minorVersion": "6", "updater": "1481696", "nstpReason": "", "comment": "Early Materialize", "ratanAction": "Materialize" }, { "cashflowId": "002023032906", "businessVersion": "0", "cashflowVersion": "0", "minorVersion": "4", "updater": "1481696", "nstpReason": "", "comment": "Early Materialize", "ratanAction": "Materialize" } ] } **EXPAND_END** **EXPAND: Request** { "lifecycleRequests":[ { "cashflowId": "002023032905", "businessVersion": "0", "cashflowVersion": "0", "minorVersion": "6", "updater": "1481696", "nstpReason": "", "comment": "Failed ReInstate", "ratanAction": "ReInstate" }, { "cashflowId": "002023032906", "businessVersion": "0", "cashflowVersion": "0", "minorVersion": "4", "updater": "1481696", "nstpReason": "", "comment": "Failed ReInstate", "ratanAction": "ReInstate" } ] } **EXPAND_END** | { "cashflowStatusResponseCode": "SUCCESS", "cashflowStatusProcessingEntities": [ { "cashflowId": "002023032910", "businessVersion": "0", "cashflowVersion": "0", "action": "Materialize", "updater": "1481696", "previousCashflowIndex": { "minorVersion": "0", "cashflowStatus": { "cashflowEnumMainStatus": "PROJECTED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "nextCashflowIndex": { "minorVersion": "1", "cashflowStatus": { "cashflowEnumMainStatus": "QUEUED", "cashflowEnumSubStatus": "NA", "cashflowEnumSubStatusType": "NA" } }, "cashflowStatusResponseCode": "SUCCESS", "reason": null, "upgrade": false } ] } | |
| 10 | Manual Fail | [http://uklvadapp1340.uk.dev.net:8453/api](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update)/v1/camunda/task/fail | [ { "cashflowId": "eddie2023022301", "cashflowVersion": 0, "businessVersion": 0, "minorVersion": "2" }, { "cashflowId": "eddie2023022303", "cashflowVersion": 0, "businessVersion": 0, "minorVersion": "2" } ] | { "status": "", "errorCode": "", "errorMessage": "" } | |
| 11 | Manual Reinstate | [http://uklvadapp1340.uk.dev.net:8453/api](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update)/v1/camunda/task/reinstate | [ { "cashflowId": "eddie2023022301", "cashflowVersion": 0, "businessVersion": 0, "minorVersion": "2" }, { "cashflowId": "eddie2023022303", "cashflowVersion": 0, "businessVersion": 0, "minorVersion": "2" } ] | { "status": "", "errorCode": "", "errorMessage": "" } | |
| 12 | Swift Suppress Maker | [http://uklvadapp1340.uk.dev.net:8453/api](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update)/v1/ratan/lifecycle/suppress/maker | { "action": "ManualSwiftSuppress", "comment": "123", "cashflows": [ { "cashflowId": "123", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" }, { "cashflowId": "456", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" } ] } | { "status": "", "errorCode": "", "errorMessage": "" } | |
| 13 | Swift Suppress Checker | [http://uklvadapp1340.uk.dev.net:8453/ap](http://uklvadapp1340.uk.dev.net:8453/api/v1/ratan/cashflow/user/status/update)i/v1/ratan/lifecycle/suppress/checker | { "action": "Approve / Reject", "comment": "123", "cashflows": [ { "cashflowId": "123", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" }, { "cashflowId": "456", "businessVersion": "", "cashflowVersion": "", "minorVersion": "" } ] } | { "status": "", "errorCode": "", "errorMessage": "" } | |

**EXPAND_END**

## Events

**EXPAND: Creation - Projected&New**

{
    "messageId":"7ba714be17e84277ab4bcec9819a8d53",
    "aggregateId":"003690235969",
    "aggregateType":"Cashflow",
    "type":"CashflowCreationEvent",
    "payload":{
        "cashflow":{
            "cashflowId":"003690235969",
            "cashflowBusinessVersion":"0",
            "cashflowVersion":"0",
            "cashflowMinorVersion":"0",
            "cashflowStatus":"PROJECTED",
            "cashflowSubStatus":"NA",
            "cashflowSubStatusType":"NA",
            "cashflowSubStatusUpdater":"STELLA",
            "cashflowRowData":"<SCBML>message</SCBML>"
        }
    },
    "version":71203,
    "revision":2,
    "timestamp":1667285771640,
    "metadata":{
        "traceId":"c-74c9c36cf4f3439ba27f8571b4d168cb"
    },
    "status":"PUBLISHED"
}

**EXPAND_END**

**EXPAND: Amendment - Projected&Amend**

{
    "messageId":"8b9dd0dd8a7f42228a3e5286137a970b",
    "aggregateId":"003690235969",
    "aggregateType":"Cashflow",
    "type":"CashflowAmendEvent",
    "payload":{
        "cashflow":{
            "cashflowId":"003690235969",
            "cashflowBusinessVersion":"1",
            "cashflowVersion":"1",
            "cashflowMinorVersion":"2",
            "cashflowStatus":"QUEUED",
            "cashflowSubStatus":"NA",
            "cashflowSubStatusType":"NA",
            "cashflowSubStatusUpdater":"STELLA",
            "cashflowRowData":"<SCBML>message</SCBML>"
        }
    },
    "version":71206,
    "revision":5,
    "timestamp":1667285979782,
    "metadata":{
        "traceId":"c-181322c273394ed6aa92978aaae81eda"
    },
    "status":"PUBLISHED"
}

**EXPAND_END**

**EXPAND: StatusUpdate - Status update**

{
    "messageId":"db04fabc25d54dc1bdb2ac814d2fd7f3",
    "aggregateId":"003690235969",
    "aggregateType":"Cashflow",
    "type":"CashflowStatusUpdateEvent",
    "payload":{
        "cashflow":{
            "cashflowId":"003690235969",
            "cashflowBusinessVersion":"0",
            "cashflowVersion":"0",
            "cashflowMinorVersion":"1",
            "cashflowStatus":"QUEUED",
            "cashflowSubStatus":"NA",
            "cashflowSubStatusType":"NA",
            "cashflowSubStatusUpdater":"1481696"
        }
    },
    "version":71204,
    "revision":3,
    "timestamp":1667285931167,
    "metadata":{
        "traceId":"ab64121631183f77"
    },
    "status":"PUBLISHED"
}

**EXPAND_END**

## Database

Below is a list of questions to be addressed as a result of this requirements document: