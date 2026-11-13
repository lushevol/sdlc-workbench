# 1. user-e2e-test-case

| case | Test | Result Report Link | Over Time Charts | Statistics | Errors |
| --- | --- | --- | --- | --- | --- |
| <u>*user-e2e-test-case*</u> | 1X 2026-03-18 20:25:00 ~ 2026-03-18 21:25:04 | [Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1773836704621/report/index.html) | ![image-2026-3-25_10-15-48.png](attachments/image-2026-3-25_10-15-48.png) | ![image-2026-3-25_10-16-29.png](attachments/image-2026-3-25_10-16-29.png) | ![image-2026-3-25_10-16-46.png](attachments/image-2026-3-25_10-16-46.png) |
| 2X 2026-03-19 07:40:00 ~ 2026-03-19 08:40:00 | [Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1773877202808/report/index.html) | ![image-2026-3-25_10-22-18.png](attachments/image-2026-3-25_10-22-18.png) | ![image-2026-3-25_10-23-6.png](attachments/image-2026-3-25_10-23-6.png) | ![image-2026-3-25_10-23-28.png](attachments/image-2026-3-25_10-23-28.png) |
| 4X 2026-03-19 19:00:00 ~ 2026-03-19 20:00:00 | [Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1773918048233/report/index.html) | ![image-2026-3-25_10-27-26.png](attachments/image-2026-3-25_10-27-26.png) | ![image-2026-3-25_10-27-56.png](attachments/image-2026-3-25_10-27-56.png) | ![image-2026-3-25_10-28-14.png](attachments/image-2026-3-25_10-28-14.png) |
| 6X 2026-03-19 23:15:00 ~ 2026-03-20 00:15:00 | [Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1773933306911/report/index.html) | ![image-2026-3-25_10-29-11.png](attachments/image-2026-3-25_10-29-11.png) | ![image-2026-3-25_10-29-49.png](attachments/image-2026-3-25_10-29-49.png) | ![image-2026-3-25_10-30-14.png](attachments/image-2026-3-25_10-30-14.png) |
| 8h 2026-03-18 21:50:00 ~ 2026-03-19 05:50:00 | [Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1773841844384/report/index.html) | ![image-2026-3-25_10-30-53.png](attachments/image-2026-3-25_10-30-53.png) | ![image-2026-3-25_10-31-21.png](attachments/image-2026-3-25_10-31-21.png) | ![image-2026-3-25_10-31-43.png](attachments/image-2026-3-25_10-31-43.png) |

# 2. sett

| case | pt traffic volume | case traffic volume | start time | end time | processing duration | Average Latency | SQL Scripts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| *<u>[sett](https://confluence.global.standardchartered.com/display/DSP/sett-murex)</u>** ** ** * | 1X | 21000 messages (topic = Settlement_Performance_Test_Out_Murex_CN) | 2026-03-18 20:25:00 SGT | 2026-03-18 21:25:00 SGT | 1 hr | 3.2s | [Settlement latency calculation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Settlement+latency+calculation) |
| 2X | 21000*2 messages (topic = Settlement_Performance_Test_Out_Murex_CN) | 2026-03-19 07:40:00 SGT | 2026-03-19 08:40:00 SGT | 1 hr | 3.8s | |
| 4X | 21000*4 messages (topic = Settlement_Performance_Test_Out_Murex_CN) | 2026-03-19 19:00:00 SGT | 2026-03-19 20:00:00 SGT | 2hr 14 mins | 3.91s | |
| 6X | 21000*6 messages (topic = Settlement_Performance_Test_Out_Murex_CN) | 2026-03-19 23:15:00 SGT | 2026-03-20 00:15:00 SGT | 3hr 01 mins | 4.01s | |
| 8H | 21000messages (topic = Settlement_Performance_Test_Out_Murex_CN) | 2026-03-18 21:50:00 SGT | 2026-03-19 05:50:00 SGT | 8 hrs | same as 1X | |

# 3. trade

| case | pt traffic volume | case traffic volume | start time | end time | processing duration | Average Latency | SQL Scripts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <u>*[trade](https://confluence.global.standardchartered.com/display/DSP/trade-murex)*</u> * ** ** * | 1X | 28000 messages | 2026-03-18 20:25:00 SGT | 2026-03-18 21:25:00 SGT | 1hr | *0.71s * | *<u>[Trade latency calculation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Trade+latency+calculation)</u>* |
| 2X | 28000*2 messages | 2026-03-19 07:40:00 SGT | 2026-03-19 08:40:00 SGT | 1hr | 2.93s |
| 4X | 28000*4 messages | 2026-03-19 19:00:00 SGT | 2026-03-19 20:00:00 SGT | 3hr1mins | 24 mins 55s |
| 6X | 28000*6 messages | 2026-03-19 23:15:00 SGT | 2026-03-20 00:15:00 SGT | 3hr50mins | 42mins 55s |
| 8h | 28000 messages | 2026-03-18 21:50:00 SGT | 2026-03-19 05:50:00 SGT | 8hr01mins | 0.88s |