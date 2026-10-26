---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# UI coverage evidence

> **Critical conclusions: Review required before business acceptance**
>
> **Review the final local results before business acceptance.**
> Action: Triage retained failures and definition limits. Consequence: Local execution cannot establish deployed business acceptance.
> Owner: unknown. Evidence: The [current audit review](step-audit-20261022/current-report.md).
>
> **The user excluded 27 cases with unavailable external prerequisites.**
> Action: Retain these cases as `SKIPPED_BY_USER`. Consequence: Their execution remains unclaimed.
> Owner: Codex harness maintainer. Evidence: The [scope decision](step-audit-20261022/user-scope-exclusions.json).
>
> **The three clarified entitlement rules apply across all portal environments. Owner approval remains unconfirmed.**
> Action: Obtain approval evidence from the user-identified `portal team`. Consequence: Policy acceptance and publication remain blocked.
> Owner: `portal team`, user-reported for the three rules. Evidence: The [clarification stage](../05-entry-clarification.md#current-task-state).
>
> **Eight policy answers and one shared ownership/contact entry remain.**
> Action: Complete the [remaining entries](../05-knowledge-questions.md#answer-navigation). Consequence: Missing policy blocks its affected acceptance definition.
> Owner: user or delegated topic owner. Evidence: The [investigation reconciliation](question-refinement-20261026/reconciliation.json).

> **UI trace archives remain local and are absent from fresh Git checkouts.**
> Action: Restore required traces before full artifact audits. Consequence: Missing traces block complete artifact verification.
> Owner: Codex harness maintainer. Evidence: The [trace exclusion and revision map](trace-git-exclusion-20261023/manifest.json).

## Screenshot storage: 23 October 2026

The [request](screenshot-dedup-20261023/user-input.txt) authorizes symbolic links for identical screenshots.
Deduplication replaced 47,787 copies across 54,463 screenshots.
The [record](screenshot-dedup-20261023/deduplication.json) lists regular sources, aliases, hashes, prior Git revisions, and checks.
Existing screenshot paths, capture metadata, and case outcomes remain unchanged.

Aliases use relative links. Preserve each regular source while any alias consumes it.
Windows needs Git symbolic-link support. Windows was not tested.
Use regular sources for ingestion. Original Git objects remain available through the local trace-exclusion backup.

## Trace storage: 23 October 2026

The [request](trace-git-exclusion-20261023/user-input.txt) selects trace ZIP exclusion and a push when the resulting size permits it.
The [exclusion record](trace-git-exclusion-20261023/manifest.json) identifies 1,661 local UI trace paths and their unchanged hashes.
It maps the 23 original unpublished revisions to filtered revisions.
Mapped revisions preserve all non-trace file bytes and modes.
Original commits remain reachable through the recorded local backup reference.

Current Git ignores new trace ZIPs. Three published trace archives remain tracked for their existing consumers.
Existing raw manifests and case results remain unchanged. Fresh checkouts require local UI traces for complete artifact audits.

## Current evidence navigation

For current questions and answers, use the [single knowledge question document](../05-knowledge-questions.md).
Version 3 retains all 60 IDs. Investigation reduces the editable entries to eight policy answers and one shared contact entry.
Source-backed findings include multiple-entity matching, current EMS3 support, profile fields, login flags, and twenty analytics attributes.

The [refinement request](question-refinement-20261026/user-request.json) and [continuation](question-refinement-20261026/user-continuation.json) retain the user's exact input.
The [reconciliation](question-refinement-20261026/reconciliation.json) records confidence, scope, sources, hashes, limits, and each disposition.
The [current checks](question-refinement-20261026/checks.json) record preservation, links, source bindings, validation, and writing limits.
Conditional deployment and release evidence remains follow-up work. Human review and publication remain separate gates.

The [format instruction](clarification-20261023/review-format-user-input.md#exact-user-input) permits asynchronous completion before requested ingestion continuation.
The [reference-priority instruction](clarification-20261023/reference-priority-user-input.md#exact-user-input) requires saved user input as a high-priority reference.
The [format checks](clarification-20261023/review-format-checks.json) record preserved answers, question coverage, links, and writing limits.
The [batch-workflow source](clarification-20261022/batched-question-workflow-source.json) records the user's requested answer and review loop.
The [historical question source map](question-batch-20261022/source-map.json) retains the original batch mapping and document hash.
The [batch checks](question-batch-20261022/checks.json) record coverage, links, preservation, and writing limits.

For current entry-policy intent, use the [living clarification stage](../05-entry-clarification.md#current-task-state).
It records the three clarified rules, all-environment scope, and portal-team ownership without approval or verification.
The [entry source](clarification-20261022/ui-q-002-source.json), [scope source](clarification-20261022/ui-q-002-scope-source.json), and [owner source](clarification-20261022/ui-q-002-owner-source.json) retain the answers.
The [tile answer](clarification-20261022/empty-entity-source.json) applies when a tile has no configured EMS2 entity.
It selects hidden tiles and denied direct launch.
The [recovered session excerpt](clarification-20261022/recovered-session-source.json) retains exact response records and their recorded timestamps.

The [user's reference-priority instruction](clarification-20261022/user-reference-priority-source.json) governs how new answers are recorded and used.
The [procedure record](../05-entry-clarification.md#user-reference-priority) keeps intended behavior separate from observed results and publication approval.
The [current clarification checks](clarification-20261022/checks-empty-subject.json) cover the procedure and new business clarification.
The [empty-subject answer](clarification-20261022/empty-subject-source.json) selects visibility and launch through one configured entity.
The [owner and scope answer](clarification-20261022/empty-subject-owner-scope-source.json) confirms portal-team ownership across all portal environments.

The [tile-rule owner answer](clarification-20261022/empty-entity-owner-scope-source.json) confirms portal-team ownership across all portal environments.
The [earlier owner and scope checks](clarification-20261022/checks-owner-scope.json) record hashes and review limits.
The [earlier check receipt](clarification-20261022/checks.json) retains the version 4 checks.
Historical reports retain their original entry-conflict statements. The clarification changes no historical result or canonical case bytes.

Start with the [current execution stage](../08-execution-stage.md), [current audit review](step-audit-20261022/current-report.md), and [case gallery](audit-run-20261022/report-006/index.html).
The current scope includes 494 cases.
The latest ledger records 420 passes, 72 failures, and two active blockers.
It also records 27 user exclusions across the complete 521-case catalog.
Each executed canonical step retains a fresh screenshot.
The [screenshot correction review](screenshot-review-20261022/review.md) resolves setup, timing context, and browser target gaps.

The [correction receipt](screenshot-review-20261022/correction-verification.json) binds 19 passing attempts across 14 unique cases.
Complete step bindings measure structural coverage. They do not establish visual review of every frame.
The [earlier gallery](audit-run-20261022/report-001/index.html) remains immutable.
Its 66 local passes and 455 blocked cases describe the earlier stage only.
The audit retains screenshots, assertions, traces, and historical failed attempts.

Controlled service fixtures limit local results.
The [intake](../01-intake.md) and [canonical case navigation](../06-test-cases.md#coverage-navigation) preserve the definition baseline.
The active [refinement stage](../05-refinement.md) applies the new UI writing rules to all 521 definitions.
All 521 refinements are saved in the [checkpoint](refinement/progress.json) and [case review metadata](refinement/case-reviews.jsonl).
The [quality gate](refinement/quality-results.json) reports 28 FAIL and 493 UNVERIFIED cases.
The [binding register](../05-refinement.md#unresolved-ui-bindings) identifies every failed case and affected step.

The design baseline lacked reviewed automation bindings for all 521 cases.
The [current audit ledger](audit-run-20261022/report-006/case-results.json) records subsequent local assertions separately.
The inventory counts 521 definitions across 46 groups.
It records 336 implementation characterizations, 23 documented draft expectations, and 162 proposals.
Counts do not prove independent rule coverage or exhaustive combinations.

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| UI-EV-001 | Case identities, coverage counts, and execution states | [case-inventory.json](case-inventory.json) | 2026-10-22; exact source revisions appear in the manifest. | `f08ae44d02fda86ce44101bc8c6893dc26cd8e1cb446d1b5d2caa1ea372fc851` | 521 version 2 definitions; all NOT_RUN. Definitions remain in the canonical catalog. |
| UI-EV-002 | Exact source hashes and retained source identities | [source-manifest.json](source-manifest.json) | 2026-10-22; exact source revisions appear in the manifest. | `40d31144443438ad6550805cd3b4bad9a59ea78acd3478151a4bef57786378c4` | 139 source files; implementation and draft-source authority remain distinct. |
| UI-EV-003 | UI source and inspected assertion scope | [ui-source-inspection.md](ui-source-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `ece95bfbc0719307783708c38b0d017c384d3383d63195623c63f09e6885f5bc` | 156 source-derived UI cases. Conditional hook coverage is explicitly proposed. |
| UI-EV-004 | UI source-byte receipt | [ui-source-inspection.json](ui-source-inspection.json) | 2026-10-22; exact source revisions appear in the manifest. | `b72056ade9c8798369dada96d38927599ab42f35eccbe2d36ad0c7fd095406ae` | Inspected source hashes and baseline checks. No business execution. |
| UI-EV-005 | Authentication and session source scope | [session-source-inspection.md](session-source-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `b7a1d819f9ddf998ab0f061147a19f48757d81230665d8fb28588f4e34d3c1e6` | 144 source-derived UI cases. Timings characterize local code. |
| UI-EV-006 | BFF administration boundaries | [admin-boundary-inspection.md](admin-boundary-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `aa9ff5337ea325d0880b7a8bb794f60e566277ff3b96423cec76a82e3093156a` | 97 boundary cases. DDL limits require a prepared-schema fixture. |
| UI-EV-007 | Draft domain intent, conflicts, and prior-run limits | [knowledge-inspection.md](knowledge-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `5defcf79f4aa1abc36f1dac7c5cd5c2fd13dd1d9caf90a8b4cbb84bd1a82eca6` | 52 domain cases. Business source approval remains unrecorded. |
| UI-EV-008 | Quality probes, shared fields, and assertion limits | [crosscut-inspection.md](crosscut-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `85b3b46814d5862057f1b0dd874fb84fc5f60b5fb4fde5c9bfc5a4c642653407` | 72 UI quality and boundary cases. Proposed policy remains unapproved. |
| UI-EV-009 | Registered local resources and schemas | [workspace-status.json](workspace-status.json) | 2026-10-22; exact source revisions appear in the manifest. | `7e2d1428b83ebc67ab0d30b8eaa6e0b3e8c8706daff9775d55637a4e78057c80` | Local discovery succeeded. No external connector call occurred. |
| UI-EV-010 | Staging retention reconciliation | [authoring-cleanup.json](authoring-cleanup.json) | 2026-10-22; exact source revisions appear in the manifest. | `5f4636122ba68500edb79034366b5dfa478f87e45b0ff1eef395bc6806cc68e5` | Only new generated inputs were removed after canonical reconciliation. |

## Task document order

Read documents by lifecycle stage. Use the existing current-stage links to assess the latest scope.
Filename numbers do not establish readiness or approval.

| Stage | Document |
| --- | --- |
| 01 Receive | [01-intake.md](../01-intake.md) |
| 05 Analyze | [05-refinement.md](../05-refinement.md); [entry clarification](../05-entry-clarification.md) |
| 06 Implement | [06-test-cases.md](../06-test-cases.md) |
| 08 Execute cases | [08-execution-stage.md](../08-execution-stage.md) |

The [filename map](document-order.json) retains original paths, compatibility links, source revisions, and unchanged hashes.

## Refinement evidence

| Evidence | Result and limits |
| --- | --- |
| [Component and step manifest](refinement/gherkin-manifest.json) | All 521 cases mapped. Source fingerprints and exact canonical step lines are retained. |
| [Final quality results](refinement/quality-results.json) | 28 FAIL; 493 UNVERIFIED. No automation readiness is claimed. |
| [Current case metadata](refinement/case-reviews.jsonl) | One current record per case. Includes components, step support, gaps, cleanup, and limits. |
| [Baseline audit](refinement/baseline-quality.json) and [initial refinement audit](refinement/initial-quality.json) | Preserve material failed checks for comparison. They do not establish execution. |
| [Refinement document checks](refinement/document-checks.json) | Checks IDs, 1,596 assertions, links, fingerprints, and checkpoint consistency. |
| [Runtime validation](refinement/validation-results.json) | Records tests, offline wheel construction, and installed workspace validation. |
| [Authoring cleanup](refinement/authoring-cleanup.json) | Records intermediate hashes, compacted metadata, and preserved canonical steps. |

## Validation

The [original document checks](document-checks.json) retain definition version 1 results.
The [refinement checks](refinement/document-checks.json) apply to version 2.
Lint warnings retain unknown owners, pending review, unresolved policies, and pending ASD review.
Document validation does not execute business scenarios.
Existing snapshots, task histories, source repositories, and audit events remain unchanged.
The [supplemental discovery review](step-audit-20261022/supplemental-discovery-review.md) preserves a listing probe with zero executed cases.

## Resume

Review the proposed and draft expectations before business acceptance.
Triage the retained failed predicates and definition conflicts before changing business source.
Resolve the [two active prerequisites](step-audit-20261022/current-report.md#remaining-active-prerequisites) before their later assertions.
The user excluded 27 dependency-bound cases for this audit.
Keep the current case IDs stable.
Save every completed execution immediately under this evidence directory.

Record actual results and material limits separately from the case definitions.
