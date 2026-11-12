---
type: "Concept"
sources: ["summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
description: "The reported DNS-to-Nginx-to-API-gateway-to-BFF route serving the post-trade portal."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Portal Ingress Path

The **portal ingress path** is the reported route that an external request follows to reach the portal backends: a common public domain resolves through DNS to [[entities/nginx]], which forwards to [[entities/api-gateway]], which forwards to application services such as [[entities/single-ui-bff]]. This concept captures the *transport* path, which is logically separate from the *contract* between the frontend microfrontends and the BFF.

The [[summaries/KT-portal-purpose]] topic describes a common application entry and names the portal's Nginx boundary as the integration point for tenant UI and API routing. Those statements are capability-level and are consistent with the topology below, but they add no route table, deployment identifier, or DNS record.

## Reported topology

| Stage | Component | Reported role |
| --- | --- | --- |
| 1 | Public domain + DNS | Single common domain for the portal scope |
| 2 | [[entities/nginx]] | First ingress endpoint; rules belong to the RATAN Ansible load-balancer scope |
| 3 | [[entities/api-gateway]] | Second ingress endpoint; forwards requests to application services |
| 4 | [[entities/single-ui-bff]] | Sole backend for the described portal scope |

This ordering comes from the user-supplied architecture clarification recorded in [[summaries/ARC-portal-service-relationships]]. The clarification is candidate knowledge: it names responsibilities but no effective deployment, environment identifier, or DNS record. The portal-purpose materials corroborate the Nginx boundary at a capability level only.

## Key qualifications

- **Unverified runtime.** DNS resolution, effective upstreams, gateway routes, and the active deployment were not exercised. No live requests or browser behavior were tested.
- **Gateway implementation excluded.** No API Gateway repository was available, so its implementation remains an unopened boundary.
- **Direct proxy exceptions.** The local Nginx template (`ratan_servers.conf.j2`) contains gateway routes *and* direct proxy routes. The supplied copy therefore cannot establish that all traffic traverses the gateway; per-route exceptions may bypass it.
- **Logical contract vs. transport.** The MFE-to-BFF interface contract (HTTP headers, token validation) is a separate concern from the physical path above. See [[concepts/single-ui-sdk-authentication]] for how requests carry the `Single-UI-Authorization` header and how the SDK filter validates them.
- **Single backend is scoped.** The "sole backend" claim applies only to the described portal scope; it does not prove RATAN has one backend across every application.
- **Capability-level corroboration only.** The portal-purpose topic names common entry and an Nginx integration boundary, but it supplies no route-level evidence and its own source authority, page revisions, and approval states remain unconfirmed.

## Relationship to composition

The ingress path sits beneath the four-layer frontend stack described in [[concepts/microfrontend-layering]]. Static entry resources and JavaScript bundles are served through this path, while [[entities/single-spa]] lifecycle and SystemJS module loading happen entirely in the browser after delivery. Container and tile routing (React Router paths, container/module/tile props) is likewise client-side. These are separate logical stages from ingress forwarding; the effects of effective route and rewrite configuration remain unverified. The portal-purpose materials describe the shared entry and composition capabilities at the same capability level; they do not change the client-side execution model.

## Open questions

| Gap | Consequence |
| --- | --- |
| No deployment identifier | Cannot confirm active DNS or gateway forwarding |
| Nginx template mixes gateway and direct routes | Cannot confirm universal gateway traversal |
| No gateway repository | Cannot analyze gateway behavior |
| No authenticated architecture owner | No authoritative confirmation path |

Resolving these requires the rendered deployment configuration and the original repository revisions, neither of which was available when [[summaries/ARC-portal-service-relationships]] was recorded. The [[summaries/KT-portal-purpose]] topic adds the same limit: its source ownership, applicability, and original revisions are unconfirmed.

## Related

- [[concepts/microfrontend-layering]] — the client-side composition served over this path
- [[concepts/identity-provider-delegation]] — authentication that occurs after ingress
- [[entities/fmo-post-trade-portal]] — the portal served by this path
- [[entities/nginx]], [[entities/api-gateway]], [[entities/single-ui-bff]] — the stages above

See also: [[summaries/KT-frontend-composition]], [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-observability-and-performance]]

See also: [[summaries/KT-admin-and-onboarding]]

See also: [[summaries/KT-release-operations]]