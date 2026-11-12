---
sources: ["summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/KT-release-operations.md"]
type: "Product"
description: "Microsoft identity platform selected for Portal SSO without OneMFA fallback."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Entra

## What it is

Entra is the identity platform selected for Portal user SSO. The November clarification prohibits OneMFA fallback. The integration documents describe the design, Phase 1 scope, and former pilot activation steps. [Canonical SSO criterion](../sources/KT-authentication-and-sessions.md#portal-sso-ac-001)

Two evidence strands exist. The release calendar records Entra go-live entries as planning milestones. The authentication and sessions topic records the design intent and the unresolved questions around it.

## Key facts from the source

### Release calendar entries

- The release calendar lists separate **Entra technical** and **Entra business** go-live entries. [Release calendar, lines 5–16](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/page.md#L5>)
- This entry pair separates a technical milestone from a business activation milestone.
- A calendar entry gives planning context only. It does not prove deployment, approval, or successful adoption.
- No document in this set records an Entra configuration change, a completed go-live, or an acceptance sign-off.

### Intended authentication flow

- The design uses a browser redirect followed by an authorization-code exchange through the BFF. [Entra design, lines 7–31, 40–68](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md>)
- The BFF builds user information, retrieves EMS2 entitlements, and issues authentication and entitlement tokens.
- The historical design retained OneMFA fallback during the pilot and described a separate username/password path.
- The migration replaces the SSO provider. Entitlement retrieval and portal-session management remain separate responsibilities.

### Phase 1 scope

- Phase 1 covers UI SSO migration only. [Entra phase 1, lines 15–21, 48–57](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/page.md>)
- It excludes EMS2 replacement, portal session management, and tenant-onboarding authentication.
- Machine-to-machine authentication has a separate phase 2 service-account document with unresolved central dependencies. [Service-account migration, lines 1–10](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal & RATAN Entra Migration - Phase 2 - service account/page.md>)

### Onboarding and verification steps

- The non-production guide requires a development AD account, Authenticator registration, and RATAN AD-group membership. [Non-production verification guide, lines 5–56, 58–126](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Non Prod Verification/page.md>)
- It asks teams to check successful login, user information, and expected tile visibility. Its FAQ associates missing entitlements with tile access and EMS2 configuration.
- The production pilot describes Windows Hello or Authenticator login and an Entra session of one hour. [Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)
- That one-hour provider session does not settle the portal refresh-token lifetime.

### Profile differences during migration

- The production guide warns that AD profile values differ from OUD values.
- It identifies changed surname formatting, country codes, and missing locale values.
- Downstream audit or application logic can therefore require profile-field review during migration.

### Former pilot activation

- The design uses `ENABLE_ENTRA_SSO=true/false`.
- The production guide uses `yes/no` and describes both temporary activation and persistent activation after first use.
- These conflicting instructions concern the former pilot.

## Why the distinction matters

The release topic treats technical readiness and business activation as separate evidence classes. The Entra entry pair is one documented example of that split. See [[concepts/tenant-production-readiness]] for the wider readiness evidence model.

The same separation appears in other sources. The [[entities/openfin]] briefing splits technical onboarding from business user onboarding. The [[entities/ddr]] request places business UAT sign-off after technical go-live. KT release operations records these cases together.

The portal has separate limits of 15 minutes idle and 60 minutes absolute from portal authentication. The stated logout ideal revokes portal sessions immediately and excludes the Entra session. [Canonical renewal criteria](../sources/REQ-active-session-renewal.md#acceptance-criteria) · [Canonical logout criterion](../sources/KT-authentication-and-sessions.md#portal-logout-ac-001)

## Related pages

- [[concepts/identity-provider-delegation]] — how identity duties are delegated across applications.
- [[concepts/cross-application-authentication-handoff]] — how authentication passes between applications.
- [[concepts/single-ui-sdk-authentication]] — the SDK path for authentication in the Portal.
- [[concepts/entitlement-retrieval]] — how the BFF obtains EMS2 entitlements after authentication.
- [[concepts/token-lifecycle-and-timeout-policy]] — portal timeout ceilings and token lifetime questions.
- [[concepts/session-activity-renewal]] and [[concepts/session-expiry-prompt-recovery]] — intended portal-session renewal behavior.
- [[concepts/identity-profile-attribute-migration]] — AD-to-OUD profile value differences.
- [[concepts/machine-to-machine-authentication]] — the separate service-account migration path.
- [[concepts/portal-entry-and-tile-authorization]] — the entry rule applied after authentication.
- [[entities/ratan-auth-server]] and [[entities/fmaa]] — other authentication components named in this document set.
- [[entities/single-ui-bff]] and [[entities/ems2]] — the components that consume Entra logins and supply entitlements.
- [[entities/portal-team]] — earlier access-rule responsibility and the later RATAN portal-policy ownership clarification.
- [[entities/fmo-post-trade-portal]] and [[entities/markets-operations-one-release]] — the Portal and the release programme that schedule the Entra go-live dates.
- Release window governance — how release windows are scheduled and frozen.
- [[summaries/KT-release-operations]] and [[summaries/KT-authentication-and-sessions]] — the source summaries for this page.

## Evidence limits

Effective Entra deployment, tenant mapping, and go-live completion remain unverified. The RATAN team owns and reviews portal policy under ICS. Original pilot page revisions and human publication review remain pending.


## Related Documents

- [[summaries/KT-release-operations]]
- [[summaries/KT-authentication-and-sessions]]
- [[summaries/KT-sdk-and-entitlements]]
- [[summaries/REQ-active-session-renewal]]
