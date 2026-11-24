**EXPAND: 1: Metric Collection**

In order to make a reasonable assessment on this performance testing, during testing we need to collect the necessary metric as the testing evidence. According to *[Ratan Performance Testing Guideline v.24](https://confluence.global.standardchartered.com/display/DSP/Ratan+Performance+Testing+Guideline),  *we know that the best practice is to collect the "**Four Golden Signals" **metric data, for this part we can collect them from **Ratan Central Monitoring System** directly. But for other** statistical data** like how much time spend on a certain volume business data processing for each case, they are not able to be collected from central monitoring system directly since they are a not a pure metric but a statistical data. for such important statistical data we can calculate them out by **SQL scripts **or **log data **parsing when each case testing round completed.

We organized all necessary testing data and snapshot here as the testing evidence:

- <u>**[Service Group Metric Collection](https://confluence.global.standardchartered.com/display/DSP/Service+Group+Metric+Collection)**:</u> this part we collected the **resource **consumption metric for different VM groups, they are **Database**, **Infra & Common** Service, **Cash Settlement** Group and** Trade Control** Group, base on the group view we can asses the VM resource usage during each system load. *<u> </u>*[*<u>link</u>* ](https://confluence.global.standardchartered.com/display/DSP/Service+Group+Metric+Collection)

**EXPAND_END**

**EXPAND: 2: Test Data Analysis**

| Test Type | Process duration (min) |
| --- | --- |
| trade | sett |
| 1X | 60 | 60 |
| 2X | 60 | 60 |
| 4X | 181 | 134 |
| 6X | 230 | 181 |

| Test Type | avg CPU load (%) |
| --- | --- |
| database | infra | settlement | trade |
| 1X | 44 | 49.1 | 26 | 2.6 |
| 2X | 82 | 60 | 30 | 2.9 |
| 4X | 83.4 | 64 | 50 | 6.6 |
| 6X | 79.7 | 66 | 58 | 6.6 |

| Test Type | avg memory load (%) |
| --- | --- |
| database | infra | settlement | trade |
| 1X | 50 | 52 | 44 | 19.7 |
| 2X | 50 | 54 | 46 | 20.2 |
| 4X | 50 | 56 | 47 | 20.5 |
| 6X | 50 | 56 | 48 | 20.5 |

| Test Type | system load (%) |
| --- | --- |
| database | infra | settlement | trade |
| 1X | 76 | 131 | 37 | 6 |
| 2X | 150 | 142 | 53 | 6 |
| 4X | 181 | 167 | 73 | 6 |
| 6X | 158 | 176 | 90 | 7 |

- For peak load testing, when system running on 1X peak volume, the system can finish the processing within 1 hour, and the average latency for both front end and back end is under 5s, server CPU for database under 50% and memory under 50%, server CPU for application server under 50% and memory under 30%
- For stress testing, when system running on 2X peak volume, the system can still finish the processing within 1 hour, but the average latency for backend processing will exceed 5s till 10s, server CPU for database exceed 70% and memory under 50%, server CPU for infra and common hosts reach around 60% and memory under 30%, server CPU for settlement nodes under 50% and memory under 30%
- For stress testing, when system running on 4X peak volume, the system will reach throughput, the total processing during took 3 hours 1 minutes, and the average latency for both frontend and backend will break SLA (recorded frontend response is good but there will be lots of timeout), server CPU for database exceed 80% and memory under 50%, server CPU for infra and common hosts reach around 60% and memory under 30%, server CPU for settlement nodes under 50% and memory under 30%
- For stress testing, when system running on 6X peak volume, the system will reach throughput, the total processing during took 3 hours 50 mins, and the average latency for both frontend and backend will break SLA, server CPU for database exceed 80% and memory under 50%, server CPU for infra and common hosts reach around 60% and memory under 30%, server CPU for settlement nodes under 50% and memory under 30%
- The behavior for 8 hour endurance/soak test (use peak volume to simulate behavior under peak situation) align with 1 hour peak testing

**EXPAND_END**

**EXPAND: 3: Conclusion**

| Description | RAG Status | Comments |
| --- | --- | --- |
| Overall Conclusion | | The performance meet expectation under 1X and 2X peak volume |
| Issue and Risk Impact | | When peak volume has plan to reach 4X volume, the application need to optimize both the processing time and the system load |
| Deviations from Plan | | NA |
| Environment Variance | | NA |

| **Legend** | | Can recommend release | | Concerns/Caveats signatory must accept | | Cannot recommend release |
| --- | --- | --- | --- | --- | --- | --- |

- The system load and processing time for both front end and back end meet SLA under 1X peak volume
- The system load and processing time for front end can still meet SLA under 2X peak concurrencies, but processing time for backend STP need optimization although processing duration still within 1 hour
- Both system load and processing time will break SLA when stress reach 4X peak volumes, which means the system will reach bottleneck under 4X stress, application team need to enlarge the system capacity together with processing optimization
- When peak hour stress reach volumes larger then 4X, for example 6X, the system load will not increase as it's already reach to threshold, but processing time become larger and larger

### Open Risks and Issues

| SN | Risk/Issue Description | Severity H/M/L | Probability H/M/L | Mitigation Plan | Owner |
| --- | --- | --- | --- | --- | --- |
| 1 | CPU pressure: when business volume > 4x, the CPU usage will more than 70%. | L | L | Dev team will monitor CPU usage and changes and will solve the problem if peak volume increases. To solve the issue, either a dispensation will be needed, or in most case a CR is created for CPU capacity expansion, which is typically resolved in 3 to 4 days. Until the CR completed, if the CPU usage reaches 100%, the cashflow data will keep processing but there could be delays in processing. | Dev team |
| 2 | Process time: when business volume > 4x, the processing time will reach throughput and take longer time | L | L | Dev team will have plan to optimize the processing time when peak volume increases. To solve the issue, either a dispensation will be needed, or in most case a CR is created for CPU capacity expansion, which is typically resolved in 3 to 4 days. Until the CR completed, if the CPU usage reaches 100%, the cashflow data will keep processing but there could be delays in processing. | Dev team |
| 3 | | | | | |

**EXPAND_END**

**EXPAND: 4: Appendix**

- As the purpose for this performance test is to very the performance under deployment strategy change with services mover to new servers. The cpmarision result refer to sub pages under [Zero - The testing before new deployment - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Zero+-+The+testing+before+new+deployment), which proved the conclusion that the process time and throughput is the same before and after deployment strategy change, but CPU and memory already break agreement when stress reach 2X peak. The main purpose for the deployment change is to separate business workload to new servers.

| Test Type | Process duration (min) |
| --- | --- |
| trade | sett |
| 1XA | 60 | 60 |
| 1XB | 60 | 60 |
| 2XA | 60 | 60 |
| 2XB | 60 | 60 |
| 4XA | 181 | 134 |
| 4XB | 81 | 105 |
| 6XA | 230 | 181 |
| 6XB | 121 | 145 |

| Test Type | Average Latency (sec) |
| --- | --- |
| trade | sett | GUI |
| 1XA | 0.7 | 3.2 | 0.94 |
| 1XB | 0.68 | 3.5 | 1.2 |
| 2XA | 2.9 | 3.8 | 0.85 |
| 2XB | 2.8 | 6.96 | 2.5 |
| 4XA | 1440 | 3.9 | 2.0 |
| 4XB | 734 | 1380 | 2.6 |
| 6XA | 2580 | 4.1 | 2.2 |
| 6XB | 2095 | 2640 | 2.9 |

📎 [system_metrics.xlsx](attachments/system_metrics.xlsx)

**EXPAND_END**