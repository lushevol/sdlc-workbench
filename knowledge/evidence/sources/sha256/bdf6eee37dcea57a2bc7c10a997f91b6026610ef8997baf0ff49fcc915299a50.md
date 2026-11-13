*This article is based on [GraphQL Used For Front End In RATAN]*

To unify the UI query method and proposal to apply GraphQL on all eligible query to take full advantage of it.

# Advantages of GraphQL over Restful API

- Improve performance due to reduced number of requests. Time wasting on browser and network is much more than in backend handling.
- Increase flexibility in terms of data fetching.
- better data validation and error handling.
- reduce network traffic.
- easier to evolve data schema.
- better support for real-time updates.
- Increase security.

# Principle

Every API segment should meet the performance criteria to make the aggregation speed always the best.

### Response Speed Minor Requirement

| API Segment Size | Recommended Response Time | Minor Response Time |
| --- | --- | --- |
| <= 500B | <= 200ms | <= 300ms |
| <= 1KB | <= 200ms | <= 300ms |
| <= 50KB | <= 500ms | <= 1000ms |
| <= 100kb | <= 1000ms | <= 1500ms |

reference: [https://www.hobo-web.co.uk/your-website-design-should-load-in-4-seconds/](https://www.hobo-web.co.uk/your-website-design-should-load-in-4-seconds/)

# Client/Server implementation

| Type | implement | Support Features | details |
| --- | --- | --- | --- |
| Client | Apollo-Client@3.7.13 | Query/Mutations/Subscription/@defer | [https://github.com/apollographql/apollo-client](https://github.com/apollographql/apollo-client) |
| Server | DGS@4.9.24 | Query/Mutations/Subscription | [https://github.com/netflix/dgs-framework](https://github.com/netflix/dgs-framework) |

# Use Cases

## 1. Cashflow - Settlement CN

### Multi Exceptions

Multi Exceptions is new features in CN which could show all exceptions and bulk fixing when viewing cashflow details. It should be covered by GraphQL modeling.

#### Approach Steps

| Steps | Status | Comment | |
| --- | --- | --- | --- |
| Evaluate current Restful APIs | Done | | |
| Mapping current APIs to GraphQL schemas. | Done | | |
| Implement GraphQL new Schema. | Done | | |
| Testing the result and performance, if match performance requirements. | Done | optimize loading time from 2.5s to 1s, reduce 80% request when initialing. - [x] PT on graphql api. | ![image2023-6-1_10-17-47.png](attachments/image2023-6-1_10-17-47.png)![image2023-6-1_10-18-12.png](attachments/image2023-6-1_10-18-12.png) |
| Test all user cases. | Done | | |
| Go live and phase Out Restful APIs. | Done | | |

#### Workflow on Restful API

![image2023-5-8_14-44-17.png](attachments/image2023-5-8_14-44-17.png)

Totally cost 2.5s to finish the whole workflow.

#### GraphQL Aggregation

#### New Schema Definition

##### Query Schema

##### Result Schema

📎 [ratan_suppression_fields_v34.1.0.dev.csv](attachments/ratan_suppression_fields_v34.1.0.dev.csv)

#### Explanation on Schema

schema fields with green color are new added, otherwise are already defined.

| Definition | Schema | Type | Description | Restful Mapping | Restful Loading Speed (Office) (Latency/Resource Size) |
| --- | --- | --- | --- | --- | --- |
| Exception List | ratanException → Exception | New | Realtime exceptions in cashflow. | /v1/rep/exceptions/byEntity | 297ms/677B |
| Maker Input | ratanException → Exception → Stashing | New | User Generated Data which stashed for further usage. Like Maker Input. | - /v1/nstpException/actionData - /v2/stamping/query/makerInput | - 430ms/167B - 295ms/173B |
| Vostro Candidate List | ratanVostroCandidates → SSI Array | New | Available Vostro List | /v2/stamping/query/vostro | 990ms/3.9kB |
| Nostro Candidate List | ratanNostroCandidates → SSI Array | New | Available Nostro List | /v2/stamping/query/nostro | 433ms/708B |
| Affirmation MetaData | ratanAffirmation → AffirmationInfo | New | Affirmation Data | /v1/nstpException/metaData | |
| Back Value MetaData | cashflow → SSI → Swift_Payment_Date | New | Back Value Data | /v1/nstpException/metaData | |
| System Assigned SSI | cashflow → Settlement_Instruction → SSI | Existing | - Good Stamped SSI - Nostro Default when Vostro Exception | - /v2/stamping/cashflow/query/vostro - /v2/stamping/cashflow/query/nostro | - 356ms/2.0kB - 323ms/649B |
| Trade Confirmation Status | cashflow → Confirmation → Confirmation_Staus | Existing | Trade Confirmation Status | | |

#### Related Stories & Tasks

#### Performance Testing

The Average Response Time of all the simples are less than 0.5s, full GraphQL Request cost the most time, ART is 393ms while other partial requests are around 220ms – 320ms.

![image2023-6-6_10-18-38.png](attachments/image2023-6-6_10-18-38.png)

![image2023-6-6_10-18-45.png](attachments/image2023-6-6_10-18-45.png)

P.S. Max time wasting on Full Request and Candidates are pretty long (4.6s and 9.6s) which will be disaster on that query. Maybe we can set timeout for 2s.

## Error Handling

### Partial Failed

Once one field or some fields failed to fetch when query, the correct value eventually can't be read from response. UI expects key or path of those fields are still existing in response, but with <u>empty value</u> sets.

#### Retry Policy

Only resend failed paths to fetch data again.

### Fully Failed

Fully failed often occurs when query services are down or bad network condition.

# FAQ