# Background

As user raised requirement for better query performance, we need to consider push the OpenSearch to business live in 2026

OpenSearch has already technical Live with cashflow/cashflow history data persistence implemented, the next step would be:

1. Other domain data persistence if required.
2. Query business data from OpenSearch and decommission PG as a target.

# Objective

OpenSearch Business Live, but before that, we need a detail plan to make it happen

# Materials

OpenSearch Technical Go-Live: [OpenSearch Technical Go Live Introduction - 2025 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/OpenSearch+Technical+Go+Live+Introduction+-+2025)

OpenSearch PT: [2024-12-16: OpenSearch Inbound/Outbound Performance Testing - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3212175335)

# Solutioning

## Overview

Day-1 Internal Flow Switch to OpenSearch

1. Development base on detail data flow. 1. Other domain data persistence(Trade, NSTP Exception) 2. Query from OpenSearch base on Ultra query.
2. Cashflow Blotter & Detail Query from OpenSearch is the default behavior. and keep the PG persistence as well.
3. Cashflow Dashboard Query from OpenSearch is the default behavior.
4. If any issues from production, 2, 3 switch to PG query immediately.
5. One time data migration with cutoff time to ensure all historical data and real time data exist after business live.
6. Data migration should be idempotent to prevent the generation of dirty data.
7. Real time recon is required among three data sources 1. Lifecycle service - SCBML history 2. Query service PG - cashflow data & cashflow data history 3. OpenSearch - cashflow index & cashflow history index

Day-2 External Flow Switch to OpenSearch

1. If any change with current OpenSearch data model, external query need to be changed as well.
2. Open the Firewall, provide v2 API for query.

## Data Model Adaptation

### Sort out RatanCashSettlementData.proto, ResultNew graphql schema and opensearch schema definition. Need to align with each other without any confusion.

1. Difference between data persistence model and data query model
2. Current GraphQL query covers domain data as below, need to identify which should from OpenSearch, with from domain service.

- - Cashflow Data Query - Cashflow Data History Query - Exception Query - SSI Stashing Query - SSI Candidates Query - Affirmation Details - Netting Component Query

## Data Flow Implementation

Currently in prod(after technical live), cash settlement is using double-writing model, and other domain data need to follow the same strategy.

### OpenSearch Integration Low Level Design(Internal Flow)

1. Query from Opensearch

## Real-time Reconciliation

Link: [Middleware - OpenSearch - Ratan Central Monitoring - Middleware & Microservice Level - Dashboards - Grafana](https://uklvapapp591.gdc.standardchartered.com:3000/d/fxz10qqf6kvswa/middleware-opensearch?from=now-5m&to=now&timezone=browser&var-application=ratanone-opensearch-agent&var-instance=uklvadrtn002a.pi.dev.net:ratanone-opensearch-agent:0&var-datasource=de6jyvajhwbnkd&var-Month=2025-08&var-monthPattern=2025-08.%2A&var-Day=$__all&refresh=5m)

Data reconciliation is an important data monitoring approach. It brings us confidence and proudly say the system is running well, no issues.

Otherwise, if there are any issues, it also enables us to detect and resolve them in a timely manner.

Currently in prod we have a data recon section in Grafana dashboard. But it is not accurate. So we need to enhance it.

![image-2025-12-4_16-56-42.png](attachments/image-2025-12-4_16-56-42.png)

## Exception Management

Once we have the real-time reconciliation. If any data mismatched, if 20 record missing, then we want to know which are the missing cashflows, without a doubt.

Currently, OpenSearch agent has exception handling with Kafka non-blocking retry, but no further operation on DLT messages. Better we have a index to record the DLT messages

and provide manual/auto replay function accordingly.

## Data Migration

Historical Data Migration is an important step before business live. Keeping data integrity and consistency can make the underlying data source change transparency to user,

which helps build users' trust in switching of the underlying database, as we ensure that it will not impact our business at all.

| Industry ETL Tool | Language | Pros | Cons | Official Website | |
| --- | --- | --- | --- | --- | --- |
| pgsync | Python | lightweight | only support PG as data source | [AtomGit | GitCode - 全球开发者的开源社区,开源代码托管平台}](https://gitcode.com/gh_mirrors/pgs/pgsync) | |
| Apache NIFI | java | support customized requirement UI management | Complicate Learning curve not easy to maintain | [Apache NiFi](https://nifi.apache.org/) | |
| Logstash | Ruby | existing tech stack | Need development | [Logstash: Collect, Parse, Transform Logs | Elastic](https://www.elastic.co/logstash) | |
| Self Development | Java/python | easy to customized | dev effort | | |

## CCR Enhancement

Need Zeyu's input

## Data Visible

Opensearch Dashboard

Dev: [OpenSearch Dashboards](http://10.198.199.160:5602/app/home)

DBever Driver

## Relevant Repo

[51358-ratan-cashflow-lifecycle-service - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cashflow-lifecycle-service)

[51358-ratan-cash-settlement-query-service - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service)

[51358-ratanone-data-provider-internal-client - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-data-provider-internal-client)

[51358-ratanone-internal-component-simulator - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-internal-component-simulator)

[51358-ratanone-data-provider-external-client - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-data-provider-external-client)

[51358-ratanone-external-component-simulator - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-external-component-simulator)

[51358-ratanone-opensearch-agent - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-opensearch-agent)

[51358-ratanone-grpc-api - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-grpc-api)