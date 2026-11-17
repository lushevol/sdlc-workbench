# Workbench optimization plan

> **Optimize dependable completion and reduce supervision.** Extend existing source status, recovery pointers, question reconciliation, and evaluation tools.
> **Implement in measured stages.** Freeze a baseline first. Retain changes only when outcomes improve without losing meaning or evidence.
> This is an unapplied plan. Numeric targets are proposals, not current results or whole-system guarantees.

## Direction, scope, and starting evidence

Authority: [exact planning request](01-maintenance.md#planning-follow-up-17-november-2026).
Source checkout inspected: `9cf70cc7a4abaf81dd81bb9c475b362dfc4dbfca`, with unrelated local changes recorded in the retrospective.
Implementation must recheck revisions and preserve unrelated changes before editing.

The primary outcome is fewer user interventions between a stated goal and a trustworthy result.
Secondary outcomes are accurate status, reliable recovery, preserved meaning, lower repeated processing cost, and practical portability.
The [retrospective](01-maintenance.md#explicit-preferences) supplies the preference evidence.

Preserve the single Python runtime, installed package name, existing engine lifecycles, and independent repository ownership.
Use task records and current receipts as authorities. Add no parallel status database, question store, or background runner.
Keep plain workspace discovery `status` compatible. Keep domain intent, conformance, publication, and deployment decisions separate.
No dependency additions are planned.

Technical implementation owner: unassigned Workbench maintainer. Semantic assessment owner: unassigned independent reviewer.
Human business acceptance and publication owners remain those recorded in the selected business task.

## Sequence and completion conditions

Stage 0 precedes implementation. Stages 1, 2, and 4 can then use separate file ownership.
Stage 3 evaluates semantic safeguards. Stage 5 measures reuse. Stage 6 integrates the complete workflow and installed distribution.
Coordinate shared edits to `core/cli.py`, lifecycle guidance, and final packaging through one writer.
Commit each verified stage separately. Restore or revise a stage when its comparison shows a regression.

### Stage 0 — Freeze the baseline and success criteria

Direction: Measure actual effort and quality before expanding infrastructure.

1. Select eight retained source documents: two from each of the four current knowledge collections.
2. Include conditions, exceptions, conflicts, draft intent, cross-topic dependencies, and the diagnosed zero-output cases where applicable.
3. Define 24 atomic predicates and 12 questions from those exact sources. Label applicable claim classes and expected uncertainty.
4. Record each source hash, locator, candidate version, wiki output, recipe, reviewer, and permitted operation.
5. Run three baseline cohort-workflow trials using pinned skills, selected models, reasoning, fixtures, and concurrency.
6. Record time, actual token usage when available, user interventions, unsupported claims, and repeated work.
7. Pin one engineering baseline/candidate case with available assertions and execution prerequisites for Stage 6.
8. Run its baseline assessment before workflow changes when prerequisites permit. Otherwise, report engineering metrics as absolute values only.

Files:

- Update the baseline table below and the existing [maintenance record](01-maintenance.md) with actual execution references.
- Create task-scoped `evidence/optimization-baseline.json` and `evidence/optimization-scorecard.json` during execution.
- Retain canonical run payloads once. Store their paths and hashes in those two manifests.

Expected outcome: A reproducible before/after comparison with explicit denominators and task-specific completion evidence.

Proposed acceptance: All eight documents, 24 predicates, and 12 questions have exact locators and reviewed expectations.
Record unavailable model usage as UNKNOWN. Input bytes may be reported separately; they are not token measurements.
An unavailable engineering environment limits that pilot; it does not block independent harness work.

| Baseline | Current evidence | Stage 0 measurement |
| --- | --- | --- |
| Source conversion | The inspected diagnostic reports 139/622 output-linked identities. Complete semantic coverage remains UNKNOWN. | Freeze selected source membership, receipts, and output hashes. Recompute current counts before use. |
| Review quality | The retrospective identifies lost qualifications and challenged sufficiency judgments. No bounded benchmark score exists. | Assess the 24 predicates and 12 questions with exact source support. |
| Supervision and recovery | Repeated status and continuation requests establish friction. Comparable effort measurements remain unavailable. | Record three cohort-workflow trials, interventions, and interruption timestamps. |
| Latency and processing cost | No comparable measurements were established by the retrospective. | Record machine, workload, elapsed time, tokens when available, and accepted distinct outcomes. |

### Stage 1 — Make current progress accurate and inexpensive

Direction: Expose trustworthy source status and combine existing lifecycle facts in one current task summary.

Current evidence: [plan_sources()](../../core/ingestion/incremental.py#L304) writes baseline files.
Its [queue calculation](../../core/ingestion/incremental.py#L263) also counts some excluded pages as unchanged.
Therefore, unchanged counts must not be presented as completed knowledge conversion.

Steps:

1. Extract shared classification from `_capture()` and `_queues()` without changing existing plan results.
2. Add `source_status(root, source_id, recipe)` in the same runtime module.
3. Report present kept identities, current output-linked receipts, current zero-output receipts, selection review, held items, and processing reasons.
4. Mark missing preparation, stale bindings, and concurrent changes explicitly. Include capture time, scope, recipe, and source bindings.
5. Add the proposed `ai-sdlc sources status --source ID --recipe ID` route.
6. Reuse wiki `update_plan()` with its exact recipe. Do not call compilation or select an external provider for status.
7. Recheck component bindings after source/wiki inspection. Report concurrent changes as incomplete before updating the existing task header.
8. Show source processing, semantic review, wiki freshness, publication, blockers, and next action as separate facts.

The coordinator retains exact supporting receipt links in that task header. This update is separate from status inspection itself.

Files to modify:

- [core/ingestion/incremental.py](../../core/ingestion/incremental.py): shared classification and public status helper.
- [core/cli.py](../../core/cli.py): additive source-status parser and dispatch.
- [tests/test_incremental_ingestion.py](../../tests/test_incremental_ingestion.py): denominators, zero-output separation, invalidation, and no durable writes.
- [tests/test_source_preparation_cli.py](../../tests/test_source_preparation_cli.py): command routing, recipe handling, and structured errors.
- [manage-knowledge-lifecycle/SKILL.md](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md): use the source result and existing wiki plan.
- [docs/KNOWLEDGE_LIFECYCLE.md](../../docs/KNOWLEDGE_LIFECYCLE.md): explain current metrics and their limits.

Reuse [wiki update_plan()](../../.agents/skills/llm-wiki/scripts/wiki.py#L364). Change its implementation only if the no-durable-write check finds a defect.
Leave `Workbench.describe()` and existing workspace discovery contracts unchanged.

Expected outcome: One understandable progress summary, backed by current calculations rather than manually reconstructed counts.

Proposed acceptance:

- Exact expected classification for every synthetic identity; zero excluded identities counted as converted.
- Zero durable changes to plans, receipts, sources, records, audits, or wiki content during status inspection.
- Concurrent component changes produce an incomplete diagnosis, never an unsupported coherent-snapshot claim.
- Measure 20 warm status calls on a fixed 1,000-source, 200-record fixture. Provisional p95 target: five seconds or less.
- Record cold latency separately. Keep timing benchmarks outside timing-sensitive unit-test assertions.

Transient lock creation is allowed by the existing lock contract. Cross-lifecycle inspection is not one atomic transaction.

### Stage 2 — Make interruption recovery explicit and testable

Direction: Recover accepted work and the next authorized action without requiring the user to repeat context.

Current evidence: [run_hook()](../../core/hooks.py#L261) retains session-scoped results but shows only a generic record pointer at startup.
Existing task [checkpoint rules](../README.md#save-case-evidence-and-resume-checkpoints) already define the durable recovery record.

Steps:

1. Add `inspect_scope(root, client, session)` using existing identity, scope, loading, and fingerprint helpers.
2. Return bound paths, missing inputs, recorded check status, and CURRENT/STALE/NOT_CHECKED freshness.
3. Add the proposed `ai-sdlc hooks inspect --client CLIENT --session SESSION` route.
4. Include the last recorded ACTION_REQUIRED in startup advice. Label its freshness unchecked until inspection.
5. Keep document contents out of native startup context. Link the existing living record instead.
6. Recover a new session by inspecting the explicitly named old session, reopening its checkpoint, and rebinding existing scope pointers.
7. Verify actual dispatch and the next accepted checkpoint. Requested model settings alone do not prove execution identity.

Files to modify:

- [core/hooks.py](../../core/hooks.py): inspection helper and bounded startup advice.
- [core/cli.py](../../core/cli.py): inspect parser and dispatch.
- [tests/test_hooks.py](../../tests/test_hooks.py): inspection, stale results, missing scope, isolation, and failure visibility.
- [tests/test_interfaces.py](../../tests/test_interfaces.py): additive CLI behavior and malformed arguments.
- [docs/HOOKS.md](../../docs/HOOKS.md): same-session inspection and explicit cross-session rebinding.
- [manage-knowledge-lifecycle/SKILL.md](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md): checkpoint-first recovery.

Expected outcome: Recovery exposes unfinished work without inventing a scheduler or selecting tasks from dirty files.

Proposed acceptance:

- Eight recovery cases across three adapters: unbound, recorded failure, changed watch, missing input, relocation, malformed state, same-session recovery, new-session rebinding.
- Correct scope and diagnosis in all 24 combinations; zero inspection writes or validator dispatches.
- Three controlled interruptions of the selected task; zero repeated accepted cases and zero requests to restate saved answers.
- Provisional median recovery target: five minutes from fresh-session entry to the first useful authorized action.
- Record time to the next accepted checkpoint separately. Do not substitute a written recovery plan for resumed work.

### Stage 3 — Detect lost meaning and unsupported quality judgments

Direction: Test semantic preservation and reader usefulness beyond valid hashes and receipt declarations.

Current evidence: [wiki review checks](../../.agents/skills/llm-wiki/scripts/wiki.py#L895) validate claim-review declarations.
The [evaluation helper](../../tests/skill_evaluation.py) already prepares isolated inputs and supports installed workspace skills.
Its [review procedure](../../tests/README.md#evaluate-skill-decisions) keeps assessor criteria outside the evaluated agent's context.

Steps:

1. Add three cases: lost behavioral qualification, misleading zero-output completion, and a detailed but unsupported answer.
2. Define expected findings in the existing assessor rubric. Keep rubric criteria out of answering-agent inputs.
3. Run the frozen 12-question, 24-predicate cohort before and after the proposed workflow changes.
4. Use three independent question trials per workflow: 72 total answers across baseline and candidate.
5. Have an independent reviewer inspect source support, omissions, claim classification, conflicts, and useful organization.
6. Preserve adverse examples and correction reasons. Revise shared guidance only where failures justify a change.
7. Compare the diagnosed zero-output cases with actual source clauses and candidate coverage.

Files to modify:

- [tests/skill-evaluation-cases.json](../../tests/skill-evaluation-cases.json): three adversarial cases and source fixtures.
- [tests/skill-evaluation-rubric.json](../../tests/skill-evaluation-rubric.json): independent semantic criteria.
- [tests/README.md](../../tests/README.md): trial protocol, denominators, and reporting limits.
- Conditional: [evaluate-knowledge-retrieval/SKILL.md](../../.agents/skills/evaluate-knowledge-retrieval/SKILL.md) and [review-knowledge-claims/SKILL.md](../../.agents/skills/review-knowledge-claims/SKILL.md), for observed procedural gaps.

Reuse the existing evaluator and claim-removal controls. No new semantic grading service is planned.
Keep legitimate zero-output `no_change` receipts supported. Review omission evidence before proposing a narrower runtime completion contract.
Actual business-record corrections belong to their owning task and governance scope.

Expected outcome: Quality comparisons identify missing meaning and unsupported claims even when structural checks pass.

Proposed acceptance: All 24 material predicates remain correctly represented or explicitly accounted for in each candidate trial.
Detect all three seeded faults in all three trials. Permit zero unsupported critical claims or invented publication/execution claims.
Score fidelity and organization separately. Success establishes only this bounded benchmark.
Question trials measure answer quality. Cohort-workflow trials separately measure coordination, recovery, and processing effort.

### Stage 4 — Turn existing questions into an actionable attention view

Direction: Reduce repeated questions and distinguish agent investigation from required human decisions.

Current evidence: [reconcile_questions()](../../core/question_reconciliation.py#L12) already handles multiple documents and answer propagation.
REFERENCES_COMPLETE deliberately concerns references. It does not establish that questions have been answered.

Steps:

1. Add exact source anchors and authored owner/next-action fields to reconciled rows where available.
2. Derive an `attention` array and explicit status counts from existing rows and findings.
3. Preserve unknown status. An absent Status line does not establish an unanswered question.
4. Keep existing top-level status, exit semantics, IDs, answer hashes, and `verification: NOT_VERIFIED`.
5. Have the coordinator separate source investigation, human policy decisions, publication review, and deferred work.
6. Group related decisions through semantic review in the existing question document. Preserve original questions and user answers.
7. Explicitly disclose unsupported table formats. Do not claim the heading-based checker has parsed all 310 bundle rows.

Files to modify:

- [core/question_reconciliation.py](../../core/question_reconciliation.py): additive attention fields and conservative authored-field extraction.
- [tests/test_question_reconciliation.py](../../tests/test_question_reconciliation.py): unknown statuses, existing answers, source anchors, and stale consumers.
- [docs/QUESTION_RECONCILIATION.md](../../docs/QUESTION_RECONCILIATION.md): attention categories and unchanged reference-status meaning.
- [resolve-knowledge-questions/SKILL.md](../../.agents/skills/resolve-knowledge-questions/SKILL.md): investigate attention items before asking.
- [manage-knowledge-lifecycle/SKILL.md](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md): scoped blockers and consolidated decisions.

Expected outcome: A compact attention view points to existing authoritative answers and leaves independent work available.

Proposed acceptance: Correctly account for 12 reviewed test entries, including answered, unknown, deferred, duplicate, stale, and evidence-follow-up cases.
Zero already-answered questions are sent back to the user in three pilot trials.
Every human-decision item names its consequence and source, plus an owner or explicit unknown.
Measure compression using reviewed distinct decisions, not raw question-row counts.

### Stage 5 — Verify incremental savings and control new evidence growth

Direction: Spend model effort on changed work and retain one canonical evidence payload.

Steps:

1. Run unchanged, one-source-change, and shared-dependency-change variants of the frozen cohort.
2. Record new original review, dependency reconciliation, reused work, and receipt refreshes separately.
3. Compare expected affected closure with actual semantic work and output changes.
4. Measure input tokens, elapsed active work, and newly retained bytes for equal-quality accepted outcomes.
5. Reuse current outputs and payload references. Keep failures, original snapshots, audit history, and recovery evidence.
6. Change invalidation or payload handling only when the comparison demonstrates unnecessary work.

Conditional implementation files:

- [core/ingestion/incremental.py](../../core/ingestion/incremental.py) and [tests/test_incremental_ingestion.py](../../tests/test_incremental_ingestion.py): proven over-invalidation or missed dependencies.
- [wiki.py](../../.agents/skills/llm-wiki/scripts/wiki.py) and [tests/test_openkb_workflow.py](../../tests/test_openkb_workflow.py): proven repeated compilation or incorrect reuse.
- [core/evidence/README.md](../../core/evidence/README.md) and [tasks/README.md](../README.md): only if measured payload duplication reveals a missing rule.

Existing reuse may already satisfy this stage. Passing measurements can close it without code changes.

Expected outcome: Less repeated reading and evidence duplication without weakening review or provenance.

Proposed acceptance:

- Unchanged eligible inputs trigger zero semantic processing and zero new completion events in all three repetitions.
- Changed runs process the reviewed affected closure; zero omitted necessary dependents.
- Every retained evidence reference resolves to the intended hash. No historical evidence deletion is included.
- Candidate quality must meet Stage 3 before cost savings count.
- If baseline redundant semantic work exists, target a 30% reduction in input tokens per accepted distinct outcome.
- If the baseline already has zero redundant work, preserve it. Do not invent a savings percentage.

### Stage 6 — Prove the combined workflow and installed adoption

Direction: Demonstrate useful engineering results and practical operation outside the source checkout.

Engineering pilot:

1. Recheck the selected portal case's source revisions, expected behavior, assertions, consumer scope, environment, and authorization.
2. Use one existing review index and the existing assurance commands.
3. Compare the same relevant case at baseline and candidate where execution is available.
4. Report all three coverage mappings, passing execution separately, user impact, residual gaps, and the next decision.
5. Compare interventions and decision time with Stage 0's engineering assessment. Without that baseline, report absolute metrics only.

Files updated during the authorized pilot:

- Existing [portal coverage record](../portal-background-session-20261019/09-coverage.md) and [renewal execution record](../portal-background-session-20261019/08-test-execution-renewal.md), if that scope is selected.
- The selected task's existing review index and canonical case definitions only when reviewed findings require updates.
- Conditional: [docs/BEHAVIOR_REVIEW.md](../../docs/BEHAVIOR_REVIEW.md) for a demonstrated procedural gap.

Reuse [core/review_index.py](../../core/review_index.py) and [core/review_coverage.py](../../core/review_coverage.py). No new coverage engine is planned.
Diagnostic completion requires accurate accounting; a discovered business failure remains a failure.

Installed adoption pilot:

1. Extend the existing source-distribution, wheel, external-installation, and workspace-initialization test.
2. Exercise installed source status, hook inspection, and evaluator skill inputs outside this checkout.
3. Confirm portable paths, empty catalogs, preserved native upstream files, and excluded runtime/project history.
4. Rebuild matching-platform offline bundles after packaged skills change. Use existing bounded acquisition and validation.
5. Run one independent-system workflow in the intended company environment.
6. Observe actual start/stop dispatch for each available selected client. Record unavailable clients as untested.
7. Update setup and dependency limits from observed target results.

Files to modify:

- [tests/test_workspace_layout.py](../../tests/test_workspace_layout.py): extend the existing external installation pipeline.
- [docs/SETUP.md](../../docs/SETUP.md) and [docs/DEPENDENCIES.md](../../docs/DEPENDENCIES.md): observed setup, bundle, and target limits.
- Conditional: [scaffold.json](../../scaffold.json), [core/workspace.py](../../core/workspace.py), [core/bootstrap.py](../../core/bootstrap.py), or [core/offline.py](../../core/offline.py), only for demonstrated distribution defects.

Expected outcome: One complete decision workflow works through the installed package and selected real client/environment.

Proposed acceptance:

- Every selected AC, changed behavior, assertion, and required execution combination is accounted for, with unknowns explicit.
- All applicable candidate unit tests pass; no skipped failures or weakened assertions.
- Required installed artifacts match their declared hashes: 100%. Prohibited generated-workspace artifacts: zero.
- Offline installation makes zero unexpected acquisition attempts.
- Report actual native dispatches as observed clients divided by selected clients. Do not replace target evidence with adapter fixtures.
- Provisional knowledge-workflow target: 50% fewer avoidable user interventions than matched baseline trials, with no semantic-quality regression.
- Apply an engineering improvement percentage only when the same-case baseline assessment exists.

## Measurement definitions

Use the same cohort, revisions, environment, model settings, and concurrency for paired comparisons.
Run three knowledge-workflow trials and three question trials per variant. The latency metric uses 20 timing samples.
Report the engineering pilot's actual trial count. Do not borrow its baseline from the knowledge cohort.
Report individual values and medians. Small samples establish a pilot result, not broad statistical reliability.

| Metric | Calculation and evidence | Proposed criterion |
| --- | --- | --- |
| Avoidable supervision | Count prompts needed to repeat saved context, restart accepted work, correct status, or reconcile duplicate outputs. Exclude new business decisions. | Candidate median at most 50% of baseline; report absolute counts when baseline is zero. |
| Progress correctness | Correctly classified synthetic identities / frozen synthetic identities. Compare source membership and hashes, not counts alone. | 100%; zero excluded identities counted as converted. |
| Recovery | Minutes from fresh entry to first useful authorized action; also record time to next accepted checkpoint. | Median at most five minutes; zero repeated accepted cases. |
| Predicate preservation | Correctly retained or explicitly justified predicates / 24 reviewed predicates. Report every disposition. | 24/24 per trial; zero unsupported critical claims. |
| Seeded-fault detection | Correctly identified seeded failures / three seeded cases, per trial. | 3/3 in each of three trials. |
| Question handling | Correct attention classifications / 12 reviewed entries; count repeated requests for existing answers. | 12/12; zero repeated answered questions. |
| Reader usefulness | Independent assessor scores completeness, organization, qualification visibility, and action clarity from 0–2 each. | No dimension below baseline; factual criteria remain separate. |
| Status latency | `perf_counter` around source status; nearest-rank p95 over 20 warm calls. Record machine and corpus. | Provisional p95 at most five seconds; cold latency reported separately. |
| Processing efficiency | Input tokens / accepted distinct reviewed outcomes. Separate refreshed receipts, reused work, wall time, and active work. | 30% reduction only where redundant baseline work exists and quality passes. |
| Evidence integrity | Hash-valid references / all referenced retained payloads; record newly added bytes and repeated payload bytes separately. | 100% references valid; one canonical copy of each newly reused payload. |
| Engineering traceability | Separate AC-to-assertion, AC-to-implementation, changed-behavior-to-assertion, and current passing-execution fractions. | 100% inventory accounting; no unsupported equivalence or passing claim. |

Zero denominators produce NOT_APPLICABLE or UNKNOWN with a reason. They never produce an automatic 100% score.
Do not combine semantic quality, execution status, publication, and deployment into one opaque percentage.

## Verification and delivery

For each stage, run focused tests for the changed interface and compare preserved command behavior.
At runtime/distribution completion, run the repository-required checks from the standalone source checkout:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
ai-sdlc --workspace PATH validate
```

Replace `PATH` with the selected workspace. Validate the externally initialized workspace as well.
Run installed-workspace and matching offline checks after shared skills change.
Measure native company-environment execution separately. Missing access remains an explicit limit, not an application failure.
Update existing current guides, review the complete staged diff, and commit the verified stage.

## Plan verification and limits

Only the plan and owning task record change during this planning request.
Existing runtime functions, callers, relevant tests, skills, packaging, and guides received source inspection.
Targeted peer feedback identified a missing engineering baseline. The revised plan requires that baseline before engineering improvement percentages.
The [plan document checks](evidence/plan-document-checks.json) verify local links, inventory counts, retained-input hashes, and selected prose limits.
No candidate optimization, business verification, native dispatch, token benchmark, or target-platform pilot ran.
The source inspection fixes implementation targets; Stage 0 must establish measured baselines before performance claims.
The main risks are inconsistent cross-lifecycle captures, incomplete semantic relationships, and unavailable independent review or target environments.
Use explicit partial results and existing recovery controls when those risks occur.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
