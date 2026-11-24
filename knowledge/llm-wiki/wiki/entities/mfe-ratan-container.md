---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "RATAN container microfrontend (mfe-ratan-container): the third portal layer, its routing, and migration duties"
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# RATAN Container

## What it is

The RATAN Container is the third layer of the portal's four-layer microfrontend hierarchy. Its repository is `mfe-ratan-container`. It sits between the shell ([[entities/mfe-base]]) and the feature tiles such as [[entities/mfe-cashflow-blotter]].

Within the portal, the container supplies application routing, shared components, utilities, and related services.

## Key facts from this document

### Position in the layering

| Order | Layer | Repository | Responsibility |
| --- | --- | --- | --- |
| 1 | Base | `mfe-root-config` | HTML and static entry resources; initializes Single-SPA and registers only MFE Base. |
| 2 | Shell | `mfe-base` | Themes, login, logout, sessions, tiles, drawers, remote container loading. |
| 3 | Container | `mfe-ratan-container` | Application routing, shared components, utilities, related services. |
| 4 | Tile | `mfe-cashflow-blotter` example | Feature views and application functionality. |

The base layer declares only `@fm/base`; it does not register the container directly. See [[concepts/microfrontend-layering]] and [[entities/mfe-root-config]].

### Loading and routing

- [[entities/single-spa]] registers the shell; SystemJS loads named modules.
- The shell selects `props.container` and forwards `module`, `tile`, `parameters`, `panelId`, and `tabId`.
- The container uses `props.module` to select its route (`src/Root/routing/common/useController.ts`).
- A selected loader imports the tile and forwards props to it (`src/Root/import/CashFlowCN.tsx`).
- The tile then uses `props.tile` for its own feature route.

These are distinct routing and loading stages, not one shared mechanism.

### Shared-code flow

Shared-code imports also flow in the reverse direction: containers and tiles import back to shell and container libraries. The tile import index (`src/Root/import/ratancomponents/index.ts`) shows reuse of container components. The user describes JavaScript entry bundles; lazy loading permits additional chunks.

## CES migration and provider compatibility

The CES migration contract applies to the shared Ratan container and its upper applications from 6 November 2026. See [[summaries/KT-ces-migration-parity]].

### Preserving upper-application APIs

The migration prioritizes compatibility with existing upper-application APIs in the container. Provider-specific identities and permission data are adapted internally so that established caller contracts are preserved where possible. Non-unique roles are the identified compatibility gap; this does not establish that every other container API is compatible. See [[concepts/ces-role-multiplicity]] and [[concepts/ems2-to-ces-permission-mapping]].

### Per-tile provider selection

Each tile admits through its own configured provider. An EMS2 tile keeps its existing admission logic; a CES tile uses CES admission logic, configured application identity, and CES permission structure. Moving one tile to CES must not force unrelated tiles to change provider, so container routing must not assume a single provider for all tiles. See [[concepts/per-tile-provider-selection]], [[entities/ems2]], and [[entities/ces]].

### Provider-union permission checks

Existing `hasPermission(code)` calls may accept a mapped grant from either EMS2 or CES. The check logs which provider supplied an accepted grant and requires no additional caller scope argument. This shared functional check is separate from tile admission. See [[concepts/permission-check-provider-union]].

### CES entity role and application fields

The BFF must expose two new CES fields on EMS3 entities passed through the container: `roleList` carries the application-scoped CES entitlement names, and `applicationId` carries the CES application `itam_id`. For the Ratan mapping, the existing `name` is `RATAN_ENTITLEMENT_RULE`, the existing `applicationName` remains the legacy team label `RATAN`, and the new `applicationId` is `"51358"`. See [[entities/ratan]].

These fields expose assignment names and application identity. They do not select a scalar role, and multiple entitlement names must not be represented as one proven assigned role.

### Role-owned writes stay pending

CES saved-view and filter writes that require one owner role remain unavailable until an ownership rule is agreed. No primary CES role may be selected and no comma-joined role names may be submitted as a scalar owner. Existing EMS2 role-owned write behavior is preserved.

## Boundaries and open points

The clarification identifies no effective deployment, complete consumer inventory, or authenticated architecture owner. The container is reported architecture; no runtime verification, browser behavior, or live request testing was executed.

For the migration scope, the evidence establishes user-stated intent only. It does not prove implemented, tested, or deployed container behavior, and it records no complete API compatibility mapping or agreed scalar role mapping.

## Related

- [[summaries/ARC-portal-service-relationships]]
- [[summaries/KT-ces-migration-parity]]
- [[entities/mfe-base]]
- [[entities/mfe-cashflow-blotter]]
- [[entities/ratan]]
- [[entities/single-spa]]
- [[entities/single-ui-bff]]
- [[concepts/microfrontend-layering]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/per-tile-provider-selection]]
- [[concepts/permission-check-provider-union]]
- [[concepts/ces-role-multiplicity]]
- [[concepts/ems2-to-ces-permission-mapping]]


See also: [[summaries/KT-frontend-composition]]
