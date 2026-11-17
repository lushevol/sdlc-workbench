## Trade Confirmation/Validation Flow Background

1. Trade confirmation: Internal counterparty and SCF deals from Murex would be auto confirmed and confirmation won't be available in CDU, and quite a number of payments are pending for affirmation in BAU
2. Trade validation: Settlement ops would like to process payment only when trade validation done which would happen after cashflow flow into Ratan
3. Both trade confirmation and validation status would be available in TDS3

## Principle

1. Source trade status (confirmation & validation) from TDS3 for FMRP and Murex, maintain trade key information in Ratan, CDUPS dependency is only for FX SWAP near leg confirmation (TBD)
2. Trade validated condtion: 1. FMRP: trade id + major version + status ( SENT, AFFIRMED, CONFIRMED, TOBESENT+Validate[action] ) 2. Murex: trade id + status (VALD, COMP)
3. FMRP trade validation will take effect on trade id and major version backward (like major version 4 will be seen as 1,2,3 validated)
4. Murex trade validation will only take effect based on trade id
5. Group will be PENDING until all cashflows arrived
6. Group will be PENDING_TRADE_VALIDATION if all cashflows arrived but found trade not validated
7. Cashflow will be OFFSET if when both new/withdrawal arrived and PENDING
8. Maintain trade status within ratan-cashflow-standarlization-service (group service), support trade status query within settlement domain

| | Option 1 (Preferred 2024-05-29 ) | ~~Option 2~~ |
| --- | --- | --- |
| | | |
| High Level Design | | |
| Group service | 1. Add one more control, hold messages when trade not validated 2. Publish to workflow after 1. Group completed 2. AND Trade Validated 3. Function "Manual STP" to be disabled for items with trade not validated | Logic enhancement to get confirmation/valid status |
| Lifecycle service | No Change | 1. Create a new status TOBEVALIDATED before PROJECTED 2. Query on group service for trade validation check |
| PROs | No change in current main workflow/lifecycle | 1. Clear status to OPS on cashflows with trade not validated 2. Clear responsibility of domain service that 1. lifecycle service to control cashflow status movement and workflow for STP 2. group service maintains only group management |
| CONs | 1. ~~Unclear domain service responsibility, Standardization (group) service participate on the cashflow lifecycle management other than only group management 2024-05-29 Additional requirement which is not cashflow lifecycle, but control before it.~~ 2. Users can not have an overview from cashflow blotter, they will need to check both blotters, and group blotter can support only simple queries 2024-05-29 summary in dashboard 3. On amendment, cashflow holding in group will probably lead to unnecessary payments 2024-05-29 control on this case is not must have as this is Murex current behavior, better to have a hold control 1. C1 in Waiting, T1 V1 validated 2. C1 W + C2 N come, but stuck because of T1 V2 not validated 3. C1 settled 4. T1V2 validation late 5. C1 W + C2 N to be settled | 1. Changes in main workflow and new Status introduced 2. More regression effort as it may impact the whole workflow |
| Effort | | |
| Open questions | 1. **Linkage issue for Murex trade and cashflows, pending analysis from Murex, ** 1. **Impact mainly on validation as it may block cashflows for Murex** 2. **Impact LIEN STP processing** |

##

## Cashflow Group service

- cashflow scbml xpath

| field | xpath |
| --- | --- |
| originalTradeId(murex) | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:originatingTradeId/conf:tradeId[@tradeIdScheme='[http://www.sc.com/coding-scheme/tradeId/originatingTradeId](http://www.sc.com/coding-scheme/tradeId/originatingTradeId)'] |
| tradeId(murex) | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:tradeId[@tradeIdScheme='[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)'] |
| tradeId(stella) | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:tradeId[@tradeIdScheme='[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)'] |
| tradeStatus(both) | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:state[@stateScheme='[http://www.sc.com/coding-scheme/state/tradeWorkflowStatus](http://www.sc.com/coding-scheme/state/tradeWorkflowStatus)'] |

- trade scbml logic model

| **Field** | **Logic Model Name(Murex)** | **Logic Model Name(Stella)** |
| --- | --- | --- |
| tradeId | Source_System_Trade_Internal_Id | Trade_Id |
| majorVersion | | Trade_Lake_Trade_Major_Version |
| trackingVersion | | Tracking_Version |
| tradeStatus | Source_System_Validation_Status | Trade_State |
| productType | Instrument_Common.ISDA_Taxonomy | Instrument_Common.ISDA_Taxonomy |
| action | Source_System_Action_Type | Action_Type |
| sourceSystem | Data_Flow.Data_Sender | Data_Flow.Data_Sender |

- CashflowGroup state mechine

- menual deliver cashflow for trade validated