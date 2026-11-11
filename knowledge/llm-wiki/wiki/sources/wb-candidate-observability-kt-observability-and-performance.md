---
title: "Portal observability, performance, and cache behavior"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/observability/KT-observability-and-performance.md
source: raw/workbench/knowledge/candidates/observability/KT-observability-and-performance.md
source_hash: c23c2cac937ba81b
last_updated: 2026-11-11
candidate_id: KT-observability-and-performance
candidate_version: 2
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: observability
workbench_origin: knowledge/candidates/observability/KT-observability-and-performance.md
workbench_sha256: c23c2cac937ba81bb8187f5514d99a51f34cd632ea1dd129e078e7137ab1850f
workbench_status: candidate-derived
---

# Portal observability, performance, and cache behavior

## Scope

This topic connects user interaction analytics, frontend measurements, service throughput, and cache strategy.
It preserves historical observations separately from current operational requirements and capacity.

## Summary

Analytics explain how users interact with Portal features.
Performance plans define measurements and workloads.
Cache strategy trades update detection against repeated asset requests.
The supplied reports do not establish current production capacity or approved service limits.

## Documented knowledge

### Interaction purpose and event vocabulary

The analytics introduction aims to understand interaction, improve adoption, and reduce time to value.
The design captures tiles, modals, workspace tabs, buttons, switches, and dropdowns.
Tiles and modals expose open and close events.
Tabs, buttons, and switches expose click events.
Dropdowns expose select events.
[Analytics background, lines 1–5](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/page.md#L1>)
[Analytics design, scope and events, lines 7–29](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L7>)

The documented event identity combines container, tile, and component name.
Optional values and custom attributes describe interactions such as searches.
These fields connect an interaction to its UI context.
They do not define an approved vocabulary for every tenant event.
[Analytics design, identifiers and specific attributes, lines 31–47](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L31>)

The example `useAnalytics` hook submits events to `/analytics/v1/fmo/print?extend=false`.
The surrounding prose gives `/api/analytics/v1/fmo/print?extend=false` as the requested API.
The example attaches session-derived authorization information for user identification.
The source also describes deriving client addresses from request headers and the remote address.
This topic records the design without copying credentials, tokens, or individual user data.
[Analytics design, hook and request description, lines 117–129 and 222–241](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L117>)

`AnalyticsData` declares 20 custom attribute fields.
`AnalyticsType` declares 10, and the explanatory prose also refers to 10.
The supported producer, transport, and storage limit remains unresolved.
[Analytics design, model declarations, lines 55–114](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L55>)

### Usage dashboards

The dashboard guide reports nine dashboards for Portal usage.
They cover authentication, authentication errors, tiles, workspace movement, workspace additions, selected buttons, login choices, and themes.
The error dashboard exposes `traceId` for investigation.
The guide describes downloadable raw data for further analysis.
Its Production dashboard URL remains a placeholder.
These statements do not prove present dashboard availability or data completeness.
[Dashboard guide, lines 11–105](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Analytic Dashboard in Kibana/page.md#L11>)

### Frontend measurement intent

The monitoring page proposes weekly review of development performance.
It discusses login, post-login, and blotter rendering with cache and compression changes.
The May 2023 performance document is explicitly a draft.
Its sign-off table has no attached approval or sign-off date.
The document therefore supplies historical test intent and reported measurements.
[Monitoring introduction and scenarios, lines 1–41](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/page.md#L1>)
[May 2023 performance document, history and sign-off, lines 5–36](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L5>)

The draft lists five-second response time, 100 users, CPU below 50%, and JavaScript heap below 80%.
These are draft targets, without established current approval.
Its scenarios cover login, home, trade, cashflow, exception, and rules pages.
Its tools include browser performance monitoring and Lighthouse.
The plan assumes supporting APIs remain available and sufficiently responsive.
[May 2023 document, NFR, scenarios, and tools, lines 68–89 and 188–226](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L68>)

The draft reports login FCP 0.8 seconds and LCP 1.3 seconds.
It reports home FCP 0.9 seconds and LCP 1.3 seconds.
The underlying screenshots and measurement captures are absent from this supplied copy.
These reported values cannot establish present performance or capacity.
[May 2023 document, result tables, lines 230–256](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L230>)

### Service throughput and capacity boundaries

The UAT throughput page describes 500 users, a 250-second ramp-up, and five iterations.
It reports 17,500 successful requests and a maximum response time of 2,023 milliseconds.
That maximum concerns `/api/auth/v2/sso/validate` in the reported test.
The source links a JMeter plan and result archive that are absent from this supplied copy.
The summary alone does not establish current production capacity or verified business behavior.
[UAT throughput, workload and result summary, lines 11–42](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Throughput Testing in UAT/page.md#L11>)

The newer deployment page reports user estimates and additional performance figures.
It also describes expected future onboarding and architecture changes.
The associated test-result and metric materials are not supplied here.
Those figures require their workload, time period, environment, and execution evidence before sizing decisions.
[Portal new deployment, requirements and performance state, lines 3–47](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3>)

### Cache strategy and update limits

The cache guide proposes revalidation of layer entry files and longer caching of subsequent static files.
Its table assigns 120 days to chunks, images, CSS, fonts, JSON, and icons.
A changed entry should reference new subsequent files under the described approach.
Users still need logout or page refresh to obtain updated UI code.
The guide explicitly excludes a first-load improvement.
These are documented design rules; current response headers and build naming remain unverified.
[Cache strategy, introduction, limitations, and expiry table, lines 1–43](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1>)

## Connections

Frontend composition ([[wb-candidate-architecture-kt-frontend-composition]]) explains the container and tile identities used in analytics.
Authentication and sessions ([[wb-candidate-security-kt-authentication-and-sessions]]) supplies context for login and session interaction events.
Architecture evolution ([[wb-candidate-evolution-kt-architecture-evolution]]) separates future sizing proposals from established implementation context.

Registry capability `single-ui-analytics` and contract `single-ui-analytics-proxy` provide related candidate interface context.
Capability `single-ui-workspace-composition` provides the declared UI composition connection.
These identifiers do not prove deployed collection, dashboard coverage, or business behavior.

## Evidence limits

The named non-functional requirements page contains no substantive text.
It supplies no accepted service targets or measurable acceptance criteria.
[Empty NFR page, line 1](../../../candidates/evidence/knowledge/migration-20261020/cleanup.json>)

Local hashes identify supplied document bytes, without establishing original authority or current applicability.
The sources mix design examples, draft targets, reported results, and future planning.
Missing diagrams, screenshots, JMeter plans, and execution archives limit verification.
No browser measurement, telemetry query, load test, or server-header check ran during ingestion.
No individual identity, credential, or token value is reproduced here.

## Open questions

| Issue and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Analytics models declare 20 and 10 custom attributes. See analytics design, lines 55–114. | Producers could send attributes that downstream systems omit. | unknown | Reconcile producer, transport, storage, and dashboard schemas. |
| Historical results lack their referenced execution artifacts. See throughput, lines 25–44, and May 2023 results. | Current capacity and response time cannot be established. | unknown | Retain dated workloads, assertions, environments, results, and approved limits. |
| Production dashboard address remains unresolved. See dashboard guide, lines 11–13. | Production observation coverage remains unknown. | unknown | Confirm dashboard access, event completeness, and operational ownership. |
| Examples collect identity context and search values without retention rules. See analytics design, lines 43–47 and 88–114. | Approved collection and retention boundaries remain unclear. | unknown | Confirm permitted fields, access, redaction, and retention. |
| Cache implementation section contains no configuration. See cache guide, line 45. | The documented strategy cannot prove deployed cache behavior. | unknown | Inspect current headers, entry revalidation, and chunk naming against the guide. |

Evidence: The named NFR page is empty.
Consequence: Historical test targets cannot be treated as accepted current service limits.
Owner: unknown.
Next action: obtain applicable NFR intent and reviewed measurable limits.
