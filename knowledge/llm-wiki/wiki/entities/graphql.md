---
sources: ["summaries/KT-architecture-evolution.md"]
type: "Product"
description: "A query language used in portal notification experiments over SSE and WebSocket."
---

# GraphQL

GraphQL is a query language and runtime for APIs. In [[summaries/KT-architecture-evolution]], it appears only as the API layer in two notification transport experiments. The materials do not describe GraphQL itself in detail, and they do not record an accepted decision to use it.

## Role in the notification experiments

The notification draft describes three separate proof-of-concept implementations for delivering common events across portal tiles:

- **GraphQL over SSE with a Node.js backend.** This experiment pairs a GraphQL API with Server-Sent Events and a Node.js server. See [[concepts/realtime-notification-delivery]].
- **GraphQL over WebSocket with Spring Boot.** This experiment pairs a GraphQL API with WebSocket transport and a [[entities/spring-boot]] backend.
- **SSE using Spring Boot.** A third experiment uses SSE with a Spring Boot backend and does not use GraphQL.

GraphQL is therefore one of two measured transport patterns in the experiment set, not a platform standard. The two GraphQL experiments differ in both transport and backend runtime, so their results are not directly comparable without the demonstration materials.

## Decision status

The draft describes these as experiments. Branch and demonstration references establish where the experiments lived, not that they ran successfully or were retained. The source does not establish which protocol, if any, became a supported portal service.

## Evidence limits

The experiments are documented in draft pages. The materials include no accepted notification decision, supported code revision, or execution evidence. Do not treat GraphQL as the selected notification API from this source.

## Related pages

- [[concepts/realtime-notification-delivery]] — the transport and subscription problem these experiments address.
- [[entities/spring-boot]] — backend runtime for two of the three experiments.
- [[summaries/KT-architecture-evolution]] — the source summary for this page.