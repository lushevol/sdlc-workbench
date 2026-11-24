# 1. Background

Setting up a server for Ebbs involved copying everything from YAML configurations to properties classes, configuration classes, and builder classes. This resulted in high code duplication and difficulty in maintenance.

Taking setting up a Solace link for Ebbs as an example, the development steps are roughly as follows:

1) Add a file named application-enterprise-solace-ebbs-bridge.yml, add configuration information, and configure the application.yml file to read this file;

2) Add the class EnterpriseSolaceEbbsConfigProperties, and configure it to read YAML configuration files starting with enterprise-solace-ebbs-bridge;

3) Add the class EnterpriseSolaceEbbsJmsComponentConfiguration， The `EnterpriseSolaceEbbsJmsComponentConfiguration` class reads properties from the `EnterpriseSolaceEbbsConfigProperties` class to create `JmsComponent`, `CachingConnectionFactory`, `SolConnectionFactory`, etc., and reads specific `com.scb.ratan.messagebridge.enums.TopicType`;

4) Add the class `EnterpriseSolaceEbbsConsumerClientRouteBuilder` ，In the `enterpriseSolaceEbbsConsumerClientRouteBuilder` class, specify the specific `com.scb.ratan.messagebridge.enums.TopicType`;

5) Modify the class `ConsumerClientRouteBuilderConfiguration`，and Initialize the `enterpriseSolaceEbbsConsumerClientRouteBuilder` bean
6) Modify all classes related to the specific `com.scb.ratan.messagebridge.enums.TopicType` of EBBS, such as `com.scb.ratan.messagebridge.processor.pre.OffsetProcessor`, `com.scb.ratan.messagebridge.processor.pre.TargetRouteProcessor`, `com.scb.ratan.messagebridge.properties.TopicDetailProperties`, `com.scb.ratan.messagebridge.route.producer.MessageProducerImpl`, etc.;

**Three new classes need to be added, a configuration file needs to be added, and six classes need to be modified.**

The main problems are as follows:

| Serial number | item to be optimized | problem/pain point |
| --- | --- | --- |
| 1 | Generalized configuration | Each type has its own separate yml and Properties class, resulting in a lot of repetition and making maintenance difficult. |
| 2 | Generic Properties class | One Properties class for each type |
| 3 | JmsComponent Registration | One @Configuration for each type, duplicate Bean registrations. |
| 4 | RouteBuilder generalization | Each type has its own RouteBuilder class, with a similar code structure. |
| 5 | RouteBuilder Registration | Manually registering each type of bean using @Bean is prone to omissions and errors. |
| 6 | TopicType Centralized Management | Multiple if/else statements or hard-coded TopicType in Lists result in poor extensibility. |
| 7 | Code reuse | There's a lot of copying and pasting involved, and adding new types requires multiple modifications. |

# 2. Optimization strategy

Considering code usability, maintainability, and extensibility，The optimization approach is as follows:

| Serial number | Optimization items | Optimization plan/idea | description | Extensibility |
| --- | --- | --- | --- | --- |
| 1 | Generalized configuration | Uses Map/List structures for unified configuration, type differentiation, and supports multiple instances. | Configure all JMS/Kafka instances uniformly using a Map/List structure. | Adding a new type only requires adding configuration. |
| 2 | Generic Properties class | A generic JmsBridgeConfigProperties | Manage all instance configurations using a Map<String, JmsInstanceConfig>. | No need to create a new Properties class for new types |
| 3 | JmsComponent Registration | Automatically register all enabled instances using a factory/loop. | | No need to manually add @Bean to new types |
| 4 | RouteBuilder generalization | Abstract base class + parameterization, subclasses only need to pass type/key, and even automatic registration. | | Adding new types requires minimal code or can be automatically registered. |
| 5 | RouteBuilder Registration | Configure the driver and register all RouteBuilders of the enabled type in a loop. | | Adding new types requires minimal code or can be automatically registered. |
| 6 | TopicType Centralized Management | Use Sets for centralized management, or use configuration/enumeration. | Use Set/enumeration to centrally manage all types and avoid hard-coding multiple if/else statements. | Adding a new type only requires adding an enumeration or configuration. |
| 7 | Code reuse | Only configuration is required, with minimal code changes, making it easy to maintain. | Unified processing logic to avoid copying and pasting | No need to copy and paste when adding new types |

Summary

1，All bridge configs are unified under message-bridge.instances in application.yml.
2，A generic properties class supports all types and is easily extensible.
3，Components are registered dynamically by type.
4，RouteBuilder is abstracted for reuse.
5，TopicType sets are managed centrally for easy extension.

# Purpose

**Reduce the repetitive operations of steps 2, 3, 4, and 5 mentioned above**

**Add new bridge types by adding a config block—no need to create new config classes or** beans.（**This approach maximizes maintainability and extensibility**）

2.1. Code Adjustment Demo

yml：
message-bridge:
instances:
enterpriseSolaceKoreaJmsComponent:
enabled: XXXX
topicType: enterprise_korea
host: XXX
vpn: XXX
username: XXX
keyStoreFormat: jks
keyStoreFile: XXX
keyStorePwd: XXX
trustStoreFile: XXXX
trustStorePwd: XXX
trustStoreFormat: jks
solaceJmsComponent:
enabled: XXX
topicType: solace
clientIdPrefix: 51358-ratanone
host: XXX
vpn: XXX
username: srv.51358.ratanone.001
password: XXX
principal: srv.51358.ratanone.001
jndiName: XXX
cerFile: XXX
cerFilePwd: XXX
kafkaBridgeNew:
enabled: true
topicType: kafka
commonConfigs:
brokers: XXX
reconnectBackoffMs: 10000
consumer:
consumersCount: 1
allowManualCommit: true
autoCommitEnable: false
autoOffsetReset: latest
breakOnFirstError: true
producer:
retries: 10
retryBackoffMs: 1000
bufferMemorySize: 67108864
compressionCodec: lz4
maxRequestSize: 20971520

properties class：

@ConfigurationProperties(prefix = "message-bridge")
public class MessageBridgeConfigProperties {
    /**
     * key: instance name
     * val: instance configuration
     */
    private Map<String, InstanceConfig> instances;

@Data
    public static class InstanceConfig {
        private boolean enabled;
        // TopicType Enum
        private String topicType;
        // Common
        private String host;
        private String vpn;

private Map<String, Object> commonConfigs;

// Kafka
       private Map<String, Object> consumer;
       private Map<String, Object> producer;
    }
}

enum class：

public enum TopicType {
    // kafka
    KAFKA,
    
    ENTERPRISE_EBBS,
    
    ENTERPRISE_KOREA,
    
    ;
}

# 3. Question

1. Does the new solution support the new bridge configuration, or does it migrate all the old bridges to the new solution? Support all bridge.
2. Does Kafka Bridge also need to be migrated to the new configuration class? Yes
3. Kafka Bridge has some special processing logic, such as handling URLs for topics and queues in a particular way, which requires reading the properties class. Resolved

Business Points (Special Processing Points):

1) In general Solace connections, IMS needs to be processed, i.e., com.scb.ratan.messagebridge.route.consumer.SolaceConsumerClientRouteBuilder#isImsReceivedRequired returns true. Done

2) In the general Solace connection, initialContext.env needs to be processed, i.e., com.scb.ratan.messagebridge.configuration.SolaceJmsComponentConfiguration#afterPropertiesSet. Done

3) General Solace/ebbs Solace/atlas Solace connections all need to initialize properties, i.e., com.scb.ratan.messagebridge.route.producer.MessageProducerImpl#initSolaceJmsProperties. Done

4) TopicType list and judgment, i.e., com.scb.ratan.messagebridge.properties.TopicDetailProperties#afterPropertiesSet, com.scb.ratan.messagebridge.processor.pre.TargetRouteProcessor#process, com.scb.ratan.messagebridge.route.AbstractConsumerClientRouteBuilder#initRoute. Done

5) Concatenate Kafka/SFTP topics/queues, and read properties from kafkaProperties/sftpProperties for judgment.

6) Special judgment for IBMMQ endpoints, i.e., com.scb.ratan.messagebridge.route.producer.MessageProducerImpl#sendBody. Done

7) Special judgment for SFTP endpoints, i.e., com.scb.ratan.messagebridge.route.producer.MessageProducerImpl#sendBody. Done

8) Special judgment for folder endpoints, i.e., com.scb.ratan.messagebridge.route.producer.MessageProducerImpl#sendBody. Done

# 4. Comparison results

A comparison of the results of adding a Solace link to the old and new solutions, and adding or modifying code.

**old solution: Three new classes need to be added, a configuration file needs to be added, and six classes need to be modified.**

**new solution:  Add configuration blocks to the yml file and add enumerations to TopicType.**

# 5. Functional verification

5.1 env: dev，1 yml configuration

| Topic type | Flow config | Route name | route_type | log | remark |
| --- | --- | --- | --- | --- | --- |
| solace | | TARGET | | Message published to endpoint: solaceJmsComponent:topic:v1/post-trade/51358-ratanone/ratanone/ims/ack for exchange id: 54108C38521194A-0000000000000AFB | IMS |
| kafka | uber-flow | SOURCE | solace | camel route: [ solaceJmsComponent-uber-flow-1 ] ==> [ solaceJmsComponent:queue:q-51358-ratanone-uber-msg ] receives message, start to pre-process message if needed | tradeId:8663462470 |
| TARGET | kafka | Message published to endpoint: kafka:tdsx_uber_message_json_inbound?valueSerializer=com.scb.ratan.messagebridge.serial.TDSXUberToJsonSerializer&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 | |
| | | Message published to endpoint: kafka:Common_Event_Record_In?brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for exchange id: 024CF2893819CED-0000000000001B31 | |
| enterprise_korea | settlement-korea | SOURCE | kafka | camel route: [ Kafka-Consumer-Route-settlement-korea-1 ] ==> [ kafka:Cash_Settlement_EBBS_Process_Out_HK?groupId=Cash_Settlement_EBBS&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed | |
| TARGET | settlement-korea | Message published to endpoint: enterpriseSolaceKoreaJmsComponent:topic:v1/51358-ratan/casa/json-v1/hk/req/post/fnd/medium/14147-ebbs-hk for exchange id: A1A72AECED020B2-00000000000002C8 | |
| TARGET | kafka | Message published to endpoint: kafka:Cash_Settlement_Korea_Ack_NAck_In?brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for exchange id: A1A72AECED020B2-00000000000002C9 | |
| sftp | swift-flow | SOURCE | kafka | Receved messages of tracking id: Random-653e9912-acaf-4884-a445-1c5ff18b1872, JMSMessageID: null, JMSCorrelationID: null, JMSTimestamp: null | |
| TARGET | sftp | Message published to endpoint: sftp:10.61.17.228:22/../../enisis/AFT_MSG/RATAN/MXOUTGOING?preferredAuthentications=publickey&username=ratanuser&privateKeyFile=/apps/ratanrt/iso_ssh_keys/id_rsa&passiveMode=false&binary=true&useUserKnownHostsFile=false&jschLoggingLevel=DEBUG&disconnect=false&autoCreate=false&charset=UTF-8&stepwise=false | |
| ibmmq | mxg-cashflow-ACK | SOURCE | kafka | camel route: [ Kafka-Consumer-Route-mxg-cashflow-ACK-21 ] ==> [ kafka:Ratan-Mxg-Cashflow-Adaptor-Murex-Ack?groupId=mxg-cashflow-kafka-consumer-group-v1&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed | |
| TARGET | ibmmq | Message published to endpoint: [ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2](ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2) for tracking id: Random-cd04f9bd-9213-4915-a011-d48afe966a3a | |
| folder | strategic-settlement | SOURCE | folder | camel route: [ folderBridge-strategic-settlement-39 ] ==> [ [file:/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true](http://file/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true) ] receives message, start to pre-process message if needed | |
| TARGET | kafka | Message published to endpoint: kafka:Cash_Settlement_EBBS_Ack_Nack?groupId=group-accounting-response&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-b8a49748-b10b-4270-9339-2a00e5fe0a34, | |

5.2 env:dev, Split YAML configuration

| Topic type | Flow config | Route name | route_type | log | remark |
| --- | --- | --- | --- | --- | --- |
| solace | | TARGET | | Message published to endpoint: solaceJmsComponent:topic:v1/post-trade/51358-ratanone/ratanone/ims/ack for tracking id: null | IMS |
| kafka | uber-flow | SOURCE | solace | camel route: [ solace-bridge-uber-flow-1 ] ==> [ solaceJmsComponent:queue:q-51358-ratanone-uber-msg ] receives message, start to pre-process message if needed | tradeId: 7140876736 |
| TARGET | kafka | Message published to endpoint: kafka:tdsx_uber_message_json_inbound?valueSerializer=com.scb.ratan.messagebridge.serial.TDSXUberToJsonSerializer&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: de6eccc9b39dc9da01a2bcc0685eb73b | |
| | kafka | Message published to endpoint: kafka:Common_Event_Record_In?brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: de6eccc9b39dc9da01a2bcc0685eb73b | |
| enterprise_korea | settlement-korea | SOURCE | kafka | camel route: [ Kafka-Consumer-Route-settlement-korea-1 ] ==> [ kafka:Cash_Settlement_EBBS_Process_Out_HK?groupId=Cash_Settlement_EBBS&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed | |
| TARGET | settlement-korea | Message published to endpoint: kafka:Cash_Settlement_Korea_Ack_NAck_In?brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-01ab2d35-a805-4d86-919e-3b6108491636, | |
| TARGET | kafka | Message published to endpoint: kafka:Cash_Settlement_EBBS_Ack_Nack?groupId=group-accounting-response&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-01ab2d35-a805-4d86-919e-3b6108491636, | |
| sftp | swift-flow | SOURCE | kafka | camel route: [ Kafka-Consumer-Route-swift-flow-11 ] ==> [ kafka:Swift_MX_ENISIS_Out?groupId=Message_Bridge&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed | |
| TARGET | sftp | Message published to endpoint: sftp:10.61.17.228:22/../../enisis/AFT_MSG/RATAN/MXOUTGOING?preferredAuthentications=publickey&username=ratanuser&privateKeyFile=/apps/ratanrt/iso_ssh_keys/id_rsa&passiveMode=false&binary=true&useUserKnownHostsFile=false&jschLoggingLevel=DEBUG&disconnect=false&autoCreate=false&charset=UTF-8&stepwise=false for tracking id: Random-0eecdff8-b01d-4f9f-a6cc-086e88ad1a5b | |
| ibmmq | mxg-cashflow-ACK | SOURCE | kafka | camel route: [ Kafka-Consumer-Route-mxg-cashflow-ACK-21 ] ==> [ kafka:Ratan-Mxg-Cashflow-Adaptor-Murex-Ack?groupId=mxg-cashflow-kafka-consumer-group-v1&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed | |
| TARGET | ibmmq | Send message: 224693 to target: [ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2](ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2) fail | |
| TARGET | kr_mq | Send message: 231507 to target: [krmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2](krmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2) fail | |
| folder | strategic-settlement | SOURCE | folder | camel route: [ folder-bridge-strategic-settlement-39 ] ==> [ [file:/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true](http://file/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true) ] receives message, start to pre-process message if needed | |
| TARGET | kafka | Message published to endpoint: kafka:Cash_Settlement_EBBS_Ack_Nack?groupId=group-accounting-response&brokers=10.198.199.160:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-872a0097-1eba-4a9a-aabf-f526ec133e25 | |

5.3 env: uat4， one yml config

| Topic type | Flow config | Route name | route_type | route_id | log | remark |
| --- | --- | --- | --- | --- | --- | --- |
| solace | | TARGET | | | Message published to endpoint: solaceJmsComponent:topic:v1/post-trade/51358-ratanone/ratanone/ims/ack for tracking id: null | IMS |
| kafka | uber-flow | SOURCE | solace | 1 | camel route: [ solaceJmsComponent-uber-flow-1 ] ==> [ solaceJmsComponent:queue:q-51358-ratanone-uber-msg ] receives message, start to pre-process message if needed | tracking id:dd6765c6c83133a11dc869ad124dc912 |
| TARGET | kafka | Message published to endpoint: kafka:tdsx_uber_message_json_inbound?valueSerializer=com.scb.ratan.messagebridge.serial.TDSXUberToJsonSerializer&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: dd6765c6c83133a11dc869ad124dc912 |
| | | | Message published to endpoint: kafka:Common_Event_Record_In?brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: dd6765c6c83133a11dc869ad124dc912 |
| enterprise_korea | settlement-korea | SOURCE | kafka | 1 | camel route: [ Kafka-Consumer-Route-settlement-korea-1 ] ==> [ kafka:Cash_Settlement_EBBS_Process_Out_HK?groupId=Cash_Settlement_EBBS&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed | tracking id: Random-5770bb0b-8830-41fa-ae2f-ff26d6d30b68 |
| TARGET | enterprise_korea | Message published to endpoint: enterpriseSolaceKoreaJmsComponent:topic:v1/51358-ratan/casa/json-v1/hk/req/post/fnd/medium/14147-ebbs-hk for tracking id: Random-5770bb0b-8830-41fa-ae2f-ff26d6d30b68 |
| TARGET | kafka | Message published to endpoint: kafka:Cash_Settlement_Korea_Ack_NAck_In?brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-5770bb0b-8830-41fa-ae2f-ff26d6d30b68 |
| sftp | swift-flow | SOURCE | kafka | 11 | camel route: [ Dispatch-Producer-Route ] receives message, start to determine whether to send message to final target endpoint: TargetEndpoint [id=1, endpoint=sftp:10.61.17.228:22/../../enisis/AFT_MSG/RATAN/MXOUTGOING?preferredAuthentications=publickey&username=ratanuser&privateKeyFile=/apps/ratanrt/iso_ssh_keys/id_rsa&passiveMode=false&binary=true&useUserKnownHostsFile=false&jschLoggingLevel=DEBUG&disconnect=false&autoCreate=false&charset=UTF-8&stepwise=false] and failure counter: 0 | tracking id: Random-34674537-4aca-4d02-9b4e-044548932cad |
| TARGET | sftp | Message published to endpoint: sftp:10.61.17.228:22/../../enisis/AFT_MSG/RATAN/MXOUTGOING?preferredAuthentications=publickey&username=ratanuser&privateKeyFile=/apps/ratanrt/iso_ssh_keys/id_rsa&passiveMode=false&binary=true&useUserKnownHostsFile=false&jschLoggingLevel=DEBUG&disconnect=false&autoCreate=false&charset=UTF-8&stepwise=false for tracking id: Random-34674537-4aca-4d02-9b4e-044548932cad |
| ibmmq | mxg-cashflow-ACK | SOURCE | kafka | 21 | camel route: [ Kafka-Consumer-Route-mxg-cashflow-ACK-21 ] ==> [ kafka:Ratan-Mxg-Cashflow-Adaptor-Murex-Ack?groupId=mxg-cashflow-kafka-consumer-group-v1&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed | tracking id: Random-3f1bd416-b419-45e1-8e9f-51ab8d3973a8 |
| TARGET | ibmmq | Message published to endpoint: [ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2](ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2) for tracking id: Random-3f1bd416-b419-45e1-8e9f-51ab8d3973a8 |
| TARGET | kr_mq | Message published to endpoint: [krmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2](krmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2) for tracking id: Random-3f1bd416-b419-45e1-8e9f-51ab8d3973a8 |
| folder | strategic-settlement | SOURCE | folder | 39 | camel route: [ folderBridge-strategic-settlement-39 ] ==> [ [file:/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true](http://file/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true) ] receives message, start to pre-process message if needed | tracking id: Random-6b750104-fd4f-4ba5-8908-d4627c646746 |
| TARGET | kafka | Message published to endpoint: kafka:Cash_Settlement_EBBS_Ack_Nack?groupId=group-accounting-response&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-6b750104-fd4f-4ba5-8908-d4627c646746 |

5.4 env:uat4, Split YAML configuration

| Topic type | Flow config | Route name | route_type | route_id | log |
| --- | --- | --- | --- | --- | --- |
| solace | | TARGET | | | Message published to endpoint: solaceJmsComponent:topic:v1/post-trade/51358-ratanone/ratanone/ims/ack for tracking id: null |
| kafka | uber-flow | SOURCE | solace | 1 | camel route: [ solaceJmsComponent-uber-flow-1 ] ==> [ solaceJmsComponent:queue:q-51358-ratanone-uber-msg ] receives message, start to pre-process message if needed |
| TARGET | kafka | Message published to endpoint: kafka:tdsx_uber_message_json_inbound?valueSerializer=com.scb.ratan.messagebridge.serial.TDSXUberToJsonSerializer&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: a1e8563d5bf8e86754bb1668fa36eab3 |
| | | | Message published to endpoint: kafka:Common_Event_Record_In?brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: a1e8563d5bf8e86754bb1668fa36eab3 |
| enterprise_korea | settlement-korea | SOURCE | kafka | 1 | ~~camel route: [ Kafka-Consumer-Route-settlement-korea-1 ] ==> [ kafka:Cash_Settlement_EBBS_Process_Out_HK?groupId=Cash_Settlement_EBBS&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed~~ |
| TARGET | enterprise_korea | ~~Message published to endpoint: enterpriseSolaceKoreaJmsComponent:topic:v1/51358-ratan/casa/json-v1/hk/req/post/fnd/medium/14147-ebbs-hk for tracking id: Random-dc803c13-1dfc-4d98-afe0-2a52ebcd4381~~ |
| TARGET | kafka | ~~Message published to endpoint: kafka:Cash_Settlement_Korea_Ack_NAck_In?brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-dc803c13-1dfc-4d98-afe0-2a52ebcd4381~~ |
| sftp | swift-flow | SOURCE | kafka | 11 | camel route: [ Kafka-Consumer-Route-swift-flow-11 ] ==> [ kafka:Swift_MX_ENISIS_Out?groupId=Message_Bridge&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed |
| TARGET | sftp | Message published to endpoint: sftp:10.61.17.228:22/../../enisis/AFT_MSG/RATAN/MXOUTGOING?preferredAuthentications=publickey&username=ratanuser&privateKeyFile=/apps/ratanrt/iso_ssh_keys/id_rsa&passiveMode=false&binary=true&useUserKnownHostsFile=false&jschLoggingLevel=DEBUG&disconnect=false&autoCreate=false&charset=UTF-8&stepwise=false for tracking id: Random-07593dd2-dcb7-4f43-8f02-d315a3357ec7 |
| ibmmq | mxg-cashflow-ACK | SOURCE | kafka | 21 | camel route: [ Kafka-Consumer-Route-mxg-cashflow-ACK-21 ] ==> [ kafka:Ratan-Mxg-Cashflow-Adaptor-Murex-Ack?groupId=mxg-cashflow-kafka-consumer-group-v1&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&consumersCount=1&allowManualCommit=true&autoCommitEnable=false&autoOffsetReset=latest&breakOnFirstError=true ] receives message, start to pre-process message if needed |
| TARGET | ibmmq | Message published to endpoint: ibmmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2 for tracking id: Random-a5b6a14c-844a-4783-945e-badd96aaaefc |
| TARGET | kr_mq | Message published to endpoint: krmqJmsComponent://queue:CF.RATAN.MXG.RESP.uat2 for tracking id: Random-a5b6a14c-844a-4783-945e-badd96aaaefc |
| folder | strategic-settlement | SOURCE | folder | 39 | camel route: [ folderBridge-strategic-settlement-39 ] ==> [ [file:/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true](http://file/apps/ratanrt/services/test/settlement/tech-release/cashflow/topic/ToRatanEbbsAck?readLock=markerFile&readLockDeleteOrphanLockFiles=false&initialDelay=1s&move=done&moveFailed=error&autoCreate=true) ] receives message, start to pre-process message if needed |
| TARGET | kafka | Message published to endpoint: kafka:Cash_Settlement_EBBS_Ack_Nack?groupId=group-accounting-response&brokers=10.198.199.164:9092&reconnectBackoffMs=10000&retries=10&retryBackoffMs=1000&bufferMemorySize=67108864&compressionCodec=lz4&maxRequestSize=20971520 for tracking id: Random-f7d19303-1dff-4838-bd28-931f80cdbdbf |

5.5 flow config

![image-2026-2-20_14-4-24.png](attachments/image-2026-2-20_14-4-24.png)

# 6. Migration Plan

~~6.1, Migration Method:~~

~~1) Copy the corresponding topicType's yml configuration to application-bridge.yml, ensuring variable names do not contain hyphens;~~

~~2) Open the com.scb.ratan.messagebridge.route.consumer.configuration.ConsumerClientRouteBuilderConfiguration class and comment out the code of the corresponding topicType's routeBuilder Bean;~~

~~3) Delete the corresponding topicType's yml file and the spring.profiles.include reference in application.yml;~~

~~4) Delete the corresponding routeBuilder class (located in the com.scb.ratan.messagebridge.route.consumer directory), Configuration class (located in the com.scb.ratan.messagebridge.configuration directory), and Properties class (located in the com.scb.ratan.messagebridge.properties directory).~~

~~Note: Do not delete the KakfaConfigProperties and SftpConfigProperties classes and their yml files yet.~~

6.2, Migration timeline

the timeline for switching these configurations to the new solution is as follows:

| Serial number | Topic type | Does the new plan support? | Planned start time | Planned end time | remark | |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | enterprise_atlas | Yes | | | SolConnectionFactory | Similar configuration |
| 2 | enterprise_solace | Yes | | |
| 3 | enterprise_ebbs | Yes | | |
| 4 | enterprise_fileit | Yes | | |
| 5 | enterprise_korea | Yes | | | Implemented through dynamic configuration |
| 6 | ibmmq | Yes | | | MQQueueConnectionFactory | Similar configuration |
| 7 | kr_mq | Yes | | | No flow configurations were found in the uat1, fmrp1, fmrp2, and staging environments. |
| 8 | solace | Yes | | | SolaceJmsConnectionFactory | |
| 9 | kafka | Yes | | | | |
| 10 | folder | Yes | | | | |
| 11 | sftp | Yes | | | | |

6.3, File changes

File changes after complete migration

| | **new solution(one total yml)** | **new solution(keep split yml)** |
| --- | --- | --- |
| add yml count | 1 | 0 |
| add class count | 9 | 9 |
| delete yml count | 10 | 0 |
| delete class count | 31 | 31 |

# **7. New solution development process**

7.1, **one total yml**

**a）Add a configuration block to the application-bridge.yml file**

**b）TopicType class add an enum of type**

**7.2, keep split yml**

**a）Add a configuration block to an new yml file, for example : application-enterprise-korea-bridge.yml**
enterpriseSolaceKoreaJmsComponent:
enabled: true
**b）The application.yml file adds a reference to the new yml file, for example:  spring.profiles.include : -enterprise-korea-bridge**

**c）TopicType class add an enum of type**