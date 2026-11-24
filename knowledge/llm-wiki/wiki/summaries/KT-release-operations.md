---
type: "Summary"
description: "Portal and tenant teams coordinate release planning, configuration promotion, and readiness."
doc_type: short
full_text: "sources/KT-release-operations.md"
---

> Derived from [KT-release-operations, version 5](../../../records/candidates/operations/KT-release-operations.md), candidate/draft. [Source bindings](../../source-manifest.json).

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

## Additional source-scoped release conditions

The unfinished checklist makes base-provided Axios and backend SDK validation mandatory in its documented release workflow. Its FMAA upload path requires matching FMAA account and EMS2 IDs plus an active token. The replacement authentication dependency remains unresolved. [Checklist authentication](../../../records/candidates/operations/KT-release-operations.md#checklist-authentication-conditions).

The checklist requests first-onboarding module, new-category drawer, and per-tile metadata records. It requires at least two maker/checker test accounts, uses deactivation for deletion requests, and checks entitled versus unentitled visibility. Its RATAN_CASHFLOW_BLOTTER action requirement remains a specific example. The historical account path distinguishes non-production Hashicorp from production OUD, with scheduled production vault onboarding. Dark and light themes remain documented checklist scope. [Operational predicates](../../../records/candidates/operations/KT-release-operations.md#unfinished-checklist-operational-predicates).

Each tenant owns configuration, repositories, production/UAT change requests, ADO work items, and pipelines under the promotion guide. The historical flow requires environment-specific FMAA/OUD service accounts and uses client-credential JWTs. These instructions supply no credential-access or deployment authorization. [Promotion ownership](../../../records/candidates/operations/KT-release-operations.md#configuration-promotion-ownership-and-authentication).

Cash Projection requests 10 total, 10 new, and 5 concurrent users. FSS requests total/new/concurrent counts of 10/10/5 for Funds Gating and Gold Custody. Domestic Disbursement requests 25/10/10; SSI requests 11/11/5. Collateral uses existing users with no numeric count. Domestic messages follow EBBS credit and go to SeCCuRe. Gold Custody names India and daily CSS positions. These are request-specific scope and planning values. [Cash Projection request](../../../records/candidates/operations/KT-release-operations.md#cash-projection-request-scope). [FSS profiles and counts](../../../records/candidates/operations/KT-release-operations.md#fss-request-scope-and-profiles). [Requested jurisdictions](../../../records/candidates/operations/KT-release-operations.md#tenant-capabilities-described-in-requests).

DDR requests 700 total, 200 new, and 20 concurrent users under the FSS Services container. Its listed country codes define the requested entity scope. Entities use FSS_UI_RF_ plus country code. MASTER, MAKER, CHECKER, PSS_USER, and BUSINESS_USER share the corresponding country prefix. These are requested profiles without current grant, usage, or deployment evidence. [DDR requested scope](../../../records/candidates/operations/KT-release-operations.md#ddr-request-scope-and-profiles).

The older deployment guide targets desktop/mobile browsers, mobile WebViews, and OpenFin with latest-version frontend deployment. It calls Production blue and Pilot green, sharing a backend. These are historical delivery assumptions. [Artifact delivery assumptions](../../../records/candidates/operations/KT-release-operations.md#historical-frontend-artifact-delivery-assumptions).
