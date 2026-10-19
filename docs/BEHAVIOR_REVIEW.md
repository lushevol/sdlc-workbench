# Behavior evidence review

The `assurance` CLI checks a narrow behavior evidence contract.
It validates saved records, checks source freshness, preserves baselines, and compares declared evidence relationships.
Every business verification field remains `NOT_VERIFIED`.

Use the [shared procedure](../.agents/skills/verify-implementation/references/behavior-review.md) to extract behaviors, inspect source, map assertions, and classify gaps.
Use the [traceability template](../core/knowledge/templates/sdlc/traceability-record.md) for human review notes.
The JSON baseline adds deterministic checks; it does not replace approved knowledge or its audit history.

## Interpret the result

Read contract validity, freshness, retained results, and business verification separately.

| Field | Values | Meaning and limit |
| --- | --- | --- |
| `contract_status` | `VALID`, `INVALID` | Schema and reference checks pass or fail. Validity does not prove source meaning. |
| `freshness` | `CURRENT`, `STALE`, `UNKNOWN` | Current retained bytes and declared Git sources agree, differ, or cannot be fully assessed. |
| Execution `source_freshness` | `CURRENT`, `STALE`, `UNKNOWN` | Source inventory, source bytes, and declared bindings agree, differ, or remain incomplete. |
| Execution `result` | `PASSED`, `FAILED`, `UNKNOWN` | The retained report declares this result. The command does not authenticate its execution. |
| Execution `assertion_bindings` | `DECLARED` | Review metadata names a retained check. The original run did not contain these baseline bindings. |
| `verification` | `NOT_VERIFIED` | The command never grants business verification. |

A `VALID` baseline can contain stale evidence, failed execution, missing approval, simulation, or a lower verification level.
`CURRENT` concerns the selected retained bytes and declared revisions.
It does not establish the latest repository HEAD, deployed configuration, or actual service execution.
Missing execution keeps overall freshness `UNKNOWN` unless another item makes it `STALE`.
Read diagnostics and per-record states beside the aggregate result.

The implementation provides no approval engine, assertion parser, or native test-result importer.
It does not authenticate reviewer identities, execution modes, commands, or environments.
Use existing [knowledge governance](../knowledge/README.md) for human review and publication.

## Prepare the baseline

Print the installed schema before creating records:

```sh
ai-sdlc assurance schema > behavior-review.schema.json
```

Use `schema_version: 1` and all required top-level collections.
The schema rejects undeclared properties.
Use globally unique record IDs and at least one active behavior.
Keep behavior IDs prefixed with `story_id` and a colon.
For example, story `STORY-104` can contain behavior `STORY-104:BEH-01`.

| Collection or field | Required content |
| --- | --- |
| `baseline_id` | A unique retained baseline identity. |
| `story_id`, `scope`, `limitations` | Stable story identity, included evidence scope, and explicit limits. |
| `artifacts` | `INTENT`, `CODE`, `TEST`, or `EXECUTION` records with retained paths and raw file hashes. |
| `behaviors` | Stable IDs, versions, criterion IDs, intent locators, Gherkin clauses, measures, negative cases, and required levels. |
| `links` | Behavior/artifact identities, canonical record hashes, exact line ranges, relationship grades, and limits. |
| `executions` | Retained result identity, code inventory, declared assertion bindings, mode, level, environment, command, and limits. |
| `findings` | Behavior identity, gap category, evidence IDs, consequence, owner, and next action. |

`IMPLEMENTED_BY` links target `CODE` artifacts.
`ASSERTED_BY` links target `TEST` artifacts and include the inspected assertion.
Grades are `CONFIRMED`, `LIKELY`, `POSSIBLE`, and `UNRESOLVED`.
These are declared relationship grades; the command does not inspect their semantic correctness.

Behavior `state` is `ACTIVE` or `RETIRED`.
Required levels are `UNIT`, `INTEGRATION`, or `SYSTEM`.
Execution modes are `CONTROLLED_SOURCE`, `SIMULATION`, or `ACTUAL_IMPLEMENTATION`.
Record actual boundaries and limitations beside the selected mode and level.

Use strict UTF-8 JSON objects with unique keys and finite numbers.
Baseline and evidence files must be regular local files of at most sixteen MiB.
Evidence paths must stay inside the workspace without symbolic links or traversal.
Preserve original evidence bytes when creating retained snapshots.

Every `CODE` artifact requires a registered `repository_id`, exact `revision`, and repository-relative `source_path`.
Revisions must contain the complete 40-character or 64-character hexadecimal Git object ID.
When another artifact supplies Git metadata, it must supply all three fields.
The command compares retained hashes with Git bytes at those declared revisions.
Unavailable checkouts or unavailable revision bytes produce unknown source freshness.
The operation does not fetch repositories or rewrite source files.

## Distinguish the two hashes

Artifact `sha256` identifies the raw retained file bytes.
Changes to whitespace or file endings change that hash.

Fields such as `record_sha256` identify a complete metadata record.
Calculate these hashes from sorted JSON keys, compact separators, preserved Unicode, UTF-8 encoding, and SHA-256:

```python
import hashlib
import json

def record_sha256(record):
    encoded = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
```

Hash the entire referenced record, including its ID, source metadata, and limitations.
Do not substitute a raw file hash for a record hash.
Changed metadata can invalidate a relationship even when the retained file bytes remain unchanged.
Hashes identify content; they do not authenticate approval or execution.

## Bind retained execution declarations

Reference an unchanged original JSON result through an `EXECUTION` artifact.
Its usable fields include:

```json
{
  "status": "PASSED",
  "source_sha256": {
    "service.py": "<original 64-character lowercase SHA-256>"
  },
  "checks": [
    {"name": "accepts valid instruction", "status": "PASSED"}
  ]
}
```

This fragment illustrates field names; replace the digest placeholder only with an actual retained result.
Do not rewrite an original run to create missing provenance.
Native Robot or other reports require separate inspection when they lack this JSON source inventory.

Supply a complete, nonempty `source_sha256` inventory from the original run.
Its paths must match the execution's bound `code_artifact_ids` exactly.
Each bound code artifact needs matching retained bytes and Git bytes at its declared revision.
One execution inventory uses one repository and one exact revision.
Use separate execution records for independent repository revisions.
The command cannot discover source files omitted from the original inventory.

Each assertion binding records `link_id`, `link_record_sha256`, and the original `check_name`.
The named check must exist with a `PASSED` or `FAILED` result.
Check names must be unique strings.
Bindings remain `DECLARED` because the baseline adds this relationship after the original run.
Preserve original results and bindings when later code, assertions, or intent change.

## Validate, save, and report

Replace `PATH` and baseline filenames with the selected workspace and input files.
Baseline inputs must remain inside that workspace.
All operations print JSON to stdout.
Shell redirection can retain the result separately from the baseline.

```sh
ai-sdlc --workspace PATH assurance validate --baseline review.json
ai-sdlc --workspace PATH assurance validate --baseline review.json --require-current
ai-sdlc --workspace PATH assurance save --baseline review.json
ai-sdlc --workspace PATH assurance report --baseline review.json > review-report.json
```

Normal `validate` succeeds when the contract is valid, including valid stale or unknown evidence.
`validate --require-current` returns a nonzero exit code for invalid, stale, or unknown evidence.
`report` emits the same analysis without writing a Markdown report.
It returns a nonzero exit code when the contract is invalid.
Neither a zero exit code nor `CURRENT` grants verified business behavior.

`save` requires a valid contract and permits valid stale or unknown evidence.
It creates `relationships/requirement-code/baselines/<baseline_id>.json` with exclusive file creation.
An existing baseline ID fails; the command never overwrites its file.
The response includes `saved_path`.
Save successor evidence with a new baseline ID and preserve the earlier file.

Artifact `lint` and workspace `validate` retain their separate contracts.
Use them for authoring documents and governed knowledge as applicable.
They do not replace `assurance validate` for this JSON baseline.

## Interpret metrics

The implemented metrics count active behaviors, including unmapped active behaviors in every denominator.
Retired behaviors remain in history and do not enter that denominator.

| Metric | Numerator and limit |
| --- | --- |
| `behavior_to_code` | Behaviors with a current `CONFIRMED` implementation link. Source meaning remains a review responsibility. |
| `behavior_to_test` | Behaviors with a current `CONFIRMED` assertion link. Required test levels are not an automated verification gate. |
| `current_source_execution` | Behaviors with current source execution declarations covering their current code links and an applicable assertion binding. |

Each metric includes `numerator`, `denominator`, and `percentage`.
`current_source_execution` measures declared source freshness and binding availability.
It can include failed results, simulation, and lower-level execution.
It is not passing behavior coverage or Verified Behavior Coverage.
The runtime does not calculate the six directional review metrics from the shared procedure.
Those measures require separately declared code and test inventories.
Empty or retired-only behavior scope is invalid and cannot establish successful coverage.

## Compare later evidence

```sh
ai-sdlc --workspace PATH assurance compare \
  --before relationships/requirement-code/baselines/story-review-1.json \
  --after relationships/requirement-code/baselines/story-review-2.json > comparison.json
```

Both contracts must be valid and share the same `story_id`.
Their `baseline_id` values must differ.
Preserve removed behavior IDs as `RETIRED` records in the successor baseline.
Increase a behavior's version when any of its record contents change.
Behavior versions cannot decrease.
Check affected links and execution declarations after their dependencies change.

The comparison returns `changed_records`, `affected_behaviors`, and both current analyses under `before` and `after`.
It follows declared artifact, behavior, link, execution, and finding dependencies.
Both analyses read current retained files during comparison.
Their counts do not establish historical assurance improvement.
Changed or removed finding records do not establish approved resolution.
The comparison's business verification remains `NOT_VERIFIED`.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
