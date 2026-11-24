# Introduction

## Background

Currently in FMRP, there are multiple data model across various systems SCBML, LM, Itradeable, internal data models per system, some systems are maintain and using all three data model.

For Ratan, we consume SCBML and extract required information via xml xpath. Given this disparity in the data model usage, it is firstly impractical to maintain and secondly it impedes quick onboarding of any product/ system. Hence, we want to decommission SCBML in the strategic flow entirely and allow us to move to a single JSON data model across the entire stack

UBER is an aggregation message that contains below information in proto buffer format, generate on each event to contain all the relevant information as snapshot. UBER message contains the following parts:

1. Trade Info
2. Cashflow Info
3. Fixing Info

UBER uses Logic Model to generate it's proto buffer schema and SDK for consumers, down streams are able to consume the entire transaction data include above 1~3 in one message.

**Uber Data Structure:**

| Key Fields | Type |
| --- | --- |
| tradeRecord | Object |
| cashFlowData | Object [] |
| FixingNotice | Object [] |
| Has_Changed | "Has_Changed": { "Cashflows": true, "Trade": false, "FixingNotice": true }, |

**EXPAND: High Level Integration**

**Current processing via SCBML: **[Ratan processing on cashflow events - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+processing+on+cashflow+events)

****

| Uber |
| --- |
| uber_id | trade_id | total | valid | w | n | mv | trade_state | action_type | Biz Event Type | tc | cc | fc | Group Status | cashflows |
| 1 | ["4354367341"] | 13 | 13 | 0 | 13 | [1] | ["TOBESENT"] | ["Book"] | Trade | TRUE | TRUE | FALSE | Pending Trade Validation | <details> <summary>Expand Details</summary> ["004354367437"]-N;["004354367438"]-N;["004354367439"]-N;["004354367440"]-N;["004354367441"]-N;["004354367442"]-N;["004354367443"]-N;["004354367444"]-N;["004354367445"]-N;["004354367446"]-N;["004354367447"]-N;["004354367448"]-N;["004354367449"]-N </details> |
| 2 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["TOBESENT"] | ["Book"] | | | | | | |
| 3 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["SENT"] | ["Send"] | | TRUE | FALSE | FALSE | Completed | |
| 4 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["SENT"] | ["Send"] | | FALSE | TRUE | FALSE | | |
| 5 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["SENT"] | ["Send"] | | FALSE | TRUE | FALSE | | |
| 6 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["SENT"] | ["Send"] | | FALSE | TRUE | FALSE | | |
| 7 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["SENT"] | ["Send"] | | FALSE | TRUE | FALSE | | |
| 8 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["SENT"] | ["Send"] | | FALSE | TRUE | FALSE | | |
| 9 | ["4354367341"] | 13 | -1 | -1 | -1 | NA | ["SENT"] | ["Send"] | | FALSE | TRUE | FALSE | | |
| 10 | ["4354367341"] | 25 | 23 | 11 | 12 | [2] | ["TOBESENT"] | ["Book"] | RemainingPartyFull Clearing | TRUE | TRUE | FALSE | Pending Trade Validation | <details> <summary>Expand Details</summary> ["004354367439"]-W;["004354367440"]-W;["004354367441"]-W;["004354367442"]-W;["004354367443"]-W;["004354367444"]-W;["004354367445"]-W;["004354367446"]-W;["004354367447"]-W;["004354367448"]-W;["004354367449"]-W;["004354367934"]-N;["004354367935"]-N;["004354367936"]-N;["004354367937"]-N;["004354367938"]-N;["004354367939"]-N;["004354367940"]-N;["004354367941"]-N;["004354367942"]-N;["004354367943"]-N;["004354367944"]-N;["004354367945"]-N </details> |
| 11 | ["4354367341"] | 25 | -1 | -1 | -1 | NA | ["NONCONFIRMED"] | ["Nonconfirm"] | | TRUE | FALSE | FALSE | Completed | |
| 12 | ["4354367341"] | 25 | -1 | -1 | -1 | NA | ["NONCONFIRMED"] | ["Nonconfirm"] | | | | | | |
| 13 | ["4354367341"] | 35 | 19 | 9 | 10 | [3] | ["TOBESENT"] | ["Book"] | PartialTermination Partial Unwind | TRUE | TRUE | FALSE | Pending Trade Validation | <details> <summary>Expand Details</summary> ["004354367936"]-W;["004354367937"]-W;["004354367938"]-W;["004354367939"]-W;["004354367940"]-W;["004354367941"]-W;["004354367942"]-W;["004354367944"]-W;["004354367945"]-W;["004354368086"]-N;["004354368098"]-N;["004354368099"]-N;["004354368100"]-N;["004354368101"]-N;["004354368102"]-N;["004354368103"]-N;["004354368104"]-N;["004354368105"]-N;["004354368106"]-N </details> |
| 14 | ["4354367341"] | 35 | -1 | -1 | -1 | NA | ["NONCONFIRMED"] | ["Nonconfirm"] | | TRUE | FALSE | FALSE | Completed | |
| 15 | ["4354367341"] | 35 | 15 | 15 | 0 | [4] | ["TOBESENT"] | ["Book"] | Withdrawal | TRUE | TRUE | FALSE | Pending Trade Validation | <details> <summary>Expand Details</summary> ["004354367437"]-W;["004354367438"]-W;["004354367934"]-W;["004354367935"]-W;["004354367943"]-W;["004354368086"]-W;["004354368098"]-W;["004354368099"]-W;["004354368100"]-W;["004354368101"]-W;["004354368102"]-W;["004354368103"]-W;["004354368104"]-W;["004354368105"]-W;["004354368106"]-W </details> |
| 16 | ["4354367341"] | 35 | -1 | -1 | -1 | NA | ["NONCONFIRMED"] | ["Nonconfirm"] | | TRUE | FALSE | FALSE | Completed | |
| 17 | ["4354367341"] | 35 | 10 | 0 | 10 | [5] | ["TOBESENT"] | ["Revive"] | PartialTermination Undo | TRUE | TRUE | FALSE | Pending Trade Validation | <details> <summary>Expand Details</summary> ["004354368086"]-N;["004354368098"]-N;["004354368099"]-N;["004354368100"]-N;["004354368101"]-N;["004354368102"]-N;["004354368103"]-N;["004354368104"]-N;["004354368105"]-N;["004354368106"]-N </details> |
| 18 | ["4354367341"] | 37 | 2 | 0 | 2 | [5] | ["TOBESENT"] | ["Revive"] | PartialTermination Fixing | FALSE | TRUE | TRUE | Pending Trade Validation | ["004354425778"]-N;["004354425779"]-N |

**EXPAND_END**

**More Uber details please refer to the pages:**

- [Uber Mesages - SABRE - Confluence](https://confluence.global.standardchartered.com/display/SABRE/Uber+Mesages)
- [TDSX Uber Message - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/TDSX+Uber+Message)
- [https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/lm/logical-model-json-validator/v6.1/logical-model-json-validator-v6.1-Json.zip](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/lm/logical-model-json-validator/v6.1/logical-model-json-validator-v6.1-Json.zip)
- [Atomicity for FMRP flows in TL - SABRE - Confluence](https://confluence.global.standardchartered.com/display/SABRE/Atomicity+for+FMRP+flows+in+TL)

## Objective & Scope

Uber adoption is a milestone for Ratan strategic cash settlement. Team is willing to take this opportunity to do some enhancement.

This document will cover high level technical design of UBER integration on RATAN strategic cash settlement. Below points should be covered:

- Uber message integration
- Strategic cash settlement flow optimization
- Lifecycle restructure
- Technical analysis on performance and tuning if possible
- Backward compatibility on historical data

Processing flow could be changed, but **no new business requirement **introduced.

## Challenges

1. By analyzing the current service code, it's high coupled with SCBML especially in grouping, orchestration, lifecycle, it's foreseeable that maybe a big effort to completely decouple the SCBML.
2. Uber is only onboarded on Stella, so the Uber adoption need to compatible with Murex.
3. Compatible with lived historical data.

## Open Questions

Collect all open questions related to Uber to below table:

15 in total, 2 items are still not closed.

**EXPAND: Click here to expand open questions...**

| 1 | The process/sequence of UBER generation 1. Principle of UBER generation? 2. Trigger point? 1. Each trade events? 2. Each cashflow events? 3. Fixing events? | Uber will be generated on anytime if trade or cashflow transaction happen. | |
| --- | --- | --- | --- |
| 2 | Transaction control. | UBER is not atomic transaction. It is possible that UBER generated but some cashflows will be missing, which may drive above 1 and 2 cannot be achieved. Solution: There will be a new attribute exception flag introduced, RATAN need to filter out the entire uber message if there is any exception in indicator flag | |
| 3 | Sequence sensitive or not. | No, there is no sequence indicator | |
| 4 | Data extraction - Data in UBER are all Arrays ![image-2025-3-21_15-25-6.png](attachments/image-2025-3-21_15-25-6.png) | Have confirmed with Li, Rui, he has raised requirement to DM team to correct the repeated type. Keep the array as repeated and remove the repeated if not an array. But now only trade block has been refreshed, cashflow still not get updated. I will keep following up. | |
| 5 | Cashflow identification - No straight way to find out impacted cashflows, can only compare with last version. | Only handle the difference cashflow from the last version | |
| 6 | Cashflow identification - For Trade status (Validated/Confirmed) which drive payments STP, the UBER will show "Hash_Change.Cashflow: **false**" ![image-2025-3-21_15-30-51.png](attachments/image-2025-3-21_15-30-51.png) | Change flag is not fit for Uber processing because each Uber message sequence can't be guaranteed, in case the sequence issue and message lost issue, better to compare the message with latest version. | |
| 7 | If any cashflow failure the entire Uber message will not be generated or Uber message publish with the partial success cashflows? | Publish partial success cashflows, the exceptional case should be cashflow major exception from TDS3 will not block Uber generation but the issued cashflow will not be included. Still under discussion. Confirmed there will be a exception indicator for RATAN to filter uber | |
| 8 | There is no Uber technical version, can't do duplication check and overdue check. | Agreed with Li, Rui to add a timestamp so that we can do the duplication check and overdue check. Still have some risk: 1. If the uber 1 and uber 3 comming , uber 2 lost, ratan can't identify. need to confirm with @Lina Feng whether there is business impact. 2. Last Uber missed, ratan can't handle, need to monitor from upstream 3. Uber ack message is not used at all. Currently we can use tracking id for duplicate check. | |
| 9 | TDSX schema is defined only for downstream consumption or all downstream interaction data modeling standard? As attributes under Trade.Settlement_Instruction.proto is far from enough. Trade SSI stamping request with Uber, Ratan has to provide a new data model as SSI stamping response for CDUPS to process, which is not such strategic. | Discussed with Ankur, got answer below: 1. This will need to be a data-modelling discussion. Should this exist in trade-data, for RATAN and CDU-PS to communicate with each other? If it is agreed and modelled and populated, TDSX will automatically expose it. 2. Overall, the trade data model will only have minimum possible fields that are needed by multiple consumers and determined upstream. Ratan will create our own model with Settlement Instruction included. No need to ask them adding. | |
| 10 | About TDSX query API, how to invoke API call? | TDSX API call is used to query data from TL with specific params. given the code sample below: private TDSXQuery queryUberMessageData(String tradeId, Instant effective, Instant asOf) { return TDSXQueryBuilderWrapper.builder() .fields("*") .asOf(asOf) .effective(effective) .includeCashflowFields("*") .includeFixingNoticeFields("*") .includeDuplicateBooking() .includeComputedData(TDSXComputedDataTypes.FixingInformationComputed) .filter(f -> f.eq(TradeFields.TradeId, tradeId)) .build(); } | |
| 11 | Does API call result is exactly follow Uber schema | No, there are some difference, given the code to build the Uber by client self. public Optional<TDSXUberMessage> generateUberMessage(String tradeId, Instant effective, Instant asOf, Map<String, Boolean> hasChanged) { Stream<TradeData> tradeDataStream = tdsxApiService.getApiClient().queryTrade(queryUberMessageData(tradeId, effective, asOf), throwable -> {}, TracingService.getCurrentTraceId(), TracingService.getCurrentSpanId()); return tradeDataStream.findFirst().map(tradeData -> { TDSXUberMessage.Builder tdsxUberMessage = TDSXUberMessage.newBuilder(); tdsxUberMessage.setTDS3Data(tradeData.getTDS3Data()); Optional.of(tradeData) .map(TradeData::getTDS3Data) .map(TDS3Data::getTradeRecord) .ifPresent(tradeRecord -> { Optional.of(tradeRecord).map(TradeRecord::getTradeIdList).flatMap(tradeIdList -> tradeIdList.stream().findFirst()).ifPresent(tdsxUberMessage::setTradeId); Optional.of(tradeRecord).map(TradeRecord::getTrackingVersionList).flatMap(trackingVersionList -> trackingVersionList.stream().findFirst()).ifPresent(tdsxUberMessage::setTrackingVersion); }); Optional.ofNullable(hasChanged).ifPresentOrElse(hc -> { // provided hasChange info Map<String, BoolValue> protoHasChanged = hc.entrySet().stream().collect(Collectors.toMap(Map.Entry::getKey, e -> BoolValue.of(e.getValue()))); tdsxUberMessage.putAllHasChanged(protoHasChanged); }, () -> { // no hasChange info provided // We need check Uber message to find out what changed, ideally the changed data has same and later transaction time. // TODO, do we need this? put it to TODO first }); return tdsxUberMessage.build(); }); } | |
| 12 | What is asOf and effective? | It is bi-tempral model | Field name | Mandatory | Condition | | --- | --- | --- | | asOf=<iso8601 date> | No (defaults to NOW()) | Trade_Lake_Transaction_To_Date_Time > asOf | | AND Trade_Lake_Transaction_From_Date_Time <= asOf | | effective=<iso8601 date> | No (defaults to NOW()) | Trade_Lake_Valid_To_Date_Time > effective | | AND Trade_Lake_Valid_From_Date_Time <= effe | v1 , from t1 -> to tMax --------------------------- when v2 coming at t2 time --------------------------- v1, from t1 -> to t2 v2, from t2 -> to tMax | |
| Field name | Mandatory | Condition |
| asOf=<iso8601 date> | No (defaults to NOW()) | Trade_Lake_Transaction_To_Date_Time > asOf |
| AND Trade_Lake_Transaction_From_Date_Time <= asOf |
| effective=<iso8601 date> | No (defaults to NOW()) | Trade_Lake_Valid_To_Date_Time > effective |
| AND Trade_Lake_Valid_From_Date_Time <= effe |
| 13 | Convert SCBML to Logical Model in Json | <scbml-lm-converter.version>1.2.0-alpha-20250529.3-00cc886b</scbml-lm-converter.version> <dependency> <groupId>com.scb.sabre.fmrep</groupId> <artifactId>scbml-lm-converter</artifactId> <version>${scbml-lm-converter.version}</version> </dependency> return new Scbml2LmConverter(rosettaReleaseVersion, false); [https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/lm/logical-model-json-validator/](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/lm/logical-model-json-validator/) rosettaReleaseVersion | |
| 14 | Will Uber contains all required information for RATAN to do cash settlement processing ? | Yes and confirmed | |
| 15 | Downstream integration should be considered? | No, Down stream will keep the same (Razor, LMS etc.) | |

**EXPAND_END**

# Feasibility & Benefit Analysis

## Benefits

Currently RATAN is consuming data from TDS3 for Trade Data and Cashflow Data separately, overall good for past years, but we found below limitations that may be solved by Uber messages:

| | RATAN Function | Limitations for Now | With UBER |
| --- | --- | --- | --- |
| 1 | Data assembling | TDS publishes trades and cashflows separately. Technically the trade and cashflow sequence can't be ensured. Ratan need to query upstream to get trade information which potentially impact our performance. | TDS assembles everything according to logic model, the message contains entire trade information with all cashflow snapshots and fixing snapshots. |
| 2 | Grouping management | RATAN need to wait all the cashflows under particular trade event before processing, grouping logic to avoid duplicate payment is complicated and always challenged by user why cashflow stuck in grouping blotter. | Uber message contains all cashflows snapshot and fixing notice under a trade event, grouping logic is no longer required. |
| 3 | Settlement Control on Trade Validation | After all cashflows all arrived, grouping blotter still need to wait trade validation event, which may also stuck in group blotter | Ratan may clearly know whether the cashflow related trade has been validated or not, and only handle the cashflow only if trade validated. |
| 4 | Data parsing & validation | RATAN is parsing SCBML in each service, the data type is not easy to be figured out from SCBML message, need to be very careful to handle data format. Previously we had a prod issue because date string is not correctly parsed. | UBER is based on proto buffer and generated SDK is provided for serialization and deserialization with strong data type, services can deal with the data via java object easily and consistently, which avoid data quality issue. |
| 5 | Data modeling | We always be told to relied on the strict adherence to the definition of data modeling, but in fact, the cashflow xpath we currently use is defined separately in the constant of the service, which is not uniform and does not have strict checks. | UBER schema is based on logical model and can be naturally follow data modeling definition strictly by using central serialization |
| 6 | Cashflow attribute stamping | Currently attribute stamping such as entity and counterparty query is cashflow level, assume 40 payment under 1 trade, Ratan will invoke 40 times API query with same condition | Ratan is able to query sci API only once for each Uber message in trade event level which will reduce the network cost. |

## Feasibility

After Uber use case analysis, the conclusion is Uber can fit our current requirement, but we need do some enhancement

📎 [Uber Use Cases.xlsx](attachments/Uber Use Cases.xlsx)
![image-2025-6-6_15-47-24.png](attachments/image-2025-6-6_15-47-24.png)

# Proposal

## Design Principles

Trade-offs must be made to choose the best option for us to achieve design goals, and we consider the something more valuable than others:

## Re-Design consideration

| | Consideration | Comment | Status |
| --- | --- | --- | --- |
| 1 | Anti-Corruption Layer Design | Define common model for cash settlement | Covered by Uber |
| 2 | Clarify responsibility of each domain | Cashflow stamping, Validation | Covered by Standardization, workflow |
| 3 | Async / Sync processes definition | e.g. Swift generation should be sync process | Covered by workflow enhancement |
| 4 | Netting/Unneting Performance | absolutely transactional should be considered | Covered by lifecycle restructure |
| 5 | Lock mechanism | [RATANONE Distributed Lock ReDesign - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATANONE+Distributed+Lock+ReDesign) | Covered by Joey |
| 6 | Single responsibility is principal, structuring the complicated code | eg. lifecycle service | Covered by lifecycle restructure |

## Anti-Corruption Layer Design

Currently, we're highly coupled with SCBML in most services of RATAN, and each service has it's own way to parse SCBML or extract values from the configured xpath, it works but not a good way because:

- SCBML is so specific type, if the data type change, the current implementation will not work without large effort. - Lifecycle service process state machine. - Workflow processing SCBML with camunda API request/response - SSI Stamping according to the SCBML template - query service handle domain events. - LMS processing with SCBML - Netting service resultant cashflow generation
- Data serialization & deserialization by service itself, not easy to maintain and extend.
- Duplicate code everywhere, such as CashflowScbmlFactory, XpathParser, XpathConstants...etc.

As we are integrating Uber, we foresee a lot of changes. Base on that we realize we really need **Anti-Corruption Layer. **

**What's the benefit of Anti-Corruption Layer:**

1. Introduce a standardized model inside all Ratan Services. Ratan standardized model means DM standardized model + Ratan Internal data model.
2. Keep consistence on terminology and reduce duplications
3. Decouple the impact of external data formats. Flexible to support different data format.

**The key take-aways of this approach are as following:**

- Define the Logic Model and develop the SDK for data transformation and other common operations
- Migrate our services to the ideal protocols step-by-step by sustainable iterations and controllable changes

## Ratan Data Model

**Data Transmisson Format - JSON**

Compared with the JSON and Protobuf, Protobuf is smaller and faster than JSON. But due to the human readable is more important and required by our current application, finally we choose **JSON **as our final data format

**Schema Definition Stategy - Proto**

Compared with proto file and java class

| | Java class | proto |
| --- | --- | --- |
| Convert JSON | Rely on Spring/Jackson | Rely on Google protobuf util |
| Cross Language | No | Yes |
| Efficient Serialization | No | Yes |
| Automatic Code Generation | No, need manual create class | Yes |
| Simple | Yes | No, need mvn plugin to generate Java class |
| Extendsion | Not easy to extend from TDSX | Yes, naturedly supported |

It's obviously that Proto is our first choice to create Ratan data model.

**Ratan Data Model Definition as below:**

## Uber Adoption and Simplify Our STP flow

**Cash Settlement Flow 2.0 - High Level Diagram**

**Cash Settlement Flow 2.0 - Uber Data Flow**

# Delivery Plan

## Timeline

@Ruiheng Cao

## Development Scope & Task break down

| SN | Service/Component | ADO Number | Task Description | Owner | Data Model Change Points | Key change | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ratanone-foundation/ratanone-data-model | | 1. Add dependency of TDSX schema and TDSX SDK 2. Provide RatanCashSettlementData model for common usage 3. Provide Kafka Serializer/Deserializer for data mapping between json string and Ratan common model 4. Provide SCBML convert to Json util | @Xinmiao Huang | 1. Integrate with TDSX Schema and SDK 2. Ratan cash settlement model definition/revision 3. Uber message to ratan cash settlement data converter 4. SCBML Convert to ratan cash settlement Json Util | | |
| 2 | ratanone-message-bridge | | 1. Set up connectivity with EDMI new topic for Uber consumption 2. Support failure message resend on byte[] 3. Provide Uber Serializer from byte[] to JSON 4. Key identifier on happy flow and replay flow | @Xinmiao Huang | 1. Uber integrate with EDMI and message consumption 2. Data Serialization to Ratan cash settlement json and message publishing 3. Failure message handing(message persistence, replay with correct key) | | |
| 3 | ratan-cash-settlement-standardization-service | | 1. Detail design and implementation to onboard Uber flow 1. Uber parsing, validation and data persistence 2. Identify cashflows to be processed, reuse the current group and group message table for UI requirement 3. Group management on identified cashflow and trade validation check on Uber level. 4. Cashflow stamping on Uber level before STP to workflow 5. Able to publish all required information in cashflow level. 2. Intent to Settle support filter out false element | @Xinmiao Huang | | Yes, New processing on UBER | |
| 4 | ratan-cash-settlement-orchestration | | 1. Decommission SCBML parsing and use java model RatanCashSettlementData instead 2. CamundaApiRequest and CamundaApiResponse change 3. Move workflow starter from foundation to orchestration 4. Refer to "Topic 2: Workflow Optimization" in **[Cash Settlement 2.0 Technical Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+2.0+Technical+Design) ** | @Chen Yang | 1. Inbound message processor(DuplicationProcessor, RawMessageProcessor) 2. Message parsing for inbound and outbound message (EntryRoute, Publisher) 3. Exception processing(ExceptionAssembleService) 4. Maker/Checker service(UserOperatorService) 5. Adhoc processing service(AdhocService) 6. Workflow internal variable(CommonEventEvaluateListener) 7. Workflow other listener(ParallelTaskListener, InitCashflowListener, AdhocSsiTaskListener) | No, Data model change only | |
| 5 | ratan-cash-settlement-ssi-stamping-service | | 1. Decommission SCBML parsing and use Java model RatanCashSettlementData instead 2. Remove SCBML SSI block template, set value to particular object directly after best matching/SSI exception approved/Adhoc SSI approved | @Quill Li | 1. /v1/stamping/cashflow/enrich API - Build Cashflow from UBER instead of SCBML - Change response to stamped UBER (StampScbmlCashflowService) - Change payload for updating cashflow status (CashFlowApiClient/CashFlowLifeCycleRequest 2. Adhoc ssi - Parse cashflow from UBER in CheckerConfirmedEventHandler 3. Historical data compatibility & migration - Add new type "UBER" to raw_message and store UBER json - Parse instance accroding to type | No, Data model change only | |
| 6 | ratan-cashflow-lifecycle-service | | 1. Decommission SCBML parsing and use Java model RatanCashSettlementData instead 2. Cashflow message data format change SCBML to JSON 3. Historical data adaptor - State machine processing on SCBML format should be compatible, once updated should convert to JSON format 4. Domain event format should change to common model 5. Generate SCBML before publishing to razor via template 6. Refer to "Topic 1: State machine Restructure" in **[Cash Settlement 2.0 Technical Design - Derivative Strategy Projects - Confluenc](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+2.0+Technical+Design)e** | @Xinmiao Huang | Many, that's why restructure required as well. | Yes, Restructure required | |
| 7 | ratan-nstp-service/ratanone-rule-engine | | 1. Decommission SCBML parsing and use Java model RatanCashSettlementData instead 2. Align rule engine model with common model in NSTP service if any gaps. | @Chongxuan Li | AbstractRuleServiceImpl IrsRuleServiceImpl NettingRuleServiceImpl NstpRuleServiceImpl | No, Data model change only | |
| 8 | ratan-cash-settlement-query-service | | 1. Decommission current JSON and SCBML parsing, use Java model RatanCashSettlementData instead when handle DomainEvent 2. Historical data adaptor - conversion between RatanCashSettlementData and CashflowData | @Chen Yang | 1. Domain event message parsing (ScbmlCashFlowFactory) 2. Xml mapping (XmlObjectFields, XPathXmlObjectMapper ) | No, Data model change only | |
| 9 | ratan-cash-settlement-netting-service | | 1. Netting resultant generation should use RatanCashSettlementData instead of SCBML template | @Fengke Wu | 1.NettingService 2.UnNettingService 3.NettingDomainService 4.Cashflow 5.NettedCashFlow DM for lifecycle、camunda、storage | No, Data model change only | |
| 10 | ratan-cash-settlement-lms-service | | 1. Domain event consuming - decommission SCBML parsing and use Java model RatanCashSettlementData instead 2. Inbound cashflow - decommission SCBML parsing and use Java model RatanCashSettlementData instead | @Fengke Wu | 1.LMSCashflowEvent 2.ScbmlCashflowCommand 3.LMSCashflowDomainEventEntrypoint 4.LMSCashflowMessageEntrypoint 5.LMSCashflowReleaseFacade 6.LMSMessageOperationTemplate 7.LMSCashflowPendingFacade 8.LMSCashflowTerminatedFacade 9.LMSKafkaMessageEntrypoint 10.? implements LMSRawMessageFilter(5) LMSBusinessEventRatanMessageFilter LMSInvalidEntityMessageFilter LMSJerseyEntityMessageFilter LMSProjectedFailedMessageFilter LMSStatusUpdateMessageFilter DM for get cashflow properties fiter valid message | No, Data model change only | |
| 11 | ratanone-swift-service | | 1. SCBML consuming - decommission SCBML parsing and use Java model RatanCashSettlementData instead 2. Conversion between current cashflow model and RatanCashSettlementData 3. Provide a Rest API for Swift Generation | @Mingyang Zhong | 1. only message received from workflow changed, just updating scbml parser to Uber parser is fine. MessageBridgeReceiver.handleReleasedPayment() | No, Data model change only | |
| 12 | ratan-cash-settlement-accounting-service | | 1. Domain event consuming - decommission SCBML parsing and use Java model RatanCashSettlementData instead 2. Conversion between current accounting model and RatanCashSettlementData | @Chongxuan Li | Read Json instead of SCBML: ReversalProcessorFilter NettedProcessorFilter NormalTaskServiceImpl <details> <summary>Expand Details</summary> CashflowDomainEventListener CashflowStatusEventFilter DomainEventStatusFilter EntityCheckEventFilter NewProcessorFilter ReversalProcessorFilter NettedEventProcessor NewEventProcessor ReversalEventProcessor NormalTaskServiceImpl PrecicousMetalEventFilter ProcessorDispatcher ReversalTaskServiceImpl </details> miss filed: reversalTag | No, Data model change only | |
| 13 | automation test code | | 1. Add automation script to support Uber 2. Update if any SCBML dependency | @Kuan Wang | | | |

# Appendix

## EDMI Topic creation

📎 [ProjectEngagement_Template-RATANONE.xlsx](attachments/ProjectEngagement_Template-RATANONE.xlsx)

📎 [RE RATAN moving to LM json - EDMI topic required.msg](attachments/RE RATAN moving to LM json - EDMI topic required.msg)

## Estimation

**EXPAND: Estimation Detail of 2 proposals**

| | | Processing Object | Proposal 1 | | Proposal 2 | |
| --- | --- | --- | --- | --- | --- | --- |
| | Component | Now | With UBER | | Estimation | | Estimation |
| Inbound | Message Bridge | SCBML | JSON | @Xinmiao Huang From the confluence above, TDSX publish bytes array into EDMI topic, MB need to convert the message if needs extract more information, shall we use their SDK or API? | 10 | | 10 |
| | Murex Adaptor | MXML → UBER Perhaps not change at this point Potentially payment will be missing to show on group blotter when the group is not completed | NA | | NA |
| | Group Service | 1. UBER convertor 2. Identify cashflows from UBER to be processed 3. Stella status write back change@Xinmiao Huang 1. Item 3 no need change from group service, the change in stella ambassador depends on Stella. 2. How to duplicate check uber message 3. Publish JSON format to workflow in cashflow level, so is it required to align with uber message format in cashflowData? 4. Is there any limitation on message payload size? | 30 | Same with proposal 1, but convert cashflow to SCBML | 50 |
| Workflow | Lifecycle Service | 1. Processing Object change to JSON on cashflow level 2. Camunda interfaces param to JSON Historical data transition would be a problem | 15 | NA | |
| | Camunda | 15 | NA | |
| | NSTP Service | 5 | NA | |
| | SSI Stamping Service | 15 | NA | |
| | Netting Service | 10 | NA | |
| | SWIFT Service | 5 | NA | |
| | Accounting Service | 5 | NA | |
| | Query Service | 5 | NA | |
| | Exception Platform | NA | 0 | NA | |
| Outbound | FMSGW | Change to JSON format, including ACK/NACK Downstream dependency, can be simplified if we do a reverse conversion to original message format. | 15 | NA | |
| | LMS | Change to JSON format, including ACK/NACK Downstream dependency, can be simplified if we do a reverse conversion to original message format. | 5 | NA | |
| | RAZOR | Change to JSON format, including ACK/NACK Downstream dependency, can be simplified if we do a reverse conversion to original message format. | 15 | NA | |
| Overall | | | | | 160 | | 60 |

**EXPAND_END**

## Detailed design

### How to use proto buffer

![](https://protobuf.dev/images/protocol-buffers-concepts.png)

### RATAN cashflow model schema

Apart from logical model fields defined in Rosetta, RATAN team additionally defines 122 fields as a supplemental for internal handling and downstream required.

Below table indicates whether the fields are still required or can be discarded after Uber integrated.

TBD: Put the entire fields here such as proto files.

### Ratan Supplemental Fields

<details>
<summary>Expand Details</summary>

| Additional Fields Defined By Ratan | Context: CASHFLOW_DATA? | | | | |
| --- | --- | --- | --- | --- | --- |
| Level1 Path | Level2 Path | Level3 Path | Exist in Rosetta | Exist in Uber Schema | Field Status | Strategic Settlement Internal Required | Comments |
| BCS_Trade_Id | | | | | | NO | Remove duplicate |
| Effective_Date_Time | | | | | | | Remove duplicate |
| Linked_Trade_ID | | | | | | NO | Remove useless |
| TP_System_Name | | | | | | | Remove duplicate |
| Trade_Date | | | | | | | Redundant of Trade |
| Trade_Original_Source_System_Name | | | | | | | Remove duplicate |
| Trade_Purpose | | | | | | | Remove duplicate |
| Trade_Version | | | | | | | Remove duplicate |
| Cashflow | Booking_System_Event | | | | | YES | |
| | Bypass_Workflow_Indicator | | | | | | |
| | Cashflow_Affirmation_Status | | | | | | Remove duplicate |
| | Cashflow_Event_Reason | | | | | YES | |
| | Cashflow_SubEvent_Type | | | | | | Remove duplicate |
| | Clearing_Alpha | | | | | YES for Murex | |
| | Duplicate_NDS_FXD | | | | | YES for Murex | |
| | Exception_Reason | | | | | | |
| | Execution_Date_Time | | | | | There is same field defined in parent level | Use correct field |
| | General_Ledger_Owner_Id | | | | | | Remove duplicate |
| | Is_Adhoc_Net | | | | | | |
| | Is_Amended_Post_Settlement | | | | | | Remove duplicate |
| | Is_Cashflow_Reinstate | | | | | YES | |
| | Is_Cashflow_SettleAsGross | | | | | YES | |
| | Is_Cashflow_Swift_Unsuppress | | | | | | |
| | Is_Cashflow_Unnet | | | | | | Remove duplicate |
| | Is_Cashflow_Unsuppress | | | | | | |
| | Is_Commodity | | | | | YES for Murex | |
| | Is_Netting_Required | | | | | | Remove duplicate |
| | Is_Pending_Fixing | | | | | Np | Remove duplicate |
| | Is_Private_Banking_Cashflow | | | | | | Remove duplicate |
| | Is_STP | | | | | | Remove duplicate |
| | Is_STP_RATAN | | | | | Is_STP | Remove duplicate |
| | Is_Withdrawal_On_Component | | | | | YES | |
| | Lien_Monitoring | | | | | YES for Murex | |
| | Murex_Structure_Id | | | | | YES for Murex | |
| | ND_Parent_Trade_Id | | | | | YES for Murex | |
| | ND_Parent_Typology | | | | | YES for Murex | |
| | NSTP_Reason | | | | | ? | |
| | Netting_Id | | | | | | Remove duplicate |
| | Parent_Cashflow_State | | | | | YES | |
| | Payer_Name | | | | | | Remove duplicate |
| | Pending_Fixing_Flag | | | | | YES for Murex | |
| | Transaction_Details | | | | | NO | Remove useless |
| Entity | Booking_Entity_Country_ISO_Code | | | | | | Remove duplicate |
| | Booking_Entity_SCI_FMCODE | | | | | YES | |
| | Counterparty_Client_Type | | | | | YES | |
| | Counterparty_Is_Internal | | | | | YES | |
| | Counterparty_Murex_Display_Shortcode | | | | | YES for Murex | |
| | Counterparty_SCI_BIC_Code | | | | | YES | |
| | Counterparty_SCI_BIC_Net_Flag | | | | | YES | |
| | Counterparty_SCI_DOMICILE_COUNTRY | | | | | YES | |
| | Counterparty_SCI_FMCODE | | | | | YES | |
| | Person | Event_Booking_Marketer_PSID | | | | Booking_Marketer_PSID | Use correct field |
| | | Event_Coverage_Marketer_PSID | | | | Coverage_Marketer_PSID | Use correct field |
| | | Event_Execution_Marketer_PSID | | | | Execution_Marketer_PSID | Use correct field |
| | | Event_Trader_PSID | | | | Trader_PSID | Use correct field |
| Instrument_Common | CFI_Code | | | | | | Remove duplicate |
| | Murex_Product_Family | | | | | YES for Murex | |
| | Murex_Product_Group | | | | | YES for Murex | |
| | Murex_Product_Strategy | | | | | YES for Murex | |
| | Murex_Product_Type | | | | | YES for Murex | |
| | Murex_Product_Typology | | | | | YES for Murex | |
| Portfolio | Booking_Entity_Trade_Portfolio_Name | | | | | | Remove duplicate |
| Settlement_Instruction | Account | Beneficiary_Account_Name | | | | | |
| | | Beneficiary_Account_Name_2 | | | | | |
| | | Beneficiary_Account_Number | | | | | |
| | | Beneficiary_BIC_code | | | | | |
| | | Beneficiary_Bank_Account_Name | | | | | |
| | | Beneficiary_Bank_Account_Number | | | | | |
| | | Beneficiary_Bank_BIC_code | | | | | |
| | | Beneficiary_Bank_City | | | | | |
| | | Beneficiary_Bank_Street_Address | | | | | |
| | | Beneficiary_City | | | | | |
| | | Beneficiary_Correspondent_Account_Name | | | | | |
| | | Beneficiary_Correspondent_Account_Number | | | | | |
| | | Beneficiary_Correspondent_BIC_code | | | | | |
| | | Beneficiary_Correspondent_City | | | | | |
| | | Beneficiary_Correspondent_Street_Address | | | | | |
| | | Beneficiary_Street_Address | | | | | |
| | | Booking_Entity_Correspondent_Account_Name | | | | | |
| | | Booking_Entity_Correspondent_Account_Number | | | | | |
| | | Booking_Entity_Correspondent_BIC_code | | | | | |
| | | Booking_Entity_Correspondent_City | | | | | |
| | | Booking_Entity_Correspondent_Street_Address | | | | | |
| | | Counterparty_CMS_Account_Number | | | | | |
| | | EBBS_Account_Number | | | | | |
| | | EBBS_Bridge_Account_Number | | | | | |
| | | Intermediary_Account_Name | | | | | |
| | | Intermediary_Account_Number | | | | | |
| | | Intermediary_BIC_code | | | | | |
| | | Intermediary_City | | | | | |
| | | Intermediary_Street_Address | | | | | |
| | | Ordering_Customer_Account_Name | | | | | |
| | | Ordering_Customer_Account_Number | | | | | |
| | | Ordering_Customer_BIC_Code | | | | | |
| | | Ordering_Customer_City | | | | | |
| | | Ordering_Customer_Street_Address | | | | | |
| | | SCB_Nostro_Account_Number | | | | | |
| | | SCB_Nostro_Account_Type | | | | | |
| | Charge_Bearer | | | | | | |
| | Is_Third_Party_Payment | | | | | | |
| | Nostro_Id | | | | | | |
| | Nostro_Swift_Message_Type | | | | | | |
| | Remittance_Information_1 | | | | | | |
| | Remittance_Information_2 | | | | | | |
| | Remittance_Information_3 | | | | | | |
| | Remittance_Information_4 | | | | | | |
| | SSI_Id | | | | | | |
| | SSI_Priority | | | | | | |
| | SSI_Source | | | | | | |
| | SSI_Unique_Id | | | | | | |
| | Sender_To_Receiver_Information_1 | | | | | | |
| | Sender_To_Receiver_Information_2 | | | | | | |
| | Sender_To_Receiver_Information_3 | | | | | | |
| | Sender_To_Receiver_Information_4 | | | | | | |
| | Sender_To_Receiver_Information_5 | | | | | | |
| | Sender_To_Receiver_Information_6 | | | | | | |
| | Settlement_Method | | | | | | |
| | Swift_Message_Type | | | | | | |
| | Swift_Payment_Date | | | | | | |
| | Swift_Payment_Method | | | | | | |
| | Value_Date | | | | | | |
| | Value_Date_Business_Day_Convention | | | | | | |

</details>

## Data Analysis & Limitation

<details>
<summary>Expand Details</summary>

| | Issue Type | Observation | Impact | Sample Data |
| --- | --- | --- | --- | --- |
| 1 | Data extraction | Data in UBER are all Arrays | | ![image-2025-3-21_15-25-6.png](attachments/image-2025-3-21_15-25-6.png) |
| 2 | Cashflow identification | No straight way to find out impacted cashflows, can only compare with last version. | | |
| 3 | Cashflow identification | For Trade status (Validated/Confirmed) which drive payments STP, the UBER will show "Hash_Change.Cashflow: **false**" | | ![image-2025-3-21_15-30-51.png](attachments/image-2025-3-21_15-30-51.png) |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |

</details>

## Uber and Proto Buffer Comparation

Since Ratan has to extend from the standard data model for internal settlement processing, then a unified data type must be agreed. There are two data types for service interaction, JSON and Protocol Buffers.

| | JSON | Protocol Buffers(Protobuf) |
| --- | --- | --- |
| Data Format | Text-based | - [x] Binary |
| Readability | - [x] Human-readable | Not Human-readable |
| Serialization/Deserialization Speed | Slower | - [x] Faster |
| Data Size | Larger | - [x] Smaller |
| Schema | Optional | - [x] Required |
| Compatibility | Not compatible if name changed | - [x] Supports backward and forward compatibility |
| Tooling | - [x] Minimal setup required | Requires .proto file and code generation |

![](https://images.ctfassets.net/23aumh6u8s0i/7fE582myNrMvGWhM0xUcLb/ab87c994b0321433417acc25f2c4381e/java-times)

## Fields are configurable

Since the Logic Model contains lots of fields (3000+), in case most of trade fields are not required by Ratan, upstream is able to provide al filter which will filter unnecessary fields out according to downstream requirements, Integration logical diagram should be:

Highlight points from the diagram:

- There will be a new topic for Uber message from TDSX → RATAN(See attachment **3.1 EDMI Topic creation**)

| v1/post-trade/29126-sabre-fmrptdsx/enricher/protobuf-1.0/uber-msg/ratanone/pub | q-51358-ratanone-uber-msg |
| --- | --- |
| v1/post-trade/51358-ratanone/tdsx/protobuf-1.0/tech/-/pub/ack | q-29126-sabre-fmrptdsx-enricher-uber-msg-ratanone-res |

- Filter is supposed to mask the useless fields to empty to reduce the payload size. If there is no black/white list, entire data will be published. **(TBD)**
- TDSX SDK is exactly follow the DM standard, any additional data should be maintained by the application itself.

# Reference document:

[Beating JSON performance with Protobuf](https://auth0.com/blog/beating-json-performance-with-protobuf/)

[Protocol Buffers Documentation](https://protobuf.dev/)