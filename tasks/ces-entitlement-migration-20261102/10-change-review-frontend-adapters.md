---
artifact_kind: change-request
id: CR-CES-FRONTEND-ADAPTER-IMPLEMENTATION
version: 2
status: draft
owner: unknown
source_refs: [USER-DELIVERY-BRANCHES-20261106, USER-FRONTEND-TESTS-FIRST-20261106, CR-CES-FRONTEND-ENTITLEMENT-IMPACT]
related_ids: [CES-MIGRATION]
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

# Tests-first CES frontend adapters

> **The tests-first adapter implementation is complete for the declared local scope.**
> Action: review the [changes and evidence](#stage-evidence-and-completion) before environment validation.
> Consequence: local results establish selected predicates, while live parity remains unverified.
> Owner: Codex for this implementation. Source: [user request](evidence/frontend-entitlement-impact-20261105/user-tests-first-implementation-20261106.md#exact-user-input).

> **CES role-owned writes remain pending under the user decision.**
> Action: agree ownership, query, exclusion, and trusted data-profile rules before expanding role-sensitive CES behavior.
> Consequence: role-owned writes and two role-restricted exception helpers remain unavailable under CES.
> Owner: unknown. Sources: [ownership decision](evidence/frontend-entitlement-implementation-20261106/user-role-owned-writes-20261106.md#exact-user-answer) and [role boundary](06-test-cases.md#tc-fe-ces-011).

## Delivery branches

The [latest user instruction](evidence/frontend-entitlement-implementation-20261106/user-delivery-branches-20261106.md#exact-user-input) reserves main for PROD.
All three repositories now use `codex/ces-entitlement-migration-20261106` for delivery.
The [branch verification](evidence/frontend-entitlement-implementation-20261106/delivery-branches.json) records exact refs and unchanged source bindings.

| Repository | Delivery commit | Main disposition |
| --- | --- | --- |
| mfe-base | `23dfdf6` | Restored to the pre-migration revision `4c36f8e`. |
| mfe-ratan-container | `d5b5cc5` | No authoritative main was supplied. Local snapshot baseline: `647e6b3`. |
| single-ui-bff | `95480c0` | Preserved unchanged at `834b415`. |

The container now owns local Git history, reconstructed from the supplied snapshot and verified patch.
Its delivery commit contains seven modified files and five added files.
The [container binding](evidence/frontend-entitlement-implementation-20261106/container-delivery-branch.json) preserves baseline provenance and source checks.
Do not treat that reconstructed snapshot as an authoritative PROD revision.
All three worktrees are clean. Source bytes match the tested candidate.
No remote is configured. No push or deployment occurred.

## Request and source facts

Readiness: `READY` for the bounded tests-first shared adapter implementation.
The [proposal](05-impact-analysis-frontend-entitlements.md#proposed-code-snippets) defines the affected interfaces and remaining limits.
The [canonical catalog](06-test-cases.md#tests-first-shared-adapter-implementation) owns case definitions.
The user requested implementation after cases and E2E scripts exist.
Local controlled execution is authorized. Enterprise access remains outside this stage.

## Proposed change

Add an authoritative BFF `entitlementRouting` field without changing existing response fields.
Each route contains tile ID, effective source, entity names, features, and optional CES application ID.
Build routes before assignment filtering, using the same effective mode as authorized drawers.
Keep base login and upper-application permission signatures.
Preserve tile database IDs and resolve current authorized definitions at launch and restore.
Add scoped CES permission and role-list adapters in the shared container.
Do not infer scalar ownership or data-profile meaning from CES assignment names.

## Proposed acceptance and validation

| Intent | Canonical cases | Planned changes |
| --- | --- | --- |
| Preserve ordinary application calls | [TC-FE-CES-007](06-test-cases.md#tc-fe-ces-007), [TC-FE-CES-012](06-test-cases.md#tc-fe-ces-012) | Shared permission dispatch and base launch/restore. |
| Isolate providers and applications | [TC-FE-CES-006](06-test-cases.md#tc-fe-ces-006), [TC-FE-CES-009](06-test-cases.md#tc-fe-ces-009), [TC-FE-CES-010](06-test-cases.md#tc-fe-ces-010) | BFF routing, state replacement, and exact grant matching. |
| Migrate each tile independently | [TC-FE-CES-008](06-test-cases.md#tc-fe-ces-008), [TC-FE-CES-012](06-test-cases.md#tc-fe-ces-012) | Bound facade for conflicting features and current tile identity. |
| Preserve identity and role boundaries | [TC-FE-CES-011](06-test-cases.md#tc-fe-ces-011) | Profile display, scoped role list, and conservative role-sensitive checks. |

Definitions, inspected assertions, application conformance, and passing execution remain separate measures.
The [controlled browser script](frontend-tests/run-browser.mjs) executes actual shared modules with a substituted hooks store.
It does not execute the complete portal, CES, identity service, or BFF controller.

## Options and consequences

Use additive shared adapters and keep ordinary application calls.
This option needs complete BFF routing before CES tiles are enabled.
Keep CES role-owned writes pending under the [user decision](evidence/frontend-entitlement-implementation-20261106/user-role-owned-writes-20261106.md#exact-user-answer).
Do not select one role or submit joined roles as a scalar owner.
A bound facade handles identical features under conflicting providers. Such callers need an explicit binding point.

## Scope and affected artifacts

| Repository | Production scope | Test scope |
| --- | --- | --- |
| [mfe-base](../../repos/ui/mfe-base/) | Login/state, tile identity/admission, mount/restore, profile, and admin routing fields. | Owning Jest cases, declaration checks, and actual React portal execution. |
| [mfe-ratan-container](../../repos/ui/mfe-ratan-container/) | Provider resolver, scoped role names, telemetry labels, and pending role-owned writes. | Existing legacy assertions, new resolver/store/control assertions, and browser integration. |
| [single-ui-bff](../../repos/services/single-ui-bff/) | Additive effective route catalog, response propagation, and effective drawer source marker. | Actual-source routing, serialization, and drawer tests. |

The container began as a filesystem copy. It now owns local snapshot and delivery branches.
The retained patch preserves its original source hashes. Each repository owns its Git history.

## Implementation and release proposal

Deploy the BFF routing field with the corresponding base and container adapters before enabling CES tile migration.
Keep ordinary EMS2-only deployments compatible when routing is absent and no CES entities exist.
Deny unresolved mixed-provider targets. Do not interpret missing CES grants as an EMS2 route.
No deployment, publication, or release approval is requested or inferred here.
Complete missing full application and service validation before a delivery recommendation.

## Sources and evidence limits

The [proposal](05-impact-analysis-frontend-entitlements.md) retains exact original source and capture bindings.
The [tests-first checkpoint](evidence/frontend-entitlement-implementation-20261106/tests-first-checkpoint.json) records pre-implementation definitions and scripts.
The [baseline catalog snapshot](evidence/frontend-entitlement-implementation-20261106/baseline-case-catalog.md) preserves the exact initial case bytes.
Controlled hooks tests execute selected real modules. They do not execute the complete application.
Portal E2E executes the actual React base with synthetic services and an isolated remote contract consumer.
The focused Java runner executes real selected source. Missing private starters prevent the owning Maven suite.
Container dependency boundaries use explicit substitutes for focused tests and selected type checks.
No local result establishes live CES assignments, deployed import-map compatibility, backend data authorization, or business acceptance.

## Unknowns and blockers

| Remaining boundary | Consequence | Owner and next action |
| --- | --- | --- |
| CES scalar ownership and role-query policy. | Role-owned writes remain unavailable. Query parity remains unverified. | unknown; agree the business rule and backend contract. |
| CES multiple-role exclusions and data profiles. | Two role-restricted exception helper paths remain unavailable under CES. | unknown; define the exclusion and trusted profile rules. |
| Identical feature calls under different providers/apps. | Global one-argument calls cannot identify the caller. | application owner unknown; use an explicit bound facade for those callers. |
| Blank CES feature policy. | The frontend admits feature-controlled CES tiles only. | policy owner unknown; reconcile the existing BFF bypass before expanding admission. |
| Full BFF suite and live enterprise verification. | Release readiness and live parity remain unestablished. | service owner unknown; restore private dependencies and execute the declared environment cases. |

## Requested decision and actual disposition

The user authorized tests-first implementation through the [recorded request](evidence/frontend-entitlement-impact-20261105/user-tests-first-implementation-20261106.md#exact-user-input).
The user then directed CES role-owned writes to remain pending.
The [knowledge update](evidence/frontend-entitlement-implementation-20261106/role-write-knowledge-update.json) records candidate version 5 and its new criterion.
Human publication review and business acceptance remain separate from implementation authorization.

## Stage evidence and completion

The [tests-first checkpoint](evidence/frontend-entitlement-implementation-20261106/tests-first-checkpoint.json) precedes application edits.
The original controlled browser baseline has one passing and eight failing checks.
Implementation, source review, and local execution reconciliation are complete for the declared scope.
The [source binding](evidence/frontend-entitlement-implementation-20261106/source-commit-bindings.json) records exact baseline and candidate commits.
No release, publication, or business acceptance is established by this stage.

| Check | Final result | Retained evidence |
| --- | --- | --- |
| Complete base Jest suite | 502 passed, zero failed, zero skipped; 130 suites. | [Final base run](evidence/frontend-entitlement-implementation-20261106/base-complete-final.json). |
| Base TypeScript check | Passed with zero diagnostics. | [Type check](evidence/frontend-entitlement-implementation-20261106/base-typecheck-final.json). |
| Focused container suite | 72 passed, zero failed, zero skipped; includes 18 original legacy cases. | [Container result](evidence/frontend-entitlement-implementation-20261106/container-final.json). |
| Selected container types and patch | Four production sources pass isolated type checking; patch reproduces all 12 files. | [Checks and hashes](evidence/frontend-entitlement-implementation-20261106/container-final.json). |
| Focused BFF Java tests | 28 routing/drawer and 34 identity checks pass; zero failed or skipped. | [Routing](evidence/frontend-entitlement-implementation-20261106/bff-routing-candidate/result.json) and [identity](evidence/frontend-entitlement-implementation-20261106/bff-identity-final/result.json). |
| Browser shared-module integration | Nine checkpoints pass. The original baseline passed one and failed eight. | [Final browser run](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json). |
| Actual React portal E2E | All four checkpoints pass: login, profile, mixed launches, and access withdrawal. | [Portal run](evidence/frontend-entitlement-implementation-20261106/portal-final/run.json). |
| Independent frontend review | Four probes pass. All four material findings are closed. | [Review](evidence/frontend-entitlement-implementation-20261106/independent-review.json). |
| UI specification quality | Zero FAIL findings. Expectation review remains UNVERIFIED because candidate intent is draft. | [Checker](evidence/frontend-entitlement-implementation-20261106/ui-gherkin-check.json) and [mapped manifest](evidence/frontend-entitlement-implementation-20261106/ui-gherkin-manifest.json). |

The final base discovery includes three admin serializer cases added after the earlier 499-case run.
Their display ID changed to [TC-FE-CES-004](06-test-cases.md#tc-fe-ces-004); their assertions remain unchanged.
The [test-label record](evidence/frontend-entitlement-implementation-20261106/base-admin-test-label-correction.json) preserves both hashes.
One BFF identity fixture lacked `user_data.itam_id` while expecting `51358`.
The [fixture correction](evidence/frontend-entitlement-implementation-20261106/bff-change-summary.json) preserves the original assertions and production mapper behavior.

### Final source identities

| Source | Baseline | Candidate or retained patch |
| --- | --- | --- |
| mfe-base | `4c36f8e14e3d9f178b226000ebbcb41aa611616a` | `23dfdf6`; 25 changed files. |
| single-ui-bff | `c114b9c67f7bd6a2afc8a4394b4c372e2aea2e2d` | `95480c0`; seven changed files. |
| mfe-ratan-container | Local snapshot `647e6b3`; seven original files retain SHA-256 bindings. | `d5b5cc5` and [applyable patch](frontend-tests/mfe-ratan-container.patch); 12 changed or new files. |

The patch SHA-256 is `cecbdf2710e3f26643e60de018dfe39aa70634011eb39fb5680890fe2b50b58a`.
The [final reconciliation](evidence/frontend-entitlement-implementation-20261106/final-run-reconciliation.json) checks 175 browser source/script hashes and 12 container file hashes.
All checked hashes match. No deployment or remote write occurred.
The [document and script checks](evidence/frontend-entitlement-implementation-20261106/validation.json) pass within their declared scope.
The complete container suite and full BFF Maven/controller integration remain unexecuted.
The [Maven failure](evidence/frontend-entitlement-implementation-20261106/bff-maven-baseline.json) records two missing private starters.

### Compatibility exceptions

Ordinary mapped permission calls, getUser envelope, and launch signatures remain available.
CES roleList remains an array. Joined role labels have display meaning only.
[Scoped roles](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts) do not invent a scalar role or data profile.
Conflicting feature/provider bindings need additive `createAuthenticator({ tileId })`; unbound conflicting calls deny.
Old EMS2-only responses retain their legacy path without routing metadata.
Responses with CES data require complete BFF routing before permission evaluation.
Private creator-owned writes and established EMS2 writes remain available.
Full admin maker/checker workflow, deployed import-map compatibility, and live query policy remain unverified.

### Baseline and candidate review cases

The [independent review](evidence/frontend-entitlement-implementation-20261106/independent-review.json) retains each closed finding and exact source hashes.
Each case follows its canonical setup and numbered actions below.
Owner: Codex for the correction. Application and environment acceptance owners remain unknown.

| Setup and numbered actions | Required result | Earlier candidate or original result | Final result and consequence |
| --- | --- | --- | --- |
| [TC-FE-CES-003](06-test-cases.md#tc-fe-ces-003): 1. Load an authorized CES tile with blank legacy subject. 2. Evaluate its configured feature. | Use authoritative CES route features. | Earlier candidate used the legacy field and denied a valid tile. | [Two admission regressions](evidence/frontend-entitlement-implementation-20261106/base-admission-feature-regression-before.json) fail before correction. The [final suite](evidence/frontend-entitlement-implementation-20261106/base-complete-final.json) and portal pass. The valid tile mounts. |
| [TC-FE-CES-007](06-test-cases.md#tc-fe-ces-007): 1. Load the captured Peregrine EMS2 grant. 2. Call its existing normalized permission code. | Preserve the original granted result. | Original source returned true. Earlier candidate returned false. | [Same baseline/candidate comparison](evidence/frontend-entitlement-implementation-20261106/review-final-jest-result.json) passes. Existing EMS2 aliases remain usable. |
| [TC-FE-CES-014](06-test-cases.md#tc-fe-ces-014): 1. Select malformed role-owned filter details. 2. Attempt hook cleanup. | Send zero delete calls. | Earlier candidate sent a delete request with stale or absent owner metadata. | [Unchanged hook assertion](evidence/frontend-entitlement-implementation-20261106/review-final-jest-result.json) passes. Requested-row ownership controls cleanup. |
| [TC-FE-CES-014](06-test-cases.md#tc-fe-ces-014): 1. Configure conflicting strategic aliases beside an EMS2 alias. 2. Attempt role-owned creation. | Keep the write pending and send zero requests. | Earlier candidate dropped the unresolved alias and sent creation. | [Same two assertions](evidence/frontend-entitlement-implementation-20261106/review-final-jest-result.json) pass. Configured CES ambiguity cannot bypass the hold. |

These controlled failures establish client predicates. They do not establish live failure frequency or server mutation.
All four corrections have retained failing evidence. No open material frontend finding remains.

## Scoped coverage matrices

Scope: five candidate version 5 criteria and eight production behavior groups below.
The [tests-first checkpoint](evidence/frontend-entitlement-implementation-20261106/tests-first-checkpoint.json) binds the initial definitions and scripts.
The [final reconciliation](evidence/frontend-entitlement-implementation-20261106/final-run-reconciliation.json) binds the browser results to inspected source hashes.
The [proposal comparison](05-impact-analysis-frontend-entitlements.md#proposed-code-snippets) retains the old behavior and intended adapter changes.

All five criteria have canonical definitions and selected passing assertion evidence: `5/5` in this declared scope.
All eight behavior groups have direct assertion links and selected passing execution: `8/8` in this declared scope.
These counts measure traceability for selected predicates. Predicate-complete conformance and business acceptance remain `UNKNOWN`.
The complete enterprise application and acceptance inventories remain `UNKNOWN`.

### AC to test cases and assertions

| Candidate version 5 criterion and intended predicate | Canonical cases | Inspected assertions and matching execution | Definition, assertion, and acceptance limits |
| --- | --- | --- | --- |
| [FE-COMPAT-AC-001](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-001): preserve mapped permission calls and results. | [TC-FE-CES-007](06-test-cases.md#tc-fe-ces-007), [TC-FE-CES-012](06-test-cases.md#tc-fe-ces-012), [TC-FE-CES-013](06-test-cases.md#tc-fe-ces-013). | [Resolver assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ces.test.ts), [dispatcher assertions](../../repos/ui/mfe-base/src/hooks/dispathcer/ces.test.ts), [browser script](frontend-tests/run-browser.mjs), and [portal script](frontend-tests/run-portal.mjs). Selected [container](evidence/frontend-entitlement-implementation-20261106/container-final.json), [browser](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json), and [portal](evidence/frontend-entitlement-implementation-20261106/portal-final/run.json) outcomes pass. | Defined. Selected boolean, helper, launch, and parameter predicates pass. Full consumer compatibility remains unaccepted. |
| [FE-COMPAT-AC-002](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-002): isolate providers, applications, features, and actions. | [TC-FE-CES-003](06-test-cases.md#tc-fe-ces-003), [TC-FE-CES-006](06-test-cases.md#tc-fe-ces-006), [TC-FE-CES-009](06-test-cases.md#tc-fe-ces-009), [TC-FE-CES-010](06-test-cases.md#tc-fe-ces-010). | [BFF routing assertions](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/util/EntitlementRoutingTest.java), [admission assertions](../../repos/ui/mfe-base/src/utils/tileEntitlements.test.ts), [state assertions](../../repos/ui/mfe-base/src/utils/login.ces.test.ts), and [resolver assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ces.test.ts). [BFF routing](evidence/frontend-entitlement-implementation-20261106/bff-routing-candidate/result.json), [base](evidence/frontend-entitlement-implementation-20261106/base-complete-final.json), and [browser](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json) checks pass. | Defined. Selected grant-chain, denial, duplicate-row, and refresh predicates pass. Live assignments and blank-feature policy remain outside acceptance. |
| [FE-COMPAT-AC-003](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-003): switch one tile independently and preserve role multiplicity. | [TC-FE-CES-008](06-test-cases.md#tc-fe-ces-008), [TC-FE-CES-011](06-test-cases.md#tc-fe-ces-011). | [Bound resolver and role assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ces.test.ts), [profile assertions](../../repos/ui/mfe-base/src/components/Profile/util.ces.test.ts), and [mixed-tile browser assertions](frontend-tests/run-browser.mjs). Selected [container](evidence/frontend-entitlement-implementation-20261106/container-final.json) and [browser](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json) outcomes pass. | Defined. The mixed-feature fixture uses explicit tile binding. Unbound conflicting targets deny; role-dependent business mappings remain unresolved. |
| [BFF-ENTITY-AC-002](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002): keep application ID, CES name, and team name separate. | [TC-FE-CES-011](06-test-cases.md#tc-fe-ces-011), [TC-FE-CES-013](06-test-cases.md#tc-fe-ces-013). | [Mapper identity assertions](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java), [profile assertions](../../repos/ui/mfe-base/src/components/Profile/util.ces.test.ts), and [portal assertions](frontend-tests/run-portal.mjs). Selected [mapper](evidence/frontend-entitlement-implementation-20261106/bff-identity-final/result.json) and [portal](evidence/frontend-entitlement-implementation-20261106/portal-final/run.json) outcomes pass. | Defined. Mapper assertions check all three exact values. Portal services are synthetic; live response acceptance remains unexecuted. |
| [FE-ROLE-WRITE-AC-001](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-role-write-ac-001): send zero pending CES role-owned writes and preserve EMS2. | [TC-FE-CES-014](06-test-cases.md#tc-fe-ces-014). | [Store and request assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/roleOwnership.ces.test.ts), [control assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/roleOwnership.ui.ces.test.tsx), and [actual-hook cleanup assertions](evidence/frontend-entitlement-implementation-20261106/review-role-delete.ces.test.tsx). [Container](evidence/frontend-entitlement-implementation-20261106/container-final.json) and [independent cleanup](evidence/frontend-entitlement-implementation-20261106/review-role-delete-final-result.json) outcomes pass. | Defined. Selected create, update, delete, malformed-item, and private-write predicates pass with substituted services. Backend ownership policy remains unresolved. |

### AC to changed code

| Candidate version 5 criterion | Changed behavior groups and inspected source | Required unchanged paths and conformance limits |
| --- | --- | --- |
| [FE-COMPAT-AC-001](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-001). | Container permissions: [authenticator](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts). Base admission and restore: [dispatcher](../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts), [workspace resolver](../../repos/ui/mfe-base/src/utils/drawer.ts), and [container mount](../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx). | Ordinary permission and launch signatures remain. Unbound conflicting feature targets require explicit binding; full consumer equivalence remains unproved. |
| [FE-COMPAT-AC-002](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-002). | BFF routing and effective drawer source: [routing builder](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/EntitlementRouting.java) and [drawer utility](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java). Base state: [login](../../repos/ui/mfe-base/src/utils/login.ts). Base admission: [common helpers](../../repos/ui/mfe-base/src/utils/common.ts). Container permissions: [authenticator](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts). | Legacy EMS2 authorization remains required. Missing mixed routing denies. BFF blank-feature admission and live service conformance remain unresolved. |
| [FE-COMPAT-AC-003](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-003). | Base admin: [editor fields](../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx), and [audit fields](../../repos/ui/mfe-base/src/admin/Tile/common/useAudit.tsx). Container permissions: [bound resolver](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts). Profile: [formatter](../../repos/ui/mfe-base/src/components/Profile/util.ts). Roles and telemetry: [analytics helper](../../repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.ts). | Existing [request services](../../repos/ui/mfe-base/src/admin/Tile/services/useServices.ts) and maker/checker policy remain required. Admin payload assertions do not establish full workflow conformance. Scalar role semantics remain unchanged for EMS2. |
| [BFF-ENTITY-AC-002](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002). | Profile: [formatter](../../repos/ui/mfe-base/src/components/Profile/util.ts) and [profile component](../../repos/ui/mfe-base/src/components/Profile/index.tsx). Base state: [entity retention](../../repos/ui/mfe-base/src/utils/login.ts). | The earlier [BFF mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java) remains required existing implementation. This stage does not relabel it as a new mapper change. |
| [FE-ROLE-WRITE-AC-001](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-role-write-ac-001). | Ownership: [ownership guard](../../repos/ui/mfe-ratan-container/src/ratanutils/roleOwnership.ts), [view store](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts), [filter store](../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/store.ts), [view controls](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/ViewName.tsx), and [filter controls](../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/FilterName.tsx). | EMS2 role writes and CES private creator-owned writes remain required. Backend role-query and ownership conformance remain unverified. |

### Changed code to test cases and execution

| Production behavior group and affected predicates | Canonical cases | Direct assertion locations | Matching execution and remaining limits |
| --- | --- | --- | --- |
| BFF routing and effective drawer source: catalog before grant filtering, denied routes, rollback, and invalid CES definitions. | [TC-FE-CES-009](06-test-cases.md#tc-fe-ces-009). | [Routing tests](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/util/EntitlementRoutingTest.java) and [drawer tests](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/util/AdminModuleUtilTest.java). | [28 focused checks pass](evidence/frontend-entitlement-implementation-20261106/bff-routing-candidate/result.json). Full Maven and controller/service integration remain unexecuted. |
| Base state: replace routing and grants together; clear explicit empty drawers; preserve omitted drawers. | [TC-FE-CES-010](06-test-cases.md#tc-fe-ces-010), [TC-FE-CES-013](06-test-cases.md#tc-fe-ces-013). | [Login tests](../../repos/ui/mfe-base/src/utils/login.ces.test.ts), [browser script](frontend-tests/run-browser.mjs), and [portal script](frontend-tests/run-portal.mjs). | [Complete base suite](evidence/frontend-entitlement-implementation-20261106/base-complete-final.json), [browser](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json), and [portal](evidence/frontend-entitlement-implementation-20261106/portal-final/run.json) pass. Portal services are synthetic. |
| Base admission and restore: current authorized tile, preserved database ID, exact restore, revoked and ambiguous denial. | [TC-FE-CES-003](06-test-cases.md#tc-fe-ces-003), [TC-FE-CES-012](06-test-cases.md#tc-fe-ces-012), [TC-FE-CES-013](06-test-cases.md#tc-fe-ces-013). | [Admission tests](../../repos/ui/mfe-base/src/utils/tileEntitlements.test.ts), [drawer tests](../../repos/ui/mfe-base/src/utils/drawer.ces.test.ts), [dispatcher tests](../../repos/ui/mfe-base/src/hooks/dispathcer/ces.test.ts), and [portal script](frontend-tests/run-portal.mjs). | [Base suite](evidence/frontend-entitlement-implementation-20261106/base-complete-final.json), [browser](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json), and [portal](evidence/frontend-entitlement-implementation-20261106/portal-final/run.json) pass. Blank-feature policy acceptance remains unresolved. |
| Base admin: forward four routing fields through create, update, and verify requests. | [TC-FE-CES-004](06-test-cases.md#tc-fe-ces-004). | [Service payload tests](../../repos/ui/mfe-base/src/admin/Tile/services/ces.test.tsx). | [Three payload checks pass](evidence/frontend-entitlement-implementation-20261106/base-admin-label-final-jest.json). Full create/checker/title-edit/audit E2E remains `NOT_RUN`. Field display has source inspection only. |
| Profile: preserve team label; display scoped assignment labels and structured CES actions with distinct keys. | [TC-FE-CES-011](06-test-cases.md#tc-fe-ces-011), [TC-FE-CES-013](06-test-cases.md#tc-fe-ces-013). | [Formatter tests](../../repos/ui/mfe-base/src/components/Profile/util.ces.test.ts), [component tests](../../repos/ui/mfe-base/src/components/Profile/index.ces.test.tsx), and [portal script](frontend-tests/run-portal.mjs). | [Base suite](evidence/frontend-entitlement-implementation-20261106/base-complete-final.json) and [portal](evidence/frontend-entitlement-implementation-20261106/portal-final/run.json) pass. [34 mapper checks](evidence/frontend-entitlement-implementation-20261106/bff-identity-final/result.json) preserve the upstream identity contract. |
| Container permissions: complete CES grant chain, row union, provider precedence, bound conflicts, and legacy aliases. | [TC-FE-CES-006](06-test-cases.md#tc-fe-ces-006), [TC-FE-CES-007](06-test-cases.md#tc-fe-ces-007), [TC-FE-CES-008](06-test-cases.md#tc-fe-ces-008), [TC-FE-CES-009](06-test-cases.md#tc-fe-ces-009). | [Resolver tests](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ces.test.ts), [legacy alias comparison](evidence/frontend-entitlement-implementation-20261106/review-legacy-alias.ces.test.ts), and [browser script](frontend-tests/run-browser.mjs). | [72 focused container checks](evidence/frontend-entitlement-implementation-20261106/container-final.json), [browser](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json), and [independent alias comparison](evidence/frontend-entitlement-implementation-20261106/review-legacy-alias-final-result.json) pass. Complete container integration remains unexecuted. |
| Roles and telemetry: scoped assignment labels, unchanged no-argument legacy label, and conservative role-sensitive exception checks. | [TC-FE-CES-011](06-test-cases.md#tc-fe-ces-011). | [Role and exception assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ces.test.ts) and [telemetry assertions](../../repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.ces.test.ts). | [Container checks](evidence/frontend-entitlement-implementation-20261106/container-final.json) pass. Two CES exception paths remain closed pending the business exclusion rule. |
| Ownership: zero pending role-owned requests, preserved private/EMS2 writes, malformed cleanup, and unresolved builder aliases. | [TC-FE-CES-014](06-test-cases.md#tc-fe-ces-014). | [Store tests](../../repos/ui/mfe-ratan-container/src/ratanutils/roleOwnership.ces.test.ts), [control tests](../../repos/ui/mfe-ratan-container/src/ratanutils/roleOwnership.ui.ces.test.tsx), and [actual-hook cleanup tests](evidence/frontend-entitlement-implementation-20261106/review-role-delete.ces.test.tsx). | [Container checks](evidence/frontend-entitlement-implementation-20261106/container-final.json) and [independent cleanup](evidence/frontend-entitlement-implementation-20261106/review-role-delete-final-result.json) pass with substituted services. No live ownership writes ran. |

The [browser run](evidence/frontend-entitlement-implementation-20261106/browser-final/run.json) has nine passing checkpoints.
The [portal run](evidence/frontend-entitlement-implementation-20261106/portal-final/run.json) has four passing checkpoints.
The two focused BFF groups contain 62 passing checks. They do not replace the complete service suite.
