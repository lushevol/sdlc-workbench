#

# Requirement

ADO: [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11796064](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11796064)

1. Only data will be stored onshore. No change or processing, it will continue to be done by GBS KL users
2. Display Indonesia cashflows on same Post Trade Portal along with other countries (ID data will be stored onshore, but in GUI it will be shown along with other entity data which is stored in GDC)
3. Data Entitlement requirements as applied via CES must be enforced (i.e., ID onshore users get only ID data access. Other country onshore users do not get ID data access unless specifically approved. Group users like GBS Settlements, MO, PSS, Dev, PO get ID data access)
4. There should not be any delays in processing the data (Same benchmark as GDC)
5. No new Business requirements / Functional changes including Profiles
6. Regulatory Reporting should not be impacted

# Questions

**EXPAND: Click here to expand question details...**

| S.N. | Description | Comments | Status |
| --- | --- | --- | --- |
| 1 | Is it possible to connect FM Solace and IBMMQ from ID location, new trust store required? | As confirmed by Geoffrey, for payment flow, Murex IBMMQ can't change which means it can not be 1 producer to multi consumer. For trade flow, it's not ready yet. | |
| 2 | MB has function to persist failure message(payments), is it regulatory eligible if we use GDC MB as an adaptor? | Agreed it is fine | |
| 3 | Can we create new queue for ID region consumption on Trade and SSI+ flow? | Trade and ssi+ flow, we can discuss with them, but not start yet | |
| 4 | User has ID and other entities data entitlement at same time, is it possible? | Yes. | |
| 5 | Is it able for two consumers to consume message from same queue with different group? Is it able for two publishers to publish message to same topic? IBMMQ and Solace queue | Technically yes, but IBMMQ doesn't support currently. refer to 1 and 3 | |
| 6 | How to identify the cluster for different user? physical location or entitlement role? | entitlement role and eligible Legal entity fmid. Details need further analysis | |
| 7 | About infra service, do we need to deploy to ID onshore? If no, what can be defined as infra service? such as data-ambassador, static-data | Not settle down yet, need to align with data Ops for static/rule data maintenance. for DA and other stateless services, we can deploy to ID onshore. Confirmed all related data will store in ID local with local services deployed | |
| 8 | CDUPS is ID upstream ? | | |
| 9 | Static tables are all available? ratan_static__beneficiary_bic_netting ratan_static__cashflow_ebbs_bridge_account ratan_static__cashflow_ebbs_txn_code ratan_static__cashflow_nostro ratan_static_brdm_history ratan_static_brdm_record ratan_static_cashflow_country_mapping ratan_static_cashflow_currency_cut_off ratan_static_cashflow_currency_holiday ratan_static_rdm_holiday_weekend_message ratan_static_spot_rate | Refer to 7 | |

**EXPAND_END**

# Assumptions

1. ID payments will be published by Murex instead of TDS3
2. ID trades will be published by TDS3
3. It's possible for a user who has both ID and Global entitlements
4. It's possible to extract user's region entitlement from JWT, if not, able to enrich the required information to JWT
5. ~~Only cashflow, trade data has regulatory restriction, other data like nostro static, NSTP rules could be persisted in global database ~~

# Solutioning

After several round discussion and agreed with user, ID shoring will isolate all related data with to different location. Ratan GDC and Ratan ID will not interact with each other except murex IBMMQ.

ID and GDC data will be isolated absolutely.

## Deployment Diagram

### Logical Diagram

### Request Flow

## Development Plan(Non-prod Readiness)

[Indonesia Development Plan - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Indonesia+Development+Plan)

## Upstream & Downstream Integration

![image-2026-4-13_17-27-4.png](attachments/image-2026-4-13_17-27-4.png)

## Upstream/Downstream Details

[Indonesia Upstream/Downstream Details - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3788008855)

## Cash Settlement Platform

![image-2026-4-13_16-46-19.png](attachments/image-2026-4-13_16-46-19.png)

# Technical Implementation

## Service Property

For Indonesia instance, there is a new service properties repository **51358-ratan-service-properties-indonesia, **this is for ID Environment variables and profiles configuration.

There is no change on config-server, ansible playbook will rename the folder name to **51358-ratan-service-properties **after deployment done, otherwise the properties can not be found.

```yml
spring:
  cloud:
    config:
      server:
        git:
          uri: file:/apps/ratanrt/services/ratan-service-properties
```

## DB Repository

For Indonesia instance, there is a new repository **51358-ratanone-db-repository-indonesia, **which to cover all DB script for Indonesia particularly.

How to initialize day0 database?

**51358-ratanone-db-repository-indonesia **initialization script includes:

1. Export DDL script from prod(tables, indexes, sequences?)
2. Sort out all DML script

## Time Zone Setting

Considering Ratan ID servers are all in Indonesia location, by default the VM and DB server time zone will be UTC+7 , which has impact on our functions.

1. Job scheduler(Netting, Accounting, Release etc.)
2. Data query which has timestamp condition
3. Upstream data processing with timestamp attribute

Solution details please see child page:

<u>[UTC Time zone impact - Indonesia - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/UTC+Time+zone+impact+-+Indonesia)</u>

## Netting/Splitting

Considering Ratan GDC netting & splitting has cashflow id generating function, which is using hardcoded prefix(S/N) + DB sequence and with "0" in the middle to make a total of 12 digits.

e.g. N + 00000000 + 123 = N00000000123

As Ratan ID will use different DB server and sequence will be start from 1, the potential issue is ID and GDC cashflow id will definitely collided.

Solution is to use a different prefix rather than "N" and configurable the prefix

e.g. NID +  000000 + 123 = N00000000123; SID +  000000 + 123 = N00000000123;

## Upstream data provisioning

ID volume is not large but there are two provisioning ways:

1. real time mxml inbound
2. cashflow batch file
3. fixing flag batch file

For item 1, we can easily implement as below

**Solution diagram - 1**

But there is item 2, with batch file processing, it doesn't work if Ratan ID directly deploy batch-service like GDC, because

1. GDC solution is NAS mounting to Murex and Ratan server, which is not allowed(cross country NAS) by Ratan ID.
2. Batch file not group by booking entity, which means ID payments and non-ID payments will be generated in same file if any.

**Solution diagram - 2**

With diagram1 + diagram2 we need two topic&queue pairs, to make it more easier, only need 1 flow.

**Solution diagram - 3**

****

**Solution compare:**

| Solution | Change points | Suggestion |
| --- | --- | --- |
| Diagram 1 + Diagram 2 | 1. New solace topic & queue for Murex real time Mxml message 2. New solace topic & queue for Murex batch json service 3. [GDC] MB new real time flow & filter setup and existing filter change 4. [GDC] Batch service publish topic should be changed in order to consumed by MB instead of adaptor 5. [GDC] MB new batch flow & filter setup, to publish ID to solace new topic and publish non-ID to existing adaptor topic 6. [ID] MB add 2 new flows to consume real-time and batch messages from GDC | 1. Message routing immediately once identify ID payments 2. Clearly difference real time and batch flows for processing. 3. ID no need to deploy batch-service but mxg-adaptor is required |
| Diagram 3 | 1. Only 1 New Solace topic & queue creation required for SCBML 2. [GDC] Adaptor publish SCBML to message bridge Kafka topic instead of standardization-service topic 3. [GDC] MB consume SCBML from adaptor and publish ID cfs to Solace, non-ID cfs to existing standardization-service topic 4. [ID] MB add 1 new flows to consume SCBML from GDC | 1. Message routing happen when convert to standard SCBML message. 2. 2 two scenarios shares same topic & queue, simpler. 3. ID no need to deploy batch-service and mxg-adaptor, naturally become strategic settlement platform 4. ! There is GDC DB persistence as adaptor will save data to DB while converting to SCBML. |

### Conclusion:

**We will use diagram 3 as data provisioning solution**

1. real time cashflow inbound from murex ibmmq, then adaptor convert to scbml and publish to message bridge, mb will determine whether it goes to FM solace or group service
2. cashflow batch file will follow the existing flow until adaptor publish it out, then follow 1 process.
3. fixing flag batch file will be parsed by batch service who will check the cashflow entity , then determine whether publish to mb, or goes to existing process logic.

## Downstream API Call

According to the deployment diagram above, there are two options to expose our API for downstream query

Option1: Downstream(e.g. DQSL) → Ratan ID directly.

Option 2: Downstream(e.g. DQSL) → Ratan GDC → Ratan ID

| | Option 1 | Option 2 |
| --- | --- | --- |
| Prons | 1. Decouple with GDC 2. FE API call and downstream API call can be clearly distinguished from URL sight | 1. Only need to open firewall between Ratan GDC and Ratan ID 2. FE API call and downstream API call are use same URL |
| Cons | 1. Open firewall for each downstream 2. FE API call and downstream API call are different URL | Has dependency with GDC, but currently all backend API call from UI has this dependency |

Currently we prefer **option 1**

## UI Nginx

All services in Indonesia need to be implemented locally in Indonesia, except for the difference in data between GDC and Indonesia, all other UI layout/API interfaces are the same, so we need a solution on how to distinguish whether call GDC or ID API.

| | Solution Flow | Nginx | Pros | Cons |
| --- | --- | --- | --- | --- |
| Option1 | user login ↓ load importmap.json ↓ SSO login → api response { idns: true } ↓ store.indonisia = true ↓ call injectIdnsImportmap() → Dynamically inject a new importmap, covering the path of the /ratan_ * module as/idns/ratan_* ↓ axios interceptor add prefix /api/ratan/... → /**idns**/api/ratan/... ↓ SystemJS load module use the /idns/xxx path → nginx location /idns/ → proxy_pass [http://idns](http://idns) (uklvadrat0013a:8453) ↓ Indonisia local nginx → local backend services | ``` location /idns/ { rewrite ^/idns/(.*)$ /$1 break; proxy_redirect off; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-Proto http; proxy_set_header X-Forwarded-For $remote_addr; proxy_set_header X-Forwarded-Host $remote_addr; proxy_pass http://idns; } upstream idns { least_conn; server uklvadrat0013a.pi.dev.net:8453; } ``` | 1. Simple nginx config — single location /idns/ block, no conditional logic required 2. Clear observability — URL in access logs clearly distinguishes GDC vs Indonesia traffic 3. Independent environments — Indonesia nginx is fully isolated; config differences between GDC and ID won't interfere with each other 4. Stateless routing — nginx performs pure path-based routing without inspecting business logic | 1. Dual nginx maintenance — Indonesia nginx must maintain a nearly identical set of location blocks as GDC 2. Static module URLs also affected — paths like /ratan_container/, /ratan_cashflow_blotter/ also need the prefix |
| Option2 | ID user login → store.idns = true ↓ axios interceptor add header: X-Idns: true ↓ nginx at the same location，determine the X-idns header through map ↓ 有 header → proxy_pass [http://idns](http://idns) 无 header → proxy_pass [http://ratan_backend_api_gateway（](http://ratan_backend_api_gateway（原)GDC） | ``` map $http_x_idns $idns_backend { default "ratan_backend_api_gateway"; "true" "idns"; } location /api/ratan/ { rewrite ^/api/ratan/(.*)$ /$1 break; proxy_pass http://$idns_backend; } ``` | 1. Clean URLs — API paths remain unchanged, no impact on API contracts 2. No static asset changes — frontend resource URLs are unaffected 3. Follows REST conventions — using headers to differentiate request variants is a standard practice | 1. Complex nginx config — every location that needs routing differentiation must be updated, for these add judgment logic 2. Poor observability — identical URLs in logs make it hard to distinguish GDC vs Indonesia traffic without additional log fields 3. Security risk — clients can spoof the X-Idns header; nginx must sanitize externally supplied headers |

### Summary various URLs

| URL Type | Example | Solution |
| --- | --- | --- |
| API request | /api/ratan/... | Axios interceptor with/idns/prefix |
| Static JS module | /ratan_container/ratan_container.js | runtime dynamic injection of importmap override |
| SSO/Auth request | /api/auth/... | without prefix (using GDC unified authentication) |
| Public resources | /js/external/...、/base/base.js | without prefix (provided uniformly by GDC) |

# Active-Active to Active-Passive

[Active-Active to Active-Passive - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Active-Active+to+Active-Passive)

# Proposal

## Multi-region System

A multi-region system is an architecture where resources, services, and data are deployed across multiple geographic regions (such as different data centers or cloud regions). This design is commonly used to improve availability, disaster recovery, latency, and regulatory compliance.

The system architecture aims to distributes its components across two or more regions, which are typically isolated from each other, with their often with each region operating independently but able to synchronize or replicate data and state as needed. Regions are typically isolated from each other, with their own resources, but can communicate via secure, high-speed links.

Ratan ID shoring will use multi-region system to resolve the regulatory restrictions.

## Deployment Diagram

<details>
<summary>展开详情</summary>

### Option-1 Two Regions Deploy Independently, All services duplicate to ID region, static and rule data are share or not is on demand.

![image-2026-3-17_17-24-9.png](attachments/image-2026-3-17_17-24-9.png)

### Option-2 Two Regions Deploy Independently except shared static data service and rule engine

![image-2026-3-17_17-24-49.png](attachments/image-2026-3-17_17-24-49.png)

</details>

## Ratan Multi-region Detail Design Consideration

### Integration with up streams and down streams

#### Solution A

<details>
<summary>展开详情</summary>

![image-2026-3-15_17-34-53.png](attachments/image-2026-3-15_17-34-53.png)

Key points explanation:

1. Inbound flow 1~4, the connectivity with current flow will note change, the change is to add new solace topic & queue between Ratan GDC as a producer and Ratan ID as a consumer. 1. Flow-1: Murex → IBMMQ → Ratan GDC(New topic) → FM Solace → Ratan ID(New queue) 2. Flow-2: TDS3 → FM Solace → Ratan GDC(New topic) → FM Solace → Ratan ID(New queue) 3. Flow-3: SSI+ → FM Solace → Ratan GDC(New topic) → FM Solace → Ratan ID(New queue)
2. Inbound flow-4 1. Create new enterprise solace queue to consume RDM real time data by Ratan ID 2. RDM file could reuse this new queue, Ratan GDC and Ratan ID would receive the notification and process RDM file at same time, need double confirm whether has potential issue.
3. Outbound flow-5 the status write back will publish to the solace topic as well, not required new integration.

</details>

#### Solution B

<details>
<summary>展开详情</summary>

![image-2026-3-15_14-17-19.png](attachments/image-2026-3-15_14-17-19.png)

Key points explanation:

1. Add new IBMMQ CF.MXG.RATAN.RQSTIN.ID to subscribe CF.MXG.RATAN.RQST, RATAN GDC will filter out ID cashflows, and RATAN ID will implement the oppoiste logic.
2. Ratan ID need new solace queue q-51358-ratanone-confirmation-id, filter ID trades for settlement processing.
3. SSI Refresh flow, no need to filter, only need a new solace queue q-51358-ratanone-ssiplus-id for ID processing independently.
4. For RDM flow, Ratan ID does not integrate with RDM separately, Data will persist in RATAN GDC and provide query for RATAN ID instance

</details>

### UI Interaction

#### UI Blotters and Data Category

**Data Category**

| Category | Restricted | Data Source | Target Location | integration across region |
| --- | --- | --- | --- | --- |
| Restricted business data | Yes | Upstream | ID local | No |
| General configurable data(see below diagram) | TBC | Delta script, UI | TBC | Yes |
| Common Static data | No | Delta script | ID local | No |
| Frequently refreshed static data(RDM, Legal Entity) | No | Upstream | GDC | Yes |

**UI Blotter and Data source**

![image-2026-3-15_17-53-24.png](attachments/image-2026-3-15_17-53-24.png)

Key points explanation:

1. There is no doubt that restricted data should be persisted and query from ID local database.
2. General configurable data can be defined as not restricted data, can be persisted to either GDC or ID local database.
3. General configurable data characteristics: 1. Initialized by Ratan initialization DB script 2. updated by DB script as well according to user ad hoc requests 3. User manual configure from UI themselves. 4. There is no integration with up streams.

#### UI Interaction solution A

<details>
<summary>展开详情</summary>

Maintain two GUIs with different domain URL

![image-2026-3-15_18-7-49.png](attachments/image-2026-3-15_18-7-49.png)

Key points explanation:

1. All data persist ID locally no matter it's restricted or general configurable data.
2. as general configurable data maintained two location, if any update or creation, need user to consider whether need to update twice manually.
3. If a user doesn't have ID profile he is not able to see any blotters after login, GDC bypass this logic validation.
4. Ratan ID need to deploy entire cluster and apply new domain name.

</details>

#### UI interaction Solution B

<details>
<summary>展开详情</summary>

![image-2026-3-15_18-40-1.png](attachments/image-2026-3-15_18-40-1.png)

Key points explanation:

1. Only 1 entrance to RATAN multi-region UI(Domain URL is a little bit confused)
2. If user has multi region profile, force user to select 1 region before explore data.
3. If user switch the region, force refresh the blotter, and recreate the WS channel .
4. There is no additional blotter, always use the same blotter to query the data from selected region.
5. If any general configurable data could be shared across the region, user need to update twice under different region.

</details>

#### UI interaction Solution C

<details>
<summary>展开详情</summary>

According to the UI Blotters and Data Category diagram, we can get some information and make some assumptions.

If general configurable data could be always shared and could be persisted in GDC, then region switch on these blotter is not required.

Solution is to add 3 new blotters for ID specifically.

![image-2026-3-15_18-55-34.png](attachments/image-2026-3-15_18-55-34.png)

With this choice, the challenge would be:

1. Creation, modification, delete - Cashflow behavior change driven by data modification - Nostro refresh, rule refresh(Not available, but need to consider)
2. Query - General configurable data is in GDC, but it requires by ID instances.

</details>

| | | |
| --- | --- | --- |
| | | |
| | | |
| | | |
| | | |

### Data Isolation and Synchronization

**What kind of data need to be isolated?**

Cashflow related data, trade related data, rules and static data

<details>
<summary>展开详情</summary>

**[Discard]**

**What kind of data can be synchronized?**

1. General configurable data
2. Common Static data
3. Frequently refreshed static data

Considered 2 is managed by Ratan backed itself, so the easy way is to duplicate it to ID local instance. Any changes to this kind of data are accompanied by go-live and restart, we can control the data consistency.

Considered 3 there is no event refresh use case, only need to query across region.

Considered 1 there are both event refresh and query across region.

#### Solution A - GDC Single DB persistence

![image-2026-3-15_20-17-5.png](attachments/image-2026-3-15_20-17-5.png)

#### Solution B - Local DB persistence

![image-2026-3-15_21-22-10.png](attachments/image-2026-3-15_21-22-10.png)

| | Solution | GDC servers | ID servers | | | |
| --- | --- | --- | --- | --- | --- | --- |
| A | Deploy individually, isolation start from UI. No integration between GDC and ID except message bridge | all applications | all applications | 1. No cross region integration 2. UI force refresh after switch region 3. Easy to implement, all services, middleware, databases are independent 4. User has to maintain general configurable data separately | | |
| B | Isolation on restricted data only(cashflow, trade). Integration required between GDC and ID | all applications | share static/rule | 1. Cross region integration 2. UI to create new blotter for onshore entity 3. There is latency to sync up general configurable data and take effective. 4. There is no chance for user to maintain different general configurable data | | |
| C | Isolation start from API gateway, transparent to user, very complex. | | | 1. Transparent to user. 2. Hard to implement, GDC gateway logic would be complex. 3. Cross region integration is required for any data without a region flag. | | |

</details>

### Key Considerations

| | Description | Comment |
| --- | --- | --- |
| 1 | Network connectivity between regions. | Only need to consider network connectivity between 1. ID and GDC 2. ID and enterprise solace. |
| 2 | Data security between regions | 1. Security control between selected region and entitlement 2. Downstream query cashflow should meet regulatory compliance 3. Data offloading should be 100% accurate a. data persistence - Message Bridge b. data query - Nginx + API Gateway |
| 3 | Cost management (cross-region traffic can be expensive). | User's geographic location request may cause high latency by request GDC nginx and infra service. |
| 4 | Monitoring and alerting across regions. | Central monitoring can be reused with new indexing/dashboard 1. ELK 2. Prometheus + Grafana 3. ITRS |
| 5 | Cashflow notification | Nginx should also add routing logic for WebSocket endpoint in different region according to the region header |
| 6 | Shared repo | Any change on ado repository should consider compatibility on both internal region and across region e.g. Biz domain service → infra service, should be gateway-to-gateway, but if call in same region, call internal API directly is more better |

### Impacted Scope Detail

| | Ratan Component | Change description | Effort |
| --- | --- | --- | --- |
| 1 | GUI | 1. Check User entitlement, ask user to select if user has multi region entitlement 2. Add selected region to request header | Small |
| 2 | Nginx | 1. Determine API gateway endpoint according to the region header 2. Determine notification subscription endpoint according to the selected region header | Small |
| 3 | API Gateway | Validate user requested region and entitlement match or not, if not match reject directly | Small |
| 4 | Message bridge routing config. | enterprise solace connectivity with RATAN GDC and down streams | Small |
| 5 | Microservice which has infra service integration | All business domain service to infra service call change to gateway-to-gateway model | Middle |
| 6 | Infra service | Scale up to fulfill the traffic from two regions | Small |

<details>
<summary>展开详情</summary>

New Entity Onboarding Check

[New Entity onboarding checking list - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/New+Entity+onboarding+checking+list)

| 1 | Description | Details | Type | Status |
| --- | --- | --- | --- | --- |
| 1 | LMS Feed | Blacklist includes ID - 8 ID will not generate LMS feeding | Config | |
| 2 | Swift | ID will flow to strategic flow orchestration + accounting use this property to determine the business flow | Config | |
| 3 | SWIFT Generation Changes - Booking Entity FMID(mandatory for each entity) - Booking Entity SWIFT BIC (Sender BIC in SWIFT) (mandatory for each entity) - Field 53 SWIFT BIC (for LCY & Over Account) (mandatory for each entity) - Field 58 SWIFT BIC (for Flip MT202) (mandatory for each entity) - Receiver BIC (MT604/605) - Branch code mapping (mandatory for each entity) - Any other branch specific requirement on SWIFT | Need to be added for new entity | Config | |
| 4 | Currency Release Time (mandatory for each entity) | Need to be added for new entity | Config | |
| 5 | NDS Auto Netting | Blacklist: TBD | Config | |
| 6 | Pending Fixing STP/NSTP Control( in case new product have fixing events) | Blacklist: TBD | Config | |
| 7 | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | Whitelist: CN/MY/IN/SG/LOANID old logic Rest: new logic | Config | |
| 8 | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | | Config | |
| 9 | Settlement Accounting - Bridge Account # (mandatory for each entity) - EBBS Branch code & EBBS Transaction type (mandatory for each entity) - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | Need to be added for new entity | Config | |
| 10 | Include new branch in GUI Drop down - Cashflow Blotter (mandatory for each entity) - Dashboard (mandatory for each entity) | Need to be added for new entity | Config | |
| 11 | Vostro SI Input Screen - Include New Settlement Means | | Config | |
| 12 | Rounding - applicable for special currency/requirement only | | Config | |
| 13 | Nostro Static Setup (mandatory for each entity) | | Static | |
| 14 | Vostro Static Setup (Vostro to drive Nostro assignment) - Over-Account Clients to be created as Branch specific SSI | | Static | |
| 15 | Business Rules Setup - Cashflow Suppression - White List for in scope entities - Swift Suppression - Auto Debit by Agent - Nostros shared with other entity (example: China) - NSTP - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity - Netting Static - BIC Netting Static | | Static | |

Proposal A  Logical Diagram

Diagram

Proposal B Logical Diagram

</details>

Appendix

Diagram Draft Version: