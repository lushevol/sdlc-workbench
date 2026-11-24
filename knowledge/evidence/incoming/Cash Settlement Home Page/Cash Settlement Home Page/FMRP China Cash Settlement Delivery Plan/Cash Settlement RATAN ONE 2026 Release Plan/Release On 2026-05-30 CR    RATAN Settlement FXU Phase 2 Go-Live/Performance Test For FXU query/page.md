# Test Plan

- Target URL: [https://fmo-mfe-preprod.pi.dev.net:8453/api/ratan/v1/fx/utilization/trade/getCurrency2ByCurrency1](https://fmo-mfe-preprod.pi.dev.net:8453/api/ratan/v1/fx/utilization/trade/getCurrency2ByCurrency1) (Staging)
- Parameters { "Trade": { "Trade_Id": "4100002999", "Trade_Lake_Trade_Major_Version": "1", "Swap_Leg_ID": "", "Exchanged_Currency1_Payment_Amount_Currency": "USD", "Exchanged_Currency1_Util_Amount": "200" } }
- Concurrency: 50 users
- Duration: 3600s

# Test Result

- [Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1779421344572/report/index.html)
- Resource

![](https://confluence.global.standardchartered.com/download/attachments/3744446292/image-2026-5-22_13-52-26.png?version=1&modificationDate=1779429149000&api=v2)

![image-2026-5-22_13-53-2.png](attachments/image-2026-5-22_13-53-2.png)

![image-2026-5-22_13-56-58.png](attachments/image-2026-5-22_13-56-58.png)