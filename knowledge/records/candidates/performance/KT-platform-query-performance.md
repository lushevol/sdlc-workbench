---
type: KnowledgeTopic
id: KT-platform-query-performance
version: 3
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Performance/Batch Status Update API Tuning/page.md
  revision: sha256:2710f81415f72724f968bc77aa89b0a9d0dedb3bed4d2b807042f6f37076d5ec
  sha256: 2710f81415f72724f968bc77aa89b0a9d0dedb3bed4d2b807042f6f37076d5ec
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Performance/Cashflow Blotter Page Size Performance/page.md
  revision: sha256:a44b67973b7870ef210b6c698d10b3ec99c87f92333c591c904da2c8eff79400
  sha256: a44b67973b7870ef210b6c698d10b3ec99c87f92333c591c904da2c8eff79400
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Performance/Cashflow Blotter Query Performance Optimization/page.md
  revision: sha256:3ccf96029a2a48bcaea747054811a7a2704d1df2fa2c32171b3fd1fd69b5406d
  sha256: 3ccf96029a2a48bcaea747054811a7a2704d1df2fa2c32171b3fd1fd69b5406d
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Performance/PT Batch Group Stg/page.md
  revision: sha256:60944570b207979fb1d4a7516d0ca135e058d783757dd991d428231f6156b43c
  sha256: 60944570b207979fb1d4a7516d0ca135e058d783757dd991d428231f6156b43c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Performance/PT Orchestration Stg/page.md
  revision: sha256:c5b79eb03d184e4291137c82f14521952c41b15c07f197fc1d93847009fe5626
  sha256: c5b79eb03d184e4291137c82f14521952c41b15c07f197fc1d93847009fe5626
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Kafka
    Listener Consumption Time Tracking Design Scheme/page.md
  revision: sha256:5a3e0a8ecf5a2e32a42e82841e37b4a5158ae2513d747e159a9e82603dff1a77
  sha256: 5a3e0a8ecf5a2e32a42e82841e37b4a5158ae2513d747e159a9e82603dff1a77
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Kafka
    consumer issue for large lag during drop3 migration testing/page.md
  revision: sha256:cc833f7bf163e7e467d8e0da70492c07fad100f76aefc9ade0cb8b4d4b8cc61d
  sha256: cc833f7bf163e7e467d8e0da70492c07fad100f76aefc9ade0cb8b4d4b8cc61d
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    UI Performance Analysis (2022 Dec)/page.md
  revision: sha256:5cc8b18323b13f457c1c44a2c022e1dfe3a2c6cbb5d7463021b91869190321e0
  sha256: 5cc8b18323b13f457c1c44a2c022e1dfe3a2c6cbb5d7463021b91869190321e0
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    UI Performance Optimize Cases/page.md
  revision: sha256:a1c72499d9e8a698b32806490ea1202addef282e35b7512e5f67ffb9f4019c58
  sha256: a1c72499d9e8a698b32806490ea1202addef282e35b7512e5f67ffb9f4019c58
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/[MB]An
    error occurs which cause the message to be lost/page.md
  revision: sha256:92afa40d75454caf9179c7cbb872b4ceee7774118f475d933f3909e75b6a6e25
  sha256: 92afa40d75454caf9179c7cbb872b4ceee7774118f475d933f3909e75b6a6e25
- id: SRC-7a83fe96a2f68ccc46569ba9
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Performance/PostgreSQL performance/PostgreSQL increase work_mem up
    to 30MB & user define pg function risk analyze/page.md
  revision: sha256:cb53d8e39b62f81d79301803e488bcdab26b337d62a4a53760896a6978678751
  sha256: cb53d8e39b62f81d79301803e488bcdab26b337d62a4a53760896a6978678751
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T02:09:38.119069+00:00'
verified: []
scope: Historical selected-source design for platform query performance.
classification: performance
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which value-date behavior and page-size SLA are approved, including exactly one
  month and removed defaults?
- Which batch transaction, asynchronous completion, lock-list, and Uber queue/topic
  topology are approved?
- Which Kafka timeout values, interceptor registration, tracking format, and UI timing/loading
  contract apply?
- 'KDQ-6fd7c4bd16: Which environments approve the proposed work_mem and to_number_ratan
  expression-index changes?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
previous_content_sha256: 78ff72ab1b8b465a580d9698039382106723f785b98bccbac75a03b5df31b13a
---
# Platform query performance

## Scope

Historical selected-source design for platform query performance.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Value-date search proposal

ID-like searches retain existing behavior.
Non-ID searches in quick search, advanced search, or quick filters default missing value date to today.
Users can remove that default with a warning.
Ranges over one month trigger a warning and block search.

The proposal also says ranges must be less than one month.
Behavior for exactly one month remains unresolved.
The cases apply to temporary, saved, mixed, and advanced filters.

Sources: [original lines 1–3](../../../evidence/sources/sha256/3ccf96029a2a48bcaea747054811a7a2704d1df2fa2c32171b3fd1fd69b5406d.md#L1-L3), [original lines 11–26](../../../evidence/sources/sha256/3ccf96029a2a48bcaea747054811a7a2704d1df2fa2c32171b3fd1fd69b5406d.md#L11-L26), [original lines 28–40](../../../evidence/sources/sha256/3ccf96029a2a48bcaea747054811a7a2704d1df2fa2c32171b3fd1fd69b5406d.md#L28-L40).

### Blotter performance and SLA scope

The page-size analysis proposes revising user-action turnaround expectations when increasing page size.
Its recommendation treats indexed predicates with =, IN, or BET as valid NFR queries.
It gives no response-time guarantee for other query shapes.
A separate alternative proposes pg_hint_plan; no selected decision approves it.

Sources: [original lines 21–24](../../../evidence/sources/sha256/a44b67973b7870ef210b6c698d10b3ec99c87f92333c591c904da2c8eff79400.md#L21-L24), [original lines 34–39](../../../evidence/sources/sha256/a44b67973b7870ef210b6c698d10b3ec99c87f92333c591c904da2c8eff79400.md#L34-L39), [original lines 79–81](../../../evidence/sources/sha256/a44b67973b7870ef210b6c698d10b3ec99c87f92333c591c904da2c8eff79400.md#L79-L81), [original lines 42–44](../../../evidence/sources/sha256/3ccf96029a2a48bcaea747054811a7a2704d1df2fa2c32171b3fd1fd69b5406d.md#L42-L44).

### Batch transaction responsibilities

The draft proposes moving net/unnet into lifecycle to avoid interservice timeout.
Batch status processing fetches required data together, computes in memory, and persists in batches within one transaction.
Post-processing covers CQRS, exception closure, and Kafka STP triggers.
It retains alternative list-lock strategies using parallel acquisition or Lua.

Large requests motivate asynchronous processing and a proposed notification center.
These are alternatives, not an adopted transaction or retry guarantee.

Sources: [original lines 34–40](../../../evidence/sources/sha256/2710f81415f72724f968bc77aa89b0a9d0dedb3bed4d2b807042f6f37076d5ec.md#L34-L40), [original lines 43–64](../../../evidence/sources/sha256/2710f81415f72724f968bc77aa89b0a9d0dedb3bed4d2b807042f6f37076d5ec.md#L43-L64), [original lines 65–96](../../../evidence/sources/sha256/2710f81415f72724f968bc77aa89b0a9d0dedb3bed4d2b807042f6f37076d5ec.md#L65-L96).

### Uber processing and capacity proposals

One proposal splits the solution queue into eight queues by primary asset class.
A separate batch-group page splits one topic into seven topics.
The selected sources do not reconcile queue and topic topology.
Batch-group recommendations add connection capacity, batch Materialize/currency-cutoff queries, and a singleton validation factory.

The orchestration analysis recommends reducing expensive synchronous HTTP work and reusing intermediate results.
It prioritizes msgEventCheck, cashflow/stamp, status/move, checkPaymentDateForIRS, netForIRS, and preCheck.

Sources: [original lines 1–3](../../../evidence/sources/sha256/92afa40d75454caf9179c7cbb872b4ceee7774118f475d933f3909e75b6a6e25.md#L1-L3), [original lines 1–3](../../../evidence/sources/sha256/60944570b207979fb1d4a7516d0ca135e058d783757dd991d428231f6156b43c.md#L1-L3), [original lines 27–47](../../../evidence/sources/sha256/60944570b207979fb1d4a7516d0ca135e058d783757dd991d428231f6156b43c.md#L27-L47), [original lines 1–3](../../../evidence/sources/sha256/c5b79eb03d184e4291137c82f14521952c41b15c07f197fc1d93847009fe5626.md#L1-L3), [original lines 46–63](../../../evidence/sources/sha256/c5b79eb03d184e4291137c82f14521952c41b15c07f197fc1d93847009fe5626.md#L46-L63), [original lines 146–170](../../../evidence/sources/sha256/c5b79eb03d184e4291137c82f14521952c41b15c07f197fc1d93847009fe5626.md#L146-L170), [original lines 171–197](../../../evidence/sources/sha256/c5b79eb03d184e4291137c82f14521952c41b15c07f197fc1d93847009fe5626.md#L171-L197).

### Environment and listener tracking design

The migration-testing proposal uses small-volume EKS business tests and environment-specific Kafka poll/session timeouts.
The selected configuration leaves timeout values as placeholders.
The monitoring design proposes a Spring Kafka RecordInterceptor that preserves the original ConsumerRecord.
It extracts trackingId from headers and logs a configurable trace string.

The design requires no listener-source changes, extensible formats, testable components, and a configuration switch.
Spring Kafka 2.3+ is its stated prerequisite.
Full listener coverage remains an objective, without verified registration or duration measurement.

Sources: [original lines 24–37](../../../evidence/sources/sha256/cc833f7bf163e7e467d8e0da70492c07fad100f76aefc9ade0cb8b4d4b8cc61d.md#L24-L37), [original lines 1–62](../../../evidence/sources/sha256/5a3e0a8ecf5a2e32a42e82841e37b4a5158ae2513d747e159a9e82603dff1a77.md#L1-L62).

### UI timing and loading proposals

The historical UI page gives example budgets: first cashflow page under three seconds and table display under 300 milliseconds.
Quick search is under 500 milliseconds; custom search is under 1000 milliseconds.
These example budgets are not current accepted SLA thresholds.
The page proposes one-request config loading, caching, versioning, audit, access control, and deployment hooks.

It proposes loading priorities, skeletons, shared load status, and custom performance tracking.
A companion page offers asynchronous config requests or server-rendered script configuration as alternatives.
Neither selected source settles the final loading approach.

Sources: [original lines 53–64](../../../evidence/sources/sha256/5cc8b18323b13f457c1c44a2c022e1dfe3a2c6cbb5d7463021b91869190321e0.md#L53-L64), [original lines 96–106](../../../evidence/sources/sha256/5cc8b18323b13f457c1c44a2c022e1dfe3a2c6cbb5d7463021b91869190321e0.md#L96-L106), [original lines 150–166](../../../evidence/sources/sha256/5cc8b18323b13f457c1c44a2c022e1dfe3a2c6cbb5d7463021b91869190321e0.md#L150-L166), [original lines 65–77](../../../evidence/sources/sha256/a1c72499d9e8a698b32806490ea1202addef282e35b7512e5f67ffb9f4019c58.md#L65-L77).

### L3-PG-01 — Cashflow query-service optimization proposal

The risk analysis proposes increasing PostgreSQL work_mem from 4MB to 30MB for each query-service session.
Its stated aim is to avoid lossy bitmap scans, with database memory impact requiring assessment.
It also proposes to_number_ratan for expression indexes on the cashflow JSONB column of cashflow_data.
These are source-specific optimization proposals. Their effective environment and approval remain unresolved.
The reported memory estimates and test results remain independent task evidence.

[Original evidence](../../../evidence/sources/sha256/cb53d8e39b62f81d79301803e488bcdab26b337d62a4a53760896a6978678751.md#L3-L8).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which value-date behavior and page-size SLA are approved, including exactly one month and removed defaults?
- Which batch transaction, asynchronous completion, lock-list, and Uber queue/topic topology are approved?
- Which Kafka timeout values, interceptor registration, tracking format, and UI timing/loading contract apply?
