# Background

Story: [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/3733407](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/3733407)

SSI Stamping in strategic cash settlement flow: [FMRP - SSI Stamping Flow]

Egypt, Saudi, Nepal entity is onboarding to RATAN strategic cashflow settlement flow, in this story we need to

1. Design and implement the logic in CN process to be able to pick the expected Nostro for util cashflow
2. Design should work for local currency of specific entities.
3. Configurable to include more entities in the future

# Principals

1. Concepts: | Attribute | Source | Meaning | Value | Xpath | | --- | --- | --- | --- | --- | | CCY Pair | SCBML | Currency pair, new xpath added by Ratan | eg. EGOUSD | TBD | | Entity Fm Id | SCBML | Booking eneity fm id, existing xpath | SA: 400991880 NP: 400007847 EG: 401036553 | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party1']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)'] | | Product Taxonomy | SCBML | Product type | ForeignExchange:Forward ForeignExchange:Swap ForeignExchange:Spot | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:productId[@productIdScheme="[http://www.fpml.org/coding-scheme/product-taxonomy](http://www.fpml.org/coding-scheme/product-taxonomy)"] | | Settlement_Instruction. Account.SCB_Nostro_Account_Type | SSI+ | Settlement means | FXBRREC | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/scb:settlementMeans/scb:settlementAccountNo | | Currency_Pair | TDS3 | Trade field: Instrument_Common.Currency_Pair | eg. EGOUSD | |
2. Group management service need to enrich the correct value to CCY pair after group ready and match the condition below: 1. Cashflow booking entity fm id in SA, NP, EG 2. ISDA taxonomy in spot, forward, swap 3. Technical check only 2 payment currency under grouped cashflows
3. No need to enrich CCY pair if three conditions above are not met.
4. SSI service nostro stamping: 1. Single Vostro - if settlement means is FXBRREC and CCY pair exists, then quey **Nostro** with CCY pair, otherwise follow CN logic. 2. Missing/Multi Vostro -~~ ~~if CCY pair exists, then query **primary Nostro** with CCY pair, otherwise follow CN logic.
5. **Open Questions**

| | Item | Impact point | Status | Comment |
| --- | --- | --- | --- | --- |
| 1 | Nostro static data structure confirm | Group ready logic to enrich CCY pair, static data service query logic change potentially. | | Wayne need confirm |
| 2 | Whether need to use CCY pair when query primary Nostro | SSI stamping query static data service | | Wayne need confirm |
| 3 | New xpath definition | Group service enrich and SSI stamping extract | | Wayne or Geoffrey need confirm |
| 4 | CCY Pair enrich mechanism rule or properties | | | |
| 5 | Pick 1 of 2 possible solutions | | | |

# Logic workflow(Change points in red)

## Option 1: Group management service help to enrich CCY pair in advance

### Exception cases

| service | case | |
| --- | --- | --- |
| group-service | manual delivery the cashflow group but some cashflow of group is not recieved. then the currency pair is not enriched. | |
| group-service | Exception generated when processing the ccy. | |
| ssi-stamping-service | nostro is not exist by querying with ccyPair. then whether to query nostro without ccyPair | |
| ssi-stamping-service | whether to define a new missing ccy pair excepiton in order to replay | |

### Flow chart of option 1

## Option 2: SSI stamping service query TDS3 to get CCY pair instead of waiting for another leg.

## Comparison of Option 1 and Option 2

1. option1 requires two service changes. one is group management service and another is ssi stamping service. group management service need enrich the ccy pair in order to ssi stamping service parse the ccy pair from scbml.
2. option2 only require one service change. but need query ccy pair from TDS3 resulting in degraded performance

# DB Change

There is no DB change on both Group management service and cash settlement ssi stamping service.