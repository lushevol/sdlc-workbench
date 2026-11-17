## Background

Since day 1 requirement, FMCODEs for entity and counterparty as well as Client type are required, and FMCODEs are identified as mandatory information, and we built the integration with BPSI to fetch and stamping logic in lifecycle when cashflow flows into the workflow within the Data Persistence Node.

With H2 requirements, we found more and more attributes to be stamped, it does not make sense to keep the stamping logic coupled with data persistence step, we need a more clear design and implementation.

| Phase | Cashflow attribute | Mandatory |
| --- | --- | --- |
| Day 1 for CN | Booking entity FMCODE | Yes |
| Day 1 for CN | Counterparty FMCODE | Yes |
| Day 1 for CN | Client Type | No |
| Day 1 for CN | Reversal / Rebook | No |
| H2 for UK/DE | Client domicile country | No |
| H2 for UK/DE | Client BIC | No |
| For UK 2025 | LIEN AMOUNT | No |
| For UK 2025 | Pending Fixing Flag | No |

## Design

Below shows the current implementation and the proposed model.

1. Simplify the logic of data persistence node and responsibility
2. Move the stamping logic to a separate API still within lifecycle service
3. Make cashflow attributes stamping become a new action within lifecycle, which could be easily reused by other workflow processing like reinstate

##

Precheck logic:

1. `convert to StellaInfo, is it still required?`
2. convert to RatanStellaMessageEvent 1. ` convert to StellaInfo again, why?` 2. `` publish common Event, still required?`` 3. Settlement Amount rounding 4. `` Format settlementDate "yyyy-MM-dd"`` 5. `` Enrich Legal entity(party1 party2 - FMCODE, FMTYPE, DOMICILECOUNTRY, ADDRLINE)`` 6. ` Format withdrawal settlement Date if exists, still required? /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event='Withdrawal']/scb:payment/conf:paymentDate/conf:unadjustedDate, not in use, removed.` 7. ` Enrich event reason` 8. `` Enrich beneficiary ```bic flag`
3. Validation 1. amount is a number 2. value date format 3. amount greater than 0 4. entity fmid exists 5. CFI code exists 6. currency exists 7. counterparty fmid exists 8. entity fmid exists - duplicate d 9. cashflow length is 12
4. If withdrawal 1. if SUSPENDED and SUSPENDED_MATURED return FAIL 2. Query whether cashflow id exists, not exists not bypass holding disable and data persistence 3. Cashflow exists and status was NETTED or SPLIT, and its resultant cashflow is not post released, then return FILTERED to workflow to unnet first. 4. If no need unnet, disable holding queue 5. persist RatanStellaMessageEvent 6. construct SCBML by current message and event 7. build lifecycle request 8. run lifecycle
5. If New 1. if not PROJECTED return FAIL 2. persist RatanStellaMessageEvent 3. construct SCBML by current message and event 4. build lifecycle request 5. run lifecycle