# **1,  Background**

**Previously, all Uber messages were sent to a single solution queue. The goal is to change this by splitting the queue into eight queues based on the "primary asset class". **

**![image-2026-6-16_9-15-30.png](attachments/image-2026-6-16_9-15-30.png)**

**However, data comparison revealed that FMRP2 exhibits message loss issues.**

**Env: fmrp1 & fmrp2**

# **2，Cause Analysis**

## **2.1，fmrp2 lose message**

trade: 7153422395, traceId: 16a6f26acc4f17d39e9cf45454113ba0

trade: 7153422382, traceId: 7a756a7f83018dda1316ec41bcc9c661

![image-2026-6-11_15-36-6.png](attachments/image-2026-6-11_15-36-6.png)

![image-2026-6-11_17-42-55.png](attachments/image-2026-6-11_17-42-55.png)

The message was lost due to a workerPool error and the message was subject to duplicate prevention within 2 minutes.

Impact: messages are lost and will not be sent to the group service.

### **2.1.1，Analysis**

**Why does a workerPool exception occur?**

Old configuration (1:1):

Solace-Consumer-Route-uber-flow-A ──→ kafka:topicX (Only one thread participates in initialization for this route)

New configuration (N:1):

Solace-Consumer-Route-uber-flow-1 ──┐

Solace-Consumer-Route-uber-flow-2 ──┤

Solace-Consumer-Route-uber-flow-3 ──┤─→ kafka:topicX (Threads for N routes compete for initialization simultaneously)

... ┤

Solace-Consumer-Route-uber-flow-N ──┘

T=0ms Application startup complete, startAllRoutes() triggered

T=1ms Solace-Consumer-Route-uber-flow-1 receives message → ProducerTemplate.send("kafka:topicX?...") → Lazy creation of KafkaEndpoint

T=2ms Solace-Consumer-Route-uber-flow-2 receives message → ProducerTemplate.send("kafka:topicX?...") → Obtains the same KafkaEndpoint instance

T=2ms Solace-Consumer-Route-uber-flow-3 receives message → ProducerTemplate.send("kafka:topicX?...") → Obtains the same KafkaEndpoint instance

...
Thread-1: doStart() is initializing workerPool (incomplete)

Thread-2: Attempting KafkaProducer.process() → workerPool == null → ❌ Exception

Thread-3: Attempting KafkaProducer.process() → workerPool == null → ❌ exception

When N Consumer Routes simultaneously send messages for the first time, the probability of threads competing to initialize `workerPool` using `doStart()` increases sharply as N increases.

When N is greater than 10, is it almost certain that consuming a large number of messages simultaneously will trigger a workerPool is null exception?

### **2.1.2，root cause**

1, The launch of MB and the large number of Uber messages at the time caused multi-threaded contention.

code:

`TargetSplittingRoute.selfConfigure()`

.split().method(splitter)

.parallelProcessing()   // Parallel processing, submitted to the thread pool by MulticastProcessor

.to(MessageBridgeConstants.DIRECT_SUPPRESSION_ROUTE)

2, MessageProducerImpl trigger lazy initialization

`If one thread has not finished initializing the workPool while another thread has already acquired a KafkaEndpoint instance and attempted to send a message, a "workerPool == null" exception will be hit in Camel.`

`sentExchange = this.template.send(endpoint, sentExchange);

`

`In summary, changing the original 1:1 relationship between Solace and Kafka to an 8:1 relationship will amplify the potential for concurrent contention.`

## **`2.2，The fail_message table does not save message records`**

There's a strange phenomenon: when a workerpool exception occurs, the message is not saved to the raw_message table， why?

### **2.2.1，Analysis**

sendBody() exception
→ DispatchProducerRoute.onException (6 retries)
→ DIRECT_EXCEPTION_ROUTE
→ ExceptionProducerRoute.process()
→ DIRECT_RAW_MESSAGE_PERSISTENCE_ROUTE
→ RawMessagePersistenceProducerRoute.saveRawMessage()
→ ★ write ratan_bridge_fail_message

![image-2026-6-17_15-30-51.png](attachments/image-2026-6-17_15-30-51.png)

DispatchProducerRoute** print error log:**

![image-2026-6-16_19-44-6.png](attachments/image-2026-6-16_19-44-6.png)

om.scb.ratan.messagebridge.exception.MessageBridgeSolaceConsumeException: Solce route sends exchange to endpoint: kafka:tdsx_uber_message_json_inbound?valueSerializer=com.scb.ratan.messagebridge.serial.TDSXUberToJsonSerializer&brokers=10.198.24.247:9092,10.198.24.249:9092,10.198.24.251:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 failed with exception: workerPool must be specified at com.scb.ratan.messagebridge.route.producer.MessageProducerImpl.sendBody(MessageProducerImpl.java:111)

but in ExceptionProducerRoute class, tThere are no logs about "Processing occurs exception for target".

![image-2026-6-16_19-58-11.png](attachments/image-2026-6-16_19-58-11.png)

From all the logs above, we can analyze that:

1) For the two source keys used for deduplication prevention, the second deduplication flag was set to true, so the message was dropped directly.

★ Evidence 1 (09:51:12.922): The source key was written to Redis during the initial Solace delivery process.

key = ratanone:mb:dc:s:Solace-Consumer-Route-uber-flow-10-7a756a...-11550-null

is_duplicated = false (initial write), TTL = 120s

★ Evidence 2 (09:51:13~09:51:18): A workerPool error caused sendBody() to fail twice.

Each try-catch block only deleted the TARGET key (ratanone:mb:dc:s:kafka:tdsx_uber_message_json_inbound?...).

The SOURCE key was never deleted by any code path!

★ Evidence 3 (09:52:34.696): After Solace re-delivered the message, the source key was still in Redis:

key = ratanone:mb:dc:s:Solace-Consumer-Route-uber-flow-10-7a756a...-11550-null

is_duplicated = true → The message was FILTERED

★ Evidence 4: From 09:51:12.922 to 09:52:34.696, the time difference was approximately 82 seconds. Within TTL=120s,

the source key did not expire, causing the Solace re-delivered message to be mistakenly judged as a duplicate.

So why is the source key protected against duplicates?

Looking at the code, the source key and target key use the same variable, "duplication_check_key," and...
// TargetSplittingRoute.process() ：
exchange.setProperty(DUPLICATION_CHECK_KEY, "ratanone:mb:dc:s:Solace-Consumer-Route-uber-flow-10-...");
// ↑ SourceKey is written to DUPLICATION_CHECK_KEY// DispatchProducerRoute.process() ：
exchange.setProperty(DUPLICATION_CHECK_KEY, "ratanone:mb:dc:s:kafka:tdsx_uber_message_json_inbound?...");
// ↑ targetKey has overwritten sourceKey!//DispatchProducerRoute try-catch ：
DuplicationCheckHelper.removeDuplicationKey(exchange);
// → Reading `exchange.getProperty(DUPLICATION_CHECK_KEY) = targetKey` (already overwritten).
// → Redis.remove(targetKey)
// → The sourceKey can never be deleted through this path!

2）Due to an exception occurring in the workerPool, DispatchProducerRoute throws an exception, and Kafka will automatically retry (up to 6 times) and delete the target key.

3）The absence of execution records for ExceptionProducerRoute indicates that no fatal exception has occurred, requiring ExceptionProducerRoute to execute and the RAW_MESSAGE route to run.

Combining points 2 and 3, we can deduce that Kafka is still retrying sending, so there's no need to save it to raw_message.

## **`2.3，Phenomenon in fmrp1`**

**`tradeId: 8009318839,traceId: b9c77c3e52eecdfa0449b464feadbde1`**

![image-2026-6-12_13-23-50.png](attachments/image-2026-6-12_13-23-50.png)

` Since the re-consumption time exceeds 2 minutes, the consumption logic is re-executed, and the message is sent to the downstream.`

# `**3，Solution**

a）`