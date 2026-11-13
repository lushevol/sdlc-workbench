| Scenario | Description | ratan_stella_message_event_source | ratan_cashflow_scbml_history | ratan_cashflow_scbml_message | ratan_cashflow_cutoff_info | ratan_cashflow_holding_message | ratan_cashflow_affirmation_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Cashflow Id is New | Insert | Insert | Insert | Insert | NA | Insert if Affirmed in SCBML |
| 2 | Business version downgrade(late start, early arrival) eg: 005564082752 | Insert | Insert new and update current | Update | Insert | NA | Insert if Affirmed in SCBML |
| 3 | Business version upgrade | Insert | Insert new and update current | Update | Insert | Update current on demand | Insert if Affirmed in SCBML |
| 4 | Business version not change | Update | Insert new and update current | Update | Insert if not exists | Insert on demand | Insert if Affirmed from request |

Scenario 1: Cashflow id is new.

| Table | Entity | Field | Source From | Update Condition |
| --- | --- | --- | --- | --- |
| | | | New | Update | |
| ratan_stella_message_event_source | CashflowMessageEventSource | allotment | | | |
| | | bicNetFlag | | | |
| | | bodyEventRowkey | | | |
| | | bookingSystemEvent | | | |
| | | businessEvent | | | |
| | | businessEventRatan | | | |
| | | businessUnitId | | | |
| | | captureSystem | | | |
| | | cashflowAggId | | | |
| | | cashflowEventReason | | | |
| | | cashflowVersion | | | |
| | | cashflowWorkflowStatus | | | |
| | | cfiCode | | | |
| | | clearingAlpha | | | |
| | | clientType | | | |
| | | counterpartFmcode | | | |
| | | counterpartFmid | | | |
| | | counterpartyBic | | | |
| | | counterpartyDomicileCountry | | | |
| | | countryCode | | | |
| | | createTime | | | |
| | | deliveryMethod | | | |
| | | description | | | |
| | | domainName | | | |
| | | entityFmcode | | | |
| | | entityFmid | | | |
| | | eventDate | | | |
| | | eventType | | | |
| | | initialRatanEvent | | | |
| | | initiatedTimestamp | | | |
| | | isCommodity | | | |
| | | isPva | | | |
| | | isPvb | | | |
| | | isUnnet | | | |
| | | lienMonitor | | | |
| | | majorVersion | | | |
| | | messageSender | | | |
| | | murexFamily | | | |
| | | murexGroup | | | |
| | | murexStrategy | | | |
| | | murexType | | | |
| | | murexTypology | | | |
| | | ndParentTradeId | | | |
| | | ndParentTradeTypology | | | |
| | | nettingId | | | |
| | | originatingTradeId | | | |
| | | passed | | | |
| | | payerParty | | | |
| | | pendingFixingFlag | | | |
| | | portfolioName | | | |
| | | portfolioUniqueName | | | |
| | | prevBusinessEvent | | | |
| | | prevBusinessVersion | | | |
| | | prevCashflowId | | | |
| | | prevCashflowVersion | | | |
| | | prevCashflowWorkflowStatus | | | |
| | | prevEventDate | | | |
| | | prevPayerParty | | | |
| | | prevReceiverParty | | | |
| | | prevSettlementAmount | | | |
| | | prevSettlementCurrency | | | |
| | | prevSettlementDate | | | |
| | | productTaxonomy | | | |
| | | receiverParty | | | |
| | | settlementAmount | | | |
| | | settlementCurrency | | | |
| | | settlementDate | | | |
| | | settlementMethod | | | |
| | | settlementType | | | |
| | | stackFlow | | | |
| | | stpIndicator | | | |
| | | trackingId | | | |
| | | trackingUuid | | | |
| | | tradeId | | | |
| | | tradeOriginalSourceSystem | | | |
| | | tradeVersion | | | |
| | | tradeWorkflowStatus | | | |
| | | versionedTradeId | | | |

| previousStatus | action | nextStatus | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANCELLED+NA+NA | New | PROJECTED+NA+NA | | | | | | | | |
| CANCELLED+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| ERROR+NA+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| ERROR+NA+NA | New | CANCELLED+NA+NA | | | | | | | | |
| ERROR+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | ReInstate | QUEUED+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | Fail | FAILED+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | UnNet | DEAD+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | Net | NETTED+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | Affirmed | QUEUED+Pending Exception+NA | | | | | | | | |
| FAILED+NA+NA | ReInstate | QUEUED+NA+NA | | | | | | | | |
| FAILED+NA+NA | AccountingAck | FAILED+Accounting Acked+NA | | | | | | | | |
| FAILED+NA+NA | UnNet | DEAD+NA+NA | | | | | | | | |
| FAILED+NA+NA | SsiStamped | FAILED+NA+NA | | | | | | | | |
| FAILED+NA+NA | VostroStamped | FAILED+NA+NA | | | | | | | | |
| FAILED+NA+NA | NostroStamped | FAILED+NA+NA | | | | | | | | |
| FAILED+NA+NA | Affirmed | FAILED+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | Amendment | QUEUED+NA+NA | | | | | | | | |
| FAILED+NA+NA | Amendment | QUEUED+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| FAILED+NA+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| FAILED+NA+NA | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| FAILED+NA+NA | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| QUEUED+Pending Exception+NA | New | QUEUED+NA+NA | | | | | | | | |
| FAILED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| HOLD+NA+Pending Verification | UnHold | NA+NA+NA | | | | | | | | |
| HOLD+NA+Pending Verification | UnNet | DEAD+NA+NA | | | | | | | | |
| HOLD+NA+Pending Verification | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| HOLD+NA+Pending Verification | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| HOLD+NA+Pending Verification | Amendment | QUEUED+NA+NA | | | | | | | | |
| QUEUED+Pending Exception+NA | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| QUEUED+Pending Exception+NA | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| HOLD+NA+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| HOLD+NA+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| HOLD+NA+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| NETTED+NA+NA | UnNet | QUEUED+NA+NA | | | | | | | | |
| NETTED+NA+NA | SentToRazor | NETTED+Pending Ack+NA | | | | | | | | |
| NETTED+NA+NA | GenerateSwift | NETTED+Pending Ack+NA | | | | | | | | |
| NETTED+Pending Ack+NA | SentToRazor | NETTED+Pending Ack+NA | | | | | | | | |
| NETTED+Pending Ack+NA | GenerateSwift | NETTED+Pending Ack+NA | | | | | | | | |
| NETTED+Pending Ack+NA | Release | NETTED+Released+NA | | | | | | | | |
| NETTED+Pending Ack+NA | Settle | NETTED+Settled+NA | | | | | | | | |
| NETTED+NA+NA | Release | NETTED+Released+NA | | | | | | | | |
| NETTED+NA+NA | Settle | NETTED+Settled+NA | | | | | | | | |
| NETTED+NA+NA | Net | NETTED+NA+NA | | | | | | | | |
| NETTED+NA+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| NETTED+Pending Ack+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| NETTED+Released+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| NETTED+Released+NA | Settle | NETTED+Settled+NA | | | | | | | | |
| NETTED+Pending Ack+NA | ReplayStatusWriteBack | NETTED+Pending Ack+NA | | | | | | | | |
| NETTED+Released+NA | ReplayStatusWriteBack | NETTED+Released+NA | | | | | | | | |
| NETTED+Settled+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| NETTED+Settled+NA | NostroMatch | NETTED+NostroMatched+NA | | | | | | | | |
| NETTED+Settled+NA | ReplayStatusWriteBack | NETTED+Settled+NA | | | | | | | | |
| NETTED+NostroMatched+NA | ReplayStatusWriteBack | NETTED+NostroMatched+NA | | | | | | | | |
| NETTED+NostroMatched+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| NETTED+NA+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| NETTED+Pending Ack+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| NETTED+Released+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| NETTED+Settled+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| NETTED+NostroMatched+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| NETTED+NA+NA | New | ERROR+NA+NA | | | | | | | | |
| NETTED+Pending Ack+NA | New | ERROR+NA+NA | | | | | | | | |
| NETTED+Released+NA | New | ERROR+NA+NA | | | | | | | | |
| NETTED+Settled+NA | New | ERROR+NA+NA | | | | | | | | |
| NETTED+NostroMatched+NA | New | ERROR+NA+NA | | | | | | | | |
| NA+NA+NA | New | PROJECTED+NA+NA | | | | | | | | |
| NA+NA+NA | Amendment | PROJECTED+NA+NA | | | | | | | | |
| NA+NA+NA | NetNew | QUEUED+NA+NA | | | | | | | | |
| NA+NA+NA | SplitNew | QUEUED+NA+NA | | | | | | | | |
| NA+NA+NA | Withdrawal | ERROR+NA+NA | | | | | | | | |
| NOSTRO_MATCHED+NA+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| NOSTRO_MATCHED+NA+NA | ReplayStatusWriteBack | NOSTRO_MATCHED+NA+NA | | | | | | | | |
| NOSTRO_MATCHED+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| NOSTRO_MATCHED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | Amendment | PROJECTED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | Materialize | QUEUED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | Suppress | CASHFLOW_SUPPRESSED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | Affirmed | PROJECTED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| PROJECTED+NA+NA | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| PROJECTED+NA+NA | Net | NETTED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| PROJECTED+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| PROJECTED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | Amendment | QUEUED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | IsNettingEligible | WAITING+Pending Netting+Pending Operator | | | | | | | | |
| QUEUED+NA+NA | WaitingAnotherLeg | WAITING+Pending Another Leg+Pending Operator | | | | | | | | |
| QUEUED+NA+NA | IsAutoNettingEligible | WAITING+Auto Netting+NA | | | | | | | | |
| QUEUED+NA+NA | IsNstp | WAITING+Pending Exception+Pending Operator | | | | | | | | |
| QUEUED+NA+NA | IsNstpChecker | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| QUEUED+NA+NA | ValidateDirect | READY+NA+NA | | | | | | | | |
| QUEUED+NA+NA | Net | NETTED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | SwiftSuppress | SWIFT_SUPPRESSED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | Suppress | CASHFLOW_SUPPRESSED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| QUEUED+NA+NA | UnNet | DEAD+NA+NA | | | | | | | | |
| QUEUED+NA+NA | UnSplit | DEAD+NA+NA | | | | | | | | |
| QUEUED+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| QUEUED+NA+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | SsiStamped | QUEUED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | NostroStamped | QUEUED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | VostroStamped | QUEUED+NA+NA | | | | | | | | |
| QUEUED+NA+NA | Split | SPLIT+NA+NA | | | | | | | | |
| QUEUED+NA+NA | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| QUEUED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| READY+Pending Ack+NA | Release | RELEASED+NA+NA | | | | | | | | |
| READY+Pending Ack+NA | SwiftUpdate | READY+Pending Ack+NA | | | | | | | | |
| READY+Pending Ack+NA | Settle | SETTLED+NA+NA | | | | | | | | |
| READY+Pending Ack+NA | ResendToRazor | READY+Pending Ack+NA | | | | | | | | |
| READY+Pending Ack+NA | ReGenerateSwift | READY+Pending Ack+NA | | | | | | | | |
| READY+Pending Ack+NA | Suppress | CASHFLOW_SUPPRESSED+NA+NA | | | | | | | | |
| READY+Pending Ack+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| READY+Pending Ack+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| READY+Pending Ack+NA | Fail | FAILED+NA+NA | | | | | | | | |
| READY+Pending Ack+NA | New | QUEUED+NA+NA | | | | | | | | |
| READY+NA+NA | Amendment | QUEUED+NA+NA | | | | | | | | |
| READY+NA+NA | Release | RELEASED+NA+NA | | | | | | | | |
| READY+NA+NA | RevertPenVerfication | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| READY+NA+NA | IsNstpChecker | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| READY+NA+NA | IsNstp | WAITING+Pending Exception+Pending Operator | | | | | | | | |
| READY+NA+NA | SettleDirect | SETTLED+NA+NA | | | | | | | | |
| READY+NA+NA | SentToRazor | READY+Pending Ack+NA | | | | | | | | |
| READY+NA+NA | GenerateSwift | READY+Pending Ack+NA | | | | | | | | |
| READY+NA+NA | EarlyRelease | READY+NA+NA | | | | | | | | |
| READY+NA+NA | UnNet | DEAD+NA+NA | | | | | | | | |
| READY+NA+NA | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| READY+NA+NA | Suppress | CASHFLOW_SUPPRESSED+NA+NA | | | | | | | | |
| READY+NA+NA | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| READY+NA+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| READY+NA+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| READY+NA+NA | Net | NETTED+NA+NA | | | | | | | | |
| READY+NA+NA | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| READY+NA+NA | Split | SPLIT+NA+NA | | | | | | | | |
| READY+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| READY+NA+NA | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| READY+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| RELEASED+NA+NA | Settle | SETTLED+NA+NA | | | | | | | | |
| RELEASED+NA+NA | ReplayStatusWriteBack | RELEASED+NA+NA | | | | | | | | |
| RELEASED+NA+NA | SwiftUpdate | RELEASED+NA+NA | | | | | | | | |
| RELEASED+NA+NA | ManualSettle | RELEASED+Manual Settle+Pending Verification | | | | | | | | |
| RELEASED+Manual Settle+Pending Verification | Approve | SETTLED+NA+NA | | | | | | | | |
| RELEASED+Manual Settle+Pending Verification | Reject | NA+NA+NA | | | | | | | | |
| RELEASED+Manual Settle+Pending Verification | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| RELEASED+Manual Settle+Pending Verification | Settle | SETTLED+NA+NA | | | | | | | | |
| RELEASED+NA+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| RELEASED+NA+NA | Fail | RELEASED+NA+NA | | | | | | | | |
| RELEASED+Manual Settle+Pending Verification | Fail | RELEASED+NA+NA | | | | | | | | |
| RELEASED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| RELEASED+Manual Settle+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| SETTLED+NA+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| SETTLED+NA+NA | ReplayStatusWriteBack | SETTLED+NA+NA | | | | | | | | |
| SETTLED+NA+NA | SwiftUpdate | SETTLED+NA+NA | | | | | | | | |
| SETTLED+NA+NA | NostroMatch | NOSTRO_MATCHED+NA+NA | | | | | | | | |
| SETTLED+NA+NA | Fail | SETTLED+NA+NA | | | | | | | | |
| SETTLED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| SPLIT+NA+NA | UnSplit | QUEUED+NA+NA | | | | | | | | |
| SPLIT+NA+NA | Release | SPLIT+Released+NA | | | | | | | | |
| SPLIT+Released+NA | Settle | SPLIT+Settled+NA | | | | | | | | |
| SPLIT+Settled+NA | NostroMatch | SPLIT+NostroMatched+NA | | | | | | | | |
| SPLIT+Released+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| SPLIT+Settled+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| SPLIT+NostroMatched+NA | Withdrawal | QUEUED+NA+NA | | | | | | | | |
| SPLIT+NA+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| SPLIT+Released+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| SPLIT+Settled+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| SPLIT+NostroMatched+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| SPLIT+NA+NA | New | ERROR+NA+NA | | | | | | | | |
| SPLIT+Released+NA | New | ERROR+NA+NA | | | | | | | | |
| SPLIT+Settled+NA | New | ERROR+NA+NA | | | | | | | | |
| SPLIT+NostroMatched+NA | New | ERROR+NA+NA | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | UnSuppress | QUEUED+NA+NA | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | ManualUnSuppress | WAITING+Undo Cashflow Suppression+Pending Verification | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | UnNet | DEAD+NA+NA | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | Amendment | QUEUED+NA+NA | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| CASHFLOW_SUPPRESSED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | ManualSwiftUnSuppress | WAITING+Undo Swift Suppression+Pending Verification | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | Fail | FAILED+NA+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | AccountingAck | SWIFT_SUPPRESSED+Accounting Acked+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | SsiStamped | SWIFT_SUPPRESSED+NA+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | NostroStamped | SWIFT_SUPPRESSED+NA+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | UnNet | DEAD+NA+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | VostroStamped | SWIFT_SUPPRESSED+NA+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| SWIFT_SUPPRESSED+NA+NA | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Submit | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | ApproveOnlyMaker | READY+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Reject | WAITING+Pending Exception+Pending Operator | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | SsiStamped | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | NostroStamped | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | VostroStamped | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | PaymentDateUpdate | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Affirmed | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Affirmed | WAITING+Pending Exception+Pending Operator | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | Affirmed | WAITING+Pending Netting+Pending Operator | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | ManualAffirmed | WAITING+Pending Exception+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | ManualAffirmed | WAITING+Pending Exception+Pending Operator | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | NostroStamped | WAITING+Pending Netting+Pending Operator | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | VostroStamped | WAITING+Pending Netting+Pending Operator | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | SsiStamped | WAITING+Pending Netting+Pending Operator | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | SettleAsGross | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Approve | READY+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | Approve | READY+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | UnNet | DEAD+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | UnNet | DEAD+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | UnNet | DEAD+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | NostroStamped | WAITING+Pending Another Leg+Pending Operator | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | NostroStamped | WAITING+Pending Another Leg+Pending Operator | | | | | | | | |
| WAITING+Pending Another Leg+NA | VostroStamped | WAITING+Pending Another Leg+Pending Operator | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | VostroStamped | WAITING+Pending Another Leg+Pending Operator | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | ManualStp | QUEUED+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | AutoStp | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | SsiStamped | WAITING+Pending Another Leg+Pending Operator | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | SsiStamped | WAITING+Pending Another Leg+Pending Operator | | | | | | | | |
| WAITING+Pending Another Leg+NA | SettleAsGross | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | SettleAsGross | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Split | SPLIT+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Split | SPLIT+NA+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | Split | SPLIT+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | Split | SPLIT+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | Split | SPLIT+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | Split | SPLIT+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | Split | SPLIT+NA+NA | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | Net | NETTED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | TechFail | QUEUED+Pending Exception+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Netting Review+Pending Verification | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Pending Another Leg+NA | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | Hold | HOLD+NA+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | RevertToQueued | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | Amendment | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Netting Review+Pending Verification | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Another Leg+NA | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | ManualSuppress | WAITING+Cashflow Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Netting Review+Pending Verification | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Another Leg+NA | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | ManualSwiftSuppress | WAITING+Swift Suppression+Pending Verification | | | | | | | | |
| WAITING+Cashflow Suppression+Pending Verification | UnNet | DEAD+NA+NA | | | | | | | | |
| WAITING+Cashflow Suppression+Pending Verification | Reject | NA+NA+NA | | | | | | | | |
| WAITING+Cashflow Suppression+Pending Verification | Approve | CASHFLOW_SUPPRESSED+NA+NA | | | | | | | | |
| WAITING+Undo Cashflow Suppression+Pending Verification | UnNet | DEAD+NA+NA | | | | | | | | |
| WAITING+Undo Cashflow Suppression+Pending Verification | Reject | NA+NA+NA | | | | | | | | |
| WAITING+Undo Cashflow Suppression+Pending Verification | Approve | QUEUED+NA+NA | | | | | | | | |
| WAITING+Swift Suppression+Pending Verification | UnNet | DEAD+NA+NA | | | | | | | | |
| WAITING+Swift Suppression+Pending Verification | Reject | NA+NA+NA | | | | | | | | |
| WAITING+Swift Suppression+Pending Verification | Approve | SWIFT_SUPPRESSED+NA+NA | | | | | | | | |
| WAITING+Undo Swift Suppression+Pending Verification | UnNet | DEAD+NA+NA | | | | | | | | |
| WAITING+Undo Swift Suppression+Pending Verification | Reject | NA+NA+NA | | | | | | | | |
| WAITING+Undo Swift Suppression+Pending Verification | Approve | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Cashflow Suppression+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Undo Cashflow Suppression+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Swift Suppression+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Undo Swift Suppression+Pending Verification | Withdrawal | CANCELLED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Cashflow Suppression+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Undo Cashflow Suppression+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Swift Suppression+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Undo Swift Suppression+Pending Verification | Fail | FAILED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | TestFail | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Operator | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Exception+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Netting+Pending Operator | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Netting Review+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+NA | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Another Leg+Pending Operator | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Reversal Rebook+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Pending Netting 4 Withdrawal+Pending Operator | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Cashflow Suppression+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Undo Cashflow Suppression+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Swift Suppression+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |
| WAITING+Undo Swift Suppression+Pending Verification | New | QUEUED+NA+NA | | | | | | | | |