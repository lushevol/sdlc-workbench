# Local review helpers

Read this reference when running the helpers or adding project-specific checks.
Use installed Python 3.10+ and Git with `rev-parse --end-of-options` support.
No additional Python package, service, work item, or account is required.
All three scripts operate independently of the Workbench runtime.

## Select one comparison

| Mode | Baseline | Candidate | Use |
| --- | --- | --- | --- |
| `worktree` | `HEAD`, or empty baseline before the first commit. | Final tracked files and nonignored untracked files. | Local changes, including staged and unstaged effects. |
| `staged` | `HEAD`, or empty baseline before the first commit. | Index blobs. | Exactly the staged candidate. |
| `branch` | Merge base of `--base` and `--head`. | Resolved `--head` commit. | Branch or PR changes. |
| `range` | Resolved `--base` commit. | Resolved `--head` commit. | Explicit endpoint comparison. |

`--repo` is required; it can name the checkout or a directory inside it.
`--mode` defaults to `worktree`; `--head` defaults to `HEAD`.
Branch and range modes require `--base`.
Local modes reject explicit base refs and nondefault heads.
Committed comparisons exclude dirty worktree content and untracked files.
Review unrelated local changes separately when they affect execution.
For a single ordinary commit, use its parent as `--base` and that commit as `--head`.
Choose a merge commit's parent explicitly rather than guessing.

Use quoted paths and refs when constructing commands.
`--git-command "sc-cli git"` selects an installed wrapper when repository instructions require it.
The helper parses that wrapper into arguments and uses no shell.
Do not supply shell operators, credentials, or untrusted executable choices.

## Context output

Run `scripts/review_context.py` with the selected comparison arguments.
It emits comparison identity, `fingerprint`, `line_basis`, `files`, `change_count`, and `limitations`.
`change_count` counts reported file changes.
Unborn commit fields are `null`.
File records include `path`, `status`, `content_sha256`, `before_content_sha256`, `added_ranges`, `removed_ranges`, and `binary`.
Exact-content renames also include `old_path`.
Deleted files have no candidate content hash or added ranges.
Added ranges use inclusive, one-based candidate line numbers.
Removed ranges use inclusive, one-based baseline line numbers.
`line_basis: raw-content-comparison` identifies the local comparison algorithm.
Those ranges do not certify a hosting provider's diff anchors.

The helper uses NUL-delimited Git inventories and hashes compared bytes.
It identifies exact-content renames; edited moves can appear as deletion and addition.
Worktree comparison uses raw file bytes rather than executing Git clean filters.
Line-ending normalization can therefore differ from a configured Git diff.
Inspect the actual source and repository configuration when this distinction matters.
Check provider-supplied diff annotations before publishing an inline comment, even when local report validation passed.

The fingerprint binds comparison identity, selected bytes, file modes, paths, and the local index where applicable.
It does not bind requirements, unchanged callers, review judgments, analyzer databases, or tool configuration.
Record those identities separately and rerun affected checks when they change.
The helper creates no cache, history, report file, or passing review decision.

Binary and non-UTF-8 content cannot receive text analysis.
Content above 1 MiB is hashed but excluded from text analysis.
Symlinks and gitlinks are identified without traversing their targets.
Submodule working contents require a separate review inside the owning repository.
Unresolved local index conflicts stop collection.
Keep every reported limit beside the review claim it limits.

## Scan output and exit codes

Run `scripts/scan_changes.py` with exactly the same comparison arguments.
It scans added text lines for private-key markers, selected provider token shapes, access identifiers, and credential assignments.
These patterns are limited detection aids; they do not establish token validity or complete credential absence.
Findings contain location, detector ID, suggested severity, and a static message.
They exclude matched source lines and credential values.
All findings use `kind: candidate` until contextual review establishes a defect.

| Helper | Exit 0 | Exit 1 | Exit 2 |
| --- | --- | --- | --- |
| Context | Metadata collected; inspect limitations. | Unused. | Arguments, Git scope, or content collection failed. |
| Scanner | No candidates; inspect limitations. | Candidates require inspection. | Configuration or scope collection failed. |

Scanner `COMPLETE_WITH_LIMITS` means pattern scanning completed with the listed limits.
It does not mean the change passed security review.
`FINDINGS` identifies candidates rather than an automatic publication or merge gate.
Review the structured result rather than converting every nonzero exit into an infrastructure failure.
Do not suppress errors or echo raw Git diagnostics that could contain private values.

## Optional custom rules

Pass `--rules /absolute/path/review-rules.json` to request custom literal checks.
No rule or ignore file is discovered automatically.
The draft's `.codeshield-rules.yml` regex format is not supported.
Convert simple checks to literal rules; use existing analyzers for semantic or regex-based policies.

```json
{
  "rules": [
    {
      "id": "no-process-exit",
      "contains": "System.exit(",
      "severity": "HIGH"
    },
    {
      "id": "review-tracked-todos",
      "contains": "TODO",
      "requires_nearby": "ISSUE-",
      "case_sensitive": false,
      "severity": "LOW"
    }
  ],
  "exclude": ["generated/*"]
}
```

These examples define no universal project policy.
Apply only checks supplied by the repository or requested by the user.
`contains` and `requires_nearby` are literal substrings, not regular expressions.
Matching is case-sensitive unless `case_sensitive` is `false`.
`requires_nearby` suppresses a candidate when its literal occurs within five added physical lines in the same file.
The distance uses candidate line numbers, not the number of entries in the diff.
Unchanged nearby lines are unavailable to this check; inspect them before confirming a violation.

`exclude` uses case-sensitive shell glob matching against repository-relative paths for custom checks only.
It never suppresses built-in secret candidates.
Supported severities are `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW`; contextual review sets the final finding priority.
Each rule requires a unique ID, `contains`, and `severity`.
Unknown fields, duplicate IDs, duplicate JSON keys, invalid values, and oversized files fail validation.
Limits are 64 KiB per configuration, 128 rules or excludes, and 512 characters per literal or glob.
IDs use 1–64 letters, digits, dots, underscores, or hyphens and start with a letter or digit.
The scanner records a canonical rule fingerprint without copying rule literals into its output.

## Retain and verify

Inspect candidate secrets privately; retain only redacted findings and required source identities.
Do not test a credential against an external service merely to confirm a pattern match.
Follow the repository's actual incident procedure for confirmed exposure.
Deleting an added line does not establish removal from Git history or deployed systems.

Save JSON output only when the requested evidence workflow requires it.
Use an authorized evidence location outside the compared files while collecting the review.
Recollect the final scope and compare fingerprints after inspection or requested fixes.
Helpers do not replace full diff review, assertion inspection, source freshness checks, or human approval.

## Validate structured reports

Use `scripts/validate_review.py` only when the review requires [structured output](review-schema.md).
It checks report structure, frozen comparison identity, complete path accounting, and local added or removed ranges.
Pass `--repo` to independently recollect local context and reject stale or altered scope metadata.
Without that option, the validator checks only the supplied documents.
Exit 0 means structurally valid; exit 1 means invalid structure or scope; exit 2 means unreadable or invalid JSON.
No validator result establishes citation accuracy, complete review, business verification, or permission to publish.
