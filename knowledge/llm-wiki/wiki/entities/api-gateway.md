---
sources: ["summaries/KT-release-operations.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "Ingress product said to forward portal requests from Nginx to application services."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# API Gateway

## What it is

The API Gateway is the second ingress endpoint in the reported portal topology. Per the user clarification recorded in [[summaries/ARC-portal-service-relationships]], it receives traffic that has already reached [[entities/nginx]] and forwards requests on to the application services behind the portal.

Its role is therefore described only at the boundary level: a forwarding hop between the edge and the backend, on the [[concepts/portal-ingress-path]] from a common public domain, through DNS, to Nginx, then to the gateway.

## Key facts from this document

- **Second ingress endpoint.** Nginx is named as the first ingress endpoint; the API Gateway is the second, and forwards requests to application services.
- **Relationship to the BFF is logical, not transport-level.** The recorded MFE-to-[[entities/single-ui-bff]] contract is described as a logical one and is kept distinct from the reported transport path through the gateway.
- **Implementation is unavailable.** No gateway repository was available to the reviewers, so a gateway implementation analysis was explicitly excluded from the review.
- **Listed as an unverified boundary.** The record keeps the gateway visible as an unavailable boundary rather than an inspected component. Effective upstreams, gateway routes, and the active deployment remain unverified.
- **Possible bypasses.** The inspected Nginx template contains gateway routes but also direct proxy exceptions, so the supplied copy cannot establish that all portal traffic traverses the gateway.
- **No deployment identifier.** The user clarification carries no deployment identifier, so reported forwarding cannot be confirmed as the active configuration.

## Open qualifications

| Evidence gap | Consequence |
| --- | --- |
| No gateway repository available | Implementation cannot be analysed; the boundary is recorded but not inspected. |
| Nginx templates include direct proxy routes | Universal gateway traversal cannot be established. |
| No deployment identifier in the clarification | Active DNS and gateway forwarding remain unconfirmed. |

The suggested next action in the record is to obtain the effective configuration if deployment confirmation becomes necessary, and to compare rendered Nginx routes with the reported environment.

## Related pages

- [[concepts/portal-ingress-path]] — the reported DNS → Nginx → gateway → services path.
- [[entities/nginx]] — first ingress endpoint; its Ansible-scoped rules sit upstream of the gateway.
- [[entities/single-ui-bff]] — the sole backend for the described portal scope, reached logically behind ingress.
- [[entities/ratan-auth-server]] — internal service authentication and external API caller authorization.
- [[entities/fmo-post-trade-portal]] — the portal whose scope the described topology covers.
- [[summaries/ARC-portal-service-relationships]] — source record for all statements above.

See also: [[summaries/KT-frontend-composition]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-release-operations]]