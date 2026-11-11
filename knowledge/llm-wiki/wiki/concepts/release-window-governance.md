---
type: "Concept"
sources: ["summaries/KT-release-operations.md"]
description: "Candidate release-window scheduling and ownership proposal, with unresolved duration and urgent-release confirmation rules."
---

# Release Window Governance

Release window governance describes how the supplied release proposal schedules Portal changes, freezes their scope, and coordinates Portal and tenant responsibilities. The governing source is [[summaries/KT-release-operations]], a version 2 candidate/draft topic. Its historical and proposed procedures have unconfirmed current authority; this page does not establish an approved operating policy.

## Proposed scheduling rules

| Area | Statement in the proposal |
| --- | --- |
| Regular windows | First, third, and available fifth Saturdays, starting at 09:00 SGT. |
| Scope cutoff | Monday EOD in the first week of the release window. |
| Empty windows | Cancel a window when it has no requests. |
| Late scope | Require an approved exception for additions after the cutoff. |
| Freeze periods | Reschedule or obtain dispensation under the proposal. |
| New interfaces | Begin engagement 30 days before release under the proposal. |

These statements describe proposed controls. A calendar entry or requested date does not prove that a release was approved, executed, or accepted.

## Unresolved rules

The source preserves two conflicts that this concept does not resolve:

| Decision | Conflicting source statements | Remaining action |
| --- | --- | --- |
| Window duration | The proposal summary specifies 24 hours; its detailed table specifies 10 hours with a 19:00 SGT finish. | The responsible owner must confirm the applicable duration before it is treated as a target rule. |
| Urgent-release confirmation | The urgent-release section requires all confirmations and also permits proceeding when nobody raises concerns. | Confirm whether explicit stakeholder confirmation is required; silence and confirmation remain different conditions. |

Owner and current approval authority are unknown. Neither alternative becomes approved through its appearance in this wiki.

## Responsibilities and readiness

The proposal assigns Portal routing, route enabling, tenant interfaces, Portal-owned production changes, and routing rollback to Portal teams. Tenant teams retain responsibility for their UI, backend, services, databases, infrastructure, application validation, UVT, and tenant issues. These remain documented responsibility statements with unconfirmed present approval; see [[concepts/application-ownership]].

Requested readiness inputs include solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning. The unfinished checklist adds SDK validation, shared frontend requests, entitlements, disaster recovery, performance, operating agreements, and penetration testing. Their presence in a checklist does not establish completion for a specific request. [[concepts/frontend-onboarding]] and [[concepts/tenant-production-readiness]] explain those evidence boundaries.

## Relationship to configuration and activation

[[concepts/configuration-promotion]] concerns the documented CSV and Admin-service workflow for promoting tenant configuration. Successful upload does not establish routing, connectivity, release sign-off, UVT, or business readiness.

Portal deployment, tenant deployment, technical go-live, and business activation have separate planning and evidence boundaries. Release-calendar entries and tenant requests can describe their sequence without proving completed deployment or business acceptance. See [[concepts/tenant-production-readiness]] and [[entities/markets-operations-one-release]].

## Evidence limits and open questions

The source topic binds supplied document bytes but does not confirm original page revisions, present authority, or human approval. No pipeline, deployment, configuration upload, rollback, or production access check was executed during compilation.

- Which duration applies: 10 hours or 24 hours?
- Does an urgent release require explicit confirmation from every stakeholder?
- Which checklist and deployment process currently govern each environment?
- Which retained evidence establishes technical readiness and business activation separately?
- Which tenant request establishes accepted capability scope and completed readiness?

These questions remain in the canonical candidate topic. Compiled pages and linked records cannot supply the missing approval or execution evidence.
