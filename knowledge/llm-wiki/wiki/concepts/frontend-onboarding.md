---
type: "Concept"
sources: ["summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md"]
description: "How an application team registers containers and tiles and proves release readiness."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Frontend onboarding and app registration

## Definition

Frontend onboarding is the repeatable procedure by which an application team creates its own container and tile repositories, registers them with the shared portal, and delivers them into a running workspace. Application registration is the second half of that act: the platform must know where a tile's code lives, which module name resolves to which asset path, and which route or menu entry should load it.

The concept sits between the design of the [[concepts/microfrontend-layering]] and the operational delivery described in release and administration processes. The composition model itself is summarized in [[summaries/KT-frontend-composition]]. Registration is performed through the portal's admin catalog functions, which are covered in [[concepts/admin-catalog-configuration]].

## Why it exists

The documented design separates common platform modules from application-owned domain modules. The stated problems behind this split are coupled releases, broad testing scope, unclear ownership, and duplicated components. Onboarding is the mechanism that turns that separation into a working product: each team ships its own container and tiles on its own pipeline while users remain inside one portal shell.

An earlier admin overview describes the previous process, in which every tile change required editing the base shell source and raising a production change request. It proposes tenant-maintained configuration so that routine catalog changes do not repeat that release work. That proposal does not establish an approved exemption from production change controls.

Ownership is therefore part of onboarding, not an afterthought. See [[concepts/application-ownership]] for the division of responsibilities between the platform team and tenant teams. The development principle assigns portal-backend availability to the microfrontend team and each application's backend availability to its application team; it also separates feature-branch contribution from review and approval of shared-repository changes.

## Documented sequence

1. **Obtain the templates.** Take the root configuration and the application container and tile templates from the platform team. The frontend procedure starts from these separate container and tile templates.
2. **Create two repositories.** The container and the tile are separate projects with separate pipelines.
3. **Adapt the templates.** Update module names, build configuration, imports, exported interfaces, and container entry points.
4. **Update tests and the local import map.** Unit tests must follow the renamed modules; the local import map must point at the new module names.
5. **Configure the tile administratively.** The tile is registered through the Admin Module procedure so the portal knows it exists. This step is described under *Registration, verification, and activation* below.
6. **Build, deploy, and hand over URLs.** Each application supplies its own build pipeline and tells the platform team the static-file URL and the API URL for the deployed configuration.
7. **Complete backend prerequisites.** Supply application URLs for proxy configuration and CORS handling, create the required roles or entitlements in EMS2, and integrate SDK-based JWT validation and entitlement checks in the service.

Step 5 links onboarding to [[concepts/portal-entry-and-tile-authorization]]: registration makes a tile addressable, but whether a given user can open it is decided by entitlement and entry rules, not by registration alone.

## Release intake and readiness gates

The release material reviewed in [[summaries/KT-release-operations]] treats onboarding as an intake process that precedes scheduling, not as a code task alone. Under the release proposal, a new interface requires 30 days of engagement, and the request must carry solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning. The blank change-request template used by [[entities/markets-operations-one-release]] adds DNS resolution, expected total, new, and concurrent user counts, plus separate fields for routing changes, connectivity evidence, sign-off, and UVT contacts.

An unfinished checklist widens the readiness set: SDK validation, shared frontend requests, entitlement checks, disaster recovery, performance inputs, operating agreements, and penetration testing. These are stated prerequisites, not evidence that any tenant has satisfied them. The checklist itself is still under construction, so which document currently governs each environment is unresolved. Release windows, scope freeze, and exception handling are covered in [[concepts/release-window-governance]]; the tenant-side gate set is covered in [[concepts/tenant-production-readiness]].

Onboarding should also separate technical onboarding from business activation. The release calendar keeps Portal release dates apart from tenant release dates and lists separate Entra technical and business go-live entries. The DDR request states that business UAT sign-off follows technical go-live, and the request template explicitly allows Portal deployment before application deployment. A calendar entry or a target date therefore does not prove a completed deployment or accepted capability.

Tenant requests expose how often that evidence is incomplete. The [[entities/cdups]] request leaves UAT sign-off, user profiles, user counts, and UVT details unprovided. The [[entities/ddr]] request records pending connectivity and separates technical sign-off from business validation. Several [[entities/vpa]] evidence references are struck through. Withdrawn or missing references cannot close the corresponding gate.

## Registration, verification, and activation

The admin manual identifies three catalog functions. A **module mapping** connects an import-map module name with its asset path; users enter the module name without the `@fm/` prefix and without spaces, and the active import-map API adds the prefix automatically. A **drawer category** groups application tiles and carries a unique label. A **tile record** connects display details, container identity, route information, and entitlement configuration. The manual lists labels, descriptions, theme images, container identity, routes, role subjects, and role entities as tile fields, and requires module and tile paths to match their routing paths. Those paths are entered without a leading slash or spaces, and comma-separated role entities are converted into an array by the API.

Registration is not immediate activation. Creation or modification produces an `un-verified` record; a different user checks and verifies that record before it becomes active. Deactivation of a verified record returns it to `un-verified` status, and each admin function keeps its own audit history with record-specific history viewing. The supplied text does not fully specify rollback, activation propagation, or concurrent edits. See [[concepts/maker-checker-verification-workflow]].

The manual identifies `FMO PORTAL ADMIN` entitlements for the import-map, category, and tile functions. Those entitlements and the EMS2 role assignments are prerequisites for onboarding; they are not evidence that any current operator holds them.

## Roles in the procedure

| Element | Responsibility during onboarding |
| --- | --- |
| Root configuration and import map | Locate modules and carry shared loading configuration ([[entities/mfe-root-config]]). |
| [[entities/systemjs]] | Resolve registered module names to deployed files. |
| [[entities/single-spa]] | Mount the shell and manage application lifecycle. |
| Base shell | Provide common routing, global state, and theme context ([[entities/mfe-base]]). |
| Application container | Connect the team's domain modules to the portal (for example [[entities/mfe-ratan-container]]). |
| Application tiles | Supply the user-facing domain views (for example [[entities/mfe-cashflow-blotter]]). |
| Admin backend | Serve catalog administration; the overview records reuse of [[entities/single-ui-bff]]. |
| [[entities/ems2]] | Hold entities, actions, roles, and subjects used for tile and function entitlements. |
| [[entities/nginx]] | Route static files and API requests through configured locations; see [[concepts/portal-ingress-path]]. |

The microfrontend team owns shared backend availability and reviews changes to shared repositories. Each application team owns its domain backend availability, chooses its deployment approach, and supplies the static-file and API URLs. The release proposal draws the same line: Portal teams own Portal routing, route enabling, tenant interfaces, and Portal production changes, while tenant teams keep responsibility for their UI, backend, services, databases, and infrastructure, and perform their own validation and UVT.

## Entitlement conditions attached at registration

Registration defines which entities may reach a tile, but the authorization vocabulary comes from [[concepts/ems2-entitlement-provisioning]]: an entity, its actions, its roles, and its subjects are created first, then actions are assigned to role-and-subject combinations. Onboarding therefore spans routing, authentication, authorization data, and UI registration rather than UI code alone.

One explicit user clarification covers tiles whose subject setting is empty. Such a tile may be visible and launched through a single configured entity, provided the user satisfies portal-entry requirements and holds entitlement for that entity. The `portal team` owns this decision across local, test, UAT, and production, and approval is still pending. The clarification resolves only the single-entity, empty-subject scope; it selects no multiple-entity matching rule and no delegation option. See [[concepts/portal-entry-and-tile-authorization]].

The SSDR onboarding discussion records further alternatives for tenants whose report and download users hold different entity assignments: multiple tile entities, optional subject checks per tenant, adding missing EMS2 assignments, or delegating authorization to SSDR. Under those proposals an empty subject would skip validation — which the clarification above addresses only for the single-entity case. The temporary guest-access approach is struck through, and the discussion states that the portal does not implement entitlement control outside existing systems such as EMS2. None of these alternatives establishes an approved bypass or a deployed permission rule.

## Routing and connectivity intake

The NGINX draft collects the routing information that onboarding must supply: upstream name, host, port, route path, rewrite rule, protocol, request limits, environment, WebSocket settings, timeouts, load-balancing method, and custom headers. It separates non-production maintenance from UAT and stage configuration work, and raises configuration testing and rollback as improvement proposals rather than settled procedure. A separate firewall register supplies operational connectivity context; its addresses and contact details remain in the original material and current network approvals were not verified.

The production checklist recommends the same boundary from the deployment side: Portal connections should pass through tenant Nginx or load balancers, leaving tenant teams in control of internal server and port changes behind that point. It asks separately for browser reachability, Portal-to-tenant connectivity, operating agreements, security testing, and tile release.

These fields describe what onboarding must determine. They do not establish current endpoint values, active configuration, or a working deployment pipeline.

## Configuration promotion path

The Admin Module release flow documents how catalog records travel from development to production, distinct from pressing buttons in the admin screens. Teams first edit Module Map, Drawer Category, and Tile Configuration records in Development, export those records as CSV files, and retain them in a tenant-owned repository. An ADO pipeline then uploads the configuration to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`; the flow states that the service validates an [[entities/fmaa]] JWT before processing the CSV files.

The first bulk insert into UAT and Production uses a separate BFF release rather than tenant tooling, and later uploads depend on tenant connectivity to the Admin service. The checklist also flags planned FMAA decommissioning, which leaves an unresolved dependency in the documented promotion path. This is described procedure only; no upload execution was inspected during ingestion. See [[concepts/configuration-promotion]] for the cross-document view.

## Development standards applied at onboarding

The development guideline prescribes TypeScript, functional components, shared [[entities/mui]] themes, and separation of view, logic, styles, and interfaces. It names React 18.2.0 and prefers Context and Reducer over additional state libraries. Optional loading guidance suggests files of about 500 KB and six concurrent static-file requests, but this is not an accepted performance SLA.

Shared components can also be consumed outside the container-and-tile model: the standalone [[entities/react]] template reuses [[entities/mfe-base]] components through import-map registration. Its no-install claim concerns consuming those components only; the template still installs its own dependencies.

Because modules are shared by registered name, onboarding is where [[concepts/shared-dependency-governance]] becomes concrete. A new tile that pins a different shared-library version can affect other consumers, so dependency choices should be agreed before the first deployment rather than discovered afterwards.

The supplementary dependency principle prohibits direct external GUI dependencies unless the platform reviews and approves an exception; tenant teams retain security, licensing, vulnerability, support, resilience, and rollback responsibility for anything they introduce.

## Deployment path at handover

The supplied deployment material does not converge on one pipeline. The older frontend deployment guide describes static artifacts, a proposed blue-green model, shared Pilot and Production backends, feature checks, artifact publication, and a manual production deployment after approval. The Nginx draft proposes versioned configuration, syntax checks, restart checks, and rollback. Neither document establishes the currently deployed mechanism, so onboarding handover must confirm the active pipeline rather than inherit either description.

## Persistence behind catalog records

The [[entities/flyway]] page retains SQL that defines import-map records with unique keys, categories with unique labels, and tile records that reference both through foreign keys, plus separate audit tables for each. These definitions use the same vocabulary as the admin screens, but they are retained design statements rather than a confirmed deployed schema or an executed migration.

## Evidence limits

The onboarding procedure is documented, but the supplied copy depends on missing archives and screenshots for the getting-started guide, so the full local setup cannot be reproduced from the text alone. The admin overview and the schema draft are proposals, while the user manual is procedural; combining them cannot establish that the proposed controls became production behavior. The admin EMS2 page refers to absent entitlement spreadsheets and change attachments, and the user manual depends on screenshots missing from this copy.

The guideline names an older React version without an effective date or supersession record, so it cannot establish the current platform baseline. Diagrams, emails, and example projects cited by the release and deployment guides are absent from the supplied set. The firewall register has no verified reachability, and no migration, proxy change, upload, deployment, or rollback was executed during ingestion. Named owners and effective approvals are not recorded, and the current runtime implementation is not confirmed.

## Open questions

- Which repository revisions implement the current container, tile, and routing interfaces?
- Which schema migration and catalog revisions are deployed in the current environment?
- Which development guidelines and shared dependency versions are currently accepted?
- Which owner controls compatibility changes across shared modules and tenant applications?
- Which dependency exceptions have platform review, accountable tenant ownership, and effective dates?
- Which standalone template and shared-component versions remain supported?
- Which cross-tenant write and verification permissions apply to makers and checkers? Portal administrators may read audit history and configuration across tenants. A tile must never reference another tile's metadata. [Admin access criteria](../../../candidates/operations/KT-admin-and-onboarding.md#portal-administrator-reads-and-tile-metadata-references)
- Which release, approval, rollback, and emergency-change controls govern self-service catalog changes in production?
- Which checklist governs each environment, and what replaces FMAA authentication after the planned decommissioning?
- Which evidence proves technical readiness and business activation separately for each tenant request?
- Which SSDR entitlement option and multiple-entity matching rule apply to the current tenant configuration?

## Related pages

- [[concepts/microfrontend-layering]]
- [[concepts/admin-catalog-configuration]]
- [[concepts/configuration-promotion]]
- [[concepts/maker-checker-verification-workflow]]
- [[concepts/ems2-entitlement-provisioning]]
- [[concepts/application-ownership]]
- [[concepts/shared-dependency-governance]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/portal-ingress-path]]
- [[concepts/release-window-governance]]
- [[concepts/tenant-production-readiness]]
- [[entities/mfe-root-config]]
- [[entities/mfe-base]]
- [[entities/single-ui-bff]]
- [[entities/ems2]]
- [[entities/fmaa]]
- [[entities/flyway]]
- [[entities/markets-operations-one-release]]
- [[entities/fmo-post-trade-portal]]
- [[summaries/KT-frontend-composition]]
- [[summaries/KT-admin-and-onboarding]]
- [[summaries/KT-release-operations]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-architecture-evolution]]
