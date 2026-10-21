---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Setup readiness and deployment evidence skills

**This stage completes the remaining setup readiness and deployment evidence improvements through existing skills.**
The earlier [task-status and behavior-comparison stage](skill-workflow-enhancement.md) completed the other three improvements.
This stage adds no runtime, dependency, business policy, or deployment change.

## Scope and consumers

This work maintains the Workbench harness. It requires no business task or domain knowledge record.
Qualitative risk is low. Agent decisions and shipped guidance are the affected interfaces.
Source inspection covered existing doctor, CLI, setup, packaging, Robot, browser, and connector responsibilities.

| Consumer | Improvement and observable benefit |
| --- | --- |
| [Repository onboarding](../../.agents/skills/repository-onboarding/SKILL.md) and [connectors](../../.agents/skills/connectors/SKILL.md) | Share one [setup readiness view](../../.agents/skills/repository-onboarding/references/setup-readiness.md). Identify the required runner, missing boundaries, and next usable operation. |
| [Implementation verification](../../.agents/skills/verify-implementation/SKILL.md) and [browser investigations](../../.agents/skills/verify-implementation/references/browser-investigation.md) | Use the [deployment comparison](../../.agents/skills/verify-implementation/references/deployment-comparison.md). Bind environment claims to effective settings and running components. |
| Skill maintainers | Reuse the expanded [case catalog](../../tests/skill-evaluation-cases.json), [rubric](../../tests/skill-evaluation-rubric.json), and [evaluation procedure](../../tests/README.md#evaluate-skill-decisions). |

The readiness procedure preserves static onboarding and existing execution authorization.
It separates package presence, launch evidence, application routing, and selected-suite assertions.
Optional integration gaps cannot block unrelated operations. Required gaps retain their blocked action, owner, and next action.
Robot Browser execution remains separate from Playwright investigation smoke checks.
Offline bundles require matching target conditions. Package availability does not establish endpoint access or native Windows readiness.

The deployment comparison reuses the existing timing worksheet.
It distinguishes defaults, effective overrides, observed issued values, and unknown configuration sources.
It binds the actual host, embedded application, services, clocks, transformations, and assertion results.
Local evidence remains useful within its scope. Unknown UAT settings cannot acquire a local passing claim.
Technical verification, business approval, and knowledge publication retain separate meanings.

## Independent evaluation

Two independent agents completed the new requests without the assessor rubric.
The coordinating agent inspected their responses, source bindings, and integrity checks.
Both exercises passed all 12 assessed criteria.
The [retained evaluation bundle](setup-deployment-skill-evaluation.json) preserves original responses, raw inputs, checks, and individual assessments.

| Exercise | Assessed result |
| --- | --- |
| Setup readiness | Preserved aggregate INCOMPLETE and usable core prerequisites. Identified Robot assets and BFF blockers. Rejected incompatible Windows bundle evidence. |
| Deployment comparison | Rejected UAT acceptance. Separated local override, UAT sample, wrong embedded application, unknown artifacts, clocks, and missing Extend assertions. |

Both fixture repositories retained their candidate revision, branch, clean index, and original input hashes.
Neither agent installed dependencies, launched applications, ran business tests, or accessed external services.
The catalog now contains seven cases. The earlier stage assessed five cases against its separately recorded skill hashes.
The earlier cases were not rerun during this stage. Automatic skill selection was not evaluated.

## Validation and limits

| Check | Result |
| --- | --- |
| Skill frontmatter and scaffold validation | PASSED for three changed entrypoints. |
| Runtime suite | PASSED; 562 tests ran, with two optional skips. |
| Source workspace diagnostics | Core doctor READY. Workspace validation VALID. External integration access remains UNTESTED. |
| Wheel and external initialization | PASSED. All six changed skill files matched generated files. Three skills and aliases remained discoverable. |
| Installed-skill fixture preparation | PASSED using the externally initialized workspace. |
| Source distribution | PASSED. Seven evaluation cases and both new references were included. |
| Links and report checks | PASSED for local targets, heading anchors, retained hashes, metadata, and whitespace. |

The wheel check used an isolated package installation with the existing interpreter dependencies.
It did not repeat connected dependency downloads or native platform installation.
The procedures changed no dependency installation path.
Native Windows, actual Robot business execution, and live UAT verification remain untested by this stage.
The synthetic exercises establish no business behavior or general model reliability.
No comparison against previous skill instructions was executed.

Owner: Workbench maintainer. The named owner is unknown.
Next action: rerun affected evaluations after procedure changes. Keep real target evidence within its authorized business investigation.
ASD writing review remains pending.
