# 1. Background

For CN Settlement workflow there are several significant status change which need to be synchronized to Stella. Stella has provided SDK for service integration before and created an additional channel for strategic cashflow.

This page is used to record integration detail with Stella and Ratan CN cashflow lifecycle service.

# 2. Reference

## 2.1 Strategic Cash Transaction State Model

[Process Model - Strategic Cash Generation - FM re-platforming - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/FMRP/Process+Model+-+Strategic+Cash+Generation)

## 2.2 Ratan Ambassador Document

[Stella API Enhancement - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Stella+API+Enhancement)

[Stella Ambassador Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Stella+Ambassador+Design)

# 3. Stella SDK Upgrade

## 3.1 Dependency

```java
<dependency>
    <groupId>com.scb.sabre.fmrep</groupId>
    <artifactId>sabre-booking-api</artifactId>
    <version>1.2.0</version>
</dependency>
```

## 3.2 New Channel

```java
package com.scb.sabre.booking.api.common;

public enum StellaChannel {
    ...

	RATANCASH_V2("ratancash-v2"),    
    ...

}
```

# 4. Integration

## 4.1 Stella Status Action Flow

## 4.2 Test Case

| Stella Env: dev |
| --- |
| SN | Cashflow Id | Status Before | Action | Status After | Transaction Version | Status | Comments | Evidence |
| 1 | 003486517198 | PROJECTED | Net | NETTED | 0->1 | | TL delay is a protential issue, follow up via email | ![image2023-3-29_11-10-28.png](attachments/image2023-3-29_11-10-28.png) |
| | 003486517198 | NETTED | Unnet | PROJECTED | 1->2 | |
| | 003486517198 | PROJECTED | Release | RELEASED | 2->3 | |
| | 003486517198 | RELEASED | Settle | SETTLED | 3->4 | |
| 2 | 003486517199 | PROJECTED | Settle | SETTLED | 0->1 | | Stella doesn't allow cross statuses update | |
| 3 | 003486517199 | PROJECTED | Net | NETTED | 0->1 | | | |
| | 003486517199 | NETTED | Release | RELEASED | 1->2 | | | |
| | 003486517199 | RELEASED | Settle | SETTLED | 2->3 | | | |

## 4.2 Interact with Cashflow Lifecycle

| Config Name | Topic | Producer | Consumer | Consumer group | Comments | Message Sample(Highlight in Red) |
| --- | --- | --- | --- | --- | --- | --- |
| message-batch | Cashflow_Status_Batch_Command_In | ratan-cashflow-lifecycle-service | ratanone-stella-ambassador | Stella-Ambassador-Message-Batch-Group | Cashflow scheduled job | Header: **Key:** cashflowId: 003486517198 stellaMessageType: STRATEGIC_CASHFLOW responseTopic: XXXXXX **Payload:** [ { "action": "Release", "businessVersion": "0", "cashflowId": "003486517198", "cashflowVersion": "1", "commandId": "c32f416e-df0c-415f-b23c-84af91975076", "correlationId": "1032892", "operation": "STATUS_UPDATE", "trackingId": "aae38b50-e495-4f85-8a3e-28ea55fbbe64" }, { "action": "Net", "businessVersion": "0", "cashflowId": "003486517199", "cashflowVersion": "0", "commandId": "c32f416e-df0c-415f-b23c-84af91975076", "correlationId": "1015376", "operation": "STATUS_UPDATE", "trackingId": "0bbdc024-68af-4974-a6bd-f8bf4fb62c6e" }, |
| message | Cashflow_Status_Command_In | ratan-cashflow-lifecycle-service | ratanone-stella-ambassador | Stella-Ambassador-Message-Group | Status update trigger | Header: **Key:** cashflowId: 003486517198 stellaMessageType: STRATEGIC_CASHFLOW responseTopic: XXXXXX **Payload:** { "action": "Release", "businessVersion": "0", "cashflowId": "003486517198", "cashflowVersion": "2", "commandId": "12031", "correlationId": "3832245079", "operation": "STATUS_UPDATE", "trackingId": "MX_FXCASH_330840406_289337760_1679548904267" } |
| batch-result | Cashflow_Status_Batch_Response_In **Can we change to below topic on strategic cashflow result?** Cash_Settlement_Cashflow_Status_Batch_Response_In | ratanone-stella-ambassador | ratan-cashflow-lifecycle-service | cashflow-service-stella-batch-response | When StellaResultEvent is published out with eventType is ALL or BROADCAST, and api type is BATCH, then publish to here | **Nothing has been changed， just for information** { "success": false, "commandId": "3b8fe58f-6c05-4929-9798-45c1d7958dc0", "errorCode": "TimeoutException", "errorMessage": null, "result": null } |
| result | Cashflow_Status_Response_In **Can we change to below topic on strategic cashflow result?** **Cash_Settlement_Cashflow_Status_Response_In** | ratanone-stella-ambassador | ratan-cashflow-lifecycle-service | cashflow-service-stella-response | When StellaResultEvent is published out with eventType is ALL or BROADCAST, and api type is SIGNLE, then publish to here | **Nothing has been changed， just for information** { "id": "b165c2ba-1bbc-4e76-b344-7a9e3c7b7029", "commandId": "12031", "trackingId": "MX_FXCASH_330840406_289337760_1679548904267", "cashflowId": "003486517198", "correlationId": "3832245079", "businessVersion": "0", "cashflowVersion": "1", "razorStatus": null, "stellaCashflowVersion": "2", "processStatus": "SUCCESS", "errorCode": null, "errorMessage": null, "stellaStatus": "PROJECTED" } Or { "id": "5d74cb40-ebff-4bbe-a752-e75ed1e18108", "commandId": "12031", "trackingId": "MX_FXCASH_330840406_289337760_1679548904267", "cashflowId": null, "correlationId": null, "businessVersion": null, "cashflowVersion": null, "razorStatus": null, "stellaCashflowVersion": "2", "processStatus": "FAILED", "errorCode": "TL_RETRY_ERROR", "errorMessage": "Errors:ProcessingError - Errors:TL_RETRY_ERROR - RETRY MAX TIMES in Elastic Search for transactionId=003486517198, transactionVersion=2\n\n", "stellaStatus": "" } |

## 4.3 Stella Exceptions and Actions

| Exception & Error | Exception source | Reason | Action |
| --- | --- | --- | --- |
| java.util.concurrent.TimeoutException: null at java.base/java.util.concurrent.CompletableFuture.timedGet(CompletableFuture.java:1886) at java.base/java.util.concurrent.CompletableFuture.get(CompletableFuture.java:2021) at com.scb.sabre.booking.api.common.StellaBookingApi.sendMessage(StellaBookingApi.java:415) at com.scb.sabre.booking.api.common.StellaBookingApi.sendScbml(StellaBookingApi.java:183) at com.scb.ratan.ambassador.stella.wrapper.StellaSingleMessageApi.doSend(StellaSingleMessageApi.java:57) at com.scb.ratan.ambassador.stella.wrapper.AbstractStellaApiWrapper.sendScbml(AbstractStellaApiWrapper.java:78) at com.scb.ratan.ambassador.stella.executor.StellaApiCallExecutor.lambda$execute$0(StellaApiCallExecutor.java:107) at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128) at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628) at java.base/java.lang.Thread.run(Thread.java:834) | Stella Api | Stella environment is not running | Retry until success(Cannot reproduce and test) |
| { "status": "FAIL", "detail": "Errors:ProcessingError - Errors:TRANSACTION_WORKFLOW_MISMATCH - New action for txn 003486517198 on workflow Cash Settlement does not match existing transaction workflow of Standard Cash Settlement. Transitions can only be performed on the same workflow\n\n", "transactionId": "003486517198", "transactionVersion": 2, "tradeId": null, "tradeVersion": null, "errorType": "BUSINESS", "originalMessageSender": "Ratan", "childTransactions": null, "fromState": null, "currentState": null, "action": "Release", "errorCodes": ["TRANSACTION_WORKFLOW_MISMATCH"], "identifiers": null, "attributes": null } | Stella Api | Stella handled last request got issue, Previous Unnet request didn't sync to Trade Lake but return success to ambassandor | Stella needs to resolve this issue to keep this workflow as a transaction |
| { "status": "FAIL", "detail": "Errors:ProcessingError - Errors:TL_RETRY_ERROR - RETRY MAX TIMES in Elastic Search for transactionId=003486517198, transactionVersion=2\n\n", "transactionId": "003486517198", "transactionVersion": 2, "tradeId": null, "tradeVersion": null, "errorType": "SYSTEM", "originalMessageSender": "Ratan", "childTransactions": null, "fromState": null, "currentState": null, "action": "Release", "errorCodes": [ "TL_RETRY_ERROR" ], "identifiers": null, "attributes": null } | Stella Api | Trade Lake is down | |

# 5. Developer Mind Map

![image2023-4-19_10-31-16.png](attachments/image2023-4-19_10-31-16.png)