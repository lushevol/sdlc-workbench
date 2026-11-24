# Background

**OJK** (Indonesian regulator) requires SCB to establish on-shore back-office capabilities to serve as last-mile processing system for relevant products. The onshoring of derivatives payment processing through RATAN Indonesia is planned for delivery by 2026.

The Proposal is to implement a local instance of **RATAN** which is the strategic settlement system within the Strategic FM re-platforming technology stack. **RATAN Indonesia **will be established as a new application asset hosted on the Indonesia infrastructure.

## **Detail Requirements**

1. Data storage to be onshore. Processing will remain unchanged and will continue to be performed by GBS KL users.
2. Indonesia cashflows must be displayed in the same Post Trade Portal together with other countries. (Indonesia data will be stored onshore, while other entity data remains stored in GDC.)
3. Data entitlement rules enforced through CES must be strictly applied. (i.e., ID onshore users get only ID data access. Other country onshore users do not get ID data access unless specifically approved. Group users like GBS Settlements, MO, PSS, Dev, PO get ID data access)
4. Data processing must not be delayed and should meet the same performance benchmark as GDC.
5. Regulatory reporting must not be impacted.
6. Data Ops users require a new static data replication process to reduce manual error risk and improve operational efficiency.

# UAT Status

| UAT Scope | Total Case Count | Completed | Ref. |
| --- | --- | --- | --- |
| **MX211** | 3 | | |
| **RATAN** | 22 | | 9 remaining include 7 - global rule sync, 2 - access control |
| **[FMSGW](https://confluence.global.standardchartered.com/display/DSP/RATAN+ID+Cash+Settlements+Migration+-+UAT+Scope#RATANIDCashSettlementsMigrationUATScope-FMSGW:)** | 6 | | 3 remaining |
| **LMS** | 1 | | |
| **EBBS & TLM (Accounting)** | 1 | | |
| **SSDR (via DQSL) & FMMIS** | 5 | | |
| **Market UDP ** | 7 | | |

# Project Delivery Plan

![image-2026-9-4_11-8-53.png](attachments/image-2026-9-4_11-8-53.png)

# Surrounding System Integration

| System name | Business purpose/Benefit |
| --- | --- |
| Murex2.11 | Legacy cashflow source |
| Trade Lake/Stella | Strategic cashflow source of FMRP Migration |
| CES | Data entitlement and access control on Need To Know Basis. |
| SSI+ | Standing Settlement Instruction (Vostro) source for payment generation, including SSI updates |
| SCI | Legal entity data for cashflow processing |
| MDS | FX rate data for high value payment calculation & control |
| RDM | Currency holiday to calculate accurate cutoffs and control of bad business day. |
| FMSGW&AMH | Swift process |
| EBBS ID | Accounting process |
| DQSL&TLM | Reconciliation |
| FMMIS | MI dashboard |
| UDP | Reporting |
| FM Solace | Messaging between FM applications |
| Central Solace | Messaging at enterprise level. |
| LMS | Liquidity management |

# Demo Environment

[Markets Operations One](https://fmo-mfe-fmrp2.pi.dev.net:8453/)

# Demo Details

## Access control

### Global Users can view both GDC and ID blotters

**User Id:** 1129381- K Thirunavukarasu, Cordelia Sumita

![image-2026-8-27_14-20-1.png](attachments/image-2026-8-27_14-20-1.png)

### ID Onshore users can only view ID blotters

**User Id:** 1140336 - Eliana, Eliana

![image-2026-8-27_14-22-49.png](attachments/image-2026-8-27_14-22-49.png)

### Global Users without ID access can see only GDC blotters

**User Id: **1462616 -Ali, Shaukat

![image-2026-8-27_14-27-34.png](attachments/image-2026-8-27_14-27-34.png)

### Data ops user can access both GDC and ID static & rule blotters

**User Id: **1434424 - Shankar M, Shiva

![image-2026-8-27_14-57-56.png](attachments/image-2026-8-27_14-57-56.png)

![image-2026-8-27_14-59-7.png](attachments/image-2026-8-27_14-59-7.png)

## Global rule sync

### NSTP - Global Rule could be sync to ID instance

Case Description - NSTP rule creation, then approve, rule will be sync up to ID

Step-1 Rule creation

![image-2026-8-27_15-35-14.png](attachments/image-2026-8-27_15-35-14.png)

Step - 2 "Add Pending" status will not synchronize, Sync Status is N/A

![image-2026-8-27_15-36-33.png](attachments/image-2026-8-27_15-36-33.png)

Step - 3 Approve creation

![image-2026-8-27_15-40-8.png](attachments/image-2026-8-27_15-40-8.png)

Step - 4 Rule status change to "LIVE" after approve, sync status change to "SYNC"

![image-2026-8-27_15-42-45.png](attachments/image-2026-8-27_15-42-45.png)

Step - 5 Go to ID NSTP rule tile, can see rule has been synced up with "LIVE" status and Is Sync Rule is "Yes"

![image-2026-8-27_15-46-42.png](attachments/image-2026-8-27_15-46-42.png)

### Netting - Global Rule could be sync to ID instance

Case Description - Netting rule update, then approve, rule will be sync up to ID

Step - 1 Create new Netting rule and approve, rule id is 7498654800279109632, synced up to ID

Step - 2 Update Rule, Status to UPDATE_PENDING, Sync Status is N/A， rule id is 7498655977784012800

![image-2026-8-27_16-21-29.png](attachments/image-2026-8-27_16-21-29.png)

![image-2026-8-27_16-23-54.png](attachments/image-2026-8-27_16-23-54.png)

Step - 3 Approve Rule update, Status to LIVE, Sync Status is ACK

![image-2026-8-27_16-24-42.png](attachments/image-2026-8-27_16-24-42.png)

Step - 4  Go to ID Netting Static tile, can see rule has been synced up with "LIVE" status and Is Sync Rule is "Yes"

![image-2026-8-27_16-26-13.png](attachments/image-2026-8-27_16-26-13.png)

### Swift Suppression - Global Rule could be sync to ID instance

Case Description - Global Swift Suppression rule disable/enable, rule will be synced up to ID

Step - 1 Create new Swift Suppression rule and approve, rule id is 7498664825846489088, synced up to ID

Step - 2 Disable the rule. rule will be synced up to ID

![image-2026-8-27_16-59-45.png](attachments/image-2026-8-27_16-59-45.png)

![image-2026-8-27_17-0-14.png](attachments/image-2026-8-27_17-0-14.png)

Step - 3 Enable the rule, rule will be synced up to ID

![image-2026-8-27_17-1-13.png](attachments/image-2026-8-27_17-1-13.png)

![image-2026-8-27_17-1-38.png](attachments/image-2026-8-27_17-1-38.png)

### Cashflow Suppression - Global Rule could be sync to ID instance

Case Description - Global Suppression rule create/update, then reject, rule will not be synced up to ID

Step - 1 Create new Swift Suppression rule, rule id is 7498666468392435712, Status is ADD_PENDING, Sync Status is N/A, not synced up to ID

Step - 2 Reject rule, rule will disappear, not synced up to ID

![image-2026-8-27_17-5-46.png](attachments/image-2026-8-27_17-5-46.png)

### ![image-2026-8-27_17-7-17.png](attachments/image-2026-8-27_17-7-17.png)

Step - 3 Find another active rule, update, status is UPDATE_PENDING, rule id is 7498667884821671936, not synced up to ID

Step - 4 Reject the rule, rule will disappear and can't find in ID rule blotter

![image-2026-8-27_17-10-43.png](attachments/image-2026-8-27_17-10-43.png)

![image-2026-8-27_17-12-15.png](attachments/image-2026-8-27_17-12-15.png)

### ID rule tiles cannot update global rules

Case-1 User can't update and disable rule as long as Is Sync Rule = Yes

![image-2026-8-27_17-13-53.png](attachments/image-2026-8-27_17-13-53.png)

![image-2026-8-27_17-16-25.png](attachments/image-2026-8-27_17-16-25.png)

Case-2  User can manage local rule only

![image-2026-8-27_17-18-36.png](attachments/image-2026-8-27_17-18-36.png)

![image-2026-8-27_17-18-13.png](attachments/image-2026-8-27_17-18-13.png)

### Indonesia rules not reflect in all Global Blotter

Case description: create new Rule via ID NSTP rule blotter, and approve the rule creation, the rule should not be found in global NSTP rule blotter

Step-1: create new NSTP rule with ex code "ID rule for demo", and approve, rule id is 7498671479971844096

![image-2026-8-27_17-21-20.png](attachments/image-2026-8-27_17-21-20.png)

![image-2026-8-27_17-24-38.png](attachments/image-2026-8-27_17-24-38.png)

Step-2: Go to global NSTP rule blotter, search by rule id, ID rule 7498671479971844096 should not be found

![image-2026-8-27_17-26-30.png](attachments/image-2026-8-27_17-26-30.png)

### Exception handling

![image-2026-8-27_17-38-22.png](attachments/image-2026-8-27_17-38-22.png)

| Sync Status with Exception | Explanation | Action |
| --- | --- | --- |
| NACK | ID sync status failure and feedback to GDC | 1. User manual resync via GDC rule blotter. 2. User manual create/update rule via ID rule blotter |
| FAILED | GDC publish sync event failure, ID doesn't receive the notification | 1. User manual resync via GDC rule blotter. 2. System will retry automatically every 5 min 3. User manual create/update rule via ID rule blotter |
| TIMEOUT | GDC publish sync event success, but no response for long time (5~10 min) |

Manual resync via GUI

![image-2026-8-27_17-46-30.png](attachments/image-2026-8-27_17-46-30.png)

## Cashflow inbound and STP process

Case description: Cashflow inbound and able to hit rule sync from GDC.

Sample cashflow id: **M03337013112**

![image-2026-8-27_18-13-52.png](attachments/image-2026-8-27_18-13-52.png)

### ![image-2026-8-27_18-17-31.png](attachments/image-2026-8-27_18-17-31.png)

Swift

![image-2026-8-27_18-18-3.png](attachments/image-2026-8-27_18-18-3.png)

Accounting

![image-2026-8-27_18-18-43.png](attachments/image-2026-8-27_18-18-43.png)

# Appendix

## UAT Test Scope

[RATAN ID Cash Settlements Migration - UAT Scope - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+ID+Cash+Settlements+Migration+-+UAT+Scope)