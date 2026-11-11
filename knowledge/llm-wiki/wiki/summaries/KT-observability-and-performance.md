---
type: "Summary"
description: "Connects analytics, performance tests, throughput, and cache design; flags unverified capacity."
doc_type: short
full_text: "sources/KT-observability-and-performance.md"
---

# Portal observability, performance, and cache behavior

## Scope and main contribution

This topic links four evidence streams: interaction analytics, usage dashboards, frontend performance testing, and cache strategy. It separates documented design intent from current operational requirements and capacity. The main contribution is a cautious synthesis: analytics can explain adoption, performance plans describe measurement intent, and historical reports cannot establish present production capacity without execution evidence.

## Interaction analytics

- The analytics effort aims to understand user interaction, improve adoption, and reduce time to value.
- Captured UI elements include tiles, modals, workspace tabs, buttons, switches, and dropdowns.
- Tiles and modals expose open and close events; tabs, buttons, and switches expose click events; dropdowns expose select events.
- Event identity combines container, tile, and component name. Optional values and custom attributes describe interactions such as searches, but do not define an approved vocabulary for every tenant event.
- The example `useAnalytics` hook posts to `/analytics/v1/fmo/print?extend=false`, while the surrounding prose gives `/api/analytics/v1/fmo/print?extend=false` as the requested API. The example uses session-derived authorization and describes deriving client addresses from request headers and the remote address. No credentials, tokens, or individual user data are reproduced.
- `AnalyticsData` declares 20 custom attribute fields, while `AnalyticsType` declares 10. The supported producer, transport, and storage limit remains unresolved.

Related concept: [[concepts/interaction-analytics]]. Governance concern: telemetry governance.

## Usage dashboards

The [[entities/kibana]] dashboard guide reports nine dashboards for Portal usage: authentication, authentication errors, tiles, workspace movement, workspace additions, selected buttons, login choices, and themes. The error dashboard exposes `traceId` for investigation, and the guide describes downloadable raw data. Its Production dashboard URL remains a placeholder. These statements do not prove present dashboard availability or data completeness.

Related concept: usage dashboards.

## Frontend performance and non-functional requirements

The monitoring page proposes weekly review of development performance. It discusses login, post-login, and blotter rendering with cache and compression changes.

The May 2023 performance document is explicitly a draft. Its sign-off table has no attached approval or sign-off date. It lists draft targets of five-second response time, 100 users, CPU below 50 percent, and JavaScript heap below 80 percent. Its scenarios cover login, home, trade, cashflow, exception, and rules pages. Its tools include browser performance monitoring and Lighthouse. The plan assumes supporting APIs remain available and sufficiently responsive.

The draft reports login FCP 0.8 seconds and LCP 1.3 seconds, plus home FCP 0.9 seconds and LCP 1.3 seconds. The underlying screenshots and measurement captures are absent from the supplied copy. These values cannot establish present performance or capacity, and the draft targets are not approved current service limits.

Related concepts: [[concepts/frontend-performance]], non-functional requirements.

## Service throughput and capacity

The UAT throughput page describes 500 users, a 250-second ramp-up, and five iterations. It reports 17,500 successful requests and a maximum response time of 2,023 milliseconds for `/api/auth/v2/sso/validate`. The linked [[entities/apache-jmeter]] plan and result archive are absent from the supplied copy.

The newer deployment page reports user estimates and additional performance figures, and it describes expected future onboarding and architecture changes. Its associated test-result and metric materials are not supplied. Those figures require their workload, time period, environment, and execution evidence before sizing decisions.

Related concepts: service throughput, capacity planning, observability.

## Cache strategy and update limits

The cache guide proposes revalidation of layer entry files and longer caching of subsequent static files. Its table assigns 120 days to chunks, images, CSS, fonts, JSON, and icons. A changed entry should reference new subsequent files under the described approach. Users still need logout or page refresh to obtain updated UI code, and the guide explicitly excludes a first-load improvement. These are documented design rules; current response headers and build naming remain unverified. The cache implementation section contains no configuration.

Related concept: [[concepts/mfe-cache-strategy]].

## Evidence limits

The named non-functional requirements page contains no substantive text, so it supplies no accepted service targets or measurable acceptance criteria. Historical test targets therefore cannot be treated as accepted current service limits.

Local hashes identify supplied document bytes without establishing original authority or current applicability. The sources mix design examples, draft targets, reported results, and future planning. Missing diagrams, screenshots, JMeter plans, and execution archives limit verification. No browser measurement, telemetry query, load test, or server-header check ran during ingestion.

## Open questions

| Issue | Consequence | Next action |
| --- | --- | --- |
| Analytics models declare 20 and 10 custom attributes. | Producers could send attributes that downstream systems omit. | Reconcile producer, transport, storage, and dashboard schemas. |
| Historical results lack referenced execution artifacts. | Current capacity and response time cannot be established. | Retain dated workloads, assertions, environments, results, and approved limits. |
| Production dashboard address remains unresolved. | Production observation coverage remains unknown. | Confirm dashboard access, event completeness, and operational ownership. |
| Examples collect identity context and search values without retention rules. | Approved collection and retention boundaries remain unclear. | Confirm permitted fields, access, redaction, and retention. |
| Cache implementation section contains no configuration. | The documented strategy cannot prove deployed cache behavior. | Inspect current headers, entry revalidation, and chunk naming against the guide. |

## Connections

[[concepts/microfrontend-layering]] explains the container and tile identities used in analytics, alongside [[concepts/portal-tile-workspace-model]]. Authentication and sessions supply context for login and session interaction events: [[concepts/single-ui-sdk-authentication]] and [[concepts/cross-application-authentication-handoff]]. [[summaries/KT-architecture-evolution]] separates future sizing proposals from established implementation context.

## Related Concepts
- [[concepts/shared-dependency-governance]]
- [[concepts/portal-ingress-path]]
- [[concepts/application-ownership]]

## Entities
- [[entities/single-ui-bff]]
- [[entities/fmo-post-trade-portal]]
- [[entities/mfe-base]]
- [[entities/mfe-root-config]]
- [[entities/single-ui-sdk]]
- [[entities/nginx]]
- [[entities/ems2]]
