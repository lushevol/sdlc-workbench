---
type: KnowledgeTopic
id: KT-observability-and-performance
version: 3
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/Analytics/page.md
  revision: sha256:40fa7dd90ccb5d1c71eb51791e160c1db5703ca50ed4ea4ab7626ca77f3d3f69
  sha256: 40fa7dd90ccb5d1c71eb51791e160c1db5703ca50ed4ea4ab7626ca77f3d3f69
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/Analytics/Design/page.md
  revision: sha256:7117c9bfce3d74ed0c7e15910d329355cc4dfcb585404e6a819bb47e366f75c6
  sha256: 7117c9bfce3d74ed0c7e15910d329355cc4dfcb585404e6a819bb47e366f75c6
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/Analytics/Analytic Dashboard in Kibana/page.md
  revision: sha256:02ef377427c8d25b38babe9fd0c12a982326e1a309dfde650d3415f7dd234bcd
  sha256: 02ef377427c8d25b38babe9fd0c12a982326e1a309dfde650d3415f7dd234bcd
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/MFE Performance Monitoring/page.md
  revision: sha256:c2679a7e724234e85a30f461bb58d2b2af0caccd64b77d33f7202984a4018263
  sha256: c2679a7e724234e85a30f461bb58d2b2af0caccd64b77d33f7202984a4018263
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance
    Testing May 2023/page.md
  revision: sha256:77108627a097f42f68be95abaf21d29b9bce8e8390ddf6b8c4f09aa3ce6673bb
  sha256: 77108627a097f42f68be95abaf21d29b9bce8e8390ddf6b8c4f09aa3ce6673bb
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md
  revision: sha256:14f4a4cf6c2caaff279947a5497dba886b683256e64acae6dce68f89faf09320
  sha256: 14f4a4cf6c2caaff279947a5497dba886b683256e64acae6dce68f89faf09320
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/Admin Module/Throughput Testing in UAT/page.md
  revision: sha256:35a2a306c69d061472c5df0c8355af01399a5beaa7c3ec11f9555adbe5f02a71
  sha256: 35a2a306c69d061472c5df0c8355af01399a5beaa7c3ec11f9555adbe5f02a71
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md
  revision: sha256:6a6cd47cad4a73d0e98b3f3c61b93d63a710adf6c965ca800d4bb472b97a34ce
  sha256: 6a6cd47cad4a73d0e98b3f3c61b93d63a710adf6c965ca800d4bb472b97a34ce
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade
    Portal Home/Technical Design and Document/FM Post Trade Portal - Non Functional
    Requirements/page.md
  revision: sha256:01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
  sha256: 01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
- resource: workbench-evidence:domain-knowledge-cleanup-20261020
  revision: migration-20261020
  sha256: 4027b8034b07676b7f80e9b4c023f0459a5ed7f594dbcc7da214b56a480f7fa0
- resource: conversation:codex/portal-knowledge-ingestion/2026-11-12/answers
  revision: sha256:b2820b053e32a9b45b44f177e539c2bfe8106c29c9b74c09c8fbd94c8e116303
  sha256: b2820b053e32a9b45b44f177e539c2bfe8106c29c9b74c09c8fbd94c8e116303
previous_version: 2
previous_content_sha256: c23c2cac937ba81bb8187f5514d99a51f34cd632ea1dd129e078e7137ab1850f
generated:
  by: agent:codex
  at: '2026-11-12T21:27:34+08:00'
verified: []
classification: observability
scope: Portal interaction analytics, current API performance intent, historical performance
  materials, and documented frontend cache strategy.
summary: The API loading limit is five seconds. Portal analytics support CPO review of
  business product usage. The PROD retention period is three months.
related:
- KT-portal-purpose
- KT-frontend-composition
- KT-authentication-and-sessions
- KT-architecture-evolution
- single-ui-analytics
- single-ui-analytics-proxy
- single-ui-workspace-composition
open_questions:
- What API scope, timing boundaries, and workload apply when measuring the loading limit?
- Which analytics schema defines the accepted custom attribute contract?
- Which deployed cache settings and asset naming rules implement the documented strategy?
- Which analytics fields and readers are permitted, and what rules apply to identifiable values?
- Which retention clock and expiry treatment apply to PROD user activity data?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Portal observability, performance, and cache behavior

## Scope

This topic connects user interaction analytics, frontend measurements, service throughput, and cache strategy.
It preserves historical observations separately from current operational requirements and capacity.

## Summary

Portal analytics collect user activity for CPO review of business product usage.
The PROD retention period for this data is three months.
The current API loading limit is five seconds. The clarification gives no mandatory UI performance metric.
Cache strategy trades update detection against repeated asset requests.
The historical reports supply no current production capacity evidence.

## Documented knowledge

### Interaction purpose and event vocabulary

The primary purpose of Portal analytics is to collect user activity.
The data supports CPO review of how users use business products.
The retention requirement for this data in PROD is three months.
The clarification gives no field allowlist, reader-role rules, or rules for identifiable values.
[User clarification, answer 9](../../../../tasks/ui-test-coverage-20261022/evidence/portal-ingestion-answers-20261112.md#L8)

#### PORTAL-ANALYTICS-AC-001

```gherkin
Feature: Retain Portal user activity analytics in PROD
  @PORTAL-ANALYTICS-AC-001
  Scenario: Apply the three-month retention period
    Given a Portal user activity analytics record stored in PROD
    When the record is evaluated under its applicable retention clock
    Then the record is retained for a period of 3 months
```

The retention clock and the expected expiry treatment require further specification before this criterion can be executed.
[User clarification, answer 9](../../../../tasks/ui-test-coverage-20261022/evidence/portal-ingestion-answers-20261112.md#L8)

The analytics introduction aims to understand interaction, improve adoption, and reduce time to value.
The design captures tiles, modals, workspace tabs, buttons, switches, and dropdowns.
Tiles and modals expose open and close events.
Tabs, buttons, and switches expose click events.
Dropdowns expose select events.
[Analytics background, lines 1–5](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/page.md#L1>)
[Analytics design, scope and events, lines 7–29](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L7>)

The documented event identity combines container, tile, and component name.
Optional values and custom attributes describe interactions such as searches.
These fields connect an interaction to its UI context.
They do not define an approved vocabulary for every tenant event.
[Analytics design, identifiers and specific attributes, lines 31–47](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L31>)

The example `useAnalytics` hook submits events to `/analytics/v1/fmo/print?extend=false`.
The surrounding prose gives `/api/analytics/v1/fmo/print?extend=false` as the requested API.
The example attaches session-derived authorization information for user identification.
The source also describes deriving client addresses from request headers and the remote address.
This topic records the design without copying credentials, tokens, or individual user data.
[Analytics design, hook and request description, lines 117–129 and 222–241](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L117>)

`AnalyticsData` declares 20 custom attribute fields.
`AnalyticsType` declares 10, and the explanatory prose also refers to 10.
The supported producer, transport, and storage limit remains unresolved.
[Analytics design, model declarations, lines 55–114](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L55>)

### Usage dashboards

The dashboard guide reports nine dashboards for Portal usage.
They cover authentication, authentication errors, tiles, workspace movement, workspace additions, selected buttons, login choices, and themes.
The error dashboard exposes `traceId` for investigation.
The guide describes downloadable raw data for further analysis.
Its Production dashboard URL remains a placeholder.
These statements do not prove present dashboard availability or data completeness.
[Dashboard guide, lines 11–105](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Analytic Dashboard in Kibana/page.md#L11>)

### Current API loading limit

The user defines a five-second NFR for API loading.
The user gives no mandatory UI performance metric.
The clarification leaves API scope, measurement start and end, and applicable workload open.
[User clarification, answer 8](../../../../tasks/ui-test-coverage-20261022/evidence/portal-ingestion-answers-20261112.md#L8)

#### PORTAL-API-PERF-AC-001

```gherkin
Feature: Meet the Portal API loading limit
  @PORTAL-API-PERF-AC-001
  Scenario: Meet the threshold for a Portal API loading measurement
    Given a Portal API request within the applicable scope and workload
    When the request runs and the loading duration is measured using the applicable timing boundaries
    Then the measured API loading duration is at most 5 seconds
```

Acceptance execution needs the applicable measurement scope and method.
[User clarification, answer 8](../../../../tasks/ui-test-coverage-20261022/evidence/portal-ingestion-answers-20261112.md#L8)

### Historical frontend measurement intent

The monitoring page proposes weekly review of development performance.
It discusses login, post-login, and blotter rendering with cache and compression changes.
The May 2023 performance document is explicitly a draft.
Its sign-off table has no attached approval or sign-off date.
The document therefore supplies historical test intent and reported measurements.
[Monitoring introduction and scenarios, lines 1–41](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/page.md#L1>)
[May 2023 performance document, history and sign-off, lines 5–36](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L5>)

The draft lists five-second response time, 100 users, CPU below 50%, and JavaScript heap below 80%.
These are draft targets, without established current approval.
Its scenarios cover login, home, trade, cashflow, exception, and rules pages.
Its tools include browser performance monitoring and Lighthouse.
The plan assumes supporting APIs remain available and sufficiently responsive.
[May 2023 document, NFR, scenarios, and tools, lines 68–89 and 188–226](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L68>)

The draft reports login FCP 0.8 seconds and LCP 1.3 seconds.
It reports home FCP 0.9 seconds and LCP 1.3 seconds.
The underlying screenshots and measurement captures are absent from this supplied copy.
These reported values cannot establish present performance or capacity.
[May 2023 document, result tables, lines 230–256](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L230>)

### Service throughput and capacity boundaries

The UAT throughput page describes 500 users, a 250-second ramp-up, and five iterations.
It reports 17,500 successful requests and a maximum response time of 2,023 milliseconds.
That maximum concerns `/api/auth/v2/sso/validate` in the reported test.
The source links a JMeter plan and result archive that are absent from this supplied copy.
The summary alone does not establish current production capacity or verified business behavior.
[UAT throughput, workload and result summary, lines 11–42](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Throughput Testing in UAT/page.md#L11>)

The newer deployment page reports user estimates and additional performance figures.
It also describes expected future onboarding and architecture changes.
The associated test-result and metric materials are not supplied here.
Those figures require their workload, time period, environment, and execution evidence before sizing decisions.
[Portal new deployment, requirements and performance state, lines 3–47](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3>)

### Cache strategy and update limits

The cache guide proposes revalidation of layer entry files and longer caching of subsequent static files.
Its table assigns 120 days to chunks, images, CSS, fonts, JSON, and icons.
A changed entry should reference new subsequent files under the described approach.
Users still need logout or page refresh to obtain updated UI code.
The guide explicitly excludes a first-load improvement.
These are documented design rules; current response headers and build naming remain unverified.
[Cache strategy, introduction, limitations, and expiry table, lines 1–43](<../../../evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

## Connections

[Frontend composition](../architecture/KT-frontend-composition.md) explains the container and tile identities used in analytics.
[Authentication and sessions](../security/KT-authentication-and-sessions.md) supplies context for login and session interaction events.
[Architecture evolution](../evolution/KT-architecture-evolution.md) separates future sizing proposals from established implementation context.

Registry capability `single-ui-analytics` and contract `single-ui-analytics-proxy` provide related candidate interface context.
Capability `single-ui-workspace-composition` provides the declared UI composition connection.
These identifiers do not prove deployed collection, dashboard coverage, or business behavior.

## Evidence limits

The named non-functional requirements page contains no substantive text.
It supplies no accepted service targets or measurable acceptance criteria.
[Empty NFR page, line 1](<../../../evidence/migration-20261020/cleanup.json>)

Local hashes identify supplied document bytes, without establishing original authority or current applicability.
The export mixes design examples, draft targets, reported results, and future planning.
The later clarification supplies current intent for API loading and PROD analytics retention.
Missing diagrams, screenshots, JMeter plans, and execution archives limit verification.
No browser measurement, telemetry query, load test, or server-header check ran during ingestion.
No individual identity, credential, or token value is reproduced here.

## Open questions

| Issue and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Analytics models declare 20 and 10 custom attributes. See analytics design, lines 55–114. | Producers could send attributes that downstream systems omit. | unknown | Reconcile producer, transport, storage, and dashboard schemas. |
| The current five-second API loading limit has no measurement scope or method. See user answer 8. | Acceptance cannot be executed consistently. | unknown | Confirm the covered API requests, timing boundaries, workload, environment, and measurement method. |
| Historical results lack their referenced execution artifacts. See throughput, lines 25–44, and May 2023 results. | Current capacity and API loading behavior remain unverified. | unknown | Retain dated workloads, assertions, environments, and results. |
| Production dashboard address remains unresolved. See dashboard guide, lines 11–13. | Production observation coverage remains unknown. | unknown | Confirm dashboard access, event completeness, and operational ownership. |
| The design includes identity and search values. User answer 9 supplies a purpose, intended audience, and three-month PROD retention. | Permitted fields, all authorized readers, treatment of identifiable values, and the retention clock remain open. | unknown | Confirm the field and access rules, the retention clock, and expected expiry treatment. |
| Cache implementation section contains no configuration. See cache guide, line 45. | The documented strategy cannot prove deployed cache behavior. | unknown | Inspect current headers, entry revalidation, and chunk naming against the guide. |
