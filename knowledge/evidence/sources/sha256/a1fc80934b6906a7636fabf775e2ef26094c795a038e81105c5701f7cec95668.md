[RATAN Foundation 2.0 - OpenSearch : Development Plan - 202407 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+Foundation+2.0+-+OpenSearch+%3A+Development+Plan+-+202407#RATANFoundation2.0OpenSearch:DevelopmentPlan202407-No-FunctionRequirementDefinition)

# Use Case Definition

1. Main goal 1. Better performance on UI query 2. Less pressure on relational database
2. Impacted blotters: 1. cashflow blotter 2. cashflow details page 3. dashboard 4. Group blotter 5. API expose to third party

| **Item** | **Details** | **NFR** |
| --- | --- | --- |
| Cashflow blotter | Payment date query SLA | 2s for initial loading & each subsequent page loading of 20k cashflows including usage of filters Default page size: 20,000 Update the load next button to 20,000 Remove the limitation to fetch more than 30 days and replace it with limitation based on volume |
| Pre Validation Blotter (Group Blotter) | | 2s for initial loading & each subsequent page loading of 20k cashflows Default page size: 20,000 Pending only Update the load next button to 20,000 |
| Dashboard | | 2s to load |
| Trade Details | | Depending on TDS/TDSX performance |
| Cashflow Details | | 1 seconds |
| Cashflow History | | 1 seconds |
| Swift Query | | 1 seconds |
| Accounting Query | | 1 seconds |
| Static/Rules | | 2 seconds |
| | | |
| Exception handling | Single exception processing | 1 s |
| | Bulk exception processing | 3 s for 1000 records |
| Netting | Manual Netting | 5 seconds for 50,000 records |
| | CLS Netting | 1 M per Month |
| Swift/Cashflow Suppression | Bulk | 3 s for 1000 records |
| | Single | 1 seconds |

# Plan

Issues:

1. HA issue. CCR does not work for data sync up between 2 data centers.
2. Data issue: FMO Comment timestamp data format on nano. Discover - Elastic
3. Real time recon missing
4. No proper UAT yet

| | Activity | Time | Purpose |
| --- | --- | --- | --- |
| 1 | Open Search Agent Delivery to production | 2026-01-31 | Technical live for data loading |
| 2 | Query service delivery (new code, no overlap) UI delivery (New cashflow blotter) (new code, no overlap) | 2026-02-07 | Technical live for pilot users only, a new tile |
| 3 | | | |
| 4 | Real time recon | | |
| 5 | CCR issue | | |
| 6 | UAT | | |
| 7 | Data migration | | |
| 8 | Production data dev access (Kibana) | | |

On FMRP2:

1. Kibana readiness @Zeyu Zhou
2. New open search agent installation @zhang jiangnan @Zeyu Zhou

| | | Complete date | Owner |
| --- | --- | --- | --- |
| Development | OpenSearch schema update based on UBER Open search agent Query service | 2026-01-28 | @zhang jiangnan @Xinmiao Huang |
| **Open search Agent delivery** | Technical go live to receive | 2025-12-31 | @zhang jiangnan @Zeyu Zhou |
| Development | Data migration strategy from DB to Open Search | 2026-02-06 | @Chen Yang |
| Development | Recon strategy | 2026-02-06 | |
| UAT | UAT on cashflow blotter based on the Open search | | |
| | | | |
| | | | |
| Go Live | DB + Open search in parallel run for 1 month | | |
| Go live | Recon between DB and Open Search | | |
| Go Live | Remove DB dependency post say 1 month | | |
| | | | |

# Non Functional Requirement

1. Supporting Model, infra ownership 1. Maintenance strategy
2. Data Migration