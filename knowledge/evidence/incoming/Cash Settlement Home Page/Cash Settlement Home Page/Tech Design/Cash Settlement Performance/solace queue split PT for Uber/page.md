# 1, overall

env: staging

vpn: FMEDMI2_GDCW_PT

Overall data:

| queue name | start time | end time | total messages | total time(sec) | average rate(msg/sec) | TPS(msg/sec) |
| --- | --- | --- | --- | --- | --- | --- |
| total | 2026-05-13 17:59 PM | 2026-05-13 22:30 PM | 696547 | 16260 | 42.8 | |
| fx-other-msg | 2026-05-13 17:59:00 | 2026-05-13 18:42:48 | 31842 | 2628 | 12.1 | 23 |
| fx-spot-msg | 2026-05-13 17:59:00 | 2026-05-13 18:06:14 | 1624 | 434 | 3.7 | 17 |
| equity-msg | 2026-05-13 17:59:00 | 2026-05-13 18:03:51 | 306 | 291 | 1 | 13 |
| cash-msg | 2026-05-13 17:59:00 | 2026-05-13 18:23:45 | 13822 | 1485 | 9.3 | 19 |
| com-msg | 2026-05-13 17:59:00 | 2026-05-13 21:33:13 | 213766 | 12853 | 16.6 | 23 |
| interestrate-msg | 2026-05-13 17:59:00 | 2026-05-13 22:29:06 | 432012 | 16206 | 26.7 | 39 |
| loan-msg | 2026-05-13 17:59:00 | 2026-05-13 18:05:17 | 3173 | 377 | 8.4 | 53 |
| credit-msg | 2026-05-13 17:59:00 | 2026-05-13 17:59:04 | 2 | 4 | 0.5 | 1 |

anil's reply：

Intrestrates & comodity queues

![image-2026-5-18_10-8-16.png](attachments/image-2026-5-18_10-8-16.png)

![image-2026-6-4_15-7-21.png](attachments/image-2026-6-4_15-7-21.png)

![image-2026-6-4_15-7-43.png](attachments/image-2026-6-4_15-7-43.png)

# 2, log monitor

uber total :

![image-2026-5-14_9-30-4.png](attachments/image-2026-5-14_9-30-4.png)

fx-other :

![image-2026-5-14_9-32-34.png](attachments/image-2026-5-14_9-32-34.png)

fx-spot :

![image-2026-5-14_9-33-11.png](attachments/image-2026-5-14_9-33-11.png)

equity-msg:

![image-2026-5-14_9-34-34.png](attachments/image-2026-5-14_9-34-34.png)

cash-msg:

![image-2026-5-14_9-35-5.png](attachments/image-2026-5-14_9-35-5.png)

com-msg:

![image-2026-5-14_9-36-1.png](attachments/image-2026-5-14_9-36-1.png)

interestrate-msg:

![image-2026-5-14_9-37-15.png](attachments/image-2026-5-14_9-37-15.png)

loan-msg total:

![image-2026-5-14_9-38-44.png](attachments/image-2026-5-14_9-38-44.png)

credit-msg total:

![image-2026-5-14_9-40-3.png](attachments/image-2026-5-14_9-40-3.png)

# 3 kafka monitor

tdsx_uber_message_json_inbound

![image-2026-5-18_11-47-13.png](attachments/image-2026-5-18_11-47-13.png)

# 4, backend service monitor

mb:

group:

**![image-2026-5-19_9-53-8.png](attachments/image-2026-5-19_9-53-8.png)**

![image-2026-5-19_10-38-36.png](attachments/image-2026-5-19_10-38-36.png)

**orchestration**

**![image-2026-5-19_9-56-43.png](attachments/image-2026-5-19_9-56-43.png)**