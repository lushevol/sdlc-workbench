# Observed issue

We've found lots of error log:

![image-2026-4-9_14-55-49.png](attachments/image-2026-4-9_14-55-49.png)

The stack trace:

```java
java.lang.IllegalArgumentException: User must not be null
	at org.springframework.util.Assert.notNull(Assert.java:181)
	at org.springframework.messaging.simp.SimpMessagingTemplate.convertAndSendToUser(SimpMessagingTemplate.java:225)
	at org.springframework.messaging.simp.SimpMessagingTemplate.convertAndSendToUser(SimpMessagingTemplate.java:217)
	at org.springframework.messaging.simp.SimpMessagingTemplate.convertAndSendToUser(SimpMessagingTemplate.java:203)
	at com.scb.ratan.ratanone.query.notify.websocket.controller.QueryServiceWebBroker.onMessage(QueryServiceWebBroker.java:42)
	...
	at java.util.concurrent.CompletableFuture$AsyncRun.run(CompletableFuture.java:1804)
	at java.lang.Thread.run(Thread.java:833)
```

# Direct Impacts

- In cashflow blotter, user will possibility lose some cashflow notice.
- Too many error logs might produce heavy pressure to log infra

# Context

We've released data-entitlement control in cashflow notification, which requires the frontend to subscribe the cashflow by user, and in backend when send notice to user, we'll check one by one.

Though CES is currently disabled, we're still send to user one by one, and just bypassed the data entitlement checking.

In 9th Apr, we've received around 10,000+ cashflows.

# Issue analysis

The exception is thrown when we send the cashflow notice to user WS session:

```java
@KafkaListener(topics = "${settlement-query-service.notify.topics.cashflow-update-notify}", groupId = GROUP_ID_SPEL, batch = "false", concurrency = "36")
public void onMessage(ConsumerRecord<String, String> consumerRecord) {
    String event = consumerRecord.value();
    log.debug("Received cashflow changed notification: {}", event);

    String topic = "/cashflow/notification";
    int count = webSocketSessionHandler.getActiveSessionCount();
    for (QueryServiceWebSocketSession session : webSocketSessionHandler.getAllSessions()) {
        try {
            log.info("Sent cashflowNotice to topic={}, user={} total:{}", topic, session.getName(), count);
            messagingTemplate.convertAndSendToUser(session.getName(), topic, event); // --> this line will throw is session.getName() is null
        } catch (Exception e) {
            log.error("Failed to handle with cashflow update Event: {}", event, e);
        }
    }
}
```

We can confirm that, in some case `session.getName()` is null and this is the direct cause of this issue:

![image-2026-4-9_15-7-47.png](attachments/image-2026-4-9_15-7-47.png)

Normally, this user name is parsed in AuthInboundChannelInterceptor.java:

![image-2026-4-9_15-9-50.png](attachments/image-2026-4-9_15-9-50.png)

So there're a few possibilities that this value is not set:

1. If some token does not contain valid sub
2. Somehow the interceptor invoked but failed
3. This interceptor is not invoked

By searching the log, we can confirm that all tokens are valid with sub:

![image-2026-4-9_15-12-14.png](attachments/image-2026-4-9_15-12-14.png)

![image-2026-4-9_15-13-18.png](attachments/image-2026-4-9_15-13-18.png)

So 1) could be eliminated. By checking if somehow we got exception during parsing, we can exclude 2) as there's no error record:

![image-2026-4-9_15-15-55.png](attachments/image-2026-4-9_15-15-55.png)

So the only possibility is that, in some case the session is created but this interceptor is not triggered. Notice that this interceptor will only be executed in "CONNECT" event.

![image-2026-4-9_15-17-56.png](attachments/image-2026-4-9_15-17-56.png)

Below is the session creation logic:

![image-2026-4-9_15-19-21.png](attachments/image-2026-4-9_15-19-21.png)

By checking the logs, we can confirm that some session with null user is created:

![image-2026-4-9_15-20-3.png](attachments/image-2026-4-9_15-20-3.png)

Going further, if we check the logs of specific sessions, we may notice that a session with same sessionId but empty user is created right after the session is removed. This however, causes the problem.

![image-2026-4-9_15-21-32.png](attachments/image-2026-4-9_15-21-32.png)

![image-2026-4-9_15-22-9.png](attachments/image-2026-4-9_15-22-9.png)

# Root cause

### Trigger: Buffer overflow disconnect

The SockJS send buffer limit is set to **1MB** in `WebSocketConfig`:
`registration.setSendBufferSizeLimit(1024 * 1024);
`
With **36 concurrent Kafka listener threads** all calling `convertAndSendToUser()` simultaneously, a slow or backgrounded client's buffer fills and overflows, causing a forced disconnect.

### Race condition: Outbound channel vs. Disconnect handler

`convertAndSendToUser()` is non-blocking — it enqueues messages onto the `ClientOutboundChannel` thread pool and returns immediately. This creates a race between two threads:

| Thread C — Disconnect Handler | Thread B — Outbound Channel |
| --- | --- |
| `SessionDisconnectEvent` fires | Processes a message queued *before* disconnect |
| `removeSession(k0kcvcp1)` → map is now empty | `preSend()` runs in `DataEntitlementOutboundChannelInterceptor` |
| ✅ Session correctly removed | Calls `getSession({sessionId=k0kcvcp1})` ← **create-if-not-exists!** |
| | Session not found → **creates `{sessionId=k0kcvcp1, name=null}` and stores it** ❌ |

### The zombie session accumulates forever

The disconnect event **already fired** — no future event will call `removeSession()` for this zombie. It grows in the map indefinitely.

### Compounding loop

On every subsequent Kafka event:

1. `getAllSessions()` returns the zombie
2. `convertAndSendToUser(null, ...)` is called
3. Spring throws an exception on `null` user
4. Try-catch swallows it silently
5. Repeat forever — and each new buffer-overflow disconnect adds another zombie

### The buggy code

**File:** `DataEntitlementOutboundChannelInterceptor.java`
`// getSession() has create-if-not-exists semantics
QueryServiceWebSocketSession webSocketSession = QueryServiceWebSocketSession.builder()
.sessionId(accessor.getSessionId())
.build(); // name = null
webSocketSession = webSocketSessionHandler.getSession(webSocketSession); // ← creates zombie
`
`WebSocketSessionHandler.getSession()`:
`} else {
sessions.put(sessionId, session); // ← stores the null-name zombie!
log.info("Created new session: {} for user: {}", sessionId, session.getName());
return session;
}`
**![image-2026-4-9_22-0-44.png](attachments/image-2026-4-9_22-0-44.png)**

# Reproduce the issue

1. trigger 500 + cashflows
2. observed that session removed, and outbound interceptor cannot get the session
3. the client only received 109 cashflows and then got error 4500
4. the client then reconnect, but other cashflows cannot be received

![image-2026-4-10_16-59-26.png](attachments/image-2026-4-10_16-59-26.png)

| Buffer size | Received cashflows in client | |
| --- | --- | --- |
| 1Mb | 60 | |
| 2Mb | 109 | |
| 4mb | 75/95/101 | |

# Proposed fix

**File:** `DataEntitlementOutboundChannelInterceptor.java`

Replace `getSession()` (create-if-not-exists) with `getSessionById()` (pure lookup). If the session is gone, drop the message — the client is already disconnected.
`// BEFORE
QueryServiceWebSocketSession webSocketSession = QueryServiceWebSocketSession.builder()
.sessionId(accessor.getSessionId())
.build();
webSocketSession = webSocketSessionHandler.getSession(webSocketSession);

// AFTER
QueryServiceWebSocketSession webSocketSession = webSocketSessionHandler.getSessionById(accessor.getSessionId());
if (webSocketSession == null) {
log.warn("Session {} already disconnected, dropping outbound message", accessor.getSessionId());
return null;
}
`
`getSessionById()` already exists in `WebSocketSessionHandler` as a plain `sessions.get(sessionId)` — no code changes needed there.

## Additional Recommendation

Increase the send buffer limit in `WebSocketConfig` to reduce frequency of buffer-overflow disconnects:
`// BEFORE
registration.setSendBufferSizeLimit(1024 * 1024); // 1MB

// AFTER
registration.setSendBufferSizeLimit(4 * 1024 * 1024); // 4MB
`
> This does not eliminate the race condition — it only reduces how often it is triggered. The interceptor fix above is the primary fix.

| Metric | Before Fix | After Fix |
| --- | --- | --- |
| Zombie sessions in map | Accumulates indefinitely | None created |
| `total` in broadcast log | Inflated, grows over time | Reflects real active users only |
| `user=null` log errors | Every Kafka event × zombie count | Eliminated |
| CPU waste | Iterating + entitlement-checking dead sessions | Eliminated |

3. Check if frontend will re-connect automatically (Yes)

![image-2026-4-9_15-54-54.png](attachments/image-2026-4-9_15-54-54.png)