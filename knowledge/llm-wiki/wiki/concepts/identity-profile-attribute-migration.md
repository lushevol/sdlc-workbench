---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md"]
description: "Risk that user profile attribute values change between identity providers during SSO migration, affecting downstream logic."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Identity Profile Attribute Migration

## Definition
Identity profile attribute migration is the risk that user profile attribute values change format or availability when the identity provider changes, and that downstream logic which reads those values behaves differently after the migration.

## Source detail
During the Entra migration, the production pilot guide warns that AD profile values differ from OUD values. It identifies three concrete differences:

- Surname formatting changes.
- Country codes change.
- Locale values can be missing.

The guide states that downstream audit or application logic can therefore require a profile-field review during migration. The same guide describes the intended pilot-user authentication journey, including Windows Hello or Authenticator authentication and a one-hour Entra session. That provider-session statement does not settle portal refresh-token lifetime or profile contracts.
[Production pilot guide](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

## Where the profile is built
The Entra design describes a browser redirect and BFF code exchange. The BFF builds user information, retrieves EMS2 entitlements, and issues authentication and entitlement tokens. The design places provider-to-portal profile mapping at the BFF and leaves the full downstream contract open. The November clarification prohibits OneMFA fallback for portal SSO. [Canonical SSO criterion](../sources/KT-authentication-and-sessions.md#portal-sso-ac-001)
[Entra design, lines 7–31, 40–68](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md>)

## Scope boundaries
Phase 1 of the migration covers UI SSO only. It excludes EMS2 replacement, portal session management, and tenant-onboarding authentication. Machine-to-machine authentication has a separate migration document with unresolved central dependencies. Profile attribute differences therefore sit inside the phase 1 SSO boundary but can still affect any downstream consumer of user attributes.
[Entra phase 1, lines 15–21, 48–57](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/page.md>)
[Service-account migration, lines 1–10](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal & RATAN Entra Migration - Phase 2 - service account/page.md>)

## Non-production checks
The non-production verification guide requires a development AD account, Authenticator registration, and RATAN AD-group membership. It asks teams to check successful login, user information, and expected tile visibility. It does not name a profile-field comparison step.
[Non-production verification guide, lines 5–56, 58–126](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Non Prod Verification/page.md>)

## Evidence limits
- The supplied pilot documents have local byte revisions. Human publication review and the full downstream profile contract remain pending.
- The open question in the source topic remains: which identity-provider profile contract must downstream services support?
- The attribute differences are documented warnings, not a verified inventory of affected fields or consumers.
- The FAQ links missing entitlements to tile access and EMS2 configuration; that is an entitlement concern, not a profile-attribute concern, and the two should not be merged.

## Related topics
- [[summaries/KT-authentication-and-sessions]] holds the consolidated authentication and session material, including this warning.
- [[concepts/identity-provider-delegation]] covers which provider authenticates the user and which component exchanges the code.
- [[concepts/single-ui-sdk-authentication]] covers how the frontend consumes authentication and user state.
- [[concepts/entitlement-retrieval]] covers the separate EMS2 entitlement lookup that follows authentication.
- [[concepts/portal-entry-and-tile-authorization]] covers how user and entitlement data gate portal entry and tile visibility.
- [[concepts/cross-application-authentication-handoff]] covers how identity context passes between applications.
- [[concepts/tenant-production-readiness]] covers the broader set of checks required before a tenant or environment goes live.
- [[entities/entra]] is the intended identity provider. [[entities/fmo-post-trade-portal]] is the affected portal. The RATAN team owns portal policy under ICS, and downstream application owners need to confirm any additional profile fields.

## Open action
Confirm any additional profile fields with the owners of affected downstream services.
