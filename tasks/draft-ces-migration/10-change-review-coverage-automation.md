---
artifact_kind: change-request
id: CES-COVERAGE-AUTOMATION
version: 3
status: draft
owner: unknown
source_refs: [USER-EMS2-ENV-20261103, USER-COVERAGE-20261103, USER-MOCK-20261103, CES-COVERAGE-CASES, KT-ces-migration-parity, COVERAGE-REPLAY, COVERAGE-LIVE-PREFLIGHT]
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

# Migration and EMS2 coverage automation: stage review

> **The combined launcher compares EMS2 PROD with CES UAT and EMS2 UAT. Complete population parity remains unassessed.**
> Action: follow the [operating guide](coverage/README.md#run-all-coverage) and review the [combined dashboard](evidence/coverage-runs/all-coverage-20261103/index.html).
> Consequence: absent captures and inventories limit each comparison independently.
> Owner: unknown. Evidence: [latest tooling request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input).

## Request and source facts

- Requester: the user; named operational owner remains unknown.
- Current baseline: [prior source-understanding stage](01-intake.md#migration-data-coverage-understanding) at Git `6854a6b63c323fd9c4eb15bb27725e49f302f712`.
- Latest extension: [instructions for all coverage and EMS2 UAT-versus-PROD comparison](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input).
- Request source: [exact automation clarification](evidence/coverage-automation-20261103/user-input.md#exact-user-input).
- Latest execution boundary: [use supplied API responses as mock data](evidence/coverage-mock-20261103/user-input.md#exact-user-input).
- Environment limit: real environments are inaccessible from this session. No further enterprise access attempts are authorized by this stage.
- Rationale: run both comparison families through one command and preserve separate denominators, definitions, and account outcomes.
- Entry route: requirements first. The user requested implementation after reviewing the supplied sources.
- Chronology: source analysis and automation implementation occurred on 3 November 2026.
- Evidence limit: the user-stated no-gap objective does not establish measured migration success.

The user resolves FMO Portal Admin as an unlaunched non-production exception with no current account assignments.
Its comparison remains lower priority and outside production denominators.
The [candidate knowledge](../../knowledge/candidates/security/KT-ces-migration-parity.md) records this clarification and the four-concept mapping.

## Stage boundary and readiness

| Named stage | Readiness | Rationale and limit | Owner and next action |
| --- | --- | --- | --- |
| Runner implementation handoff | READY | Controlled runtime tests and wheel construction pass. The operating guide defines mock scope and evidence limits. | unknown; use the documented launcher. |
| Supplied-response mock verification | READY | The user explicitly requests this bounded execution. Supplied examples support both comparisons and complete discovered-population accounting. | Codex; retain the mock run and relevant assertions. |
| EMS2 environment and suite extension | READY | The latest request authorizes read-only tooling. Supplied PROD and UAT captures support bounded replay. | Codex; retain environment contracts, source assertions, and aggregate output. |
| Migration acceptance or deployment | NEEDS_CLARIFICATION | Complete live comparison, data-scope definitions, and applicable human disposition remain unavailable. | unknown; obtain the required evidence and review. |

Assessor: Codex, 3 November 2026, Asia/Singapore.
Live migration collection is outside the current session scope. No credential or certificate action is requested.
The intake remains living; no frozen intake was supplied for this stage.
Earlier source conclusions remain bound to their own dates and hashes.
Compared baseline: Workbench Git `6854a6b63c323fd9c4eb15bb27725e49f302f712` plus the current scoped local additions.
The default mock revision compares against `85d8a9967db7774f8ea83a60495d1852827abcc3`.
The [mock binding](evidence/coverage-runs/mock-supplied-20261103/binding.json) identifies configuration, implementation, matrices, mode, and retained examples by SHA-256.
The earlier [validation](evidence/coverage-automation-20261103/final-validation.json) remains bound to its prior source hashes.
The [mock validation](evidence/coverage-mock-20261103/validation.json) records checks for the revised default execution boundary.
Intake freeze integrity is not applicable.
The earlier validation confirms source bindings, all 800 runtime tests, and 47 final coverage tests.
That wheel installed outside this checkout. A fresh workspace initialized and validated successfully.
That HTML summary and account filter passed browser inspection.
The earlier mock-default revision passed all 802 runtime tests, including 49 coverage tests, with zero failures, errors, or skips.
The environment extension passed 44 affected checks, including 16 EMS2 comparator tests and six suite tests.
The complete suite rerun could not start: automatic permission review timed out twice for the required localhost listeners.
The prior 802-test result retains its unchanged-source scope. It does not cover the new modules.
The revised wheel built and installed outside this checkout. Its default mode equals `replay`.
The separate [verification evidence](evidence/coverage-mock-20261103/validation.json) binds these results to current source hashes.
The [environment validation](evidence/ems2-environment-coverage-20261103/validation.json) binds the new comparator and suite checks to their exact sources.
Earlier test counts apply only to their recorded source hashes. They do not substitute for the extension checks.
Windows launcher execution remains untested. Its documented arguments match the supported command.

## Proposed change

All additions below are implemented in the local candidate.

| Aspect | Before | Implemented addition | Evidence |
| --- | --- | --- | --- |
| Entitlement comparison | Static source inspection and sample counts. | Compare scoped application, entitlement, feature, and action relationships. | [normalization and comparison](../../core/entitlement_reconciliation.py#L88). |
| Account collection | Two supplied effective-user examples. | Expand matrix cells and catalog memberships, then compare every discovered account against available stored responses. | [source parsing](../../core/entitlement_sources.py#L130) and [runner](../../core/entitlement_coverage.py#L377). |
| Difference review | Manual comparison. | Retain matched counts and JSON details; filter matches from active HTML and CSV differences. | [report completion](../../core/entitlement_coverage.py#L304). |
| Repeat execution | Only the migration comparator had a launcher. | Run both comparison families with separate outputs and a combined dashboard. | [suite](../../core/coverage_suite.py) and [all-coverage instructions](coverage/README.md#run-all-coverage). |
| EMS2 environments | No executable PROD-to-UAT comparison. | Compare names within entities using each environment's request identifiers. | [environment runner](../../core/ems2_coverage.py) and [configuration](coverage/ems2-config.json). |

## Scope and affected artifacts

| Artifact | Version or identity | Effect | Risk and basis | Owner |
| --- | --- | --- | --- | --- |
| Three Python helper modules | [Exact mock hashes](evidence/coverage-runs/mock-supplied-20261103/binding.json). | Add scoped source acquisition, semantic comparison, and reporting. | Moderate; source incompleteness or scope errors could misstate coverage. | unknown |
| [Task configuration](coverage/config.json) | SHA-256 in the run binding. | Keep tenant endpoints, entity mappings, exclusions, and workbook paths outside shared defaults. | Moderate; mappings control comparison meaning. | unknown |
| [Canonical cases](06-test-cases.md) | Version 3. | Define thirteen comparison, failure, recovery, isolation, and suite cases. | Low; actual outcomes remain separate. | unknown |
| Four test modules | [Earlier suite](evidence/coverage-automation-20261103/unit-tests-all.log) and [mock validation](evidence/coverage-mock-20261103/validation.json). | Preserve 47 earlier checks and add default mock-isolation assertions. | Low; controlled services limit live claims. | unknown |
| [Candidate intent](../../knowledge/candidates/security/KT-ces-migration-parity.md) | Version 1; [audit](../../evidence/knowledge/audit/AUD-20261103-KT-ces-migration-parity-v1.yaml). | Preserve user clarification and source provenance. | Candidate only; publication remains pending. | unknown |
| [EMS2 environment runner](../../core/ems2_coverage.py) | Hashes in [environment validation](evidence/ems2-environment-coverage-20261103/validation.json). | Compare environment inventories and each discovered account while preserving entity identity. | Moderate; wrong environment routing could misstate parity. | unknown |
| [Coverage suite](../../core/coverage_suite.py) | Hashes in the same validation. | Invoke both comparators, retain child failures, and render one dashboard. | Low; aggregate status must retain incomplete children. | unknown |

The single Python runtime remains under `core/`, with installed package name `ai_sdlc_workbench`.
The helper uses the existing dependency set and standard-library XLSX extraction.
No dependency or startup download was added. No application authorization implementation was changed.

## User impact

| Actor and journey | Trigger | Before and after | Consequence | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Migration analyst | Starts one launcher. | Manual samples become a combined acquisition and comparison run. | Less manual work; visible missing, additional, and unassessed content. | [Controlled runner assertions](../../tests/test_entitlement_coverage.py#L193); enterprise access remains unavailable. | unknown | Review supplied-response differences and unassessed accounts. |
| Production application user | Uses existing authorization. | This change modifies no application permission enforcement. | No demonstrated application session impact from the helper. | Source scope is analysis and reporting only. | unknown | Assess migration effects from acquired comparison evidence. |

## System impact

| Changed path | Inspected consumer | Interface effect | Failure or concurrency risk | Evidence | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| [entitlement_reconciliation.py](../../core/entitlement_reconciliation.py#L53) | Source parser and coverage runner. | Return scoped sets, explicit differences, and unavailable data-scope state. | Mapping collisions or malformed content must fail visibly. | [Mapping assertions](../../tests/test_entitlement_reconciliation.py#L65). | unknown | Preserve exact context checks. |
| [entitlement_sources.py](../../core/entitlement_sources.py#L130) | Coverage collector. | Read matrices and collection exports; acquire bounded JSON over verified TLS. | Errors, redirects, or partial bodies must not produce empty passes. | [HTTP assertions](../../tests/test_entitlement_sources.py#L167). | unknown | Preserve verified TLS in the optional live path; use replay for this session. |
| [entitlement_coverage.py](../../core/entitlement_coverage.py#L377) | Module entry point and task launchers. | Collect bounded batches; persist completed accounts; render reports and resume exact bindings. | Global access failures stop scheduling; incomplete accounts remain visible. | [Failure](../../tests/test_entitlement_coverage.py#L238) and [recovery](../../tests/test_entitlement_coverage.py#L345) assertions. | unknown | Inspect mock outcomes without extrapolating missing responses. |
| [ems2_coverage.py](../../core/ems2_coverage.py#L212) | EMS2 launcher and suite. | Compare PROD baseline with UAT target using environment-specific request IDs. | Numeric differences must not hide name or entity differences. | [Semantic and provenance assertions](../../tests/test_ems2_coverage.py#L69). | unknown | Review each entity and unavailable source. |
| [coverage_suite.py](../../core/coverage_suite.py#L60) | Combined task launchers. | Invoke both configured comparison families and keep separate output identities. | Child failure must not omit another comparison or produce a passing aggregate. | [Failure-isolation assertions](../../tests/test_coverage_suite.py#L61). | unknown | Review child outcomes before interpreting aggregate status. |

The [environment runner](../../core/ems2_coverage.py) reuses the existing collection, matrix, and EMS2 normalization contracts.
It preserves entity names instead of mapping them into the shared CES application.
The [suite](../../core/coverage_suite.py) calls both module entry points through configured comparison identities.
No existing Workbench CLI parser or application authorization caller was changed.
Task launchers use the installed Python modules.

## Options and consequences

| Option | Consequence | Evidence | Decision |
| --- | --- | --- | --- |
| Run replay against supplied examples. | Checks supplied captures and retains unavailable accounts without enterprise access. | [Mock run](evidence/coverage-runs/mock-supplied-20261103/result.json). | Selected by the latest user instruction and default launcher. |
| Run live collection. | Requires a different authorized environment and its own evidence boundary. | [Historical preflight](evidence/coverage-runs/live-access-check-unsandboxed/result.json). | Outside this session. No credential or CA action is requested. |
| Accept catalog counts as complete migration proof. | Would omit assignments, extra grants, unavailable accounts, and data restrictions. | [Candidate evidence limits](../../knowledge/candidates/security/KT-ces-migration-parity.md#evidence-limits). | Unsupported by current evidence. |

## Proposed acceptance and validation

The automation scope contains ten criteria and thirteen canonical case definitions.
The initial seven criteria retain their inspected source and direct assertion chains.
The eighth criterion adds the user-required default mock boundary.
The ninth and tenth criteria add EMS2 environment comparison and combined suite execution.
The earlier 49 focused tests cover supported parser, transport, comparison, report, recovery, and default mock boundaries.
The earlier default revision passed no-network, no-credential-loading, and explicit mock-label assertions.
The current extension passed 44 affected tests, including all 22 tests for the new modules.
These counts establish bounded runner verification, not complete migration conformance.

### AC-to-test matrix

| Criterion | Canonical cases | Inspected executable assertion | Retained outcome |
| --- | --- | --- | --- |
| [COV-AC-001](01-intake.md#cov-ac-001) | [TC-COV-001](06-test-cases.md#tc-cov-001), [TC-COV-003](06-test-cases.md#tc-cov-003) | [Scoped four-concept mapping](../../tests/test_entitlement_reconciliation.py#L65), [role content difference](../../tests/test_entitlement_reconciliation.py#L203), [live inventory renames](../../tests/test_entitlement_coverage_sources.py#L135). | Passed within the [runtime suite](evidence/coverage-automation-20261103/unit-tests-all.log). |
| [COV-AC-002](01-intake.md#cov-ac-002) | [TC-COV-002](06-test-cases.md#tc-cov-002) | [5,000-ID cell expansion](../../tests/test_entitlement_reconciliation.py#L41), [membership expansion](../../tests/test_entitlement_reconciliation.py#L122), [complete union fetch](../../tests/test_entitlement_coverage.py#L193). | Passed in controlled conditions. |
| [COV-AC-003](01-intake.md#cov-ac-003) | [TC-COV-003](06-test-cases.md#tc-cov-003), [TC-COV-008](06-test-cases.md#tc-cov-008) | [Changed role with equal union](../../tests/test_entitlement_coverage.py#L222), [data and provenance limits](../../tests/test_entitlement_reconciliation.py#L150), [catalog conflict](../../tests/test_entitlement_coverage_sources.py#L106). | Passed; full data-scope equality remains unassessed. |
| [COV-AC-004](01-intake.md#cov-ac-004) | [TC-COV-004](06-test-cases.md#tc-cov-004) | [Exact difference sets](../../tests/test_entitlement_reconciliation.py#L188), [HTML and CSV match filtering](../../tests/test_entitlement_coverage.py#L193), [unexpected features retained](../../tests/test_entitlement_coverage_sources.py#L83). | Passed in controlled conditions. |
| [COV-AC-005](01-intake.md#cov-ac-005) | [TC-COV-005](06-test-cases.md#tc-cov-005) | [Failed account denominator](../../tests/test_entitlement_coverage.py#L238), [unavailable inventory](../../tests/test_entitlement_coverage.py#L255), [HTTP error and redaction](../../tests/test_entitlement_sources.py#L167). | Passed; unavailable accounts do not become passing profiles. |
| [COV-AC-006](01-intake.md#cov-ac-006) | [TC-COV-006](06-test-cases.md#tc-cov-006) | [Excluded FMO and absent FMO requests](../../tests/test_entitlement_coverage.py#L193). | Passed for configured production exclusion. |
| [COV-AC-007](01-intake.md#cov-ac-007) | [TC-COV-007](06-test-cases.md#tc-cov-007), [TC-COV-009](06-test-cases.md#tc-cov-009) | [Combined output](../../tests/test_entitlement_coverage.py#L193), [checkpoint persistence](../../tests/test_entitlement_coverage.py#L365), [resume source binding](../../tests/test_entitlement_coverage.py#L345), [tamper rejection](../../tests/test_entitlement_coverage.py#L400). | Passed in controlled conditions; supplied replay also produced all report artifacts. |
| [COV-AC-008](01-intake.md#cov-ac-008) | [TC-COV-010](06-test-cases.md#tc-cov-010) | [Default CLI and mock labels](../../tests/test_entitlement_coverage.py#L302), [missing-capture accounting without HTTP fallback](../../tests/test_entitlement_coverage.py#L323). | See [mock validation](evidence/coverage-mock-20261103/validation.json) for the matching execution. |
| [COV-AC-009](01-intake.md#cov-ac-009) | [TC-COV-011](06-test-cases.md#tc-cov-011), [TC-COV-012](06-test-cases.md#tc-cov-012) | [Numeric IDs and mock isolation](../../tests/test_ems2_coverage.py#L69), [role changes](../../tests/test_ems2_coverage.py#L90), [direction](../../tests/test_ems2_coverage.py#L104), [unavailable captures](../../tests/test_ems2_coverage.py#L117), [entity context](../../tests/test_ems2_coverage.py#L182), [recovery](../../tests/test_ems2_coverage.py#L208). | [Environment validation](evidence/ems2-environment-coverage-20261103/validation.json) records matching execution and limits. |
| [COV-AC-010](01-intake.md#cov-ac-010) | [TC-COV-013](06-test-cases.md#tc-cov-013) | [Both-child invocation](../../tests/test_coverage_suite.py#L43), [setup failure](../../tests/test_coverage_suite.py#L61), [durability](../../tests/test_coverage_suite.py#L75), [difference exit](../../tests/test_coverage_suite.py#L95), [match and incomplete exits](../../tests/test_coverage_suite.py#L122). | The same validation records aggregate and child outcomes. |

Definition denominator: 10 criteria and 13 readable cases.
Earlier assertion denominator: 8 criteria with inspected direct assertion chains.
The two extension criteria have separate assertion and execution evidence in [environment validation](evidence/ems2-environment-coverage-20261103/validation.json).
The default mock criterion passed its direct assertions in the earlier bound runtime suite.
Earlier execution denominator: 49 coverage tests; all 49 passed against their bound sources.
Current affected execution denominator: 44 tests; all 44 passed with zero failures, errors, or skips.
The thirteen readable cases are specifications. They are not thirteen separately recorded enterprise executions.

### AC-to-code-change matrix

| Criterion | Changed implementation | Conformance evidence and limit |
| --- | --- | --- |
| [COV-AC-001](01-intake.md#cov-ac-001) | [EMS2 normalization](../../core/entitlement_reconciliation.py#L88), [CES catalog normalization](../../core/entitlement_reconciliation.py#L155), [set comparison](../../core/entitlement_reconciliation.py#L244). | Preserves scoped four-concept definitions; configured mappings control semantics. |
| [COV-AC-002](01-intake.md#cov-ac-002) | [Cell expansion](../../core/entitlement_reconciliation.py#L53), [matrix parsing](../../core/entitlement_sources.py#L130), [dynamic run population](../../core/entitlement_coverage.py#L377). | Covers supplied matrix and CES membership populations; no complete EMS2 directory endpoint was supplied. |
| [COV-AC-003](01-intake.md#cov-ac-003) | [Account comparison](../../core/entitlement_coverage.py#L209), [CES effective normalization](../../core/entitlement_reconciliation.py#L194). | Separates assignments, reconstructed profile grants, effective grants, and data-scope limits. |
| [COV-AC-004](01-intake.md#cov-ac-004) | [Comparison results](../../core/entitlement_reconciliation.py#L244), [HTML rendering](../../core/entitlement_coverage.py#L269), [CSV and JSON output](../../core/entitlement_coverage.py#L304). | Matched content remains in JSON. Explicit exclusions do not hide arbitrary new features. |
| [COV-AC-005](01-intake.md#cov-ac-005) | [HTTP acquisition](../../core/entitlement_sources.py#L256), [account error state](../../core/entitlement_coverage.py#L209), [summary denominator](../../core/entitlement_coverage.py#L304). | Retains unassessed counts and null final coverage when baseline assessment is incomplete. |
| [COV-AC-006](01-intake.md#cov-ac-006) | [Included entity selection](../../core/entitlement_coverage.py#L175), [FMO task configuration](coverage/config.json). | FMO remains a reported non-production exception. |
| [COV-AC-007](01-intake.md#cov-ac-007) | [Run and checkpoint control](../../core/entitlement_coverage.py#L377), [entry point](../../core/entitlement_coverage.py#L483), [macOS launcher](run-coverage.command), [Windows launcher](run-coverage.cmd). | One invocation writes both comparisons. Resume rejects changed bound sources. |
| [COV-AC-008](01-intake.md#cov-ac-008) | [Replay default](../../core/entitlement_coverage.py#L377), [CLI default](../../core/entitlement_coverage.py#L483), [collector isolation](../../core/entitlement_coverage.py#L83), [mock labels](../../core/entitlement_coverage.py#L269). | Default replay skips private environment loading and HTTP client construction. Missing responses remain unassessed. |
| [COV-AC-009](01-intake.md#cov-ac-009) | [Name-based account comparison](../../core/ems2_coverage.py#L60), [paired inventories](../../core/ems2_coverage.py#L86), [run control](../../core/ems2_coverage.py#L212), [environment configuration](coverage/ems2-config.json). | PROD is the baseline. Name tuples retain entity context. Missing captures and data scope stay unassessed. |
| [COV-AC-010](01-intake.md#cov-ac-010) | [Suite run control](../../core/coverage_suite.py#L60), [dashboard](../../core/coverage_suite.py#L27), [suite configuration](coverage/suite.json), [combined launchers](coverage/README.md#run-all-coverage). | Both comparisons run independently; aggregate results preserve child differences and incompleteness. |

The earlier automation implementation scope covers 8 criteria with source, assertions, and retained execution.
The extension adds 2 criteria; its current verification disposition is retained in [environment validation](evidence/ems2-environment-coverage-20261103/validation.json).
This statement does not establish complete business mappings, full data access equality, or 100% production migration conformance.

### Code-change-to-test matrix

| Changed runtime unit | Direct assertion chains | Execution and denominator |
| --- | --- | --- |
| [entitlement_reconciliation.py](../../core/entitlement_reconciliation.py) | [Mapping](../../tests/test_entitlement_reconciliation.py#L65), [membership](../../tests/test_entitlement_reconciliation.py#L122), [set equality](../../tests/test_entitlement_reconciliation.py#L188). | 15 focused tests passed. |
| [entitlement_sources.py](../../core/entitlement_sources.py) | [XLSX identity cells](../../tests/test_entitlement_sources.py#L58), [collection credential omission](../../tests/test_entitlement_sources.py#L83), [TLS preservation](../../tests/test_entitlement_sources.py#L188). | 12 focused tests passed. |
| [entitlement_coverage.py](../../core/entitlement_coverage.py) | [Controlled HTTP runner](../../tests/test_entitlement_coverage.py#L193), [resume](../../tests/test_entitlement_coverage.py#L345), [new-feature regression](../../tests/test_entitlement_coverage_sources.py#L83), [source conflict reporting](../../tests/test_entitlement_coverage_sources.py#L113). | 15 integration tests and 7 source-consistency tests passed. |
| [ems2_coverage.py](../../core/ems2_coverage.py) | [Semantic equality](../../tests/test_ems2_coverage.py#L69), [role provenance](../../tests/test_ems2_coverage.py#L90), [missing capture](../../tests/test_ems2_coverage.py#L117), [count and context failures](../../tests/test_ems2_coverage.py#L168), [recovery](../../tests/test_ems2_coverage.py#L208). | All 16 tests passed; source hashes are in [environment validation](evidence/ems2-environment-coverage-20261103/validation.json). |
| [coverage_suite.py](../../core/coverage_suite.py) | [Both-child and dashboard assertions](../../tests/test_coverage_suite.py#L43), [setup failure](../../tests/test_coverage_suite.py#L61), [durability](../../tests/test_coverage_suite.py#L75), [difference exit](../../tests/test_coverage_suite.py#L95), [match and incomplete exits](../../tests/test_coverage_suite.py#L122). | All six tests passed; the same validation binds their outcomes to current sources. |

The revised [runner](../../core/entitlement_coverage.py) also maps directly to [default isolation](../../tests/test_entitlement_coverage.py#L302).
Its [missing-capture assertions](../../tests/test_entitlement_coverage.py#L323) bind incomplete profile coverage to the same mock boundary.
See [earlier mock validation](evidence/coverage-mock-20261103/validation.json) for the original execution counts and source hashes.
The [environment validation](evidence/ems2-environment-coverage-20261103/validation.json) binds current extension checks and source identities.

Runtime inventory: three existing coverage modules plus two new extension modules.
Both new modules have inspected direct assertion chains and matching passing execution in the extension validation.
Task configuration, launchers, documentation, provenance, and test files are supporting artifacts outside that runtime-module denominator.
Existing authorization code is unchanged and is not counted as a newly implemented permission behavior.

## Implementation and release proposal

- Implementation: local candidate adds only the bounded coverage helper, task configuration, launchers, tests, and evidence.
- Release proposal: no application deployment or migration acceptance is proposed by this record.
- Estimate: not applicable; the implementation stage is complete.
- Reversal: remove this helper and its task launchers through a scoped change. Retain claim-bearing evidence and immutable audit history.
- Bounded exploration: not applicable. The user directly requested implementation of the scoped automation.

## Sources and evidence limits

| Source | Identity | Authority and limit |
| --- | --- | --- |
| [Latest tooling request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input) | SHA-256 in [environment validation](evidence/ems2-environment-coverage-20261103/validation.json). | Authorizes all-coverage guidance and an EMS2 UAT-versus-PROD comparison. |
| [Environment contracts](evidence/ems2-environment-coverage-20261103/contracts.json) | Supplied PROD/UAT source hashes and routing identities. | Defines observed captures and context limitations, without enterprise requests. |
| [Combined supplied-response run](evidence/coverage-runs/all-coverage-20261103/result.json) | Child run bindings and actual aggregate outcome. | Missing captures prevent complete population claims. |
| [Automation user input](evidence/coverage-automation-20261103/user-input.md#exact-user-input) | SHA-256 `10c503fba499b7dfbcad08481293fcfd9cf0b108f692052bb9f5537a3d89ff57`. | Defines requested mapping, full discovered account scope, filtering, and FMO exception. |
| [Latest mock instruction](evidence/coverage-mock-20261103/user-input.md#exact-user-input) | SHA-256 `72e80490baec682cca54f4288496026105466d2e2b676c7d964bc72f135da887`. | Requires supplied responses as mock data; real environments are inaccessible in this session. |
| [Source contract inspection](evidence/coverage-automation-20261103/contracts.json) | Exact input hashes and source locators. | Describes supplied contracts; does not establish universal API support. |
| [Runtime suite](evidence/coverage-automation-20261103/unit-tests-all.log) | 800 discovered tests; 800 passed; zero failures, errors, or skips. | Optional Node integration was enabled through `WORKBENCH_CONNECTOR_INTEGRATION=1`. The final 47 coverage tests also passed. |
| [Earlier runtime suite](evidence/coverage-mock-20261103/unit-tests-all.log) | 802 discovered tests; 802 passed; zero failures, errors, or skips. | Predates the environment extension. Includes all 49 prior coverage tests. |
| [Environment extension checks](evidence/ems2-environment-coverage-20261103/coverage-tests.log) | 44 tests passed; zero failures, errors, or skips. | Includes all 22 new module tests and 22 affected semantic/source checks. No enterprise requests occurred. |
| [Wheel construction](evidence/coverage-automation-20261103/wheel-build.log) | Built `ai_sdlc_workbench-0.1.0-py3-none-any.whl`. | Build passed. This does not establish enterprise access. |
| [Supplied-response mock run](evidence/coverage-runs/mock-supplied-20261103/result.json) | Bound retained API responses and three production matrices. | No network acquisition. Full discovered population is accounted for, with unavailable captures visible. |
| [Historical enterprise preflight](evidence/coverage-runs/live-access-check-unsandboxed/result.json) | Earlier live mode; `TLS_ERROR`; zero compared accounts. | Retained failed evidence. The latest mock-only instruction supersedes its CA action. |

The earlier migration replay discovers 1,051 account IDs from 747 matrix accounts and 1,050 CES catalog accounts.
Only two accounts have paired captured responses. Both report differences, while 1,049 remain unassessed.
The final functional profile coverage rate is `null`.
All 23 baseline subjects and 786 scoped role/feature/action definitions occur in the CES capture.
The capture also has 130 additional role/feature/action definitions, six additional subjects, and 38 additional profile names.
One baseline profile name, `EMS2_ADMIN`, is missing from the catalog comparison and lacks matrix content evidence.
These observations do not establish missing production access or complete migration success.
Additional `Reports` and `FMID Reports` grants remain visible. Catalog membership discrepancies remain unassessed pending inheritance semantics.
The EMS2 environment comparison has its own population, inventory denominators, and [source context limits](evidence/ems2-environment-coverage-20261103/contracts.json).
It discovers 747 accounts. Two have comparable paired captures; both differ, and 745 remain unassessed.
User `1289935` retains 25 of 28 effective permissions, with three missing and 39 additional UAT permissions.
User `1481696` retains 24 of 29 effective permissions, with five missing and 40 additional UAT permissions.
Four of four assessed subject names are retained. The `X_RATANONE` subject inventory remains unassessed.
All 24 assessed role names are retained. Role inventories for the other two entities remain unassessed.
These partial inventories cannot establish complete subject or role coverage.
Its results remain separate from the migration metrics in the [combined dashboard](evidence/coverage-runs/all-coverage-20261103/index.html).

## Unknowns and blockers

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Supplied responses cover only two paired users. | [Mock run](evidence/coverage-runs/mock-supplied-20261103/result.json). | The other 1,049 discovered accounts remain unassessed. | unknown | Preserve the sample limit and unavailable accounts; do not fabricate responses. |
| Data restriction definitions are incomplete. | [Candidate open questions](../../knowledge/candidates/security/KT-ces-migration-parity.md#open-questions). | Full data-profile equality remains unassessed. | unknown | Obtain authoritative EMS2 field/value definitions. |
| Discovery sources are bounded. | [Contract inspection](evidence/coverage-automation-20261103/contracts.json). | Accounts absent from both matrices and the CES catalog are outside demonstrated discovery coverage. | unknown | Supply an authoritative complete account inventory when available. |
| Additional grants and source discrepancies need review. | [Mock differences](evidence/coverage-runs/mock-supplied-20261103/differences.csv). | Exact equal-content acceptance remains unresolved. | unknown | Review mappings, empty profiles, and catalog membership semantics. |

## Stage evidence and completion

| Stage | Required evidence | Current result | Limit and next action |
| --- | --- | --- | --- |
| Scope and impact | Inspected callers, imports, and configuration boundaries. | Complete for five coverage modules, task configurations, and launchers. | Existing application behavior was not changed. |
| Runtime verification | Environment comparison, suite routing, report, recovery, and mock assertions. | All 44 affected tests passed. | Full-suite rerun did not start because automatic permission review timed out. Earlier 802-test evidence remains separately bound. |
| Controlled E2E | HTTP acquisition through both comparisons and retained artifacts. | Controlled runner tests passed. | Synthetic services and accounts do not establish enterprise reachability. |
| Earlier migration mock replay | Full discovered inventory and captured comparisons. | INCOMPLETE, with 1,049 unassessed accounts. | This result retains its earlier source binding. |
| Environment and suite extension | Both child reports, declared populations, inventory comparisons, and aggregate outcome. | See [retained extension validation](evidence/ems2-environment-coverage-20261103/validation.json). | Missing or invalid captures remain unassessed; no enterprise requests run in this session. |
| Enterprise execution | Latest execution instruction. | Outside scope for this session. | Retain the historical TLS failure; make no further live attempts. |
| Report browser review | Rendered dashboard and individual reports. | Unavailable: browser policy blocked local-file navigation. | Static report and link checks passed. Automatic browser opening remains unverified. |

## Requested decision and actual disposition

- Requested decision: use the documented commands and review each comparison within its declared mock scope.
- Authorized decision owner: unknown.
- Actual implementation authorization: [initial script request](evidence/coverage-automation-20261103/user-input.md#exact-user-input) and [environment extension request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input).
- Implementation status: complete local candidate, identified by the retained source binding and subsequent scoped commit.
- Intent review: user-sourced mapping and FMO clarification recorded; candidate knowledge publication remains pending.
- Execution outcome: supplied-response replay accounts for the discovered population, but only two users have paired responses.
- Execution boundary: default mock verification requires no enterprise access. Historical TLS failure remains retained evidence.
- Business acceptance: pending. No release, publication, deployment, or migration acceptance is recorded.

Matching implementation and controlled tests do not supply human business approval.
