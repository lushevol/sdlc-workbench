---
sources: ["summaries/KT-release-operations.md"]
type: "Event"
description: "Release program governing Portal and tenant release windows, scope, and readiness gating."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Markets Operations One Release

## What it is

Markets Operations One Release is a recurring Portal release programme coordinated by [[entities/portal-team]] for the [[entities/fmo-post-trade-portal]]. Tenant teams submit change requests for new or changed tiles, and the Portal team schedules, routes, and executes the Portal-side release work. The supplied materials describe the programme through a release proposal, a release calendar, per-tenant change requests, a request template, and supporting checklists; their current authority is unconfirmed.

Source summary: [[summaries/KT-release-operations]]

## Documented release window rules (proposed)

The release proposal schedules releases on the first, third, and available fifth Saturdays, starting at 09:00 SGT. Scope freezes after Monday EOD in the first week of the window. Windows without requests are cancelled, and late additions need approved exceptions. Freeze periods require rescheduling or dispensation. These rules are proposed, not confirmed. See [[concepts/release-window-governance]].

### Unresolved duration and confirmation rules

- The summary states 24 hours; the detailed table states 10 hours ending at 19:00 SGT.
- The urgent-release section requires all confirmations but also permits proceeding when nobody raises concerns. Silence and explicit confirmation are different conditions.

## Ownership split

Under the proposal, the release covers Portal routing, route enabling, tenant interfaces, and Portal-owned production changes. Tenant teams retain responsibility for their UI, backend, services, databases, and infrastructure. Portal teams execute Portal releases and routing rollback; tenant teams validate applications, perform UVT, and support tenant issues. Routing and entry behaviour connect to [[concepts/portal-ingress-path]].

## Readiness inputs

The proposal requests solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning. New interfaces require 30 days of engagement under the proposal. An unfinished checklist adds SDK validation, shared frontend requests, entitlement checks, disaster recovery, performance inputs, operating agreements, and penetration testing. See [[concepts/tenant-production-readiness]] and [[concepts/frontend-onboarding]].

## Configuration promotion dependency

Release execution depends on the Admin Module promotion flow. Teams change Module Map, Drawer Category, and Tile Configuration in Development, export CSV files to a tenant-owned repository, and an ADO pipeline uploads to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`. The documented flow states that an [[entities/fmaa]] JWT is validated before processing. The first bulk insert into UAT and Production uses a separate BFF release; later uploads depend on tenant connectivity to the Admin service. The checklist flags planned FMAA decommissioning, an unresolved dependency. See [[entities/admin-module]] and [[concepts/configuration-promotion]].

## Change requests in the calendar

The release calendar lists tenant change requests. The following describe intended business functions; they do not establish approved rules, completion, or present availability.

| Request | Documented purpose |
| --- | --- |
| [[entities/fss]] Cash Projection | Cash-projection rule-engine tile |
| [[entities/fss]] Funds Gating | Limit investor redemptions to a percentage of daily NAV |
| [[entities/fss]] SSI | Generate settlement instructions from stored agent accounts |
| [[entities/fss]] Domestic Disbursement | Reconcile depository files and create MT566 messages |
| [[entities/fss]] Gold Custody | Capture purchases and sales, settle services, daily position updates |
| [[entities/fss]] Digital Asset Collateral | Collateral use of custodied digital assets |
| [[entities/ddr]] Reporting | Show reports received upstream and forwarded downstream |
| [[entities/cdups]] Confirmation | Outbound and inbound confirmation blotters |
| [[entities/vpa]] Fix Link and Trade Monitor | Correct broken links; monitor trade status and retrieve files |

## Technical versus business activation

The release calendar separates Portal release dates from tenant release dates, and lists separate [[entities/entra]] technical and business go-live entries. The [[entities/openfin]] briefing likewise separates technical onboarding from business user onboarding. The DDR request places business UAT sign-off after technical go-live and lists separate target dates. The VPA request separates Portal and application go-live dates, and the request template allows Portal deployment before application deployment. These records describe sequencing; they do not prove completed deployments or business acceptance.

## Readiness evidence gaps

- CDUPS request: UAT sign-off, user profiles, user counts, and UVT details unprovided.
- DDR request: connectivity pending; technical sign-off separated from business validation.
- VPA request: several evidence references struck through.
- Blank request template asks for DNS resolution, user totals, routing changes, connectivity evidence, sign-off, and UVT contacts.

Missing or withdrawn references cannot establish a release gate.

## Related environment guidance

Deployment guidance is unresolved. An older frontend deployment guide describes static artifacts, a proposed blue-green model, a shared Pilot and Production backend, feature checks, artifact publication, and manual production deployment after approval. An Nginx draft proposes versioned configuration, syntax checks, restart checks, and rollback. The production checklist recommends Portal connections through tenant [[entities/nginx]] or load balancers, with tenant teams controlling internal server and port changes behind that boundary.

## Open questions

| Issue | Consequence | Next action |
| --- | --- | --- |
| 10 vs 24 hour release duration | Occupancy and standby planning uncertain | Confirm one duration with the policy owner |
| Urgent-release confirmation vs silence | Release could proceed without explicit agreement | Define required confirmations and decision authority |
| Unfinished checklist and planned FMAA decommissioning | Promotion prerequisites and authentication continuity uncertain | Confirm governing checklist and replacement authentication plan |
| Technical and business dates lack completion evidence | Planned dates mistaken for delivered capability | Link deployment, validation, and activation records |
| Pending or struck-through request evidence | Target dates cannot establish readiness | Retain configuration, connectivity, sign-off, and UVT evidence per gate |
| Conflicting deployment guides | Teams could apply unsuitable procedure | Identify the active pipeline and environment controls |
