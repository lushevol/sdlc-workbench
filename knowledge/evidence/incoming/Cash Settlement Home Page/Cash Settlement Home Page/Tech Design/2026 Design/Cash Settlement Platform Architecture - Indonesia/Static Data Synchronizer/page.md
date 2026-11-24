# ****

# **Background**

When Ratan builds sub-instances for different entities, users require that incremental static data and rules should be synchronized to the sub-instances automatically when they maintain these data in Ratan GDC, rather than to maintain them in multiple places.

To reduce the duplicate efforts in synchronizing data for each instance, we decided to build the Static Data Synchronizer to support this requirement in a consistent way.

# **Key Points**

Here are some key points we need to consider:

- **Async**

The synchronization should not impact the main flow in GDC, means we need to build it in an individual service and also handle it in** async way**.

- Failed Retry

We need to build failed retry for **exception handling** to make synchronization stable.

- **Observation**

The synchronization status should be observable, means we need to build it in **request/response mode** and also enabled for user to do resync manually on GUI.

- **Idempotent **

The synchronization should be **idempotent **and all sub instances with **no duplicate and no loss.**

- **Multi Consumers**

One synchronized data can be consumed  by multi sub instances  at the same time in the **one request-multi response mode**, and the data synchronizer maintain the sync status of all sub instance.

# **Overall Design**

## **System Definition**

The Static Data Synchronizer is a data transfer service that transmits data from one place to others. What it care about is where the data comes from and where it goes, and it makes sure the data is fully delivered as expected.

The main functions includes:

1. Data Inbound Adapter
2. Sync Message Management
3. Exception Handling
4. Sync Data Observation
5. SyncProduceSDK/SyncConsumeSDK

## **High Level Diagram**

## **Overall Framework**

- Each data has **only one** sync record to record the **newest **sync event in Producer side.
- Each sync event brings a unique request_id and a data version.
- Retry sync event will **reuse **the **request_id **and **data_version **and override the previous sync record.
- Sync status are SENT, ACK, NACK, FAILED, TIMEOUT, IGNORE for each sub-instance.

SENT: Data produced successfully by Producer.

FAILED:  Data produced failed on Producer side.

ACK:  Data consumed successfully by Consumer.

NACK: Data consumed failed by Consumer.

TIMEOUT: No sync response received in 5~10 minutes.

IGNORE:  When there is a SyncIgnoreConstraint exists in protocol, the SyncFailedRetryer will ignore the retry for special ids in the protocol.

# **Data Producer**

Data Producer is a component that receive data from outside and wrap it to a sync event and then send the event out to Consumer side, meanwhile,  It also manage the sync status lifecycle to ensure the sync is done as expected.

## **Inbound Adapter**

This is a high level interface that define a various of methods to handle the heterogeneous data access and build-in some default implementation.

## **Data Sync Checker**

This component is a validator/checker/filter collection that support previous validation on input data.

DataSyncConfigChecker

## **Data Sync Produce Processor**

DataVersionGenerator

RequestIdGenerator

SyncEventPublisher

## **Data Constraint**

SyncIgnoreConstraint

## **Data Sync Produce Manager**

This component is designed to manage status lifecycle inludes:

1. Syn response handler
2. Sync Controller
3. Sync Timeout Monitor
4. Sync Failed Retryer

### Sync Response Handler

- Sync Response drop

### Sync Controller

- Sync Status Query

- Manually Resync

### Sync Timeout Monitor

### Sync Failed Retryer

SyncFailedRetryer in data producer to resync the records with  FAILED and TIMEOUT status and set status to SENT.

# **Data Consumer**

## **Sync message duplicate and disorder handle**

Use request_id and data_version to handle message duplicate and disorder in consumer.

## **Outbound Adapter**

### DataTypeCustomization

Be able to customize for endpoint protocol of each data type.

# **Protocols**

## **Data Access Protocol**

```
REQ:   
{
        "data_unique_id": "7469639288002646016",
        "data_version": 1,
		"data_type": "RuleEngine",
		"operation_type": "CREATE", // CREATE|UPDATE|DELETE
        "pre_processors":[
            {
              "name": "A",
              "parameters": {
                  "a": "1",
                  "b": "2"
               }
            },
             {
              "name": "B",
              "parameters": {
                  "a": ["xxx","xxx","xxx"],
                  "b": ""
               }
            } 
         ],
		"payload": {
          "id" : "7469639288002646016",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"4\"",
          "runningRule" : "xxx",
          "status" : "LIVE",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : null,
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-21T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 1,
          "metaData" : "xxx"
         },
         "post_processors": [
            {
              "name": "RetryIngore",
              "parameters": {
                  "ignore_unique_ids": ["1","2","3"]
               }
            }
         ]
    }

RESP:
{
	"code": 0,
    "data_unique_id": "7469639288002646016",
    "message": "received"
}
```

## **Data Sync Protocols**

### **Multiple Consumers Support**

Sync Status Definition:

```
[
    {
        "dc": "ID", 
        "requestId": "252980c4-8bb4-4530-98bd-39a4f1346551", 
        "status": "ACK", 
        "message": ""
    }, 
    {
        "dc": "NP", 
        "requestId": "252980c4-8bb4-4530-98bd-39a4f1346551", 
        "status": "NACK", 
        "message": ""
    }, 
    {
        "dc": "MY", 
        "requestId": "252980c4-8bb4-4530-98bd-39a4f1346551", 
        "status": "FAILED", 
        "message": ""
    }, 
    {
        "dc": "EG", 
        "requestId": "252980c4-8bb4-4530-98bd-39a4f1346551", 
        "status": "TIMEOUT", 
        "message": ""
    }
]
```

### **Producer & Consumer Inner Sync Protocol**

Sync Data definition:

```
REQ:
    {
        "id": 1,
        "data_unique_id": "7469639288002646016",
		"data_version": 1,
		"data_type": "RuleEngine",
        "request_id": "5b02926e-e83c-4936-b7a8-28c2f17231f9",
        "dc": "GLOBAL",
		"operation_type": "CREATE", // CREATE|UPDATE|DELETE
         "pre_processors":[
            {
              "name": "A",
              "parameters": {
                  "a": "1",
                  "b": "2"
               }
            },
             {
              "name": "B",
              "parameters": {
                  "a": ["xxx","xxx","xxx"],
                  "b": ""
               }
            } 
         ], 
        "payload": {
          "id" : "7469639288002646016",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"4\"",
          "runningRule" : "xxx",
          "status" : "LIVE",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : null,
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-21T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 1,
          "metaData" : "xxx"
        },
        "post_processors": [
            {
              "name": "RetryIngore",
              "parameters": {
                  "ignore_unique_ids": ["1","2","3"]
               }
            }
         ] 
    }
 
RESP:
    {
        "id": 1,
        "data_unique_id": "7469639288002646016",
		"data_version": 1,
		"data_type": "RuleEngine",
        "request_id": "5b02926e-e83c-4936-b7a8-28c2f17231f9",
        "dc": "ID",
        "message": "",
        "status": "ACK"
    }
    OR
    {
        "id": 1,
        "data_unique_id": "7469639288002646016",
		"data_version": 1,
		"data_type": "RuleEngine",
        "request_id": "5b02926e-e83c-4936-b7a8-28c2f17231f9",
        "dc": "ID",
        "message": "xxx",
        "status": "NACK"
    }
```

# Sync Examples

## Rule Engine Sync

**CREATION:**

rule creation

PROCESSING

```
    {
        "data_unique_id": "7503343354181808128",
        "data_version": 0,
		"data_type": "RuleEngine",
		"operation_type": "CREATE",
		"payload": {
          "id" : "7503343354181808128",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"-100\"",
          "runningRule" : "xxx",
          "status" : "PROCESSING",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : null,
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-21T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 0,
          "metaData" : "xxx"
         }
    }
```
ADD_PENDING
```
    {
        "data_unique_id": "7503343354181808128",
        "data_version": 1,
		"data_type": "RuleEngine",
		"operation_type": "UPDATE",
		"payload": {
          "id" : "7503343354181808128",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"-100\"",
          "runningRule" : "xxx",
          "status" : "ADD_PENDING",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : null,
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-22T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 1,
          "metaData" : "xxx"
         }
    } 
```

rule creation checker approval:
LIVE
```
   {
        "data_unique_id": "7503343354181808128",
        "data_version": 2,
		"data_type": "RuleEngine",
		"operation_type": "UPDATE",
		"payload": {
          "id" : "7503343354181808128",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"-100\"",
          "runningRule" : "xxx",
          "status" : "LIVE",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : null,
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-22T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 2,
          "metaData" : "xxx"
         }
    }  
```

**UPDATE:**

rule creation maker update:
PROCESSING
```
    {
        "data_unique_id": "7503347298069082112",
        "data_version": 0,
		"data_type": "RuleEngine",
		"operation_type": "CREATE",
		"payload": {
          "id" : "7503347298069082112",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"-100\"",
          "runningRule" : "xxx",
          "status" : "PROCESSING",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : "7503343354181808128",
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-21T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 0,
          "metaData" : "xxx"
         }
    }
```

```
   {
        "data_unique_id": "7503347298069082112",
        "data_version": 1,
		"data_type": "RuleEngine",
		"operation_type": "UPDATE",
		"payload": {
          "id" : "7503347298069082112",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"-101\"",
          "runningRule" : "xxx",
          "status" : "ADD_PENDING",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : "7503343354181808128",
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-21T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 1,
          "metaData" : "xxx"
         }
    } 
```

rule creation checker approval:
LIVE
```
    {
        "data_unique_id": "7503347298069082112",
        "data_version": 2,
		"data_type": "RuleEngine",
		"operation_type": "UPDATE",
		"payload": {
          "id" : "7503347298069082112",
          "businessFlow" : "STRATEGIC_SETTLEMENT",
          "ruleType" : "NSTP",
          "userRule" : "Trade_Id == \"-101\"",
          "runningRule" : "xxx",
          "status" : "LIVE",
          "reason" : "test",
          "comment" : "2",
          "needDryRun" : false,
          "referenceRuleId" : "7503343354181808128",
          "createdAt" : "2026-06-21T23:28:44.915Z",
          "updatedAt" : "2026-06-21T23:33:47.629Z",
          "createdBy" : "1492285",
          "updatedBy" : "1434424",
          "version" : 2,
          "metaData" : "xxx"
         },
          "post_processors": [
            {
              "name": "RetryIngore",
              "parameters": {
                  "ignore_unique_ids": ["7503343354181808128"]
               }
            }
         ] 
    }  
```

# Appendix