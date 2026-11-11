---
sources: ["summaries/KT-observability-and-performance.md"]
type: "Product"
description: "Open-source load testing tool referenced as the execution vehicle for Portal throughput tests."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Apache JMeter

Apache JMeter is a load testing tool. In the supplied materials it appears only as the named execution vehicle for Portal throughput testing, not as a subject of design discussion.

## Role in the documented record

The UAT throughput page for the FMO Post Trade Portal describes a workload of 500 users, a 250-second ramp-up, and five iterations. It reports 17,500 successful requests and a maximum response time of 2,023 milliseconds for `/api/auth/v2/sso/validate`. The page links a JMeter plan and a result archive that support these figures.

That JMeter plan and its result archive are absent from the supplied copy. The reported figures therefore remain a summary without their execution artifacts. They cannot establish current production capacity or verified business behavior on their own.

## Verification considerations

A JMeter result is only interpretable together with its plan, assertions, workload shape, target environment, and date. None of these are available here. Any future sizing decision should be based on retained, dated JMeter artifacts rather than the summary line alone.

## Related pages

- [[summaries/KT-observability-and-performance]] — the topic page that records this test summary and its evidence limits.
- [[concepts/frontend-performance]] — performance measurement intent for the Portal frontend, distinct from server-side load testing.
- [[entities/fmo-post-trade-portal]] — the system under test in the reported UAT run.
- [[entities/kibana]] — usage dashboards that provide observation data rather than load generation.