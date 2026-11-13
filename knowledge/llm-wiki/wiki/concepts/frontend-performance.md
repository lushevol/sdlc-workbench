---
type: "Concept"
sources: ["summaries/KT-observability-and-performance.md"]
description: "Portal API loading intent, historical frontend measurements, throughput, and cache evidence."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical basis: [current API loading limit](../../../records/candidates/observability/KT-observability-and-performance.md#current-api-loading-limit), [historical frontend measurement intent](../../../records/candidates/observability/KT-observability-and-performance.md#historical-frontend-measurement-intent), and [capacity evidence limits](../../../records/candidates/observability/KT-observability-and-performance.md#service-throughput-and-capacity-boundaries).

# Frontend performance measurement and capacity evidence

## Definition

This concept covers the evidence needed to turn frontend performance statements into defensible capacity claims. Measurements, draft targets, historical load-test results, and cache design rules describe intent or past observations; they become capacity evidence only when their workload, environment, time period, approval state, and execution artifacts are available.

## Why it matters

Portal performance discussions mix several kinds of material: design proposals, draft non-functional targets, reported browser metrics, load-test summaries, and future sizing estimates. Without clear provenance, a draft target can be mistaken for an accepted service limit, or a historical result can be treated as current production capacity. The concept therefore separates measurement intent from verified operational evidence.

## Key details from the source

### Current API loading limit

The 12 November 2026 clarification gives a five-second API loading limit and specifies no mandatory UI performance metric. Covered API requests, timing boundaries, workload, environment, and measurement method remain open. [API performance criterion](../../../records/candidates/observability/KT-observability-and-performance.md#portal-api-perf-ac-001)

### Historical draft targets

The May 2023 frontend performance document lists draft targets of five-second response time, 100 users, CPU below 50 percent, and JavaScript heap below 80 percent. Its sign-off table has no attached approval or sign-off date. The named non-functional requirements export contains no substantive text. [Historical frontend measurement intent](../../../records/candidates/observability/KT-observability-and-performance.md#historical-frontend-measurement-intent)

### Reported browser metrics

The draft reports login FCP 0.8 seconds and LCP 1.3 seconds, and home FCP 0.9 seconds and LCP 1.3 seconds. The underlying screenshots and measurement captures are absent from the supplied copy. These reported values cannot establish present performance or capacity. Its scenarios cover login, home, trade, cashflow, exception, and rules pages, and its tools include browser performance monitoring and Lighthouse. The plan assumes supporting APIs remain available and sufficiently responsive. See [[entities/kibana]] for the related dashboard context.

### Throughput and load-test summaries

The UAT throughput page describes 500 users, a 250-second ramp-up, and five iterations. It reports 17,500 successful requests and a maximum response time of 2,023 milliseconds for `/api/auth/v2/sso/validate`. The linked JMeter plan and result archive are absent from the supplied copy. A summary alone does not establish current production capacity or verified business behavior. See [[entities/apache-jmeter]].

A newer deployment page reports user estimates and additional performance figures, along with expected future onboarding and architecture changes. Its associated test-result and metric materials are not supplied. Those figures require their workload, time period, environment, and execution evidence before sizing decisions. See [[summaries/KT-architecture-evolution]].

### Cache strategy as a performance variable

The cache guide proposes revalidation of layer entry files and longer caching of subsequent static files, with 120 days assigned to chunks, images, CSS, fonts, JSON, and icons. A changed entry should reference new subsequent files. Users still need logout or page refresh to obtain updated UI code, and the guide explicitly excludes a first-load improvement. These are documented design rules; current response headers and build naming remain unverified. The cache implementation section contains no configuration, so the documented strategy cannot prove deployed cache behavior. See [[concepts/mfe-cache-strategy]].

### Analytics as an adjacent evidence stream

Interaction analytics support CPO review of product usage. API timing and capacity require separate measurements. The analytics examples contain identity and search values, and the models declare conflicting custom attribute counts of 20 and 10. See [[concepts/interaction-analytics]] for the candidate retention period and open collection and access rules.

## Evidence standard

A capacity claim should be backed by dated execution records that include workload, assertions, environment, results, and approved limits. Local hashes identify supplied document bytes without establishing original authority or current applicability. Missing diagrams, screenshots, JMeter plans, and execution archives limit verification. No browser measurement, telemetry query, load test, or server-header check ran during ingestion.

## Open questions

- Which API requests, timing boundaries, workloads, environments, and measurement methods apply to the five-second limit?
- Which current execution records establish API loading time and capacity?
- Which deployed cache settings and asset naming rules implement the documented strategy?
- Which analytics model defines the supported custom attribute limit?
- Which analytics fields and readers are permitted, and which retention clock and expiry treatment apply?

## Related pages

- [[summaries/KT-observability-and-performance]]
- [[concepts/mfe-cache-strategy]]
- [[concepts/interaction-analytics]]
- [[concepts/application-ownership]]
