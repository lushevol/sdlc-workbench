# Structured review report contract

Use this contract when the user, repository, or downstream consumer requests structured review output.
Ordinary review responses can remain concise Markdown.
This is a skill-local report, not a governed Workbench knowledge record or approval artifact.
The [validator](../scripts/validate_review.py) owns deterministic checks; [the template](../assets/review-report.template.json) supplies the authoring shape.

## Capture and validate

Set `REVIEW_DIR` to an authorized evidence directory outside the selected comparison.
For business tasks, use the owning task's evidence location.
Create that directory only within the existing authorization.
Capture context with the same mode and revisions used for the review:

```sh
python3 "$SKILL_DIR/scripts/review_context.py" --repo "$REPO" --mode branch --base "$BASE" --head "$HEAD" > "$REVIEW_DIR/context.json"
python3 "$SKILL_DIR/scripts/validate_review.py" --review "$REVIEW_DIR/review.json" --context "$REVIEW_DIR/context.json" --repo "$REPO"
```

Use `--mode staged`, `--mode worktree`, or exact `--mode range` when that is the requested comparison.
Use the same installed Git wrapper through `--git-command` when required by repository instructions.
The validator does not collect requirements, write the review, apply fixes, or publish results.
Read every reported limit before delivering the report.

## Comparison identity and coverage

Set `schema_version` to the string `1.0`.
Copy `target` values directly from collected context:

| Field | Required value |
| --- | --- |
| `repository` | Exact collected repository locator. |
| `mode` | `worktree`, `staged`, `branch`, or `range`. |
| `base` | Full resolved base commit, or `null` for an unborn local repository. |
| `head` | Full resolved head commit, or `null` for an unborn local repository. |
| `comparison_base` | Full merge base or exact baseline commit; `null` only for an unborn local repository. |
| `fingerprint` | Collected SHA-256 comparison fingerprint. |
| `line_basis` | `raw-content-comparison`. |

Use `reviewed_paths` for inspected changed paths.
Use `skipped_paths` objects with `path` and a nonempty `reason` for every uninspected path.
Both lists must be unique, disjoint, and together match the collected file paths exactly.
Include changed configuration, tests, deletions, binaries, and generated files in that accounting.
Do not mark a path reviewed merely because a tool listed it.

## Independent review axes

`axes` requires `spec`, `standards`, `security`, `integration`, and `tests`.
Each axis contains `status` and a nonempty `reason` that states evidence and limits.

| Status | Meaning |
| --- | --- |
| `REVIEWED` | The stated scope was inspected without a confirmed actionable finding on that axis. |
| `ISSUES_FOUND` | One or more reported findings belong to that axis. |
| `UNVERIFIED` | Missing context prevents the stated review conclusion. |
| `NOT_APPLICABLE` | The axis does not apply; the reason explains why. |

Each finding's primary and related axes must use `ISSUES_FOUND`.
Each `ISSUES_FOUND` axis requires at least one finding assigned through either relationship.
Use one finding for a shared root cause rather than duplicating it across review passes.
Missing specifications limit specification conclusions but do not prevent useful correctness or security inspection.
Account for each supplied acceptance criterion in axis reasons, evidence references, or the accompanying trace table.
Link criterion definitions, implementation, assertions, and retained execution separately.
The validator cannot discover criteria omitted from the supplied report.

## Findings

Every finding requires these fields:

| Field | Contract |
| --- | --- |
| `id` | Unique, nonempty finding identity. |
| `axis` | One of the five review axes. |
| `priority` | Existing `P0`, `P1`, `P2`, or `P3` scheme. |
| `confidence` | `CONFIRMED` or `INFERRED`; no numerical confidence gate. |
| `title` | Concise, actionable defect title. |
| `path` | An inspected path in the collected file records. |
| `location` | `INLINE` or `FILE`. |
| `side` | `LEFT` or `RIGHT` for inline findings; `null` for file findings. |
| `line` | Positive integer for inline findings; `null` for file findings. |
| `trigger` | Concrete input, state, or sequence that exposes the defect. |
| `impact` | Observable consequence with evidence and relevant limits. |
| `owner` | Known owner or `unknown`. |
| `fix` | Concrete next correction or required investigation. |
| `verification` | Focused assertion, reproduction, or suggested verification. |
| `evidence_refs` | Nonempty source locator strings with exact revisions or hashes. |
| `unverified_conditions` | Explicit condition strings; nonempty for inferred findings. |

Optional `related_axes` lists other affected axes for the same root cause.
Use unique supported axis names and exclude the primary `axis`.
Those axes reference the same finding through this field and must also record `ISSUES_FOUND`.

`CONFIRMED` describes the stated source-supported mechanism; it does not claim successful execution.
Use `checks_executed` to record actual observed execution separately.
Attempt to disprove each candidate using actual callers, protections, contracts, and assertions before accepting it.
Use `unverified_assumptions` for unresolved suspicions that do not justify a finding.

For `INLINE`, `RIGHT` lines must belong to the file's `added_ranges`.
`LEFT` lines must belong to its `removed_ranges`.
Use the current context record's `path`; use `old_path` when mapping an applicable rename to a provider's baseline path.
For binary or unsupported text boundaries, use a justified `FILE` finding instead of inventing a line number.
File findings cannot become inline comments without separate, valid provider annotations.

## Checks, outcomes, and writing review

`checks_executed` contains objects with `command`, `result`, and `notes`.
Results are `PASSED`, `FAILED`, or `ERROR` for checks actually attempted.
Use `suggested_checks` for unexecuted commands and verification suggestions.
Describe missing tools, skipped checks, unavailable platforms, and their consequences in relevant axis reasons or assumptions.
Mark an affected axis `UNVERIFIED` when a material assumption prevents its conclusion.
An assumption alone does not mechanically change the outcome; its affected axis must record the limit.
Explain failed or errored checks through the affected axes or findings rather than treating every command failure as a defect.
Keep baseline failures separate from failures introduced by the selected change.
`summary` contains a concise assessment with material limits.

Set `outcome` from the report's actual evidence state:

| Outcome | Deterministic condition |
| --- | --- |
| `FINDINGS_PRESENT` | At least one finding or an `ISSUES_FOUND` axis. |
| `INCOMPLETE` | No findings, but skipped paths, unverified axes, or collected limitations remain. |
| `NO_ACTIONABLE_FINDINGS` | No findings and none of those coverage gaps. |

An outcome does not grant merge approval, prove complete test coverage, or establish business verification.
The validator does not derive correctness from a successful command or report shape.

Every saved report includes `writing_review` with separate automated and complete ASD review states.
Use `standard: ASD-STE100`, factual `automated_check`, factual `asd_review`, `reviewer`, `reviewed_at`, and `limitations`.
Keep `asd_review: PENDING` and reviewer fields `null` until a complete writing review occurs.
Retain the template's limitation about dictionary and grammar coverage.
Passing the structural validator does not complete the ASD review.

## Validation limits

Unknown report fields, duplicate JSON keys, invalid types, non-finite numbers, and incomplete coverage fail validation.
Each input file is limited to 4 MiB and 64 nested JSON containers.
Oversized reports require a separately agreed smaller comparison; do not truncate scope evidence or omit paths.
The validator checks supplied local ranges; it does not authenticate the report or its author.
With `--repo`, it independently recollects the frozen local scope and compares metadata.
Without `--repo`, altered context documents can only receive structural checks.
Frozen commit validation does not establish that a moving branch or remote PR still has that head.
Recheck the remote head and provider diff anchors before any authorized publication.

The local collector compares raw bytes, including untracked files and line-ending changes.
Git attributes, hunk algorithms, rename detection, and provider conventions can produce different published anchors.
Structural success does not establish technical accuracy, criterion completeness, correct citations, or safe severity classification.
Those claims require independent source review and meaningful verification.
