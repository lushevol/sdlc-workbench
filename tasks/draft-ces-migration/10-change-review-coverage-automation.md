---
artifact_kind: change-request
id: CES-COVERAGE-AUTOMATION
version: 2
status: draft
owner: unknown
source_refs: [USER-COVERAGE-20261103, USER-MOCK-20261103, CES-COVERAGE-CASES, KT-ces-migration-parity, COVERAGE-REPLAY, COVERAGE-LIVE-PREFLIGHT]
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

# CES coverage automation: stage review

> **The default launcher verifies supplied mock responses; complete migration parity remains unassessed.**
> Action: review the [mock report](evidence/coverage-runs/mock-supplied-20261103/report.html) and preserve unavailable comparisons.
> Consequence: two paired user captures cannot establish equality for the complete account population.
> Owner: unknown. Evidence: [mock execution instruction](evidence/coverage-mock-20261103/user-input.md#exact-user-input).

## Request and source facts

- Requester: the user; named operational owner remains unknown.
- Current baseline: [prior source-understanding stage](01-intake.md#migration-data-coverage-understanding) at Git `6854a6b63c323fd9c4eb15bb27725e49f302f712`.
- Request source: [exact automation clarification](evidence/coverage-automation-20261103/user-input.md#exact-user-input).
- Latest execution boundary: [use supplied API responses as mock data](evidence/coverage-mock-20261103/user-input.md#exact-user-input).
- Environment limit: real environments are inaccessible from this session. No further enterprise access attempts are authorized by this stage.
- Rationale: compare mapped entitlement definitions and all discovered accounts through one executable command.
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
The revised default passed all 802 runtime tests, including 49 coverage tests, with zero failures, errors, or skips.
The revised wheel built and installed outside this checkout. Its default mode equals `replay`.
The separate [verification evidence](evidence/coverage-mock-20261103/validation.json) binds these results to current source hashes.
Windows launcher execution remains untested. Its documented arguments match the supported command.

## Proposed change

All additions below are implemented in the local candidate.

| Aspect | Before | Implemented addition | Evidence |
| --- | --- | --- | --- |
| Entitlement comparison | Static source inspection and sample counts. | Compare scoped application, entitlement, feature, and action relationships. | [normalization and comparison](../../core/entitlement_reconciliation.py#L88). |
| Account collection | Two supplied effective-user examples. | Expand matrix cells and catalog memberships, then compare every discovered account against available stored responses. | [source parsing](../../core/entitlement_sources.py#L130) and [runner](../../core/entitlement_coverage.py#L377). |
| Difference review | Manual comparison. | Retain matched counts and JSON details; filter matches from active HTML and CSV differences. | [report completion](../../core/entitlement_coverage.py#L304). |
| Repeat execution | No combined launcher. | Default to supplied-response replay, save checkpoints, and validate resume identity. | [entry point](../../core/entitlement_coverage.py#L483) and [launchers](coverage/README.md#run-both-checks). |

## Scope and affected artifacts

| Artifact | Version or identity | Effect | Risk and basis | Owner |
| --- | --- | --- | --- | --- |
| Three Python helper modules | [Exact mock hashes](evidence/coverage-runs/mock-supplied-20261103/binding.json). | Add scoped source acquisition, semantic comparison, and reporting. | Moderate; source incompleteness or scope errors could misstate coverage. | unknown |
| [Task configuration](coverage/config.json) | SHA-256 in the run binding. | Keep tenant endpoints, entity mappings, exclusions, and workbook paths outside shared defaults. | Moderate; mappings control comparison meaning. | unknown |
| [Canonical cases](06-test-cases.md) | Version 2. | Define ten comparison, failure, recovery, and mock-isolation cases. | Low; actual outcomes remain separate. | unknown |
| Four test modules | [Earlier suite](evidence/coverage-automation-20261103/unit-tests-all.log) and [mock validation](evidence/coverage-mock-20261103/validation.json). | Preserve 47 earlier checks and add default mock-isolation assertions. | Low; controlled services limit live claims. | unknown |
| [Candidate intent](../../knowledge/candidates/security/KT-ces-migration-parity.md) | Version 1; [audit](../../evidence/knowledge/audit/AUD-20261103-KT-ces-migration-parity-v1.yaml). | Preserve user clarification and source provenance. | Candidate only; publication remains pending. | unknown |

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

No existing Workbench CLI parser or application caller was changed.
Both task launchers invoke the installed module entry point.

## Options and consequences

| Option | Consequence | Evidence | Decision |
| --- | --- | --- | --- |
| Run replay against supplied examples. | Checks supplied captures and retains unavailable accounts without enterprise access. | [Mock run](evidence/coverage-runs/mock-supplied-20261103/result.json). | Selected by the latest user instruction and default launcher. |
| Run live collection. | Requires a different authorized environment and its own evidence boundary. | [Historical preflight](evidence/coverage-runs/live-access-check-unsandboxed/result.json). | Outside this session. No credential or CA action is requested. |
| Accept catalog counts as complete migration proof. | Would omit assignments, extra grants, unavailable accounts, and data restrictions. | [Candidate evidence limits](../../knowledge/candidates/security/KT-ces-migration-parity.md#evidence-limits). | Unsupported by current evidence. |

## Proposed acceptance and validation

The automation scope contains eight criteria and ten canonical case definitions.
The initial seven criteria retain their inspected source and direct assertion chains.
The eighth criterion adds the user-required default mock boundary.
The 49 focused tests cover supported parser, transport, comparison, report, recovery, and default mock boundaries.
The revised default passed no-network, no-credential-loading, and explicit mock-label assertions.
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

Definition denominator: 8 criteria and 10 readable cases.
Assertion denominator: 8 criteria, each with inspected direct assertion chains.
The default mock criterion passed its direct assertions in the current runtime suite.
Execution denominator: 49 coverage tests; all 49 passed against their bound sources.
The ten readable cases are specifications. They are not ten separately recorded enterprise executions.

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

The automation implementation scope covers 8 of 8 criteria, with source, assertions, and retained execution.
This statement does not establish complete business mappings, full data access equality, or 100% production migration conformance.

### Code-change-to-test matrix

| Changed runtime unit | Direct assertion chains | Execution and denominator |
| --- | --- | --- |
| [entitlement_reconciliation.py](../../core/entitlement_reconciliation.py) | [Mapping](../../tests/test_entitlement_reconciliation.py#L65), [membership](../../tests/test_entitlement_reconciliation.py#L122), [set equality](../../tests/test_entitlement_reconciliation.py#L188). | 15 focused tests passed. |
| [entitlement_sources.py](../../core/entitlement_sources.py) | [XLSX identity cells](../../tests/test_entitlement_sources.py#L58), [collection credential omission](../../tests/test_entitlement_sources.py#L83), [TLS preservation](../../tests/test_entitlement_sources.py#L188). | 12 focused tests passed. |
| [entitlement_coverage.py](../../core/entitlement_coverage.py) | [Controlled HTTP runner](../../tests/test_entitlement_coverage.py#L193), [resume](../../tests/test_entitlement_coverage.py#L345), [new-feature regression](../../tests/test_entitlement_coverage_sources.py#L83), [source conflict reporting](../../tests/test_entitlement_coverage_sources.py#L113). | 15 integration tests and 7 source-consistency tests passed. |

The revised [runner](../../core/entitlement_coverage.py) also maps directly to [default isolation](../../tests/test_entitlement_coverage.py#L302).
Its [missing-capture assertions](../../tests/test_entitlement_coverage.py#L323) bind incomplete profile coverage to the same mock boundary.
See [mock validation](evidence/coverage-mock-20261103/validation.json) for current execution counts and source hashes.

Changed runtime denominator: three new modules; all three have direct assertion chains.
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
| [Automation user input](evidence/coverage-automation-20261103/user-input.md#exact-user-input) | SHA-256 `10c503fba499b7dfbcad08481293fcfd9cf0b108f692052bb9f5537a3d89ff57`. | Defines requested mapping, full discovered account scope, filtering, and FMO exception. |
| [Latest mock instruction](evidence/coverage-mock-20261103/user-input.md#exact-user-input) | SHA-256 `72e80490baec682cca54f4288496026105466d2e2b676c7d964bc72f135da887`. | Requires supplied responses as mock data; real environments are inaccessible in this session. |
| [Source contract inspection](evidence/coverage-automation-20261103/contracts.json) | Exact input hashes and source locators. | Describes supplied contracts; does not establish universal API support. |
| [Runtime suite](evidence/coverage-automation-20261103/unit-tests-all.log) | 800 discovered tests; 800 passed; zero failures, errors, or skips. | Optional Node integration was enabled through `WORKBENCH_CONNECTOR_INTEGRATION=1`. The final 47 coverage tests also passed. |
| [Current runtime suite](evidence/coverage-mock-20261103/unit-tests-all.log) | 802 discovered tests; 802 passed; zero failures, errors, or skips. | Includes all 49 coverage tests. Local HTTP fixtures use controlled accounts and responses. |
| [Wheel construction](evidence/coverage-automation-20261103/wheel-build.log) | Built `ai_sdlc_workbench-0.1.0-py3-none-any.whl`. | Build passed. This does not establish enterprise access. |
| [Supplied-response mock run](evidence/coverage-runs/mock-supplied-20261103/result.json) | Bound retained API responses and three production matrices. | No network acquisition. Full discovered population is accounted for, with unavailable captures visible. |
| [Historical enterprise preflight](evidence/coverage-runs/live-access-check-unsandboxed/result.json) | Earlier live mode; `TLS_ERROR`; zero compared accounts. | Retained failed evidence. The latest mock-only instruction supersedes its CA action. |

The replay discovers 1,051 account IDs from 747 matrix accounts and 1,050 CES catalog accounts.
Only two accounts have paired captured responses. Both report differences, while 1,049 remain unassessed.
The final functional profile coverage rate is `null`.
All 23 baseline subjects and 786 scoped role/feature/action definitions occur in the CES capture.
The capture also has 130 additional role/feature/action definitions, six additional subjects, and 38 additional profile names.
One baseline profile name, `EMS2_ADMIN`, is missing from the catalog comparison and lacks matrix content evidence.
These observations do not establish missing production access or complete migration success.
Additional `Reports` and `FMID Reports` grants remain visible. Catalog membership discrepancies remain unassessed pending inheritance semantics.

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
| Scope and impact | Inspected callers, imports, and configuration boundaries. | Complete for the three helper modules and task launchers. | Existing application behavior was not changed. |
| Runtime verification | Parser, comparison, transport, report, recovery, and default mock assertions. | All 49 coverage tests and 802 full-suite tests passed. | Revised-default source identities remain bound separately in mock validation. |
| Controlled E2E | HTTP acquisition through both comparisons and retained artifacts. | Controlled runner tests passed. | Synthetic services and accounts do not establish enterprise reachability. |
| Supplied-response mock replay | Full discovered inventory and captured comparisons. | INCOMPLETE, with 1,049 unassessed accounts. | Missing captures remain visible; mock mechanics and migration parity are separate conclusions. |
| Enterprise execution | Latest execution instruction. | Outside scope for this session. | Retain the historical TLS failure; make no further live attempts. |
| Browser execution | Native UI or application journey assertions. | Not applicable to this command and static report change. | Browser opening is a launcher convenience, not application behavior verification. |

## Requested decision and actual disposition

- Requested decision: review supplied-response differences within the declared mock scope.
- Authorized decision owner: unknown.
- Actual implementation authorization: [user's explicit script request](evidence/coverage-automation-20261103/user-input.md#exact-user-input).
- Implementation status: complete local candidate, identified by the retained source binding and subsequent scoped commit.
- Intent review: user-sourced mapping and FMO clarification recorded; candidate knowledge publication remains pending.
- Execution outcome: supplied-response replay accounts for the discovered population, but only two users have paired responses.
- Execution boundary: default mock verification requires no enterprise access. Historical TLS failure remains retained evidence.
- Business acceptance: pending. No release, publication, deployment, or migration acceptance is recorded.

Matching implementation and controlled tests do not supply human business approval.
