# Workbench skill optimization plan

> **Improve existing skill decisions before expanding runtime infrastructure.** Strengthen source accounting, recovery, question handling, and semantic assessment.
> **Add one distinct skill: `evaluate-harness`.** It compares workflow behavior across skill revisions using isolated trials and independent assessment.
> Implementation is under completion audit. Bounded checks passed, but the planned behavioral comparison still needs retained respondent and assessor evidence.

The [requirements table and skill map](07-requirements-and-skills.md) defined the approved scope.
The [maintenance record](01-maintenance.md#completion-audit-continuation-17-november-2026) records the missing evaluation work and current corrections.

## Direction and evidence

Authority: [planning request](01-maintenance.md#planning-follow-up-17-november-2026) and [skills-first clarification](01-maintenance.md#skills-first-clarification-17-november-2026).
Current source inspection includes checkout `d8e4f43e2046eb79b412475a012c62fb105bcb33` and the recorded unrelated local changes.
Recheck revisions and file ownership before implementation.

The intended outcome is fewer interventions between a stated goal and a trustworthy, checkable result.
Optimize decisions and observable behavior. More instructions, files, receipts, or skill invocations are not success measures.
The [retrospective](01-maintenance.md#explicit-preferences) supplies the preference evidence.

Existing skills already require investigation, scoped continuation, checkpoints, claim classification, and evidence-backed handoffs.
Avoid repeating those rules across every entrypoint. Add a decision aid only where a realistic trial exposes its value.
Keep essential routing in `SKILL.md`. Put substantial conditional methods in existing references.

The [saved diagnostic](../workbench-knowledge-raw-import-20261113/evidence/conversion-diagnostic-20261117.md) found two selected draft omissions behind accepted zero-output receipts.
It also distinguishes fresh wiki bindings from complete source conversion.
The [workflow review](../workbench-knowledge-raw-import-20261113/evidence/conversion-diagnostic-20261117-workflow-review.md#questions-and-available-work) reports 310 blank question rows, with overlapping decisions.
These saved findings justify targeted cases. They do not establish a current whole-corpus failure rate.

Preserve the single Python runtime, existing lifecycle controls, independent repositories, and portable shared skills.
Use existing task records, questions, receipts, and review evidence. Add no parallel state store or model service.
No new dependency is planned. Business corrections remain in their owning tasks and authorization scopes.

Implementation role: Workbench maintainer; named owner: unknown.
Assessment role: independent agent or reviewer; record the actual identity and limits for each assessment.
Business review, publication, and deployment owners retain their existing authority.

## Specific work and file ownership

| Priority | Optimization direction and specific change | Files to modify | Expected outcome | Proposed measurement |
| --- | --- | --- | --- | --- |
| 0 | Freeze realistic requests, source expectations, and baseline behavior before changing skills. | Existing evaluation catalogs and this task's evidence. | A defensible before/after comparison. | Seven existing cases plus six targeted cases; all inputs and criteria pinned. |
| 1 | Add `evaluate-harness` for experiment design, isolated trials, independent assessment, and comparison. | New skill, its conditional reference, discovery metadata, alias, and packaging registration. | A reusable owner for evaluating the harness itself. | An independent worker can follow the protocol; every scored result has retained evidence. |
| 2 | Strengthen `ingest-knowledge` source-to-output accounting, especially legitimate versus unsupported `no_change`. | Ingestion entrypoint and existing source-preparation reference. | Selected substantive intent cannot disappear behind a successful receipt. | Both seeded omissions detected; valid redundancy accepted; 24 predicates accounted for. |
| 3 | Tighten `manage-knowledge-lifecycle` reconciliation of disagreeing progress evidence and interrupted work. | Lifecycle entrypoint and existing lifecycle guide. | Accurate status and the next authorized action survive a fresh session. | Zero repeated accepted cases; zero saved answers requested again. |
| 4 | Improve `resolve-knowledge-questions` decision grouping and blocker scope. | Question-resolution entrypoint and existing question guide. | Fewer redundant questions without losing authority or context. | All 12 entries accounted for; zero invalid merges or overwritten answers. |
| 5 | Improve `review-knowledge-claims` and `evaluate-knowledge-retrieval` with source-based completeness and reader trials. | Both entrypoints and the existing evidence worksheet. | Semantic omissions and unsupported sufficiency claims become observable. | 24/24 predicates accounted for; zero unsupported critical claims; no quality regression. |
| 6 | Verify distribution, discovery, and one engineering workflow using the same evaluation discipline. | Existing layout tests and current discovery/setup sections where affected. | Improvements remain usable outside this source checkout. | Correct installed artifacts; all regression criteria pass; target limits stated. |

These are five existing skill owners and one new skill. Conditional changes require observed failures, not blanket rewrites.

## Stage 0 — Establish the behavioral baseline

Direction: Translate historical corrections into reproducible tasks before prescribing additional instructions.

1. Retain the seven existing synthetic cases as engineering, evidence, scope, and readiness regression coverage.
2. Add the six cases below to [tests/skill-evaluation-cases.json](../../tests/skill-evaluation-cases.json).
3. Add source-grounded criteria to [tests/skill-evaluation-rubric.json](../../tests/skill-evaluation-rubric.json).
4. Select eight source documents: two per current collection, including the diagnosed omissions when available.
5. Freeze 24 material predicates and 12 reader questions from their exact revisions. Record conditions, exceptions, and expected uncertainty.
6. Create synthetic equivalents where isolation or privacy requires them. Mark synthetic records and their evidence limits.
7. Use [tests/skill_evaluation.py](../../tests/skill_evaluation.py) with separate skill roots and new external directories.
8. Run baseline screening before editing target skills. Record actual failures, successful existing behavior, cost, and missing observations.

| New case | Evaluated skills | Observable decision |
| --- | --- | --- |
| `lifecycle-accounting` | `manage-knowledge-lifecycle` | Distinguish source coverage, zero-output receipts, wiki freshness, publication, and stale progress prose. |
| `interrupted-handoff` | `manage-knowledge-lifecycle`, `ingest-knowledge` | Reopen accepted work, distinguish an unfinished draft, and perform the next authorized unit. |
| `source-dispositions` | `ingest-knowledge`, `prepare-knowledge-sources` | Reject two substantive omissions while accepting justified unchanged coverage or contextual material. |
| `semantic-preservation` | `review-knowledge-claims`, `maintain-wiki-content` | Preserve numerical qualifications and dated observations in their correct evidence class and location. |
| `decision-grouping` | `resolve-knowledge-questions` | Reuse saved answers and group equivalent decisions without merging different scopes or authorities. |
| `reader-usefulness` | Unchanged `query-knowledge` answering; `evaluate-knowledge-retrieval` review | Review paired drafts, correct supported findings, and check 12 final answers against 24 source predicates. |

All six cases now exist in the executable catalog, alongside the seven engineering cases.
The corrected corpus contains eight synthetic documents across four collections and twenty-four assessor-only predicates.
It retains twelve reader questions, a real unfinished draft, saved answers, and neutral source requests.
The [rejected draft](evidence/rejected-fixture-draft.json) was superseded before respondent execution.
The [baseline manifest](evidence/optimization-baseline.json) records exact catalog and rubric hashes.
Existing [evaluation instructions](../../tests/README.md#evaluate-skill-decisions) already separate respondent inputs from assessor criteria.
The preparer already supports `--skills-root`. No helper code change is currently justified.

Files created during execution: task-scoped `evidence/optimization-baseline.json` and `evidence/optimization-scorecard.json`.
Each manifest links canonical responses, artifacts, assessments, input hashes, and actual settings. Retain each payload once.
Update [tests/README.md](../../tests/README.md#evaluate-skill-decisions) with the additional cases and comparison protocol.

Expected outcome: Known failures and successful counterexamples have explicit, reproducible denominators.
Exit criterion: All 13 cases have frozen inputs and assessor criteria before target-skill changes begin.

## Stage 1 — Add a narrowly scoped evaluation skill

Direction: Make behavioral evaluation reusable across knowledge, engineering, setup, and future skill changes.

1. Create `evaluate-harness` with a precise description for evaluating agent workflows and skill revisions.
2. Accept a bounded task, raw fixture assets, candidate and baseline skills, permitted actions, and evaluation criteria.
3. Keep the respondent blind to the rubric, suspected failure, intended answer, and prior conclusions.
4. Give a separate assessor the raw sources, rubric, observed response, artifacts, and action evidence.
5. Record criterion outcomes as `PASSED`, `FAILED`, or `NOT_ASSESSED`, with exact evidence.
6. Compare quality, scope compliance, recovery, side effects, and effort. Preserve adverse results before changing guidance.
7. Support user-supplied fixtures in generated workspaces. Reuse the source preparer only when its files are available.
8. Forward-test the new protocol through an independent worker on one omission case and one valid no-change counterexample.

New files:

- `.agents/skills/evaluate-harness/SKILL.md`: purpose, discovery boundary, inputs, routing, and completion evidence.
- `.agents/skills/evaluate-harness/references/trials.md`: isolation, paired comparisons, assessor separation, and scorecard fields.
- `.agents/skills/evaluate-harness/agents/openai.yaml`: consistent discovery metadata.
- `.claude/skills/evaluate-harness`: relative discovery alias.

Existing files to modify:

- [scaffold.json](../../scaffold.json): add the alias mapping. Shared skill directories are already included.
- [tests/test_workspace_layout.py](../../tests/test_workspace_layout.py): register the canonical ID and verify installed copies.
- [README.md](../../README.md): add the evaluation skill to existing shared-skill discovery guidance.
- [tests/README.md](../../tests/README.md#evaluate-skill-decisions): document optional source-checkout preparation.

The new skill evaluates repeated workflow decisions and artifacts.
[Retrieval evaluation](../../.agents/skills/evaluate-knowledge-retrieval/SKILL.md) continues to assess individual knowledge answers.
[Implementation verification](../../.agents/skills/verify-implementation/SKILL.md) continues to assess implementation and execution evidence.
[Document validation](../../.agents/skills/validate-sdlc-documents/SKILL.md) retains document-contract checks.

Expected outcome: One discoverable evaluation workflow works with supplied assets and existing tools.
Exit criteria: Both forward trials retain checkable results. Respondent contexts contain no assessor rubric.
No installed instruction requires the omitted source `tests/` directory.
This adds no automatic model runner, semantic grading service, or new approval gate.

## Stage 2 — Strengthen source accounting in ingestion

Direction: Make a zero-output judgment explain selected intent, rather than treating unchanged bytes as sufficient evidence.

1. Before completing a selected source, compare its material clauses with actual canonical sections and unresolved scope.
2. For `no_change`, cite existing coverage or explain why the selected content needs no canonical intent output.
3. Preserve draft intent with its draft status. Unresolved authority can limit publication without erasing supported selected intent.
4. Leave incomplete substantive scope pending. Do not force new records for redundant or contextual sources.
5. Use the existing review note and task evidence for accounting. Keep receipt schemas and lifecycle state unchanged.
6. Replan after accepted work. Count output-linked, justified zero-output, held, missing, and excluded identities separately.

Files to modify:

- [ingest-knowledge/SKILL.md](../../.agents/skills/ingest-knowledge/SKILL.md): add the decision point before `sources complete`.
- [source-preparation.md](../../.agents/skills/ingest-knowledge/references/source-preparation.md#record-canonical-processing-completion): add contrasting no-change examples and required supporting evidence.

Keep source preparation responsible for selection and hash-bound views. Keep canonical coverage decisions with ingestion and claim review.
The [preparation skill](../../.agents/skills/prepare-knowledge-sources/SKILL.md) needs no duplicate canonical-review procedure.

Expected outcome: Unsupported zero-output completion becomes a visible omission; valid unchanged work remains reusable.
Proposed acceptance: Detect both seeded omissions in every repeated trial. Accept the valid no-change counterexample without unnecessary record edits.
Every reviewed predicate has a supported output, a justified no-output disposition, or an explicit unresolved status.
Accounting for an unresolved predicate does not count as completed conversion.

## Stage 3 — Improve lifecycle reconciliation and recovery

Direction: Give the coordinator a compact method for resolving contradictory progress evidence and recovering the next unit.

1. Add an example where wiki receipts are fresh while selected source coverage remains incomplete.
2. Compare identity sets and output evidence before repeating a saved completion claim.
   Keep selected but omitted identities in the requested denominator as pending. Separate explicitly excluded or out-of-scope identities.
3. On interruption, reopen the existing checkpoint, accepted artifacts, saved answers, unfinished draft, and explicit owned paths.
4. Resume the next authorized unit. Keep a held decision local to its affected scope.
5. Distinguish requested worker settings from observed dispatch settings. Keep unknown dispatch identity explicit.
6. Update the existing living record during execution. A status-only request remains read-only.

Files to modify:

- [manage-knowledge-lifecycle/SKILL.md](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md): one reconciliation example and a concise recovery decision aid.
- [docs/KNOWLEDGE_LIFECYCLE.md](../../docs/KNOWLEDGE_LIFECYCLE.md#lifecycle-coordination-and-next-actions): integrate the measured method into current coordination guidance.

Expected outcome: The next useful action follows retained evidence, including after a fresh session starts.
Proposed acceptance: Correctly distinguish every supplied lifecycle dimension in three candidate trials.
Repeat zero accepted cases. Ask for zero saved answers. Preserve unfinished drafts and unrelated edits.
Measure recovery time to the first useful action and to the next accepted checkpoint separately.
Provisional target: median first-action recovery within five minutes on the bounded fixture.

## Stage 4 — Reduce question burden without losing distinctions

Direction: Present distinct consequential decisions, while preserving original questions and answer authority.

1. Investigate each unresolved item using available sources before grouping or asking.
2. Group questions only when the same decision resolves them under matching authority, actor, environment, and version.
3. Keep original IDs, exact answers, source links, affected records, and separate conflicting scopes.
4. Distinguish missing investigation, owner intent, publication review, execution evidence, and deferred work.
5. Present grouped decisions in the existing editable document, with consequence, owner or `unknown`, and next action.
6. Propagate returned answers through existing record updates and reconciliation. Continue independent authorized work.

Files to modify:

- [resolve-knowledge-questions/SKILL.md](../../.agents/skills/resolve-knowledge-questions/SKILL.md): grouping criteria and differing-scope counterexample.
- [docs/QUESTION_RECONCILIATION.md](../../docs/QUESTION_RECONCILIATION.md): explain semantic grouping beside existing reference checks.

Reuse [core/question_reconciliation.py](../../core/question_reconciliation.py). Its reference status does not establish answered intent.
An absent machine Status field does not prove an unanswered question. Unsupported table formats remain an explicit checker limit.

Expected outcome: A smaller, defensible decision queue preserves all original information.
Proposed acceptance: Account for all 12 fixture entries. Permit zero invalid merges, answer overwrites, or repeated answered questions.
Measure unresolved distinct decisions and user review time. Do not report row reduction as question resolution.

## Stage 5 — Evaluate meaning and reader usefulness

Direction: Make semantic review compare source expectations with output, including facts that disappeared during editing.

1. Extend the existing claim worksheet with reverse source-to-output accounting for material changed or omitted predicates.
2. Use that method for omission-prone changes and source-disposition review, rather than every sentence in every task.
3. Use unchanged `query-knowledge` to draft answers for the 12 reader questions. Freeze the same drafts within each paired trial.
4. Use baseline or candidate retrieval-evaluation guidance to review those drafts independently. Permit only supported corrections; retain drafts, reviews, and final answers.
5. Assess final answers against exact sources and applicable versions. Separate factual fidelity from completeness, organization, qualification visibility, and action clarity.
6. Include a detailed unsupported answer and a shorter supported counterexample. Count correct findings, missed omissions, and invented findings separately.
7. Preserve legitimate policy corrections and qualified implementation/test observations in their correct locations.
8. Tighten wiki maintenance only if its targeted trial exposes a decision gap beyond the existing claim-removal controls.

Files to modify:

- [review-knowledge-claims/SKILL.md](../../.agents/skills/review-knowledge-claims/SKILL.md): route omission-prone reviews to the existing worksheet.
- [evidence.md](../../.agents/skills/ingest-knowledge/references/evidence.md#claim-worksheet): add source predicate, destination/disposition, and unresolved-scope fields.
- [evaluate-knowledge-retrieval/SKILL.md](../../.agents/skills/evaluate-knowledge-retrieval/SKILL.md): add repeatable reader-question comparison with factual and usability results separated.
- Conditional: [maintain-wiki-content/SKILL.md](../../.agents/skills/maintain-wiki-content/SKILL.md), only for demonstrated failures after existing guards apply.

Expected outcome: Reviews detect lost meaning even when hashes, schemas, receipts, and prose appearance look satisfactory.
Proposed acceptance: All 24 predicates receive correct dispositions in each repeated reader trial.
Require zero unsupported critical claims, invented approvals, or inferred live execution.
Every claimed completed answer must preserve its applicable conditions. Unresolved predicates remain visible.
No usability dimension may fall below the matched baseline. A factual failure cannot be offset by presentation scores.

## Stage 6 — Validate distribution and an engineering transfer case

Direction: Prove the revised skills remain portable and useful beyond the knowledge pilot.

1. Validate changed skills, references, descriptions, and discovery metadata. Run the skill creator's `quick_validate.py` where available.
2. Use the existing source-distribution, wheel, external-installation, and workspace-initialization checks.
3. Verify the new skill, references, aliases or copy fallback, empty catalogs, and absence of runtime source/project history.
4. Evaluate supplied fixtures using the installed skills root. Do not copy the source test suite into generated workspaces.
5. Regenerate any selected matching-platform offline bundle because shared-skill fingerprints change.
6. Run the seven engineering regression cases against baseline and candidate skill sets.
7. Select one authorized real engineering assessment with exact revisions, consumer contracts, assertions, and retained execution where available.
8. Capture a same-case baseline before claiming engineering efficiency gains. Otherwise, report absolute observations only.
9. Exercise a selected real client/environment when available. Record unavailable clients and environments as untested.

Files:

- [tests/test_workspace_layout.py](../../tests/test_workspace_layout.py): extend existing distribution assertions only where coverage is missing.
- [README.md](../../README.md) and [docs/KNOWLEDGE_LIFECYCLE.md](../../docs/KNOWLEDGE_LIFECYCLE.md): integrate current discovery and workflow changes.
- Conditional: [docs/SETUP.md](../../docs/SETUP.md) and [docs/DEPENDENCIES.md](../../docs/DEPENDENCIES.md), for changed bundle or observed setup instructions.
- The selected engineering task's existing assessment and evidence records; select their paths before execution.

Expected outcome: Installed skill behavior preserves useful engineering decisions and independent checkout ownership.
Proposed acceptance: All existing regression criteria pass; every required installed artifact matches its declared source bytes.
Prohibited generated-workspace artifacts: zero. Unexpected offline acquisition attempts: zero.
Native dispatch counts remain separate from adapter fixture results. Business failures remain failures despite harness evaluation success.

## Quantifiable measurement protocol

Screen all 13 cases once per variant. Preserve quality failures as baseline observations.
Repeat the six targeted cases twice more for both frozen variants when execution remains safe.
The complete scheduled comparison comprises 50 case-level trials and their independent assessments.
The reader workflow produces 72 final answers across three trials and two variants. Drafting and specialized review add agent calls.
Count all drafting, review, correction, and assessment effort. Protocol forward-tests, retries, and real-environment pilots add further cost.
Stop execution that exceeds the trial's permitted actions. Retain the failure and mark unfinished criteria unassessed.
Revise a failed candidate under a new version. Keep earlier adverse results and distinguish reruns from scheduled repetitions.
Report every attempt, variant, and executed denominator. Never select only favorable repetitions.
Unmatched or interrupted comparisons support descriptive results only; do not claim matched medians or percentage gains.

Keep fixture content, execution limits, model, reasoning, concurrency, and assessor criteria comparable across variants.
Record observed settings or `UNKNOWN`. Keep assessors independent of the author and blind to variant labels where practical.
Pin checkout revisions and hash loaded references, scripts, and metadata. The preparer currently hashes selected skill Markdown only.
Fixture Git IDs and absolute paths can differ. Compare source content and normalized contracts, rather than manifest byte equality.
Report individual outcomes and medians. Three trials support a bounded pilot conclusion, not statistical reliability.

| Metric | Calculation | Proposed target |
| --- | --- | --- |
| Behavioral correctness | Passed criteria / all applicable frozen criteria; show failures and unassessed items separately. | All critical criteria pass; no existing regression criterion fails. |
| Source accounting | Correct represented, justified no-output, or explicitly unresolved predicates / 24 reviewed predicates. | 24/24 accounted for; unresolved scope excluded from completed conversion. |
| Seeded omissions | Correctly identified omissions / two known omissions in `source-dispositions`. | 2/2 in each of three candidate trials; valid no-change counterexample also accepted. |
| Semantic fidelity | Unsupported critical claims, lost applicable conditions, and incorrect claim classes per trial. | Zero; presentation quality cannot compensate. |
| Retrieval review accuracy | Correct findings / frozen material draft defects; missed defects and invented findings reported separately. | Detect every critical defect; zero invented defects against the supported counterexample. |
| Question handling | Correct dispositions / 12 frozen entries; invalid merges, overwritten answers, and repeated answered questions. | 12/12; zero destructive or redundant handling. |
| Recovery | Minutes to first useful action; minutes to accepted checkpoint; repeated accepted cases. | First-action median at most five minutes; zero repeated accepted cases. |
| Avoidable supervision | Prompts to repeat saved context, correct progress, or restart accepted work. Exclude new business decisions. | Provisional 50% fewer than matched baseline; report counts when baseline is zero. |
| Reader usefulness | Independent 0–2 scores for completeness, organization, qualification visibility, and action clarity. | No dimension below baseline; factual criteria reported separately. |
| Processing effort | Actual input tokens and active minutes / accepted distinct outcomes of the same type. | Provisional 30% token reduction only where redundant baseline work exists and quality passes. |
| Scope and integrity | Unauthorized side effects; hash-valid references / all retained referenced payloads. | Zero scope violations; 100% valid references; preserve adverse evidence. |
| Portability | Passing installed artifacts and observed client invocations / explicitly selected artifacts and clients. | Complete artifact accounting; unavailable native clients remain untested. |

Zero denominators produce `NOT_APPLICABLE` or `UNKNOWN` with reasons. They never produce an automatic perfect score.
Input bytes are not tokens. Receipt refreshes, unchanged reuse, and new accepted semantic work remain separate measures.
Measure entrypoint bytes and actually loaded context before/after. Reduce duplicated guidance only when behavior and references remain correct.

## Conditional runtime follow-up

The earlier runtime-oriented proposal remains in commit `cd0d56ea2`. Its implementation is deferred behind the skill trials.
A failed agent decision first belongs to the relevant skill. A missing deterministic capability can justify a separate runtime change.

| Demonstrated mechanical gap | Candidate files, only if needed |
| --- | --- |
| Current source state cannot be inspected accurately without durable planning writes. | [core/ingestion/incremental.py](../../core/ingestion/incremental.py), [core/cli.py](../../core/cli.py), and existing ingestion/CLI tests. |
| Explicit bound-session state cannot be inspected for recovery. | [core/hooks.py](../../core/hooks.py), CLI dispatch, and existing hook/interface tests. |
| Existing question output cannot expose required authored fields. | [core/question_reconciliation.py](../../core/question_reconciliation.py) and its existing tests. |
| Correctly supplied dependencies still cause unnecessary repeated processing. | Existing ingestion or wiki invalidation helper and focused regression tests. |

Require a reproducible trigger, affected consumer, and expected result before selecting these changes.
Reuse existing helpers and contracts. Add no scheduler or parallel lifecycle store.

## Verification, delivery, and current limits

Implement one measured change group at a time. Preserve unrelated edits and use one writer for shared catalogs and guides.
Run focused checks for each changed interface. Review descriptions and references as well as frontmatter.
At skill distribution completion, run the repository-required commands from the standalone source checkout:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
ai-sdlc --workspace PATH validate
```

Replace `PATH` with the selected workspace. Validate the externally initialized workspace as well.
Commit each verified stage after explicit staging and staged-diff review. Revise changes that worsen matched outcomes.

Only this task's plan, maintenance record, and document-check evidence change during the current planning request.
Two independent read-only audits checked ownership, portability, denominators, reader responsibilities, and baseline comparability.
Their findings corrected the plan before commitment.
The [plan document checks](evidence/plan-document-checks.json) cover local links, input bindings, counts, and selected prose limits.
The earlier structural examples did not complete the planned behavioral comparison.
The completion audit now runs fifty isolated trials with independent assessment before each next enhancement stage.
The earlier instruction chronology cannot be reconstructed. The retained baseline uses exact pre-enhancement skill bytes for retrospective comparison.
Token savings remain unmeasured when actual usage is unavailable. Synthetic trials establish no business execution or production behavior.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
