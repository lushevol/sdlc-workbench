# ****

# **6.7.3.14-lock-SNAPSHOT**

Fixed dead lock issue

# **6.7.3.13-lock-SNAPSHOT**

## Changes

ratanone-lock-spring-boot-starter:

1. Add redisson for distribution lock framwork
2. Springboot upgraded to 3.4.4 (old: 3.4.1)
3. Sprintcloud upgraded to 2024.0.1 (old: 2024.0.0)

camunda upgrade to 7.23.0

## Important changes on domain service:

for domain service, changes as below:

1. springboot parent upgrade to 3.4.4

![image-2025-8-1_14-12-43.png](attachments/image-2025-8-1_14-12-43.png)

2. Failsafe framework is not required for lock scenarios

3. Lock parameters are the same as below, but for second parameter, the meaning changes

for example :

Old:
public void run(String key, long expireMilliSeconds, String actionInProgress, CommandNoReturn commandNoReturn) {
the second parameter is lock expire time, unit is millsecond

if exceed this time, lock will be released

New:
public void run(String key, long waitTimeSeconds, String actionInProgress,  CommandNoReturncommandNoReturn)
the second parameter is wait time, unit is second.

expire time will be deprecated because Redisson will hold the key until application execute over by watch dog

**waitTimeSeconds    **means if this application can not get the lock at present, how long it will be waiting, that's why we deprecate failsafe , because Redisson already support auto retry

# **6.7.3.12-SNAPSHOT**

*ratanone-data-model:*

1. Upgrade TDSX proto schema version from V7.1-RELEASE to V7.8-RELEASE
2. Change some fields from **single value** to **array** according to upgraded schema definition.
3. Correct internal field value type.
4. Add new internal field for FXU.

*ratanone-commons:*

* *

1. In ProtoTypeUtils.class time zone set to UTC when convert Timestamp value.

1. Provide capability to parse value from supported message types , developer can **parse & enrich** value without care about the message type. How to use as below sample:

| *CashflowMessageHolder<?> messageHolder = CashflowParserHelper.init({your scmbl or json});* * * *messageHolder.parseString(XpathEnum. **CASHFLOW__CASHFLOW_ID); // Parse value* * * *Map<XpathEnum, Object> fieldMap = Maps.newHashMap(); * *fieldMap.put(CASHFLOW__EVENT_REASON, "Reversal");* *fieldMap.put(CASHFLOW__MINOR_VERSION, 10);* *messageHolder.enrich(fieldMap); // Enrich value* *messageHolder.getMessage(); // Get message* |
| --- |

For more use cases please refer to the UT in foundation code.

1. Provide full cashflow mappings between logical model and xpath in XpathEnum.class with value type. For derived fields will support separately.

* *

*ratanone-cqrs-spring-boot-starter:*

* *

1. Domain event Kafka publisher serialize message with the ObjectMapper injected automatically by Spring instead of the self-created one.
2. Domain event Jdbc mapper use the auto injected ObjectMapper as well.
3. This is to support the T of DoaminEvent<T> could be able to specific the serilaizer/deserializer yourself, e.g. In lifecycle service, publish DomainEvent<RatanCashSettlementData>, need to add configuration

| *@Configuration public class ObjectMapperConfig { @Autowired private ObjectMapper objectMapper; @PostConstruct public void registerModules() { objectMapper.registerModule(new SimpleModule("RatanCashSettlementDataModel") .addSerializer(RatanCashSettlementData.class, new RatanCashflowRecordJacksonSerializer()) .addDeserializer(RatanCashSettlementData.class, new RatanCashflowRecordJacksonDeserializer())); } }* |
| --- |

* *

1. Not foundation change but an agreement - Let’s use the same topic* **cash_settlement_cashflow_domain_events ***

*** ***

| * * *RatanApiContextHolder.getContext().set("payloadStrategy", "JSON");* *RatanApiContextHolder.getContext().get("payloadStrategy”);* * * * * |
| --- |

*** ***

*ratanone-scbml-lm-converter:*

1. Upgrade Rosetta mapping version to v7.8-RELEASE
2. Provide capability to auto generate XpathEnum automatically.