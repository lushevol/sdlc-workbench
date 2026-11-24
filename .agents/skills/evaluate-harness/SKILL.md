---
name: evaluate-harness
description: Compare baseline and candidate agent workflows with isolated fixtures, independent assessment, and retained evidence.
---

# Evaluate an agent workflow

Use this skill when a shared skill, prompt, adapter, or workflow changes and the useful question is whether the agent now makes better decisions.
This is an evaluation protocol. It does not run a model, approve a business result, publish knowledge, or authorize deployment.

## Prepare the trial

1. Define one bounded task, its permitted actions, the expected decision predicates, and the limits.
2. Pin the baseline and candidate skill roots, fixture bytes, source revisions, model settings, and assessor criteria.
3. Prepare a new isolated trial directory. Use the repository's `tests/skill_evaluation.py` fixture preparer when it is available; otherwise retain an equivalent input manifest.
4. Verify every bound input is readable and matches its pinned hash before dispatch.
5. Give the respondent only the task, fixture, selected skills, and permitted actions. Keep the rubric, suspected defect, variant label, and prior result outside its context.
6. Save the respondent's answer, changed files, command outputs, and actual settings before assessment.

If a read-only input disappears or changes, preserve the attempt.
Restore pinned bytes in the isolated trial copy before further dispatch.
Record any availability limit for an answer produced before recovery.

Use synthetic fixtures when isolation or privacy requires them. Mark them as synthetic and do not treat them as business or production evidence.

## Assess the result

An independent assessor receives the raw fixture, pinned expectations, respondent output, artifacts, and action evidence.
Recheck read-only inputs before assessment. Retain authorized edits with their original and resulting hashes.
For every criterion record `PASSED`, `FAILED`, or `NOT_ASSESSED`, with an exact evidence locator and material limit.
Compare baseline and candidate on the same fixture and permitted action set.

Score these dimensions separately:

| Dimension | Record |
| --- | --- |
| Correctness | Expected predicates satisfied; missed and invented findings counted separately. |
| Scope and safety | Unauthorized edits, external calls, publication, or approval claims. |
| Evidence | Exact source, revision, assertion, and environment bindings. |
| Recovery | Saved answers, accepted artifacts, unfinished work, and next authorized unit. |
| Effort | Actual prompts, active minutes, input tokens, and repeated work. |
| Usefulness | Completeness, organization, visible qualifications, and action clarity. |

Never let presentation or effort compensate for a factual or scope failure.
Preserve adverse results and rerun evidence. A revised candidate receives a new variant or revision; do not overwrite the failed comparison.

## Complete the trial

Return a scorecard with the fixture and skill hashes, variant, settings, criteria, outcomes, evidence links, limits, and next action.
Use the [trial manifest fields](references/trials.md) when retaining a paired comparison.
Report denominators and zero-denominator reasons. Separate tool completion, semantic review, business verification, and human authorization.
State when the assessor was not independent or when a requested client, model, or environment was unavailable.

Passing a trial supports only the stated fixture and scope. It does not establish general model reliability, production behavior, or business acceptance.
