# **The purpose**

# **System architecture design**

## RatanOne Service

| Num | Service name | Type | Responsibility | Note |
| --- | --- | --- | --- | --- |
| 1 | FMO-Shell | Frontend | | |
| 2 | FMO Post Trade Portal | Frontend | | |
| 3 | AUTHENTICATION | Common | | |
| 4 | SINGLE-UI-BFF | Common | | |
| 5 | RATANONE-API-GATEWAY | Common | | |
| 6 | CONFIG-SERVER | Common | | |
| 7 | CONFIRMATION-ORCHESTRATION | Common | | |
| 8 | DISCOVERY-SERVICE | Common | | |
| 9 | MESSAGE-BRIDGE | Common | | |
| 10 | MESSAGE-EVENT | Common | | |
| 11 | RATAN-SERVICE-GUI-BFF | Common | | |
| 12 | RATANONE-CASHFLOW-SERVICE | BAU | | |
| 13 | RATANONE-DATA-AMBASSADOR | Common | | |
| 14 | RATANONE-EXCEPTION-SERVICE | BAU | | |
| 15 | RATANONE-QUERY-SERVICE | BAU | | |
| 16 | RATANONE-SETTLEMENT-ORCHESTRATION | BAU | | |
| 17 | RATANONE-STAMPING-SERVICE | BAU | | |
| 18 | RATANONE-STATIC-DATA-SERVICE | Common | | |
| 19 | RATANONE-STELLA-AMBASSADOR | Common | | |
| 20 | RATANONE-Swift MX Convertion service | BAU | | |
| 21 | RATANONE-SUPPRESSION-SERVICE | BAU | | |
| 22 | RATANONE-TRADE-SERVICE | BAU | | |
| 23 | RATAN-CASH-SETTLEMENT-NETTING-SERVICE | CN | | |
| 24 | RATAN-CASH-SETTLEMENT-ORCHESTRATION | CN | | |
| 25 | RATAN-CASH-SETTLEMENT-QUERY-SERVICE | CN | | |
| 26 | RATAN-CASH-SETTLEMENT-SSI-STAMPING-SERVICE | CN | | |
| 27 | RATAN-CASHFLOW-LIFECYCLE-SERVICE | CN | | |
| 28 | RATAN-EXCEPTION-SERVICE | CN | | |
| 29 | RATAN-MXG-CASHFLOW-ADAPTOR | CN | | |
| 30 | RATAN-RULE-SERVICE | CN | | |
| 31 | RATAN-CASH-SETTLEMENT-GROUP-MANAGEMENT-SERVICE | CN | | |

## The technical stack of the Cash Settlement Platform

| Number | Name | Category | Version | Note |
| --- | --- | --- | --- | --- |
| 1 | React | Frontend | 17 | |
| 2 | GraphQL | Frontend | 15.4.0 | |
| 3 | antd | Frontend | 4.9.4 | UI component |
| 4 | Typscript | Frontend | 4 | |
| 5 | Spring Boot | Backend | 2.6.6 | |
| 6 | Spring Cloud Gateway | Backend | 3.1.1 | |
| 7 | Spring Cloud Open Feign | Backend | 3.1.1 | spring-cloud-starter-openfeign |
| 8 | Camunda engine | Backend | 7.10.0 | |
| 9 | Spring BPM Camunda | Backend | 3.2.0 | camunda-bpm-spring-boot-starter-root |
| 10 | Spring Cloud Consul | Backend | 3.1.0 | spring-cloud-starter-consul-discovery |
| 11 | Kafka | Infra | 2.5.0 | |
| 12 | CONSUL | Infra | V1.10.12 | |
| 13 | PostgreSQL | Infra | 12.x | |
| 14 | ElasticSearch | Infra | 8.1.0 | log search/index (ELK) |
| 15 | Logstash | Infra | 8.1.0 | Log message (ELK) |
| 16 | Kibana | Infra | 8.1.0 | Web Front End (ELK) |
| 17 | Redis | Infra | 6.2.6 | will update to 6.2.6 |
| | | | | |
| | | | | |

# **Component design**

## Functional

| Functional | design Link |
| --- | --- |
| Query for SSDR | [Ratan expose the cashflow data to SSDR ](https://confluence.global.standardchartered.com/display/DSP/Ratan+expose+the+cashflow+data+to+SSDR)design |

## Non-Functional

| Non-Functional | design Link |
| --- | --- |
| cache layer | [The cache data layer design](https://confluence.global.standardchartered.com/display/DSP/The+cache+data+layer+design) |
| | |

# **Data**

## System data volume

![image2023-4-25_16-54-13.png](attachments/image2023-4-25_16-54-13.png)
📎 [STP Volumn.xlsx](attachments/STP Volumn.xlsx)

## Data volume estimate

| Year | Daily average Vol | Daily Max Vol | Monthly average Vol | Monthly Max Vol | Annual average Vol | Annual Max Vol | Half of annual average Vol | Half of annual Max Vol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023（2%） | 400 | 900 | 8800 | 19,800 | 105,600‬ | 237,600 | 52,800 | 118,800‬ |
| 2024（90%) | 18,000‬ | 40500 | 396,000‬ | 891000 | 4,752,000‬ | 10,692,000‬ | 2,376,000 | 5,346,000‬ |

| Year | Daily average records | Daily average 8 hours to handle | Daily average 24 hours to handle | Daily Max records | Daily Max 8 hours to handle | Daily average 24 hours to handle |
| --- | --- | --- | --- | --- | --- | --- |
| 2023（2%） | 400 | 0.83 records/min | 0.28 records/min | 900 | 1.875 records/min | 0.625 records/min |
| 2024（90%) | 18,000‬ | 37.5 records/min | 12.5 records/min | 40500 | 84.3 records/min | 28.1 records/min |

📎 [Murex_Payment_Volume202310311534.csv](attachments/Murex_Payment_Volume202310311534.csv)

Murex

| Month | ACU SING | DBU SING | GCT | GIFTCITY | HONGKONG | LONDON | MUMBAI | OBU TAIPEI | SACU SING | SDBU SING | SSTL | TAIPEI | Total Records | Daily average records | Daily Max Vol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9 | 80 | 125 | 2 | 181 | 20814 | 731854 | 19255 | 7042 | 27342 | 4863 | 8 | 2445 | 814,011 | 40,500 | 63,720 |
| 10 | 69 | 163 | 9 | 105 | 19731 | 707800 | 12132 | 3349 | 28644 | 4777 | 0 | 2223 | 779,002 | 38,950 | 57,871 |
| 11 | | | | | 6140 | 62468 | | | | | | | | | |
| 12 | | | | | 3427 | 79899 | | | | | | | | | |

| | Daily average Vol | Daily Max Vol | Monthly average Vol | Monthly Max Vol | Annual average Vol | Annual Max Vol | Half of annual average Vol | Half of annual Max Vol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Murex Data | 40,500 | 63,720 | 810,000‬ | 1,274,400 | 9,720,000 | 15,292,800 | 4,860,000‬ | 7,646,400 |

| | Daily average records | Daily average 8 hours to handle | Daily average 24 hours to handle | Daily Max records | Daily Max 8 hours to handle | Daily average 24 hours to handle |
| --- | --- | --- | --- | --- | --- | --- |
| Murex Data | 40,500 | 84.3 records/min | 28.1 records/min | 63,720 | 132.7 records/min | 44.2 records/min |