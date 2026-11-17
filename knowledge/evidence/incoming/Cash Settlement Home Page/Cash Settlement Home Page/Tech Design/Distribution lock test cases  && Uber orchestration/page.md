# Technical Flow

7K Netting comparison

| Version | Old Lock (staging 4 server) | New Lock (uat4 1 server) | |
| --- | --- | --- | --- |
| Get Lock time | 22 seconds From Sep 26, 2025 @ 16:00:41.081 to Sep 26, 2025 @ 16:01:02.134 | 279 milli seconds From 2025-09-29 10:08:25.484 to 2025-09-29 10:08:25.663 | ![image-2025-9-26_17-15-15.png](attachments/image-2025-9-26_17-15-15.png) ![image-2025-9-26_17-16-12.png](attachments/image-2025-9-26_17-16-12.png) |
| Query cashflows | From Sep 26, 2025 @ 16:00:19.388 to Sep 26, 2025 @ 16:00:40.832 total cost: 21 seconds | From: 2025-09-29 10:08:13.767 to 2025-09-29 10:08:25.367 total cost: 12 second | |
| | | | |
| | | | |
| Release lock | 12 seconds from : Sep 26, 2025 @ 16:03:35.618 to: Sep 26, 2025 @ 16:03:47.909 | 85 milli seconds from: 2025-09-29 10:09:52.988 to: 2025-09-29 10:09:53.073 | ![image-2025-9-29_18-12-33.png](attachments/image-2025-9-29_18-12-33.png) |
| Total | ![image-2025-9-26_16-53-9.png](attachments/image-2025-9-26_16-53-9.png) | ![image-2025-9-26_16-53-30.png](attachments/image-2025-9-26_16-53-30.png) | |

# New Lock usage Guideline

New distribution lock commit to   foundation service -  feature/new-lock-for-domain-service

1. Build foundation with the feature branch
2. Any domain service want to use the new distribution lock, then import the foundation version you just build
3. Ensure you springboot version upgrade to 3.4.4

<parent>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-parent</artifactId>
<version>3.4.4</version>
<relativePath /> <!-- lookup parent from repository -->
</parent>

The new distribute lock usage is the same with before, the only diff is the second parameter

in old version,  second parameter is locking time.  In new version, the second parameter is  retry time.  Locking time is extended by Redisson watch dog

Single key:

resourceLockManager.get(cashflowId, 30, "serviceA",
() -> {
           somemethod .......
});

Bulk key:

resourceLockManager.get(batchList, 30, "serviceB",
() -> {
somemethod .......
return "Success";
});

# **Distribute lock Test cases**

| Case | Service-A | Service-B |
| --- | --- | --- |
| Single-Single exclusiveness | t1 - 2025-06-27T16:01:36.053 ------------Start to lock key [M1000] t2 - 2025-06-27T16:01:36.642 : ------------Key [M1000] have been locked t5 - 2025-06-27T16:01:47.959 : ------------mxgadaptor released key M1000 t6 - 2025-06-27T16:01:47.717: ------------is lock owner and mxgadaptor start to release key M1000 | t3 - 2025-06-27T16:01:37.438 : ------------Start to lock key [M1000] t4 - 2025-06-27T16:01:37.642 : ------------Locked by others, subscribing key: M1000{100} t7 - 2025-06-27T16:01:48.224 : ------------Key [M1000] have been locked t8 - 2025-06-27T16:01:49.504 : ------------lifecycle released key M1000 |
| Lock reentrance | t1 - 2025-06-27T17:07:10.893: Start to lock key [M1000] t2 - 2025-06-27T17:07:11.129: Key [M1000] have been locked t6 - 2025-06-27T17:07:18.109 : mxgadaptor released key M1000 | t3 - 2025-06-27T17:07:11.627 : Receive request t4 - 2025-06-27T17:07:11.862 : Lock process id is existing, bypass locking for key: M1000 t5 - 2025-06-27T17:07:16.870 : Execution over start to output result |
| Watchdog (mock 60 seconds) | t1 - 2025-06-27T17:19:58.155: Start to lock [M1001, M1002, M1003, M1004, M1005, M1006, M1007, M1008, M1009... . . after 10 seconds t2 - 2025-06-27T17:20:19.105 : Watchdog start to renew expiretime t3 - 2025-06-27T17:20:29.896 : Watchdog start to renew expiretime t4 - 2025-06-27T17:20:40.862: Watchdog start to renew expiretime ![](https://confluence.global.standardchartered.com/download/attachments/3301076122/image-2025-6-25_11-50-42.png?version=1&modificationDate=1750823442000&api=v2) . t5 - 2025-06-27T17:20:58.164+08:00 : mxgadaptor start to release batch lock | |
| Single-Multi exclusiveness | Single key: t1 - 2025-06-30T15:27:11.575: Start to lock key [M1050] t4 - 2025-06-30T15:27:23.098: : is lock owner and lifecycle start to release key M1050 t5 - 2025-06-30T15:27:23.357: lifecycle released key M1050 | Multi keys t2 - 2025-06-30T15:27:13.278: Start to lock [M1001, M1002, M1003, M1004, M1005, M1006, M1007, M1008, M1009.... t3 - 2025-06-30T15:27:14.080 >>>lock by others, start to subscribe lock id:M1050{100} receive release notificaiton ![](https://confluence.global.standardchartered.com/download/attachments/3301076122/image-2025-6-25_13-54-56.png?version=1&modificationDate=1750830896000&api=v2) t6 - 2025-06-30T15:27:23.836+08:00 : [M1001, M1002, M1003, M1004, M1005, M1006, M1007, .....] locked and start to execute command t7 - 2025-06-30T15:27:33.845: mxgadaptor start to release batch lock |
| Multi-Single exclusiveness | Single key t3 - 2025-06-30T15:36:22.424: Start to lock key [M1050] t4 - 2025-06-30T15:36:22.676: locked by others, subscribing key: M1050{100} receive release notification ![](https://confluence.global.standardchartered.com/download/attachments/3301076122/image-2025-6-25_13-54-56.png?version=1&modificationDate=1750830896000&api=v2) t6 - 2025-06-30T15:36:32.605: Key [M1050] have been locked by lifecycle t7 - 2025-06-30T15:36:33.616: lock owner and lifecycle start to release key M1050 t8 - 2025-06-30T15:36:33.874: lifecycle released key M1050 | Multi keys t1 - 2025-06-30T15:36:20.678: Start to lock [M1001, M1002, M1003, M1004, M1005, M1006, M1007.... t2 - 2025-06-30T15:36:21.232: [M1001, M1002, M1003, M1004, M1005, M1006, M1007.....locked and start to execute command t5: 2025-06-30T15:36:31.234: mxgadaptor start to release batch lock |
| Bulk lock 5K | Performance 1. Start to Lock 2025-07-01T15:56:36.448 2. Locked 2025-07-01T15:56:39.705 **cost: 3 seconds** 1. Watchdog renew first time renew: 2025-07-01 15:56:39.570 2. Watchdog renew second time renew: 2025-07-01 15:56:53.590 3. Watchdog renew third time renew: 2025-07-01 15:57:07.621 4. Watchdog renew fourth time renew: 2025-07-01 15:57:18.835 5. Watchdog renew fifth time renew: 2025-07-01 15:57:29.420 6. Watchdog renew fifth time renew: 2025-07-01 15:57:43.472 1-2 4 second 2-3 4 second 3-4 1 second 4-5 1 second 5-6 4 second **cost: <=4 second** | |
| Lock transfer level control | Case 1: Lock transfer level control ![image-2025-7-3_17-48-33.png](attachments/image-2025-7-3_17-48-33.png) Service A t1 - 2025-07-03T17:51:07.664: Start to lock key [M1050] t2 - 2025-07-03T17:51:07.689: call lifecycle service t10 - 2025-07-03T17:51:14.296: prepare to release key M1050 holdCount:0 t11 - 2025-07-03T17:51:190: adaptor released key M1050 | Service B Service C t3 - 2025-07-03T17:51:09.224 Receive request>> t4 - 2025-07-03T17:51:09.226: Start to lock key [M1050] t5 - 2025-07-03T17:51:09.840: Start to call batch service t6 - 2025-07-03T17:51:10.268: Receive Request t7 - 2025-07-03T17:51:10.775: Lock can not be locked exceed 2 level t8 - 2025-07-03T17:51:12.915 :lifecycle prelease key M1050 holdCount:1 t9 - 2025-07-03T17:51:13.541: lifecycle released key M1050 |
| Lock concurrent conrole | Case: ![image-2025-7-3_18-29-18.png](attachments/image-2025-7-3_18-29-18.png) | |

# 10K  netting test

## Old on staging:

Mock 10k in staging  start with  RD335

![image-2026-3-6_13-49-51.png](attachments/image-2026-3-6_13-49-51.png)

show all cashflows and do netting

![image-2026-3-6_13-56-18.png](attachments/image-2026-3-6_13-56-18.png)

Previw take time   4.6min

![image-2026-3-6_14-38-28.png](attachments/image-2026-3-6_14-38-28.png)

netting take time 6min

![image-2026-3-6_14-52-30.png](attachments/image-2026-3-6_14-52-30.png)

## FRMP1  netting 10K

show all cashflow

![image-2026-3-6_17-11-37.png](attachments/image-2026-3-6_17-11-37.png)

preview   4.6m

![image-2026-3-6_17-14-49.png](attachments/image-2026-3-6_17-14-49.png)

netting take  3.4m

![image-2026-3-9_10-42-16.png](attachments/image-2026-3-9_10-42-16.png)

## New on staging  10K

search all cashflows

![image-2026-3-9_17-45-41.png](attachments/image-2026-3-9_17-45-41.png)

preview take  55s

![image-2026-3-9_17-46-21.png](attachments/image-2026-3-9_17-46-21.png)

netting take  3.2m

![image-2026-3-9_17-50-49.png](attachments/image-2026-3-9_17-50-49.png)