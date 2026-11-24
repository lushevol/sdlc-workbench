Analysis of the problem of missing traceId in logs

# **1，Background**

When checking the logs, it was found that the traceId field was not displayed, and the problem also existed in prod. See the image below

![image-2026-3-23_11-33-16.png](attachments/image-2026-3-23_11-33-16.png)

The classes involved are as follows, these classes mainly involve camel's asynchronous processing logic, such as SuppressionRoute, SplittingRoute, and DispatchRoute. In addition, there is asynchronous message processing EventProducerRoute, as well as thread pools, which cause log query gaps and seriously affect the query of the entire message chain.

all of which are related to messages：

com.scb.ratan.messagebridge.route.producer.SuppressionRouteBuilder

com.scb.ratan.messagebridge.route.producer.EventProducerRoute

com.scb.ratan.messagebridge.processor.suppression.ExchangeUberBodySuppressProcessor

com.scb.ratan.messagebridge.route.producer.MessageProducerImpl

com.scb.ratan.messagebridge.processor.suppression.BaseSuppressProcessor

com.scb.ratan.messagebridge.route.producer.TargetSplittingRoute

com.scb.ratan.messagebridge.processor.suppression.ExchangeBodySuppressProcessor

com.scb.ratan.messagebridge.destination.SolaceDestinationResolver

com.scb.ratan.messagebridge.route.producer.DispatchProducerRoute

# **2，Problem Analysis**

2.1，`MDC` (Mapped Diagnostic Context) is thread-local storage, and traceId loss can occur in the following scenarios:

| | Scene | Reason | Related classes |
| --- | --- | --- | --- |
| 1 | Split message | Camel assigns each split sub-message to a different thread. | com.scb.ratan.messagebridge.route.producer.TargetSplittingRoute#parallelProcessing() |
| 2 | asynchronous threads | Use Spring's `@Async` independent thread pool | com.scb.ratan.messagebridge.route.producer.EventProducerRoute |
| 3 | Scheduled task thread | Ues @Scheduled | TargetDestinationStatusDetector |
| 4 | Other asynchronous logic | CompletableFuture.runAsync() | com.scb.ratan.messagebridge.route.producer.DispatchProducerRoute |

2.2，Potential gaps

Message arrived         Empty Body Branch
    ↓                                  ↓
MessageInboundPropertyCustomizationProcessor         ← MDC does not yet have traceId
ImsIntegrationProcessor                                                  ← MDC does not yet have traceId
setProperty(MESSAGE_RECEIVED_TIMESTAMP)               ← MDC does not yet have traceId
    ↓
[Empty Body?]──yes──> This only retrieves the trackingId from the Header and writes it to the Exchange Property, but MDC.put() is never called ← Gap ①

↓ otherwise
trackingIdProcessor                                                          ← This is where MDC.put("traceId", ...) is called.
    ↓
preProcessors (TargetRouteProcessor )
    ↓
direct:targetSplittingRoute
    ↓
split().parallelProcessing()                                                 ← Parallel sub-threads, MDC does not automatically inherit ← Gap ②
    ↓
direct:suppressionRoute → direct:dispatchRoute
    ↓
MessageProducerImpl.sendBody()                                   ← Manually enter the trackingId, but the MDC may have been lost.
    ↓
EventProducerRoute（@Async thread）                          ← New thread, MDC completely lost ← Gap ③
    ↓
TargetDestinationStatusDetector（Scheduled task thread）    ← MDC completely lost ← Gap④

2.3，Existing mechanisms

| | class | code | effect |
| --- | --- | --- | --- |
| 1 | TrackingIdProcessor.process() | MDC.put("traceId", trackingId) | Write to MDC after the message enters the otherwise branch. |
| 2 | AbstractConsumerClientRouteBuilder#initRoute() | .process(trackingIdProcessor) | Call the processor above |
| 3 | | | |

# **3，Solution**

3.1，Camel MDC Logging, and Use `slf4j.MDC` uniformly.

Camel has a built-in `useMDCLogging` switch. When enabled, Camel automatically writes Exchange-related properties to the MDC and automatically transfers the MDC context during thread switching (including `parallelProcessing`).

// MessageBridgeApplication.java
@Override
public void afterPropertiesSet() throws Exception {
    if (this.camelContext != null) {
        this.camelContext.setNameStrategy(new DefaultCamelContextNameStrategy("Message-Bridge-CamelContext"));
        this.camelContext.getExecutorServiceManager().setThreadNamePattern("CamelThread-##counter#");
        this.camelContext.setMessageHistory(false);

// ① Enable Camel MDC logging to automatically synchronize Exchange properties to the MDC.
        this.camelContext.setUseMDCLogging(true);
        // ② Specify which Exchange Properties need to be synchronized to MDC
        this.camelContext.setMDCLoggingKeysPattern("traceId,trackingId,flowName");
    }
}

The current code in TrackingIdProcessor uses `org.jboss.logging.MDC`, which needs to be changed to the standard `org.slf4j.MDC`.

3.2，Write a temporary traceId in advance at the very beginning of the consumer routing

// AbstractConsumerClientRouteBuilder.initRoute() 
from(camelRoute).noAutoStartup().routeId(routeId).startupOrder(StartOrderLevel.SECOND.order())
    .log(...)
    // Immediately after receiving a message, the route generates a temporary traceId and writes it to the Exchange Property.
    // Subsequently, the TrackingIdProcessor will overwrite it with the actual trackingId from the message.
    .process(exchange -> {
        String earlyTraceId = exchange.getIn().getHeader("JMSMessageID", String.class);
        if (earlyTraceId == null) {
            earlyTraceId = exchange.getIn().getHeader(KafkaConstants.OFFSET,
                    exchange.getExchangeId(), Object.class).toString();
        }
        exchange.setProperty("traceId", earlyTraceId);
        MDC.put("traceId", earlyTraceId);
    })
    .setProperty(IGNORE_SOURCE_RAW_MESSAGE_PROPERTY, ...)
```

3.3，Solving the problem of MDC loss after parallel splitting

In `TargetSplittingRoute.EndpointSplitter.splitTargetEndpoint()`, write the `traceId` to the header of each split sub-message, and restore MDC at the `direct:suppressionRoute` entry point.

// TargetSplittingRoute.EndpointSplitter
for (TargetEndpoint endpoint : endpointProperty) {
    DefaultMessage message = new DefaultMessage(camelContext);
    message.setHeaders(new HashMap<>(exchange.getIn().getHeaders()));
    // Pass traceId into sub-message
    message.setHeader("traceId", exchange.getProperty("traceId", String.class));
    message.setHeader(BRIDGE_FLOW_ID, endpoint.getTarget().getItemId());
}

Restore MDC at the beginning of `SuppressionRouteBuilder.selfConfigure()` route:

from(MessageBridgeConstants.DIRECT_SUPPRESSION_ROUTE)
    .routeId(thisRouteBuilderId())
    .startupOrder(StartOrderLevel.FIRST.order())
    // Sub-thread recovery MDC traceId
    .process(exchange -> {
        String traceId = exchange.getIn().getHeader("traceId", String.class);
        if (traceId != null) {
            MDC.put("traceId", traceId);
            exchange.setProperty("traceId", traceId);
        }
    }).id("restoreMdcTraceIdProcessor")
    .process(exchange -> {
        final TargetEndpoint targetEndpoint = ...;
        [log.info](http://log.info)("...");
    }).id("suppressionMsgInLogProcessor")

3.4，Resolving the issue of lost MDC for @Async threads

Modify `MessageBridgeApplication.EventAsyncConfigurer` to use a thread pool that can propagate MDC:

@Component
public static class EventAsyncConfigurer implements AsyncConfigurer {

@Override
    public Executor getAsyncExecutor() {
        // Wrap the thread with an MDC-aware TaskDecorator to ensure that the @Async thread inherits the MDC of the calling thread.
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setTaskDecorator(runnable -> {
            // Capture the current MDC when submitting a task
            Map<String, String> mdcContext = MDC.getCopyOfContextMap();
            return () -> {
                // Restore MDC while performing tasks
                if (mdcContext != null) {
                    MDC.setContextMap(mdcContext);
                }
                try {
                    runnable.run();
                } finally {
                    MDC.clear();
                }
            };
        });
        executor.setThreadNamePrefix("EventThread-");
        executor.initialize();
        return executor;
    }
}

# 4，Evidence

4.1, uber

env: uat4

![image-2026-3-24_16-58-24.png](attachments/image-2026-3-24_16-58-24.png)

![image-2026-3-24_16-56-50.png](attachments/image-2026-3-24_16-56-50.png)

4.2, scbml

env: fmrp1

![image-2026-3-25_17-40-45.png](attachments/image-2026-3-25_17-40-45.png)

![image-2026-3-25_17-41-48.png](attachments/image-2026-3-25_17-41-48.png)

![image-2026-3-25_17-43-0.png](attachments/image-2026-3-25_17-43-0.png)

4.3, fxu

env: uat4

![image-2026-3-24_17-11-45.png](attachments/image-2026-3-24_17-11-45.png)