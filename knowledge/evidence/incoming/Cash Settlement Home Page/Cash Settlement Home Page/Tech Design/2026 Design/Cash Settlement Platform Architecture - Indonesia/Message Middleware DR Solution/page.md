#

# Background

Given Ratan is going to follow the technical standard to change our cluster model from Active-Active to Active-Passive according to the page below:

<u>[RATAN active-active to active-passive - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+active-active+to+active-passive)</u>

Considering Ratan is using Kafka as the message middleware, and there is only 1 cluster cross two data centers(Active-Active mode).

With Active-Passive mode:

1. Assume we still use Kafka, there will be two Kafka clusters, it brings new topic that how to synchronize data(Topics, Partition, Offsets, ACLs etc.) between two Kafka clusters.
2. Assume we can propose a new solution to replace exiting Kafka if the 1st. item can be covered naturally, e.g. FM Solace.

# Objective

Message middleware Active-Passive Dual-Cluster DR Solution

- **RTO:** Within 2 hours (automated)
- **RPO:** 0 minutes for Active-Passive deployments

*RTO (Recovery Time Objective): the maximum acceptable downtime before service is restored. Example: RTO 30 minutes means the system must be back up within 30 minutes after a failure.
*RPO (Recovery Point Objective): the maximum acceptable data loss measured in time. Example: RPO 5 minutes means you can lose up to 5 minutes of data.

# Consumption

1. Assume FM solace fulfill our DR requirement RTO=2hours, RPO=0mins
2. Assume Indonesia need to be implemented with Active-Passive solution

# Kafka Usage in Cash Settlement

## **Topic with multi-partition**

This is the most common use case, currently in production, each topic has 6 partitions at least.

**How to implement in Solace?**

Solace has partitioned queue to support consuming in parallel which is similar with Kafka partition concept.

But, queue should be configured as non-exclusive.

Solace partitioned queue guarantees partition-key ordering instead of queue global ordering.

![types-of-queues.png](attachments/types-of-queues.png)

## **Topic has multiple consumer groups**

This is also common use case, e.g. cash_settlement_cashflow_domain_events has 7 consumer groups.

**How to implement in Solace?**

Here in Solace, the concept is queue. Topic

<details>
<summary>Expand Details</summary>

</details>

## **Partitioned Key Ordering**

In Kafka, partitioned key ordering means when producer publish messages with same key, after hashing or customized partitioner calculation, message will be delivered to the same partitions forever, in order to consuming in sequence.

**How to implement in Solace?**

As mentioned above, Solace technically support partitioned queue to guarantee partition-key ordering as well.

## **Kafka Non-blocking Retry**

Spring Kafka support non-blocking retry based on Topic + Offset + Seek, this case usually used in the case that we need better message consumption throughput and not required sequence.

**How to implement in Solace?**

Solace is not naturally support non-blocking retry as there is no offset and seek concept. If we want to migration to Solace then need to cover retry in our application.

**Business related topic definition**

[Ratan Component Core Configuration Collection - 2025 New Deployment - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+Component+Core+Configuration+Collection+-+2025+New+Deployment)

**Kafka non-blocking retry**

| | Topic Name | | |
| --- | --- | --- | --- |
| 1 | Cash_Settlement_Group_Message_Inbound | Cash_Settlement_Group_Message_Inbound-retry-0/1/2/3/dlt | Standardization service consume cashflow SCBML inbound from 1. tds3 2. mxg adaptor |
| 2 | TDS3_Trade_Message_Process_In | TDS3_Trade_Message_Process_In-retry-0/1/2/3/4/dlt | Stella trade message inbound from: 1. tds3 |
| 3 | TDS3_Trade_Murex_Message_Process_In | TDS3_Trade_Murex_Message_Process_In-retry-0/1/2/3/4/dlt | Murex trade message inbound from: 1. tds3 |
| 4 | cash_settlement_cashflow_domain_events | cash_settlement_cashflow_domain_events-retry-0/1/2/3/dlt cash_settlement_cashflow_domain_events-retry-5000/10000/20000/dlt | lifecycle domain events consumed by: 1. standardization service 2. accouting service 3. opensearch agent 4. netting service 5. fx utilization service 6. lms service 7. query service retry topics are used in query service and opensearch-agent |

<details>
<summary>Expand Details</summary>

```java
@RetryableTopic(attempts = "${ratanone.topic.upstream-inbound.attempts:5}", 
				backoff = @Backoff(delay = 15000, multiplier = 2.0), 
				topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE, 
				numPartitions = "${ratanone.topic.upstream-inbound.retry-partition:3}", 
				concurrency = "${ratanone.topic.upstream-inbound.consumer-concurrency:3}")
@KafkaListener(topics = "${ratanone.topic.upstream-inbound.topic}", batch = "false", filter = "cashflowInboundFilter", errorHandler = "consumerErrorHandler", concurrency = "${ratanone.topic.upstream-inbound.consumer-concurrency:3}")
public void handleMessage(ConsumerRecord<String, String> record) {
    //process ConsumerRecord from main topic and retry topics
}

@DltHandler
public void handleDlt(ConsumerRecord<String, String> record) {
	//handle dead letter 
}
```

</details>

**Hard dependency ****in CQRS framework**

1. CQRS is a design pattern to publish domain event asynchronously and hard dependency with Kafka
2. Producer and consumer need to import ratanone-cqrs-spring-boot-starter then no need to care about underlying message middleware logic
3. Producer need to register a specific topic for domain event publishing

# Proposal

## Kafka Active-Passive Dual-Cluster

### Current State

- Application runs active-active across two data centers.
- Single Kafka cluster shared across both data centers.
- Producers and consumers connect to the same cluster.

### Target State (Active-Passive, Dual Clusters)

- Application runs active-passive across two data centers.
- Each data center has its own Kafka cluster.
- Replication/DR strategy keeps standby cluster ready for failover.

### Options

### Option 1: Kafka MirrorMaker 2 (MM2)

**Description:** Kafka Connect-based replication from active to passive. Topics are mirrored with optional offset/ACL sync.

**Failure behavior:**

- Failover: switch producers/consumers to passive cluster.
- RPO depends on replication lag; RTO depends on failover automation.

**Pros**

- Apache Kafka native tooling, widely used.
- Flexible configuration, topic selection, and renaming.
- Compatible with open-source stacks.

**Cons**

- Eventual consistency; lag may be non-zero.
- Operational overhead (Connect workers, lag monitoring).
- Failback requires offset/consumer coordination.

### Option 2: Confluent Cluster Linking / Replicator

**Description:** Enterprise-grade Kafka replication between clusters with built-in monitoring and lower operational friction.

**Failure behavior:**

- Failover: redirect clients to passive cluster; cluster linking maintains mirrored topics.
- RPO low; RTO depends on routing and automation.

**Pros**

- Managed replication features and observability.
- Lower operational burden and better support.
- Cleaner offset handling (especially with Cluster Linking).

**Cons**

- Licensing cost and platform dependency.
- Requires Confluent platform alignment.

### Option 3: Application Dual-Write

**Description:** Producers write to both Kafka clusters; consumers read from active only.

**Failure behavior:**

- Failover: consumers switch to passive; data already present.
- RPO can be near-zero if dual write succeeds.

**Pros**

- Very low RPO.
- Avoids replication lag dependency.
- Independent of replication tooling.

**Cons**

- Requires producer code changes.
- Must handle partial-write consistency, retries, idempotence.
- Higher app complexity and testing effort.

### Option 4: Object Store Log Shipping (Cold/Warm Standby)

**Description:** Sink to object store (e.g., S3/MinIO), then restore to passive cluster if needed.

**Failure behavior:**

- Failover: restore from object store; longer RTO.
- RPO/RTO higher; not real-time.

**Pros**

- Low cost for long retention.
- Strong audit/replay capabilities.

**Cons**

- Not suitable for real-time failover.
- Longer recovery time.

## Replace Kafka With Solace

**Description:** Move messaging to Solace PubSub+ and rely on the Solace team to provide DR and cross-DC availability. Kafka is removed from the app path; client code migrates from Spring Kafka to Solace APIs (JMS/JCSMP or Spring Cloud Stream Solace binder).

**Failure behavior:**

- DR handled by Solace HA/DR (primary/backup brokers, replication, and failover policies).
- App failover is primarily endpoint/DNS reroute to the active Solace service.

**Behavior differences vs Kafka:**

- **Ordering:** Kafka guarantees order within a partition. Solace preserves order within a queue (single consumer flow) or within a topic subscription per flow, but ordering across competing consumers is not guaranteed and depends on queue/flow configuration.
- **Partitioning vs. routing:** Kafka partitions drive scale, ordering, and key-based routing. Solace uses topic hierarchy and queue bindings/selectors; key-based ordering must be modeled explicitly (e.g., one queue per key group or a consistent mapping strategy).
- **Replay/retention:** Kafka has built-in log retention and offset-based replay. Solace supports persistence and replay features, but replay behavior is different (broker-managed replay vs log offsets) and depends on platform configuration and licensing.
- **Consumer model:** Kafka consumers pull and manage offsets in a group. Solace consumers receive push-based delivery with ACKs; redelivery and backoff are handled via queue settings and client ACK behavior.
- **Delivery semantics:** Kafka provides idempotent producers and transactions for exactly-once in some flows. Solace supports persistent delivery with ACKs but does not mirror Kafka transactions semantics; idempotence is typically implemented at the application layer.
- **Scaling model:** Kafka scales by partitions and consumer group members. Solace scales via multiple consumers on a queue or topic subscriptions with flow control; throughput tuning differs.

**How to implement (high-level):**

- **Connectivity:** get Solace service endpoints, credentials, and HA/DR VIPs.
- **Client migration:** - Replace `spring-kafka` with **Spring Cloud Stream Solace binder** or **Solace JMS/JCSMP** client. - Map Kafka topics/partitions to Solace topics/queues (fanout, durable queues, selectors). - Update producer semantics (ACKs, retries, persistence, delivery mode). - Update consumer semantics (manual ACK, redelivery, backoff, concurrency).
- **Data model:** decide on message headers, schema registry alignment, and keying strategy.
- **Ops:** migrate monitoring (consumer lag -> queue depth, flow control), and update runbooks.
- **Known constraints from current app:** - Uses `spring-kafka` non-blocking retry and CQRS with a customized `KafkaListenerContainerFactory`. - Uses auto topic creation and self-managed partitioning. - Solace topic/queue provisioning is controlled by another team and requires a request form, reducing flexibility for rapid topic/partition changes.

**Pros**

- DR/HA responsibility shifts to Solace platform team.
- Mature enterprise messaging with built-in HA/DR patterns.
- Simplified cross-DC operations for the app team.

**Cons**

- Significant app refactor and testing effort.
- Behavior differences vs Kafka (ordering, replay, partitioning semantics).
- Vendor dependency and licensing considerations.
- **Current app constraints:** migration impacts custom `KafkaListenerContainerFactory`, non-blocking retry, and CQRS patterns; topic/queue provisioning is less flexible.

## 5. Comparison

| Option | RPO | RTO | Cost | Complexity | Operational Maturity |
| --- | --- | --- | --- | --- | --- |
| MM2 | Low-Medium (non-zero) | Medium | Low | Medium | Medium |
| Confluent Linking/Replicator | Low (non-zero) | Low-Medium | High | Medium | High |
| Dual-Write | Near-Zero to Zero | Low | Medium | High | High |
| Log Shipping | High | High | Low | Low-Medium | Low |
| Solace (Replace Kafka) | Low (platform-dependent) | Low-Medium | High | High | High |

## 6. Change Scope and Effort

| Solution | Pros | Cons |
| --- | --- | --- |
| Kafka cluster sync up | 1. Less code change 2. Flexibility to manage Kafka config and data internally. 1. Scaling up depends on data volume 2. Testing and development purpose 3. Ratan application integrity managed by our team | 1. Cost of Kafka cluster sync up component maintenance & trouble shooting |
| Integration with Solace | 1. Decouple with message middleware DR, rely on Solace team | 1. Hard dependency with other team 2. Topic & queue creation & configuration need additional process and need to pre-define in advance, any adjustment need more effort 3. Application has big code change effort. Need much time on development and testing. 4. Developer learning curve. 5. Hard to trouble shooting according to our application complexity 6. Not aware Solace team details such as monitoring, trouble shooting etc. 7. Not aware whether FM solace meet our DR requirement. |

### Common Changes (All Options)

- Build Kafka cluster in the passive DC.
- Configure network connectivity and security controls (TLS, ACLs, firewall).
- Add monitoring for replication lag, consumer offsets, and failover readiness.
- Define failover/failback runbooks and DR testing schedules.

### Option-Specific Scope

- **MM2:** Deploy Kafka Connect, tune replication filters, implement lag alerting.
- **Confluent Linking/Replicator:** License setup, platform configuration, monitoring integration.
- **Dual-Write:** Producer code changes, retry/idempotence logic, metrics and audit trails.
- **Log Shipping:** Sink/source connectors, storage policies, restore tooling.
- **Solace (Replace Kafka):** Client migration, semantics mapping, integration testing, and operational runbook updates.

## 7. Migration Strategy (High-Level)

1. Stand up passive Kafka cluster and validate baseline health.
2. Choose replication approach and configure syncing.
3. Run shadow consumers to validate data parity.
4. Run DR drills and measure RPO/RTO.
5. Cut over with controlled failover test.

## Recommendation

Given **RPO 0 minutes** and **producer changes allowed**, **Dual-Write** best meets the data loss objective. If licensing is acceptable and operational simplicity is prioritized, **Confluent Cluster Linking** is the next-strongest option with low lag but still non-zero RPO. MM2 remains a viable open-source baseline when cost or licensing is the dominant constraint.

**Solace recommendation:** viable when the enterprise mandates Solace as the messaging backbone and owns DR/operations. It is **not recommended** if Kafka semantics (partition ordering, replay, and ecosystem tooling) are hard requirements or if the team cannot afford a significant client migration and regression testing cycle. **Given current app constraints (custom Spring Kafka patterns and self-managed topics/partitions), Solace is higher risk unless the platform team can provide equivalent automation and provisioning flexibility.**