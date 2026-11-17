# Git-only handoff: knowledge conversion

Date: 17 November 2026 (Asia/Singapore)

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
The current worktree also contains six reviewed wiki files with uncommitted changes.
Commit those six files before transfer if the destination must reproduce their current bytes.

Do not commit unrelated changes.
The observed unrelated changes include `core/connectors/yarn.lock`, `core/release-report/`, and `tasks/workbench-ado-skills-assessment-20261113/`.

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

The current local inbox contains:

```text
knowledge/evidence/incoming/Cash Settlement Home Page/Cash Settlement Home Page/page.md
knowledge/evidence/incoming/RATAN - 51358/RATAN - 51358/page.md
```

Those bytes do not move with Git.
The manifest instead points to retained snapshots under `knowledge/evidence/sources/`.
The agent on the destination therefore knows the existing source through the manifest, snapshots, and selections.

Git-only continuation supports existing conversion queues.
It cannot refresh a collection from a newer export unless that export is supplied separately.
Do not commit the complete incoming export merely to bypass this boundary.

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
