---
sources: ["summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-application-interoperability.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md", "summaries/KT-sdk-and-entitlements.md"]
type: "Organization"
description: "User-reported owner of portal entry, tile, and release rules for the Post Trade Portal"
---

# Portal Team

## What it is
The Portal Team is the organizational owner of portal-level access rules for the [[entities/fmo-post-trade-portal]]. In the source material it appears as an owner identity recorded from user answers and as the receiving party in onboarding procedures. A draft release proposal also assigns it Portal routing, route enabling, tenant interfaces, and Portal-owned production changes. These are documented statements, not a formally confirmed authority. User identity behind the ownership statements remains unknown, and approval for the intended applicability remains pending.

## Key facts from the documents

### Access and tile rules
The Portal Team is identified as owner of these rules, in local, test, UAT, and production environments:

- **Portal entry restriction** — an authenticated SC user with no entitlement for any registered application entity is denied entry. Ownership was selected for this policy only.
- **Empty-entity tile restriction** — a tile with zero configured EMS2 entities is hidden and direct launch is denied.
- **Empty-subject tile rule** — a tile with zero configured subjects remains visible and launchable when the user holds entitlement for the tile's single configured entity.

The ownership statements come from user answers dated 22 October 2026. The document states that user identity and applicable implementation version are unknown. The answer defines no HTTP status, denial wording, or additional entity-versus-role semantics.

The entry rule agrees with the draft Portal principles, which state the same denial direction. An older tile-security proposal instead permits entry for SC accounts; that conflicting proposal is retained as historical evidence, not as the selected intent. Neither historical source establishes approved applicability. See [[concepts/portal-entry-and-tile-authorization]].

### Authentication and session ownership boundary
The portal team is named as owner of the portal-entry policy only. The authentication and session topic records no portal-team role for these adjacent areas:

- **Session renewal** — the target behavior of continued renewal under eligible activity and recoverable manual extension has no confirmed timing owner. Timeout and refresh-duration rules remain unresolved between two session designs. See [[concepts/session-activity-renewal]], [[concepts/session-expiry-prompt-recovery]], and [[concepts/token-lifecycle-and-timeout-policy]].
- **SSO migration** — [[entities/entra]] migration scope, the `ENABLE_ENTRA_SSO` activation grammar, and the persistence rule for activation have an unknown owner. See [[concepts/identity-provider-delegation]] and [[concepts/single-ui-sdk-authentication]].
- **Profile contract** — the identity-provider profile contract that downstream services must support, including changed surname, country-code, and locale values, has an unknown owner. See [[concepts/identity-profile-attribute-migration]].
- **Machine-to-machine authentication** — the historical [[entities/fmaa]] validity settings for service accounts and bank IDs carry an unknown authentication owner. See [[concepts/machine-to-machine-authentication]].

These boundaries mean the portal-team ownership statement does not extend to session timing, token validity, migration scope, or provider configuration.

### Release responsibilities
The draft release proposal in [[summaries/KT-release-operations]] separates Portal and tenant responsibilities. It covers Portal routing, route enabling, tenant interfaces, and Portal-owned production changes.

- The Portal Team executes Portal releases and routing rollback.
- Tenant teams retain responsibility for their UI, backend, services, databases, and infrastructure.
- Tenant teams validate their applications, perform UVT, and support tenant issues.

The source uses 'Portal teams' for this scope. The statements describe proposed responsibility, without confirmed present approval or evidence of execution.

### Readiness before scheduling
The release proposal requests solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning. New interfaces require 30 days of engagement under the proposal. The unfinished checklist adds SDK validation, shared frontend requests, entitlement checks, disaster recovery, performance inputs, operating agreements, and penetration testing. These are requested readiness inputs; they do not prove completed checks, and the supplied text does not name the Portal Team as owner of each input.

### Release window proposal
The proposal schedules first, third, and available fifth Saturdays at 09:00 SGT. It freezes scope after Monday EOD in the first week, cancels windows without requests, and requires approved exceptions for late additions. Two rules remain unresolved: the summary states 24 hours while the table states 10 hours ending at 19:00 SGT, and the urgent-release section requires all confirmations but also permits proceeding when nobody raises concerns. The topic does not choose between these alternatives.

### Technical and business activation
The release calendar distinguishes Portal release dates from tenant release dates and lists separate Entra technical and business go-live entries. This supports a boundary in which the Portal Team plans Portal deployment while tenant teams own application go-live and business adoption. [[concepts/tenant-production-readiness]] explains why technical deployment and business activation need distinct evidence. A calendar entry establishes planning context, without proving deployment, approval, or successful adoption.

### Onboarding role
The frontend onboarding procedure requires each application team to inform the portal team about its static-file and API URLs. The portal team therefore receives the routing information that later feeds [[entities/nginx]] configuration and the portal catalog.

The development principle assigns portal-backend availability to the microfrontend team, not to the Portal Team. It assigns each application's backend availability to that application team. The two responsibilities are separate and must not be merged.

The [[concepts/frontend-onboarding]] procedure starts from container and tile templates and then links application registration through the admin manual. These steps describe a hand-off to catalog administration, not a named Portal Team task.

### Catalog administration and promotion context
The admin manual defines Module Mapping, Drawer Category, and Tile Configuration functions and a different-user check before activation. It names `FMO PORTAL ADMIN` entitlements for those functions. The documents do not state that the Portal Team holds those entitlements or performs those actions. See [[concepts/admin-catalog-configuration]] and [[concepts/maker-checker-verification-workflow]].

[[concepts/configuration-promotion]] describes Module Map, Drawer Category, and Tile Configuration changes exported as CSV files and uploaded by an ADO pipeline to the Portal Admin service. The flow also says the service validates an FMAA JWT before processing CSV files. The supplied text does not name the Portal Team as the pipeline operator, and the checklist flags planned FMAA decommissioning as an unresolved dependency.

EMS2 setup creates entities, actions, roles, and subjects before an operator can act. The Portal Team is not recorded as the operator of that setup. See [[concepts/ems2-entitlement-provisioning]].

### Production and ingress boundary
The production checklist recommends Portal connections through tenant Nginx or load balancers. Tenant teams then control internal server and port changes behind that boundary. This makes [[concepts/portal-ingress-path]] a shared boundary rather than a purely Portal-owned path.

The production checklist separately requests browser reachability, Portal-to-tenant connectivity, operating agreements, security testing, and tile release. These are distinct checks; successful configuration upload alone does not establish business readiness. Older deployment guidance and the Nginx draft propose different mechanisms, and neither establishes the currently deployed pipeline.

## Limits and unknowns
- Authority and approval remain unconfirmed for every stated rule; publication approval and deployed enforcement are both pending. The open questions ask what evidence confirms portal-team authority and approval across the stated environments.
- The owner identity does not establish that the Portal Team operates [[entities/ems2]] or [[entities/ces]], nor that it configures tile onboarding.
- The documents do not establish that the Portal Team holds tenant-record boundaries for maker and checker users, or that it applies a multiple-entity matching rule for SSDR tenants.
- No denial message, HTTP status, timing limit, or execution evidence was selected with these rules.
- No session timing, token validity, activation grammar, or profile contract is owned by the Portal Team in the supplied material; those remain with unknown owners.
- No pipeline, deployment, routing rollback, upload, or production access check ran during the supplied release material.
- The release proposal is a draft with unresolved duration and urgent-confirmation rules. The governing checklist and active deployment process for each environment remain unconfirmed.
- Further questions ask which release and approval controls govern self-service configuration changes that the owner may authorize, and how technical readiness and business activation are proved separately.

## Related pages
[[concepts/portal-entry-and-tile-authorization]] describes the entry and tile rules the Portal Team is reported to own.
[[concepts/entitlement-retrieval]] explains how entitlement data that feeds those rules is obtained.
[[concepts/single-ui-sdk-authentication]] covers the authentication layer that precedes the entry decision.
[[concepts/session-activity-renewal]] covers the renewal behavior that has no confirmed owner.
[[concepts/session-expiry-prompt-recovery]] covers the manual recovery behavior for an expired session.
[[concepts/token-lifecycle-and-timeout-policy]] holds the unresolved timing proposals.
[[concepts/identity-provider-delegation]] and [[concepts/identity-profile-attribute-migration]] cover the migration and profile boundaries outside portal-team ownership.
[[concepts/machine-to-machine-authentication]] covers the historical service-account flows.
[[concepts/frontend-onboarding]] describes the hand-off in which application teams supply URLs to the portal team.
[[concepts/admin-catalog-configuration]] covers the catalog functions that follow onboarding.
[[concepts/configuration-promotion]] covers the CSV-to-Portal-Admin upload flow described in the release materials.
[[concepts/tenant-production-readiness]] separates technical deployment from business activation.
[[entities/single-ui-sdk]] is the SDK described in the same document.
[[entities/entra]] and [[entities/single-ui-bff]] hold the authentication responsibilities that the portal-entry policy assumes.
[[summaries/KT-sdk-and-entitlements]] is the source summary for the access statements.
[[summaries/KT-authentication-and-sessions]] is the source summary for the authentication and session boundaries.
[[summaries/KT-admin-and-onboarding]] is the source summary for the onboarding and catalog statements.
[[summaries/KT-release-operations]] is the source summary for the release responsibilities and readiness statements.

See also: [[summaries/ARC-portal-service-relationships]]

See also: [[summaries/KT-frontend-composition]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-application-interoperability]]

See also: [[summaries/REQ-active-session-renewal]]