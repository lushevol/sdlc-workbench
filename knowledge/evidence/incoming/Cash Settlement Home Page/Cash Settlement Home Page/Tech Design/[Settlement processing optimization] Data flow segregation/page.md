# Requirement:

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6325957](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6325957)

# Background

Issues found:

1. Payment processing for all entities fall into one workflow, which could causing lags
2. Query service sync up status speed should be optimized, we see lags on cashflow status sync up on UI

Process need to be optimized, data flow segregation is possible proposal

Scenario: UK batch job execution causes dat lags, at same time the CN real time payment could be stuck. To avoid the impact by different time zone, data segregation by country is a valid approach.

| Country | FMID amount |
| --- | --- |
| SG | 4 |
| GB | 2 |
| IN | 2 |
| CN | 30 |
| DE | 1 |
| MY | 2 |

# Current Producer partitioning

`
`

# Proposal:

## Solution 1: Data segregation on Topic level

To implement data segregation on topic level, for each country we should have a topic to make sure the producer publish specific message to specific topic, for example:

Assume we have 2 countries - GB, CN, topic: Cash_Settlement_Orchestration_Process_In

There could be two more additional topics:

### How to Implement:

**Producer side - **Producers Builds a topic generator based on the onboarded countries and determines the particular topic by given messages.

**Consumer side - **Consumers need to listen to all the topics with different suffix.

## Solution 2: Data segregation on Partition level

##

### How to implement

**Foundation change:**

1. Define customized KafkaTemplate with customized Partitioner, Serializer and Deserializer
2. Provide customized Partitioner implements Partitioner interface and implement partition().

**Producer side - **

1. Configure Partition group key, partition rate.
2. Publish message with DomainPartitionKey

**Consumer side - **No change

### Principals:

1. Partition group is a logical concept, it should according to the configuration.
2. According to the requirement, two-level partitioning is proposed, first level key is responsible for determining the partition group, second level key is responsible for determine the partition among the partition group, so more than 2 level partitioning will not be considered
3. Data flow segregation should only apply to the producer which need to publish with two-level partitioning key and not impact the existing producer which not change.
4. If partition scaling up, then the partition group will be recalculation, so partition is not static and fixed for each group.

Code Snippet

```java
@ConfigurationProperties(prefix = "ratanone.kafka-producer")
public class PartitionProperties {

    private List<PartitionGroup> partitionGroup;

    @Getter
    @Setter
    public static class PartitionGroup {

        private List<String> groupName;

        private Double rate;
    }

}
```

```yml
spring:
  kafka:
    consumer:
      key-deserializer: com.scb.ratan.cashflow.entrypoint.message.config.DomainPartitionKeyDeserializer
    producer:
      key-serializer: com.scb.ratan.cashflow.entrypoint.message.config.DomainPartitionKeySerializer
      properties:
        partitioner.class: com.scb.ratan.cashflow.entrypoint.message.config.RatanDomainPartitioner

ratanone:
  kafka-producer:
    strategy: cashflow-country
    partition-group:
      - groupName:
        - GB
        rate: 0.8
      - groupName:
        - SG
        - IN
        - CN
        - DE
        - MY
        rate: 0.2
```

```java
@Component
public class RatanDomainPartitioner implements Partitioner {

    @Override
    public int partition(String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, Cluster cluster) {
	 
		Integer partitionCnt = cluster.partitionCountForTopic(topic);

        if (partitionCnt == 1) {

            log.info("Topic partition count is 1, no choice to calculate, use partition-0 directly.");

            return 0;

        }

        if (key == null) {

            log.info("keyBytes is null, will use round robin partitioning.");

            return roundRobinPartitioning(topic, cluster, partitionCnt);

        }

        if (actualPartitionHelper == null){

            log.warn("No partitionHelper, partitionProperties, or partitionGroupRates for partitioning, will use default.");

            return BuiltInPartitioner.partitionForKey(keyBytes, partitionCnt);
        }

        if (key instanceof DomainPartitionKey) {

            return actualPartitionHelper.partitionSelect(topic, key, keyBytes, value, valueBytes, cluster, partitionProperties.getPartitionGroup());

        }

        return BuiltInPartitioner.partitionForKey(keyBytes, partitionCnt);

    }

    @Override
    public void close() {

    }

    @Override
    public void configure(Map<String, ?> map) {

        List<PartitionHelper> partitionHelperList = cashflowPartitionHelper.stream().toList();

        if (CollectionUtils.isEmpty(partitionHelperList)){
            log.warn("No partitionHelper bean found, please check.");
            return;
        }

        if (partitionProperties == null || CollectionUtils.isEmpty(partitionProperties.getPartitionGroup())){
            log.warn("No partition group configured. will use default partition logic.");
            return;
        }

        Optional<PartitionHelper> partitionHelperOptional = partitionHelperList.stream().filter(partitionHelper ->
                partitionHelper.getPartitionStrategy().getName().equalsIgnoreCase(partitionProperties.getStrategy())).findFirst();

        if (partitionHelperOptional.isEmpty()){
            log.warn("No partitionHelp been found by given ");
            return;
        }

        actualPartitionHelper = partitionHelperOptional.get();

        log.info("Find partitionHelper successfully: {}", actualPartitionHelper.getPartitionStrategy());
   }
}
```

```java
@@Slf4j
@Component
public class DomainPartitionHelper implements PartitionHelper {

    @Override
    public PartitionStrategy getPartitionStrategy() {

        return PartitionStrategy.CASHFLOW_COUNTRY;

    }

    public int partitionSelect(String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, Cluster cluster, List<PartitionProperties.PartitionGroupRate> partitionGroupRates) {

        Integer partitionCnt = cluster.partitionCountForTopic(topic);

        String partitionKey = ((DomainPartitionKey) key).getPartitionKey();

        Optional<PartitionProperties.PartitionGroupRate> messageGroupProperties = partitionGroupRates.stream().filter(partitionGroupRate -> partitionGroupRate.getPartitionGroups().contains(((DomainPartitionKey) key).getPartitionGroupKey())).findFirst();

        if (messageGroupProperties.isEmpty() || partitionGroupRates.size() >= partitionCnt){

            return BuiltInPartitioner.partitionForKey(keyBytes, partitionCnt);

        } else{

            long partition = doSelect(partitionKey, partitionCnt, messageGroupProperties.get(), partitionGroupRates);

            if (partition < 0 || partition >= partitionCnt){

                return BuiltInPartitioner.partitionForKey(keyBytes, partitionCnt);

            } else {

                return (int) partition;
            }
        }
    }

    private long doSelect(String partitionKey, Integer partitionCnt, PartitionProperties.PartitionGroupRate partitionGroupRate, List<PartitionProperties.PartitionGroupRate> partitionGroupRates) {

        double summaryRate = partitionGroupRates.stream().mapToDouble(PartitionProperties.PartitionGroupRate::getRate).sum();

        int index = partitionGroupRates.indexOf(partitionGroupRate);

        long partitionOffset = 0;

        if (index > 0){

            partitionOffset = partitionGroupRates.stream()
                    .filter(partitionGroupRate1 -> partitionGroupRates.indexOf(partitionGroupRate1) < index)
                    .mapToLong(partitionGroupRate1 -> Math.round(partitionCnt * partitionGroupRate1.getRate() / summaryRate) > 0 ?
                            Math.round(partitionCnt * partitionGroupRate1.getRate() / summaryRate) : 1)
                    .sum();

        }

        long partitionSize = Math.round(partitionCnt * partitionGroupRate.getRate() / summaryRate) > 0 ?
                Math.round(partitionCnt * partitionGroupRate.getRate() / summaryRate) : 1;

        log.info("Partition offset: {}, partition size: {}", partitionOffset, partitionSize);

        if (index == partitionGroupRates.size() - 1 && (partitionOffset + partitionSize) < partitionCnt){

            return Math.abs(partitionKey.hashCode()) % (partitionCnt - partitionOffset) + partitionOffset;

        }

        return Math.abs(partitionKey.hashCode()) % partitionSize + partitionOffset;
    }
} 
```

```java
public class DomainPartitionKeySerializer implements Serializer<DomainPartitionKey> {

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {
        Serializer.super.configure(configs, isKey);
    }

    @Override
    public byte[] serialize(String topic, DomainPartitionKey domainPartitionKey) {

        String keyStr = domainPartitionKey.getPartitionGroupKey() + "." + domainPartitionKey.getPartitionKey();
        return keyStr.getBytes();
    }

    @Override
    public byte[] serialize(String topic, Headers headers, DomainPartitionKey dataPartitioningKey) {
        return Serializer.super.serialize(topic, headers, dataPartitioningKey);
    }

    @Override
    public void close() {
        Serializer.super.close();
    }

}
```

```java
public class DomainPartitionKeyDeserializer implements Deserializer<DomainPartitionKey> {

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {
        Deserializer.super.configure(configs, isKey);
    }

    @Override
    public DomainPartitionKey deserialize(String s, byte[] bytes) {

        String keyStr = new String(bytes);

        String[] keyAttrs = keyStr.split("\\.");

        DomainPartitionKey dataPartitioningKey = new DomainPartitionKey();

        dataPartitioningKey.setPartitionGroupKey(keyAttrs[0]);
        dataPartitioningKey.setPartitionKey(keyAttrs[1]);

        return dataPartitioningKey;
    }

    @Override
    public DomainPartitionKey deserialize(String topic, Headers headers, byte[] data) {
        return Deserializer.super.deserialize(topic, headers, data);
    }

    @Override
    public DomainPartitionKey deserialize(String topic, Headers headers, ByteBuffer data) {
        return Deserializer.super.deserialize(topic, headers, data);
    }

    @Override
    public void close() {
        Deserializer.super.close();
    }

}
```

### Result of data sample distribution:

| | Topic Partition | Partition Group Configuration | Partition Group Key |
| --- | --- | --- | --- |
| 1 | × | × | √ |
| 2 | √ | × | × |
| 3 | × | √ | × |

1. Topic Partition, partition group configuration not changed, partition group key changed e.g. partition count for topic = 36, group GB=0.8, SG,IN,CN,DE,MY=0.2 **a. GB message partitioning** 100 GB + Random partition key distribution result: [5, 4, 6, 5, 2, 4, 7, 4, 6, 3, 1, 1, 3, 4, 4, 3, 3, 1, 5, 2, 1, 2, 0, 3, 4, 4, 3, 3, 7, 0, 0, 0, 0, 0, 0, 0] 1000 GB + Random partition key distribution result: [30, 40, 25, 26, 38, 35, 36, 37, 42, 23, 37, 37, 38, 32, 38, 36, 30, 37, 33, 37, 42, 44, 21, 34, 32, 39, 24, 33, 44, 0, 0, 0, 0, 0, 0, 0] 10000 GB + Random partition key distribution result: [326, 352, 325, 346, 336, 338, 351, 360, 343, 363, 337, 351, 330, 324, 314, 352, 342, 343, 343, 367, 341, 338, 331, 347, 344, 361, 352, 389, 354, 0, 0, 0, 0, 0, 0, 0] 100000 GB + Random partition key distribution result: [3505, 3339, 3429, 3513, 3460, 3553, 3422, 3402, 3581, 3436, 3408, 3414, 3482, 3483, 3434, 3425, 3545, 3450, 3419, 3386, 3438, 3336, 3461, 3400, 3510, 3420, 3499, 3452, 3398, 0, 0, 0, 0, 0, 0, 0] **b. IN message partitioning** 1000 IN + Random partition key distribution result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 131, 149, 133, 149, 146, 131, 161] 10000 IN + Random partition key distribution result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1474, 1399, 1373, 1487, 1447, 1434, 1386] **c. DE message partitioning** 1000 DE + Random partition key distribution result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 133, 143, 163, 130, 148, 128, 155] 10000 DE + Random partition key distribution result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1441, 1418, 1455, 1417, 1400, 1409, 1460] **d. SG message partitioning** 1000 SG + Random partition key distribution result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 133, 164, 155, 157, 113, 132] 10000 SG + Random partition key distribution result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1445, 1428, 1411, 1461, 1389, 1408, 1458] **e. HK message partitioning(not in scope) **10000 HK + Random partition key distribution result:[268, 279, 283, 293, 280, 271, 268, 265, 276, 253, 278, 285, 299, 267, 274, 271, 268, 296, 292, 304, 278, 289, 243, 287, 259, 287, 270, 292, 293, 281, 295, 267, 266, 279, 300, 244]
2. Partition group configuration, partition group key not changed, topic partition changed e.g. group GB=0.8, SG,IN,CN,DE,MY=0.2 1. **Partition count = 1** 10000 CN or IN result: [10000] 2. **Partition count <= partition group list setting（1->2）** 10000 IN, partition count from 1 to 2 result: [7472, 2528] 3. **1 change to partition count > partition group list setting（1->6）** 10000 IN, partition count from 1 to 6 result: [5000, 0, 0, 0, 0, 5000] 4. **1 change to partition count >> partition group list setting（1->36） **10000 IN, partition count from 1 to 36 result: [5000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 711, 718, 729, 694, 709, 730, 709] 5. **6 change to partition count >> partition group list setting（6->36） **10000 IN, partition count from 1 to 36 result: [0, 0, 0, 0, 0, 5000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 692, 730, 695, 717, 717, 712, 737]
3. Topic partition and partition group key not changed, partition group configuration changed. 1. Add new partition group 2. Adjust existing partition group rate. 3. Invalid configuration - Partition group summary rate over than 1

**Special case**

Case 1 - valid configuration but 1 level partition Key as result, partition count will be 0 after rounding

| partition group rate | partition count | partition count for the group | Partition Strategy |
| --- | --- | --- | --- |
| 0.1 | 1/2 3/4 | < 0.5 ~ 0 | 1 level key → group configuration size >= partition size 1 level key → calculated partition overflow, pre group 0.9 occupied all partitions. 0.1 will use default partitioner |
| 0.2 | 1/2 | < 0.5 ~ 0 | 1 level key → group configuration size >= partition size |
| 0.3 | 1 | < 0.5 ~ 0 | 1 level key → group configuration size >= partition size |
| 0.4 | 1 | < 0.5 ~ 0 | 1 level key → group configuration size >= partition size |

Case 2 - Data not covered by configuration.

Case 3 - Partition calculator result in idle partition exists.(Fixed)

e.g. partition count for topic = 36, group GB=0.4, IN, DE, SG=0.4, CN, MY=0.2

result:     [29, 30, 32, 24, 30, 31, 31, 33, 31, 21, 23, 25, 29, 31, 28, 22, 31, 31, 29, 20, 35, 20, 30, 32, 36, 18, 35, 33,** 0,** 28, 24, 27, 23, 36, 30, 32]

After Fix:

GB partition result: [39, 27, 24, 26, 28, 45, 27, 22, 29, 27, 23, 20, 38, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
IN partition result:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 27, 27, 26, 28, 35, 25, 22, 27, 38, 35, 22, 20, 33, 0, 0, 0, 0, 0, 0, 0, 0]
CN partition result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 28, 18, 19, 23, 26, 22, 31]

Case 4 - Configuration overflow -  partition group summary rate cover than 1

e.g. partition count for topic = 36, group GB=1, IN, DE, SG=1, CN, MY=1

Partition result:(12 partitions for each)

GB partition result: [34, 29, 37, 32, 31, 28, 26, 37, 34, 37, 43, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
IN partition result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 24, 18, 31, 25, 23, 23, 35, 23, 29, 23, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
CN partition result: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 32, 23, 24, 26, 30, 21, 18, 16, 23, 27, 29]

### Open Questions:

1. What if the partition overflow? e.g. configured GB-0.8, CN,DE,SG,IN-0.2, then if other country data inbound, which partition should be used? Default partition should be used or use default partitioner?

A: Yes, although there is partition group defined, our principal is no data loss. so we need to define a default partition or partitioner. default partition is very easy like partition-0, but data may not distributed in balance. Default partitioner is more strategy.

2. What if the partition group defined is more than partition amount? e.g. GB-0.8, CN,DE,SG,IN-0.2, but there's only 1 partition, or 6 partitions but 7 group defined? Is that mean the customized partitioner is invalid?

A: Before answer the question, we need to think about what is actually our expectation. if the data partitioning is not allow data overlap, I think it's very difficult to keep the high **Scalability **and** Tolerance. **We have to allow data overlap. So to answer the question, if there is only 1 partition, partition group configuration will be ignored and all data will be delivered to partition-0; if 6 partitions but 7 groups defined, then 2 groups may share same partition is acceptable.

3. Partition group name is country basis or booking entity fmid basis? Either should be provided by producer when calling kafkaTemplate.send()

A: Each way is fine, producer need to take the entity fmid and country mapping in memory if name is country basis. fmid basis is more easier for producer but not easy to calculate partition group, country basis is preferred by me so far.

4. Do we need to consider other partition strategy? Is it over design for other cases besides country-id(country-tradeId, country-cashflowId, country-nettingId) basis?

A: If it is not big effort we can consider the extension, but now we need to consider the three key types by default.

5. Detail calculation strategy, such as partition group weight

A: Yes will take some time to design this calculation strategy because it's the most important core part.

6. Any exceptions occurred during partitioning, should use default logic instead to avoid any message missing?

A: As mentioned above, we need default partitioner to avoid data loss.