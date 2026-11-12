---
type: "Concept"
sources: ["summaries/KT-architecture-evolution.md"]
description: "Proposed single-connection-per-user delivery of notifications across portal tiles, still experimental."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Realtime Notification Delivery

## Definition

Realtime notification delivery is the proposed portal service that pushes notification events to tiles without each tile opening its own subscription connection. The design is documented only as drafts and experiments. No accepted protocol, schema, or deployed service is recorded.

## Problem statement

The notification draft records that many tiles open separate subscription connections. Each tile then holds its own connection to the backend. This condition increases browser resource use and multiplies server-side subscriptions.

The draft proposes one Server-Sent Events (SSE) connection per user. The portal would then distribute received events to the interested tiles. This is proposed behavior only. The source does not establish an accepted connection limit.

## Competing experiments

The materials describe three distinct experiments. Each experiment tests a different transport and backend combination.

| Experiment | Transport | Backend |
|---|---|---|
| GraphQL over SSE | SSE | Node.js |
| GraphQL over WebSocket | WebSocket | Spring Boot |
| Plain SSE | SSE | Spring Boot |

The GraphQL experiments use [[entities/graphql]] for the message contract. Two experiments use [[entities/spring-boot]] on the server. The branch and demonstration references show experiment locations. They do not prove successful retained execution.

## Client-side consumption

The store draft considers two ways for a tile to react to an incoming event:

- a React effect that watches store state, or
- a registered callback that the store invokes.

The draft uses [[entities/react]] effects. The draft declares `isRead` as a string but assigns boolean `false` in its event handler. This contract mismatch is unresolved. The field contract must not become an implementation requirement without review.

## Proposed data model

The table draft separates four record groups:

- **Notification topics** — connect container, module, tile, endpoint, and subscription payload.
- **User subscriptions** — add enabled and muted preferences for each user and topic.
- **Notification messages** — carry the message payload.
- **User-notification state** — holds read and display flags for each user and message.

This separation keeps message content apart from per-user state. User-topic records include enabled and muted preferences; the draft does not define their effect on retained or unread messages.

## Unresolved retention rules

The draft gives three retention alternatives: one hour, six hours, or 24 hours. The same draft applies the alternatives to messages and to per-user notification data. No alternative is approved.

The draft does not define cleanup behavior. It also does not define how retention interacts with unread notifications. An implementation therefore cannot derive a cleanup interval or an unread-message rule from this draft.

## Relation to platform proposals

The 2026 and early 2027 deployment proposal lists notification as a refining requirement, not as a delivered service. Its target services separate authentication, tile management, telemetry, and AI. The proposal leaves the architecture sections empty. It therefore does not define notification interfaces or a migration path.

## Evidence limits

The notification draft references experiments and absent demonstration materials. Protocol choice, supported schema, and production adoption remain unproved. Ownership is unknown. The source manifest identifies local bytes without original page revisions.

## Open questions

- Which experiment, if any, became a supported portal service?
- Which transport and message contract are accepted?
- Which retention and unread-message rules are accepted?
- Who owns the notification service and its data model?

## Related pages

- [[summaries/KT-architecture-evolution]] — source topic that separates experiments from adopted architecture.
- [[concepts/build-tool-migration]] — parallel case of a researched recommendation without an accepted decision.
- [[concepts/component-library-selection]] — parallel case of historical evaluation versus current standard.
- [[concepts/shared-dependency-governance]] — shared runtime concerns that affect a portal-wide service.
- [[concepts/microfrontend-layering]] — tile and container boundaries that determine where a subscription lives.
- [[entities/fmo-post-trade-portal]] — the portal that would host the service.
- [[entities/graphql]], [[entities/spring-boot]], [[entities/react]] — technologies used in the experiments.