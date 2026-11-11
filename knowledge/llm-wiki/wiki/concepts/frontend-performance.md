---
type: "Concept"
sources: ["summaries/KT-observability-and-performance.md"]
description: "How frontend performance targets, throughput results, and cache behavior are evidenced before capacity claims."
---

# Frontend performance measurement and capacity evidence

## Definition

This concept covers the evidence needed to turn frontend performance statements into defensible capacity claims. Measurements, draft targets, historical load-test results, and cache design rules describe intent or past observations; they become capacity evidence only when their workload, environment, time period, approval state, and execution artifacts are available.

## Why it matters

Portal performance discussions mix several kinds of material: design proposals, draft non-functional targets, reported browser metrics, load-test summaries, and future sizing estimates. Without clear provenance, a draft target can be mistaken for an accepted service limit, or a historical result can be treated as current production capacity. The concept therefore separates measurement intent from verified operational evidence.

## Key details from the source

### Draft targets versus approved limits

The May 2023 frontend performance document is explicitly a draft. It lists five-second response time, 100 users, CPU below 50 percent, and JavaScript heap below 80 percent, but its sign-off table has no attached approval or sign-off date. These are draft targets, not established current approval. The named non-functional requirements page contains no substantive text, so it supplies no accepted service targets or measurable acceptance criteria.

### Reported browser metrics

The draft reports login FCP 0.8 seconds and LCP 1.3 seconds, and home FCP 0.9 seconds and LCP 1.3 seconds. The underlying screenshots and measurement captures are absent from the supplied copy. These reported values cannot establish present performance or capacity. Its scenarios cover login, home, trade, cashflow, exception, and rules pages, and its tools include browser performance monitoring and Lighthouse. The plan assumes supporting APIs remain available and sufficiently responsive. See [[entities/kibana]] for the related dashboard context.

### Throughput and load-test summaries

The UAT throughput page describes 500 users, a 250-second ramp-up, and five iterations. It reports 17,500 successful requests and a maximum response time of 2,023 milliseconds for `/api/auth/v2/sso/validate`. The linked JMeter plan and result archive are absent from the supplied copy. A summary alone does not establish current production capacity or verified business behavior. See [[entities/apache-jmeter]].

A newer deployment page reports user estimates and additional performance figures, along with expected future onboarding and architecture changes. Its associated test-result and metric materials are not supplied. Those figures require their workload, time period, environment, and execution evidence before sizing decisions. See [[summaries/KT-architecture-evolution]].

### Cache strategy as a performance variable

The cache guide proposes revalidation of layer entry files and longer caching of subsequent static files, with 120 days assigned to chunks, images, CSS, fonts, JSON, and icons. A changed entry should reference new subsequent files. Users still need logout or page refresh to obtain updated UI code, and the guide explicitly excludes a first-load improvement. These are documented design rules; current response headers and build naming remain unverified. The cache implementation section contains no configuration, so the documented strategy cannot prove deployed cache behavior. See [[concepts/mfe-cache-strategy]].

### Analytics as an adjacent evidence stream

Interaction analytics explain adoption and user behavior, but they do not by themselves establish performance or capacity. Analytics design examples collect identity context and search values without stated retention rules, and the models declare conflicting custom attribute counts of 20 and 10. See [[concepts/interaction-analytics]].

## Evidence standard

A capacity claim should be backed by dated execution records that include workload, assertions, environment, results, and approved limits. Local hashes identify supplied document bytes without establishing original authority or current applicability. Missing diagrams, screenshots, JMeter plans, and execution archives limit verification. No browser measurement, telemetry query, load test, or server-header check ran during ingestion.

## Open questions

- Which current execution records establish response time and capacity?
- Which deployed cache settings and asset naming rules implement the documented strategy?
- Which analytics model defines the supported custom attribute limit?
- Which data collection and retention rules govern identity and search values?

## Related pages

- [[summaries/KT-observability-and-performance]]
- [[concepts/mfe-cache-strategy]]
- [[concepts/interaction-analytics]]
- [[concepts/application-ownership]]
