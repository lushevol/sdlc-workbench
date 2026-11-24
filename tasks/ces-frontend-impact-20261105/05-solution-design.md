---
artifact_kind: system-design
id: CES-FRONTEND-SOLUTION-20261105
version: 1
status: draft
owner: unknown
source_refs: [USER-SOLUTION-001, BFF-001, BASE-001, CONTAINER-001]
related_ids: [CES-FRONTEND-IMPACT-20261105, CES-FRONTEND-CHANGE-20261105]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Flag-controlled transition and final CES design

> **Critical conclusions: Use one server-controlled mode and explicit scope for each mounted container.**
> Action: review the proposed contracts and snippets before implementation.
> Consequence: independent browser switches can disagree with server grants or mix application permissions.
> Owner: unknown; BFF and frontend maintainers. Evidence: [flag sources](#evidence-and-uncertainty) and [prior impact](05-impact-analysis.md).

## Scope and drivers

| Field | Value |
| --- | --- |
| Design state | Proposed; all snippets below are review examples. No application code was changed. |
| Problem and outcome | Support gradual tile migration and a final CES-only state through one mode control. |
| Included behavior | [User solution request](evidence/user-input-solution-20261105.md#exact-user-input); [required frontend changes](05-impact-analysis.md#proposed-change). |
| Exclusions | Implementation, deployment, and invented role or sharing policy. |
| Constraints | Preserve application isolation, existing server authorization, and meaningful rollback during transition. |
| Current revision | BFF `267081800cc28b6af0f8e080fa67c2d5f14d3a26`; Base `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`; container filesystem hashes. |

### Stage readiness and preserved baseline

The [latest request](evidence/user-input-solution-20261105.md#exact-user-input) authorizes design and snippets, without application implementation.
Readiness: `READY` for design comparison and critical snippet review only.
Assessor: agent:codex, 5 November 2026, Asia/Singapore.
Missing role policy and app identity affect implementation choices, but do not prevent this conditional proposal.
Implementation readiness and business acceptance remain unassessed.

The [completed intake](01-intake.md) remains unchanged from Workbench commit `ec5608d2e74006e8ffc0fa58e6c2a8650b2db23b`.
Its recorded hash remains in the [original manifest](evidence/source-manifest.json).
This document is the current stage record for the design extension.
The request changes no domain permission meaning; no knowledge publication or role-policy approval follows.

### One mode flag, three states

Reuse the BFF's existing `scb.authorization.migration.mode` as the rollout control.
Do not introduce independent per-frontend switches for authorization source selection.

| Period | Mode value | Tile behavior | Recovery boundary |
| --- | --- | --- | --- |
| Legacy or transition rollback | `EMS2_ONLY` | Resolve all tiles through EMS2. Return effective EMS2 scopes. | Requires retained valid legacy configuration and working EMS2 services. |
| Transition | `EMS3_PRIMARY_DUAL_READ` | Resolve legacy tiles through EMS2 and migrated tiles through CES. | An unavailable CES tile stays unavailable; other legacy tiles can remain usable. |
| Final | `EMS3_ONLY` | Resolve CES scopes only. Intended final tiles must all be migrated. | No EMS2 reads or fallback. Use CES-compatible correction or recovery. |

The transition name is existing backend terminology.
It does not mean that both providers grant every tile, or that CES failure selects EMS2 for that tile.
Sources: [mode enum](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/config/AuthorizationMigrationMode.java#L3) and [routing](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L43).

Proposed deployment configuration example:

```yaml
scb:
  authorization:
    migration:
      mode: EMS3_PRIMARY_DUAL_READ
```

Change the value to `EMS3_ONLY` for final cutover.
Existing [ConfigurationProperties](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/config/AuthorizationMigrationProperties.java#L9) do not establish live refresh.
Treat this as deployment/configuration controlled until the environment supplies an explicit refresh mechanism.
If a feature-flag service is adopted, evaluate it on the server before authorization assembly.
Keep the selected mode consistent throughout each authorization response.

Base's [existing flag helper](../../repos/ui/mfe-base/src/utils/featureFlagController.ts#L18) accepts query-string overrides.
Container flags [cache by feature name](../../repos/ui/mfe-ratan-container/src/packages/FeatureFlag/index.ts#L26), without user or authorization revision.
Neither mechanism should select the trusted authorization provider.
An optional UI rollout flag can hide new configuration controls, without changing authorization decisions.

## Components and boundaries

| Component ID | Resource kind | Responsibility | Owner | Source revision and locator |
| --- | --- | --- | --- | --- |
| BFF-001 | service | Select mode; authorize tiles; retain grant provenance before lossy projection. | unknown | Candidate above; [authorization assembly](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L43). |
| BASE-001 | frontend | Store one authorization snapshot; derive current tile scope; preserve permitted workspaces. | unknown | HEAD above; [Container](../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L26). |
| CONTAINER-001 | shared frontend | Evaluate scoped actions and preserve agreed profile-dependent behavior. | unknown | [Existing helper](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L6); filesystem hash. |

### Snippet 1 — Add an explicit response contract

The following types are proposed additions; these fields do not exist in the current BFF response.
Retain existing `entities`, `drawers`, tokens, and headers during transition for older consumers.

```ts
type Mode =
  | "EMS2_ONLY"
  | "EMS3_PRIMARY_DUAL_READ"
  | "EMS3_ONLY";

type AppKey = Readonly<{ id: string; name: string }>;
type Scope =
  | { source: "EMS2"; entityNames: readonly string[] }
  | { source: "EMS3"; applications: readonly AppKey[] };

type CesGrant = {
  application: AppKey;
  feature: string;
  actions: readonly string[];
};

type AuthorizationSnapshot = {
  schemaVersion: 1;
  revision: string; // changes for user, mode, scope or grant changes
  mode: Mode;
  cesGrants: readonly CesGrant[];
};

// Each protected BFF-authorized drawer tile gains this field:
// authorization: Scope
// The response also gains authorization: AuthorizationSnapshot.
```

`Scope.source` must describe the provider used for this response.
Do not copy the stored tile source without resolving the selected mode.
The stored `entitlementSource` remains `EMS3` during `EMS2_ONLY` rollback.

Emit CES grant application IDs before the current mapper or merge discards them.
Current [mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L72) and [merge key](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L197) cannot preserve same-name app IDs.
The browser cannot reconstruct that missing identity.
A frontend-only interim alternative requires an explicitly confirmed application-name uniqueness boundary.
That alternative is not equivalent to complete app-ID isolation.

## Relationships and interfaces

| Consumer ID | Provider ID | Contract ID | Relationship state | Evidence and limits |
| --- | --- | --- | --- | --- |
| Base | BFF | Existing login and validation response | Statically evidenced | Existing [handlers](../../repos/ui/mfe-base/src/utils/login.ts#L65). |
| Base | BFF | Snapshot and effective tile scope above | Proposed | New additive metadata; requires provider changes. |
| Container | Base | Per-mounted-container authorization context | Proposed | Existing [props](../../repos/ui/mfe-ratan-container/src/Root/routing/common/interface.ts#L1) lack this scope. |
| Downstream UI | Container | Scoped permission client | Proposed | Existing helper consumers require adaptation or an explicit bound client. |

### Snippet 2 — Base uses current authorized membership

Use one decision for drawer launches, restored workspaces, and URL launches.
Resolve the target against the latest server drawer, never saved permission metadata.

```ts
type TileRef = {
  container: string;
  module: string;
  tile: string;
};
type AuthorizedTile = TileRef & { authorization?: Scope };
type Drawer = { tiles: readonly AuthorizedTile[] };

function currentAuthorizedTile(
  drawers: readonly Drawer[],
  target: TileRef
): AuthorizedTile | undefined {
  return drawers.flatMap(drawer => drawer.tiles).find(tile =>
    tile.container === target.container &&
    tile.module === target.module &&
    tile.tile === target.tile
  );
}
```

This design trusts the BFF's granted drawer membership.
It removes the second legacy subject check for authorized targets.
It does not grant a tile that the server omitted.
Existing template exceptions remain server-controlled; do not infer new exemptions from a client flag.
An unprotected template can remain in the authorized drawer without an action scope.
A protected tile requires scope during response validation.
A template needs an explicit current authorization scope when it exposes protected actions.
The permission client denies protected actions when scope is absent.

Store response authorization, entities, drawers, and derived user metadata in one reducer update.
An explicit `drawers: []` replaces old drawers; an omitted field is a different response contract.
The current [handler](../../repos/ui/mfe-base/src/utils/login.ts#L98) ignores empty arrays.
Only entitlement-bearing responses should replace the snapshot.
Token refresh responses without authorization data must preserve its current binding.
Validate response schema and identity before installing it.
Bind each entitlement request to the current session epoch and a monotonically increasing request generation.
Install only the latest generation for that epoch; an opaque revision cannot order delayed responses.
Invalidate authorization clients immediately on logout, before outstanding requests can complete.

Proposed mounting sketch, inside the existing Base Container boundary:

```tsx
const tile = currentAuthorizedTile(snapshot.drawers, target);
if (!tile) return null; // show the existing unavailable-page treatment

return (
  <MountedContainer
    {...existingProps}
    authorizationScope={tile.authorization}
    authorizationRevision={snapshot.auth.revision}
  />
);
```

This JSX is an integration sketch; `snapshot`, `target`, and `MountedContainer` need their existing component bindings.
The container's [routing layer](../../repos/ui/mfe-ratan-container/src/Root/routing/index.tsx#L13) already spreads received props.
Pass scope into a provider or a bound client for each mounted subtree.
Do not use a mutable global current application; several panels can coexist.
If a snapshot changes, reconcile every mounted target with the new drawers.
Refresh bound clients and derived caches for the new revision.
Do not remount every panel solely because its authorization revision changed.
That can discard valid unsaved work without a permission change.
Unmount or apply the existing unavailable treatment only for revoked targets.

## Request and failure paths

| Path | Ordered actions | Observable result | Requirement or unresolved question |
| --- | --- | --- | --- |
| Permitted legacy tile | Server selects effective EMS2; Base resolves current membership; container uses scoped legacy grants. | Existing legacy action semantics remain. | Preserve [prior behavior](evidence/mfe-ratan-container-analysis.md#rc-01-resolve-permissions-by-application-feature-and-action). |
| Permitted CES tile | Server selects CES; Base passes permitted application set; container selects exact application, feature, and action. | Only the requested scoped action is enabled. | [FE-03](05-impact-analysis.md#fe-03), [FE-04](05-impact-analysis.md#fe-04). |
| Denied CES action | Resolve CES scope; no matching grant. | False; no legacy retry. | Proposed source-isolation control. |
| CES dependency failure | BFF returns denied or unavailable CES scope, according to its contract. | Legacy tiles may remain usable during transition; no extra CES grant appears. | Existing BFF failure routing. |
| Missing or incompatible metadata | Validate response before installation. | Compatibility error or unavailable affected scope; no silent legacy downgrade after activation. | Proposed protocol control. |
| Final CES state | Reject legacy scopes and use CES grants only. | No legacy adapter invocation. | Final migration intent. |

### Snippet 3 — Bind permission lookup to one tile

`LegacyCheck` is the existing EMS2 algorithm extracted over explicit source-filtered inputs.
It must not read mixed grants or a mutable active-workspace global.
The implementation below keeps CES denial separate from legacy routing.

```ts
type LegacyCheck = (
  entityNames: readonly string[], feature: string, action: string
) => boolean;

function bindPermissions(
  auth: AuthorizationSnapshot,
  scope: Scope | undefined,
  scopeRevision: string,
  legacyCheck: LegacyCheck,
  isCurrent: (revision: string) => boolean
) {
  return (application: AppKey, feature: string, action: string): boolean => {
    if (scopeRevision !== auth.revision || !isCurrent(auth.revision)) return false;
    if (!scope || !feature || !action) return false;
    if (auth.mode === "EMS3_ONLY" && scope.source !== "EMS3") return false;
    if (auth.mode === "EMS2_ONLY" && scope.source !== "EMS2") return false;

    if (scope.source === "EMS2") {
      return legacyCheck(scope.entityNames, feature, action);
    }

    const inTileScope = scope.applications.some(app =>
      app.id === application.id && app.name === application.name
    );
    return inTileScope && auth.cesGrants.some(grant =>
      grant.application.id === application.id &&
      grant.application.name === application.name &&
      grant.feature === feature &&
      grant.actions.includes(action)
    );
  };
}
```

Create this client from the same current snapshot that supplied the tile scope.
Base supplies `isCurrent` from the current authorization store, including its user binding.
`scopeRevision` comes from the mounted tile context; delayed callbacks must pass both revision guards.
The `application` argument must identify the action's explicit application from the permitted tile scope.
Multi-application tiles must not select the first name or search all user applications implicitly.
The legacy branch uses its explicit entity scope; it does not use the CES application argument.
A React hook can supply the legacy or CES facade for each component.
Non-React utilities need the bound client passed explicitly.

Multiple rows for the same CES application remain searchable through `some`.
No destructive entity-name map is needed.
Feature and action matching remains exact in this action helper.
BFF tile feature matching has its own existing case-insensitive rule.
Do not broaden action matching without a sourced rule.

### Snippet 4 — Resolve roles separately from action grants

Do not interpret an absent role as permission to bypass `PSS_RO` restrictions.
The following is a proposed conservative engineering default pending policy review.
It affects only an operation whose role restriction cannot be resolved.

```ts
type RestrictionDecision = "ALLOW" | "DENY" | "UNKNOWN";

function canCloseClientData(
  hasAction: boolean,
  restriction: RestrictionDecision
): boolean {
  return hasAction && restriction === "ALLOW";
}
```

The restriction decision requires an approved profile or capability mapping.
It must not come from the application name or an aggregated CES action list alone.
Sharing identity is a separate concern from this restricted-action decision.
Filters and views persist `assignee` and `moduleOwner`; preserve or migrate those identities explicitly.
Sources: [view ownership](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L22), [filter ownership](../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/common/useFieldNameController.ts#L28), and [read-only restriction](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L283).

A trusted temporary role mapping can support transition if its authority and source are documented.
Final CES operation must obtain equivalent sharing identities without runtime EMS2 lookup.
Do not use a CES data-profile name as a sharing role without an explicit mapping decision.

## Data and quality controls

| Concern | Proposed control | Target and conditions | Verification evidence |
| --- | --- | --- | --- |
| Grant scope | Match source, application ID/name, feature, and action. | No legacy fallback after CES denial. | Planned assertions below; new implementation NOT_RUN. |
| Session state | Replace authorization state atomically and rebuild derived clients on revision changes. | No cross-user, stale-snapshot, or cross-panel grants. | Planned assertions below. |
| User continuity | Retain unchanged workspaces and unsaved state during successful revalidation. | Revoke only unavailable targets. | Existing workspace preservation evidence is separate; new design NOT_RUN. |
| Performance | Reuse grants from the authenticated BFF snapshot. | No per-control CES network request. Numeric latency target unknown. | Measurement NOT_RUN. |
| Operations | Mode selected server-side; reconcile sessions through an entitlement-bearing response. | Switch timing depends on deployment or an explicit refresh lifecycle. | Operational mechanism remains unverified. |

### Configuration and final cleanup

For administration, send the four fields explicitly and preserve audit and checker payloads.
Example values below are illustrative; they are not approved deployment mappings.

```ts
const tilePatch = {
  entitlementSource: "EMS3",
  entitlementAppId: selectedApplicationId,
  entitlementAppName: selectedApplicationName,
  entitlementAppFeature: selectedFeatureNames.join(","),
};
```

The global mode is the rollout control; stored per-tile source selects the transition route.
FMO administrative role migration remains lower priority under the [recorded exception](../../knowledge/evidence/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input).
It still requires explicit backend maker/checker support before CES-only administration.

At final cutover, set `EMS3_ONLY` and confirm all intended business tiles use CES configuration.
The same scoped CES client remains; no second frontend entitlement rewrite is required.
After the agreed recovery window, remove the legacy adapter, legacy flag paths, and obsolete configuration.
Keep legacy source representations only where a supported contract still consumes them.
The final target must not depend on runtime EMS2 role enrichment.
The UI flag alone cannot establish zero EMS2 traffic across Auth, SDKs, caches, or downstream services.

## Decisions and verification

These are proposed design assertions, not approved business acceptance criteria or retained execution results.
The [existing canonical probe cases](06-test-cases.md) describe old helper observations, not this design's verification.
Define implementation cases in that same catalog before executable verification.

| Design decision | Planned explicit assertion | Current evidence | Result |
| --- | --- | --- | --- |
| Server-owned mode | URL query changes cannot select another provider. | Existing Base flag permits overrides; design separates authority. | New design NOT_RUN. |
| Transition per-tile routing | An EMS2 scope invokes only the legacy adapter; an EMS3 scope invokes only CES. | Current BFF routing inspected. | New design NOT_RUN. |
| CES denial | Missing action returns false and legacy invocation count equals zero. | Existing diagnostic masking case motivates separation. | New design NOT_RUN. |
| Application isolation | Same feature/action in another app ID or name returns false. | Existing payload omits IDs. | Provider extension required. |
| Mixed panels | One legacy and one CES panel keep their own scopes after tab selection changes. | Current props lack scope. | New design NOT_RUN. |
| Snapshot changes | Older request generations cannot replace current state; revoked targets disappear; unchanged targets retain state; logout invalidates clients. | Existing Base gaps inspected. | New design NOT_RUN. |
| Final mode | EMS2 scope returns false; legacy adapter and EMS2 network invocation counts equal zero within declared scope. | Existing BFF mode supports CES routing. | End-to-end evidence absent. |
| Role restrictions | UNKNOWN never enables the affected restricted action. | Current `undefined !== PSS_RO` concern. | Policy review required. |
| Configuration | Create/edit/checker/audit preserve all four fields; omitted source never silently changes provider. | Existing DTO defaults source to EMS2. | New design NOT_RUN. |

Readiness: proposed design review is complete within source limits.
Implementation prerequisites: explicit provider metadata, role/sharing policy, compatible bundle rollout, and snapshot-refresh behavior.
Alternative: a frontend-only name-scoped adapter can reduce provider edits where application-name uniqueness is explicitly established.
Its identity limit must remain visible; do not present it as the full app-ID-safe design.
No new dependency, feature-flag package, or external service is required by this proposal.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| USER-SOLUTION-001 | [Exact solution request](evidence/user-input-solution-20261105.md#exact-user-input) | 2026-11-05 | [Solution manifest](evidence/solution-source-manifest.json) | User; design only, no implementation. |
| BFF-001 | [Mode routing](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L43) | `267081800cc28b6af0f8e080fa67c2d5f14d3a26` | [Original manifest](evidence/source-manifest.json) | Owner unknown; static current source. |
| BASE-001 | [Flag helper](../../repos/ui/mfe-base/src/utils/featureFlagController.ts#L18) and [mount boundary](../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L26) | `66c6411ade58e4d134e381c2baee8ad3f76a8dbf` | [Solution manifest](evidence/solution-source-manifest.json) | Owner unknown; static source, local edits preserved. |
| CONTAINER-001 | [Flag helper](../../repos/ui/mfe-ratan-container/src/packages/FeatureFlag/index.ts#L26) and [routing](../../repos/ui/mfe-ratan-container/src/Root/routing/index.tsx#L13) | Filesystem copy | [Solution manifest](evidence/solution-source-manifest.json) | Owner unknown; no deployment identity. |

Facts: the BFF already exposes three internal modes, but does not emit the proposed snapshot or scope contract.
Facts: Base's existing feature-flag helper accepts browser query overrides.
Inferences: one resolved response and per-container clients can prevent provider disagreement and global scope leakage.
Unknowns: role policy, sharing migration, app-name uniqueness, release inventory, and live flag refresh.
Source confidence is high; proposed snippets are not validated application behavior.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SOL-01 | Existing browser flag overrides | Browser state cannot be the trusted source route. | unknown | Reuse server mode and emit it with grants. | Proposed |
| SOL-02 | Missing app IDs and effective scope | Frontend cannot preserve identity already lost upstream. | unknown | Add explicit metadata before merging, or confirm the interim uniqueness constraint. | Open |
| SOL-03 | Mixed mounted panels | Global active-app context can affect another panel. | unknown | Bind a client per subtree or pass context explicitly. | Proposed |
| SOL-04 | Role-dependent storage and restrictions | Missing role can change sharing or restricted controls. | unknown | Approve separate sharing and restriction mappings. | Open |
| SOL-05 | Configuration lacks a demonstrated refresh lifecycle | Switch may require deployment or authenticated snapshot refresh. | unknown | Define switch application timing and active-session reconciliation. | Open |

Document and snippet checks are retained in [solution validation](evidence/solution-validation.json).
They do not execute or approve the proposed business behavior.
