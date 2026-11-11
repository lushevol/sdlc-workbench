---
query: "Which responsibilities belong to Portal and tenant teams for routing, release, validation, and rollback?"
---

## Portal vs. tenant responsibilities (routing, release, validation, rollback)

The split comes from a **draft, unapproved release proposal**, so these are intended responsibility statements rather than confirmed authority (see [[summaries/KT-release-operations]], [[entities/portal-team]], [[concepts/application-ownership]]).

### Portal team
- **Routing / release scope:** owns Portal routing, route enabling, tenant interface changes, and Portal-owned production changes. Portal teams execute Portal releases.
- **Rollback:** Portal teams perform **routing rollback**.
- **Routing intake:** receives static-file and API URLs from application teams during onboarding, which then become the [[entities/nginx]] proxy configuration.
- **Readiness intake (requested, not proven):** solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning; new interfaces require 30 days of engagement under the proposal.
- **Ingress boundary:** Portal-side routing ownership is shared with the tenant, per the production checklist recommendation that Portal traffic reach tenants through tenant-controlled Nginx/load balancers.

### Tenant teams
- **Ownership retained:** their UI, backend, services, databases, and infrastructure.
- **Validation:** tenant teams **validate their applications**, perform **UVT**, and support tenant-raised issues after release. UAT sign-off and UVT contacts are request-template fields.
- **Rollback accountability:** tenant teams retain security, licensing, vulnerability, support, resilience, and **rollback** accountability for dependency exceptions.
- **Tenant boundary:** they control internal server and port changes behind their Nginx/load-balancer boundary, and must supply browser reachability, Portal-to-tenant connectivity, operating agreements, and penetration-testing evidence.
- **Release dates:** the calendar separates Portal release dates from tenant release dates; the request template explicitly allows Portal deployment before application deployment.

### Shared / unresolved
- **Configuration promotion** is joint: tenant teams edit Module Map / Drawer Category / Tile Configuration in Development, export CSVs to a tenant-owned repo; the first bulk insert into UAT and Production runs as a **separate BFF release**; later uploads depend on tenant connectivity ([[concepts/configuration-promotion]]).
- **Unresolved owners:** release-window exceptions and urgent-release confirmations; who owns Nginx configuration testing and rollback (the Nginx draft proposes versioned config, syntax checks, restart checks, and rollback, but names no approver); who records technical go-live separately from business activation. See [[concepts/tenant-production-readiness]] and [[concepts/portal-ingress-path]].

**Evidence limits:** no pipeline, deployment, upload, rollback, or production access check was executed during ingestion, and the release proposal plus admin release checklist are unapproved/under construction.
