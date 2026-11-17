#

# Background

We got a requirement on "Commodity or PM for UK payment", which can't be perform with current filter builder and should introduce "OR" concept to it.

| | Current Filter Logic | Required Filter Logic |
| --- | --- | --- |
| **Scope** | Provide a simple mode of querying logic: "All filters should be matched to results", technically explain is "All filter items conjunct with "AND"". | Filters can be combined with AND/OR conjunction, and also be nested with groups. |
| **Expression Sample** | (field1 is "value" AND field2 is "value" AND field3 is "value") | (field1 is "value" AND field2 is "value" AND (field3 is "value" OR field4 is "value")) |
| **UI Sample** | ![image-2025-4-2_9-37-27.png](attachments/image-2025-4-2_9-37-27.png) | ![image-2025-4-2_9-38-12.png](attachments/image-2025-4-2_9-38-12.png) |

***Detail Requirements**: [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7529554](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7529554)*

# ![image-2025-4-3_17-16-18.png](attachments/image-2025-4-3_17-16-18.png)

# Principle

**1. All existing query scenarios should be covered properly in new design.**

**2. For more complex scenarios supporting and better user experience, enable flexible querying with AND/OR/GROUP requests.**

**3. Align query model with OpenSearch query interface, for seamless migration in the future.**

# Proposal

Front to back query DSL should contains

| Features | New Scope | Must to have |
| --- | --- | --- |
| Query on fields, support available operators. | No | Yes |
| Query with AND/OR conjunctions. | Yes | Yes |
| Query with Group. | Yes | Yes |
| Specify offset and limits. | No | Yes |
| Specify return logic model body. | No | Yes |
| Specify sorting model on result | Yes | No |
| Compatible with OpenSearch solution, seamless migration in the future. | Yes | No |

## Architecture Diagram

## Query DSL

Query DSL includes,

| Query DSL Items |
| --- |
| Filter Model |
| Pagination |
| *Sorting Model** |

## Filter Model Design

Filter is essentially for data set fields querying, describe how the results like. Fields filter model definition below,

```js
input LogicFilter {
  and: [LogicFilter!]
  or: [LogicFilter!]
  filters: [FilterArg!]
}
```

***and***: specify the AND group,

***or***: specify the OR group,

***filters***: specify filter args, which stands for atom filter item.

### Schema Rules

| Rule | Description | Sample |
| --- | --- | --- |
| LogicFilter can be nested, max depth is 3 | For current use case, we 3 level depth can matches all requirements. | **EXPAND: valid case 1** { "and": [ { "and": [ { "and": [ { "filters": [ { "field": "Cashflow.Pay_Receive_Indicator", "operator": "EQ", "values": "Pay" }, { "field": "Cashflow.Cashflow_Version", "operator": "EQ", "values": 1 } ] } ] }, { "filters": [ { "field": "Cashflow.Cashflow_Sub_State", "operator": "EQ", "values": "Pending Operator" } ] } ] }, { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" } ] } ] } **EXPAND_END** |
| For each logicfilter object in any level, should obtains only one key in and/or/filters. | If several items/and groups/or groups in the same level, split them into multiple items. Don't obtains in one logicfilter | **EXPAND: valid case 1** { "and": [ { "or": [ { "filters": [ { "field": "Cashflow.Cashflow_Sub_State", "operator": "EQ", "values": "Pending Operator" }, { "field": "Cashflow.Cashflow_Version", "operator": "EQ", "values": 1 } ] } ] }, { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" } ] } ] } **EXPAND_END** **EXPAND: invalid case 1** { "and": [ { "or": [ { "filters": [ { "field": "Cashflow.Cashflow_Sub_State", "operator": "EQ", "values": "Pending Operator" }, { "field": "Cashflow.Cashflow_Version", "operator": "EQ", "values": 1 } ] } ], // ERROR: don't use more than 2 keys in one filter object. "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" } ] } ], // ERROR: don't use more than 2 keys in one filter object. "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" } ] } **EXPAND_END** |
| filters in the first level has at most 1 item. [OpenSearch Schema Compatible] | If filters on the first level, should only contains 1 item, otherwise move it to and/or group. | **EXPAND: valid case 1** { "filters": [ { "field": "Cashflow.Pay_Receive_Indicator", "operator": "EQ", "values": "Pay" }, // ERROR: filters in first level should not contains more than 1 item. { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" }, ] } **EXPAND_END** |
| When don't have child group, and/or should contains more than 1 filter item, otherwise move it to parent group. [OpenSearch Schema Compatible] | Only one filter item in and/or group is meaningless, whether in and/or, the item follows the same logic with parent group. | **EXPAND: valid case 1** { "and": [ { "or": [ { "filters": [ { "field": "Cashflow.Cashflow_Sub_State", "operator": "EQ", "values": "Pending Operator" }, { "field": "Cashflow.Cashflow_Version", "operator": "EQ", "values": 1 } ] } ] }, { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" } ] } ] } **EXPAND_END** **EXPAND: invalid case 1** { "and": [ { // ERROR: there is only one filter item in or, should move to parent filters "or": [ { "filters": [ { "field": "Cashflow.Cashflow_Sub_State", "operator": "EQ", "values": "Pending Operator" } ] } ] }, { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" } ] } ] } // Change to { "and": [ { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" }, { "field": "Cashflow.Cashflow_Sub_State", "operator": "EQ", "values": "Pending Operator" } ] } ] } **EXPAND_END** |

### Samples for Filter DSL

| Filter Builder UI | Params Schema | SQL |
| --- | --- | --- |
| ![image-2025-4-1_16-26-8.png](attachments/image-2025-4-1_16-26-8.png) | **EXPAND: param json** { "and": [ { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" } ] } ] } **EXPAND_END** | Cashflow__Cashflow_State = "WAITING" |
| ![image-2025-4-1_16-23-52.png](attachments/image-2025-4-1_16-23-52.png) | **EXPAND: param json** { "and": [ { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" }, { "field": "Cashflow.Payment_Amount", "operator": "EQ", "values": "100.00" } ] } ] } **EXPAND_END** | Cashflow__Cashflow_State = "WAITING" and Cashflow__Payment_Amount = "100.00" |
| ![image-2025-4-1_16-29-40.png](attachments/image-2025-4-1_16-29-40.png) | **EXPAND: param json** { "and": [ { "or": [ { "filters": [ { "field": "Trade_State", "operator": "EQ", "values": "AFFIRMED" }, { "field": "Settlement_Date", "operator": "EQ", "values": "2025-04-01" } ] } ] }, { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "WAITING" }, { "field": "Cashflow.Payment_Amount", "operator": "EQ", "values": "100.00" } ] } ] } **EXPAND_END** | (Trade_State = "AFFIRMED" or Settlement_Date = "2025-04-01") and Cashflow__Cashflow_State = "WAITING" and Cashflow__Payment_Amount = "100.00" |
| ![image-2025-4-2_9-47-29.png](attachments/image-2025-4-2_9-47-29.png) | **EXPAND: param json** { "and": [ { "or": [ { "filters": [ { "field": "Cashflow.Is_Commodity", "operator": "EQ", "values": "true" }, { "field": "Instrument_Common.ISDA_Taxonomy", "operator": "EQ", "values": "Commodity:Metals:Precious:SpotFwd:Physical" } ] } ] }, { "or": [ { "filters": [ { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "FAILED" }, { "field": "Cashflow.Cashflow_State", "operator": "EQ", "values": "READY" } ] } ] }, { "filters": [ { "field": "Entity.Booking_Entity_SCI_FMCODE", "operator": "EQ", "values": "SCB LONDON*LDN" }, { "field": "Entity.Counterparty_SCI_FMCODE", "operator": "NOTIN", "values": [ "ABSA*JBG", "GUEC000U*ZRH", "INTBRKUKLTD*LDN", "GUEC000D*LDN", "USD FUT COMEX*SYD", "GREENLAGMF*GCN", "GREENLANGLO*EBE", "GUEC0JPB*LDN", "CHASE*LDN" ] } ] } ] } **EXPAND_END** | Entity.Booking_Entity_SCI_FMCODE = "SCB LONDON*LDN" and Entity.Counterparty_SCI_FMCODE in ("ABSA*JBG", "GUEC000U*ZRH", "INTBRKUKLTD*LDN", "GUEC000D*LDN", "USD FUT COMEX*SYD", "GREENLAGMF*GCN", "GREENLANGLO*EBE", "GUEC0JPB*LDN", "CHASE*LDN") (Cashflow.Is_Commodity = True or Instrument_Common.ISDA_Taxonomy = "Commodity:Metals:Precious:SpotFwd:Physical") and (Cashflow.Cashflow_State = FAILED or Cashflow.Cashflow_State = READY) and () |

## Pagination Model

| Pagination | Description | Scope |
| --- | --- | --- |
| Index | Page Index/Page Size | |
| *Cursor* | Cursor based | Placeholder, not implemented |
| *No Index* | Full data set loaded | Placeholder, not implemented |

## *Sorting Model*

By default, response data set sorted by created time, can specify sorting fields. Placeholder, not implemented.

## Endpoints Legends

| Query Endpoint | GraphQL Type | Sample | Referrence |
| --- | --- | --- | --- |
| Ultra Query | <details> <summary>Expand Details</summary> type Query { cashflowUltraQuery(payload: RatanUltraQuery): UltraQueryResult! } input RatanUltraQuery { filters: LogicFilter! pagingOption: PagingOption! pageIndex: Int! itemsPerPage: Int! orderArgs: [QueryOrder!]! # placeholder cursor: String # placeholder } # each logic filter item, only contains one key below. input LogicFilter { and: [LogicFilter!] # items > 1 or: [LogicFilter!] # items > 1 filters: [FilterArg!] # if level=0, items = 1, else >= 1 } input QueryOrder { orderField: String! orderType: QueryOrderType! } enum QueryOrderType { ASC DESC } enum PagingOption { CURSOR # placeholder PAGE_INDEX NO_PAGINATION # placeholder } type ResultCursorType { previous: String next: String } type UltraQueryResult { # totalHits totalResult: Int! # pageNo pageIndex: Int # pageSize itemsPerPage: Int! lastPage:Boolean! pagingCursors: ResultCursorType results: [ResultNew!]! } </details> | <details> <summary>Expand Details</summary> { "payload": { "filters": { "and": [ { "filters": [ { "field": "Cashflow.Payment_Date", "operator": "IN", "values": [ "2025-01-24", "2025-03-17" ] }, { "field": "Cashflow.Cashflow_State", "operator": "IN", "values": [ "WAITING", "RELEASED", "SETTLED", "READY" ] } ], }, { "or": [ { "filters": [ { "field": "Cashflow.Is_Commodity", "operator": "EQ", "values": "true" }, { "field": "Instrument_Common.ISDA_Taxonomy", "operator": "EQ", "values": "Commodity:Metals:Precious:SpotFwd:Physical" } ] } ] } ] }, "itemsPerPage": 1000, "orderArgs": [], "pageIndex": 0, "pagingOption": "PAGE_INDEX" } } </details> | [https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-api-hub?path=%2Ffoundation-2.0%2Fmd-doc%2Fuser-guide%2Fquery-dsl.md&version=GBdevelop&_a=contents](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-api-hub?path=%2Ffoundation-2.0%2Fmd-doc%2Fuser-guide%2Fquery-dsl.md&version=GBdevelop&_a=contents) |
| Ultra Query Count | <details> <summary>Expand Details</summary> type Query { cashflowUltraQueryCount(payload: RatanUltraQueryCount): UltraQueryCountResult! } input RatanUltraQueryCount{ filters: LogicFilter! } type UltraQueryCountResult { count: Int! } </details> | <details> <summary>Expand Details</summary> { "payload": { "filters": { "and": [ { "filters": [ { "field": "Cashflow.Payment_Date", "operator": "IN", "values": [ "2025-01-24", "2025-03-17" ] }, { "field": "Cashflow.Cashflow_State", "operator": "IN", "values": [ "WAITING", "RELEASED", "SETTLED", "READY" ] } ], "or": [ { "filters": [ { "field": "Cashflow.Is_Commodity", "operator": "EQ", "values": "true" }, { "field": "Instrument_Common.ISDA_Taxonomy", "operator": "EQ", "values": "Commodity:Metals:Precious:SpotFwd:Physical" } ] } ] } ] } } } </details> | |

# Implementation

We are implement this feature via GraphQL front to back.

## UI

**Technical Stack**: Redux-Toolkit, graphql-codegen.

**Diagram**:

## BE

# Benchmark

## Query Count Performance (Dashboard)

![image-2025-3-26_9-25-22.png](attachments/image-2025-3-26_9-25-22.png)

graphql count api (new)

![image-2025-3-26_9-25-29.png](attachments/image-2025-3-26_9-25-29.png)

graphql query api (old)

![image-2025-3-26_9-29-6.png](attachments/image-2025-3-26_9-29-6.png)

Conclusion: overall performance of count query is better than normal query.

**TODO: high volume cashflow PT.**

# Benefits

| Name | Description |
| --- | --- |
| Extend Query Capability | Support AND/OR/GROUP for query. Support ORDER. |
| Compatible with OpenSearch | Full compatible with OpenSearch query, seamless migration to OpenSearch when ready. |
| GraphQL Best Practice | Used Standard GraphQL implementation |
| Better Performance & Less Risk | No risk of OOM issue |