# Resume interrupted knowledge processing

> **Implementation is in progress.** Inspect existing recovery controls and resume the earliest unfinished authorized operation.

## Request and scope

Source is the current Codex conversation, received 18 November 2026.
Exact user input follows.

```text
add a resume capability to knowledge processing while any breaking on any step in processing.
```

The request authorizes knowledge-processing resume enhancements and applicable verification.
Use existing shared skills, task checkpoints, source receipts, governance events, and wiki recovery controls.
Cover interruptions during source preparation, canonical processing, review, audit, completion receipts, and derived wiki maintenance.
Retain saved answers, accepted work, partial drafts, source revisions, and existing authorization when processing resumes.
Continue independent scopes while a required decision blocks another scope.

## Starting state and affected scope

Source revision is `d460e4ed8`.
Existing unrelated changes include the deleted `core/connectors/yarn.lock` and untracked `core/release-report/`.
Affected consumers include knowledge lifecycle skills and generated workspaces.
Inspect runtime entry points before choosing any runtime changes.
Qualitative risk is medium because retries can duplicate writes or conceal unfinished operations.

## Work and verification

1. Map each interruption boundary to its existing durable evidence and safe recovery operation.
2. Implement the missing resume behavior using the existing owners.
3. Evaluate each completed enhancement before continuing to the next enhancement.
4. Verify interrupted retries, unchanged accepted work, changed inputs, and completion through normal entry points.
5. Verify packaging and installed shared skills when distribution changes.

Current documentation owners are `docs/KNOWLEDGE_LIFECYCLE.md` and the affected operation references.
The target is successful recovery at every supported processing boundary, with zero repeated accepted units or duplicate audit events.
Retain actual test counts, evidence links, remaining decisions, and material execution limits here.

## Delivered recovery behavior

Source views now build in ignored staging directories and publish one complete directory.
An interrupted render leaves no partial requested output and can retry the same output path.

Wiki compilation now treats a persisted `running` attempt as retryable when its derived outputs are unchanged.
Failures while binding generated pages persist a `failed` attempt without advancing an incomplete source binding.
The next local plan returns that source to the retry queue, or to explicit output review when partial derived pages exist.
Successful compilation still ends at explicit output review.

Existing source plans, canonical receipts, sealed harness reports, audit events, and paired wiki provenance remain the resume records for their stages.
Repeated completion remains idempotent when the same plan and reviewed result are supplied.

## Verification

Focused source and wiki recovery tests passed with the project OpenKB environment.

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest \
  tests.test_source_preparation.SourcePreparationTests.test_interrupted_view_can_retry_same_output_path \
  tests.test_source_preparation.SourcePreparationTests.test_target_change_during_link_creation_never_publishes_valid_view \
  tests.test_source_preparation.SourcePreparationTests.test_views_bind_links_and_excerpts_to_original_and_output_hashes \
  tests.test_openkb_workflow.OpenKBWorkflowTests.test_binding_failure_marks_compilation_retryable \
  tests.test_openkb_workflow.OpenKBWorkflowTests.test_failed_attempt_stays_visible_and_retryable -v
```

The full source, incremental, CLI, and wiki regression groups contain 123 passing tests in this environment.
The repository-wide suite and wheel build remain pending.
Live provider compilation, remote access, publication, and deployment authorization remain outside this maintenance check.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
