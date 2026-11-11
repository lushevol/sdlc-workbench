---
title: "Architecture evolution and proposal boundaries"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/evolution/KT-architecture-evolution.md
source: raw/workbench/knowledge/candidates/evolution/KT-architecture-evolution.md
source_hash: e89f82a3803eb61b
last_updated: 2026-11-11
candidate_id: KT-architecture-evolution
candidate_version: 2
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: evolution
workbench_origin: knowledge/candidates/evolution/KT-architecture-evolution.md
workbench_sha256: e89f82a3803eb61b562c419e82df1ed29f44c1510d6499aa731821ae08114552
workbench_status: candidate-derived
---

# Architecture evolution and proposal boundaries

## Scope

This topic preserves the relationships between historical evaluations, technical experiments, and future platform proposals.
It separates documented recommendations from adoption evidence.
The materials do not establish one continuous, approved architecture roadmap.

## Summary

Component-library comparisons address design consistency and application needs.
Build-tool research addresses development tooling within the microfrontend architecture.
Notification experiments explore common event delivery across tiles.
The deployment proposal describes broader platform changes for 2026 and early 2027.
Their decision status and implementation relationships remain unresolved.

## Documented knowledge

### Component-library evaluation

The library comparison records GitHub statistics dated 5 July 2023.
It compares MUI, Ant Design, and AG Grid across components, styling, licensing, and related criteria.
The Ant Design note emphasizes forms, feedback components, and layout differences. [Library comparison](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/page.md#L1>); [Ant Design assessment](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/Usage of Ant Design/page.md#L1>).
These records explain evaluation concerns at their stated historical context.
They do not establish present library capabilities or an accepted purchasing decision.

The conceptual-design draft contains unresolved rationale and selection placeholders.
Its review and decision tables do not establish completed approval.
Its approval link points to a ClickHouse design without explaining relevance. [Draft assessment](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/Draft/Conceptual Design DRAFT/page.md#L7>); [Draft review and decision sections](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/Draft/Conceptual Design DRAFT/page.md#L169>).
Keep this draft separate from a completed architecture decision.

### Composition as a migration constraint

The UI stack explanation distinguishes SystemJS module resolution from single-spa lifecycle management.
The development guideline records shared MUI themes and a specific React version. [Stack responsibilities](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/page.md#L35>); [Guideline baseline](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L1>).
These materials explain why a tooling migration must consider more than individual application builds.
Inference: Changed output formats or shared dependencies can affect the portal loading boundary.
The applicable implementation versions require inspection before validating that inference for a proposed migration.

### Build-tool research

The research recommends Rspack for incremental migration from Webpack and Vite for new or simpler applications.
It treats SystemJS compatibility as an architectural constraint.
Its proposed pilot checks loading, HMR, and asset paths before gradual rollout. [Research conclusions](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L13>); [Pilot proposal](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L261>).

The report also proposes a longer-term move away from SystemJS.
That suggestion changes the platform boundary beyond a bundler substitution. [Long-term proposal](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L369>).
The supplied report lacks a publication date and retained project benchmark provenance.
Its recommendations remain research statements, not verified technical conclusions or accepted migration instructions.

### Notification experiments

The notification draft describes many tiles opening separate subscription connections.
It proposes one SSE connection per user to reduce browser resources. [Problem and objective](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/page.md#L58>).
This is proposed behavior; the source does not establish an accepted connection limit or deployed service.

The materials describe three distinct experiments.
One uses GraphQL over SSE with a Node.js backend.
Another uses GraphQL over WebSocket with Spring Boot.
A third uses SSE with a Spring Boot backend. [GraphQL SSE POC](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/POC GraphQL over SSE/page.md#L11>); [WebSocket POC](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/POC GraphQL over WebSocket/page.md#L11>); [Spring SSE POC](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/POC SSE using Spring Boot/page.md#L11>).
Their branch and demonstration references establish experiment locations, not successful retained execution.

The store draft considers tile reactions through React effects or registered callbacks.
It declares `isRead` as a string but assigns boolean `false` in its event handler. [Store draft](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L1>); [Event handler](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L63>).
The field contract remains unresolved and must not become a generated implementation requirement without review.

### Notification entity and retention draft

The table draft separates notification topics, user subscriptions, notification messages, and each user's read or display state.
Topics connect container, module, tile, endpoint, and subscription payload.
User-topic records add enabled and muted preferences.
Notification records carry message payloads; user-notification records hold read and display flags.
[Notification table draft, lines 1–11, 18–32](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Table Schema/page.md#L1>).

The same draft suggests one-hour, six-hour, or 24-hour retention for messages and per-user notification data.
These are unresolved alternatives, not an approved retention policy.
The draft does not establish cleanup behavior or how retention interacts with unread notifications.
[Retention alternatives, lines 20 and 30](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Table Schema/page.md#L20>).

### Platform proposals for 2026 and early 2027

The deployment proposal describes tenant changes, workflow AI, telemetry, and infrastructure migration.
It lists notification, persona dashboards, and OpenFin as refining requirements.
Its target deployment names separate authentication, tile-management, telemetry, and AI services. [Proposed changes](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3>); [Target services](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L58>).

The current-architecture section has no explanatory content.
The target logical-architecture section has no explanatory content either.
The proposed service names therefore do not define their interfaces or migration path. [Architecture sections](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L1>); [Target logical architecture](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L49>).

### Unchecked future-work list

A separate unchecked list proposes central-monitoring foundation work and an upgrade to Spring Boot 4.0.6.
It also proposes moving properties into services and removing account-and-password login.
The list supplies proposed work, without completion records, migration order, or accepted scope.
Its wording cannot establish current platform versions or enabled login methods.
[Unchecked work list, lines 1–4](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operation One TODO List/page.md#L1>).

## Connections

- Portal purpose ([[wb-candidate-background-kt-portal-purpose]]) supplies the capability context for these proposals.
- Frontend composition ([[wb-candidate-architecture-kt-frontend-composition]]) supplies the documented loading and ownership boundaries.
- Application interoperability ([[wb-candidate-interoperability-kt-application-interoperability]]) covers OpenFin and cross-application context.
- Observability and performance ([[wb-candidate-observability-kt-observability-and-performance]]) distinguishes monitoring and reported measurements from proposal estimates.
- Release operations ([[wb-candidate-operations-kt-release-operations]]) provides operating constraints for an eventual migration.

## Evidence limits

Evidence: The [source manifest](../../../../evidence/knowledge/manifest.yaml) identifies local bytes without original page revisions or confirmed source authority.
Consequence: The citations support a reproducible reading but do not establish approved or current project intent.
Owner: unknown.
Next action: Confirm source ownership, applicability, and original revisions before publication.

Evidence: The [library comparison](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/page.md#L3>) dates some statistics to 2023, while the [conceptual draft](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/Draft/Conceptual Design DRAFT/page.md#L7>) retains placeholders.
Consequence: Historical comparison and incomplete rationale cannot establish an accepted current technology standard.
Owner: unknown.
Next action: Locate the completed component and licensing decisions, including their effective versions.

Evidence: The [build-tool report](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L52>) provides benchmark tables without retained inputs or execution records.
Consequence: Its performance rankings cannot predict results for these repositories.
Owner: unknown.
Next action: Identify the report's provenance and evaluate a bounded project pilot before adopting its recommendation.

Evidence: The [notification draft](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/page.md#L92>) references experiments and absent demonstration materials.
Consequence: The chosen protocol, supported schema, and production adoption remain unproved.
Owner: unknown.
Next action: Locate the accepted notification decision, supported code revision, and relevant execution evidence.

Evidence: The [deployment proposal](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L49>) leaves architectural detail incomplete.
Consequence: AI cannot infer service contracts, migration order, or approved delivery scope from its target list.
Owner: unknown.
Next action: Obtain accepted requirements and a complete design before deriving implementation tasks.

Evidence: The [notification table draft](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Table Schema/page.md#L20>) gives three retention alternatives.
Consequence: An implementation cannot derive an accepted cleanup interval or unread-message rule from this draft.
Owner: unknown.
Next action: Agree notification ownership, retention, cleanup, and unread-message behavior before deriving acceptance criteria.

## Open questions

Owner: unknown for all questions.

- Which component-library and licensing choices have accepted decisions and effective dates?
- Who authored the build-tool research, and which versions and benchmark runs support it?
- Which notification experiment, if any, became a supported portal service?
- Which 2026 and 2027 target services have approved requirements and deployed implementations?

- Which notification retention and unread-message rules have accepted decisions?
- Which unchecked work items have accepted scope, owners, and completion evidence?

Next action: Resolve decision status and applicability before combining these materials into a current architecture baseline.
