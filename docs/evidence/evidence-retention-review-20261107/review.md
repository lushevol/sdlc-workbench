# Task and evidence retention review

**Retain critical evidence once. Rule updates are authorized; historical cleanup still requires a scoped review.**
Owner: Workbench maintainer. Action: Apply the rules below to new evidence and select historical cleanup batches separately.
Evidence: [follow-up request](user-followup.md#exact-user-input), [current UI stage](../../../tasks/ui-test-coverage-20261022/08-execution-stage.md), and the measured inventory below.

The [initial request](user-input.md) requires classification before historical changes.
The [latest request](user-followup.md) authorizes rules for critical content and reuse without duplication.
Task categories remain proposals. No historical artifact was deleted, moved, or untracked.

## Scope and confidence

Review date: 7 November 2026, Asia/Singapore.
Inspected Workbench revision: `e7ae8ecfa6a1fa6277d2af47e8536818214fa60b`.
The scan used `git ls-files` and filesystem metadata under `tasks/`, `docs/evidence/`, and `evidence/`.
It counted regular-file bytes without following symlinks. Values use decimal MB and GB.
These values do not measure recoverable disk space or Git object storage.
Local ignored files are outside the Git revision binding.

Confidence is **HIGH** for measured sizes, existing ignore rules, and named reference consumers.
Confidence is **MEDIUM** for proposed task categories. Recorded stage states do not establish current business acceptance or deployment.
The review did not resolve every artifact reference. No candidate below is a verified safe deletion list.

Initial unrelated work remains outside this review:

- Untracked `core/release-report/`.
- Two untracked captures under [CES supplied material](<../../../tasks/ces-entitlement-migration-20261102/ces migration/>).

The captures are `application_tile_1105.csv` and `login-response.json`, totaling 231,500 bytes.
Do not automatically stage or ignore these supplied inputs. Their retained source role needs review first.

## Measured inventory

Counts exclude symlinks and this review's new notes. They describe the initial inventory, before the rule update.

| Area | Tracked regular files | Tracked bytes | Ignored regular files | Ignored bytes |
| --- | ---: | ---: | ---: | ---: |
| UI coverage task | 42,395 | 1.439 GB | 7,223 | 18.783 GB |
| Portal session task | 6,234 | 184.29 MB | 7 | 0.16 MB |
| CES migration umbrella | 927 | 11.85 MB | 252 | 46.22 MB |
| Other five tasks | 285 | 7.75 MB | 0 | 0 |
| Task guide | 1 | 0.05 MB | 0 | 0 |
| Root `docs/evidence/` | 894 | 40.42 MB | 0 | 0 |
| Root `evidence/` | 168 | 1.75 MB | 0 | 0 |

Tasks also contain 24,963 tracked symlinks and 23,120 ignored symlinks.
Many already consolidate screenshots and source bindings. Removing their targets can break several consumers.

The [5 November review](../task-evidence-growth-20261105/review.md#confirmed-causes) measured trace copying across three output categories.
Its duplicate-byte findings are historical measurements. This review did not repeat the complete payload hash scan.
Existing capture prevention changes already reduce future duplication. Historical cleanup remains a separate decision.

## Proposed task working set

These categories control attention. They do not authorize moving, ignoring, merging, or deleting task folders.

| Task | Proposed category | Evidence and remaining work |
| --- | --- | --- |
| [CES migration](../../../tasks/ces-entitlement-migration-20261102/evidence/index.md) | Active: keep prominent | Migration umbrella. [Frontend review](../../../tasks/ces-entitlement-migration-20261102/10-change-review-frontend-adapters.md) retains consumer compatibility and rollout questions. Live parity remains incomplete. |
| [Portal session](../../../tasks/portal-background-session-20261019/evidence/index.md) | Active: keep prominent | [Six open gaps](../../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md) retain behavior, remote UAT, and deployment questions. Historical release assessments have bounded source identities. |
| [UI coverage](../../../tasks/ui-test-coverage-20261022/08-execution-stage.md) | Local execution complete; triage and policy review open | Recorded outcomes: 420 passes, 72 failures, two blockers, and 27 exclusions. Business acceptance remains unestablished. |
| [Single UI SDK migration](../../../tasks/single-ui-sdk-ces-migration-20261101/10-change-review.md) | Implementation complete; acceptance follow-up open | SDK 3.0.0 and controlled checks exist. Live parity and actual consumer compatibility remain unproved. CES consumes these records. |
| [CES frontend impact](../../../tasks/ces-frontend-impact-20261105/05-solution-design.md) | Historical design reference | Proposed design only. Later implementation belongs to the CES umbrella. Remove from routine reading; retain its design provenance. |
| [EMS3 entitlement review](../../../tasks/ems3-entitlement-review-20261027/07-code-review.md) | Historical baseline; reconcile findings when relevant | Fifteen historical findings and dependency failures remain evidence. Their applicability to newer revisions needs reconciliation. |
| [Release Clinic HTML](../../../tasks/release-clinic-html-20261020/09-parity-review.md) | Completed maintenance record | Retain parity evidence and the shared upstream defect reproduction. Upstream follow-up remains separate. |
| [SDLC task intake](../../../tasks/sdlc-task-intake-20261019/09-verification.md) | Completed maintenance record | Retain request, final checks, packaging boundaries, and meaningful evaluation failures. No routine investigation is proposed. |

## Evidence categories

| Category | Examples | Proposed treatment |
| --- | --- | --- |
| Current decision records | Intake, current stage, canonical cases, gap record, short evidence index | Keep tracked and prominent. Read these first. |
| Direct supporting evidence | Assertions, execution results, run bindings, required screenshots, baseline comparisons, meaningful failures | Keep tracked or in approved durable storage. Link from current records. |
| Protected provenance | [Knowledge manifest](../../../evidence/knowledge/manifest.yaml), registered snapshots, [audit events](../../../evidence/knowledge/audit/), relocation and cleanup manifests | Preserve bytes and identities. Do not blanket-ignore. |
| Historical supporting records | Older source reviews, maintenance checks, superseded but meaningful attempts | Keep available. Skip routine reading unless a current claim needs them. |
| Optional generated views | New HTML exports, repeated full galleries, presentation previews | Prefer existing ignored runtime storage for future exports. Keep canonical evidence durable. |
| Local runtime material | Browser installations, dependencies, caches, build outputs | Already largely ignored. Review active consumers before disk cleanup. |
| Redundant or empty material | Proven duplicate copies, empty logs without unique evidence value | Review exact paths and references before an authorized cleanup. |

The [task retention rules](../../../tasks/README.md#evidence-priorities-and-cleanup) already distinguish necessary, important, and unimportant evidence.
The update clarifies these existing procedures. It adds no retention service, automatic deletion, or deduplication engine.

## Rule update

The [critical evidence policy](../../../tasks/README.md#critical-evidence-and-reusable-payloads) is the canonical rule for tasks and harness maintenance.
Keep only content needed for decisions, required assertions, reproduction, recovery, material failures, or protected provenance.
Use one owning document, one evidence inventory, shared run bindings, and canonical payload references.
Separate capture and execution identities even when their stored bytes match.

Routine successful commands need compact receipts. Full logs remain required when they support a claim or applicable procedure.
Optional exports, repeated clean diagnostics, caches, and installations stay in ignored runtime storage.
Required evidence must remain durable before a case completes or runtime cleanup starts.
Recoverable source can use exact verified Git locators. Preserve source bytes that cannot be retrieved later.

The [root ignore rule](../../../.gitignore) now excludes optional task HTML bundles:

```gitignore
/tasks/*/evidence/**/html-report/
```

This pattern does not ignore canonical case results, source bindings, decision HTML, or screenshot directories elsewhere.
Already tracked artifacts remain tracked.
The historical audit ignore file also excludes `playwright-artifacts/`. That directory can now hold canonical reporter attachments.
The [E2E guide](../../../e2e/README.md#screenshot-audit-runs) requires checking inherited ignores and selecting an unignored output location.
The existing historical ignore file remains unchanged to avoid exposing duplicate legacy outputs as new files.

The [release assessment skill](../../../.agents/skills/release-confidence/SKILL.md) now uses one living assessment during active review.
Its [reporting guide](../../../.agents/skills/release-confidence/references/reporting.md) also reuses one current validation record.
Separate successors require a frozen decision baseline. Consequential failures and protected manifests remain retained.

Affected scope: project instructions, task policy, browser and E2E guides, release reporting instructions, and initialized workspace defaults.
Runtime risk is low because executable code is unchanged.
The consequential boundary is hiding required evidence. The narrow pattern and keep/ignore checks address that risk.

## Proposed review batches

### R1: UI report exports and trace copies

This batch offers the largest potential benefit.
The current [UI index](../../../tasks/ui-test-coverage-20261022/evidence/index.md) consumes both current and historical report versions.

| Candidate cohort | Measured volume | Proposed decision and constraint |
| --- | ---: | --- |
| [Reports 002–006](../../../tasks/ui-test-coverage-20261022/evidence/audit-run-20261022/) | 456.75 MB tracked | Select required baselines before consolidating generated views. Report 006 is current. Report 001 is explicitly immutable and outside this candidate cohort. |
| [Application runs](../../../tasks/ui-test-coverage-20261022/evidence/audit-run-20261022/application/), `cases/` | 800.74 MB tracked; 6.198 GB ignored | Keep assertion records and canonical step screenshots. Review repeated trace attachments separately. |
| Application runs, `playwright-artifacts/` | 6.204 GB ignored | Compare payload hashes and consumers before selecting canonical copies. Required failure or timing evidence must remain available. |
| Application runs, `html-report/` | 9.72 MB tracked; 6.365 GB ignored | Optional exports can duplicate captures. Do not remove evidence that exists only in an export. |

These cohorts overlap by payload, but their directory byte totals are separate.
They are not estimates of safe savings.
Report 002 supports screenshot diagnosis. Reports 004 and 005 have generation and validation consumers.
Different report versions can preserve distinct attempts and conclusions.

The [audit ignore file](../../../tasks/ui-test-coverage-20261022/evidence/audit-run-20261022/.gitignore) already excludes runner artifacts and HTML report outputs.
The [root ignore file](../../../.gitignore) excludes new trace ZIPs, with three explicit historical exceptions.
Additional ignore rules alone cannot resolve this accumulation.

Proposed choices: review report baselines first; review local trace copies first; defer this batch; another answer.

**Answer:**

### R2: Portal presentation material and small clutter

The portal task is much smaller. Start with presentation evidence before behavior evidence.

- [Report clarity](../../../tasks/portal-background-session-20261019/evidence/report-clarity-20261029/), impact-priority, readable-issues, and collapsed-details screenshots total 6.30 MB.
- Thirteen empty logs add navigation clutter. Some remain registered in execution manifests.
- Equal-byte regular files suggest 28.06 MB of duplicate overhead. This is an upper bound requiring consumer review.

Presentation folders also contain active scripts and manifests. Do not ignore whole folders.
Different cases can have identical screenshots while retaining different assertions and provenance.
Keep those case meanings if canonical image references are later consolidated.

Proposed choices: review presentation screenshots; keep this batch unchanged; another answer.

**Answer:**

### R3: Root evidence and historical task visibility

Root evidence totals approximately 42.17 MB. Most supports maintenance history or knowledge provenance.
It is a lower storage priority than the UI audit.

Keep [knowledge provenance](../../../evidence/knowledge/README.md), registered raw sources, audit events, findings, and migration manifests.
The [ingestion harness](../../../core/ingestion/harness.py) and [governance validator](../../../core/governance/validation.py) consume those contracts.

Treat most `docs/evidence/` as supporting history, outside the routine reading set.
Existing [review documents](../../reviews/) still cite historical checks and failures.
Passing current tests cannot recreate their historical observations.

Potential small deduplication examples remain subject to reference repair:

- [Shared graph screenshot](../service-dependencies-trace-comparison-20261016/06-shared-after.png) and `12-parent-local-after.png` have identical bytes.
- [Doctor result](../workbench-capability-dependency-review-20261103/doctor.json) matches `dependency-setup-maintenance-20261103/current-all-check.json`.

The largest root cohort is [conversation improvement evidence](../conversation-improvements-implementation-20261030/), totaling 20.55 MB.
Its graph `attempt01` receipt explains a failed assertion. Its filename does not make it disposable.

Both root Draw.io files remain editable design sources with [navigation consumers](../../diagrams/workbench/README.md).
The [distribution manifest](../../../MANIFEST.in) excludes project evidence from generated workspaces, apart from selected guides.
This evidence therefore does not inflate shipped workspace contents.

Proposed choices: keep history but skip routine reading; review named duplicate files; another answer.

**Answer:**

## Ignore behavior and change boundary

Ignoring a path stops future untracked files from appearing in normal Git status.
It does not untrack existing files or remove local bytes. Removing tracked files also leaves prior Git history intact.

Existing rules already exclude `.workbench/`, dependencies, browser artifacts, build outputs, and many optional traces.
The [CES verifier rules](../../../tasks/ces-entitlement-migration-20261102/spring-verifier/.gitignore) also exclude local libraries, reports, targets, and private configuration.
No additional blanket ignore rule is recommended now.
Do not ignore whole task folders, root evidence, PNG files, JSON files, or logs by extension.

After a batch is selected, prepare exact paths, hashes, current consumers, retained canonical paths, and recovery limits.
The user can then review the concrete retention change.
An authorized cleanup must record removals, repair active references, and validate retained hashes.

## Checks and limits

The initial inventory reconciled regular-file totals and resolved all 34 original review links.
The rule update passed these scoped checks:

| Check | Outcome |
| --- | --- |
| `.venv/bin/python -m unittest discover -s tests -p test_workspace_layout.py -v` | 22 tests passed; zero failures, errors, or skips. |
| Skill Creator `quick_validate.py .agents/skills/release-confidence` | Valid skill structure. Agent adherence remains untested. |
| Isolated Git ignore probes | 18 checks passed. Critical case files and three historical trace exceptions stay visible. |
| Added guide links | Ten links and their heading anchors resolved. |
| `.venv/bin/python -m pip wheel . --no-deps --no-build-isolation --wheel-dir /tmp/workbench-evidence-policy-wheel-20261107` | Wheel built without dependency acquisition. |
| Installed wheel outside this checkout | Six shipped files matched source bytes. Three generated-workspace ignore checks passed. |
| Installed `ai-sdlc --workspace PATH validate` | Generated workspace returned `VALID`. Project evidence remained excluded. |
| Diff and note checks | Whitespace, local links, and writing-review metadata passed. |

Built wheel SHA-256: `038cfb19a2f4e91af3774c2389bda1e3cc35aa4655b502917424a8e4fb05bf85`.
The complete runtime suite and business executions were not run. Executable code is unchanged.
The review did not inspect every payload or establish current production behavior.
Existing historical evidence, business task records, and application code remain unchanged.
The completed rule stage is ready for its required Git commit.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
