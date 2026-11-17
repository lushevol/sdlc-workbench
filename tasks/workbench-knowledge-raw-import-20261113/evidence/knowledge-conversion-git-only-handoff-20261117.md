# Git-only handoff: knowledge conversion

Date: 17 November 2026 (Asia/Singapore)

## Direct instruction for the next AI agent

You are continuing the existing knowledge conversion in this repository.
Read `AGENTS.md`, this handoff, and the linked diagnostic before editing.

Work only on the four registered source collections and their owning task evidence.
Use retained snapshots under `knowledge/evidence/sources/` as the existing source.
Create fresh plans and fresh plan-bound views because `.workbench/` is not transferred by Git.

Run the following checks before semantic work:

```sh
git status --short --branch
git log --oneline -5
git diff --check
.venv/bin/ai-sdlc --workspace . validate
```

Then run the four `sources plan` commands in this document.
Continue independent supported work until a material owner, source, model, or authorization dependency blocks it.

Use GPT-6.1 Sol / Medium for review.
Use GPT-6 Luna / Max for document batches when that runtime is available.
Record the actual runtime selection and its evidence limit.

Save every completed case immediately under the owning task evidence.
Preserve failures, partial results, held sources, rejected attempts, hashes, and unresolved questions.
Keep all questions in `evidence/canonical-draft-questions-20261115.md`.

Use isolated worker output under `.workbench/`; only the coordinator updates shared receipts, canonical records, audits, task documents, and wiki provenance.
Do not run `git add -A`, `git clean`, destructive resets, or source deletion.
Stage only the exact completed task files.
Do not publish knowledge or infer business approval from passing checks.
Do not push semantic conversion changes unless the current user explicitly authorizes that push.

Stop and record a blocker when a required retained snapshot is missing, a plan is stale, a sealed check fails, the required model is unavailable, or owner input is required.
Continue unrelated eligible collections while one collection is blocked.

## Purpose

Use this handoff when only the Git repository can move to another machine.
The conversion remains partial. The destination must create fresh local plans.

## Source checkout at handoff

The observed branch was `feature/knowledge-layout-consolidation`.
The observed pre-handoff `HEAD` was:

```text
cd0d56ea2b30dc70c46251824cc792f9ba6ed6c4
```

The conversion diagnostic is committed in the history at `af3f978405776c9d63c8664176d1164676a9904c`.
This handoff is committed at `86e7588b07b706b7c0d4c5a20d466b080dc2ea4a`.
The six reviewed wiki refresh files are committed at `56cd8196c7f8541698b58c724cc86986523d980b`.

Do not transfer unrelated changes.
The observed unrelated changes include `core/connectors/yarn.lock`, `core/release-report/`, and `tasks/workbench-ado-skills-assessment-20261113/`.

## Bootstrap gate

From the workspace root, establish the branch and record the starting state before running setup:

```sh
git fetch origin
git switch feature/knowledge-layout-consolidation
git pull --ff-only origin feature/knowledge-layout-consolidation
git show --stat --oneline d8e4f43e2
git rev-parse HEAD
git status --short --branch
git diff --name-status
```

The checkout must contain the handoff history and the reviewed wiki commit.
Stop before editing if a protected tracked file is dirty or the branch cannot fast-forward.
Preserve unrelated dirty files and report them.

Use the workspace-relative `.venv/bin/ai-sdlc` path when it is not on the AI client's `PATH`.
Hooks are optional evidence only; never infer the active record from dirty files.

## What Git contains

Git contains the retained conversion inputs and records:

- `knowledge/evidence/manifest.yaml` with source identities, revisions, hashes, and snapshot paths.
- `knowledge/evidence/sources/` with 1,035 tracked retained source files.
- `knowledge/evidence/selections/` with selection decisions and source bindings.
- `knowledge/evidence/processing/` with current processing receipts.
- `knowledge/evidence/audit/` with immutable governance events.
- `knowledge/records/` with canonical candidate records.
- `knowledge/llm-wiki/` with the tracked derived wiki files.
- `tasks/workbench-knowledge-raw-import-20261113/` with checkpoints, reports, questions, and diagnostic evidence.

These files let a new machine resume processing of retained source revisions.

## What Git does not contain

`.workbench/` is ignored. It contains temporary plans, filtered views, worker sessions, and runtime handoffs.
The destination cannot resume those exact worker sessions from Git alone.

`.env`, `workspace.local.yaml`, virtual environments, independent repository checkouts, and `node_modules` are also local.
Recreate them on the destination.

## The incoming folder

`knowledge/evidence/incoming/` is intentionally ignored.
It stores replaceable complete exports before source refresh.
It is not the retained source of record.

Confirm the boundary on the destination:

```sh
git check-ignore -v knowledge/evidence/incoming/
git ls-files knowledge/evidence/incoming
git ls-files knowledge/evidence/sources | wc -l
```

The second command should return no paths.
The third command should report the retained snapshot inventory.

The current local inbox contains:

```text
knowledge/evidence/incoming/Cash Settlement Home Page/Cash Settlement Home Page/page.md
knowledge/evidence/incoming/RATAN - 51358/RATAN - 51358/page.md
```

Those bytes do not move with Git.
The manifest instead points to retained snapshots under `knowledge/evidence/sources/`.
The agent on the destination therefore knows the existing source through the manifest, snapshots, and selections.

Do not report a missing source only because `incoming/` is empty.
For existing work, resolve the source from the manifest entry and its retained `snapshot` path.
Report a source as missing only when the required retained snapshot or manifest binding is absent.

Git-only continuation supports existing conversion queues.
It cannot refresh a collection from a newer export unless that export is supplied separately.
Do not commit the complete incoming export merely to bypass this boundary.

Never use `knowledge/evidence/sources/` as the `sources refresh --input` directory.
Do not run `sources refresh` because `incoming/` is absent.
Refresh only after a complete newer export is separately supplied and hash-recorded.

If a new export becomes available, place it in the matching inbox directory on the destination and run:

```sh
.venv/bin/ai-sdlc --workspace . sources refresh \
  --source COLLECTION \
  --input knowledge/evidence/incoming/COLLECTION

.venv/bin/ai-sdlc --workspace . sources verify --source COLLECTION
```

Record the export transfer and its hash in the owning task evidence.
Never overwrite retained snapshots.

## Destination restore

Clone the repository and use the conversion branch:

```sh
git clone <repository-url> workbench
cd workbench
git checkout feature/knowledge-layout-consolidation
```

Install the local runtime. Do not copy the source machine's virtual environment:

```sh
./setup.command --core-only
./setup.command --check
```

Validate the restored tracked workspace:

```sh
.venv/bin/ai-sdlc --workspace . status
.venv/bin/ai-sdlc --workspace . validate
```

Expected validation is `VALID` with the tracked document set.

## Resume procedure

Create fresh plans because ignored plans are absent and receipt state can change:

```sh
.venv/bin/ai-sdlc --workspace . sources plan \
  --source cash-settlement-home-page --recipe canonical-v1

.venv/bin/ai-sdlc --workspace . sources plan \
  --source ratan-51358 --recipe canonical-v1

.venv/bin/ai-sdlc --workspace . sources plan \
  --source portal-document-export --recipe canonical-v1

.venv/bin/ai-sdlc --workspace . sources plan \
  --source settlement-netting --recipe canonical-v1
```

For each collection, run the stages in this order:

1. Run `sources verify` and retain its status. `NEEDS_REVIEW` is expected for held identities. Do not force it to `READY`.
2. Run `sources plan --recipe canonical-v1` and save the printed plan path and `plan_id`.
3. Inspect the plan counts before creating a view.
4. Run `sources view --plan` with a new output directory.
5. Verify the view manifest source hashes, plan binding, and explicit omissions.
6. Review the selected pages and every affected canonical dependent.
7. Run preparation and the sealed check.
8. Run `sources complete` with the matching plan and results.
9. Record `remaining_process` and `remaining_review`, then create a fresh plan.

Stop the affected collection when the plan is stale, an input or output hash changes, a view binding is invalid, an affected closure expands without review, or a sealed check fails.
Continue other collections when their evidence remains valid.

Generate a new plan-bound view for each fresh plan:

```sh
.venv/bin/ai-sdlc --workspace . sources view \
  --source COLLECTION \
  --plan .workbench/ingestion/<fresh-plan>.json \
  --output .workbench/ingestion/filtered/<new-run>
```

Review the queued pages and affected canonical closure.
Use the existing question annex for material questions.
Save each completed review under task evidence before continuing.

Use GPT-6.1 Sol / Medium for review.
Use GPT-6 Luna / Max for document batches when that runtime is available.
Record the actual model selection and retain the runtime limitation.

After review, run the sealed preparation check and `sources complete`.
Include every affected canonical output, including preserved dependents.
Replan after each completion wave.

## Required evidence for every case or batch

Save the evidence before starting the next case, waiting, or handing off.
Record the collection ID, source ID, relative source path, retained revision, source SHA-256, decision and ranges, policy/context hashes, plan ID, view-manifest hash, actual model/client/runtime, review scope, disposition, all canonical outputs, prepared and sealed checkpoint paths, command statuses, question IDs, and before/after queue counts.

Use dispositions exactly as supported by the source command: `updated`, `no_change`, `excluded`, or `missing_reviewed`.
Retain failed, partial, blocked, rejected, and `NEEDS_REVIEW` results.
Do not infer completion from a process exit code, a test name, a citation link, or a matching output count.

## Git write boundary

Stage only files produced by the authorized conversion wave.
Allowed paths are the owning task evidence and the specifically reviewed `knowledge/` records, receipts, audits, or wiki outputs.
Inspect the staged snapshot before every commit:

```sh
git diff --cached --name-status
git diff --cached --check
git status --short
```

The staged set must contain no `.workbench/`, `.venv/`, `.env`, `knowledge/evidence/incoming/`, or unrelated paths.
Use one scoped commit per completed wave.
Push only when the current user explicitly authorizes that push.

## Current conversion reference

The diagnostic snapshot reports:

| Measure | Value |
| --- | ---: |
| Current selected output-linked receipts | 139 / 622 (22.35%) |
| Current selected processing receipts | 159 / 622 (25.56%) |
| Exact selected source citations | 589 / 622 (94.69%) |
| Queued identities | 465 |
| Held identities | 44 |
| Current candidate records | 117 |
| Current wiki inputs | 117 / 117 |
| Published records | 0 / 117 |
| Complete semantic conversion | UNKNOWN |

Recompute these values after fresh planning.
The diagnostic report is [conversion-diagnostic-20261117.md](conversion-diagnostic-20261117.md).

## Resume completion condition

The handoff is complete when the destination has:

1. The conversion branch at the transferred revision.
2. The tracked manifest, retained snapshots, selections, receipts, records, and task evidence.
3. A valid local Workbench runtime.
4. Fresh plans and plan-bound views for every active collection.
5. New receipts with sealed checks for each completed batch.
6. Updated queue counts and unresolved held-source questions.

Do not claim semantic completion from citation rates, passing validators, or current wiki freshness.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Git-only transfer omits ignored incoming exports and temporary worker state.
  - Existing retained snapshots support continuation, but newer exports need separate transfer.
  - Complete semantic conversion remains unknown.
  - Human publication approval remains pending.
```
