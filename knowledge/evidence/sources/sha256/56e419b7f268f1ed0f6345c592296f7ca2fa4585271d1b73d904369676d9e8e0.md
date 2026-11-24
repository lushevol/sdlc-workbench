# 1, overall

env: staging

vpn: FMEDMI2_GDCW_PT

Overall data:

| condition | message size | queue type | queue name | Consumption start time | Consumption End time | Total consumption | Total consumption time（sec） | Consumption avg rate(msg/sec) | consumer tps(msg/sec) | publisher tps(msg/sec) | comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| memory: 1G | 25KB | normal queue | q-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-05-13 17:59:00 | 2026-05-13 22:29:06 | 432012 | 16206 | 26.7 | 39 | 30 | |
| q-51358-ratanone-fmrptdsx-uber-com-msg | 2026-05-13 17:59:00 | 2026-05-13 21:33:13 | 213766 | 12853 | 16.6 | 23 | 30 | |
| q-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-04 10:38:39 | 2026-09-04 11:01:34 | 36000 | 1375 =22m 55s | 26.2 | 32 | 60 Hold for 10 minutes | |
| partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-03 16:03:16 | 2026-09-03 17:03:16 | 429970 | 3600 =60m | 119.4 | 133 | 120 Hold for 60 minutes | |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-03 16:03:16 | 2026-09-03 17:03:27 | 430350 | 3611 =60m 11s | 119.2 | 126 | 120 Hold for 60 minutes | |
| partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-03 19:15:11 | 2026-09-03 19:28:34 | 95520 | 600+180+23=803 =13m 23s | 118.9 | 187 | 160 Hold for 10 minutes | |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-03 19:15:11 | 2026-09-03 19:28:55 | 100438 | 600+180+44=824 =13m 44s | 121.7 | 194 | 160 Hold for 10 minutes | |
| partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-03 20:35:20 | 2026-09-03 20:45:41 | 78680 | 621 =10m 21s | 126.7 | 154 | 140 Hold for 10 minutes | |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-03 20:35:20 | 2026-09-03 20:45:29 | 76516 | 609 =10m 9s | 125.6 | 148 | 140 Hold for 10 minutes | |
| partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-04 13:08:17 | 2026-09-04 13:18:18 | 81000 | 600 =10m | 135 | 149 | 135 Hold for 10 minutes | |
| memory: 2G | 25K | partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-04 14:42:05 | 2026-09-04 14:52:28 | 74250 | 623 =6m 23s | 119.2 | 177 | 150 Hold for 10 minutes | |
| 2026-09-04 16:06:31 | 2026-09-04 16:19:38 | 84600 | 783 =13m 7s | 108 | 158 | 145 Hold for 10 minutes | |
| 2026-09-09 09:04:18 | 2026-09-09 09:07:17 | 65354 | 179 = 2 m 59s | 365 | 443 | 120 Hold for 10 minutes | stop mb Code optimization |
| normal queue | q-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-09 09:12:00 | 2026-09-09 09:30:59 | 72000 | 1079 =17 m 59s | 66.7 | 84 | 120 Hold for 10 minutes | stop mb Code optimization |
| 25KB | partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-21 11:13:52 | 2026-09-21 11:19:42 | 72,000 | 350 s 5 m 50 s | 205 | | | stop mb， Send/receive messages at same time |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-21 11:13:52 | 2026-09-21 11:19:43 | | 351 s 5 m 51 s | 205 | | |
| partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-21 09:51:17 | 2026-09-21 09:54:32 | 66,752 | 195 s | 342 | | | stop mb， Pass-through protobuf， Send/receive messages at same time |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-21 09:51:17 | 2026-09-21 09:54:32 | 66,781 | 195 s | 342 | | |

| condition | message size | queue type | queue name | start time | end time | total count | total time(sec) | Consumption avg rate(msg/sec) | consumer tps(msg/sec) | publisher tps(msg/sec) | comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| memory: 1G | 349KB | partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-03 20:00:40 | 2026-09-03 20:10:41 | 19440 | 600 =10m | 32.4 | 39 | 120 Hold for 10 minutes | |
| pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-03 20:20:41 | 2026-09-03 20:30:53 | 22400 | 612 =10m 12s | 36.6 | 53 | 140 Hold for 10 minutes | |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-03 20:55:37 | 2026-09-03 21:05:38 | 18240 | 600 =10m | 30.4 | 40 | 40 Hold for 10 minutes | 40*600*349K =7.98G |
| 157KB（avg） 620KB（max） 151KB（median） | normal queue | q-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-14 16:00:00 prod | 2026-09-14 20:00:00 | 75965 | 14400 =240m =4h | 5 | 20 | | |
| memory: 2G | 349KB | partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-04 13:54:58 | 2026-09-04 14:04:48 | 27717 | 590 =9m 50s | 46.9 | 59 | 120 Hold for 10 minutes | stop mb 120*600*349K =23.96G |
| 2026-09-09 08:46:18 | 2026-09-09 08:47:44 | 19200 | 86 =1m 26s | 223 | 298 | 120 Hold for 10 minutes | stop mb Code optimization |
| 2026-09-15 19:38:49 | 2026-09-15 19:39:41 | 19080 | 52 s | 366 | 398 | 120 Hold for 10 minutes | stop mb Pass-through protobuf |
| normal queue | q-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-09 08:29:17 | 2026-09-09 08:37:52 | 19200 | 515 =8m 35s | 37.3 | 40 | 120 Hold for 10 minutes | stop mb Code optimization |
| partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-21 10:40:39 | 2026-09-21 10:44:08 | 10,220 | 209 s 3 m 29 s | 48.9 | | | stop mb， Send/receive messages at same time |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-21 10:40:39 | 2026-09-21 10:44:21 | 10,211 | 222 3 m 42 s | 46 | | |
| partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-21 10:17:11 | 2026-09-21 10:17:56 | 10,080 | 44 s | 229 | | | stop mb， Pass-through protobuf， Send/receive messages at same time |
| pq-51358-ratanone-fmrptdsx-uber-com-msg | 2026-09-21 10:17:11 | 2026-09-21 10:17:54 | 10,200 | 43 s | 237 | | |
| memory: -Xms2G -Xmx4G | 349KB | partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-07 17:53:13 | 2026-09-07 18:03:14 | 19200 | 600 =10m | 32 | 35 | 120 Hold for 10 minutes | |
| 2026-09-07 18:22:31 | 2026-09-07 18:28:00 | 13329 | 329 = 5 m 29 s | 40.5 | 59 | 120 | stop mb |
| memory: -Xms4G -Xmx4G | 349KB | partition queue | pq-51358-ratanone-fmrptdsx-uber-interestrate-msg | 2026-09-07 19:40:25 | 2026-09-07 19:42:48 | 7163 | 143 =2 m 23 | 50 | 61 | 120 | stop mb |

# 2, System Information (jvm 1G)

CPU

![image-2026-9-4_9-11-6.png](attachments/image-2026-9-4_9-11-6.png)

Memory（jvm: 1G）

![image-2026-9-4_9-11-52.png](attachments/image-2026-9-4_9-11-52.png)

GC Count

![image-2026-9-4_9-12-37.png](attachments/image-2026-9-4_9-12-37.png)

# 3, System info （jvm: 2G）

CPU

![image-2026-9-4_15-0-2.png](attachments/image-2026-9-4_15-0-2.png)

Memory（jvm: 2G）

![image-2026-9-4_15-0-53.png](attachments/image-2026-9-4_15-0-53.png)

GC count

![image-2026-9-4_15-1-36.png](attachments/image-2026-9-4_15-1-36.png)

2026-09-15 19：00~20：00

cpu

![image-2026-9-16_16-44-48.png](attachments/image-2026-9-16_16-44-48.png)

memory

![image-2026-9-16_16-43-39.png](attachments/image-2026-9-16_16-43-39.png)

gc count

![image-2026-9-16_16-42-59.png](attachments/image-2026-9-16_16-42-59.png)

# 4, Prod System info

2026-08-14  16:00 ~ 20:00

Message received （IMS: [View panel - IMS Dashboard latest - TOOLS - Dashboards - Grafana](https://sabre-prod-cloud-global.gdc.standardchartered.com/grafana/d/a893ad95-eaf3-4c16-a5af-2b99b1b1e46c/ims-dashboard-latest?from=1786694400000&to=1786709579000&orgId=1&var-Sender=All&var-Receiver=RATAN&var-OLA=TDSX_RATAN_TECH_UBER_INTERESTRATE&var-lag=1d&viewPanel=1)）

![image-2026-9-4_15-46-52.png](attachments/image-2026-9-4_15-46-52.png)

3400 messages consumed in 10 minutes， avg rata: 5.6 msg/sec

Latency（central monitor: [View panel - RATAN PSS Customization Dashboard - Ratan Central Monitoring - Business Level - Dashboards - Grafana](https://uklvapapp591.gdc.standardchartered.com:3000/d/cfcswyfscaakgc/ratan-pss-customization-dashboard?from=2026-08-14T08:00:00.000Z&to=2026-08-14T12:10:59.000Z&timezone=utc&viewPanel=panel-7)）

![image-2026-9-4_9-18-13.png](attachments/image-2026-9-4_9-18-13.png)

Message size distribution

![image-2026-9-4_15-4-6.png](attachments/image-2026-9-4_15-4-6.png)

![image-2026-9-4_15-8-4.png](attachments/image-2026-9-4_15-8-4.png)

Solace ingress and egress rata:

![image-2026-9-4_16-30-16.png](attachments/image-2026-9-4_16-30-16.png)