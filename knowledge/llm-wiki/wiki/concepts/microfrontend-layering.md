---
type: "Concept"
sources: ["summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
description: "The portal's four-tier frontend composition model and how tiers load and share code."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical basis: [four-layer clarification](../../../candidates/architecture/KT-frontend-composition.md#current-four-layer-clarification).

# Microfrontend Layering

Microfrontend layering is the portal's four-tier frontend composition model. Each tier owns a distinct responsibility and is composed at runtime rather than at build time. The layering separates static entry delivery, shell concerns, application routing, and feature rendering so that each tier can evolve independently. In the portal capability map, this layering is the composition mechanism that lets tenant applications share a common entry point and workspace while retaining their own domain functions, as summarized in [[summaries/KT-portal-purpose]].

Source basis: the candidate architecture record [[summaries/ARC-portal-service-relationships]], which captures a user-reported clarification of 22 October 2026 plus bounded source review; the documented composition topic [[summaries/KT-frontend-composition]]; the portal-purpose synthesis [[summaries/KT-portal-purpose]]; and the evolution-and-proposal topic [[summaries/KT-architecture-evolution]], which supplies the build-tool, component-library, notification, and platform-proposal material referenced below. The portal-purpose topic adds business framing and a working vocabulary—tenant application, tile, workspace, container, and import map—but also carries draft principles and 2026–2027 proposals. Treat its forward-looking items as intent, not as layer facts. The architecture record and composition topic describe the same model, but they do not use identical layer names.

## The four layers

| Order | Layer | Repository | Responsibility |
| --- | --- | --- | --- |
| 1 | Base / root configuration | [[entities/mfe-root-config]] | Serve HTML and static entry resources. Initialize Single-SPA and register only the shell. Hold the import map that connects module names to deployed files. |
| 2 | Shell | [[entities/mfe-base]] | Supply themes, login, logout, sessions, tiles, drawers, and remote container loading. |
| 3 | Container | [[entities/mfe-ratan-container]] | Supply application routing, shared components, utilities, and related services. |
| 4 | Tile | [[entities/mfe-cashflow-blotter]] (example) | Render feature views and application functionality. |

The root layout declares only `@fm/base`, so the base tier deliberately knows nothing about containers or tiles. Registering a single child keeps the composition boundary narrow.

Terminology differs between the sources. [[summaries/KT-frontend-composition]] names the layers Root Config, Base shell, application container, and feature tile, and its role table assigns common routing, global state, and theme context to a "base container". The reconciled reading is that the root configuration registers only the shell, and the shell carries shared presentation context. The exact split of routing responsibility between the shell and the application container is not confirmed by inspected declarations. The portal-purpose topic uses container for both the shared base and application-owned modules; the role must therefore be stated explicitly whenever an interface is described.

### Where layering sits in the portal capability map

The portal-purpose topic describes the composition boundary in business terms: the platform supplies common entry, composition, access, administration, integration, observation, and interoperability, while tenant applications keep domain functionality. The four tiers implement composition, tile and workspace structure, and dynamic module loading. Entry and identity, access, administration, observation, and interoperability cross the layers rather than belonging to a single tier. The portal-purpose materials describe these as documented capabilities, not confirmed deployed coverage, and mix present-tense descriptions with unfinished items such as FDC3.

## Loading and routing stages

Loading is staged, and each stage selects the next by props rather than by static imports:

1. [[entities/single-spa]] registers the shell; [[entities/systemjs]] resolves named modules and loads the corresponding files into the page through the import map.
2. The shell selects `props.container` and forwards `module`, `tile`, `parameters`, `panelId`, and `tabId`.
3. The container uses `props.module` to choose its route; a selected loader imports the tile and forwards props.
4. The tile uses `props.tile` for its feature route.

These are distinct routing and loading stages. A route decision at one tier is not the same as a module load at the next, so path configuration and bundle configuration must be reasoned about separately. [[entities/nginx]] routing of application static files and API requests is a further, transport-level concern and does not change the logical staging. The import map used here is the same mapping the portal-purpose topic defines for locating modules during dynamic loading.

Stage 1 is also the point where the layering constrains tooling. The build-tool research recorded in [[summaries/KT-architecture-evolution]] treats SystemJS compatibility as an architectural constraint of the platform boundary, not as a per-application preference. Its recommendations—[[entities/rspack]] for incremental migration from [[entities/webpack]] and [[entities/vite]] for new or simpler applications—are research statements tied to a proposed pilot that would check loading, HMR, and asset paths before any gradual rollout. The same report also sketches a longer-term move away from SystemJS, which would replace the module-resolution stage rather than substitute a bundler inside it. Both proposals are unverified and undated; nothing here establishes that either was adopted, so the four-tier model should still be read as operating on the import-map mechanism described above. See [[concepts/build-tool-migration]].

## Shared code flows upward

Dependencies are not strictly one-directional for code reuse. Containers and tiles import shared libraries back from the shell and container tiers; the tile imports show reuse of container components. Layering therefore constrains *ownership and loading*, not every import edge.

Modules are shared through exports, imports, and registered names in the import map. Containers and tiles can therefore consume shell and container code without owning its release. The consequence is that shared dependencies require coordinated upgrades: a shared interface change can affect several tenant consumers. That inference needs exact provider and consumer evidence before any particular change is assessed, and the accepted versions are not confirmed. See [[concepts/shared-dependency-governance]].

The shell's shared theme is one instance of this pattern. Because presentation context is supplied once at the shell and consumed by every downstream tier, a change of component library or theme tokens is a layering-wide change rather than a local one. The component-library evaluation recorded in [[summaries/KT-architecture-evolution]] compares [[entities/mui]], [[entities/ant-design]], and [[entities/ag-grid]] on components, styling, and licensing, with some statistics dated July 2023, and its conceptual-design draft still contains placeholders and unresolved rationale. Those records explain the concerns behind the current baseline; they do not establish present library capability or an accepted decision, and they are not evidence for changing the shared theme boundary. See [[concepts/component-library-selection]].

Bundle shape is also qualified: the reported model describes JavaScript entry bundles, and lazy loading permits additional chunks beyond the declared entries.

## Ownership and onboarding

The documented design assigns shared backend availability and review of shared repositories to the microfrontend team. Each application team owns its domain backend availability, chooses its deployment approach, and supplies static-file and API URLs. The intended benefit is separate team delivery within one user workspace. The portal-purpose topic frames the same split as tenant applications retaining domain functions while the platform supplies shared integration capabilities. These are stated role declarations; current named owners and effective approvals are unknown. See [[concepts/application-ownership]].

The documented onboarding sequence condenses the [[concepts/frontend-onboarding]] flow:

1. Obtain root configuration and application templates.
2. Create separate application container and tile repositories.
3. Update module names, build configuration, imports, interfaces, and container entry points.
4. Update unit tests and the local import map.
5. Configure the tile through the Admin Module procedure.
6. Build and deploy the application files, then supply static-file and API URLs to the platform team.

Step 3 is where a layering decision becomes a per-application task. A bundler change, an import-map change, or a shared-library upgrade propagates through the module-name and build-configuration items for every application that follows the sequence, which is why those changes are governed at the platform level rather than per repository.

## Development conventions and standalone use

The documented guideline prescribes TypeScript, functional components, shared [[entities/mui]] themes, and separation of view, logic, styles, and interfaces. It names [[entities/react]] 18.2.0 and prefers Context and Reducer over additional state libraries. These versioned instructions must retain their source context before reuse; they do not establish the current platform baseline. The unchecked future-work list summarized in [[summaries/KT-architecture-evolution]] separately proposes a [[entities/spring-boot]] 4.0.6 upgrade and moving properties into services without recording completion, owners, or ordering, so it likewise cannot be read as a current version statement for the platform.

The onboarding procedure also suggests 500 KB files and six concurrent static-file requests as optional loading guidance. This is not an accepted performance SLA.

A standalone [[entities/react]] template reuses [[entities/mfe-base]] components through import-map registration. Its no-install statement concerns consuming those shared components only; the template still installs its own dependencies. This pattern describes shared-component reuse outside the documented container-and-tile startup example and does not show that every standalone application integrates without adaptation.

## Layering under per-tile behavior

Because tiles load and render independently, any cross-tile capability must be designed at a layer above them. The notification materials summarized in [[summaries/KT-architecture-evolution]] show the problem: many tiles opening separate subscription connections, with one server-sent-events connection per user proposed as a remedy. That proposal is a platform-level concern that the four loading tiers do not currently express—no tier in the table owns cross-tile event delivery. The store draft likewise considers tile reactions through React effects or registered callbacks, and it declares `isRead` as a string while assigning boolean `false` in its event handler. The field contract is unresolved.

The three notification experiments described—[[entities/graphql]] over SSE with a Node.js backend, [[entities/graphql]] over WebSocket with [[entities/spring-boot]], and SSE with a [[entities/spring-boot]] backend—are experiment locations and branch references, not evidence of a supported portal service. Nothing in the layering should be read as assuming one exists. See [[concepts/realtime-notification-delivery]].

## Relationship to the rest of the portal

- The layering sits behind the [[concepts/portal-ingress-path]] (DNS to [[entities/nginx]], then [[entities/api-gateway]]). The logical MFE-to-BFF contract is distinct from that transport path, and no effective deployment is confirmed.
- Backend calls from the layered frontend go to [[entities/single-ui-bff]] in the described portal scope, using the `Single-UI-Authorization` header with authentication, analytics, and SSE exceptions.
- Entry and tile-level access decisions are a separate concern described in [[concepts/portal-entry-and-tile-authorization]].
- Token validation on application backends is described in [[concepts/single-ui-sdk-authentication]] and [[summaries/KT-sdk-and-entitlements]].
- Authentication delegation sits outside the frontend layers and is described in [[concepts/identity-provider-delegation]].
- Direct external GUI dependencies are governed separately; platform review and an approved exception are required, with tenant teams retaining security, licensing, vulnerability, support, resilience, and rollback responsibilities.
- The layering is the composition substrate for the portal described in [[summaries/KT-portal-purpose]]. It supports the common entry, tile selection, multiple workspaces, and dynamic loading that the portal-purpose topic groups under composition. Tile-and-workspace behavior itself is described in [[concepts/portal-tile-workspace-model]].
- The portal-purpose topic lists entry and identity, access, administration, integration, observation, and interoperability as separate capability boundaries. They are not additional frontend tiers and should not be mapped one-to-one onto the four loading layers. Cross-application interaction, including [[entities/fdc3]], is an interoperability concern marked in progress in those materials.
- The 2026 and early 2027 deployment proposal summarized in [[summaries/KT-architecture-evolution]] names separate authentication, tile-management, telemetry, and AI services, but its current-architecture and target logical-architecture sections carry no explanatory content. Those names therefore do not define interfaces or a migration path for the layers, and they should not be mapped onto the four tiers.

## Qualifications and evidence limits

The responsibility model is user-reported and document-derived rather than extracted end to end. Inspected declarations cover the layout, root bootstrap, shell loader, container routing, tile loader, and shared tile imports, but four repositories have no independent Git history, so file hashes identify inspected files without an upstream commit. No live requests or browser behavior were tested.

The getting-started and standalone setup procedures depend on archives and screenshots that are absent from the supplied copies, so they cannot be reproduced completely. The development guideline names React 18.2.0 without an effective date or supersession record, and the framework comparison contains scores without retained project measurements. The build-tool report has no publication date and no retained benchmark inputs or execution records, so its ranking cannot predict results for these repositories. The portal-purpose topic also carries draft principles and a deployment proposal for 2026 and early 2027; those forward-looking items are not evidence of layer implementation or approved scope. The layering should therefore be treated as candidate architecture pending deployment and source-ownership confirmation.

## Related pages

- [[summaries/ARC-portal-service-relationships]] · [[summaries/KT-frontend-composition]] · [[summaries/KT-portal-purpose]] · [[summaries/KT-architecture-evolution]]
- [[entities/mfe-root-config]] · [[entities/mfe-base]] · [[entities/mfe-ratan-container]] · [[entities/mfe-cashflow-blotter]]
- [[entities/single-spa]] · [[entities/systemjs]] · [[entities/nginx]] · [[entities/fmo-post-trade-portal]]
- [[concepts/portal-ingress-path]] · [[concepts/portal-entry-and-tile-authorization]] · [[concepts/portal-tile-workspace-model]]
- [[concepts/application-ownership]] · [[concepts/frontend-onboarding]] · [[concepts/shared-dependency-governance]]
- [[concepts/build-tool-migration]] · [[concepts/component-library-selection]] · [[concepts/realtime-notification-delivery]]
- [[entities/react]] · [[entities/mui]] · [[entities/fdc3]] · [[entities/rspack]] · [[entities/vite]] · [[entities/webpack]] · [[entities/graphql]] · [[entities/spring-boot]]

See also: [[summaries/KT-application-interoperability]]

See also: [[summaries/KT-observability-and-performance]]

See also: [[summaries/KT-admin-and-onboarding]]

See also: [[summaries/KT-release-operations]]