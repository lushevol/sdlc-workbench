# Release confidence skill design and validation

The skill provides evidence-based production recommendations for a defined release scope.
It keeps confidence, production recommendations, and human authorization separate.

## Request and scope

Read the [exact user request](user-request.md).
Baseline revision: `7acd8c24a9ee5e03198f6e5149a1d036ecc10c1a`.
The initial worktree had no local changes.
This change maintains the Workbench harness.
It requires no business task or domain knowledge record.

Affected consumers include shared skill discovery, workspace initialization, wheel packaging, and Claude discovery aliases.
The existing runtime discovers canonical skill directories dynamically.
The scaffold copies canonical skills and creates declared aliases.
No runtime symbol or dependency changed.

Qualitative risk: moderate.
An unsupported release recommendation could mislead a production decision.
Missing packaged references could also prevent use in generated workspaces.

## Design decisions

Use qualitative confidence with separate evidence dimensions.
Keep the production recommendation separate from deployment authorization.
Reuse the release-readiness artifact and existing behavior traceability records.
Do not add a score engine, runtime release gate, or deployment operation.
Use scoped numerators and denominators for requirement, assertion, execution, and code coverage.
Preserve blockers, missing evidence, conflicting results, and unknown owners.

The design follows the [principles](../../../PRINCIPLE.md), [architecture](../../../ARCHITECTURE.md), and [workspace design](../../WORKSPACE_DESIGN.md).
The [behavior handoff](../../../.agents/skills/verify-implementation/references/behavior-review.md#report-coverage) forbids a combined assurance score.
The [release template](../../../core/knowledge/templates/sdlc/release-readiness.md) separates readiness from authorization.

## Independent design input

Source: `release_confidence_design` agent message, 2026-10-22.
The agent identified the existing prohibition against one combined coverage score.
It recommended qualitative confidence and a separate production recommendation.
It recommended explicit blocking gaps and reuse of existing release-readiness artifacts.
These recommendations informed the design above.

The completed independent review defined confidence as evidence adequacy.
Strong evidence can support high confidence in a negative release recommendation.
It identified stale runs, mocked boundaries, failure assertions, and unknown artifacts as important validation cases.
It recommended policy-based exceptions and impact-based operational checks.
It rejected universal priority thresholds and automatic waivers for existing defects.
It recommended reassessment when relevant intent, source, tests, artifacts, configuration, or environments change.

## Validation

An independent source review found no actionable decision defect.
Its [retained report](independent-review.json) records inspected hashes and 23 valid Markdown links.
The [workspace tests](integration.json) passed all 20 cases.

The full runtime suite ran 611 tests.
It passed 608 tests and skipped two optional connector integrations.
One mock-registry test could not bind its local server within the sandbox.
Its [targeted rerun](mock-registry-retest.log) passed with local server access.
The [original output](runtime-tests.log) preserves the failed environment check.

The [wheel build](wheel-build.log) passed without network access or new dependencies.
The first installation check compared CLI output without accounting for its added newline.
That temporary assertion failed before comparing packaged file bytes.
The check now accounts for CLI formatting and still compares copied file bytes exactly.
No runtime change was needed.

The [isolated installation check](wheel-install-check.json) passed from the built wheel outside this checkout.
It verified all four skill files, CLI discovery, the Claude alias, and workspace validation.
The generated workspace retained guides and templates without runtime source or project tasks.

The [independent forward evaluation](forward-evaluation.json) assessed four synthetic candidates.
It supported a positive recommendation only within the fully evidenced synthetic scope.
It rejected stale passes and a current mandatory behavior failure.
It preserved an unchanged requirement violation without inventing a waiver.
It reported insufficient evidence when retained execution was unavailable.
All authorization fields remained null.

The [retained inputs](forward-inputs.json) preserve raw fixture source, tests, results, policies, and identities.
The [fixture builder](forward-fixture-builder.py) records their construction procedure.
These fixtures establish no actual business approval or PROD readiness.
The [validation summary](validation-summary.json) separates automated results from the pending writing review.

Validation used macOS with Python 3.14.
Windows and two optional Node connector integrations remain untested.
No implementation blocker remains within this skill creation scope.

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
