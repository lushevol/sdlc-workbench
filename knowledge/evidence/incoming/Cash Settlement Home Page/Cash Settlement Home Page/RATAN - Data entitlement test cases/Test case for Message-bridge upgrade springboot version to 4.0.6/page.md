env: dev

flow logs:

| Flow config | Route name | route_type | log |
| --- | --- | --- | --- |
| kr-oltp-flow | SOURCE | kafka | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Kafka-Consumer-Route-kr-oltp-flow-1 ] |
| TARGET | solace | camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: solaceJmsComponent:topic:v1/post-trade/51358-ratanone/ratanone/json-4.0/accounting/-/pub ] |
| mxg-cashflow-ACK | SOURCE | kafka | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Kafka-Consumer-Route-mxg-cashflow-ACK-21 ] |
| TARGET | ibmmq | camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: [ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP](ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP) ] |
| swift-flow | SOURCE | kafka | 2026-05-22 02:09:34.778 || 2738 || CamelThread-#3 || INFO || Kafka-Consumer-Route-swift-flow-11 || || ti:Random-127648d7-dc3c-4ae0-9bea-3287e22cf46f || camel route: [ Kafka-Consumer-Route-swift-flow-11 ] ==> [ kafka:Swift_MX _ENISIS_Out?groupId=Message_Bridge&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed |
| TARGET | sftp | 2026-05-22 02:09:39.374 || 2738 || EventThread-3 || INFO || c.s.r.m.r.p.EventProducerRoute || || ti: || camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: sftp:10.61.17.228:22/../ ../enisis/AFT_MSG/RATAN/MXOUTGOING?preferredAuthentications=publickey&username=ratanuser&privateKeyFile=/apps/ratanrt/iso_ssh_keys/id_rsa&passiveMode=false&binary=true&useUserKnownHostsFile=false&jschLoggingLevel=DEBUG&disconn ect=false&autoCreate=false&charset=UTF-8&stepwise=false ] |
| strategic-settlement | SOURCE | folder | 2026-05-22 02:20:50.372 || 2738 || CamelThread-#13 || INFO || LocalFolder-Consumer-Route-strategic-settlement-39 || || ti:Random-82cd250f-fa3f-489b-aca0-4e311ca82a07 || camel route: [ LocalFolder-Consumer-Route-strategic-set tlement-39 ] ==> [ [file:/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatan](http://file/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatan)EbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true ] rec eives message, start to pre-process message if needed |
| TARGET | kafka | 2026-05-22 02:20:50.408 || 2738 || EventThread-4 || INFO || c.s.r.m.r.p.EventProducerRoute || || ti: || camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: kafka:Cash_Settlement_EB BS_Ack_Nack?groupId=group-accounting-response&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 ] |
| strategic-settlement | SOURCE | kafka | camel route: [ Kafka-Consumer-Route-strategic-settlement-100 ] ==> [ kafka:Cash_Settlement_EBBS_Process_Out_SA?groupId=Cash_Settlement_EBBS&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed |
| TARGET | enterprise_ebbs | camel route: [ direct:dispatchRoute ], trackingId: Random-3d9f7e4a-f853-4b33-8821-d6ec90f2246e dispatch to target: [ enterpriseSolaceEbbsJmsComponent:topic:v1/51358-ratan/casa/json-v1/sa/req/post/fnd/medium/14147-ebbs-sa ] |
| | | | |
| | | | |
| | | | |
| | | | |

camel log:

![image-2026-5-25_10-51-28.png](attachments/image-2026-5-25_10-51-28.png)

Env: uat4

flow logs:

| Flow config | Route name | route_type | log |
| --- | --- | --- | --- |
| uber-flow | SOURCE | solace | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Solace-Consumer-Route-uber-flow-1 ] |
| TARGET | kafka | Message flowName: uber-flow, correlationId:4a0ad0df3894d9d6d4b21830f9edf669_7153008709, trackingId: 4a0ad0df3894d9d6d4b21830f9edf669, endpoint:kafka:tdsx_uber_message_json_inbound?valueSerializer=com.scb.ratan.messagebridge.serial.TDSXUberToJsonSerializer&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 processed, cost time: 105 ms |
| kr-mxg-cashflow | SOURCE | kafka | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Kafka-Consumer-Route-kr-mxg-cashflow-151 ] |
| TARGET | ibmmq | camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: [ibmmqJmsComponent://queue:RATAN.KOREAMXG.FLW.RESP](ibmmqJmsComponent://queue:RATAN.KOREAMXG.FLW.RESP) ] |
| swift-flow | SOURCE | kafka | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Kafka-Consumer-Route-swift-flow-11 ] |
| TARGET | sftp | camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: sftp:10.61.17.228:22/../../enisis/AFT_MSG/RATAN/MXOUTGOING?preferredAuthentications=publickey&username=ratanuser&privateKeyFile=/apps/ratanrt/iso_ssh_keys/id_rsa&passiveMode=false&binary=true&useUserKnownHostsFile=false&jschLoggingLevel=DEBUG&disconnect=false&autoCreate=false&charset=UTF-8&stepwise=false ] |
| kr-oltp-flow | SOURCE | kafka | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Solace-Consumer-Route-kr-oltp-flow-2 ] |
| TARGET | solace | camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: solaceJmsComponent:topic:v1/post-trade/51358-ratanone/ratanone/json-4.0/accounting/-/pub ] |
| SOURCE | solace | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Solace-Consumer-Route-kr-oltp-flow-2 ] |
| TARGET | kafka | camel route: Event-Producer-Route is about to send event: [ PROCESSED ] , comment: [ . sent to: kafka:Cash_Settlement_OLTP_Response?brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 ] |
| strategic-settlement | SOURCE | kafka | camel route: Event-Producer-Route is about to send event: [ RECEIVED ] , comment: [ . message received from: Kafka-Consumer-Route-strategic-settlement-100 ] |
| TARGET | enterprise_ebbs | |

camel log:

![image-2026-5-25_14-1-54.png](attachments/image-2026-5-25_14-1-54.png)