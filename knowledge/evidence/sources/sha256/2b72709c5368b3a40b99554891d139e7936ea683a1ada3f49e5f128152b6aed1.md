**1.background**

During the comparison of Uber queue split data from May 25th, it was discovered that a message was missing in fmrp2: trade: 7153008753, traceId: 20884002ba5214319625367b862437ca.

In fact, tdxs has already sent this message in the split queue.

Further investigation revealed:

When the group service was consuming Uber messages, an exception occurred and the group deleted the original message, resulting in the message not being consumed normally.

![image-2026-5-27_16-22-33.png](attachments/image-2026-5-27_16-22-33.png)

![image-2026-5-28_9-39-4.png](attachments/image-2026-5-28_9-39-4.png)

![image-2026-6-3_16-2-40.png](attachments/image-2026-6-3_16-2-40.png)

inbound message in uat4 db:

![image-2026-5-27_16-23-55.png](attachments/image-2026-5-27_16-23-55.png)

but inbound message in fmrp2 db is missing:

![image-2026-5-27_16-25-3.png](attachments/image-2026-5-27_16-25-3.png)

## **1.1, ****Cause Analysis**

[1] handleMessage() execution

│
▼
[2] save(VALIDATED) → ratan_inbound_message insert record id=100

│
▼
[3] resourceLockManager.run() → publishEvent(UberValidatedEvent)

│ Downstream processing failed, throw Exception e

▼
[4] catch(Exception e):

deleteById(100) → ✅ Deletion successful, inbound table record disappears， Moreover, it only occurred once, indicating that there were no retries.

throw e

│
▼
[5] Spring Kafka catches exception

→ Call consumerErrorHandler.handleError()

→ consumerErrorHandler throws RatanServiceException

│
▼
[6] Exception is passed to container-level DefaultErrorHandler

→ Determine if the message has reached the retry limit (or because ListenerErrorHandler no longer seek-back after intervention)

→ Execute seekToNext(), offset advance

│
▼
[7] Result:

❌ No record found in ratan_inbound_message (deleted by deleteById)

❌ Kafka offset has been advanced (message will no longer be retried)

❌ Business processing incomplete

═══ Message permanently lost ═══

## Analysis process

1. The `TdsxUberMessageListener` currently only has `@KafkaListener`, **but not `@RetryableTopic`, so it won't read the `attempts` configuration.

2. This listener uses `errorHandler = "consumerErrorHandler"`, while `MessageConsumerErrorHandler` will continue to throw exceptions.

3. No custom `CommonErrorHandler/DefaultErrorHandler` bean configurations are seen in the project, so the container will fall into Spring Kafka's default container-level error handling.

Under this default path, the default backoff behavior of `DefaultErrorHandler` is usually (commonly `FixedBackOff(0, 9)`), which means:

**1 initial consumption + 9 memory retries = a total of 10 executions**.

It can also be determined that Uber's current retry semantics are: **in-memory retry**.

The core issue is that after the exception occurred, the message  has reached the retry limit（refer to 3 evidence）,

and at the same time, the data in the inbound table was deleted, resulting in the deletion of both the message and the original record.

# **2, other example**

2026-05-27,  f62f462588a404a5cf204757bb3231c3_7151397157, not consume both uat4 and fmrp2

cfid: 007390420129

in this case, the exception is "Duplicate key" Exception，There are 3 cashflows under trade, and all three cashflowIds are the same, as are the major versions.

![image-2026-5-28_9-41-38.png](attachments/image-2026-5-28_9-41-38.png)

![image-2026-6-3_16-9-16.png](attachments/image-2026-6-3_16-9-16.png)

📎 [7151397157.txt](attachments/7151397157.txt)

# **3，Evidence**

**3.1， reproducing the scenario**

**By reproducing the scenario in the dev environment, it was found that the group processed the same trade 10 times.**

![image-2026-6-26_10-53-15.png](attachments/image-2026-6-26_10-53-15.png)

# **4，Solution**

Comparing the retry mechanisms of the Uber and Scbml Listeners:

| Listener | Retry Mechanism | Retry Method | Final Guarantee |
| --- | --- | --- | --- |
| CashflowInboundListener | @RetryableTopic(attempts=5, backOff=15s*2) | Sends to a dedicated retry topic; Kafka layer guarantees retry; | DLT (Dead Letter Topic) fallback |
| TdsxUberMessageListener | None @RetryableTopic | Relies solely on container-level DefaultErrorHandler; In-memory retries | No DLT, discards messages after retries are exhausted |

## `**4.1，Uber adds retry configuration，using Kafka persistence retries**`

@RetryableTopic(
attempts = "${ratanone.topic.tdsx-uber-json-inbound.attempts:5}",
backOff = @BackOff(delay = 15000, multiplier = 2.0),
topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE,
numPartitions = "${ratanone.topic.tdsx-uber-json-inbound.retry-partition:3}",
concurrency = "${ratanone.topic.tdsx-uber-json-inbound.concurrency:1}"
)
@KafkaListener(topics = "${ratanone.topic.tdsx-uber-json-inbound.name}", batch = "false", errorHandler = "consumerErrorHandler", concurrency = "${ratanone.topic.tdsx-uber-json-inbound.concurrency:1}")
public void handleMessage(ConsumerRecord<String, String> record) {
}
## ~~**`4.2，Remove `deleteById` and replace it with findOrCreate to retain inbound records.`**~~

## ~~uberMessageInbound.setTradeId(tradeId);~~

~~uberMessageInbound.setAggId(new UberMessageInbound.UberMessageId(correlationId));~~
~~uberMessageInbound.setMessage(uberMessage);~~
~~uberMessageInbound.setMessageType(UBER);~~
~~uberMessageInbound.setStatus(UberMessageInbound.StatusEnum.VALIDATED);~~
~~uberMessageRepository.save(uberMessageInbound);~~

~~try {~~
~~resourceLockManager.run("trade_" + tradeId,~~
~~60,~~
~~String.format("Uber(%s-%s) message is in progress", tradeId, correlationId),~~
~~() -> eventPublisher.publishEvent(new UberValidatedEvent(uberMessageInbound)));~~
~~} catch (Exception e) {~~
~~log.error("Exception occurred when handling Uber message. " +~~
~~"correlationId: {}, tradeId: {}, uberMessageId: {}. " +~~
~~"Inbound record is PRESERVED for retry idempotency and audit.",~~
~~correlationId, tradeId, uberMessageInbound.getId(), e);~~
~~throw e;~~
~~}~~

## `**4.3，Add `@DltHandler` to provide a fallback mechanism at the Kafka layer.**

`

1. Referring to SCBML's DLT processing model, complete the Uber DLT logic:

a) Save `ratan_inbound_message` (Uber inbound message)

b) Save `ratan_cashflow_group`

c) Save `ratan_cashflow_group_message`

2. Compare the data with the already stored data according to the `major_version` + cashflow event (New/Withdrawal) scenario:

a) Data that has already been processed will not be processed again.

b) Data that has not been processed and needs to be processed is marked as ERROR.

## **4.4，Added retry and fallback functionality to CashflowGraphQLService.**

**Following the retry pattern of CashflowService.queryCashflow(), fault tolerance is added to the two external method calls.**

**CashflowService — with retries and degradation features**
} catch (Exception e) {
if (queryTimes < QUERY_MAX_TIME) {
log.warn("Query cashflow history one more time as exception occurred, cashflowId: {}, retryCount: {}",
cashflowId, queryTimes + 1, e);
return queryCashflowHistoriesByCashflowId(cashflowId, ++queryTimes);
} else {
log.error("Exception occurred when querying cashflow history, reached max retry {}, cashflowId: {}, degraded to empty list.",
QUERY_MAX_TIME, cashflowId, e);
return Lists.newArrayList();
}
}

![image-2026-6-25_16-30-53.png](attachments/image-2026-6-25_16-30-53.png)
## **`5，Before and after repair comparison`**

| step | Before repair | After repair |
| --- | --- | --- |
| The queryCashflowHistoriesByCashflowId call failed. | Immediately throw an exception and propagate it upwards. | After 3 retries, the system eventually returns an empty set. |
| The exception propagates to the TdsxUberMessageListener catch. | `deleteById` deletes the `VALIDATED` record. | log errors and retain records with ERROR status |
| Kafka retry | The record has been deleted; upon re-entry, it will be treated as a new message and may be duplicated. | Use Kafka's persistence retry mechanism to support DLT. |
| Final result | Message lost | Messages were processed normally, with no duplicates. |

# 6, Dependent services

| service | class | location | Failure behavior |
| --- | --- | --- | --- |
| ratanone-static-data-service | StaticDataServiceClient | `AmendmentGroupEventProcessor#isDedicatedChange` -> `findDedicateds` | `isDedicatedChangeWithCatch` has been caught; therefore, it should be returned as `true`. |
| `CashflowCutoffCommand#getMaterializeCutoff` | The exception was caught, and the command-level degradation occurred (some fields are missing). |
| `FXUSettlementMethodCommand#execute` | The exception is caught, and the degradation is not marked `UTIL`. |
| `CashflowBicNettingFlagCommand#execute` | The exception is caught and downgraded to an empty string. |
| RATANONE-DATA-AMBASSADOR | DataAmbassadorClient | `LegalEntityCommand#execute` -> `counterparty` | The exception is caught, downgraded to an empty field, and an exception flag is added. |
| DATradeRepository | `DataAmbassadorClient#queryTrade` | Built-in retry + catch, returns an empty list/empty flag on failure. |
| RATAN-CASH-SETTLEMENT-BATCH-SERVICE | BatchServiceClient | `CashflowPendingFixingFlagCommand#execute` | The exception is caught and the default value is degraded. |
| ATAN-CASH-SETTLEMENT-NETTING-SERVICE | NettingClient | `LienFlagCommand#fetchOriginalTradeIds` | If the exception is not caught separately within this method, it will be passed up to the command/outer layer for handling. |
| RATAN-CASH-SETTLEMENT-QUERY-SERVICE | CashflowGraphQLClient | AmendmentGroupEventProcessor.processReadyEvent | No retries, no downgrades |

# **7，Test case**

env: dev

tradeId: 7153008753

correlationId：e059cfa144bb9bc3222f50fb1b4f5c22_7153008753

Before the enhancement, an exception occurred while processing Uber messages.

The message was lost after 10 retries in memory via Kafka, and there was no data in the group/group_message/inbound table.

## 7.1 Case 1 The message was persisted in Kafka and retried 4 times before entering DLT

After the enhancement, an exception occurred during the processing of Uber messages.

1, The message was persisted in Kafka and retried 4 times before entering DLT;

![image-2026-7-1_11-4-10.png](attachments/image-2026-7-1_11-4-10.png)

2, The status of the group table was PENDING;

![image-2026-7-1_11-4-31.png](attachments/image-2026-7-1_11-4-31.png)

3, the status of group_message was ERROR;

![image-2026-7-1_11-4-58.png](attachments/image-2026-7-1_11-4-58.png)

4, the status of the inbound table was also ERROR;

![image-2026-7-1_11-5-30.png](attachments/image-2026-7-1_11-5-30.png)

5, cashflow was not sent downstream.

![image-2026-7-1_11-5-57.png](attachments/image-2026-7-1_11-5-57.png)

6，group blotter

![image-2026-7-1_11-9-52.png](attachments/image-2026-7-1_11-9-52.png)

7.2 Case 2  **The message was persisted in Kafka and retried less 4 times, and retry success**

**message was handle successfully in all table.**

**![image-2026-7-2_11-24-10.png](attachments/image-2026-7-2_11-24-10.png)**

**![image-2026-7-2_11-24-28.png](attachments/image-2026-7-2_11-24-28.png)**

**![image-2026-7-2_11-24-45.png](attachments/image-2026-7-2_11-24-45.png)**