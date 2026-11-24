In cashflow migration process, for Korea cashflow, as can't got 'COMP' status from TDS3, the solution is that Murex Korea send trade message with  COMP status directly to RATAN side.

Sample MXML message:

| | Trade id | Package id | Structure |
| --- | --- | --- | --- |
| Single trade | 5001566464 | | ![image-2026-7-9_10-6-56.png](attachments/image-2026-7-9_10-6-56.png) |
| Package child trade1 | 5001566453 | | ![image-2026-7-9_10-6-59.png](attachments/image-2026-7-9_10-6-59.png) |
| Package child trade2 | 5001566454 | | ![image-2026-7-9_10-7-16.png](attachments/image-2026-7-9_10-7-16.png) |

Sample SCBML message:

Field mapping between MXML and SCBML:

| | SCBML path | SCBML field | Murex path | Murex field | Logic |
| --- | --- | --- | --- | --- | --- |
| 1 | /scb:SCBML/scb:header/scb:originationDetails/scb:messageSender/scb:messageSender[@systemScheme="[http://www.sc.com/coding-scheme/system-1-0](http://www.sc.com/coding-scheme/system-1-0)] | Murex | NONE | NONE | Hardcode |
| 2 | /scb:SCBML/scb:payload/scb:FPMLPayload/scb:header/scb:process/scb:subState[@stateScheme='[http://www.sc.com/coding-scheme/state/Murex](http://www.sc.com/coding-scheme/state/Murex)'] | COMP | /MxML/trades/trade/tradeStatus/validationLevel | COMP | Direct mapping |
| 3 | /scb:SCBML/scb:payload/scb:FPMLPayload/scb:header/scb:process/scb:transactionType[@transactionTypeScheme="[http://www.sc.com/coding-scheme/action/Murex](http://www.sc.com/coding-scheme/action/Murex)] | validation | /MxML/events/mainEvent/action | validation | Direct mapping |
| 4 | /scb:SCBML/scb:payload/scb:FPMLPayload/conf:party/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/entity](http://www.sc.com/coding-scheme/partyId/entity)] | SCFB_SEOUL | /MxML/trades/trade/tradeHeader/tradeViews/tradeView/entity | SCFB_SEOUL | Direct mapping |
| 5 | /scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade/conf:tradeHeader/conf:partyTradeIdentifier/conf:tradeId[@tradeIdScheme="[http://www.sc.com/coding-scheme/tradeId/Murex/tradeInternalId](http://www.sc.com/coding-scheme/tradeId/Murex/tradeInternalId)"] | 5001566464 | /MxML/trades/trade/tradeHeader/tradeViews/tradeView/tradeId/tradeInternalId | 5001566464 | Direct mapping |
| 6 | /scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade/conf:tradeHeader/conf:partyTradeIdentifier/conf:tradeId[@tradeIdScheme="[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)"] | 5001566464 | /MxML/trades/trade/tradeHeader/tradeViews/tradeView/tradeId/tradeInternalId | 5001566464 | Direct mapping |
| 7 | /scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade/conf:taxonomy/conf:productId[@productIdScheme="[http://www.fpml.org/coding-scheme/product-taxonomy](http://www.fpml.org/coding-scheme/product-taxonomy)] | CURR|OPT|ASN | /MxML/trades/trade/tradeHeader/tradeCategory/tradeFamily /MxML/trades/trade/tradeHeader/tradeCategory/tradeGroup /MxML/trades/trade/tradeHeader/tradeCategory/tradeType | CURR OPT ASN | Logic mapping |

OPEN QUESTION:

1. If original trade had not been confirmed, after cancel and reissue, original cashflow will be cancelled directly in RATAN, and new cashflow will waiting for new trade's confirmation. YES. New trade will push COMP message again.