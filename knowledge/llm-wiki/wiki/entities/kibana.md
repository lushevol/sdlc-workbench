---
sources: ["summaries/KT-observability-and-performance.md"]
type: "Product"
description: "Kibana is the dashboard tool documented for Portal interaction analytics and usage monitoring."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Kibana

## What it is

Kibana is a data visualization and dashboard product, commonly used to explore and present analytics data. In the supplied Portal documentation, it is named as the tool that hosts the Portal usage dashboards derived from interaction analytics events.

## Role in the Portal documentation

The analytics design describes how user interaction events are produced by Portal UI components. The dashboard guide then describes how those events are examined in Kibana. Kibana therefore sits at the observation end of the analytics flow: events are captured in the browser, submitted to the analytics API, and reviewed through dashboards.

The current analytics candidate identifies CPO review of business product usage as the purpose and sets three months of PROD retention. The authorized Kibana readers, field handling, and expiry details remain open. [Analytics purpose](../../../records/candidates/observability/KT-observability-and-performance.md#interaction-purpose-and-event-vocabulary) · [Retention criterion](../../../records/candidates/observability/KT-observability-and-performance.md#portal-analytics-ac-001)

See [[concepts/interaction-analytics]] for the event vocabulary (tiles, modals, tabs, buttons, switches, dropdowns) that feeds these dashboards, and [[summaries/KT-observability-and-performance]] for the broader evidence assessment.

## Documented dashboards

The guide reports nine dashboards for Portal usage:

- authentication
- authentication errors
- tiles
- workspace movement
- workspace additions
- selected buttons
- login choices
- themes

The error dashboard exposes `traceId` for investigation. The guide also describes downloadable raw data for further analysis. Workspace-oriented views connect to the [[concepts/portal-tile-workspace-model]] that organizes the Portal UI.

## Stated limitations

- The Production dashboard URL remains a placeholder in the supplied copy.
- The statements do not prove present dashboard availability or data completeness.
- Supported custom attribute limits and dashboard field coverage remain unresolved. One documented model declares 20 custom attribute fields and another declares 10.

No dashboard was opened, queried, or verified during ingestion. The documentation establishes intended dashboard scope, not observed production coverage.

## Related entities and pages

- [[entities/fmo-post-trade-portal]] — the Portal whose usage the dashboards describe.
- [[entities/apache-jmeter]] — the load-testing tool used in the separate throughput work; its results are a different evidence stream from Kibana dashboards.
- [[concepts/frontend-performance]] — frontend measurement intent that is distinct from usage analytics.
- [[concepts/mfe-cache-strategy]] — cache behavior documented alongside these observability materials.
- [[summaries/KT-observability-and-performance]] — the source summary for this page.
