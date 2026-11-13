---
type: "Summary"
description: "Portal and tenant teams coordinate release planning, configuration promotion, and readiness."
doc_type: short
full_text: "sources/KT-release-operations.md"
---

> Derived from [KT-release-operations, version 3](../../../records/candidates/operations/KT-release-operations.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Portal release operations — Summary

## Overview
This topic links release planning with [[concepts/configuration-promotion]] and [[concepts/tenant-production-readiness]]. The supplied materials mix procedures, an unfinished checklist, historical deployment guidance, and a release proposal whose current authority is unconfirmed.

## Responsibilities
The release proposal assigns Portal routing, route enabling, tenant interfaces, and Portal-owned production changes to Portal teams. Tenant teams retain responsibility for their UI, backend, services, databases, and infrastructure. Portal teams run Portal releases and routing rollback; tenant teams validate applications, perform UVT, and support tenant issues.

## Readiness and scheduling
Requested inputs include solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning; new interfaces require 30 days of engagement under the proposal. The unfinished checklist adds SDK validation, shared frontend requests, entitlement checks, disaster recovery, performance inputs, operating agreements, and penetration testing. The unfinished checklist also calls for tenant review with RATAN before preparing each production release and assigns the tenant the upstream disaster-recovery check. The portal load balancer has no DR responsibility in that checklist. This guidance requires applicability review. [Canonical readiness section](../../../records/candidates/operations/KT-release-operations.md#readiness-before-scheduling).

## Configuration promotion
The documented flow starts with Module Map, Drawer Category, and Tile Configuration changes in Development. Teams export CSV files to a tenant-owned repository, then an ADO pipeline uploads configuration to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`. The flow says the service validates an FMAA JWT before processing CSV files. The first bulk insert into UAT and Production uses a separate BFF release; later uploads depend on tenant connectivity. The checklist also flags planned FMAA decommissioning, creating an unresolved dependency.

## Tenant capabilities in requests
Release requests describe intended business functions: FSS Cash Projection, FSS Funds Gating, FSS SSI, FSS Domestic Disbursement, FSS Gold Custody, FSS Digital Asset Collateral, DDR Reporting, CDUPS Confirmation, VPA Fix Link, and VPA Trade Monitor. These show why tenant tiles need Portal integration; they do not establish approved rules, completion, or present availability.

## Release window proposal
[[concepts/release-window-governance]] is proposed rather than confirmed. The proposal schedules first, third, and available fifth Saturdays at 09:00 SGT, freezes scope after Monday EOD in the first week, cancels windows without requests, and requires approved exceptions for late additions. Freeze periods need rescheduling or dispensation. Two ambiguities remain: the summary says 24 hours while the table says 10 hours ending at 19:00 SGT; the urgent-release section requires all confirmations but also permits proceeding when nobody raises concerns. Silence and explicit confirmation are different conditions.

## Technical and business activation
Tenant onboarding requires separate evidence for technical deployment and business activation. The release calendar separates Portal release dates from tenant release dates and lists separate Entra technical and business go-live entries. The OpenFin briefing separates technical onboarding from business user onboarding. The DDR request says business UAT sign-off follows technical go-live and lists separate dates. The VPA request separates Portal and application go-live dates, and the request template allows Portal deployment before application deployment. These records describe sequencing, not completed deployments or business acceptance.

## Readiness evidence gaps
The CDUPS request leaves UAT sign-off, user profiles, user counts, and UVT details unprovided. The DDR request records pending connectivity and separates technical sign-off from business validation. Several VPA evidence references are struck through. Missing or withdrawn references cannot establish the corresponding release gate. The blank request template asks for DNS resolution, user totals, routing changes, connectivity evidence, sign-off, and UVT contacts, but does not show any specific request satisfying them.

## Deployment evolution
Deployment strategy is unresolved in the supplied materials. The older frontend deployment guide describes static artifacts, a proposed blue-green model, shared Pilot and Production backend, feature checks, artifact publication, and manual production deployment after approval. The Nginx draft proposes versioned configuration, syntax checks, restart checks, and rollback. Neither document establishes the currently deployed pipeline. The production checklist recommends Portal connections through tenant Nginx or load balancers, with tenant teams controlling internal server and port changes behind that boundary. It separately requests browser reachability, including viewing the sign-in page before authentication, plus Portal-to-tenant connectivity, operating agreements, security testing, and tile release. [Canonical deployment section](../../../records/candidates/operations/KT-release-operations.md#deployment-evolution).

## Connections
- [[summaries/KT-admin-and-onboarding]] covers configuration and entitlement inputs.
- [[summaries/KT-frontend-composition]] explains how registered modules become Portal workspaces.
- [[summaries/KT-application-interoperability]] separates desktop technical onboarding from business adoption.
- Related registry IDs: `single-ui-importmap-admin`, `single-ui-active-importmap`, and `single-ui-category-tile-admin`; capability `single-ui-application-catalog`.

## Evidence limits and open questions
Local hashes identify supplied bytes; original page revisions, current authority, and human approval remain unconfirmed. Diagrams, emails, and example projects referenced by the guides are absent. No pipeline, deployment, upload, rollback, or production access check ran during ingestion. Open questions include: 10 vs 24 hour releases; urgent-release confirmation vs silence; which checklist and deployment process govern each environment; how to prove technical readiness and business activation separately; and which tenant request evidence establishes accepted scope and completed readiness.

## Related Concepts
- [[concepts/application-ownership]]
- [[concepts/frontend-onboarding]]
- [[concepts/identity-provider-delegation]]
- [[concepts/admin-catalog-configuration]]
- [[concepts/portal-ingress-path]]
- [[concepts/interoperability-contract-governance]]
- [[concepts/entitlement-retrieval]]
- [[concepts/ems2-entitlement-provisioning]]
- [[concepts/maker-checker-verification-workflow]]
- [[concepts/mfe-cache-strategy]]
- [[concepts/microfrontend-layering]]
- [[concepts/portal-tile-workspace-model]]
- [[concepts/shared-dependency-governance]]

## Entities
- [[entities/markets-operations-one-release]]
- [[entities/admin-module]]
- [[entities/entra]]
- [[entities/fmaa]]
- [[entities/fss]]
- [[entities/cdups]]
- [[entities/vpa]]
- [[entities/ddr]]
- [[entities/fmo-post-trade-portal]]
- [[entities/nginx]]
- [[entities/portal-team]]
- [[entities/single-ui-bff]]
- [[entities/openfin]]
- [[entities/single-ui-sdk]]
- [[entities/ems2]]
- [[entities/ems3]]
- [[entities/api-gateway]]
- [[entities/mfe-base]]
- [[entities/single-spa]]
