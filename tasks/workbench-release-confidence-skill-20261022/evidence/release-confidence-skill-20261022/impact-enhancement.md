# Business and system impact enhancement

The release assessment reports business impact and system impact separately.
Impact determines applicable verification and recovery evidence.
High impact alone does not lower evidence confidence or prohibit a release.

## Scope and source

Read the [exact follow-up request](impact-enhancement-request.md).
The baseline is commit `971964829eaf4966955d5e6ab17c2caa1c85205e`.
The initial worktree was clean.
This work maintains shared skill instructions and their project navigation.
It changes no business policy, runtime, dependency, or artifact schema.

Affected consumers include release-confidence users, assessment reports, shared discovery, and generated workspace instructions.
The [post-change procedure](../../../.agents/skills/impact-analysis/references/post-change-review.md) already separates user impact from system impact.
The [change request template](../../../core/knowledge/templates/sdlc/change-request.md) already retains those assessments.
The skill links these records instead of creating competing impact definitions.

Qualitative risk: moderate.
Confusing impact with evidence confidence could distort production recommendations.
Ignoring interactions between individually tested changes could also conceal a material release risk.

## Independent design input

Source: `impact_design_review` agent message, 2026-10-22.
The agent recommended separate business-impact and system-impact rows with linked source evidence.
It distinguished impact, risk, confidence, recommendation, and authorization.
It recommended stronger relevant verification and recovery scrutiny for consequential effects.
It rejected automatic confidence reductions or release blocks based only on high impact.
It recommended reuse of existing impact records without a new artifact kind.

The completed review also identified exposure, combined release effects, data recovery, detection, rollout containment, and deferral consequences.
It recommended mapping material effects to requirements, canonical cases, required test levels, results, mitigations, and owners.
It noted that monitoring cannot establish a low failure likelihood.
It noted that canaries cannot replace requirement conformance or missing integration evidence.

## Validation

The [skill and link checks](impact-validation.json) passed.
All 30 checked Markdown links and anchors resolve.
The skill metadata and scoped prose checks passed.
CLI discovery returned the current canonical skill.
Workspace validation returned `VALID` without findings.

All 20 [workspace tests](impact-workspace-tests.log) passed.
They cover canonical discovery, workspace copies, packaging boundaries, and forwarding aliases.
This documentation stage changed no runtime, dependency, schema, or packaging configuration.
The full runtime suite and wheel build were not repeated.

The [independent review](impact-independent-review.json) found no actionable instruction defect.
The [three stipulated cases](impact-decision-cases.json) exercised impact-sensitive decision logic.
Complete evidence supported a positive recommendation despite high impact.
Missing combined-release evidence produced an insufficient-evidence result.
A demonstrated integrity failure prevented a positive recommendation despite urgency and alerting.
All deployment authorization fields remained null.

These cases do not verify source authenticity, business execution, or actual PROD readiness.
The writing review remains pending.
No implementation blocker remains within this enhancement scope.

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
