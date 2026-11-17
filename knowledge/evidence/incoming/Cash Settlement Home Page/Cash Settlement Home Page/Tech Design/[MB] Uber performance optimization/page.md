# 1，background

In the prod environment, it was found that when a large number of IRS Uber messages entered the MB, the processing time reached 100-350ms. This meant that only 3-6 messages could be consumed per second, resulting in a large backlog of messages in the Solace queue, which had a significant impact.

# 2，Bottleneck Analysis

Preliminary analysis suggests that MB performs **multiple protobuf to JSON conversions **when processing Uber messages to obtain information such as tradeId, version, and sender. When Uber messages are very large, the overall processing time becomes extremely high.

Each time MessageBridgeCommonUtils.parserJsonValue(...)` / `parserJsonValueSupportArray(...) is called to retrieve attribute values, the following operations are performed:

1. Call `serializer.serialize(KAFKA_UBER_FLOW, exchangeBody)`

2. In `TDSXUberToJsonSerializer:

- Deserialize using protobuf

- Convert to JSON

- Compact the JSON again

3. Then call `ObjectMapper.readTree(...)`

4. Retrieve fields by path

4.1 Uber Message Duplicate Parsing

a）Preprocessing：

`UberKafkaKeyProcessor` - Retrieves `tradeId`: 1 time

`UberMarketOperationProcessor` - Retrieves `tradeId`, `marketOperation`, total: 2 times

`UberMessageSenderProcessor` - Retrieves `tradeId`, `sender`, total: 2 times

`UberMessageVersionProcessor` - Retrieves `tradeId`, `version`, total: **2 times**

Total 1 + 2 + 2 + 2 = at least 7 complete parsing operations.

b）After suppression, ExchangeUberBodySuppressProcessor will perform the following additional operations:

- Retrieve the `tradeId` once

- Retrieve the field once for each JSON rule

at least 1 + 1 per suppression rule.

c）Adding the final Kafka send, the Kafka target uses TDSXUberToJsonSerializer, which will perform another 1 complete protobuf -> JSON processing operations during sending.

Therefore, the total number of operations becomes: at least 9 + 1 per suppression rule.

When dealing with large messages, repeated parsing significantly amplifies hotspot overhead.

# 3，Optimization plan

## 3.1，Modify Uber messages to "single-time parsing, multiple-use"

a）At the very beginning of Uber Flow's preprocessing, the original protobuf body is converted in one go to:

- JSON string

- JsonNode

- and commonly used fields（tradeId, version, sender ）

for example:

TDSXUberMessage msg = TDSXUberMessage.parseFrom(bytes);
String json = TdsxJsonFormat.printer().omittingInsignificantWhitespace().print(msg);
JsonNode root = MAPPER.readTree(json);

exchange.setProperty("UBER_JSON_STRING", json);
exchange.setProperty("UBER_JSON_NODE", root);
exchange.setProperty(MessageBridgeConstants.MESSAGE_TRADE_ID_PROPERTY,
JsonParser.getValueByPath(root, "TDS3Data.tradeRecord.Trade_Id"));
exchange.setProperty(MessageBridgeConstants.MESSAGE_SENDER_PROPERTY,
JsonParser.getValueByPath(root, "TDS3Data.tradeRecord.Data_Flow.Data_Sender"));
exchange.setProperty(MessageBridgeConstants.MESSAGE_VERSION_PROPERTY,
JsonParser.getValueByPath(root, "TDS3Data.tradeRecord.Trade_Lake_Trade_Major_Version"));
exchange.setProperty(MessageBridgeConstants.MESSAGE_MARKET_OPERATION_PROPERTY,
JsonParser.getValueByPath(root, "TDS3Data.tradeRecord.Last_Action_Type"));

b）Processing merged metadata，Use the data that has already been parsed above directly.

String tradeId = exchange.getProperty(MessageBridgeConstants.MESSAGE_TRADE_ID_PROPERTY, String.class);
String sender = exchange.getProperty(MessageBridgeConstants.MESSAGE_SENDER_PROPERTY, String.class);
String version = exchange.getProperty(MessageBridgeConstants.MESSAGE_VERSION_PROPERTY, String.class);
String operation = exchange.getProperty(MessageBridgeConstants.MESSAGE_MARKET_OPERATION_PROPERTY, String.class);

if (StringUtils.isNotBlank(tradeId)) {
exchange.getIn().setHeader(KafkaConstants.KEY, tradeId);
}
if (StringUtils.isNotBlank(sender)) {
exchange.setProperty(MessageBridgeConstants.MESSAGE_SENDER_PROPERTY, sender);
}
if (StringUtils.isNotBlank(version)) {
exchange.setProperty(MessageBridgeConstants.MESSAGE_VERSION_PROPERTY, version);
}
if (StringUtils.isNotBlank(operation)) {
exchange.setProperty(MessageBridgeConstants.MESSAGE_MARKET_OPERATION_PROPERTY, operation);
}

c）UberSuppressProcessor reuses already parsed fields

JsonNode root = exchange.getProperty("UBER_JSON_NODE", JsonNode.class);
String tradeId = exchange.getProperty(MessageBridgeConstants.MESSAGE_TRADE_ID_PROPERTY, String.class);

for (Entry<Integer, String> rule : rules.entrySet()) {
String jsonPath = StringUtils.trim(rule.getValue());
String jsonValue = JsonParser.getValueByPath(root, jsonPath);
// ... Existing verification logic
}

## 3.2，Optimize the internal implementation of `TDSXUberToJsonSerializer`

The current implementation performs the following steps: protobuf -> JSON string -> ObjectMapper parse -> ObjectMapper write compact JSON.

String uberJson = ProtobufUtils.toJson(tdsxUberMessage);
String targetJson = MessageBridgeCommonUtils.compactJson(uberJson);
return StringUtils.isNotEmpty(targetJson) ? targetJson.getBytes(StandardCharsets.UTF_8) : null;

Output compact JSON directly, instead of "outputting first and then compressing it again".
TDSXUberMessage message = TDSXUberMessage.parseFrom(byteArr);
String json = TdsxJsonFormat.printer().omittingInsignificantWhitespace().print(message);
return json.getBytes(StandardCharsets.UTF_8);

The advantage is that each serializer call reduces the number of complete JSON parse/write operations by one.

## 3.3，The Uber filter logic has been taken offline and replaced by the group service.

Uber messages are no longer filtered by ExchangeUberBodySuppressProcessor; all Uber messages are sent to the group service, which filters the necessary Uber messages.

## 3.4， Generate JSON in advance and store it in the exchange; reuse it directly when sending messages without calling TDSXUberToJsonSerializer again.

old db config: tdsx_uber_message_json_inbound_interestrate?valueSerializer=com.scb.ratan.messagebridge.serial.TDSXUberToJsonSerializer

new db config: tdsx_uber_message_json_inbound_interestrate

Generate JSON in advance and store it in the exchange