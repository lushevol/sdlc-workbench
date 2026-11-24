Note: STELLA will handle Cashflow statuses for BCS and EGYPT as per current model

## Cashflow Status List

| **Cashflow Status** | **Process Step** | User Description | **Sent by RATAN to STELLA** |
| --- | --- | --- | --- |
| PROJECTED | STELLA generates cashflow | Cashflow generated but not yet due for settlement | N/A |
| QUEUED | RATAN materializes the Cashflow & checks for exceptions | Cashflow due for settlement | No |
| WAITING | Cashflow has exceptions which require manual action | Cashflow pending for user action | No |
| READY | No exceptions found / Exceptions resolved and waiting for release | Cashflow waiting for auto release to payment gateway | No |
| RELEASED | Cashflow has been Ack’d by FMSRE | Cash flow message has been released to payment gateway | Yes |
| SETTLED | Cashflow has been Ack’s by AMH / SCPAY | Released from payment gateway or no SWIFT required for receipt | Yes |
| NETTED | Cashflow has been Netted in RATAN | Cashflow has been netted part of a netting set and replaced by a net cashflow | Yes |
| SPLIT | Cashflow has been Split in RATAN | Cashflow has been split into multiple payments | Yes |
| CANCELLED | Withdrawal received from upstream into RATAN | Cashflow has been cancelled due to a trade event | No |
| SWIFT SUPPRESSED | Payment / Receipt is Suppressed | Payment / Receipt SWIFT is suppressed but Settlement Accounting will be generated | No |
| CASHFLOW SUPPRESSED | Cashflow is Suppressed (Both SWIFT and Accounting) | No SWIFT or Settlement Accounting will be generated | No (Being sent in BCS model) |
| FAILED | Cashflow is left in WAITING status till EOD | Cashflow not processed and marked as failed by system or user | No |
| DEAD | Un-net is done in RATAN (status is for Net Resultant Cashflow) | Net resultant Cashflow has been cancelled due to Un-net action | No (Net cashflow does not exist in STELLA) |
| HOLD | Cashflow is put on hold in RATAN by user | Cashflow has been put on hold by user | No |
| NOSTRO MATCHED | Payment / Receipt is confirmed in Nostro feed | Cashflow has been successfully reconciled against Nostro statement | TBC (Day 2 Scope) |
| FMSG HOLD | Cashflow requires manual action in FMSG | Cashflow requires manual action in FMSG | TBC (Day 2 Scope) |

## Cashflow Status Movement

![Cashflow status 15 Apr 23.JPG](attachments/Cashflow status 15 Apr 23.JPG)