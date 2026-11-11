---
title: "Portal composition and interoperability"
type: concept
tags: [candidate-derived, architecture]
sources: [wb-candidate-background-kt-portal-purpose, wb-candidate-architecture-kt-frontend-composition, wb-candidate-interoperability-kt-application-interoperability, wb-candidate-evolution-kt-architecture-evolution]
workbench_status: candidate-derived
---

# Portal composition and interoperability

This topic connects the candidate records describing the shared Portal workspace, independently owned frontend modules, and application-to-application cooperation. The records remain candidate or draft knowledge.

## Core model

- The Portal provides shared entry, shell, workspace, routing, and integration capabilities while tenant teams retain domain functionality. [[wb-candidate-background-kt-portal-purpose]]
- Root Config, the Base shell, application containers, and feature tiles have separate responsibilities and ownership boundaries. [[wb-candidate-architecture-kt-frontend-composition]]
- Loading a module and requesting a business action from another application are separate interoperability concerns. [[wb-candidate-interoperability-kt-application-interoperability]]
- Contexts, intents, authentication handoff, registration, and provider readiness require an agreed contract before joint production readiness can be claimed. [[wb-candidate-interoperability-kt-application-interoperability]]

## Open boundaries

Build-tool research, notification experiments, and proposed service decomposition remain separate investigations. The candidate records do not establish a complete application inventory, approved intent schema, deployed authentication handoff, or universal compatibility contract. [[wb-candidate-evolution-kt-architecture-evolution]]
