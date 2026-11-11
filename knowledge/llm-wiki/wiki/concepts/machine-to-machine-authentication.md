---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md"]
description: "How non-human callers authenticate via client credentials, service accounts, and bank IDs, distinct from UI SSO."
---

# Machine-to-Machine Authentication

## Definition

Machine-to-machine (M2M) authentication is how non-human callers — services, scheduled jobs, and integration components — prove their identity to portal APIs without a user present. It is the counterpart to interactive user login: instead of a browser redirect and an authorization-code exchange, a caller presents its own credentials, typically client credentials tied to a provisioned service account. Callers receive tokens that applications validate the same way they validate user tokens, but the identity that the token represents is an application or service rather than a person.

## Position within the authentication landscape

The source topic [[summaries/KT-authentication-and-sessions]] separates three concerns that are easy to conflate: user authentication (who the person is), entitlements (what that identity may see or do), and the portal session (how long a UI interaction lasts). M2M authentication belongs to the first concern but sits on a different path. The Entra UI SSO work described in that topic covers only interactive browser logins for phase 1; it explicitly excludes machine-to-machine flows, which have their own migration document and their own unresolved dependencies. M2M therefore is not solved by the UI SSO migration and should not be assumed to follow the same provider timeline.

This distinction matters operationally: a change to the interactive identity provider does not automatically change how services authenticate to each other, and a pilot that validates browser login says nothing about service-account readiness.

## Documented model: FMAA client credentials

The historical [[entities/fmaa]] reference describes the documented M2M model:

- **Client-credential authentication.** Callers authenticate with client credentials issued to them, rather than with a user's credentials.
- **Separate onboarding paths.** Service-account onboarding is treated separately from bank-ID onboarding. They are distinct flows with distinct credential lifecycles, not variants of one flow.
- **OUD-managed accounts.** Accounts are managed in the directory (OUD) and authenticated through FMAA, so directory state and authentication state are coupled.
- **Asymmetric validity.** The reference states 17-year validity for service accounts and seven-day validity for bank IDs.

That asymmetry is the most consequential detail in the source. A 17-year credential implies a deliberately long-lived, rarely rotated trust relationship; a seven-day credential implies frequent rotation. Systems that assume uniform rotation policy across both categories will mis-handle at least one of them.

## Evidence limits

The FMAA values are **historical reference values, not approved policy**. They come from an admin-module release checklist reference page, carry no confirmed approval authority, and predate the current provider direction. They must not be copied into a target rule without authoritative confirmation. Specifically, they do not establish:

- current token validity or rotation requirements;
- which of the two onboarding paths a given caller should use;
- whether client credentials remain the target mechanism under the current identity provider;
- any portal session limit (M2M callers have no portal session).

The source topic records this as an open question: which documented FMAA flows and validity settings remain intended requirements, with an unknown authentication owner and a next action to confirm the intended provider contract and validity limits for each supported flow.

## Why this is hard to settle

M2M authentication couples several independently owned concerns:

1. **Credential issuance** — who mints a client credential and on what authority.
2. **Directory ownership** — accounts live in OUD today; a provider migration changes who governs them.
3. **Token contract** — what claims downstream services can rely on, mirroring the user-token questions in [[concepts/token-lifecycle-and-timeout-policy]].
4. **Entitlement lookup** — service callers still need scoped access to resources, which connects to [[concepts/ems2-entitlement-provisioning]].
5. **Onboarding sequencing** — a service cannot authenticate before its account exists, tying M2M to [[concepts/admin-catalog-configuration]].

Because each concern has a different owner, M2M migration tends to lag user-facing SSO migration. The source notes unresolved central dependencies for the service-account phase, which is the practical signature of this coupling.

## Relationship to adjacent concepts

- [[concepts/identity-provider-delegation]] — how the portal delegates authentication to an external provider; the M2M path is a separate delegation surface.
- [[concepts/single-ui-sdk-authentication]] — the interactive counterpart, covering browser login for the UI.
- [[concepts/cross-application-authentication-handoff]] — token passing between applications, which applies to both user and service tokens.
- [[concepts/portal-entry-and-tile-authorization]] — the user-facing outcome that M2M flows do not participate in.
- [[entities/entra]] and [[entities/ratan-auth-server]] — the provider and server contexts within which the M2M target must eventually be stated.

## Open questions

- Which documented FMAA flows and validity settings remain intended requirements?
- Which provider contract must non-human callers support after migration?
- Which onboarding path applies to each caller category, and who owns credential rotation?
- What happens to the 17-year service-account model under a provider that assumes shorter-lived credentials?

Owner: unknown authentication owner. Next action: confirm the intended provider contract and validity limits for each supported flow, with authoritative approval, before any historical value is treated as a target requirement.