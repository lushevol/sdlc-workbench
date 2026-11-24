1, fmo  page

cashflow ID : C06810140003   **[Fixed]  actionTime format is waiting for confirming**

![image-2025-8-27_15-49-18.png](attachments/image-2025-8-27_15-49-18.png)

![image-2025-8-27_15-50-0.png](attachments/image-2025-8-27_15-50-0.png)

2, lifecycle error

cashflow ID : C06810140004

Exception happened -- [http://ratan-cashflow-lifecycle-service/v1/cashflow/camunda/holding-check](http://ratan-cashflow-lifecycle-service/v1/cashflow/camunda/holding-check), ReplayTopic is [Settlement_Orchestration_Adhoc_Ssi], Exception reason is [[500 ] during [POST] to [[http://ratan-cashflow-lifecycle-service/v1/cashflow/camunda/holding-check]](http://ratan-cashflow-lifecycle-service/v1/cashflow/camunda/holding-check]) [CommonServiceCaller#execute(URI,CamundaApiRequest)]: [{"status":500,"errorCode":"SERVICE_INTERNAL_ERROR","errorMessage":"Text '2025-09-19T18:00:00Z' could not be parsed, unparsed text found at index 19","metadata":null}]]

3,  swift suppresssed but no accounting **[Fixed]**

C06810140005

accounting service update SSI stamp URL and parameters, accounting-service version updated to 2.0.0

![image-2025-8-29_10-34-45.png](attachments/image-2025-8-29_10-34-45.png)

4，swift unsuppress approve , lifecycle service not publish to process_in topic

C06810140005

5, not publish to process in topic  **[Fixed]**

N00000062629

![image-2025-8-27_16-25-49.png](attachments/image-2025-8-27_16-25-49.png)

6, manual un-net not call  query service  **[Fixed]**

N00000062629

![image-2025-8-27_16-29-22.png](attachments/image-2025-8-27_16-29-22.png)

7,  ui un-net call swift suppress/unsupress approve api

N00000062629

8,

N00000062629,C06810140005, C06810141005

![image-2025-8-27_16-41-19.png](attachments/image-2025-8-27_16-41-19.png)

9. auto-unnet

N00000062630,C06810140005,C06810141005

ratan-cash-settlement-orchestration || STELLA.1755538990974.6b9cc4d8-5a42-4e02-8ef8-721306996a8c-1-1_1001 || Stella || RAZOR || null || Exception happened -- [http://ratan-cash-settlement-netting-service/v2/netting/camunda/autoUnNet](http://ratan-cash-settlement-netting-service/v2/netting/camunda/autoUnNet), ReplayTopic is [null], Exception reason is [[500 ] during [POST] to [[http://ratan-cash-settlement-netting-service/v2/netting/camunda/autoUnNet]](http://ratan-cash-settlement-netting-service/v2/netting/camunda/autoUnNet]) [CommonServiceCaller#execute(URI,CamundaApiRequest)]: [{"status":500,"message":"No static resource v2/netting/camunda/autoUnNet.","data":null}]]

![image-2025-8-27_16-48-27.png](attachments/image-2025-8-27_16-48-27.png)

10,  auto-unnet **[Fixed]**

N00000062630,C06810140005,C06810141005

![image-2025-8-27_16-58-22.png](attachments/image-2025-8-27_16-58-22.png)

[com.cn](http://com.cn).ratan.netting.domain.common.error.NettingServiceException: Payload must not be null
        at [com.cn](http://com.cn).ratan.netting.application.service.UnNettingService.unNetCashflow(UnNettingService.java:188)
        at [com.cn](http://com.cn).ratan.netting.application.service.UnNettingService.lambda$unNetCashflowWithLock$3(UnNettingService.java:146)
        at com.scb.ratan.service.template.ResourceLockManager.run(ResourceLockManager.java:72)
        at [com.cn](http://com.cn).ratan.netting.application.service.UnNettingService.unNetCashflowWithLock(UnNettingService.java:129)
        at [com.cn](http://com.cn).ratan.netting.application.service.UnNettingService.lambda$autoUnNet$1(UnNettingService.java:102)

11, bulk submit   case 13 passed

C06810142008,C06810142009

12,  reinstate ui call /v2/ratan/cashflow/move/status/user remove scbml field

reinstate

C06810142008,C06810142009

13, reinstate faild                      **[Fixed]**

C06810142009

fail action call this api but ui history missed this event action

[https://fmo-mfe-dev.uk.dev.net:8453/api/ratan/v1/camunda/task/fail](https://fmo-mfe-dev.uk.dev.net:8453/api/ratan/v1/camunda/task/fail)

message format error,  topic: cash_settlement_cashflow_domain_events

![image-2025-8-27_17-42-29.png](attachments/image-2025-8-27_17-42-29.png)

14, SettleAsGross  action need publish to process in

CH6800724464

15, orchestration   1_1 camuda modify  @yang chen      **[Passed]**

16, Materialize action error.

Lifecycle need to know whether need to publish process-in

C07810140013