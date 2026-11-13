TODO:

- [ ] Exception handling
- [ ] SSI UBER structure
- [ ] Trade ssi refresh, scope
- [ ] Business case
- [ ] 2-1/2-2 need update
- [ ] 4/ Low priority

WIP:

- [ ] UBER trade model mapping(extract currencies from each product)
- [ ] Store SSI info in RATAN cashflow
- [ ] SSI refresh logic details

# Background

This is part of UBER integration design. By leveraging UBER, SSI stamping flow could be optimized:

- Cash SSI stamping could reuse the SSI stamping result of the trade that produces the cashflow
- UBER could be used as standard format for communication between RATAN and CDUPS for trade stamping
- Downstream systems would benefit from being notified of SSI refreshing that is handled in RATAN

CDU PS Request

| Key | Data Model | Sample | |
| --- | --- | --- | --- |
| Trade_Id | { "key": [logical model indexed term], "value": [actual value] } 1. Value + Key will be used for validation. 2. Trade_Id to be used for linkage. 3. Value will be used for stamping query. | { "key": "Trade_Id", "value": "4354367341"} | |
| Major_Version | { "key": "Trade_Lake_Trade_Major_Version", "value": "5"} | |
| Trade_Date | { "key": "Trade_Date", "value": "2025-05-01"} | |
| | | |
| Booking Entity Fmid | { "key": "Entity.Booking_Entity_SCI_FMID", "value": "USD"} | |
| Counterparty Fmid | { "key": "Entity.Counterparty_SCI_FMID", "value": "400202766"} | |
| CFI | { "key": "Instrument_Common.CFI_Code", "value": "SRCXCX"} | |
| --------------------------Start Loop Array [ | | |
| Currency_X | { "key": "Swap_Instrument.IR_Leg.First_Leg.Notional_Amount_Currency", "value": "USD"} | |
| PayReceive_Currency_X | { "key": "Swap_Instrument.IR_Leg.First_Leg.Payer_Party_Reference", "value": "party1"} | |
| ]--------------------------End Loop Array | | |

## Current implementation with SCBML

See [SSI Stamping Implementation\(SCBML\)]

## Objective

- Provide unified SSI stamping API that is product agnostic and single responsibility
- Reduce unnecessary stamping and reuse the stamping result of trade for cashflow as much as possible
- Use UBER as standard exchange format
- Be able to support new architecture that defined in UBER integration design

# Strategic SSI stamping proposal

## Trade & Cashflow SSI stamping

This part covers sub-processes 1-1, 1-2, 1-3, and 1-4.

### RATAN Logic Model Mapping

When an UBER message is received, it needs to be decoded into a RATAN Logic Model format. This process involves mapping the UBER message fields to the corresponding fields in the RATAN LM.

RATAN Logic Model(hereafter referred to as RATAN LM) is a data model that extends from the UBER message format. It is designed to be compatible with the UBER message format, but also includes additional fields and structures that are specific to the RATAN system.

To perform SSI stamping, it is necessary to extract and standardize the trade currency information from multiple fields in the RATAN LM. The currencies of each trade may vary depending on the trade product. By standardize the currencies, we could perform product agnostic SSI stamping with uniform logic.

Fields relevant for SSI stamping are listed bellow. The detailed mapping are listed in appendix  .

- Product Type
- Trade ID
- Trade major version
- Counterpart FMID
- CFI Code
- Settlement Method
- Settlement Type
- Currency
- Debit/Credit

### Trade stamping and version control

- [ ] MajorVersion will not be used because?
- [ ] What field could be used for identifying UBER message? (traceId in header, asOf+effectiveDate)
- [ ] If we use effectiveDate, be aware that the effective_end_date will be 9999/ and will not be updated automatically
- [ ] How CDUPS will query us? if query with UBER, then we may still need to compare currencies; if with asOf+effectiveDate, additional DQSL query needed, and need to assemble UBER manually

When trade changes, the major version will increase. Since trade currencies are extracted from trade data, same trade with different major version are not compatible to reuse SSI stamping result. The following rules are applied for trade stamping:

- SSI stamp result will be stored per tradeId + majorVersion, no restamp if already exists in db
- When query trade SSI stamp result, the correspondent result of tradeId + majorVersion will be returned. It's supposed that downstream will always query SSI stamp result using latest trade data, ie. largest majorVersion. If no result found on db at the point of query, then we do ad-hoc stamping (not persisted).
- SSI refresh will only impact the current latest major version

### Trade stamping query

### Cashflow splitting

Since UBER contains all cashflows, we need to identify the change and only execute SSI stamping for changed cashflows.

### Cashflow SSI stamping

When cashflow(s) of a trade received from upstream, now we should be able to get the trade ssi stamping result and apply it directly to cashflows :

- query stamp result by trade id
- get stamp result by matching currency, direction, .. (if good stamped)
- otherwise raise exception and NSTP

**Option A: Batch stamp in group service**

****

In this option, we do trade SSI stamping and get enriched cashflows at the same time. The SSI information will be used to override existing data in lifecycle-service later.

Note that a proper mechanism must be applied to prevent concurrent access on same cashflow.

**Option B: Stamp in orchestration**

Another approach is to do cashflow in orchestration service. Trade SSI stamping will be processed when UBER received, and the SSI information will be reused when stamping cashflow.

SSI stamping service will be invoked 1 + N times in this flow.

****

## SSI change notify

There're a few issues on current implementation of SSI update notification: :

- The implementation has complex query to locate impacted cashflows
- Trade SSI not supported

### Impacted trade stamping addressing

### Impacted cashflow addressing

### Refresh trade stamping result

### Refresh cashflow SSI

### Concurrency control

**SSI stamping service:**

Incase of concurrent stamping, we'll introduce optimistic lock on trade stamping process.

1. If stamping result not found by tradeId + majorVersion, then start stamping
2. A unique key constraint will be created on tradeId+majorVersion, if multiple stamping process of same tradeId + majorVersion started, only one of them will succeed
3. If the stamping process failed due to key conflict, then retry the process. Since the stamping result has already been saved, no further stamping required.

The ssi notification topic is single partitioned in order to consume sequentially.

## Exception handling

### Stamping same trade for multiple times

If upstream make ssi stamping for same trade for multiple times:

- We need to do stamp for each request and store a record, since trade currencies might be different
- When query stamping result, always return newest data

- [ ] if we recevice a trade ssi stamping, but it;s already stamped in cashflows

### Stamp failed

If trade stamp failed, and then when cashflow comes:

- Get stamp result by tradeId first, and the stamping result is failure(or partial failure)
- Perform a batch SSI stamping again to check if stamping could be fixed, otherwise stamping failed for the cashflow
- batch stamping using cashflow information as compensation for new product not onboarded yet

### Trade stamping result not found

If no trade stamping result found, then we do a trade stamping , which will create trade stamping result,

and apply the result to cashflows.

# Downstream SCBML generation

we need to store SSI information in RATAN model, and translate it to SCBML when sending to Razor

# Appendix

## UBER message field mapping

**ANCHOR: uber-mapping**

| Field | UBER path | Example value | Remark |
| --- | --- | --- | --- |
| Product type | Instrument_Common.ISDA_Taxonomy | InterestRate:LoanDeposit InterestRate:IRSwap:OIS | Need a mechanism to map to existing product type (IRS, BullionSwap, etc) |
| Tracking Id | Trade_Lake_Trade_Id | | |
| Trade Id | | | |
| Party1 FMID | Entity.Booking_Entity_SCIFMID | | |
| Party2 FMID | | | |

## Database schema

| TABLE | Columns | Description |
| --- | --- | --- |
| cashflow_stamping | | |
| cashflow_stamping_legacy_exception | | |
| stamped_nostro_account | | |
| stamped_vostro_account | | |
| maker_checker_request | | |
| trade_stamping_message | | |
| raw_message | | |

## API schema

| API | INPUT | OUTPUT | USER |
| --- | --- | --- | --- |
| batch SSI stamping | currencies | mapping of refId → stamp result | Potentially be used by RATAN services |
| trade SSI stamping | UBER | parsed currencies refId → stamp result | orchestration service |
| trade SSI stamping query | tradeId | parsed currencies refId → stamp result | group service |

see api specification:

📎 [strategic-ssi-stamping.yml](attachments/strategic-ssi-stamping.yml)