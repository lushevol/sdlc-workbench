# ADO

[Story 6962983 Swap Agent Day2](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6962983)

# Dependency

**Murex**: Consume new field Clearing ID from Murex

# Requirement Details

1. Auto net cash flow according to cash flow type “coupon/ MTM” - this has dependency on auto netting function - 2 auto netting rule need to be created: - **SAL MTM Netting: ** ***Product_Strategy =”SWAP_AGENT” && Payment_Type =“Interim MTM” && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "")*** - **SAL Coupon Netting: *****Product_Strategy =”SWAP_AGENT” && Payment_Type =“Coupon” && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "")*** - System will net above swap agent cashflow with the same*** booking entity + counterparty + ccy+ VD + payment type ***which means MTM will not net with Coupon
2. Auto-netting time can be configured - system will start the auto netting at configured time, if there is any job failure, the cashflow should be netted in another job 30 mins later.
3. Reflect the cash flow type after the cash flow auto netted. - expected payment type in netting resultant should be - **SAL MTM Netting** - **SAL Coupon Netting**
4. Auto swift_suppress the netting resultant cashflow from “coupon/MTM/” - new suppression rule to be added : ***Payment_Type in ("*****SAL MTM Netting*****","*****SAL Coupon Netting*****") && ******(Cashflow__Netting_Id != null && Cashflow__Netting_Id != "")***
5. Add **Clearing_Organization_Trade_Id** and **Trade_External_Id **in view builder of Ratan Cashflow Blotter, user can drag them to their own custom view - once cashflow received in Ratan, we will call TDS3 API to get the field value, if the value updated from trade and trade event sent to Ratan, we will refresh the value for active cashflow (PROJECTED/QUEUED/WAITING/READY) (not notification, means when user manually query the cashflow, it will display the latest value) - The field will not be added to customized filter in cashflow blotter. - | Logic model | Rosetta Link | Physical model | | --- | --- | --- | | Clearing_Organization_Trade_Id | | (/scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade|/scb:SCBML/scb:payload/scb:FPMLPayload/((*/(*:originalTrade|*:trade))|((*:novation|*:cancelReissue)/*:newTrade)))/conf:tradeHeader/conf:partyTradeIdentifier[conf:partyReference/@href=(/scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade|/scb:SCBML/scb:payload/scb:FPMLPayload/((*/(*:originalTrade|*:trade))|((*:novation|*:cancelReissue)/*:newTrade)))/conf:tradeHeader/conf:partyTradeInformation/conf:relatedParty[conf:role="ClearingOrganization"]/conf:partyReference/@href]/conf:tradeId[@tradeIdScheme=[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)] | | Trade_External_Id | | ### (/scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade|/scb:SCBML/scb:payload/scb:FPMLPayload/((*/(*:originalTrade|*:trade))|((*:novation|*:cancelReissue)/*:newTrade)))(:[@xsi:type=fn:QName('','scbextn:Trade')]:)/conf:tradeHeader/conf:partyTradeIdentifier[conf:partyReference/@href='party1']/conf:tradeId[@tradeIdScheme='http://www.sc.com/coding-scheme/tradeId/sourceSystem/tradeExternalId'] |
6. ~~Send Clearing ID to downstream (TLM, RATAN EOD)--~~
7. the netting resultant should not be sent to LMS because of swift suppressed status

# Business User Case

| | Function | Scenario | Expected Result |
| --- | --- | --- | --- |
| 1 | Swap Agent MTM | 1. auto netting rule created in netting static 2. swift suppress rule created in swift suppression rule blotter 3. book 2 cashflow C1, C2 (Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM') 4. trigger scheduled job | 1. netting rule is active 2. swift suppression rule is active 3. C1,C2 cashflow state ='WAITING', cashflow sub state type ='Pending Auto Netting' 4. C1,C2 cashflow state ='Netted', Netting resultant N1 created (Cashflow State = 'SWIFT_SUPPRESSED', payment type ='SAL MTM Netting'), Accounting entry generated and sent as expected |
| 2 | Swap Agent Coupon | 1. auto netting rule created in netting static 2. swift suppress rule created in swift suppression rule blotter 3. book 2 cashflow C1, C2 (Murex_Product_strategy=SWAP_AGENT, Payment Type ='Coupon') 4. trigger scheduled job | 1. netting rule is active 2. swift suppression rule is active 3. C1,C2 cashflow state ='WAITING', cashflow sub state type ='Pending Auto Netting' 4. C1,C2 cashflow state ='Netted', Netting resultant N1 created (Cashflow State = 'SWIFT_SUPPRESSED', payment type ='SAL Coupon Netting'), Accounting entry generated and sent as expected |
| 3 | Swap Agent Initial/Final Exchange | 1. auto netting rule created in netting static 2. swift suppress rule created in swift suppression rule blotter 3. book 2 cashflow C1, C2 (Murex_Product_strategy=SWAP_AGENT, Payment Type ='Initial Notional' or 'Final Notional') | 1. netting rule is active 2. swift suppression rule is active 3. C1,C2 will not hit auto netting rule |
| 4 | Check clearing ID | 1. user add "Clearing Organization Trade Id" and "External Trade Id" in cashflow blotter customized view | data displayed as expected, the value is the same as the parent trade |

# Links

[Swap Agent Payment]