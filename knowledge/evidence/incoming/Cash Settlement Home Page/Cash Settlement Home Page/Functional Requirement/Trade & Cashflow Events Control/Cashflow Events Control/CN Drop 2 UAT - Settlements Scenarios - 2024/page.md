| # | Scenario | IRS Trade ID | CCS Trade ID | NDF Trade ID | SCF Trade ID | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | New Booking : Single | 4330391694 | 4330391714 | 4333274674 | 4354273171 | |
| 2 | BTB3/5/7 | 4330389552, BTB Package Id - 395865 | Leg 1 - Outright: 4348268299, BTB Package Id - 405002. | BTB3 NDF - Trade ID - 4330390050 | | |
| 3 | Inter Entity | Leg 1 - Outright: 4348263947, BTB Package Id - 404967 | Package 404965 Trade 4348263943 | | 4354272830, BTB Package Id - 406702 | |
| 4 | Intra Entity | Leg 1 - Outright: 4348263945, BTB Package Id - 404966 | Leg 1 - Outright : 4348263941, BTB Package Id - 404964 | | | |
| 5 | Backdated new booking (Single) | IRS Leg 1 - Outright : 4348265294, | | 4354330764 | | |
| 6 | Backdated new booking (BTB3/5/7) | 4330389552 | 4348268299 | MTC23 - 4354324733, BTB Package Id - 410747 | | |
| 7 | Backdated new booking (Inter Entity) | 4348263947 | 4348263943 | | | |
| 8 | Backdated new booking (Intra Entity) | 4348263945 | 4348263941 | | | |
| 9 | Customised Cashflows (excluding ON Index date customisation) | | | | | |
| 10 | Customised Coupon and spread | 4348265294/ 4354320579 | | | | |
| 11 | Ammortsing Notional | | | | | |
| 12 | Upfront fees (not multiple fees) | 4354284410 | 4330410445 / 4339289521 | | | |
| 13 | AmendmentFee | | | | | |
| 14 | TerminationFee | 4339289519 / 4354320579 | 4354320365 | 4354330764 | | |
| 15 | Novation Fee | | | | | |
| 16 | SCF: Yearly-PL-Sweep (Payment Suppressed) | | | | 4354278027 | |
| 17 | SCF: Compression | | | | 4354278029 | |
| 18 | SCF: XVA-Premium | | | | 4354278025 | |
| 19 | SCF: XVA-Manual * | | | | 407802 Trade id 4354275974 & 4354275975 | |
| 20 | SCF: Funding | | | | 407803, 4354275976 & 4354275977 | |
| 21 | SCF: AGENCY_FEE | | | | 4354278181 | |
| 22 | SCF: Generic | | | | 4354278183 | |
| 23 | IMM roll - Not applicable for China | | | | | |
| 24 | Upfront/End Stubs : Accrual, Termin, Payment Adjustment can be defined | | | | | |
| 25 | Netting | | 4330410445 & 4330404441 4330410490 & 4330410734 | | | |
| 26 | Netting of IRS auto netted cashflow with other product cashflows | | | | | |
| 27 | B2b non-China cash flow suppression | | 4330331504 | | | |
| 28 | Manual Re-Fixing (fix 3 times and check no duplicate payment issue) | | | | | |
| 29 | Auto Re-Fixing (fix 3 times and check no duplicate payment issue) | | | | | |
| 30 | Trade booked via MO Bulk Upload Tool | | | | | |

**Trade Events**

| # | | Scenario | IRS Trade ID | CCS Trade ID | NDF Trade ID | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1A | Amendment (Single) Client Facing - After Payment Release. | Backdated new booking (Single)IRS Leg 1 - Outright : 4348265294, | | 4354325346 | |
| 2 | 1B | Confirm FO got hard block and MO got soft block | | | | Blade ready only by 30 Nov for UAT |
| 3 | 2A | Amendment (BTB3/5/7) - After Payment Release. | | | | |
| 4 | 2B | Confirm FO got hard block and MO got soft block | | | | |
| 5 | 3A | Amendment (Inter Entity) - After Payment Release. | | | | |
| 6 | 3B | Confirm FO got hard block and MO got soft block | | | | |
| 7 | 4A | Amendment (Intra Entity) - After Payment Release. | | | | |
| 8 | 4B | Confirm FO got hard block and MO got soft block | | | | |
| 9 | | Amendment (Single) Client Facing - **Before **Payment Release | | | | |
| 10 | 5A | Cancellation/Withdrawal (Single) - After Payment Release. | | | | |
| 11 | 5B | Confirm FO got hard block and MO got soft block | | | | |
| 12 | 6A | Cancellation/Withdrawal (BTB3/5/7) - After Payment Release. | | | | |
| 13 | 6B | Confirm FO got hard block and MO got soft block | | | | |
| 14 | 7A | Cancellation/Withdrawal (Inter Entity) - After Payment Release. | | | | |
| 15 | 7B | Confirm FO got hard block and MO got soft block | | | | |
| 16 | 8A | Cancellation/Withdrawal (Intra Entity) - After Payment Release. | | | | |
| 17 | 8B | Confirm FO got hard block and MO got soft block | | | | |
| 18 | | Cancellation/Withdrawal (Single) - **Before **Payment Release | | | | |
| 19 | | Partial Early Termination (Issue : Unwind fees cannot be amended) | | 4354320365 | 4354330764 | |
| 20 | | Full Early Termination (Issue : Unwind fees cannot be amended) | 4354311148 | 4354320365 | 4354330764 | |
| 21 | | Upfront Fee (Full Termination) | | | | |
| 22 | | Expiry | | | | |
| 23 | | Portfolio Reassignment - before payment released | 4354284477 | 4354282030, BTB Package Id - 407822 | 4354283045 | |
| 24 | | Portfolio Reassignment - **after **payment released | 4354284410 | 4354283158 | 4354272978/4354273898 | |
| 25 | | Payment Released on original deal + Portfolio Reassignment (in NSTP queue) + Financial Amendment | 4354356503/4354365376 | 4354356592/4354357090 | Not in Scope. (just take note FX product portfolio reassignment is not in scope for CPT so can skip the testing on that for now) | |
| 26 | | Close-Out - Out of scope for Rates. Applicable only for FX | | | | |
| 27 | | Undo on Trade Cancellation: Original Payment not Released: Original Cashflow which went to cancelled status will now become live again | | | | |
| 28 | | Undo on Trade Cancellation: Original Payment released, but Cancellation not yet released: Cancellation will be discarded, original cashflow will remain in Released status | | | | |
| 29 | | Undo on Trade Cancellation: Cancellation (MTx92) Released: FO & MO should not be able to do Undo | | | | |
| 30 | | Undo on Early Termination: Original Payment not Released: Original Cashflow which went to cancelled status will now become live again. Fee not yet released: Fee will be cancelled | | | | |
| 31 | | Undo on Early Termination: Original Payment released, but Cancellation not yet released: Cancellation will be discarded, original cashflow will remain in Released status. Fee not yet released: Fee will be cancelled | | | | |
| 32 | | Undo on Early Termination: Original Payment not Released: Original Cashflow which went to cancelled status will now become live again. Fee is released: MO should not be able to do Undo | | | | |
| 33 | | Undo on Early Termination: Cancellation (MTx92) Released: FO & MO should not be able to do Undo | | | | |
| 34 | | Undo on Cancellation of a confirmed trade | | | | |
| 35 | | Trade Expiry: Trade will not expire if any of the cashflow status is not SETTLED | | | | |
| 36 | | Undo on Expiry: Cashflows generated from Undo will be discarded | | | | |
| 37 | | Novation: Remaining Party Full before Payment Release | | 4330417668 | 4354330764 | |
| 38 | 9A | Novation: Remaining Party Full **after **Payment Release | | | | |
| 39 | 9B | Confirm that FO / MO got Hard Block / Soft Block | | | | |
| 40 | | Backdated Events (covered as part of above in order to trigger settlement since RAZOR UAT env date is 03 Oct) | | | | |
| 41 | | Cancellation after net payment released | | | | |
| 42 | | Amendment after net payment released | | | | |
| 43 | | Amendment before net payment released | | | | |
| 44 | | Cancellation before net payment released | | | | |

**Payment Issues **

| # | Issue Description | | Issue Type | Sample Trade | Priority | Assignee | ADO | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Pending affirmation exception has triggered for reversal cashflow | | Closed | 4354277014/4354280366 | Medium | Eddie | 1834584 | Updated reversal cashflow identifier |
| 2 | NDIRS cashflow from Stella didn't trigger auto-net | | Closed | 4339288251 | Medium | -- | -- | It's due to environment issue when payment flow in, auto-netted after failed and reinstate |
| 3 | NDIRS booked for CNY fixed-floating IRS flowed into RATAN as USD Coupon/float for both leg | | Enhancement in Cortex? | 4348263238 | Pending | | | |
| 4 | NDF New(C1 released) -> Amend amount (N1 released =C1 withdrawal + C2) -> Withdrawal C2 (C2 withdrawal SWIFT_SUPPRESSED for accounting generation, N1 and C1 MT192 will be manually drafted in AMH) | H1 | Enhancement | 4354277014 | H1 | | 3668730 3667427 | NSTP-Alert for withdrawal event without new released |
| 5 | Rebook should be excluded from auto-netting? | Drop2 | Enhancement | 4354311203 | Q2 | | 3706639 | Add ‘Pending Another Leg’ condition into auto-net rebook + reversal to be netted together |
| 6 | Future cash flow revived from queued status after undo Email Subject: future value cash flows has moved to cashflow_suppressed state | Drop2 | Enhancement | 4354311148 | High | Geoffrey | 3706652 | Cashflow to be resumed from projected status after UNDO raised if not released/settled Cashflow to be resumed from released/settled status after UNDO raised if released/settled |
| ~~7~~ | ~~exception triggered as multi vostro but SSI details has not available in checker level. ~~ | | ~~TBD~~ | ~~4354320365~~ | ~~Dropped~~ | | | ~~Didn't see further cases~~ |
| 8 | system as un-net this cash flow 4354325346 & N00000027434 | Drop2 | Closed | 4354325346 | High | Caroline | 3721993 | Filter TDS3 cashflow message which is status_update from RATAN |
| ~~9~~ | ~~SSI Update should not be applicable for withdrawal event~~ | ~~Drop2~~ | ~~Enhancement~~ | ~~004354320443 ~~ | ~~Dropped~~ | | ~~3878077~~ | ~~Enhancement is required to exclude withdrawal event for SSI refresh.~~ |
| 10 | Withdrawal didn't process in RATAN, after ACK post NACK from RAZOR | Drop2 | Enhancement | 004354330765 | Medium | Yang3, Chen | 3885405 | Enhancement to move status to techfail, post NACK from Razor, then withdrawal can be processed to cancel. ACK post NACK from Razor will not be supported. |
| 11 | Undo didn't work for FT CPT - TC 35. That is UNDO termination of TC 2 (Trade id 5068035670) | Drop2 | Defect | 4354505639 | High | Caroline | 3919066 | Tech Issue: 004354505655: Minor version does not match, please validate, expected: [0], request is: [NA] |
| 12 | Rebook didn't show as expected Email Subject: China Drop 2- CPT deals Settlement | Drop2 | | 005068036598 | High | | | LMS |
| 13 | Filter for Stella Cashflows | Drop2 | Enhancement | | Medium | | 3971337 | Create white list for Stella Cashflows Cover #8 scenario also |
| 14 | Duplicate Scenario - Withdrawal after netted Email Subject: Duplicate cash flow has generated for trade 4357280775 | Drop2 | Defect | 4357280775 | High | | 3971687 | No new resultant cashflow generated. |