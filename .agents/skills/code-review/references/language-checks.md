# Conditional language and platform checks

Use these questions only when the selected change affects the named technology or business behavior.
Treat each question as an investigation prompt, not an established defect.
Use the [semantic checklist](review-checklist.md) for shared risks and the [validation guide](validation.md) for evidence claims.
Inspect configured behavior, affected callers, and meaningful assertions before reporting a failure.

## React and TypeScript

- Can effects or callbacks retain obsolete props, state, identity, or entitlements through stale closures?
- Do effect dependencies and inspected identity transitions establish a reachable stale-value path?
- Can concurrent requests, delayed responses, retries, or cancellation overwrite newer state or display another user's data?
- Do cache keys and invalidation preserve tenant, user, permission, and session boundaries after identity changes?
- Can unmounting, remounting, tab suspension, or reconnect leave subscriptions, timers, observers, or sockets active incorrectly?
- Do supported server rendering and hydration paths agree on browser access, initial state, identity, and rendered output?
- Do changed controls preserve keyboard operation, focus, accessible names, and the supported error feedback?
- Can rendering or state updates repeat costly work under an established interaction or collection size?

## Microfrontends and desktop integration

Use this section only when the inspected system contains the named integration.

- Do Module Federation, SystemJS, or import maps load compatible runtime contracts and the intended shared module identities?
- Do actual resolver settings preserve required React singletons across hosts and remotes?
- Can initialization, disposal, version skew, or partial remote failure break a supported host lifecycle?
- Does cross-window messaging validate both the sender origin and source window before trusting message content?
- Do iframe permissions, message schemas, and navigation preserve the established application and tenant boundaries?
- Do OpenFin or FDC3 registrations, intent routing, context schemas, and permissions match the inspected integration contracts?
- Can disposal or identity changes leave stale intent handlers, unauthorized contexts, or duplicate broker subscriptions?

## Spring Boot, Java, and persistence

- Do route and method authorization enforce the required operation, object, tenant, and entitlement checks?
- Can proxy self-invocation bypass required transaction or method-security advice under the configured interception model?
- Do inspected proxies, caller paths, and configuration confirm whether that advice applies?
- Can asynchronous execution or cancellation move database work outside its required transaction or cleanup path?
- Do transaction boundaries, isolation, locking, and rollback rules preserve the demonstrated business invariant?
- Can lazy JPA relationships be read after the persistence context closes under the actual serialization flow?
- Does query count grow with returned entities on a path with an established consequential workload?
- Can changed queries, mappings, pagination, or fetch plans alter result ordering, completeness, locking, or resource use?
- Do connection, query, and request timeouts release resources and preserve the caller's failure contract?
- Do retries, duplicate requests, and partial external failures preserve idempotency and committed state?
- Do external configuration, feature flags, and gateway rewrites resolve consistently across the supported deployment paths?

## Messaging

- Do producers and consumers preserve required schemas, keys, ordering, and mixed-version compatibility?
- Can acknowledgment, offset commit, transaction commit, and external side-effect ordering lose or repeat a business effect?
- Do inspected consumer groups, partitions, concurrency settings, and retry paths support the claimed delivery behavior?
- Do poison-message retries, dead-letter handling, and replay follow the supplied failure policy?
- Can cancellation, rebalancing, or shutdown interrupt processing before required persistence or cleanup completes?
- Do deduplication keys and retention cover the actual replay and duplicate-delivery conditions?

## Financial and enterprise behavior

Use this section only when source-backed business rules make these checks relevant.

- Do decimal types, currency scales, rounding, and conversion order match the supplied financial rules?
- Do timestamps, time zones, business calendars, and cutoffs preserve the required effective date?
- Can duplicate delivery, concurrent transitions, or retries repeat settlement or another irreversible business effect?
- Do status transitions enforce required preconditions, terminal states, authorization, and audit records?
- Can the inspected business event be traced through service calls, messages, persisted effects, and user-visible status?
- Do error paths preserve required audit evidence without exposing customer data, credentials, or sensitive financial values?

State missing contracts, unsupported workloads, unavailable integrations, and unexecuted paths beside the conclusions they limit.
