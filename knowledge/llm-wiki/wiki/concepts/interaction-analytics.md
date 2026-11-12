---
type: "Concept"
sources: ["summaries/KT-observability-and-performance.md"]
description: "Portal activity analytics for CPO usage review, with event design and PROD retention."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Interaction analytics and event vocabulary

## Definition

Interaction analytics collects Portal user activity for CPO review of business product usage. The event vocabulary describes which UI elements emit events and which event types apply to each element. [Current analytics purpose](../../../candidates/observability/KT-observability-and-performance.md#interaction-purpose-and-event-vocabulary)

This concept is documented in [[summaries/KT-observability-and-performance]].

## Purpose

The analytics introduction states three aims:

- Understand user interaction with Portal features.
- Improve feature adoption.
- Reduce time to value for users.

These aims are product goals. They do not define accepted measurement targets or approved reporting requirements.

## Event vocabulary

The design defines the observed UI elements and their event types.

| UI element | Event types |
| --- | --- |
| Tile | open, close |
| Modal | open, close |
| Workspace tab | click |
| Button | click |
| Switch | click |
| Dropdown | select |

The element set matches the composition model described in [[concepts/portal-tile-workspace-model]]. Tiles and workspace tabs are first-class Portal structures, so their events connect interaction data to the container and tile identities used elsewhere.

## Event identity

A documented event identity combines three names:

- Container name.
- Tile name.
- Component name.

Optional values and custom attributes describe the specific interaction, for example the value entered in a search field. These fields connect one interaction to its UI context. The source does not define an approved vocabulary for every tenant event, so the identity model is a design example and not a controlled schema.

## Transport and hook design

The example `useAnalytics` hook submits events to `/analytics/v1/fmo/print?extend=false`. The surrounding prose gives `/api/analytics/v1/fmo/print?extend=false` as the requested API, so the two paths differ.

The design derives user identification from session authorization information. It also describes deriving client addresses from request headers and from the remote address. This page records the design intent only. It does not reproduce credentials, tokens, or individual user data.

## Schema limits

The TypeScript declarations disagree on custom attribute capacity:

- `AnalyticsData` declares 20 custom attribute fields.
- `AnalyticsType` declares 10 custom attribute fields, and the explanatory prose also states 10.

The supported producer, transport, and storage limit remains unresolved. A producer could send attributes that a downstream system omits. Reconciliation of the producer, transport, storage, and dashboard schemas is an open action.

## Data governance

The candidate requires three months of retention for Portal user activity analytics in PROD. The design examples include identity context and search values. Permitted fields, authorized reader roles, handling of identifiable values, the retention clock, and expiry treatment remain open. [Retention criterion](../../../candidates/observability/KT-observability-and-performance.md#portal-analytics-ac-001) · [Canonical open questions](../../../candidates/observability/KT-observability-and-performance.md#open-questions)

## Reporting surface

The dashboards described for this data are hosted in [[entities/kibana]]. The documented set has nine dashboards covering authentication, authentication errors, tiles, workspace movement, workspace additions, selected buttons, login choices, and themes. The error dashboard exposes `traceId` for investigation. The Production dashboard address remains a placeholder, so production observation coverage is unknown.

## Related pages

- [[summaries/KT-observability-and-performance]] — source synthesis, including evidence limits.
- [[concepts/frontend-performance]] — API loading intent and historical frontend measurements.
- [[concepts/mfe-cache-strategy]] — cache rules that affect when updated event code reaches users.
- [[concepts/portal-tile-workspace-model]] — container, tile, and workspace identities used in event names.
- [[concepts/portal-entry-and-tile-authorization]] — authorization context for login and session events.
- [[entities/kibana]] — dashboard platform for the reported usage views.
- [[entities/apache-jmeter]] — load testing tool used in the separate throughput work.

## Open questions

- Which model defines the supported custom attribute limit?
- Which fields and reader roles are permitted, and how must identifiable values be handled?
- Which retention clock and expiry treatment apply to the three-month PROD period?
- Which analytics model reconciles producer, transport, storage, and dashboard schemas?
- Which owner confirms production dashboard access and event completeness?
