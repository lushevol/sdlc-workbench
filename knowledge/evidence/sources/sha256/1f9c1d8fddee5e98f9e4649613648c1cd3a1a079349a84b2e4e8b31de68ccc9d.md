# 1. Background

Per FMRP project, as there is limitation for Stella processing settlement method, rate related FX trade (Spot/Forward/Swap) and cashflow generated from these trade will be processed in Razor.

For trade processing, data flow is Stella→Ratan→Razor, detailed requirement can be found in <u>[Ratan / TDS3 Replication to Razor - FM re-platforming - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2895614039)</u>

For Cashflow generated from trade, data flow is Razor→ Ratan→ Stella, as Stella side needs payment status to facilitate Hard block logic.

Targeting to go live the function as drop 2 (2024).

# 2. Requirement

1. The primary objective is to mitigate risk of duplicate payment.
2. Resultant cashflow from Net/Split is not required to be write back into Stella.
3. Once cashflow is Netted/Split/Settled/Released in Razor, status should be updated to SUSPENDED-MATURED in Stella.
4. For Netted/Split/Settled/Released, if status update in Stella is the same (from SUSPENDED-MATURED to SUSPENDED-MATURED), it’s preferred not to be updated in Stella.
5. Economic fields and message ID will be used to link between Razor and Stella cashflow.
6. Un-net / Un-split not required to write back as there is still a risk of duplicate payment.
7. 1. As there is no trade version from RAZOR, payment from RAZOR will be matched to Stella latest version of cashflow in RATAN. 2. For Eco amendment in STELLA, RATAN will wait for RAZOR cashflow to update STELLA payment status; for Non-eco amendment in STELLA, RATAN will directly update the payment status if previous version payment is SUSPEND-MATURED. 1. RAZOR will only perform non-eco amendment, which will not be sent be RATAN.

# 3. Current RAZOR & Stella Behavior

## Razor

1. Currently there is no indicator to identify economic amendment or non-economic amendment in Razor, while non-economic amendment from Razor after trade payment already in Netted/Split/Settled/Released/CCPNetted status is not a valid scenario per attachment.
2. If any non-economic amendment happens on unreleased/unsettled in RAZOR, it will not generate new cashflow.
3. Non-economic (only settlement method) amendment happens on released/settled in RAZOR, it's confirmed by user as invalid case.
4. Reference <u>[Payment Status write-back - Razor Development - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/Razor/Payment+Status+write-back).</u>

## Stella

1. As FX cashflow is processed in RAZOR instead of Stella, to separate it with Stella cashflow, SUSPENDED-MATURED/ SUSPENDED status is preferred.
2. Stella hard block based on T1 or T1&live cashflow
3. TDS3 generated cashflow for FX will be set as Suspended by default and not send down, with fee related cashflow to be exception and set as Projected for RATAN to consume and process separately.
4. Fee related cashflow released/settled status is not required for hard block.
5. If user cancel/update on trade with SUSPENDED-MATURED cashflow, the hard block will be auto lifted until new cashflow is SUSPENDED-MATURED status.
6. For a trade with 2 cashflows, if one cashflow is in SUSPENDED-MATURED, the trade will be in hard block.

# 4. Assumption and Limitations

4.1 As there is no trade version from RAZOR, payment from RAZOR will be matched to Stella latest version of cashflow in RATAN.

4.2 For Eco amendment in STELLA, RATAN will wait for RAZOR cashflow to update STELLA payment status;

For Non-eco amendment in STELLA, RATAN will directly update the payment status if previous version payment is SUSPEND-MATURED.

4.3 RAZOR will only perform non-eco amendment, which will not be sent be RATAN.

4.4 There is no ACK/NACK mechanism for FX status write back, recon is not in place.

4.5 Stella Non ISO Currency VS Razor ISO Currency:

- - Ratan receive the original booking currency from Stella like CNY - Razor have the local NON ISO to ISO conversion, which convert the CNY to CNH - Razor return cashflow status to Ratan with post convert currency CNH, they don’t have the capacity to return the original currency - Ratan would have CNY from Stella while CNH from Razor, we can’t fully match these 2 currency. - Compromised solution is we just compare the first 2 characters of the currency code, so CNY -> CN* is same with CNH -> CN*. The risk is if someone created any unknown currency with CN* this would be consider same as CNY/CNH.

4.6 Stella original payment amount VS Razor rounded amount:

- - - Stella generated cashflow with original amount - Razor would do the rounding on the amount and only return this rounding amount to Razor, they don’t have the capacity to return the original amount - Ratan can’t perfectly match the Stella original amount VS Razor rounded amount - Compromised solution is we accept the difference within the decimal for non JPY and within 100 for JPY, e.g. 123.3 USD would be same with 124.2 USD. Similarly 100300 JPY would be consider the same with 100201 JPY. The risk is we won’t have the exactly match but with some agreed tolerance only.

# 5.RATAN Technical Design

## 5.1 Technical Process

For FX replication cashflow from Stella, save the trade ID, trade version and the 6 economic fields.

Compare the same trade ID's latest version cashflow with previous cashflow for the 6 fields,

If Non-Eco amendment,

If previous cashflow status is SUSPENDED-MATURED,

Update Stella latest new cashflow status to SUSPENDED-MATURED.

Else If previous cashflow status is SUSPENDED,

Wait for Razor cashflow.

If new only or eco amendment, wait for RAZOR's cashflow.

For FX replication cashflow from Razor

If cashflow validation status in (Released, Settled, Netted, Split, CCPNetted) and Reverse Status in (None, Correction) 
and same Razor cashflow ID didn't proceed successful previously.

Map Stella latest new cashflow with the 6 economic fields.

If all matches, then update Stella latest new cashflow status to SUSPENDED-MATURED

else instore the NACK in RATAN for phase 1.

If withdrawal only Ignore.

6 economic fields:

- - Booking Entity - Counterparty - Currency - Amount - Value Date - Pay/Receive

## 5.2 Interface Specification

- ACK is required from Razor.
- No field convention in Razor.

| # | Business Term | Physical Model | Sample Value |
| --- | --- | --- | --- |
| | Razor FX replication cashflow | Message Header | |
| | Razor Stella trade ID | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/conf:originatingTradeId/conf:tradeId | |
| | Razor Trade ID | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowStatus/scb:linkId [@linkIdScheme="[http://www.sc.com/coding-scheme/tradeId/Razor](http://www.sc.com/coding-scheme/tradeId/Razor)"] | |
| | Razor Cashflow ID | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowStatus/scb:cashflowIdentifier/scb:cashflowId | 373670953 |
| | Razor Cashflow Validation Status | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowStatus/scb:state | Released, Settled, Netted, Split, CCPNetted |
| | Razor Cashflow Original ID | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowStatus/scb:linkId[@linkIdScheme="[http://www.sc.com/coding-scheme/cashflowId/creator/PaymentId](http://www.sc.com/coding-scheme/cashflowId/creator/PaymentId)"] | |
| | Razor Cashflow Reverse Status | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:eventReason | None, Correction |
| | Razor Booking Entity | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party/conf:partyId in party 1 | |
| | Razor Counterparty | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party/conf:partyId in party 2 | |
| | Razor Currency | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency | CNH |
| | Razor Amount | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount | |
| | Razor Value Date | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowStatus/scb:paymentDate | 20230707 |
| | Razor Pay/Receive | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:payerPartyReference | |
| | Stella FX replication cashflow | SUSPENDED status cashflow from Stella | |
| | Stella Trade ID | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:tradeId[@tradeIdScheme="[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)"] | |
| | Stella Trade Version | | |
| | Stella Booking Entity | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id="party1"]/conf:partyId[@partyIdScheme="[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)"] | 10036642 |
| | Stella Counterparty | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id="party2"]/conf:partyId[@partyIdScheme="[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)"] | 300079654 |
| | Stella Currency | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency[@currencyScheme="[http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15](http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15)"] | CNO |
| | Stella Amount | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount | 900000000.000000 |
| | Stella Value Date | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentDate/conf:unadjustedDate | 2023-12-01 |
| | Stella Pay/Receive | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id=/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:payerPartyReference/@href] | party1 |
| | Stella latest withdrawal cashflow | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:event[@eventScheme="[http://www.sc.com/coding-scheme/event/scbml-business-event](http://www.sc.com/coding-scheme/event/scbml-business-event)"] == Withdrawal | |

# 6. Reference

📎 [FW_ FX Replication - Payment Status write back.msg](attachments/FW_ FX Replication - Payment Status write back.msg)
     
📎 [RE_ 1834488 Cashflow status sync with RAZOR Analysis.msg](attachments/RE_ 1834488 Cashflow status sync with RAZOR Analysis.msg)
   
📎 [FMRP payment status.xml](attachments/FMRP payment status.xml)
   
📎 [FX cashflow status write back.xlsx](attachments/FX cashflow status write back.xlsx)

# 7. Flow Diagram

# 8. DB Design

| ratan_razor_fx_cashflow_data |
| --- |
| Column Name | Description | Sample Value |
| id | Technical primary id | |
| stella_trade_id | Stella trade id | 50011008 |
| cashflow_id | razor cashflow id | 373670953 |
| trade_id | razor trade id | 330134747 |
| original_cashflow_id | razor original cashflow id if reverse happen | 123456 |
| cashflow_status | razor cashflow status | RELEASED, SETTLED, NETTED, SPLIT, CCPNETTED |
| reverse_status | reverse status | NONE, CORRECTION |
| payment_indicator | combine 6 payment attributes together for easy compare | 10062461|400899993|CNO|62785.000000|2024-01-12|Receive| |
| status | message status | PENDING, SENT |
| version | optimistic lock | |
| created_at | technical audit field. | |
| updated_at | technical audit field. | |
| created_by | technical audit field. | |
| updated_by | technical audit field. | |

| ratan_razor_fx_cashflow_data_history |
| --- |
| Column Name | Description | Sample Value |
| id | Technical primary id | |
| cashflow_data_id | ratan_razor_fx_cashflow_data primary key | |
| stella_trade_id | Stella trade id | 50011008 |
| cashflow_id | razor cashflow id | 373670953 |
| trade_id | razor trade id | 330134747 |
| original_cashflow_id | razor original cashflow id if reverse happen | 123456 |
| cashflow_status | razor cashflow status | RELEASED, SETTLED, NETTED, SPLIT, CCPNETTED |
| reverse_status | reverse status | NONE, CORRECTION |
| payment_indicator | combine 6 payment attributes together for easy compare | 10062461|400899993|CNO|62785.000000|2024-01-12|Receive| |
| status | message status | PENDING, SENT |
| version | optimistic lock | |
| created_at | technical audit field. | |
| updated_at | technical audit field. | |
| created_by | technical audit field. | |
| updated_by | technical audit field. | |

# 9. Developer Use Case

📎 [FX Status write back - developper use case.xlsx](attachments/FX Status write back - developper use case.xlsx)