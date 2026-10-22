---
name: release-confidence
description: Assess whether defined code changes are suitable for PROD using code review, requirement conformance, assertion coverage, retained tests, and deployment evidence. Use for release confidence and go/no-go advice; keep recommendations separate from human authorization.
---

# Assess release confidence

Judge a defined release candidate against its applicable production conditions.
Explain confidence through evidence quality and explicit limits.
Keep the production recommendation separate from deployment authorization.
This skill provides an agent procedure. It adds no runtime release gate.

## Establish scope and authority

Read the owning project guides and preserve the user's exact request before investigation or delegation.
Select the release scope from the request, task records, registry, and retained release evidence.
Read existing reports before asking for information already available.
Keep business requirements, observed behavior, knowledge review, test results, and approval records separate.

For business changes, use the existing task's intake, evidence index, and current stage record.
Reconcile the [current task view](../analyze-requirement/references/current-task-view.md) before reusing conclusions.
Require `READY` for the named assessment phase before a downstream recommendation.
`READY_WITH_LIMITS` permits further intake evidence collection only.
`NEEDS_CLARIFICATION` blocks the next phase.
Keep a provisional evidence report when the intake gate remains unresolved.
Use [analyze-requirement](../analyze-requirement/SKILL.md) for missing intake and material intent clarification.
Preserve completed intake bytes and use current stage records for later decisions.

Harness maintenance needs no business task or domain knowledge record.
Assess its actual change contract and checks directly under the [scope rules](../../../tasks/README.md#scope).
For mixed releases, retain the business scope in its owning task.

Record these identities before interpreting passing results:

- Release ID, included changes, active behavior versions, exclusions, and assessment time.
- Repository IDs, full base and candidate commits, comparison mode, and relevant local content hashes.
- Build IDs, immutable artifact digests, build provenance, and deployment/configuration identities when available.
- Test revisions, inputs, environment, execution mode, run time, and retained result identities.
- Target PROD environment, known deployed baseline, affected services, contracts, and consumers.
- Release policy source/version, applicable conditions, responsible owners, and recorded exception authority.

Separate a source-only assessment from a deployable artifact assessment.
Unknown build provenance or target configuration limits production claims.
Follow [deployment comparison](../verify-implementation/references/deployment-comparison.md) for environment-dependent conclusions.
Do not infer deployed bytes from a checkout, branch name, or PR status.

## Assemble the evidence

Read the [decision model](references/decision-model.md) before choosing confidence or a recommendation.
Use the [report guidance](references/reporting.md) to retain a reviewable assessment.
Scale evidence collection to change impact and applicable release conditions.
Do not require unrelated checks merely because a tool exists.

| Evidence dimension | Procedure and required inspection |
| --- | --- |
| Code review | Use [code-review](../code-review/SKILL.md). Check comparison identity, inspected files, exclusions, findings, and resolution evidence. |
| Intent and conformance | Read exact requirements and latest clarifications. Reuse [behavior mappings](../verify-implementation/references/behavior-review.md#keep-one-evidence-handoff). |
| Change and regression impact | Use [impact-analysis](../impact-analysis/SKILL.md). Inspect callers, unchanged affected paths, contracts, data, configuration, and cross-repository effects. |
| Assertion coverage | Use [verify-implementation](../verify-implementation/SKILL.md). Inspect setup, helpers, invocation, predicates, mocks, and required test levels. |
| Execution results | Bind actual retained outcomes to candidate bytes, assertions, inputs, environment, and configuration. Keep failures and unavailable checks visible. |
| Deployment and recovery | Inspect applicable deployment order, compatibility, migration, recovery, monitoring, and operator evidence. |
| Residual risk and decisions | Record consequence, exposure, mitigation, owner, actual disposition, authority, scope, and expiry when supplied. |

Use [gherkin-quality](../gherkin-quality/SKILL.md) when UI scenario quality or framework bindings require inspection.
Use [detect-gaps](../detect-gaps/SKILL.md) when material mappings or definitions remain unresolved.
Use static graphs for discovery after checking freshness and coverage. Missing graph edges do not establish no impact.
Inspect exact source before confirming consequential dependency claims.

Treat Release Clinic reports as supplementary evidence with their own scope, identities, versions, and limits.
Use [release-clinic](../release-clinic/SKILL.md) when collecting or producing those reports.
A TDA verdict, quality gate, or pipeline success does not establish complete business verification.

Reuse current, inspectable evidence before running more checks.
For connectors, use Workbench `status`, resource `list`, and granted `call` operations.
Read schemas and exact grants before invocation. Follow the [connector guide](../../../docs/CONNECTORS.md).
Keep credentials in the workspace root `.env`, outside reports and call arguments.
An assessment does not authorize PROD tests, deployments, external writes, or messages.
Follow existing task authorization for appropriate local validation and permitted test environments.

## Judge and retain

Report each applicable dimension separately with evidence, status, limits, and findings.
Calculate coverage only from explicit inventories under the [coverage rules](references/decision-model.md#coverage-with-declared-denominators).
Do not average review, intent, assertion coverage, execution, and operational evidence into one score.
Do not invent a success probability or numeric release threshold.

Choose `HIGH`, `MODERATE`, `LOW`, or `UNDETERMINED` evidence confidence for the stated recommendation.
Choose `RECOMMEND`, `DO_NOT_RECOMMEND`, or `INSUFFICIENT_EVIDENCE` separately.
Strong evidence can support `HIGH` confidence in `DO_NOT_RECOMMEND`.
One consequential failure can control the recommendation despite many passing cases.
State the evidence that would change the judgment and the responsible owner.

Save findings and completed case evidence immediately under the owning task's evidence rules.
Keep one canonical case definition with measurable Gherkin and explicit assertions.
Link intended, old, and new results separately for requirement or regression gaps.
Preserve failed, stale, contradictory, and interrupted results with their limits.
Retain the original evidence. Save a successor assessment when relevant inputs change.

Before completion, recheck candidate identity and material evidence freshness.
Report the recommendation, confidence rationale, blocking actions, residual risks, and actual authorization state first.
Keep unknown owners explicit. Keep required human decisions pending until recorded evidence exists.

Use this skill on demand.
Scheduling, source changes, deployment, approval publication, and external communication require their own authorized scope.
