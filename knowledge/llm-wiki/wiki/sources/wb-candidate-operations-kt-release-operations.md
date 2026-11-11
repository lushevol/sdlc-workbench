---
title: "Portal release and tenant operation boundaries"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/operations/KT-release-operations.md
source: raw/workbench/knowledge/candidates/operations/KT-release-operations.md
source_hash: e81bca3a19c30837
last_updated: 2026-11-11
candidate_id: KT-release-operations
candidate_version: 2
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: operations
workbench_origin: knowledge/candidates/operations/KT-release-operations.md
workbench_sha256: e81bca3a19c3083724b84ef78b5d3b0c47546d380624043019e1d493f471f1cb
workbench_status: candidate-derived
---

# Portal release and tenant operation boundaries

## Scope

This topic connects release planning with tenant configuration promotion and production readiness.
The supplied materials contain procedures, an unfinished checklist, historical deployment guidance, and a release proposal.
Their current authority remains unconfirmed.

## Summary

Portal changes and tenant deployments have separate responsibilities.
Configuration promotion connects tenant metadata, routing, authentication, entitlements, and validation.
Technical deployment and business activation require distinct evidence.
The release proposal contains unresolved duration and confirmation rules.

## Documented knowledge

### Ownership and release scope

The proposal covers Portal routing, route enabling, tenant interfaces, and Portal-owned production changes.
Tenant teams retain responsibility for their UI, backend, services, databases, and infrastructure.
Portal teams execute Portal releases and routing rollback.
Tenant teams validate their applications, perform UVT, and support tenant issues.
These are documented responsibility statements, without confirmed present approval.
[Release proposal, sections 2 and 7, lines 25–40 and 119–131](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L25>)

### Readiness before scheduling

The proposal requests solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning.
New interfaces require 30 days of engagement under the proposal.
The unfinished checklist adds SDK validation, shared frontend requests, entitlement checks, disaster recovery, and performance inputs.
It also identifies operating agreements and penetration testing as onboarding inputs.
These statements describe requested readiness, without proving completed checks.
[Release proposal, sections 4–5, lines 58–98](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L58>)
[Checklist, lines 1–29](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L1>)

### Configuration promotion

The documented flow starts with Module Map, Drawer Category, and Tile Configuration changes in Development.
Teams export those records as CSV files and retain them in a tenant-owned repository.
An ADO pipeline then uploads configuration to the Portal Admin service.
The documented upload interface is `/api/auth/v1/fmo/admin/config/upload`.
The flow states that the service validates an FMAA JWT before processing CSV files.
This describes the procedure; this ingestion inspected no upload execution.
[Admin release flow, lines 3–24](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3>)

The first bulk insert into UAT and Production uses a separate BFF release under this guide.
Later uploads depend on tenant connectivity to the Admin service.
The checklist also flags planned FMAA decommissioning.
That warning creates an unresolved dependency for the documented promotion workflow.
[Admin release flow, lines 14–17 and 53–57](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L14>)
[Checklist, line 16](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L16>)

### Tenant capabilities described in requests

Release requests explain why tenant tiles need Portal integration.
The following descriptions identify intended business functions from those requests.
They do not establish approved detailed rules, release completion, or present availability.

| Requested capability | Documented purpose | Evidence |
| --- | --- | --- |
| FSS Cash Projection | Supply a cash-projection rule-engine tile. | [Cash Projection request, lines 9–10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS DS Cash Projection Change Request/page.md#L9>) |
| FSS Funds Gating | Limit investor redemptions to a percentage of daily net asset value. | [FSS capability descriptions, line 10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS Gating, SSI, CA Domestic and Gold Custody Change Request/page.md#L10>) |
| FSS SSI | Generate settlement instructions from stored agent accounts, with email and download options. | [FSS capability descriptions, line 10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS Gating, SSI, CA Domestic and Gold Custody Change Request/page.md#L10>) |
| FSS Domestic Disbursement | Reconcile depository files and create MT566 messages after credit for downstream processing. | [FSS capability descriptions, line 10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS Gating, SSI, CA Domestic and Gold Custody Change Request/page.md#L10>) |
| FSS Gold Custody | Capture purchases and sales, settle services, and produce daily position updates. | [FSS capability descriptions, line 10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS Gating, SSI, CA Domestic and Gold Custody Change Request/page.md#L10>) |
| FSS Digital Asset Collateral | Support collateral use of custodied digital assets and counterparty-risk reduction. | [FSS capability descriptions, line 10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS Gating, SSI, CA Domestic and Gold Custody Change Request/page.md#L10>) |
| DDR Reporting | Show reports received from upstream systems and forwarded downstream. | [DDR request, lines 4–5](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L4>) |
| CDUPS Confirmation | Manage outbound confirmation documents and inbound confirmations in separate blotters. | [CDUPS request, lines 9–10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/Markets Operation One Change Request - CDUPS/page.md#L9>) |
| VPA Fix Link | Correct broken links so subsequent trade processing can continue. | [VPA request, lines 9–10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/VPA Fix-link and Monitor Change Request/page.md#L9>) |
| VPA Trade Monitor | Monitor trade status and retrieve source and transformed files. | [VPA request, lines 9–10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/VPA Fix-link and Monitor Change Request/page.md#L9>) |

### Release window proposal

The proposal schedules first, third, and available fifth Saturdays, starting at 09:00 SGT.
It freezes scope after Monday EOD in the first week of the release window.
It cancels windows without requests and requires approved exceptions for late additions.
Freeze periods require rescheduling or dispensation under the proposal.
These rules remain proposed context pending authority and ambiguity resolution.
[Release proposal, sections 3–6, lines 44–115](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L44>)

The summary specifies 24 hours, while the detailed table specifies 10 hours and a 19:00 SGT finish.
The urgent-release section requires all confirmations but also permits proceeding when nobody raises concerns.
Silence and explicit confirmation are different conditions.
This topic does not choose between these alternatives.
[Release proposal, lines 17–19, 50–52, and 144–151](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L17>)

### Technical and business activation

The release calendar distinguishes Portal release dates from tenant release dates.
It also lists separate Entra technical and business go-live entries.
The OpenFin briefing similarly separates technical onboarding from business user onboarding.
A calendar entry establishes planning context, without proving deployment, approval, or successful adoption.
[Release calendar, lines 5–16](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/page.md#L5>)
[OpenFin briefing, release phases, lines 157–163](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L157>)

The DDR request states that business UAT sign-off follows technical go-live.
It lists separate technical and business target dates.
The VPA request also separates Portal and application go-live dates.
The request template explicitly allows Portal deployment before the application deployment.
These records describe sequencing; their dates do not prove completed deployments or business acceptance.
[DDR request, lines 9–17](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L9>)
[VPA request, lines 20–22](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/VPA Fix-link and Monitor Change Request/page.md#L20>)
[Request template, lines 21–23](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/[Template] Markets Operations One Change Request/page.md#L21>)

Requests also expose incomplete readiness evidence.
The CDUPS request leaves UAT sign-off, user profiles, user counts, and UVT details unprovided.
The DDR request records pending connectivity and separates technical sign-off from business validation.
Several VPA evidence references are struck through.
Missing or withdrawn references cannot establish the corresponding release gate.
[CDUPS request, lines 14–21](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/Markets Operation One Change Request - CDUPS/page.md#L14>)
[DDR request, lines 9–13](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L9>)
[VPA request, lines 12–22](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/VPA Fix-link and Monitor Change Request/page.md#L12>)

The blank request template includes DNS resolution and expected total, new, and concurrent users.
It asks separately for routing changes, connectivity evidence, sign-off, and UVT contacts.
These are expected request fields, without evidence that a specific request satisfies them.
[Request template, lines 9–23](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/[Template] Markets Operations One Change Request/page.md#L9>)

### Deployment evolution

The older frontend deployment guide describes static artifacts and a proposed blue-green model.
Its Pilot and Production environments share a backend.
The guide separates feature checks, artifact publication, and manual production deployment after approval.
The Nginx draft proposes versioned configuration, syntax checks, restart checks, and rollback.
Neither document establishes the currently deployed pipeline.
[Frontend deployment, lines 3–11 and 41–73](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-Frontend Deployment/page.md#L3>)
[Nginx deployment draft, lines 1–34](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/Nginx Automated Deployment Solution/page.md#L1>)

The production checklist recommends Portal connections through tenant Nginx or load balancers.
Tenant teams then control internal server and port changes behind that boundary.
It separately requests browser reachability, Portal-to-tenant connectivity, operating agreements, security testing, and tile release.
These are distinct checks; successful configuration upload alone does not establish business readiness.
[Production checklist, sections at lines 16, 22, 30, 40, and 71](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Production Release and Tenant on-boarding Checklist/page.md#L16>)

## Connections

Admin and onboarding ([[wb-candidate-operations-kt-admin-and-onboarding]]) explains the configuration and entitlement inputs.
Frontend composition ([[wb-candidate-architecture-kt-frontend-composition]]) explains how registered modules become Portal workspaces.
Application interoperability ([[wb-candidate-interoperability-kt-application-interoperability]]) separates desktop technical onboarding from business adoption.

Registry IDs `single-ui-importmap-admin`, `single-ui-active-importmap`, and `single-ui-category-tile-admin` identify related candidate interfaces.
Capability `single-ui-application-catalog` groups that declared context.
These connections establish navigation, without proving current routing, operational ownership, or passing execution.

## Evidence limits

Local hashes identify the supplied bytes.
Original page revisions, current authority, and human approval remain unconfirmed.
Several diagrams, emails, and example projects referenced by these guides are absent from this supplied copy.
No pipeline, deployment, upload, rollback, or production access check ran during ingestion.

## Open questions

| Issue and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Release duration differs between summary and table. See release proposal, lines 17–19 and 50–52. | Release occupancy and standby planning remain uncertain. | unknown | Confirm one duration with the release policy owner. |
| Urgent-release confirmation and silence rules coexist. See release proposal, lines 144–151. | A release could proceed without explicit stakeholder agreement. | unknown | Define required confirmations and the decision authority. |
| Checklist remains under construction; FMAA decommissioning is planned. See checklist, lines 1 and 16. | Promotion prerequisites and authentication continuity remain uncertain. | unknown | Confirm the governing checklist and replacement authentication plan. |
| Calendar separates technical and business dates without retained completion evidence. See calendar, lines 7–16. | Planned dates could be mistaken for delivered capability. | unknown | Link separate deployment, validation, and business activation records. |
| Tenant requests contain pending or struck-through readiness evidence. See CDUPS, lines 14–21, DDR, lines 9–13, and VPA, lines 12–22. | A target date cannot establish release readiness or acceptance. | unknown | Retain applicable configuration, connectivity, sign-off, and UVT evidence for each gate. |
| Deployment guides describe different historical and proposed mechanisms. See deployment and Nginx draft. | Teams could apply an unsuitable deployment procedure. | unknown | Identify the active pipeline and its environment-specific controls. |
