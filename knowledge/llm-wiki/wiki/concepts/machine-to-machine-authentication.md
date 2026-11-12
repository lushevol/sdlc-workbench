---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md"]
description: "How non-human callers authenticate via client credentials, service accounts, and bank IDs, distinct from UI SSO."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Machine-to-Machine Authentication

## Definition

Machine-to-machine (M2M) authentication is how non-human callers — services, scheduled jobs, and integration components — prove their identity to portal APIs without a user present. It is the counterpart to interactive user login: instead of a browser redirect and an authorization-code exchange, a caller presents its own credentials, typically client credentials tied to a provisioned service account. Callers receive tokens that applications validate the same way they validate user tokens, but the identity that the token represents is an application or service rather than a person.

## Position within the authentication landscape

The source topic [[summaries/KT-authentication-and-sessions]] separates three concerns that are easy to conflate: user authentication (who the person is), entitlements (what that identity may see or do), and the portal session (how long a UI interaction lasts). M2M authentication belongs to the first concern but sits on a different path. The Entra UI SSO work described in that topic covers only interactive browser logins for phase 1; it explicitly excludes machine-to-machine flows, which have their own migration document and their own unresolved dependencies. M2M therefore is not solved by the UI SSO migration and should not be assumed to follow the same provider timeline.

This distinction matters operationally: a change to the interactive identity provider does not automatically change how services authenticate to each other, and a pilot that validates browser login says nothing about service-account readiness.

## Documented model: FMAA client credentials

The historical [[entities/fmaa]] reference describes the documented M2M model:

- **Client-credential authentication.** Callers authenticate with client credentials issued to them, rather than with a user's credentials.
- **Separate onboarding paths.** The reference gives separate procedures for service-account onboarding and bank-ID onboarding.
- **OUD-managed accounts.** The historical reference describes accounts managed in OUD and authenticated through FMAA. Current directory ownership remains unconfirmed.
- **Generated-token validity.** The historical reference states generated-token validity of 17 years for service accounts and seven days for bank IDs.

These historical generated-token examples define no password or client-secret rotation interval. The applicable provider contract, validity limits, and rotation policy require authoritative confirmation. See the [canonical historical M2M limits](../../../candidates/security/KT-authentication-and-sessions.md#historical-machine-to-machine-authentication).

## Evidence limits

The FMAA values are **historical reference values, not approved policy**. They come from an admin-module release checklist reference page, carry no confirmed approval authority, and predate the current provider direction. They must not be copied into a target rule without authoritative confirmation. Specifically, they do not establish:

- current token validity or rotation requirements;
- which of the two onboarding paths a given caller should use;
- whether client credentials remain the target mechanism under the current identity provider;
- any portal session limit (M2M callers have no portal session).

The source topic records this as an open question: which documented FMAA flows and validity settings remain intended requirements, with an unknown authentication owner and a next action to confirm the intended provider contract and validity limits for each supported flow.

## Why this is hard to settle

Confirm the target provider contract through the following linked questions:

1. **Credential issuance** — who issues a client credential, and under which authority?
2. **Directory ownership** — which directory and owner apply to each supported caller, given the historical OUD reference?
3. **Token contract** — which claims may downstream services rely on? See [[concepts/token-lifecycle-and-timeout-policy]].
4. **Entitlement lookup** — which scoped access must each service caller receive? See [[concepts/ems2-entitlement-provisioning]].
5. **Onboarding sequencing** — which account and application configuration prerequisites apply? See [[concepts/admin-catalog-configuration]].

The source records unresolved central dependencies for the service-account phase. Current ownership for each concern and the migration schedule remain unconfirmed.

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
- Which generated-token validity limits and credential-rotation policy apply to each supported caller category under the target provider?

Owner: unknown authentication owner. Next action: confirm the intended provider contract and validity limits for each supported flow, with authoritative approval, before any historical value is treated as a target requirement.