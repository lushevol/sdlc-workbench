# **1，Backgroud**

**Split one topic into seven topics, and have each of the seven topics consume Uber messages.**

** fmrp2:  Instance count：3, partition：12（Only 9 partitions were actually used） ， concurrent： 3 ；  db pool:  min 2, max 8**

| ** ** | **Scenario** | time | send tps | result | remark |
| --- | --- | --- | --- | --- | --- |
| **1 trade and 40 cashflows** | Distribute 100 messages to 7 topics in 50 seconds | 07-13 10:16 | 2 | max consume tps: 0.467 group max cpu: 81.7% | no exception |
| Distribute 100 messages to 7 topics in 25 seconds | 07-13 10:30 | 3 | max consume tps: 2.14 group max cpu: 83.2% | no exception |
| Distribute 100 messages to 7 topics in 25 seconds | 07-13 09:38 | 4 | max consume tps: 0.418 group max cpu: 82.8% | db timeout, db connection limit reached |
| Distribute 100 messages to 7 topics in 20 seconds | 07-06 09:10 | 5 | max consume tps: 2.52 group max cpu: 68.0% | db timeout, db connection limit reached |
| **1 trade and 12 cashflows** | Distribute 1000 messages to 7 topics in 250 seconds | 07-06 10:34 | 4 | max consumetps: 3.35 group max cpu: 69.8*% | no exception |
| Distribute 1000 messages to 7 topics in 200 seconds | 07-06 10:52 | 5 | max consumetps: 3.28 group max cpu: 72.5% | no exception |
| Distribute 1000 messages to 7 topics in 166 seconds | 07-07 09:06 | 6 | max consumetps: 2.98 group max cpu: 90.8% | db timeout, db connection limit reached |
| ** ****1 trade and 6 cashflows**** ** | Distribute 1000 messages to 7 topics in 100 seconds | 07-06 09:35 | 10 | max consume tps: 3.33 group max cpu: 72.9% | no exception |
| Distribute 1000 messages to 7 topics in 83 seconds | 07-06 09:43 | 12 | max consume tps: 3.08 group max cpu: 74.8% | no exception |
| Distribute 1000 messages to 7 topics in 72 seconds | 07-14 13:11 | 14 | max consume tps: 3.23 group max cpu: 81.1% | db timeout, db connection limit reached |
| Distribute 1000 messages to 7 topics in 63 seconds | 07-13 13:19 | 16 | | db timeout, db connection limit reached |

**fmrp2:  Instance count：3, partition：12（9 concurrencies） ， concurrent： 3 ；  **

**Staging:  Instance count：4, partition：12（12 concurrencies） ， concurrent： 3 ； **

| ** ** | ** Conditions** | **db pool** | **Scenario** | time（lag = 0） | Average cashflow count (total count / total second ) * 40 | Staging Statistics | result | remark | consumer Tps | group cpu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **6 partition**** ** | ** ****1 trade and 6 cashflows**** **** **** ** | **min 2, max 24** | Each topic contains about 1,000 messages, 7 topic | 07-20 19:57:05 ~ 20:08:00 total cost: 10m55s , 655s total count: 7000 | 64 | | It took a total of 10 minutes and 55 seconds to consume all the data, and no Exception | group max cpu: 87.4 lifecycle max cpu: 86.4 orchestration max cpu: 88.7 kafka consume tps: 3.37 | ![image-2026-7-20_21-2-59.png](attachments/image-2026-7-20_21-2-59.png) | ![image-2026-7-20_20-59-57.png](attachments/image-2026-7-20_20-59-57.png) |
| **min 2, max 56** | | | | | | | | |
| ** ****1 trade and 12 cashflows**** ** | **min 2, max 24** | Each topic contains about 1000 messages, 7 topic | 07-20 20:32:21 ~ 20:46:36 total cost: 14m 15s, 855s; total count: 7000 | 98.2 | | It took a total of 14 minutes and 15 seconds to consume all the data, and no Exception | group max cpu: 86.9 lifecycle max cpu: 89.4 orchestration max cpu: 86.8 kafka consume tps: 1.62 | ![image-2026-7-20_21-4-12.png](attachments/image-2026-7-20_21-4-12.png) | ![image-2026-7-20_21-4-45.png](attachments/image-2026-7-20_21-4-45.png) |
| **min 2, max 56** | | | | | | | | |
| **1 trade and 40 cashflows ** ** ** | **min 2, max 24** | Each topic contains about 1000 messages, 7 topic | 07-20 21:06:10 ~ 21:51:00 total cost: 44m 50s, 2690s total count: 9379 (include retries) | 139.4 | | It took a total of 44 minutes and 50 seconds to consume all the data, and no Exception | group max cpu: 87.6 lifecycle max cpu: 87.5 orchestration max cpu: 87.8 kafka consume tps: 1.78 | ![image-2026-7-21_10-50-14.png](attachments/image-2026-7-21_10-50-14.png) | ![image-2026-7-21_9-21-24.png](attachments/image-2026-7-21_9-21-24.png) |
| **min 2, max 56** | | | | | | | | |
| **12 partition**** ** | ** 1 trade and 6 cashflows** ** ** | **min 2, max 24** | Each topic contains about 1,000 messages, 7 topic | 07-20 22:03:19 ~ 22:10:30 total cost: 7m 11s, 431s total count: 7000 | 97.4 | | It took a total of 7 minutes and 11 seconds to consume all the data, and no Exception | group max cpu: 84.4 lifecycle max cpu: 84.1 orchestration max cpu: 85.3 kafka consume tps: 1.56 | ![image-2026-7-21_11-22-6.png](attachments/image-2026-7-21_11-22-6.png) | ![image-2026-7-21_9-18-54.png](attachments/image-2026-7-21_9-18-54.png) |
| **min 2, max 56** | Each topic contains about 1,000 messages, 7 topic | 07-21 20:03:39 ~ 20:10:30 total cost: 6m 51s, 411s; total count: 7000 | 102 | | | group max cpu: 92.0 lifecycle max cpu: 91.5 orchestration max cpu: 87.3 kafka consume tps: 1.62 20:03:46 db pool init Uber message handling completed, total time cost: 8.401468207 after init 20:05:24 Uber message handling completed, total time cost: 2.980737971 | ![image-2026-7-21_20-39-3.png](attachments/image-2026-7-21_20-39-3.png) | ![image-2026-7-21_20-35-25.png](attachments/image-2026-7-21_20-35-25.png) |
| **1 trade and 12 cashflows** ** ** | **min 2, max 24** | Each topic contains about 1000 messages, 7 topic | 07-20 22:13:50 ~ 22:28:10 total cost: 14m 20s, 860 s total count: 7000 | 97.6 | | It took a total of 14 minutes and 20 seconds to consume all the data, and no Exception | group max cpu: 87.2 lifecycle max cpu: 87.1 orchestration max cpu: 87.6 kafka consume tps: 3.03 | ![image-2026-7-21_11-22-12.png](attachments/image-2026-7-21_11-22-12.png) | ![image-2026-7-21_9-17-54.png](attachments/image-2026-7-21_9-17-54.png) |
| **min 2, max 56** | Each topic contains about 1000 messages, 7 topic | 07-21 20:16:15 ~ 20:29:05 total cost: 12m 50s, 770s; total count: 7327 (include retries) | 114 | | | group max cpu: 84.0 lifecycle max cpu: 88.5 orchestration max cpu: 84.3 kafka consume tps: 1.79 Uber message handling completed, total time cost: 2.186551014 | ![image-2026-7-21_20-39-8.png](attachments/image-2026-7-21_20-39-8.png) | ![image-2026-7-21_20-40-14.png](attachments/image-2026-7-21_20-40-14.png) |
| **1 trade and 40 cashflows** ** ** | **min 2, max 24** | | | | | | | | |
| **min 2, max 56** | Each topic contains about 1000 messages, 7 topic | 07-21 20:41:52 ~ 21:19:37 total cost: 37m 45s, 2265s total count: 7000 | 123 | 153 SCBML: 137 [CN Trade Migration - Ratan Performance Testing - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/CN+Trade+Migration+-+Ratan+Performance+Testing) | | Uber message handling completed, total time cost: 16.186403032， | | |
| ** ** | ** ** | ** ** | | | | | | | | |

# **2，Test Scenario**

**env: fmrp2**

## **2.1，Distribute 100 messages to 7 topics in 20 seconds**

2026-07-06 09:10:11,202 [INFO] Total send seconds: 20.050
2026-07-06 09:10:11,202 [INFO] Total send TPS: 4.99
2026-07-06 09:10:11,202 [INFO] Done. generated=100 sent=100
2026-07-06 09:10:11,202 [INFO] Topic dispatch summary:
2026-07-06 09:10:11,202 [INFO]   tdsx_uber_message_json_inbound_fx_other -> 18
2026-07-06 09:10:11,202 [INFO]   tdsx_uber_message_json_inbound_fx_spot -> 13
2026-07-06 09:10:11,202 [INFO]   tdsx_uber_message_json_inbound_equity -> 11
2026-07-06 09:10:11,202 [INFO]   tdsx_uber_message_json_inbound_cash -> 13
2026-07-06 09:10:11,202 [INFO]   tdsx_uber_message_json_inbound_commodity -> 13
2026-07-06 09:10:11,202 [INFO]   tdsx_uber_message_json_inbound_interestrate -> 19
2026-07-06 09:10:11,202 [INFO]   tdsx_uber_message_json_inbound_loan -> 13

### 2.1.1 Performance

max tps: 2.52

max cpu: 68.0%

Due to a database anomaly, consumer performance could not be improved.

### 2.1.2 evidence

kafka tps:

![image-2026-7-7_10-15-42.png](attachments/image-2026-7-7_10-15-42.png)

group cpu:

![image-2026-7-7_10-17-24.png](attachments/image-2026-7-7_10-17-24.png)

orchestration cpu

![image-2026-7-7_10-19-14.png](attachments/image-2026-7-7_10-19-14.png)

lifecycle cpu:

**![image-2026-7-7_10-18-13.png](attachments/image-2026-7-7_10-18-13.png)**

### **2.1.3 result**

**Due to a database exception, the message entered the topic's retry queue.**

**Database connection timed out, connection limit reached.**

![image-2026-7-3_15-27-14.png](attachments/image-2026-7-3_15-27-14.png)

**2.2，Distribute 1000 messages to 7 topics in 166 seconds**

**tps: 2.98**

**![image-2026-7-7_10-40-16.png](attachments/image-2026-7-7_10-40-16.png)**

**group cpu:**

**![image-2026-7-7_10-38-25.png](attachments/image-2026-7-7_10-38-25.png)**

**orchestration cpu**

** lifecycle cpu:**

# **3，conclusion**