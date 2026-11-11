---
title: "Portal purpose and capability map"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/background/KT-portal-purpose.md
source: raw/workbench/knowledge/candidates/background/KT-portal-purpose.md
source_hash: 29b0432d30bd7ae2
last_updated: 2026-11-11
candidate_id: KT-portal-purpose
candidate_version: 2
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: background
workbench_origin: knowledge/candidates/background/KT-portal-purpose.md
workbench_sha256: 29b0432d30bd7ae28dc636bfce8834e7297c9af6cd59e0632bbc9eb57e3ab620
workbench_status: candidate-derived
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
These statements synthesize the [guild mission](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/page.md#L8>) and [portal introduction](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md#L5>).

## Documented knowledge

### Business purpose

The portal introduction names affirmation, confirmation, settlements, and reporting as supported post-trade activities.
It lists blotters, a rules engine, and other tools as examples.
The page explicitly remains under edit.
These examples describe its stated scope, not a complete application inventory. [Portal design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md#L1>).

The guild separates common UI work from application teams' business delivery.
It proposes shared themes, components, utilities, and collaboration through one design language.
The portal is one implementation of that UI approach. [Guild vision and mission](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/page.md#L3>).

### Working vocabulary

| Term | Meaning in these materials |
| --- | --- |
| Tenant application | A domain application integrated into the shared portal. |
| Tile | An application view that a user opens in a workspace. |
| Workspace | A user area that holds opened tiles. |
| Container | An application-owned module or the shared base that supplies common context. |
| Import map | A mapping used to locate modules for dynamic loading. |

The [tile lifecycle description](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L63>) and [module ownership design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L130>) support these terms.
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

This map summarizes the [capabilities page](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L3>).
That page mixes present-tense descriptions with an unfinished FDC3 item.
The wording does not establish deployed or tested coverage for each capability.

### User and application flow

The capabilities page describes one entry, authentication, tile selection, and multiple workspaces.
It connects module loading with import maps and renewal with session control.
This sequence explains how the documented capabilities fit together.
It is a synthesis, not retained execution evidence. [Entry and lifecycle descriptions](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L3>).

### Scope and roadmap

The draft principles focus on SSO, tile authorization, interoperability, action tracing, and a forthcoming notification center.
Their login and tile eligibility statements remain draft intent. [Draft principles](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L1>).

The deployment proposal names onboarding changes, workflow AI, telemetry, and infrastructure migration for 2026 and early 2027.
It also lists notification, dashboards, and OpenFin as refining requirements.
Its target service list describes a proposed decomposition. [Deployment proposal](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3>).
These targets must remain distinct from the capability inventory and current implementation.

## Connections

- Frontend composition ([[wb-candidate-architecture-kt-frontend-composition]]) explains modules, ownership, loading, and shared dependencies.
- Authentication and sessions ([[wb-candidate-security-kt-authentication-and-sessions]]) and SDK and entitlements ([[wb-candidate-security-kt-sdk-and-entitlements]]) explain identity and downstream access boundaries.
- Administration and onboarding ([[wb-candidate-operations-kt-admin-and-onboarding]]) and Release operations ([[wb-candidate-operations-kt-release-operations]]) explain integration and operating procedures.
- Application interoperability ([[wb-candidate-interoperability-kt-application-interoperability]]) and Observability and performance ([[wb-candidate-observability-kt-observability-and-performance]]) explain cross-application context and observations.
- Architecture evolution ([[wb-candidate-evolution-kt-architecture-evolution]]) separates historical evaluation from proposed changes.

## Evidence limits

Evidence: The [source manifest](../../../../evidence/knowledge/manifest.yaml) identifies local bytes without original page revisions or confirmed source authority.
Consequence: The citations support a reproducible reading but do not establish approved or current project intent.
Owner: unknown.
Next action: Confirm source ownership, applicability, and original revisions before publication.

Evidence: The [portal introduction](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md#L1>) remains under edit, and [principles](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L1>) remain draft.
Consequence: This topic cannot establish accepted scope or enforceable business rules.
Owner: unknown.
Next action: Confirm scope, naming, and accepted principles with the accountable platform owner.

Evidence: The [capabilities page](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L7>) depends on screenshots absent from the supplied export.
Consequence: This topic preserves textual meaning but cannot reconstruct the illustrated behavior.
Owner: unknown.
Next action: Recover relevant screenshots and compare their meaning with the text.

Evidence: The [deployment proposal](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3>) describes future changes without an approval record in these materials.
Consequence: Target services and planned features cannot serve as current implementation facts.
Owner: unknown.
Next action: Link approved requirements and exact implementation evidence when investigating each proposal.

## Open questions

Owner: unknown for all questions.

- Which owner can confirm the current portal name, scope, and capability inventory?
- Which draft principles became accepted rules, and when?
- Which 2026 and 2027 proposals have approved scope or deployed implementations?

Next action: Resolve these questions before using this topic as approved project intent.
