# Restore deleted SDLC Draw.io diagrams

> **No critical conclusions require user attention or action.**
> Both deleted diagrams are restored at their original root paths.
> Their exact historical bytes passed the checks recorded below.

## Request and authorization

- Date: 25 November 2026, Asia/Singapore.
- Source: User message in Codex session `01a21186-b2b2-7ef3-8b32-1d607c27c096`.
- Exact user input:

> SDLC drawio files are deleted in some commits, find it out and restore them.

The user authorizes investigation and restoration of deleted SDLC Draw.io files.
This is repository maintenance.
It does not change business behavior or authorize remote publication.

## Repository and scope

- Repository: `https://github.com/lushevol/sdlc-workbench.git`.
- Branch: `feature/knowledge-layout-consolidation`.
- Starting HEAD: `b9ce58b4a`.
- Comparison: `HEAD` against `origin/feature/knowledge-layout-consolidation`.
- Freshness: `git fetch --all` succeeded on 25 November 2026.
- State: Clean worktree; three local commits ahead; zero incoming commits.
- Local commits: `502856727`, `36f4aa7ea`, and `b9ce58b4a`.
- Local scope: Session-learning assets and repository procedures.

Affected files are `AI SDLC.drawio` and `AI SDLC Workbench.drawio` at the repository root.
The user needs the editable diagrams for inspection and reuse.
Current source inspection found no active runtime consumers.
Risk is low because restoration adds static files without changing implementation.
Their content is historical and includes outdated paths and capability labels.
Current architecture guides retain their authority.

## Deletion history and selected source

| Commit | Date, Asia/Singapore | Effect |
| --- | --- | --- |
| `516857d649f5dc557ff58731bb17a09e0308ffce` | 13 November 2026, 15:31 | Deleted both diagrams from the repository root. |
| `55bc74d19` | 13 November 2026, 16:20 | Recovered both under `tasks/workbench-documentation-migration-20261113/evidence/historical-diagrams/`. |
| `b3df0435d023330eca456414ad7b25b43935a68b` | 24 November 2026, 18:08 | Deleted the recovered copies during maintenance-task cleanup. |

The [cleanup manifest](../cleanup-manifest.json) records both deleted copies, their hashes, and their prior revision.
The selected original revision is `79a4104035785b7d8c37e6d424d5d4c888104eee`, the parent of `516857d64`.
Both original files match the recovered copies before cleanup, byte for byte.
The selected destination restores each original root path.
No historical cleanup record requires rewriting.

## Work and next action

Repository history identified exactly two distinct SDLC Draw.io files.
Both files were restored from the selected original revision.
Validation passed for exact bytes, hashes, XML, page structures, cell references, and workspace metadata.
The scoped commit includes only both restored diagrams and this task.

| Restored file | Bytes | Pages | Cells | SHA-256 |
| --- | --- | --- | --- | --- |
| [AI SDLC.drawio](../../AI%20SDLC.drawio) | 29,042 | 1 | 76 | `bff26cffb78900a884e93bd6a1fef2840b4961b5062dc1881f5dc22b9a76a213` |
| [AI SDLC Workbench.drawio](../../AI%20SDLC%20Workbench.drawio) | 115,624 | 4 | 288 | `6304cfef1d795fe6d25650d4ccde942a8b8c173c9ae15ccfc5b1c6683e729b23` |

The Workbench drawing retains concept, lifecycle, architecture, and evidence pages.

The native hook binding succeeded through `.venv/bin/ai-sdlc`.
The unqualified command was unavailable on `PATH`.
Capability lookup through `learning list` returned no matching rules.
No reusable asset changes are needed for this direct Git restoration.

## Documentation assessment

Reviewed [documentation navigation](../../docs/README.md), [architecture](../../ARCHITECTURE.md), and [documentation ownership](../../docs/WORKSPACE_DESIGN.md#documentation-ownership).
These guides describe current behavior.
The restored files preserve historical bytes and do not introduce a current contract.
No current guide change is needed.
This task provides recovery provenance and direct links to both restored files.

## Checks and limits

- Repository freshness: `git fetch --all` passed.
- Native session binding: `.venv/bin/ai-sdlc --workspace . hooks bind ...` returned `BOUND`.
- Capability lookup: `.venv/bin/ai-sdlc --workspace . learning list --query 'restore deleted drawio diagrams git'` returned no matches.
- Byte assertions matched both files against the original revision and pre-cleanup recovered copies.
- SHA-256 and size assertions matched both entries in the existing cleanup manifest.
- XML assertions passed for both `mxfile` roots, five pages, and 364 cells.
- Cell assertions passed for unique IDs and valid parent, source, and target references.
- Relative Markdown link checks passed for the maintenance record.
- `.venv/bin/ai-sdlc --workspace . validate` returned `VALID`, with 119 documents and no findings.
- `git diff --check` passed before staging.

No runtime behavior changed, so runtime tests and package builds were not applicable.
Draw.io visual rendering was not checked.
Historical paths and capability labels remain unchanged inside the original bytes.
No reusable learning changes or remote publication were performed.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
