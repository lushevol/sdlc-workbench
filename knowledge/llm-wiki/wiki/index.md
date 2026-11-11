# Knowledge Base Index

This wiki and its saved explorations are derived from candidate/draft Workbench records. Their source authority remains unconfirmed, and compilation does not publish knowledge or establish implemented behavior or business acceptance. Reopen the canonical records and their evidence before using a claim for an engineering decision.

Exact canonical paths, record versions, lifecycle states, and SHA-256 source bindings are recorded in [source-manifest.json](../source-manifest.json). The `sources/` entries link to those canonical records; changes to compiled pages do not promote the records.

## Documents
- [[summaries/KT-ces-migration-parity]] (short) — Defines intended EMS2-to-CES permission parity, per-tile migration, and frontend compatibility rules.
- [[summaries/KT-authentication-and-sessions]] (short) — Maps portal authentication, session renewal intent, Entra SSO migration, and open policy gaps.
- [[summaries/REQ-active-session-renewal]] (short) — Candidate requirement for renewable portal sessions via activity, plus expiry-prompt recovery criteria.
- [[summaries/KT-release-operations]] (short) — Portal and tenant teams coordinate release planning, configuration promotion, and readiness.
- [[summaries/KT-admin-and-onboarding]] (short) — Links onboarding, admin catalog setup, EMS2 roles, and maker-checker review.
- [[summaries/KT-observability-and-performance]] (short) — Connects analytics, performance tests, throughput, and cache design; flags unverified capacity.
- [[summaries/KT-application-interoperability]] (short) — Portal interoperability via FDC3/OpenFin: caller-provider duties and evidence limits.
- [[summaries/KT-architecture-evolution]] (short) — Maps historical UI evaluations, experiments, and platform proposals with unresolved decisions.
- [[summaries/KT-portal-purpose]] (short) — Summarizes the post-trade portal's purpose, shared capabilities, and draft or proposed scope.
- [[summaries/KT-frontend-composition]] (short) — Documents a four-layer microfrontend model, ownership rules, and onboarding flow.
- [[summaries/ARC-portal-service-relationships]] (short) — Maps the four-layer portal MFE stack, ingress, BFF, SDK, and RATAN auth responsibilities with evidence limits.
- [[summaries/KT-sdk-and-entitlements]] (short) — SDK integration, entitlement retrieval, CES migration, and portal entry rules.

## Concepts
- [[concepts/release-window-governance]] — Candidate release-window scheduling and responsibilities, preserving unresolved duration and urgent-release confirmation rules.
- [[concepts/ces-role-multiplicity]] — CES assignments can hold multiple roles, which cannot be collapsed into one scalar role for legacy callers.
- [[concepts/permission-check-provider-union]] — Existing hasPermission(code) calls accept a mapped grant from either EMS2 or CES, with the provider logged.
- [[concepts/per-tile-provider-selection]] — Each portal tile selects EMS2 or CES entitlement admission independently, without forcing other tiles to migrate.
- [[concepts/ems2-to-ces-permission-mapping]] — How EMS2 roles, entities, subjects, and actions map to CES entitlements, applications, features, and actions with parity rules.
- [[concepts/identity-profile-attribute-migration]] — Risk that user profile attribute values change between identity providers during SSO migration, affecting downstream logic.
- [[concepts/machine-to-machine-authentication]] — How non-human callers authenticate via client credentials, service accounts, and bank IDs, distinct from UI SSO.
- [[concepts/token-lifecycle-and-timeout-policy]] — Access, refresh, and idle/absolute token timeout concepts plus the unresolved portal timing rules.
- [[concepts/session-expiry-prompt-recovery]] — How the expiry prompt behaves across pending, success, and rejection renewal states.
- [[concepts/session-activity-renewal]] — Session lifetime extended by mouse, keyboard, and scroll activity instead of a fixed elapsed-time reauthentication maximum.
- [[concepts/tenant-production-readiness]] — Separating technical deployment evidence from business activation before a tenant goes live.
- [[concepts/configuration-promotion]] — Moving Portal catalog and tile configuration from Development to UAT and Production.
- [[concepts/ems2-entitlement-provisioning]] — How EMS2 creates and assigns entity, action, role, and subject records, and how they map to CES.
- [[concepts/maker-checker-verification-workflow]] — Two-person review that verifies an un-verified admin record before activation.
- [[concepts/admin-catalog-configuration]] — Portal admin functions that maintain module mappings, drawer categories, and tiles as versioned configuration
- [[concepts/mfe-cache-strategy]] — Revalidate layer entry files and long-cache hashed assets to speed loads, but updates still need a refresh.
- [[concepts/frontend-performance]] — How frontend performance targets, throughput results, and cache behavior are evidenced before capacity claims.
- [[concepts/interaction-analytics]] — Event taxonomy and identity model for capturing Portal user interactions in analytics.
- [[concepts/cross-application-authentication-handoff]] — Passing an authenticated identity from one application to another so users avoid repeated logins.
- [[concepts/interoperability-contract-governance]] — How intent names, context schemas, versions, and readiness gates are agreed and verified across caller and provider teams.
- [[concepts/intent-based-application-interoperability]] — Portal-mediated sharing of context and intent requests between applications via FDC3 on OpenFin.
- [[concepts/component-library-selection]] — Evaluating and choosing a shared UI component library for the portal's microfrontends.
- [[concepts/realtime-notification-delivery]] — Proposed single-connection-per-user delivery of notifications across portal tiles, still experimental.
- [[concepts/build-tool-migration]] — Proposed migration of portal React builds from Webpack to Rspack or Vite, constrained by SystemJS loading.
- [[concepts/portal-tile-workspace-model]] — Portal tile/workspace model with intent-mediated navigation and context handoff.
- [[concepts/application-ownership]] — How platform and tenant teams divide delivery, catalog, and release accountability.
- [[concepts/shared-dependency-governance]] — Rules and practices controlling shared code, library versions, and module interfaces across teams.
- [[concepts/frontend-onboarding]] — How an application team registers containers and tiles and proves release readiness.
- [[concepts/identity-provider-delegation]] — How the portal defers authentication to external identity providers and authorization to EMS2/EMS3, and what remains unproven.
- [[concepts/portal-ingress-path]] — The reported DNS-to-Nginx-to-API-gateway-to-BFF route serving the post-trade portal.
- [[concepts/microfrontend-layering]] — The portal's four-tier frontend composition model and how tiers load and share code.
- [[concepts/portal-entry-and-tile-authorization]] — Two-layer portal access model: portal entry plus per-tile admission by EMS2 or CES provider.
- [[concepts/entitlement-retrieval]] — How downstream services obtain a user's entitlements from EMS2 or CES, including provider-union checks and entity fields.
- [[concepts/single-ui-sdk-authentication]] — How the Single UI SDK validates portal JWTs and exposes authenticated user context to downstream services.

## Entities
- [[entities/ratan]] (organization) — Legacy team and shared container whose EMS2 entity X_RATANONE maps to CES application RATAN_ENTITLEMENT_RULE (itam_id 51358).
- [[entities/ddr]] (product) — FSSDS Data Distribution and Reporting product requested for Portal integration to show downstream report distribution.
- [[entities/vpa]] (product) — Post-trade product whose Fix Link and Trade Monitor tiles were requested for Portal release.
- [[entities/cdups]] (product) — Confirmation-management product whose Portal tile was requested via a Markets Operations One change request.
- [[entities/fss]] (organization) — Tenant organization requesting multiple Portal tiles, including gating, SSI, custody, and collateral capabilities.
- [[entities/fmaa]] (product) — Authentication component issuing client-credential tokens for portal admin uploads and machine-to-machine callers.
- [[entities/entra]] (product) — Microsoft identity platform replacing Portal SSO; migration scope and activation rules remain unapproved.
- [[entities/admin-module]] (product) — Portal product where tenant catalog configuration (module map, drawer, tile) is uploaded and promoted across environments.
- [[entities/markets-operations-one-release]] (event) — Release program governing Portal and tenant release windows, scope, and readiness gating.
- [[entities/flyway]] (product) — Database migration tool whose retained SQL defines the portal admin catalog schema draft.
- [[entities/apache-jmeter]] (product) — Open-source load testing tool referenced as the execution vehicle for Portal throughput tests.
- [[entities/kibana]] (product) — Kibana is the dashboard tool documented for Portal interaction analytics and usage monitoring.
- [[entities/openfin]] (product) — Desktop runtime and platform product referenced in Portal materials for application hosting and onboarding phases.
- [[entities/spring-boot]] (product) — Java backend framework used in portal notification experiments and a proposed version upgrade.
- [[entities/graphql]] (product) — A query language used in portal notification experiments over SSE and WebSocket.
- [[entities/webpack]] (product) — JavaScript module bundler named as the incumbent tool in the portal's build-tool migration research.
- [[entities/vite]] (product) — Frontend build tool recommended in the portal's build-tool research for new or simpler applications.
- [[entities/rspack]] (product) — Rust-based JavaScript bundler recommended for incremental migration from Webpack in the portal.
- [[entities/ag-grid]] (product) — Data-grid product evaluated in a 2023 UI library comparison against MUI and Ant Design.
- [[entities/ant-design]] (product) — A React component library evaluated alongside MUI and AG Grid in the TPT UI library comparison.
- [[entities/fdc3]] (product) — Cross-application interoperability standard used with OpenFin in the FMO Post Trade Portal.
- [[entities/mui]] (product) — React component library evaluated for shared theming in the portal.
- [[entities/react]] (product) — JavaScript UI library used across the portal's microfrontend layers and standalone templates.
- [[entities/systemjs]] (product) — Module loader in the portal microfrontend design and a constraint on build-tool migration.
- [[entities/single-spa]] (product) — Single-SPA is the microfrontend orchestration framework that mounts the portal's registered shell.
- [[entities/ems3]] (product) — Entitlement provider reported in the portal and used as the CES wire value in the migration contract.
- [[entities/api-gateway]] (product) — Ingress product said to forward portal requests from Nginx to application services.
- [[entities/nginx]] (product) — Web server and reverse proxy at the portal ingress edge and tenant connectivity boundary.
- [[entities/ratan-auth-server]] (product) — Portal authentication and authorization service delegating identity checks to OUD, Entra and FMAA.
- [[entities/single-ui-bff]] (product) — Portal backend-for-frontend for auth, sessions, admin, entitlements, analytics, and CES metadata.
- [[entities/mfe-cashflow-blotter]] (product) — Feature tile microfrontend in the RATAN portal that renders cashflow blotter views.
- [[entities/mfe-ratan-container]] (product) — RATAN container microfrontend (mfe-ratan-container): the third portal layer, its routing, and migration duties
- [[entities/mfe-base]] (product) — MFE Base is the Single-SPA shell layer supplying themes, routing, sessions, and the shared permission and request APIs.
- [[entities/mfe-root-config]] (product) — First microfrontend layer: portal HTML entry, import map, and Single-SPA bootstrap.
- [[entities/portal-team]] (organization) — User-reported owner of portal entry, tile, and release rules for the Post Trade Portal
- [[entities/fmo-post-trade-portal]] (product) — SCB post-trade portal product: entry, tile authorization, microfrontend composition, admin, release, and session policy.
- [[entities/ces]] (product) — Successor entitlement service to EMS2, supplying CES roles and application identity to consumers.
- [[entities/ems2]] (product) — EMS2 is the legacy entitlement system defining portal application entities, roles, subjects, and actions.
- [[entities/single-ui-sdk]] (product) — Java library for validating portal JWTs and retrieving entitlements.

## Explorations
- [[explorations/how-should-the-portal-preserve-an-active-session-across-refr]] — Activity-driven renewal and retry behavior after rejected renewal, with candidate-status and timing-policy caveats.
- [[explorations/what-candidate-mapping-rules-map-ems2-roles-and-entitlements]] — Candidate EMS2-to-CES mapping rules, parity limits, and unresolved role/data-source gaps.
- [[explorations/what-are-the-portal-frontend-composition-layers-and-ownershi]] — Frontend layers, ownership boundaries, and deployment-evidence limits.
- [[explorations/which-responsibilities-belong-to-portal-and-tenant-teams-for]] — Draft Portal/tenant responsibilities for routing, release, validation, and rollback.
- [[explorations/what-candidate-interoperability-contract-and-openfin-fdc3-co]] — Candidate caller/provider contract and OpenFin/FDC3 readiness gaps.
- [[explorations/what-telemetry-and-performance-or-capacity-evidence-exists-f]] — Telemetry, performance, and capacity evidence versus proposals and missing execution records.
