---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
---

# Learning from two days of Workbench sessions

> **Three concrete learning proposals await your confirmation.**
> C06 improves review coverage; C07 protects authored assets; C08 checks complete installed skill trees.
> Owner: user. Next action: approve, reject, or revise the [draft changes](review-20261126/candidates/proposed-guidance.md).
> No reusable asset, packet, registry rule, or personal memory was changed.
>
> **Five explicit preferences already have maintained owners.**
> Reuse those owners without duplicating their rules.
> The graph's latest service-centric requirement remains with its active task.

## Scope and actual source coverage

Request: [exact input and scope](01-maintenance.md#two-day-learning-review).
Window: 24 November 2026, 16:04:45 through 26 November 2026, 16:04:45, Asia/Singapore.
This is a rolling 48-hour review, not two complete calendar days.

Inspected recent turn excerpts from seven accessible Codex chats and the seven corresponding retained task records.
Both active and archived chat listings were checked; no archived result fell inside the window.
Thread summaries supported discovery only. Selected message and command pages supported the conversation review.
Some turn histories were paginated or truncated; this is not a complete transcript audit.
Older executions in the task records provide context, not additional sessions inside the window.

| Chat title | Scope inspected | Durable task source |
| --- | --- | --- |
| Create session learning skill | Consolidation, confirmation gate, retained trial results. | [Session learning](01-maintenance.md) |
| Improve dependency graph HTML | Completed viewer changes, dependency classification, latest service-centric request. | [Graph task](../service-graph-viewer-20261125/01-maintenance.md) |
| Assess and adapt requirement-grill | Source adaptation, integration, validation, and scoped commit. | [Requirement Grill](../requirement-grill-adoption-20261125/01-maintenance.md) |
| Configure automatic staged commits | Initial option, confirmed additional defaults, probe failures and corrections. | [Settings task](../workbench-commit-config-20261125/01-maintenance.md) |
| Restore deleted SDLC drawio files | Deletion lineage, restoration, original bytes, and verification limits. | [Restoration task](../restore-sdlc-drawio-20261125/01-maintenance.md) |
| Update pre-action fetch rule | Explicit freshness direction, scoped rule change, and limits. | [Freshness task](../repository-fetch-first-rule-20261125/01-maintenance.md) |
| Optimize task evidence files | In-window branch handoff; earlier retention decisions as background. | [Retention task](../workbench-evidence-log-retention-20261124/01-maintenance.md) |

The [review receipt](evidence/two-day-learning-review.json) retains chat IDs, source hashes, dispositions, and limits.
Hashes describe inspected bytes; concurrently active task records can subsequently change.
No private client history store was crawled.

## Explicit preferences already represented

These are sourced instructions, not inferred personal traits.

| ID | Learning | Current owner and disposition |
| --- | --- | --- |
| C01 | Fetch first, disclose differences, and wait for integration instructions. | [Repository freshness](../../AGENTS.md#repository-freshness-before-codebase-actions). Active; no duplicate rule. |
| C02 | Make agent defaults configurable and retain existing behavior as defaults. | [Agent settings](../../README.md#configure-agent-settings). Active; no new configuration. |
| C03 | Keep routine logs beside their task and outside Git; retain consequential evidence. | [Evidence boundary](../README.md#git-managed-evidence-and-local-logs). Active; no reclassification. |
| C04 | Clarify material missing criteria before dependent impact or implementation work. | [Requirement Grill](../../.agents/skills/requirement-grill/SKILL.md). Active; no additional refinement skill. |
| C05 | Present extracted learning and obtain explicit confirmation before finalization. | [Confirmation gate](../../.agents/skills/learn-from-sessions/SKILL.md#human-confirmation-before-finalization). Active; this review stops at candidates. |

The settings source records: “yes add these configs, use current value as default.”
That answer confirms those five settings; it does not authorize future unrelated settings.
The retention source records: “I prefer to keep logs still in task but git ignore them.”
That instruction concerns routine logs; required evidence still follows its existing retention rules.

## C06: Recent-session discovery must survive large task archives

Evidence: this review ran the existing scanner with `--past-duration 48h`.
The scanner reported success with truncation after 512 files from one older task.
It reached no session roots. This cannot establish that no session exports exist.
Source inspection confirmed that default tasks precede explicit paths and lack the session-time filter.

A separate review root and seven explicit source paths produced a complete seven-record inventory without truncation.
Connected Codex history provided the actual chat discovery and selected message review.
The lesson is to separate session-window selection from older contextual task material.

Proposed owner: the existing history-scan reference.
Exact proposed text: [C06 draft](review-20261126/candidates/proposed-guidance.md#c06-preserve-recent-session-coverage).
Scope: agent workflow guidance, using existing tools and scanner options.
Confidence: high for the observed truncation and selected-source workaround.
Limit: no general transcript export or new scanner API is implemented.

## C07: Authored editable assets need explicit cleanup treatment

The restoration task recovered two Draw.io files after root deletion and later deletion of their recovered task copies.
The files exactly match their original Git blobs and cleanup hashes.
The retained task says the user needs them for inspection and reuse despite no active runtime consumers.
This supports distinguishing human-authored assets from disposable generated evidence during cleanup.
It does not prove every historical diagram must be retained forever.

Proposed owner: the existing cleanup procedure, with an optional read-only verification helper.
Exact proposed text: [C07 draft](review-20261126/candidates/proposed-guidance.md#c07-protect-authored-assets-during-cleanup).
The [draft script](review-20261126/candidates/verify_restored_assets.py) compares existing files with exact historical Git blobs.
It checks byte equality and optional XML parseability without restoring or deleting files.

The current diagrams passed exact-byte checks and XML parsing across their five pages.
Six [isolated draft checks](review-20261126/candidates/check_restoration_draft.py) passed without failures or skips.
They cover matching bytes, unchanged index, mismatch, missing files, parent traversal, symlinks, and malformed XML.
Confidence: high for this recovery procedure; broader retention policy remains a proposal.
Limits: visual rendering and historical content accuracy were not established.

## C08: Validate complete installed skill output

The consolidation's first installed-wheel check found three auxiliary references inside a retired skill folder.
The replacement entry point and its focused tests had already passed.
Relocating those references corrected the installed output; the final wheel check passed.
See the [original failure](evidence/wheel-initialization-failure.json) and [corrected check](evidence/wheel-smoke.json).

Other reviewed sessions exposed probe assumptions about temporary-path aliases and generated `core/` responsibility guides.
Those assumptions required probe corrections, not product behavior changes.
Repeated sandbox socket failures also passed under permitted local execution without weakening assertions.
The lesson is to identify the failure's layer and verify the actual installed contract.

Proposed owner: the existing shared-asset promotion reference.
Exact proposed text: [C08 draft](review-20261126/candidates/proposed-guidance.md#c08-check-the-installed-result-after-skill-changes).
Confidence: high for the retained cases and their stated environments.
Limits: no current full-suite rerun or new packaging implementation was needed for this retrospective.

## Scoped graph preferences and incomplete work

C09 is explicit current intent: prioritize inbound, outbound, upstream, and downstream service relationships.
Keep low-priority internals in data or service cards instead of separate primary graph nodes.
The user also requests service-centric nodes and a clearer layout for roughly one hundred repositories.
The [active follow-up](../service-graph-viewer-20261125/01-maintenance.md#follow-up-scope-service-centric-projection) owns this work.
Retain it there; do not publish its unfinished implementation as verified reusable behavior.

The earlier completed viewer used one progressive graph and a compact local HTML entry point.
Its receipt reports approximately 35.7 MB becoming 65.6 KB of HTML plus 12.6 MB of separate data.
That demonstrates saved-snapshot loading improvements, not elimination of the underlying evidence volume.
Gigabyte-scale snapshots, other browsers, and current live dependencies remain unverified.

C10 is task-scoped: the user requested a plan before implementing complex graph changes.
Keep that preference scoped to this task unless the user explicitly broadens it.
The graph chat remains active; its latest results were not assumed complete.

## Verification, disposition, and human decision

Actual checks performed during this review:

- Fetched Workbench refs and compared `HEAD` with the configured upstream.
- Inspected current effective settings, maintained owners, exact sources, and selected verification receipts.
- Reproduced scanner truncation and completed a seven-source fallback inventory.
- Verified both restored diagrams against exact historical bytes and XML structure.
- Executed six isolated candidate-helper tests; all passed.
- Checked candidate syntax, report links, JSON structure, and the scoped diff.

No shared skill, guide, configuration, registry rule, experience packet, or global memory entry was finalized.
Only task-owned review evidence and unactivated drafts were prepared.
The current documentation remains unchanged because these proposals await confirmation.
Formal ASD writing review remains pending.

| Candidate | Human decision | Confirmed scope |
| --- | --- | --- |
| C06: bounded history discovery guidance | PENDING | None |
| C07: authored-asset cleanup guidance and read-only helper | PENDING | None |
| C08: complete installed-skill verification guidance | PENDING | None |

Approve, reject, or revise those candidates against the linked draft text and script.
The [skill](../../.agents/skills/learn-from-sessions/SKILL.md#human-confirmation-before-finalization) requires: “Ask the human to approve, reject, or revise specific candidates, then wait for an explicit answer.”
That instruction blocks finalizing the extracted learning; it permits retaining this review and its drafts.
