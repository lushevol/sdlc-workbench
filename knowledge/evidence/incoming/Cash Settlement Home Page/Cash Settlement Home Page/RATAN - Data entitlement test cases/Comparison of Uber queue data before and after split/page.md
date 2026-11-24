uat4:    Consuming Uber messages from the overall queue;

fmrp2: Consuming Uber messages from split queues;

**1，Comparison results**

Comparison process：Compare the number of Uber messages in the inbound tables of uat4 and fmrp2 within the same time period.

**1.1，Comparison time：2026-06-08 00:00:00 ~ 2026-06-11 00:00:00**

Comparison data volume： 3391

**Comparison result： Two data entries were found to be missing in the fmrp2 environment  (refer to 2.3)**

Miss correlation_id： 16a6f26acc4f17d39e9cf45454113ba0_7153422395，7a756a7f83018dda1316ec41bcc9c661_7153422382

**1.2，Comparison time：2026-06-11 00:00:00 ~ 2026-06-12 00:00:00**

Comparison data volume： 627

**Comparison result：Pass**

**1.3，Comparison time：2026-06-12 00:00:00 ~ 2026-06-15 00:00:00**

Comparison data volume： 2038

**Comparison result：Pass**

**1.4，Comparison time：2026-06-16 00:00:00 ~ 2026-06-17 00:00:00**

Comparison data volume： 3764

**Comparison result：No Pass，No retry mechanism upstream**

**Miss correlation_id: **

| 22a59e110bb15a5c30c7a97e045356b5_7156125050 |
| --- |
| 2e9ad0757070f98ab52f97fba001e947_7156125047 |
| 0be8ef0bae2e3450694c2a88a6d8104f_7156122430 |
| 7f6b7144d09c5d2a8be154c41f419dcb_7156116015 |

**
📎 [uat4_compareto_fmrp2-0617.xlsx](attachments/uat4_compareto_fmrp2-0617.xlsx)
**

**Reason: The nonprod solution is not very stable, and there are link issues with edmi.**

**![image-2026-6-18_11-9-38.png](attachments/image-2026-6-18_11-9-38.png)**

**1.5，Comparison time：2026-06-22 00:00:00 ~ 2026-06-25 00:00:00**

Comparison data volume： 3580

**Comparison result：No Pass**

**Miss correlation_id: uat4 lost 81 uber messages**

**
📎 [uat4_compareto_fmrp2-0624-0625.xlsx](attachments/uat4_compareto_fmrp2-0624-0625.xlsx)
**

**Reason:   UAT4 changes password, causing Uber message processing to fail **

**2，Problems discovered**

**2.1，Upstream lost messages of type "Simple Cash Flow"  --Resolved**

On April 21, Ratan discovered that the trade 7150248766 could receive messages in the queue: q-51358-ratanone-uber-msg, but the split queues did not receive messages.

Upon investigation, it was discovered that the primary asset class of this trade is Simple Cash Flow, but this asset class was overlooked during the analysis.

**2.2，Group service detects lost messages  --resolved**

**refer to: [Analyzing the issue of deleting Uber consumer data - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Analyzing+the+issue+of+deleting+Uber+consumer+data)**

**2.3，mb error occurs when publishing message (fmrp1 & fmrp2)  --Unresolved**

**refer to : [An MB error occurs when publishing a message, causing the message to be lost - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/An+MB+error+occurs+when+publishing+a+message%2C+causing+the+message+to+be+lost)**