# Concept of UI Performance Metrics

## Basic Metrics

![UI-Performance-Concept.jpg](attachments/UI-Performance-Concept.jpg)

### FCP: First Contentful Paint

First Contentful Paint marks the time at which the first text or image is painted.

### FMP: First Meaningful Paint

The duration of finishing rendering the content user concerts.

### TTI: Time to Interactive

The duration when user can interactive with application, depend on the loading of action logic.

### TBT: Total Blocking Time

Sum of all time periods between FCP and Time to Interactive, when task length exceeded 50ms.

### LCP: Largest Contentful Paint

Largest Contentful Paint marks the time at which the largest text or image is painted

### FID: First Input Delay

The duration from first user interaction with page to the page response.

> [https://web.dev/user-centric-performance-metrics/](https://web.dev/user-centric-performance-metrics/)

## Refer Values of Basic Metrics

| Metric | Good | Need Improvement | Poor |
| --- | --- | --- | --- |
| FCP | < 1.8 sec | 1.8 ~ 3.0 sec | > 3 sec |
| LCP | < 2.5 sec | 2.5 ~ 4.0 sec | > 4 sec |
| FID | < 100 ms | 100 ~ 300 ms | > 300 ms |
| TTI | Reduce the gap between FCP to TTI |
| TBT | Reduce the TBT |

> FCP: [https://web.dev/fcp/](https://web.dev/fcp/)
>
> LCP: [https://web.dev/lcp/](https://web.dev/lcp/)
>
> FID: [https://web.dev/fid/](https://web.dev/fid/)
>
> TTI: [https://web.dev/tti/](https://web.dev/tti/)
>
> TBT: [https://web.dev/tbt/](https://web.dev/tbt/)

## Custom Metrics

We can define custom metrics based on our UI rendering logic, such as duration of cashflow data first page.

Example:

| Metric Name | Description | Value |
| --- | --- | --- |
| Cashflow Loaded | Duration from init cashflow blotter to display the first data table | < 3 sec |
| Cashflow Table Loaded | Duration from init cashflow table to display the first data table | < 300 ms |
| Cashflow Quick Search Interaction | Duration from click search button to display the search result | < 500 ms |
| Cashflow Custom Search Interaction | Duration from change custom search or view to display the result | < 1000 ms |

# RatanOne UI Loading Bottleneck

## Benchmark Case and Environment

| Name | Environment | Description | Expect | Layout Strucure |
| --- | --- | --- | --- | --- |
| Case I | UAT Office Network | Workspace1: Cashflow Blotter Workspace2: None | ![image2022-12-7_15-10-11.png](attachments/image2022-12-7_15-10-11.png) | ![UI-Performance-Case I.jpg](attachments/UI-Performance-Case I.jpg) |
| Case II | UAT Office Network | Workspace1: Cashflow Blotter, Suppression Rules And Validation Exception In first screen Workspace2: None | ![image2022-12-7_15-15-0.png](attachments/image2022-12-7_15-15-0.png) | ![UI-Performance-Case II.jpg](attachments/UI-Performance-Case II.jpg) |
| Case ||| | UAT Office Network | Workspace1： Cashflow Blotter and Trade Blotter In first screen; Validation Exception and Settlement Exceptions In second screen Workspace2： None | ![image2022-12-7_15-26-14.png](attachments/image2022-12-7_15-26-14.png) | ![UI-Performance-Case III.jpg](attachments/UI-Performance-Case III.jpg) |
| Case IV | UAT Office Network | Workspace1： Cashflow Blotter and Trade Blotter In first screen; Workspace2： Validation Exception and Settlement Exceptions behind | ![image2022-12-7_15-26-14.png](attachments/image2022-12-7_15-26-14.png) | ![UI-Performance-Case IV.jpg](attachments/UI-Performance-Case IV.jpg) |

## Benchmark Score

| Case | FCP | TTI | TBT | LCP | Performance Score |
| --- | --- | --- | --- | --- | --- |
| I | 1.9 sec | 8.8 sec | 2000 ms | 3.1 sec | 27 |
| II | 1 sec | 9.2 sec | 4350 ms | 2.2 sec | 27 |
| III | 1.9 sec | 13.7 sec | 5340 ms | 3.1 sec | 17 |
| IV | 1.7 sec | 19.8 sec | 14100 ms | 3.3sec | 13 |

You may challenge me  the scores are too low, is there something wrong?

Yep, the score is depend on my notebook which perform badly, but it's not a excuse.

Here is the calculator, we try to improve TBT TTI, we may get a better score easily.

![image2022-12-8_15-28-33.png](attachments/image2022-12-8_15-28-33.png)

[https://googlechrome.github.io/lighthouse/scorecalc/#FCP=1540&SI=5090&FMP=4000&TTI=5130&FCI=6500&LCP=2520&TBT=620&CLS=0.04&device=mobile&version=8](https://googlechrome.github.io/lighthouse/scorecalc/#FCP=1540&SI=5090&FMP=4000&TTI=5130&FCI=6500&LCP=2520&TBT=620&CLS=0.04&device=mobile&version=8)

## Bottleneck， Reasons， Improvement

### Config JSON Loading Blocks JS Execution

| Topic | Description |
| --- | --- |
| Phenomenon | With local cache, still have to wait, when single application ( Case I ) |
| Reason | Each Blotter Application will load different config Json synchronously, will block main.js |
| | ![](https://confluence.global.standardchartered.com/download/attachments/2608603607/Annotation%202022-12-06%20102508.jpg?version=1&modificationDate=1670293540000&api=v2) |
| Improvement | Config Map Solution: - Provide an API to GET config in one request; - Support config file http-cache-control, server side cache control, loading fast enough; - Support config file sync, version, audit, DEVOPS hook; - Manage config under policy, with access control and handle settings easily. |
| Benefit: - Reduce IO, fasten main application JS execute. - Particle, Flexible management of config file. - More optimize measure compared with only Javascript. |

Benchmark Properties:

- DEV-EKS
- Performance API - Trade & Cashflow Blotter

| Trade (Benchmark I) | CashFlow(Benchmark I) | CashFlow Wth Zipped Config(Benchmark II) |
| --- | --- | --- |
| ![image2022-12-12_18-37-38.png](attachments/image2022-12-12_18-37-38.png) | Action | Duration | Total Time | | --- | --- | --- | | load-config-start | 0 | 0 | | load-ratanConfig-done | 315.60 | 315.60 | | load-cashflowDetailsConfig-done | 276.20 | 591.80 | | load-cashflowDetailsConfig-done | 274.60 | 866.40 | | load-tradeDetailsConfig-done | 276.30 | 1142.70 | | load-tradesConfig-done | 265.50 | 1408.20 | | load-exceptionConfig-done | 267.70 | 1675.90 | | load-cashflowConfig-done | 0.00 | 1675.90 | | set-config-done | 0.20 | **1676.10** | | mount-app | 2170.60 | 3846.70 | | FMP: mount-cashflow-grid | 610.70 | 4457.40 | | ![image2022-12-12_18-38-19.png](attachments/image2022-12-12_18-38-19.png) | Action | Duration | Total Time | | --- | --- | --- | | load-config-start | 0 | 0 | | load-ratanConfig-done | 314.60 | 314.60 | | load-cashflowDetailsConfig-done | 285.20 | 599.80 | | load-cashflowDetailsConfig-done | 290.00 | 889.0 | | load-tradeDetailsConfig-done | 288.30 | 1178.10 | | load-tradesConfig-done | 285.20 | 1463.30 | | load-exceptionConfig-done | 286.70 | 1750.00 | | load-cashflowConfig-done | 0.00 | 1750.00 | | set-config-done | 0.10 | **1750.10** | | mount-app | 435.30 | 2185.40 | | FMP: mount-cashflow-grid | 708.60 | 2894.00 | | ![image2022-12-12_19-6-1.png](attachments/image2022-12-12_19-6-1.png) | Action | Duration | Total Time | | --- | --- | --- | | load-config-start | 0 | 0 | | load-zippedConfig-done | 257.60 | 257.60 | | load-config-all-done | 0.20 | 257.80 | | set-config-done | 0.00 | **257.80** | | mount-app | 343.90 | 601.70 | | FMP: mount-cashflow-grid | 424.30 | 1026.00 | |
| Action | Duration | Total Time |
| load-config-start | 0 | 0 |
| load-ratanConfig-done | 315.60 | 315.60 |
| load-cashflowDetailsConfig-done | 276.20 | 591.80 |
| load-cashflowDetailsConfig-done | 274.60 | 866.40 |
| load-tradeDetailsConfig-done | 276.30 | 1142.70 |
| load-tradesConfig-done | 265.50 | 1408.20 |
| load-exceptionConfig-done | 267.70 | 1675.90 |
| load-cashflowConfig-done | 0.00 | 1675.90 |
| set-config-done | 0.20 | **1676.10** |
| mount-app | 2170.60 | 3846.70 |
| FMP: mount-cashflow-grid | 610.70 | 4457.40 |
| Action | Duration | Total Time |
| load-config-start | 0 | 0 |
| load-ratanConfig-done | 314.60 | 314.60 |
| load-cashflowDetailsConfig-done | 285.20 | 599.80 |
| load-cashflowDetailsConfig-done | 290.00 | 889.0 |
| load-tradeDetailsConfig-done | 288.30 | 1178.10 |
| load-tradesConfig-done | 285.20 | 1463.30 |
| load-exceptionConfig-done | 286.70 | 1750.00 |
| load-cashflowConfig-done | 0.00 | 1750.00 |
| set-config-done | 0.10 | **1750.10** |
| mount-app | 435.30 | 2185.40 |
| FMP: mount-cashflow-grid | 708.60 | 2894.00 |
| Action | Duration | Total Time |
| load-config-start | 0 | 0 |
| load-zippedConfig-done | 257.60 | 257.60 |
| load-config-all-done | 0.20 | 257.80 |
| set-config-done | 0.00 | **257.80** |
| mount-app | 343.90 | 601.70 |
| FMP: mount-cashflow-grid | 424.30 | 1026.00 |

Test

iFrame Application Background Loading Uncontrollable

| Topic | Description |
| --- | --- |
| Phenomenon | - The blotter in first screen is loaded later than the blotter in second screen (Case III) - The blotter in first screen is loaded later than the blotter behind (Case IV) - More blotters will be slower and load progress become confuse |
| | ![image2022-12-8_15-7-18 (2).png](attachments/image2022-12-8_15-7-18 (2).png) |
| Reason | - Blotter is loaded in iFrame, shell didn't arrange loading priority |
| Improvement | - Add Skeleton take a layout place before load - Design loading priority control logic - Share loading statues through "ratan-message" ![UI-Performance-Loading Confuse.jpg](attachments/UI-Performance-Loading Confuse.jpg) |
| | Benefit: - User will access first screen faster - Load on requirement |

# Keep An Eye on Performance in Long Term

| How | Why |
| --- | --- |
| Possibility of Migrate Framework to Single-SPA | - iFrame micro-frontend can easily separate style and resolve cross-domain message, when we add more and more blotter, optimize will limited - duplicate resource - can not load core js in shell reduce each application js size |
| Add Custom Performance Track Case | Help us get more detail and know where is the bottleneck in runtime |
| Performance Monitor | For collecting and analyzing performance statues |

# GraphQL

## Background

Now, "CN Cash Settlement" cashflow blotter UI fetching data follows the graphQL.

How to improve performance?

Any benefit from graphQL in short term and long term?

## Why GraphQL

### One UI render depend on serval resource from micro-service

![UI-Performance-Without graphQL.jpg](attachments/UI-Performance-Without graphQL.jpg)

In this case, to render a UI, may contain several request, for example: a list api, value configs for fields apis.

and have to wait all the api response, merge in client side.

With graghQL, we may pay more operation effort, but if in very complex frontend case it will help a lot.

![UI-Performance-graphQL less IO.jpg](attachments/UI-Performance-graphQL less IO.jpg)

**IMPORTANT: Makesure the mirco-service is highly performance, the perfermance of graphQL is depend on the lowest.**

### Friendly to Domain Drive Design

GraphQL is closer to domain model

![UI-Performance-DDD.jpg](attachments/UI-Performance-DDD.jpg)

### An Important UI Infra (BFF)

- BFF: Backend for Frontend, improve the first view performance.

| Name | Description | Provider |
| --- | --- | --- |
| GraphQL | Provide flexible request and data. | Facebook, Netflix |
| SSR | Server Side Rendering. | React, Vue |
| ConfigMap | UI application env file management. | |

- Flexible integration with database, a REST API, a cloud service, and a JSON file

**![](https://cdn.hashnode.com/res/hashnode/image/upload/v1617264296534/9o-zqrCgn.png?auto=compress,format&format=webp)
**

## CN query-service Restful API vs GraphQL testing

Before Testing：

- Prepare 10,000,000 Data in DB
- Prepare request body, will fetch same amount of data

| | GraphQL | Restful |
| --- | --- | --- |
| URL | /v1/query/cashflows | /v1/query/cashflows |
| POST body | ``` { "variables": {}, "query": "{\n cashflowsNew(\n filter: [{ field: \"Cashflow.Cashflow_State\", operator: NOTIN, values: [\"NETTED\",\"DEAD\"]}]\n page: 0\n size: 100\n) {\n pageInfo {\n totalHits\n pageNo\n pageSize\n lastPage\n }\n results {\n FMO_Comments {\n FMO_Comment\n FMO_Comment_Timestamp\n FMO_Comment_Updater\n }\n Cashflow {\n Cashflow_Business_Version\n Cashflow_Version\n Cashflow_State\n Cashflow_Affirmation_Status\n Cashflow_Event_Type\n Cashflow_Minor_Version\n Payment_Currency\n Payment_Date\n Payment_Type\n Payment_Cutoff_Time\n Pay_Receive_Indicator\n Payment_Amount\n Netting_Id\n Payment_Receiver_Party_Reference\n Payment_Payer_Party_Reference\n Cashflow_Sub_State\n Cashflow_Sub_State_Type\n Cashflow_Sub_State_Updater\n Status_Event_Type\n Event_Date\n }\n Entity {\n Booking_Entity_SCI_FMID\n Booking_Entity_SCI_FMCODE\n Counterparty_SCI_FMID\n Counterparty_SCI_FMCODE\n }\n Portfolio {\n Booking_Entity_Trade_Portfolio_Name\n }\n }\n }\n}\n" } ``` | ``` { "filter": [ {"field": "Cashflow.Cashflow_State", "operator": "NOTIN", "values": ["NETTED", "DEAD"]} ], "page": 0, "size": 100 } ``` |
| Response Total Hits | 11 | 11 |

**Case 1： how much time needed before fetch data**

Send One request to the two api by Postman， each request add timestamp

![image2022-12-13_19-55-44.png](attachments/image2022-12-13_19-55-44.png)

| | GraphQL | Resuful |
| --- | --- | --- |
| before query data | 77 ms | 119 ms |
| fetch data | 3819 ms | 3619 ms |
| response | 3860 ms | 3720 ms |
| Response Size | 9.93 KB | 60.66 KB |

### Case 2：Concurrency Post Bottleneck test

Request Timeout: 30s

Env: Local

Worker: 15

| reqeuests | workers | GraphQL | Resuful |
| --- | --- | --- | --- |
| 10 | 10 | 5.05 sec | 5.06 sec |
| 50 | 10 | 18.19sec | 18.14 sec |
| 100 | 20 | 41.34 sec | 44.4 sec |
| 300 | 20 | 130.08 sec | 143.22 sec |

### Case 3: Single Request  on request traffic

- start load test (300 request)
- wait for 40sec then trigger one request

| | GraphQL | Resuful |
| --- | --- | --- |
| response | 11.89 sec / 9.04kb ![image2022-12-13_21-50-40.png](attachments/image2022-12-13_21-50-40.png) | 13.12 sec / 60.66KB ![image2022-12-13_21-53-5.png](attachments/image2022-12-13_21-53-5.png) |

### Compare

| | GraphQL | Restful |
| --- | --- | --- |
| Request Resolve | Better | |
| **Data Fetch** | Same | Same |
| **Concurrent Performance** | Same | Same |
| Response size | Better | |
| Support Paging | True | True |
| Support JWT | True | True |

## **Further Test On Staging Env**

| Requests | Index | **First Page of UI Datagrid** | ** Find Cashflows By Cashflow_Id （Field with DB Index）** |
| --- | --- | --- | --- |
| | | **GraphQL** | **Restful** | **GraphQL** | **Restful** |
| **Single Request** | Request Structure | ![image2022-12-26_12-8-25.png](attachments/image2022-12-26_12-8-25.png) | ![image2022-12-26_11-57-57.png](attachments/image2022-12-26_11-57-57.png) | ![image2022-12-26_12-37-1.png](attachments/image2022-12-26_12-37-1.png) | ![image2022-12-26_12-29-59.png](attachments/image2022-12-26_12-29-59.png) |
| Parse Params Duration**<sup>1</sup>** | 176 ms | 190 ms | 180 ms | 183 ms |
| Response Size | 89.27 KB | 658.77KB | 2.08 KB | 13.43 KB |
| Total Duration | 1883 ms | 3580 ms | 271.45 ms | 500.62 ms |
| | ![image2022-12-26_14-53-51.png](attachments/image2022-12-26_14-53-51.png) | ![image2022-12-26_14-54-36.png](attachments/image2022-12-26_14-54-36.png) | ![image2022-12-26_12-38-4.png](attachments/image2022-12-26_12-38-4.png) | ![image2022-12-26_12-35-54.png](attachments/image2022-12-26_12-35-54.png) |
| **Concurrently Send Requests ** | **Requests** | **Works** | **Duration** | **Duration** | **Duration** | **Duration** |
| 10 | 10 | 6.09 sec | 9.06 sec | 1.04 sec | 2.04 sec |
| 50 | 10 | 26.23 sec | 49.52 sec | 2.07 sec | 3.09 sec |
| 100 | 20 | 56.42 sec | 77.85 sec | 2.04 sec | 3.04 sec |
| 300 | 20 | 174.59 sec | 217 sec | 3.05 sec | 5.06 sec |
| 300 | 150 | - | - | 2.11 sec | 2.23 sec |
| 300 | 300 | - | - | **2.10 sec<sup>2</sup>** | 2.49 sec |
| 500 | 100 | - | - | 3.14 sec | 4.21 sec |

1. <u>*GraphQL parsing params is same as Restlful.*</u>
2. <u>*My laptop can only open 300 parallel wokers and become slow.*</u>

## Support

### Community

Individuals can follow these channels for updates and information:

- http://[github.com/graphql](https://github.com/graphql)
- [https://discord.graphql.org/](https://discord.graphql.org/)

### GraphQL Foundation

"GraphQL Foundation" supports community

> The **GraphQL Foundation** is a neutral foundation founded by global technology and application development companies.
>
> The GraphQL Foundation encourages contributions, stewardship, and a shared investment from a broad group in vendor-neutral events, documentation, tools, and support for GraphQL.

Organization membership:

> Organizations can [join the GraphQL Foundation](https://graphql.org/foundation/join/#graphql-foundation), which is the non-profit that supports the sustainability of the GraphQL community.
>
> This is accomplished through annual membership fees, which are allocated by the Governing Board for the benefit of the GraphQL ecosystem.

Benefits:

> The GraphQL Foundation Governing Board is responsible for setting high-level policy and allocating the GraphQL Foundation budget in ways that benefit the technical community.
>
> The first 20 members of the GraphQL Foundation participate as voting members of the Governing Board. Any additional members vote to select up to five additional seats.