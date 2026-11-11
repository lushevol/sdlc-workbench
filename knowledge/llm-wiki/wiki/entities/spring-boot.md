---
sources: ["summaries/KT-architecture-evolution.md"]
type: "Product"
description: "Java backend framework used in portal notification experiments and a proposed version upgrade."
---

# Spring Boot

Spring Boot is a Java application framework used as the backend runtime in portal-side experiments and proposals. This page records only what [[summaries/KT-architecture-evolution]] reports; it does not document the framework itself.

## What the document records

Spring Boot appears in three distinct contexts. Each has a different decision status.

### Notification experiments

Two of the three notification experiments use a Spring Boot backend:

- **GraphQL over WebSocket** — a Spring Boot backend serves GraphQL subscriptions over WebSocket. See [[entities/graphql]].
- **SSE with Spring Boot** — a Spring Boot backend serves Server-Sent Events directly.

The third experiment uses GraphQL over SSE with a Node.js backend, so Spring Boot is not universal across the experiments. The draft also proposes one SSE connection per user to reduce browser resource use. Whether any experiment became a supported service is unresolved. Related: [[concepts/realtime-notification-delivery]].

The document treats branch and demonstration references as experiment locations, not proof of successful retained execution. A Spring Boot-based implementation in a draft is therefore not evidence of a deployed portal service.

### Proposed version upgrade

An unchecked future-work list proposes an upgrade to Spring Boot 4.0.6. The list supplies no completion record, migration order, or accepted scope. The document explicitly warns that its wording cannot establish current platform versions. Treat the proposed version as a plan item, not the running version.

### Platform proposals

The 2026–2027 deployment proposal describes target services for authentication, tile management, telemetry, and AI. The source does not state which runtime these services would use, so Spring Boot should not be assumed for them.

## Related entities and concepts

- [[entities/fmo-post-trade-portal]] — the portal context for the notification drafts and the proposed upgrade.
- [[entities/graphql]] — used in two of the notification experiments; one of them runs on Spring Boot.
- [[entities/react]] — the frontend runtime for the notification store and tiles that would consume these backends.
- [[concepts/realtime-notification-delivery]] — the cross-document topic covering protocol choice and connection strategy.

## Evidence status

- The notification experiments are drafts. Protocol choice, schema, and production adoption remain unproved.
- The version upgrade sits in an unchecked list with no owner or completion evidence.
- Source ownership is unknown, and the manifest does not record original page revisions.

Next action: confirm which Spring Boot version is deployed, and locate the accepted notification decision and supported code revision before treating either item as current architecture.