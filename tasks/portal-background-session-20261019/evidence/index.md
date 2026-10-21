---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Portal session: evidence and reading guide

> **Action required: investigate the corrected Cashflow Blotter condition.**
> Consequence: UAT cause confirmation and idle-timeout acceptance remain blocked.
> Owner: unknown application owner. Action: correlate blotter requests, `/sso/extend`, and access expiry.
> Evidence: [current UAT inquiry](../change-review.md#uat-timeout-inquiry-21-october-2026).
> The dashboard explanation is withdrawn. The blotter extension hook alone does not establish recurring renewal or causation.

> **🔴 Action required: review the two P2 regressions and decide the remaining recovery scope.**
> Consequence: active work or a fresh session can end. Acceptance remains open.
> Owner: unknown application owner; user for scope decisions.
> Evidence and next actions: [current decisions](../change-review.md#unknowns-and-blockers) and [confirmed findings](../code-review-minor-20261021.md#review-findings).
> Local controlled results do not establish production frequency or release approval.

## Start here

| Read | Purpose |
| --- | --- |
| **1. [Current stage](../change-review.md#read-this-first)** | 👤 Key points, pending decisions, and blocked actions. |
| [UAT timeout inquiry](../change-review.md#uat-timeout-inquiry-21-october-2026) | Corrected background Cashflow Blotter condition, possible extension path, and prior review limits. |
| **2. [Current review](../code-review-minor-20261021.md#read-this-first)** | 🔴 Two P2 regressions, 🟡 one P3 issue, and 🟠 inherited delayed recovery. |
| **3. [Execution report](../test-execution-report.md#assertions-and-outcomes)** | Browser outcomes: five passes, fourteen failures, one diagnostic failure, and two observations. |
| **4. [Canonical cases](../test-cases.md#catalog-navigation)** | Setup, Gherkin, numbered steps, assertions, and retained results. |

## UAT timeout inquiry evidence: 21 October 2026

| Evidence | Supported claim and limit |
| --- | --- |
| [User correction](uat-timeout-inquiry-20261021/blotter-correction.txt), [original answers](uat-timeout-inquiry-20261021/user-request.txt) | Latest minor branch; untouched background tab; Cashflow Blotter supersedes Dashboard. No retained UAT capture exists. |
| [Corrected source receipt](uat-timeout-inquiry-20261021/blotter-analysis.json) | Blotter route, installed extension hook, notification limits, source hashes, and downgraded causal confidence. |
| [Historical dashboard receipt](uat-timeout-inquiry-20261021/analysis.json) | Preserved at Workbench `3257b6f8736b88e47f0f239a8653dfa8f1862c0a`. Its incident-specific dashboard explanation is withdrawn. |
| [Prior integration risk](../code-review.md#review-findings), [impact boundary](../impact-analysis.md#user-view) | API completion can renew outside activity and visibility checks. Representative embedded execution remained open. |
| [Local idle execution](minor-branch-rerun-20261020/browser/minor-idleLogout-20261020T143628/artifacts/result.json#L106) | Dialog appeared with shortened local lifetimes. This result does not establish representative embedded blotter or UAT behavior. |

## Current review evidence: 21 October 2026

| Evidence | Supported claim and limit |
| --- | --- |
| [Inputs](code-review-refresh-20261021/inputs.json), [export binding](code-review-refresh-20261021/execution-setup.json) | Exact baseline, head, authorization, dependencies, and frozen intake hash. |
| [Paired reconciliation](code-review-refresh-20261021/summary.json) | Twelve executions cover six paired conditions. Characterization passes can demonstrate defects. |
| [User questions](code-review-refresh-20261021/user-clarification.txt), [answers](code-review-refresh-20261021/clarification.json) | Conditional active cutoff, response aborts, inherited recovery, and timer impact. |
| [Full Jest](code-review-refresh-20261021/suite-suite-suite/run.json), [compiler](code-review-refresh-20261021/types-corrected/run.json) | 116 suites and 413 runner passes, including one expected failure. Compiler passes. |
| [Integrity](code-review-refresh-20261021/integrity.json) | Source, refs, staged content, intake, and pre-existing cache were preserved during review. |
| [Earlier document checks](code-review-refresh-20261021/document-validation-final.json), [clarity checks](document-clarity-20261021/validation.json) | Separate validation stages. Full ASD review remains pending. |

## Earlier stages and historical documents

**📚 Historical documents describe their recorded revisions. They do not establish the current branch status.**

| Stage or document | Source and purpose | Current navigation |
| --- | --- | --- |
| [Frozen intake](../intake.md) | Original issue; Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. | [Current stage](../change-review.md). |
| [Original verification](../verification.md) | Original background failure and assertion limits; MFE `f025513f`, BFF `85d7cc03`. | [Original events](portal/run-001/browser/browser-events-001.json), [source receipt](source-inspection.json). |
| [Earlier review](../code-review.md), [impact](../impact-analysis.md), [coverage](../coverage.md) | Broader correction stage, including MFE `4da985a`; distinct source and verification evidence. | [Retained source inventory](correction-20261020/source-inventory.json), [exact diff](post-change-review-20261020/code-review/change.diff). |
| Reduced-branch browser execution | Runtime `6d4c37c`; tests `7a504c1`; 22 outcomes and separate probes. | [Manifest](minor-branch-rerun-20261020/browser-manifest.json), [integrity](minor-branch-rerun-20261020/integrity-review.json), [report](../test-execution-report.md). |
| Test-only repair and reassessment | Test commit `6e34da3`; original runtime unchanged. | [Repair summary](baseline-reassessment-20261021/test-repairs/repair-summary.json), [commit binding](baseline-reassessment-20261021/commit-binding.json), [progress](baseline-reassessment-20261021/progress.json). |
| Earlier failed checks | Initial runner error and compiler failures remain useful evidence. | [Runner error](baseline-reassessment-20261021/full-unit/run.json), [initial review](code-review-20261021/inputs.json). Latest results appear above. |
| Reorganized Robot modules | Test-engine `975af64`; offline checks pass. Business execution is `NOT_RUN`. | [Source bindings](../test-cases.md#current-robot-and-javascript-source), [offline checks](robot-case-modules-20261021/offline-checks.json). |
| [Authentication baseline](authentication/ARCH-authentication-runtime-baseline.md) | Preserved source investigation. Earlier internal paths require the migration map. | [Migration map](../../../evidence/knowledge/migration-20261020/cleanup.json). |

### Historical source references

Five source links in the preserved coverage report refer to replaced or removed checkout lines.
Use these exact retained diff locations for MFE `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`.

| Historical source locator | Retained local equivalent |
| --- | --- |
| `sessionLifecycle.test.tsx:779` | [Lifecycle assertion](post-change-review-20261020/code-review/change.diff#L969). |
| `Timeout/common/useController.ts:127` | [Timeout controller](post-change-review-20261020/code-review/change.diff#L135). |
| `renewalCompletion.test.tsx:127` | [Completion assertion](post-change-review-20261020/code-review/change.diff#L381). |
| `renewalCompletion.test.tsx:151` | [Rejection and retry assertion](post-change-review-20261020/code-review/change.diff#L405). |
| `relogin.response.ts:1` | [Relogin response helper](post-change-review-20261020/code-review/change.diff#L733). |

## Provenance, screenshots, and cleanup history

[Raw source identities](../../../evidence/knowledge/manifest.yaml) retain revisions, snapshot hashes, and stable source IDs.
The [candidate requirement](../../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains version 4 with pending publication review.
The [governance findings](../../../evidence/knowledge/findings/GF-session-renewal-verification-gates.md) retain execution and policy boundaries.

[Browser case captures](../test-execution-report.md#browser-evidence-bindings) retain run-specific context and limits.
The [Edge smoke](browser-final/edge/manifest.json) is a synthetic tooling check.
The [Sign In image](portal/run-001/reviews/sign-in-context.jpg) has unresolved capture time and phase.
Neither image establishes business unit-test execution or a thirty-minute returned-page result.

[Report consolidation](report-consolidation-20261020.json), [earlier cleanup](manifest.json), and [relocation map](organization-20261020/relocation-map.json) retain prior removal and recovery records.
This clarity revision removes repeated document prose. It deletes no evidence files or historical reports.
