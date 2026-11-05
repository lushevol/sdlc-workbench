---
artifact_kind: change-request
id: CES-FRONTEND-CHANGE-20261105
version: 1
status: draft
owner: unknown
source_refs: [USER-001, BFF-001, BASE-001, CONTAINER-001, INTENT-001]
related_ids: [CES-FRONTEND-IMPACT-20261105, CES-MIGRATION]
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

# Required frontend changes for the BFF CES migration

> **Critical conclusions: Update shell tile checks and shared application permissions before CES adoption.**
> Action: implement [FE-01](#fe-01) and [FE-04](#fe-04), then resolve [FE-05](#fe-05) role behavior.
> Consequence: controlled migrated payloads lose workspace access or valid action permissions.
> Owner: unknown; frontend and BFF maintainers. Evidence: [four helper observations](evidence/contract-probe-summary.json).

The BFF preserves the login response structure but changes its entitlement identities.
Required frontend work concerns authorization consumers, shared types, profile handling, and configuration surfaces.
The comparison does not establish a production failure or authorize application changes.

## Request and source facts

- Requester: user; identity unknown.
- Request source: [exact input](evidence/user-input.md#exact-user-input).
- Follow-up: [proposed code examples](evidence/user-input-snippets.md#exact-user-input); examples remain unapplied.
- Entry route: [existing implementation](../README.md#enter-with-existing-implementation).
- BFF comparison: local `main` `834b4155232222347220e47139a502ee43a9cbdf` to `267081800cc28b6af0f8e080fa67c2d5f14d3a26`.
- BFF candidate branch: `codex/apply-service-diffs-20261027`; latest commit dated 4 November 2026.
- Base source: `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`, plus preserved local Home controller edits.
- Base main: `f025513f696476a9cc8162681410cbd21e029bcb`.
- Container source: filesystem copy; no independent Git history. [Hashes](evidence/container-source-hashes.json) identify inspected bytes.
- Actual chronology: task registered 5 November 2026; previous implementation approval remains unknown.
- Supported rationale: [permission preservation and mapping intent](../../evidence/knowledge/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input).
- Evidence limit: local refs were not refreshed from a remote. Deployed builds and live CES behavior remain unknown.

## Stage boundary and readiness

| Stage | State | Basis and limit |
| --- | --- | --- |
| Source-based impact identification | READY; completed | Exact provider changes, frontend consumers, assertions, and helper results support the listed work. |
| Product implementation | Not assessed | Role/profile policy and complete application identity need resolution for affected changes. |
| Business verification and release | Not assessed | No candidate frontend change set, live contract, browser run, or deployment evidence. |

Assessor: agent:codex, 5 November 2026, Asia/Singapore.
The [intake](01-intake.md) was created and completed during this investigation.
No earlier frozen intake exists; its completed hash appears in the [manifest](evidence/source-manifest.json).
The first task commit supplies its Git identity.
Application files and unrelated local edits remain unchanged.

## Proposed change

These changes are recommendations. They have not been applied.

| ID and status | Repository and exact edit surface | Required change | Consequence and confidence | Owner |
| --- | --- | --- | --- | --- |
| [FE-01](#fe-01), required | Base [validateTile/validateWorkspace](../../repos/ui/mfe-base/src/utils/common.ts#L260), [deep links](../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L66) | Use the current BFF-authorized tile decision for restoration and deep links. Reject tiles absent from current drawers. | Legacy subjects can reject authorized CES pages. High; controlled helper observation. | unknown |
| [FE-02](#fe-02), required | Base [shared models](../../repos/ui/mfe-base/src/hooks/model/root.ts#L42), [profile](../../repos/ui/mfe-base/src/components/Profile/index.tsx#L109) | Add optional source markers and nullable legacy metadata. Use available stable keys and safe profile rendering. | CES leaves legacy IDs and role names null. High source confidence; presentation impact is limited. | unknown |
| [FE-03](#fe-03), required contract coordination | Base hooks and container [props](../../repos/ui/mfe-ratan-container/src/Root/routing/common/interface.ts#L1) | Expose the current tile's application scope and effective grant provenance through a shared contract. | An unscoped feature lookup can use the wrong application. High source confidence; implementation design remains proposed. | unknown |
| [FE-04](#fe-04), required | Container [getUser/hasPermission](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L6) | Resolve CES application → feature → action. Retain source identity; remove legacy masking and destructive overwriting. | Valid CES actions return false in controlled fixtures. High. | unknown |
| [FE-05](#fe-05), required where role consumers remain active | Container [role consumers](evidence/mfe-ratan-container-analysis.md#rc-03-resolve-role-dependent-filters-views-and-exception-gates) | Agree a role/profile or capability contract for filters, views, sharing, and `PSS_RO` restrictions. | CES grants do not provide the legacy role. High source confidence; exact replacement policy is unresolved. | unknown |
| [FE-06](#fe-06), conditional administration scope | Base [tile form](../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L232), [audit](../../repos/ui/mfe-base/src/admin/Tile/common/useAudit.tsx#L124) | Support and preserve all four entitlement fields across create, edit, checker, audit, and bulk configuration. | Existing UI cannot configure CES. Omitted source can select EMS2. High source confidence. | unknown |

### FE-01

The BFF grants CES tiles through configured feature matching before returning drawers.
It returns CES application names in `tile.entity`, while `tile.subject` still contains the legacy `ems2_subject`.
Base then repeats an entity/subject check during restoration and URL launch.
Sources: [drawer construction](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183) and [feature matching](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileFeatureMatcher.java#L13).

Use one shared tile-access decision based on current authorized drawer membership.
Do not substitute aggregate action grants for the BFF's per-tile decision.
Preserve rejection when the tile is absent, including permission revocation.
The [workspace caller](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L284) and deep-link caller must use the same rule.

The stored tile marker alone cannot identify the effective provider.
During `EMS2_ONLY` rollback, a stored `EMS3` tile can return legacy entities.
Use returned decisions consistently, or expose the effective provider explicitly.
See [mode handling](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L42).

Adjacent concern: [handleDrawers](../../repos/ui/mfe-base/src/utils/login.ts#L98) ignores `drawers: []`.
Clear explicit empty results before relying on current drawer membership.
Preserve state when a response omits drawers intentionally.
This concern predates CES; no deployed access bypass is established.
Owner: unknown. Next action: include empty-result replacement and omitted-field preservation assertions.

### FE-02

Add `entitlementSource?: "EMS2" | "EMS3"` to subjects and tiles.
Allow absent or null entity, subject, action, and role identifiers where the mapper leaves them unset.
The [CES mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L68) assigns names and action names, without legacy role metadata.

Adapt profile titles, keys, DOM IDs, and missing-map guards.
Do not invent numeric IDs or substitute an application name for a role.
The existing `appName:null` token key can still match serialized null roles.
A guaranteed profile crash is not established.
Owner: unknown. Next action: add roleless CES profile fixtures and retain legacy rendering coverage.

### FE-03

The container currently receives module and tile information, without a distinct entitlement application identifier.
A proposed shared context can carry current application names and effective subject source.
Derive it from current authorized data; do not trust URL-supplied scope.
Coordinate the exported Base contract and its container import.

The BFF response omits CES app IDs.
If different app IDs share a name, the frontend cannot reconstruct lost application identity.
Confirm name uniqueness or extend the BFF response before depending on name-only keys.
See [application identity limitation](evidence/bff-contract-analysis.md#conditional-application-identity-limitation).
Owner: unknown. Next action: select the minimum explicit context contract supported by the release inventory.

### FE-04

`getUser` collapses grants into maps keyed only by entity and subject names.
Repeated names overwrite earlier entries.
`hasPermission` returns from the first `X_RATANONE` match, even when a CES entity grants the action.
Its legacy fallback assumes the entity name contains the requested subject.

Use exact, scoped feature/action checks for CES subjects.
Select the effective provider for the current application before resolving grants.
Merge only equivalent source and application scopes; preserve multiple grants within that scope.
An unrestricted union across applications or providers can grant unsupported actions.

Keep the external helper API compatible where practical.
Verify consumers such as [view permission controls](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/ViewName.tsx#L43).
Changing only the `X_RATANONE` constant cannot handle arbitrary configured application names or mixed responses.
Owner: unknown. Next action: implement the scoped adapter and inspect affected consumers' allow and deny assertions.

### FE-05

The container reads roles from legacy user fields or `X_RATANONE.roleName`.
CES feature/action aggregation does not establish role attribution or a data profile.
User-confirmed name correspondence does not establish role equivalence.
See [original clarification](../ces-entitlement-migration-20261102/evidence/user-input-20261030-field-equivalence.txt).

Affected paths include [FilterSelector storage](../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/store.ts#L23), [ViewSelector storage](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L22), and exception close/replay gates.
A missing role satisfies `role !== "PSS_RO"` when an action check passes.
This predicts a UI restriction change, without proving server authorization bypass.

Decide whether to retain an explicit trusted profile or replace each role test with an approved capability rule.
Preserve saved ownership and sharing semantics through that decision.
Owner: unknown. Next action: obtain the BFF/Auth and application-owner contract before dependent implementation.

### FE-06

Use these exact wire fields:

| Field | Client handling |
| --- | --- |
| `entitlementSource` | Select EMS2 or CES in the UI; send `EMS2` or `EMS3` respectively. |
| `entitlementAppId` | One trimmed ID; maximum 64 characters; no comma. |
| `entitlementAppName` | English-comma list; normalized maximum 512 characters. |
| `entitlementAppFeature` | English-comma list; normalized maximum 512 characters. |

Require all three CES values for source `EMS3`.
Do not infer a required legacy entity from backend error wording.
See [actual validation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java#L22).

Current record cloning and request spreading can preserve returned fields during unrelated edits.
The failure is not inevitable for every existing edit.
However, a payload omitting source receives the DTO's `EMS2` default.
Send the source explicitly and test round trips.
See [request default](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L32).

CSV supports four entitlement headers together, or a legacy file without them.
Quote comma-separated lists. Partial entitlement headers fail validation.
See [CSV contract](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/CsvUtility.java#L93).

FMO Portal Admin remains lower priority under the [3 November clarification](../../evidence/knowledge/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input).
That source reports non-production, unlaunched, and unassigned status.
CES-only admin authorization also requires backend maker/checker role support.
This analysis does not establish an admin production blocker.
Owner: unknown. Next action: schedule configuration UI work when that interface enters delivery scope.

## Scope and affected artifacts

| Artifact | Identity | Effect and qualitative risk | Evidence | Owner |
| --- | --- | --- | --- | --- |
| BFF contracts | Baseline → candidate above | Source authority for normalized grants and drawers. High compatibility sensitivity. | [Contract analysis](evidence/bff-contract-analysis.md) | unknown |
| Base shell and shared interfaces | Current HEAD plus identified local edits | Page-entry and restoration changes. High functional risk for affected mappings. | [Base analysis](evidence/mfe-base-analysis.md) | unknown |
| Container permission adapter | Filesystem hashes | Shared action controls and role consumers. High functional sensitivity; production reachability unverified. | [Container analysis](evidence/mfe-ratan-container-analysis.md) | unknown |
| Admin configuration and profile display | Same inspected sources | Conditional administration and limited presentation impact. | [Base analysis](evidence/mfe-base-analysis.md) | unknown |

## User impact

Setup: use equivalent grants with the same tile identity and a reviewed migration mapping.

1. Authenticate and receive a BFF-authorized tile.
2. Restore the saved workspace or request the mapped action.
3. Compare the legacy and reconstructed CES responses.

| Journey | Intended result | Old result | New result | Evidence and limit |
| --- | --- | --- | --- | --- |
| Workspace and deep link | Authorized page remains available. | Legacy subject matches; workspace retained. | Differing CES feature fails; workspace replaced and launch callback unused. | [PROBE-01](06-test-cases.md#probe-01--legacy-subject-rejects-an-authorized-ces-tile); controlled helpers only. |
| Application action | Mapped grant resolves within its application. | X_RATANONE grant returns true. | RATAN_ENTITLEMENT_RULE counterpart returns false. | [PROBE-02](06-test-cases.md#probe-02--ces-application-bypasses-legacy-permission-lookup); synthetic equivalent grants. |
| Mixed migration | Resolve grants from the selected source without losing identity. | Separate legacy representation supported. | Legacy early return masks CES; repeated names overwrite. | [PROBE-03](06-test-cases.md#probe-03--a-legacy-entity-masks-a-ces-grant) and [PROBE-04](06-test-cases.md#probe-04--repeated-application-names-overwrite-grants); policy selection remains unresolved. |

Each row predicts a tangible page or control consequence from inspected callers.
No forced logout, deployed disruption, frequency, or production security bypass was demonstrated.
Owner: unknown. Next action: retain browser assertions for the affected journeys after implementation.

## System impact

The [BFF comparison](evidence/bff-contract-analysis.md#public-contract-comparison) covers login, grants, drawers, tokens, configuration, and migration modes.
Existing login and validation URLs, response fields, and HTTP authorization headers remain supported.
`/auth/v3/sso/login` is the Entra login path; it does not select CES authorization.
No direct browser CES client or FMAA credential handling is required.

Existing `filterRule`, `entryName`, and server-side data authorization remain separate.
This diff does not establish changes to the container's entitlement-rule service endpoints.
Keep backend data permissions distinct from tile and frontend control visibility.

## Options and consequences

| Option | Consequence | Basis | Required decision |
| --- | --- | --- | --- |
| Scoped adapters with retained normalized response | Supports CES while preserving legacy consumers during migration. | Recommended from inspected contracts. | Agree application scope and role/profile semantics. |
| Rename the legacy entity constant only | Leaves generic application names, overwriting, and workspace validation unresolved. | Controlled probes and caller inspection. | Insufficient for this change inventory. |
| Rebuild frontend authorization directly from CES | Adds another integration contract without evidence of need. | BFF already supplies grants and tile decisions. | No required frontend change established. |

## Proposed acceptance and validation

The rows below are proposed compatibility obligations, not approved product ACs.
Existing assertions are inspected source evidence, without fresh suite execution.

### AC to test coverage

| Proposed obligation | Existing inspected assertions | Controlled diagnostic | Required implementation verification |
| --- | --- | --- | --- |
| [FE-01](#fe-01) | [Legacy validation assertions](../../repos/ui/mfe-base/src/utils/common.test.ts#L339) | [PROBE-01](06-test-cases.md#probe-01--legacy-subject-rejects-an-authorized-ces-tile) | Authorized and denied restoration/deep links; empty drawers; rollback. |
| [FE-02](#fe-02) | [Profile legacy rendering](../../repos/ui/mfe-base/src/components/Profile/index.test.tsx#L111) | None | Null-role metadata, stable keys, safe missing-map handling. |
| [FE-03](#fe-03) | No direct scoped-context assertion identified. | None | Correct app; wrong app; same feature in two apps. |
| [FE-04](#fe-04) | [Legacy permission assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.xratanone.test.ts#L21) | [PROBE-02](06-test-cases.md#probe-02--ces-application-bypasses-legacy-permission-lookup), [PROBE-03](06-test-cases.md#probe-03--a-legacy-entity-masks-a-ces-grant), [PROBE-04](06-test-cases.md#probe-04--repeated-application-names-overwrite-grants) | CES exact allow/deny; source selection; duplicate grants in both orders. |
| [FE-05](#fe-05) | [Legacy role extraction](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.test.ts#L397) | None | Approved profile; saved ownership; sharing; read-only restrictions. |
| [FE-06](#fe-06) | [Tile service tests](../../repos/ui/mfe-base/src/admin/Tile/services/index.test.tsx#L29) lack entitlement-payload assertions. | None | Four-field create/edit/checker/audit and CSV round trip. |

Denominator: six proposed obligation groups, including conditional administration.
Four diagnostics cover current behavior in two groups; they do not verify corrected implementation.
Approved product AC inventory remains unresolved, so product AC coverage is not calculable.

### AC to code-change coverage

| Proposed obligation | Required changed units | Relevant unchanged contract | Current conformance evidence |
| --- | --- | --- | --- |
| [FE-01](#fe-01) | Shared tile validator and its callers | BFF per-tile authorization and returned drawer membership | Controlled mismatch. No fix applied. |
| [FE-02](#fe-02) | Shared interfaces and profile rendering | BFF retains normalized hierarchy and token transport | Source mismatch. No fix applied. |
| [FE-03](#fe-03) | Shared application context, or a provider contract extension | Existing Base hooks and module loading | Design proposed; identity question open. |
| [FE-04](#fe-04) | Container normalization and permission resolver | Existing public permission helper consumers | Controlled mismatches. No fix applied. |
| [FE-05](#fe-05) | Active role-dependent consumers after policy decision | Backend action and data enforcement | Replacement policy unresolved. |
| [FE-06](#fe-06) | Tile form, audit, payload and bulk fixtures | Backend four-field schema and maker/checker enforcement | Conditional work; no fix applied. |

Denominator: six proposed groups; zero frontend implementation changes were applied.
Code-derived obligations are not accepted business intent.

### Code-change to test coverage

| Change class | Denominator | Evidence | Result |
| --- | --- | --- | --- |
| Frontend migration implementation | 0 supplied or applied units | Read-only source investigation | N/A; no candidate frontend change set. |
| Diagnostic probes | 4 cases | [Canonical cases](06-test-cases.md), [actual assertions](evidence/contract-probes.cjs), [retained results](evidence/contract-probe-summary.json) | 4 observation assertions passed; product verification not established. |
| Task documentation | Completed artifacts only | [Document validation](evidence/validation.json) | Separate from application behavior. |

No line coverage, complete conformance, or release-confidence percentage is claimed.

## Implementation and release proposal

Recommended sequence:

1. Agree the application context and role/profile contracts.
2. Implement Base tile decisions and the scoped container adapter together.
3. Update shared types, profile rendering, and active role consumers.
4. Add administration fields when that interface enters scope.
5. Run relevant regressions and the complete applicable unit suites before delivery.
6. Verify browser journeys against actual BFF/CES responses and explicit EMS2 rollback behavior.

Proposed release, estimate, deployment owner, and reversal authorization: unknown.
Application fixes and deployment remain outside the current analysis request.
Bounded exploration coding is not applicable; existing helpers were executed without application edits.

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| USER-001 | [Current request](evidence/user-input.md) | 2026-11-05 | [Manifest](evidence/source-manifest.json) | User; analysis scope only. |
| BFF-001 | [Provider comparison](evidence/bff-contract-analysis.md) | Exact base and candidate above | [Manifest](evidence/source-manifest.json) | Owner unknown; current source evidence. |
| BASE-001 | [Base consumers](evidence/mfe-base-analysis.md) | Exact HEAD and baseline above | [Hashes](evidence/mfe-base-source-hashes.json) | Owner unknown; local state preserved. |
| CONTAINER-001 | [Container consumers](evidence/mfe-ratan-container-analysis.md) | No independent revision | [Hashes](evidence/container-source-hashes.json) | Owner unknown; filesystem snapshot. |
| INTENT-001 | [Mapping clarification](../../evidence/knowledge/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md) | user-clarification-20261103-1 | [Knowledge manifest](../../evidence/knowledge/manifest.yaml) | User-stated mapping and FMO exception; no execution proof. |

The graph snapshot is [STALE](evidence/graph-coverage.json) for current BFF source.
Direct current source supports this report; the graph was not rebuilt.
Non-Git source bytes and local edits are retained through the [source manifest](evidence/source-manifest.json).

## Unknowns and blockers

| Question | Consequence | Evidence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Which CES role/profile replaces each active legacy role behavior? | Blocks dependent ownership and restriction implementation. | [FE-05](#fe-05) | unknown | Define explicit profile or capability semantics. |
| Are application names unique across selected app IDs? | Blocks proof of complete application isolation with current name-only payloads. | [FE-03](#fe-03) | unknown | Confirm uniqueness or expose app IDs. |
| Which frontend and backend builds form the release? | Blocks deployed compatibility claims. | [Source manifest](evidence/source-manifest.json) | unknown | Bind import maps, bundles, configuration, and environment. |

These unknowns do not block identification of the required changes.
They are implementation dependencies, not automatic production release holds.

## Stage evidence and completion

| Stage | Required evidence | Record | Result | Remaining action |
| --- | --- | --- | --- | --- |
| Impact analysis | Exact diff and affected consumers | This report and repository analyses | Completed for local source scope | Review implementation dependencies. |
| Formal defect review | Reachable trigger and tangible deployed impact | Not requested | Not assessed | Retain limits beside source concerns. |
| Helper execution | Four canonical diagnostic cases | [Summary](evidence/contract-probe-summary.json) | Four expected current observations retained | Verify corrected behavior during implementation. |
| Browser execution | Actual UI and BFF/CES contracts | None | NOT_RUN | Execute after a frontend candidate exists. |
| Document checks | Schema, links, source hashes, and diff | [Validation](evidence/validation.json) | Recorded separately | ASD review remains PENDING. |

One initial probe setup omitted an injected Hooks binding.
The [setup record](evidence/probe-setup.json) identifies the correction.
The completed first case was preserved before the remaining cases ran.
This setup error is not a product failure.

## Requested decision and actual disposition

- Requested decision: identify required changes; completed in this report.
- Authorized decision owner for implementation or release: unknown.
- Actual business decision: pending; no approval recorded.
- Application implementation: unchanged.
- Intent review: existing mappings retained; replacement role policy remains unresolved.
- Execution: controlled helper observations only; no application suites, browser, or live CES execution.
- Business acceptance and deployment authorization: not established.

## Proposed code examples

The [follow-up request](evidence/user-input-snippets.md#exact-user-input) asks for snippets.
These examples are unapplied. They are not a complete patch or verified implementation.

### Shared types in mfe-base

Update [root.ts](../../repos/ui/mfe-base/src/hooks/model/root.ts#L42).
Keep other existing model fields.

```ts
export type EntitlementSource = "EMS2" | "EMS3";

// Proposed shared context; requires an explicit provider contract.
export interface AuthorizationScope {
  effectiveSource: EntitlementSource;
  applicationNames: readonly string[];
}

export interface Action {
  name: string;
  id?: number | null;
  entitlementId?: number | null;
}

export interface Subject {
  name: string;
  longName?: string | null;
  id?: number | null;
  entitlementSource?: EntitlementSource;
  actions: Action[];
}

export interface Entity {
  name: string;
  id?: number | null;
  applicationName?: string | null;
  roleId?: number | null;
  roleName?: string | null;
  subjects: Subject[];
}

// Add to the existing Tile interface:
// entitlementSource?: EntitlementSource;
```

### Tile restoration and URL launch in mfe-base

Replace the legacy recheck in [common.ts](../../repos/ui/mfe-base/src/utils/common.ts#L293).
Retain the current first-container workspace lookup in this example.

```ts
export const validateWorkspace = (
  workspaces: Workspace[],
  _entities: Entity[] | undefined, // Keep the current caller signature.
  drawers: Tiles[]
): Workspace[] => {
  const retained = workspaces.filter((workspace) =>
    workspace.containers.length === 0 || Boolean(findTile(drawers, workspace))
  );
  return retained.length ? retained : [firstWorkspace()];
};
```

In [useParameters.ts](../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L73), use the current drawer lookup:

```ts
const tile = findTileConfig(
  store.drawers,
  `${Module_PREFIX}/${container_}`,
  `/${module_}`,
  `/${tile_}`
);
if (tile) {
  setParamsAndAddTile(tile, parameters_);
}
```

Also replace [handleDrawers](../../repos/ui/mfe-base/src/utils/login.ts#L98) with explicit empty-array handling:

```ts
export const handleDrawers = (response: AxiosResponse) => {
  const drawers = response?.data?.drawers;
  if (Array.isArray(drawers)) {
    const { baseDispatch } = getHooksBase();
    baseDispatch({ type: ActionType.SET_DRAWERS, data: { drawers } });
  }
};
```

A missing tile remains unavailable. An omitted drawers field preserves state.
These browser checks do not replace backend authorization.

### Scoped CES permissions in mfe-ratan-container

Add a CES resolver beside [authenticator.ts](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L38).
Use current raw entities to avoid the destructive name-map conversion.

```ts
export function hasCesPermission(
  entities: readonly Entity[] | null | undefined,
  applicationNames: readonly string[],
  feature: string,
  action: string
): boolean {
  if (!applicationNames.length || !feature || !action) return false;

  const allowedApps = new Set(applicationNames.filter(Boolean));
  return (entities ?? []).some((entity) =>
    allowedApps.has(entity.name) &&
    (entity.subjects ?? []).some((subject) =>
      subject.entitlementSource === "EMS3" &&
      subject.name === feature &&
      (subject.actions ?? []).some((grant) => grant.name === action)
    )
  );
}

// Example inside a mounted container's CES permission branch:
const canExportFromCes = authorizationScope.effectiveSource === "EMS3" && hasCesPermission(
  getHooks().store?.entities,
  authorizationScope.applicationNames,
  "RATAN_TRADE_BLOTTER",
  "F_Export_Data"
);
```

`Entity` uses the revised shared model above.
`authorizationScope` is a proposed contract; the current BFF does not return it.
Bind effective provider and application names to the selected tile and current session.
Refresh that context on validation and relogin.
Stored `tile.entitlementSource` alone cannot identify the effective rollback provider.

Use this helper only for the effective CES branch.
Do not fall back to legacy permissions after a CES denial.
The EMS2 branch needs source-filtered legacy grants, including isolation from stale flat action lists.
Do not install one global application scope across multiple mounted workspaces.

This example requires unique application names within the selected app IDs.
Otherwise, extend the BFF contract to retain application IDs before frontend resolution.
It preserves exact feature/action matching; confirm canonical names and case in actual CES responses.

### Tile administration payloads in mfe-base

Use the full edited record in [tile services](../../repos/ui/mfe-base/src/admin/Tile/services/useServices.ts#L66).
The form must expose all four fields before this serializer can support CES creation.

```ts
type TileRecord = {
  entitlementSource?: EntitlementSource;
  entitlementAppId?: string | null;
  entitlementAppName?: string | null;
  entitlementAppFeature?: string | null;
  [field: string]: unknown;
};

function toTilePayload(record: TileRecord): TileRecord {
  const source = record.entitlementSource;
  if (source !== "EMS2" && source !== "EMS3") {
    throw new Error("Select an entitlement source.");
  }

  const config = {
    entitlementSource: source,
    entitlementAppId: record.entitlementAppId?.trim(),
    entitlementAppName: record.entitlementAppName?.trim(),
    entitlementAppFeature: record.entitlementAppFeature?.trim(),
  };
  if (source === "EMS3" && [
    config.entitlementAppId,
    config.entitlementAppName,
    config.entitlementAppFeature,
  ].some((value) => !value)) {
    throw new Error("CES requires an application ID, application name, and feature.");
  }
  return { ...record, ...config };
}

await updateTile(store.entitlementsToken, toTilePayload(record));
```

`TileRecord` means the existing admin record plus the four [entitlement fields](#fe-06).
Apply the same serializer to create and checker submissions.
Retain backend length and comma-list validation; this snippet only shows required-field checks.
Show the same fields in audit and verification views.
The source wire value for CES is `EMS3`.

### Role-dependent behavior remains unresolved

The replacement for `getUser().role` needs an explicit trusted role/profile contract.
Do not derive it from CES application names, feature names, or aggregated actions.
That decision controls saved ownership, sharing, and `PSS_RO` restrictions.
No speculative role mapping or new missing-profile policy is included in these examples.
