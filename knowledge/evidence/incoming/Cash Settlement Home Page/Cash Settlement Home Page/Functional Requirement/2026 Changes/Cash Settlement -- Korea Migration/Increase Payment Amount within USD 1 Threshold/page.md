##

## Background

One of the pain points Ops face is decimal difference on our payments vs Counterparty expectation (due to rounding differences). Generally, Ops team always affirm with clients before value date or on value date. And the modification could be done before cashflow been settled.

Some of the clients are insistent that we need to pay the exact decimal amount as per their books for Audit purpose.

- When our payment amount is higher example: xxxx5.02 on our side vs xxxx5.01 on client side, Setts will split the amount, pay xxxx.01 and suppress the remaining 0.01
- When our payment amount is lower example xxxx7.01 on our side vs xxxx7.02 on client side, Setts team suppress the payment in Ratan and do a manual payment via Oscar.

This has risk of manual error, hence team is requesting a feature to allow increase of payment amount within a threshold (USD 1 equivalent) with maker / checker.

Impact volume:

## Story Link

[Story 14047448 Update Amount on Payment within USD 1 threshold](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14047448)

## Payment Scope

1. Any cashflow amount could be updated
2. Amount can be updated for **any currency（ Exclude precious metal currency，which currency code start with 'X'）**
3. Amount can be updated up to maximum of USD 1 **equivalent (<1 USD, not include =1 USD). **
4. Amount can be amended only before cashflow is released to downstream.
5. Need to support this on **any cashflow gross**, **net resultant** (including bilateral, BIC netting, Inter Entity Netting, Aggregation resultant), **split parent cashflow(Cashflow ID not start with 'S')**.
6. When cashflow had been adjusted, it can't be netted.
7. Not allowed adjust amount on split resultant cashflows.
8. When amount-adjusted cashflow **revert to QUEUED** status, keep the adjust amount.
9. Amount amendment must be via Maker +Checker. - Cashflow detail page must **highlight the adjusted amount** for Checker. - Ability for Checker to reject to Maker if there is an error made by Maker.
10. Payment Swift must be generated for the adjusted amount – applies to **all swift formats**(MT/MX), including Flip MT202.
11. Settlement Accounting must be based on **original** cashflow amount only
12. Downstream FMSWG, ENISIS, and LMS will be impacted.

## Business Scenarios

| Number | Description | Comments |
| --- | --- | --- |
| 1 | Adjust amount on Simple cashflow C1(Waiting) + Settle + Withdrawal C1 | |
| 2 | Adjust amount on Simple cashflow C1(Ready) + Settle + Withdrawal C1 | |
| 3 | Adjust amount on Net resultant cashflow N1(Waiting +Pending Operator +Pending Exception) + Settle N1 + Withdrawal component cashflow + Net reversal leg and rebook leg->N2 | The amount difference on N1 will not impact N2 |
| 4 | Adjust amount on Net resultant cashflow N3(Ready+ NA +NA) + Settle N3 + Withdrawal component cashflow + Net reversal leg and rebook leg->N4 | The amount difference on N3 will not impact N4 |
| 5 | Not allow net amount-adjusted cashflow. Component cashflow C4 (Ready+ NA +NA) Adjust C4 amount New C5 Try to net C4 and C5—not allowed Cancel C4's adjust amount Net C4 and C5, →N3 Adjust N3 Settle N3 | |
| 6 | Not allow amount-adjust on split resultant cashflow. Simple cashflow P1 Adjust P1 Split P1 → S1, S2 Not allow tweak amount on S1 &S2(if would like to adjust amount on S1, please unsplit → adjust P1's amount→ split P1 again) | If allow to adjust on split resultant cashflow, the sum of S1's adjust amount and S2's adjust amount will be exceed 1 USD, This will not be expected. |
| 7 | Simple cashflow C6 in (Ready+ NA +NA) from **MUREX** Adjust C6 amount Withdrawal C6 New C7 to replace C6, C7 will not inherit C6‘ adjust amount. | |
| 8 | Simple cashflow C8 in (Ready+ NA +NA) from **STELLA** Adjust C8 amount Withdrawal C8 New C9 to replace C8, C8 will not inherit C8‘ adjust amount. | |
| 9 | When amount-adjusted cashflow revert to QUEUE, keep the adjust amount. | |
| 10 | Not support precious metal cashflow | |
| 11 | Cashflows with not USD currency cases. | |

## FrontEnd requirement

1. In Cashflow Detail window, add 'Adjust amount' module following 'Original Amount'.
2. [O](https://confluence.global.standardchartered.com/display/DSP/Increase+Payment+Amount+within+USD+1+Threshold)nly Maker have access to fill adjust amount field.
3. Only when cashflow status is **'Waiting + Pending Operator + Pending Exception' & Exception code not include 'Pending NDS Netting'** or** 'Ready + NA + NA',** 'Adjust amount' could be edit.
4. When click 'Adjust amount' window, will prompt amount scope. The amount scope need to be got when open Cashflow Detail window.
5. 'Adjust amount' edit box will **limit the number of decimal places** of the corresponding currency, will **limit amount scope**.
6. After modify 'Adjust amount',** highlight **'Adjust amount' field. All users could see it if only have read only access.
7. If maker set value of 'Adjust amount' is 'null'. Then checker won't see field 'Adjust amount'.
8. Amount can be updated for **any currency（Exclude PM CCY，start with 'X'）**

## Backend requirement

1. When open Cashflow Detail window, will call backend API, should return this cashflow's amount modify scope. For example, cashflow amount is 100 USD, return scope [99.01 USD – 100.99 USD].
2. Backend will log this in cashflow history. Add new action 'TweakAmount' and 'unTweakAmount'.
3. After maker(the first user) submit cashflow(not only adjust amount, but make sure has affirmed all items under multi exception list which are pending operator), frontend will send all cashflow information to backend, and backend should validate (CCY code, scope, the number of decimal places) and restore it in DB. Log this action as 'TweakAmount'.
4. Set 2 Checker-only NSTP rules: Adjusted Amount Cashflow Exception & Cancel Adjust Amount Cashflow.
5. If Ops update the amount again, front end will send new value to backend. Backend should overwrite old value with new value. Log this action as 'TweakAmount'.
6. If Ops delete adjust amount, front end will send 'null' to backend. Backend should overwrite old value with 'null'. Log this action as 'unTweakAmount'.
7. Checker only could approve or reject adjust amount. Checker don't have access to adjust amount.

## Status Flow

Only cashflow status in 'Waiting +Pending Operator Pending Exception' & Exception code not include 'Pending NDS Netting' or 'Ready +NA +NA', are applicable to amend amount.

1. Only cashflow status in '**Waiting +Pending Operator +Pending Exception**' **& Exception code not include 'Pending NDS Netting'** or 'Ready + NA +NA', maker could 'TweakAmount' or 'unTweakAmount'. Then status will reach 'Waiting+ Pending Verification + Pending Exception'.
2. Then Checker could see the highlighted amount and need to approve/reject the amendment. If approve, status reach to 'Ready'. If reject, status will back to 'Waiting +Pending Operator Pending Exception'.

| | Source Cashflow Status | Source Cashflow Sub Status | Source Cashflow Sub Status Type | If adjust amount | Action | Target Cashflow Status | Target Cashflow Sub Status | Target Cashflow Sub Status Type | If adjust amount |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | WAITING | Pending Operator | Pending Exception + Other Exception | Null | TweakAmount | WAITING | Pending Verification | Pending Exception+ Other Exception+ AdjustAmountException | Y |
| 2 | READY | NA | NA | Null | TweakAmount | WAITING | Pending Verification | Pending Exception+ AdjustAmountException | Y |
| 3 | READY | NA | NA+AdjustAmount | Y | UnTweakAmount | WAITING | Pending Verification | Pending Exception + UnAdjust Amount Exception | Null |
| 4 | WAITING | Pending Verification | Pending Exception+ Other Exception+ AdjustAmountException | Y | Approve | READY | NA | NA | Y |
| 5 | WAITING | Pending Verification | Pending Exception+ Other Exception+ AdjustAmountException | Y | Reject | WAITING | Pending Operator | Pending Exception + Other Exception +AdjustAmountException | Null |
| 6 | WAITING | Pending Verification | Pending Exception + Adjust Amount Exception | Y | Approve | READY | NA | NA | Y |
| 7 | WAITING | Pending Verification | Pending Exception + Adjust Amount Exception | Y | Reject Adjust Amount | WAITING | Pending Operator | Pending Exception + AdjustAmountException | Null |
| 8 | WAITING | Pending Verification | Pending Exception + UnAdjust Amount Exception | Null | Approve | READY | NA | NA | Null |
| 9 | WAITING | Pending Verification | Pending Exception + UnAdjust Amount Exception | Null | Reject UnAdjust Amount | WAITING | Pending Operator | Pending Exception + UnAdjustAmountException | Y |
| 10 | WAITING | Pending Operator | Pending Exception + AdjustAmountException | Null | TweakAmount | WAITING | Pending Verification | Pending Exception + Adjust Amount Exception | Y |
| 11 | WAITING | Pending Operator | Pending Exception + AdjustAmountException | Null | UnTweakAmount | WAITING | Pending Verification | Pending Exception + UnAdjust Amount Exception | Null |
| 12 | WAITING | Pending Operator | Pending Exception + UnAdjustAmountException | Y | TweakAmount | WAITING | Pending Verification | Pending Exception+ AdjustAmountException | Y |
| 13 | WAITING | Pending Operator | Pending Exception + UnAdjustAmountException | Y | UnTweakAmount | WAITING | Pending Verification | Pending Exception + UnAdjust Amount Exception | Null |

## Analysis on upstream and downstream

| Related Function | Upstream/downstream | Impacted or not | Open Questions | Email & SPOC | Comments | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TP system | Murex GDC, Murex Korea, Blade(Stella) | No | If need to write back to upstream? No need. | | Need to let TP system know this change | In progress |
| Accounting system | EBBS, Aspire, OLTP | No | Why does not need change amount to accounting system? As this requirement mainly focus on Nostro recon, so the scope only focus on Swift messages. | | Need to let accounting system know this change | In progress |
| Reporting system | (DQSL) SSDR, FMMIS | No | | | Need to let reporting system know this change | In progress |
| Confirmation | CDUPS | No | | | Need to let CDUPS system know this change | In progress |
| Liquidity | LMS | Yes. | 2026-07-28 Dinesh, Arockia <K.[A.Dinesh@sc.com](mailto:A.Dinesh@sc.com)>Specifically LMS wanted the adjusted amount in their feed. 2026-07-06 From Nivethitha to RATAN The ask is instead of the original amount in the FMRP message to LMS can you send the Adjusted amount? | Subject: RE: Update Amount on Payment Swift From Nivethitha | Need to arrange UAT with LMS | In progress |
| | FXU | No | | | As no swift message generated for FXU | Done |
| Swift | FM Swift Gateway, ENISIS | Yes. | | | Need to arrange UAT with Swift systems | In progress |
| | Razor(LoanIQ swift) | No | Should amount amendment on LoanIQ cashflows? No need. As RATAN did not feed LoanIQ payment amount. | | | Done |
| Recon | TLM | No. | | Subject: Increase Payment Amount within USD 1 Threshold George, Vinish | Need to arrange UAT with TLM | In progress |
| Precious Metal | NA | No | 2026-07-06 From Dinesh to Vivek Realistically PM ccy decimal difference will be more than 1 USD. . [@Aggarwal, Vivek](mailto:Vivek.Aggarwal@sc.com), please let know your feedback. For splitting, you had requested to put a hard block in Ratan on PM ccys since CIS will have an issue. What about decimal difference adjustment? | Subject: RE: Update Amount on Payment Swift Aggarwal, Vivek | Need to do FIT internally | In progress |

## User Cases

When we consider withdrawal scenarios

1. Single cashflow(positive case +withdrawal)
2. Net resultant cashflow(bilateral netting, BIC netting, Inter Entity Netting, Aggregation resultant, manual netting), withdrawal component cashflow.
3. Split resultant cashflow
4. Consider other actions: hold/unhold, Net/unNet, Send to waiting.

| 1. Simple cashflow (Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Settle + Withdrawal |
| --- |
| | Steps | Expected result | Testing Result |
| | Simple cashflow which won't be netted or splitted. Status in 'Waiting +Pending Operator +Pending Exception' . **not include 'Pending NDS Netting' exception code.** Cashflow C1 | C1 in 'Waiting +Pending Operator +Pending Exception' | |
| | Maker fill in adjusted amount, and process other exceptions. Submit. | C1 in 'Waiting +Pending Verification+Pending Exception' | |
| | Checker approve cashflow. Cashflow C1 be settled. | Swift message with *adjusted amount*; Accounting message with original amount; LMS message with *adjusted amount*. | |
| | Withdrawal this cashflow, and process by maker and checker. | Swift message with adjusted amount; Accounting message with original amount. LMS message with adjusted amount. | |
| 2. Simple cashflow (Ready +NA +NA) + <u>Adjust amount</u> + Settle + Withdrawal component cashflow |
| | Steps | Expected result | |
| | Simple cashflow which won't be netted or splited. Status in 'Ready +NA +NA' | | |
| | Maker fill in adjusted amount, and process other exceptions. Submit. | | |
| | Checker approve cashflow. Cashflow will be settled. | Swift message with adjusted amount; Accounting message with original amount; LMS message with adjusted amount. | |
| | Withdrawal this cashflow. | Swift message with adjusted amount; Accounting message with original amount. LMS message with adjusted amount. | |
| 3. Netting resultant cashflow(Bilateral Netting) (Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Withdrawal Component cashflow & UnNet netting resultant cashflow |
| | Steps | Expected result | |
| | Bilateral netting cashflow which status in 'Ready +NA +NA' | | |
| | Maker fill in adjusted amount. Submit. Checker approve cashflow. Status in 'Ready +NA +NA'. | | |
| | Withdrawal Component cashflow, UnNet netting resultant cashflow. | | |
| 3. Netting resultant cashflow(Bilateral Netting) (Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Early Settled+ EcoAmend+ Netting + Settled |
| | Steps | Expected result | |
| | Bilateral netting cashflow N1(C1 + C2) which status in 'Ready +NA +NA' | | |
| | Maker fill in *adjusted amount* in N1. Submit. Checker approve cashflow. Status in 'Ready +NA +NA'. | | |
| | Settle N1. | Swift message with adjusted amount; Accounting message with original amount; LMS message with adjusted amount. | |
| | C1 reversal by C3, C4 is rebook of C1. Net C3 and C4 → N2. Settle N2. | Process N2 as usual | |
| 4. Netting resultant cashflow(BIC Netting) (Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Settle + Withdrawal Component cashflow |
| | Steps | Expected result | |
| | Netting resultant cashflow which status in 'Ready +NA +NA' Maker fill in adjusted amount, and process other exceptions. Submit. Checker approve cashflow. Net resultant cashflow be settled. Withdrawal component cashflow. | | |
| 5. Netting resultant cashflow(Inter Entity Netting) (Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Settle + Withdrawal Component cashflow |
| | Steps | Expected result | |
| | Netting resultant cashflow which status in 'Ready +NA +NA' Maker fill in adjusted amount, and process other exceptions. Submit. Checker approve cashflow. Net resultant cashflow be settled. Withdrawal component cashflow. | | |
| 6. Netting resultant cashflow(Aggregation resultant) (Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Settle + Withdrawal Component cashflow |
| | Steps | Expected result | |
| | Netting resultant cashflow which status in 'Ready +NA +NA' Maker fill in adjusted amount, and process other exceptions. Submit. Checker approve cashflow. Net resultant cashflow be settled. Withdrawal component cashflow. | | |
| 7. Netting resultant cashflow(Manual Netting) (Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Settle + Withdrawal Component cashflow |
| | Steps | Expected result | |
| | Netting resultant cashflow which status in 'Ready +NA +NA' Maker fill in adjusted amount, and process other exceptions. Submit. Checker approve cashflow. Net resultant cashflow be settled. Withdrawal component cashflow. | | |
| 8. Split resultant cashflow(Waiting +Pending Operator +Pending Exception) + <u>Adjust amount</u> + Settle + Withdrawal parent cashflow |
| | Steps | Expected result | |
| | Split resultant cashflow which status in 'Waiting +Pending Operator +Pending Exception' | | |
| | Maker fill in adjusted amount, and process other exceptions. Submit. | | |
| | Checker approve cashflow. Cashflow will be settled. | Swift message with adjusted amount; Accounting message with original amount; LMS message with adjusted amount. | |
| | Withdrawal parent cashflow | Swift message with adjusted amount; Accounting message with original amount; LMS message with adjusted amount. | |
| 9. 'Send to Waiting' after adjust amount. |
| | Steps | Expected result | |
| | Simple cashflow which won't be netted or splitted. Status in 'Ready +NA +NA' Maker fill in *adjusted amount*, and process other exceptions. Submit. Checker approve cashflow. Status in 'Ready +NA +NA'. Hold cashflow, RevertToQueued cashflow | Adjust amount keep same. | |
| 10. No Eco amendment. |
| | Steps | Expected result | |
| | Simple cashflow which won't be netted or splitted. Status in 'Ready +NA +NA' Maker fill in *adjusted amount*, and process other exceptions. Submit. Checker approve cashflow. Status in 'Ready +NA +NA'. Push no eco amendment cashflow into group. | No impact on original C1. Adjust amount keep same. | |

## Technical Solution

FrontEnd Demo

![image-2026-9-29_17-36-54.png](attachments/image-2026-9-29_17-36-54.png)

**RATAN-CASH-SETTLEMENT-LMS-SERVICE**

**RATAN-CASH-SETTLEMENT-NETTING-SERVICE**

**RATAN-CASH-SETTLEMENT-QUERY-SERVICE**

**RATAN-CASHFLOW-LIFECYCLE-SERVICE**

**RATANONE-SWIFT-SERVICE**

## Schedule

| Phases | Start Day &Time | End Day & Time | Comments |
| --- | --- | --- | --- |
| Analysis | 14-Sep-2026 | 25-Sep-2026 | |
| Dev | 21-Sep-2026 | 16-Oct-2026 | |
| SIT | 16-Oct-2026 | 30-Oct-2026 | |
| UAT | 23-Oct-2026 | 30-Oct-2026 | |
| Regression Testing | 30-Oct-2026 | 7-Nov-2026 | |
| Preparations before go live | 7-Nov-2026 | 14-Nov-2026 | |
| Go live | 14-Nov-2026 | 14-Nov-2026 | |
| Post Go live | 14-Nov-2026 | 21-Nov-2026 | |

## Contract

| System | Contract |
| --- | --- |
| Ratan | Geoffrey, Song Yinghua |
| LMS | BA: Foong, Wei Mun <WeiMun.Foong@[sc.com](http://sc.com)> |
| FMSWG | Yang, Nicole Liu |
| ENISIS | Park, Jung Hyeon |
| TLM | Sittrarasu, Balaji |
| SSDR | Cherry, Lv Wenjie |
| FMMIS | Lv Wenjie |
| EBBS | Devlal Munde, Neha |
| OLTP | Jin, Yeon Su |
| ASPIRE | Sittrarasu, Balaji |
| Murex GDC | |
| Murex Korea | |
| Blade | |
| CDUPS | |

## Reference table:

select * from ratan_cashflow_lifecycle_service.ratan_cashflow_rounding_config rcrc

## Open Questions

| Number | Question | Answer | Status |
| --- | --- | --- | --- |
| 1 | Would like to limit adjust on split resultant cashflow, but could do adjust amount on split parent cashflow. | Only allow adjust amount on split parent cashflow. [2-RE Increase Payment Amount within USD 1 Threshold.msg](https://dev.azure.com/sc-ado/777f0ba6-cfdf-4f44-99dd-ae1dc434f5c5/_apis/wit/attachments/eebfe018-d57f-4896-8937-21fd12c9a7e1?fileName=2-RE%20Increase%20Payment%20Amount%20within%20USD%201%20Threshold.msg&download=true) | Close. |
| 2 | What is current action after rebook one in Oscar? Is there any link between the one in Ratan and the one in Oscar? | | Open |
| 3 | How many of cashflows need to adjust amount of different entity? | | Open |
| 4 | Is the difference in amount adjustment < $1 or <=$1? | Dinesh: for safety, only <1 USD. | Close |
| 5 | How to do UAT? Who will provide UAT sign off? | | Open |
| 6 | Real samples which need to adjust | | |

## Reference Link

[LMS Feed - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/LMS+Feed)

[Status Machine - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Status+Machine)

[Ratan One Processing Guide (DOI) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2863770766#RatanOneProcessingGuide(DOI)-Login)

[FMRP Swift Generation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)

[RATAN to ENISIS - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+to+ENISIS)