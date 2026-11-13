# Backgroud

Since Uber has fully integrated with the settlement, it is necessary to verify the processing performance of the workflow under different partitions in order to decide whether to expand the partition or server capacity.

# **PT result**

**5.6W cashflow **:

| | Scene A: partition:36, total consumer thread: 9 | Scene B: partition:36, total consumer thread: 18 | Scene C: partition:72, total consumer thread: 9 | Scene D: partition:72, total consumer thread: 18 | conclusion |
| --- | --- | --- | --- | --- | --- |
| total cost time | 104 m 15 s = 6255s | 98 m 47 s = 5927s | 88 m 7s = 5287s | 83 m 47s = 5027s | Scene D is 21 minutes shorter than Scene A. |
| db connections （active connections） | group : 30 lifecycle : 6 orchestration : 9 | group : 24 lifecycle : 6 orchestration : 11 | group : 21 lifecycle : 5 orchestration : 9 | group : 24 lifecycle : 7 orchestration : 18 | The number of db connections in scenario D also doubled. |
| CPU（max） | group : 90.4 lifecycle : 92.3 orchestration : 88.2 | group : 95.1 lifecycle : 96.4 orchestration : 94.4 | group : 98.3 lifecycle: 97.6 orchestration : 98.0 | group : 98.2 lifecycle : 99.1 orchestration : 99.7 | Maximum CPU usage close to 100% |

**2，****Camunda & Kafka Performance Report**

Key Takeaways

- Partition count alone is not the primary bottleneck.
- A real throughput gain only appears when partition count and total consumer-thread count increase together
- The performance improvement did not reach the theoretical doubling.

# PT

service: orchestration

staging:  Instance count：4

JVM： -Xms1024m -Xmx2048m
DB connections: miniIdle: 4, maxPoolSize: 20

topic: Cash_Settlement_Orchestration_Inbound， partition：36

| Conditions | Scenario | group cost time | orchestration cost time | result | group | lifecycle | orchestration CPU | orchestration Memory | orchestration db connections |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 trade and 40 cashflows | Send messages to 7 topics, each with 200 messages. Each message has a completely different cashflowId, meaning the group will not filter any cashflows, which is the worst-case scenario. consumersCount： 9 | start time: 2026-08-14 20:07:49 end time: 2026-08-14 20:12:19 total cost: 4m30s = 270s Total count of messages : 1400 total count of cashflow: 5.6W | start time: 2026-08-14 20:07:57 end time: 2026-08-14 21:52:12 total cost: 104m15s = 6255s | no error logs group max cpu: 90.4 lifecycle max cpu: 92.3 orchestration max cpu: 88.2 group db active connections used: 30 lifecycle db active connections used: 6 orchestration db active connections used: 9 | ![image-2026-8-15_15-23-0.png](attachments/image-2026-8-15_15-23-0.png) db connections ![image-2026-8-15_17-52-3.png](attachments/image-2026-8-15_17-52-3.png) | ![image-2026-8-15_15-22-11.png](attachments/image-2026-8-15_15-22-11.png) db connections ![image-2026-8-15_17-53-26.png](attachments/image-2026-8-15_17-53-26.png) | ![image-2026-8-15_15-23-33.png](attachments/image-2026-8-15_15-23-33.png) | ![image-2026-8-15_17-54-55.png](attachments/image-2026-8-15_17-54-55.png) | ![image-2026-8-15_17-50-51.png](attachments/image-2026-8-15_17-50-51.png) |
| | Send messages to 7 topics, each with 200 messages. Each message has a completely different cashflowId, meaning the group will not filter any cashflows, which is the worst-case scenario. consumersCount： 18 | start time: 2026-08-13 23:16:58 end time: 2026-08-13 23:21:09 total cost: 4m7s = 247s Total count of messages : 1400 total count of cashflow: 5.6W | start time: 2026-08-13 23:17:09 end time: 2026-08-14 00:55:56 total cost: 98m47s = 5927s | no error logs group max cpu: 95.1 lifecycle max cpu: 96.4 orchestration max cpu: 94.4 group db active connections used: 24 lifecycle db active connections used: 6 orchestration db active connections used: 11 | ![image-2026-8-14_9-18-51.png](attachments/image-2026-8-14_9-18-51.png) db connections ![image-2026-8-15_17-57-16.png](attachments/image-2026-8-15_17-57-16.png) | ![image-2026-8-14_9-27-49.png](attachments/image-2026-8-14_9-27-49.png) db connections ![image-2026-8-15_17-57-58.png](attachments/image-2026-8-15_17-57-58.png) | ![image-2026-8-14_9-17-54.png](attachments/image-2026-8-14_9-17-54.png) | ![image-2026-8-14_9-23-38.png](attachments/image-2026-8-14_9-23-38.png) | ![image-2026-8-15_17-56-40.png](attachments/image-2026-8-15_17-56-40.png) |

topic: Cash_Settlement_Orchestration_Inbound， partition：72

| Conditions | Scenario | group cost time | orchestration cost time | result | group | lifecycle | orchestration CPU | orchestration Memory | orchestration db connections |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 trade and 40 cashflows | Send messages to 7 topics, each with 200 messages. Each message has a completely different cashflowId, meaning the group will not filter any cashflows, which is the worst-case scenario. consumersCount： 9 | start time: 2026-08-15 15:32:14 end time: 2026-08-15 15:36:33 total cost: 4 m 19 s = 259 s Total count of messages : 1400 total count of cashflow: 5.6W | start time: 2026-08-15 15:32:19 end time: 2026-08-15 17:00:26 total cost: 88 m 7s = 5287s | no error logs group max cpu: 98.3 lifecycle max cpu: 97.6 orchestration max cpu: 98.0 group db active connections used: 21 lifecycle db active connections used: 5 orchestration db active connections used: 9 | ![image-2026-8-15_17-41-43.png](attachments/image-2026-8-15_17-41-43.png) db ![image-2026-8-15_17-43-38.png](attachments/image-2026-8-15_17-43-38.png) | ![image-2026-8-15_17-40-55.png](attachments/image-2026-8-15_17-40-55.png) db ![image-2026-8-15_17-45-59.png](attachments/image-2026-8-15_17-45-59.png) | ![image-2026-8-15_17-40-13.png](attachments/image-2026-8-15_17-40-13.png) | ![image-2026-8-15_17-38-36.png](attachments/image-2026-8-15_17-38-36.png) | ![image-2026-8-15_17-48-5.png](attachments/image-2026-8-15_17-48-5.png) |
| | Send messages to 7 topics, each with 200 messages. Each message has a completely different cashflowId, meaning the group will not filter any cashflows, which is the worst-case scenario. consumersCount： 18 | start time: 2026-08-15 17:32:09 end time: 2026-08-15 17:37:19 total cost: 5 m 10 s = 310 s Total count of messages : 1400 total count of cashflow: 5.6W | start time: 2026-08-15 17:32:19 end time: 2026-08-15 18:56:06 total cost: 83 m 47s = 5027s | no error logs group max cpu: 98.2 lifecycle max cpu: 99.1 orchestration max cpu: 99.7 group db active connections used: 24 lifecycle db active connections used: 7 orchestration db active connections used: 18 | ![image-2026-8-15_21-24-19.png](attachments/image-2026-8-15_21-24-19.png) db ![image-2026-8-15_21-27-11.png](attachments/image-2026-8-15_21-27-11.png) | ![image-2026-8-15_21-25-4.png](attachments/image-2026-8-15_21-25-4.png) db ![image-2026-8-15_21-27-58.png](attachments/image-2026-8-15_21-27-58.png) | ![image-2026-8-15_21-23-42.png](attachments/image-2026-8-15_21-23-42.png) | ![image-2026-8-15_21-25-53.png](attachments/image-2026-8-15_21-25-53.png) | ![image-2026-8-15_21-26-31.png](attachments/image-2026-8-15_21-26-31.png) |

# Based Runtime Performance Analysis

Current Processing Model

The current `InboundRoute` behaves as a **strong synchronous chain**:Kafka consume
-> RawMessage / DuplicationCheck
-> PublishEventProcessor
-> WorkflowProcessor#startConfirmationFlow
-> Camunda startProcessInstanceByKey(...)
-> inline BPMN progression
-> CommitKafkaOffsetProcessor

What This Means

1. A Kafka consumer thread stays busy during Camunda inline execution.
2. Kafka offset commit happens only after `startProcessInstanceByKey(...)` returns.
3. Any downstream HTTP latency inside Camunda service tasks directly increases consumer-thread occupancy time.

## Three real STG CSV datasets were analyzed

- **STG-A**: first real-server dataset
- **STG-B**: second real-server dataset
- **STG-C**: third real-server dataset

### Core Metrics Comparison

| Metric | STG-A | STG-B | STG-C | Class Or Method |
| --- | --- | --- | --- | --- |
| Complete samples | 21 | 40 | 33 | |
| `raw-message` avg | 19.1ms | 29.7ms | 19.6ms | RawMessageProcessor |
| `pre-workflow` avg | 53.5ms | 73.6ms | 52.1ms | WorkflowProcessor#doProcess |
| `start-process-instance-by-key` avg | 2655.5ms | 2863.4ms | 2260.6ms | WorkflowProcessor.startProcessInstance |
| `end-to-end-consume-to-commit` avg | 2751.1m | 2998.6ms | `2357.6ms | CommitKafkaOffsetProcessor#doProcess |
| `kafka-commit` avg | 13.0ms | 16.9ms | 15.9ms | CommitKafkaOffsetProcessor#doProcess |
| `service_sum` avg | 1971.7ms | 2050.9ms | 1650.2ms | BaseJavaDelegate#execute |
| `http_sum` avg | 1489.9ms | 1451.5ms | 1210.9ms | call downstream-http |

### Time Allocation Comparison

| Component | STG-A | STG-B | STG-C |
| --- | --- | --- | --- |
| Downstream HTTP share | 56.1% | `50.7% | 53.6% |
| Task-local processing share | 18.1% | 20.9% | 19.4% |
| Camunda / process-progression share | 25.8% | `28.4% | 27.0% |

### Readout

- **STG-B** was the slowest sample set
- **STG-C** was the fastest sample set
- **STG-C** also showed a much tighter tail than STG-B

### Performance Movement

1. STG-B was about `9.0%` slower than STG-A
2. STG-C was about `21.4%` faster than STG-B
3. STG-C was about `14.3%` faster than STG-A

Conclusion

> The realistic runtime baseline is not a fixed 3 seconds. Across the STG datasets, it is more accurately in the 2.3s to 3.0s range, with occasional higher tails.

# Stable Hotspots Across All CSV Runs

The hotspot pattern was highly consistent.

## Stable HTTP Hotspots

1. `msgEventCheck`   
2. `cashflow/stamp`  （Why directly access the group via lifecycle?）
3. `status/move`         （A single call takes a short time, but the number of calls is high.）
4. `checkPaymentDateForIRS`
5. `netForIRS`
6. `preCheck`

## STG-C HTTP Averages

| Endpoint | Count | Avg (ms) | Max (ms) |
| --- | --- | --- | --- |
| /v1/ratan/camunda/lifecycle/msgEventCheck | 68 | 242.2 | 306 |
| /v2/ratan/camunda/cashflow/stamp | 68 | 205.6 | 321 |
| /v1/netting/camunda/checkPaymentDateForIRS | 68 | 172.6 | 300 |
| /v2/ratan/camunda/lifecycle/status/move | 136 | 129.1 | 226 |
| /v2/ratan/camunda/cashflow/preCheck | 68 | 128.7 | 195 |
| /v1/netting/camunda/netForIRS | 68 | 124.3 | 225 |

## What Improved in STG-C vs STG-B

| Hotspot | STG-B Avg (ms) | STG-C Avg (ms) | Change |
| --- | --- | --- | --- |
| msgEventCheck | 351.9 | 242.2 | Significant improvement |
| cashflow/stamp | 201.7 | 205.6 | Roughly flat |
| status/move | 127.8 | 129.1 | Roughly flat |
| checkPaymentDateForIRS | 155.5 | 172.6 | Slightly higher |
| preCheck | 148.2 | 128.7 | Significant improvement |
| netForIRS | 142.4 | 124.3 | Significant improvement |

Interpretation

STG-C became faster not because the bottleneck pattern disappeared, but because several of the main hotspots improved at the same time.

# Bottleneck Interpretation

## What Is *Not* the Primary Bottleneck

The following are **not** the leading issue based on the current evidence:

1. Kafka commit
2. Raw-message handling
3. Pre-workflow overhead
4. Resource lock by itself
5. Partition count by itself

## What *Is* the Primary Bottleneck

The dominant cost structure is:

1. Synchronous downstream HTTP time
2. Synchronous Camunda inline orchestration
3. Consumer-thread occupancy until process progression returns
4. A fixed number of effective parallel slots during peak load

Core Framing

Camunda is not showing clear evidence of an abnormal engine-side failure. It is being used as a synchronous orchestrator, and that architecture makes downstream latency directly limit Kafka throughput.

# Optimization Recommendations

## Priority 1 — Optimize the Highest-Contribution HTTP Calls

Focus first on:

1. `msgEventCheck`
2. `cashflow/stamp`
3. `status/move`
4. `checkPaymentDateForIRS`
5. `netForIRS`
6. `preCheck`

## Priority 2 — Reduce the Number of Synchronous Steps

Even if single calls are acceptable, too many synchronous steps still accumulate to multi-second consumer occupancy.

Evaluate:

1. Merging some `status/move` operations
2. Merging duplicated checks
3. Moving eligible rule checks earlier
4. Reusing intermediate results instead of repeating remote calls

Key Point

> Reducing one synchronous remote call is often more valuable than micro-tuning a Camunda parameter.