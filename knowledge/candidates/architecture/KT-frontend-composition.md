---
type: KnowledgeTopic
id: KT-frontend-composition
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md
  revision: sha256:572dffb64891e80af50f57d5cc2e34fe8ffb3d92751b779d25b5b8b84b999cf7
  sha256: 572dffb64891e80af50f57d5cc2e34fe8ffb3d92751b779d25b5b8b84b999cf7
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Single SPA vs Module Federation vs iFrame/page.md
  revision: sha256:160a35ff2264138ee7f53fbb9798b28848d172d07208e78ba9d98adb4ae2025d
  sha256: 160a35ff2264138ee7f53fbb9798b28848d172d07208e78ba9d98adb4ae2025d
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md
  revision: sha256:6734c72b2f533af13944ad668a4a6d6bbccd79e60e7bdfbed9e59ed528c68215
  sha256: 6734c72b2f533af13944ad668a4a6d6bbccd79e60e7bdfbed9e59ed528c68215
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Development Principle/page.md
  revision: sha256:06ce1c57bd699e5100e82a59b79c59a1cec1a8973223586a2eba9a9bda29d5b3
  sha256: 06ce1c57bd699e5100e82a59b79c59a1cec1a8973223586a2eba9a9bda29d5b3
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Development Guideline/page.md
  revision: sha256:4e7399bf03a672bb61ca5d1a30ee3275e44e779ba5f0f097db9613a3fe47391d
  sha256: 4e7399bf03a672bb61ca5d1a30ee3275e44e779ba5f0f097db9613a3fe47391d
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md
  revision: sha256:b93d2fc08759df036482b632fe9c8f8f966be1d4c98eedc235c5206a036c587f
  sha256: b93d2fc08759df036482b632fe9c8f8f966be1d4c98eedc235c5206a036c587f
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/page.md
  revision: sha256:a287cbc3a9ece0575b92860108de185b1303655322af30e9dc14a60709cb4137
  sha256: a287cbc3a9ece0575b92860108de185b1303655322af30e9dc14a60709cb4137
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_
    External Frontend Dependency Control/page.md
  revision: sha256:d95c3a34b07bccd986dee4b7508d6723ca938ef5addc44419e48d58801dca0f6
  sha256: d95c3a34b07bccd986dee4b7508d6723ca938ef5addc44419e48d58801dca0f6
- resource: knowledge/raw/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md
  revision: sha256:a1ae5104849e9ca7b6276064b6f8c7870fe55b36e7cc5c80be54b11619a1b4cf
  sha256: a1ae5104849e9ca7b6276064b6f8c7870fe55b36e7cc5c80be54b11619a1b4cf
generated:
  by: agent:codex
  at: '2026-10-15T00:38:52.657060+00:00'
verified: []
classification: architecture
scope: The documented microfrontend design, shared UI boundaries, and application onboarding flow.
summary: The design combines shared portal modules with independently owned tenant containers and tiles.
related:
- KT-portal-purpose
- KT-admin-and-onboarding
- KT-authentication-and-sessions
- KT-sdk-and-entitlements
- KT-release-operations
- KT-architecture-evolution
open_questions:
- Which exact repository revisions implement the current container, tile, and routing interfaces?
- Which development guidelines and shared dependency versions are currently accepted?
- Which owner controls compatibility changes across shared modules and tenant applications?
- Which dependency exceptions have platform review, accountable tenant ownership, and effective dates?
- Which standalone template and shared-component versions remain supported?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Frontend composition and application ownership

## Scope

This topic explains the documented composition model and the responsibilities required to onboard an application.
It connects design explanations, development guidance, and setup procedures.
It does not inspect current repository code or establish deployed interface compatibility.
The source dates and applicable framework versions remain partly unresolved.

## Summary

The design separates common platform modules from application-owned domain modules.
Import maps connect module names to deployed files.
The shared base supplies common context while tenant teams supply containers and tiles.
The [ownership design](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L130>) and [onboarding procedure](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L1>) describe this division.

## Documented knowledge

### Why the design separates modules

The microfrontend explanation identifies coupled releases, broad testing scope, unclear ownership, and repeated components as design problems.
It proposes application-specific repositories and pipelines alongside shared modules.
The intended benefit is separate team delivery within one user workspace. [Design problems and ownership](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L119>).
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

The [module design](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L147>), [stack explanation](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/page.md#L35>), and [development principles](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md#L4>) support these roles.
The table explains the source model; it does not assert the current runtime implementation.

### Ownership and availability

The principles assign shared backend availability to the microfrontend team.
They assign application-domain backend availability to each application team.
Each application team can choose its deployment approach and must supply static-file and API URLs.
The same principles reserve review and approval of shared repositories to the microfrontend team. [Team responsibilities](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md#L4>).
These are recorded role declarations; named current owners and effective approvals remain unknown.

### Documented onboarding sequence

1. Obtain root configuration and application templates.
2. Create separate application container and tile repositories.
3. Update module names, build configuration, imports, interfaces, and container entry points.
4. Update unit tests and the local import map.
5. Configure the tile through the Admin Module procedure.
6. Build and deploy the application files, then supply static-file and API URLs to the platform team.

This sequence condenses the [frontend onboarding procedure](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L1>).
The [getting-started guide](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md#L11>) describes three local projects and attached source archives.
Those archives and setup screenshots are absent from the supplied copy.
No setup command or deployment was executed during this ingestion.

### Shared code and compatibility

The design uses exports and imports to share modules through registered names.
The framework comparison distinguishes shared dependencies from libraries retained within individual applications.
It cautions that shared dependencies require coordinated upgrades. [Sharing model](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L79>); [Dependency comparison](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Single SPA vs Module Federation vs iFrame/page.md#L11>).
Inference: A shared interface change can affect several tenant consumers.
This inference requires exact provider and consumer evidence before assessing a particular change.

### Development guidance and performance boundaries

The guideline prescribes TypeScript, functional components, shared MUI themes, and separation of view, logic, styles, and interfaces.
It also names React 18.2.0 and prefers Context and Reducer over additional state libraries. [Development guideline](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L1>).
These versioned instructions must retain their source context before reuse for new development.

The onboarding procedure suggests 500 KB files and six concurrent static-file requests as optional loading guidance.
It does not establish an accepted performance SLA. [Optional loading guidance](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L15>).

### Standalone React integration pattern

The standalone guide describes a React template that reuses MFE-Base components through import-map registration.
Its no-install statement concerns consuming those components; the example still installs the template's own dependencies.
The guide also states that the template includes Jest configuration.
[Standalone template, lines 1–17](<../../raw/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L1>).

This pattern describes shared-component reuse outside the documented container-and-tile startup example.
It does not establish that every standalone application can integrate without adaptation.
The linked `simple-app.zip` archive and screenshot are absent from this supplied copy.
Current template, dependency, and loading compatibility require separate inspection.
[Standalone archive and setup, lines 7–17](<../../raw/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L7>).

### External frontend dependencies

The supplementary principle prohibits direct external GUI dependencies unless platform governance reviews and approves an exception.
It describes internal packaging and tenant-owned backend encapsulation as implementation options.
Tenant teams retain security, licensing, vulnerability, support, resilience, and rollback responsibilities.
These are source-stated rules with unconfirmed authority and effective applicability.
[Dependency principle, lines 3–10, 23–54](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_ External Frontend Dependency Control/page.md#L3>).

## Connections

- [Portal purpose](../background/KT-portal-purpose.md) explains the user and platform goals behind composition.
- [Administration and onboarding](../operations/KT-admin-and-onboarding.md) supplies tile configuration and promotion context.
- [Authentication and sessions](../security/KT-authentication-and-sessions.md) and [SDK and entitlements](../security/KT-sdk-and-entitlements.md) describe identity propagation across these boundaries.
- [Release operations](../operations/KT-release-operations.md) describes controlled delivery and rollback procedures.
- [Architecture evolution](../evolution/KT-architecture-evolution.md) distinguishes existing guidance from migration proposals.

## Evidence limits

Evidence: The [source manifest](../../raw/manifest.yaml) identifies local bytes without original page revisions or confirmed source authority.
Consequence: The citations support a reproducible reading but do not establish approved or current project intent.
Owner: unknown.
Next action: Confirm source ownership, applicability, and original revisions before publication.

Evidence: The [getting-started guide](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md#L13>) depends on missing archives and screenshots.
Consequence: The supplied text cannot reproduce its complete setup procedure.
Owner: unknown.
Next action: Recover the applicable templates and compare them with exact registered repository revisions.

Evidence: The [guideline](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L2>) names an older React version without an effective-date or supersession record.
Consequence: Its technical instructions cannot establish the current platform baseline.
Owner: unknown.
Next action: Confirm accepted versions, shared dependency policy, and applicable guideline revisions.

Evidence: The [framework comparison](<../../raw/confluence/FM TPT UI Guild/Microfrontend/Single SPA vs Module Federation vs iFrame/page.md#L18>) contains scores and technical opinions without retained project measurements.
Consequence: Its ranking cannot establish current compatibility, security, or performance.
Owner: unknown.
Next action: Treat it as historical rationale and collect project evidence for any new framework decision.

Evidence: The [standalone guide](<../../raw/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L7>) depends on an absent template archive.
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
