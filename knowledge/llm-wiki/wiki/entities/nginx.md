---
sources: ["summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "Web server and reverse proxy at the portal ingress edge and tenant connectivity boundary."
---

# Nginx

Nginx is the web server and reverse proxy that acts as the portal's first ingress endpoint in the reported architecture. It receives requests for the common public domain after DNS forwarding and passes them on toward the [[entities/api-gateway]]. The portal materials also treat it as the boundary through which tenant UI and API routing pass, as a configuration dependency for each application that onboards, and as the tenant-side connection point recommended for production release readiness.

## Reported role

- **First ingress endpoint.** The user clarification places Nginx at the outer edge of the request path, ahead of the API Gateway, which is the second ingress endpoint and forwards to application services.
- **Integration boundary.** [[summaries/KT-portal-purpose]] lists tenant UI and API routing as a shared platform capability and names the portal's Nginx boundary as the place where that routing occurs. The portal therefore presents one outer entry for tenant applications rather than exposing each application's routing separately.
- **Ownership.** The user reports that Nginx rules belong to the RATAN Ansible load-balancer scope rather than to any single application repository.
- **Logical vs. transport contract.** The frontend-to-backend contract ([[entities/mfe-base]] calling the [[entities/single-ui-bff]]) is logically distinct from this transport path; the ingress chain does not change the API contract.

## Configuration intake

[[summaries/KT-admin-and-onboarding]] records a draft intake for proxy configuration. It collects an upstream name, host, port, route path, rewrite rule, protocol, and request limits. It also collects environment, WebSocket settings, timeout values, load-balancing method, and custom headers. These fields describe the routing information that tenant onboarding requires; they do not establish current endpoint values, active configuration, or a working deployment pipeline.

Onboarding makes Nginx a per-application dependency. The development principle assigns each application's backend availability to its application team, and application teams provide static-file and API URLs for Nginx configuration. The backend procedure also requests application URLs for proxy configuration and CORS handling. See [[concepts/frontend-onboarding]].

The draft separates non-production maintenance from UAT and stage configuration work. Its manual-deployment discussion identifies configuration testing and rollback as improvement proposals. Those proposals need an applicable operating procedure before use.

A retained firewall register supplies operational connectivity context for onboarding. Its addresses and contact details remain in the original material, and current network approvals and reachability were not verified.

## Tenant boundary and production readiness

The production release and tenant on-boarding checklist recommends that Portal connections reach tenant applications through tenant Nginx or load balancers. Tenant teams then control internal server and port changes behind that boundary, so the proxy configuration is a handover point between Portal routing and tenant infrastructure ownership.

The same checklist keeps several checks distinct: browser reachability, Portal-to-tenant connectivity, operating agreements, security testing, and tile release. A successful Portal-side configuration upload therefore does not establish that Nginx routing works or that the tenant capability is business-ready. [[concepts/tenant-production-readiness]] covers that separation of technical and business activation evidence, and [[concepts/portal-ingress-path]] covers the ingress chain itself.

These statements describe recommended connectivity practice. The supplied material contains no executed connectivity test, approved network permission, or confirmed production proxy configuration.

## Deployment proposals

A draft automated deployment solution proposes managing Nginx configuration as versioned files, with syntax checks, restart checks, and rollback. It is filed as a draft, so it records a proposal rather than a running procedure.

The older frontend deployment guide describes a different mechanism — static artifacts, a proposed blue-green model, and manual production deployment after approval — and does not describe how Nginx configuration is promoted.

Neither document establishes the currently deployed pipeline. The active configuration-promotion path, its environment-specific controls, and its rollback ownership remain unidentified. See [[concepts/configuration-promotion]] and [[summaries/KT-release-operations]].

## Source qualification

Local Nginx templates exist in the reviewed copy — the template `repos/infra/nginx/ratan_servers.conf.j2` (lines 150–256) includes both API Gateway routes and **direct proxy exceptions**. This means the supplied copy cannot establish that every request traverses the API Gateway.

The wider Ansible repository and any rendered deployment were unavailable. Consequently, DNS records, effective upstreams, gateway routes, and the active deployment all remain unverified, and the reported topology cannot establish live forwarding behavior. The draft intake fields and the firewall register have no inspected deployment or connectivity execution, so they cannot establish the current schema of active routes or network permissions.

[[summaries/KT-portal-purpose]] describes the routing boundary in present tense but does not provide configuration or test evidence for it. That statement establishes intended scope, not verified routing coverage.

## Open questions

- Which routes bypass the gateway through direct proxy exceptions?
- What do the rendered (as opposed to templated) server blocks contain in the target environment?
- Which draft intake fields are mandatory in the current operating procedure, and how are inbound values validated?
- Which deployment process governs Nginx configuration in each environment — the versioned draft solution, the manual guide, or neither?
- What approved procedure covers configuration testing and rollback for manual changes?
- Who owns deployment confirmation — currently recorded as `unknown` in the source record?

## Connections

[[concepts/portal-ingress-path]] describes the ingress chain Nginx anchors. [[concepts/portal-entry-and-tile-authorization]] covers authorization decisions made after ingress. See [[summaries/ARC-portal-service-relationships]] for the full candidate architecture record, including its evidence limits table.

See also: [[summaries/KT-frontend-composition]], [[summaries/KT-portal-purpose]], [[summaries/KT-admin-and-onboarding]], [[summaries/KT-release-operations]]

See also: [[summaries/KT-observability-and-performance]]