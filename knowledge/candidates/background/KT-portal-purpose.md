---
type: KnowledgeTopic
id: KT-portal-purpose
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: knowledge/raw/confluence/FM TPT UI Guild/page.md
  revision: sha256:6b458e2eaba665a6b28512ae08f1b928c3593be0980595bd7f3e56f27bb273b8
  sha256: 6b458e2eaba665a6b28512ae08f1b928c3593be0980595bd7f3e56f27bb273b8
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md
  revision: sha256:3849130c1253c6e5da38c63fa43e8d3afb4258d271b3f5548762dcb661c6979d
  sha256: 3849130c1253c6e5da38c63fa43e8d3afb4258d271b3f5548762dcb661c6979d
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal
    Capabilities/page.md
  revision: sha256:43f0376aec7a5453ef401509865738f85380f6f665607caf9bf2e94f98d6398b
  sha256: 43f0376aec7a5453ef401509865738f85380f6f665607caf9bf2e94f98d6398b
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal
    Principles (Draft)/page.md
  revision: sha256:7c99a4cd761b9590aa4ecc721718537892267d6af98ef0b11062393d281bc012
  sha256: 7c99a4cd761b9590aa4ecc721718537892267d6af98ef0b11062393d281bc012
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md
  revision: sha256:6a6cd47cad4a73d0e98b3f3c61b93d63a710adf6c965ca800d4bb472b97a34ce
  sha256: 6a6cd47cad4a73d0e98b3f3c61b93d63a710adf6c965ca800d4bb472b97a34ce
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md
  revision: sha256:572dffb64891e80af50f57d5cc2e34fe8ffb3d92751b779d25b5b8b84b999cf7
  sha256: 572dffb64891e80af50f57d5cc2e34fe8ffb3d92751b779d25b5b8b84b999cf7
generated:
  by: agent:codex
  at: '2026-10-15T00:38:52.657060+00:00'
verified: []
classification: background
scope: The supplied portal and UI platform materials, including draft principles and future deployment proposals.
summary: The portal connects tenant applications through shared entry, composition, authentication, and operating
  capabilities.
related:
- KT-frontend-composition
- KT-authentication-and-sessions
- KT-sdk-and-entitlements
- KT-admin-and-onboarding
- KT-application-interoperability
- KT-observability-and-performance
- KT-release-operations
- KT-architecture-evolution
open_questions:
- Which owner can confirm the current portal name, scope, and capability inventory?
- Which draft principles became accepted rules, and when?
- Which 2026 and 2027 proposals have approved scope or deployed implementations?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Portal purpose and capability map

## Scope

This topic connects the portal's stated purpose, common platform functions, and tenant application responsibilities.
It covers the supplied UI platform materials.
It does not establish complete Financial Markets business-domain coverage.
The exported page revisions, authors, and approval states remain unconfirmed.

## Summary

The guild aims to provide consistent design, shared components, and utilities across application teams.
The portal supplies a common entry and workspace for post-trade applications.
Application teams retain their domain functions while the platform supplies shared integration capabilities.
These statements synthesize the [guild mission](<../../raw/confluence/FM TPT UI Guild/page.md#L8>) and [portal introduction](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md#L5>).

## Documented knowledge

### Business purpose

The portal introduction names affirmation, confirmation, settlements, and reporting as supported post-trade activities.
It lists blotters, a rules engine, and other tools as examples.
The page explicitly remains under edit.
These examples describe its stated scope, not a complete application inventory. [Portal design](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md#L1>).

The guild separates common UI work from application teams' business delivery.
It proposes shared themes, components, utilities, and collaboration through one design language.
The portal is one implementation of that UI approach. [Guild vision and mission](<../../raw/confluence/FM TPT UI Guild/page.md#L3>).

### Working vocabulary

| Term | Meaning in these materials |
| --- | --- |
| Tenant application | A domain application integrated into the shared portal. |
| Tile | An application view that a user opens in a workspace. |
| Workspace | A user area that holds opened tiles. |
| Container | An application-owned module or the shared base that supplies common context. |
| Import map | A mapping used to locate modules for dynamic loading. |

The [tile lifecycle description](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L63>) and [module ownership design](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L130>) support these terms.
The sources use container for both common and application-specific roles.
Keep the role explicit when describing an interface.

### Capability boundaries

| Concern | Capability described in the supplied material |
| --- | --- |
| Entry and identity | Common application entry, SSO, MFA, and session renewal. |
| Composition | Shared themes, dynamic module loading, tiles, and workspaces. |
| Access | EMS2 roles and configured tile eligibility. |
| Administration | Configuration management and tenant onboarding. |
| Integration | Tenant UI and API routing through the portal's Nginx boundary. |
| Observation | Analytics for user activity and performance. |
| Interoperability | Cross-application interaction, with FDC3 explicitly marked as in progress. |

This map summarizes the [capabilities page](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L3>).
That page mixes present-tense descriptions with an unfinished FDC3 item.
The wording does not establish deployed or tested coverage for each capability.

### User and application flow

The capabilities page describes one entry, authentication, tile selection, and multiple workspaces.
It connects module loading with import maps and renewal with session control.
This sequence explains how the documented capabilities fit together.
It is a synthesis, not retained execution evidence. [Entry and lifecycle descriptions](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L3>).

### Scope and roadmap

The draft principles focus on SSO, tile authorization, interoperability, action tracing, and a forthcoming notification center.
Their login and tile eligibility statements remain draft intent. [Draft principles](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L1>).

The deployment proposal names onboarding changes, workflow AI, telemetry, and infrastructure migration for 2026 and early 2027.
It also lists notification, dashboards, and OpenFin as refining requirements.
Its target service list describes a proposed decomposition. [Deployment proposal](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3>).
These targets must remain distinct from the capability inventory and current implementation.

## Connections

- [Frontend composition](../architecture/KT-frontend-composition.md) explains modules, ownership, loading, and shared dependencies.
- [Authentication and sessions](../security/KT-authentication-and-sessions.md) and [SDK and entitlements](../security/KT-sdk-and-entitlements.md) explain identity and downstream access boundaries.
- [Administration and onboarding](../operations/KT-admin-and-onboarding.md) and [Release operations](../operations/KT-release-operations.md) explain integration and operating procedures.
- [Application interoperability](../interoperability/KT-application-interoperability.md) and [Observability and performance](../observability/KT-observability-and-performance.md) explain cross-application context and observations.
- [Architecture evolution](../evolution/KT-architecture-evolution.md) separates historical evaluation from proposed changes.

## Evidence limits

Evidence: The [source manifest](../../raw/manifest.yaml) identifies local bytes without original page revisions or confirmed source authority.
Consequence: The citations support a reproducible reading but do not establish approved or current project intent.
Owner: unknown.
Next action: Confirm source ownership, applicability, and original revisions before publication.

Evidence: The [portal introduction](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md#L1>) remains under edit, and [principles](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L1>) remain draft.
Consequence: This topic cannot establish accepted scope or enforceable business rules.
Owner: unknown.
Next action: Confirm scope, naming, and accepted principles with the accountable platform owner.

Evidence: The [capabilities page](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L7>) depends on screenshots absent from the supplied export.
Consequence: This topic preserves textual meaning but cannot reconstruct the illustrated behavior.
Owner: unknown.
Next action: Recover relevant screenshots and compare their meaning with the text.

Evidence: The [deployment proposal](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3>) describes future changes without an approval record in these materials.
Consequence: Target services and planned features cannot serve as current implementation facts.
Owner: unknown.
Next action: Link approved requirements and exact implementation evidence when investigating each proposal.

## Open questions

Owner: unknown for all questions.

- Which owner can confirm the current portal name, scope, and capability inventory?
- Which draft principles became accepted rules, and when?
- Which 2026 and 2027 proposals have approved scope or deployed implementations?

Next action: Resolve these questions before using this topic as approved project intent.
