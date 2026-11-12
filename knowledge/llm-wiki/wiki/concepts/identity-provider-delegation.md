---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/KT-release-operations.md", "summaries/KT-application-interoperability.md", "summaries/KT-portal-purpose.md", "summaries/ARC-portal-service-relationships.md"]
description: "How the portal defers authentication to external identity providers and authorization to EMS2/EMS3, and what remains unproven."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Identity Provider Delegation

Identity provider delegation uses external providers for identity checks and entitlement retrieval. The portal's own services — chiefly the [[entities/ratan-auth-server]] and the [[entities/single-ui-bff]] — accept credentials or tokens, call out to a provider, and translate the answer into portal-local sessions, attributes, and entitlements. Portal and application components still enforce their relevant entry, tile-admission, and protected-operation rules. The reported delegation does not establish a universal Auth Server call path.

This page records the user-reported delegation model from [[summaries/ARC-portal-service-relationships]], separates it from what the inspected source copies actually contain, and adds the operational evidence recorded in [[summaries/KT-release-operations]] and the design-level evidence in [[summaries/KT-authentication-and-sessions]].

## Two distinct delegation duties

Delegation splits along a clean line, and conflating the two is the main source of confusion in the clarification:

| Duty | Reported delegate(s) | Purpose |
| --- | --- | --- |
| Authentication | OUD, Entra SPN, FMAA | Establish who the caller is — internal service authentication and external API caller identity. |
| Authorization | [[entities/ems2]], [[entities/ems3]] | Decide what the authenticated caller may do — entitlement resolution. |

The [[entities/ratan-auth-server]] is reported as the component that performs internal service authentication and external API caller authorization. Entitlement retrieval is therefore a downstream, separate concern; see [[concepts/entitlement-retrieval]].

## What the inspected sources support

- Local OUD, FMAA, and EMS2 paths are supported by the source review accompanying the clarification.
- The Auth Server copy in hand contains **no identified Entra SPN or EMS3 implementation**.
- Those two providers do appear elsewhere in inspected code, but under the [[entities/single-ui-bff]] rather than the Auth Server: an Entra token exchange service and an EMS3 entitlement filter/service.
- Source paths in the BFF remain relevant evidence. The clarification does **not** license redrawing them as an inferred Auth Server hop.

The Entra design material in [[summaries/KT-authentication-and-sessions]] is consistent with that BFF placement. It describes a browser redirect followed by an authorization-code exchange performed by the BFF, after which the BFF builds user information, retrieves EMS2 entitlements, and issues authentication and entitlement tokens. That is a documented *design proposal*, not evidence that the code inspected implements it, but it does mean the BFF-side exchange is not an accident of the code snapshot — it is where the design intends trust translation to happen.

## Entra migration as a delegation change

The Entra work is best read as swapping one authentication delegate while deliberately leaving other delegation duties alone. The phase 1 scope is UI SSO only. It explicitly excludes EMS2 replacement, portal session management, and tenant-onboarding authentication, and it defers machine-to-machine authentication to a separate migration document with unresolved central dependencies.

Three consequences follow for this concept:

1. **The entitlement delegate is out of scope.** EMS2 stays the authorization delegate during phase 1, so authentication migration must not be read as an entitlement redesign. See [[concepts/ems2-entitlement-provisioning]] and [[concepts/entitlement-retrieval]].
2. **The portal keeps owning its own session.** Provider authentication establishes identity; the portal session lifecycle — access token, idle timeout, absolute timeout, refresh token — remains a portal concern. See "Provider session versus portal session" below.
3. **Entra is the current SSO target.** The November clarification prohibits OneMFA fallback. The pilot design retained fallback and described a separate username/password path. [Canonical SSO criterion](../sources/KT-authentication-and-sessions.md#portal-sso-ac-001)

The former pilot materials used different activation flag values and gave inconsistent persistence instructions. Those details describe the former pilot.

## Provider session versus portal session

The production pilot describes Windows Hello or Authenticator and a one-hour Entra session. The portal has separate ceilings of 15 minutes idle and 60 minutes absolute from portal authentication. The absolute ceiling applies during eligible activity and renewal. The ideal portal logout revokes all portal sessions immediately and leaves identity-provider sessions intact. [Canonical renewal criteria](../sources/REQ-active-session-renewal.md#acceptance-criteria) · [Canonical logout criterion](../sources/KT-authentication-and-sessions.md#portal-logout-ac-001)

## Profile attributes cross the delegation boundary

The production guide warns that AD profile values differ from OUD values: surname formatting, country codes, and missing locale values. Downstream audit or application logic that consumes those attributes can therefore change behavior when the authentication delegate changes, even though nothing in the authorization delegate moved. Attribute shape is part of the delegation contract, not an implementation detail — see [[concepts/identity-profile-attribute-migration]].

## FMAA in a documented operational path

The release-operations material adds one concrete, procedure-level anchor for the FMAA delegate. The Admin Module configuration promotion flow states that the Portal Admin upload interface `/api/auth/v1/fmo/admin/config/upload` validates an **FMAA JWT** before it processes the tenant CSV configuration files. The recurring tenant-pipeline CSV upload path therefore depends on FMAA validation. The first bulk insert into UAT and Production uses a separate BFF release under the guide. [Canonical promotion procedure](../sources/KT-release-operations.md#configuration-promotion)

The authentication topic adds the historical shape of that delegate. The FMAA reference describes client-credential authentication for machine-to-machine callers, separates service-account onboarding from bank-ID onboarding, and describes OUD-managed accounts authenticated through FMAA, with 17-year validity for service accounts and seven-day validity for bank IDs. Those values are historical examples and do not establish current token policy; see [[concepts/machine-to-machine-authentication]].

That same release material also records a **planned FMAA decommissioning** in the Admin Module release checklist. The checklist remains under construction, so the decommissioning statement is a warning rather than a plan with a replacement. For delegation this creates an unresolved dependency: the documented configuration promotion procedure and the documented authentication delegate cannot both persist unchanged. See [[concepts/configuration-promotion]] and [[concepts/tenant-production-readiness]].

The evidence remains procedural and documentary. No upload, token validation, or FMAA call ran during ingestion, and the checklist cites no replacement provider.

## Reported scope versus proven behavior

Five qualifications bound this concept:

1. **Reported, not deployed.** The clarification carries no deployment identifier, so it cannot establish active DNS, gateway forwarding, or which provider a given environment actually reaches. The transport side of this question belongs to [[concepts/portal-ingress-path]].
2. **Not every request.** The reported Auth Server scope does not prove that every portal request invokes that service. Some paths may delegate directly from the BFF.
3. **Provider list is partial locally.** The absence of Entra SPN and EMS3 in the Auth copy is an evidence limit, not a claim that the reported delegation is wrong.
4. **Procedures and designs are not proof.** A documented FMAA validation step in a promotion guide, or a documented authorization-code exchange in an Entra design, shows intended dependency and intended flow — not that a given environment enforces it, nor that FMAA will survive decommissioning.
5. **Candidate review remains pending.** The RATAN team owns and reviews portal policy under ICS bank security policy. The applicable ICS revision and deployment configuration still require evidence.

## Position in the request chain

Delegation sits behind request admission, not in front of it. The reported path runs from a common public domain through [[entities/nginx]] and the [[entities/api-gateway]] to the portal backend; only then does delegated authentication occur. Because gateway implementation is unavailable and the Nginx templates contain direct proxy exceptions alongside gateway routes, universal gateway traversal cannot be established. See [[concepts/portal-ingress-path]] and [[concepts/portal-entry-and-tile-authorization]].

Once identity is established, the token contract carries it onward: the shared frontend interceptor sends `Single-UI-Authorization`, and the [[entities/single-ui-sdk]] validates supported requests in application backends and supplies request attributes. That validation layer is adjacent to, but distinct from, provider delegation itself — see [[concepts/single-ui-sdk-authentication]].

## Design takeaways

- Treat authentication delegation and entitlement delegation as two contracts with different owners and different failure modes.
- Keep the provider hop explicit in designs; do not infer which portal component calls a provider from the provider's mere presence in the estate.
- Preserve the current Entra SSO rule when reviewing configuration. Use the former fallback paths only as historical design context.
- Separate provider session lifetime from portal session lifetime in every design and test statement.
- Treat identity-attribute shape as part of the delegation contract, and review downstream consumers before switching providers.
- Record provider lists as candidate knowledge until an effective deployment configuration is available.
- Treat any announced decommissioning of an authentication delegate as a cross-cutting dependency: it touches identity, configuration promotion, and tenant readiness at the same time.

## Open questions

- Which revision of the Auth Server implements Entra SPN and EMS3, if any?
- Do BFF-side Entra exchange and EMS3 calls eventually move behind the Auth Server, or are they the permanent design?
- Is OUD the sole internal identity store, or one of several for internal service authentication?
- What replaces FMAA JWT validation on the Admin config upload path after the planned decommissioning?
- Does the FMAA dependency in the promotion flow sit behind the Auth Server or inside the Portal Admin service itself?
- Which effective configuration enforces the current Entra SSO policy in the applicable environment?
- Which identity-provider profile contract must downstream services support after the AD/OUD attribute differences are resolved?
- Which historical FMAA validity settings remain intended requirements for machine-to-machine callers?

## Related pages

- [[summaries/ARC-portal-service-relationships]] — the clarification this page draws on
- [[summaries/KT-release-operations]] — the operational evidence for FMAA in configuration promotion
- [[summaries/KT-authentication-and-sessions]] — the Entra design, session boundary, and FMAA history
- [[concepts/entitlement-retrieval]] — the authorization half of delegation
- [[concepts/configuration-promotion]] — the workflow that depends on FMAA token validation
- [[concepts/tenant-production-readiness]] — how dependency changes affect tenant onboarding
- [[concepts/portal-ingress-path]] — how requests reach the delegating services
- [[concepts/single-ui-sdk-authentication]] — token validation downstream of delegation
- [[concepts/token-lifecycle-and-timeout-policy]] — portal timing ceilings and the unresolved exact timeout settings
- [[concepts/machine-to-machine-authentication]] — client-credential delegation for non-human callers
- [[concepts/identity-profile-attribute-migration]] — attribute differences introduced by the new provider
- [[concepts/ems2-entitlement-provisioning]] — the authorization delegate left out of phase 1
- [[entities/ratan-auth-server]], [[entities/single-ui-bff]], [[entities/ems2]], [[entities/ems3]], [[entities/fmaa]], [[entities/entra]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-application-interoperability]]

See also: [[summaries/REQ-active-session-renewal]]


See also: [[summaries/KT-ces-migration-parity]]
