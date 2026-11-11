---
title: "Frontend composition and application ownership"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/architecture/KT-frontend-composition.md
source: raw/workbench/knowledge/candidates/architecture/KT-frontend-composition.md
source_hash: c3a94ee436261ed9
last_updated: 2026-11-11
candidate_id: KT-frontend-composition
candidate_version: 3
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: architecture
workbench_origin: knowledge/candidates/architecture/KT-frontend-composition.md
workbench_sha256: c3a94ee436261ed95cf91fe02bcb4c15965a95cea03a548070a96f16529b2718
workbench_status: candidate-derived
---

# Frontend composition and application ownership

## Scope

This topic explains the documented composition model and the responsibilities required to onboard an application.
It connects design explanations, development guidance, and setup procedures.
The linked architecture clarification adds bounded inspection of current local source.
Deployed interface compatibility remains unconfirmed.
The source dates and applicable framework versions remain partly unresolved.

## Summary

The design separates common platform modules from application-owned domain modules.
Import maps connect module names to deployed files.
The shared base supplies common context while tenant teams supply containers and tiles.
The [ownership design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L130>) and [onboarding procedure](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L1>) describe this division.

## Documented knowledge

### Current four-layer clarification

The user identifies four layers: Root Config, Base shell, application container, and feature tile.
The service relationship record ([[wb-candidate-architecture-arc-portal-service-relationships]]) retains the layer roles and inspected loading paths.
Single-SPA registers only the shell. SystemJS and React Router support successive container and tile loading.
Container and tile props select distinct route stages.

The [clarification](../../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L7-L12) supplies current reported architecture.
The [source review](../../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) records matching local declarations and limits.
JavaScript entry bundles can produce lazy chunks. Shared-code dependencies also point back toward common libraries.
This clarification does not establish runtime rendering, accepted dependency versions, or active deployment.

### Why the design separates modules

The microfrontend explanation identifies coupled releases, broad testing scope, unclear ownership, and repeated components as design problems.
It proposes application-specific repositories and pipelines alongside shared modules.
The intended benefit is separate team delivery within one user workspace. [Design problems and ownership](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L119>).
These are design goals; the document does not demonstrate their achievement across every application.

### Roles in composition

| Element | Documented responsibility |
| --- | --- |
| Root configuration and import map | Locate modules and support shared loading configuration. |
| SystemJS | Resolve module names to files and load modules into the page. |
| Single-spa | Mount applications and manage application lifecycle. |
| Base container | Provide common routing, global state, and theme context. |
| Application container | Connect an application's domain modules with the shared portal. |
| Application tiles | Supply user-facing domain views that open within workspaces. |
| Nginx integration | Route application static files and API requests through configured locations. |

The [module design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L147>), [stack explanation](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/page.md#L35>), and [development principles](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md#L4>) support these roles.
The table explains the source model; it does not assert the current runtime implementation.

### Ownership and availability

The principles assign shared backend availability to the microfrontend team.
They assign application-domain backend availability to each application team.
Each application team can choose its deployment approach and must supply static-file and API URLs.
The same principles reserve review and approval of shared repositories to the microfrontend team. [Team responsibilities](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md#L4>).

The sources record role declarations. Current named owners and effective approvals remain unknown.

### Documented onboarding sequence

1. Obtain root configuration and application templates.
2. Create separate application container and tile repositories.
3. Update module names, build configuration, imports, interfaces, and container entry points.
4. Update unit tests and the local import map.
5. Configure the tile through the Admin Module procedure.
6. Build and deploy the application files, then supply static-file and API URLs to the platform team.

This sequence condenses the [frontend onboarding procedure](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L1>).
The [getting-started guide](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md#L11>) describes three local projects and attached source archives.
Those archives and setup screenshots are absent from the supplied copy.
This ingestion executed no setup command or deployment.

### Shared code and compatibility

The design uses exports and imports to share modules through registered names.
The framework comparison distinguishes shared dependencies from libraries retained within individual applications.
It cautions that shared dependencies require coordinated upgrades. [Sharing model](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L79>); [Dependency comparison](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Single SPA vs Module Federation vs iFrame/page.md#L11>).
Inference: A shared interface change can affect several tenant consumers.
This inference requires exact provider and consumer evidence before assessing a particular change.

### Development guidance and performance boundaries

The guideline prescribes TypeScript, functional components, shared MUI themes, and separation of view, logic, styles, and interfaces.
It also names React 18.2.0 and prefers Context and Reducer over additional state libraries. [Development guideline](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L1>).
These versioned instructions must retain their source context before reuse for new development.

The onboarding procedure suggests 500 KB files and six concurrent static-file requests as optional loading guidance.
It does not establish an accepted performance SLA. [Optional loading guidance](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L15>).

### Standalone React integration pattern

The standalone guide describes a React template that reuses MFE-Base components through import-map registration.
Its no-install statement concerns consuming those components; the example still installs the template's own dependencies.
The guide also states that the template includes Jest configuration.
[Standalone template, lines 1–17](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L1>).

This pattern describes shared-component reuse outside the documented container-and-tile startup example.
It does not establish that every standalone application can integrate without adaptation.
The linked `simple-app.zip` archive and screenshot are absent from this supplied copy.
Current template, dependency, and loading compatibility require separate inspection.
[Standalone archive and setup, lines 7–17](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L7>).

### External frontend dependencies

The supplementary principle prohibits direct external GUI dependencies unless platform governance reviews and approves an exception.
It describes internal packaging and tenant-owned backend encapsulation as implementation options.
Tenant teams retain security, licensing, vulnerability, support, resilience, and rollback responsibilities.
These are source-stated rules with unconfirmed authority and effective applicability.
[Dependency principle, lines 3–10, 23–54](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_ External Frontend Dependency Control/page.md#L3>).

## Connections

- Portal purpose ([[wb-candidate-background-kt-portal-purpose]]) explains the user and platform goals behind composition.
- Administration and onboarding ([[wb-candidate-operations-kt-admin-and-onboarding]]) supplies tile configuration and promotion context.
- Authentication and sessions ([[wb-candidate-security-kt-authentication-and-sessions]]) and SDK and entitlements ([[wb-candidate-security-kt-sdk-and-entitlements]]) describe identity propagation across these boundaries.
- Release operations ([[wb-candidate-operations-kt-release-operations]]) describes controlled delivery and rollback procedures.
- Architecture evolution ([[wb-candidate-evolution-kt-architecture-evolution]]) distinguishes existing guidance from migration proposals.

## Evidence limits

Evidence: The [source manifest](../../../../evidence/knowledge/manifest.yaml) identifies local bytes without original page revisions or confirmed source authority.
Consequence: The citations support a reproducible reading but do not establish approved or current project intent.
Owner: unknown.
Next action: Confirm source ownership, applicability, and original revisions before publication.

Evidence: The [getting-started guide](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md#L13>) depends on missing archives and screenshots.
Consequence: The supplied text cannot reproduce its complete setup procedure.
Owner: unknown.
Next action: Recover the applicable templates and compare them with exact registered repository revisions.

Evidence: The [guideline](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L2>) names an older React version without an effective-date or supersession record.
Consequence: Its technical instructions cannot establish the current platform baseline.
Owner: unknown.
Next action: Confirm accepted versions, shared dependency policy, and applicable guideline revisions.

Evidence: The [framework comparison](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Single SPA vs Module Federation vs iFrame/page.md#L18>) contains scores and technical opinions without retained project measurements.
Consequence: Its ranking cannot establish current compatibility, security, or performance.
Owner: unknown.
Next action: Treat it as historical rationale and collect project evidence for any new framework decision.

Evidence: The [standalone guide](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L7>) depends on an absent template archive.
Consequence: Its reuse instructions cannot establish runnable setup or current shared-component compatibility.
Owner: unknown.
Next action: Recover the applicable template and inspect its import map, shared dependencies, and retained test assertions.

## Open questions

Owner: unknown for all questions.

- Which exact repository revisions implement the current container, tile, and routing interfaces?
- Which development guidelines and shared dependency versions are currently accepted?
- Which owner controls compatibility changes across shared modules and tenant applications?
- Which dependency exceptions have platform review, accountable tenant ownership, and effective dates?

- Which standalone template and shared-component versions remain supported?

Next action: Resolve the relevant boundary before using this topic to implement a new application or shared change.
