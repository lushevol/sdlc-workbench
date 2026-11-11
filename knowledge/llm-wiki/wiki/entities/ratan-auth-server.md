---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "Portal authentication and authorization service delegating identity checks to OUD, Entra and FMAA."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# RATAN Auth Server

RATAN Auth Server is the portal's authentication and authorization service, as reported in the user architecture clarification captured in [[summaries/ARC-portal-service-relationships]]. It handles two distinct jobs: **internal service authentication** and **authorization of external API callers**.

## Reported responsibilities

According to the user clarification, the Auth Server delegates:

- **Authentication** to OUD, Entra SPN, and FMAA.
- **Authorization** to EMS2 and EMS3.

This delegation model is the concrete instance of [[concepts/identity-provider-delegation]] and [[concepts/entitlement-retrieval]], where the portal separates *who the caller is* from *what the caller may do*.

## What the local sources confirm

The source review behind the architecture record supports local OUD, FMAA, and [[entities/ems2]] paths. It does **not** find an identified Entra SPN or [[entities/ems3]] implementation inside this copy of the Auth Server.

The same capabilities do appear elsewhere in the examined code:

- [[entities/single-ui-bff]] contains Entra token exchange logic.
- The BFF also contains EMS3 entitlement calls.

So the reported provider list is not fully represented in the Auth Server copy under review. The clarification should not be read as proving an inferred Auth Server hop for those providers.

## Machine-to-machine authentication

[[summaries/KT-authentication-and-sessions]] supplies the historical provider context for the FMAA path. The historical FMAA reference describes client-credential authentication for machine-to-machine callers, separates service-account onboarding from bank-ID onboarding, and describes OUD-managed accounts authenticated through [[entities/fmaa]]. It states 17-year validity for service accounts and seven-day validity for bank IDs. Those historical values are recorded examples, not approved token policy or current portal-session limits. See [[concepts/machine-to-machine-authentication]].

The same topic records a separate Phase 2 migration document for the portal and RATAN service accounts. That document describes machine-to-machine authentication migration with unresolved central dependencies; it does not establish an Auth Server implementation change.

## Entra migration context

The Entra migration materials describe a browser redirect followed by an authorization-code exchange through [[entities/single-ui-bff]]. The BFF builds user information, retrieves EMS2 entitlements, and issues authentication and entitlement tokens, and its design retains OneMFA fallback plus a separate username/password path. Phase 1 covers UI SSO only and explicitly excludes EMS2 replacement, portal session management, and tenant-onboarding authentication.

This places user-facing authentication in the BFF rather than in the Auth Server copy under review. The Entra migration replaces the SSO provider while preserving separate entitlement and portal-session responsibilities; it does not document a change to the Auth Server's internal service authentication role.

Operational onboarding also depends on directory configuration: the non-production verification guide requires a development AD account, Authenticator registration, and RATAN AD-group membership, and the production pilot warns that AD profile values differ from OUD values in surname formatting, country codes, and missing locale values. Those differences can affect downstream audit or application logic and are tracked as [[concepts/identity-profile-attribute-migration]].

All of these statements come from candidate topic and source materials with unconfirmed original page revisions and approval authority. Provider scope, token validity, and session timing remain open questions, with no authoritative owner confirmed.

## Boundaries and caveats

- The reported scope does not establish that every portal request invokes the Auth Server. Authentication for portal traffic is also described through [[concepts/single-ui-sdk-authentication]] and the [[entities/single-ui-sdk]] library used by application backends.
- The upstream ingress chain — [[entities/nginx]] and [[entities/api-gateway]] — is reported but its effective deployment is unconfirmed, so the Auth Server's runtime position in that path is unverified.
- The copy inspected here has no independent Git history; file hashes identify content, not an upstream commit.
- Timeout and refresh-duration rules for portal sessions are unresolved across competing session designs; see [[concepts/token-lifecycle-and-timeout-policy]]. Portal-session renewal intent is held separately in [[concepts/session-activity-renewal]] and [[concepts/session-expiry-prompt-recovery]].

## Related pages

- [[summaries/ARC-portal-service-relationships]] — the source record for these claims.
- [[summaries/KT-authentication-and-sessions]] — authentication, session, and Entra migration boundaries.
- [[concepts/portal-ingress-path]] — the reported Nginx to gateway to service path.
- [[concepts/microfrontend-layering]] — the frontend layers whose sessions this service underpins.
- [[concepts/cross-application-authentication-handoff]] — how authentication context moves between applications.
- [[entities/single-ui-bff]] — the portal backend holding Entra and EMS3 code that the Auth Server copy lacks.

See also: [[summaries/REQ-active-session-renewal]], [[summaries/KT-sdk-and-entitlements]]

See also: [[summaries/KT-ces-migration-parity]]