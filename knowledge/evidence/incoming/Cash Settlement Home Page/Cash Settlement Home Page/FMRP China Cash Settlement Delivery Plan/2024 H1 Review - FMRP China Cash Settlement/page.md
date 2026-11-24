# Key Deliveries

The strategic settlement platform successfully business go live by 13 Nov, which is a big victory!

| | Features |
| --- | --- |
| 1 | SWIFT Processing |
| 2 | Accounting Processing |
| 3 | CCIL Netting |
| 4 | Bulk Submit / Bulk Approve in Cashflow Blotter |
| 5 | Payment amount rounding |
| 6 | NFR - Performance Enhancement |
| 7 | |

# BAU - STP rate increase

![image2024-5-23_13-19-40.png](attachments/image2024-5-23_13-19-40.png)

# NFR - PT enhancement

Please see the latest PT result (page is in progress) as below, testing scope was 180 K + payments samples from trade migration:

| **Status** | **Count** | **Total Cost** | **Start Time** | **End Time** | **CPU occupation** | **Throughout (per hour)** |
| --- | --- | --- | --- | --- | --- | --- |
| Projected | 142,551 | 1.5 hours | 2024-05-02 15:05:48 | 2024-05-02 16:38:58 | Up to 55% | 121,403 |
| Suspended | 39,554 |

Detailed level categories, which means Ratan is able to process max daily (8 hours): 142,551 * 8 / 1.5= 760,272 payments.

| **Category** | **Count** | **Maximum (s)** | **Minimal (s)** | **Average (s)** | **Total cost (m)** |
| --- | --- | --- | --- | --- | --- |
| Overall | 142,551 | 11.2 | 0.2 | 0.9 | 90 mins |
| Inbound only (>VD+5) | 121,413 | 2.0 | 0.2 | 0.5 | 54 mins |
| End to End (<VD+5) | 21,138 | 11.2 | 0.3 | 3 | 36 mins |
| Current PT | 9,288 | 45 | 5 | 16 | 256 mins |

Processing details for End to End (21,138):

| **Cost** | **Count** | **Percentage** |
| --- | --- | --- |
| < 4s | 19,418 | 88.35% |
| 4 – 6 s | 2,354 | 10.71% |
| 6 - 8 s | 170 | 0.77% |
| 8 – 12 s | 37 | 0.17% |