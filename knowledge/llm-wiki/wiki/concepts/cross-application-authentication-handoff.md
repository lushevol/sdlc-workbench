---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/KT-observability-and-performance.md", "summaries/KT-application-interoperability.md"]
description: "Passing an authenticated identity from one application to another so users avoid repeated logins."
---

# Cross-Application Authentication Handoff

Cross-application authentication handoff is the transfer of an authenticated identity — usually a token or a session assertion — from one application to another so the second application does not prompt the user to log in again. In a Portal-mediated desktop, the handoff links an authentication provider to the applications that Portal opens.

## Why it matters for interoperability

Interoperability features that open a target tile from a source tile raise an ownership question. If the target application runs in a separate window or view under [[entities/openfin]], it may not share the source application's browser session. The handoff answers how the target knows who the user is.

The topic is described in [[summaries/KT-application-interoperability]] alongside intent navigation, because an intent request that opens another application is only usable if the launched application can act on behalf of the same user.

## The proof-of-concept pattern

The supplied interoperability proof of concept describes a concrete sequence:

1. The user authenticates against the provider.
2. Application launches carry the provider token in URL parameters.
3. The launched application reads the token and skips its own login prompt.

It also notes that the proof of concept simplifies the provider interface, and that a real provider should run hidden after authentication rather than presenting an interactive screen.

This is an example technique, not an approved design. The source explicitly leaves production authentication design, security approval, and token-transport verification unresolved.

## Open risks

- **Token exposure.** A token in a URL can be captured in logs, history, referrers, or window titles. The source raises this as unresolved without prescribing a transport.
- **Trust boundary.** It is not documented which component validates the token at each launch, or whether each target application re-validates it.
- **Hidden-provider assumption.** Running the provider invisibly assumes a prior session already exists; the fallback when it does not is undocumented.
- **Environment drift.** The proof of concept and the later briefing describe different phases, and no source confirms what is deployed in each environment.

## Relationship to other authentication concepts

- [[concepts/single-ui-sdk-authentication]] covers the SDK-based authentication path within a single UI.
- [[concepts/identity-provider-delegation]] covers delegating identity checks to an identity provider.
- [[concepts/entitlement-retrieval]] covers what happens after identity is known — resolving what the user may access.
- [[concepts/portal-entry-and-tile-authorization]] covers authorization at Portal entry and at tile level.

The handoff concept sits between identity establishment and authorization: it carries an already-established identity across an application boundary so that downstream authorization can run.

## Relationship to interoperability concepts

- [[concepts/intent-based-application-interoperability]] — the navigation model whose launches need a handed-off identity.
- [[concepts/interoperability-contract-governance]] — the governance gap: the example channel and intent names are not an approved contract, and token transport has no equivalent approved contract at all.
- [[entities/fdc3]] — the intent and context abstraction used in the examples.
- [[entities/fmo-post-trade-portal]] and [[entities/mfe-ratan-container]] — the Portal and container components involved in launching applications.

## What the sources do not establish

No production authentication design was inspected. No security approval, penetration test, or token-handling review is supplied. No credential, token value, or personal identifier is reproduced in the wiki. Whether the described pattern is in use in any environment remains an open question recorded in [[summaries/KT-application-interoperability]].

## Open question

How does production authentication avoid unsafe token handling across application launches, and which component is responsible for validating a handed-off identity before the target application acts on it?

See also: [[summaries/KT-observability-and-performance]]

See also: [[summaries/REQ-active-session-renewal]]

See also: [[summaries/KT-authentication-and-sessions]]