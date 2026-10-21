---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Task status and behavior comparison skills

**Existing skills now reconcile current evidence and distinguish introduced failures from inherited behavior.**
Five independent synthetic trials satisfied 21 assessed criteria.
The [retained evidence](skill-workflow-evaluation.json) contains prompts, outputs, source identities, execution records, and individual assessments.
No comparison with the previous skill version was executed.
These results establish neither general model reliability nor business verification.

## Scope and responsibility

This change maintains the Workbench harness. It requires no business task or domain knowledge record.
Current consumers are agents answering task-status questions and reviewing changes.
Qualitative risk is low. Changes affect procedures, review templates, and isolated evaluation resources.
No runtime command, model service, dependency, business source, or schema changed.

| Consumer | Change and observable benefit |
| --- | --- |
| [Requirement intake](../../.agents/skills/analyze-requirement/SKILL.md) and [implementation verification](../../.agents/skills/verify-implementation/SKILL.md) | Share one [current task view](../../.agents/skills/analyze-requirement/references/current-task-view.md). Reuse existing intake or stage summaries. |
| [Code review](../../.agents/skills/code-review/SKILL.md) and [impact analysis](../../.agents/skills/impact-analysis/SKILL.md) | Share the [behavior comparison](../../.agents/skills/verify-implementation/references/behavior-review.md#compare-old-and-new-behavior). Keep intended, old, and new results together. |
| Skill maintainers | Reuse five [evaluation cases](../../tests/skill-evaluation-cases.json) and the separate [assessor rubric](../../tests/skill-evaluation-rubric.json). Follow the [evaluation procedure](../../tests/README.md#evaluate-skill-decisions). |

The current view preserves completed intake and historical results.
It links definitions, assertions, and execution separately. It identifies stale evidence, blockers, owners, and next actions.
The comparison uses exact endpoints and equivalent cases. It labels observations, source predictions, and unknown results.
Passing assertions that expect an undesired outcome cannot establish requirement satisfaction.
Ordinary code reviews remain within their requested scope.

## Independent evaluation

Three independent agents received prepared inputs and the selected skills.
They did not receive the assessor rubric. The coordinating agent inspected their outputs and supporting evidence.
The [preparer](../../tests/skill_evaluation.py) creates synthetic local repositories and records source hashes.
It calls no model or business test runner. It refuses existing output directories.

| Case | Assessed outcome |
| --- | --- |
| `known-policy` | Reused recorded intent without repeating the resolved policy question. Preserved candidate review status and completed intake. |
| `current-results` | Reported zero current passes. Kept the earlier pass historical and linked definitions, scripts, results, and blockers. |
| `regression-comparison` | Identified pending logout as introduced. Classified rejected-renewal logout as an unchanged failure through paired observations. |
| `failure-assertion` | Rejected a passing logout assertion as proof of required retry behavior. |
| `review-scope` | Completed the review without fixes, new tests, business tasks, or external calls. |

All input source, canonical definitions, completed intake, and retained execution bytes remained unchanged.
Only authorized stage summaries changed. Review repositories retained their selected branch, candidate, and clean index state.
Full original report content and execution output remain embedded in the [evidence bundle](skill-workflow-evaluation.json).
Historical temporary paths remain source locators. Embedded content and SHA-256 values preserve their evidence.

## Validation and limits

| Check | Result |
| --- | --- |
| Skill frontmatter and scaffold validation | PASSED for four changed entrypoints. |
| Skill and test-guide links | PASSED; 90 local links and anchors before this report. |
| Runtime suite | PASSED; 562 tests ran, with two optional skips. |
| Initial sandbox execution | One existing HTTP fixture could not bind localhost. The unrestricted rerun passed. |
| Wheel and external initialization | PASSED; all nine changed skill assets were byte-identical. Four skills and their aliases remained discoverable. |
| Source distribution | PASSED; the evaluation preparer and both JSON resources were included. |
| Fixture preparation | PASSED for all five cases. Reusing an existing output directory was rejected. |

The [execution evidence](skill-workflow-evaluation.json) preserves the failed attempt, successful rerun, and installation results.
The trials used local Python 3.14.5 on macOS. Native Windows and live deployment behavior remain untested.
The fixture lacked an installed Workbench CLI. Agents disclosed that limit and completed authorized source inspection.
The separately installed wheel passed workspace validation.

Owner: Workbench maintainer. The named owner is unknown.
Next action: rerun the affected cases when these procedures change. Retain failures before revising the guidance.
ASD writing review remains pending.
