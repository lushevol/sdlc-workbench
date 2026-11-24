Background

Previously, all Uber messages were sent to a single solution queue. The goal is to change this by splitting the queue into eight queues based on the "primary asset class".

[refer to: Performance Improvement - BAU- TDSX Partitioning Key and Uber Topic Splitting - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Performance+Improvement+-+BAU-+TDSX+Partitioning+Key+and+Uber+Topic+Splitting)

test env： fmrp1, fmrp2

MB: receive uber message

| queue | tradeId | traceId | log | comment |
| --- | --- | --- | --- | --- |
| q-51358-ratanone-fmrptdsx-uber-fx-spot-msg | 7156032226 | 30d58a62f074483641974ef495ec3590 | ![image-2026-6-11_11-19-38.png](attachments/image-2026-6-11_11-19-38.png) | fmrp2 |
| q-51358-ratanone-fmrptdsx-uber-fx-other-msg | 7156032307 | 22e86788b597844a01a7e28cbce0d2e8 | ![image-2026-6-11_11-20-46.png](attachments/image-2026-6-11_11-20-46.png) | fmrp2 |
| q-51358-ratanone-fmrptdsx-uber-cash-msg | 7156032174 | ea8cc8df89731186e2b4834dbafee288 | ![image-2026-6-11_11-21-46.png](attachments/image-2026-6-11_11-21-46.png) | fmrp2 |
| q-51358-ratanone-fmrptdsx-uber-com-msg | 7156032136 | c574419c67a58ec86fb9aaa1c4584b22 | ![image-2026-6-11_11-22-46.png](attachments/image-2026-6-11_11-22-46.png) | fmrp2 |
| q-51358-ratanone-fmrptdsx-uber-interestrate-msg | 7156032295 | 5f9cdfaeea0d0bd613885559718a4602 | ![image-2026-6-11_11-23-43.png](attachments/image-2026-6-11_11-23-43.png) | fmrp2 |
| q-51358-ratanone-fmrptdsx-uber-equity-msg | 8012741767 | 31c9e43e1aba3e9a3ff5750a6782e333 | ![image-2026-6-11_11-26-45.png](attachments/image-2026-6-11_11-26-45.png) | fmrp1 |
| q-51358-ratanone-fmrptdsx-uber-loan-msg | | | | fmrp2 |
| q-51358-ratanone-fmrptdsx-uber-credit-msg | 7156011045 | 287a049ccc76297e13502f7978e32826 | ![image-2026-6-11_11-25-8.png](attachments/image-2026-6-11_11-25-8.png) | fmrp2 |
| | | | | |
| | | | | |

MB： filter uber message

When one source corresponds to two targets, the filter test results are as follows.

Case 1:

target 1: fx_other: Source_Stack_Flow_Name in FMRP~FMRPSTELLA

tradeId: 7159338329

Stack name: FMRPSTELLA

result : pass

Because the stack name meets the filter rules, the message enters the fx_other topic.

![image-2026-7-21_16-38-51.png](attachments/image-2026-7-21_16-38-51.png)

target 2: fx_other_egnpsa: Booking_Entity_SCI_FMID in 400007847~401036553~400991880

tradeId: 7159338329

fmid:  400452428

result : pass

Because fmid didn't meets the filter rules, the message did't enters the fx_other_egnpsa topic.

![image-2026-7-21_16-41-35.png](attachments/image-2026-7-21_16-41-35.png)

![image-2026-7-21_17-33-25.png](attachments/image-2026-7-21_17-33-25.png)

Case 2:

target 1: fx_other: Source_Stack_Flow_Name in FMRP~FMRPSTELLA

tradeId: 7159413392

Stack name: FMRPSTELLA

result : pass

the stack name meets the filter rules, the message enters the fx_other topic.

![image-2026-7-22_14-17-23.png](attachments/image-2026-7-22_14-17-23.png)

target 2: fx_other_egnpsa: Booking_Entity_SCI_FMID in 400007847~401036553~400991880~10075222

tradeId:7159413392

fmid:  10075222

result : pass

the fmid meets the filter rules, the message enters the fx_other topic.

![image-2026-7-22_14-19-12.png](attachments/image-2026-7-22_14-19-12.png)