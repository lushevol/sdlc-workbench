# Implemented Capabilities (Based on Current Code State)

## 1.1 Dynamic Routing and Route Management

- Routes are dynamically generated from the `OpenApi` model: `src/main/java/com/scb/ratan/gateway/core/OpenApiRouteDefinitionLocator.java`
- Route configuration sources include:
 - Local configuration: `ratanone.api-gateway.open-apis`
 - Redis storage: `src/main/java/com/scb/ratan/gateway/api/repository/RedisOpenApiRepository.java`
- Management APIs are available for querying, publishing, and deleting OpenApi definitions: `src/main/java/com/scb/ratan/gateway/management/OpenApiManagementController.java`
- In Kubernetes deployments, route refresh is supported through Redis Pub/Sub: `src/main/java/com/scb/ratan/gateway/api/refresh/RedisPubSubOpenApiRefresher.java`

## 1.2 Security, Authentication and Authorization (AuthN/AuthZ)

- Token validation for management APIs: `src/main/java/com/scb/ratan/gateway/management/OpenApiManagementSecurityFilter.java`
- ACL-based authorization filter for business APIs: `src/main/java/com/scb/ratan/gateway/filter/factory/OpenApiAclGatewayFilterFactory.java`
- Token validation via authentication service endpoint `/v3/authenticate`: `src/main/java/com/scb/ratan/gateway/security/TokenAuthenticationService.java`

## 1.3 Auditing and Tracing

- Audit filter implementation: `src/main/java/com/scb/ratan/gateway/filter/factory/OpenApiAuditGatewayFilterFactory.java`
- Audit events are published to Kafka: `src/main/java/com/scb/ratan/gateway/audit/KafkaOpenApiAuditService.java`
- Trace context injection: `src/main/java/com/scb/ratan/gateway/filter/factory/OpenApiTraceGatewayFilterFactory.java`

## 1.4 Baseline Dependencies for Circuit Breaker and Rate Limiting

- Resilience4j dependency is already included: `pom.xml`
- Global default filter includes `CircuitBreaker`: `src/main/resources/application.yml`
- Route-level `rateLimiter` structure is present and can assemble `RequestRateLimiter`:
 - `src/main/java/com/scb/ratan/gateway/api/repository/OpenApiRateLimiter.java`
 - `src/main/java/com/scb/ratan/gateway/core/OpenApiRouteDefinitionLocator.java`

# Current Gaps and Risks

## 2.1 Missing Fallback Handling Capability (Critical)

- No explicit `fallbackUri` or unified fallback controller is currently observed.
- After circuit-breaker activation, the gateway cannot return a standardized fallback response, impacting service availability and user experience.

## 2.2 Incomplete Circuit-Breaker Policy Design

- The current approach primarily relies on timeout plus `CircuitBreakerConfig.ofDefaults()`, without production-grade fine-tuning parameters such as:
 - Failure-rate threshold
 - Slow-call threshold
 - Half-open strategy
 - Sliding-window configuration

## 2.3 Uncertainty in the Rate-Limiting Execution Path

- Although `RequestRateLimiter` is injected into dynamic routes, `key-resolver` is not explicitly bound.
- `apiGatewayRatelimiterKeyResolver` is defined in `ApplicationConfiguration`, but actual runtime binding behavior is uncertain.
- Current key generation is path-only (`exchange.getRequest().getURI().getPath()`), which may cause quota sharing across users and is not suitable for user-level throttling.

## 2.4 Insufficient Test Coverage

- Test coverage for resilience controls (circuit breaker / fallback handling / rate limiting) is limited.
- Some integration test classes are marked with `@Disabled`, weakening regression confidence.

# Capability Conclusion Against Mainstream Gateway Expectations

- Circuit breaker: **Partially supported (baseline only)**
- Fallback handling: **Largely unsupported (no production fallback path implemented)**
- Rate limiting: **Partially supported (available but not fully production-configured)**

# Implementation Plan (Prioritized)

## 4.1 Phase 1: Productionize Rate Limiting First (1-2 days)

### Objective

Make `RequestRateLimiter` fully controllable, explainable, and observable.

### Design

#### 1. Explicitly configure the following during dynamic route assembly:

- `key-resolver: "#{@apiGatewayRatelimiterKeyResolver}"`
 - `deny-empty-key: false` (or `true` for strict mode)

#### 2. Extend `OpenApiRateLimiter` with:

- `replenishRate`
 - `burstCapacity`
 - `requestedTokens`
 - `keyType` (`PATH` / `USER` / `TOKEN` / `IP`)

#### 3. Enable multi-strategy key generation in `apiGatewayRatelimiterKeyResolver`:

- Primary: user dimension (`userId` / token)
 - Secondary: client IP
 - Final fallback: request path

### Primary Code Touchpoints

- `src/main/java/com/scb/ratan/gateway/api/repository/OpenApiRateLimiter.java`
- `src/main/java/com/scb/ratan/gateway/core/OpenApiRouteDefinitionLocator.java`
- `src/main/java/com/scb/ratan/gateway/infra/ApplicationConfiguration.java`

## 4.2 Phase 2: Complete Circuit-Breaker + Fallback Handling Closed Loop (2-3 days)

### Objective

Implement configurable circuit-breaker policies with standardized fallback responses.

### Design

#### 1. Add a `resilience` (or `circuitBreaker`) section to `OpenApi`:

- `enabled`
 - `circuitBreakerName`
 - `fallbackUri`
 - `recordStatusCodes` (optional)

#### 2. Inject route-level `CircuitBreaker` in `OpenApiRouteDefinitionLocator` (instead of depending only on global `default-filter`).

3. Add an internal fallback endpoint: `forward:/internal/fallback/{routeId}`.
4. Standardize fallback response schema:

- Error code
 - Error message
 - `routeId`
 - `traceId`
 - Timestamp

### Suggested New Classes

- `src/main/java/com/scb/ratan/gateway/route/FallbackController.java`
- `src/main/java/com/scb/ratan/gateway/api/repository/OpenApiResilience.java` (or equivalent naming)

## 4.3 Phase 3: Operationally Tune Circuit-Breaker Parameters (1 day)

### Objective

Replace default settings with production-operable and tunable circuit-breaker policies.

### Recommended Resilience4j Parameters

- `failureRateThreshold`
- `minimumNumberOfCalls`
- `slidingWindowType` / `slidingWindowSize`
- `waitDurationInOpenState`
- `permittedNumberOfCallsInHalfOpenState`
- `slowCallDurationThreshold`
- `slowCallRateThreshold`

### Recommendation:

manage these values dynamically via a configuration center by environment, with independent circuit-breaker instances per backend service.

## 4.4 Testing and Observability Enhancements (Mandatory)

### Automated Testing Recommendations

#### 1. **Circuit-breaker trigger test**: Simulate downstream timeout/5xx and verify circuit-breaker state transitions.

2. **Fallback handling test**: After circuit-breaker trigger, verify fallback routing and standardized payload.
3. **Rate-limiting test**: Under high concurrency, validate 429 ratio and recovery behavior.
4. **KeyResolver test**: Validate USER/TOKEN/IP/PATH key strategies.

### Metrics Recommendations

#### - `gateway.ratelimit.rejected`

- `gateway.fallback.count`
- `gateway.circuitbreaker.open`
- Add tags by `routeId`, service, and status.

# Architecture Recommendations vs. Mainstream Gateways

## 5.1 Continue Evolving the Current Architecture (Recommended)

The current gateway already contains clear business-specific capabilities (ACL, auditing, dynamic OpenApi management). Continue evolving with Spring Cloud Gateway as the core platform.

## 5.2 Incrementally Complete the Core Gateway Capability Checklist

### 1. Route-level policy center (circuit breaker / rate limiting / timeout / retry)

2. Standardized fallback response model and error-code governance
3. Closed-loop observability (metrics + alerting + dashboards)
4. Canary release capabilities (by header / user / country)

## 5.3 Mid- to Long-Term Evolution Path

### - If higher performance and broader plugin ecosystem become priorities, consider a dual-layer model:

 - Front layer: APISIX/Kong for northbound traffic governance
 - Current gateway: southbound business orchestration

# Recommended Delivery Sequence (Execution-Ready)

### 1. **P1**: Implement rate-limiting parameters and key resolver strategy

2. **P1**: Implement fallback controller and route-level circuit-breaker configuration
3. **P1**: Production-tune circuit-breaker parameters
4. **P1**: Complete integration tests (circuit breaker / fallback handling / rate limiting)
5. **P2**: Deliver dashboard and alerting
6. **P2**: Build canary and governance platform capabilities

# Executive Conclusion

The project already has a solid API Gateway foundation and partial resilience capabilities; however, **fallback handling is not yet fully implemented, and circuit-breaker/rate-limiting strategies are not production-ready**.
After completing the four phases above, the gateway can meet mainstream enterprise requirements for availability, resilience, and operational manageability.