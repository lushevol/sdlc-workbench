---
query: "What are the Portal frontend composition layers and ownership boundaries among root config, base, container, feature, module, and tile?"
---

## Short answer

The wiki does **not** describe six layers — it records a **four-layer** composition. "Feature" and "module" are *routing-stage and vocabulary terms*, not separate tiers.

> Source basis: [[concepts/microfrontend-layering]], [[summaries/ARC-portal-service-relationships]] (user clarification dated 22 Oct 2026), [[summaries/KT-frontend-composition]] (v3, candidate/draft).

## The four layers and their boundaries

| # | Layer | Repository | Owns |
|---|---|---|---|
| 1 | **Root config** | `mfe-root-config` | HTML document, static entry resources, the **import map** (module name → deployed file), Single-SPA bootstrap; registers **only** `@fm/base` |
| 2 | **Base / shell** | `mfe-base` | Themes + shared MUI context, common routing and global state, login/logout, sessions, tiles & drawers, remote container loading, shared request interceptor (`Single-UI-Authorization` / `Single-UI-Refresh`) |
| 3 | **Container** | `mfe-ratan-container` | Application routing, shared components, utilities, related services |
| 4 | **Tile** (a.k.a. *feature tile*) | e.g. `mfe-cashflow-blotter` | Feature views and application functionality |

The root layout declares only `@fm/base`, so the root tier deliberately knows nothing about containers or tiles — that narrow single-child registration *is* the composition boundary ([[entities/mfe-root-config]], [[entities/mfe-base]], [[entities/mfe-ratan-container]], [[entities/mfe-cashflow-blotter]]).

## Where "feature" and "module" fit

They name **stages in the loading chain**, not tiers:

- Shell selects `props.container` → forwards `module`, `tile`, `parameters`, `panelId`, `tabId`
- Container uses **`props.module`** to select *its* route; a loader then imports the tile
- Tile uses **`props.tile`** for its *feature* route

So "module" ≈ the container-level route/domain grouping, "feature" ≈ the tile-level view. The sources stress these are **distinct routing and loading stages** — a route decision at one tier is not the same as a module load at the next, so path config and bundle config must be reasoned about separately. Separately, "module" also appears in the import-map sense (shared platform modules vs. application-owned domain modules).

## Ownership boundaries

- **Microfrontend team ([[entities/portal-team]])**: shared backend availability, review/approval of shared repositories, root configuration and import map, base/shell interfaces.
- **Application teams**: domain backend availability, their own deployment approach, their own **container and tile repositories**, and supplying static-file and API URLs to the platform team.
- **Tile metadata** is owned via admin catalog configuration (Admin Module), not shell source code — historically each tile update required a `mfe-base` source change plus a production CR.
- **External GUI dependencies**: platform review/approval required; tenant teams retain security, licensing, vulnerability, support, resilience, rollback.

Onboarding sequence (where the boundary becomes a per-team task): get root config + templates → create separate container and tile repos → update module names, build config, imports, interfaces, entry points → update tests + local import map → configure tile via Admin Module → build/deploy and hand URLs to the platform team ([[concepts/frontend-onboarding]]).

## What the four tiers do *not* own

Cross-cutting capabilities — entry/identity, access, administration, observation, interoperability — **cross** the layers rather than belonging to one, and must not be mapped one-to-one onto the tiers. Notably, **no tier owns cross-tile event delivery** (the notification/SSE case). CES migration also cuts across: `mfe-base` and the Ratan container share the frontend compatibility scope from 6 Nov 2026, and because each tile selects its own entitlement provider, **container routing must not assume a single provider** ([[concepts/per-tile-provider-selection]]).

## Caveats the wiki flags

- Naming differs between sources: KT-frontend-composition says "Root Config, Base shell, application container, feature tile" and assigns routing/global state/theme to a **"base container"**. The reconciled reading is root registers only the shell, and the shell carries shared presentation context — but **the exact split of routing responsibility between shell and container is unconfirmed**. "Container" is used ambiguously for both the shared base and application-owned modules, so state the role explicitly whenever describing an interface.
- This is **candidate, user-reported architecture** (22 Oct 2026 clarification plus local file inspection), not verified deployment: no live requests or browser behavior tested, four repositories lack independent Git history, and **named owners and effective approvals are unknown**.
