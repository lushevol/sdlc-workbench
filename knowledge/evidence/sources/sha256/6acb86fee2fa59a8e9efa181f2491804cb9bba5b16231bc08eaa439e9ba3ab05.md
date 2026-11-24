In previous GraphQL proposal, we made a new schema to includes cashflow details query. Here we are going to complete GraphQL schema to more scenarios.

# FMRP Strategic Settlement Scenarios

## Cashflow Blotter

| Action | Type | Description | Proposal Schema |
| --- | --- | --- | --- |
| Cashflow Record Count | Query | Only get the count of cashflows. Have the same parameters with cashflows query. | type Query { cashflowsCount(filter:[FilterArg]): ResultPageInfo! } type ResultPageInfo { totalHits: Float! } |
| Top Exposure | Query | Get the top N counterparties trading with SCB. | type query { topExposure(filter: [FilterArg], top: Int!): [TopExposureRecord!]! } type TopExposureRecord { counterparty: String! clientType: String! amount: Float! } |

## Group Blotter Query

| Action | Type | Description | Schema |
| --- | --- | --- | --- |
| Group Record Count | Query | Only get the count of group records. Have the same paramters with group blotter query. | type Query { groupMessagesCount(filter:GroupMsgReq): ResultPageInfo! } type ResultPageInfo { totalHits: Float! } |

## Exception

| Action | Type | Description | Schema |
| --- | --- | --- | --- |
| Exception Statistic From Filter | Query | get exception statistic by filters, filters are the same pattern with cashflow query. | type Query { exceptionCodeStatisticsByFilter(filter:[FilterArg!]!): [ExceptionCodeStatistics!]! } type ExceptionCodeStatistics { exceptionCode: String! count: Int! } |

## Rate

| Action | Type | Description | Schema |
| --- | --- | --- | --- |
| Rate to USD | Query | Get rate of current ccy to USD | type Query { rate2usd(ccy: [String!]!): [Rate2USDMapping] } type Rate2USDMapping { ccy: String! rate: Float! } |

## Netting

| Action | Type | |
| --- | --- | --- |
| Netting Preview | Query | |
| Netting Execution | Mutation | |