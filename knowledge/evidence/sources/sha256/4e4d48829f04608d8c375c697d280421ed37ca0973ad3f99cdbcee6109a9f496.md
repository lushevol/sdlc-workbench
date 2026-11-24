****

# **The purpose**

AS STP system, when the RatanOne system handle the cashflow , the system needs some static data to support the STP process.

This document will define the strategy how to store theses static data and how to update.

There are two kind of static data, one is the refence data which in the surrounding system like Vostro and Counterparty data. RatanOne would like to store this part of data to make system more stable and reduce access pressure to these systems.

Two is RatanOne Own data which maintained by RatanOne-self，like Nostor data. RatanOne needs to store this part of data to keep STP system run as well.

# **Strategy for ****static data**

## **Strategy ****of query and sync refence data**

1 Init data with DB dump which provide by golden source system.

2 Receive the update notification from the golden source though EDMI (FM-EDMI or Enterprise-EDMI) which with data payload and then refresh the data in RatanOne system.

3 The Golden Source system need to provide the daily changes of data as file.  RatanOne will sync this file from FileIT (Or other data channel if better then FileIT) .

4 Need to recon the data flies from RatanOne and Golden Source system, if not same then parse the file from Golden Source system and refresh the data by the end of date.

## **Strategy ****of RatanOne Own static data**

## **Cache (In-memory) vs Database **

### **principle for static data**

If application can meet business NFRs with database then should not use cache middleware (In-menory) to store data.

### **rule for static data (refence data) **

**  Store DB firstly and keep to update **

| DATA Type | ** Store strategy for RatanOne** | Business NFRs match | **Data volume** | **Use frequency** | Change frequency | Note |
| --- | --- | --- | --- | --- | --- | --- |
| Refence data | cache in memory （all data in DB） | not match | small | common case need （often） | more than one hour | |
| Refence data | cache in memory （all data in DB） | not match | small | common case need （often） | Less than one hour | |
| Refence data | DB | not match | small | special case need （not often） | more than one hour | |
| Refence data | Query Golden Source | not match | small | special case need （not often） | Less than one hour | |
| Refence data | parts of data cache in memory and all data in DB | not match | big | common case need （often） | more than one hour | |
| Refence data | parts of data cache in memory and all data in DB | not match | big | common case need （often） | Less than one hour | |
| Refence data | DB | not match | big | special case need （not often） | more than one hour | |
| Refence data | Query Golden Source | not match | big | special case need （not often） | Less than one hour | |
| Ratan data | cache in memory （all data in DB） | not match | small | common case need （often） | more than one hour | |
| Ratan data | cache in memory （all data in DB） | not match | small | common case need （often） | Less than one hour | |
| Ratan data | DB | not match | small | special case need （not often） | more than one hour | |
| Ratan data | DB | not match | small | special case need （not often） | Less than one hour | |
| Ratan data | parts of data cache in memory and all data in DB | not match | big | common case need （often） | more than one hour | |
| Ratan data | parts of data cache in memory and all data in DB | not match | big | common case need （often） | Less than one hour | |
| Ratan data | DB | not match | big | special case need （not often） | more than one hour | |
| Ratan data | DB | not match | big | special case need （not often） | Less than one hour | |
| | | | | | | |

# **RatanOne ****Static Data Service Design**

## **High level design**

## **CN Cashflow Data Volume**

| Year | Daily volume | 8 hours to handle | each instance handle (based on six instances) | Daily Max records | Daily Max 8 hours to handle | each instance handle (based on six instances) |
| --- | --- | --- | --- | --- | --- | --- |
| 2023 | 400 records | 0.83 records/min | 0.14 records/min | 900 | 1.875 records/min | 0.3 records/min |
| 2024 | 18000 records | 37.5 records/min | 6.25 records/min | 40500 | 84.3 records/min | 14 records/min |

| Year | Daily volume | 24 hours to handle | each instance handle (based on six instances) | Daily Max records | Daily Max 24 hours to handle | each instance handle (based on six instances) |
| --- | --- | --- | --- | --- | --- | --- |
| 2023 | 400 records | 0.28 records/min | 0.05 records/min | 900 | 0.625 records/min | 0.1 records/min |
| 2024 | 18000 records | 12.5 records/min | 2.1 records/min | 40500 | 28.1 records/min | 4.6 records/min |

# **Use cases**

## **Vostro Data for SSI Stamping**

| Time | number of records | data volume | note |
| --- | --- | --- | --- |
| 2022 | about one million | | |

### How to initialization

Initialize data with DB dump which provide by SSI+

### How to cache

| Key | Data |
| --- | --- |
| SSI-ID | { "Entity": { "Counterparty_City": "KC", "Counterparty_Long_Name": "TECHCOMP LIMITED ", "Counterparty_Legal_Name": "TECHCOMP LIMITED", "Counterparty_Street_Address": "RM 6 BLK 1 26 F EVER GAIN PLZ", "Counterparty_Has_NDAgreement": "False", "Counterparty_Incorporated_Country_ISO_Code": "HK" }, "Maker_Checker_Items": {}, "Settlement_Instruction": { "SSI_Id": "46756400", "Account": { "Beneficiary_City": "KC", "Cash_Custodian_City": null, "Beneficiary_BIC_code": null, "Cash_Local_Agent_City": null, "Counterparty_BIC_Code": null, "Cash_Custodian_BIC_code": "SCBLHKHHXXX", "Has_Beneficiary_Account": "true", "SCB_Nostro_Account_Type": "NOS", "Beneficiary_Account_Name": "TECHCOMP LIMITED", "Beneficiary_Country_Name": "Hong Kong", "Cash_Local_Agent_BIC_code": "SCBLUS33XXX", "SCB_Nostro_Account_Number": "USD MAIN", "Beneficiary_Account_Name_2": null, "Beneficiary_Street_Address": "RM 6 BLK 1 26 F EVER GAIN PLZ", "Has_Cash_Custodian_Account": "true", "Cash_Correspondent_BIC_code": null, "Cash_Custodian_Account_Name": null, "Counterparty_Has_CMS_Account": "false", "Has_Cash_Local_Agent_Account": "true", "Cash_Custodian_Account_Number": "40710874782", "Cash_Custodian_Street_Address": null, "Cash_Local_Agent_Account_Name": null, "Has_Cash_Correspondent_Account": "false", "Cash_Local_Agent_Account_Number": null, "Cash_Local_Agent_Street_Address": null, "Counterparty_CMS_Account_Number": null, "Cash_Correspondent_Account_Number": null, "Cash_Local_Agent_Sub_Account_Number": null, "Cash_Correspondent_Sub_Account_Number": null }, "CFI_Code": "SR****", "Comments": null, "Usual_Id": null, "Event_Type": "Insert", "SSI_Source": "Import", "SSI_Status": "New", "Debit_Credit": "Both", "Charge_Bearer": "OUR", "ISDA_Taxonomy": null, "SSI_Unique_Id": "46756400", "Effective_Date": null, "Is_Default_SSI": "true", "Settlement_Code": null, "Settlement_Type": "CASH", "Payment_Currency": "USD", "BranchId_Murex3Id": "Global", "Settlement_Method": "CASH", "Swift_Message_Type": "MT103", "Primary_Asset_Class": null, "Counterparty_SCI_FMID": "400035604", "Is_Third_Party_Payment": "false", "Remittance_Information_1": null, "Remittance_Information_2": null, "Remittance_Information_3": null, "Remittance_Information_4": null, "Source_System_Instrument_Id": "SCBIRDIRS", "Sender_To_Receiver_Information_1": null, "Sender_To_Receiver_Information_2": null, "Sender_To_Receiver_Information_3": null, "Sender_To_Receiver_Information_4": null, "Sender_To_Receiver_Information_5": null, "Sender_To_Receiver_Information_6": null, "Settlement_Location_Country_ISO_Code": "US" } } |

### How to sync

Receive the notification from SSI+ system and then update cache data in RatanOne.

Recon and refresh the data by EOD

## **Nostro Data for SSI Stamping**

| Time | number of records | data volume | note |
| --- | --- | --- | --- |
| 2022 | one hundred thousand | | |

### How to initialization

Initialize data with manual

### How to cache

| Key | Data |
| --- | --- |
| legalEntityFmId+Currency+settlementMeans+settlementAccount | { "legalEntity": "SCB SHANGH*SHA", "primaryFlag": "true", "legalEntityFmid": "10036642", "noticeToReceive": "Y", "settlementMeans": "NOS", "ebbsBridgeAccount": null, "ebbsNostroAccount": "44444444444", "settlementAccount": "EUR MAIN", "settlementCurrency": "EUR", "sendersCorrespondent53City": "GERMANY", "nostroSettlementMessageType": "MT210", "sendersCorrespondent53Swift": "SCBLDEFXXXX", "sendersCorrespondent53Account": "2343875345", "sendersCorrespondent53Address": "STANDARD CHARTERED BANK AG FRA", "sendersCorrespondent53Fullname": "SCB FRANKFURT - EUR Nostro account", "sendersCorrespondent53PostCode": null } |

### How to update

Update data with data dump when have new data

## **Counterparty information Data for SSI Stamping**

| Time | number of records | volume | note |
| --- | --- | --- | --- |
| 2022 | four hundred | | |

### How to initialization

Initialize data with API Query which provide by SCI

### How to cache

| Key | Data |
| --- | --- |
| FMID | { "fm_profile_sys_gen_id": "10075222", "fpi_fm_code": "SCB LONDON*LDN" } |

### How to sync

①Receive the notification from SCI system and then update cache data in RatanOne.

②Use schedule job to sync data from SCI every data. (Consider using third-party tools to run schedule job in case the SCI or Ratan service for crash case)

# **Cache middleware use cases in RatanOne**

| **Use cases** | **Middleware ** | Note |
| --- | --- | --- |
| Distributed locks | Redis | |
| Duplicate check | Redis | |
| User Session （X-Token） | Redis | |
| URL whitelist in API Gateway | Redis | |
| cache data | Redis | |

For user query case (from UI), service can cache data in the local or in Redis （follow the **2.3.2** **cache rule for static data** ）

# ** Hazelcast IMDG **

## **What is Hazelcast IMDG **

Hazelcast IMDG is an open-source distributed in-memory object store supporting a wide variety of data structures.

Hazelcast IMDG is highly scalable and available. Distributed applications can use it for distributed caching.

Hazelcast IMDG is designed to be lightweight and easy to use.

Since it is delivered as a compact library (JAR) and has no external dependencies other than Java, it easily plugs into your software solution and provides distributed data structures and computing utilities.

## ** Distributed Data Structures of Hazelcast**

| **Data structure** | **Description** |
| --- | --- |
| [Map](https://docs.hazelcast.com/hazelcast/latest/data-structures/map) | Key-value pairs that are partitioned across a cluster. Maps offer a wide range of features such as SQL queries, WAN replication |
| [Multimap](https://docs.hazelcast.com/hazelcast/latest/data-structures/multimap) | A specialized Hazelcast map. It is a distributed data structure where you can store multiple values for a single key. |
| [Atomic Long](https://docs.hazelcast.com/hazelcast/latest/data-structures/iatomiclong) | A data structure for dealing with long values that can be updated atomically in a distributed environment. |
| [Queue](https://docs.hazelcast.com/hazelcast/latest/data-structures/queue) | A data structure for adding an item in one member/client and removing it from another one. |
| [List](https://docs.hazelcast.com/hazelcast/latest/data-structures/list) | Similar to Hazelcast set, except a list allows duplicate elements and preserves their order. |
| [Set](https://docs.hazelcast.com/hazelcast/latest/data-structures/set) | A distributed and concurrent collection that contains no duplicate elements and does not preserve their order. |

## **Deployment strategy **

Deploy the Hazelcast as cluster model.

## **Monitor**

Management Center is a tool for managing and monitoring Hazelcast Platform clusters.

- Monitor the performance of your clusters from the UI
- See statistical information about your members, clients, and data structures.
- Execute SQL queries on your clusters.
- Use REST API endpoints to return the information presented in Management Center.

![Picture2.png](attachments/Picture2.png)

## **HA**

RATAN system will deploy Hazel cast instance on each of the 6 production nodes on both ARK and Watford.

The ARK and Watford VM servers with active-active mode, which provide both High reliability and availability.

The traffic from Ratan service route the live service node.

## **DR strategy**

Same with HA strategy

# **Hazelcast VS Redis**

** Refer:  [Redis vs MemcacheD vs Hazelcast ](https://confluence.global.standardchartered.com/display/DBENG/Redis+vs+MemcacheD+vs+Hazelcast)**

# **Cache Middleware upgrade ****strategy**

Since RatanOne already use Redis in the system, considering the cost and risk, Redis will be upgraded to v6+ for Day1 release.

About the HazelCast will as an improvement point for NFR of the system after Day1.

# **Cache (Redis) vs Database performance comparison（unofficial）**

**Test case ：Q****uery nostros**

**Test API：   [http://domain/v1/static/nostros/fuzzy?legalEntityFmid=401021850&currency=EUR](http://localhost:8989/v1/static/nostros/fuzzy?legalEntityFmid=401021850&currency=EUR)**

**Test Env： Server - Dev Env**

**                   Client - CPU: i5  /Memnoy 8G / Storage: 500G  **

**Save Time: for this case Redis will save time about 65% comparison with DB**

| storage | average | | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cache ( Redis 5) | 285.7ms | 265ms | 280ms | 269ms | 290ms | 282ms | 324ms | 292ms | 326ms | 251ms | 278ms |
| DB (PostgreSQL 12） | 814 ms | 730ms | 736ms | 846ms | 867ms | 759ms | 784ms | 855ms | 868ms | 888ms | 807ms |